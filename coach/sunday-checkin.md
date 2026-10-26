# Runbook: Sunday check-in

Last updated: 2026-10-21

Protocol: `guide/08-weekly-coaching-cadence.md` section 2. General rules: `coach/README.md`. This is a conversation with two turns. Turn 1 asks; turn 2, after the lifter answers, plans and delivers.

## Turn 1: prepare and ask

1. Fetch and check out the branch the scheduled task names. Read the following:
   - `data/track-state.md`
   - `data/weekly-plan.md`
   - the newest file in `data/checkins/`
   - `templates/README.md`
   - `templates/progression-tracks.md`
2. Get the week's results (`coach/README.md`, "Getting the week's results"). Find every session since the last check-in.
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
3. Bodyweight this morning?
4. How many days can you train this week, and which ones?
5. Anything to plan around (travel, different gym, illness)?

Reply tonight and Monday's full workout comes straight back.
Training Monday before you reply? Do <merged session from the pointer, e.g. Full A>: <main lifts with loads, one line each>; accessories as in the <N>-day template.
```

If a session has no logged data, add it to question 1. Ask for its top sets; don't assume them. The provisional Monday session is the pointer's half-session merged with the next one (the 3-day default). It is correct for any 3-4-day week. In a 5-6-day week it costs one merge, which the plan absorbs when it is re-laid from the new pointer.

## Turn 2: plan and deliver (after the lifter replies)

1. **Fold in last week.** Add any results reported in the chat to `data/manual-log.csv`. Then update each track in `data/track-state.md` from its H exposure:
   - increment, hold or miss per §5 (bench and press: update the step counter);
   - stall reset per §6;
   - add to the e1RM history (§10);
   - set the last-exposure date.
   Accessories use double progression (§11).
2. **Readiness.** Write the four scores and bodyweight to the check-in record. A score of 1-2 on the same item two Sundays running is one flag (`guide/08` §2.3). Count the performance flags: reps down or RPE up at the same load on two consecutive exposures of a lift.
3. **Deload decision** (`guide/03` §4.5). Deload if any of these holds:
   - it is block week 5-7, and preferably a 3-day week when the calendar allows;
   - there are two flags;
   - the lifter is ill.
   Do not schedule two deloads within four weeks.
4. **Week shape.**
   - Merges = 6 minus days. Pick the template.
   - If the pointer is not at L1, write the next six half-sessions from the pointer and apply the merges (`templates/README.md`, "The rotation pointer").
   - Place sessions on the days given, following the template's "Placement" line. Don't put two merged sessions with heavy top sets back to back if a gap is possible.
   - 2 days: `guide/03` §4.6. 7 days: train 6.
5. **Loads.**
   - Apply the gap clock (§8) to each main lift for its first exposure this week.
   - Back-offs are the top set x 0.93; V sets are 90% of the track load. Round every barbell load to the nearest 5 lb; the smallest plate is 2.5 lb (§9). Dumbbells: one load in 2.5 lb steps (per dumbbell); machines: the nearest pin; never a range. Bench and press advance through the step counter (§5).
   - If deloading: top sets x 0.90-0.92 at RPE 6-7, one back-off, V at 2 sets, accessories 1-2 sets.
6. **Cardio**: place it per `guide/03` §7.
7. **Write the files.**
   - `data/weekly-plan.md`: the whole file, in its format.
   - `data/checkins/<today>.md`: answers, flags, decisions, and every rule that fired, with its section.
   - `data/track-state.md`: update the "Last updated" line.
8. Commit with the message `Check-in <date>: <days>-day week, <deload or block week k>`, then push.
9. **Send the plan, then Monday's brief** if Monday is a training day. Format: `coach/nightly-brief.md`, step 5. Message:

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

If the lifter changes the plan in a later reply, redo steps 4-9 for the change.

## If there is no reply

The Monday nightly run checks `data/weekly-plan.md`. If its status is still `awaiting check-in`, that run plans a provisional **3-day week**: Mon/Wed/Fri if Monday is still open, otherwise the next three days with a rest day between where possible. It uses the lower day count (`guide/03` §4.1 step 1). It sends Tuesday's brief, if any, and repeats the five questions. A later reply re-plans the rest of the week from the pointer.
