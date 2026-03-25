# T1 Desk Legacy Page Map

Source: `My tier 1 desk Lol not GS (1).pdf`  
Purpose: page-linked topic map for structured extraction.

## High-confidence topic ranges

### Pages 1-6 - Pre-open ladder validation and Module 041
- IBKR volatility graphs and options structure are used to validate a proposed NVDA buy ladder.
- Explicit formalisation of **Module 041: Strategic Ladder Validator (SLV)**.
- Subcomponents include strike pressure mapping, volatility-envelope fit, fill-probability estimation, and participant-pressure logic.
- This is the cleanest explicit module definition in the document.

### Pages 10-15 - Volatility sentiment and macro-micro filter
- **Module 42: Volatility Sentiment Index (VSI)** appears as a dynamic sentiment / aggression filter.
- Inputs include VXX move, VIX term structure, implied-volatility change, and macro shock posture.
- Useful as a volatility-state gating or sizing concept, not as raw data.

### Pages 25-70 - Live ladder management, options pressure, and first session-phase thinking
- Large amount of screenshot-driven options interpretation around active ladder levels.
- Repeated use of put pressure, call decay, IV level, and distance-to-VWAP for execution logic.
- First explicit intraday phase reasoning appears:
  - open disorder,
  - VWAP anchoring,
  - structured repricing,
  - drift / fade windows.

### Pages 68-72 - Session clock becomes explicit
- Pages in this range lay out a more formal intraday actor/phase model.
- Distinguishes open chaos, early VWAP anchoring, institutional repricing, lunch drift, and later-session behaviour.
- Strong candidate source range for a formal session-clock feature family.

### Pages 95-106 - Time-of-day market structure refinement
- Session segmentation is restated more cleanly:
  - equilibrium tests,
  - midday compression,
  - post-lunch drift,
  - power hour setup,
  - dealer unwind / gamma ramp.
- Useful for phase-aware weighting and replay segmentation.

### Pages 156-159 - Overfitting, false positives, and evaluation method
- Explicit guidance on:
  - rolling walk-forward / expanding-window backtests,
  - false-positive handling,
  - parameter optimisation,
  - regime-specific validation.
- Valuable as doctrine for `TESTING_AND_PROMOTION`, not as market alpha.

### Pages 200-220 - Diagnostic clusters and module-stack design
- The document becomes more systematic about:
  - OBV/VI combo flow confirmation,
  - compression regime cluster,
  - options behaviour cluster,
  - execution and laddering cluster,
  - cross-cluster synergies,
  - adaptive macro overlays.
- Pages 218-220 are especially useful for module/feature harvesting.

### Pages 258-340 - High-volatility tariff / macro week and “sit out with structure”
- Macro-volatility environment dominates the read.
- Strong doctrine around:
  - not forcing trades in broken conditions,
  - letting repricing settle,
  - using VIX/VVIX and macro state as filters rather than theatre.
- Pages 330+ include manual Greek modelling from screenshot-derived options data; useful as a cautionary example and possible feature seed, but requires recomputation.

### Page 338 - “Post-It board” and guardrail doctrine
- This page is particularly useful because it lists future experiments directly:
  - VIX/VVIX crossover and slope modeling,
  - overlay filtering,
  - yield-curve steepening,
  - IV-rank vs IV-percentile timing,
  - time-to-profit drift,
  - ADR delta divergence,
  - put-ladder rationality vs call decay.
- Also states philosophical guardrails:
  - do not trade like retail,
  - do not overfit,
  - track entropy before acting,
  - build systems,
  - wait when uncertainty dominates.

### Pages 539-560 - Post-weekend structure, Asia open, and pre-market carry logic
- Rich source range for:
  - post-event vol collapse / IV-HV divergence,
  - retail bleed vs desk absorption,
  - Asia-market precursor context,
  - pre-market carry / overnight planning,
  - what to hold overnight and why.

### Pages 620-636 - Two-brain architecture and memory design
- Explicit split between:
  - GPT layer for narrative and memory,
  - Python layer for deterministic execution logic.
- Discusses how memory should be stored, session-awareness, and structured engine outputs.
- This range maps directly to the repo’s current research/runtime split.

### Pages 655-658 - O1-briefing and next-week framing
- Captures a late-stage attempt to brief a stronger reasoning model.
- Useful mainly as:
  - evidence of the operator workflow,
  - a reminder that the project was moving toward better briefing discipline,
  - not as a direct runtime design source.

## Confidence notes

### High confidence
- Explicit module names and descriptions.
- Directly stated feature candidates and guardrails.
- Session-clock concepts stated repeatedly.
- Evaluation-method guidance.

### Medium confidence
- Screenshot-derived option reads and macro overlays.
- Market-state interpretations based on options pressure and IV/skew.
- Overnight posture logic.

### Low confidence until recomputed
- Manually reconstructed Greeks.
- Any hard numeric threshold proposed conversationally without a deterministic formula trail.
- Assertions that a module was “in the stack”, “wired”, “committed”, or otherwise already software-real.
