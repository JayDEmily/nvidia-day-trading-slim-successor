# 01_NORMATIVE

## Purpose

This file defines the binding authority hierarchy, frozen invariants, terminology, package-organisation rules, and contract rules for this repo.

## Document precedence

If documents disagree, use this order:

1. `docs/01_NORMATIVE.md`
2. machine-readable contracts under `src/nvda_desk/schemas/`
3. DB metadata and Alembic migrations
4. `docs/02_OPERATING_MODEL.md`
5. `docs/03_DOMAIN_MODEL.md`
6. `docs/04_TECHNICAL_ARCHITECTURE.md`
7. `docs/05_GUARDRAILS.md`
8. `docs/TESTING_AND_PROMOTION.md`
9. repo-root `PLANS.md`
10. dated execution plans under `docs/planning/`
11. `AGENTS.md`
12. `README.md`
13. `docs/status/*`
14. `docs/legacy/*`

## Frozen invariants

The following are frozen unless deliberately revised with a changelog entry:

- the system is split into research and deterministic execution;
- GPT is a research and drafting tool, not a live execution engine;
- the broker boundary sits behind an internal adapter interface;
- PostgreSQL is the primary long-term system of record;
- the current local SQLite backbone exists only to accelerate deterministic build-out;
- the Makefile is the single operational front door;
- contracts, interfaces, and promotion states are more stable than policy thresholds;
- all order paths pass through posture, risk, deployable-capital governance, and ledger surfaces;
- replayability, auditability, and explanation are first-class requirements;
- the human desk operator lens is the binding design lens for every module, feature, and coefficient.

## Desk Cognition Grammar (binding runtime order)

The deterministic runtime follows this order:

1. temporal context
2. market regime context
3. options and flow context
4. posture and risk permission
5. playbook eligibility
6. expression and execution
7. review and explanation

No module bypasses this order.

## Adaptation law

The repo preserves a stable cognition grammar and only allows bounded, approved change in operating posture. That means:

- historical replay is the research and discovery surface;
- live paper is the falsification and promotion surface for locked candidates;
- review does not imply change, and **no change** is a valid governed outcome;
- runtime never invents new coefficients or hidden policy in place;
- baseline coefficient changes happen only through reviewed release, never through runtime self-adjustment.

## State-policy ontology

- **invariant surface**: runtime truth that never varies in response to session state. Examples: desk cognition grammar order, stage ownership, calendar truth, event identity, raw market facts, and review lineage.
- **baseline coefficient**: released default numeric or categorical policy surface that may change only through reviewed release. Runtime may read it but may not mutate it in place.
- **state-conditioned modifier**: typed bounded policy object that reads an approved state vector and lawfully deforms a mutable downstream surface without changing cognition grammar.
- **effective coefficient**: the review-visible result of baseline plus approved modifier lineage for one mutable surface.
- approved modifier transform family is limited to: `multiplicative_scale`, `additive_offset`, `clamp`, `rank_weight_adjustment`, and `suppression_veto`.
- approved mutable runtime surfaces are limited to: `entry_gate_score_floor`, `zone_score_threshold`, `distance_to_vwap_soft_limit_pct`, `risk_vix_caution_threshold`, `risk_vix_hot_threshold`, `max_risk_per_trade`, `target_fresh_deployable_pct`, and `hedge_required`.
- prohibited runtime variation includes: cognition grammar order, stage ownership, baseline coefficient values, calendar truth, event identity, raw market facts, playbook registry membership, and review-packet lineage.

## Non-action, conflict, and discretion law

- non-action is a first-class valid runtime outcome, not a missing action.
- stand-down classes are explicit and governed across data quality, temporal, event-risk, regime, options/flow, posture/risk, eligibility, and execution-readiness surfaces.
- conflict classes are explicit and ordered: `observation_divergence`, `confirmation_conflict`, `posture_degradation`, and `hard_veto_conflict`.
- the degradation ladder is explicit and ordered: `normal`, `confirmation_tightened`, `confidence_reduced`, `size_reduced`, `watch_only`, `stand_down`, `veto`.
- discretionary runtime override is forbidden. The only lawful non-runtime escape hatches are `audit_annotation_only` and `human_review_release_only`, both of which must remain visible in review surfaces.

## Canonical terminology

- **module**: deterministic runtime component with a clear contract.
- **feature**: reusable input, derived value, or bounded signal consumed by one or more modules.
- **classifier**: deterministic component that labels or scores state without directly allocating capital.
- **overlay**: deterministic component that reshapes, caps, vetoes, or annotates downstream behaviour.
- **playbook**: named trading behaviour that becomes eligible only after posture and permission are known.
- **gate**: binding milestone or runtime veto surface that cannot be skipped.
- **review packet**: structured explanation artefact that reconstructs how the runtime reached a decision.
- **concept-contract**: preserved non-runtime idea expressed in typed form until dependencies are ready.

## Package-organisation rules

- `src/nvda_desk/schemas/` contains strict contracts only.
- `src/nvda_desk/services/` contains deterministic business logic only.
- `src/nvda_desk/domain/` contains stable domain primitives only.
- `src/nvda_desk/api/` remains thin and delegates to services.
- planning artefacts live under `docs/planning/`.
- preserved historical evidence remains outside active runtime packages unless imported through a typed contract.

## Docstring rules

Every new or refactored Python module includes a top-level module docstring.
Every public class and public function includes a docstring that states:

- purpose;
- required inputs;
- produced outputs;
- deterministic assumptions where relevant.

No touched Python file is merged without clear docstrings.

## Contract rules

Every imported runtime module defines or reuses a typed input contract and a typed output contract.
Every runtime output that affects posture, risk, playbook eligibility, execution, or review is traceable in a review packet.
No runtime module depends on implicit hidden state.
For enum-like vocabularies that exist in `src/nvda_desk/schemas/`, the schema values are authoritative over prose mirrors.

## What varies via config

These items vary via config without altering the architecture:

- risk thresholds;
- instrument subsets;
- bounded option-strip windows;
- module coefficients and parameters;
- no-trade windows;
- runtime feature toggles;
- OpenAI model choice within the supported API surface.


## Stability corridor and scorecard law

Stability is judged through a frozen multi-axis scorecard rather than a single raw P&L line.

- the canonical scorecard axes are diagnosis quality, decision quality, economic quality, execution quality, and posture-law fidelity;
- the canonical metric families include level, slope, change in slope, persistence, dispersion, corridor width, breach frequency, breach severity, and coverage;
- every governed stability surface is assessed against a corridor algebra with target, tolerated-drift, and breach zones;
- a surface may be `breathing`, `drifting`, or `decaying`, and that distinction must remain explicit in review evidence;
- event-slice, regime-slice, and session-slice coverage must remain visible so apparent stability is not confused with thin sampling.

## Review-eligibility law

Not every observed movement deserves a review.

- review eligibility requires a governed evidence block with explicit minimum floors;
- review triggers combine evidence sufficiency with corridor-breach and persistence law;
- review may conclude `review_not_eligible` or `review_no_change` without any downstream change request;
- bounded adjustment request, candidate replacement request, research reset, and missing-module suspicion are governed review outcomes, not narrative suggestions;
- live paper remains a falsification and promotion surface for locked candidates, never an in-place coefficient search loop.

## Candidate and adjudication law

Historical research creates bounded candidate sets; live paper compares locked candidates under governed review.

- candidate sets are bounded in size and role shape before any later replay or paper comparison;
- candidate roles are limited to champion, shadow challenger, dormant candidate, and retired candidate;
- promotion, replacement, demotion, retirement, and research reset occur only at governed review boundaries;
- at least one reserved adjudication span remains untouched until final governed comparison consumes it;
- when evidence points to ontology failure rather than bounded adjustment, the correct governed result is research reset rather than another runtime tweak.

## Event taxonomy law

Event identity must remain bounded, typed, and desk-relevant.

- runtime and review may only consume events through the bounded top-level classes `company`, `peer_company`, `macro`, `policy`, `expiry`, and `venue_session`;
- event identity must separate the event existing, the market pricing it, and the realised reaction after it;
- event materiality is governed through explicit tiers `background`, `monitor`, `posture_relevant`, and `desk_critical`;
- NVDA-specific company events, bounded peer events, bounded macro/policy releases, expiry events, and venue/session events must remain distinct subclasses rather than loose labels;
- no later gate may expand the event taxonomy through free-text strings or ad hoc new classes without an explicit authority update.

## Desk-calendar and venue law

Calendar truth must come from bounded venue contracts rather than one generic open/closed flag.

- the canonical venue set for this tranche is US Nasdaq cash, JPX cash, HKEX cash, SSE/SZSE cash, and CFFEX index futures;
- venue contracts must carry timezone authority, session template, closure class, and bridge rules;
- US early-close and half-day semantics, HK holiday-eve half-day semantics, Japan split-session semantics, and Mainland China bridge/make-up-day semantics must remain explicit;
- expiry interaction with shortened sessions and carry-sensitive horizons must be recorded as calendar facts, not inferred casually downstream.

## Temporal event-window law

Event timing must remain typed, bounded, and explicit rather than described with loose words like "near event".

- event proximity states are `no_event_context`, `event_scheduled`, `event_same_day`, `event_same_session`, `event_imminent`, and `event_live_or_passed`;
- event-window states are `clear_window`, `same_session_event_window`, `event_imminent_window`, `event_live_window`, `event_cooling_off_window`, and `event_memory_window`;
- overlapping or stacked events must resolve through explicit overlap classes and priority rules rather than ad hoc judgement;
- company-event and macro-event windows may share names but not necessarily the same pre-window, post-window, cooling-off, or carry-sensitive treatment.

## Precursor-universe law

Precursor context must remain bounded to an explicit Asia/ex-US universe rather than expanding opportunistically.

- the precursor universe is bounded to JPX cash equity indices, HKEX cash equity indices, Mainland China cash equity indices, and CFFEX index futures;
- allowed raw fields are session return, opening gap, session range, realised volatility, close location in range, relative volume, futures basis, and close timing;
- allowed derived fields are directional composite, cross-venue agreement, futures-cash divergence, impulse persistence, precursor pressure, and carry-risk warning;
- Europe, commodities, crypto, and single-stock chatter remain excluded until a later explicit authority change says otherwise.

## Phase-of-day and carryover policy law

Phase and carry context may change bounded posture, but it must not mutate the desk grammar or force action merely because time advanced.

- approved day-phase states are `opening_disorder`, `opening_resolution`, `trend_window`, `midday_compression`, `late_session`, `close_auction`, and `post_close`;
- carry-horizon states are `intraday_only`, `overnight_setup`, `weekend_setup`, and `event_carry_setup`;
- midday compression and late-session carry preparation may prefer or require no-action even when no hard veto exists;
- phase/carryover policy may alter only approved mutable surfaces while invariant grammar and baseline coefficients remain unchanged.

## Event/options-stress policy law

Event-conditioned and options-stress-conditioned posture must remain one explicit matrix rather than loose trader folklore.

- event/options-stress states are `event_imminent`, `event_live`, `event_suppressed`, `negative_gamma_stress`, `pin_risk`, and `expiry_distortion`;
- the matrix must state what is suppressed, degraded, widened, capped, hedged, or blocked under each state;
- company-event, macro-event, policy-event, venue-event, and options-geometry examples may share vocabulary but not necessarily the same behavioural consequence;
- combined event-plus-options examples must remain internally consistent while final precedence waits for Gate 71;
- hard-block conditions must stay explicit rather than implied by desk lore.

## Modifier-control law

Multiple active states must resolve through one deterministic control law rather than blended judgement.

- precedence bands are `kill_switch`, `hard_block`, `event_options_stress`, `phase_carry`, `precursor`, `regime`, and `baseline`;
- compatible modifiers may combine only through bounded algebra such as `most_restrictive_wins`, `multiply_then_clamp`, `additive_offset_then_clamp`, or `block_overrides_scale`;
- caps, floors, vetoes, and kill-switch conditions must stay explicit and review-visible;
- lineage must record which precedence band won, which laws applied, which states were suppressed, and whether a kill switch fired.

## Event-source ingestion and provenance law

Supported event sources must normalise through one explicit provenance contract before any shared consumer sees them.

- supported source classes are `exchange_calendar`, `issuer_ir`, `macro_calendar`, `policy_calendar`, `internal_curated`, and `options_expiry_calendar`;
- freshness states are `current`, `stale`, and `deferred`; confidence tiers are `authoritative`, `corroborated`, `provisional`, and `degraded`;
- source conflict must stay visible through explicit dispositions rather than silent merge heuristics;
- source outages must remain explicit through governed fallback policies instead of pretending the source was healthy.

## Normative versus historical docs

- Files in `docs/` with stable names are normative unless they explicitly mark themselves as archived or historical context.
- Files in `docs/planning/` are active execution artefacts under repo-root `PLANS.md`.
- Files in `docs/status/` are dated implementation notes.
- Files in `docs/legacy/` are historical design artefacts kept for provenance.

## Naming rules

- Stable operational docs use stable names.
- Historical milestone notes use dated names.
- Changelog entries use UTC ISO time plus Unix milliseconds.
- Canonical import registries, grammar mappings, and leaf ledgers use dated filenames under `docs/planning/`.
