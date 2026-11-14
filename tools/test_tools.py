#!/usr/bin/env python3
"""Offline tests for the Hevy integration and the progression-rule engine.

    python3 tools/test_tools.py

No network: the API client is not exercised beyond payload shapes. Rule and
rendering cases start from a frozen copy of the track state
(tools/fixtures/tracks.json, data/tracks.json as of 85b16d9), so a Hevy sync
that rewrites data/tracks.json does not change their expected numbers.
templates/rotation.json is read live. Only the consistency checks
(RotationFile, the committed-history replay) read the live data/tracks.json.
"""
import copy
import csv
import datetime as dt
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import build_dashboard as dash  # noqa: E402
import gitguard  # noqa: E402
import hevy_pull as pull  # noqa: E402
import hevy_push_routines as push  # noqa: E402
import localtime  # noqa: E402
import update_tracks as upd  # noqa: E402
import week  # noqa: E402
from hevy_api import HISTORY_COLUMNS, workout_rows  # noqa: E402


def load(path):
    with open(os.path.join(ROOT, path)) as f:
        return json.load(f)


ROTATION = load("templates/rotation.json")
TRACKS = load("tools/fixtures/tracks.json")  # frozen; tests depend on its loads and counters
LIVE_TRACKS = load("data/tracks.json")  # rewritten by every sync; consistency checks only
ALIASES = load("tools/lift_aliases.json")
EXMAP = {ex["name"]: {"hevy_title": ex["hevy"][0], "template_id": "T-" + ex["name"][:6].upper()}
         for s in ROTATION["sessions"].values() for ex in s["exercises"]}
TODAY = dt.date(2026, 10, 22)


def fresh_tracks(**over):
    t = copy.deepcopy(TRACKS)
    for lift, fields in over.items():
        t["tracks"][lift].update(fields)
    return t


LB = 0.45359237


def lbs(sets):
    """Payload sets -> loads in pounds (None stays None)."""
    return [None if s["weight_kg"] is None else round(s["weight_kg"] / LB, 3) for s in sets]


def normal(sets):
    return [s for s in sets if s["type"] == "normal"]


def history_csv(rows):
    """rows: (date, title, exercise, set_index, type, weight_lb, reps, rpe).
    Written as weight_kg rounded to 2 decimals, as hevy_pull stores the API's kg."""
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=HISTORY_COLUMNS)
    w.writeheader()
    for i, (date, title, ex, idx, typ, wt, reps, rpe) in enumerate(rows):
        w.writerow({"date": date, "workout_title": title, "exercise": ex, "set_index": idx, "set_type": typ,
                    "weight_kg": "" if wt in ("", None) else round(wt * LB, 2), "reps": reps, "rpe": rpe, "notes": "", "source": "hevy-api", "workout_id": f"w-{date}-{title}"})
    f = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False)
    f.write(buf.getvalue())
    f.close()
    return f.name


def run_update(tracks, rows, **kw):
    path = history_csv(rows)
    try:
        sessions = upd.load_sessions(path)
        log, flags = upd.process(tracks, sessions, ALIASES, ROTATION, **kw)
    finally:
        os.unlink(path)
    return log, flags


class RotationFile(unittest.TestCase):
    def test_cross_block_pairs_carry_the_main_lifts_of_both_halves(self):
        for pair in ("U1+L2", "U2+L3", "U3+L1"):
            session = ROTATION["sessions"][pair]
            self.assertTrue(session.get("merged"), pair)
            self.assertEqual(upd.parse_slot(session["title"]), pair)
            want = {}
            for half in pair.split("+"):
                for ex in ROTATION["sessions"][half]["exercises"]:
                    if ex["role"] in ("H", "V"):
                        want[ex["track"]] = ex["role"]
            got = {ex["track"]: ex["role"] for ex in session["exercises"] if ex["role"] in ("H", "V")}
            self.assertEqual(got, want, pair)

    def test_nine_sessions_and_all_tracks_have_one_h_and_one_v(self):
        self.assertEqual(set(ROTATION["sessions"]), {"L1", "U1", "L2", "U2", "L3", "U3", "Full A", "Full B", "Full C",
                                                     "U1+L2", "U2+L3", "U3+L1"})
        for lift, t in LIVE_TRACKS["tracks"].items():
            for slot_list, role in ((t["h_slots"], "H"), (t["v_slots"], "V")):
                for slot in slot_list:
                    roles = [ex["role"] for ex in ROTATION["sessions"][slot]["exercises"] if ex.get("track") == lift]
                    self.assertEqual(roles, [role], f"{lift} in {slot} should be exactly one {role}")

    def test_every_accessory_has_a_load_entry(self):
        for s in ROTATION["sessions"].values():
            for ex in s["exercises"]:
                if ex["role"] == "acc":
                    self.assertIn(ex["name"], LIVE_TRACKS["accessories"], ex["name"])

    def test_fixture_has_the_same_shape_as_the_live_tracks(self):
        # A structural change to data/tracks.json (new track, accessory, or field) needs the fixture refreshed.
        self.assertEqual(set(TRACKS["tracks"]), set(LIVE_TRACKS["tracks"]))
        self.assertEqual(set(TRACKS["accessories"]), set(LIVE_TRACKS["accessories"]))
        transient = {"work_up"}  # update_tracks.py drops it once the work-up has found a load
        for lift, t in LIVE_TRACKS["tracks"].items():
            self.assertEqual(set(TRACKS["tracks"][lift]) - transient, set(t) - transient, lift)


class RenderRoutines(unittest.TestCase):
    def test_l1_squat_heavy(self):
        payload, unresolved = push.build_routine("L1", ROTATION, TRACKS, EXMAP, TODAY)
        self.assertEqual(unresolved, [])
        squat = payload["exercises"][0]
        self.assertEqual(squat["exercise_template_id"], EXMAP["Back squat"]["template_id"])
        types = [s["type"] for s in squat["sets"]]
        self.assertEqual(types, ["warmup"] * 2 + ["normal"] * 4)
        self.assertEqual(lbs(normal(squat["sets"])), [135, 125, 125, 125])
        self.assertEqual([(w, s["reps"]) for w, s in zip(lbs(squat["sets"][:2]), squat["sets"][:2])], [(45, 5), (110, 2)])  # bar, 80%
        self.assertIn("RPE 8", squat["notes"])
        self.assertIn("Rate it: 7 easy, 8 on target, 9 hard", squat["notes"])
        self.assertIn("Change the reps if you did more or fewer", squat["notes"])
        self.assertIn("Regain phase (to e1RM 263 lb", squat["notes"])  # the fixture squat is in the regain phase
        self.assertIn("never more than +10 lb", squat["notes"])
        self.assertNotIn("REP-OUT", squat["notes"])
        # outside a phase, the normal increment note
        tr = fresh_tracks(squat={"regain": {"exit_e1rm_lb": 263, "until": "2027-01-09", "ended": "2026-10-20: test"}})
        payload, _ = push.build_routine("L1", ROTATION, tr, EXMAP, TODAY)
        self.assertIn("+5 lb next time", payload["exercises"][0]["notes"])
        # superset ids pass through
        self.assertEqual(payload["exercises"][3]["superset_id"], 1)
        self.assertEqual(payload["exercises"][4]["superset_id"], 1)

    def test_ramp_adds_60_percent_step_from_225_lb(self):
        self.assertEqual(len(push.warmup_sets("ramp", 220)), 2)
        heavy = push.warmup_sets("ramp", 225)
        self.assertEqual([(s["weight_lb"], s["reps"]) for s in heavy], [(45, 5), (135, 3), (180, 2)])
        self.assertEqual(push.warmup_sets("feeder", 150), [{"type": "warmup", "weight_lb": 100, "reps": 3}])  # 97.5 rounds up
        self.assertEqual(push.warmup_sets("feeder", 60)[0]["weight_lb"], 45)  # never below the bar

    def test_payload_weights_are_exact_pounds(self):
        title = {v["template_id"]: v["hevy_title"] for v in EXMAP.values()}
        for slot in ROTATION["sessions"]:
            payload, _ = push.build_routine(slot, ROTATION, TRACKS, EXMAP, TODAY)
            for ex in payload["exercises"]:
                for s in ex["sets"]:
                    if s["weight_kg"] is None:
                        continue
                    lb = s["weight_kg"] / LB
                    self.assertAlmostEqual(lb, round(lb * 2) / 2, places=9)  # whole or half pounds, full precision
                    if "(Barbell)" in title[ex["exercise_template_id"]]:
                        self.assertAlmostEqual(lb / 5, round(lb / 5), places=9, msg=f"{slot} {lb}")  # 2.5-lb plates

    def test_merged_full_a_has_two_backoffs_and_three_rows(self):
        payload, _ = push.build_routine("Full A", ROTATION, TRACKS, EXMAP, TODAY)
        squat, bench, row = payload["exercises"][:3]
        self.assertEqual(len(normal(squat["sets"])), 3)
        self.assertEqual(lbs(normal(bench["sets"])), [95, 90, 90])
        self.assertEqual(lbs([s for s in bench["sets"] if s["type"] == "warmup"]), [60])  # feeder at 65%
        self.assertIn("hold, not a miss", bench["notes"])
        self.assertIn("every second top set", bench["notes"])
        self.assertEqual(len(row["sets"]), 3)
        self.assertEqual(row["sets"][0]["rep_range"], {"start": 6, "end": 8})
        self.assertEqual(lbs(row["sets"][:1]), [70])
        self.assertNotIn("reps", row["sets"][0])

    def test_volume_sets_are_90_percent_and_warm_up_off_the_v_load(self):
        payload, _ = push.build_routine("U3", ROTATION, TRACKS, EXMAP, TODAY)
        bench, press, row, pull = payload["exercises"][:4]
        self.assertEqual(lbs(normal(bench["sets"])), [85] * 4)
        self.assertEqual([s["reps"] for s in normal(bench["sets"])], [6] * 4)
        self.assertEqual(lbs([s for s in bench["sets"] if s["type"] == "warmup"]), [45, 70])  # 80% of 85
        self.assertEqual(lbs(normal(press["sets"])), [55] * 3)
        self.assertEqual(lbs(row["sets"][:1]), [65])
        self.assertEqual(lbs(pull["sets"][:1]), [115])

    def test_work_up_renders_blank_loads(self):
        payload, _ = push.build_routine("L2", ROTATION, TRACKS, EXMAP, TODAY)
        dl = payload["exercises"][0]
        self.assertTrue(all(s["weight_kg"] is None for s in dl["sets"]))
        self.assertIn("95 x 4", dl["notes"])
        self.assertIn("rounded to the nearest 5 lb", dl["notes"])

    def test_every_exercise_has_a_timer_and_rest_note(self):
        for slot in ROTATION["sessions"]:
            for deload in (False, True):
                payload, _ = push.build_routine(slot, ROTATION, TRACKS, EXMAP, TODAY, deload=deload)
                self.assertRegex(payload["notes"], r"Target about \d+ min")
                self.assertRegex(payload["exercises"][0]["notes"], r"^Session: target about \d+ min")
                for ex in payload["exercises"]:
                    self.assertGreater(ex["rest_seconds"] or 0, 0, slot)
                    self.assertIn(push.mmss(ex["rest_seconds"]), ex["notes"], slot)

    def test_rest_notes_and_superset_timers(self):
        payload, _ = push.build_routine("L1", ROTATION, TRACKS, EXMAP, TODAY)
        squat, _, _, curl, calf, _ = payload["exercises"]
        self.assertIn("Rest 3:30 after the top set (timer + 0:30), 3:00 between back-offs.", squat["notes"])
        self.assertEqual((curl["rest_seconds"], calf["rest_seconds"]), (60, 120))
        self.assertIn("rest 1:00, then standing calf raise", curl["notes"])
        self.assertIn("rest 2:00 after the round", calf["notes"])

    def test_session_length_estimate(self):
        for slot, lo, hi in (("L1", 55, 65), ("U2", 55, 65), ("Full A", 62, 75), ("Full C", 62, 75)):
            payload, _ = push.build_routine(slot, ROTATION, TRACKS, EXMAP, TODAY)
            minutes = int(payload["notes"].split("Target about ")[1].split()[0])
            self.assertTrue(lo <= minutes <= hi, (slot, minutes))
        normal, _ = push.build_routine("U1", ROTATION, TRACKS, EXMAP, TODAY)
        deload, _ = push.build_routine("U1", ROTATION, TRACKS, EXMAP, TODAY, deload=True)
        self.assertLess(push.estimate_minutes(ROTATION["sessions"]["U1"]["exercises"], deload["exercises"])[0],
                        push.estimate_minutes(ROTATION["sessions"]["U1"]["exercises"], normal["exercises"])[0])

    def test_deload(self):
        payload, _ = push.build_routine("U1", ROTATION, TRACKS, EXMAP, TODAY, deload=True)
        bench, row = payload["exercises"][:2]
        self.assertEqual(lbs(normal(bench["sets"])), [85, 80])  # 95 x 0.91 = 86.45 -> 85; one back-off
        self.assertNotIn("step counter", bench["notes"])
        self.assertEqual(len(normal(row["sets"])), 2)
        self.assertTrue(payload["title"].endswith("(deload)"))
        acc = payload["exercises"][2]
        self.assertEqual(len(acc["sets"]), 2)

    def test_gap_modifiers(self):
        t = fresh_tracks(squat={"top_set_lb": 140, "last_h_load_lb": 135, "last_exposure": {"date": "2026-10-01", "type": "H"}})["tracks"]["squat"]
        # regain phase (section 5.1): 8-14 days takes the planned load; 15+ days as section 8
        self.assertEqual(push.gap_modifier(t, dt.date(2026, 10, 11))[:2], (140, 0))
        self.assertIn("regain phase", push.gap_modifier(t, dt.date(2026, 10, 11))[2])
        self.assertEqual(push.gap_modifier(t, dt.date(2026, 10, 19))[:2], (135, -1))
        t = dict(t, regain=None)
        self.assertEqual(push.gap_modifier(t, dt.date(2026, 10, 8)), (140, 0, None))         # 7 days: normal
        self.assertEqual(push.gap_modifier(t, dt.date(2026, 10, 11))[:2], (135, 0))          # 10 days: hold
        self.assertEqual(push.gap_modifier(t, dt.date(2026, 10, 19))[:2], (135, -1))         # 18 days: hold, one fewer back-off
        self.assertEqual(push.gap_modifier(t, dt.date(2026, 10, 26))[:2], (130, 0))          # 25 days: -5% (128.25)
        self.assertEqual(push.gap_modifier(t, dt.date(2026, 11, 5))[:2], (120, 0))           # 35 days: -10% (121.5)

    def test_rep_out_and_caution_notes_and_session_note(self):
        tr = fresh_tracks(deadlift={"rep_out_due": True, "top_set_lb": 150, "last_h_load_lb": 145,
                                    "last_exposure": {"date": "2026-10-20", "type": "H"}})
        payload, _ = push.build_routine("L2", ROTATION, tr, EXMAP, TODAY)
        dl = payload["exercises"][0]["notes"]
        self.assertIn("REP-OUT", dl)
        self.assertIn("back position", dl)
        self.assertIn("only with a logged RPE 7 or easier", dl)
        push.add_session_note(payload, "R+3 after the race: deadlift top set capped at RPE 7.")
        self.assertTrue(payload["notes"].startswith("R+3 after the race"))
        self.assertTrue(payload["exercises"][0]["notes"].startswith("R+3 after the race"))
        # row regain note
        payload, _ = push.build_routine("U1", ROTATION, TRACKS, EXMAP, TODAY)
        row = next(e for e in payload["exercises"] if "Regain phase: +10 lb" in e["notes"])
        self.assertIn("first set reaches 11", row["notes"])

    def test_gap_hold_changes_backoff_count_in_payload(self):
        tr = fresh_tracks(squat={"top_set_lb": 140, "last_h_load_lb": 135, "last_exposure": {"date": "2026-10-01", "type": "H"}})
        payload, _ = push.build_routine("L1", ROTATION, tr, EXMAP, dt.date(2026, 10, 19))
        squat = payload["exercises"][0]
        self.assertEqual(lbs(normal(squat["sets"])), [135, 125, 125])


class UpdateRules(unittest.TestCase):
    def test_slot_parsing(self):
        self.assertEqual(upd.parse_slot("L1 Lower A"), "L1")
        self.assertEqual(upd.parse_slot("full b"), "Full B")
        self.assertEqual(upd.parse_slot("FULL C (deload)"), "Full C")
        self.assertIsNone(upd.parse_slot("Evening workout"))
        self.assertIsNone(upd.parse_slot("L10 something"))

    def test_pair_titles_are_merged_sessions(self):
        self.assertEqual(upd.parse_slot("U3 + L1 (merged)"), "U3+L1")
        self.assertEqual(upd.parse_slot("Race Week 1 - Tue (U2 + L3)"), "U2+L3")
        self.assertEqual(upd.parse_slot("Full A (L1 + U1)"), "Full A")
        self.assertEqual(upd.parse_slot("L1+U1"), "Full A")
        self.assertEqual(upd.parse_slot("L1 + L2 test"), "L1")  # two lowers is not a merge; prefix wins
        self.assertTrue(upd.is_merged("U3+L1"))
        self.assertEqual(upd.advance_pointer("U3+L1", ROTATION), "U1")
        self.assertEqual(upd.advance_pointer("U2+L3", ROTATION), "U3")

    def test_pair_session_classifies_each_half(self):
        tr = fresh_tracks()
        run_update(tr, [
            ("2026-10-27", "Race Week 2 - Wed (U3 + L1)", "Squat (Barbell)", 0, "normal", 135, 4, 8),
            ("2026-10-27", "Race Week 2 - Wed (U3 + L1)", "Bench Press (Barbell)", 0, "normal", 90, 6, ""),
        ])
        self.assertEqual(tr["tracks"]["squat"]["last_exposure"], {"date": "2026-10-27", "type": "H"})
        self.assertEqual(tr["tracks"]["squat"]["top_set_lb"], 140)
        self.assertEqual(tr["tracks"]["bench"]["last_exposure"], {"date": "2026-10-27", "type": "V"})
        self.assertEqual(tr["pointer"], "U1")

    def test_logged_kg_reads_back_as_exact_pounds(self):
        self.assertEqual(upd.kg_to_lb(61.24), 135.0)
        self.assertEqual(upd.kg_to_lb(43.09), 95.0)
        self.assertEqual(upd.kg_to_lb(20.41), 45.0)
        self.assertIsNone(upd.kg_to_lb(None))

    def test_increment_on_rpe_8(self):
        tr = fresh_tracks()
        log, flags = run_update(tr, [
            ("2026-10-27", "L1 Lower A", "Squat (Barbell)", 0, "warmup", 45, 5, ""),
            ("2026-10-27", "L1 Lower A", "Squat (Barbell)", 2, "normal", 135, 4, 8),
            ("2026-10-27", "L1 Lower A", "Squat (Barbell)", 3, "normal", 125, 4, 7),
        ])
        sq = tr["tracks"]["squat"]
        self.assertEqual(sq["top_set_lb"], 140)
        self.assertEqual(sq["last_h_load_lb"], 135)
        self.assertEqual(sq["miss_counter"], 0)
        self.assertEqual(sq["last_exposure"], {"date": "2026-10-27", "type": "H"})
        self.assertEqual(sq["e1rm_history"][-1]["e1rm"], 162.0)  # 135 x (1 + 6/30)
        self.assertEqual(tr["pointer"], "U1")
        self.assertEqual(flags, [])

    def test_big_step_on_rpe_7_and_actual_load_is_the_base(self):
        tr = fresh_tracks()
        run_update(tr, [("2026-10-27", "L1", "Squat (Barbell)", 0, "normal", 145, 4, 7)])
        self.assertEqual(tr["tracks"]["squat"]["top_set_lb"], 155)

    def test_bench_adds_5_lb_every_second_success(self):
        tr = fresh_tracks()
        log, _ = run_update(tr, [("2026-10-27", "U1", "Bench Press (Barbell)", 0, "normal", 95, 4, 8)])
        b = tr["tracks"]["bench"]
        self.assertEqual((b["top_set_lb"], b["step_counter"], b["miss_counter"]), (95, 1, 0))
        self.assertIn("success 1 of 2", log[0])
        run_update(tr, [("2026-11-03", "U1", "Bench Press (Barbell)", 0, "normal", 95, 4, 7.5)])
        self.assertEqual((b["top_set_lb"], b["step_counter"]), (100, 0))
        # RPE 7 or lower: +5 lb at once, counter cleared
        tr = fresh_tracks(bench={"step_counter": 1})
        run_update(tr, [("2026-10-27", "U1", "Bench Press (Barbell)", 0, "normal", 95, 4, 7)])
        self.assertEqual((tr["tracks"]["bench"]["top_set_lb"], tr["tracks"]["bench"]["step_counter"]), (100, 0))
        # a hold keeps the count
        tr = fresh_tracks(bench={"step_counter": 1})
        run_update(tr, [("2026-10-27", "U1", "Bench Press (Barbell)", 0, "normal", 95, 4, 9)])
        self.assertEqual((tr["tracks"]["bench"]["top_set_lb"], tr["tracks"]["bench"]["step_counter"]), (95, 1))

    def test_hold_and_miss(self):
        tr = fresh_tracks()
        run_update(tr, [("2026-10-27", "U1", "Bench Press (Barbell)", 0, "normal", 95, 4, 9)])
        self.assertEqual(tr["tracks"]["bench"]["top_set_lb"], 95)
        self.assertEqual(tr["tracks"]["bench"]["miss_counter"], 0)
        tr = fresh_tracks()
        run_update(tr, [("2026-10-27", "U1", "Bench Press (Barbell)", 0, "normal", 95, 3, 10)])
        self.assertEqual(tr["tracks"]["bench"]["miss_counter"], 1)

    def test_merged_second_lift_at_rpe_9_5_is_a_hold_not_a_miss(self):
        tr = fresh_tracks()
        log, _ = run_update(tr, [
            ("2026-10-27", "Full A", "Squat (Barbell)", 0, "normal", 135, 4, 8),
            ("2026-10-27", "Full A", "Bench Press (Barbell)", 0, "normal", 95, 4, 9.5),
        ])
        self.assertEqual(tr["tracks"]["bench"]["miss_counter"], 0)
        self.assertEqual(tr["tracks"]["bench"]["top_set_lb"], 95)
        self.assertEqual(tr["pointer"], "L2")

    def test_stall_flagged_then_reset(self):
        tr = fresh_tracks(squat={"miss_counter": 1, "last_h_load_lb": 135, "top_set_lb": 135})
        log, _ = run_update(tr, [("2026-10-27", "L1", "Squat (Barbell)", 0, "normal", 135, 3, 10)])
        self.assertIn("STALL", log[0])
        self.assertEqual(tr["tracks"]["squat"]["top_set_lb"], 135)  # held without --reset-on-stall
        tr = fresh_tracks(squat={"miss_counter": 1, "last_h_load_lb": 135, "top_set_lb": 135})
        run_update(tr, [("2026-10-27", "L1", "Squat (Barbell)", 0, "normal", 135, 3, 10)], reset_on_stall=True)
        self.assertEqual(tr["tracks"]["squat"]["top_set_lb"], 120)  # floor(135 x 0.925 = 124.9) to 5 lb
        self.assertEqual(tr["tracks"]["squat"]["stalls"], 1)
        self.assertEqual(tr["tracks"]["squat"]["miss_counter"], 0)

    def test_double_progression_row(self):
        tr = fresh_tracks()
        run_update(tr, [("2026-10-27", "U1", "Bent Over Row (Barbell)", i, "normal", 70, 8, 8) for i in range(4)])
        self.assertEqual(tr["tracks"]["row"]["top_set_lb"], 75)
        tr = fresh_tracks()
        run_update(tr, [("2026-10-27", "U1", "Bent Over Row (Barbell)", i, "normal", 70, r, 8) for i, r in enumerate([8, 7, 6, 6])])
        self.assertEqual(tr["tracks"]["row"]["top_set_lb"], 70)
        self.assertEqual(tr["tracks"]["row"]["miss_counter"], 0)
        tr = fresh_tracks()
        run_update(tr, [("2026-10-27", "U1", "Bent Over Row (Barbell)", i, "normal", 70, r, 9) for i, r in enumerate([5, 5, 4])])
        self.assertEqual(tr["tracks"]["row"]["miss_counter"], 1)

    def test_work_up_sets_the_deadlift_track(self):
        tr = fresh_tracks()
        run_update(tr, [
            ("2026-10-29", "L2", "Deadlift (Barbell)", 0, "normal", 115, 4, 6),
            ("2026-10-29", "L2", "Deadlift (Barbell)", 1, "normal", 135, 4, 7),
            ("2026-10-29", "L2", "Deadlift (Barbell)", 2, "normal", 145, 4, 8),
            ("2026-10-29", "L2", "Deadlift (Barbell)", 3, "normal", 135, 4, 7.5),
        ])
        dl = tr["tracks"]["deadlift"]
        self.assertEqual(dl["top_set_lb"], 150)
        self.assertNotIn("work_up", dl)

    def test_volume_and_untitled_sessions_only_touch_the_clock(self):
        tr = fresh_tracks()
        log, _ = run_update(tr, [
            ("2026-10-31", "L3", "Squat (Barbell)", 0, "normal", 120, 6, 7),
            ("2026-11-02", "Evening workout", "Bench Press (Barbell)", 0, "normal", 110, 5, 9),
        ])
        self.assertEqual(log, [])
        self.assertEqual(tr["tracks"]["squat"]["top_set_lb"], 135)
        self.assertEqual(tr["tracks"]["squat"]["last_exposure"], {"date": "2026-10-31", "type": "V"})
        self.assertEqual(tr["tracks"]["bench"]["last_exposure"], {"date": "2026-11-02", "type": "other"})
        self.assertEqual(tr["pointer"], "U3")

    def test_no_rpe_is_flagged_and_treated_as_8(self):
        tr = fresh_tracks()
        _, flags = run_update(tr, [("2026-10-27", "L1", "Squat (Barbell)", 0, "normal", 135, 4, "")])
        self.assertEqual(tr["tracks"]["squat"]["top_set_lb"], 140)
        self.assertTrue(flags and "no RPE" in flags[0])

    def test_processed_through_prevents_double_counting(self):
        tr = fresh_tracks()
        rows = [("2026-10-27", "L1", "Squat (Barbell)", 0, "normal", 135, 4, 8)]
        run_update(tr, rows)
        run_update(tr, rows)
        self.assertEqual(tr["tracks"]["squat"]["top_set_lb"], 140)
        self.assertEqual(len(tr["tracks"]["squat"]["e1rm_history"]), 2)  # seed + one

    def test_committed_history_does_not_move_any_track(self):
        # Live invariant: a sync processes every session in history.csv, so replaying it moves nothing.
        tr = copy.deepcopy(LIVE_TRACKS)
        sessions = upd.load_sessions(os.path.join(ROOT, "data", "history.csv"))
        log, _ = upd.process(tr, sessions, ALIASES, ROTATION)
        self.assertEqual(log, [])
        for lift in LIVE_TRACKS["tracks"]:
            self.assertEqual(tr["tracks"][lift]["top_set_lb"], LIVE_TRACKS["tracks"][lift]["top_set_lb"])

    def test_md_table_renders(self):
        table = upd.md_table(TRACKS)
        self.assertIn("Next H load (lb)", table)
        self.assertIn("| Back squat | **135** | 125 | 120 |", table)
        self.assertIn("| Bench press | **95** | 90 | 85 |", table)
        self.assertIn("work up", table)


class BusyGym(unittest.TestCase):
    """guide/03 section 4.3 "Station taken"; progression-tracks.md section 9."""

    def test_row_variant_counts_with_its_own_load(self):
        tr = fresh_tracks()
        log, _ = run_update(tr, [("2026-11-10", "U1", "Bent Over Row (Dumbbell)", i, "normal", 70, 8, None) for i in range(4)])
        row = tr["tracks"]["row"]
        self.assertEqual(row["variants"]["DB row (two-arm)"]["top_set_lb"], 75)
        self.assertEqual(row["top_set_lb"], TRACKS["tracks"]["row"]["top_set_lb"])  # barbell load untouched
        self.assertEqual(row["last_exposure"], {"date": "2026-11-10", "type": "H"})
        self.assertEqual(len(row["e1rm_history"]), len(TRACKS["tracks"]["row"]["e1rm_history"]))
        self.assertTrue(any("DB row (two-arm)" in line for line in log))

    def test_one_arm_and_chest_supported_rows_are_separate_variants(self):
        tr = fresh_tracks()
        run_update(tr, [("2026-11-10", "U1", "Chest Supported Incline Row (Dumbbell)", i, "normal", 60, 7, 8) for i in range(4)])
        vs = tr["tracks"]["row"]["variants"]
        self.assertEqual(vs["Chest-supported row"]["top_set_lb"], 60)
        self.assertIsNone(vs["DB row (two-arm)"]["top_set_lb"])
        tr = fresh_tracks()
        run_update(tr, [("2026-11-10", "U1", "Dumbbell Row", i, "normal", 40, 8, 8) for i in range(4)])
        self.assertEqual(tr["tracks"]["row"]["variants"]["One-arm DB row"]["top_set_lb"], 45)

    def test_barbell_row_wins_over_a_variant_in_the_same_session(self):
        tr = fresh_tracks()
        run_update(tr, [("2026-11-10", "U1", "Bent Over Row (Barbell)", i, "normal", 70, 8, 8) for i in range(4)]
                   + [("2026-11-10", "U1", "Bent Over Row (Dumbbell)", 4 + i, "normal", 60, 8, 8) for i in range(2)])
        self.assertEqual(tr["tracks"]["row"]["top_set_lb"], 75)
        self.assertIsNone(tr["tracks"]["row"]["variants"]["DB row (two-arm)"]["top_set_lb"])

    def test_squat_substitute_moves_the_top_set_to_the_volume_slot(self):
        tr = fresh_tracks(squat={"top_set_lb": 155, "last_h_load_lb": 155, "regain": None})
        log, _ = run_update(tr, [("2026-11-12", "L1", "Leg Press (Machine)", i, "normal", 270, 10, 8) for i in range(4)])
        sq = tr["tracks"]["squat"]
        self.assertEqual(sq["top_set_lb"], 155)
        self.assertEqual(sq["h_owed"]["slot"], "L1")
        self.assertEqual(sq["last_sub_exposure"]["date"], "2026-11-12")
        self.assertIn("moves to the next", log[0])
        # L3: the V slot is run as the heavy exposure (top set at the planned load)
        log, _ = run_update(tr, [("2026-11-14", "L3", "Squat (Barbell)", 0, "normal", 155, 4, 8),
                                 ("2026-11-14", "L3", "Squat (Barbell)", 1, "normal", 145, 4, 7.5)])
        self.assertNotIn("h_owed", sq)
        self.assertEqual(sq["last_exposure"], {"date": "2026-11-14", "type": "H"})
        self.assertEqual(sq["top_set_lb"], 160)
        self.assertEqual(sq["e1rm_history"][-1]["slot"], "L3")

    def test_promoted_top_set_at_9_5_is_a_hold_not_a_miss(self):
        tr = fresh_tracks(squat={"top_set_lb": 155, "last_h_load_lb": 155, "regain": None,
                                 "h_owed": {"from": "2026-11-12", "slot": "L1"}})
        run_update(tr, [("2026-11-14", "L3", "Squat (Barbell)", 0, "normal", 155, 4, 9.5)])
        self.assertEqual(tr["tracks"]["squat"]["miss_counter"], 0)

    def test_volume_sets_do_not_count_as_the_moved_top_set(self):
        tr = fresh_tracks(squat={"top_set_lb": 155, "last_h_load_lb": 155, "h_owed": {"from": "2026-11-12", "slot": "L1"}})
        run_update(tr, [("2026-11-14", "L3", "Squat (Barbell)", i, "normal", 140, 6, None) for i in range(4)])
        sq = tr["tracks"]["squat"]
        self.assertEqual(sq["top_set_lb"], 155)
        self.assertEqual(sq["last_exposure"]["type"], "V")
        self.assertIn("h_owed", sq)  # the next heavy slot clears it

    def test_incline_db_press_is_not_a_bench_substitute(self):
        tr = fresh_tracks()
        run_update(tr, [("2026-11-10", "U1", "Incline Bench Press (Dumbbell)", 0, "normal", 70, 8, 8)])
        self.assertNotIn("last_sub_exposure", tr["tracks"]["bench"])
        self.assertIn("h_owed", tr["tracks"]["bench"])  # bench missing from its heavy slot

    def test_substitute_caps_the_gap_modifier_at_a_hold(self):
        base = {"top_set_lb": 140, "last_h_load_lb": 135, "regain": None, "last_exposure": {"date": "2026-10-01", "type": "H"}}
        t = fresh_tracks(squat=dict(base, last_sub_exposure={"date": "2026-10-20", "type": "H"}))["tracks"]["squat"]
        self.assertEqual(push.gap_modifier(t, dt.date(2026, 10, 26))[:2], (135, 0))   # 25 d barbell, 6 d sub: hold
        self.assertEqual(push.gap_modifier(t, dt.date(2026, 11, 5))[:2], (135, -1))   # 16 d since the sub
        self.assertEqual(push.gap_modifier(t, dt.date(2026, 10, 8)), (140, 0, None))  # 7 d: normal either way

    def test_routine_renders_the_moved_top_set_and_station_notes(self):
        tr = fresh_tracks(squat={"top_set_lb": 155, "last_h_load_lb": 155, "h_owed": {"from": "2026-11-12", "slot": "L1"},
                                 "last_exposure": {"date": "2026-11-12", "type": "V"}})
        tr["tracks"]["row"]["variants"]["DB row (two-arm)"]["top_set_lb"] = 75
        payload, _ = push.build_routine("L3", ROTATION, tr, EXMAP, dt.date(2026, 11, 14))
        squat = payload["exercises"][0]
        self.assertIn("TOP SET MOVED HERE", squat["notes"])
        self.assertEqual(lbs(normal(squat["sets"]))[-3:], [155, 145, 145])
        self.assertIn("Smith machine squat", squat["notes"])
        payload, _ = push.build_routine("U1", ROTATION, tr, EXMAP, dt.date(2026, 11, 14))
        row = payload["exercises"][1]
        self.assertIn("DB row (two-arm) 75 lb", row["notes"])
        payload, _ = push.build_routine("U3", ROTATION, tr, EXMAP, dt.date(2026, 11, 14))
        row = next(e for e in payload["exercises"] if "DB row (two-arm)" in e["notes"])
        self.assertIn("DB row (two-arm) 70 lb", row["notes"])  # V: 90% of 75, nearest 5


class EffortAndRegainRules(unittest.TestCase):
    """progression-tracks.md section 5 (effective RPE, unrated rule, re-anchor) and 5.1-5.3."""

    def test_reps_above_target_are_credited(self):
        # 6 @ 8 reads 6 at rep 4: the big step (the 27 Oct bench hand amendment), counter cleared
        tr = fresh_tracks(bench={"step_counter": 1})
        log, flags = run_update(tr, [("2026-10-27", "U1", "Bench Press (Barbell)", 0, "normal", 105, 6, 8)])
        self.assertEqual((tr["tracks"]["bench"]["top_set_lb"], tr["tracks"]["bench"]["step_counter"]), (110, 0))
        self.assertIn("reads 6", log[0])
        self.assertEqual(flags, [])

    def test_five_at_rpe_10_is_a_hold_not_a_miss(self):
        tr = fresh_tracks()
        run_update(tr, [("2026-10-27", "L2", "Deadlift (Barbell)", 0, "normal", 145, 5, 10)])
        dl = tr["tracks"]["deadlift"]
        self.assertEqual((dl["top_set_lb"], dl["miss_counter"]), (145, 0))

    def test_unrated_reps_above_target(self):
        cases = [(4, 140), (5, 140), (6, 145), (7, 145)]  # squat at 135: unrated 4 and 5 step, 6 and 7 big step
        for reps, expected in cases:
            tr = fresh_tracks()
            _, flags = run_update(tr, [("2026-10-27", "L1", "Squat (Barbell)", 0, "normal", 135, reps, "")])
            self.assertEqual(tr["tracks"]["squat"]["top_set_lb"], expected, reps)
            self.assertTrue(flags and "no RPE" in flags[0], reps)

    def test_unrated_e1rm_assumes_rir_1_above_the_target(self):
        tr = fresh_tracks()
        run_update(tr, [("2026-10-27", "L1", "Squat (Barbell)", 0, "normal", 150, 6, "")])
        self.assertEqual(tr["tracks"]["squat"]["e1rm_history"][-1]["e1rm"], 185.0)  # 150 x (1 + 7/30)

    def test_re_anchor_caps(self):
        # 155 x 8 @ 8 reads 4: e1RM 206.7 / 1.2 = 172 -> 170; +10% cap 170. Regain cap on the squat: +10
        tr = fresh_tracks(squat={"regain": {"exit_e1rm_lb": 999, "until": "2027-01-09"}})
        log, _ = run_update(tr, [("2026-10-27", "L1", "Squat (Barbell)", 0, "normal", 155, 8, 8)])
        self.assertEqual(tr["tracks"]["squat"]["top_set_lb"], 170)
        self.assertIn("re-anchor", log[0])
        tr = fresh_tracks()
        log, _ = run_update(tr, [("2026-10-27", "L1", "Squat (Barbell)", 0, "normal", 155, 8, 8)])
        self.assertEqual(tr["tracks"]["squat"]["top_set_lb"], 165)
        self.assertIn("capped at +10", log[0])

    def test_regain_phase_bench_steps_every_success_and_exits(self):
        regain = {"exit_e1rm_lb": 130, "until": "2027-01-09"}
        tr = fresh_tracks(bench={"regain": dict(regain)})
        run_update(tr, [("2026-10-27", "U1", "Bench Press (Barbell)", 0, "normal", 95, 4, 8)])
        b = tr["tracks"]["bench"]
        self.assertEqual((b["top_set_lb"], b["step_counter"]), (100, 0))
        self.assertNotIn("ended", b["regain"])
        # 105 x 6 @ 8: e1RM 133 >= 130, phase ends; the next success waits for the counter again
        run_update(tr, [("2026-11-03", "U1", "Bench Press (Barbell)", 0, "normal", 105, 6, 8)])
        self.assertIn("ended", b["regain"])
        run_update(tr, [("2026-11-10", "U1", "Bench Press (Barbell)", 0, "normal", 110, 4, 8)])
        self.assertEqual((b["top_set_lb"], b["step_counter"]), (110, 1))

    def test_regain_phase_ends_on_a_hard_top_set_or_the_date(self):
        tr = fresh_tracks()
        log, _ = run_update(tr, [("2026-10-27", "L1", "Squat (Barbell)", 0, "normal", 135, 4, 9)])
        self.assertIn("Regain phase ends", log[0])
        self.assertTrue(tr["tracks"]["squat"]["regain"]["ended"].startswith("2026-10-27"))
        # after the until date the cap no longer applies: 155 x 8 @ 8 re-anchors to 170
        tr = fresh_tracks()
        run_update(tr, [("2027-01-11", "L1", "Squat (Barbell)", 0, "normal", 155, 8, 8)])
        self.assertEqual(tr["tracks"]["squat"]["top_set_lb"], 170)

    def test_regain_row_jumps_10(self):
        tr = fresh_tracks()
        log, _ = run_update(tr, [("2026-10-27", "U1", "Bent Over Row (Barbell)", i, "normal", 70, r, "") for i, r in enumerate([11, 9, 8, 8])])
        self.assertEqual(tr["tracks"]["row"]["top_set_lb"], 80)
        tr = fresh_tracks()
        run_update(tr, [("2026-10-27", "U1", "Bent Over Row (Barbell)", i, "normal", 70, 8, 7) for i in range(4)])
        self.assertEqual(tr["tracks"]["row"]["top_set_lb"], 80)
        tr = fresh_tracks()  # all at 8 but RPE 8: the normal +5
        run_update(tr, [("2026-10-27", "U1", "Bent Over Row (Barbell)", i, "normal", 70, 8, 8) for i in range(4)])
        self.assertEqual(tr["tracks"]["row"]["top_set_lb"], 75)

    def test_deadlift_caution(self):
        # unrated 6 would be a big step; caution needs a logged RPE: +5
        tr = fresh_tracks()
        log, _ = run_update(tr, [("2026-10-29", "L2", "Deadlift (Barbell)", 0, "normal", 145, 6, "")])
        self.assertEqual(tr["tracks"]["deadlift"]["top_set_lb"], 150)
        self.assertIn("caution (no logged RPE)", log[0])
        # rated 4 @ 7: +10, then not twice in a row
        tr = fresh_tracks()
        run_update(tr, [("2026-10-29", "L2", "Deadlift (Barbell)", 0, "normal", 145, 4, 7)])
        self.assertEqual(tr["tracks"]["deadlift"]["top_set_lb"], 155)
        log, _ = run_update(tr, [("2026-11-05", "L2", "Deadlift (Barbell)", 0, "normal", 155, 4, 7)])
        self.assertEqual(tr["tracks"]["deadlift"]["top_set_lb"], 160)
        self.assertIn("big step last time", log[0])

    def test_two_unrated_fours_set_a_rep_out_and_the_rep_out_is_read(self):
        tr = fresh_tracks()
        run_update(tr, [("2026-10-27", "U2", "Overhead Press (Barbell)", 0, "normal", 60, 4, "")])
        self.assertFalse(tr["tracks"]["press"]["rep_out_due"])
        _, flags = run_update(tr, [("2026-11-03", "U2", "Overhead Press (Barbell)", 0, "normal", 65, 4, "")])
        self.assertTrue(tr["tracks"]["press"]["rep_out_due"])
        self.assertTrue(any("rep-out" in f for f in flags))
        # top 65 x 4 unrated, last back-off 60 x 9: reads RPE 7, the big step (+5 for the press), streak cleared
        log, _ = run_update(tr, [
            ("2026-11-10", "U2", "Overhead Press (Barbell)", 0, "normal", 65, 4, ""),
            ("2026-11-10", "U2", "Overhead Press (Barbell)", 1, "normal", 60, 4, ""),
            ("2026-11-10", "U2", "Overhead Press (Barbell)", 2, "normal", 60, 9, ""),
        ])
        p = tr["tracks"]["press"]
        self.assertEqual((p["top_set_lb"], p["rep_out_due"], p["unrated_streak"]), (70, False, 0))
        self.assertIn("rep-out 9", log[0])

    def test_rep_out_of_four_when_due_is_not_done(self):
        tr = fresh_tracks(press={"unrated_streak": 2, "rep_out_due": True})
        _, flags = run_update(tr, [
            ("2026-11-10", "U2", "Overhead Press (Barbell)", 0, "normal", 65, 4, ""),
            ("2026-11-10", "U2", "Overhead Press (Barbell)", 1, "normal", 60, 4, ""),
        ])
        self.assertTrue(tr["tracks"]["press"]["rep_out_due"])
        self.assertTrue(any("read as not done" in f for f in flags))

    def test_live_phases_match_the_rules_file(self):
        t = LIVE_TRACKS["tracks"]
        self.assertEqual(t["squat"]["regain"]["exit_e1rm_lb"], 263)
        self.assertEqual(t["row"]["regain"]["exit_e1rm_lb"], 128)
        self.assertTrue(t["deadlift"]["caution"]["big_step_needs_rating"])
        for lift in ("bench", "press", "deadlift", "pullup"):
            self.assertNotIn("regain", t[lift], lift)


class SlotArgs(unittest.TestCase):
    def test_normalize_slots(self):
        self.assertEqual(push.normalize_slots(["L1", "Full", "C", "fullA", "full b"], ROTATION), ["L1", "Full C", "Full A", "Full B"])


class ApiShapes(unittest.TestCase):
    def test_workout_rows_flatten(self):
        w = {"id": "abc", "title": "L1 Lower A", "start_time": "2026-10-27T17:00:00Z",
             "exercises": [{"title": "Squat (Barbell)", "notes": "felt, good\nok",
                            "sets": [{"index": 0, "type": "warmup", "weight_kg": 20, "reps": 10, "rpe": None},
                                     {"index": 1, "type": "normal", "weight_kg": 60, "reps": 4, "rpe": 8}]}]}
        rows = list(workout_rows(w))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[1]["rpe"], 8)
        self.assertEqual(rows[0]["rpe"], "")
        self.assertEqual(rows[0]["notes"], "felt; good ok")
        self.assertEqual(rows[0]["workout_id"], "abc")
        self.assertEqual(rows[0]["date"], "2026-10-27")


class LocalDates(unittest.TestCase):
    """The lifter's calendar day, not the UTC day (tools/localtime.py)."""

    def workout(self, start, wid="abc", title="L2 Lower B"):
        return {"id": wid, "title": title, "start_time": start,
                "exercises": [{"title": "Deadlift (Barbell)", "notes": "",
                               "sets": [{"index": 0, "type": "normal", "weight_kg": 72.57, "reps": 5, "rpe": 8}]}]}

    def test_evening_workout_keeps_its_local_day(self):
        # 7:22 pm Eastern on Thu 12 Nov is 00:22 UTC on Fri 13 Nov
        row = next(workout_rows(self.workout("2026-11-13T00:22:14+00:00")))
        self.assertEqual(row["date"], "2026-11-12")
        self.assertEqual(row["start_time"], "2026-11-13T00:22:14+00:00")

    def test_local_date_edges(self):
        self.assertEqual(localtime.local_date("2026-11-12T23:30:00Z"), "2026-11-12")   # 6:30 pm EST
        self.assertEqual(localtime.local_date("2026-07-17T00:18:00Z"), "2026-07-16")   # 8:18 pm EDT
        self.assertEqual(localtime.local_date("2026-07-17T04:30:00Z"), "2026-07-17")   # 12:30 am EDT
        self.assertEqual(localtime.local_date("2026-11-12"), "2026-11-12")
        self.assertEqual(localtime.local_date(""), "")

    def test_local_today_after_utc_midnight(self):
        now = dt.datetime(2026, 11, 13, 0, 19, tzinfo=dt.timezone.utc)
        self.assertEqual(localtime.local_today(now), dt.date(2026, 11, 12))

    def test_redate_changes_only_date_and_start_time(self):
        rows = [{"date": "2024-07-17", "workout_id": "a", "rpe": "8", "reps": "5"},
                {"date": "2026-11-10", "workout_id": "b", "rpe": "", "reps": "4"},
                {"date": "2024-01-01", "workout_id": "", "rpe": "", "reps": "3"}]
        moved = pull.redate(rows, {"a": "2024-07-17T00:18:00+00:00", "b": "2026-11-10T12:41:00+00:00"})
        self.assertEqual(moved, {"a": ("2024-07-17", "2024-07-16")})
        self.assertEqual([r["date"] for r in rows], ["2024-07-16", "2026-11-10", "2024-01-01"])
        self.assertEqual(rows[0]["rpe"], "8")
        self.assertNotIn("start_time", rows[2])

    def test_second_session_on_a_processed_date_is_not_skipped(self):
        first = [("2026-10-27", "L1 Lower A", "Squat (Barbell)", 0, "normal", 145, 4, 8)]
        tracks = fresh_tracks()
        path = history_csv(first)
        upd.process(tracks, upd.load_sessions(path), ALIASES, ROTATION)
        os.unlink(path)
        self.assertEqual(tracks["processed_through"], "2026-10-27")
        self.assertEqual(tracks["processed_ids"], ["w-2026-10-27-L1 Lower A"])
        both = first + [("2026-10-27", "U1 Upper A", "Bench Press (Barbell)", 0, "normal", 105, 4, 8)]
        path = history_csv(both)
        log, _ = upd.process(tracks, upd.load_sessions(path), ALIASES, ROTATION)
        os.unlink(path)
        self.assertEqual(len([line for line in log if "Bench" in line]), 1, log)
        self.assertFalse([line for line in log if "Squat" in line], log)
        self.assertEqual(tracks["pointer"], "L2")
        # a third run changes nothing
        path = history_csv(both)
        log, _ = upd.process(tracks, upd.load_sessions(path), ALIASES, ROTATION)
        os.unlink(path)
        self.assertEqual(log, [])


class FakeHevy:
    """Stands in for the API: routines by id, counts the writes."""

    def __init__(self, routines=None):
        self.routines = routines or {}
        self.puts = []

    def routine(self, rid):
        return {"routine": copy.deepcopy(self.routines[rid])}

    def update_routine(self, rid, title, exercises, folder_id=None, notes=None):
        self.puts.append(rid)
        self.routines[rid] = {"title": title, "exercises": copy.deepcopy(exercises)}
        return self.routines[rid]


def a_week(**over):
    w = {"week_of": "2026-11-09", "status": "confirmed", "deload": False, "sessions": [
        {"date": "2026-11-10", "slot": "U1", "state": "done", "routine_id": "r1"},
        {"date": "2026-11-12", "slot": "L2", "state": "planned", "routine_id": "r2"},
        {"date": "2026-11-14", "slot": "U2", "state": "planned", "routine_id": "r3"}]}
    w.update(over)
    return w


class PushChecks(unittest.TestCase):
    def test_tonights_session_is_pushed_and_skips_carry_a_reason(self):
        # 7:19 pm Eastern on the 12th: the UTC date is already the 13th
        today = localtime.local_today(dt.datetime(2026, 11, 13, 0, 19, tzinfo=dt.timezone.utc))
        week = a_week()
        week["sessions"].append({"date": "2026-11-15", "slot": "ZZ", "state": "planned"})
        todo, skipped = push.week_plan(week, ROTATION, today)
        self.assertEqual([s["date"] for s, _ in todo], ["2026-11-12", "2026-11-14"])
        why = {s["date"]: reason for s, reason in skipped}
        self.assertEqual(why["2026-11-10"], "done")
        self.assertIn("not in the rotation", why["2026-11-15"])
        todo, skipped = push.week_plan(week, ROTATION, dt.date(2026, 11, 13))
        self.assertEqual([s["date"] for s, _ in todo], ["2026-11-14"])
        self.assertIn("before today", {s["date"]: r for s, r in skipped}["2026-11-12"])

    def test_verify_routine(self):
        payload, _ = push.build_routine("L2", ROTATION, fresh_tracks(), EXMAP, TODAY)
        live = copy.deepcopy({"title": payload["title"], "exercises": payload["exercises"]})
        self.assertEqual(push.verify_routine(payload["title"], payload["exercises"], live), [])
        live["exercises"][1]["notes"] += " edited in the app"
        self.assertEqual(len(push.verify_routine(payload["title"], payload["exercises"], live)), 1)
        self.assertEqual(push.verify_routine(payload["title"], payload["exercises"], live, notes=False), [])
        live["exercises"][0]["sets"][-1]["weight_kg"] = 999.0
        live["title"] = "L2 Lower B (Fri 13 Nov)"
        diffs = push.verify_routine(payload["title"], payload["exercises"], live, notes=False)
        self.assertEqual(len(diffs), 2, diffs)
        live["exercises"].pop()
        self.assertTrue(any("exercises, sent" in d for d in push.verify_routine(payload["title"], payload["exercises"], live)))

    def test_only_what_differs_is_written(self):
        payload, _ = push.build_routine("L2", ROTATION, fresh_tracks(), EXMAP, TODAY)
        h = FakeHevy({"x": {"title": payload["title"], "exercises": copy.deepcopy(payload["exercises"])}})
        self.assertEqual(push.sync_routine(h, "x", payload["title"], payload, 1), (True, "in step"))
        self.assertEqual(h.puts, [])
        h.routines["x"]["title"] = "renamed in the app"
        ok, msg = push.sync_routine(h, "x", payload["title"], payload, 1, mode="check")
        self.assertFalse(ok)
        self.assertIn("DIFFERS", msg)
        self.assertEqual(h.puts, [])                       # check never writes
        self.assertEqual(push.sync_routine(h, "x", payload["title"], payload, 1), (True, "updated and read back"))
        self.assertEqual(h.puts, ["x"])
        push.sync_routine(h, "x", payload["title"], payload, 1, mode="all")
        self.assertEqual(h.puts, ["x", "x"])

    def test_week_push_uses_the_week_file(self):
        week = a_week(deload=True)
        h = FakeHevy({"r2": {"title": "old", "exercises": []}, "r3": {"title": "old", "exercises": []}})
        state = {"this_week": {"folder_id": 9, "routine_ids": ["r1", "r2", "r3"]}}
        results, changed = push.push_this_week(h, state, week, ROTATION, fresh_tracks(), EXMAP, dt.date(2026, 11, 12))
        self.assertFalse(changed)
        self.assertEqual(sorted(h.puts), ["r2", "r3"])
        self.assertEqual(h.routines["r3"]["title"], "U2 Upper B (deload) (Sat 14 Nov)")   # the week's deload flag reaches the routine
        self.assertEqual(upd.parse_slot(h.routines["r3"]["title"]), "U2")
        self.assertIn("DELOAD", h.routines["r3"]["exercises"][0]["notes"])
        self.assertEqual([r[2] for r in results if r[1] is None], ["skipped: done"])


class WeekFile(unittest.TestCase):
    def test_every_dated_title_reads_back_as_its_slot(self):
        for slot in ROTATION["sessions"]:
            title = week.title_for({"date": "2026-11-14", "slot": slot}, ROTATION)
            self.assertIn("(Sat 14 Nov)", title)
            self.assertEqual(upd.parse_slot(title), slot, title)

    def test_order_check_catches_skipping_ahead(self):
        tracks = fresh_tracks()
        tracks["pointer"] = "U2"
        w = a_week()
        w["sessions"] = [{"date": "2026-11-14", "slot": "L3", "state": "planned"},
                         {"date": "2026-11-15", "slot": "U3", "state": "planned"}]
        found = week.problems(w, tracks, ROTATION, dt.date(2026, 11, 13))
        self.assertTrue(any("U2 is owed before L3" in p for p in found), found)
        w["sessions"] = [{"date": "2026-11-14", "slot": "U2", "state": "planned"},
                         {"date": "2026-11-15", "slot": "Full C", "state": "planned"}]
        self.assertEqual(week.problems(w, tracks, ROTATION, dt.date(2026, 11, 13)), [])

    def test_spacing_and_unlogged_checks(self):
        tracks = fresh_tracks()
        tracks["pointer"] = "L3"
        w = a_week()
        w["sessions"] = [{"date": "2026-11-10", "slot": "L3", "state": "planned"},      # squat V, deadlift V
                         {"date": "2026-11-11", "slot": "U3", "state": "planned"},
                         {"date": "2026-11-12", "slot": "L1", "state": "planned"}]      # squat H two days later: fine
        self.assertEqual(week.problems(w, tracks, ROTATION, dt.date(2026, 11, 10)), [])
        w["sessions"][2]["date"] = "2026-11-11"
        w["sessions"][1]["date"] = "2026-11-12"
        w["sessions"].sort(key=lambda s: s["date"])
        found = week.problems(w, tracks, ROTATION, dt.date(2026, 11, 10))
        self.assertTrue(any(p.startswith("spacing: Back squat") for p in found), found)
        found = week.problems(a_week(), fresh_tracks(), ROTATION, dt.date(2026, 11, 13))
        self.assertTrue(any("no workout logged" in p and "Thu 12 Nov" in p for p in found), found)

    def logged(self, *items):
        return [((d, t, f"w-{d}-{t}"), []) for d, t in items]

    def test_reconcile(self):
        w = a_week()
        w["sessions"][1].update(slot="Full B")
        notes = week.reconcile(w, self.logged(("2026-11-12", "L2 Lower B (Fri 13 Nov)")), ROTATION, dt.date(2026, 11, 13))
        s = w["sessions"][1]
        self.assertEqual((s["slot"], s["planned_slot"], s["state"]), ("L2", "Full B", "done"))
        self.assertTrue(any("planned Full B, logged L2" in n for n in notes), notes)
        # a second run adds nothing
        before = copy.deepcopy(w)
        self.assertEqual(week.reconcile(w, self.logged(("2026-11-12", "L2 Lower B (Fri 13 Nov)")), ROTATION, dt.date(2026, 11, 13)), [])
        self.assertEqual(w, before)

    def test_reconcile_unplanned_and_untitled(self):
        w = a_week()
        notes = week.reconcile(w, self.logged(("2026-11-11", "L1 Lower A"), ("2026-11-13", "Evening workout"), ("2026-11-20", "L3 Lower C")),
                               ROTATION, dt.date(2026, 11, 14))
        self.assertEqual(len(w["sessions"]), 4)                     # the 20th is outside the week
        added = next(s for s in w["sessions"] if s["date"] == "2026-11-11")
        self.assertTrue(added["unplanned"])
        self.assertTrue(any("names no rotation slot" in n for n in notes), notes)

    def test_plan_block_and_ids(self):
        w = a_week()
        for s in w["sessions"]:
            s.pop("routine_id")
        week.assign_ids(w, ["a", "b"])
        self.assertEqual([s.get("routine_id") for s in w["sessions"]], [None, "a", "b"])   # done sessions take none
        block = week.render_block(w, fresh_tracks(), ROTATION, [], ALIASES, dt.date(2026, 11, 12))
        self.assertIn("| 2026-11-14 | Sat | U2 Upper B (Sat 14 Nov) | Overhead press H", block)
        self.assertTrue(block.startswith(week.MD_BEGIN) and block.endswith(week.MD_END))


class EngineReviewFixes(unittest.TestCase):
    """Defects found by the engine review of 2026-11-13, each against the written rule."""

    def test_a_deload_session_moves_no_track(self):                     # section 7
        t = fresh_tracks(squat={"top_set_lb": 155}, bench={"top_set_lb": 115, "step_counter": 1})
        rows = [("2026-10-27", "Full A (deload) (Tue 27 Oct)", "Squat (Barbell)", 0, "normal", 140, 4, 6.5),
                ("2026-10-27", "Full A (deload) (Tue 27 Oct)", "Bench Press (Barbell)", 0, "normal", 105, 4, None)]
        log, _ = run_update(t, rows)
        self.assertEqual((t["tracks"]["squat"]["top_set_lb"], t["tracks"]["bench"]["top_set_lb"]), (155, 115))
        self.assertEqual(t["tracks"]["bench"]["step_counter"], 1)
        self.assertEqual(t["tracks"]["squat"]["last_exposure"], {"date": "2026-10-27", "type": "H"})
        self.assertEqual(t["last_deload"], "2026-10-27")
        self.assertEqual(t["pointer"], "L2")                            # the session still counts for the rotation
        self.assertTrue(any("no track moves" in line for line in log), log)
        # the same through the week file's deload flag, with an ordinary title
        t = fresh_tracks(squat={"top_set_lb": 155})
        run_update(t, [("2026-10-27", "L1 Lower A", "Squat (Barbell)", 0, "normal", 140, 4, 6.5)], deload_dates={"2026-10-27"})
        self.assertEqual(t["tracks"]["squat"]["top_set_lb"], 155)

    def test_first_session_after_a_deload_opens_a_new_block(self):
        t = fresh_tracks()
        t["block_start"] = "2026-09-29"
        rows = [("2026-10-27", "L1 Lower A (deload)", "Squat (Barbell)", 0, "normal", 120, 4, 6),
                ("2026-11-03", "U1 Upper A", "Bench Press (Barbell)", 0, "normal", 95, 4, 8)]
        run_update(t, rows)
        self.assertEqual((t["block_start"], t["block_week"]), ("2026-11-03", 1))

    def test_a_flagged_stall_can_be_reset_on_a_later_run(self):         # section 6
        t = fresh_tracks(bench={"top_set_lb": 100, "last_h_load_lb": 100, "miss_counter": 1})
        log, _ = run_update(t, [("2026-10-27", "U1 Upper A", "Bench Press (Barbell)", 0, "normal", 100, 3, 10)])
        self.assertTrue(any("STALL" in line for line in log), log)
        self.assertTrue(t["tracks"]["bench"]["stall_pending"])
        self.assertEqual(t["tracks"]["bench"]["top_set_lb"], 100)
        self.assertIn("STALL: reset pending", upd.md_table(t))
        path = history_csv([("2026-10-27", "U1 Upper A", "Bench Press (Barbell)", 0, "normal", 100, 3, 10)])
        try:
            log, _ = upd.process(t, upd.load_sessions(path), ALIASES, ROTATION, reset_on_stall=True)   # nothing new logged
        finally:
            os.unlink(path)
        self.assertEqual(t["tracks"]["bench"]["top_set_lb"], 90)        # 100 x 0.925, rounded down to 5
        self.assertNotIn("stall_pending", t["tracks"]["bench"])
        self.assertEqual(t["tracks"]["bench"]["stalls"], 1)
        self.assertTrue(any("reset 100 -> 90" in line for line in log), log)

    def test_gap_hold_never_raises_the_load(self):                      # section 8
        t = fresh_tracks(bench={"top_set_lb": 90, "last_h_load_lb": 100, "last_exposure": {"date": "2026-10-12", "type": "H"}})
        load, _, note = push.gap_modifier(t["tracks"]["bench"], dt.date(2026, 10, 22))
        self.assertEqual(load, 90, note)
        t = fresh_tracks(bench={"top_set_lb": 105, "last_h_load_lb": 100, "last_exposure": {"date": "2026-10-12", "type": "H"}})
        self.assertEqual(push.gap_modifier(t["tracks"]["bench"], dt.date(2026, 10, 22))[0], 100)   # the ordinary hold

    def test_bodyweight_pull_ups_do_not_zero_the_pulldown_load(self):
        t = fresh_tracks()
        rows = [("2026-10-27", "U2 Upper B", "Pull Up", i, "normal", None, 6, None) for i in range(3)]
        log, flags = run_update(t, rows)
        self.assertEqual(t["tracks"]["pullup"]["top_set_lb"], 125)
        self.assertEqual(t["tracks"]["pullup"]["last_exposure"], {"date": "2026-10-27", "type": "H"})
        self.assertTrue(any("load is unchanged" in line for line in log), log)
        payload, _ = push.build_routine("U2", ROTATION, t, EXMAP, dt.date(2026, 10, 28))
        self.assertEqual(lbs(normal(payload["exercises"][1]["sets"]))[0], 125)

    def test_an_extra_heavier_double_is_not_the_top_set(self):          # section 5
        t = fresh_tracks(squat={"top_set_lb": 155, "regain": None})
        rows = [("2026-10-27", "L1 Lower A", "Squat (Barbell)", 0, "normal", 155, 4, 8),
                ("2026-10-27", "L1 Lower A", "Squat (Barbell)", 1, "normal", 165, 2, None)]
        log, _ = run_update(t, rows)
        self.assertEqual((t["tracks"]["squat"]["top_set_lb"], t["tracks"]["squat"]["miss_counter"]), (160, 0), log)
        # trying the planned load and falling short is still the miss it looks like
        t = fresh_tracks(squat={"top_set_lb": 155, "regain": None})
        run_update(t, [("2026-10-27", "L1 Lower A", "Squat (Barbell)", 0, "normal", 145, 4, 8),
                       ("2026-10-27", "L1 Lower A", "Squat (Barbell)", 1, "normal", 155, 2, None)])
        self.assertEqual((t["tracks"]["squat"]["top_set_lb"], t["tracks"]["squat"]["miss_counter"]), (155, 1))
        # equal loads: the first is the top set, the later ones are back-offs
        t = fresh_tracks(squat={"top_set_lb": 155, "regain": None})
        run_update(t, [("2026-10-27", "L1 Lower A", "Squat (Barbell)", 0, "normal", 155, 4, 9),
                       ("2026-10-27", "L1 Lower A", "Squat (Barbell)", 1, "normal", 155, 5, None)])
        self.assertEqual(t["tracks"]["squat"]["top_set_lb"], 155)       # 4 @ 9 is a hold

    def test_ordinary_back_offs_do_not_clear_the_unrated_count(self):   # section 5.3
        t = fresh_tracks(squat={"top_set_lb": 155, "regain": None, "unrated_streak": 1})
        rows = [("2026-10-27", "L1 Lower A", "Squat (Barbell)", 0, "normal", 155, 4, None),
                ("2026-10-27", "L1 Lower A", "Squat (Barbell)", 1, "normal", 145, 5, None),
                ("2026-10-27", "L1 Lower A", "Squat (Barbell)", 2, "normal", 145, 5, None)]
        run_update(t, rows)
        self.assertEqual(t["tracks"]["squat"]["unrated_streak"], 2)
        # a drop set far below the top set is not a rep-out either
        t = fresh_tracks(squat={"top_set_lb": 155, "regain": None})
        run_update(t, [("2026-10-27", "L1 Lower A", "Squat (Barbell)", 0, "normal", 155, 4, None),
                       ("2026-10-27", "L1 Lower A", "Squat (Barbell)", 1, "normal", 115, 9, None)])
        self.assertEqual(t["tracks"]["squat"]["top_set_lb"], 160)       # the normal step, not the big one


class Amendments(unittest.TestCase):
    def test_set_is_logged(self):
        t = fresh_tracks()
        line = upd.amend(t, "squat.top_set_lb=155", "lifter did 155 x 5 off plan", "2026-11-05")
        self.assertEqual(t["tracks"]["squat"]["top_set_lb"], 155)
        self.assertEqual(t["amendments"][-1]["to"], 155)
        self.assertIn("Amended by hand: squat.top_set_lb", line)
        upd.amend(t, "pointer=U2", "re-plan", "2026-11-05")
        self.assertEqual(t["pointer"], "U2")
        with self.assertRaises(SystemExit):
            upd.amend(t, "nolift.top_set_lb=1", "x", "2026-11-05")


class GitGuard(unittest.TestCase):
    """The rule that Hevy only gets what is on origin/main, against real git."""

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.old = os.environ.pop("WORKOUT_NO_GIT", None)
        g = lambda *a, cwd: subprocess.run(["git", *a], cwd=cwd, check=True, capture_output=True)  # noqa: E731
        self.g = g
        self.remote = os.path.join(self.dir, "remote.git")
        g("init", "--bare", "-b", "main", self.remote, cwd=self.dir)
        self.a = os.path.join(self.dir, "a")
        g("clone", self.remote, self.a, cwd=self.dir)
        for k, v in (("user.email", "t@example.invalid"), ("user.name", "t"), ("commit.gpgsign", "false")):
            g("config", k, v, cwd=self.a)
        os.makedirs(os.path.join(self.a, "data"))
        with open(os.path.join(self.a, "data", "tracks.json"), "w") as f:
            f.write("{}\n")
        g("add", "-A", cwd=self.a)
        g("commit", "-m", "start", cwd=self.a)
        g("push", "origin", "HEAD:main", cwd=self.a)

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)
        if self.old is not None:
            os.environ["WORKOUT_NO_GIT"] = self.old

    def edit(self, repo, text):
        with open(os.path.join(repo, "data", "tracks.json"), "w") as f:
            f.write(text)

    def test_unpublished_inputs_block_the_push(self):
        self.assertEqual(gitguard.unpublished(["data/tracks.json"], cwd=self.a), [])
        self.edit(self.a, '{"squat": 160}\n')
        self.assertEqual(gitguard.unpublished(["data/tracks.json"], cwd=self.a), ["data/tracks.json"])    # edited, not committed
        self.assertIsNotNone(gitguard.commit(["data/tracks.json"], "sync", cwd=self.a))
        self.assertEqual(gitguard.unpublished(["data/tracks.json"], cwd=self.a), ["data/tracks.json"])    # committed, not on main
        self.assertEqual(gitguard.publish(cwd=self.a), (True, ""))
        self.assertEqual(gitguard.unpublished(["data/tracks.json"], cwd=self.a), [])
        self.assertIsNone(gitguard.commit(["data/tracks.json"], "nothing new", cwd=self.a))
        with open(os.path.join(self.a, "data", "week.json"), "w") as f:
            f.write("{}\n")
        self.assertEqual(gitguard.unpublished(["data/week.json"], cwd=self.a), ["data/week.json"])        # new file

    def test_a_stale_checkout_cannot_sync(self):
        b = os.path.join(self.dir, "b")
        self.g("clone", self.remote, b, cwd=self.dir)
        for k, v in (("user.email", "t@example.invalid"), ("user.name", "t"), ("commit.gpgsign", "false")):
            self.g("config", k, v, cwd=b)
        self.assertEqual(gitguard.preflight(cwd=b), [])
        self.edit(self.a, '{"squat": 160}\n')
        gitguard.commit(["data/tracks.json"], "another session", cwd=self.a)
        gitguard.publish(cwd=self.a)
        found = gitguard.preflight(cwd=b)
        self.assertEqual(len(found), 1)
        self.assertIn("1 commit(s) behind origin/main", found[0])

    def test_a_read_only_session_cannot_sync(self):
        self.g("remote", "set-url", "--push", "origin", os.path.join(self.dir, "missing.git"), cwd=self.a)
        found = gitguard.preflight(cwd=self.a)
        self.assertEqual(len(found), 1, found)
        self.edit(self.a, '{"squat": 165}\n')
        gitguard.commit(["data/tracks.json"], "local only", cwd=self.a)
        ok, _ = gitguard.publish(cwd=self.a, retries=1)
        self.assertFalse(ok)


class PullNoNews(unittest.TestCase):
    def test_same_rows_compare_equal_whatever_their_order(self):
        rows = [{"date": "2026-11-10", "workout_id": "a", "exercise": "Squat (Barbell)", "set_index": "1", "reps": "4"},
                {"date": "2026-11-10", "workout_id": "a", "exercise": "Squat (Barbell)", "set_index": "0", "reps": "5"}]
        self.assertEqual(pull.normalized(rows), pull.normalized(list(reversed(rows))))
        changed = copy.deepcopy(rows)
        changed[0]["reps"] = "5"
        self.assertNotEqual(pull.normalized(rows), pull.normalized(changed))


class Dashboard(unittest.TestCase):
    MUSCLES = {"Squat (Barbell)": {"primary": "quadriceps", "secondary": ["glutes", "hamstrings"], "type": "weight_reps"},
               "Bench Press (Barbell)": {"primary": "chest", "secondary": ["triceps", "shoulders"], "type": "weight_reps"},
               "Pull Up (Assisted)": {"primary": "lats", "secondary": ["biceps"], "type": "bodyweight_assisted"}}

    def build(self, rows, today=TODAY):
        path = history_csv(rows)
        try:
            return dash.build(path, fresh_tracks(), ALIASES, self.MUSCLES, today)
        finally:
            os.unlink(path)

    def test_weekly_volume_and_muscle_credit(self):
        data = self.build([
            ("2026-10-19", "L1", "Squat (Barbell)", 0, "warmup", 40, 5, ""),
            ("2026-10-19", "L1", "Squat (Barbell)", 1, "normal", 60, 4, 8),
            ("2026-10-19", "L1", "Squat (Barbell)", 2, "normal", 55, 6, ""),
            ("2026-10-21", "U1", "Bench Press (Barbell)", 0, "normal", 40, 5, ""),
            ("2026-10-21", "U1", "Pull Up (Assisted)", 0, "normal", 20, 8, ""),
        ])
        w = data["weeks"][-1]
        self.assertEqual(w["week"], "2026-10-19")
        self.assertEqual((w["sessions"], w["days"], w["sets"]), (2, 2, 4))
        self.assertEqual(w["tonnage"], 60 * 4 + 55 * 6 + 40 * 5)  # warm-up and assisted sets left out
        self.assertEqual(w["muscles"]["quads"], 2)
        self.assertEqual(w["muscles"]["hams_glutes"], 1)  # glutes and hamstrings credit the group once per set
        self.assertEqual(w["muscles"]["triceps"], 0.5)
        self.assertEqual(w["muscles"]["back"], 1)
        self.assertEqual(w["target"], [4, 6])

    def test_week_over_week_trend_and_restart(self):
        rows = [("2026-08-03", "L1", "Squat (Barbell)", 0, "normal", 60, 4, 8),
                ("2026-10-05", "L1", "Squat (Barbell)", 0, "normal", 60, 4, 8),
                ("2026-10-12", "L1", "Squat (Barbell)", 0, "normal", 65, 4, 8),
                ("2026-10-19", "L1", "Squat (Barbell)", 0, "normal", 65, 4, 8)]
        weeks = {w["week"]: w for w in self.build(rows)["weeks"]}
        self.assertEqual(weeks["2026-08-03"]["lifts"]["squat"]["trend"], "first")
        self.assertEqual(weeks["2026-10-05"]["lifts"]["squat"]["trend"], "restart")
        self.assertEqual(weeks["2026-10-12"]["lifts"]["squat"]["trend"], "up")
        self.assertEqual(weeks["2026-10-19"]["lifts"]["squat"]["trend"], "flat")
        self.assertEqual(weeks["2026-10-12"]["lifts"]["squat"]["prev_week"], "2026-10-05")

    def test_empty_weeks_filled_and_streaks(self):
        rows = [(d, "L1", "Squat (Barbell)", 0, "normal", 60, 4, 8)
                for d in ("2026-09-14", "2026-09-21", "2026-10-05", "2026-10-12")]
        data = self.build(rows, today=dt.date(2026, 10, 22))
        self.assertEqual([w["week"] for w in data["weeks"]][-2:], ["2026-10-12", "2026-10-19"])
        self.assertEqual(data["weeks"][-1]["sessions"], 0)
        self.assertEqual(data["consistency"]["current_streak"], 2)  # the week in progress does not break it
        self.assertEqual(data["consistency"]["longest_streak"], 2)
        # one gap clock: the lifts table and the track card read the track's own clock
        path = history_csv(rows)
        try:
            ten_days = {"last_exposure": {"date": "2026-10-12", "type": "H"}}
            data = dash.build(path, fresh_tracks(squat=ten_days, bench=ten_days), ALIASES, self.MUSCLES, dt.date(2026, 10, 22))
        finally:
            os.unlink(path)
        squat = next(l for l in data["lifts"] if l["key"] == "squat")
        card = next(c for c in data["tracks"] if c["key"] == "squat")
        self.assertEqual((card["gap_days"], card["gap"]), (squat["gap_days"], squat["gap"]))
        # the same rule as the routine: a regain-phase lift is not held at 8-14 days, another lift is
        self.assertEqual((squat["gap_days"], squat["gap"]["key"]), (10, "normal"))
        self.assertIn("regain", squat["gap"]["label"].lower())
        bench = next(c for c in data["tracks"] if c["key"] == "bench")
        self.assertEqual((bench["gap_days"], bench["gap"]["key"]), (10, "hold"))

    def test_week_set_count_survives_a_better_set(self):
        rows = [("2026-10-19", "U1", "Bench Press (Barbell)", i, "normal", w, r, None)
                for i, (w, r) in enumerate([(95, 4), (100, 4), (90, 6), (90, 6)])]
        week = self.build(rows)["weeks"][-1]["lifts"]["bench"]
        self.assertEqual(week["sets"], 4)
        self.assertEqual((week["top_load"], week["top_reps"]), (100, 4))

    def test_render_inlines_data(self):
        data = self.build([("2026-10-19", "L1", "Squat (Barbell)", 0, "normal", 60, 4, 8)])
        data["unmapped"] = ["</script><b>x"]
        html = dash.render(data)
        self.assertNotIn(dash.PLACEHOLDER, html)
        self.assertNotIn("</script><b>", html)
        self.assertIn('"week":"2026-10-19"', html)

    def test_track_log_parse(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write("# Track log\n\n## 2026-10-27\n\n- 2026-10-27 L1 Back squat: top 60 x 4 @ 8 -> +2.5\n"
                    "- 2026-10-27 L1 Bench press: STALL on Bench press\n- Flag: pointer jumped\n")
        try:
            log = dash.parse_track_log(f.name)
        finally:
            os.unlink(f.name)
        self.assertEqual([x["kind"] for x in log], ["decision", "stall", "flag"])
        self.assertEqual(log[0]["date"], "2026-10-27")


if __name__ == "__main__":
    unittest.main(verbosity=1)
