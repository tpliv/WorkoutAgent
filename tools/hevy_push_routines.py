#!/usr/bin/env python3
"""Render the rotation into Hevy routines and create or update them over the API.

Usage:
    python3 tools/hevy_push_routines.py --dry-run            # print the payloads, no network
    python3 tools/hevy_push_routines.py --resolve            # only fill data/hevy-exercise-map.json
    python3 tools/hevy_push_routines.py                      # create or update the nine routines
    python3 tools/hevy_push_routines.py --only L1 U1         # a subset of slots
    python3 tools/hevy_push_routines.py --deload             # deload rendering (section 7)
    python3 tools/hevy_push_routines.py --as-of 2026-11-03   # gap modifiers as of that date

Inputs:
    templates/rotation.json        the nine sessions as data
    data/tracks.json               planned loads per main lift, accessory loads
    data/hevy-exercise-map.json    program exercise -> Hevy template id (filled on first run)
    data/hevy-state.json           folder id and routine ids (filled on first run)

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
from hevy_api import Hevy, HevyError  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROTATION = os.path.join(ROOT, "templates", "rotation.json")
TRACKS = os.path.join(ROOT, "data", "tracks.json")
EXMAP = os.path.join(ROOT, "data", "hevy-exercise-map.json")
STATE = os.path.join(ROOT, "data", "hevy-state.json")

RAMP = [(0.0, 10), (0.40, 8), (0.60, 5), (0.80, 2)]  # fraction of the top set, reps
FEEDER = [(0.65, 3)]
BAR_KG = 20

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
    with open(path, "w") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


def round_to(x, step):
    """Round to the nearest multiple of step, halves up (so 38.25 -> 38.5 at 0.5 kg)."""
    if x is None:
        return None
    return round(math.floor(x / step + 0.5) * step, 2)


def gap_modifier(track, as_of):
    """Section 8. Returns (load_for_next_H, backoff_delta, note) given the planned
    track load, the last lifted H load and the days since the last exposure."""
    planned = track.get("top_set_kg")
    last = track.get("last_h_load_kg")
    exp = (track.get("last_exposure") or {}).get("date")
    if planned is None or not exp:
        return planned, 0, None
    try:
        days = (as_of - dt.date.fromisoformat(exp)).days
    except ValueError:
        return planned, 0, None
    base = last if last is not None else planned
    step = track.get("round_step_kg", 2.5)
    if days <= 7:
        return planned, 0, None
    if days <= 14:
        return base, 0, f"gap {days} d: holding {base} (take the increment next time if this comes in at RPE 7.5 or lower)"
    if days <= 21:
        return base, -1, f"gap {days} d: holding {base}, one fewer back-off"
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


def warmup_sets(kind, top_kg):
    if not kind or top_kg is None:
        return []
    plan = RAMP if kind == "ramp" else FEEDER
    out = []
    for frac, reps in plan:
        w = BAR_KG if frac == 0 else max(BAR_KG, round_to(top_kg * frac, 2.5))
        out.append({"type": "warmup", "weight_kg": w, "reps": reps})
    return out


def render_exercise(ex, tracks, as_of, deload=False, merged=False):
    """Return (sets, notes, meta) for one rotation.json exercise."""
    role = ex["role"]
    sets, notes = [], []
    if role in ("H", "V"):
        t = tracks["tracks"][ex["track"]]
        step = t.get("round_step_kg", 2.5)
        scheme = t.get("scheme", "top_set")
        if role == "H":
            load, bo_delta, gap_note = gap_modifier(t, as_of)
            if scheme == "top_set":
                if load is None:
                    notes.append(t.get("work_up_note") or "Work up to 4 reps at RPE 8 and log that load.")
                    n_bo = ex.get("backoffs", 3)
                    sets += [{"type": "normal", "weight_kg": None, "reps": t.get("rep_target", 4)}]
                    sets += [{"type": "normal", "weight_kg": None, "reps": t.get("rep_target", 4)} for _ in range(n_bo)]
                    notes.append(f"Then {n_bo} back-off(s) x {t.get('rep_target', 4)} at 93% of the load found.")
                else:
                    if deload:
                        load = round_to(load * 0.91, step)
                        n_bo = 1
                        notes.append(f"DELOAD: top set {load} x {t.get('rep_target', 4)} at RPE 6-7, one back-off. Track does not advance.")
                    else:
                        n_bo = max(1, ex.get("backoffs", 3) + bo_delta)
                        notes.append(f"Top set {load} x {t.get('rep_target', 4)} @ RPE 8 (2 RIR). Rate it immediately.")
                    bo = round_to(load * t.get("backoff_pct", 0.93), step)
                    notes.append(f"Back-offs {n_bo} x {t.get('rep_target', 4)} at {bo} (RPE 7-8; stop if a set reaches 9).")
                    if gap_note:
                        notes.append(sentence(gap_note))
                    sets += warmup_sets(ex.get("warmup"), load)
                    sets.append({"type": "normal", "weight_kg": load, "reps": t.get("rep_target", 4)})
                    sets += [{"type": "normal", "weight_kg": bo, "reps": t.get("rep_target", 4)} for _ in range(n_bo)]
                if merged and ex.get("warmup") != "ramp":
                    notes.append("Merged session: judge by RPE, a 4 @ 9.5 here is a hold, not a miss.")
            else:  # double progression
                lo, hi = t.get("rep_range", [6, 8])
                n = 2 if deload else ex.get("sets", 4)
                if gap_note:
                    notes.append(sentence(gap_note))
                notes.append(f"{n} x {lo}-{hi} at {load} kg, RPE 8 on every set. +{t.get('increment_kg', 2.5)} kg when every set reaches {hi}.")
                if ex["track"] == "pullup":
                    notes.append("Pulldown until a set at about bodyweight reaches 8, then weighted pull-ups.")
                sets += warmup_sets(ex.get("warmup"), load)
                sets += [{"type": "normal", "weight_kg": load, "rep_range": {"start": lo, "end": hi}} for _ in range(n)]
        else:  # V
            base = t.get("top_set_kg")
            load = round_to(base * t.get("volume_pct", 0.9), step) if base is not None else None
            n = 2 if deload else ex.get("sets", 3)
            if load is None:
                notes.append("Track load not set yet: use 90% of the load found at the last heavy exposure.")
            if scheme == "top_set":
                notes.append(f"Volume: {n} x {ex.get('reps')} at {load if load is not None else '90% of track'} (90% of the track load). No set past RPE 9; do not chase the track.")
                sets += warmup_sets(ex.get("warmup"), base)
                sets += [{"type": "normal", "weight_kg": load, "reps": ex.get("reps")} for _ in range(n)]
            else:
                lo, hi = ex.get("rep_range", t.get("rep_range", [6, 8]))
                notes.append(f"Volume: {n} x {lo}-{hi} at {load if load is not None else '90% of track'} (RPE 7). Never changes the track.")
                sets += [{"type": "normal", "weight_kg": load, "rep_range": {"start": lo, "end": hi}} for _ in range(n)]
            if deload:
                notes.insert(0, "DELOAD: 2 sets.")
    else:  # accessory
        acc = (tracks.get("accessories") or {}).get(ex["name"]) or {}
        load = acc.get("weight_kg")
        lo, hi = ex.get("rep_range", [8, 12])
        n = min(2, ex.get("sets", 3)) if deload else ex.get("sets", 3)
        notes.append(f"{n} x {lo}-{hi} at RPE {ex.get('rpe', '8')}{' per leg' if ex.get('per_leg') else ''}. Double progression: add reps until every set reaches {hi}, then the smallest load step and back to {lo}.")
        if acc.get("note"):
            notes.append(sentence(acc["note"]))
        if ex.get("optional"):
            notes.insert(0, "Optional (skip if over 70 min).")
        if deload:
            notes.insert(0, "DELOAD: light, 1-2 sets.")
        sets += [{"type": "normal", "weight_kg": load, "rep_range": {"start": lo, "end": hi}} for _ in range(n)]
    return sets, " ".join(notes)


def build_routine(slot, rotation, tracks, exmap, as_of, deload=False, folder_id=None):
    session = rotation["sessions"][slot]
    merged = bool(session.get("merged"))
    exercises = []
    unresolved = []
    for ex in session["exercises"]:
        tid = (exmap.get(ex["name"]) or {}).get("template_id")
        if not tid:
            unresolved.append(ex["name"])
        sets, notes = render_exercise(ex, tracks, as_of, deload=deload, merged=merged)
        rest = rest_note(ex, session["exercises"], bool(ex.get("warmup")))
        notes = " ".join(n for n in (notes, rest) if n)
        exercises.append({
            "exercise_template_id": tid,
            "superset_id": ex.get("superset"),
            "rest_seconds": ex.get("rest"),
            "notes": notes,
            "sets": sets,
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


def main(argv=None):
    ap = argparse.ArgumentParser(description="Create or update the rotation's routines in Hevy.")
    ap.add_argument("--dry-run", action="store_true", help="print payloads; no network, no file writes")
    ap.add_argument("--resolve", action="store_true", help="only resolve exercise template ids and write the map")
    ap.add_argument("--only", nargs="*", help="slots to push (default: all nine)")
    ap.add_argument("--deload", action="store_true")
    ap.add_argument("--as-of", help="date for gap modifiers (YYYY-MM-DD, default today)")
    ap.add_argument("--rotation", default=ROTATION)
    ap.add_argument("--tracks", default=TRACKS)
    ap.add_argument("--exmap", default=EXMAP)
    ap.add_argument("--state", default=STATE)
    args = ap.parse_args(argv)

    rotation = load_json(args.rotation)
    tracks = load_json(args.tracks)
    exmap = load_json(args.exmap, {}) or {}
    state = load_json(args.state, {}) or {}
    as_of = dt.date.fromisoformat(args.as_of) if args.as_of else dt.date.today()
    slots = normalize_slots(args.only, rotation) if args.only else list(rotation["sessions"].keys())

    if args.dry_run:
        for slot in slots:
            payload, unresolved = build_routine(slot, rotation, tracks, exmap, as_of, deload=args.deload, folder_id=state.get("folder_id"))
            print(f"\n=== {slot}: {payload['title']}  (unresolved exercises: {unresolved or 'none'})")
            print(json.dumps({"routine": payload}, indent=1, ensure_ascii=False))
        return

    try:
        h = Hevy()
        custom = {k: v.get("hevy_exercise") for k, v in tracks["tracks"].items() if v.get("hevy_exercise")}
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
        if folder_id is None:
            f = h.find_folder(folder_title)
            if f is None:
                f = h.create_folder(folder_title)
                print(f"Created folder {f.get('id')} {folder_title!r}")
            folder_id = f.get("id")
            state["folder_id"] = folder_id
            state["folder_title"] = folder_title
            save_json(args.state, state)

        routines = state.setdefault("routines", {})
        for slot in slots:
            payload, _ = build_routine(slot, rotation, tracks, exmap, as_of, deload=args.deload, folder_id=folder_id)
            rid = routines.get(slot)
            if rid:
                r = h.update_routine(rid, payload["title"], payload["exercises"], folder_id=folder_id, notes=payload["notes"])
                print(f"Updated {slot}: {payload['title']} ({rid})")
            else:
                r = h.create_routine(payload["title"], payload["exercises"], folder_id=folder_id, notes=payload["notes"])
                routines[slot] = r.get("id")
                print(f"Created {slot}: {payload['title']} ({r.get('id')})")
            save_json(args.state, state)
        state["last_push"] = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        state["last_push_deload"] = bool(args.deload)
        save_json(args.state, state)
        print(f"Done. Open Hevy > Workout > folder {folder_title!r} and start the routine the pointer names ({tracks.get('pointer')}).")
    except HevyError as e:
        sys.exit(str(e))


if __name__ == "__main__":
    main()
