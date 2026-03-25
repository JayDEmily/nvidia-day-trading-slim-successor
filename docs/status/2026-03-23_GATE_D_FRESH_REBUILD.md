# 2026-03-23 Gate D Fresh Rebuild

## Purpose

Rebuild Gate D desk logic from scratch on a clean work branch rather than patching the earlier claimed completion.

## What changed

### Temporal
- rewrote `src/nvda_desk/services/temporal_context.py` to expose explicit `desk_window`, `event_window_state`, and `carryover_state`
- expanded `TemporalContextOutput` in `src/nvda_desk/schemas/cognition.py`
- added Gate-D temporal tests in `tests/test_temporal_context_runtime.py`

### Regime
- rewrote `src/nvda_desk/services/market_regime_context.py` to classify:
  - breadth vs concentration
  - rates regime
  - FX stress
  - regime conflict state
  - VIX/VVIX spread surface
- expanded `MarketRegimeContextOutput` in `src/nvda_desk/schemas/cognition.py`
- added Gate-D regime tests in `tests/test_market_regime_context.py`

### Options and flow
- rewrote `src/nvda_desk/services/options_flow_context.py` to promote:
  - live strike-cluster extraction
  - pin progression state
  - tenor-curve state
  - repeated snapshot evolution
  - VIX spread detector logic
  - IV-vs-RV-by-expiry logic
  - runtime behaviour clustering
- expanded options contracts in `src/nvda_desk/schemas/cognition.py`
- added Gate-D options tests in `tests/test_options_flow_context.py`

### Inventory, posture, playbooks
- rewrote `src/nvda_desk/services/posture_risk.py` to make inventory posture, thesis state, fresh-vs-inventory state, and signal conflict explicit
- rewrote `src/nvda_desk/services/playbook_eligibility.py` around four Gate-D families:
  - `continuation_ladder`
  - `negative_gamma_flush`
  - `pin_reversion`
  - `compression_breakout`
- added explicit no-trade vetoes, watch-only, and probe-only surfaces
- added Gate-D posture/playbook tests in `tests/test_posture_risk_and_playbook.py`

### Execution and review
- rewrote `src/nvda_desk/services/execution_expression.py` so execution shape, scaling plan, invalidation reasons, and exit reasons vary by playbook family
- rewrote `src/nvda_desk/services/review_explanation.py` to emit signal conflict density, contradiction packets, and module attribution
- expanded execution/review contracts in `src/nvda_desk/schemas/cognition.py`
- added Gate-D runtime integration tests in `tests/test_execution_review_runtime.py`

## Validation
- `.venv/bin/python -m pytest -q` → `81 passed`
- `make check` → `ruff` clean, `mypy` clean, `81 passed`

## Branch and merge
- branch: `work/gate-d-fresh-rebuild-20260323`
- merged back to `main` after validation
