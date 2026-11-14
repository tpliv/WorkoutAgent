# Tools

Scripts that connect the program to a Hevy account and keep the progression
tracks current. Python 3, standard library only. The API schema they use was
verified against the official OpenAPI document on 2026-10-21
(`research/mobile-workout-trackers.md`, addendum).

## The loop in one command

```bash
python3 tools/hevy_sync.py            # everything below, in order
python3 tools/hevy_sync.py --dry-run  # show what would happen; writes nothing here, on GitHub or in Hevy
python3 tools/hevy_sync.py --check    # is Hevy the same as the repo? read-only
```

| Step | What | Stops the run if it fails |
|---|---|---|
| 1. check | this checkout is up to date with `origin/main` and may write to it (`gitguard.py`) | yes, before anything changes |
| 2. pull | new Hevy workouts into `data/history.csv` | yes |
| 3. apply | `templates/progression-tracks.md` to the tracks; table and log | yes |
| 4. week | logged sessions marked done in `data/week.json`; plan tables regenerated | yes |
| 5. build | the dashboard, only when data changed | no (reported at the end) |
| 6. commit, publish | the changed data files, to `origin/main` | yes: Hevy is not touched |
| 7. push | the routines that differ from Hevy, each read back | exit code 1 |

`main` is the source of truth, so the repo is published **before** Hevy is
touched: Hevy can never hold something the repo does not. Run it after
training is logged, after any change to the week (`week.py`) or a hand
amendment (`update_tracks.py --set`), and whenever you want to know the app is
right. With no news it changes nothing and commits nothing.

Two rules the tools enforce (`gitguard.py`):

- A session that cannot write to `main` cannot sync. It gets
  `Sync not started; nothing was changed` and Hevy stays as it is.
- `hevy_push_routines.py` refuses when `tracks.json`, `rotation.json`,
  `week.json`, `hevy-state.json` or the exercise map differ from `origin/main`.

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
6. `python3 tools/hevy_sync.py` to create the folder `Rotation 2026-10`
   with the twelve rotation routines: six half-sessions (L1, U1, L2, U2, L3, U3), three merged (Full A, Full B, Full C) and three cross-block merges (U1 + L2, U2 + L3, U3 + L1) for weeks that start mid-block. The dated copies of the current week's sessions go in a second folder, `This Week`.
   Routine ids are saved in `data/hevy-state.json`, so later runs update in
   place.

## Scripts

| Script | Purpose |
|---|---|
| `hevy_api.py` | API client used by the others, and a read-only inspector: `whoami`, `count`, `workouts`, `events --since`, `routines`, `folders`, `templates --search`, `history <template_id>`, `measurements`. |
| `hevy_pull.py` | Workouts into `data/history.csv`. Incremental by default (events since `last_pull` in `data/hevy-state.json`, which moves only when the pull changed the history); `--full` re-pulls everything; `--inspect` prints one raw workout; `--redate` fills `start_time` and the local date on existing rows without touching anything else. Dates are the lifter's calendar day (`localtime.py`). |
| `update_tracks.py` | Applies `templates/progression-tracks.md` to the sessions logged since the last run and rewrites `data/tracks.json`: increment, hold, miss, stall, double progression, gap clock, pointer, e1RM history. `--write-md` refreshes the generated block in `data/track-state.md` (tracks and accessory loads); `--reset-on-stall` applies the 7.5% reset instead of flagging it; `--dry-run` shows the decisions. `--set PATH=VALUE --reason "..."` is the only way to amend a value by hand (`squat.top_set_lb=155`, `pointer=U2`, `"accessories.Leg press.weight_lb=180"`): it is written to `data/track-log.md` and to `amendments` in the JSON. Appends to `data/track-log.md`. Writes nothing when nothing changed. |
| `hevy_push_routines.py` | Brings the Hevy routines in line with the repo: renders `templates/rotation.json` and the sessions in `data/week.json` with the loads in `data/tracks.json`, compares each with what Hevy holds (title, exercises, sets, loads, reps, exercise notes), updates the ones that differ and reads each back. `--check` compares only and exits 1 on any difference; `--all` updates everything; `--week-only` only the dated copies; `--only L1 U1` a subset of rotation slots; `--dry-run` prints payloads without network; `--deload` forces the deload rendering (a planned deload week is `week.py deload on`); `--as-of` sets the date for the gap modifiers and the This Week filter (default: today in the lifter's zone). The dated copies go first; a skipped session is printed with its reason; a failed routine does not stop the others; the exit code is non-zero unless Hevy matches. Refuses when its inputs differ from `origin/main` (`--unpublished` overrides; avoid). |
| `hevy_sync.py` | The loop above. `--no-pull`, `--no-push`, `--reset-on-stall`, `--full`, `--deload`, `-m "commit message"`; `--dry-run` writes nothing anywhere; `--check` is read-only; `--no-git` skips the checks and the commit (the Hevy push then refuses until the changes are on `main`). |
| `week.py` | The week's schedule, `data/week.json`: `show`, `plan --week-of <Mon> DATE=SLOT@TIME ...`, `add`, `set DATE --slot/--date/--time/--note/--state/--calendar`, `drop`, `status`, `deload on/off`, `reconcile` (the sync runs it), `render`, `brief [DATE]` (the numbers of the night-before brief, from the routine renderer). Prints the week with rendered loads and its checks: order (the rotation never skips ahead of the pointer), spacing (H the day after any exposure of the same lift), unlogged, unplanned or re-slotted sessions. Regenerates the Status and Sessions tables in `data/weekly-plan.md`. |
| `gitguard.py` | The two rules above, and the commit and publish the sync does. Skipped outside a git checkout or with `WORKOUT_NO_GIT=1`. |
| `localtime.py` | The lifter's time zone (`TRAINING_TZ`, default `America/New_York`). `local_today()` and `local_date(timestamp)`; every tool takes its dates from here, never from the server clock or the UTC date of a timestamp. |
| `build_dashboard.py` | Builds `dashboard/index.html` (one self-contained page) and `dashboard/data.json` from the history, the tracks and the track log: weekly tonnage and working sets, sets per muscle against the guide's targets, week-over-week e1RM per main lift, gap clock, track state, streaks. Offline; `--refresh-muscles` first refreshes `data/exercise-muscles.json` from Hevy's exercise templates; `--today` fixes the date. See "Progress dashboard" below. |
| `hevy_csv_import.py` | Fallback without Pro or network: converts the app's CSV export into `data/history.csv`. |
| `analyze_history.py` | Summarizes `data/history.csv` (per-exercise e1RM history, proposed starting loads) into `data/history-summary.md`. Used once to seed the tracks. |
| `lift_aliases.json` | Maps the six main lifts to exercise names in the log; `update_tracks.py` and `analyze_history.py` both use it. |
| `test_tools.py` | Offline tests of the rule engine and the routine rendering: `python3 tools/test_tools.py`. Rule and rendering cases start from the frozen `tools/fixtures/tracks.json` (the track state of 21 Oct 2026), so a sync does not break them; only the consistency checks read the live `data/tracks.json`. Refresh the fixture only when the shape of `tracks.json` changes (a test flags it), and update the expected numbers with it. |

## Files the tools read and write

| File | Written by | Read by | Committed |
|---|---|---|---|
| `templates/rotation.json` | hand (mirror of the markdown templates) | push | yes |
| `data/tracks.json` | `update_tracks.py` (amend with `--set`, never by editing) | push, update, week, dashboard | yes |
| `data/week.json` | `week.py` (never by editing) | push, week | yes |
| `data/weekly-plan.md` | `week.py` (the block between the `week:` markers); the rest by hand | people and agents | yes |
| `data/track-state.md` | `update_tracks.py --write-md` (the block between the `tracks:` markers); the notes by hand | people and agents | yes |
| `data/track-log.md` | `update_tracks.py` (append) | people and agents | yes |
| `data/history.csv` | `hevy_pull.py`, `hevy_csv_import.py` | update, analyze | yes |
| `data/hevy-exercise-map.json` | `hevy_push_routines.py --resolve` | push | yes |
| `data/hevy-state.json` | pull and push (folder ids, routine ids, the pool of dated routines, `last_pull`) | pull, push, week | yes |
| `data/exercise-muscles.json` | `build_dashboard.py --refresh-muscles` (and hand edits) | dashboard | yes |
| `dashboard/template.html` | hand | dashboard | yes |
| `dashboard/index.html`, `dashboard/data.json` | `build_dashboard.py` | people and agents | yes |
| `data/raw/` | pull (raw JSON) | nobody | no (gitignored) |

## Progress dashboard

```bash
python3 tools/build_dashboard.py                    # rebuild from the committed data
python3 tools/build_dashboard.py --refresh-muscles  # also refresh muscle groups from Hevy (after new exercises appear)
```

`dashboard/index.html` opens in any browser. It is also published as a
private claude.ai page; after each sync, republish the same file to the same
page rather than creating a new one. Published page:
https://claude.ai/artifact/ThkGMNsr2pwdMd8AoStU6Q (private to the account owner).

What it shows, by ISO week (Monday to Sunday), for the last 12, 26 or 52
weeks or all history:

| Panel | Rule | Source |
|---|---|---|
| This week | Tonnage, working sets, days trained against last week and the 4-week average; main lifts that went up | history |
| Volume | Tonnage (load x reps, warm-ups, bodyweight and assisted sets excluded) and working sets per week | history |
| Sets per muscle | 1 per set for the primary muscle group, 0.5 for each secondary; target band by days trained (`guide/03-flexible-scheduling.md` section 3) | history, `data/exercise-muscles.json` |
| Overload | Best e1RM per week per main lift (Epley, RPE-adjusted when logged, 1-12 reps), change against the previous week trained; up or down at 1% or more; a gap over four weeks reads "restart" | history, `tools/lift_aliases.json` |
| Gap clock | Days since the last exposure, banded per `templates/progression-tracks.md` section 8 | history, tracks |
| Tracks | Next heavy load, last heavy load, misses, stalls, last exposure, e1RM history; the latest track-log lines | `data/tracks.json`, `data/track-log.md` |
| Consistency | Days trained per week against the 3- and 5-day plans, weekly streaks | history |

Working sets are an upper bound on hard sets: most logged sets have no RPE.
Exercises missing from `data/exercise-muscles.json` get a muscle group from a
keyword table and are listed at the bottom of the page.

## What a routine looks like in the app

For each exercise the routine carries the sets Hevy can represent (warm-up
ramp, top set, back-offs, or sets with a rep range) with the planned load in
pounds (sent to the API as kg at full precision, so the app, set to lb, shows
exact pounds), the rest timer, superset grouping, and a note with the RPE target and the
rule for that exercise. Routine sets have no RPE field in Hevy, so the note is
where the target lives; you log the actual RPE on each set when you train.

Every exercise note ends with its rest, matching the timer. Hevy has one timer
per exercise, so a top set's longer rest is in the note ("Rest 3:30 after the
top set (timer + 0:30)"). Supersets use 1:00 on each exercise but the last and
2:00 on the last, so the timer gives 60 s to the partner and 2 min after the
round. The routine note, and the note on the first exercise (the API never
returns routine notes, so the first exercise is the place the app is known to
show), open with the target session length at those rests,
warm-up included, and when the main lifts should be done; it is estimated from
the rendered sets with the time budget in `guide/05-exercise-selection.md`,
section 6.2, so deloads come out shorter.

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
Full B, Full C; the routine titles start with it), or a lower-upper pair anywhere in the title ("U3 + L1 (merged)" is a merged U3 and L1; the pointer moves past L1) and matches lifts through
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
- Busy gym (`templates/progression-tracks.md` section 9): a row or pulldown
  variant from `lift_aliases.json` `_variants` counts as the exposure and runs
  double progression on its own load (`tracks.<lift>.variants`). A heavy slot
  without the barbell squat, bench, deadlift or press sets `h_owed`; the
  lift's next V slot is then pushed as top set + 2 back-offs and read as the
  heavy exposure. A substitute from `_substitutes` is stored as
  `last_sub_exposure` and caps the gap modifier at a hold. Every main lift's
  routine note carries a "Station taken" line with the fallbacks from
  `rotation.json` `substitutes` and their loads.
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
  `PUT /routines/{id}` with a new `folder_id` does move a routine between
  folders (verified 2026-11-06), so a retired routine can be rewritten and
  reused instead of deleted. The dated copies of the week's sessions (folder
  "This Week") are a pool of routines listed in `data/hevy-state.json`
  (`this_week.routine_ids`); `week.py` hands them out again each week and the
  push creates more when a week needs them. A pool routine not used this week
  keeps its old title in the app until it is used again.
- Routine-level notes are accepted by the API but never returned, so they
  cannot be compared; the first exercise note carries the same text.
- Saving a workout back to its routine in the app changes the routine. The
  next sync sees the difference and restores it.
- The API is Pro-only and Hevy says it may change without notice.
- `update_tracks.py` skips sessions dated before `processed_through` in
  `data/tracks.json`, and on that date the workout ids in `processed_ids`. A
  second session on a day already synced is processed on the next run. Sessions
  replay in `start_time` order.
