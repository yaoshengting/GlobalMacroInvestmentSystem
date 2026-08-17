"""UTF-8 YAML loading and project configuration validation."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import yaml

from .models import ConfigValidationError, PortfolioConfig, WatchItem

LOGGER = logging.getLogger(__name__)
REQUIRED_CONFIGS = (
    "watchlist.yaml",
    "thresholds.yaml",
    "sources.yaml",
    "portfolio.example.yaml",
    "report_template.yaml",
)


def project_root() -> Path:
    """Return the repository root based on this installed source tree."""
    return Path(__file__).resolve().parents[2]


def load_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML mapping from *path* with actionable errors."""
    try:
        with path.open("r", encoding="utf-8") as stream:
            value = yaml.safe_load(stream)
    except OSError as exc:
        raise ConfigValidationError(f"Cannot read {path}: {exc}") from exc
    except yaml.YAMLError as exc:
        raise ConfigValidationError(f"Invalid YAML in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ConfigValidationError(f"Top level of {path} must be a mapping")
    return value


def validate_watchlist(value: dict[str, Any]) -> None:
    """Validate all macro watch items, including allowed priorities."""
    macro = value.get("macro")
    if not isinstance(macro, dict):
        raise ConfigValidationError("watchlist.macro must be a mapping")
    for region, raw_items in macro.items():
        if not isinstance(raw_items, list):
            raise ConfigValidationError(f"watchlist.macro.{region} must be a list")
        for raw_item in raw_items:
            if not isinstance(raw_item, dict):
                raise ConfigValidationError(f"Watch item in {region} must be a mapping")
            WatchItem.from_dict(raw_item)


def validate_all(config_dir: Path | None = None) -> dict[str, dict[str, Any]]:
    """Load and validate every version-controlled project YAML file."""
    directory = config_dir or project_root() / "config"
    loaded: dict[str, dict[str, Any]] = {}
    for filename in REQUIRED_CONFIGS:
        loaded[filename] = load_yaml(directory / filename)
    validate_watchlist(loaded["watchlist.yaml"])
    PortfolioConfig.from_dict(loaded["portfolio.example.yaml"])
    sections = loaded["report_template.yaml"].get("sections")
    if not isinstance(sections, list) or not all(isinstance(item, str) for item in sections):
        raise ConfigValidationError("report_template.sections must be a list of strings")
    hypotheses_path = directory.parent / "hypotheses" / "hypotheses.yaml"
    hypotheses = load_yaml(hypotheses_path)
    entries = hypotheses.get("hypotheses")
    if not isinstance(entries, dict) or not entries:
        raise ConfigValidationError("hypotheses.hypotheses must be a non-empty mapping")
    required = {
        "status",
        "confidence",
        "current_view",
        "supporting_evidence",
        "contrary_evidence",
        "falsification_conditions",
        "last_updated",
    }
    for hypothesis_id, hypothesis in entries.items():
        if not isinstance(hypothesis, dict):
            raise ConfigValidationError(f"Hypothesis {hypothesis_id} must be a mapping")
        missing = required.difference(hypothesis)
        if missing:
            raise ConfigValidationError(f"Hypothesis {hypothesis_id} missing fields: {sorted(missing)}")
    loaded["hypotheses/hypotheses.yaml"] = hypotheses
    LOGGER.info("Validated %d project YAML files", len(loaded))
    return loaded
