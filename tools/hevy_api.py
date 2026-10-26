#!/usr/bin/env python3
"""Hevy public API client and command-line inspector. Standard library only.

The schema here was read from the OpenAPI document embedded in
https://api.hevyapp.com/docs/ on 2026-10-21 (see
research/mobile-workout-trackers.md, addendum of that date). The API is
Pro-only; the key comes from https://hevy.com/settings?developer and is read
from the HEVY_API_KEY environment variable, or is attached by the cloud
environment's proxy when a network secret exists for api.hevyapp.com (then no
variable is needed). Never pass it on the command line or write it into the repo.

Library use:

    from hevy_api import Hevy
    h = Hevy()                       # reads HEVY_API_KEY
    for w in h.iter_workouts(): ...  # newest first, 10 per page
    ids = h.exercise_template_index()  # {title: template_id}
    r = h.create_routine(title="L1 Lower A", folder_id=42, exercises=[...])

Command line (each prints JSON or a short table; workouts and history add
weight_lb beside each weight_kg, since the program runs in pounds):

    python3 tools/hevy_api.py whoami
    python3 tools/hevy_api.py count
    python3 tools/hevy_api.py workouts [--pages 1]
    python3 tools/hevy_api.py events --since 2026-10-01T00:00:00Z
    python3 tools/hevy_api.py routines
    python3 tools/hevy_api.py folders
    python3 tools/hevy_api.py templates [--search "bench"]
    python3 tools/hevy_api.py history <exercise_template_id> [--start 2026-01-01]
    python3 tools/hevy_api.py measurements

Endpoints (all under https://api.hevyapp.com/v1, header `api-key`):

    GET  /workouts?page&pageSize(<=10)        -> {page, page_count, workouts[]}
    GET  /workouts/count                       -> {workout_count}
    GET  /workouts/events?since&page&pageSize  -> {page, page_count, events[]}
    GET  /workouts/{id}                        -> Workout
    POST /workouts                             -> {workout: [Workout]}
    PUT  /workouts/{id}
    GET  /user/info                            -> {data: {...}}
    GET  /routines?page&pageSize(<=10)         -> {page, page_count, routines[]}
    POST /routines                             -> {routine}   (403 = routine limit)
    GET  /routines/{id}
    PUT  /routines/{id}                        -> {routine}
    GET  /routine_folders?page&pageSize(<=10)  -> {page, page_count, routine_folders[]}
    POST /routine_folders                      -> RoutineFolder (created at index 0)
    GET  /routine_folders/{id}
    GET  /exercise_templates?page&pageSize(<=100) -> {page, page_count, exercise_templates[]}
    POST /exercise_templates                   (custom exercise)
    GET  /exercise_templates/{id}
    GET  /exercise_history/{templateId}?start_date&end_date -> {exercise_history[]}
    GET  /body_measurements?page&pageSize      -> paginated
    POST /body_measurements, GET/PUT /body_measurements/{date}

There is no delete endpoint for routines or folders and no webhook endpoint
in the published spec. Workout sets carry `rpe` (6-10 in 0.5 steps); routine
sets carry `weight_kg`, `reps` or `rep_range {start, end}`, `type`
(warmup, normal, failure, dropset) and no RPE.
"""
import argparse
import datetime as dt
import json
import os
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://api.hevyapp.com/v1"
MAX_PAGE_SIZE = {"workouts": 10, "workouts/events": 10, "routines": 10,
                 "routine_folders": 10, "exercise_templates": 100, "body_measurements": 10}


class HevyError(RuntimeError):
    pass


class Hevy:
    def __init__(self, key=None, base=BASE, timeout=60, verbose=False):
        # Two ways to supply the key. (1) HEVY_API_KEY in the environment: the
        # client sends it in the api-key header itself. (2) A cloud-environment
        # "network secret" for api.hevyapp.com with a custom header named
        # api-key: the proxy adds the header after the request leaves the VM,
        # so no variable is needed here and the key never enters the sandbox.
        self.key = key or os.environ.get("HEVY_API_KEY")
        if not self.key and verbose:
            print("HEVY_API_KEY not set; relying on a network secret for api.hevyapp.com", file=sys.stderr)
        self.base = base
        self.timeout = timeout
        self.verbose = verbose
        self._templates = None

    # ----- transport -------------------------------------------------------

    def request(self, method, path, params=None, body=None, retries=5):
        url = self.base + path
        if params:
            url += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
        data = json.dumps(body).encode() if body is not None else None
        headers = {"accept": "application/json"}
        if self.key:
            headers["api-key"] = self.key
        if data is not None:
            headers["content-type"] = "application/json"
        if self.verbose:
            print(f"  {method} {url}", file=sys.stderr)
        for attempt in range(retries):
            req = urllib.request.Request(url, data=data, headers=headers, method=method)
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    raw = resp.read()
                    return json.loads(raw) if raw else {}
            except urllib.error.HTTPError as e:
                text = e.read().decode(errors="replace")[:500]
                if e.code in (401, 403) and "limit" not in text.lower():
                    how = "HEVY_API_KEY" if self.key else "no HEVY_API_KEY is set and no network secret for api.hevyapp.com added an api-key header"
                    raise HevyError(f"Hevy refused the request (HTTP {e.code}): {how}. The key comes from https://hevy.com/settings?developer and needs Pro. {text}")
                if e.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                    time.sleep((2 ** attempt) + random.random())
                    continue
                raise HevyError(f"HTTP {e.code} on {method} {path}: {text}")
            except urllib.error.URLError as e:
                if attempt < retries - 1:
                    time.sleep((2 ** attempt) + random.random())
                    continue
                raise HevyError(f"Could not reach {self.base}: {e.reason}. In a cloud sandbox, api.hevyapp.com must be an allowed host.")

    def get(self, path, **params):
        return self.request("GET", path, params=params or None)

    def post(self, path, body):
        return self.request("POST", path, body=body)

    def put(self, path, body):
        return self.request("PUT", path, body=body)

    def paginate(self, resource, key, **params):
        """Yield items from a paged list endpoint. `key` is the array field name."""
        size = MAX_PAGE_SIZE.get(resource, 10)
        page = 1
        while True:
            data = self.get("/" + resource, page=page, pageSize=size, **params)
            items = data.get(key) or []
            for it in items:
                yield it
            page_count = data.get("page_count") or 0
            if not items or page >= page_count:
                return
            page += 1

    # ----- account ---------------------------------------------------------

    def user_info(self):
        return self.get("/user/info").get("data", {})

    def workout_count(self):
        return self.get("/workouts/count").get("workout_count")

    # ----- workouts (read) -------------------------------------------------

    def iter_workouts(self, max_pages=None):
        """Newest first. Each workout: id, title, routine_id, start_time, end_time,
        exercises[{index, title, exercise_template_id, notes, superset_id,
        sets[{index, type, weight_kg, reps, rpe, duration_seconds, distance_meters}]}]."""
        for i, w in enumerate(self.paginate("workouts", "workouts")):
            if max_pages is not None and i >= max_pages * MAX_PAGE_SIZE["workouts"]:
                return
            yield w

    def workout(self, workout_id):
        return self.get(f"/workouts/{workout_id}")

    def iter_workout_events(self, since):
        """Events since an ISO-8601 timestamp, newest first:
        {type: 'updated', workout: Workout} or {type: 'deleted', id, deleted_at}."""
        return self.paginate("workouts/events", "events", since=since)

    def exercise_history(self, template_id, start_date=None, end_date=None):
        return self.get(f"/exercise_history/{template_id}", start_date=start_date, end_date=end_date).get("exercise_history", [])

    # ----- workouts (write) ------------------------------------------------

    def create_workout(self, title, start_time, end_time, exercises, description=None, is_private=False):
        body = {"workout": {"title": title, "start_time": start_time, "end_time": end_time,
                            "description": description, "is_private": is_private, "exercises": exercises}}
        return self.post("/workouts", body)

    # ----- routines and folders ------------------------------------------

    def iter_routines(self):
        return self.paginate("routines", "routines")

    def routine(self, routine_id):
        return self.get(f"/routines/{routine_id}")

    def create_routine(self, title, exercises, folder_id=None, notes=None):
        body = {"routine": {"title": title, "folder_id": folder_id, "notes": notes, "exercises": exercises}}
        return self.post("/routines", body).get("routine", {})

    def update_routine(self, routine_id, title, exercises, folder_id=None, notes=None):
        body = {"routine": {"title": title, "folder_id": folder_id, "notes": notes, "exercises": exercises}}
        return self.put(f"/routines/{routine_id}", body).get("routine", {})

    def iter_folders(self):
        return self.paginate("routine_folders", "routine_folders")

    def create_folder(self, title):
        """The spec shows a bare RoutineFolder; the live API wraps it as
        {"routine_folder": {...}}. Accept both."""
        r = self.post("/routine_folders", {"routine_folder": {"title": title}})
        return r.get("routine_folder", r) if isinstance(r, dict) else r

    def find_folder(self, title):
        for f in self.iter_folders():
            if (f.get("title") or "").strip().lower() == title.strip().lower():
                return f
        return None

    # ----- exercise templates --------------------------------------------

    def exercise_templates(self, refresh=False):
        if self._templates is None or refresh:
            self._templates = list(self.paginate("exercise_templates", "exercise_templates"))
        return self._templates

    def exercise_template_index(self):
        """{lowercased title: template dict}. Built-in Hevy titles look like
        'Bench Press (Barbell)'; custom ones are whatever the user named them."""
        return {(t.get("title") or "").strip().lower(): t for t in self.exercise_templates()}

    def find_template(self, title):
        return self.exercise_template_index().get(title.strip().lower())

    def create_custom_exercise(self, title, exercise_type="weight_reps", equipment="other", muscle_group="other", other_muscles=None):
        body = {"exercise": {"title": title, "exercise_type": exercise_type, "equipment_category": equipment,
                             "muscle_group": muscle_group, "other_muscles": other_muscles or []}}
        return self.post("/exercise_templates", body)

    # ----- body measurements ---------------------------------------------

    def iter_measurements(self):
        return self.paginate("body_measurements", "body_measurements")


# ----- helpers shared by the other tools --------------------------------------

HISTORY_COLUMNS = [
    "date", "workout_title", "exercise", "set_index", "set_type",
    "weight_kg", "reps", "rpe", "notes", "source", "workout_id",
]


def workout_rows(w, source="hevy-api"):
    """Flatten one API workout into normalized set rows (tools/README.md)."""
    date = (w.get("start_time") or "")[:10]
    title = w.get("title") or ""
    for ex in w.get("exercises") or []:
        for s in ex.get("sets") or []:
            yield {
                "date": date,
                "workout_title": title,
                "exercise": ex.get("title") or "",
                "set_index": s.get("index", ""),
                "set_type": s.get("type") or "normal",
                "weight_kg": "" if s.get("weight_kg") is None else round(s.get("weight_kg"), 2),
                "reps": "" if s.get("reps") is None else s.get("reps"),
                "rpe": "" if s.get("rpe") is None else s.get("rpe"),
                "notes": (ex.get("notes") or "").replace("\n", " ").replace(",", ";"),
                "source": source,
                "workout_id": w.get("id") or "",
            }


def now_iso():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


# ----- CLI ---------------------------------------------------------------------

def _print(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def with_lb(obj):
    """Add weight_lb (to 0.1 lb) beside every weight_kg, for reading output in
    the program's units. The API itself only speaks kg."""
    if isinstance(obj, list):
        return [with_lb(x) for x in obj]
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            out[k] = with_lb(v)
            if k == "weight_kg":
                out["weight_lb"] = None if v is None else round(v / 0.45359237, 1)
        return out
    return obj


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("-v", "--verbose", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("whoami")
    sub.add_parser("count")
    p = sub.add_parser("workouts"); p.add_argument("--pages", type=int, default=1)
    p = sub.add_parser("events"); p.add_argument("--since", required=True)
    sub.add_parser("routines")
    sub.add_parser("folders")
    p = sub.add_parser("templates"); p.add_argument("--search")
    p = sub.add_parser("history"); p.add_argument("template_id"); p.add_argument("--start"); p.add_argument("--end")
    sub.add_parser("measurements")
    args = ap.parse_args(argv)

    try:
        h = Hevy(verbose=args.verbose)
        if args.cmd == "whoami":
            _print(h.user_info())
        elif args.cmd == "count":
            print(h.workout_count())
        elif args.cmd == "workouts":
            _print(with_lb(list(h.iter_workouts(max_pages=args.pages))))
        elif args.cmd == "events":
            _print(list(h.iter_workout_events(args.since)))
        elif args.cmd == "routines":
            for r in h.iter_routines():
                print(f"{r.get('id')}  folder={r.get('folder_id')}  {r.get('title')}  ({len(r.get('exercises') or [])} exercises)")
        elif args.cmd == "folders":
            for f in h.iter_folders():
                print(f"{f.get('id'):>6}  idx={f.get('index')}  {f.get('title')}")
        elif args.cmd == "templates":
            q = (args.search or "").lower()
            for t in h.exercise_templates():
                if q in (t.get("title") or "").lower():
                    print(f"{t.get('id'):>10}  {t.get('title')}  [{t.get('type')}, {t.get('equipment')}, {t.get('primary_muscle_group')}{', custom' if t.get('is_custom') else ''}]")
        elif args.cmd == "history":
            _print(with_lb(h.exercise_history(args.template_id, args.start, args.end)))
        elif args.cmd == "measurements":
            _print(list(h.iter_measurements()))
    except HevyError as e:
        sys.exit(str(e))


if __name__ == "__main__":
    main()
