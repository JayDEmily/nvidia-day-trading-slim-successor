# 2026-04-03_GATE185_SURFACE_ANCHOR_DIVERGENCE

## Purpose

Add one bounded derived feature for surface-anchor divergence versus live spot and carry it through the prepared snapshot, cognition input, and options-flow classification path.

## What changed

- added `surface_anchor_to_spot_pct` to the prepared/runtime and cognition contracts in `src/nvda_desk/schemas/dataset.py` and `src/nvda_desk/schemas/cognition.py`
- computed the feature from lawful near-spot call/put mid-price evidence in `src/nvda_desk/services/real_data_loader.py`
- threaded the feature through `src/nvda_desk/services/chain_to_cognition.py`
- added bounded output state in `src/nvda_desk/services/options_flow_context.py`
- regenerated the checked-in prepared runtime fixture pack so the lawful derived field is preserved on disk

## Definition-of-done evidence

- the feature is carried end-to-end as a bounded packet field rather than as prose or screenshot lore
- options-flow output can distinguish ordinary balanced flow from materially anchored-away surface conditions without creating a second engine

## Proof surfaces

- `tests/test_gate185_surface_anchor_divergence.py`
- `tests/test_real_data_loader.py`
