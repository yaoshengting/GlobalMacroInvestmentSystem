"""Command-line interface for validation and report generation."""

from __future__ import annotations

import argparse
import logging
from datetime import date
from pathlib import Path
from typing import Sequence

from .config import project_root, validate_all
from .models import ConfigValidationError
from .report_generator import generate_daily_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="gmios")
    parser.add_argument("--root", type=Path, default=project_root(), help="Project root")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate", help="Validate all YAML configuration")
    report_parser = subparsers.add_parser("daily-report", help="Generate a daily report skeleton")
    report_parser.add_argument("--date", required=True, type=date.fromisoformat, metavar="YYYY-MM-DD")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    args = build_parser().parse_args(argv)
    try:
        configs = validate_all(args.root / "config")
        if args.command == "validate":
            print(f"Validated {len(configs)} YAML files.")
        elif args.command == "daily-report":
            path = generate_daily_report(args.date, configs["report_template.yaml"], args.root)
            print(path)
    except (ConfigValidationError, RuntimeError) as exc:
        logging.getLogger(__name__).error("%s", exc)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

