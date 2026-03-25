# Strategic Ladder Validator (SLV) — Promotion Plan

Status: planned
Source: legacy module `legacy-module-001`

## Purpose

Validate a proposed NVDA entry ladder before orders remain active. The aim is not to predict direction perfectly; the aim is to prevent structurally bad ladders from reaching the runtime.

## Why it survives

This is one of the cleanest legacy ideas because it is bounded, pre-trade, and falsifiable. It is a sanity gate, not an oracle.

## Proposed module class

`execution` with strong interaction with `risk`

## Proposed typed outputs

- `ladder_validity_score: float`
- `overall_decision: enum[accept, adjust, reject]`
- `rung_decisions: list[enum[keep, adjust, drop]]`
- `reasons: list[str]`
- `confidence: enum[low, medium, high]`

## Required inputs

### Raw or canonical upstream
- current NVDA spot / pre-market price
- bounded NVDA option strip
- option bid/ask/last/volume/open interest
- session clock phase

### Derived features required first
- `iv_hv_divergence_by_expiry`
- `oi_cluster_width`
- `distance_to_vwap`
- `put_ladder_rationality_vs_call_decay`
- `fill_plausibility_score` (new)
- `strike_pressure_map` (new)

## What must be recomputed

The legacy maths around IV/HV and ladder rationality should be recomputed from canonical inputs. Do not reuse screenshot-era numbers as direct truths.

## Runtime boundary

SLV should not place orders. It should only validate or downgrade a proposed ladder and emit a structured decision that the runtime can consume.

## Research boundary

GPT/research may propose the ladder and explain the context. SLV only judges the ladder against deterministic features.

## Minimum replay design

Replay one historical pre-open + first 30-minute window and ask:
- did the accepted ladder get touched/fill plausibly?
- did rejected ladders avoid poor entries?
- did adjusted ladders outperform the original proposal?

## Pass/fail criteria for implementation readiness

Implementation-ready when:
- all required inputs have typed sources;
- rung-level decisions are deterministic;
- replay can compare original versus adjusted ladder outcomes;
- reasons are generated from structured conditions, not prose improvisation.

## First implementation slice

Do not build full ladder optimisation.
Build only:
1. accept / adjust / reject;
2. per-rung keep / adjust / drop;
3. top 3 deterministic reasons.

## Risks

- overfitting to old options heuristics;
- pretending fill plausibility is more precise than it is;
- mixing discretionary narrative with deterministic validation.

## Recommendation

Promote to typed-contract design next. High-value candidate.
