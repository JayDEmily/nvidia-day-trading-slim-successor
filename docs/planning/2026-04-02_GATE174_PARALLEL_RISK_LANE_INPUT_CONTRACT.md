# 2026-04-02_GATE174_PARALLEL_RISK_LANE_INPUT_CONTRACT

## Purpose

Implement the first typed runtime contract for the co-resident independent parallel risk lane, preserving the seven-stage serial spine and lawful-read boundary.

## Runtime surfaces added here

- `src/nvda_desk/schemas/parallel_risk.py`
- `src/nvda_desk/services/parallel_risk_lane.py`
- `src/nvda_desk/services/cognition_runtime.py` integration seam
- `src/nvda_desk/schemas/cognition.py` review-input seam for later downstream use

## What the contract does now

- creates a `ParallelRiskLanePacket` immediately after temporal evaluation
- records approved invariant reads available from session start
- records lawful stage-output read status for all serial stages
- marks temporal as the only stage output used in Gate 174-175
- preserves explicit notes that the lane is co-resident, not `step_1_1`, not `step_8`, and not an arbiter

## What the contract does not do yet

- no final arbiter behaviour
- no candidate-specific fragility logic yet
- no options/dislocation logic yet
- no review-surface emission beyond lawful carriage into runtime inputs

## Lawful-read boundary frozen here

- direct invariant reads: allowed from session start
- lawful stage-output reads: allowed only after stage production
- grammar order, stage ownership, raw market facts, baseline coefficient authority, and lineage remain invariant surfaces rather than lane-owned mutable state
