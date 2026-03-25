# T1 Desk Legacy Value Capture

Source: `My tier 1 desk Lol not GS (1).pdf`  
Status: extracted as doctrine and backlog material, not runtime truth

## Executive read

This PDF is one of the strongest legacy corpora in the NVIDIA project history.

It is valuable because it contains:
- real screenshot-derived market observations,
- early module invention,
- a richer intraday phase model,
- explicit coefficient / weighting / validation thinking,
- overnight posture logic,
- and a late-stage architecture split between GPT reasoning and deterministic Python execution.

It is **not** valuable as direct implementation truth.
The document repeatedly uses conversational “done / added / wired” language that does not prove software existed.

The right use is to treat it as:
- a legacy doctrine source,
- a module and feature backlog source,
- and a failure-pattern source.

## What survives cleanly

### 1. Strategic Ladder Validator survives
The strongest explicit module concept in the whole document is **Module 041: Strategic Ladder Validator (SLV)**.

Its durable thesis is:
- do not place or keep a ladder just because price “looks cheap”;
- validate ladder levels against actual option-pressure structure, IV/HV context, pre-market distance, and expected fill plausibility.

Why it survives:
- it is bounded,
- it is pre-trade,
- it fits the current runtime’s deterministic design,
- and it helps stop dumb fills rather than force a directional prediction.

How it maps now:
- repo layer: `derived_features` + `execution_records`
- module class: `execution`
- future role: pre-open validation / ladder sanity gate

### 2. The session clock absolutely survives
A very large amount of durable value in the PDF is the recognition that the trading day is not homogeneous.

The document repeatedly separates the day into behaviourally distinct zones:
- open chaos / disorder,
- early VWAP anchoring,
- institutional repricing,
- transition creep,
- lunch fade / compression,
- post-lunch drift,
- power hour,
- dealer unwind / gamma ramp.

Why it survives:
- it is a feature family, not a fragile prediction;
- it can improve both replay and operator-facing interpretation;
- it matches how real intraday behaviour changes over the day.

How it maps now:
- repo layer: `derived_features`
- future role: first-class `session_clock_state` and `phase_id` features

### 3. Volatility-state overlays survive
The PDF gives repeated weight to:
- VIX,
- VVIX,
- VXX,
- term-structure shifts,
- IV/HV divergence,
- and macro-volatility environment.

The valuable insight is not “vol predicts price”.
The valuable insight is:
- volatility state changes whether a setup is tradeable,
- changes holding-period logic,
- and changes whether an entry ladder is even sane.

How it maps now:
- repo layer: `canonical_market` + `derived_features`
- future role: volatility-state filter, sizing bias, and no-trade veto input

### 4. Module-stack thinking survives
The document is already thinking in the right shape:
- modules have coefficients,
- modules interact,
- modules can be promoted or demoted,
- no single signal should run the whole show,
- false positives and cross-cluster contradictions matter.

This is one of the best signs that the project direction was not wrong.
It was already moving toward:
- formal module stacks,
- attribution,
- and controlled promotion.

How it maps now:
- repo layer: `research_artefacts` -> deterministic runtime
- future role: module registry backlog and replay/evaluation design

### 5. “Sit out with structure” survives
A strong recurring instinct in the PDF is that the right move is often to wait.

Not “wait because scared”.
Wait because:
- volatility regime is broken,
- repricing is incomplete,
- options structure is too noisy,
- macro event risk dominates the micro read,
- or signal density is too low.

This is worth preserving because it is adult desk behaviour, not retail FOMO theatre.

How it maps now:
- repo layer: `risk` and `research_artefacts`
- future role: veto modules, no-trade states, and operator workflow

### 6. Overnight posture logic survives
The PDF does not stay purely intraday.
It repeatedly reasons about:
- whether capital should stay engaged overnight,
- whether limit orders should remain active,
- whether Asia/pre-market conditions justify carry,
- and whether Friday setups justify Monday exposure.

This is still underdeveloped in the current repo and should become a first-class planning artefact.

How it maps now:
- repo layer: `research_artefacts` -> future deterministic carry planner
- future role: `overnight_planner` or `carry_candidate` artefact

### 7. The two-brain architecture survives
Pages 620-636 are particularly important because they show the legacy project already converging on the same split we have now frozen:
- GPT layer for narrative, timestamps, what-is-missing logic, and desk-style interpretation;
- Python layer for deterministic strategy logic once the field map is complete.

This confirms the present repo architecture is not a random invention.
It is the cleaned-up form of where the thinking was already going.

## What does **not** survive cleanly

### 1. Screenshot-native data handling
The document relies heavily on screenshots, OCR-like reconstruction, pasted ladders, and hand-built market tables.

That history is useful as provenance, but it is not how the current system should work.
The new architecture exists specifically to end this workflow.

### 2. Conversation reality
Statements like:
- “it’s in the stack”,
- “it’s committed”,
- “it’s wired”,
- “this engine now does X”
must be treated as conversational artefacts, not engineering proof.

### 3. Manually modelled Greeks without deterministic provenance
These passages are still useful as hypothesis generation, but they require recomputation before they become features or module inputs.

### 4. Over-attribution risk
The document sometimes reads options structure and macro context with more confidence than the evidence clearly warrants.
That does not make it useless.
It means the interpretation layer needs explicit humility and replay discipline.

## Highest-value extractions from this pass

### Explicit module candidates
1. Strategic Ladder Validator (SLV)
2. Volatility Sentiment Index (VSI)
3. OBV/VI combo flow confirmation as a candidate signal
4. Compression regime detector
5. Options-behaviour / gamma-wall framing logic
6. Macro adaptive weighting / state filter
7. Overnight carry evaluator
8. Asia-to-US precursor context filter

### Explicit feature candidates
1. VIX/VVIX crossover and slope
2. VIX term structure (9D/1M/3M)
3. IV rank vs IV percentile timing
4. IV-HV divergence by expiry
5. OI-cluster width and strike-pressure density
6. put-ladder rationality vs call decay
7. distance to VWAP
8. envelope-band width
9. CHOP / compression state
10. PPO-OBV contradiction
11. ADR delta divergence (NVDA vs SOXX vs QQQ)
12. yield-curve steepening / macro-pivot proxy
13. Asia precursor composite
14. time-to-profit drift after macro shocks

## What should happen next in the repo

### Planning artefacts
The following should exist after this pass:
- `docs/legacy/T1DESK_PAGE_MAP.md`
- `docs/legacy/T1DESK_FAILURE_PATTERNS.md`
- `backlog/legacy_module_backlog.jsonl`
- `backlog/legacy_feature_backlog.jsonl`

### Backlog promotion rule
Nothing from this PDF goes straight into runtime.
Everything first becomes:
1. backlog item,
2. typed contract,
3. replay candidate,
4. eval result,
5. only then promotion candidate.

## Bottom line

This document proves the project was already pointing in the right direction over a year ago.

The most durable ideas are:
- pre-open ladder validation,
- session-clock / phase-awareness,
- volatility-state overlays,
- module-stack weighting,
- no-trade discipline,
- overnight posture logic,
- and the GPT/Python two-brain split.

The value is real.
The packaging was the mess.
