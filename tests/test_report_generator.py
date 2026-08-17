from datetime import date
from pathlib import Path

from gmios.report_generator import generate_daily_report


def test_daily_report_generated_to_correct_directory(tmp_path: Path) -> None:
    template = {"sections": ["Cognition Update", "Investment Execution"], "placeholder": "Pending."}
    output = generate_daily_report(date(2026, 8, 2), template, tmp_path)
    assert output == tmp_path / "reports" / "daily" / "2026-08-02.md"
    content = output.read_text(encoding="utf-8")
    assert "## Cognition Update" in content
    assert "## Investment Execution" in content

