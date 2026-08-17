"""Generate evidence-ready daily report skeletons."""

from __future__ import annotations

import logging
from datetime import date
from pathlib import Path
from typing import Any

LOGGER = logging.getLogger(__name__)


def render_daily_report(report_date: date, template: dict[str, Any]) -> str:
    """Render a complete Markdown report without inventing observations."""
    title = str(template.get("title", "Daily Global Macro Report"))
    sections = template.get("sections", [])
    placeholder = str(template.get("placeholder", "No verified observations recorded."))
    lines = [f"# {title} — {report_date.isoformat()}", "", "> Draft skeleton. Verify facts and cite sources before forming judgments.", ""]
    for section in sections:
        lines.extend((f"## {section}", "", placeholder, ""))
    return "\n".join(lines)


def generate_daily_report(
    report_date: date,
    template: dict[str, Any],
    output_root: Path,
) -> Path:
    """Write the daily report to reports/daily/YYYY-MM-DD.md."""
    daily_dir = output_root / "reports" / "daily"
    daily_dir.mkdir(parents=True, exist_ok=True)
    destination = daily_dir / f"{report_date.isoformat()}.md"
    try:
        destination.write_text(render_daily_report(report_date, template), encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"Unable to write report {destination}: {exc}") from exc
    LOGGER.info("Generated daily report: %s", destination)
    return destination

