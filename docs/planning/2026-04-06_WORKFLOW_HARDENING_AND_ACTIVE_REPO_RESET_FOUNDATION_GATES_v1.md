# 2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_GATES_v1

## Purpose

Create the first post-Gate-205 active planning pack so the repo can move from recovery-era closeout into a cleaner GitHub-native planning and execution model without reopening the closed Gate 200-205 successor pack, without changing runtime behaviour under `src/`, and without starting the substantive test-audit or slim-repo cutover work prematurely.

## Scope

In scope:
- planning and routing control surfaces for the next tranche after Gate 205;
- repo workflow-law alignment across `PLANS.md`, `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`, `AGENTS.md`, the canonical gate map, and the tranche template pack;
- planning/evidence taxonomy under `docs/planning/`;
- onboarding/operator guidance in `README.md`;
- operator execution surface guidance in `Makefile`;
- the explicit cutover brief and entry criteria for the later slim active-repo and test-audit work.

Out of scope:
- runtime logic under `src/nvda_desk/`;
- schema, packet, DB, or API changes;
- substantive keep/retire/rewrite decisions for the test inventory;
- creation of the slim successor repo itself;
- any claim that a later coding/evidence tranche has already begun.

## Supersession and active authority

- This document is intended to become the active gate authority for Gate 206 onward.
- It does not reopen the closed target-repo admitted-evidence successor planning pack.
- It supersedes no currently active pack because repo-root `PLANS.md` currently routes no active pack.
- The latest closed pack remains evidence input only:
  - `docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_GATES_v1.md`
  - `docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_LEAVES_v1.json`
  - `docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_EXECUTION_LOG_v1.md`

## Governing inputs

- `docs/01_NORMATIVE.md`
- `docs/02_OPERATING_MODEL.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`
- `docs/05_GUARDRAILS.md`
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `docs/08_TESTING_AND_PROMOTION.md`
- `AGENTS.md`
- repo-root `PLANS.md`
- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- `docs/planning/tranche_briefing_template_pack/README.md`
- `docs/planning/tranche_briefing_template_pack/HOW_TO_USE_THESE_DOCUMENTS.md`
- `docs/planning/tranche_briefing_template_pack/2026-03-29_GENERIC_TRANCHE_BRIEFING_DOCTRINE_v2.md`
- `docs/planning/tranche_briefing_template_pack/2026-03-29_GENERIC_GATE_TEMPLATE_v2.md`
- `docs/planning/tranche_briefing_template_pack/2026-03-29_GENERIC_LEAVES_TEMPLATE_v2.json`
- `docs/planning/tranche_briefing_template_pack/2026-03-30_GENERIC_EXECUTION_LOG_TEMPLATE_v1.md`
- `docs/planning/tranche_briefing_template_pack/2026-03-30_GENERIC_DOCUMENT_TOUCH_CHECKLIST_TEMPLATE_v1.md`
- `README.md`
- `Makefile`

## Workflow placement

This tranche sits between:
1. the closed Gate 200-205 evidence-governance successor pack; and
2. the later slim active-repo cutover plus substantive test-audit work.

It is upstream governance and routing work, not runtime behaviour work.

The chosen gate count is five because the repo currently has five distinct workflow defects or tensions that should not be blurred together:
1. a new pack must be created and routed lawfully;
2. the live router/doctrine surfaces must be consolidated;
3. the template pack must be rewritten to match the GitHub-native workflow law;
4. the planning/evidence tree needs an explicit taxonomy;
5. the operator-facing README/Makefile/cutover boundary must be aligned.

Collapsing those into one or two gates would hide the control-surface intent and make later proof too vague.

Answer explicitly:
- This tranche is upstream workflow and authority infrastructure.
- Later coding and evidence-execution tranches must consume the cleaned router, template pack, and cutover brief.
- No downstream runtime consumer may treat historical closed packs as active authority unless `PLANS.md` routes them explicitly.

## Intent and workflow anchor

The governing repo lens is still: research and planning are upstream of deterministic execution; GitHub history is the primary routine execution ledger; control surfaces must move together; and one active pack at a time remains binding.

This tranche therefore hardens the planning master -> coding executor split without creating a second hidden workflow and without letting recovery-era closeout artefacts remain the de facto operating system for later work.

## Retain / retire-from-authority / amend / add matrix

### Retain as canonical
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `AGENTS.md` as the stable behavioural layer only
- repo-root `PLANS.md` as the router only
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md` as the canonical gate-level control surface
- `docs/08_TESTING_AND_PROMOTION.md`
- the closed Gate 200-205 successor pack as evidence only
- `README.md` as onboarding context only, not the active router

### Retire from authority (compatibility-only unless later removed)
- diary-style historical router markers inside repo-root `PLANS.md`
- stale gate-map prose that still labels the closed 2026-04-05 successor pack as active
- template-pack instructions that make routine zip handoff the default execution model
- any implied assumption that `make test` / `make check` must always mean broad blind execution for planning-governance work

### Mandatory amendments
- repo-root `PLANS.md` because it must become a genuinely short router again
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md` because it still carries stale “active” references and must route Gate 206 onward truthfully
- `AGENTS.md` because it should point to the workflow-law file rather than partially duplicating old process text
- `docs/planning/tranche_briefing_template_pack/*` because the templates still encode a zip-first workflow that conflicts with current repo law
- `README.md` because onboarding should reflect the hardened planning/coding split and the no-active-pack / new-pack-required state model
- `Makefile` because the operator surface should align with bounded proof discipline and should not read as the only lawful test path for every future governance gate

### New additions
- `docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_GATES_v1.md`
- `docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_LEAVES_v1.json`
- `docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_EXECUTION_LOG_v1.md`
- `docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_DOCUMENT_TOUCH_CHECKLIST_v1.md`
- `docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_SCOPE_NOTE_v1.md`
- `docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_CONTRADICTION_REPORT_v1.md`
- a later Gate 210 cutover brief for the slim active-repo successor tranche

## Vocabulary discipline

- The active vocabulary authority must be read before introducing new planning or workflow labels.
- This tranche should avoid inventing new runtime/domain terminology.
- Where possible, it should reuse existing repo-law terms such as `active pack`, `closed pack`, `router`, `execution log`, `document-touch checklist`, `contradiction report`, `evidence input only`, and `GitHub-native execution ledger`.
- Any new term that would affect runtime, review, packets, or durable repo governance must be proposed explicitly before merge.

## Packet / contract discipline

- `docs/03_DOMAIN_MODEL.md` is mandatory baseline reading for this tranche because it names the packet/data contract authority in the absence of an active pack.
- This tranche is governance-only. It must not alter schema shape, packet carriage, lineage contracts, API contracts, or DB contracts.
- If any later gate in this pack discovers a genuine packet/contract mismatch, that mismatch must be recorded as a downstream successor requirement rather than silently folded into this governance pack.

## Contradiction scan and state-integrity rules

The contradiction report for this pack is:
- `docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_CONTRADICTION_REPORT_v1.md`

This pack freezes the following invariants:
- `completed_leaf_ids` and `remaining_leaf_ids` are disjoint;
- every referenced leaf id exists in the leaves ledger;
- `active_gate = none` is lawful only when `remaining_leaf_ids` and `pending_gate_ids` are empty;
- a closed pack must not remain labelled active in any live router surface;
- later-proof tests must permit later valid states or be retired/replaced during closeout.

## Document-touch checklist

The checklist for this tranche is:
- `docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_DOCUMENT_TOUCH_CHECKLIST_v1.md`

## Testing and promotion discipline

- Repo-local environment required: `.venv` via `make install` (`uv sync --extra dev`)
- Minimum validation slice for this governance pack:
  - `python -m pytest -q tests/test_tranche_briefing_template_pack.py`
  - `python -m pytest -q tests/test_gate206_workflow_hardening_pack_planning.py`
  - gate-local targeted governance tests for Gates 207-210 as they are implemented
- Full suite is not the default closeout proof for governance-only gates unless the blast radius expands into runtime or shared code paths.
- A gate is not complete until:
  - the declared targeted tests ran green;
  - `PLANS.md`, the canonical gate map, the active leaves ledger, and the active execution log moved together;
  - GitHub branch/commit/merge receipts are recorded;
  - a zip exists only if the operator explicitly requested backup/offline handoff packaging.

## Gates

### Gate 206: Workflow-hardening pack bootstrap and contradiction freeze

**Objective**
- Create and route the new post-Gate-205 active planning pack, freeze the material contradictions that justify it, and make the repo truthful about the fact that a new planning pack now exists.

**In-scope surfaces**
- `PLANS.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- new Gate 206 pack quartet and support artefacts
- targeted planning tests for Gate 206

**Definition of done**
- the new pack quartet, scope note, and contradiction report exist;
- repo-root `PLANS.md` names this pack as active and no longer claims that no active pack exists;
- the canonical gate map routes Gate 206 as active and stops labelling the closed Gate 200-205 pack as active.

### Gate 207: Router and doctrine consolidation

**Objective**
- Make `PLANS.md`, the canonical gate map, `AGENTS.md`, and `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md` behave as one clean authority stack instead of overlapping partial truth surfaces.

**In-scope surfaces**
- `PLANS.md`
- `AGENTS.md`
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- targeted governance tests

**Definition of done**
- `PLANS.md` is router-only again;
- `AGENTS.md` is behavioural, not quasi-router/process diary;
- stale “active” references or duplicated workflow-law fragments are removed or reduced to evidence-only notes.

### Gate 208: Template-pack GitHub-native rewrite

**Objective**
- Rewrite the tranche template pack so future planning packs inherit the live GitHub-native workflow law instead of the older zip-first execution grammar.

**In-scope surfaces**
- `docs/planning/tranche_briefing_template_pack/*`
- `tests/test_tranche_briefing_template_pack.py`
- any directly coupled planning-template tests

**Definition of done**
- template pack README/how-to/doctrine/gate/leaves/execution-log/checklist surfaces match current repo law;
- routine zip packaging is no longer encoded as mandatory default closeout for ordinary execution;
- template tests prove the updated planning grammar.

### Gate 209: Planning-tree and evidence taxonomy hardening

**Objective**
- Define and document the repo’s planning/evidence taxonomy so active authority, latest closed evidence, and older historical planning material stop blending together conceptually.

**In-scope surfaces**
- `PLANS.md`
- `README.md`
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `docs/planning/` taxonomy notes or companion docs if needed
- targeted governance tests

**Definition of done**
- the repo has one explicit active-vs-evidence taxonomy;
- later readers can distinguish active pack, latest closed evidence, and older historical material without reading chat history;
- no mass archive move is performed unless the taxonomy itself proves it necessary.

### Gate 210: Operator-surface alignment and active-repo cutover criteria

**Objective**
- Align onboarding and operator-facing workflow text with the hardened planning model, and define the exact cutover boundary for the later slim active-repo and substantive test-audit work.

**In-scope surfaces**
- `README.md`
- `Makefile`
- a new cutover brief under `docs/planning/`
- targeted governance/operator-surface tests

**Definition of done**
- `README.md` describes the hardened planning/coding workflow truthfully;
- `Makefile` guidance matches bounded proof discipline rather than implying one blunt default path for all governance work;
- the slim active-repo successor entry criteria are explicit and ready for the next pack.
