from pathlib import Path

import pytest

from gmios.config import load_yaml, validate_all, validate_watchlist
from gmios.models import ConfigValidationError, PortfolioConfig


def test_all_yaml_loads() -> None:
    configs = validate_all(Path(__file__).parents[1] / "config")
    assert len(configs) == 6


def test_invalid_priority_errors() -> None:
    value = {"macro": {"us": [{"id": "x", "name": "X", "priority": "urgent", "category": "rates"}]}}
    with pytest.raises(ConfigValidationError, match="Invalid priority"):
        validate_watchlist(value)


def test_portfolio_targets_must_sum_to_one() -> None:
    with pytest.raises(ConfigValidationError, match="sum to 1"):
        PortfolioConfig.from_dict({"targets": {"cash": 0.8}, "rules": {"auto_trade": False}})


def test_load_yaml_returns_mapping(tmp_path: Path) -> None:
    path = tmp_path / "ok.yaml"
    path.write_text("key: value\n", encoding="utf-8")
    assert load_yaml(path) == {"key": "value"}
