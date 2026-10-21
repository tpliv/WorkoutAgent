# Liftosaur rendering of the rotation

Last updated: 2026-10-21 (revised the same day against the official Liftoscript doc, the grammar file and the built-in exercise list; `research/mobile-workout-trackers.md`, addendum "official-source verification")

`rotation.liftoscript` is a Liftoscript version of the six half-sessions in `templates/6-day-week.md`, with the main-lift top-set and back-off structure and the accessory double progression from `templates/progression-tracks.md`, and the rest timers, warm-ups and supersets from `templates/rotation.json`. Why Liftosaur, and the alternatives: `guide/07-tracking-and-apps.md`.

## Read this first: what is verified and what is not

The first rendering used syntax quoted second-hand. The research addendum of 2026-10-21 checked it against the [Liftoscript doc](https://www.liftosaur.com/doc/liftoscript), the [grammar file](https://github.com/astashov/liftosaur/blob/master/src/pages/planner/plannerExercise.grammar) and the [built-in exercise list](https://github.com/astashov/liftosaur/blob/master/src/models/exercise.ts), and the file was rewritten to match.

| Item | Status | Where it matters |
|---|---|---|
| Exercise line shape `Exercise / sets x reps weight @RPE / section / ...` | **Verified** (doc, grammar) | Every line |
| `@8+` logs the actual RPE; `%` means percent of 1RM; `kg` and `lb` number types | **Verified** | Every line; `%` is **not** percent of the top set, so back-offs are written as absolute weights |
| Week and day headers `# Week 1`, `## Day 1: name` | **Verified.** The header runs to the end of the line, so everything after `#` or `##` is the name | The week and six day headers |
| Comments | **Verified, and different from what the first rendering assumed.** `///` is a hidden note. `//` is a description **shown to the lifter**: above an exercise it describes the exercise, above `# Week` or `## Day` it describes the week or day. Comments are whole lines only; text after an exercise on the same line breaks the parse | All notes are now `///` lines; each day has a `//` description taken from the session notes in `templates/rotation.json` |
| `lp(increase, attempts, current attempt, decrease, decrease attempts, current decrease attempt)` | **Verified.** `lp(2.5kg, 2)` = +2.5 kg after every second success | H lines; bench and press without 0.5 kg plates |
| `lp()` advances on completed reps, not on RPE | **Verified.** It has no RPE argument | The hold rule (known gaps below) |
| `dp(step, minReps, maxReps)` | **Verified.** The doc writes the sets at the bottom of the range (`3x8 / progress: dp(5lb, 8, 12)`) | Every accessory line and the row and pull-up tracks, now written that way |
| `sum(reps threshold, weight increase)` and `custom() {~ ... ~}` with `completedRPE`, `completedReps`, `weights`, `rm1` | **Verified** (doc) | Not used yet; `custom()` is how an RPE-conditional hold would be written |
| One progression per exercise across the program | **Verified.** A second, different rule for the same exercise is an error. A label (`v: Squat`) makes a separate exercise | V lines carry the label `v:`; the Day 5 calf raise carries `hirep:` |
| Rest timers | **Verified.** `/ 90s` for every set of an exercise, or per set (`1x12 20s`) | Every line, values from `templates/rotation.json` |
| Warm-ups | **Verified.** `warmup: 1x5 45lb, 1x3 80%` or `warmup: none`; percentages are of the **first working set**; no RPE or timer in warm-ups. Without the section the app adds its default warm-ups | H and V main-lift lines (ramp and feeder from `templates/rotation.json`); accessories keep the app default |
| Supersets | **Verified.** `/ superset: A` | The superset pairs in `templates/rotation.json` |
| Added load on bodyweight lifts | **Verified.** `Pull Up` defaults to Bodyweight equipment; with "Bodyweight for Bar" on (Me → Equipment) the number on the line is the added load | Pull Up lines |
| Omitted weight | **Verified.** With an `@RPE` target the app computes the weight from its RPE table and the exercise's 1RM; with neither weight nor RPE the field is blank and must be typed | Accessory lines (they carry an RPE, so they get a computed weight) |
| Exercise names | **Verified** against the built-in list; equipment after a comma where the default differs (`Romanian Deadlift, Barbell`; the default is dumbbell) | Every line |
| Share links, export formats, Premium price, API | **Verified** (sections below) | Getting data back out |
| Whether an `lp()` step rewrites the weight on every day the exercise appears | **Unverified in official text.** A local run of Liftosaur's own code says yes (see Validation) | Why the V lines are labelled |
| `dp()` with sets written as a rep range (`3x8-10`) | **Unverified in official text.** A local run collapsed the range (8-10 became 10-10), so the file avoids it | Accessory, row and pull-up lines |
| API rate limits; a percent decrease in `lp()`'s fourth argument | **Unverified** | Only if you automate it |

## Validation

The file was checked by three means, none of which used an account or an API key:

1. **Reading** the doc, the grammar and the exercise list (above).
2. **Liftosaur's own parser.** The generated parser in the Liftosaur source (`src/pages/planner/plannerExerciseParser.ts`) parses the file with no error nodes. The previous rendering produced parse errors on every exercise line with a trailing `//` note.
3. **Liftosaur's own evaluator and playground code, run locally.** The official `POST /api/v1/playground` endpoint needs a Premium key, so it was not called. Instead, the same functions it calls (`Playground_validateProgramText` and `Playground_run` in `src/playground/playground.ts`, open source on GitHub, master of 2026-10-21) were run offline with the app's default settings. Validation returned no errors (no unknown exercise, no conflicting progression). Each of the six days was then simulated with every set completed and the workout finished: the squat and deadlift tracks moved on Days 1 and 3 and stayed put after Day 5; the `v:` lines did not move; the bench went 85 → 86 kg; the row went 4 x 6 → 4 x 7; accessories gained a rep. Default settings round some loads in the workout view (back-off 112.5 shows as 112 kg); set your own plates in Me → Equipment.

A local run is not the hosted service. Paste the file into the web editor before the first session; it shows any error with its line.

## Files

| File | What it is |
|---|---|
| `rotation.liftoscript` | The six half-sessions, Day 1 = L1 through Day 6 = U3, with starting loads from the worked example in `guide/03-flexible-scheduling.md`, section 6 |
| `README.md` | This file |

## How to import

1. **Web editor.** Open Liftosaur's web editor on a desktop, create a new program, switch to the full-text mode, paste the contents of `rotation.liftoscript`, fix anything the editor flags, save. The program syncs to the phone with an account.
2. **Text in the app.** Paste the program text where the app asks for it.
3. **Share link.** Once imported, the app can make a public link `https://www.liftosaur.com/p/<id>`. It is a frozen snapshot: later edits need a new link. Import a link with Me → Program → Import.

All three work on the free tier: "programs and the editor, Liftoscript, logging workouts, history, ... sharing, import and export" are free ([Premium page](https://www.liftosaur.com/features/premium)).

## What to adjust before the first session

1. **Starting loads.** The file carries the worked example (squat 120, bench 85, deadlift 150, press 55, row 70, pull-up +10 kg). Replace them using `templates/progression-tracks.md`, section 2: 95% of a recent 5RM, or 80% of a recent 1RM, or work up on the first H exposure and type in what 4 reps at RPE 8 turned out to be. Then recompute the dependent numbers:

   | Line | Formula | Example (squat 120) |
   |---|---|---|
   | H back-off weight | top set x 0.93, rounded to the nearest loadable weight | 111.6 -> 112.5 |
   | V weight (Days 5-6) | top set x 0.90, rounded | 108 -> 107.5 |
   | Pull-up V added load | reduce until the sets land at RPE 7; 0 kg = bodyweight | +10 -> +5 |

2. **kg or lb.** The file is in kg. For pounds, change every `kg` to `lb` and the increments: `lp(2.5kg)` -> `lp(5lb)`, `lp(1kg)` -> `lp(2.5lb)`, `dp(2.5kg, ...)` -> `dp(5lb, ...)`, dumbbell steps `2kg` -> `5lb`, the bar in the warm-up `20kg` -> `45lb`. Set the app's plates in Me → Equipment.
3. **Fractional plates.** Bench and press use `lp(1kg)`, which needs 0.5 kg plates. Without them, change both to `lp(2.5kg, 2)`: +2.5 kg after every second successful exposure (`templates/progression-tracks.md`, section 9).
4. **Exercise names and equipment.** The names are Liftosaur built-ins. Change the equipment after the comma to what your gym has (the calf raise, reverse fly and preacher curl are written as Leverage Machine). The substitutions from the template are in each day's description.
5. **Accessory starting loads.** Accessory lines carry an RPE and no weight, so on the first exposure the app computes a weight from the RPE table and the exercise's 1RM. If you have not entered a 1RM, that guess can be far off: type the weight you can lift for the bottom of the range with 2-3 reps in reserve (`progression-tracks.md`, section 11). After the first load step the app writes the weight into the line. Dumbbell steps (`2kg`) should be one step on your rack.
6. **Pull-ups.** Turn on "Bodyweight for Bar" for the Bodyweight equipment (Me → Equipment) so the number on the line is the added load.
7. **Warm-ups and rest** are in the file: ramp (bar x 10, 40% x 8, 60% x 5, 80% x 2 of the first working set) on the first main lift of each day, a 1 x 3 feeder at 65% on the second, rest per `templates/rotation.json` (deadlift 240 s, squat, bench and press 180 s on H days, 60-150 s elsewhere). Edit them in the file, not in the app, so a re-render does not undo your change.

## How the app runs the rotation

- **Pointer.** Finishing a workout runs the progressions and advances the program to the next day whatever the calendar says (REST API doc: `workout/finish` "save it, run progressions, advance the day"). Day 6 returns to Day 1. That is the pointer in `guide/03-flexible-scheduling.md`, section 1.4; you never pick a day by weekday.
- **Short weeks.** The file is the split form. In a 3-, 4- or 5-day week, do two consecutive program days in one gym visit (L3 then U3 = Full C; L1 then U1 = Full A; L2 then U2 = Full B; merge C first, then A, then B) and skip the sets the merged template drops: one back-off per H lift, one set per V exposure, the accessories listed as dropped in `templates/3-day-week.md`. Whether the app lets you finish two program days on one calendar day was not verified; if it does not, ask an agent to render a merged-week variant file.
- **Deload** (every 4-6 passes or on two readiness flags): not encoded. Either edit the top-set weights to 0.90-0.92 of the track for one pass, one back-off, V and accessories at 1-2 sets, and add `/ progress: none` to the H lines for that pass, then restore the pre-deload loads, or ask an agent for a deload rendering.
- **Gaps.** The gap clock (`progression-tracks.md`, section 8) is not encoded. Hold the load after 8-21 days away from a lift; reduce 5-10% after 21 days. Edit the weight before the session.

## Known gaps between the rendering and the program rules

| Program rule | Rendered as | Gap | Manual fix |
|---|---|---|---|
| Top set 4 @ 8 or lower: +2.5 kg (squat, deadlift) or +1 kg (bench, press). RPE 8.5-9: hold. RPE 9.5-10 or under 4 reps: hold and count a miss | `lp(2.5kg)` / `lp(1kg)` on the H line | `lp()` reads completed reps, not RPE. It will advance after a 4 @ 9 that the program says to hold, and it may not advance if a back-off is stopped early at RPE 9 (the program says back-offs never touch the track). It also adds the step to the back-offs, which keeps them about 7% down | After each H: if the top set was RPE 8.5 or higher, edit the weight back down; if you stopped back-offs early but the top set was RPE 8 or lower, edit it up by the step. Keep the miss counter in your log. The documented fix is a `custom()` progression that reads `completedRPE`; it is not written or tested here yet |
| Stall after two misses: reset 7.5% | Not encoded | | Edit the weight; the agent re-renders |
| V sets at 90% of the **current** track | Absolute weights on `v:`-labelled lines with no progression | Labelled lines are separate exercises, so the V weight does not follow the H weight | When the Day 1-4 top set moves, edit the matching Day 5-6 weight to 90% of the new track, or ask the agent to re-render after each pass |
| Stale-track rule: last V set RPE 6 or lower twice running, take the increment anyway | Not encoded | | Watch the logged `+` RPE on V lines |
| Row and pull-up: fixed load, add reps until every set reaches 8 at RPE 8 or less, then +2.5 kg and back to the bottom; first set under the bottom of the range twice = drop 5% | `4x6 ... dp(2.5kg, 6, 8)` / `4x5 ... dp(2.5kg, 5, 8)` | The app adds one rep per successful exposure, not as many as you managed; it ignores RPE; the 5% drop is not encoded | If you beat the prescribed reps comfortably, edit the reps up. Edit the weight on a stall |
| Accessory double progression, drop 5% after two exposures without a rep gained | `dp(...)` at the bottom of the range | Same | Same |
| A repeated accessory (leg curl on Days 1, 3, 5; calf raise on Days 1 and 3; dumbbell lateral raise on Days 2 and 6) | One rule, on its first appearance | Reps and load move together on every day it appears | Intended: the template treats it as one exercise |

## Getting data back out

- **Free, by hand:** Me → Import / Export. "Export history to CSV file" gives one row per set (warm-ups included and flagged), with Workout DateTime, Program, Day Name, Exercise, required and completed reps, required and completed RPE, required and completed weight and unit, and notes. "Export data to JSON file" is the full backup. "Export all programs to text file" gives the Liftoscript. Drop the CSV in the repo; the agent loop in `guide/07-tracking-and-apps.md`, section 4, maps it to the eight-column log (the Day Name column gives the slot). [Import and Export](https://www.liftosaur.com/features/import-export).
- **Premium, automated:** the official REST API (`https://www.liftosaur.com/api/v1`, key from Me → API Keys, `Authorization: Bearer`) reads history and reads and writes programs; `POST /playground` checks a program and simulates a day without saving. This repo does not implement it. A key would follow the same secret rules as the Hevy key. [REST API doc](https://www.liftosaur.com/doc/api).
- Premium also gates the Apple Watch app, graphs, plates per side and rest-timer notifications. Monthly $4.99, yearly $39.99, lifetime $99.99 (US App Store, 2026-10-21).

## Re-rendering

An agent re-renders this file from the logged data at every block boundary (4-6 passes plus deload) and after any hold, miss, stall, reset, deload or gap event that the in-app `lp()` steps cannot express. It rewrites only the weights (and the V weights to 90% of the new tracks) and, after a second stall on a lift, the rep scheme for that lift (1 x 6 @ 8 with 3 x 6 back-offs for one block). Re-import by the same path you used the first time; a share link has to be generated again. Keep the rules of this file: notes as `///` lines, one progression per exercise, `v:` labels on V lines, double-progression sets at the bottom of the range.

## Checklist against liftosaur.com/doc/liftoscript

- [x] Week and day header syntax
- [x] Comment syntax (`///` hidden, `//` shown, whole lines only)
- [x] `lp()` trigger conditions (completed reps; no RPE) and `lp(2.5kg, 2)` for every second success
- [x] `dp()` argument order
- [x] Progression state is per exercise across the program; labels separate exercises
- [x] Bodyweight exercises with added load
- [x] Omitted weight with an RPE target
- [x] Exercise names in the built-in library
- [x] Rest-timer and warm-up syntax
- [x] Export formats and API (Premium for the API only)
- [ ] Paste into the web editor and confirm no errors with your own settings
- [ ] Whether the app lets you finish two program days on one calendar day (merged weeks)
- [ ] A `custom()` progression for the RPE hold rule, tested in the playground

## Sources

- `research/mobile-workout-trackers.md`: KQ1-KQ3 and KQ5, and the addendum "official-source verification (open internet)" of 2026-10-21 (verification table and the Liftoscript check of this file).
- `templates/6-day-week.md` (exercises, sets, reps, RPE targets, rest), `templates/rotation.json` (rest seconds, warm-up ramp and feeder, supersets, session notes), `templates/3-day-week.md` (what a merged session drops), `templates/progression-tracks.md` (starting loads, -7% back-offs, 90% V sets, increments, stall, deload, gap rules, accessory double progression), `guide/03-flexible-scheduling.md`, section 6 (the example loads).
- Liftosaur, official: [Liftoscript doc](https://www.liftosaur.com/doc/liftoscript), [REST API doc](https://www.liftosaur.com/doc/api), [Premium](https://www.liftosaur.com/features/premium), [Import and Export](https://www.liftosaur.com/features/import-export), [Sharing Programs](https://www.liftosaur.com/features/sharing-programs), source on [GitHub](https://github.com/astashov/liftosaur): `src/pages/planner/plannerExercise.grammar`, `src/pages/planner/plannerExerciseParser.ts`, `src/models/exercise.ts`, `src/playground/playground.ts`, `lambda/utils/apiv1.ts` (the playground endpoint validates with the same `PlannerProgram_evaluateFull` call that was run locally).
