#!/usr/bin/env python3
"""Bring the Hevy routines in line with the repo.

Renders the rotation (templates/rotation.json) and this week's sessions
(data/week.json) with the loads in data/tracks.json, compares each routine with
what Hevy holds, and updates the ones that differ. Every update is read back.

Usage:
    python3 tools/hevy_push_routines.py                      # update whatever differs (rotation routines + This Week copies)
    python3 tools/hevy_push_routines.py --check              # compare only; exit 1 if Hevy differs from the repo
    python3 tools/hevy_push_routines.py --week-only          # only the dated This Week copies
    python3 tools/hevy_push_routines.py --only L1 U1         # a subset of rotation slots
    python3 tools/hevy_push_routines.py --all                # update everything, matching or not
    python3 tools/hevy_push_routines.py --dry-run            # print the payloads, no network
    python3 tools/hevy_push_routines.py --resolve            # only fill data/hevy-exercise-map.json
    python3 tools/hevy_push_routines.py --deload             # deload rendering (section 7)
    python3 tools/hevy_push_routines.py --as-of 2026-11-03   # gap modifiers as of that date

Hevy only gets what is on origin/main: the push refuses when tracks.json,
rotation.json, week.json, hevy-state.json or the exercise map differ from it
(tools/gitguard.py). `python3 tools/hevy_sync.py` commits and publishes first.
A skipped session is always printed with its reason, a failed routine does not
stop the others, and the exit code is non-zero unless Hevy matches the repo.

Inputs:
    templates/rotation.json        the twelve sessions as data (6 half-sessions, 3 merged, 3 cross-block merges)
    data/week.json                 this week's dated sessions (tools/week.py)
    data/tracks.json               planned loads per main lift, accessory loads
    data/hevy-exercise-map.json    program exercise -> Hevy template id (filled on first run)
    data/hevy-state.json           folder ids, routine ids, the pool of dated routines

Units: tracks.json is in pounds. Every load is rendered in pounds and converted
to weight_kg (lb x 0.45359237, full precision) only in the payload, because the
Hevy API speaks kg; the app, set to lb, then shows exact pounds.

What each routine contains:
    - H exposure (top-set lifts): warm-up ramp, 1 top set at the track load,
      back-offs at backoff_pct. Row and pull-up: fixed load with the rep range.
    - V exposure: sets at volume_pct of the track load.
    - Accessories: rep range and the load from tracks.json (blank if unknown).
    - Exercise notes carry the RPE targets, since routine sets have no RPE field,
      and the rest for that exercise; rest_seconds sets Hevy's timer. A top set's
      longer rest (rest_top) goes in the note, since Hevy has one timer per exercise.
    - The routine note and the first exercise note open with the target session
      length at those rests (estimate_minutes, using the time budget in guide/05
      section 6.2). The first exercise carries it because the API never returns
      routine notes, so they cannot be confirmed to show in the app.
    - Gap modifiers (templates/progression-tracks.md section 8) are applied as a
      view from each lift's last exposure date to --as-of (default today) and
      never written back to tracks.json.
    - --deload: top sets at 0.91 x track, one back-off, V and double-progression
      lifts at 2 sets, accessories at most 2 sets.

Routines are matched by slot through data/hevy-state.json, so re-running updates
in place (PUT) instead of creating duplicates. There is no delete endpoint: to
retire a routine, delete it in the app and remove its id from hevy-state.json.
"""
import argparse
import datetime as dt
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gitguard  # noqa: E402
from hevy_api import Hevy, HevyError  # noqa: E402
from localtime import local_today  # noqa: E402
from week import WEEK, is_deload, load_week, save_week, title_for  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROTATION = os.path.join(ROOT, "templates", "rotation.json")
TRACKS = os.path.join(ROOT, "data", "tracks.json")
EXMAP = os.path.join(ROOT, "data", "hevy-exercise-map.json")
STATE = os.path.join(ROOT, "data", "hevy-state.json")

RAMP = [(0.0, 5), (0.80, 2)]  # fraction of the day's working load, reps
RAMP_MID = (0.60, 3)  # added between bar and 80% from RAMP_MID_FROM_LB (coaching convention)
RAMP_MID_FROM_LB = 225
FEEDER = [(0.65, 3)]
BAR_LB = 45
WARMUP_STEP_LB = 5
LB_KG = 0.45359237


def to_kg(lb):
    return None if lb is None else lb * LB_KG


def fmt(x):
    """125.0 -> '125', 62.5 -> '62.5'."""
    return f"{x:g}"

# Session-length estimate (guide/05-exercise-selection.md, section 6.2), seconds.
GENERAL_WARMUP_S = 300   # light cardio and mobility before the first ramp set
WARMUP_SET_S = 90        # one ramp or feeder set plus loading the bar
WORK_SET_S = 45          # one working set with setup
PER_LEG_SET_S = 90       # both sides of a per-leg set
TRANSITION_S = 90        # moving to and setting up the next exercise


def load_json(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path) as f:
        return json.load(f)


def save_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, path)


def round_to(x, step):
    """Round to the nearest multiple of step, halves up (so 122.5 -> 125 at 5 lb)."""
    if x is None:
        return None
    return round(math.floor(x / step + 0.5) * step, 2)


def gap_modifier(track, as_of):
    """Section 8. Returns (load_for_next_H, backoff_delta, note) given the planned
    track load, the last lifted H load and the days since the last exposure."""
    planned = track.get("top_set_lb")
    last = track.get("last_h_load_lb")
    exp = (track.get("last_exposure") or {}).get("date")
    if planned is None or not exp:
        return planned, 0, None
    try:
        days = (as_of - dt.date.fromisoformat(exp)).days
    except ValueError:
        return planned, 0, None
    base = last if last is not None else planned
    step = track.get("round_step_lb", 5)
    if days <= 7:
        return planned, 0, None
    sub = (track.get("last_sub_exposure") or {}).get("date")
    if sub and sub > exp:
        # Section 9: a pattern-matched substitute keeps the muscle trained, so a
        # gap it covered is never worse than a hold (no back-off cut, no reduction).
        try:
            sub_days = (as_of - dt.date.fromisoformat(sub)).days
        except ValueError:
            sub_days = days
        days = max(8, min(days, sub_days))
    regain = track.get("regain") or {}
    if days <= 14 and regain and not regain.get("ended") and as_of.isoformat() <= regain.get("until", "9999-12-31"):
        return planned, 0, f"gap {days} d: regain phase, take the planned load (section 5.1)"
    if days <= 14:
        return base, 0, f"gap {days} d: holding {fmt(base)} lb (take the increment next time if this comes in at RPE 7.5 or lower)"
    if days <= 21:
        return base, -1, f"gap {days} d: holding {fmt(base)} lb, one fewer back-off"
    if days <= 28:
        return round_to(base * 0.95, step), 0, f"gap {days} d: reduced 5%, cap the top set at RPE 7"
    return round_to(base * 0.90, step), 0, f"gap {days} d: reduced 10%, first exposure RPE 6-7"


def normalize_slots(tokens, rotation):
    """Accept 'L1', 'full a', 'Full A' (two tokens) or 'FullA'."""
    canon = {k.replace(" ", "").lower(): k for k in rotation["sessions"]}
    out, buf = [], ""
    for tok in tokens:
        key = (buf + tok).replace(" ", "").lower()
        if key in canon:
            out.append(canon[key])
            buf = ""
        elif key == "full":
            buf = tok
        else:
            sys.exit(f"Unknown slot {(buf + ' ' + tok).strip()!r}; choose from {list(rotation['sessions'])}")
    if buf:
        sys.exit(f"Incomplete slot {buf!r}; choose from {list(rotation['sessions'])}")
    return out


def sentence(s):
    """First letter upper-cased, rest untouched (so 'DB' stays 'DB')."""
    s = (s or "").strip()
    return (s[0].upper() + s[1:] + ("" if s.endswith(".") else ".")) if s else ""


def mmss(seconds):
    return f"{seconds // 60}:{seconds % 60:02d}"


def lower_name(name):
    """'Incline DB curl' -> 'incline DB curl'; leaves acronyms alone."""
    return name if name[:2].isupper() else name[:1].lower() + name[1:]


def rest_note(ex, session_exercises, has_warmups):
    """The rest instruction for one exercise, matching the Hevy timer (rest_seconds)."""
    rest = ex.get("rest")
    if not rest:
        return ""
    if ex.get("superset"):
        group = [e for e in session_exercises if e.get("superset") == ex["superset"]]
        pos = next(i for i, e in enumerate(group) if e["name"] == ex["name"])
        if pos < len(group) - 1:
            note = f"Superset: rest {mmss(rest)}, then {lower_name(group[pos + 1]['name'])}."
        else:
            note = f"Superset: rest {mmss(rest)} after the round, then back to {lower_name(group[0]['name'])}."
    elif ex.get("rest_top") and ex["rest_top"] != rest:
        extra = ex["rest_top"] - rest
        note = (f"Rest {mmss(ex['rest_top'])} after the top set (timer + {mmss(extra)}), "
                f"{mmss(rest)} between back-offs.")
    elif ex.get("rest_top"):
        note = f"Rest {mmss(rest)} after the top set and between back-offs."
    else:
        note = f"Rest {mmss(rest)} between sets."
    if has_warmups:
        note += " Warm-ups: about 1:00 apart, as long as loading the bar takes."
    return note


def estimate_minutes(session_exercises, rendered):
    """Start-to-finish minutes at the timer rests, and the minute the main lifts finish.
    Works from the rendered sets, so deloads and gap modifiers are reflected.
    Optional exercises are left out."""
    keep = [k for k, e in enumerate(session_exercises) if not e.get("optional")]
    session_exercises = [session_exercises[k] for k in keep]
    rendered = [rendered[k] for k in keep]
    t = GENERAL_WARMUP_S
    main_done = None
    i = 0
    while i < len(session_exercises):
        ex = session_exercises[i]
        if i:
            t += TRANSITION_S
        if ex.get("superset"):
            idx = [j for j in range(i, len(session_exercises)) if session_exercises[j].get("superset") == ex["superset"]]
            counts = [sum(1 for s in rendered[j]["sets"] if s["type"] == "normal") for j in idx]
            rounds = max(counts)
            for r in range(rounds):
                live = [j for j, n in zip(idx, counts) if n > r]
                for k, j in enumerate(live):
                    t += PER_LEG_SET_S if session_exercises[j].get("per_leg") else WORK_SET_S
                    if k < len(live) - 1 or r < rounds - 1:
                        t += session_exercises[j].get("rest") or 0
            i = idx[-1] + 1
            continue
        sets = rendered[i]["sets"]
        n_warm = sum(1 for s in sets if s["type"] == "warmup")
        if ex.get("warmup") and not n_warm:  # load not set yet: the lifter works up anyway
            n_warm = len(RAMP if ex["warmup"] == "ramp" else FEEDER)
        t += WARMUP_SET_S * n_warm
        n = sum(1 for s in sets if s["type"] == "normal")
        rest = ex.get("rest") or 0
        for k in range(n):
            t += PER_LEG_SET_S if ex.get("per_leg") else WORK_SET_S
            if k < n - 1:
                t += ex.get("rest_top", rest) if k == 0 else rest
        if ex["role"] in ("H", "V"):
            main_done = t
        i += 1
    return round(t / 60), (round(main_done / 60) if main_done is not None else None)


def warmup_sets(kind, work_lb):
    """Ramp or feeder sets in pounds. work_lb is the day's working load: the top
    set on an H day, the V load on a volume day."""
    if not kind or work_lb is None:
        return []
    plan = RAMP if kind == "ramp" else FEEDER
    if kind == "ramp" and work_lb >= RAMP_MID_FROM_LB:
        plan = [RAMP[0], RAMP_MID] + RAMP[1:]
    out = []
    for frac, reps in plan:
        w = BAR_LB if frac == 0 else max(BAR_LB, round_to(work_lb * frac, WARMUP_STEP_LB))
        out.append({"type": "warmup", "weight_lb": w, "reps": reps})
    return out


def phase_active(block, as_of):
    return bool(block) and not block.get("ended") and as_of.isoformat() <= block.get("until", "9999-12-31")


def increment_note(t, as_of=None):
    """The track's increment rule, as it should read on the top-set exercise."""
    inc, every = t.get("increment_lb", 5), t.get("increment_every", 1)
    big = t.get("big_increment_lb", inc)
    regain, caution = t.get("regain"), t.get("caution")
    if as_of and phase_active(regain, as_of):
        cap = regain.get("max_step_lb")
        return (f"Regain phase (to e1RM {fmt(regain['exit_e1rm_lb'])} lb or {regain['until']}): +{fmt(inc)} lb at 4 @ 8; "
                f"+{fmt(big)} lb at 5 @ 8, 6 reps or 4 @ 7" + (f"; never more than +{fmt(cap)} lb." if cap else "."))
    if as_of and phase_active(caution, as_of):
        return (f"+{fmt(inc)} lb next time at 4 @ 8. +{fmt(big)} lb only with a logged RPE 7 or easier, "
                f"and not twice in a row (caution until {caution['until']}). Any low-back pain: hold.")
    if every == 1:
        return f"+{fmt(inc)} lb next time if the top set is {t.get('rep_target', 4)} @ RPE 7.5-8."
    nth = {2: "second", 3: "third"}.get(every, f"{every}th")
    return (f"+{fmt(inc)} lb after every {nth} top set at {t.get('rep_target', 4)} @ RPE 7.5-8 (step counter); "
            f"+{fmt(t.get('big_increment_lb', inc))} lb at once if RPE 7 or lower.")


def render_exercise(ex, tracks, as_of, deload=False, merged=False, rotation_subs=None):
    """Return (sets, notes) for one rotation.json exercise. Set loads are in
    pounds under 'weight_lb'; build_routine converts them to weight_kg.
    rotation_subs: rotation.json "substitutes" (lift -> names, first choice first)."""
    rotation_subs = rotation_subs or {}
    role = ex["role"]
    sets, notes = [], []
    promoted = False
    if role in ("H", "V"):
        t = tracks["tracks"][ex["track"]]
        step = t.get("round_step_lb", 5)
        scheme = t.get("scheme", "top_set")
        if role == "V" and t.get("h_owed") and scheme == "top_set" and t.get("top_set_lb") is not None and not deload:
            # guide/03 section 4.3: the last heavy slot ran without this lift, so
            # its top set moves here (update_tracks.py reads it as the H exposure).
            role, promoted = "H", True
            ex = dict(ex, backoffs=2, warmup=ex.get("warmup") or "feeder")
        if role == "H":
            load, bo_delta, gap_note = gap_modifier(t, as_of)
            if scheme == "top_set":
                if load is None:
                    notes.append(t.get("work_up_note") or "Work up to 4 reps at RPE 8 and log that load.")
                    n_bo = ex.get("backoffs", 3)
                    sets += [{"type": "normal", "weight_lb": None, "reps": t.get("rep_target", 4)}]
                    sets += [{"type": "normal", "weight_lb": None, "reps": t.get("rep_target", 4)} for _ in range(n_bo)]
                    notes.append(f"Then {n_bo} back-off{'s' if n_bo != 1 else ''} x {t.get('rep_target', 4)} at "
                                 f"{t.get('backoff_pct', 0.93):.0%} of the load found, rounded to the nearest {fmt(step)} lb.")
                else:
                    if deload:
                        load = round_to(load * 0.91, step)
                        n_bo = 1
                        notes.append(f"DELOAD: top set {fmt(load)} lb x {t.get('rep_target', 4)} at RPE 6-7, one back-off. Track does not advance.")
                    else:
                        n_bo = max(1, ex.get("backoffs", 3) + bo_delta)
                        notes.append(f"Top set {fmt(load)} lb x {t.get('rep_target', 4)} @ RPE 8 (2 RIR). "
                                     f"If rep {t.get('rep_target', 4)} is clearly easy, keep going, 6 at most; stop at the first slow rep. "
                                     "Rate it: 7 easy, 8 on target, 9 hard, 10 nothing left. Change the reps if you did more or fewer than shown.")
                    bo = round_to(load * t.get("backoff_pct", 0.93), step)
                    notes.append(f"Back-offs {n_bo} x {t.get('rep_target', 4)} at {fmt(bo)} lb (RPE 7-8; stop if a set reaches 9).")
                    if t.get("rep_out_due") and not deload:
                        notes.append("Last back-off: REP-OUT. Keep going to about RPE 9, 10 reps at most, safeties set"
                                     + (" (stop when your back position changes)" if ex.get("track") == "deadlift" else "")
                                     + ". Log the reps.")
                    if not deload:
                        notes.append(increment_note(t, as_of))
                    if gap_note:
                        notes.append(sentence(gap_note))
                    sets += warmup_sets(ex.get("warmup"), load)
                    sets.append({"type": "normal", "weight_lb": load, "reps": t.get("rep_target", 4)})
                    sets += [{"type": "normal", "weight_lb": bo, "reps": t.get("rep_target", 4)} for _ in range(n_bo)]
                if promoted:
                    notes.insert(0, f"TOP SET MOVED HERE: the last heavy {t['name'].lower()} slot ran without it (station taken). "
                                    "Top set and 2 back-offs instead of the volume sets; judge by RPE, a 4 @ 9.5 is a hold, not a miss. "
                                    "If the station is taken again, do the volume sets later or the substitute; the next heavy slot runs as written.")
                elif merged and ex.get("warmup") != "ramp":
                    notes.append("Merged session: judge by RPE, a 4 @ 9.5 here is a hold, not a miss.")
            else:  # double progression
                lo, hi = t.get("rep_range", [6, 8])
                n = 2 if deload else ex.get("sets", 4)
                if gap_note:
                    notes.append(sentence(gap_note))
                step_note = f" ({t['increment_note']})" if t.get("increment_note") else ""
                notes.append(f"{n} x {lo}-{hi} at {fmt(load)} lb, RPE 8 on every set. +{fmt(t.get('increment_lb', 5))} lb{step_note} when every set reaches {hi}.")
                rg = t.get("regain")
                if phase_active(rg, as_of) and not deload:
                    notes.append(f"Regain phase: +{fmt(rg.get('big_increment_lb', 10))} lb if every set reaches {hi} at RPE 7 or easier, "
                                 f"or the first set reaches {rg.get('first_set_reps', 11)}.")
                if ex["track"] == "pullup":
                    notes.append("Pulldown until a set at about bodyweight reaches 8, then weighted pull-ups.")
                sets += warmup_sets(ex.get("warmup"), load)
                sets += [{"type": "normal", "weight_lb": load, "rep_range": {"start": lo, "end": hi}} for _ in range(n)]
        else:  # V
            base = t.get("top_set_lb")
            load = round_to(base * t.get("volume_pct", 0.9), step) if base is not None else None
            n = 2 if deload else ex.get("sets", 3)
            if load is None:
                notes.append(f"Track load not set yet: use {t.get('volume_pct', 0.9):.0%} of the load found at the last heavy "
                             f"{t['name'].lower()}, rounded to the nearest {fmt(step)} lb.")
            if scheme == "top_set":
                at = f" at {fmt(load)} lb ({t.get('volume_pct', 0.9):.0%} of the track load)" if load is not None else ""
                notes.append(f"Volume: {n} x {ex.get('reps')}{at}. No set past RPE 9; do not chase the track.")
                sets += warmup_sets(ex.get("warmup"), load)
                sets += [{"type": "normal", "weight_lb": load, "reps": ex.get("reps")} for _ in range(n)]
            else:
                lo, hi = ex.get("rep_range", t.get("rep_range", [6, 8]))
                at = f" at {fmt(load)} lb" if load is not None else ""
                notes.append(f"Volume: {n} x {lo}-{hi}{at} (RPE 7). Never changes the track.")
                sets += [{"type": "normal", "weight_lb": load, "rep_range": {"start": lo, "end": hi}} for _ in range(n)]
            if deload:
                notes.insert(0, "DELOAD: 2 sets.")
    else:  # accessory
        acc = (tracks.get("accessories") or {}).get(ex["name"]) or {}
        load = acc.get("weight_lb")
        lo, hi = ex.get("rep_range", [8, 12])
        n = min(2, ex.get("sets", 3)) if deload else ex.get("sets", 3)
        notes.append(f"{n} x {lo}-{hi} at RPE {ex.get('rpe', '8')}{' per leg' if ex.get('per_leg') else ''}. Double progression: add reps until every set reaches {hi}, then {acc.get('step') or 'the smallest load step'} and back to {lo}.")
        if acc.get("note"):
            notes.append(sentence(acc["note"]))
        if ex.get("optional"):
            notes.insert(0, "Optional (skip if over 70 min).")
        if deload:
            notes.insert(0, "DELOAD: light, 1-2 sets.")
        sets += [{"type": "normal", "weight_lb": load, "rep_range": {"start": lo, "end": hi}} for _ in range(n)]
    if role in ("H", "V"):
        busy = station_note(ex["track"], role, tracks, rotation_subs)
        if busy:
            notes.append(busy)
    if ex.get("note"):
        notes.insert(0, sentence(ex["note"]))
    return sets, " ".join(notes)


def station_note(track_key, role, tracks, rotation_subs):
    """The busy-gym line for a main lift (guide/03 section 4.3)."""
    t = tracks["tracks"].get(track_key) or {}
    def at(load):
        return f" {fmt(load)} lb" if load else ""
    if t.get("scheme") == "double_progression":
        vs = t.get("variants") or {}
        names = rotation_subs.get(track_key) or list(vs)
        if not names:
            return None
        pct = 1 if role == "H" else t.get("volume_pct", 0.9)
        parts = []
        for n in names:
            load = (vs.get(n) or {}).get("top_set_lb")
            parts.append(n + (at(round_to(load * pct, t.get("round_step_lb", 5))) if load else ""))
        return ("Station taken: any of these counts for this track, same sets and reps, each with its own load: "
                + "; ".join(parts) + ".")
    names = rotation_subs.get(track_key) or []
    if not names:
        return None
    acc = tracks.get("accessories") or {}
    parts = [n + at((acc.get(n) or {}).get("weight_lb")) for n in names]
    if role == "H":
        return ("Station taken: do the next main lift whose station is free and come back. Still taken after that: "
                + " or ".join(parts) + ", same number of working sets, 6-10 reps at RPE 8. "
                "It does not change the track; the top set moves to the next session with this lift.")
    return ("Station taken: do these sets later in the session, or " + " or ".join(parts)
            + " for the same sets at 8-12 reps, RPE 7-8.")


def payload_set(s):
    """Rendered set (pounds) -> API set (weight_kg)."""
    out = {k: v for k, v in s.items() if k != "weight_lb"}
    out["weight_kg"] = to_kg(s.get("weight_lb"))
    return out


def build_routine(slot, rotation, tracks, exmap, as_of, deload=False, folder_id=None):
    session = rotation["sessions"][slot]
    merged = bool(session.get("merged"))
    exercises = []
    unresolved = []
    for ex in session["exercises"]:
        tid = (exmap.get(ex["name"]) or {}).get("template_id")
        if not tid:
            unresolved.append(ex["name"])
        sets, notes = render_exercise(ex, tracks, as_of, deload=deload, merged=merged,
                                     rotation_subs=rotation.get("substitutes"))
        rest = rest_note(ex, session["exercises"], bool(ex.get("warmup")))
        notes = " ".join(n for n in (notes, rest) if n)
        exercises.append({
            "exercise_template_id": tid,
            "superset_id": ex.get("superset"),
            "rest_seconds": ex.get("rest"),
            "notes": notes,
            "sets": [payload_set(s) for s in sets],
        })
    title = session["title"] + (" (deload)" if deload else "")
    notes = session.get("notes", "")
    minutes, main_done = estimate_minutes(session["exercises"], exercises)
    timing = f"Target about {minutes} min start to finish at the timer rests, warm-up included"
    if main_done:
        timing += f"; main lifts done at about {main_done} min"
    timing += ". Finishing much sooner means rest was cut."
    # The API accepts routine notes but never returns them, so the first exercise
    # note, which the app does show, carries the target too.
    if exercises:
        exercises[0]["notes"] = f"Session: {timing[0].lower()}{timing[1:]} {exercises[0]['notes']}"
    notes = timing + " " + notes
    if deload:
        notes = "DELOAD WEEK. " + notes
    notes += f" Rendered {as_of.isoformat()} from data/tracks.json (updated {tracks.get('updated')})."
    payload = {"title": title, "folder_id": folder_id, "notes": notes, "exercises": exercises}
    return payload, unresolved


def resolve_exercises(h, rotation, exmap, custom_lookup=None):
    """Fill exmap[name] = {hevy_title, template_id} for every exercise in the rotation.
    Tries each candidate title in order against the account's exercise templates."""
    index = h.exercise_template_index()
    changed = False
    for session in rotation["sessions"].values():
        for ex in session["exercises"]:
            name = ex["name"]
            if (exmap.get(name) or {}).get("template_id"):
                continue
            candidates = list(ex.get("hevy") or [])
            # the pull-up track can be re-pointed at a different exercise in tracks.json
            if ex.get("track") and custom_lookup and custom_lookup.get(ex["track"]):
                candidates.insert(0, custom_lookup[ex["track"]])
            for cand in candidates:
                t = index.get(cand.strip().lower())
                if t:
                    exmap[name] = {"hevy_title": t["title"], "template_id": t["id"]}
                    changed = True
                    break
            else:
                exmap.setdefault(name, {"hevy_title": None, "template_id": None, "tried": candidates})
                changed = True
    return changed


def add_session_note(payload, note):
    """A dated session's own note (state['this_week'].sessions[].note, e.g. a race
    rule) leads the routine note and the first exercise note, which the app shows."""
    if not note:
        return payload
    payload["notes"] = f"{note} {payload['notes']}"
    if payload["exercises"]:
        payload["exercises"][0]["notes"] = f"{note} {payload['exercises'][0]['notes']}"
    return payload


def _norm(text):
    return " ".join((text or "").split())


def verify_routine(sent_title, sent_exercises, got, notes=True):
    """Compare what the repo renders with the routine Hevy holds. Returns a list
    of differences (empty when it matches). Loads compare to 0.05 kg. With
    notes=True the exercise notes must match too (they carry the loads in
    words); the routine-level note is never returned by the API."""
    diffs = []
    if (got.get("title") or "") != sent_title:
        diffs.append(f"title is {got.get('title')!r}")
    theirs = got.get("exercises") or []
    if len(theirs) != len(sent_exercises):
        diffs.append(f"{len(theirs)} exercises, sent {len(sent_exercises)}")
        return diffs
    for i, (mine, live) in enumerate(zip(sent_exercises, theirs), 1):
        if mine.get("exercise_template_id") != live.get("exercise_template_id"):
            diffs.append(f"exercise {i} is {live.get('title')!r}")
            continue
        a, b = mine.get("sets") or [], live.get("sets") or []
        if len(a) != len(b):
            diffs.append(f"exercise {i} ({live.get('title')}): {len(b)} sets, sent {len(a)}")
            continue
        for j, (x, y) in enumerate(zip(a, b), 1):
            wx, wy = x.get("weight_kg"), y.get("weight_kg")
            if (wx is None) != (wy is None) or (wx is not None and abs(wx - wy) > 0.05) or x.get("reps") != y.get("reps") \
                    or (x.get("type") or "normal") != (y.get("type") or "normal"):
                diffs.append(f"exercise {i} ({live.get('title')}) set {j}: {wy} kg x {y.get('reps')}, sent {wx} kg x {x.get('reps')}")
                break
        else:
            if notes and _norm(mine.get("notes")) != _norm(live.get("notes")):
                diffs.append(f"exercise {i} ({live.get('title')}): note differs")
    return diffs


def read_back(h, routine_id):
    r = h.routine(routine_id)
    r = r.get("routine", r)
    return r[0] if isinstance(r, list) else r


def sync_routine(h, routine_id, title, payload, folder_id, mode="diff"):
    """Bring one routine in line with the repo. mode: 'diff' (default) updates
    only when Hevy differs, 'all' always updates, 'check' never writes.
    Returns (ok, message): ok is True (in step), False (failed or, in check
    mode, different)."""
    try:
        if mode != "all":
            before = verify_routine(title, payload["exercises"], read_back(h, routine_id))
            if not before:
                return True, "in step"
            if mode == "check":
                return False, "DIFFERS: " + "; ".join(before[:4])
        h.update_routine(routine_id, title, payload["exercises"], folder_id=folder_id, notes=payload["notes"])
        after = verify_routine(title, payload["exercises"], read_back(h, routine_id))
    except HevyError as e:
        return False, f"FAILED: {e}"
    if after:
        return False, "MISMATCH after push: " + "; ".join(after[:4])
    return True, "updated and read back"


def week_plan(week, rotation, as_of):
    """Split the week's sessions (data/week.json) into (to_push, skipped).
    Nothing is dropped silently: every skipped session carries its reason."""
    todo, skipped = [], []
    for s in (week or {}).get("sessions", []):
        day = dt.date.fromisoformat(s["date"])
        if s["slot"] not in rotation["sessions"]:
            skipped.append((s, f"slot {s['slot']!r} is not in the rotation"))
        elif s.get("state") in ("done", "missed"):
            skipped.append((s, s["state"]))
        elif day < as_of:
            skipped.append((s, f"dated {s['date']}, before today ({as_of}), and not marked done: move it or mark it with tools/week.py"))
        else:
            todo.append((s, day))
    return todo, skipped


def week_payload(s, day, week, rotation, tracks, exmap, deload, folder_id):
    dl = deload or is_deload(week, day)
    title = title_for(s, rotation, deload=dl)
    payload, _ = build_routine(s["slot"], rotation, tracks, exmap, day, deload=dl, folder_id=folder_id)
    payload["title"] = title
    add_session_note(payload, s.get("note"))
    return title, payload


def push_this_week(h, state, week, rotation, tracks, exmap, as_of, deload=False, mode="diff"):
    """Bring the dated copies of the week's sessions (Hevy folder "This Week")
    in line with data/week.json. Each is rendered with its own date for the gap
    modifiers. Returns ([(label, ok, message)], ids_changed); skips included."""
    tw = state.setdefault("this_week", {})
    folder_id = tw.get("folder_id")
    pool = tw.setdefault("routine_ids", [])
    todo, skipped = week_plan(week, rotation, as_of)
    results = [(f"This Week: {title_for(s, rotation) if s['slot'] in rotation['sessions'] else s['slot']}", None, "skipped: " + why)
               for s, why in skipped]
    changed = False
    used = {s.get("routine_id") for s in week.get("sessions", []) if s.get("routine_id")}
    for s, day in todo:
        title, payload = week_payload(s, day, week, rotation, tracks, exmap, deload, folder_id)
        label = f"This Week: {title}"
        if not s.get("routine_id"):
            free = [i for i in pool if i not in used]
            if free:
                s["routine_id"] = free[0]
                used.add(free[0])
                changed = True
            elif mode == "check":
                results.append((label, False, "DIFFERS: no routine in Hevy yet"))
                print(f"  {label}: {results[-1][2]}")
                continue
            else:
                try:
                    if folder_id is None:
                        f = h.find_folder(tw.get("folder_title") or "This Week") or h.create_folder(tw.get("folder_title") or "This Week")
                        folder_id = tw["folder_id"] = f.get("id")
                        tw.setdefault("folder_title", "This Week")
                    r = h.create_routine(title, payload["exercises"], folder_id=folder_id, notes=payload["notes"])
                    s["routine_id"] = r.get("id")
                    pool.append(r.get("id"))
                    used.add(r.get("id"))
                    changed = True
                    results.append((label, True, f"created ({r.get('id')})"))
                except HevyError as e:
                    results.append((label, False, f"FAILED: {e}"))
                print(f"  {label}: {results[-1][2]}")
                continue
        ok, msg = sync_routine(h, s["routine_id"], title, payload, folder_id, mode)
        results.append((label, ok, msg))
        print(f"  {label}: {msg}")
    return results, changed


def main(argv=None):
    ap = argparse.ArgumentParser(description="Bring the Hevy routines in line with the repo: the rotation routines and this week's dated copies.")
    ap.add_argument("--dry-run", action="store_true", help="print payloads; no network, no file writes")
    ap.add_argument("--check", action="store_true", help="compare Hevy with the repo; write nothing; exit 1 if anything differs")
    ap.add_argument("--all", action="store_true", help="update every routine even when Hevy already matches")
    ap.add_argument("--resolve", action="store_true", help="only resolve exercise template ids and write the map")
    ap.add_argument("--only", nargs="*", help="rotation slots to push (default: every rotation routine, plus the dated This Week copies)")
    ap.add_argument("--week-only", action="store_true", help="only the dated This Week copies, not the rotation routines")
    ap.add_argument("--deload", action="store_true", help="render everything as a deload (data/week.json 'deload' does this for its week)")
    ap.add_argument("--unpublished", action="store_true", help="push even though the inputs differ from origin/main (leaves Hevy ahead of the repo; avoid)")
    ap.add_argument("--as-of", help="date for gap modifiers and the This Week filter (YYYY-MM-DD, default today in TRAINING_TZ, America/New_York)")
    ap.add_argument("--rotation", default=ROTATION)
    ap.add_argument("--tracks", default=TRACKS)
    ap.add_argument("--exmap", default=EXMAP)
    ap.add_argument("--state", default=STATE)
    ap.add_argument("--week", default=WEEK)
    args = ap.parse_args(argv)

    rotation = load_json(args.rotation)
    tracks = load_json(args.tracks)
    exmap = load_json(args.exmap, {}) or {}
    state = load_json(args.state, {}) or {}
    week = load_week(args.week)
    as_of = dt.date.fromisoformat(args.as_of) if args.as_of else local_today()
    deload = args.deload or is_deload(week, as_of)
    slots = normalize_slots(args.only, rotation) if args.only else list(rotation["sessions"].keys())
    if args.week_only:
        slots = []
    mode = "check" if args.check else "all" if args.all else "diff"

    if args.dry_run:
        for slot in slots:
            payload, unresolved = build_routine(slot, rotation, tracks, exmap, as_of, deload=deload, folder_id=state.get("folder_id"))
            print(f"\n=== {slot}: {payload['title']}  (unresolved exercises: {unresolved or 'none'})")
            print(json.dumps({"routine": payload}, indent=1, ensure_ascii=False))
        if not args.only:
            todo, skipped = week_plan(week, rotation, as_of)
            for s, day in todo:
                title, payload = week_payload(s, day, week, rotation, tracks, exmap, args.deload, (state.get("this_week") or {}).get("folder_id"))
                print(f"\n=== This Week: {title}  ({s.get('routine_id') or 'new routine'})")
                print(json.dumps({"routine": payload}, indent=1, ensure_ascii=False))
            for s, why in skipped:
                print(f"\n=== This Week: {s['date']} {s['slot']}  NOT pushed: {why}")
        return

    defaults = (args.rotation, args.tracks, args.week, args.state) == (ROTATION, TRACKS, WEEK, STATE)
    if mode != "check" and not args.resolve and not args.unpublished and defaults:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        stale = gitguard.unpublished([os.path.relpath(p, root) for p in (ROTATION, TRACKS, WEEK, STATE, EXMAP)])
        if stale:
            sys.exit("Not pushed. Hevy only gets what is on origin/main, and these differ from it: " + ", ".join(stale)
                     + ".\nRun `python3 tools/hevy_sync.py` (it commits, publishes, then pushes), or commit and push them to main first."
                     "\n`--check` compares without writing.")

    try:
        h = Hevy()
        custom = {k: v.get("hevy_exercise") for k, v in tracks["tracks"].items() if v.get("hevy_exercise")}
        if mode != "check":
            if resolve_exercises(h, rotation, exmap, custom_lookup=custom):
                save_json(args.exmap, exmap)
        missing = sorted(n for n, v in exmap.items() if not v.get("template_id"))
        if missing:
            print("Could not match these program exercises to a Hevy exercise template:")
            for n in missing:
                print(f"  - {n}: tried {exmap[n].get('tried')}")
            print("Find the right title with `python3 tools/hevy_api.py templates --search <word>` and put it in data/hevy-exercise-map.json (hevy_title and template_id), or add it to the 'hevy' list in templates/rotation.json.")
            if not args.resolve:
                sys.exit("Fix the map and re-run; nothing was pushed.")
        if args.resolve:
            print(f"Exercise map written to {args.exmap} ({len(exmap) - len(missing)} resolved, {len(missing)} missing).")
            return

        folder_id = state.get("folder_id")
        folder_title = rotation.get("folder_title", "Rotation")
        if folder_id is None and mode != "check":
            f = h.find_folder(folder_title)
            if f is None:
                f = h.create_folder(folder_title)
                print(f"Created folder {f.get('id')} {folder_title!r}")
            folder_id = f.get("id")
            state["folder_id"] = folder_id
            state["folder_title"] = folder_title
            save_json(args.state, state)

        routines = state.setdefault("routines", {})
        results = []
        ids_changed = False
        verb = {"check": "Checking", "all": "Pushing everything", "diff": "Pushing what differs"}[mode]
        print(f"{verb} as of {as_of} ({'deload' if deload else 'normal'} rendering).")
        # The dated sessions go first: they are what the lifter opens next, so a
        # rate limit part-way through must not leave them stale.
        if not args.only:
            wk, ids_changed = push_this_week(h, state, week, rotation, tracks, exmap, as_of, args.deload, mode)
            results += wk
            if ids_changed:
                save_week(args.week, week)
                save_json(args.state, state)
        else:
            print("  This Week routines left alone (--only was given).")
        for slot in slots:
            payload, _ = build_routine(slot, rotation, tracks, exmap, as_of, deload=deload, folder_id=folder_id)
            label = f"{slot}: {payload['title']}"
            rid = routines.get(slot)
            if rid:
                ok, msg = sync_routine(h, rid, payload["title"], payload, folder_id, mode)
            elif mode == "check":
                ok, msg = False, "DIFFERS: no routine in Hevy yet"
            else:
                try:
                    r = h.create_routine(payload["title"], payload["exercises"], folder_id=folder_id, notes=payload["notes"])
                    routines[slot] = r.get("id")
                    save_json(args.state, state)
                    ids_changed = True
                    ok, msg = True, f"created ({r.get('id')})"
                except HevyError as e:
                    ok, msg = False, f"FAILED: {e}"
            results.append((label, ok, msg))
            print(f"  {label}: {msg}")

        failed = [r for r in results if r[1] is False]
        skipped = [r for r in results if r[1] is None]
        same = sum(1 for r in results if r[1] and r[2] == "in step")
        done = sum(1 for r in results if r[1]) - same
        if mode == "check":
            print(f"\nCheck: {same} in step, {len(failed)} differ, {len(skipped)} skipped.")
        else:
            print(f"\nPush summary: {done} updated, {same} already in step, {len(skipped)} skipped, {len(failed)} failed.")
        for label, _, msg in skipped + failed:
            print(f"  {label}: {msg}")
        if ids_changed:
            print("New Hevy routine ids were recorded in data/hevy-state.json or data/week.json: commit and push them (hevy_sync.py does).")
        if failed and mode == "check":
            sys.exit("Hevy does not match the repo. `python3 tools/hevy_sync.py` brings it in line.")
        if failed:
            sys.exit("Push incomplete: Hevy does not match the repo for the routines above. Re-run `python3 tools/hevy_push_routines.py` "
                     "(the tracks are already updated; do not re-apply the rules by hand).")
        if mode != "check":
            print(f"Done. Hevy matches the repo. Next session owed: {tracks.get('pointer')}.")
    except HevyError as e:
        sys.exit(str(e))


if __name__ == "__main__":
    main()
