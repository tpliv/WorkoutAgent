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
- Research note `research/body-recomposition.md` (maintenance estimation,
  recomposition rates and muscle memory, US population body-composition
  norms). Chapter 06 gains section 4.3 on estimating maintenance and running a
  recomposition. `data/body-composition.md` records the user's baseline
  (InBody 2026-10-21: 181 lb, SMM 88 lb, 16.5% body fat), population
  comparison, calorie plan (2,500 / 2,700 kcal, 180 g protein) and a scan log,
  so later scans can be compared against it.
