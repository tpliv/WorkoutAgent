# WorkoutTrainer

A knowledge base for building effective lifting programs. The repository
accumulates sourced research on training science and turns it into a practical
training guide and ready-to-use weekly templates.

## Who this is for

The primary user trains with barbells, dumbbells, and machines, and has a
schedule that changes week to week: some weeks allow 5 to 6 sessions, other
weeks only 3. Every template and rule in this repo is written so that the same
program can scale between 3 and 6 days without losing progress.

## Layout

| Folder | Purpose |
| --- | --- |
| `research/` | Raw research notes written by agents. Each file covers one topic, cites its sources, and separates evidence from coaching convention. Notes are the record of what was found and are not rewritten after the fact. |
| `guide/` | The synthesized training guide. Each chapter draws on the research notes and gives rules and numbers a lifter can act on. |
| `tools/` | The Hevy integration, in one command (`python3 tools/hevy_sync.py`): pull workouts over the API, apply the progression rules, commit and publish the data to `main`, then bring the Hevy routines in step and read each back. The routines are the 12 rotation routines (six half-sessions, Full A/B/C, and the cross-block merges U1 + L2, U2 + L3, U3 + L1) plus dated copies of the current week's sessions in a Hevy folder called "This Week". `tools/week.py` changes the week. Also the CSV fallback and the history analyzer. |
| `data/` | The normalized training log, its summary, `tracks.json` and `track-state.md` (the live state of the progression tracks), the track log, `week.json` (this week's sessions) and `weekly-plan.md` (its generated tables and the reasoning), `checkins/` (one record per Sunday check-in), and the Hevy ids the tools need. Raw exports are gitignored. |
| `coach/` | Agent runbooks for the weekly coaching cadence: the Sunday check-in and the night-before workout brief. |
| `PORTABILITY.md` | What lives in the repo versus the Claude account, the cloud environment spec, and the checklist for moving to another account. |
| `templates/` | Weekly session templates for 3, 4, 5, and 6 training days, the per-lift progression rules (`progression-tracks.md`), the session contents as data (`rotation.json`, which the Hevy routines are rendered from), the rules for switching between week types, a Liftosaur export of the rotation (unmaintained since October 2026), and a CSV log template. |

## Reading order

1. `guide/00-overview.md` for the core principles in one page.
2. `guide/03-flexible-scheduling.md` for how to run a 3-day week and a 6-day week on the same program.
3. `templates/README.md` then the template for this week's day count.
4. `guide/07-tracking-and-apps.md` to pick a mobile tracker and set up logging; `tools/README.md` for the Hevy setup and the weekly sync.
5. `guide/08-weekly-coaching-cadence.md` for the Sunday check-in and the night-before workout brief.
6. `research/` when you want the evidence behind a rule.

## The program in one paragraph

One fixed rotation of six half-sessions: Lower A (squat heavy), Upper A (bench and
row heavy), Lower B (deadlift heavy), Upper B (press and pull-up heavy), Lower C
(squat and deadlift volume), Upper C (all upper lifts volume). A 6-day week runs
them as six sessions. A 3-day week merges each pair into a full-body session.
Every week type completes one pass, so each main lift gets one heavy and one
volume exposure per week and its load progression never depends on how many
days the week had. Shorter weeks drop accessory volume, never intensity.

## Guide chapters

| Chapter | Topic |
| --- | --- |
| `guide/00-overview.md` | Ten rules and a reading map |
| `guide/01-training-principles.md` | Volume, frequency, intensity, failure proximity, rest, maintenance dose |
| `guide/02-program-structures.md` | Splits and named programs by days per week, with a variable-week verdict |
| `guide/03-flexible-scheduling.md` | Running one program across 3- to 6-day weeks; race weeks; where runs go |
| `guide/04-periodization-and-progression.md` | Periodization evidence, progression schemes, rating accuracy, deloads, plateaus, returning after a layoff |
| `guide/05-exercise-selection.md` | Movement patterns, best exercises, substitutions, warm-up, technique |
| `guide/06-recovery-nutrition-cardio.md` | Recovery, sleep, protein, measuring body composition, alcohol, energy availability, running alongside lifting, sauna, age |
| `guide/07-tracking-and-apps.md` | What to log, tracker app comparison, integration workflows |
| `guide/08-weekly-coaching-cadence.md` | Sunday check-in, night-before workout brief, mid-week changes |

## Caveat on sources

The first research round was done from a sandbox that could not fetch most
journal and program web pages directly, so the notes rely on abstracts, search
summaries, and reputable secondary reviews. Each note flags numbers it could not
verify against the primary source. A follow-up pass with full web access should
verify the flagged items first.

## Contributing knowledge

Research is done by agents following the conventions in `CLAUDE.md`. In short:
one topic per file in `research/`, every claim cited, exact numbers kept, and
disagreements between sources recorded rather than smoothed over. The guide is
updated only after the underlying research note exists.
