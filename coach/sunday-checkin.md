# Runbook: Sunday check-in

Last updated: 2026-11-13 (the week is planned with `tools/week.py`; the sync saves everything in both turns; loads come from the tool, not arithmetic). Earlier: 2026-11-06 (drinks and runs in the questions; race weeks; regain, caution and rep-out in the loads), 2026-10-26 (tracks via `tools/hevy_sync.py`; works on `main`)

Protocol: `guide/08-weekly-coaching-cadence.md` section 2. General rules: `coach/README.md`. This is a conversation with two turns. Turn 1 asks; turn 2, after the lifter answers, plans and delivers.

## Turn 1: prepare and ask

1. Check out `main` (`coach/README.md`, rule 1). Read the following:
   - `python3 tools/week.py show` (this week as planned and as trained)
   - `data/tracks.json`, `data/track-state.md` and `data/track-log.md`
   - `data/weekly-plan.md`
   - the newest file in `data/checkins/`
   - `templates/README.md`
   - `templates/progression-tracks.md`
2. Get the week's results: `python3 tools/hevy_sync.py` (`coach/README.md`, "Getting the week's results"). It commits and publishes what it changes, so nothing is left unsaved when this turn ends. If it prints `Sync not started`, follow "When the repo is read-only" there and still ask the five questions. Find every session since the last check-in.
3. Build the recap:
   - sessions planned vs done, by slot;
   - each main lift's top set as load x reps @ RPE, and whether it counts as a hit, hold or miss (`progression-tracks.md` §5);
   - the pointer;
   - block week.
4. Check for a scheduled deload: block week 5-7, or a reactive trigger already on record. Don't decide yet; it depends on the answers.
5. Send this message, then end the turn:

```
Sunday check-in, week of <Mon date>.

Last week: <n> of <m> sessions (<slots>). Pointer: <slot>. Block week <k> of 6.
Top sets: Squat <load x reps @RPE> (<hit/hold/miss>), Bench ..., Deadlift ..., Press ..., Row ..., Pull-up ...
<one line on anything notable: a miss, a gap, a deload due, sessions missing from the log>

Five quick ones:
1. Anything the log won't show (skips, swaps, pain, how the top sets felt)?
2. Sleep, soreness, stress, joint pain, 1-5 each (5 = best)?
3. Bodyweight this morning, and waist if you measured it? Drinks last week (how many, which nights)?
4. How many days can you train this week, and which ones?
5. Anything to plan around (travel, different gym, illness, a race or long run)?

Reply tonight and Monday's full workout comes straight back.
Training Monday before you reply? Do <merged session from the pointer, e.g. Full A>: <main lifts with loads, one line each>; accessories as in the <N>-day template.
```

If a session has no logged data, add it to question 1. Ask for its top sets; don't assume them. The provisional Monday session is the pointer's half-session merged with the next one (the 3-day default). It is correct for any 3-4-day week. In a 5-6-day week it costs one merge, which the plan absorbs when it is re-laid from the new pointer.

## Turn 2: plan and deliver (after the lifter replies)

1. **Fold in last week.** Logged sessions were applied by the sync in turn 1; run it again first if the lifter trained since. If `data/track-log.md` flagged a stall and the answers rule out sleep, food and bodyweight as the cause (§6), run `python3 tools/hevy_sync.py --no-pull --reset-on-stall`. Results reported only in the chat go to `data/manual-log.csv` and into the tracks with logged amendments (`coach/README.md`, "Getting the week's results", step 4). Accessories use double progression (§11): change an accessory load with `python3 tools/update_tracks.py --set "accessories.<name>.weight_lb=<load>" --reason "..."`.
2. **Readiness.** Write the four scores, bodyweight, waist and the drinks count to the check-in record (drinks: `guide/06` §4.4). A score of 1-2 on the same item two Sundays running is one flag (`guide/08` §2.3). Count the performance flags: reps down or RPE up at the same load on two consecutive exposures of a lift.
3. **Deload decision** (`guide/03` §4.5). Deload if any of these holds:
   - it is block week 5-7, and preferably a 3-day week when the calendar allows;
   - there are two flags;
   - the lifter is ill.
   Do not schedule two deloads within four weeks.
4. **Week shape.**
   - Merges = 6 minus days. Pick the template.
   - Write the next six half-sessions from the pointer and apply the merges (`templates/README.md`, "The rotation pointer"). The pointer is in `python3 tools/week.py show`.
   - Place sessions on the days given, following the template's "Placement" line. Don't put two merged sessions with heavy top sets back to back if a gap is possible.
   - 2 days: `guide/03` §4.6. 7 days: train 6.
   - If an InBody scan date falls in the week (`data/body-composition.md` §8), keep the 48 h before it free of lifting and say so in the plan.
5. **Write the week.** One command; add `--deload` for a deload week:

   ```
   python3 tools/week.py plan --week-of <Monday> <date>=<slot>@<time> <date>=<slot> ...
   ```

   Read what it prints. **Checks** must not show an `order` line: the sessions have to follow the rotation from the pointer. Treat `spacing` lines as advice and decide. Add a note to any session that needs one (race rule, a cap, a moved top set): `python3 tools/week.py set <date> --note "..."`; the note leads that routine in Hevy.
6. **Loads.** Do not compute them. The table `week.py` printed has each session's main lifts with the gap clock (§8), regain and caution phases (§5.1-5.2), moved top sets and the deload already applied, and the Hevy routines are rendered from the same code. Check them against the rules and the answers, and look for what the tool cannot know: a rep-out that should wait (deload, race week, or a later lift in a merged session), pain, illness. If a load must differ, amend the track with `update_tracks.py --set ... --reason` and say why in the check-in record.
7. **Runs and cardio**: place them per `guide/03` §7 (lift first on lower days; long and quality runs 48 h before a heavy lower slot). If a race falls in this week or fell in the last 7 days, apply `guide/03` §4.7 to the lower slots and the runs, and add the fueling days from `data/body-composition.md` (pattern in §5.1).
8. **Write the hand-written files.**
   - `data/weekly-plan.md`, outside the generated block: update "Last updated", the spacing reasoning, race or deload notes, cardio, and start a fresh "Changes this week" list. Do not restate loads.
   - `data/checkins/<today>.md`: answers, flags, decisions, and every rule that fired, with its section.
9. **Save and push everything:** `python3 tools/hevy_sync.py --no-pull -m "Check-in <date>: <days>-day week, <deload or block week k>"`. In the push summary every session of the new week must read `updated` or `in step`. If it stops with an error, say so in the message; do not work around it.
10. **Send the plan, then Monday's brief** if Monday is a training day (`python3 tools/week.py brief <Monday>`; format: `coach/nightly-brief.md`, step 5). Message:

```
This week: <days>-day week, block week <k><, deload>.
| Day | Session | Main lifts |
|---|---|---|
| Mon 27 Oct | Full A | Squat H 135, Bench H 95, Row H 70 |
| ... |
Cardio: <days>. Changes: <rules that fired, or "none">.
Reply to change anything.

<Monday's brief>
```

If the lifter changes the plan in a later reply, redo steps 4-10 for the change.

## If there is no reply

The Monday nightly run checks `data/weekly-plan.md`. If its status is still `awaiting check-in`, that run plans a provisional **3-day week**: Mon/Wed/Fri if Monday is still open, otherwise the next three days with a rest day between where possible. It uses the lower day count (`guide/03` §4.1 step 1). It sends Tuesday's brief, if any, and repeats the five questions. A later reply re-plans the rest of the week from the pointer.
