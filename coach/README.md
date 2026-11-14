# Coach runbooks

Last updated: 2026-11-13 (one week file and `tools/week.py`; the sync commits and publishes before it touches Hevy; what to do when the repo is read-only). Earlier: 2026-11-10 (rule 4: busy-gym exceptions), 2026-10-26 (runs work on `main` of `tpliv/WorkoutAgent`; tracks updated by `tools/hevy_sync.py`)

Agent instructions for the weekly coaching cadence in `guide/08-weekly-coaching-cadence.md`. Scheduled tasks start a Claude session and point it at one of these files. The tasks and their prompts are recorded in `PORTABILITY.md`.

| Scheduled task | When (America/New_York) | Runbook | Ends with |
|---|---|---|---|
| Sunday training check-in | Sun 6:47 pm | `sunday-checkin.md` | The five questions. After your answers: the week plan and Monday's workout |
| Tomorrow's workout | Mon-Sat 7:47 pm | `nightly-brief.md` | Tomorrow's session, or one line on a rest day |

## The three stores and who writes them

`main` on GitHub is the source of truth. Hevy and the dashboard page are projections of it. One command keeps them in step.

| Fact | Lives in | Changed with | Never |
|---|---|---|---|
| Loads, counters, pointer, block week | `data/tracks.json` | `python3 tools/hevy_sync.py` (from the Hevy log); a hand amendment only with `python3 tools/update_tracks.py --set PATH=VALUE --reason "..."` | edit the JSON or the generated table in `data/track-state.md` |
| This week's sessions (date, slot, state), deload flag | `data/week.json` | `python3 tools/week.py plan / add / set / drop / status / deload` | edit the JSON, the tables between the markers in `data/weekly-plan.md`, or routine titles in Hevy |
| What the week means (spacing reasoning, race rules, cardio, changes) | `data/weekly-plan.md`, outside the generated block | by hand | restate loads there; they are in the generated table |
| Check-in answers and decisions | `data/checkins/YYYY-MM-DD.md` | by hand, Sunday | |
| Sets reported only in the chat | `data/manual-log.csv` (`templates/log-template.csv` columns, pounds) | by hand | |
| Logged history, Hevy ids, dashboard | `data/history.csv`, `data/hevy-state.json`, `dashboard/` | `python3 tools/hevy_sync.py` | by hand |
| The program | `templates/`, `guide/` | only by the CLAUDE.md update procedure | in a coaching run |

**`python3 tools/hevy_sync.py` is the only way anything reaches GitHub or Hevy.** In order: it checks that this checkout is current and can write to `main`; pulls new workouts; applies the progression rules; marks logged sessions done in the week; rebuilds the dashboard when data changed; commits the files above; publishes to `main`; then updates the Hevy routines that differ and reads each back. Run it after training is logged and after every change to the week or to a hand-written state file (`--no-pull` when nothing was trained; `-m "message"` sets the commit message). Never run `git commit` or `git push` yourself for these files, and never push to Hevy any other way.

Read its output every time. It ends with the week (with a **Checks** list: order, spacing, unlogged or unplanned sessions) and a push summary (updated, already in step, skipped with the reason, failed). A non-zero exit means something is not in step: say so in the message.

## When the repo is read-only

If the sync prints `Sync not started; nothing was changed`, the session cannot write to `tpliv/WorkoutAgent` (the repository is not attached to the scheduled task) or the checkout is behind `main`.

- Behind `main`: `git merge --ff-only origin/main`, then run the sync again.
- Cannot write: **change nothing.** Do not edit files, do not commit, do not try other ways to reach Hevy; the tools refuse on purpose, because a session that cannot save its state must not change what the lifter sees in the app. Send a read-only message instead: the first line says `Read-only run: I can't save to GitHub, so nothing was synced or changed. Attach tpliv/WorkoutAgent to this scheduled task (PORTABILITY.md, "Scheduled tasks").` Then give what the checkout already holds: `python3 tools/week.py show` and, for a brief, `python3 tools/week.py brief`. Say plainly that today's training is not folded in.

## Rules every run follows

1. **Branch.** Work on `main`, and say so explicitly: the checkout may start on another branch. `git fetch origin main && git checkout main && git merge --ff-only origin/main`. If `tpliv/WorkoutAgent` isn't checked out and the session has an add-repo tool, attach it with push access and clone it. Files outside the table above are never touched by these runs.
2. **Dates.** Get today's date with `TZ=America/New_York date +%F` (the tools print `today:` too). "Tomorrow" means tomorrow in that time zone. The server clock is UTC, which is already tomorrow after 7 pm (8 pm in summer): never take a date from plain `date`, from a commit time, or from the first 10 characters of a Hevy timestamp. The tools use the same zone (`tools/localtime.py`), and `data/history.csv` dates are local days.
3. **Units and plates.** Pounds everywhere the lifter sees. The smallest plate is 2.5 lb, so every barbell load is a multiple of 5 lb. Dumbbell loads are the total of the dumbbells in the hands, as the lifter logs them (two 20s = 40): multiples of 5 lb for two dumbbells, 2.5 lb for one. Machine loads are the nearest pin. Every load is a single number, never a range. `data/history.csv` stores kilograms (x 0.45359237) as the API returns them; the tools convert, so read loads from `data/tracks.json`, not from the CSV.
4. **Never** advance a load on a miss, during a deload, from a V exposure, or from a squat, bench, deadlift or press substitute (`guide/07-tracking-and-apps.md` §4). Two exceptions, both applied by `tools/update_tracks.py` (`templates/progression-tracks.md` §9): a row or pulldown variant updates its own load in `tracks.<lift>.variants` and counts as the exposure; and a lift with `h_owed` takes its top set at its next V exposure.
5. **Never** invent results. If the log has no data for a session and the lifter hasn't said, ask. Don't assume it went to plan.
6. **Rules come from the repo, not memory.** Loads: `templates/progression-tracks.md`. Week shape: `templates/README.md` and `guide/03-flexible-scheduling.md` §4. Session content: the matching `templates/N-day-week.md`.
7. **Medical.** For pain that changes movement, or illness, suggest a physician or physiotherapist. Give only general training guidance.
8. **Record changes.** Write what changed and why as a dated line in the check-in record (Sunday), or in the `Changes this week` list in `data/weekly-plan.md` (nightly).
9. **The last message is the deliverable.** The final text of the run is what the lifter sees in the notification. Put the questions or the brief there, not a summary of the git work.

## Getting the week's results

1. Run `python3 tools/hevy_sync.py`. The Hevy key is a network secret that the proxy adds, so `HEVY_API_KEY` is usually **not** set; do not test the variable. Read the output: the decisions (also appended to `data/track-log.md`), the week and its Checks, the push summary. A stall is only flagged: apply the reset with `--reset-on-stall` only after the check-in has covered sleep, food and bodyweight (§6).
2. The week reconciles itself. A logged workout whose title names the planned slot marks that session done. If the Checks say `planned X, logged Y`, the lifter trained something else: the week now records Y, the pointer has moved accordingly, and the rest of the week must be re-planned from the pointer (`tools/week.py`). If they say `no workout logged`, ask; never assume. A workout whose title names no slot: ask which session it was.
3. If only the Hevy push failed (the last step), run the sync again; the tracks are already updated, so never apply the rules a second time by hand.
4. If the Hevy API is down or the pull fails: take the results from the chat and append them to `data/manual-log.csv`. Apply §5 with logged amendments, one per changed value: `python3 tools/update_tracks.py --set bench.top_set_lb=115 --reason "chat: 110 x 4 @ 7.5 on 10 Nov"` (also `miss_counter`, `step_counter`, `last_exposure`, `pointer`). Then `python3 tools/hevy_sync.py --no-pull`. Mention the failure once in the message. When the API is back, the logged workout is pulled as usual; check the track log so the same session is not counted twice.

## Changing the week

Every change goes through `tools/week.py`, then the sync:

```
python3 tools/week.py show
python3 tools/week.py plan --week-of 2026-11-16 2026-11-17=L1@7:30-9:00am "2026-11-19=Full B" 2026-11-21=U2
python3 tools/week.py set 2026-11-19 --date 2026-11-20          # move a day
python3 tools/week.py set 2026-11-19 --slot U1 --note "why"      # change what is trained
python3 tools/week.py set 2026-11-17 --state missed
python3 tools/week.py deload on
python3 tools/hevy_sync.py --no-pull -m "Move Full B to Fri 20 Nov"
```

**Planning ahead is safe.** If this week still has sessions to come when you plan a later week, the new week is staged as "next week": this week stays as it is, the new week's dated routines are created in Hevy at once, and it becomes the week on its Monday. Its order check assumes the open sessions get trained first. Planning on Sunday night after the last session simply replaces the week.

The tool prints the week with rendered loads and the Checks. **Order:** the sessions still to come must cover the next half-sessions from the pointer; the rotation never skips ahead. Fix the plan until that check is clear. **Spacing** checks are advice; keep or change the plan and say why in `data/weekly-plan.md`. Dates are the lifter's (America/New_York). The dated Hevy routines (folder This Week) take their titles, loads and notes from this file; a session's `--note` leads its routine note.

Loads in any message come from `python3 tools/week.py show` or `brief`, never from arithmetic done in the chat: the tool applies the gap clock, regain and caution phases, moved top sets and deload exactly as the Hevy routine shows them.
