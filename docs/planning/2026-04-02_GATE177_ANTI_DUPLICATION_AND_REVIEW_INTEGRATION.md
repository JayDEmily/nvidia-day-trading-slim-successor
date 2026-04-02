Status: complete on `work/gate-171-master-child-parallel-risk-integration-pack-20260402`; Gate 178 is now the active gate
# Gate 177 — Anti-Duplication Semantics and Lean Review Integration

## What closed

Gate 177 is complete on `work/gate-171-master-child-parallel-risk-integration-pack-20260402`.

The master repo now implements the first bounded runtime slice of the child planning law for:
- environmental-weather versus candidate-specific split;
- inspectable fragility dimensions;
- descriptive anti-duplication semantics;
- and lean review integration.

This implementation keeps the lane descriptive and candidate-aware. It does **not** make the lane an arbiter or a hidden second caution engine.

## Runtime semantics added

The lane packet now carries `candidate_audit_surface` inside `src/nvda_desk/schemas/parallel_risk.py` and populates it in `src/nvda_desk/services/parallel_risk_lane.py`.

That surface preserves:
- whether the lane is operating in environmental-only mode or candidate-specific mode;
- active family/setup identifiers when a candidate exists;
- environmental-weather carry-through from the market/options layer;
- inspectable fragility dimensions;
- bounded expression-posture consequence classes;
- and one anti-duplication primary binding point plus descriptive secondary reads.

## Environmental weather versus candidate-specific audit

Gate 177 now implements the split explicitly.

### Environmental weather only

When no execution candidate exists, the lane remains active but only in environmental mode.
It does not invent a candidate-specific consequence merely to look busy.

### Candidate-specific audit

When a candidate exists, the lane may now describe bounded action-shape consequences such as:
- `not_at_all`
- `wait_or_defer`
- `smaller`
- `normal`
- `reshape`
- `hedge_required`

Those consequences remain descriptive and diagnostic inside the lane. They do not replace the serial spine or final-risk ownership.

## Fragility dimensions implemented

Gate 177 now preserves a first inspectable set of lane fragility dimensions:
- structural fragility;
- dependency fragility;
- event fragility;
- translation fragility;
- timing fragility;
- carry fragility;
- execution fragility.

The implementation remains bounded and explainable rather than collapsing them into one scalar.

## Anti-duplication law implemented

Gate 177 now preserves one explicit anti-duplication surface:
- `anti_duplication_primary_binding_point`
- `descriptive_secondary_reads`
- `duplicate_caution_suppressed`

This keeps the lane from pretending it newly owns a caution family that is already primarily bound elsewhere in the serial spine.

## Lean review integration implemented

Gate 177 now integrates the lane into review in the leanest possible way:
- `review_packet["parallel_risk_lane"]`
- `review_packet["parallel_risk_lane_summary"]`

No DMP v2 schema-core redesign is claimed.
No new eighth stage is introduced.
No second review universe is created.

## Explicit non-goals preserved

Gate 177 does **not**:
- implement arbiter/final-veto logic;
- duplicate Gate 167 non-risk-lane caution ownership;
- or redesign DMP v2 schema-core.

## Receipt

- branch: `work/gate-171-master-child-parallel-risk-integration-pack-20260402`
- start commit: `1336a9a`
- closing proof command: `python -m pytest -q tests/test_gate163_ownership_output_coefficient_and_anti_duplication_law.py tests/test_gate171_master_child_parallel_risk_integration_pack_planning.py tests/test_gate177_parallel_risk_anti_duplication_and_review_integration.py`
- observed result: `passed`
