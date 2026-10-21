#!/usr/bin/env python3
"""Offline tests for the Hevy integration and the progression-rule engine.

    python3 tools/test_tools.py

No network: the API client is not exercised beyond payload shapes. Fixtures
are built in memory from the committed rotation.json and tracks.json.
"""
import copy
import csv
import datetime as dt
import io
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import hevy_push_routines as push  # noqa: E402
import update_tracks as upd  # noqa: E402
from hevy_api import HISTORY_COLUMNS, workout_rows  # noqa: E402


def load(path):
    with open(os.path.join(ROOT, path)) as f:
        return json.load(f)


ROTATION = load("templates/rotation.json")
TRACKS = load("data/tracks.json")
ALIASES = load("tools/lift_aliases.json")
EXMAP = {ex["name"]: {"hevy_title": ex["hevy"][0], "template_id": "T-" + ex["name"][:6].upper()}
         for s in ROTATION["sessions"].values() for ex in s["exercises"]}
TODAY = dt.date(2026, 10, 22)


def fresh_tracks(**over):
    t = copy.deepcopy(TRACKS)
    for lift, fields in over.items():
        t["tracks"][lift].update(fields)
    return t


def history_csv(rows):
    """rows: (date, title, exercise, set_index, type, weight, reps, rpe)."""
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=HISTORY_COLUMNS)
    w.writeheader()
    for i, (date, title, ex, idx, typ, wt, reps, rpe) in enumerate(rows):
        w.writerow({"date": date, "workout_title": title, "exercise": ex, "set_index": idx, "set_type": typ,
                    "weight_kg": wt, "reps": reps, "rpe": rpe, "notes": "", "source": "hevy-api", "workout_id": f"w-{date}-{title}"})
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
    def test_nine_sessions_and_all_tracks_have_one_h_and_one_v(self):
        self.assertEqual(set(ROTATION["sessions"]), {"L1", "U1", "L2", "U2", "L3", "U3", "Full A", "Full B", "Full C"})
        for lift, t in TRACKS["tracks"].items():
            for slot_list, role in ((t["h_slots"], "H"), (t["v_slots"], "V")):
                for slot in slot_list:
                    roles = [ex["role"] for ex in ROTATION["sessions"][slot]["exercises"] if ex.get("track") == lift]
                    self.assertEqual(roles, [role], f"{lift} in {slot} should be exactly one {role}")

    def test_every_accessory_has_a_load_entry(self):
        for s in ROTATION["sessions"].values():
            for ex in s["exercises"]:
                if ex["role"] == "acc":
                    self.assertIn(ex["name"], TRACKS["accessories"], ex["name"])


class RenderRoutines(unittest.TestCase):
    def test_l1_squat_heavy(self):
        payload, unresolved = push.build_routine("L1", ROTATION, TRACKS, EXMAP, TODAY)
        self.assertEqual(unresolved, [])
        squat = payload["exercises"][0]
        self.assertEqual(squat["exercise_template_id"], EXMAP["Back squat"]["template_id"])
        types = [s["type"] for s in squat["sets"]]
        self.assertEqual(types, ["warmup"] * 4 + ["normal"] * 4)
        self.assertEqual([s["weight_kg"] for s in squat["sets"] if s["type"] == "normal"], [60, 55, 55, 55])
        self.assertEqual(squat["sets"][0]["weight_kg"], 20)  # empty bar
        self.assertIn("RPE 8", squat["notes"])
        # superset ids pass through
        self.assertEqual(payload["exercises"][3]["superset_id"], 1)
        self.assertEqual(payload["exercises"][4]["superset_id"], 1)

    def test_merged_full_a_has_two_backoffs_and_three_rows(self):
        payload, _ = push.build_routine("Full A", ROTATION, TRACKS, EXMAP, TODAY)
        squat, bench, row = payload["exercises"][:3]
        self.assertEqual(sum(1 for s in squat["sets"] if s["type"] == "normal"), 3)
        self.assertEqual(sum(1 for s in bench["sets"] if s["type"] == "normal"), 3)
        self.assertEqual([s["weight_kg"] for s in bench["sets"] if s["type"] == "normal"], [42.5, 39.5, 39.5])
        self.assertIn("hold, not a miss", bench["notes"])
        self.assertEqual(len(row["sets"]), 3)
        self.assertEqual(row["sets"][0]["rep_range"], {"start": 6, "end": 8})
        self.assertEqual(row["sets"][0]["weight_kg"], 32.5)

    def test_volume_sets_are_90_percent(self):
        payload, _ = push.build_routine("U3", ROTATION, TRACKS, EXMAP, TODAY)
        bench, press, row, pull = payload["exercises"][:4]
        self.assertEqual([s for s in bench["sets"] if s["type"] == "normal"], [{"type": "normal", "weight_kg": 38.5, "reps": 6}] * 4)
        self.assertEqual([s["weight_kg"] for s in press["sets"] if s["type"] == "normal"], [25.0] * 3)
        self.assertEqual(row["sets"][0]["weight_kg"], 30.0)
        self.assertEqual(pull["sets"][0]["weight_kg"], 52.5)

    def test_work_up_renders_blank_loads(self):
        payload, _ = push.build_routine("L2", ROTATION, TRACKS, EXMAP, TODAY)
        dl = payload["exercises"][0]
        self.assertTrue(all(s["weight_kg"] is None for s in dl["sets"]))
        self.assertIn("40 x 4", dl["notes"])

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
        normal = [s for s in bench["sets"] if s["type"] == "normal"]
        self.assertEqual(len(normal), 2)  # top set + one back-off
        self.assertEqual(normal[0]["weight_kg"], 38.5)  # 42.5 x 0.91 rounded to 0.5
        self.assertEqual(sum(1 for s in row["sets"] if s["type"] == "normal"), 2)
        self.assertTrue(payload["title"].endswith("(deload)"))
        acc = payload["exercises"][2]
        self.assertEqual(len(acc["sets"]), 2)

    def test_gap_modifiers(self):
        t = fresh_tracks(squat={"top_set_kg": 62.5, "last_h_load_kg": 60, "last_exposure": {"date": "2026-10-01", "type": "H"}})["tracks"]["squat"]
        self.assertEqual(push.gap_modifier(t, dt.date(2026, 10, 8)), (62.5, 0, None))         # 7 days: normal
        self.assertEqual(push.gap_modifier(t, dt.date(2026, 10, 11))[:2], (60, 0))           # 10 days: hold
        self.assertEqual(push.gap_modifier(t, dt.date(2026, 10, 19))[:2], (60, -1))          # 18 days: hold, one fewer back-off
        self.assertEqual(push.gap_modifier(t, dt.date(2026, 10, 26))[:2], (57.5, 0))         # 25 days: -5%
        self.assertEqual(push.gap_modifier(t, dt.date(2026, 11, 5))[:2], (55.0, 0))          # 35 days: -10%

    def test_gap_hold_changes_backoff_count_in_payload(self):
        tr = fresh_tracks(squat={"top_set_kg": 62.5, "last_h_load_kg": 60, "last_exposure": {"date": "2026-10-01", "type": "H"}})
        payload, _ = push.build_routine("L1", ROTATION, tr, EXMAP, dt.date(2026, 10, 19))
        squat = payload["exercises"][0]
        self.assertEqual([s["weight_kg"] for s in squat["sets"] if s["type"] == "normal"], [60, 55, 55])


class UpdateRules(unittest.TestCase):
    def test_slot_parsing(self):
        self.assertEqual(upd.parse_slot("L1 Lower A"), "L1")
        self.assertEqual(upd.parse_slot("full b"), "Full B")
        self.assertEqual(upd.parse_slot("FULL C (deload)"), "Full C")
        self.assertIsNone(upd.parse_slot("Evening workout"))
        self.assertIsNone(upd.parse_slot("L10 something"))

    def test_increment_on_rpe_8(self):
        tr = fresh_tracks()
        log, flags = run_update(tr, [
            ("2026-10-27", "L1 Lower A", "Squat (Barbell)", 0, "warmup", 20, 10, ""),
            ("2026-10-27", "L1 Lower A", "Squat (Barbell)", 4, "normal", 60, 4, 8),
            ("2026-10-27", "L1 Lower A", "Squat (Barbell)", 5, "normal", 55, 4, 7),
        ])
        sq = tr["tracks"]["squat"]
        self.assertEqual(sq["top_set_kg"], 62.5)
        self.assertEqual(sq["last_h_load_kg"], 60)
        self.assertEqual(sq["miss_counter"], 0)
        self.assertEqual(sq["last_exposure"], {"date": "2026-10-27", "type": "H"})
        self.assertEqual(sq["e1rm_history"][-1]["e1rm"], 72.0)  # 60 x (1 + 6/30)
        self.assertEqual(tr["pointer"], "U1")
        self.assertEqual(flags, [])

    def test_big_step_on_rpe_7_and_actual_load_is_the_base(self):
        tr = fresh_tracks()
        run_update(tr, [("2026-10-27", "L1", "Squat (Barbell)", 0, "normal", 65, 4, 7)])
        self.assertEqual(tr["tracks"]["squat"]["top_set_kg"], 70)

    def test_hold_and_miss(self):
        tr = fresh_tracks()
        run_update(tr, [("2026-10-27", "U1", "Bench Press (Barbell)", 0, "normal", 42.5, 4, 9)])
        self.assertEqual(tr["tracks"]["bench"]["top_set_kg"], 42.5)
        self.assertEqual(tr["tracks"]["bench"]["miss_counter"], 0)
        tr = fresh_tracks()
        run_update(tr, [("2026-10-27", "U1", "Bench Press (Barbell)", 0, "normal", 42.5, 3, 10)])
        self.assertEqual(tr["tracks"]["bench"]["miss_counter"], 1)

    def test_merged_second_lift_at_rpe_9_5_is_a_hold_not_a_miss(self):
        tr = fresh_tracks()
        log, _ = run_update(tr, [
            ("2026-10-27", "Full A", "Squat (Barbell)", 0, "normal", 60, 4, 8),
            ("2026-10-27", "Full A", "Bench Press (Barbell)", 0, "normal", 42.5, 4, 9.5),
        ])
        self.assertEqual(tr["tracks"]["bench"]["miss_counter"], 0)
        self.assertEqual(tr["tracks"]["bench"]["top_set_kg"], 42.5)
        self.assertEqual(tr["pointer"], "L2")

    def test_stall_flagged_then_reset(self):
        tr = fresh_tracks(squat={"miss_counter": 1, "last_h_load_kg": 60, "top_set_kg": 60})
        log, _ = run_update(tr, [("2026-10-27", "L1", "Squat (Barbell)", 0, "normal", 60, 3, 10)])
        self.assertIn("STALL", log[0])
        self.assertEqual(tr["tracks"]["squat"]["top_set_kg"], 60)  # held without --reset-on-stall
        tr = fresh_tracks(squat={"miss_counter": 1, "last_h_load_kg": 60, "top_set_kg": 60})
        run_update(tr, [("2026-10-27", "L1", "Squat (Barbell)", 0, "normal", 60, 3, 10)], reset_on_stall=True)
        self.assertEqual(tr["tracks"]["squat"]["top_set_kg"], 55)  # floor(60 x 0.925 = 55.5) to 2.5
        self.assertEqual(tr["tracks"]["squat"]["stalls"], 1)
        self.assertEqual(tr["tracks"]["squat"]["miss_counter"], 0)

    def test_double_progression_row(self):
        tr = fresh_tracks()
        run_update(tr, [("2026-10-27", "U1", "Bent Over Row (Barbell)", i, "normal", 32.5, 8, 8) for i in range(4)])
        self.assertEqual(tr["tracks"]["row"]["top_set_kg"], 35)
        tr = fresh_tracks()
        run_update(tr, [("2026-10-27", "U1", "Bent Over Row (Barbell)", i, "normal", 32.5, r, 8) for i, r in enumerate([8, 7, 6, 6])])
        self.assertEqual(tr["tracks"]["row"]["top_set_kg"], 32.5)
        self.assertEqual(tr["tracks"]["row"]["miss_counter"], 0)
        tr = fresh_tracks()
        run_update(tr, [("2026-10-27", "U1", "Bent Over Row (Barbell)", i, "normal", 32.5, r, 9) for i, r in enumerate([5, 5, 4])])
        self.assertEqual(tr["tracks"]["row"]["miss_counter"], 1)

    def test_work_up_sets_the_deadlift_track(self):
        tr = fresh_tracks()
        run_update(tr, [
            ("2026-10-29", "L2", "Deadlift (Barbell)", 0, "normal", 50, 4, 6),
            ("2026-10-29", "L2", "Deadlift (Barbell)", 1, "normal", 60, 4, 7),
            ("2026-10-29", "L2", "Deadlift (Barbell)", 2, "normal", 65, 4, 8),
            ("2026-10-29", "L2", "Deadlift (Barbell)", 3, "normal", 60, 4, 7.5),
        ])
        dl = tr["tracks"]["deadlift"]
        self.assertEqual(dl["top_set_kg"], 67.5)
        self.assertNotIn("work_up", dl)

    def test_volume_and_untitled_sessions_only_touch_the_clock(self):
        tr = fresh_tracks()
        log, _ = run_update(tr, [
            ("2026-10-31", "L3", "Squat (Barbell)", 0, "normal", 55, 6, 7),
            ("2026-11-02", "Evening workout", "Bench Press (Barbell)", 0, "normal", 50, 5, 9),
        ])
        self.assertEqual(log, [])
        self.assertEqual(tr["tracks"]["squat"]["top_set_kg"], 60)
        self.assertEqual(tr["tracks"]["squat"]["last_exposure"], {"date": "2026-10-31", "type": "V"})
        self.assertEqual(tr["tracks"]["bench"]["last_exposure"], {"date": "2026-11-02", "type": "other"})
        self.assertEqual(tr["pointer"], "U3")

    def test_no_rpe_is_flagged_and_treated_as_8(self):
        tr = fresh_tracks()
        _, flags = run_update(tr, [("2026-10-27", "L1", "Squat (Barbell)", 0, "normal", 60, 4, "")])
        self.assertEqual(tr["tracks"]["squat"]["top_set_kg"], 62.5)
        self.assertTrue(flags and "no RPE" in flags[0])

    def test_processed_through_prevents_double_counting(self):
        tr = fresh_tracks()
        rows = [("2026-10-27", "L1", "Squat (Barbell)", 0, "normal", 60, 4, 8)]
        run_update(tr, rows)
        run_update(tr, rows)
        self.assertEqual(tr["tracks"]["squat"]["top_set_kg"], 62.5)
        self.assertEqual(len(tr["tracks"]["squat"]["e1rm_history"]), 2)  # seed + one

    def test_committed_history_does_not_move_any_track(self):
        tr = fresh_tracks()
        sessions = upd.load_sessions(os.path.join(ROOT, "data", "history.csv"))
        log, _ = upd.process(tr, sessions, ALIASES, ROTATION)
        self.assertEqual(log, [])
        for lift in TRACKS["tracks"]:
            self.assertEqual(tr["tracks"][lift]["top_set_kg"], TRACKS["tracks"][lift]["top_set_kg"])

    def test_md_table_renders(self):
        table = upd.md_table(TRACKS)
        self.assertIn("| Back squat | **60** | 55 | 55 |", table)
        self.assertIn("work up", table)


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


if __name__ == "__main__":
    unittest.main(verbosity=1)
