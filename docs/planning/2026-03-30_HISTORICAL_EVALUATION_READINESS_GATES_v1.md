Status: active historical-evaluation readiness pack; Gate 115 active, Gates 116-121 planned
# 2026-03-30 Historical Evaluation Readiness Gates v1
## Purpose

Convert the accepted pre-historical-evaluation carry-forward ideas into one active implementation pack, ordered by dependency rather than by brainstorm order, so the repo can move from alpha-shape governance into historically testable runtime refinement without smuggling deferred evaluation work into the wrong tranche.
## Scope

In scope:
- normalised prepared-runtime feature work needed before historical evaluation logic is trusted across regimes;
- temporal/event-law sharpening, precursor economics, mutable-surface truthing, candidate adjudication, execution geometry, and final risk unification;
- active planning surfaces for Gates 115-121 plus the explicit exclusion of deferred ideas from this tranche.

Out of scope:
- latency/fill-regime realism expansion that depends on historical execution evidence rather than current alpha wiring;
- large options-taxonomy rewrites before replay evidence proves the current taxonomy is wrong;
- regime-transition-state expansion before more historical windows exist;
- broad testing-regime additions that belong after this runtime-refinement tranche starts yielding historical evidence.
## Supersession and active authority

- This document becomes the active gate authority for Gates 115-121.
- It supersedes the absence of any active pack after Gate 114 closeout.
- It also supersedes the earlier draft ordering that had not yet been reconciled against the later operator JSON triage.
## Governing inputs

- `docs/01_NORMATIVE.md`
- `docs/02_OPERATING_MODEL.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`
- `docs/05_GUARDRAILS.md`
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `AGENTS.md`
- `PLANS.md`
- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`
- `docs/03_DOMAIN_MODEL.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- `docs/TESTING_AND_PROMOTION.md`
- `src/nvda_desk/services/real_data_loader.py`
- `src/nvda_desk/services/temporal_context.py`
- `src/nvda_desk/services/financial_calendar_projection.py`
- `src/nvda_desk/services/market_state.py`
- `src/nvda_desk/services/state_conditioned_modifier.py`
- `src/nvda_desk/services/execution_expression.py`
- `src/nvda_desk/services/risk_gateway.py`
- `src/nvda_desk/services/cognition_runtime.py`
## Workflow placement

This tranche sits between the alpha governance/testing foundation and the later historical-evaluation/promotion loop. It is upstream runtime-refinement work: better prepared inputs, better temporal and precursor context, honest mutable-surface authority, better candidate adjudication, richer execution expression, and one final risk join. Historical datasets and later tuning work consume the outputs of this tranche; they should not have to work around brittle raw-level thresholds, registry-order lead selection, or split permission worlds.
## Intent and workflow anchor

The binding lens is still the desk-operator research/runtime split in `docs/01_NORMATIVE.md`: this pack is not about making the system live; it is about making the deterministic runtime worth historical evaluation. The execution order is therefore dependency-first:

1. improve the substrate;
2. sharpen the upstream event/context law;
3. make precursor economics real;
4. force mutable-surface truth;
5. adjudicate among candidates properly;
6. enrich execution geometry;
7. let one final risk join bind the whole chain.
## Accepted / deferred / rejected carry-forward ideas

Accepted and integrated here:
- `C011` into Gate 115
- `C013` and `C014` into Gate 119
- `C004` and `C006` into Gate 120
- `C009` into Gate 121
- `C001` split across Gates 118 and 121

Explicitly deferred out of this pack:
- options-taxonomy refinement before replay evidence demands it
- regime-transition and persistence-state work before broader historical windows exist
- declarative setup-predicate refactors that are mostly architecture cleanup rather than immediate runtime leverage
- fresh-capital-versus-inventory permission splitting before historical evidence proves it is costing signal quality
## Retain / retire-from-authority / amend / add matrix

### Retain as canonical
- `docs/01_NORMATIVE.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`
- `docs/05_GUARDRAILS.md`
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `AGENTS.md`

### Retire from authority (compatibility-only unless later removed)
- none at planning time; specific retirements, if any, must be declared gate-by-gate during execution

### Mandatory amendments
- `PLANS.md` because the repo needs one active pack again
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md` because Gate 115 must become the active gate and Gates 116-121 must be mapped in order
- `CHANGELOG.jsonl` because a meaningful planning change is being made

### New additions
- `docs/planning/2026-03-30_HISTORICAL_EVALUATION_READINESS_GATES_v1.md`
- `docs/planning/2026-03-30_HISTORICAL_EVALUATION_READINESS_LEAVES_v1.json`
- `docs/planning/2026-03-30_HISTORICAL_EVALUATION_READINESS_EXECUTION_LOG_v1.md`
- `docs/planning/2026-03-30_HISTORICAL_EVALUATION_READINESS_DOCUMENT_TOUCH_CHECKLIST_v1.md`
- `tests/test_gate115_historical_evaluation_readiness_planning.py`
## Vocabulary discipline

- Existing vocabulary authority was read before naming the tranche and before promoting accepted operator-review ideas into gate titles.
- Carry-forward idea IDs such as `C011` are evidentiary labels only; they are not runtime vocabulary.
- No new runtime term may be introduced during execution without rereading the vocabulary authority and admitting the term if required.
## Packet / contract discipline

- `docs/03_DOMAIN_MODEL.md` remains mandatory reading for any leaf that changes prepared-runtime packet carriage, runtime ingress, execution output, or final review lineage.
- `Gate 115`, `Gate 117`, `Gate 120`, and `Gate 121` are packet-sensitive by default.
- No gate may smuggle a richer upstream source back into a legacy thin compatibility surface unless that collapse is explicit, bounded, and review-visible.
## Document-touch checklist

Checklist file: `docs/planning/2026-03-30_HISTORICAL_EVALUATION_READINESS_DOCUMENT_TOUCH_CHECKLIST_v1.md`
## Testing and promotion discipline

- Repo-local environment required: repo Python environment with pytest available
- Minimum validation slice for this planning pack:
  - `PYTHONPATH=src pytest -q tests/test_gate115_historical_evaluation_readiness_planning.py tests/test_gate114_research_mode_clarity_microtranche.py tests/test_gate113_execution_authority_microtranche.py tests/test_gate112_governance_closeout.py tests/test_gate111_governance_guardrails.py tests/test_document_hygiene.py`
- A gate is not complete until:
  - the gate-specific proof slice runs green;
  - `PLANS.md`, gate map, active leaves ledger, and active execution log move together;
  - a new full-history zip is created from the exact green repo state.
## Gates
### Gate 115: Normalised prepared-runtime features

**Objective**
- Add regime-aware normalised prepared-runtime features so historical evaluation and later threshold logic run on durable cross-regime inputs rather than raw level-heavy transforms.

**Accepted carry-forward idea IDs**
- `C011`

**In-scope surfaces**
- `src/nvda_desk/services/real_data_loader.py`
- `src/nvda_desk/services/chain_to_cognition.py`
- `src/nvda_desk/schemas/dataset.py`
- `fixtures/real_data/*`
- `tests/test_real_data_loader.py`

**Definition of done**
- the canonical normalised feature set is frozen and vocabulary-safe;
- prepared snapshots carry the new normalised fields with provenance and deterministic derivation;
- raw-to-prepared and raw-to-cognition proof surfaces show the new fields survive into the runtime ingress.

### Gate 116: Event-class-specific temporal windows

**Objective**
- Replace generic event countdown handling with event-class-specific temporal windows so macro, company, expiry, and venue-session events do not share one blunt timing law.

**In-scope surfaces**
- `src/nvda_desk/services/temporal_context.py`
- `src/nvda_desk/services/financial_calendar_projection.py`
- `tests/test_gate81_live_event_temporal_semantics.py`
- `tests/test_gate92_financial_calendar_temporal_transition.py`

**Definition of done**
- temporal context uses event-class-specific pre/live/cooling/memory windows;
- next-session-open hints and event timing reasons are calendar-aware rather than generic countdown shortcuts;
- bounded regression tests prove the canonical raw lane still resolves lawfully after the timing-law change.

### Gate 117: Precursor economics through the precursor and market-state path

**Objective**
- Make precursor economics real through the precursor and market-state path instead of leaving projection packets as mostly calendar availability facts.

**In-scope surfaces**
- `src/nvda_desk/services/market_state.py`
- `src/nvda_desk/services/financial_calendar_projection.py`
- `src/nvda_desk/schemas/market.py`
- `tests/test_market_state.py`

**Definition of done**
- raw and derived precursor economics are frozen as explicit precursor fields and slices;
- contradiction-aware precursor packets are computed through the market-state path and flow into downstream runtime posture inputs;
- supportive, hostile, and contradictory precursor fixtures prove downstream posture and review differences.

### Gate 118: Mutable-surface wire-or-shrink reconciliation

**Objective**
- Force the repo to tell the truth about which declared mutable surfaces actually have downstream authority by wiring the missing consumers or shrinking the declared active set.

**Accepted carry-forward idea IDs**
- `C001`

**In-scope surfaces**
- `src/nvda_desk/services/state_conditioned_modifier.py`
- `src/nvda_desk/services/posture_risk.py`
- `src/nvda_desk/services/execution_expression.py`
- `docs/01_NORMATIVE.md`
- `tests/test_gate97_runtime_invariants.py`

**Definition of done**
- every declared mutable surface is mapped either to a live downstream consumer or to a retired-from-authority note;
- runtime policy claims and mutable-surface declarations match actual operative behaviour;
- one regression exists for every surviving mutable surface.

### Gate 119: Candidate adjudication and contradiction resolution

**Objective**
- Replace registry-order lead selection with deterministic candidate adjudication that can resolve multiple live candidates and mixed context coherently.

**Accepted carry-forward idea IDs**
- `C013`
- `C014`

**In-scope surfaces**
- `src/nvda_desk/services/execution_expression.py`
- `src/nvda_desk/services/playbook_eligibility.py`
- `config/playbook_registry.example.yaml`
- `tests/test_gate100_bounded_scenario_matrix.py`

**Definition of done**
- lead selection is scored by explicit adjudication rules rather than ordered-list position alone;
- contradiction and tiebreak behaviour are visible in execution and review outputs;
- multi-eligible scenario fixtures prove the chosen lead is justified by score and reasons rather than registry order.

### Gate 120: Execution geometry enrichment

**Objective**
- Make execution output rich enough to simulate actual order behaviour by adding execution geometry rather than stopping at generic entry style and scaling fractions.

**Accepted carry-forward idea IDs**
- `C004`
- `C006`

**In-scope surfaces**
- `src/nvda_desk/services/execution_expression.py`
- `config/playbook_registry.example.yaml`
- `src/nvda_desk/schemas/contracts.py`
- `tests/test_gate105_ingress_db_api.py`

**Definition of done**
- execution output carries geometry fields for ladder spacing, chase limits, stop geometry, passive-versus-aggressive bias, and hedge guidance;
- execution templates/config surfaces are extended without inventing a parallel execution doctrine;
- scenario tests prove geometry changes with posture, event, and options stress rather than staying static.

### Gate 121: Final risk gateway join

**Objective**
- Make one final risk gateway join authoritative so posture, modifier control law, execution expression, and final risk disposition stop living as parallel permission worlds.

**Accepted carry-forward idea IDs**
- `C009`
- `C001`

**In-scope surfaces**
- `src/nvda_desk/services/cognition_runtime.py`
- `src/nvda_desk/services/risk_gateway.py`
- `src/nvda_desk/services/posture_risk.py`
- `src/nvda_desk/services/review_explanation.py`
- `tests/test_gate103_raw_prepared_parity.py`

**Definition of done**
- the runtime path includes a final risk join after execution synthesis;
- final risk can veto, derisk, or reshape execution output with review-visible lineage;
- legacy-versus-final-join differences are explicit in regression tests rather than implicit in detached services.

