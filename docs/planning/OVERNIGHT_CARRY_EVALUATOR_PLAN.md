# Overnight Carry Evaluator — Promotion Plan

Status: planned
Source: legacy module `legacy-module-007`

## Purpose

Produce a structured recommendation on whether to carry exposure overnight or into the weekend, whether to keep orders active, and what maximum overnight exposure is justified.

## Why it survives

This addresses a real hole in the current repo. The project already reasons about intraday states, but it does not yet have a formal carry artefact.

## Proposed module class

`sizing` with interaction with `risk`

## Proposed typed outputs

- `carry_recommendation: enum[increase, hold_small, flatten, block]`
- `overnight_exposure_pct: float`
- `keep_orders_active: bool`
- `rationale_codes: list[str]`
- `review_required: bool`

## Required inputs

### End-of-day / close state
- closing spot state
- distance to VWAP at close
- session clock end-phase
- realised vol state

### Volatility and option state
- VIX/VVIX state
- near-term option structure summary
- IV crush / unwind state
- gamma wall / magnet summary if available

### Cross-market / precursor context
- Asia precursor composite
- USDJPY / yields risk context
- next-session event calendar state

### Account / risk state
- current positions
- open orders
- gross exposure
- risk budget remaining

## Research boundary

GPT/research can produce narrative context and propose why carry might matter. The evaluator should only emit a structured recommendation from typed inputs.

## Minimum replay design

Compare three paths over historical sessions:
1. flatten at close;
2. hold baseline exposure;
3. follow carry evaluator recommendation.

Measure:
- gap P&L;
- overnight drawdown;
- open slippage / adverse excursion;
- event-week versus normal-week behaviour.

## First implementation slice

Do not start with weekend complexity and three dozen conditions.
Start with:
1. normal overnight only;
2. one exposure percentage recommendation;
3. keep/cancel orders boolean;
4. explicit review-required flag.

## Pass/fail criteria for implementation readiness

Implementation-ready when:
- all required state can be expressed from current/planned layers;
- replay can compare carry-versus-flat outcomes;
- output is clearly advisory to risk/runtime rather than direct order placement;
- weekend/event extensions are explicitly deferred.

## Risks

- treating Asia/context proxies as stronger than they are;
- confusing narrative conviction with overnight edge;
- silently mixing intraday alpha with carry logic.

## Recommendation

Promote after session clock planning, but before broker integration. High-value artefact for the research-to-runtime bridge.
