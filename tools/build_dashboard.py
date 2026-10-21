#!/usr/bin/env python3
"""Build the progress dashboard from the committed training data.

Usage:
    python3 tools/build_dashboard.py                    # data/ -> dashboard/index.html + dashboard/data.json
    python3 tools/build_dashboard.py --refresh-muscles  # first refresh data/exercise-muscles.json from Hevy
    python3 tools/build_dashboard.py --today 2026-10-21 # reproducible output

Reads data/history.csv, data/tracks.json, data/track-log.md (if present),
tools/lift_aliases.json and data/exercise-muscles.json. Everything is
aggregated by ISO week (Monday to Sunday) and written as one JSON blob, which
is also inlined into dashboard/template.html so index.html is a single
self-contained page. No network unless --refresh-muscles is given.

Metric rules follow guide/07-tracking-and-apps.md section 1.2:
  - Working sets: every set not typed warm-up. The log has no RPE for most
    sets, so this is an upper bound on hard sets (0-3 RIR).
  - Sets per muscle: 1 for the exercise's primary muscle group, 0.5 for each
    secondary group (fractional counting, guide/01 section 1). A set credits a
    group at most once.
  - Weekly targets per muscle by days trained: guide/03 section 3.
  - e1RM: Epley, reps extended by (10 - RPE) when an RPE is logged, sets of
    1-12 reps only (tools/analyze_history.py).
  - Gap clock: templates/progression-tracks.md section 8.
Tonnage is load x reps over working sets with a load, as logged (dumbbell
loads are per dumbbell; assisted exercises are left out).
"""
import argparse
import collections
import datetime as dt
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from analyze_history import epley  # noqa: E402
from update_tracks import load_sessions, matcher  # noqa: E402

HISTORY = os.path.join(ROOT, "data", "history.csv")
TRACKS = os.path.join(ROOT, "data", "tracks.json")
TRACK_LOG = os.path.join(ROOT, "data", "track-log.md")
ALIASES = os.path.join(ROOT, "tools", "lift_aliases.json")
ROTATION = os.path.join(ROOT, "templates", "rotation.json")
MUSCLES = os.path.join(ROOT, "data", "exercise-muscles.json")
OUT_DIR = os.path.join(ROOT, "dashboard")
TEMPLATE = os.path.join(OUT_DIR, "template.html")
PLACEHOLDER = "/*__DASHBOARD_DATA__*/null"

WARMUP = ("warmup", "warm-up", "warm_up")

# Display groups from guide/01 section 1 and the Hevy muscle groups that feed them.
GROUPS = [("chest", "Chest"), ("back", "Back"), ("shoulders", "Shoulders"), ("biceps", "Biceps"),
          ("triceps", "Triceps"), ("quads", "Quads"), ("hams_glutes", "Hamstrings and glutes"),
          ("calves", "Calves"), ("abs", "Abs")]
HEVY_TO_GROUP = {"chest": "chest", "lats": "back", "upper_back": "back", "traps": "back",
                 "shoulders": "shoulders", "biceps": "biceps", "triceps": "triceps",
                 "quadriceps": "quads", "hamstrings": "hams_glutes", "glutes": "hams_glutes",
                 "calves": "calves", "abdominals": "abs"}

# Used only for titles missing from data/exercise-muscles.json. First match wins.
KEYWORDS = [
    ("romanian", "hamstrings", ["glutes", "lower_back"]), ("leg curl", "hamstrings", []),
    ("deadlift", "glutes", ["hamstrings", "lower_back"]), ("hip thrust", "glutes", ["hamstrings"]),
    ("squat", "quadriceps", ["glutes"]), ("lunge", "quadriceps", ["glutes"]), ("leg press", "quadriceps", ["glutes"]),
    ("leg extension", "quadriceps", []), ("calf", "calves", []),
    ("bench", "chest", ["triceps", "shoulders"]), ("fly", "chest", []), ("push up", "chest", ["triceps"]),
    ("dip", "triceps", ["chest"]), ("triceps", "triceps", []), ("skull", "triceps", []),
    ("overhead press", "shoulders", ["triceps"]), ("shoulder press", "shoulders", ["triceps"]),
    ("arnold", "shoulders", ["triceps"]), ("lateral raise", "shoulders", []), ("face pull", "shoulders", ["upper_back"]),
    ("curl", "biceps", []), ("pull up", "lats", ["biceps"]), ("chin up", "lats", ["biceps"]),
    ("pulldown", "lats", ["biceps"]), ("row", "upper_back", ["lats", "biceps"]), ("shrug", "traps", []),
    ("crunch", "abdominals", []), ("plank", "abdominals", []), ("leg raise", "abdominals", []), ("twist", "abdominals", []),
]

# templates/progression-tracks.md section 8.
GAP_BANDS = [(7, "normal", "Normal"), (14, "hold", "Hold the top-set load"),
             (21, "hold-", "Hold, one fewer back-off"), (28, "reduce5", "Reduce 5%")]

# guide/03-flexible-scheduling.md section 3: weekly hard sets per large muscle group.
TARGETS = {0: None, 1: (4, 6), 2: (4, 6), 3: (8, 12), 4: (10, 14), 5: (14, 17), 6: (15, 20), 7: (15, 20)}

LIFT_ORDER = ["squat", "bench", "deadlift", "press", "row", "pullup"]


def monday(d):
    return d - dt.timedelta(days=d.weekday())


def gap_band(days):
    if days is None:
        return {"key": "none", "label": "Never trained"}
    for limit, key, label in GAP_BANDS:
        if days <= limit:
            return {"key": key, "label": label}
    return {"key": "reduce10", "label": "Reduce 10%"}


def load_json(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path) as f:
        return json.load(f)


def muscle_info(title, muscles):
    m = muscles.get(title)
    if m:
        return m, True
    low = title.lower()
    for key, primary, secondary in KEYWORDS:
        if key in low:
            return {"primary": primary, "secondary": secondary, "type": None}, False
    return {"primary": None, "secondary": [], "type": None}, False


def set_credit(info):
    """{group: credit} for one set of an exercise; a group is credited once."""
    credit = {}
    for m in info.get("secondary") or []:
        g = HEVY_TO_GROUP.get(m)
        if g:
            credit[g] = max(credit.get(g, 0), 0.5)
    g = HEVY_TO_GROUP.get(info.get("primary"))
    if g:
        credit[g] = 1
    return credit


def parse_track_log(path, limit=12):
    if not os.path.exists(path):
        return []
    out, date = [], None
    with open(path) as f:
        for line in f:
            m = re.match(r"^##\s+(\d{4}-\d{2}-\d{2})", line)
            if m:
                date = m.group(1)
            elif line.startswith("- "):
                text = line[2:].strip()
                kind = "stall" if "STALL" in text else "flag" if text.startswith("Flag:") else "decision"
                out.append({"date": date, "text": text, "kind": kind})
    return out[-limit:]


def build(history, tracks, aliases, muscles, today, track_log=()):
    sessions = load_sessions(history)
    match = matcher(aliases)
    lifts = [k for k in LIFT_ORDER if k in match] + [k for k in match if k not in LIFT_ORDER]

    weeks = collections.OrderedDict()
    unmapped = set()
    lift_last = {}

    def week(d):
        key = monday(d).isoformat()
        if key not in weeks:
            weeks[key] = {"week": key, "sessions": 0, "days": set(), "sets": 0, "tonnage": 0.0, "reps": 0,
                          "muscles": collections.Counter(), "lifts": {}}
        return weeks[key]

    for (date, title, wid), rows in sessions:
        d = dt.date.fromisoformat(date)
        w = week(d)
        w["sessions"] += 1
        w["days"].add(date)
        for r in rows:
            if r["_type"] in WARMUP:
                continue
            ex = (r.get("exercise") or "").strip()
            info, known = muscle_info(ex, muscles)
            if not known:
                unmapped.add(ex)
            load, reps = r["_w"], int(r["_reps"] or 0)
            w["sets"] += 1
            w["reps"] += reps
            if load and load > 0 and reps > 0 and info.get("type") != "assisted_bodyweight":
                w["tonnage"] += load * reps
            for g, c in set_credit(info).items():
                w["muscles"][g] += c
            for lift in lifts:
                if not match[lift](ex):
                    continue
                lift_last[lift] = max(lift_last.get(lift, ""), date)
                if not (load and load > 0 and 1 <= reps <= 12):
                    continue
                est = epley(load, reps, r["_rpe"])
                cur = w["lifts"].get(lift)
                if cur is None or est > cur["e1rm"]:
                    cur = w["lifts"][lift] = {"e1rm": est, "load": load, "reps": reps, "rpe": r["_rpe"], "date": date,
                                              "exercise": ex, "top_load": load, "top_reps": reps, "sets": 0}
                if load > cur["top_load"] or (load == cur["top_load"] and reps > cur["top_reps"]):
                    cur["top_load"], cur["top_reps"] = load, reps
                cur["sets"] += 1

    # Fill every week from the first logged week through the current one.
    out_weeks = []
    if weeks:
        d = dt.date.fromisoformat(next(iter(weeks)))
        end = monday(today)
        last = dt.date.fromisoformat(next(reversed(weeks)))
        end = max(end, last)
        while d <= end:
            w = weeks.get(d.isoformat()) or {"week": d.isoformat(), "sessions": 0, "days": set(), "sets": 0,
                                               "tonnage": 0.0, "reps": 0, "muscles": {}, "lifts": {}}
            days = len(w["days"])
            target = TARGETS.get(min(days, 7))
            out_weeks.append({
                "week": w["week"], "sessions": w["sessions"], "days": days, "sets": w["sets"], "reps": w["reps"],
                "tonnage": round(w["tonnage"]),
                "muscles": {g: round(w["muscles"].get(g, 0), 1) for g, _ in GROUPS if w["muscles"].get(g)},
                "target": list(target) if target else None,
                "lifts": {k: {kk: (round(vv, 1) if isinstance(vv, float) else vv) for kk, vv in v.items()}
                          for k, v in w["lifts"].items()},
            })
            d += dt.timedelta(days=7)

    # Week-over-week overload: each trained week against the previous week the lift was trained.
    for lift in lifts:
        prev = None
        for w in out_weeks:
            cur = w["lifts"].get(lift)
            if not cur:
                continue
            if prev:
                delta = cur["e1rm"] - prev["e1rm"]
                pct = delta / prev["e1rm"] * 100 if prev["e1rm"] else 0
                cur["delta"] = round(delta, 1)
                cur["delta_pct"] = round(pct, 1)
                cur["prev_week"] = prev["_week"]
                weeks_apart = (dt.date.fromisoformat(w["week"]) - dt.date.fromisoformat(prev["_week"])).days // 7
                # After more than four weeks off the comparison says more about the layoff than about overload.
                cur["trend"] = ("restart" if weeks_apart > 4 else
                                "up" if pct >= 1 else "down" if pct <= -1 else "flat")
            else:
                cur["trend"] = "first"
            cur["_week"] = w["week"]
            prev = cur
        for w in out_weeks:
            if lift in w["lifts"]:
                w["lifts"][lift].pop("_week", None)

    lift_rows = []
    track_map = (tracks or {}).get("tracks", {})
    for lift in lifts:
        trained = [w for w in out_weeks if lift in w["lifts"]]
        last_date = lift_last.get(lift)
        gap = (today - dt.date.fromisoformat(last_date)).days if last_date else None
        latest = trained[-1]["lifts"][lift] if trained else None
        best = max((w["lifts"][lift]["e1rm"] for w in trained), default=None)
        recent = [w["lifts"][lift]["e1rm"] for w in trained[-6:]]
        block = None
        if len(recent) >= 6:
            block = round(sum(recent[-3:]) / 3 - sum(recent[:3]) / 3, 1)
        lift_rows.append({"key": lift, "name": track_map.get(lift, {}).get("name", lift.title()),
                          "last_date": last_date, "gap_days": gap, "gap": gap_band(gap),
                          "latest": latest, "latest_week": trained[-1]["week"] if trained else None,
                          "best_e1rm": best, "block_change": block})

    # Consistency: weekly streaks of at least one session.
    flags = [w["sessions"] > 0 for w in out_weeks]
    longest = run = 0
    for f in flags:
        run = run + 1 if f else 0
        longest = max(longest, run)
    current = 0
    tail = flags[:]
    if tail and not tail[-1]:
        tail.pop()  # the current week may not have started yet
    for f in reversed(tail):
        if not f:
            break
        current += 1
    last12 = out_weeks[-12:]
    active = [w for w in out_weeks if w["sessions"]]
    consistency = {
        "current_streak": current, "longest_streak": longest,
        "weeks_trained_last12": sum(1 for w in last12 if w["sessions"]),
        "sessions_last12": sum(w["sessions"] for w in last12),
        "avg_days_active_week": round(sum(w["days"] for w in active) / len(active), 1) if active else 0,
        "total_sessions": sum(w["sessions"] for w in out_weeks),
        "first_date": sessions[0][0][0] if sessions else None,
        "last_date": sessions[-1][0][0] if sessions else None,
    }

    track_cards = []
    for lift in lifts:
        t = track_map.get(lift)
        if not t:
            continue
        last = (t.get("last_exposure") or {}).get("date")
        gap = (today - dt.date.fromisoformat(last)).days if last else None
        track_cards.append({
            "key": lift, "name": t.get("name"), "scheme": t.get("scheme"), "next_kg": t.get("top_set_kg"),
            "last_h_kg": t.get("last_h_load_kg"), "rep_target": t.get("rep_target"), "rep_range": t.get("rep_range"),
            "miss_counter": t.get("miss_counter", 0), "stalls": t.get("stalls", 0), "work_up": bool(t.get("work_up")),
            "last_exposure": t.get("last_exposure"), "gap_days": gap, "gap": gap_band(gap),
            "e1rm_history": t.get("e1rm_history", []),
        })

    return {
        "generated": today.isoformat(), "units": (tracks or {}).get("units", "kg"),
        "groups": [{"key": k, "label": v} for k, v in GROUPS],
        "weeks": out_weeks, "lifts": lift_rows, "consistency": consistency,
        "program": {k: (tracks or {}).get(k) for k in ("pointer", "block_start", "block_week", "deload", "processed_through")},
        "tracks": track_cards, "track_log": list(track_log), "unmapped": sorted(unmapped),
    }


def render(data, template=TEMPLATE):
    with open(template) as f:
        html = f.read()
    if PLACEHOLDER not in html:
        sys.exit(f"{template} has no {PLACEHOLDER} placeholder.")
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return html.replace(PLACEHOLDER, blob)


def refresh_muscles(path, history, rotation):
    from hevy_api import Hevy
    titles = set()
    for _, rows in load_sessions(history):
        titles.update((r.get("exercise") or "").strip() for r in rows)
    rot = load_json(rotation, {})
    for s in rot.get("sessions", {}).values():
        for ex in s.get("exercises", []):
            titles.update(ex.get("hevy", []))
    current = load_json(path, {})
    index = Hevy().exercise_template_index()
    missing = []
    for title in sorted(t for t in titles if t):
        tpl = index.get(title.lower())
        if not tpl:
            missing.append(title)
            continue
        current[title] = {"primary": tpl.get("primary_muscle_group"),
                          "secondary": tpl.get("secondary_muscle_groups") or [], "type": tpl.get("type")}
    with open(path, "w") as f:
        json.dump(dict(sorted(current.items())), f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Wrote {len(current)} exercises to {os.path.relpath(path, ROOT)}.")
    if missing:
        print("Not found in Hevy (keyword fallback applies): " + ", ".join(missing))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--history", default=HISTORY)
    ap.add_argument("--tracks", default=TRACKS)
    ap.add_argument("--aliases", default=ALIASES)
    ap.add_argument("--muscles", default=MUSCLES)
    ap.add_argument("--log", default=TRACK_LOG)
    ap.add_argument("--out", default=OUT_DIR, help="output directory for index.html and data.json")
    ap.add_argument("--today", help="override today's date (YYYY-MM-DD)")
    ap.add_argument("--refresh-muscles", action="store_true", help="refresh data/exercise-muscles.json from Hevy first")
    args = ap.parse_args(argv)

    if args.refresh_muscles:
        refresh_muscles(args.muscles, args.history, ROTATION)
    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    data = build(args.history, load_json(args.tracks, {}), load_json(args.aliases, {}),
                 load_json(args.muscles, {}), today, parse_track_log(args.log))
    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out, "data.json"), "w") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
        f.write("\n")
    with open(os.path.join(args.out, "index.html"), "w") as f:
        f.write(render(data))
    w = [x for x in data["weeks"] if x["sessions"]]
    print(f"Dashboard: {len(data['weeks'])} weeks ({len(w)} trained), {data['consistency']['total_sessions']} sessions "
          f"-> {os.path.relpath(os.path.join(args.out, 'index.html'), ROOT)}")
    if data["unmapped"]:
        print("No muscle map entry (keyword fallback used): " + ", ".join(data["unmapped"]))


if __name__ == "__main__":
    main()
