#!/usr/bin/env python3
"""Pull workouts from the Hevy API into data/history.csv.

Usage:
    HEVY_API_KEY=... python3 tools/hevy_pull.py            # incremental if data/hevy-state.json has last_pull, else full
    python3 tools/hevy_pull.py --full                      # re-pull everything
    python3 tools/hevy_pull.py --since 2024-01-01          # full pull, keep workouts on or after this date
    python3 tools/hevy_pull.py --inspect                   # print one raw workout and exit

Reads the key from the HEVY_API_KEY environment variable, or relies on a network-secret
proxy that adds it to requests for api.hevyapp.com. Never pass the
key on the command line or commit it.

Outputs:
    data/history.csv                normalized set-level log (tools/README.md), merged
    data/raw/hevy_workouts.jsonl    raw workout JSON, one per line (gitignored)
    data/hevy-state.json            last_pull timestamp for the next incremental run

Merge rules:
    - Full pull: every row whose source is hevy-api or hevy-csv is replaced (both
      describe the same Hevy account); rows from other sources (manual) are kept.
    - Incremental pull (GET /workouts/events?since=last_pull): updated workouts
      replace the rows with the same workout_id; deleted workouts drop them.
      Rows from the old CSV import have no workout_id and are left alone, so run
      one --full pull after the first API setup to replace the CSV import.

Schema verified against the OpenAPI document at api.hevyapp.com/docs on
2026-10-21: workouts carry title, start_time, exercises[].title,
exercises[].sets[].{index, type, weight_kg, reps, rpe}; set types are normal,
warmup, dropset, failure; RPE is per set and nullable.
"""
import argparse
import csv
import datetime as dt
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hevy_api import HISTORY_COLUMNS, Hevy, HevyError, now_iso, workout_rows  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY = os.path.join(ROOT, "data", "history.csv")
RAW = os.path.join(ROOT, "data", "raw", "hevy_workouts.jsonl")
STATE = os.path.join(ROOT, "data", "hevy-state.json")


def read_history(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def write_history(path, rows):
    rows.sort(key=lambda r: (r.get("date", ""), r.get("workout_title", ""), r.get("workout_id", ""), r.get("exercise", ""), float(r.get("set_index") or 0)))
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HISTORY_COLUMNS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in HISTORY_COLUMNS})


def load_state(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}


def save_state(path, state):
    with open(path, "w") as f:
        json.dump(state, f, indent=2)
        f.write("\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Pull Hevy workouts into data/history.csv.")
    ap.add_argument("--inspect", action="store_true", help="print one raw workout as JSON and exit")
    ap.add_argument("--full", action="store_true", help="re-pull all workouts instead of events since last_pull")
    ap.add_argument("--since", help="full pull: keep workouts on or after this date (YYYY-MM-DD)")
    ap.add_argument("--out", default=HISTORY)
    ap.add_argument("--raw", default=RAW)
    ap.add_argument("--state", default=STATE)
    args = ap.parse_args(argv)

    try:
        h = Hevy()
        if args.inspect:
            for w in h.iter_workouts(max_pages=1):
                print(json.dumps(w, indent=2, ensure_ascii=False))
                break
            return

        state = load_state(args.state)
        started = now_iso()
        existing = read_history(args.out)
        os.makedirs(os.path.dirname(args.raw), exist_ok=True)
        incremental = bool(state.get("last_pull")) and not args.full and not args.since

        if incremental:
            updated, deleted = {}, set()
            for ev in h.iter_workout_events(state["last_pull"]):
                if ev.get("type") == "deleted":
                    deleted.add(ev.get("id"))
                elif ev.get("type") == "updated" and ev.get("workout"):
                    w = ev["workout"]
                    updated.setdefault(w.get("id"), w)  # newest event first; keep it
            touched = set(updated) | deleted
            rows = [r for r in existing if r.get("workout_id") not in touched]
            n_rows = 0
            with open(args.raw, "a") as raw:
                for wid, w in updated.items():
                    raw.write(json.dumps(w) + "\n")
                    for row in workout_rows(w):
                        rows.append(row)
                        n_rows += 1
            write_history(args.out, rows)
            print(f"Incremental pull since {state['last_pull']}: {len(updated)} updated, {len(deleted)} deleted workouts, {n_rows} sets -> {args.out}")
        else:
            rows = [r for r in existing if r.get("source") not in ("hevy-api", "hevy-csv")]
            n_workouts = n_rows = 0
            with open(args.raw, "w") as raw:
                for w in h.iter_workouts():
                    date = (w.get("start_time") or "")[:10]
                    if args.since and date < args.since:
                        continue
                    raw.write(json.dumps(w) + "\n")
                    n_workouts += 1
                    for row in workout_rows(w):
                        rows.append(row)
                        n_rows += 1
            write_history(args.out, rows)
            print(f"Full pull: {n_workouts} workouts, {n_rows} sets -> {args.out} (raw JSON in {args.raw}); {len(existing) - sum(1 for r in existing if r.get('source') in ('hevy-api', 'hevy-csv'))} non-Hevy rows kept.")

        state["last_pull"] = started
        save_state(args.state, state)
    except HevyError as e:
        sys.exit(str(e))


if __name__ == "__main__":
    main()
