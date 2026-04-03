# 2026-04-03_GATE184_FAIL_CLOSED_WEIGHTING

## Purpose

Stop dominant-strike and cluster inference from inheriting source row order when lawful weighting truth is absent.

## What changed

- added `_lawful_weight(...)` in `src/nvda_desk/services/real_data_loader.py`
- changed `_dominant_strike(...)` to return `None` when all lawful weights are absent or zero
- changed `_nearby_strike_clusters(...)` to ignore zero-weight quotes before ranking

## Definition-of-done evidence

- dominant strike is absent rather than fabricated when no lawful weight exists
- cluster order no longer flips merely because source rows were reordered

## Proof surfaces

- `tests/test_gate184_weighting_fail_closed.py`
- `tests/test_real_data_loader.py`
