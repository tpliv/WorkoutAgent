#!/usr/bin/env python3
"""Analyze data/history.csv and propose starting loads for the six main lifts.

Usage:
    python3 tools/analyze_history.py [--history data/history.csv] [--aliases tools/lift_aliases.json]
                                     [--list-exercises] [--years] [--md data/history-summary.md]

What it does:
  1. Per-exercise summary: first and last date, number of sessions, best
     estimated 1RM (e1RM) ever and in the last 8 weeks, with the set it came from.
  2. Training-frequency summary by year (sessions per week) so old history can be
     read in context.
  3. For each main lift (mapped through lift_aliases.json), a proposed starting
     top-set load for the program's progression track, following
     templates/progression-tracks.md section 2:
       - data within the last 8 weeks:   80% of the recent best e1RM
       - data 8 weeks to 1 year old:     85% of the old top-set estimate, first
                                         exposure at RPE 6-7 (section 8 ramp)
       - data older than 1 year:         "work up" on the first H exposure;
                                         the old e1RM is shown for reference only
  e1RM uses Epley: load x (1 + reps/30). When an RPE is logged, reps are
  extended by (10 - RPE) reps in reserve before applying Epley. Sets with more
  than 12 reps, warm-up sets, or bodyweight-only rows are not used for e1RM.
"""
import argparse
import collections
import csv
import datetime as dt
import json
import math
import sys


def epley(load, reps, rpe=None):
    eff = reps + (10 - rpe) if rpe not in (None, "") else reps
    return load * (1 + eff / 30.0)


def load_history(path):
    rows = []
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            # Accept the manual log template too: 'session' and 'load' or 'load_lb' (pounds)
            # instead of 'workout_title' and 'weight_kg'.
            if "workout_title" not in r and "session" in r:
                r["workout_title"] = r["session"]
            lb = r.get("load_lb", r.get("load"))
            if "weight_kg" not in r and lb is not None:
                r["weight_kg"] = str(float(lb) * 0.45359237) if lb != "" else ""
            try:
                d = dt.date.fromisoformat(r["date"][:10])
            except ValueError:
                continue
            try:
                w = float(r["weight_kg"]) if r["weight_kg"] not in ("", None) else None
                reps = int(float(r["reps"])) if r["reps"] not in ("", None) else None
                rpe = float(r["rpe"]) if r.get("rpe") not in ("", None) else None
            except ValueError:
                continue
            rows.append({"date": d, "exercise": (r["exercise"] or "").strip(), "title": r.get("workout_title", ""),
                         "set_type": (r.get("set_type") or "normal").lower(), "w": w, "reps": reps, "rpe": rpe})
    return rows


def usable(r):
    return r["w"] and r["w"] > 0 and r["reps"] and 1 <= r["reps"] <= 12 and r["set_type"] not in ("warmup", "warm-up", "warm_up")


def round_plate(x, step=2.5):
    return math.floor(x / step) * step


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--history", default="data/history.csv")
    ap.add_argument("--aliases", default="tools/lift_aliases.json")
    ap.add_argument("--list-exercises", action="store_true")
    ap.add_argument("--md", default="data/history-summary.md", help="also write a Markdown summary here ('' to skip)")
    ap.add_argument("--today", help="override today's date (YYYY-MM-DD) for reproducible output")
    args = ap.parse_args()

    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    rows = load_history(args.history)
    if not rows:
        sys.exit(f"No usable rows in {args.history}.")

    by_ex = collections.defaultdict(list)
    for r in rows:
        by_ex[r["exercise"]].append(r)

    if args.list_exercises:
        for ex, rs in sorted(by_ex.items(), key=lambda kv: -len(kv[1])):
            sessions = len({r["date"] for r in rs})
            print(f"{sessions:4d} sessions  {min(r['date'] for r in rs)} .. {max(r['date'] for r in rs)}  {ex}")
        return

    out = []
    p = out.append
    p(f"# Training history summary\n\nGenerated {today} from `{args.history}` ({len(rows)} sets).\n")

    # 1. frequency by year
    sessions = collections.defaultdict(set)
    for r in rows:
        sessions[r["date"].year].add(r["date"])
    p("## Sessions per year\n\n| Year | Sessions | Weeks with a session | Sessions per active week |\n|---|---|---|---|")
    for y in sorted(sessions):
        days = sessions[y]
        weeks = {d.isocalendar()[:2] for d in days}
        p(f"| {y} | {len(days)} | {len(weeks)} | {len(days)/max(1,len(weeks)):.1f} |")
    first, last = min(r["date"] for r in rows), max(r["date"] for r in rows)
    p(f"\nFirst logged session {first}, last {last} ({(today-last).days} days ago).\n")

    # 2. per-exercise summary
    p("## Exercises\n\n| Exercise | Sessions | First | Last | Best e1RM (kg) | Best set | Best e1RM last 8 wk |\n|---|---|---|---|---|---|---|")
    ex_stats = {}
    for ex, rs in sorted(by_ex.items(), key=lambda kv: -len({r['date'] for r in kv[1]})):
        us = [r for r in rs if usable(r)]
        best = max(us, key=lambda r: epley(r["w"], r["reps"], r["rpe"]), default=None)
        recent = [r for r in us if (today - r["date"]).days <= 56]
        best_recent = max(recent, key=lambda r: epley(r["w"], r["reps"], r["rpe"]), default=None)
        ex_stats[ex] = {"sessions": len({r["date"] for r in rs}), "first": min(r["date"] for r in rs),
                        "last": max(r["date"] for r in rs), "best": best, "best_recent": best_recent, "sets": us}
        if ex_stats[ex]["sessions"] < 3:
            continue
        b = f"{epley(best['w'], best['reps'], best['rpe']):.0f}" if best else "-"
        bs = f"{best['w']:g} x {best['reps']}" + (f" @{best['rpe']:g}" if best and best['rpe'] else "") + f" on {best['date']}" if best else "-"
        br = f"{epley(best_recent['w'], best_recent['reps'], best_recent['rpe']):.0f}" if best_recent else "-"
        p(f"| {ex} | {ex_stats[ex]['sessions']} | {ex_stats[ex]['first']} | {ex_stats[ex]['last']} | {b} | {bs} | {br} |")

    # 3. main-lift starting loads
    aliases = json.load(open(args.aliases))
    p("\n## Proposed starting loads for the progression tracks\n")
    p("Rule source: `templates/progression-tracks.md`, section 2 (recent data) and section 8 (returning after a layoff). Proposed loads are rounded down to 5 lb; the kg column is that rounded load converted.\n")
    p("Squat, bench, deadlift, press: the top set of 4 at RPE 8. Row and pull-up or pulldown: the load for the first set of 4 x 6-8 (row) or 4 x 5-8 (pull-up) at RPE 8, per `templates/progression-tracks.md` section 1. Pounds are rounded down to 5 lb.\n")
    p("| Lift | Matched exercises | Last trained | Best e1RM (kg) | Recent e1RM (kg) | Proposed start (lb) | Proposed start (kg) | Basis |\n|---|---|---|---|---|---|---|---|")
    for lift, names in aliases.items():
        if lift.startswith("_"):
            continue
        excl = aliases.get("_exclude", {}).get(lift, [])
        matched = [ex for ex in by_ex if any(n in ex.lower() for n in names) and not any(x in ex.lower() for x in excl)]
        sets = [r for ex in matched for r in ex_stats[ex]["sets"]]
        if not matched:
            p(f"| {lift} | (none; edit tools/lift_aliases.json) | - | - | - | work up | work up | no history |")
            continue
        if not sets:
            bw = [r for ex in matched for r in by_ex[ex] if r["reps"]]
            last = max(r["date"] for r in bw) if bw else "-"
            best = max((r["reps"] for r in bw), default=0)
            p(f"| {lift} | {', '.join(matched)} | {last} | - | - | bodyweight | best logged set {best} reps | no loaded sets; apply the added-load rule in section 2 (pull-up) |")
            continue
        last = max(r["date"] for r in sets)
        age = (today - last).days
        best = max(sets, key=lambda r: epley(r["w"], r["reps"], r["rpe"]))
        best_e = epley(best["w"], best["reps"], best["rpe"])
        recent = [r for r in sets if (today - r["date"]).days <= 56]
        recent_e = max((epley(r["w"], r["reps"], r["rpe"]) for r in recent), default=None)
        # last block's heaviest top set (best e1RM in the final 28 days of logged data for this lift)
        tail = [r for r in sets if (last - r["date"]).days <= 28]
        tail_e = max(epley(r["w"], r["reps"], r["rpe"]) for r in tail)
        KG = 0.45359237
        def lbs(x):
            return math.floor(x / KG / 5) * 5
        if age <= 56 and recent_e:
            raw, basis = 0.80 * recent_e, "80% of recent e1RM (section 2)"
        elif age <= 365:
            raw, basis = 0.85 * 0.83 * tail_e, "85% of the last block's estimated 4@8 load; first exposure at RPE 6-7 (section 8)"
        else:
            raw, basis = None, f"history is {age//30} months old: work up on the first H exposure; expect roughly {lbs(0.70*0.83*tail_e):g}-{lbs(0.83*tail_e):g} lb ({round_plate(0.70*0.83*tail_e):g}-{round_plate(0.83*tail_e):g} kg) if strength is similar (reference only)"
        # Round in pounds first (the user's plates), then show the kg equivalent of that rounded load.
        prop_lb = lbs(raw) if raw else None
        prop = round(prop_lb * KG, 1) if prop_lb else None
        lb = f"{prop_lb:g}" if prop_lb else "work up"
        p(f"| {lift} | {', '.join(matched)} | {last} | {best_e:.0f} | {f'{recent_e:.0f}' if recent_e else '-'} | {lb} | {f'{prop:g}' if prop else 'work up'} | {basis} |")

    text = "\n".join(out) + "\n"
    print(text)
    if args.md:
        with open(args.md, "w") as f:
            f.write(text)
        print(f"(written to {args.md})", file=sys.stderr)


if __name__ == "__main__":
    main()
