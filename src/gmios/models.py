"""Typed configuration models and domain validation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class ConfigValidationError(ValueError):
    """Raised when configuration violates a system invariant."""


VALID_PRIORITIES = frozenset({"critical", "high", "medium", "low"})


@dataclass(frozen=True, slots=True)
class WatchItem:
    id: str
    name: str
    priority: str
    category: str

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "WatchItem":
        try:
            item = cls(
                id=str(value["id"]),
                name=str(value["name"]),
                priority=str(value["priority"]),
                category=str(value["category"]),
            )
        except KeyError as exc:
            raise ConfigValidationError(f"Watch item missing field: {exc.args[0]}") from exc
        if item.priority not in VALID_PRIORITIES:
            raise ConfigValidationError(
                f"Invalid priority {item.priority!r} for {item.id}; expected one of {sorted(VALID_PRIORITIES)}"
            )
        return item


@dataclass(frozen=True, slots=True)
class PortfolioConfig:
    targets: dict[str, float]
    rules: dict[str, Any]

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "PortfolioConfig":
        raw_targets = value.get("targets")
        if not isinstance(raw_targets, dict) or not raw_targets:
            raise ConfigValidationError("Portfolio targets must be a non-empty mapping")
        targets = {str(key): float(weight) for key, weight in raw_targets.items()}
        if any(weight < 0 or weight > 1 for weight in targets.values()):
            raise ConfigValidationError("Portfolio target weights must be between 0 and 1")
        if abs(sum(targets.values()) - 1.0) > 1e-9:
            raise ConfigValidationError(f"Portfolio target weights must sum to 1, got {sum(targets.values()):.6f}")
        rules = value.get("rules", {})
        if not isinstance(rules, dict):
            raise ConfigValidationError("Portfolio rules must be a mapping")
        if rules.get("auto_trade") is not False:
            raise ConfigValidationError("auto_trade must explicitly be false")
        return cls(targets=targets, rules=rules)

