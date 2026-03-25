# 2026-03-24 Execution Planning Contracts

Status: Active Gate-21 supporting note  
Authority: subordinate to the Gate-21 leaf and gate map.

This note freezes the Gate-21 execution-planning rule.

## 1. Frozen Gate-21 order

1. `broker_adapter`
2. `entry_planner`
3. `position_allocator`
4. `order_simulator`
5. `run_trading_bot`

## 2. Binding rules

- Every Gate-21 module must remain advisory-only and packet-serialisable.
- `broker_adapter` must stay fenced as a dry-run boundary. No live routing, credentials, acknowledgements, or daemon loop may appear here.
- `entry_planner`, `position_allocator`, and `order_simulator` may emit preview plans even when the current gate or temporal state would still veto live dispatch.
- `run_trading_bot` must remain a preview orchestration surface only. It may describe a dry-run dispatch state but must not imply a live bot loop.

## 3. Non-goals

Gate 21 must not:

- place or cancel real orders;
- invent broker callback state or fill acknowledgements;
- widen into cross-session lifecycle or review-chain work that belongs to Gates 22 and 23;
- relabel preview planning as approved runtime execution.
