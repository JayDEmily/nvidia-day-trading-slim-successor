Status: complete on `work/gate-171-master-child-parallel-risk-integration-pack-20260402`; Gate 177 is now the active gate
# Gate 176 — Market, Options, Dependency, and Dislocation Implementation

## What closed

Gate 176 is complete on `work/gate-171-master-child-parallel-risk-integration-pack-20260402`.

The master repo now implements the first bounded runtime slice of the child planning law for:
- broader-market and sector-weather reads;
- options-table translation reads;
- an `active enough to matter now` dependency filter;
- and the inspectable distinction between `dislocation_risk`, `justified_repricing`, and `impairment_risk`.

This implementation remains descriptive and candidate-aware. It does **not** become a second playbook engine.

## Runtime surfaces added

The lane packet now carries `market_translation_surface` inside `src/nvda_desk/schemas/parallel_risk.py` and populates it in `src/nvda_desk/services/parallel_risk_lane.py`.

That surface preserves:
- slower background context from the regime output;
- faster translation context from the options-flow output;
- a bounded dependency activation state;
- a boolean `active_enough_to_matter_now` filter;
- a dislocation-state classification;
- and a compact environmental-weather label.

## Mapping law implemented

### Slower background context

Gate 176 now reads and preserves bounded slower-weather surfaces from the serial regime stage, including:
- volatility regime;
- breadth state;
- sector leadership;
- rates and FX regime notes;
- signal conflict / cross-asset pressure.

### Fast translation context

Gate 176 now reads and preserves bounded faster translation surfaces from the serial options-flow stage, including:
- gamma state;
- dealer pressure;
- options-behaviour cluster;
- repeated snapshot state;
- pin progression state.

### Dependency activation filter

Gate 176 now implements a bounded `active enough to matter now` filter rather than treating every true dependency as live on every pass.

The filter is intentionally narrow. It activates only when the lane has one of:
- a live event family;
- destabilising gamma;
- elevated flow-tension pressure;
- non-aligned regime conflict;
- or material cross-asset pressure.

### Dislocation versus justified repricing versus impairment

Gate 176 now preserves three inspectable runtime classifications:
- `dislocation_risk`
- `justified_repricing`
- `impairment_risk`

This implementation keeps the child-planning principle intact: price action alone does not decide the category.

## Stage-read truth

The lane now records the following truthful stage-read changes:
- `temporal` remains the first lawful stage output used;
- `regime` is now read and marked `used`;
- `options_flow` is now read and marked `used`.

No other stage-read ownership changes are claimed in Gate 176.

## Explicit non-goals preserved

Gate 176 does **not**:
- implement arbiter logic;
- duplicate the deterministic playbook-selection engine;
- widen the live coefficient universe;
- or hide translation-state logic behind one opaque scalar.

## Receipt

- branch: `work/gate-171-master-child-parallel-risk-integration-pack-20260402`
- start commit: `1336a9a`
- closing proof command: `python -m pytest -q tests/test_gate162_market_options_dependency_and_dislocation_mapping.py tests/test_gate171_master_child_parallel_risk_integration_pack_planning.py tests/test_gate176_market_options_dependency_dislocation_runtime.py`
- observed result: `passed`
