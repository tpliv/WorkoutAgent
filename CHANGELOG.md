# Changelog

## 2026-11-08

- Race log started (`data/races.md`): the 10-mile race on 8 Nov 2026 (1:27:35, avg HR 175) against the same race in 2025 (1:28:19, avg HR 169), with mile splits. Why: the lifter shared both results; keeping them lets later check-ins compare years. Read: the 44 s gain came from a faster first half, not fitness (about 2.7% more heartbeats per mile); the mile 9 fade came 3 days after a heavy squat that the race-week rule places at R-4 or earlier. No rule or load change.
- Race log revised with the lifter's answers: race is the EQT Pittsburgh 10 Miler (9 Nov 2025, 8 Nov 2026); race-morning conditions from the PIT and AGC airport observations (40-46 °F both years; 2025 foggy and humid, 2026 sunny and windier); 2025 bodyweight 165 lb vs about 181 now; mile 9 included a shoe-tie stop. Why the read changed: about 10% more bodyweight for 3.6% more heart rate at a slightly faster pace points to equal or better aerobic fitness, not a loss, and the squat-before-race explanation for mile 9 is no longer needed. Soreness and Monday sauna noted in `data/weekly-plan.md`; no plan change.

## 2026-11-06

- Lifter's answers (6 Nov): InBody model, pre-scan state and creatine start unknown, so the 21 Oct scan is a rough start and the first standardized scan (Wed 18 Nov if Mon-Tue are rest days, else 16 Dec) becomes the reference (`data/body-composition.md` §8; the check-in keeps 48 h before a scan free of lifting). Hevy pre-fills the planned reps, so an unedited 4 reads as a success: the routine notes and `templates/progression-tracks.md` §3 now say to change the reps when they differ, above all on a missed rep (addendum in `research/effort-ratings-and-progression-without-rpe.md`); routines pushed. Gym sauna available: recorded in the profile, and the week of 9 Nov gets an optional sauna plan (after sessions, none Saturday before the Sunday squat, none on drinking nights).
- Research round on what this lifter could benefit from next (ranked list in `research/BACKLOG.md`). Seven new notes, each verified against primary sources where they could be read: `research/running-and-lifting.md`, `research/retraining-after-layoff.md`, `research/effort-ratings-and-progression-without-rpe.md`, `research/alcohol-and-training.md`, `research/energy-availability-and-fueling.md`, `research/body-composition-measurement.md`, `research/sauna.md` (the last at the user's request). Why: the general programming science was already covered; the gaps were the lifter's own situation (runs and races, back after 18 months off, no RPE logged since 27 Oct, weekend drinking, a recomposition judged by InBody).
- Progression rules (`templates/progression-tracks.md` §3, §5, §5.1-5.3, §8, §10; `tools/update_tracks.py`; `tools/hevy_push_routines.py`; 13 new tests, 53 pass). The decision now reads the effective RPE at rep 4: logged RPE minus the extra reps, and an unrated set above the target is assumed to have ended at RPE 9. So 6 @ 8 or 6 unrated reps earns the big step, 5 @ 10 is a hold rather than a miss, and an effective 5 or lower re-anchors to e1RM / 1.2 (max +10%). Top sets may run to 6 reps when rep 4 is clearly easy; one rating per lift, on the top set (7, 8, 9, 10). Regain phase for the squat (to e1RM 263) and the row (to 128), ending at the first hard top set or 9 Jan 2027: +10 lb steps capped at +10 a session, row +10 on 11+ reps, 8-14-day gaps do not block the step. Deadlift caution to 9 Jan 2027: the big step needs a logged RPE and never comes twice in a row. A rep-out on the last back-off after two unrated 4s in a row. Why: the engine ignored extra reps (the 27 Oct bench was fixed by hand), every decision since 29 Oct assumed RPE 8, and the squat sits at 62-66% of its 2024 best while the starting rule climbs at the pace for new strength. No current load changes. `data/tracks.json` gains `regain`, `caution`, `unrated_streak`, `rep_out_due`, `last_step`; the track table a Phase column. Hevy routines and the This Week copies pushed (notes only) and checked by reading Full B back.
- Race weeks (`guide/03` §4.7; `templates/README.md`): last heavy lower at R-4, none R-3 to R-1; after the race, upper from R+2, the first lower at R+3 capped at RPE 7, the first squat H at R+4, and a below-plan top set is a hold. Runs placed around the rotation (`guide/03` §7, `guide/06` §5.3, rule 9 in `guide/00`): lift first on lower days; long and quality runs 48 h before a heavy lower slot; easy runs anywhere. Applied to the week of 9 Nov: Wednesday's deadlift cap at RPE 7 is now unconditional (also in the Hevy routine's note); Monday walk only; easy runs only.
- Nutrition (`guide/06` §4.4-4.5 and §8; `data/body-composition.md` §5, §5.1): alcohol default ceiling 3 drinks, none the night before a race or key session, protein first and several hours after training; carbohydrate floor 3 g/kg; a snack before the 7:30 am sessions; run add-back 100 kcal/mile, 120 on long runs; a 4-day-week setting (2,500); a day-by-day fueling plan for the 8 Nov race. Estimated energy availability 27-36 kcal/kg FFM on planned days, above the concern range (about 9-25), except race day if the extra food is skipped.
- Measurement (`data/body-composition.md` §6.1 and §8; `guide/06` §4.3): weigh at least 4 mornings a week and judge the 4-week trend, waist weekly, InBody under fixed conditions (Wednesday, dry fast, 48 h after lifting, 72 h after a long run or alcohol), rescans 16 Dec and 13 Jan. A change between two scans counts only at 3+ points of body fat, 5+ lb of fat or fat-free mass, or 3+ lb of SMM. Addendum in `research/body-recomposition.md`.
- Sauna (`guide/06` §6.1 and §8): optional; neutral to slightly positive for muscle, never before lifting, never with alcohol, none from 2 days before a race; avoid regular use when trying to conceive.
- Coaching runbooks: the check-in asks for waist, drinks and races and applies the phases; the nightly brief adds the rating line, the rep-out line when due, and the race-week line (`coach/`, `guide/08` §2.1).

- Dumbbell loads are now the total of both dumbbells, the way the lifter logs
  them in Hevy (confirmed 6 Nov). Rule in `templates/progression-tracks.md` §9
  and §11, `coach/README.md`, `coach/sunday-checkin.md`, `data/tracks.json`
  accessories, dashboard text. Loads fixed: lateral raise 20 total (10 each),
  incline DB curl 30 total, reverse lunge 35 total, incline DB press 70 total.
  Why: the routines said "per dumbbell" while the history and the starting
  loads read as totals, so lateral raise, curl and lunge prescriptions were
  about double what was lifted. `hevy_push_routines.py` now also refreshes the
  "This Week" copies on a full push. Routines and calendar holds updated.
- Hevy folder "This Week" holds the four sessions for the week of 9 Nov as
  dated routines (titles start with the slot, so syncs read them). The three
  Race Week routines were rewritten into it: the API has no delete (tested,
  404), but a routine PUT moves folders (addendum in
  `research/mobile-workout-trackers.md`). The empty Race Week folder must be
  deleted in the app. Ids in `data/hevy-state.json` under `this_week`.
- Week of 9 Nov changed to 4 days (Tue U1, Wed Full B, Fri Full C, Sun L1)
  after the lifter gave the race (10 miles, Sun 8 Nov) and Thursday work
  travel: Tuesday becomes upper only two days after the race. Holds on the
  Workouts calendar for Tue and Wed, 7:30-9:00 am; Friday and Sunday left
  flexible. `PORTABILITY.md` now lists the calendar holds (optional; the repo
  never reads the calendar) instead of "no connectors", which was out of date.
- Cross-block merged sessions U1 + L2, U2 + L3 and U3 + L1 added to
  `templates/3-day-week.md` and `templates/rotation.json`, and pushed to Hevy
  (the two hand-made "U2 + L3" and "U3 + L1 (merged)" routines are now
  tool-managed and carry current loads; "U1 + L2 (merged)" is new). About 20
  hard sets and 60-70 min each. Rule: skip the U2 + L3 deadlift V when U1 + L2
  was the day before. `hevy_push_routines.py` writes an exercise-level `note`.
  Why: the pointer is at U1 and the lifter picked Tue, Wed, Fri mornings for the
  week of 9 Nov (`data/weekly-plan.md`, `data/checkins/2026-11-06.md`).
- Synced 29 Oct (L2) and race week (4-5 Nov). Loads going forward: squat
  135 -> 155 (155 x 5 logged; 19-day gap, so hold the load lifted, no
  increment), overhead press 60 -> 70 (70 x 4 logged, step counter 1),
  deadlift work-up done at 145 x 4 -> 150. Bench 110, row 70 and pulldown 125
  unchanged (race-week pulldowns were on another gym's stack). Incline DB curl
  25 -> 30, reverse lunge 30 -> 32.5. No RPE logged on any set; all decisions
  assume RPE 8 (`data/track-log.md`). Pointer U1. Routines pushed.
- `tools/update_tracks.py` reads a lower-upper pair anywhere in a workout title
  ("U3 + L1 (merged)", "Race Week 2 - Wed (U3 + L1)") as a merged session of
  those halves. Before, "U3 + L1 (merged)" read as U3 alone and race-week titles
  as no slot, which left the pointer at U2 and the squat and press tracks
  unread. Tests added. Why: shifted merges (`guide/03` §4.4) are how the
  rotation runs when a week starts mid-pass.

## 2026-11-02

- Hevy routine "Race Week 1 - Tue (U2 + L3)" (folder Race Week) rewritten
  for a gym with only dumbbells and barbells. Lat pulldown 3 x 5-8 at 125 ->
  one-arm DB row (Hevy "Dumbbell Row") 3 x 5-8 at 70 lb per arm, RPE 8.
  Reverse pec deck -> bent-over DB rear fly 2 x 15-20 at 15 lb. Overhead
  press, deadlift and incline DB curl unchanged; notes added for no rack (clean
  the press from the floor) and no incline bench (standing DB curl). Swaps
  follow the matrix in `guide/05-exercise-selection.md` §7.3. Per
  `templates/progression-tracks.md` §9 the DB row does not update the pull-up
  track or its gap clock. The 70 lb start is a guess from the 27 Oct DB row
  (60 x 10, 8, 10, two-handed bent-over). Why: the lifter will train at a
  dumbbell-and-barbell gym. The Race Week routines were created in Hevy on
  2 Nov outside this repo and are not in `templates/rotation.json`.

## 2026-10-27

- New rule for a busy rack or bench: reorder, do not substitute
  (`guide/03-flexible-scheduling.md` §4.3, "Station taken"; research addendum
  2026-10-27 in `research/exercise-selection-and-session-design.md`, Simão 2012
  and Nunes 2021). Mirrored in `templates/progression-tracks.md` §9,
  `templates/README.md`, the nightly brief ("Rack taken" line) and every
  routine note in `templates/rotation.json`, pushed to Hevy. Why: on 27 Oct the
  squat rack was taken and the squat top set, the one thing the program never
  cuts, was replaced by leg press.
- Bench track 105 -> 110 by hand: the lifter reported RPE 8 on 105 x 6, which is
  the §5 big-step row (4 reps would have been about RPE 6). The sync had held
  105 because it assumed RPE 8 at 4 reps and ignores extra reps.
- `tools/test_tools.py` no longer reads its fixtures from the live
  `data/tracks.json`. The 27 Oct sync moved the pointer, bench load and
  counters, and 12 tests failed plus 1 error, though the rule engine was
  unchanged. Rule and rendering cases now start from a frozen copy,
  `tools/fixtures/tracks.json` (the state at commit 85b16d9). The live file
  still feeds the rotation consistency checks and the committed-history replay,
  which hold after every sync. A new test flags when the fixture's shape drifts
  from the live file. `templates/rotation.json` stays live.

## 2026-10-26

- Consolidated the repository onto a new `main` branch. Twelve session branches
  had never been merged, so each new session started from whichever one it was
  given (one started from a kilogram branch and planned the next session in kg).
  Merged all of them. Conflicts kept the pounds tooling verified against the
  live Hevy routines, the coaching cadence (`coach/`, guide 08), the rest timers
  and session-length notes, the progress dashboard, the body-composition notes,
  the portability notes and the primary-source corrections to the research
  notes and guide. Kept the short warm-up ramp (bar x 5, 80% x 2-3) everywhere,
  including the Liftosaur export and the coaching runbooks, which still had the
  four-step ramp. Kept the verified Ribeiro 2020 wording in the progression
  tracks. Dropped `tools/hevy_push.py` and `tools/hevy_program.json`, an earlier
  routine pusher replaced by `tools/hevy_push_routines.py`.
- The dashboard now reads the pound fields of `data/tracks.json` (it read
  `top_set_kg`, which the pounds switch removed) and labels tonnage in lb.
- `tools/analyze_history.py` reads the manual log with either a `load` or a
  `load_lb` column; both are pounds.
- Coaching runbooks (`coach/`, guide 08 section 4) now run `tools/hevy_sync.py`
  to pull results, apply the rules and push the routines, instead of editing
  the track table by hand (that table is regenerated by the tools). They work
  on `main` of `tpliv/WorkoutAgent`. `CLAUDE.md` gained a branch rule.
- Routine notes print "lb" after every load again ("Top set 135 lb x 4"), as
  the routines in the app already did. Checked offline against the live
  routines: every working set, rep target and rest timer matches; only the
  warm-ups (short ramp) and note wording differ. Nothing was pushed to Hevy.

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
- Research note `research/body-recomposition.md` (maintenance estimation,
  recomposition rates and muscle memory, US population body-composition
  norms). Chapter 06 gains section 4.3 on estimating maintenance and running a
  recomposition. `data/body-composition.md` records the user's baseline
  (InBody 2026-10-21: 181 lb, SMM 88 lb, 16.5% body fat), population
  comparison, calorie plan (2,500 / 2,700 kcal, 180 g protein) and a scan log,
  so later scans can be compared against it.
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
- Converted templates, progression rules, the chapter 03 worked example, and the
  Liftosaur file from kilograms to pounds (5 lb squat and deadlift steps, 2.5 lb
  bench and press steps). Research notes and study citations stay in their
  source units.
- Weekly coaching cadence. New research note `research/coaching-check-ins.md`
  covers readiness questionnaires (Saw 2016; Hooper & Mackinnon 1995), RIR
  autoregulation, and supervision (Mazzetti 2000; Fisher 2022). New chapter
  `guide/08-weekly-coaching-cadence.md` sets out a Sunday 6:47 pm ET check-in
  (five questions, then the guide 03 section 4.1 procedure) and a night-before
  brief Mon-Sat at 7:47 pm ET. New `coach/` runbooks for the scheduled sessions,
  plus `data/weekly-plan.md`, `data/checkins/` and `data/manual-log.csv` for
  state. Results come from the Hevy API when `HEVY_API_KEY` is set, otherwise
  from the chat. Why: the user asked for a personal-trainer rhythm; the program
  rules are unchanged.
- Equipment: the lifter's smallest plate is 2.5 lb, so every barbell load is now a
  multiple of 5 lb. Bench and press move 5 lb after every second successful heavy
  top set (a step counter in `templates/progression-tracks.md` section 5 and
  `data/track-state.md`), instead of the 2.5 lb steps that needed 1.25 lb plates.
  All computed loads (back-offs, V sets, warm-ups, deloads, resets) round to the
  nearest 5 lb. Accessory loads are a single weight, not a range. The guide 03
  worked example, the guide 07 sample rows, the Liftosaur file, the coach runbooks
  and the seeded week plan were recalculated. Rationale: addendum in
  `research/periodization-and-progression.md`. Why: the user reported uneven
  load sizes they could not build with their plates.
- Dumbbells go up in 2.5 lb steps: dumbbell accessories progress and stall-drop by
  2.5 lb per dumbbell (`templates/progression-tracks.md` sections 9 and 11, coach
  runbooks, `data/track-state.md`, Liftosaur `dp(2.5lb, ...)` on dumbbell lines).
  Why: the user confirmed their dumbbell rack.
- Hevy routines rewritten in pounds. The nine "Rotation 2026-10" routines had been
  built in kilograms (squat 60 kg showed as 132.3 lb, bench 42.5 kg as 93.7 lb). They
  now carry the exact `data/track-state.md` loads (squat 135/125, bench 95/90, press
  60/55, row 70, pulldown 125, V loads 120/85/55/65/115, accessories) with notes in
  pounds. `tools/hevy_pull.py` now works when the key is a network secret the proxy
  adds (no `HEVY_API_KEY` variable) and dates workouts in local time. The coach
  runbooks check the API itself, not the variable. Why: the user reported odd load
  sizes in Hevy.
- Added `PORTABILITY.md` and a portability section in `CLAUDE.md` so the project
  can move off the current Claude account: inventory of what is account-bound,
  the cloud environment spec, and a migration checklist. `tools/hevy_pull.py`
  now also runs when the Hevy key is injected by a network secret instead of
  the `HEVY_API_KEY` variable, so it works the same in either setup.
- Added `tools/hevy_push.py` and `tools/hevy_program.json`: write the pound loads
  in `data/track-state.md` into the nine Hevy routines (dry run by default), so the
  app is ready before each session. The existing routines still held the kilogram
  loads. Research note addendum records the Hevy API spec, checked live.
