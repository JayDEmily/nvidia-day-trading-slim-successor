# 2026-04-03_GATE182_CANONICAL_IV_UNIT_CONTRACT

## Purpose

Freeze one canonical implied-volatility unit contract and stop standalone options-context evaluation from diverging from the real-data path because of mixed decimal-versus-percent inputs.

## What changed

- added `src/nvda_desk/schemas/options_units.py` as the schema-ingress normalisation boundary
- normalised IV-carrying schema fields in `src/nvda_desk/schemas/dataset.py` and `src/nvda_desk/schemas/cognition.py` to decimal-fraction semantics
- moved options-flow thresholds in `src/nvda_desk/services/options_flow_context.py` to the decimal-fraction contract
- aligned `tests/test_options_flow_context.py` to the same decimal-fraction contract used by the real-data path

## Definition-of-done evidence

- percent-style ingress now normalises to decimal fraction at schema boundary
- decimal-style and percent-style payloads classify identically after normalisation
- standalone tests no longer encode a second hidden IV unit system

## Proof surfaces

- `tests/test_gate182_options_iv_contract.py`
- `tests/test_options_flow_context.py`
