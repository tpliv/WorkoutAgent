# Liftosaur rendering of the rotation

Last updated: 2026-10-21

`rotation.liftoscript` is a best-effort Liftoscript version of the six half-sessions in `templates/6-day-week.md`, with the main-lift top-set and back-off structure and the accessory double progression from `templates/progression-tracks.md`. Why Liftosaur, and the alternatives: `guide/07-tracking-and-apps.md`.

## Read this first: what is not verified

The research note behind this file (`research/mobile-workout-trackers.md`) could not open liftosaur.com, so the file uses only the syntax the note saw quoted elsewhere, and guesses the rest. **Check every line tagged `UNVERIFIED` against https://www.liftosaur.com/docs before you import.** The gaps:

| Item | Status | Where it matters |
|---|---|---|
| Exercise line shape `Exercise / sets x reps weight @RPE / progress: rule` | Cited (Liftoscript doc, api3.liftosaur.com, agent-skill doc) | Every line |
| `@8+` logs the actual RPE; `%` means percent of 1RM; `kg` and `lb` number types | Cited | Every line; note that `%` is **not** percent of the top set, so back-offs are written as absolute weights |
| `progress: lp(5lb)` linear progression | Cited | Main-lift H lines |
| `dp(weight, minReps, maxReps)` signature | **Unverified** (from a community MCP server's fallback doc) | Every accessory line and the row and pull-up tracks |
| Week and day block headers (`# Week 1`, `## Day 1: ...`) | **Unverified** | The six section headers |
| Comment marker `//` | **Unverified** | Every comment; strip them if the parser rejects them |
| Whether `lp()` can be made conditional on the logged RPE | **Unverified**; `custom() { ... }` blocks with `{~ ~}` and a `weights` variable exist per the new-editor blog, grammar not seen | The hold rule (section 5) |
| Whether an exercise's weight state is shared across days | **Unverified** | V lines on Days 5-6 and the leg curl and calf raise repeats |
| Accessory lines with no starting weight (the note says the app estimates a weight from RPE tables when the weight is omitted) | Cited for plain lines; **unverified** in combination with `dp()` | All accessory lines |
| Added load on bodyweight lifts (pull-up `10kg`) | **Unverified** | Pull Up lines |
| Exercise names | Must match the app's exercise library or be created as custom exercises (custom exercises are cited in the README summary); the names used here are guesses | Every line |
| Rest timers and warm-up syntax | Not cited; configure in the app | Comments only |
| Share-link URL pattern, history export format, Premium price, API | **Unverified** | Getting data back out |

## Files

| File | What it is |
|---|---|
| `rotation.liftoscript` | The six half-sessions, Day 1 = L1 through Day 6 = U3, with starting loads from the worked example in `guide/03-flexible-scheduling.md`, section 6 |
| `README.md` | This file |

## How to import

Three paths, all cited by the research note:

1. **Web editor.** Open Liftosaur's web editor on a desktop, create a new program, paste the contents of `rotation.liftoscript`, fix anything the parser flags, save. The program syncs to the phone with an account.
2. **Text snippet in the app.** The App Store listing says a shared program text can be added to the app directly. Copy the file contents and paste where the app asks for program text.
3. **Share link.** Once imported, generate a share link from the app and keep it with your own notes. A later re-render can be imported the same way and the old program deleted or archived.

Importing appears to work in the free app; the note ties Premium to the API and found no paywall on text import, but this is **unverified**.

## What to adjust before the first session

1. **Starting loads.** The file carries the worked example (squat 120, bench 85, deadlift 150, press 55, row 70, pull-up +10 kg). Replace them using `templates/progression-tracks.md`, section 2: 95% of a recent 5RM, or 80% of a recent 1RM, or work up on the first H exposure and type in what 4 reps at RPE 8 turned out to be. Then recompute the dependent numbers:

   | Line | Formula | Example (squat 120) |
   |---|---|---|
   | H back-off weight | top set x 0.93, rounded to the nearest loadable weight | 111.6 -> 112.5 |
   | V weight (Days 5-6) | top set x 0.90, rounded | 108 -> 107.5 |
   | Pull-up V added load | reduce until the sets land at RPE 7; 0 kg = bodyweight | +10 -> +5 |

2. **kg or lb.** The file is in kg. For pounds, change every `kg` to `lb` and the increments: `lp(2.5kg)` -> `lp(5lb)`, `lp(1kg)` -> `lp(2.5lb)`, `dp(2.5kg, ...)` -> `dp(5lb, ...)`, dumbbell steps `2kg` -> `5lb`. Set the app's rounding to your plates (plate rounding is a cited feature).
3. **Exercise names.** Match each name to the app's library or create a custom exercise. The "or" alternatives in the comments are the template's substitutions.
4. **Accessory starting loads.** Either leave the weight off and let the app estimate from the RPE target, or write the load you can lift for the bottom of the range with 2-3 reps in reserve (`progression-tracks.md`, section 11). Dumbbell increments (`2kg`) should be one step on your rack.
5. **Warm-ups and rest.** Configure in the app: on the first compound of each day the empty bar x 5, then 80% x 2-3 of the first set (the top set); once the top set is 102.5 kg (225 lb) or more, add 60% x 3 between them (coaching convention, not evidence). Later main lifts one feeder set at 60-70%. Rest 3-4 min after a top set (deadlift 3-5), 2-3 min between compound sets, 60-90 s on isolation.

## How the app runs the rotation

- **Pointer.** Finishing a workout advances the program to the next day whatever the calendar says (research note, KQ3). Day 6 returns to Day 1. That is the pointer in `guide/03-flexible-scheduling.md`, section 1.4; you never pick a day by weekday.
- **Short weeks.** The file is the split form. In a 3-, 4- or 5-day week, do two consecutive program days in one gym visit (L3 then U3 = Full C; L1 then U1 = Full A; L2 then U2 = Full B; merge C first, then A, then B) and skip the sets the merged template drops: one back-off per H lift, one set per V exposure, the accessories listed as dropped in `templates/3-day-week.md`. Whether the app lets you finish two program days on one calendar day was not verified; if it does not, ask an agent to render a merged-week variant file.
- **Deload** (every 4-6 passes or on two readiness flags): not encoded. Either edit the top-set weights to 0.90-0.92 of the track for one pass, one back-off, V and accessories at 1-2 sets, and restore the pre-deload planned loads afterwards, or ask an agent for a deload rendering.
- **Gaps.** The gap clock (`progression-tracks.md`, section 8) is not encoded. Hold the load after 8-21 days away from a lift; reduce 5-10% after 21 days. Edit the weight before the session.

## Known gaps between the rendering and the program rules

| Program rule | Rendered as | Gap | Manual fix until `custom()` is verified |
|---|---|---|---|
| Top set 4 @ 8 or lower: +2.5 kg (squat, deadlift) or +1 kg (bench, press). RPE 8.5-9: hold. RPE 9.5-10 or under 4 reps: hold and count a miss | `lp(2.5kg)` / `lp(1kg)` on the H line | `lp()` as understood advances when the sets are completed; it does not read RPE, so it will advance after a 4 @ 9 that the program says to hold, and it may refuse to advance if a back-off is stopped early at RPE 9 (the program says back-offs never touch the track) | After each H: if the top set was RPE 8.5 or higher, edit next week's weight back down; if you stopped back-offs early but the top set was RPE 8 or lower, edit the weight up by the increment. Keep the miss counter in your log |
| Stall after two misses: reset 7.5% | Not encoded | | Edit the weight; the agent re-renders |
| V sets at 90% of the **current** track | Absolute weights with no progress rule | The V weight does not follow the H weight unless the app shares state across days (unverified) | When the Day 1-4 top set moves, edit the matching Day 5-6 weight to 90% of the new track. Or ask the agent to re-render after each pass |
| Stale-track rule: last V set RPE 6 or lower twice running, take the increment anyway | Not encoded | | Watch the logged `+` RPE on V lines |
| Row and pull-up: fixed load, add reps until every set reaches 8 at RPE 8 or less, then +2.5 kg and back to the bottom; first set under the bottom of the range twice = drop 5% | `dp(2.5kg, 6, 8)` / `dp(2.5kg, 5, 8)` | Signature unverified; the 5% drop is not encoded | Edit the weight on a stall |
| Accessory double progression, drop 5% after two exposures without a rep gained | `dp(...)` | Same | Same |
| 1 kg bench and press steps need 0.5 kg plates | `lp(1kg)` | Without fractional plates the rule is 2.5 kg every second successful exposure | Use `lp(2.5kg)` and skip every other increment by hand, or let plate rounding do it (cited feature; behaviour with 1 kg steps unverified) |

## Getting data back out

The research note could not confirm Liftosaur's history export format or the API (a third-party page says Premium plus a personal API key). Until that is checked, keep the main-lift sets in the repo CSV (`templates/log-template.csv`, layout in `guide/07-tracking-and-apps.md`, section 5) or export from the app by hand and drop the file in the repo. The agent loop in `guide/07-tracking-and-apps.md`, section 4, reads either.

## Re-rendering

An agent re-renders this file from the logged data at every block boundary (4-6 passes plus deload) and after any hold, miss, stall, reset, deload or gap event that the in-app `lp()` steps cannot express. It rewrites only the weights and, after a second stall on a lift, the rep scheme for that lift (1 x 6 @ 8 with 3 x 6 back-offs for one block). Re-import by the same path you used the first time.

## Verification checklist against liftosaur.com/docs

- [ ] Week and day header syntax
- [ ] Comment syntax
- [ ] `lp()` trigger conditions and whether it reads logged RPE
- [ ] `dp()` argument order
- [ ] Whether weight state is per exercise or per exercise-per-day
- [ ] Bodyweight exercises with added load
- [ ] Omitted weight together with `dp()`
- [ ] Exercise names in the library
- [ ] Export or API for history (and whether Premium is needed)

## Sources

- `research/mobile-workout-trackers.md`, KQ1 (Liftosaur profile), KQ2 (Liftoscript syntax and gaps), KQ3 (sequence-driven rotation), KQ5 (integration path and caveats).
- `templates/6-day-week.md` (exercises, sets, reps, RPE targets, rest), `templates/3-day-week.md` (what a merged session drops), `templates/progression-tracks.md` (starting loads, -7% back-offs, 90% V sets, increments, stall, deload, gap rules, accessory double progression), `guide/03-flexible-scheduling.md`, section 6 (the example loads).
- Liftosaur: [docs](https://www.liftosaur.com/docs), [Liftoscript doc](https://www.liftosaur.com/doc/liftoscript), [GitHub README](https://github.com/astashov/liftosaur), [new program editor blog](https://www.liftosaur.com/blog/posts/new-experimental-program-editor), [api3.liftosaur.com "How it works"](https://api3.liftosaur.com), [App Store listing mirror](https://apps.appfollow.io/ios/liftosaur-scriptable-workouts/1661880849?country=td), community [liftosaur-mcp](https://huggingface.co/spaces/davanstrien/liftosaur-mcp/blob/main/app.py) and [program-creator skill](https://agentskills.so/skills/pbantolas-liftosaur-program-creator-liftosaur-program-creator) (sources of the unverified `dp`/`sum` signatures).
