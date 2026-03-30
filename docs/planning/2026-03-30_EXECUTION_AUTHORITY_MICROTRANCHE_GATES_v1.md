Status: closed execution-authority microtranche on `main`; Gate 113 complete, no active gate

# 2026-03-30_EXECUTION_AUTHORITY_MICROTRANCHE_GATES_v1.md

## Purpose

Seal one final process-law gap before the historical-data tranche: execution threads must reread the active vocabulary authority and the active packet/data contract authority instead of inventing terms or contract assumptions during implementation.

## Scope

In scope:
- execution-mode reading-order amendments;
- stable `AGENTS.md` reading-order refinement;
- one bounded planning pack proving the authority naming requirement;
- one guard test for authority naming continuity;
- honest closeout across the planning quartet.

Out of scope:
- runtime feature work;
- historical-data ingestion;
- coefficient tuning or candidate comparison;
- reopening closed predecessor packs.

## Supersession and active authority

This document became the active gate authority for Gate 113 during execution and is now retained as the latest closed pack evidence.
It supersedes active use of the repo-process governance pack while retaining that pack as predecessor evidence.

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
- `docs/planning/tranche_briefing_template_pack/*`
- `tests/test_tranche_briefing_template_pack.py`
- `tests/test_gate111_governance_guardrails.py`

## Workflow placement

This microtranche sits between generic governance cleanup and the next historical-data planning pack. It does not change runtime semantics. It tightens the execution-mode reading law so approved future gates must consume the canonical vocabulary and packet/data contract authorities before code changes begin.

## Intent and workflow anchor

The intent is anti-drift. Planning-mode already checked vocabulary and contract authority; execution-mode now does the same explicitly so brainstorm-to-build handoff stays lawful.

## Retain / retire-from-authority / amend / add matrix

### Retain as canonical
- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`
- `docs/03_DOMAIN_MODEL.md`
- `AGENTS.md` as stable behavioural authority
- repo-root `PLANS.md` as the single live router

### Retire from authority (compatibility-only unless later removed)
- implicit execution-mode assumptions about naming and packet authority

### Mandatory amendments
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md` because execution-mode reading must name vocabulary and packet/data contract authorities explicitly
- `AGENTS.md` because the stable reading order must mirror the new execution requirement
- `docs/planning/tranche_briefing_template_pack/*` because planning packs must tell the coding thread to reread those authorities
- repo-root `PLANS.md` and the canonical gate map because the new microtranche must route and close honestly

### New additions
- `docs/planning/2026-03-30_EXECUTION_AUTHORITY_MICROTRANCHE_LEAVES_v1.json`
- `docs/planning/2026-03-30_EXECUTION_AUTHORITY_MICROTRANCHE_EXECUTION_LOG_v1.md`
- `docs/planning/2026-03-30_EXECUTION_AUTHORITY_MICROTRANCHE_DOCUMENT_TOUCH_CHECKLIST_v1.md`
- `tests/test_gate113_execution_authority_microtranche.py`

## Vocabulary discipline

- Execution threads must reread `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json` unless the active gates master admits a narrower vocabulary authority.
- New terms still require admission through the vocabulary governance workflow before merge.

## Packet / contract discipline

- Execution threads must reread `docs/03_DOMAIN_MODEL.md` unless the active gates master admits a narrower packet/data contract authority.
- Contract assumptions must not be reconstructed from memory, stale examples, or convenience.

## Document-touch checklist

- `docs/planning/2026-03-30_EXECUTION_AUTHORITY_MICROTRANCHE_DOCUMENT_TOUCH_CHECKLIST_v1.md`

## Testing and promotion discipline

Repo-local environment required: editable install or `PYTHONPATH=src`.
Minimum validation slice:
- `python -m pytest -q tests/test_gate110_agents_reading_order.py tests/test_gate111_governance_guardrails.py tests/test_gate113_execution_authority_microtranche.py tests/test_tranche_briefing_template_pack.py tests/test_document_hygiene.py`

A gate is not complete until:
- the targeted proof slice ran green;
- `PLANS.md`, the gate map, the active leaves ledger, and the active execution log moved together if the gate closes;
- a fresh full-history zip exists from the exact green repo state.

## Gates

### Gate 113: Execution-authority microtranche

**Objective**
- Make execution-mode reread vocabulary and packet/data contract authorities explicitly mandatory, prove that active packs must name them cleanly, and close the microtranche honestly.

**In-scope surfaces**
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `AGENTS.md`
- `docs/planning/tranche_briefing_template_pack/*`
- repo-root `PLANS.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- microtranche planning trio
- `tests/test_gate113_execution_authority_microtranche.py`

**Definition of done**
- execution-mode reading order names vocabulary and packet/data contract authority explicitly;
- one guard test proves a routed pack cannot omit those authorities cleanly;
- the planning quartet agrees the microtranche is closed through Gate 113 on `main`.
