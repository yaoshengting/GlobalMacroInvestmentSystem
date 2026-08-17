# Global Macro Investment System

A long-running personal global-macro research, cognition-management, and investment decision-support system. It organizes facts and evidence into falsifiable hypotheses and human-reviewed execution ideas; it is not an automated trading system.

## Architecture

See [SYSTEM.md](SYSTEM.md) for the Information → Knowledge → Decision → Execution → Review pipeline. Configuration is under `config/`, durable views under `knowledge/` and `hypotheses/`, scenario responses under `playbooks/`, and generated artifacts under `reports/`.

## Quick start and environment

Requires Python 3.12+.

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -e ".[dev]"
.venv\Scripts\python -m gmios.cli validate
.venv\Scripts\python -m gmios.cli daily-report --date 2026-08-02
```

The validator checks all version-controlled project YAML, including the hypothesis registry. Alternatively run `python scripts/validate_config.py` or `python scripts/generate_daily_report.py --date YYYY-MM-DD` after installation.

## Directory guide

- `config/`: watch lists, calibrated-alert placeholders, sources, and report structure.
- `data/`: raw, processed, and cache areas; sensitive/raw inputs are ignored.
- `knowledge/`, `hypotheses/`: versioned cognition and falsifiable long-term views.
- `portfolio/`: sanitized examples; the actual portfolio stays local and ignored.
- `playbooks/`: conditional responses, never automatic orders.
- `research/`, `reports/`: source index, research, and generated reports.
- `src/gmios/`, `tests/`: application and tests.

## Git workflow and privacy

Create a focused branch, validate configs, run tests, inspect the diff, then commit locally. Never commit `.env`, credentials, raw/cache data, private positions, cookies, tokens, keys, identity details, or `portfolio/actual_portfolio.yaml`. No remote push is performed by initialization.

## Roadmap

The first phase is deliberately minimal. See [ROADMAP.md](ROADMAP.md) for evidence ingestion, provenance, hypothesis review, portfolio analytics, and reporting milestones.
