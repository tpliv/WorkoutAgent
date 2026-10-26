# Agent instructions for WorkoutTrainer

This repository is a knowledge base, not a software project. Agents working here
research resistance-training topics and turn the findings into a training guide.

## Goals of the knowledge base

- Help an intermediate lifter build and run an effective strength and
  hypertrophy program.
- Support a variable schedule: some weeks 5 to 6 training days, other weeks
  only 3. Every recommendation must say how it changes with available days.
- Prefer evidence from peer-reviewed research, then well-cited practitioner
  sources (Stronger By Science, Renaissance Periodization, Barbell Medicine,
  MASS Research Review, program authors' own writing). Say which is which.

## Where things go

- `research/<topic>.md`: one topic per file. Dense notes with citations. Keep
  exact numbers (sets, reps, percentages, effect sizes). Record conflicting
  findings instead of picking a side silently. Add a dated "Last updated" line
  at the top. Do not rewrite another note's conclusions; add a new note or an
  addendum section with the date.
- `guide/NN-<chapter>.md`: synthesized, actionable chapters. Every rule should
  trace back to a research note. Numbered for reading order.
- `templates/<days>-day-*.md`: concrete weekly layouts with exercises, sets,
  reps, and progression rules. Templates must state how they scale up or down.

## Research conventions

- Search broadly, then verify specific claims against the primary source.
- Cite with author, year, and journal or site, plus a URL when available.
- Distinguish strength outcomes from hypertrophy outcomes.
- Mark older foundational work (pre-2016) as such.
- Note paywall or copyright status when describing a named program, and
  describe rather than reproduce copyrighted material.

## Hevy integration (`tools/`)

The user logs in Hevy (Pro) and the repo talks to it over the Hevy API.

- The key is either a cloud-environment network secret for `api.hevyapp.com`
  (header `api-key`; the proxy adds it, nothing to configure in the session) or
  the `HEVY_API_KEY` environment variable. Never ask for it in chat, never
  print it, never write it to a file or commit. If a call returns 401, neither
  is set up: tell the user how (`tools/README.md`, Setup step 2).
- `python3 tools/hevy_sync.py --dry-run` shows what a sync would do; without
  the flag it pulls new workouts, applies `templates/progression-tracks.md` to
  them, rewrites `data/tracks.json`, `data/track-state.md` and
  `data/track-log.md`, rebuilds `dashboard/index.html`, and updates the nine
  routines in the app. Run it when the user asks for their loads, their next
  session, or an update after training. Commit the changed data and dashboard
  files afterwards, then republish `dashboard/index.html` to the existing
  dashboard page (URL in `tools/README.md`, "Progress dashboard"); never
  create a second page.
- `python3 tools/build_dashboard.py` rebuilds the dashboard alone (offline).
- The program runs in pounds (`data/tracks.json`, the routines, `data/track-state.md`).
  The Hevy API and `data/history.csv` carry kg; the tools convert.
- Read `data/tracks.json` for the current loads and the pointer (the next
  half-session owed); `data/track-log.md` for what changed and why.
- `templates/rotation.json` is the machine-readable rotation. When a markdown
  template changes, change the JSON too and push the routines again.
- A stall is only flagged; apply the reset with `--reset-on-stall` after
  checking the recovery inputs with the user (section 6 of the tracks file).
- Read-only questions ("what did I lift on Monday", "find the pulldown
  template") go through `python3 tools/hevy_api.py <command>`.
- Tests: `python3 tools/test_tools.py` (offline).

## Updating the guide

1. Write or update the research note first.
2. Change the guide chapter, referencing the note.
3. Update any template the change affects.
4. Add a line to `CHANGELOG.md` describing what changed and why.

## Portability

The repo must be movable to another Claude account at any time. See
`PORTABILITY.md`.

- Commit and push anything worth keeping. Do not leave results only in a chat,
  an artifact, memory, or a scheduled task.
- Read credentials from the environment. Never write them to the repo.
- Do not use work connectors or work systems for this project.
- When a change needs a new package, host, secret, or scheduled task, update
  the spec in `PORTABILITY.md` in the same commit.

## Style

- Markdown. Tables for comparisons. Short sentences.
- Units: the user lifts in pounds. Templates, progression rules, worked examples,
  and `data/track-state.md` are in pounds. `data/history.csv` stores kilograms
  internally; research notes quote whatever the source used. Be consistent
  within a file.
- No medical advice beyond general training guidance; flag when a reader should
  consult a professional.
