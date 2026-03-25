# 02_OPERATING_MODEL

## What this repo builds

A single-operator market-state and playbook platform for NVIDIA day trading.

The current repo has three parts:
1. **market-state memory** — durable facts outside the chat thread;
2. **research cockpit** — human-directed analysis and drafting;
3. **deterministic runtime** — approved modules only, with posture, risk, ledger, replay, and review.

## Human / GPT / runtime split

### Human
- chooses the research direction;
- decides what matters;
- approves promotion, pause, retirement, and live eligibility;
- owns policy values;
- remains the binding desk lens for all runtime interpretation.

### GPT
- reads compact retrieved state;
- compares regimes and analogous sessions;
- drafts notes, hypotheses, module specs, and documentation;
- critiques overfitting and missing controls;
- helps explain post-trade outcomes.

### Deterministic runtime
- evaluates approved module stacks;
- applies posture, vetoes, and risk policy;
- records orders, fills, vetoes, blocks, and attribution;
- runs replay, backtest, and paper paths.

## Daily operating loop

```text
prepare market picture
  -> inspect market state and prior analogues
  -> discuss candidate setups with GPT
  -> draft or revise module artefacts
  -> code / gate deterministic module changes
  -> replay / backtest / paper evaluate
  -> promote, revise, or retire
  -> review post-trade attribution
```

## Desk Cognition Grammar

The runtime processes decisions in this order:

1. **temporal context** — what time it is, what happened recently, what event windows are active, and what expiry proximity matters now;
2. **market regime context** — beta, breadth, rates, FX, volatility regime, concentration, and cross-asset state;
3. **options and flow context** — term structure, skew, gamma pressure, implied-move budget, and flow-derived tension;
4. **posture and risk permission** — inventory state, fresh deployable capital, block/derisk/allow, and no-overnight rules;
5. **playbook eligibility** — which playbooks are eligible, ineligible, or watch-only;
6. **expression and execution** — laddering, sizing, hedge rules, exits, and execution shape;
7. **review and explanation** — reason packets, conflicts, attribution, and replay reconstruction.

This order is binding.

## Current operating surfaces

The current repo exposes:
- FastAPI routes for market-state retrieval, research notes, module registry, promotions, evaluation logging, risk decisions, execution records, broker paper flow, and review packets;
- deterministic services for temporal context, market regime, options/flow, posture/risk, playbook eligibility, execution expression, review explanation, and replay comparison;
- local development entrypoints through the Makefile.

No MCP adapter is part of the current repo state.

## Data-layer taxonomy

### `raw_vendor`
Vendor-shaped intake, including precomputed vendor fields.

### `canonical_market`
Normalised facts independent of vendor quirks.

### `derived_features`
Computed state such as VWAP, realised vol, opening-range metrics, options summaries, and regime tags.

### `research_artefacts`
Human and GPT outputs: notes, module specs, evaluation artefacts, and promotion decisions.

### `execution_records`
Orders, fills, vetoes, risk blocks, capital state, and attribution.

## Module model

Modules are formal desk behaviours, not free-form prompts.

The canonical module classes are defined by `src/nvda_desk/schemas/module.py`:
- `signal`
- `veto`
- `sizing`
- `execution`

The canonical module statuses are defined by `src/nvda_desk/schemas/module.py`:
- `planned`
- `draft`
- `coded`
- `backtested`
- `paper_candidate`
- `approved`
- `retired`

A module is never promoted directly from a good conversation.

## What this repo is not

- not an HFT engine;
- not a one-shot market predictor;
- not a giant OMS/EMS clone;
- not a prompt-only trading toy;
- not a system where the chat thread acts as durable memory.
