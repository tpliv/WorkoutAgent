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
- Primary-source verification of the first research round (open internet;
  the first round had journal pages and most sites blocked). Every research
  note gained a dated addendum: a claim-by-claim table, corrections, items
  still unverified, newer evidence, and guide implications. About 330
  claims checked; about 75 corrected. Main corrections: Williams 2017 found
  a larger periodization effect in untrained lifters, and Moesgaard 2022's
  trained-lifter result is undulating vs linear; Pelland et al. is now
  published (Sports Med 2026) with fractional counting best for both
  outcomes; Barbalho 2019 is retracted; the "3-7% lost after a week off"
  figure had no source (1-3 week gaps show no significant 1RM loss);
  lateral raises cue neutral rotation, not external; overhead triceps work
  grows all three heads; the superset meta-analysis is Zhang 2025; many
  misattributed authors and years (Moran-Navarro, Saric, Goulart, Helms
  2020, Lastella, Maia, Davies, Remmert). Named programs checked against the
  authors' pages (Nippard Essentials is paid; Wendler's variable-schedule
  material; RP's own landmark tables; BBB, GZCLP, StrongLifts, PHAT).
- Guide chapters 00-07 and the templates corrected to match. Caffeine
  guidance lowered to ~3 mg/kg within 200 mg per dose and 400 mg per day,
  with a see-a-professional flag; cardio kept at least 3 h, 6 h where
  possible, from lower-body lifting. No progression-rule number changed
  (`tools/test_tools.py` passes), so `templates/rotation.json` and the
  Hevy routines are unchanged. The Liftosaur export was rewritten to the
  official Liftoscript grammar. Open questions for the user: the V-set RPE
  targets and stale threshold, and a separate rule for multi-week breaks.
