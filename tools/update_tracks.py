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
    4+ reps at RPE <= 7         -> +big increment (10 lb squat and deadlift,
                                   5 lb bench and press), miss counter 0
    4+ reps at RPE 7.5-8        -> +increment (5 lb), miss counter 0. Bench and
                                   press (increment_every = 2): +5 lb on every
                                   second such result, counted in step_counter
                                   (no fractional plates)
    4+ reps at RPE 8.5-9        -> hold
    4+ reps at RPE 9.5-10       -> hold, miss +1 (merged session, lift not first: hold only)
    fewer than 4 reps           -> hold, miss +1
    No RPE logged is treated as RPE 8 and flagged.
    The new planned load is computed from the load actually lifted, so a
    work-up or a heavier-than-planned set moves the track with it.
  Heavy exposure, row and pull-up (double progression):
    every set reached the top of the range at RPE <= 8 -> +5 lb, counter 0
    first set below the bottom of the range             -> hold, miss +1
    otherwise                                           -> hold
  Stall (section 6): two consecutive misses at the same load. Flagged; the load
    is held unless --reset-on-stall is given, which applies the 7.5% reset
    (5% for row and pull-up) and counts the stall.
  Volume (V) exposures and sessions without a slot in the title never change a
    track load; they update the last-exposure date for the gap clock (section 8).
  e1RM from the top set: load x (1 + (reps + (10 - RPE)) / 30); the last 6 kept.
  Pointer: the half-session owed after the latest slot-titled session
    (split +1, merged +2).

Slots are read from the workout title: L1, U1, L2, U2, L3, U3, Full A, Full B,
Full C (case-insensitive prefix, so Hevy routines titled 'L1 Lower A' work).
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


def parse_slot(title):
    m = SLOT_RE.match(title or "")
    if not m:
        return None
    s = m.group(1).upper().replace(" ", "")
    return f"Full {s[-1]}" if s.startswith("FULL") else s


def is_merged(slot):
    return bool(slot) and slot.startswith("Full")


def round_to(x, step):
    """Nearest multiple of step, halves up."""
    return round(math.floor(x / step + 0.5) * step, 2)


def floor_to(x, step):
    return round(math.floor(x / step + 1e-9) * step, 2)


def e1rm(load, reps, rpe):
    rir = 10 - (rpe if rpe is not None else 8)
    return round(load * (1 + (reps + rir) / 30), 1)


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
        subs = [norm(n) for n in names]
        bad = [norm(b) for b in ex.get(lift, [])]
        fns[lift] = (lambda subs, bad: lambda name: any(s in norm(name) for s in subs) and not any(b in norm(name) for b in bad))(subs, bad)
    return fns


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

def apply_top_set_rule(track, top, merged_not_first, flags):
    """Section 5. `top` = the top set row. Mutates track; returns a decision string."""
    load, reps, rpe = top["_w"], int(top["_reps"]), top["_rpe"]
    target = track.get("rep_target", 4)
    inc, big = track.get("increment_lb", 5), track.get("big_increment_lb", 10)
    step = track.get("round_step_lb", 5)
    every = track.get("increment_every", 1)
    if rpe is None:
        flags.append(f"no RPE logged on the {track['name']} top set ({fmt(load)} x {reps}); treated as RPE 8")
        rpe_eff = 8.0
    else:
        rpe_eff = rpe
    prev_load = track.get("last_h_load_lb")
    track["last_h_load_lb"] = load
    if reps < target:
        decision = f"miss ({reps} reps < {target}); hold {fmt(load)}"
        track["top_set_lb"] = load
        track["miss_counter"] = track.get("miss_counter", 0) + 1
    elif rpe_eff <= 7:
        track["top_set_lb"] = round_to(load + big, step)
        track["miss_counter"] = 0
        if every > 1:
            track["step_counter"] = 0
        decision = f"4+ @ {rpe_eff:g}: big step to {fmt(track['top_set_lb'])}"
    elif rpe_eff <= 8:
        track["miss_counter"] = 0
        n = track.get("step_counter", 0) + 1
        if n >= every:
            track["top_set_lb"] = round_to(load + inc, step)
            if every > 1:
                track["step_counter"] = 0
            decision = f"{reps} @ {rpe_eff:g}: +{fmt(inc)} to {fmt(track['top_set_lb'])}"
        else:
            track["top_set_lb"] = load
            track["step_counter"] = n
            decision = f"{reps} @ {rpe_eff:g}: success {n} of {every}; hold {fmt(load)}, +{fmt(inc)} after the next one"
    elif rpe_eff <= 9:
        track["top_set_lb"] = load
        decision = f"{reps} @ {rpe_eff:g}: hold {fmt(load)}"
    else:
        track["top_set_lb"] = load
        if merged_not_first:
            decision = f"{reps} @ {rpe_eff:g} in a merged session, not first lift: hold {fmt(load)} (no miss)"
        else:
            track["miss_counter"] = track.get("miss_counter", 0) + 1
            decision = f"{reps} @ {rpe_eff:g}: hold {fmt(load)}, miss {track['miss_counter']}"
    # stall: two consecutive misses at the same load
    if track.get("miss_counter", 0) >= 2 and prev_load == load:
        track["_stall"] = True
    return decision


def apply_dp_rule(track, sets, flags):
    """Double progression for row and pull-up (section 5)."""
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
    if all(n >= hi for n in reps) and all((r or 8) <= 8 for r in rpes):
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
    if is_merged(slot):
        last = rotation["merged"][slot][-1]
    else:
        last = slot
    return order[(order.index(last) + 1) % len(order)]


def process(tracks, sessions, aliases, rotation, reset_on_stall=False):
    match = matcher(aliases)
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
            for ex in rotation["sessions"].get(slot, {}).get("exercises", []):
                if ex.get("role") == "H":
                    main_lift_order.append(ex["track"])
        for lift, t in tracks["tracks"].items():
            lift_rows = [r for r in rows if match.get(lift, lambda n: False)(r.get("exercise"))]
            sets = [r for r in working_sets(lift_rows) if r["_w"] is not None or lift == "pullup"]
            if not sets:
                continue
            session_exposed.add(lift)
            kind = "H" if slot in t.get("h_slots", []) else "V" if slot in t.get("v_slots", []) else "other"
            t["last_exposure"] = {"date": date, "type": kind}
            if kind != "H":
                continue
            merged_not_first = is_merged(slot) and main_lift_order and main_lift_order[0] != lift
            if t.get("scheme") == "double_progression":
                decision = apply_dp_rule(t, sets, flags)
                best = max(sets, key=lambda r: e1rm(r["_w"] or 0, int(r["_reps"]), r["_rpe"]))
            else:
                loaded = [r for r in sets if r["_w"]]
                if not loaded:
                    continue
                best = max(loaded, key=lambda r: (r["_w"], r["_reps"]))
                decision = apply_top_set_rule(t, best, merged_not_first, flags)
                t.pop("work_up", None)
            hist = t.setdefault("e1rm_history", [])
            hist.append({"date": date, "e1rm": e1rm(best["_w"] or 0, int(best["_reps"]), best["_rpe"]),
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
    out = ["| Lift | Next H load (lb) | Back-offs | V load | Rep target | Misses | Last exposure | e1RM history (last 6 H) |",
           "|---|---|---|---|---|---|---|---|"]
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
        out.append(f"| {t['name']} | {topcell} | {bo} | {v} | {rep} | {t.get('miss_counter', 0)} | {le.get('date', '')} ({le.get('type', '')}) | {hist} |")
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
