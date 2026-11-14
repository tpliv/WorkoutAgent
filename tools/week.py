#!/usr/bin/env python3
"""The week's schedule: one file, one tool.

data/week.json is the only place this week's sessions are written: which slot
on which date, its state, its Hevy routine. Everything else is derived from it:
the dated routines in the Hevy folder "This Week" (tools/hevy_push_routines.py)
and the Status and Sessions tables in data/weekly-plan.md (generated block).

Usage:
    python3 tools/week.py show
    python3 tools/week.py plan --week-of 2026-11-16 2026-11-17=L1@7:30-9:00am "2026-11-19=Full B" 2026-11-21=U2
    python3 tools/week.py add 2026-11-22 L3 [--time "9:00 am"] [--note "..."]
    python3 tools/week.py set 2026-11-19 --slot U1 [--date 2026-11-20] [--time ..] [--note ..] [--state missed] [--calendar "hold (Workouts)"]
    python3 tools/week.py drop 2026-11-21
    python3 tools/week.py status "week over"        # awaiting check-in | provisional | confirmed | week over
    python3 tools/week.py deload on|off
    python3 tools/week.py reconcile                 # mark logged sessions done (hevy_sync.py runs this)
    python3 tools/week.py render                    # rewrite the generated block in data/weekly-plan.md
    python3 tools/week.py brief [DATE]              # the numbers of the night-before brief for one session

Every command prints the week and its checks. A change here reaches Hevy and
GitHub with `python3 tools/hevy_sync.py`, which commits, publishes and pushes.

Checks (printed, and written into the plan):
    - order: the sessions still to come must follow the rotation from the
      pointer in data/tracks.json; the rotation never skips ahead;
    - spacing: a heavy (H) exposure of a lift the day after any exposure of it;
    - a past session with no workout logged, a logged workout that was not
      planned, a session whose logged slot differs from the planned one.
"""
import argparse
import datetime as dt
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from localtime import local_today  # noqa: E402
from update_tracks import halves, load_sessions, matcher, parse_slot, working_sets  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEEK = os.path.join(ROOT, "data", "week.json")
PLAN_MD = os.path.join(ROOT, "data", "weekly-plan.md")
TRACKS = os.path.join(ROOT, "data", "tracks.json")
ROTATION = os.path.join(ROOT, "templates", "rotation.json")
HISTORY = os.path.join(ROOT, "data", "history.csv")
ALIASES = os.path.join(ROOT, "tools", "lift_aliases.json")

STATES = ("planned", "briefed", "done", "missed")
OPEN = ("planned", "briefed")
STATUSES = ("awaiting check-in", "provisional", "confirmed", "week over")
MD_BEGIN = "<!-- week:begin -->"
MD_END = "<!-- week:end -->"
COMMENT = ("This week's sessions. The only place the schedule is written: tools/week.py edits it, "
           "tools/hevy_push_routines.py renders the dated Hevy routines from it, and the tables in "
           "data/weekly-plan.md are generated from it. Do not edit by hand; use tools/week.py.")


def load_json(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path) as f:
        return json.load(f)


def empty_week():
    return {"_comment": COMMENT, "week_of": None, "status": "awaiting check-in", "deload": False, "sessions": []}


def load_week(path=WEEK):
    week = load_json(path) or empty_week()
    week.setdefault("sessions", [])
    return week


def save_week(path, week):
    week["_comment"] = COMMENT
    week["sessions"].sort(key=lambda s: (s["date"], s.get("time") or ""))
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(week, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, path)


def day_label(date):
    d = dt.date.fromisoformat(date) if isinstance(date, str) else date
    return f"{d:%a} {d.day} {d:%b}"


def title_for(session, rotation, deload=False):
    """The dated routine's title in Hevy. It starts with the rotation title, so
    update_tracks.parse_slot reads the slot back from a logged workout."""
    if session.get("title"):
        return session["title"]
    return f"{rotation['sessions'][session['slot']]['title']}{' (deload)' if deload else ''} ({day_label(session['date'])})"


def week_span(week):
    if not week.get("week_of"):
        return None, None
    start = dt.date.fromisoformat(week["week_of"])
    return start, start + dt.timedelta(days=6)


def is_deload(week, as_of):
    start, end = week_span(week)
    return bool(week.get("deload")) and start is not None and start <= as_of <= end


def canonical_slot(text, rotation):
    """'full b', 'FullB', 'u1+l2', 'L1' -> the key in rotation['sessions']."""
    key = text.replace(" ", "").lower()
    for k in rotation["sessions"]:
        if k.replace(" ", "").lower() == key:
            return k
    sys.exit(f"Unknown slot {text!r}; choose from {', '.join(rotation['sessions'])}")


def owed(pointer, rotation, n):
    """The next n half-sessions from the pointer."""
    order = rotation["slots"]
    i = order.index(pointer) if pointer in order else 0
    return [order[(i + k) % len(order)] for k in range(n)]


def exposures(slot, rotation):
    """{lift: 'H' or 'V'} for one session."""
    out = {}
    for ex in rotation["sessions"].get(slot, {}).get("exercises", []):
        if ex.get("role") in ("H", "V") and ex.get("track"):
            if out.get(ex["track"]) != "H":
                out[ex["track"]] = ex["role"]
    return out


def problems(week, tracks, rotation, today):
    """Everything about the week that a person should look at. Empty is good."""
    out = []
    start, end = week_span(week)
    sessions = sorted(week["sessions"], key=lambda s: s["date"])
    for s in sessions:
        if s["slot"] not in rotation["sessions"]:
            out.append(f"{day_label(s['date'])}: slot {s['slot']!r} is not in the rotation")
        d = dt.date.fromisoformat(s["date"])
        if start and not (start <= d <= end):
            out.append(f"{day_label(s['date'])} {s['slot']}: outside the week of {week['week_of']}")
        if s.get("state") in OPEN and d < today:
            out.append(f"{day_label(s['date'])} {s['slot']}: no workout logged and still marked {s['state']}. "
                       "Ask before assuming; then `week.py set <date> --state missed` or move it")
        if s.get("planned_slot") and s["planned_slot"] != s["slot"]:
            out.append(f"{day_label(s['date'])}: planned {s['planned_slot']}, logged {s['slot']}")
        if s.get("unplanned"):
            out.append(f"{day_label(s['date'])} {s['slot']}: logged but was not in the plan")
    todo = [s for s in sessions if s.get("state") in OPEN and s["slot"] in rotation["sessions"]
            and dt.date.fromisoformat(s["date"]) >= today]
    pointer = (tracks or {}).get("pointer")
    if pointer and todo:
        planned = [h for s in todo for h in halves(s["slot"], rotation)]
        expect = owed(pointer, rotation, len(planned))
        if planned != expect:
            k = next(i for i, (a, b) in enumerate(zip(planned, expect)) if a != b)
            out.append(f"order: the pointer is at {pointer}, so the sessions to come should cover "
                       f"{', '.join(expect)}; the plan has {', '.join(planned)} "
                       f"({expect[k]} is owed before {planned[k]}; the rotation never skips ahead)")
    last = {}
    for s in sessions:
        if s.get("state") == "missed" or s["slot"] not in rotation["sessions"]:
            continue
        d = dt.date.fromisoformat(s["date"])
        for lift, role in exposures(s["slot"], rotation).items():
            prev = last.get(lift)
            if prev and role == "H" and (d - prev[0]).days == 1 and s.get("state") in OPEN:
                name = ((tracks or {}).get("tracks", {}).get(lift) or {}).get("name", lift)
                out.append(f"spacing: {name} {prev[1]} on {day_label(prev[0])}, then H the next day ({day_label(d)}); "
                           "48 h is preferred (guide/03, \"Consecutive days\")")
            last[lift] = (d, role)
    return out


def reconcile(week, logged, rotation, today):
    """Fold the logged workouts into the week. `logged` is
    update_tracks.load_sessions output. Returns notes for the person."""
    notes = []
    start, end = week_span(week)
    if start is None:
        return notes
    for (date, title, wid), _rows in logged:
        d = dt.date.fromisoformat(date)
        if not (start <= d <= end):
            continue
        slot = parse_slot(title)
        same_day = [s for s in week["sessions"] if s["date"] == date]
        if any(s.get("workout_id") == wid and wid for s in same_day):
            continue
        if slot and any(s["slot"] == slot and s.get("state") == "done" and not s.get("workout_id") for s in same_day):
            next(s for s in same_day if s["slot"] == slot and s.get("state") == "done" and not s.get("workout_id"))["workout_id"] = wid
            continue
        open_same = [s for s in same_day if s.get("state") in OPEN]
        match = next((s for s in open_same if s["slot"] == slot), None) or (open_same[0] if open_same else None)
        if slot is None or slot not in rotation["sessions"]:
            notes.append(f"{day_label(date)}: workout {title!r} names no rotation slot; ask which session it was")
            continue
        if match is None:
            week["sessions"].append({"date": date, "slot": slot, "state": "done", "unplanned": True, "workout_id": wid})
            notes.append(f"{day_label(date)}: {slot} was logged but not planned; added to the week")
            continue
        if match["slot"] != slot:
            notes.append(f"{day_label(date)}: planned {match['slot']}, logged {slot}; recorded as {slot}. "
                         "Re-plan the rest of the week from the pointer")
            match["planned_slot"] = match["slot"]
            match["slot"] = slot
            match.pop("title", None)
        match["state"] = "done"
        match["workout_id"] = wid
    return notes


def fmt(x):
    return f"{x:g}"


def planned_summary(slot, rotation, tracks, day, deload=False):
    """'Deadlift H 170 x 4, back-offs 2 x 4 at 160; press V 2 x 5 at 65', from
    the same renderer that builds the Hevy routine."""
    import hevy_push_routines as push  # late: that module imports this one
    session = rotation["sessions"][slot]
    parts = []
    for ex in session["exercises"]:
        if ex.get("role") not in ("H", "V"):
            continue
        sets, notes = push.render_exercise(ex, tracks, day, deload=deload, merged=bool(session.get("merged")),
                                           rotation_subs=rotation.get("substitutes"))
        work = [s for s in sets if s["type"] == "normal"]
        name = tracks["tracks"][ex["track"]]["name"]
        role = "H" if "TOP SET MOVED HERE" in notes else ex["role"]

        def reps(s):
            rr = s.get("rep_range")
            return f"{rr['start']}-{rr['end']}" if rr else str(s.get("reps"))
        groups = []
        for s in work:
            key = (s.get("weight_lb"), reps(s))
            if groups and groups[-1][0] == key:
                groups[-1][1] += 1
            else:
                groups.append([key, 1])
        bits = []
        for i, ((w, r), n) in enumerate(groups):
            at = "work up" if w is None else fmt(w)
            if role == "H" and tracks["tracks"][ex["track"]].get("scheme", "top_set") == "top_set" and len(groups) > 1:
                bits.append(f"{at} x {r}" if i == 0 else f"back-offs {n} x {r} at {at}")
            else:
                bits.append(f"{n} x {r} at {at}")
        parts.append(f"{name} {role} " + ", ".join(bits))
    return "; ".join(parts)


def logged_summary(rows, aliases, tracks):
    """Best set per main lift from the logged rows: 'Deadlift 160 x 5 @ 8'."""
    match = matcher(aliases)
    parts = []
    for lift, t in tracks["tracks"].items():
        sets = [r for r in working_sets([r for r in rows if match.get(lift, lambda n: False)(r.get("exercise"))])
                if r["_w"] is not None]
        if not sets:
            continue
        best = max(sets, key=lambda r: (r["_w"], r["_reps"]))
        rpe = f" @ {best['_rpe']:g}" if best["_rpe"] is not None else ""
        parts.append(f"{t['name']} {fmt(best['_w'])} x {int(best['_reps'])}{rpe}")
    return "; ".join(parts) or "no main lift logged"


def brief(session, week, tracks, rotation, exmap, pointer_note=True):
    """The numbers of the night-before brief (guide/08 section 3.1) for one
    session, from the same renderer as the Hevy routine, so the message and the
    app cannot disagree. The coach adds the short-on-time line and any context."""
    import re
    import hevy_push_routines as push  # late: that module imports this one
    day = dt.date.fromisoformat(session["date"])
    deload = is_deload(week, day)
    slot = session["slot"]
    sess = rotation["sessions"][slot]
    payload, _ = push.build_routine(slot, rotation, tracks, exmap, day, deload=deload)
    minutes = re.search(r"about (\d+) min", payload["notes"])
    order = rotation["slots"]
    after = order[(order.index(halves(slot, rotation)[-1]) + 1) % len(order)]
    lines = [f"{day_label(day)}: {title_for(session, rotation, deload)}   ~{minutes.group(1) if minutes else '?'} min   pointer {tracks.get('pointer')} -> {after}"]
    why = []
    if deload:
        why.append("deload week")
    letters = {}
    n = 0
    for ex, rendered in zip(sess["exercises"], payload["exercises"]):
        sets, notes = push.render_exercise(ex, tracks, day, deload=deload, merged=bool(sess.get("merged")), rotation_subs=rotation.get("substitutes"))
        warm = [s for s in sets if s["type"] == "warmup"]
        work = [s for s in sets if s["type"] == "normal"]
        if ex.get("superset"):
            if ex["superset"] not in letters:
                n += 1
                letters[ex["superset"]] = [n, 0]
            letters[ex["superset"]][1] += 1
            num = f"{letters[ex['superset']][0]}{chr(96 + letters[ex['superset']][1])}."
        else:
            n += 1
            num = f"{n}."
        role = ex.get("role")
        track = tracks["tracks"].get(ex.get("track") or "", {})
        moved = "TOP SET MOVED HERE" in notes
        tag = f" ({ex['track'].replace('pullup', 'pull-up')} {'H, moved here' if moved else role})" if role in ("H", "V") else ""

        def reps(x):
            rr = x.get("rep_range")
            return f"{rr['start']}-{rr['end']}" if rr else str(x.get("reps"))

        def load(x):
            return "work up" if x.get("weight_lb") is None and role in ("H", "V") else ("your logged load" if x.get("weight_lb") is None else fmt(x["weight_lb"]))
        groups = []
        for x in work:
            key = (load(x), reps(x))
            if groups and groups[-1][0] == key:
                groups[-1][1] += 1
            else:
                groups.append([key, 1])
        top_set = role in ("H", "V") and (role == "H" or moved) and track.get("scheme", "top_set") == "top_set" and len(groups) > 1
        if top_set:
            (w0, r0), _n0 = groups[0]
            body = f"{w0} x {r0} @ RPE {'6-7' if deload else '8'}, then " + ", ".join(f"{k} x {r} @ {w}" for (w, r), k in groups[1:])
        else:
            body = ", ".join(f"{k} x {r} @ {w}" for (w, r), k in groups)
        if ex.get("per_leg"):
            body += " per leg"
        rest = ex.get("rest")
        rest_txt = ""
        if rest:
            rt = ex.get("rest_top")
            rest_txt = f"   rest {push.mmss(rt)} after the top set, then {push.mmss(rest)}" if rt and rt != rest else f"   rest {push.mmss(rest)}"
        head = f"{num} {ex['name']}{tag}"
        if warm:
            head += "   " + ("warm-up " if len(warm) > 1 else "feeder ") + ", ".join(f"{fmt(x['weight_lb'])} x {x['reps']}" for x in warm)
        lines.append(head)
        lines.append(f"   {body}{rest_txt}" + ("   (optional)" if ex.get("optional") else ""))
        for sent in re.split(r"(?<=[.!?]) ", notes):
            if sent.startswith(("Gap ", "TOP SET MOVED", "Last back-off: REP-OUT")):
                why.append(f"{ex['name']}: {sent.rstrip('.')}")
            if sent.startswith("Station taken") and role == "H":
                lines.append(f"   {sent}")
    if session.get("note"):
        why.append(session["note"])
    lines.insert(1, "Why anything changed: " + ("; ".join(why) if why else "nothing; all tracks normal."))
    lines.append(f"After: log it in Hevy from \"{title_for(session, rotation, deload)}\" (folder This Week) and rate each top set.")
    return "\n".join(lines)


def table_rows(week, tracks, rotation, logged, aliases):
    by_key = {}
    for (date, title, wid), rows in logged or []:
        by_key.setdefault(date, []).append((title, wid, rows))
    out = []
    for s in sorted(week["sessions"], key=lambda s: (s["date"], s.get("time") or "")):
        day = dt.date.fromisoformat(s["date"])
        valid = s["slot"] in rotation["sessions"]
        if s.get("state") == "done":
            hits = by_key.get(s["date"], [])
            hit = next((h for h in hits if h[1] == s.get("workout_id")), None) or \
                next((h for h in hits if parse_slot(h[0]) == s["slot"]), None)
            main = ("Logged: " + logged_summary(hit[2], aliases, tracks)) if hit else "Done (not in the pulled history)"
        elif s.get("state") == "missed":
            main = "Missed"
        elif valid:
            main = planned_summary(s["slot"], rotation, tracks, day, deload=is_deload(week, day))
        else:
            main = "?"
        out.append({"date": s["date"], "when": f"{day:%a}" + (f" {s['time']}" if s.get("time") else ""),
                    "routine": title_for(s, rotation) if valid else s["slot"], "main": main,
                    "calendar": s.get("calendar") or "none", "state": s.get("state", "planned"),
                    "note": s.get("note") or ""})
    return out


def render_block(week, tracks, rotation, logged, aliases, today):
    start, _ = week_span(week)
    days = sorted({s["date"] for s in week["sessions"] if s.get("state") != "missed"})
    checks = problems(week, tracks, rotation, today)
    lines = [MD_BEGIN,
             "Generated by `tools/week.py` from `data/week.json` and `data/tracks.json`. Do not edit between the markers; "
             "change the week with `python3 tools/week.py` and run `python3 tools/hevy_sync.py`.",
             "",
             "| Item | Value |", "|---|---|",
             f"| Status | **{week.get('status')}** (values: {', '.join(STATUSES)}) |",
             f"| Week of | {day_label(start) + ' ' + str(start.year) if start else 'not set'} |",
             f"| Days | {len(days)}" + (f" ({', '.join(dt.date.fromisoformat(d).strftime('%a') for d in days)})" if days else "") + " |",
             f"| Block week | {tracks.get('block_week')} of 6 |",
             f"| Deload | {'Yes' if week.get('deload') else 'No'} |",
             f"| Pointer | {tracks.get('pointer')} (the next half-session owed) |",
             f"| Checks | {'; '.join(checks) if checks else 'none'} |",
             "",
             "| Date | Day and time | Hevy routine (folder This Week) | Main lifts and loads (lb) | Calendar | State |",
             "|---|---|---|---|---|---|"]
    rows = table_rows(week, tracks, rotation, logged, aliases)
    for r in rows:
        lines.append(f"| {r['date']} | {r['when']} | {r['routine']} | {r['main']} | {r['calendar']} | {r['state']} |")
    if not rows:
        lines.append("| - | - | - | No sessions planned | - | - |")
    noted = [r for r in rows if r["note"]]
    if noted:
        lines += ["", "Session notes (they lead the routine note in Hevy):", ""]
        lines += [f"- {day_label(r['date'])}: {r['note']}" for r in noted]
    lines += ["", f"State values: {', '.join(STATES)}.", MD_END]
    return "\n".join(lines)


def write_plan_md(path, block):
    with open(path) as f:
        text = f.read()
    if MD_BEGIN not in text or MD_END not in text:
        sys.exit(f"{path} has no {MD_BEGIN} / {MD_END} markers; block not written.")
    head, rest = text.split(MD_BEGIN, 1)
    _, tail = rest.split(MD_END, 1)
    new = head + block + tail
    if new != text:
        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            f.write(new)
        os.replace(tmp, path)
    return new != text


def print_week(week, tracks, rotation, logged, aliases, today):
    print(f"Week of {week.get('week_of')}  status: {week.get('status')}  deload: {'yes' if week.get('deload') else 'no'}  "
          f"pointer: {tracks.get('pointer')}  block week: {tracks.get('block_week')}  today: {today}")
    for r in table_rows(week, tracks, rotation, logged, aliases):
        print(f"  {r['date']} {r['when']:<18} {r['state']:<8} {r['routine']}")
        print(f"      {r['main']}")
    checks = problems(week, tracks, rotation, today)
    print("Checks: " + ("none" if not checks else ""))
    for c in checks:
        print("  - " + c)


def find(week, date):
    hits = [s for s in week["sessions"] if s["date"] == date]
    if not hits:
        sys.exit(f"No session on {date}. Sessions: {', '.join(s['date'] + ' ' + s['slot'] for s in week['sessions']) or 'none'}")
    if len(hits) > 1:
        sys.exit(f"Two sessions on {date}; edit data/week.json for this one")
    return hits[0]


def assign_ids(week, pool):
    """Give each open session a dated routine from the pool (Hevy cannot delete
    routines, so the same ones are reused every week)."""
    used = {s.get("routine_id") for s in week["sessions"] if s.get("routine_id")}
    free = [i for i in pool if i not in used]
    for s in sorted(week["sessions"], key=lambda s: s["date"]):
        if s.get("state") in OPEN and not s.get("routine_id") and free:
            s["routine_id"] = free.pop(0)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0], formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--week", default=WEEK)
    ap.add_argument("--tracks", default=TRACKS)
    ap.add_argument("--rotation", default=ROTATION)
    ap.add_argument("--history", default=HISTORY)
    ap.add_argument("--plan-md", default=PLAN_MD)
    ap.add_argument("--state", default=os.path.join(ROOT, "data", "hevy-state.json"))
    ap.add_argument("--today", help="override today's date (YYYY-MM-DD)")
    ap.add_argument("--dry-run", action="store_true", help="show the result, write nothing")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("show")
    p = sub.add_parser("plan", help="replace the week")
    p.add_argument("--week-of", required=True, help="the Monday (YYYY-MM-DD)")
    p.add_argument("--status", default="confirmed", choices=STATUSES)
    p.add_argument("--deload", action="store_true")
    p.add_argument("--keep-done", action="store_true", help="keep sessions already done (re-planning mid-week)")
    p.add_argument("sessions", nargs="*", help="DATE=SLOT or DATE=SLOT@TIME")
    p = sub.add_parser("add")
    p.add_argument("date"), p.add_argument("slot")
    p.add_argument("--time"), p.add_argument("--note"), p.add_argument("--calendar")
    p = sub.add_parser("set")
    p.add_argument("date")
    p.add_argument("--slot"), p.add_argument("--date", dest="new_date"), p.add_argument("--time")
    p.add_argument("--note"), p.add_argument("--state", choices=STATES), p.add_argument("--calendar")
    p = sub.add_parser("drop")
    p.add_argument("date")
    p = sub.add_parser("status")
    p.add_argument("value", choices=STATUSES)
    p = sub.add_parser("deload")
    p.add_argument("value", choices=("on", "off"))
    sub.add_parser("reconcile")
    sub.add_parser("render")
    p = sub.add_parser("brief", help="print a session's numbers for the night-before brief")
    p.add_argument("date", nargs="?", help="default: the next open session")
    args = ap.parse_args(argv)

    week = load_week(args.week)
    tracks = load_json(args.tracks)
    rotation = load_json(args.rotation)
    aliases = load_json(ALIASES, {})
    today = dt.date.fromisoformat(args.today) if args.today else local_today()
    pool = ((load_json(args.state, {}) or {}).get("this_week") or {}).get("routine_ids") or []
    cmd = args.cmd or "show"

    if cmd == "plan":
        monday = dt.date.fromisoformat(args.week_of)
        if monday.weekday() != 0:
            sys.exit(f"--week-of {args.week_of} is a {monday:%A}; give the Monday")
        kept = [s for s in week["sessions"] if args.keep_done and s.get("state") == "done"
                and monday <= dt.date.fromisoformat(s["date"]) <= monday + dt.timedelta(days=6)]
        new = []
        for item in args.sessions:
            if "=" not in item:
                sys.exit(f"{item!r}: write DATE=SLOT or DATE=SLOT@TIME")
            date, rest = item.split("=", 1)
            slot, _, time = rest.partition("@")
            dt.date.fromisoformat(date)
            s = {"date": date, "slot": canonical_slot(slot, rotation), "state": "planned"}
            if time:
                s["time"] = time.strip()
            new.append(s)
        week = {"week_of": args.week_of, "status": args.status, "deload": bool(args.deload), "sessions": kept + new}
    elif cmd == "add":
        dt.date.fromisoformat(args.date)
        s = {"date": args.date, "slot": canonical_slot(args.slot, rotation), "state": "planned"}
        for k in ("time", "note", "calendar"):
            if getattr(args, k):
                s[k] = getattr(args, k)
        week["sessions"].append(s)
    elif cmd == "set":
        s = find(week, args.date)
        if args.slot:
            s["slot"] = canonical_slot(args.slot, rotation)
            s.pop("title", None)
        if args.new_date:
            dt.date.fromisoformat(args.new_date)
            s["date"] = args.new_date
            s.pop("title", None)
        for k in ("time", "note", "state", "calendar"):
            v = getattr(args, k)
            if v is not None:
                if v == "":
                    s.pop(k, None)
                else:
                    s[k] = v
    elif cmd == "drop":
        week["sessions"].remove(find(week, args.date))
    elif cmd == "status":
        week["status"] = args.value
    elif cmd == "deload":
        week["deload"] = args.value == "on"

    if cmd == "brief":
        todo = [x for x in sorted(week["sessions"], key=lambda x: x["date"]) if x.get("state") in OPEN]
        if args.date:
            session = find(week, args.date)
        elif todo:
            session = next((x for x in todo if dt.date.fromisoformat(x["date"]) >= today), todo[0])
        else:
            sys.exit("No open session in data/week.json.")
        exmap = load_json(os.path.join(ROOT, "data", "hevy-exercise-map.json"), {}) or {}
        print(brief(session, week, tracks, rotation, exmap))
        return

    logged = load_sessions(args.history, since=week.get("week_of")) if week.get("week_of") and os.path.exists(args.history) else []
    notes = reconcile(week, logged, rotation, today) if cmd != "show" else []
    assign_ids(week, pool)
    print_week(week, tracks, rotation, logged, aliases, today)
    for n in notes:
        print("Note: " + n)
    if cmd == "show" or args.dry_run:
        if args.dry_run and cmd != "show":
            print("(dry run: nothing written)")
        return
    save_week(args.week, week)
    if os.path.exists(args.plan_md):
        write_plan_md(args.plan_md, render_block(week, tracks, rotation, logged, aliases, today))
    print(f"Wrote {os.path.relpath(args.week)}; plan tables regenerated. "
          "Run `python3 tools/hevy_sync.py` to commit, publish and push it to Hevy.")


if __name__ == "__main__":
    main()
