"""The lifter's calendar, not the server's.

Hevy timestamps and cloud containers are UTC. A workout at 7:22 pm Eastern is
already "tomorrow" in UTC, so every date the tools derive goes through here.
The zone is TRAINING_TZ (default America/New_York).
"""
import datetime as dt
import os
from zoneinfo import ZoneInfo

ZONE = ZoneInfo(os.environ.get("TRAINING_TZ") or "America/New_York")


def local_today(now=None):
    """Today's date where the lifter is. `now` is an aware datetime (tests)."""
    return (now or dt.datetime.now(dt.timezone.utc)).astimezone(ZONE).date()


def local_date(iso):
    """The lifter's calendar date (YYYY-MM-DD) of an ISO-8601 timestamp.
    A bare date or a timestamp without an offset is returned as written."""
    if not iso:
        return ""
    s = iso.strip()
    if len(s) <= 10:
        return s
    try:
        t = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return s[:10]
    if t.tzinfo is None:
        return s[:10]
    return t.astimezone(ZONE).date().isoformat()
