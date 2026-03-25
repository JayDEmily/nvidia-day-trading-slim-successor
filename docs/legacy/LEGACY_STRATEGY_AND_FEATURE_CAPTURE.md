# Legacy strategy and feature capture from remaining documents

## Executive call
The remaining documents split cleanly:
- **Data-bearing**: `Options Data CSV Output.pdf`, selected blocks in `of trading days below VWAP.pdf`
- **Doctrine / feature-bearing**: `Comprehensive Deep-Dive...pdf`, `NVDA GPT Framework Review.pdf`
- **Hybrid**: `of trading days below VWAP.pdf` because it mixes data, modules, and forensic critique

This document captures only the surviving strategy, feature, and module value.

## Strongest feature families

### 1. Session clock / phase-aware weighting
**Source pages**
- `Comprehensive Deep-Dive...pdf` 9-13
- `Comprehensive Deep-Dive...pdf` 50
- `NVDA GPT Framework Review.pdf` 16-17

**What survives**
- the day is explicitly segmented into distinct behavioural phases;
- module weighting should change by phase;
- later evaluation should group outcomes by phase, not just by date or PnL.

**Repo mapping**
- `derived_features`: session clock phase fields, intraday phase transitions
- `research_artefacts`: daily desk summary
- `execution_records`: replay attribution by phase

### 2. Overnight / carry planning
**Source pages**
- `Comprehensive Deep-Dive...pdf` 15-18
- `Comprehensive Deep-Dive...pdf` 457
- `NVDA GPT Framework Review.pdf` 12, 14

**What survives**
- overnight posture should be its own artefact, not just an afterthought;
- positioning depends on delta, gamma, vega, liquidity, and macro/event state;
- human constraints (sleep cycle, inability to monitor re-entry) belong in the planner.

**Repo mapping**
- `derived_features`: overnight context inputs
- `research_artefacts`: overnight carry recommendation / rationale
- later candidate module: overnight carry evaluator

### 3. Asia / Europe precursor context
**Source pages**
- `Comprehensive Deep-Dive...pdf` 157-177
- `Comprehensive Deep-Dive...pdf` 491-498
- `of trading days below VWAP.pdf` 165-175
- `NVDA GPT Framework Review.pdf` 17

**What survives**
- use Nikkei / Hang Seng / Europe / futures / bond yields as bounded context inputs, not infinite macro soup;
- precursor markets should influence pre-open conviction and overnight-risk posture;
- this is a feature family first, not a standalone strategy.

**Repo mapping**
- `derived_features`: Asia / Europe precursor composite
- `research_artefacts`: pre-open brief
- risk overlay / carry overlay later

### 4. Composite signal scoring
**Source pages**
- `Comprehensive Deep-Dive...pdf` 435-436
- `Comprehensive Deep-Dive...pdf` 456-457

**What survives**
- scoring should aggregate module outputs, normalise them, and preserve reasoning logs;
- entry/exit logic should sit on top of that composite layer;
- the by-day summary-table format is a good artefact template.

**What does not survive**
- the “all wired / ready for live” language later in the document.

**Repo mapping**
- `research_artefacts`: scored desk brief
- later runtime/eval layer once real data is present

### 5. Macro filter as a low-complexity veto / weighting layer
**Source pages**
- `of trading days below VWAP.pdf` 60-65
- `NVDA GPT Framework Review.pdf` 10, 14, 17

**What survives**
- 3-5 binary high-signal macro flags are enough for v1;
- macro should modify trust in IV/VWAP logic, not replace it;
- explicit examples: VIX term state, 10Y move, 2s10s stress, SMH confirmation, Asia pulse.

**Repo mapping**
- `derived_features`: macro filter inputs
- `risk` / `research_artefacts`: go/no-go overlays

## Strongest module candidates not already captured
These are additions beyond the T1-desk extraction already in the repo.

### A. Gap Fill Bias Model
**Source pages**: `of trading days below VWAP.pdf` 222  
Purpose: determine whether open gaps tend to fill, extend, or chop based on recent gap behaviour, IV/HV trend, sector ETF context, and gamma-zone location.

### B. Volatility Regime Classifier
**Source pages**: `of trading days below VWAP.pdf` 222-223  
Purpose: classify rising / stable / compressing regimes from HV slope and IV/HV relation.

### C. Macro Volatility Confirmation Module
**Source pages**: `of trading days below VWAP.pdf` 224  
Purpose: distinguish macro-aligned volatility from isolated stock/event volatility.

### D. Sentiment Shock Filter
**Source pages**: `of trading days below VWAP.pdf` 221  
Purpose: detect overnight narrative shocks and suppress whipsaw overreaction when volume does not confirm.

### E. International Index Drift Scanner
**Source pages**: `NVDA GPT Framework Review.pdf` 5, 17  
Purpose: formalise precursor-market drift into a reusable module/backlog item.

## Explicit discard / caution list
- `NVDA GPT Framework Review.pdf` 36-43: identity/career drift, not repo value.
- `Comprehensive Deep-Dive...pdf` 545-546: implementation fantasy, not evidence.
- Any “we’ve built it / it’s wired” claim inside these PDFs remains docs-only unless independently verified in code.
