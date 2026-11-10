# Track log

Append-only record of what `tools/update_tracks.py` changed and why. Newest at the bottom.

## 2026-10-27

- 2026-10-27 Full A Bench press: top 105 x 6 -> 6 @ 8: success 1 of 2; hold 105, +5 after the next one
- Flag: no RPE logged on the Bench press top set (105 x 6); treated as RPE 8
- 2026-10-27 Full A Bench press, amended by hand: the lifter reported RPE 8 on 105 x 6. Six reps at RPE 8 is at least 4 reps at RPE 6, the "4 reps at RPE 7 or lower" row of §5: big step +5 to 110 at once, step counter cleared (was: success 1 of 2, hold 105). The engine does not yet credit reps above the target.
- 2026-10-27 Full A squat and barbell row: rack taken; leg press and DB row substituted and not counted (§9). Squat and row tracks unchanged.
- 2026-10-27 Accessory: lateral raise 15 -> 20 lb per dumbbell (logged 20 x 12, 14, 12, 12 on 27 Oct, all in range; §11 records the load used).

## 2026-11-06

- 2026-10-29 L2 Deadlift: top 145 x 4 -> 4 @ 8: +5 to 150
- Flag: no RPE logged on the Deadlift top set (145 x 4); treated as RPE 8
- 2026-11-06 Race week (4-5 Nov), amended by hand. The workout titles ("Race Week 1 - Tue (U2 + L3)", "Race Week 2 - Wed (U3 + L1)") do not start with a slot, so the engine read them as "other". They are the rotation's U2, L3, U3 and L1 at race-week volume, so they count as those half-sessions (`guide/03` §4.4: merged sets dropped, not postponed). Pointer U2 -> U1 (U1, planned Fri 6 Nov, not done).
- 2026-11-05 L1 (race week) Back squat: top 155 x 5, no RPE (planned 135 x 4). First barbell squat in 19 days, so the 15-21-day row of §8 applies: hold the load lifted, no increment. Track 135 -> 155, back-offs 145, V 140. If 155 x 4 comes in at RPE 7 or lower next time, take the +10 big step (§5).
- 2026-11-04 U2 (race week) Overhead press: top 70 x 4, no RPE (planned 60 x 4), then 65 x 5 x 3. Treated as RPE 8: success 1 of 2 at 70, step counter 1. Track 60 -> 70, back-offs 65, V 65.
- 2026-11-04/05 Bench 105 x 6 x 2, deadlift 135 x 5, 4, row 65 x 8 x 2: V exposures, tracks unchanged (bench 110, deadlift 150, row 70).
- 2026-11-04/05 Pulldown 100 x 5, 6, 6 and 110 x 5, 6 on a different gym's stack: not comparable with the home stack, so the pull-up track stays at 125. Logged as V for the gap clock.
- 2026-11-06 Accessories: incline DB curl 25 -> 30 lb (standing curl 35 x 12, 10, 8 on 4 Nov; incline runs lighter). Reverse lunge 30 -> 32.5 lb (30 x 12 per leg x 3 on 29 Oct, top of 8-12). Lateral raise holds 20 (16, 18; range 12-20). Overhead triceps extension holds 25 (25 x 8, 27.5 x 8, under the 10-15 range).
- Flag: no RPE logged on any set from 29 Oct to 5 Nov. Every decision above assumes RPE 8.
- 2026-11-06 Dumbbell convention: the lifter logs the total of both dumbbells (confirmed 6 Nov; the 2024 history fits only that reading, e.g. DB bench 90 x 6 against a 105 barbell bench). Program loads are now totals. Accessories: incline DB press 35 per dumbbell -> 70 total (same weight); lateral raise stays 20 total (10 each; the routine had said 20 per dumbbell, double what was lifted); incline DB curl 30 -> 30 total (15 each; the earlier 30 per dumbbell assumed per-dumbbell logs); reverse lunge 32.5 per dumbbell -> 35 total (30 total x 12 per leg, +5 total). Overhead triceps extension unchanged (one dumbbell, 25).

## 2026-11-10

- 2026-11-10 U1 Bench press: top 110 x 6 -> rep-out 6; 6 @ 7: big step to 115
- Flag: no RPE logged on the Bench press top set (110 x 6); assumed it ended at RPE 9, so 7 at rep 4
- 2026-11-10 Accessories: incline DB press holds 70 total (6, 8, 8; range 8-12). Lateral raise holds 20 total (15, 20, 20, 20; one set short of 20). Overhead triceps extension back to 25 (27.5 x 8 x 3 against a planned 25; 8s since 20 Oct, under the 10-15 range). Row: dumbbell row 70 total x 8 x 4 replaced the barbell row, so the row track did not update (holds 70). Face pull not logged.
- 2026-11-10 Busy-gym rules (`templates/progression-tracks.md` §9, revised today), applied by hand to the 10 Nov U1: the dumbbell row (Bent Over Row (Dumbbell), 70 total x 8 x 4, unrated) now counts as the row exposure. Variant "DB row (two-arm)": all four sets at the top of 6-8, RPE assumed 8: +5 to 75 total. Row last exposure 10 Nov (H). The barbell row load stays 70; its regain phase and e1RM history are unchanged.
