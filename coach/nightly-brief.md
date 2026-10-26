# Runbook: night-before brief

Last updated: 2026-10-26 (tracks via `tools/hevy_sync.py`; short warm-up ramp)

Protocol: `guide/08-weekly-coaching-cadence.md` section 3. General rules: `coach/README.md`. Runs Mon-Sat at 7:47 pm America/New_York. Sunday's run delivers Monday's brief, so this run covers Tuesday to Sunday.

## Steps

1. **Load state.** Fetch and check out `main` (`coach/README.md`, rule 1). Then:
   - Read `data/weekly-plan.md`, `data/tracks.json` and `data/track-state.md`.
   - Get today's date and tomorrow's: `TZ=America/New_York date +%F` and `TZ=America/New_York date -d tomorrow +%F`.
2. **Check the plan's status.**
   - **Tomorrow is before the plan's `Week of` date** (the first check-in hasn't happened yet): change nothing. End with one line: `Coaching starts with the check-in on Sun <date>, 6:47 pm.`
   - **`awaiting check-in`** and today is Monday: plan a provisional 3-day week (`coach/sunday-checkin.md`, "If there is no reply"). Then carry on.
   - **`awaiting check-in`** and today is later in the week: the lifter has gone quiet. Send one line asking how many days remain, and don't brief.
   - **`week over`** (Saturday run, plan finished): do nothing.
3. **Fold in today.**
   - If today was a planned training day, get the results (`coach/README.md`, "Getting the week's results").
   - If a slot was trained, `python3 tools/hevy_sync.py` has already applied it (`coach/README.md`, "Getting the week's results"): increment, hold or miss (§5, with the bench and press step counter), the e1RM history, the last-exposure date, and the pointer (+1 for a split session, +2 for a merged one). Read `data/track-log.md` for what fired. Do not edit the tracks by hand unless the results came only from the chat (fallback, step 3 there).
   - Mark the day `done` in the plan.
   - **No data for a planned day:** don't assume. The pointer stays. If the lifter hasn't said either way, tomorrow's brief opens with "No log for today's <slot>; if you trained, reply with the top sets."
   - **A day was missed:** apply `guide/08` §3.2:
     - recount the remaining days and the half-sessions left in the pass;
     - re-merge what is left (`guide/03` §4.1, "If days change mid-week");
     - rewrite the rest of the plan;
     - add the change to `Changes this week`.
4. **Is tomorrow a training day?** If not, commit any changes from step 3, push, and end with a single line: `Rest day tomorrow. Next: <day> <session>.` Never send a workout for a rest day.
5. **Render tomorrow's session.** Use the matching template file and the slot's section, exactly as written:
   - exercise order, sets x reps, target RPE, rest;
   - in merged sessions, the merged set counts;
   - the deload form if the plan says deload.
   Fill in the loads:
   - main-lift top set from `data/tracks.json` (the Hevy routine for the slot carries the same loads after a sync);
   - back-offs = top x 0.93; V = 90% of track; every barbell load rounded to the nearest 5 lb (§9);
   - the gap clock (§8) if this is the lift's first exposure since a gap;
   - accessories from `data/tracks.json` `accessories`, or the last logged load per §11. Give one load per exercise, never a range;
   Add:
   - the warm-up ramp on the first compound: bar x 5, then 80% x 2-3 of the top set (add 60% x 3 between them once the top set is 225 lb or more), each rounded to the nearest 5 lb (never below the 45 lb bar);
   - one feeder set at 60-70% for each later main lift, rounded to the nearest 5 lb (the empty 45 lb bar if that is lower);
   - the template's cut order as the "Short on time" line.
   Use the layout in `guide/08` §3.1.
6. **Write and push.** Update `data/weekly-plan.md` with the tomorrow row, the brief sent, and the time. Commit with the message `Brief <tomorrow>: <slot>`, then push.
7. **Send the brief** as the final message.

## Replies

If the lifter replies with results, a missed day, or a change of days:
- apply step 3 or the mid-week rule;
- re-render tomorrow's brief if it changed, and say what changed in one line;
- commit and push.
