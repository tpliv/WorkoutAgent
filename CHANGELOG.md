# Changelog

## 2026-10-21

- Initial repository structure: `research/`, `guide/`, `templates/`.
- First research round: training frequency and volume evidence, splits and named
  programs, flexible-frequency programming, periodization and progression,
  exercise selection and session design, recovery, nutrition, and cardio.
- First edition of the training guide and 3/4/5/6-day templates.
- Guide chapters 00-06 written from the research notes; chapter 01 and 04 wording
  aligned with the rotation design in chapter 03 (one pass per calendar week in
  any 3-6-day week; at least 2 exposures per muscle, 3 for large muscles).
- Research note on mobile workout trackers added (Liftosaur and Hevy Pro are the
  two apps with an agent-writable program path).
- Chapter 07 on tracking and apps, a Liftosaur rendering of the rotation under
  `templates/liftosaur/`, and `templates/log-template.csv`.
- Added `tools/`: Hevy API pull, Hevy CSV import, history analysis that proposes
  starting loads per the progression tracks; `data/` for the normalized log.
- Imported the user's Hevy export (52 sessions, 2024-03 to 2026-10) to
  `data/history.csv`; `data/history-summary.md` holds the analysis and proposed
  starting loads. Analyzer gained alias exclusions and a pounds column.
- Added `data/track-state.md`: the live state of the six progression tracks in
  kilograms, seeded from the imported history, with the rotation pointer at L1.
- Hevy integration built out. Verified the Hevy public API schema against the
  official OpenAPI document (addendum in `research/mobile-workout-trackers.md`:
  per-set RPE confirmed, routine sets have no RPE, no webhooks or delete
  endpoints). Added `tools/hevy_api.py` (client and inspector),
  `tools/hevy_push_routines.py` (renders `templates/rotation.json` with the
  loads in `data/tracks.json` into nine Hevy routines, creates or updates them
  in place), `tools/update_tracks.py` (applies the increment, hold, miss, stall,
  double-progression, gap and pointer rules to the pulled history),
  `tools/hevy_sync.py` (pull, update, push) and `tools/test_tools.py`.
  `tools/hevy_pull.py` now uses the verified schema, pulls incrementally
  through workout events and carries a `workout_id` column.
  `data/tracks.json` is the machine-readable track state; the table in
  `data/track-state.md` is regenerated from it. Chapter 07 section 3.2 and the
  READMEs describe the loop; `CLAUDE.md` tells agents how to run it.
- First live run against the user's account: full API pull (52 workouts, with
  workout ids), all 25 program exercises matched to Hevy templates
  (`data/hevy-exercise-map.json`), folder `Rotation 2026-10` and the nine
  routines created (`data/hevy-state.json`). Folder-create and routine-get
  responses are wrapped objects on the live API; client adjusted.
- Shortened the warm-up ramp on each session's first compound from bar x 10,
  40% x 8, 60% x 5, 80% x 2-3 to bar x 5, 80% x 2-3, with 60% x 3 added between
  them once the top set is 225 lb (about 102 kg) or more. That added step is
  coaching convention, not evidence. Why: the old ramp took 4-6 min and the short
  one takes 2-3 min (the warm-up total in the time budget drops from about 8 to
  about 5-6 min). At current loads the 40% set was barely above the empty bar.
  Ribeiro et al. 2020 supports a two-set warm-up with one set near the working
  load: its 40%/80% two-set protocol beat six light sets on bench, and its 80%
  warm-up beat the 40% one on squat. Re-reading the abstract corrected the
  repo's earlier claim that the two-set result was on squat. Research note KQ5
  addendum, chapter 05 section 5, templates, Liftosaur notes,
  `templates/rotation.json` and `tools/hevy_push_routines.py` (with tests)
  updated. The nine Hevy routines were changed in place (warm-up sets only).
- Switched the program's tools and data from kilograms to pounds, to match the
  Hevy app (set to lb) and the routines already in it. `data/tracks.json`,
  `data/track-state.md`, `templates/progression-tracks.md` and the routine
  renderer now work in pounds. Starting loads are squat 135, bench 95,
  press 60, row 70 and pulldown 125. Every barbell load is a multiple of 5 lb,
  since the smallest plate is 2.5 lb. Rule changes that follow from the unit:
  squat and deadlift +5 lb per success (+10 lb big step); bench and press
  +5 lb after every second success, tracked by a new `step_counter`, instead
  of +1 kg each time (same weekly pace); row and pulldown +5 lb. Accessory
  notes carry each exercise's own step (one pin, or 2.5 lb per dumbbell).
  V-day warm-ups now key off the V load. `data/history.csv` stays in kg as the
  Hevy API returns it; `update_tracks.py` converts on read, and
  `hevy_api.py workouts` and `history` print `weight_lb` beside `weight_kg`.
  Why: running a sync from the kg files would have overwritten the pound
  routines (a 132.3-lb squat). Verified by rendering all nine routines
  offline and diffing them against the live app: no differences.
- Rest timers in the Hevy routines now match the templates, and every exercise
  note states its rest. `templates/rotation.json`: superset members rest 60 s,
  the last member of each superset 120 s (the key's "60 s between the two
  exercises, 2 min after the pair"); top sets carry `rest_top` (3:30 squat and
  bench, 3:00 press, 4:00 deadlift); deadlift back-off rest 3:00 (was 4:00).
  Each routine note opens with a target session length and a main-lift
  checkpoint, estimated from guide 05 section 6.2. Why: the user's logged
  sessions ran about 2 min per set against the 3 min the program prescribes.
- Progress dashboard: `tools/build_dashboard.py` builds `dashboard/index.html`
  from `data/history.csv`, `data/tracks.json` and `data/track-log.md`, applying
  the derived metrics of chapter 07 section 1.2 by week (tonnage, working sets,
  sets per muscle against the chapter 03 targets, week-over-week e1RM per main
  lift, gap clock, track state, streaks). Muscle groups come from Hevy's
  exercise templates (`data/exercise-muscles.json`). `hevy_sync.py` rebuilds it
  after each update so progress over time is visible in one page.
