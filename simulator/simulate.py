"""Run the monitoring simulator using the main application modules."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure the main application package is on the path
ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from monitor import monitor, replay


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the COTS simulator")
    sub = parser.add_subparsers(dest="command", required=True)

    mon = sub.add_parser("run", help="Start simulator monitoring")
    mon.add_argument("--db", default="monitor.db", help="SQLite database path")
    mon.add_argument(
        "--interval",
        type=int,
        default=5,
        help="Housekeeping interval (1-10 seconds)",
    )

    rep = sub.add_parser("replay", help="Replay recorded measurements from simulator")
    rep.add_argument("--db", default="monitor.db", help="SQLite database path")

    args = parser.parse_args()

    if args.command == "run":
        interval = max(1, min(10, args.interval))
        monitor(args.db, interval)
    elif args.command == "replay":
        replay(args.db)


if __name__ == "__main__":
    main()
