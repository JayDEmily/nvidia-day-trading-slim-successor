# 2026-03-24 Context Scanner Contracts

Status: Active Gate-19 supporting note  
Authority: subordinate to the Gate-19 leaf and gate map.

This note freezes the Gate-19 context/scanner import rule.

## 1. Purpose

Gate 19 deepens the context layer **above** the shared substrate. It must keep provenance explicit and must not pretend the repo has already promoted imported scanners into approved execution logic.

## 2. Frozen Gate-19 order

1. `macro_signal_score`
2. `execution_context_score`
3. `vix_spread_detector`
4. `vol_corridor`
5. `options_behaviour_cluster`
6. `asia_precursor_context_filter`
7. `macro_adaptive_weighting_filter`
8. `engine_score`

## 3. Binding rules

- Every Gate-19 contract must cite its upstream substrate or runtime dependencies explicitly.
- `execution_context_score` and `engine_score` must carry readable upstream provenance; they must not be presented as approved live-trading engines.
- Gate 19 may proxy from the existing deterministic runtime where needed, but it must not invent hidden broker feeds, side-state, or a second scoring stack.
- Gate 19 may aggregate prior Gate-19 contracts, but that aggregation must stay explicit in dependency fences and upstream slug lists.

## 4. Non-goals

Gate 19 must not:

- widen into execution-chain imports;
- relabel imported scanners as approved;
- rewrite the four live playbooks;
- hide missing live market inputs behind fake readiness labels.
