Status: closed research-mode clarity microtranche on `main`; Gate 114 complete, no active gate

# 2026-03-30 Research-Mode Clarity Microtranche Gates v1

## Purpose

Freeze one explicit anti-contamination rule: research and brainstorm mode must seek edge first, while implementation-readiness caveats belong to reporting mode unless the operator asks for readiness.

## Scope

In scope:
- explicit research-versus-reporting wording in the frozen authority docs;
- minimal template-pack wording so future planning threads preserve the same distinction;
- one guard test and honest closeout receipts.

Out of scope:
- runtime logic changes;
- test-harness changes;
- any live-trading or promotion readiness claims.

## Supersession and active authority

- This document became the active gate authority for Gate 114 during execution and is now retained as the latest closed pack evidence.
- It supersedes the absence of any active pack after Gate 113 closeout.

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
- `docs/planning/tranche_briefing_template_pack/README.md`
- `docs/planning/tranche_briefing_template_pack/HOW_TO_USE_THESE_DOCUMENTS.md`

## Workflow placement

This tranche sits above implementation planning and below the frozen strategy/runtime split. It is process-law and operator-behaviour infrastructure that keeps research discussions from being narrowed by current-state caveats unless the operator asks for those judgments.

## Intent and workflow anchor

The binding lens is the human desk operator lens in `docs/01_NORMATIVE.md`: idea generation should still seek edge, while deterministic execution and reporting remain exact and governed.

## Retain / retire-from-authority / amend / add matrix

### Retain as canonical
- `docs/03_DOMAIN_MODEL.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`
- `docs/05_GUARDRAILS.md`

### Retire from authority (compatibility-only unless later removed)
- none

### Mandatory amendments
- `docs/01_NORMATIVE.md` because the research/runtime split needs an explicit anti-contamination rule
- `docs/02_OPERATING_MODEL.md` because GPT research behaviour needs the same rule in the operating loop
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md` because process law must distinguish research-mode ideation from reporting mode
- `AGENTS.md` because operator behaviour should preserve the same distinction
- `docs/planning/tranche_briefing_template_pack/README.md` because planning threads should inherit the same rule
- `docs/planning/tranche_briefing_template_pack/HOW_TO_USE_THESE_DOCUMENTS.md` because brainstorming instructions should say it plainly

### New additions
- `docs/planning/2026-03-30_RESEARCH_MODE_CLARITY_MICROTRANCHE_LEAVES_v1.json`
- `docs/planning/2026-03-30_RESEARCH_MODE_CLARITY_MICROTRANCHE_EXECUTION_LOG_v1.md`
- `docs/planning/2026-03-30_RESEARCH_MODE_CLARITY_MICROTRANCHE_DOCUMENT_TOUCH_CHECKLIST_v1.md`
- `docs/planning/2026-03-30_GATE114_RESEARCH_MODE_CLARITY_CLOSEOUT.md`
- `tests/test_gate114_research_mode_clarity_microtranche.py`

## Vocabulary discipline

- Existing vocabulary authority was read before introducing the tranche title.
- No runtime vocabulary was changed in this tranche.

## Packet / contract discipline

- `docs/03_DOMAIN_MODEL.md` remains mandatory reading but no packet or schema surface changes in this tranche.

## Document-touch checklist

Checklist file: `docs/planning/2026-03-30_RESEARCH_MODE_CLARITY_MICROTRANCHE_DOCUMENT_TOUCH_CHECKLIST_v1.md`

## Testing and promotion discipline

- Repo-local environment required: repo Python environment with pytest available
- Minimum validation slice:
  - `PYTHONPATH=src pytest -q tests/test_gate114_research_mode_clarity_microtranche.py tests/test_gate113_execution_authority_microtranche.py tests/test_gate112_governance_closeout.py tests/test_gate111_governance_guardrails.py tests/test_tranche_briefing_template_pack.py tests/test_document_hygiene.py`
- A gate is not complete until:
  - the validation slice runs green;
  - `PLANS.md`, gate map, active leaves ledger, and active execution log move together;
  - a new full-history zip is created from the exact green repo state.

## Gates

### Gate 114: Research-mode clarity microtranche

**Objective**
- Make the repo authorities say explicitly that research ideation seeks edge first and that implementation-readiness caveats belong to reporting mode unless the operator asks for readiness.

**In-scope surfaces**
- `docs/01_NORMATIVE.md`
- `docs/02_OPERATING_MODEL.md`
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `AGENTS.md`
- `docs/planning/tranche_briefing_template_pack/README.md`
- `docs/planning/tranche_briefing_template_pack/HOW_TO_USE_THESE_DOCUMENTS.md`
- `tests/test_gate114_research_mode_clarity_microtranche.py`

**Definition of done**
- the frozen authority docs carry the explicit research-mode versus reporting-mode distinction;
- the planning quartet agrees the microtranche is closed through Gate 114 on `main`;
- the targeted proof slice runs green and the packaged repo artefact name is frozen in the closeout receipt.
