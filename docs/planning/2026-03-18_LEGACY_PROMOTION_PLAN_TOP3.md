# Legacy Promotion Plan — Top 3 Candidates

Status: planning only. No runtime promotion performed in this pass.

## Purpose

This pass takes the highest-value extractions from `My tier 1 desk Lol not GS (1).pdf` and decides how they should enter the current repo without importing year-old conversational logic straight into runtime.

The three candidates selected for first promotion planning are:
1. Strategic Ladder Validator (SLV)
2. Session Clock Feature Family
3. Overnight Carry Evaluator

These were selected because they are the clearest durable survivors from the legacy corpus and they map cleanly onto the current architecture.

## Current phase versus next phase

### What this pass does
- freezes promotion plans;
- maps each item into repo layers;
- states the typed contracts required;
- states recomputation requirements;
- states the minimum replay/eval path required before coding.

### What this pass does **not** do
- add new database tables;
- add new FastAPI routes;
- add new runtime modules;
- add new derived-feature jobs;
- promote any item into `approved` status.

## Selection rationale

### 1. Strategic Ladder Validator
Chosen because it is the strongest bounded pre-trade module concept in the corpus. It helps decide whether a proposed entry ladder is sane before orders remain active.

### 2. Session Clock Feature Family
Chosen because it is not a fragile prediction. It is a durable way to describe intraday state, and it improves research, replay, and runtime weighting simultaneously.

### 3. Overnight Carry Evaluator
Chosen because it fills a real gap in the current repo. The existing architecture has room for it, but it is not yet formalised as a first-class artefact.

## Promotion doctrine

Every candidate must move through the same path:
1. planning doc;
2. typed contract proposal;
3. feature dependency map;
4. replay/eval design;
5. implementation ticket;
6. coding pass;
7. replay result;
8. paper-candidate decision.

Nothing skips from legacy corpus straight into runtime.

## Repo-layer mapping

### Strategic Ladder Validator
- `derived_features`: option-pressure, IV/HV divergence, distance-to-VWAP, fill-plausibility inputs
- `research_artefacts`: pre-open ladder validation note and structured decision
- `risk`: ladder veto or downgrade recommendation
- `execution_records`: downstream ledger recording if a ladder was blocked/adjusted/accepted

### Session Clock Feature Family
- `canonical_market`: session calendar / market hours reference only
- `derived_features`: phase ID and phase-aware descriptors
- `research_artefacts`: human-readable state summary
- `evals`: replay slicing, attribution by phase, phase-conditioned performance

### Overnight Carry Evaluator
- `derived_features`: closing state, volatility state, Asia precursor composite, option-state summary
- `research_artefacts`: carry recommendation artefact
- `risk`: carry veto / overnight exposure ceiling recommendation
- `evals`: overnight-vs-flat comparison and weekend/event conditioning

## Minimum output of the next implementation-facing pass

The next pass should produce:
- one typed contract proposal per candidate;
- one implementation ticket/checklist per candidate;
- one replay/eval design note per candidate;
- one machine-readable backlog file with promotion state `planned`.

## Stopping rule

Stop before coding if any of these remain ambiguous:
- the feature inputs are not expressible from current or planned data layers;
- the outputs are still conversational rather than typed;
- replay criteria are not defined;
- the item still mixes research judgement with deterministic runtime behaviour.

## Bottom line

We are now in selective promotion planning, not freeform brainstorming and not direct runtime population.
