Status: active opening-drive continuation lifecycle pilot pack; Gates 135-138 complete on `main`, Gate 139 active
# 2026-04-01 Opening Drive Continuation Lifecycle Pilot Gates v1

## Purpose

Freeze and execute one bounded second-half lifecycle pilot for the canonical `opening_drive_continuation` setup variant and `continuation_ladder_exec` execution expression so the repo stops treating entry geometry plus string-labelled exits as sufficient execution truth.

This pack exists to do five things only:
1. preserve the existing DMP v2 execution-stage envelope and the existing cognition-stage order;
2. add additive execution-stage lifecycle carriage rather than inventing a new hidden side channel;
3. compile the missing second-half lifecycle logic for the continuation specimen only;
4. join that lifecycle output to the already-admitted `carry_handoff` / `carry_horizon_branch` path rather than inventing a second overnight engine;
5. add one bounded position-instance ledger pilot so the repo can manage an actual continuation expression instead of only symbol-level intent.

## Why this pack exists

The repo already selects `opening_drive_continuation`, compiles `continuation_ladder_exec`, and emits bounded entry geometry and thin exit labels. It does not yet own the managed lifecycle of a continuation position in a Tier-1 desk way. The live execution stage still reduces the second half largely to `exit_plan = list(exit_reasons)`, while the carry branch and execution ledger remain too coarse to represent a true managed options-style lifecycle.

This pack is intentionally specimen-first. It does not try to solve every playbook at once. It uses the continuation specimen because the repo already treats it as the canonical lead continuation path and because it exercises the missing seams cleanly: execution-stage carriage, carry nomination, and bounded persistence of a managed position instance.

## Scope

In scope:
- the canonical `opening_drive_continuation` setup variant, its legacy `continuation_ladder` bridge, and the `continuation_ladder_exec` execution expression;
- additive execution-stage contract work inside `ExecutionExpressionInput` / `ExecutionExpressionOutput`;
- lifecycle compilation inside `src/nvda_desk/services/execution_expression.py`;
- lifecycle-aware carry nomination through the existing `carry_handoff` and `carry_horizon_branch` path;
- one bounded position-instance execution ledger pilot sufficient to persist, reconstruct, and review the continuation specimen;
- planning, vocabulary-admission, domain-model, review, and targeted proof surfaces required to keep the repo truthful.

Out of scope:
- broad lifecycle retrofits across all other setup variants or execution expressions;
- broker-specific multi-leg routing, assignment, exercise, or external OMS semantics beyond the bounded pilot ledger;
- live-paper tuning, coefficient-search work, or playbook-eligibility rewrites unrelated to the second-half lifecycle;
- replacing the DMP v2 packet envelope or inventing a second execution-stage transport.

## Supersession and active authority

- This document becomes the active gate authority for Gates 135-139.
- It supersedes the absence of any active pack after Gate 134 closeout.
- It does not supersede the bounded trace scenario review pack as evidence; that pack remains the latest closed semantic-review receipt surface.

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
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- `docs/TESTING_AND_PROMOTION.md`
- `config/playbook_registry.example.yaml`
- `src/nvda_desk/schemas/cognition.py`
- `src/nvda_desk/services/playbook_eligibility.py`
- `src/nvda_desk/services/execution_expression.py`
- `src/nvda_desk/schemas/overnight.py`
- `src/nvda_desk/services/carry_handoff.py`
- `src/nvda_desk/services/carry_market.py`
- `src/nvda_desk/schemas/execution_records.py`
- `src/nvda_desk/db/models.py`
- `src/nvda_desk/services/execution_records.py`
- `src/nvda_desk/services/cognition_runtime.py`
- `tests/test_execution_review_runtime.py`
- `tests/test_gate48_carry_handoff.py`
- `tests/test_gate53_carry_handoff.py`
- `tests/test_runtime_parity_registry_playbooks.py`
- `tests/test_gate50_vocabulary_governance.py`
- `tests/test_gate55_vocabulary_governance.py`

## Active vocabulary authority for execution threads

`docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json` is the mandatory vocabulary authority for every execution leaf in this pack until a later leaf lawfully amends it.

The vocabulary generator and governance tests remain part of that authority whenever a leaf adds or amends governed terms.

## Active packet / data contract authority for execution threads

`docs/03_DOMAIN_MODEL.md` is the mandatory packet/data contract authority for every execution leaf in this pack.

Live schema and service files are implementation surfaces. They must not be treated as a substitute for the domain model when packet meaning, lineage, or lawful downstream consumption is in question.

## Workflow placement

This tranche sits inside Stage 6 of the binding desk cognition grammar: expression and execution. It is downstream of temporal context, regime context, options/flow context, posture permission, playbook eligibility, and candidate adjudication. It is upstream of review and explanation, and it provides the bounded lifecycle signal that the already-admitted carry branch and execution ledger must later consume.

Answer explicitly:
- this tranche is additive execution-stage contract work plus bounded downstream carry and ledger integration;
- later carry review, review explanation, replay, and execution-ledger consumers must consume the lifecycle output and its persisted position-instance truth;
- carry services, review builders, and ledger services must not infer lifecycle state from raw playbook eligibility or from a symbol-only order stream once the new contract exists.

## Pilot tradable-expression discipline

- No execution leaf may silently invent a free-form option structure for this specimen.
- Before lifecycle behaviour broadens beyond thin exit labels, execution must freeze one bounded tradable expression family for the specimen and state its legal lifecycle actions, carry eligibility, and hard-flat semantics.
- Until that freeze exists, no leaf may assume single-leg, vertical, hedge-overlay, or broader multi-leg semantics by implication.

## Intent and workflow anchor

The binding lens remains the human desk cognition chain frozen in `docs/02_OPERATING_MODEL.md`. This pack must not reorder that grammar. It must instead make Stage 6 honest for one specimen:

1. keep the selected setup variant and execution expression as the authoritative entry side;
2. add one typed position context input so the execution stage can reason about a live managed position rather than only a fresh deployable percentage;
3. freeze one bounded tradable expression family and its legal lifecycle action set for the specimen before downstream lifecycle behaviour broadens;
4. add one typed lifecycle plan output so the execution stage emits a governed second-half decision object rather than only thin exit labels;
5. compile the eight ordered lifecycle passes for the continuation specimen;
6. hand late-session lifecycle state into the existing carry path;
7. persist the bounded managed-position state so review and later runtime steps stop guessing what is open.

## Vocabulary anchor for this pack

Canonical terms already admitted and mandatory for this pack:
- `opening_drive_continuation`
- `continuation_ladder_exec`
- `carry_handoff`
- `carry_horizon_branch`
- `expression_execution`

Planning-language only unless a later leaf admits them formally:
- `position_context`
- `lifecycle_plan`
- `position-instance ledger`

The legacy flat playbook label `continuation_ladder` may still appear where the live registry or compatibility bridge already uses it, but it is not the only canonical runtime label for this specimen.

## Retain / retire-from-authority / amend / add matrix

### Retain as canonical
- the DMP v2 execution-stage envelope and stage ordering frozen by `docs/03_DOMAIN_MODEL.md`;
- the existing `opening_drive_continuation` setup-variant to `continuation_ladder_exec` execution-expression mapping;
- the existing `carry_handoff` and `carry_horizon_branch` contract surfaces as the only lawful overnight bridge for this pilot;
- the existing `modifier_runtime_packet`, candidate adjudication, and final-risk join carriage.

### Retire from authority (compatibility-only unless later removed)
- `exit_plan = list(exit_reasons)` as sufficient second-half lifecycle semantics once Gate 137 closes;
- symbol-only execution records as sufficient final execution truth for the continuation specimen once Gate 139 closes;
- `continuation_ladder` as the sole canonical label for this specimen; it remains a live compatibility bridge where existing registry/runtime surfaces still emit it.

### Mandatory amendments
- `PLANS.md` because the repo needs a truthful active pack again;
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md` because Gate 135 must become the active gate and Gates 136-139 must be mapped explicitly;
- `CHANGELOG.jsonl` because a meaningful planning change is being made;
- planning guard tests because the router truth has moved from no active pack to an active lifecycle pilot;
- `docs/03_DOMAIN_MODEL.md` and the vocabulary authority once later gates add new governed contracts or admitted terms.

### New additions
- `docs/planning/2026-04-01_OPENING_DRIVE_CONTINUATION_LIFECYCLE_PILOT_GATES_v1.md`
- `docs/planning/2026-04-01_OPENING_DRIVE_CONTINUATION_LIFECYCLE_PILOT_LEAVES_v1.json`
- `docs/planning/2026-04-01_OPENING_DRIVE_CONTINUATION_LIFECYCLE_PILOT_EXECUTION_LOG_v1.md`
- `docs/planning/2026-04-01_OPENING_DRIVE_CONTINUATION_LIFECYCLE_PILOT_DOCUMENT_TOUCH_CHECKLIST_v1.md`
- `tests/test_gate135_opening_drive_continuation_lifecycle_planning.py`

## Vocabulary discipline

- Existing vocabulary authority must be reread before introducing any new runtime, packet, schema, or planning term in this pack.
- Gates 136-139 may propose `position_context` and `lifecycle_plan`, but those terms do not become governed runtime truth until the vocabulary authority and generator admit them explicitly.
- No leaf may silently promote descriptive prose such as `position lifecycle contract` into a canonical slug without satisfying the vocabulary schema rules.

## Packet / contract discipline

- `docs/03_DOMAIN_MODEL.md` is mandatory reading for any leaf that changes execution-stage carriage, DMP lineage, execution-record schema, carry-handoff packet surfaces, or review/runtime continuity.
- This pack is additive by default. Leaves may enrich execution-stage payload content; they must not replace the DMP v2 envelope, invent a second execution-stage packet, or bypass the existing carry-handoff packet.
- External lifecycle examples remain explanatory only. They do not become repo contract authority by analogy.

## Document-touch checklist

Checklist file: `docs/planning/2026-04-01_OPENING_DRIVE_CONTINUATION_LIFECYCLE_PILOT_DOCUMENT_TOUCH_CHECKLIST_v1.md`

## Testing and promotion discipline

- Repo-local environment required: `.venv` created via `uv sync --extra dev`
- Validation commands in the supporting leaf ledger are written for an installed repo-local `.venv`; they are not permission to rely on `PYTHONPATH=src`.
- Minimum planning validation slice for this pack:
  - `.venv/bin/python -m pytest -q tests/test_gate135_opening_drive_continuation_lifecycle_planning.py tests/test_gate134_bounded_trace_reporting.py tests/test_gate128_post_flight_repo_consistency_planning.py tests/test_gate122_signal_coefficient_authority_planning.py tests/test_gate115_historical_evaluation_readiness_planning.py tests/test_gate114_research_mode_clarity_microtranche.py tests/test_gate113_execution_authority_microtranche.py tests/test_gate112_governance_closeout.py tests/test_gate111_governance_guardrails.py tests/test_gate110_agents_reading_order.py tests/test_gate109_template_pack_governance.py tests/test_gate108_router_only_control_surface.py tests/test_gate107_repo_process_governance.py tests/test_document_hygiene.py`
- A gate is not complete until:
  - the gate-specific proof slice runs green;
  - `PLANS.md`, the gate map, the active leaves ledger, and the active execution log move together;
  - a new full-history zip is created from the exact green repo state when a gate actually closes.

## Gates

### Gate 135: Freeze the specimen, naming, and packet-preservation law

**Status**
- complete on `main`

**Objective**
- Freeze the canonical specimen, preserve the DMP v2 and execution-stage boundaries, define the retain/retire/amend/add matrix, and activate the lifecycle pilot pack truthfully.

**In-scope surfaces**
- `docs/planning/2026-04-01_OPENING_DRIVE_CONTINUATION_LIFECYCLE_PILOT_GATES_v1.md`
- `docs/planning/2026-04-01_OPENING_DRIVE_CONTINUATION_LIFECYCLE_PILOT_LEAVES_v1.json`
- `docs/planning/2026-04-01_OPENING_DRIVE_CONTINUATION_LIFECYCLE_PILOT_EXECUTION_LOG_v1.md`
- `docs/planning/2026-04-01_OPENING_DRIVE_CONTINUATION_LIFECYCLE_PILOT_DOCUMENT_TOUCH_CHECKLIST_v1.md`
- repo-root `PLANS.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- `config/playbook_registry.example.yaml`
- `tests/test_gate135_opening_drive_continuation_lifecycle_planning.py`

**Definition of done**
- the canonical specimen is frozen as `opening_drive_continuation` / `continuation_ladder_exec` with the legacy `continuation_ladder` bridge called out explicitly;
- the pack states clearly that execution-stage enrichment is additive and DMP v2 envelope replacement is out of scope;
- the router, gate map, leaf ledger, and execution log all point truthfully at Gate 135 as the active gate.

### Gate 136: Add additive execution-stage lifecycle contracts

**Status**
- complete on `main`

**Objective**
- Add one bounded execution-stage ingress context and one bounded execution-stage lifecycle plan without breaking packet lineage or review/runtime payload continuity.

**In-scope surfaces**
- `src/nvda_desk/schemas/cognition.py`
- `docs/03_DOMAIN_MODEL.md`
- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`
- `src/nvda_desk/schemas/vocabulary.py`
- `scripts/build_canonical_vocabulary.py`
- `tests/test_execution_review_runtime.py`
- `tests/test_gate50_vocabulary_governance.py`
- `tests/test_gate55_vocabulary_governance.py`

**Definition of done**
- additive execution-stage lifecycle carriage exists in typed schema form;
- one bounded tradable expression family and its legal lifecycle action set are frozen for the specimen before behaviour broadens;
- any required new governed terms are admitted lawfully or explicitly deferred;
- execution-stage payload continuity remains proven without changing the DMP v2 envelope.

### Gate 137: Compile the continuation specimen lifecycle inside expression execution

**Status**
- complete on `main`

**Objective**
- Turn the already-frozen tradable specimen family’s second half into a real lifecycle compiler: normalisation, invalidation, trim, stale-thesis, close-window, carry nomination, and hard-flat handling.

**In-scope surfaces**
- `src/nvda_desk/services/execution_expression.py`
- `config/playbook_registry.example.yaml`
- `src/nvda_desk/services/cognition_runtime.py`
- `tests/test_execution_review_runtime.py`
- `tests/test_runtime_parity_registry_playbooks.py`

**Definition of done**
- the continuation specimen compiles lifecycle decisions from the new position context rather than only copying thin exit labels;
- lifecycle output remains bounded to the continuation specimen and does not silently broaden into every playbook;
- review/runtime proofs show the execution stage now emits lifecycle-aware rationale rather than only entry geometry.

### Gate 138: Integrate lifecycle output with the carry branch

**Status**
- complete on `main`

**Objective**
- Feed lifecycle state into the existing carry path so late-session continuation management becomes an explicit continuation of the same chain rather than a detached parallel decision.

**In-scope surfaces**
- `src/nvda_desk/schemas/overnight.py`
- `src/nvda_desk/services/carry_handoff.py`
- `src/nvda_desk/services/carry_market.py`
- `tests/test_gate48_carry_handoff.py`
- `tests/test_gate53_carry_handoff.py`

**Definition of done**
- lifecycle output nominates carry, carry ceilings, or flatten decisions through the existing `carry_handoff` path;
- carry services consume the richer lifecycle state without inventing a second hidden continuation engine;
- the specimen’s carry truth is review-visible and packet-lineage-safe.

### Gate 139: Add a bounded position-instance ledger and close the pack honestly

**Status**
- active next gate on `main`

**Objective**
- Upgrade the execution ledger just enough to persist and reconstruct one managed continuation position instance, then close the lifecycle pilot pack honestly.

**In-scope surfaces**
- `src/nvda_desk/schemas/execution_records.py`
- `src/nvda_desk/db/models.py`
- `src/nvda_desk/services/execution_records.py`
- `docs/03_DOMAIN_MODEL.md`
- repo-root `PLANS.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`

**Definition of done**
- one bounded position-instance contract exists for the continuation specimen with additive persistence and reconstruction;
- symbol-level order/fill records remain available, but they are no longer the only final truth for this specimen;
- the pack closes honestly through Gate 139 with the planning quartet, execution receipts, and packaging all aligned.
