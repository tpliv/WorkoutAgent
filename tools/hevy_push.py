#!/usr/bin/env python3
"""Write the next session's loads into the Hevy routines.

Usage:
    python3 tools/hevy_push.py            # dry run: show what would change
    python3 tools/hevy_push.py --apply    # write the changes to Hevy

Reads:
    data/track-state.md      main-lift loads in pounds (the six-tracks table)
    tools/hevy_program.json  routine layout, accessory loads, exercise template IDs

Writes:
    data/raw/hevy_push_plan.json   the exact request bodies (gitignored)
    Hevy (with --apply only): updates each routine in the program's folder whose
    title matches; creates any that are missing. Routines outside that folder
    are never touched.

The key comes from the HEVY_API_KEY environment variable. If it is unset the
requests go out without one, which works only behind a proxy that adds the
api-key header itself (as in the Claude Code cloud sandbox).

Hevy stores weights in kilograms. Pounds are converted with the exact factor
(1 lb = 0.45359237 kg), which is how the app itself stores pound entries, so a
135 lb plan shows as 135 in an app set to pounds. Routine sets have no RPE
field (API spec at https://api.hevyapp.com/docs/, checked 2026-10-21), so RPE
targets go in the exercise notes.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

BASE = "https://api.hevyapp.com/v1"
LB = 0.45359237
BAR_LB = 45
H_STEP_LB = {"squat": 5, "deadlift": 5, "bench": 2.5, "press": 2.5}

# Lift names in the track-state table -> exercise keys in hevy_program.json.
TRACK_ROWS = {
    "squat": "squat",
    "bench press": "bench",
    "deadlift": "deadlift",
    "overhead press": "press",
    "barbell row": "row",
    "pull-up / pulldown": "pulldown",
}


def api(method, path, body=None):
    headers = {"accept": "application/json"}
    key = os.environ.get("HEVY_API_KEY")
    if key:
        headers["api-key"] = key
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        headers["content-type"] = "application/json"
    req = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code in (401, 403) and method == "GET":
                sys.exit(f"Hevy API refused the request (HTTP {e.code}). Set HEVY_API_KEY and check the account has Pro.")
            if e.code == 429 and attempt < 4:
                time.sleep(2 ** attempt)
                continue
            sys.exit(f"{method} {path} failed: HTTP {e.code} {e.read().decode(errors='replace')[:500]}")
        except urllib.error.URLError as e:
            sys.exit(f"Could not reach {BASE}: {e.reason}. If this runs in a cloud sandbox, api.hevyapp.com must be on the environment's allowed domains.")


def get_all(path, field):
    page, items = 1, []
    while True:
        data = api("GET", f"{path}?page={page}&pageSize=10")
        items += data.get(field, [])
        if page >= data.get("page_count", 1):
            return items
        page += 1


# ---- track state ----------------------------------------------------------

def lead_number(cell):
    m = re.match(r"\**\s*(\d+(?:\.\d+)?)", cell.strip())
    return float(m.group(1)) if m else None


def round5(x):
    return 5 * round(x / 5)


def read_tracks(path):
    text = open(path).read()
    m = re.search(r"Last updated: (\d{4}-\d{2}-\d{2})", text)
    updated = m.group(1) if m else "unknown date"
    section = text.split("## The six tracks", 1)[1].split("\n## ", 1)[0]
    tracks = {}
    for line in section.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        key = TRACK_ROWS.get(cells[0].lower()) if len(cells) > 3 else None
        if not key:
            continue
        top = lead_number(cells[1])
        # With no top-set load, the other columns hold instructions, not loads.
        backoff = lead_number(cells[2]) if top else None
        v = lead_number(cells[3]) if top else None
        tracks[key] = {"top": top, "backoff": backoff, "v": v}
        if top and backoff and abs(backoff - round5(top * 0.93)) > 5:
            print(f"warning: {key} back-off {backoff:g} is not about 93% of {top:g}", file=sys.stderr)
        if top and v and abs(v - top * 0.9) > 5:
            print(f"warning: {key} V load {v:g} is not about 90% of {top:g}", file=sys.stderr)
    missing = set(TRACK_ROWS.values()) - set(tracks)
    if missing:
        sys.exit(f"{path}: no row for {', '.join(sorted(missing))} in the six-tracks table")
    return updated, tracks


# ---- routine construction -------------------------------------------------

def hevy_set(kind, lb, reps):
    rng = isinstance(reps, list)
    return {
        "type": kind,
        "weight_kg": None if lb is None else lb * LB,
        "reps": None if rng else reps,
        "rep_range": {"start": reps[0], "end": reps[1]} if rng else None,
        "distance_meters": None,
        "duration_seconds": None,
        "custom_metric": None,
    }


def warmups(load, first, bar):
    """Template rule: ramp on the session's first compound, one feeder set on later ones."""
    if load is None:
        return []
    if first:
        ramp = [(bar, 10), (round5(load * 0.4), 8), (round5(load * 0.6), 5), (round5(load * 0.8), 2)]
    else:
        ramp = [(round5(load * 0.65), 3)]
    return [hevy_set("warmup", max(bar, w), r) for w, r in ramp]


def fmt(lb):
    return f"{lb:g}"


def rep_text(reps):
    return f"{reps[0]}-{reps[1]}" if isinstance(reps, list) else str(reps)


def main_lift(e, lib, t, first):
    key, kind = e["ex"], e["kind"]
    bar = BAR_LB if "(Barbell)" in lib["name"] else 0
    top, bo, v = t["top"], t["backoff"], t["v"]
    tip = lib.get("tip", "")
    if kind == "H" and top is None:
        n = e["backoffs"]
        ramp = ", ".join(f"{fmt(w)} x 4" for w in lib["workup"])
        sets = [hevy_set("warmup", w, 4) for w in lib["workup"]]
        sets += [hevy_set("normal", None, 4)] * (1 + n)
        note = (f"Track load not set yet. Warm up, then {ramp}, then +10 lb per set until 4 reps "
                f"feel like RPE 8. Log that set as the top set with its RPE; it becomes the track "
                f"load. Then {n} x 4 at 93% of it (RPE 7-8).")
    elif kind == "H":
        n = e["backoffs"]
        sets = warmups(top, first, bar) + [hevy_set("normal", top, 4)] + [hevy_set("normal", bo, 4)] * n
        note = (f"Top set {fmt(top)} lb x 4 @ RPE 8 (2 RIR); log the RPE right after the set. "
                f"Back-offs {n} x 4 at {fmt(bo)} lb (RPE 7-8; stop if a set reaches 9). "
                f"Next time: RPE 8 or lower adds {fmt(H_STEP_LB[key])} lb; 8.5-9 holds; "
                f"RPE 10 or under 4 reps holds and counts a miss.")
        if e.get("merged"):
            note += " Merged session: judge by RPE; a 4 @ 9.5 here is a hold, not a miss."
    elif kind == "V" and v is None:
        sets = [hevy_set("normal", None, e["reps"])] * e["sets"]
        note = (f"Track load not set yet: use 90% of the top set found at the last L2 or Full B. "
                f"{e['sets']} x {rep_text(e['reps'])} at RPE {e['rpe']}; crisp, fast reps. Never moves the track.")
    elif kind == "V":
        sets = warmups(v, first, bar) + [hevy_set("normal", v, e["reps"])] * e["sets"]
        note = (f"Volume: {e['sets']} x {rep_text(e['reps'])} at {fmt(v)} lb (90% of the {fmt(top)} lb track). "
                f"RPE {e['rpe']}; no set past 9. Never moves the track.")
    elif kind == "DP":
        lo, hi = e["reps"]
        sets = warmups(top, first, bar) + [hevy_set("normal", top, e["reps"])] * e["sets"]
        note = (f"{e['sets']} x {lo}-{hi} at {fmt(top)} lb, RPE 8 on every set. "
                f"When every set reaches {hi}, add 5 lb next time.")
    elif kind == "DPV":
        sets = warmups(v, first, bar) + [hevy_set("normal", v, e["reps"])] * e["sets"]
        note = f"Volume: {e['sets']} x {rep_text(e['reps'])} at {fmt(v)} lb, RPE {e['rpe']}. Never moves the track."
    else:
        sys.exit(f"unknown kind {kind!r} for {key}")
    return sets, " ".join(x for x in (note, tip) if x)


def accessory(e, lib):
    lo, hi = e["reps"]
    sets = [hevy_set("normal", e.get("load"), e["reps"])] * e["sets"]
    note = (f"{e['sets']} x {lo}-{hi} at RPE {e['rpe']}. Double progression: add reps until every set "
            f"reaches {hi}, then the smallest load step and back to {lo}.")
    if e.get("load") is None:
        note += f" Choose the load on the day: 2-3 reps in reserve at {lo}."
    return sets, " ".join(x for x in (e.get("note", ""), note, lib.get("tip", "")) if x)


def build_routine(r, program, tracks, updated, folder_id):
    exercises, first = [], True
    for e in r["exercises"]:
        lib = program["exercises"][e["ex"]]
        if "kind" in e:
            sets, note = main_lift(e, lib, tracks[e["ex"]], first)
            first = False
        else:
            sets, note = accessory(e, lib)
        exercises.append({
            "exercise_template_id": lib["id"],
            "superset_id": e.get("superset"),
            "rest_seconds": e["rest"],
            "notes": note,
            "sets": sets,
        })
    return {"routine": {
        "title": r["title"],
        "folder_id": folder_id,
        "notes": (f"Loads in lb from data/track-state.md (updated {updated}), written by tools/hevy_push.py. "
                  "Log RPE on every top set."),
        "exercises": exercises,
    }}


# ---- diff -----------------------------------------------------------------

def set_text(s):
    w = s.get("weight_kg")
    load = "-" if w is None else fmt(round(w / LB, 1))
    rr = s.get("rep_range") or {}
    reps = f"{rr['start']:g}-{rr['end']:g}" if rr.get("start") is not None else ("?" if s.get("reps") is None else f"{s['reps']:g}")
    return ("w" if s["type"] == "warmup" else "") + f"{load}x{reps}"


def sets_text(sets):
    parts, prev, count = [], None, 0
    for t in [set_text(s) for s in sets] + [None]:
        if t == prev:
            count += 1
            continue
        if prev is not None:
            parts.append(prev + (f"(x{count})" if count > 1 else ""))
        prev, count = t, 1
    return " ".join(parts)


def show_diff(title, current, planned, names):
    new_ex = planned["routine"]["exercises"]
    if current is None:
        print(f"\n== {title}: not in Hevy, would be created")
        for e in new_ex:
            print(f"   {names[e['exercise_template_id']]}: {sets_text(e['sets'])}")
        return True
    old_ex = current["exercises"]
    changed = []
    for i in range(max(len(old_ex), len(new_ex))):
        o = old_ex[i] if i < len(old_ex) else None
        n = new_ex[i] if i < len(new_ex) else None
        name = names.get((n or o)["exercise_template_id"], (o or {}).get("title", "?"))
        lines = []
        if o is None or n is None or o["exercise_template_id"] != n["exercise_template_id"]:
            lines.append(f"      exercise: {o and o['title']} -> {n and names[n['exercise_template_id']]}")
        if o and n:
            if sets_text(o["sets"]) != sets_text(n["sets"]):
                lines.append(f"      now:  {sets_text(o['sets'])}")
                lines.append(f"      new:  {sets_text(n['sets'])}")
            if (o["rest_seconds"], o["superset_id"]) != (n["rest_seconds"], n["superset_id"]):
                lines.append(f"      rest/superset: {o['rest_seconds']}/{o['superset_id']} -> {n['rest_seconds']}/{n['superset_id']}")
            if (o.get("notes") or "") != n["notes"]:
                lines.append(f"      note: {n['notes']}")
        if lines:
            changed.append((name, lines))
    if (current.get("notes") or "") != planned["routine"]["notes"]:
        changed.append(("(routine note)", [f"      note: {planned['routine']['notes']}"]))
    if not changed:
        print(f"\n== {title}: unchanged")
        return False
    print(f"\n== {title}: {len(changed)} change(s)")
    for name, lines in changed:
        print(f"   {name}")
        print("\n".join(lines))
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write the changes to Hevy (default is a dry run)")
    ap.add_argument("--state", default="data/track-state.md")
    ap.add_argument("--program", default="tools/hevy_program.json")
    ap.add_argument("--plan", default="data/raw/hevy_push_plan.json")
    args = ap.parse_args()

    if not os.environ.get("HEVY_API_KEY"):
        print("note: HEVY_API_KEY is not set; relying on a proxy to add the api-key header.", file=sys.stderr)

    updated, tracks = read_tracks(args.state)
    program = json.load(open(args.program))
    names = {x["id"]: x["name"] for x in program["exercises"].values()}

    print(f"Track state ({args.state}, updated {updated}), lb:")
    for k, t in tracks.items():
        vals = ", ".join(f"{f} {fmt(t[f]) if t[f] is not None else 'unset'}" for f in ("top", "backoff", "v"))
        print(f"   {k:9} {vals}")

    folders = [f for f in get_all("/routine_folders", "routine_folders") if f["title"] == program["folder"]]
    folder_id = folders[0]["id"] if folders else None
    existing = {}
    if folder_id is not None:
        for r in get_all("/routines", "routines"):
            if r.get("folder_id") == folder_id:
                existing.setdefault(r["title"], r)
    print(f"Folder '{program['folder']}': " + (f"id {folder_id}, {len(existing)} routine(s)" if folder_id else "missing, would be created"))

    plans, todo = {}, []
    for r in program["routines"]:
        plan = build_routine(r, program, tracks, updated, folder_id)
        plans[r["title"]] = plan
        if show_diff(r["title"], existing.get(r["title"]), plan, names):
            todo.append(r["title"])

    os.makedirs(os.path.dirname(args.plan), exist_ok=True)
    with open(args.plan, "w") as f:
        json.dump(plans, f, indent=1)
    print(f"\n{len(todo)} of {len(plans)} routine(s) would change. Request bodies in {args.plan}.")

    if not args.apply:
        print("Dry run: nothing was sent. Re-run with --apply to write to Hevy.")
        return
    if folder_id is None:
        folder_id = api("POST", "/routine_folders", {"routine_folder": {"title": program["folder"]}})["routine_folder"]["id"]
        print(f"Created folder '{program['folder']}' (id {folder_id}).")
    for title in todo:
        plan = plans[title]
        plan["routine"]["folder_id"] = folder_id
        if title in existing:
            # Already in the folder, so leave folder_id out of the update.
            body = {"routine": {k: v for k, v in plan["routine"].items() if k != "folder_id"}}
            api("PUT", f"/routines/{existing[title]['id']}", body)
            print(f"Updated {title}.")
        else:
            api("POST", "/routines", plan)
            print(f"Created {title}.")
    print("Done. Run again without --apply to confirm every routine reads 'unchanged'.")


if __name__ == "__main__":
    main()
