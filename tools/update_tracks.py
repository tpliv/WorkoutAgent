#!/usr/bin/env python3
"""Apply the progression rules to the logged history and update data/tracks.json.

Usage:
    python3 tools/update_tracks.py --dry-run             # show what would change
    python3 tools/update_tracks.py                       # update tracks.json and data/track-log.md
    python3 tools/update_tracks.py --write-md            # also refresh the table in data/track-state.md
    python3 tools/update_tracks.py --reset-on-stall      # apply the 7.5% reset when a stall fires
    python3 tools/update_tracks.py --since 2026-11-01    # only sessions on or after this date

Reads data/history.csv (one row per set; tools/README.md) and, for every
session logged after each track's last processed exposure:

  Heavy (H) exposure, top-set lifts (templates/progression-tracks.md, section 5):
    the top set is the heaviest working set of the lift in an H-slot session.
    The decision reads the effective RPE at the rep target (4):
      rated:   logged RPE - (reps - target)        (6 @ 8 reads 6; 5 @ 10 reads 9)
      unrated: reps == target -> 8 (flagged, counted toward a rep-out)
               reps >  target -> 9 - (reps - target)   (assumes the set ended at RPE 9)
    effective <= 5              -> re-anchor: e1RM / 1.2 rounded down, at least
                                   the big step, at most +10% of the load lifted
    effective <= 7              -> +big increment (10 lb squat and deadlift,
                                   5 lb bench and press), miss counter 0
    effective 7.5-8             -> +increment (5 lb), miss counter 0. Bench and
                                   press (increment_every = 2): +5 lb on every
                                   second such result, counted in step_counter
                                   (no fractional plates)
    effective 8.5-9             -> hold
    effective 9.5-10            -> hold, miss +1 (merged session, lift not first: hold only)
    fewer than 4 reps           -> hold, miss +1
    Regain phase (section 5.1, track["regain"] while active): increment_every
      is 1, any step is capped at regain.max_step_lb, and the phase ends at the
      exit e1RM, the first top set reading 8.5+ (or a miss), or regain.until.
    Caution (section 5.2, track["caution"] while active): the big step needs a
      logged RPE and is never taken at two H exposures in a row; steps capped.
    Calibration rep-out (section 5.3): after two unrated top sets of exactly 4
      in a row, rep_out_due is set. A last back-off above the rep target is read
      as a rep-out: 8+ reps -> big step for an unrated top set, 5-7 -> normal;
      when one was due, 3 or fewer -> hold (not a miss), exactly 4 -> not done.
    The new planned load is computed from the load actually lifted, so a
    work-up or a heavier-than-planned set moves the track with it.
  Heavy exposure, row and pull-up (double progression):
    every set reached the top of the range at RPE <= 8 -> +5 lb, counter 0
    regain phase: every set at the top at a logged RPE <= 7, or the first set
      at 11+ reps -> +regain.big_increment_lb (10)
    first set below the bottom of the range             -> hold, miss +1
    otherwise                                           -> hold
  Stall (section 6): two consecutive misses at the same load. Flagged; the load
    is held unless --reset-on-stall is given, which applies the 7.5% reset
    (5% for row and pull-up) and counts the stall.
  Volume (V) exposures and sessions without a slot in the title never change a
    track load; they update the last-exposure date for the gap clock (section 8).
  Busy gym (section 9; guide/03 section 4.3, "Station taken"):
    Row and pull-up variants: when the main exercise is absent and a variant
      from lift_aliases.json "_variants" is logged, the variant is the exposure.
      It runs its own double progression in track["variants"][name] (no regain
      phase, no e1RM entry) and sets the track's last exposure.
    Squat, bench, deadlift, press: a heavy slot logged without the barbell lift
      sets track["h_owed"]; the next V exposure whose heaviest set is within 3%
      of the planned top set is read as the heavy exposure (judged by RPE: 9.5
      is a hold, not a miss) and clears it, as does any barbell H. A substitute
      from "_substitutes" in an H or V slot is recorded in
      track["last_sub_exposure"]; it never changes the track load
      (hevy_push_routines.py uses it to cap the gap modifier at a hold).
  e1RM from the top set: load x (1 + (reps + (10 - RPE)) / 30); unrated sets use
    RIR 2 at the rep target and RIR 1 above it; the last 6 kept.
  Pointer: the half-session owed after the latest slot-titled session
    (split +1, merged +2).

Slots are read from the workout title: L1, U1, L2, U2, L3, U3, Full A, Full B,
Full C (case-insensitive prefix, so Hevy routines titled 'L1 Lower A' work).
A lower-upper pair anywhere in the title ('U3 + L1 (merged)', 'Race Week 2 -
Wed (U3 + L1)') is a merged session of those two halves: a lift is H or V by
either half, and the pointer moves past the second.
Lifts are matched to exercise names through tools/lift_aliases.json.

Units: tracks.json is in pounds. history.csv keeps weight_kg exactly as the
Hevy API returns it; loads are converted to pounds (to 0.1 lb) on read.
"""
import argparse
import csv
import datetime as dt
import json
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY = os.path.join(ROOT, "data", "history.csv")
TRACKS = os.path.join(ROOT, "data", "tracks.json")
ALIASES = os.path.join(ROOT, "tools", "lift_aliases.json")
ROTATION = os.path.join(ROOT, "templates", "rotation.json")
TRACK_LOG = os.path.join(ROOT, "data", "track-log.md")
TRACK_MD = os.path.join(ROOT, "data", "track-state.md")

SLOT_RE = re.compile(r"^\s*(L[123]|U[123]|FULL\s*[ABC])\b", re.I)
MD_BEGIN, MD_END = "<!-- tracks:begin -->", "<!-- tracks:end -->"
LB_KG = 0.45359237


# ----- helpers ----------------------------------------------------------------

def norm(s):
    return re.sub(r"\s+", " ", (s or "").strip().lower())


PAIR_RE = re.compile(r"\b([LU][123])\s*\+\s*([LU][123])\b", re.I)
CANONICAL_MERGES = {("L1", "U1"): "Full A", ("L2", "U2"): "Full B", ("L3", "U3"): "Full C"}


def parse_slot(title):
    """Slot from a workout title. A pair anywhere in the title ("U3 + L1
    (merged)", "Race Week 2 - Wed (U3 + L1)") is a merged session of those two
    half-sessions; the three canonical pairs read as Full A, B, C. Otherwise the
    title must start with a slot."""
    p = PAIR_RE.search(title or "")
    if p:
        a, b = p.group(1).upper(), p.group(2).upper()
        if a[0] != b[0]:
            return CANONICAL_MERGES.get((a, b)) or f"{a}+{b}"
    m = SLOT_RE.match(title or "")
    if not m:
        return None
    s = m.group(1).upper().replace(" ", "")
    return f"Full {s[-1]}" if s.startswith("FULL") else s


def is_merged(slot):
    return bool(slot) and (slot.startswith("Full") or "+" in slot)


def halves(slot, rotation):
    """The half-sessions a slot covers, in the order trained."""
    if slot.startswith("Full"):
        return rotation["merged"][slot]
    return slot.split("+")


def round_to(x, step):
    """Nearest multiple of step, halves up."""
    return round(math.floor(x / step + 0.5) * step, 2)


def floor_to(x, step):
    return round(math.floor(x / step + 1e-9) * step, 2)


def e1rm(load, reps, rpe, target=None):
    """Epley-style e1RM. Unrated: RIR 2 at or below the rep target, RIR 1 above
    it (the set is assumed to have ended at RPE 9; progression-tracks.md §5)."""
    if rpe is not None:
        rir = 10 - rpe
    else:
        rir = 1 if (target is not None and reps > target) else 2
    return round(load * (1 + (reps + rir) / 30), 1)


def effective_rpe(reps, rpe, target):
    """RPE at the rep target (§5). Returns (effective, how)."""
    if rpe is not None:
        return rpe - (reps - target), "rated"
    if reps <= target:
        return 8.0, "unrated"
    return 9.0 - (reps - target), "unrated-over"


def active(block, date):
    """A regain or caution block applies on `date` if it has not ended."""
    return bool(block) and not block.get("ended") and date <= block.get("until", "9999-12-31")


def kg_to_lb(kg):
    """Logged kg -> lb to 0.1 lb (the API's kg carry 2-6 decimals, so a 135-lb
    set comes back as 135.0)."""
    return None if kg is None else round(kg / LB_KG, 1)


def fmt(x):
    return f"{x:g}"


def fnum(x):
    try:
        return float(x) if x not in (None, "") else None
    except ValueError:
        return None


def matcher(aliases):
    """lift -> function(exercise name) -> bool, using tools/lift_aliases.json."""
    ex = aliases.get("_exclude", {})
    fns = {}
    for lift, names in aliases.items():
        if lift.startswith("_"):
            continue
        fns[lift] = name_matcher(names, ex.get(lift, []))
    return fns


def name_matcher(names, exclude=()):
    subs = [norm(n) for n in names]
    bad = [norm(b) for b in exclude]
    return lambda name: any(s in norm(name) for s in subs) and not any(b in norm(name) for b in bad)


def variant_matchers(aliases):
    """lift -> [(variant name, matcher)] in the order listed in "_variants"."""
    return {lift: [(v, name_matcher(names)) for v, names in vs.items()]
            for lift, vs in (aliases.get("_variants") or {}).items()}


def substitute_matchers(aliases):
    """lift -> matcher for the substitutes listed in "_substitutes"."""
    return {lift: name_matcher(spec.get("match", []), spec.get("exclude", []))
            for lift, spec in (aliases.get("_substitutes") or {}).items()}


VARIANT_KEYS = ("top_set_lb", "last_h_load_lb", "miss_counter", "stalls")


def load_sessions(path, since=None):
    """Group history rows into sessions: {(date, title): [rows]} ordered by date."""
    sessions = {}
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            d = (r.get("date") or "")[:10]
            if not d or (since and d < since):
                continue
            key = (d, r.get("workout_title") or "", r.get("workout_id") or "")
            r["_w"] = kg_to_lb(fnum(r.get("weight_kg")))
            r["_reps"] = fnum(r.get("reps"))
            r["_rpe"] = fnum(r.get("rpe"))
            r["_type"] = (r.get("set_type") or "normal").lower()
            sessions.setdefault(key, []).append(r)
    return [(k, sessions[k]) for k in sorted(sessions)]


def working_sets(rows):
    out = [r for r in rows if r["_type"] in ("normal", "failure", "dropset") and r["_reps"] and r["_reps"] > 0]
    out.sort(key=lambda r: fnum(r.get("set_index")) or 0)
    return out


# ----- rules ------------------------------------------------------------------

def apply_top_set_rule(track, top, merged_not_first, flags, date="", backoff_reps=None):
    """Section 5 with 5.1-5.3. `top` = the top set row; `backoff_reps` = reps of
    the last back-off set after it (None if none). Mutates track; returns a
    decision string."""
    load, reps, rpe = top["_w"], int(top["_reps"]), top["_rpe"]
    target = track.get("rep_target", 4)
    inc, big = track.get("increment_lb", 5), track.get("big_increment_lb", 10)
    step = track.get("round_step_lb", 5)
    every = track.get("increment_every", 1)
    regain = track.get("regain") if active(track.get("regain"), date) else None
    caution = track.get("caution") if active(track.get("caution"), date) else None
    if regain:
        every = 1
    caps = [b.get("max_step_lb") for b in (regain, caution) if b and b.get("max_step_lb")]
    cap = min(caps) if caps else None

    eff, how = effective_rpe(reps, rpe, target)
    notes = []
    if how == "unrated":
        flags.append(f"no RPE logged on the {track['name']} top set ({fmt(load)} x {reps}); treated as RPE 8")
    elif how == "unrated-over":
        flags.append(f"no RPE logged on the {track['name']} top set ({fmt(load)} x {reps}); assumed it ended at RPE 9, so {fmt(eff)} at rep {target}")
    elif reps != target:
        notes.append(f"{reps} @ {fmt(rpe)} reads {fmt(eff)} at rep {target}")

    # calibration rep-out (5.3): the last back-off above the target, or any back-off when one was due
    due = track.get("rep_out_due", False)
    rep_out = None
    if backoff_reps is not None and reps >= target and (backoff_reps > target or (due and backoff_reps < target)):
        rep_out = backoff_reps
    if rep_out is not None:
        if how == "unrated":
            if rep_out >= 8:
                eff = 7.0
            elif rep_out < target:
                eff = 9.0
            notes.append(f"rep-out {rep_out} on the last back-off reads the top set as {fmt(eff)}")
        else:
            expected = 5.7 + (8 - eff)
            if abs(rep_out - expected) >= 2:
                drift = "harder" if rep_out > expected else "easier"
                flags.append(f"{track['name']}: rep-out {rep_out} vs about {expected:.0f} expected for the rating; the rating may run {drift} than the set was")
            notes.append(f"rep-out {rep_out}")
        track["unrated_streak"] = 0
        track["rep_out_due"] = False
    elif "unrated_streak" in track or how == "unrated":
        if how == "unrated" and reps == target:
            track["unrated_streak"] = track.get("unrated_streak", 0) + 1
            if due and backoff_reps == target:
                flags.append(f"{track['name']}: rep-out was due; last back-off logged at {target}, read as not done")
        else:
            track["unrated_streak"] = 0
        track["rep_out_due"] = track["unrated_streak"] >= 2
        if track["rep_out_due"] and not due:
            flags.append(f"{track['name']}: two unrated top sets of {target} in a row; next H gets a rep-out on the last back-off (section 5.3)")

    def capped(new):
        if cap is not None and new > load + cap:
            return round_to(load + cap, step), f" (capped at +{fmt(cap)})"
        return new, ""

    prev_load = track.get("last_h_load_lb")
    track["last_h_load_lb"] = load
    if reps < target:
        decision = f"miss ({reps} reps < {target}); hold {fmt(load)}"
        track["top_set_lb"] = load
        track["miss_counter"] = track.get("miss_counter", 0) + 1
        step_kind = "miss"
    elif eff <= 7:
        if eff <= 5:
            anchor = floor_to(e1rm(load, reps, rpe, target) / 1.2, step)
            new, label = max(load + big, min(anchor, floor_to(load * 1.1, step))), "re-anchor"
        else:
            new, label = load + big, "big step"
        blocked = None
        if caution and caution.get("big_step_needs_rating") and rpe is None:
            blocked = "no logged RPE"
        elif caution and caution.get("no_consecutive_big_steps") and track.get("last_step") == "big":
            blocked = "big step last time"
        if blocked:
            new, label, step_kind = load + inc, f"caution ({blocked}), +{fmt(inc)}", "step"
        else:
            step_kind = "big"
        new, capnote = capped(round_to(new, step))
        track["top_set_lb"] = new
        track["miss_counter"] = 0
        if every > 1 or "step_counter" in track:
            track["step_counter"] = 0
        decision = f"{reps} @ {fmt(eff)}: {label} to {fmt(new)}{capnote}"
    elif eff <= 8:
        track["miss_counter"] = 0
        n = track.get("step_counter", 0) + 1
        if n >= every:
            new, _ = capped(round_to(load + inc, step))
            track["top_set_lb"] = new
            if every > 1 or "step_counter" in track:
                track["step_counter"] = 0
            decision = f"{reps} @ {fmt(eff)}: +{fmt(inc)} to {fmt(new)}" + (" (regain: every success)" if regain and track.get("increment_every", 1) > 1 else "")
            step_kind = "step"
        else:
            track["top_set_lb"] = load
            track["step_counter"] = n
            decision = f"{reps} @ {fmt(eff)}: success {n} of {every}; hold {fmt(load)}, +{fmt(inc)} after the next one"
            step_kind = "hold"
    elif eff <= 9:
        track["top_set_lb"] = load
        decision = f"{reps} @ {fmt(eff)}: hold {fmt(load)}"
        step_kind = "hold"
    else:
        track["top_set_lb"] = load
        step_kind = "hold"
        if merged_not_first:
            decision = f"{reps} @ {fmt(eff)} in a merged session, not first lift: hold {fmt(load)} (no miss)"
        else:
            track["miss_counter"] = track.get("miss_counter", 0) + 1
            decision = f"{reps} @ {fmt(eff)}: hold {fmt(load)}, miss {track['miss_counter']}"
            step_kind = "miss"
    track["last_step"] = step_kind
    if notes:
        decision = "; ".join(notes) + "; " + decision
    # regain exit (5.1)
    if regain:
        reason = None
        if e1rm(load, reps, rpe, target) >= regain.get("exit_e1rm_lb", float("inf")):
            reason = f"e1RM {fmt(e1rm(load, reps, rpe, target))} reached {fmt(regain['exit_e1rm_lb'])}"
        elif step_kind == "miss" or (eff >= 8.5 and not merged_not_first):
            reason = f"top set read {fmt(eff)}" if reps >= target else "miss"
        if reason:
            regain["ended"] = f"{date}: {reason}"
            decision += f". Regain phase ends ({reason})"
    # stall: two consecutive misses at the same load
    if track.get("miss_counter", 0) >= 2 and prev_load == load:
        track["_stall"] = True
    return decision


def apply_dp_rule(track, sets, flags, date=""):
    """Double progression for row and pull-up (section 5; regain phase 5.1)."""
    lo, hi = track.get("rep_range", [6, 8])
    inc, step = track.get("increment_lb", 5), track.get("round_step_lb", 5)
    load = max(r["_w"] or 0 for r in sets)
    work = [r for r in sets if (r["_w"] or 0) >= load - 1e-6]
    reps = [int(r["_reps"]) for r in work]
    rpes = [r["_rpe"] for r in work]
    if any(r is None for r in rpes):
        flags.append(f"no RPE on some {track['name']} sets; assumed RPE 8")
    prev_load = track.get("last_h_load_lb")
    track["last_h_load_lb"] = load
    regain = track.get("regain") if active(track.get("regain"), date) else None
    regain_jump = regain and reps and (
        (all(n >= hi for n in reps) and all(r is not None and r <= 7 for r in rpes)) or reps[0] >= regain.get("first_set_reps", 11))
    if regain_jump:
        jump = regain.get("big_increment_lb", 2 * inc)
        track["top_set_lb"] = round_to(load + jump, step)
        track["miss_counter"] = 0
        why = f"first set {reps[0]}" if reps[0] >= regain.get("first_set_reps", 11) else f"all {len(reps)} sets reached {hi} at RPE 7 or lower"
        decision = f"regain phase, {why}: +{fmt(jump)} to {fmt(track['top_set_lb'])}"
    elif all(n >= hi for n in reps) and all((r or 8) <= 8 for r in rpes):
        track["top_set_lb"] = round_to(load + inc, step)
        track["miss_counter"] = 0
        decision = f"all {len(reps)} sets reached {hi}: +{fmt(inc)} to {fmt(track['top_set_lb'])}"
    elif reps and reps[0] < lo:
        track["top_set_lb"] = load
        track["miss_counter"] = track.get("miss_counter", 0) + 1
        decision = f"first set {reps[0]} < {lo}: hold {fmt(load)}, miss {track['miss_counter']}"
        if track["miss_counter"] >= 2 and prev_load == load:
            track["_stall"] = True
    else:
        track["top_set_lb"] = load
        decision = f"reps {reps} at {fmt(load)}: hold, keep adding reps"
    if regain:
        best = max(e1rm(load, n, r) for n, r in zip(reps, rpes)) if reps else 0
        reason = None
        if best >= regain.get("exit_e1rm_lb", float("inf")):
            reason = f"e1RM {fmt(best)} reached {fmt(regain['exit_e1rm_lb'])}"
        elif track.get("miss_counter", 0) > 0 and "miss" in decision:
            reason = "miss"
        if reason:
            regain["ended"] = f"{date}: {reason}"
            decision += f". Regain phase ends ({reason})"
    return decision


def apply_stall(track, reset):
    """Section 6. Returns a note."""
    track.pop("_stall", None)
    if not reset:
        return (f"STALL on {track['name']} (two misses at {fmt(track['last_h_load_lb'])}). Check sleep, calories and bodyweight for the last two weeks first; "
                f"if one is off, fix it and hold one more exposure. Otherwise re-run with --reset-on-stall.")
    pct = 0.925 if track.get("scheme") == "top_set" else 0.95
    step = track.get("round_step_lb", 5)
    new = floor_to(track["top_set_lb"] * pct, step)
    note = f"STALL on {track['name']}: reset {fmt(track['top_set_lb'])} -> {fmt(new)} ({'7.5' if pct == 0.925 else '5'}%)"
    track["top_set_lb"] = new
    track["miss_counter"] = 0
    if "step_counter" in track:
        track["step_counter"] = 0
    track["stalls"] = track.get("stalls", 0) + 1
    if track["stalls"] >= 2 and track.get("scheme") == "top_set":
        note += ". Second stall: switch this lift to a 6-rep top set for one block (section 6.2)"
    return note


# ----- main pass --------------------------------------------------------------

def advance_pointer(slot, rotation):
    order = rotation["slots"]
    last = halves(slot, rotation)[-1]
    return order[(order.index(last) + 1) % len(order)]


def process(tracks, sessions, aliases, rotation, reset_on_stall=False):
    match = matcher(aliases)
    variants = variant_matchers(aliases)
    subs = substitute_matchers(aliases)
    log = []
    flags = []
    processed_through = tracks.get("processed_through") or ""
    latest_slot_session = None
    for (date, title, wid), rows in sessions:
        slot = parse_slot(title)
        if slot:
            latest_slot_session = (date, slot)
        if date <= processed_through:
            continue
        session_exposed = set()
        main_lift_order = []
        if slot:
            parts = [slot] if slot in rotation["sessions"] else halves(slot, rotation)
            for part in parts:
                for ex in rotation["sessions"].get(part, {}).get("exercises", []):
                    if ex.get("role") == "H":
                        main_lift_order.append(ex["track"])
        for lift, t in tracks["tracks"].items():
            lift_rows = [r for r in rows if match.get(lift, lambda n: False)(r.get("exercise"))]
            sets = [r for r in working_sets(lift_rows) if r["_w"] is not None or lift == "pullup"]
            covered = {slot} | (set(halves(slot, rotation)) if slot else set())
            kind = "H" if covered & set(t.get("h_slots", [])) else "V" if covered & set(t.get("v_slots", [])) else "other"
            variant = None
            if not sets and slot:
                for vname, fn in variants.get(lift, []):
                    vsets = [r for r in working_sets([r for r in rows if fn(r.get("exercise"))]) if r["_w"] is not None]
                    if vsets:
                        variant, sets = vname, vsets
                        break
            if not sets:
                if slot and kind in ("H", "V") and t.get("scheme") == "top_set":
                    sub = working_sets([r for r in rows if subs.get(lift, lambda n: False)(r.get("exercise"))])
                    if sub:
                        t["last_sub_exposure"] = {"date": date, "type": kind, "exercise": sub[0].get("exercise")}
                    if kind == "H" and not t.get("h_owed"):
                        t["h_owed"] = {"from": date, "slot": slot}
                        instead = f" ({sub[0].get('exercise')} instead, not counted)" if sub else ""
                        log.append(f"{date} {slot} {t['name']}: heavy slot without the barbell lift{instead} -> "
                                   f"the top set moves to the next {t['name'].lower()} exposure (guide/03 §4.3)")
                continue
            session_exposed.add(lift)
            promoted = False
            if kind == "V" and variant is None and t.get("h_owed") and t.get("scheme") == "top_set":
                refs = [x for x in (t.get("top_set_lb"), t.get("last_h_load_lb")) if x]
                heaviest = max((r["_w"] or 0) for r in sets)
                if refs and heaviest >= min(refs) * 0.97 - 1e-6:
                    kind, promoted = "H", True
            t["last_exposure"] = {"date": date, "type": kind}
            if kind != "H":
                continue
            t.pop("h_owed", None)
            merged_not_first = promoted or (is_merged(slot) and main_lift_order and main_lift_order[0] != lift)
            target = t.get("rep_target")
            if variant:
                vstate = t.setdefault("variants", {}).setdefault(variant, {"top_set_lb": None, "last_h_load_lb": None, "miss_counter": 0})
                proxy = {k: v for k, v in t.items() if k not in ("regain", "variants", "e1rm_history", "last_exposure") + VARIANT_KEYS}
                proxy.update(vstate)
                proxy["name"] = f"{t['name']} ({variant})"
                decision = apply_dp_rule(proxy, sets, flags, date=date)
                load = max(r["_w"] or 0 for r in sets)
                line = f"{date} {slot} {proxy['name']}: {len(sets)} sets at {fmt(load)} -> {decision} (variant: counts as the {t['name'].lower()} exposure; own load)"
                if proxy.pop("_stall", False):
                    line += ". " + apply_stall(proxy, reset_on_stall)
                for k in VARIANT_KEYS:
                    if k in proxy:
                        vstate[k] = proxy[k]
                log.append(line)
                continue
            if t.get("scheme") == "double_progression":
                decision = apply_dp_rule(t, sets, flags, date=date)
                best = max(sets, key=lambda r: e1rm(r["_w"] or 0, int(r["_reps"]), r["_rpe"]))
            else:
                loaded = [r for r in sets if r["_w"]]
                if not loaded:
                    continue
                best = max(loaded, key=lambda r: (r["_w"], r["_reps"]))
                after = loaded[loaded.index(best) + 1:]
                backoffs = [r for r in after if r["_w"] < best["_w"]]
                backoff_reps = int(backoffs[-1]["_reps"]) if backoffs else None
                decision = apply_top_set_rule(t, best, merged_not_first, flags, date=date, backoff_reps=backoff_reps)
                t.pop("work_up", None)
            hist = t.setdefault("e1rm_history", [])
            hist.append({"date": date, "e1rm": e1rm(best["_w"] or 0, int(best["_reps"]), best["_rpe"], target),
                         "load": best["_w"], "reps": int(best["_reps"]), "rpe": best["_rpe"], "slot": slot})
            del hist[:-6]
            line = f"{date} {slot} {t['name']}: top {fmt(best['_w'] or 0)} x {int(best['_reps'])}" + (f" @ {best['_rpe']:g}" if best["_rpe"] is not None else "") + f" -> {decision}"
            if t.pop("_stall", False):
                line += ". " + apply_stall(t, reset_on_stall)
            log.append(line)
        tracks["processed_through"] = date
    if latest_slot_session:
        d, slot = latest_slot_session
        tracks["pointer"] = advance_pointer(slot, rotation)
        if not tracks.get("block_start"):
            tracks["block_start"] = d
        start = dt.date.fromisoformat(tracks["block_start"])
        tracks["block_week"] = (dt.date.fromisoformat(d) - start).days // 7 + 1
    tracks["updated"] = dt.date.today().isoformat()
    return log, flags


def md_table(tracks):
    out = ["| Lift | Next H load (lb) | Back-offs | V load | Rep target | Misses | Last exposure | e1RM history (last 6 H) | Phase |",
           "|---|---|---|---|---|---|---|---|---|"]
    for lift, t in tracks["tracks"].items():
        step = t.get("round_step_lb", 5)
        top = t.get("top_set_lb")
        if top is None:
            topcell, bo, v = "work up", "93% of the load found", "90% of the load found"
        else:
            topcell = f"**{top:g}**"
            bo = f"{round_to(top * t.get('backoff_pct', 0.93), step):g}" if t.get("scheme") == "top_set" else "n/a (double progression)"
            v = f"{round_to(top * t.get('volume_pct', 0.9), step):g}"
        rep = t.get("rep_target") if t.get("scheme") == "top_set" else "-".join(str(x) for x in t.get("rep_range", []))
        le = t.get("last_exposure") or {}
        hist = ", ".join(f"{h['e1rm']:g}" for h in t.get("e1rm_history", []))
        phase = []
        rg, ca = t.get("regain"), t.get("caution")
        if rg:
            phase.append(f"regain ended {rg['ended'].split(':')[0]}" if rg.get("ended") else f"regain to e1RM {rg['exit_e1rm_lb']:g} or {rg['until']}")
        if ca and not ca.get("ended"):
            phase.append(f"caution to {ca['until']}")
        if t.get("rep_out_due"):
            phase.append("rep-out due")
        elif t.get("unrated_streak"):
            phase.append(f"unrated 4s: {t['unrated_streak']}")
        out.append(f"| {t['name']} | {topcell} | {bo} | {v} | {rep} | {t.get('miss_counter', 0)} | {le.get('date', '')} ({le.get('type', '')}) | {hist} | {'; '.join(phase) or '-'} |")
    return "\n".join(out)


def write_md(path, tracks):
    with open(path) as f:
        text = f.read()
    if MD_BEGIN not in text or MD_END not in text:
        sys.exit(f"{path} has no {MD_BEGIN} / {MD_END} markers; table not written.")
    head, rest = text.split(MD_BEGIN, 1)
    _, tail = rest.split(MD_END, 1)
    body = (f"{MD_BEGIN}\nPointer: **{tracks.get('pointer')}**. Block week {tracks.get('block_week')}. "
            f"Processed history through {tracks.get('processed_through') or 'nothing yet'}. Generated by `tools/update_tracks.py --write-md` on {tracks.get('updated')}.\n\n"
            + md_table(tracks) + f"\n{MD_END}")
    with open(path, "w") as f:
        f.write(head + body + tail)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Apply progression rules to data/history.csv and update data/tracks.json.")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--write-md", action="store_true", help="refresh the table in data/track-state.md")
    ap.add_argument("--reset-on-stall", action="store_true")
    ap.add_argument("--since", help="ignore sessions before this date (YYYY-MM-DD)")
    ap.add_argument("--history", default=HISTORY)
    ap.add_argument("--tracks", default=TRACKS)
    ap.add_argument("--aliases", default=ALIASES)
    ap.add_argument("--rotation", default=ROTATION)
    ap.add_argument("--log", default=TRACK_LOG)
    ap.add_argument("--md", default=TRACK_MD)
    args = ap.parse_args(argv)

    with open(args.tracks) as f:
        tracks = json.load(f)
    with open(args.aliases) as f:
        aliases = json.load(f)
    with open(args.rotation) as f:
        rotation = json.load(f)
    sessions = load_sessions(args.history, since=args.since)
    log, flags = process(tracks, sessions, aliases, rotation, reset_on_stall=args.reset_on_stall)

    print(f"Pointer: {tracks.get('pointer')}   block week: {tracks.get('block_week')}   processed through: {tracks.get('processed_through') or '-'}")
    if log:
        print("\nDecisions:")
        for line in log:
            print("  " + line)
    else:
        print("\nNo new heavy exposures since the last update.")
    if flags:
        print("\nFlags:")
        for fl in flags:
            print("  - " + fl)
    print("\n" + md_table(tracks))

    if args.dry_run:
        print("\n(dry run: nothing written)")
        return
    with open(args.tracks, "w") as f:
        json.dump(tracks, f, indent=2, ensure_ascii=False)
        f.write("\n")
    if log or flags:
        new = not os.path.exists(args.log)
        with open(args.log, "a") as f:
            if new:
                f.write("# Track log\n\nAppend-only record of what `tools/update_tracks.py` changed and why. Newest at the bottom.\n")
            f.write(f"\n## {tracks['updated']}\n\n")
            for line in log:
                f.write(f"- {line}\n")
            for fl in flags:
                f.write(f"- Flag: {fl}\n")
    if args.write_md:
        write_md(args.md, tracks)
        print(f"Updated {args.md}")
    print(f"Wrote {args.tracks}")


if __name__ == "__main__":
    main()
