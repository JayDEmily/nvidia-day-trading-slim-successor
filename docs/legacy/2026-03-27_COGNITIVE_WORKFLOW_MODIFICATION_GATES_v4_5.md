# Historical salvage artefact

Status: archived context only; not an active planning authority.

This file is preserved in-repo for provenance because Gate 59 absorbed usable leaf-level detail from the later `_v4_5` salvage pair while keeping V6 as the single controlling authority.

---

# 2026-03-27 Cognitive Workflow Modification Gates v4

Status: Gates 51–58 complete on `main`; this successor pack begins at Gate 59

Version: v4.0

Historical note: v2/v3 exploratory drafts were useful for thought capture but over-broad for honest one-pass execution. This v4 pack keeps the gold while splitting the tranche into genuinely executable gate slices.

## Purpose

This document defines the **successor modification tranche** after Gate 58 for the next desk-cognition expansion work: canonical desk calendar and event taxonomy, preservation of event richness into live cognition, Asia/ex-US precursor context, state-conditioned modifier policy, stability-metric governance, candidate/adjudication doctrine, and bounded runtime integration.

This is **not** a repo rewrite. It is a controlled extension of the current deterministic desk-cognition architecture so that the runtime can preserve richer context and vary operating posture deterministically without mutating the cognition grammar.

The governing workflow remains:

`calendar/horizon -> temporal_context -> market_regime_context -> options_flow_context -> posture_risk_permission -> playbook_eligibility -> expression_execution -> review_explanation`

## Position in the planning stack

This gate pack is the canonical successor to the completed cognitive-workflow tranche and DMP promotion tranche. Gates 51–58 are historical complete state on `main`; Gates 59–78 are planned and bounded by this artefact.

## Governing inputs

- `docs/01_NORMATIVE.md`
- `docs/02_OPERATING_MODEL.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`
- `docs/05_GUARDRAILS.md`
- `docs/TESTING_AND_PROMOTION.md`
- `AGENTS.md`
- `docs/planning/2026-03-26_COGNITIVE_WORKFLOW_UPDATE.md`
- `docs/planning/2026-03-26_COGNITIVE_WORKFLOW_IMPLEMENTATION_MAP.md`
- `docs/planning/2026-03-26_COGNITIVE_WORKFLOW_BOUNDARY_RULES.md`
- `docs/planning/2026-03-26_CALENDAR_HORIZON_OWNERSHIP.md`
- `docs/planning/2026-03-26_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v1.md`
- `docs/planning/2026-03-26_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v1.json`
- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`

## Global tranche rules

1. This successor pack begins after Gates 51–58 and exists to turn the broad exploratory modification ideas into genuinely executable slices.
2. The binding cognition grammar order remains authoritative; no gate may reorder runtime stages unless a dedicated gate proves and documents the change.
3. One branch per gate; complete every planned leaf for the gate, pass targeted validation, merge to main, and only then open the next gate branch.
4. No leaf may silently introduce ad hoc event classes, calendar facts, precursor markets, or modifier surfaces outside the authority docs created in earlier gates.
5. Live paper remains a falsification/promotion surface for locked candidates, not an in-place coefficient-discovery surface.
6. State-conditioned modifiers are bounded runtime policies, not informal retuning; prohibited variable surfaces remain fixed.
7. Any gate that reveals ontology failure or a missing module must emit a research-reset note rather than smuggling the redesign into the current gate.

## Non-goals for this tranche

- inventing an unbounded event/news ontology in one pass
- letting live paper become in-place coefficient discovery
- replacing typed packet surfaces with loose dict payloads
- allowing state-conditioned modifiers to alter grammar order or hidden routing
- creating a huge free-form precursor universe without bounded desk rationale
- collapsing review into narrative commentary instead of evidence objects

---

## Gate 59 — Canonical event taxonomy

Status: planned

### Objective

Freeze a deterministic, typed event taxonomy covering company, macro, venue, expiry, and policy-significant calendar events.

### Why this gate exists

The runtime cannot reason cleanly about event identity if event classes remain loose strings or mixed free-text labels.

### Scope

- Define canonical event classes, known/priced/realised distinctions, impact tiers, and desk-relevant examples.

- Freeze canonical event-class taxonomy
- Separate known risk, priced risk, and realised reaction semantics
- Define event impact-tier vocabulary and examples
- Define company-specific event classes for NVDA and close peers
- Define macro, policy, and expiry event classes
- Freeze the event-taxonomy authority surface

### Definition of done

A typed event taxonomy exists with bounded classes, explicit meanings, and no free-text ambiguity at the runtime boundary.

### Gate outputs

- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v4.md`
- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v4.json`

---

## Gate 60 — Session, holiday, and venue-calendar contracts

Status: planned

### Objective

Formalise desk-relevant session and holiday calendars across US, Japan, Hong Kong, and China, including half-days and bridge rules.

### Why this gate exists

The desk-calendar problem is broader than events; venue sessions and holidays are first-class route selectors and precursor-context shapers.

### Scope

- Define venue/session taxonomy, holidays, half-days, bridge rules, and expiry-calendar interactions.

- Define venue and session taxonomy
- Formalise US holidays and half-day rules
- Formalise Japan, Hong Kong, and China holiday/session facts
- Define session-bridge and timezone-alignment rules
- Define expiry-calendar and session interaction rules
- Freeze the desk-calendar authority surface

### Definition of done

A canonical desk calendar contract exists for session ownership, holidays, half-days, and expiry-aware calendar facts.

### Gate outputs

- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v4.md`
- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v4.json`

---

## Gate 61 — Event-source ingestion and provenance normalisation

Status: planned

### Objective

Bind all supported event feeds to one normalised provenance contract before they touch cognition runtime state.

### Why this gate exists

If ingestion/provenance is vague, later event richness is untrustworthy and review packets cannot explain what was known when.

### Scope

- Inventory sources, normalise fields, define conflict rules, stale-data policy, and provenance requirements.

- Inventory supported event sources
- Define normalised event-source field contract
- Define provenance, confidence, and freshness rules
- Define conflict-resolution rules across sources
- Define missing-data and source-outage fallback rules
- Freeze event-ingestion and provenance authority

### Definition of done

All supported event sources map through one normalised provenance contract with explicit conflict and staleness handling.

### Gate outputs

- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v4.md`
- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v4.json`

---

## Gate 62 — Event store and query surfaces

Status: planned

### Objective

Create bounded event-store/query surfaces so runtime, review, and backtest paths consume the same event semantics.

### Why this gate exists

Event richness cannot remain trapped in one upstream service or ad hoc helper if multiple runtime consumers need stable access.

### Scope

- Define persistence/query surfaces, nearby-event selection, materiality filters, and review-facing retrieval rules.

- Define event-store persistence contract
- Define query surfaces for runtime consumers
- Define material-event selection rules
- Define nearby-event packet contract
- Define review and lineage retrieval rules for events
- Freeze shared event-store/query authority

### Definition of done

Event storage and query contracts are explicit, typed, and shared across runtime and review consumers.

### Gate outputs

- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v4.md`
- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v4.json`

---

## Gate 63 — Preserve event richness into live cognition input

Status: planned

### Objective

Carry event identity, impact, and provenance all the way into live cognition input rather than collapsing them to timestamp-only hints.

### Why this gate exists

The current live path loses useful event richness before runtime evaluation begins; that weakens deterministic reasoning.

### Scope

- Extend packets and bindings so live cognition sees event class, impact, provenance, and nearby-event summaries.

- Extend the live event snapshot contract
- Rewire real-data loading to preserve event richness
- Rewire chain-to-cognition event binding
- Define lineage retention for event-rich runtime packets
- Define regression and compatibility boundaries for event-rich packets
- Freeze the live event-richness authority surface

### Definition of done

Live cognition input preserves event richness end to end without hidden data loss between ingest and runtime.

### Gate outputs

- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v4.md`
- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v4.json`

---

## Gate 64 — Temporal event-window semantics

Status: planned

### Objective

Define how event facts become temporal window states without collapsing known risk, priced risk, and realised reaction into one bucket.

### Why this gate exists

Temporal routing needs event-window semantics, but event identity must remain distinct from pricing response and realised path.

### Scope

- Specify event-window states, thresholds, examples, and temporal ownership boundaries.

- Define event-window-state taxonomy
- Define temporal thresholds and ownership for event windows
- Preserve known-vs-priced-vs-realised distinctions through temporal mapping
- Define event-window examples for ordinary, clustered, and edge-case days
- Define temporal-output contract changes required by event windows
- Freeze temporal event-window authority

### Definition of done

Temporal event semantics are explicit enough that identical timestamps with different event classes cannot be silently conflated.

### Gate outputs

- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v4.md`
- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v4.json`

---

## Gate 65 — Asia and ex-US precursor market universe

Status: planned

### Objective

Freeze the desk-relevant overnight precursor market universe before stitching any signals into runtime state.

### Why this gate exists

The precursor concept is valuable only if the instrument and venue universe is explicit and bounded.

### Scope

- Select the Asia/ex-US markets, futures, FX, and supporting instruments the desk treats as precursor context.

- Freeze precursor market universe membership
- Define precursor source and provenance rules
- Define raw versus derived precursor fields
- Define precursor desk-relevance criteria
- Define precursor session-alignment examples
- Freeze precursor-universe authority

### Definition of done

A bounded precursor market universe exists with desk rationale and explicit ownership.

### Gate outputs

- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v4.md`
- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v4.json`

---

## Gate 66 — Precursor stitching, fallback, and contradiction rules

Status: planned

### Objective

Define how precursor facts are aligned, combined, degraded, or discarded when overnight signals are incomplete or contradictory.

### Why this gate exists

Raw precursor markets are useful, but the runtime needs deterministic stitching, timezone, and contradiction rules to avoid drift.

### Scope

- Specify stitching order, stale/missing fallback, contradiction handling, derived states, and ownership boundaries.

- Define precursor stitching order and timezone rules
- Define stale, missing, and partial precursor fallback logic
- Define contradiction resolution for precursor signals
- Define derived precursor state vocabulary
- Pin precursor ownership boundary into runtime stages
- Freeze precursor-stitching authority

### Definition of done

Precursor state derivation is deterministic, timezone-safe, and explicit about missing/contradictory inputs.

### Gate outputs

- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v4.md`
- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v4.json`

---

## Gate 67 — Precursor runtime binding and review exposure

Status: planned

### Objective

Bind precursor context into runtime and review surfaces so overnight state is visible, inspectable, and replayable.

### Why this gate exists

Precursor work is incomplete if it remains a side analysis rather than a first-class runtime and review surface.

### Scope

- Add precursor packets, runtime bindings, review exposure, and lineage rules.

- Define precursor runtime packet contract
- Plan real-data binding for precursor context
- Plan stage-level precursor consumption
- Define precursor lineage and review exposure
- Define regression boundaries for precursor runtime integration
- Freeze precursor runtime-binding authority

### Definition of done

Precursor context is visible in runtime packets, review packets, and replay/backtest surfaces.

### Gate outputs

- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v4.md`
- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v4.json`

---

## Gate 68 — State-policy vocabulary and coefficient taxonomy

Status: planned

### Objective

Define the vocabulary and object model for fixed invariants, baseline coefficients, and state-conditioned modifiers.

### Why this gate exists

State-aware behaviour will drift immediately unless the repo has one precise language for what may vary and what must never vary.

### Scope

- Freeze the state vector vocabulary, modifier objects, mutable-surface taxonomy, and prohibited variable surfaces.

- Freeze invariant, baseline, and modifier taxonomy
- Define the canonical state vector vocabulary
- Define the modifier policy object model
- Define eligible mutable runtime surfaces
- Define prohibited variable surfaces
- Freeze state-policy vocabulary authority

### Definition of done

The repo has one authoritative vocabulary for invariants, baselines, modifiers, and approved runtime state labels.

### Gate outputs

- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v4.md`
- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v4.json`

---

## Gate 69 — Phase-of-day and carryover policy matrix

Status: planned

### Objective

Write the deterministic modifier policy matrix for ordinary temporal phases and carryover conditions across the day.

### Why this gate exists

The open, midday, trend windows, late session, and carryover states should not share one undifferentiated operating posture.

### Scope

- Define approved phase states and how each state adjusts permission, capital, confirmation, and expression behaviour.

- Define approved day-phase state list
- Write open-disorder operating posture policy
- Write trend-window and orderly-session policy
- Write midday-compression policy
- Write late-session and carryover-prep policy
- Freeze phase-and-carryover policy-matrix authority

### Definition of done

A bounded phase/carryover policy matrix exists and identifies what changes, what does not, and why.

### Gate outputs

- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v4.md`
- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v4.json`

---

## Gate 70 — Event and options-stress policy matrix

Status: planned

### Objective

Write the modifier policy matrix for event-conditioned and options-stress-conditioned states.

### Why this gate exists

Event-imminent, event-live, negative-gamma, event-suppressed, and pin-risk states deserve explicit operating-posture rules.

### Scope

- Define event/options-stress modifier policies and interaction examples.

- Write event-imminent and event-live modifier policy
- Write event-suppressed and negative-gamma-stress policy
- Write pin-risk and expiry-distortion policy
- Write combined event-plus-options-state examples
- Define event/options-state non-action boundaries
- Freeze event/options-stress policy-matrix authority

### Definition of done

A bounded event/options-stress policy matrix exists with explicit behavioural consequences.

### Gate outputs

- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v4.md`
- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v4.json`

---

## Gate 71 — Modifier precedence, caps, vetoes, and kill-switches

Status: planned

### Objective

Formalise how multiple active states combine and where hard vetoes or kill-switches override soft modifier logic.

### Why this gate exists

State-conditioned modifiers become soup unless the precedence and hard-stop rules are explicit.

### Scope

- Define modifier precedence, floors/caps, vetoes, kill-switches, and conflict examples.

- Define modifier precedence graph
- Define caps, floors, and bounded adjustment forms
- Define hard veto and stand-down rules
- Define kill-switch and emergency-degradation semantics
- Define combined-state sanity examples
- Freeze modifier-control authority

### Definition of done

Multiple active state modifiers combine deterministically under one precedence and hard-stop contract.

### Gate outputs

- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v4.md`
- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v4.json`

---

## Gate 72 — Stability-metric algebra and scorecard schema

Status: planned

### Objective

Define the metrics that judge coefficient-group stability without reducing the problem to raw P&L.

### Why this gate exists

The review problem is really a metric-algebra problem: ranking stability, decision-distribution stability, and economic stability must be formalised.

### Scope

- Specify metric components, scorecards, corridor algebra, persistence measures, and event-slice views.

- Define stability-metric components
- Define per-group scorecard schema
- Define corridor algebra and thresholds
- Define persistence and hysteresis measures
- Define event-slice and coverage metrics
- Freeze stability-metric authority

### Definition of done

A typed stability-metric schema exists for each coefficient group and can emit review-ready scorecards.

### Gate outputs

- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v4.md`
- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v4.json`

---

## Gate 73 — Review-eligibility governance

Status: planned

### Objective

Turn the stability metrics into a deterministic review-eligibility contract with evidence floors and hysteresis.

### Why this gate exists

The repo needs a rule for when review is allowed, when change is justified, and when no change is the correct decision.

### Scope

- Define evidence floors, corridor breach logic, persistence windows, and review/no-change outputs.

- Define minimum evidence floors per coefficient group
- Define corridor-breach review triggers
- Define persistence and no-change outcomes
- Define live-paper falsification boundary
- Define review output states and downstream actions
- Freeze review-eligibility authority

### Definition of done

Review eligibility is governed by explicit evidence-floor, corridor, and persistence rules rather than calendar folklore.

### Gate outputs

- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v4.md`
- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v4.json`

---

## Gate 74 — Candidate, champion, challenger, and adjudication governance

Status: planned

### Objective

Formalise how historical research outputs locked candidates and how live paper falsifies or promotes them.

### Why this gate exists

The repo should not “discover” coefficients in live paper; it should compare locked candidates and promote or reject them deterministically.

### Scope

- Define candidate set bounds, champion/challenger semantics, untouched adjudication rules, and reset-to-research triggers.

- Define candidate-set size and shape constraints
- Define champion and challenger semantics
- Define promotion, replacement, and demotion rules
- Define untouched adjudication rules
- Define research-reset and new-module triggers
- Freeze candidate-governance authority

### Definition of done

Candidate governance is explicit enough that live paper becomes falsification/promotion, not ad hoc tuning.

### Gate outputs

- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v4.md`
- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v4.json`

---

## Gate 75 — Walk-forward review-horizon discovery harness

Status: planned

### Objective

Build the experimentation harness that discovers the minimum stable review horizon for each coefficient group.

### Why this gate exists

There is no single X for retuning; the review horizon itself must be discovered empirically under walk-forward replay.

### Scope

- Define window generation, offset comparison, horizon discovery, event slicing, and fragility outputs.

- Define walk-forward window-generation contract
- Define start-offset comparison logic
- Define review-horizon discovery algorithm
- Define event-sliced and regime-sliced reporting outputs
- Define fragility, ablation, and module-pruning outputs
- Freeze walk-forward harness authority

### Definition of done

The repo can empirically discover per-group review horizons and compare candidate stability across walk-forward slices.

### Gate outputs

- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v4.md`
- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v4.json`

---

## Gate 76 — Review packet upgrade and failure taxonomy

Status: planned

### Objective

Upgrade review packets so they expose what the runtime knew, what state modifiers fired, and why a result counts as read/expression/sizing/luck/ontology failure.

### Why this gate exists

A trader-grade review loop needs richer failure taxonomy and stronger evidence objects than a generic explanation packet.

### Scope

- Add review fields, failure taxonomy, economic contribution views, and promotion-evidence surfaces.

- Define review-packet event and precursor fields
- Define trader-grade failure taxonomy
- Define economic-contribution and edge-accountability fields
- Define non-action and blocked-trade explanation fields
- Define promotion-evidence packet outputs
- Freeze review-packet authority

### Definition of done

Review packets can explain event class, precursor context, state modifiers, non-action, and failure taxonomy in one evidence object.

### Gate outputs

- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v4.md`
- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v4.json`

---

## Gate 77 — Non-action, discretion, and conflict hierarchy

Status: planned

### Objective

Formalise when the correct outcome is stand-down, what discretion is forbidden, and how unresolved conflicts degrade posture.

### Why this gate exists

Serious desk logic needs explicit non-action and conflict governance, not a bias toward forced participation.

### Scope

- Define stand-down classes, conflict hierarchy, degradation hierarchy, and any permitted override boundaries.

- Define non-action taxonomy
- Define discretion boundaries
- Define signal-conflict hierarchy
- Define degradation hierarchy
- Define override/audit recording rules
- Freeze non-action/discretion/conflict authority

### Definition of done

The repo can justify non-action and signal conflict outcomes without informal discretion or narrative drift.

### Gate outputs

- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v4.md`
- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v4.json`

---

## Gate 78 — Runtime integration of state-conditioned modifiers

Status: planned

### Objective

Integrate the bounded modifier system into the runtime surfaces that actually control permission, capital, confirmation, and execution behaviour.

### Why this gate exists

The planning and governance layers are incomplete until a bounded runtime integration path is defined and proven.

### Scope

- Wire the modifier system into posture, eligibility, and execution surfaces with end-to-end tests and proofs.

- Plan posture-risk modifier integration
- Plan playbook-eligibility modifier integration
- Plan execution-expression modifier integration
- Define end-to-end runtime modifier path and explanation surfaces
- Define targeted and full-suite validation for runtime modifier rollout
- Freeze runtime modifier-integration authority

### Definition of done

State-conditioned modifiers affect runtime behaviour in bounded, tested, reviewable ways without altering the cognition grammar order.

### Gate outputs

- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v4.md`
- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v4.json`

---

## Execution order

1. Gate 59
2. Gate 60
3. Gate 61
4. Gate 62
5. Gate 63
6. Gate 64
7. Gate 65
8. Gate 66
9. Gate 67
10. Gate 68
11. Gate 69
12. Gate 70
13. Gate 71
14. Gate 72
15. Gate 73
16. Gate 74
17. Gate 75
18. Gate 76
19. Gate 77
20. Gate 78

No later gate may begin until the current gate is complete, validated, and merged.

## Why this successor pack is different

- The broad exploratory themes are preserved, but each theme has been broken into smaller authority, binding, governance, and integration slices.

- The leaf ledger uses the **same top-level and per-leaf schema family** as the repo's cognitive-workflow leaf ledger, so it can be slotted into the existing planning stack without ad hoc JSON shape drift.

- The early gates are documentation/authority/binding slices that can be executed honestly without pretending a whole subsystem was completed in one pass.

- Later gates still remain bounded: policy matrices, metric algebra, candidate governance, harness planning, review-packet upgrades, and final runtime integration are separated rather than bundled.

## Final note

This pack exists to preserve the thread gold without compressing it into un-executable mega-gates. The goal is not brevity; the goal is an honest, drift-resistant path from calendar/event richness through state-conditioned modifier governance to bounded runtime integration.
