# 2026-04-10_WORKFLOW_LAW_AND_TEMPLATE_PACK_REFRESH_GATES_v1

Status: closed governance refresh pack retained as evidence. Closed through Gate 254 in the prepared handoff workspace copy. No active pack currently routed.

## Purpose

Integrate the available workflow docs refresh bundle into the prepared handoff workspace without regressing the later Gate 253 doctrine baseline refresh. This pack carries forward the controlled-continuity additions into `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`, refreshes the tranche briefing template pack to the 2026-04-06 template generation, records the explicit contradiction between the older workflow-bundle `AGENTS.md` and the newer locked Gate 253 `AGENTS.md`, and leaves the repo in truthful no-active-pack state for Codex to apply against the live GitHub checkout.

## Scope

In scope:
- reconcile the available workflow docs refresh bundle against the prepared Gate 253 workspace state;
- preserve repo-root `AGENTS.md` from Gate 253 because it is later authority and includes the restored `docs/TESTING_AND_PROMOTION.md` read-stack requirement;
- merge the workflow-law continuity additions into `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md` without removing the later checkpoint-integrity/testing-doctrine authority;
- refresh `docs/planning/tranche_briefing_template_pack/` with the 2026-04-06 template generation and continuity worked example;
- update the affected template-pack test coverage and add a bounded Gate 254 reconciliation test;
- update repo-root `PLANS.md`, the canonical gate map, the leaves ledger, the execution log, the contradiction report, the document-touch checklist, and `CHANGELOG.jsonl` together for truthful closeout;
- package the prepared repo handoff for Codex.

Out of scope:
- overwriting Gate 253's locked `AGENTS.md` with the older workflow-bundle `AGENTS.md`;
- altering `docs/01_NORMATIVE.md`;
- touching runtime code, schema code, data fixtures, or retained execution packs beyond the bounded workflow-law/template-pack surfaces;
- treating the runtime delta bundle as repo-tree content.

## Supersession and active authority

- This document is the closed gate authority for the workflow-law and template-pack refresh handoff pack.
- It sits after the doctrine baseline refresh micro-pack closed through Gate 253.
- The contradiction between the workflow-bundle `AGENTS.md` and the later Gate 253 `AGENTS.md` is recorded explicitly in `docs/planning/2026-04-10_WORKFLOW_LAW_AND_TEMPLATE_PACK_REFRESH_CONTRADICTION_REPORT_v1.md` rather than hidden inside a silent overwrite.
- Repo-root `PLANS.md`, the canonical gate map, the leaves ledger, and the execution log now record this pack as closed through Gate 254 with no active pack routed.

## Governing inputs

Frozen doctrine and process:
- `docs/01_NORMATIVE.md`
- `docs/02_OPERATING_MODEL.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`
- `docs/05_GUARDRAILS.md`
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `docs/TESTING_AND_PROMOTION.md`
- `AGENTS.md`
- repo-root `PLANS.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- `CHANGELOG.jsonl`

Available external bundle inputs:
- `/mnt/data/workflow_docs_refresh_bundle_2026-04-06.zip`
- `WORKFLOW_DOCS_REFRESH_INTEGRATION_NOTE.md`
- `repo_updates/docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `repo_updates/docs/planning/tranche_briefing_template_pack/*`
- `external_updates/CHATGPT_OPERATOR_WORKFLOW_SIDE_CAR_2026-04-06_rev2.md`

Prior in-repo authority that remains later than the workflow bundle:
- `docs/planning/2026-04-10_DOCTRINE_BASELINE_REFRESH_FOR_AGENTS_AND_01_NORMATIVE_GATES_v1.md`
- `docs/planning/2026-04-10_DOCTRINE_BASELINE_REFRESH_FOR_AGENTS_AND_01_NORMATIVE_LEAVES_v1.json`
- `docs/planning/2026-04-10_DOCTRINE_BASELINE_REFRESH_FOR_AGENTS_AND_01_NORMATIVE_EXECUTION_LOG_v1.md`

## Gate

### Gate 254: Workflow-law and template-pack refresh for prepared Codex handoff

**Objective**
- Carry forward the workflow bundle's controlled-continuity and template-pack improvements into the prepared handoff workspace while preserving the later Gate 253 doctrine refresh and recording the explicit AGENTS-file contradiction truthfully.

**Leaf coverage**
- `LEAF-G254-001` — reconcile the workflow docs refresh bundle against the prepared Gate 253 workspace, preserve the later `AGENTS.md`, update `docs/06...` plus the template pack and bounded tests, record the contradiction and receipts, and package the prepared repo handoff.

**Definition of done**
- repo-root `AGENTS.md` remains the later Gate 253 version and is not overwritten by the older workflow bundle;
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md` carries the controlled-continuity additions while still naming `docs/TESTING_AND_PROMOTION.md` as live authority;
- the tranche briefing template pack includes the 2026-04-06 template generation and continuity worked example;
- bounded workflow-law/template-pack tests are green;
- repo-root `PLANS.md`, the canonical gate map, the leaf ledger, and the execution log agree that the pack is closed through Gate 254 with no active pack routed;
- `CHANGELOG.jsonl` contains a truthful Gate 254 receipt;
- the prepared handoff package is zipped for Codex.

## Closeout rule

This pack is intentionally one gate and one leaf only. Any later live-repo GitHub mutation work must happen in Codex or another lawful repo execution context rather than being implied by this prepared handoff workspace.
