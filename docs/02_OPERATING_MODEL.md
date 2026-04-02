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
- when the operator is in research or brainstorm mode, GPT should push for edge, asymmetry, and candidate setup discovery before discussing implementation readiness, unless readiness is the explicit question;
- critiques overfitting and missing controls;
- helps explain post-trade outcomes.

### Deterministic runtime
- evaluates approved module stacks;
- applies posture, vetoes, and risk policy;
- records orders, fills, vetoes, blocks, and attribution;
- runs replay, backtest, and paper paths.

## Adaptation and evidence law

The deterministic desk is allowed to adapt only in a bounded, inspectable way.

The research cockpit exists to observe, compare, hypothesise, and decide what deserves formalisation. Research-mode discussion is therefore idea-first: implementation caveats, live-readiness warnings, and promotion constraints belong in reporting mode unless the operator asks for them.

- The cognition grammar stays fixed unless a deliberate normative revision proves otherwise.
- Historical replay is the research/discovery surface.
- Live paper is the falsification/promotion surface for locked candidates and must not become in-place coefficient discovery.
- Review may end in `no_change`; the existence of a review does not itself authorise a runtime or coefficient edit.
- Runtime never invents coefficients or hidden policy in place.

## Daily operating loop

```text
prepare market picture
  -> inspect market state and prior analogues
  -> discuss candidate setups with GPT
  -> draft or revise module artefacts
  -> code / gate deterministic module changes
  -> replay / backtest / paper evaluate
  -> promote, revise, retire, or keep unchanged
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

## Co-resident independent parallel risk lane (planning placement)

The future independent parallel risk lane is planned as a first-class co-resident lane that starts with session start and evolves as the seven-step grammar yields new lawful outputs across the day.

- at session start the lane is limited to approved invariant truth such as desk calendar truth, calendar-horizon routing, scheduled-event authority, stage ownership, raw market facts, and released coefficient authority;
- as the day progresses, the lane may consume approved outputs from temporal context, market regime context, options and flow context, and later owned downstream surfaces only after those stages have produced them;
- this placement preserves the serial desk cognition grammar while allowing the lane to remain first-class and real-time from the beginning of the session;
- review and explanation remain responsible for preserving future reconstruction of the lane once runtime implementation exists.

## Gate 60 state-policy authority

The approved modifier read-set is an explicit state vector, not hidden ambient state. The current canonical readable fields are:

- temporal ownership: `desk_window`, `clock_envelope`, `carryover_state`, `expiry_cycle_state`, `event_proximity_state`, `event_window_state`;
- regime ownership: `volatility_regime`, `breadth_state`, `sector_leadership_state`, `rates_regime_state`, `fx_stress_state`, `signal_conflict_state`;
- options/flow ownership: `term_structure_state`, `skew_state`, `gamma_state`, `dealer_pressure_state`, `options_behavior_cluster`;
- posture/risk ownership: `inventory_posture_state`, `fresh_vs_inventory_state`, `thesis_state`, `capital_lockup_state`, `time_stop_state`, `permission_state`.

Those fields may inform bounded posture policy, but they do not authorise runtime mutation of grammar order, baseline coefficients, calendar/event truth, or registry membership.

## Gate 61 non-action and conflict authority

The deterministic desk is allowed to decide **not** to participate. That is a valid governed outcome.

- stand-down remains first-class and is not treated as a missing trade;
- conflicts stay visible in review as ordered classes rather than disappearing into narrative reasons;
- degradation is ordered from tighter confirmation through reduced confidence and size, then watch-only, stand-down, and veto;
- discretionary runtime override is forbidden, and any permitted human-only release or audit annotation must stay outside the runtime path and inside review evidence.


## Gate 62 stability authority

Stability is judged with a frozen scorecard and corridor algebra rather than a single trailing outcome snapshot.

- every governed surface receives a scorecard across diagnosis quality, decision quality, economic quality, execution quality, and posture-law fidelity;
- metric families stay explicit: level, slope, acceleration, persistence, dispersion, corridor width, breach frequency, breach severity, and coverage;
- corridor zones are explicit target, tolerated-drift, and breach ranges;
- persistence and hysteresis prevent one noisy block from becoming an automatic review demand;
- event, regime, and session slice coverage remain visible so hidden fragility is not mistaken for stability.

## Gate 63 review-eligibility authority

A review only becomes eligible when the evidence block is large enough and the observed behaviour crosses the governed trigger law.

- coefficient groups and policy surfaces carry explicit minimum evidence floors;
- review triggers are bounded to corridor breaches, persistence failures, or coverage collapse, not vague discomfort;
- downstream review outcomes stay governed: `review_not_eligible`, `review_no_change`, `bounded_adjustment_request`, `candidate_replacement_request`, `research_reset`, and `missing_module_suspicion`;
- every review outcome carries a bounded change budget;
- live paper still falsifies locked candidates and does not become a search loop for new in-place coefficients.

## Gate 64 candidate governance authority

Historical replay locks candidates; live paper adjudicates them under bounded role and span rules.

- candidate sets remain small and role-bound before later replay and live-paper wiring;
- champion, shadow challenger, dormant candidate, and retired candidate are the only governed role labels;
- adjudication keeps one reserved untouched span until final comparison consumes it deliberately;
- governed outcomes are retain champion, promote challenger, demote to dormant, retire candidate, or reset to research;
- if the failure is ontology-level rather than candidate-level, the governed answer is research reset rather than ad hoc retuning.

## Gate 65 event-taxonomy authority

Later calendar, event-window, and policy gates now inherit a frozen event identity surface.

- top-level event classes are company, peer company, macro, policy, expiry, and venue/session;
- every event keeps semantic separation between known risk, priced risk, and realised reaction;
- materiality is tiered as background, monitor, posture relevant, and desk critical;
- NVDA-specific, bounded peer, bounded macro/policy, expiry, and venue/session subclasses remain explicit rather than free-form text.

## Gate 66 desk-calendar authority

Temporal routing now depends on venue contracts rather than a single generic market-open concept.

- the supported venue set is bounded to Nasdaq US cash, JPX cash, HKEX cash, SSE/SZSE cash, and CFFEX index futures;
- venue contracts carry timezone authority, session template, closure classes, and bridge rules;
- US early closes, HK holiday-eve half-days, Japan split sessions, and Mainland China bridge/make-up-day behaviour stay explicit;
- expiry interactions with shortened sessions and carry-sensitive horizons are treated as calendar facts.

## Gate 67 temporal event-window authority

Event timing now has bounded semantics before later policy matrices consume it.

- proximity, window, overlap, risk-timing, and carry-sensitivity states are explicit typed authority, not free text;
- event windows distinguish priced risk, live release, realised reaction, cooling-off, and event-memory semantics;
- overlapping windows must resolve through explicit priority classes rather than informal discretion;
- company and macro events may share vocabulary while still carrying different time budgets.

## Gate 68 precursor-universe authority

Precursor context is now bounded before any stitching or runtime integration work begins.

- supported precursor venues are JPX cash, HKEX cash, Mainland China cash, and CFFEX index futures;
- only the approved raw and derived precursor fields may flow into later stitching and policy gates;
- session alignment must use last-complete-session semantics and keep weekend/holiday gaps explicit;
- tempting extra sources remain excluded until they are explicitly authorised.

## Gate 69 phase-and-carryover policy authority

Stable doctrine now has a bounded ordinary-session policy matrix.

- day-phase and carry-horizon states are explicit typed policy inputs rather than loose clock phrases;
- the matrix distinguishes opening disorder, orderly trend windows, midday compression, late-session carry preparation, and post-close states;
- no-action can be preferred or required by policy without inventing a discretionary override;
- the matrix only targets approved mutable runtime surfaces.

## Gate 70 event/options-stress policy authority

Stable doctrine now has an explicit matrix for event-conditioned and options-stress-conditioned posture.

- the matrix covers imminent/live event risk, event suppression, negative gamma stress, pin risk, and expiry distortion;
- behavioural consequences are bounded to tightened thresholds, hedged-only operation, size caps, watch-only posture, or hard block;
- the matrix states which mutable runtime surfaces are targeted and which conditions force no-action or stand-down;
- combined event-plus-options examples remain lawful while final precedence stays deferred to Gate 71.

## Gate 71 modifier-control-law authority

The repo now has one deterministic combination law for multiple active posture states.

- precedence bands order kill switches, hard blocks, event/options stress, phase/carry, precursor context, regime context, and baseline posture;
- compatible modifiers combine through bounded algebra and then clamp to approved caps/floors;
- vetoes and kill switches remain explicit, typed, and review-visible;
- lineage requirements now freeze how later review packets reconstruct which modifier won and why.

## Gate 72 event-ingestion and provenance authority

The repo now has one bounded provenance contract for supported event sources before shared store/query or runtime consumers read event truth.

- supported upstream sources are inventoried explicitly rather than implied by ad hoc helpers;
- every normalised event record carries freshness, confidence, lineage, and visible conflict/outage semantics;
- label conflicts and degraded sources remain explicit after normalisation;
- this gate freezes ingestion authority only; shared store/query consumers land in Gate 73.

## Gate 73 shared event-store and query authority

The repo now has one bounded shared event truth surface for runtime, review, and replay consumers.

- nearby-event selection now flows through an explicit query window contract;
- material-event filters now use explicit materiality floors;
- lineage retrieval is part of the shared event-store contract rather than a side path;
- replay uses the same event truth with a declared consumer mode instead of bespoke semantics.

## Gate 74 live event-richness authority

The live runtime preparation path now preserves a bounded `live_event_snapshot` contract from the shared event store through prepared runtime snapshots into `TemporalContextInput.live_event_snapshot`. Older temporal consumers may continue to read `next_event_at`, but that timestamp is now an additive compatibility hint derived from the richer packet, not a substitute for it.

- nearby-event selection now flows through an explicit query window contract;
- material-event filters now use explicit materiality floors;
- lineage retrieval is part of the shared event-store contract rather than a side path;
- replay uses the same event truth with a declared consumer mode instead of bespoke semantics.

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

## Gate 75 precursor-stitching authority

Gate 75 freezes one deterministic stitching order for bounded precursor venues, one timestamp discipline, one stale/degraded fallback ladder, and one contradiction classification surface before any runtime packet or policy matrix may consume precursor context.

Operational rules:
- `MarketStateService.stitch_precursor_context(...)` is the authoritative pre-runtime assembly path for precursor slices.
- precursor stitching stays descriptive at this gate; it may classify contradiction or stand-down pressure, but it must not yet mutate runtime policy surfaces.
- `PrecursorRuntimePacket` remains out of scope for Gate 75 closeout even though its future shape is now anticipated by the authority packet.

## Gate 76 precursor runtime-binding authority

Gate 76 binds precursor truth into the runtime ingress and review packet surfaces without changing runtime policy logic.

Operational rules:
- `PreparedRuntimeSnapshot.precursor_runtime_packet` and `TemporalContextInput.precursor_runtime_packet` carry the same typed precursor truth.
- `ReviewExplanationInput.temporal_input` is the lawful bridge that lets review expose exactly the precursor packet runtime received.
- legacy runtime consumers may ignore the richer precursor packet, but they must not create a competing hidden precursor surface.

## Gate 77 review-packet and failure-taxonomy authority

Gate 77 upgrades the review packet so later replay, paper review, and candidate adjudication can reconstruct what the system knew, how posture changed, why action or non-action occurred, and which failure class or ambiguity bucket applies.

Operational rules:
- `ReviewExplanationOutput.review_lineage`, `failure_taxonomy`, `economic_accountability`, and `promotion_evidence` are now mandatory typed review surfaces.
- event lineage and precursor lineage may be empty only when the runtime input truly had none; empty lineage must remain explicit, not silently omitted.
- missing modifier or effective-coefficient lineage must remain visible to later candidate-governance consumers via `PromotionEvidencePacket.missing_sections`.

## Gate 78 runtime modifier integration authority

`PostureRiskOutput`, `ExecutionExpressionOutput`, and `ReviewExplanationOutput` must all be able to see the same Gate 78 modifier packet.

Operational rules:
- effective coefficients now materialise inside runtime rather than being implied from narrative after the fact;
- posture receives bounded permission, stand-down, and target-capital consequences from the packet without changing grammar order;
- execution receives additive hedge/capital consequences from the same packet rather than a second private modifier interpretation;
- review reads the same packet for effective-policy lineage, modifier-control-law outcomes, and blocked-trade / non-action explanation.

## Gate 79 walk-forward harness authority

Gate 79 freezes the replay-side harness contract only. It may generate chronology-safe windows, compare offsets, and emit bounded horizon/fragility/coverage outputs. It may not silently become a live search loop or promotion engine.
