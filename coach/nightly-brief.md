# Runbook: night-before brief

Last updated: 2026-11-13 (sync every night; the week changes through `tools/week.py`; the brief's numbers come from `tools/week.py brief`). Earlier: 2026-11-10 (busy-gym "Rack taken" line and moved top sets), 2026-11-06 (top-set rating line, rep-out, race-week rules), 2026-10-26 (tracks via `tools/hevy_sync.py`; short warm-up ramp)

Protocol: `guide/08-weekly-coaching-cadence.md` section 3. General rules: `coach/README.md`. Runs Mon-Sat at 7:47 pm America/New_York. Sunday's run delivers Monday's brief, so this run covers Tuesday to Sunday.

## Steps

1. **Load state.** Check out `main` (`coach/README.md`, rule 1). Then:
   - Get today's date and tomorrow's: `TZ=America/New_York date +%F` and `TZ=America/New_York date -d tomorrow +%F`. At 7:47 pm the server's own date is already tomorrow; do not use it.
   - `python3 tools/hevy_sync.py`, every night, planned day or not. It folds in whatever was trained, marks it done in the week, saves and publishes, and brings Hevy in step. With no news it changes nothing. If it prints `Sync not started`, follow `coach/README.md`, "When the repo is read-only", and stop there.
   - Read its output (the decisions, the week, the **Checks**, the push summary), then `data/weekly-plan.md` for the reasoning behind the week.
2. **Check the plan's status** (first line of the week).
   - **Tomorrow is before the plan's `Week of` date** (the first check-in hasn't happened yet): change nothing. End with one line: `Coaching starts with the check-in on Sun <date>, 6:47 pm.`
   - **`awaiting check-in`** and today is Monday: plan a provisional 3-day week (`coach/sunday-checkin.md`, "If there is no reply") with `tools/week.py plan --status provisional ...`. Then carry on.
   - **`awaiting check-in`** and today is later in the week: the lifter has gone quiet. Send one line asking how many days remain, and don't brief.
   - **`week over`** (Saturday run, plan finished): do nothing.
3. **Act on the Checks.**
   - **None:** carry on.
   - **`planned X, logged Y`:** the lifter trained a different session. The week already records Y and the pointer has moved. Re-plan the days that remain from the pointer (`guide/03` §4.1, "If days change mid-week") with `tools/week.py set` / `add` / `drop` until the `order` check is clear.
   - **`no workout logged` for a past day:** don't assume. The pointer stays. If the lifter hasn't said either way, leave the session as it is and open tomorrow's brief with "No log for <day>'s <slot>; if you trained, reply with the top sets." Once the lifter says it was missed: `tools/week.py set <date> --state missed`, then apply `guide/08` §3.2: recount the remaining days and the half-sessions left in the pass, re-merge what is left, and rewrite the rest of the week with `tools/week.py`.
   - **`logged but was not in the plan`:** an extra session. It is in the week now; re-plan what remains from the pointer.
   - **`order`:** the remaining sessions skip ahead of the pointer. Fix the week; never brief a session that is not the next one owed.
   - Add one line per change to `Changes this week` in `data/weekly-plan.md`, then `python3 tools/hevy_sync.py --no-pull -m "<what changed>"`.
4. **Is tomorrow a training day?** If not, end with a single line: `Rest day tomorrow. Next: <day> <session>.` Never send a workout for a rest day.
5. **Render tomorrow's session:** `python3 tools/week.py brief <tomorrow>`. It prints the title, the time, the pointer move, "Why anything changed", every exercise with its warm-ups, sets, loads and rest, and the "Station taken" fallbacks, from the same code that renders the Hevy routine. Use its numbers as printed; never recompute a load. Add what the tool does not print:
   - the template's cut order as a "Short on time" line (the matching `templates/N-day-week.md`);
   - a "Rate it" line on each top set: up to 6 reps if rep 4 is clearly easy; one tap, 7 easy, 8 on target, 9 hard, 10 nothing left (`progression-tracks.md` §3);
   - if a race is within 7 days before or after tomorrow, the race-week or after-race line from `guide/03` §4.7 (for example "R+3: deadlift top set capped at RPE 7; below plan is a hold");
   - a rep-out the tool lists under "Why anything changed" stays unless tomorrow is a deload, a race week, or the lift comes second in a merged session; say so if you drop it.
   Use the layout in `guide/08` §3.1.
6. **Record the brief.** `python3 tools/week.py set <tomorrow> --state briefed`, then `python3 tools/hevy_sync.py --no-pull -m "Brief <tomorrow>: <slot>"`.
7. **Send the brief** as the final message.

## Replies

If the lifter replies with results, a missed day, or a change of days:
- results: run `python3 tools/hevy_sync.py` if they are in Hevy; otherwise record them as in `coach/README.md`, "Getting the week's results", step 4;
- a missed day or a change of days: change the week with `tools/week.py` (step 3 above), add the line to `Changes this week`;
- `python3 tools/hevy_sync.py --no-pull -m "<what changed>"`: this is what puts the change in Hevy and on GitHub. Check the push summary before telling the lifter Hevy is updated;
- re-render tomorrow's brief (`tools/week.py brief`) if it changed, and say what changed in one line.
