#!/usr/bin/env python3
"""Convert a Hevy app CSV export (Profile > Settings > Export & Import Data) into
data/history.csv, the normalized set-level log the analysis tools read.

Usage:
    python3 tools/hevy_csv_import.py path/to/hevy_export.csv [--out data/history.csv] [--lb]

Hevy's export column names were not verifiable from the research sandbox, so
this script matches columns by name loosely (case-insensitive, ignoring spaces
and underscores). It looks for: a workout title, a start time or date, an
exercise title, a set index, a set type, a weight (kg or lb), reps, and RPE.
It prints which column it used for each field so a mismatch is obvious. Pass
--lb if the export's weight column is in pounds.
"""
import argparse
import csv
import os
import re
import sys

HISTORY_COLUMNS = [
    "date", "workout_title", "exercise", "set_index", "set_type",
    "weight_kg", "reps", "rpe", "notes", "source",
]

CANDIDATES = {
    "workout_title": ["title", "workouttitle", "workoutname", "workout"],
    "date": ["starttime", "startdate", "date", "workoutstart"],
    "exercise": ["exercisetitle", "exercisename", "exercise"],
    "set_index": ["setindex", "setorder", "setnumber", "set"],
    "set_type": ["settype", "type"],
    "weight": ["weightkg", "weightlbs", "weightlb", "weight"],
    "reps": ["reps", "repetitions"],
    "rpe": ["rpe"],
    "notes": ["exercisenotes", "notes", "description"],
}


def norm(s):
    return re.sub(r"[^a-z]", "", s.lower())


def pick(headers, wanted):
    normed = {norm(h): h for h in headers}
    for cand in wanted:
        if cand in normed:
            return normed[cand]
    return None


def parse_date(s):
    s = s.strip()
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return m.group(0)
    for fmt in ("%d %b %Y, %H:%M", "%d %b %Y", "%m/%d/%Y %H:%M", "%m/%d/%Y", "%d/%m/%Y"):
        try:
            import datetime
            return datetime.datetime.strptime(s, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return s[:10]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("export_csv")
    ap.add_argument("--out", default="data/history.csv")
    ap.add_argument("--force", action="store_true", help="overwrite a history file that holds API rows")
    ap.add_argument("--lb", action="store_true", help="weights in the export are pounds")
    args = ap.parse_args()

    with open(args.export_csv, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        cols = {k: pick(headers, v) for k, v in CANDIDATES.items()}
        for k, v in cols.items():
            print(f"  {k:14s} <- {v!r}")
        missing = [k for k in ("date", "exercise", "weight", "reps") if cols[k] is None]
        if missing:
            sys.exit(f"Could not find columns for {missing}. Headers were: {headers}")
        lb = args.lb or (cols["weight"] and "lb" in norm(cols["weight"]))
        rows = []
        for r in reader:
            w = (r.get(cols["weight"]) or "").strip()
            try:
                w_kg = round(float(w) * (0.45359237 if lb else 1.0), 2) if w else ""
            except ValueError:
                w_kg = ""
            rows.append({
                "date": parse_date(r.get(cols["date"], "")),
                "workout_title": r.get(cols["workout_title"], "") if cols["workout_title"] else "",
                "exercise": r.get(cols["exercise"], ""),
                "set_index": r.get(cols["set_index"], "") if cols["set_index"] else "",
                "set_type": r.get(cols["set_type"], "normal") if cols["set_type"] else "normal",
                "weight_kg": w_kg,
                "reps": r.get(cols["reps"], ""),
                "rpe": r.get(cols["rpe"], "") if cols["rpe"] else "",
                "notes": (r.get(cols["notes"], "") if cols["notes"] else "").replace("\n", " "),
                "source": "hevy-csv",
            })
    rows.sort(key=lambda r: (r["date"], r["workout_title"], str(r["set_index"])))
    if os.path.exists(args.out) and not args.force:
        with open(args.out, newline="") as existing:
            if any(r.get("source") == "hevy-api" for r in csv.DictReader(existing)):
                sys.exit(f"{args.out} already holds rows pulled from the Hevy API; this import would replace the whole file "
                         "and drop their workout ids. Write somewhere else with --out, or pass --force.")
    with open(args.out, "w", newline="") as out:
        wr = csv.DictWriter(out, fieldnames=HISTORY_COLUMNS)
        wr.writeheader()
        wr.writerows(rows)
    print(f"Wrote {len(rows)} sets to {args.out} (weights {'converted from lb' if lb else 'kept as kg'}).")


if __name__ == "__main__":
    main()
