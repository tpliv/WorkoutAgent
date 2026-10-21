# Tools

Scripts that connect the program to a Hevy account and keep the progression
tracks current. Python 3, standard library only. The API schema they use was
verified against the official OpenAPI document on 2026-10-21
(`research/mobile-workout-trackers.md`, addendum).

## The weekly loop in one command

```bash
python3 tools/hevy_sync.py            # pull new workouts, apply the rules, push the new loads
python3 tools/hevy_sync.py --dry-run  # same, but only show what would change
```

That runs the three steps below in order. Run it after each pass of the
rotation (once a week for any 3- to 6-day week), or whenever you want the
routines in the app to reflect the latest logged sessions.

## Setup (once)

1. Hevy Pro, and an API key from https://hevy.com/settings?developer.
2. Give sessions the key, one of two ways. Never paste it into the chat, a
   file, or a commit.
   - **Network secret (preferred in a cloud environment).** Edit the cloud
     environment, open **Network secrets**, **Add secret**. Secret type
     **Bearer** (the default), name it anything (`Hevy`), allowed website
     `api.hevyapp.com`, and in **Custom headers** set the header name to
     `api-key`, clear the `Bearer` prefix, and paste the key as the value.
     The proxy adds the header to every request to that host; the key never
     enters the sandbox and no variable is needed.
   - **Environment variable.** Add `HEVY_API_KEY` under the environment's
     **Environment variables** (or export it in a local shell). The client then
     sends the header itself.
3. `python3 tools/hevy_api.py whoami` to confirm the key works.
4. `python3 tools/hevy_pull.py --full` to replace the old CSV import with an
   API pull that carries workout ids and per-set RPE.
5. `python3 tools/hevy_push_routines.py --resolve` to match every program
   exercise to a Hevy exercise template. It writes `data/hevy-exercise-map.json`
   and lists anything it could not match; find the right title with
   `python3 tools/hevy_api.py templates --search curl` and fix the map (or the
   `hevy` candidate list in `templates/rotation.json`).
6. `python3 tools/hevy_push_routines.py` to create the folder `Rotation 2026-10`
   with the nine routines (L1, U1, L2, U2, L3, U3, Full A, Full B, Full C).
   Routine ids are saved in `data/hevy-state.json`, so later runs update in
   place.

## Scripts

| Script | Purpose |
|---|---|
| `hevy_api.py` | API client used by the others, and a read-only inspector: `whoami`, `count`, `workouts`, `events --since`, `routines`, `folders`, `templates --search`, `history <template_id>`, `measurements`. |
| `hevy_pull.py` | Workouts into `data/history.csv`. Incremental by default (events since `last_pull` in `data/hevy-state.json`); `--full` re-pulls everything; `--inspect` prints one raw workout. |
| `update_tracks.py` | Applies `templates/progression-tracks.md` to the sessions logged since the last run and rewrites `data/tracks.json`: increment, hold, miss, stall, double progression, gap clock, pointer, e1RM history. `--write-md` refreshes the table in `data/track-state.md`; `--reset-on-stall` applies the 7.5% reset instead of flagging it; `--dry-run` shows the decisions. Appends to `data/track-log.md`. |
| `hevy_push_routines.py` | Renders `templates/rotation.json` with the loads in `data/tracks.json` into Hevy routines and creates or updates them. `--dry-run` prints the payloads without network; `--deload` renders the deload week; `--only L1 U1` limits the slots; `--as-of` sets the date for the gap modifiers. |
| `hevy_sync.py` | Runs pull, update, push. `--no-push`, `--no-pull`, `--deload`, `--reset-on-stall`, `--full` pass through. |
| `hevy_csv_import.py` | Fallback without Pro or network: converts the app's CSV export into `data/history.csv`. |
| `analyze_history.py` | Summarizes `data/history.csv` (per-exercise e1RM history, proposed starting loads) into `data/history-summary.md`. Used once to seed the tracks. |
| `lift_aliases.json` | Maps the six main lifts to exercise names in the log; `update_tracks.py` and `analyze_history.py` both use it. |
| `test_tools.py` | Offline tests of the rule engine and the routine rendering: `python3 tools/test_tools.py`. |

## Files the tools read and write

| File | Written by | Read by | Committed |
|---|---|---|---|
| `templates/rotation.json` | hand (mirror of the markdown templates) | push | yes |
| `data/tracks.json` | `update_tracks.py` (and hand edits) | push, update | yes |
| `data/track-state.md` | `update_tracks.py --write-md` (table only) | people and agents | yes |
| `data/track-log.md` | `update_tracks.py` (append) | people and agents | yes |
| `data/history.csv` | `hevy_pull.py`, `hevy_csv_import.py` | update, analyze | yes |
| `data/hevy-exercise-map.json` | `hevy_push_routines.py --resolve` | push | yes |
| `data/hevy-state.json` | pull and push (folder id, routine ids, `last_pull`) | pull, push | yes |
| `data/raw/` | pull (raw JSON) | nobody | no (gitignored) |

## What a routine looks like in the app

For each exercise the routine carries the sets Hevy can represent (warm-up
ramp, top set, back-offs, or sets with a rep range) with the planned load in
pounds (sent to the API as kg at full precision, so the app, set to lb, shows
exact pounds), the rest timer, superset grouping, and a note with the RPE target and the
rule for that exercise. Routine sets have no RPE field in Hevy, so the note is
where the target lives; you log the actual RPE on each set when you train.

Main lifts: the H exposure gets the ramp (bar x 5, 80% x 2, plus 60% x 3
between them once the top set is 225 lb or more),
the top set at the track load, and back-offs at 93%. The V exposure gets sets
at 90% of the track load. Row and pull-up get fixed-load sets with the rep
range. Accessories get the rep range and the load from `tracks.json` (blank
until you record one).

Deadlift starts as "work up": the sets are rendered with no load and the note
gives the ladder. After that first session the track holds the load you found.

## How the rules are applied

`update_tracks.py` reads the slot from the workout title (L1 ... U3, Full A,
Full B, Full C; the routine titles start with it) and matches lifts through
`lift_aliases.json`. In an H-slot session the top set is the heaviest working
set of the lift. The decision follows section 5 of
`templates/progression-tracks.md` exactly, with these implementation choices:

- A top set with no RPE logged is treated as RPE 8 and flagged.
- The new planned load is computed from the load actually lifted, so a work-up
  or a deliberately heavier top set moves the track with it.
- A stall (two misses at one load) is flagged and the load held. The reset is
  applied only with `--reset-on-stall`, because section 6 says to check sleep,
  calories and bodyweight first.
- Gap modifiers (section 8) are applied by the push step as a view from the
  last exposure to the push date; `tracks.json` keeps the unmodified planned
  load and the last lifted load.
- V exposures, substitutes and untitled sessions never change a load; they do
  update the lift's last-exposure date.
- The pointer is the half-session after the latest slot-titled session.

## Normalized log format

`data/history.csv`: one row per set.

| Column | Meaning |
|---|---|
| `date` | YYYY-MM-DD |
| `workout_title` | Session title as logged; routines started from the pushed folder carry the slot prefix |
| `exercise` | Hevy exercise title |
| `set_index` | 0-based set order within the exercise |
| `set_type` | normal, warmup, failure, dropset |
| `weight_kg` | Load in kg as the Hevy API returns it (bodyweight exercises: added load, or empty). The program runs in pounds; `update_tracks.py` converts on read (to 0.1 lb) |
| `reps` | Reps completed |
| `rpe` | Logged RPE (6-10 in 0.5 steps), if any |
| `notes` | Exercise notes |
| `source` | hevy-api, hevy-csv, or manual |
| `workout_id` | Hevy workout id (API rows only; used to merge incremental pulls) |

`templates/log-template.csv` is the manual-entry version with fewer columns;
`analyze_history.py` reads either.

## Limits

- No webhook or delete endpoint exists in the published API: the loop is run by
  hand or on a schedule, and a retired routine is deleted in the app (then
  remove its id from `data/hevy-state.json`).
- The API is Pro-only and Hevy says it may change without notice.
- `update_tracks.py` skips sessions dated on or before `processed_through` in
  `tracks.json` when applying rules, so two sessions on the same calendar day
  are processed together on the next run, not separately.
