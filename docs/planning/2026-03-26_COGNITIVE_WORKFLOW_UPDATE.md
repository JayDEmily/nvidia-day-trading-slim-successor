# 2026-03-26 Cognitive Workflow Update

Status: planning update
Version: v1.0
Purpose: capture the clarified trader-thinking workflow agreed in thread form so it exists as a dated repo artefact rather than ephemeral chat context.
Authority boundary: this file does not replace `docs/01_NORMATIVE.md` through `docs/05_GUARDRAILS.md`. It records a clarified planning/workflow model that future gates and family-population work must respect.

## Why this update exists

The repo has already moved away from a thin, flat "seven playbooks" model. The missing piece was to write down the intended trader-thinking workflow clearly enough that future playbook, carry, vocabulary, and runtime work can populate the model without drifting its shape.

This update captures that shape.

## Core principle

The repo is modelling a deterministic cognition chain, not a fuzzy LLM planner.

The target behaviour is:

1. diagnose state
2. determine permission
3. generate plausible candidate families
4. select the live setup variant
5. select the execution expression
6. decide carry separately when the horizon is overnight/weekend/event carry
7. reconstruct why action or non-action occurred

## Cognitive workflow tree

### 0. Calendar / horizon gate

Before intraday reasoning begins, classify the evaluation horizon:

- normal trading day
- event day
- expiry week/day
- Friday into weekend
- out-of-hours carry context

The first branch decision is whether the system is evaluating:

- intraday deployment, or
- carry / overnight / weekend / event carry

Weekend is therefore a distinct carry-horizon problem, not just a late-session variant.

### 1. Temporal context — what time/phase is it?

Temporal context has two sublayers.

#### 1A. Clock/calendar truth

- session date
- weekday / month / expiry context
- minutes since open / minutes to close
- event proximity
- next-expiry proximity

#### 1B. Behavioural phase

Derived from primitive observables rather than fixed hour buckets.

Examples:

- open discovery
- early anchor
- compression
- trend persistence
- power hour
- close unwind

The purpose of Step 1 is to gate what is plausible and to downgrade obviously stupid expressions. It is not itself a trade selector.

### 2. Market regime context

Determine what kind of tape is in force.

Examples:

- supportive vs hostile tape
- broad vs narrow participation
- vol-stressed conditions
- semis leading / lagging
- macro crosswinds from rates / FX / beta indices

Regime context informs setup quality. It does not replace setup selection.

### 3. Options / flow context

Determine what options structure is doing to intraday behaviour.

Examples:

- strike magnetism / pin risk
- negative gamma destabilisation
- front-vs-next term distortion
- skew pressure / hedge pressure
- dealer damping vs amplification
- near-spot OI concentration

Options context is a first-class stage, not a decorative overlay.

### 4. Posture / risk permission

Ask whether business is allowed here at all.

Examples:

- risk-on
- reduced risk
- no new risk
- hedge required
- event lockout
- close/weekend caution
- carry allowed / carry blocked

This stage acts as the trader's internal risk committee and can overrule tempting setups.

### 5. Candidate setup generation

The model must not jump directly from state to one of a tiny number of flat leaf trades.

Instead it should generate plausible **candidate families** that fit the current state.

Candidate generation is where trader realism begins: multiple themes may be live, but only some are valid enough to survive posture/risk and phase constraints.

### 6. Setup variant selection

Within the selected family, choose the exact setup variant that is live now.

Examples:

- opening drive continuation
- pullback then resume
- soft strike drift
- failed breakout reversal
- event spike then fade
- stretched-from-VWAP mean reversion

This step turns a broad theme into a concrete deterministic pattern.

### 7. Execution expression

Separate **what trade/setup is live** from **how it should be expressed**.

Examples:

- starter then ladder
- breakout add after hold/reclaim
- fade extension back to value
- reduced size
- tighter invalidation
- wider tactical stop
- defined-risk options spread
- hedge into the move rather than chase

A trader may recognise the same setup but express it differently depending on volatility, liquidity, pricing, and permission state.

### 8. Carry / overnight / weekend branch

Carry is a distinct horizon branch, not a normal intraday leaf.

Questions include:

- flatten?
- hold baseline?
- reduce?
- add?
- block carry?
- event carry allowed?
- weekend carry allowed?

The carry branch receives end-of-session state but must remain its own decision surface.

### 9. Review / explanation

After action or non-action:

- why did we act?
- why did we not act?
- which stage overruled which other stage?
- which family / setup / expression was selected?
- which risk gate blocked alternatives?

The goal is desk-style reconstruction, not just a signal output.

## Structural hierarchy

The agreed playbook structure is:

**family -> setup variant -> execution expression**

With overlays for:

- phase constraints
- state requirements
- risk overrides
- horizon (`intraday`, `overnight`, `weekend`, `event_carry`)

This hierarchy replaces the idea that a trader thinks in a tiny flat list of leaf plays.

## Twelve-family scaffold

The current agreed scaffold is:

1. Trend continuation
2. Compression breakout
3. Pin / magnet behaviour
4. Negative gamma destabilisation
5. Front-expiry pin pressure
6. Term-structure dislocation
7. Skew / hedge-pressure transition
8. Gap / overnight inventory response
9. Event repricing / vol crush
10. Failed auction / trap reversal
11. Value reversion / VWAP gravity
12. Close / auction unwind

These are top-level families, not the final leaf count.

## What remains overlays or sub-variants for now

Do not promote these to top-level families yet unless replay and evidence later prove the need:

- relative leadership divergence
- call-wall / put-wall breaks
- dealer sign-flip
- liquidity vacuum / spread blowout

These are better treated as overlays, state tags, or sub-variants until proven otherwise.

## Architectural rules preserved by this update

1. **Temporal context stays first-class and separate.**
   Step 1 must not consume later-stage verdicts.

2. **Shared primitives are fine; downstream loops are not.**
   Multiple stages may reuse the same primitive data, but Step 1 must not depend on Step 2/3 conclusions.

3. **Typed contracts and DMP stay stable.**
   Modules are interchangeable only within their grammar slot.

4. **Weekend/carry is a separate branch.**
   It is not merely another intraday phase.

5. **Raw and derived data remain separated.**
   Especially for options-chain capture and temporal observables.

## Implications for future work

This update does not itself implement new families or variants. It exists to constrain future gates so that:

- family/variant population work grows inside an agreed tree
- carry work respects the separate horizon branch
- vocabulary governance can map terms against stable workflow concepts
- future module expansion does not flatten the architecture back into a small list of ad hoc playbooks

## Short form

The clarified deterministic workflow is:

**calendar/horizon -> temporal phase -> regime -> options/flow -> posture/risk permission -> candidate families -> setup variant -> execution expression -> carry branch if relevant -> review/explanation**
