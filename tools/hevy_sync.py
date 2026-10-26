#!/usr/bin/env python3
"""One command for the weekly loop: pull Hevy history, apply the progression
rules, rebuild the progress dashboard, push the updated routines back to Hevy.

Usage:
    python3 tools/hevy_sync.py                 # pull -> update tracks -> push routines
    python3 tools/hevy_sync.py --dry-run       # pull (read-only), then show decisions and payloads without writing
    python3 tools/hevy_sync.py --no-push       # pull and update tracks only
    python3 tools/hevy_sync.py --deload        # push the deload rendering after updating tracks
    python3 tools/hevy_sync.py --reset-on-stall

Equivalent to:
    python3 tools/hevy_pull.py
    python3 tools/update_tracks.py --write-md [--reset-on-stall]
    python3 tools/build_dashboard.py             (skipped with --dry-run)
    python3 tools/hevy_push_routines.py [--deload]
"""
import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def run(script, *flags):
    cmd = [sys.executable, os.path.join(HERE, script), *flags]
    print(f"\n$ python3 {os.path.relpath(cmd[1])} {' '.join(flags)}".rstrip())
    return subprocess.call(cmd)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-pull", action="store_true", help="skip the pull (use the committed history.csv)")
    ap.add_argument("--no-push", action="store_true")
    ap.add_argument("--deload", action="store_true")
    ap.add_argument("--reset-on-stall", action="store_true")
    ap.add_argument("--full", action="store_true", help="full re-pull instead of incremental")
    args = ap.parse_args(argv)

    if not args.no_pull:
        if run("hevy_pull.py", *(["--full"] if args.full else [])):
            sys.exit("Pull failed; stopping.")
    upd = ["--write-md"] + (["--reset-on-stall"] if args.reset_on_stall else []) + (["--dry-run"] if args.dry_run else [])
    if run("update_tracks.py", *upd):
        sys.exit("Track update failed; stopping.")
    if not args.dry_run and run("build_dashboard.py"):
        print("Dashboard build failed; continuing.")
    if args.no_push:
        return
    push = (["--deload"] if args.deload else []) + (["--dry-run"] if args.dry_run else [])
    if run("hevy_push_routines.py", *push):
        sys.exit("Push failed.")


if __name__ == "__main__":
    main()
