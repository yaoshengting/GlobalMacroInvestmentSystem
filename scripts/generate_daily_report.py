"""Generate a dated daily report."""

import argparse

from gmios.cli import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    args = parser.parse_args()
    raise SystemExit(main(["daily-report", "--date", args.date]))

