Status: active repo-process governance pack on `main`; Gates 107-108 complete, Gate 109 next

# 2026-03-30_REPO_PROCESS_GOVERNANCE_GATES_v1.md

## Purpose

Freeze a canonical planning/execution process layer for the repo, clean the live routing surface, canonise the reusable template pack, stabilise `AGENTS.md`, add governance guard tests, and then close the tranche honestly.

## Scope

In scope:
- permanent process-law documentation;
- router-only `PLANS.md` cleanup;
- planning template-pack canonisation;
- stable `AGENTS.md` reading-order refinement;
- governance guard tests;
- honest closeout across the planning quartet.

Out of scope:
- runtime feature work;
- market logic changes;
- schema changes not required for governance truth;
- reopening closed predecessor packs as active authority.

## Supersession and active authority

This document becomes the active gate authority for Gates 107–112.
It supersedes active use of the successor testing pack while retaining that pack as predecessor evidence.

## Governing inputs

- `docs/01_NORMATIVE.md`
- `docs/02_OPERATING_MODEL.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`
- `docs/05_GUARDRAILS.md`
- `docs/TESTING_AND_PROMOTION.md`
- `AGENTS.md`
- `PLANS.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- `docs/planning/tranche_briefing_template_pack/*`
- `tests/test_tranche_briefing_template_pack.py`
- `tests/test_document_hygiene.py`

## Workflow placement

This tranche sits above runtime feature work and above testing-pack execution. It governs how planning artefacts are created, routed, executed, and closed. It must not change runtime semantics directly.

## Intent and workflow anchor

The intent is to stop future work from depending on thread memory. This tranche converts repo process from a remembered habit into a frozen in-repo contract.

## Retain / retire-from-authority / amend / add matrix

### Retain as canonical
- `AGENTS.md` as stable behaviour authority
- repo-root `PLANS.md` as the single live router
- predecessor packs under `docs/planning/` as evidence only

### Retire from authority (compatibility-only unless later removed)
- stale tranche-history narrative embedded in `PLANS.md`
- any implication that closed packs remain active after closeout

### Mandatory amendments
- `docs/01_NORMATIVE.md` because the new process-law document must have explicit precedence
- repo-root `PLANS.md` because it must become a strict router
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md` because it must align with the active governance pack and final closeout
- `docs/planning/tranche_briefing_template_pack/*` because templates must freeze the canonical planning machine, not just the earlier testing tranche vocabulary

### New additions
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `docs/planning/2026-03-30_REPO_PROCESS_GOVERNANCE_LEAVES_v1.json`
- `docs/planning/2026-03-30_REPO_PROCESS_GOVERNANCE_EXECUTION_LOG_v1.md`
- governance integrity tests for the control surfaces

## Testing and promotion discipline

Repo-local environment required: editable install or `PYTHONPATH=src`.
Minimum validation slice for each gate:
- `python -m pytest -q tests/test_document_hygiene.py`
- gate-specific planning/governance tests added by this tranche

A gate is not complete until:
- its targeted proof slice ran green;
- `PLANS.md`, the gate map, the active leaves ledger, and the active execution log moved together if the gate closes;
- a fresh full-history zip exists before the tranche is finally called closed.

## Gates

### Gate 107: Permanent process-law installation and governance-pack activation

**Objective**
- Install the permanent process-law document and make this governance pack the active authority.

**In-scope surfaces**
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `docs/01_NORMATIVE.md`
- `PLANS.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- governance-pack planning trio

**Definition of done**
- the process-law document exists and has explicit precedence;
- the governance pack exists and is the active pack on `main`;
- Gate 108 becomes the next active gate without ambiguity.

### Gate 108: Router-only control-surface cleanup

**Objective**
- Reduce `PLANS.md` to a strict router and align the gate map to the same truth.

**In-scope surfaces**
- `PLANS.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- governance-pack planning trio

**Definition of done**
- `PLANS.md` no longer carries stale tranche diary text;
- the gate map agrees with the router on the active governance gate;
- predecessor evidence remains named without looking active.

### Gate 109: Planning template-pack canonisation

**Objective**
- Make the template pack the canonical source for future gates, leaves, execution logs, and document-touch lists.

**In-scope surfaces**
- `docs/planning/tranche_briefing_template_pack/*`
- `tests/test_tranche_briefing_template_pack.py`
- governance-pack planning trio

**Definition of done**
- the template pack contains gates, leaves, execution-log, and document-touch checklist templates;
- template guidance names the permanent process-law document and router discipline;
- Gate 110 becomes the next active gate.

### Gate 110: `AGENTS.md` stabilisation and reading-order refinement

**Objective**
- Keep `AGENTS.md` stable but explicit about the new process-law layer and router/pack hierarchy.

**In-scope surfaces**
- `AGENTS.md`
- governance-pack planning trio

**Definition of done**
- `AGENTS.md` remains behavioural rather than historical;
- reading order includes the process-law document;
- behaviour authority versus work authority is explicit and coherent.

### Gate 111: Governance guard tests

**Objective**
- Add tests that fail if planning and routing surfaces drift.

**In-scope surfaces**
- new governance tests
- selected older planning tests that need future-proofing
- governance-pack planning trio

**Definition of done**
- tests prove the process-law doc exists and is routed correctly;
- tests prove `PLANS.md` is router-only and coherent with the gate map;
- tests prove the template pack and `AGENTS.md` agree with the canonical process rules.

### Gate 112: Honest governance-tranche closeout

**Objective**
- Close the governance pack honestly across the planning quartet and package the repo from the exact green state.

**In-scope surfaces**
- `PLANS.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- governance-pack leaves and execution log
- closeout doc and packaging artefact

**Definition of done**
- the planning quartet agrees the governance pack is closed through Gate 112 on `main`;
- no stale active-gate sentence remains in the router;
- the packaged repo artefact name is frozen in the closeout receipt.
