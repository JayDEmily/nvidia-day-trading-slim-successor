# 2026-03-26 DMP v2 Promotion Gates v1

Status: executed and closed through Gate 58 on `main`  
Version: v1.0

## Purpose

This document defines the next bounded planning pack after Gate 55.

It exists to do three things in order:
1. audit and future-proof the DMP v2 protocol against the now-expanded cognitive workflow and the current normative stack;
2. promote DMP v2 to the canonical live producer surface in a bounded, testable tranche;
3. retire DMP v1 only after canonical v2 production is proven and any temporary compatibility shim is no longer needed.

This is intentionally **not** a one-gate "flip everything and pray" plan.

## Position in the planning stack

This pack is the successor to:
- `docs/planning/2026-03-26_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v1.md`
- `docs/planning/2026-03-26_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v1.json`

It is subordinate to:
- `docs/01_NORMATIVE.md`
- `docs/02_OPERATING_MODEL.md`
- `docs/03_DATA_AND_PACKAGING.md`
- `docs/04_ANALYSIS_AND_WORKBENCH.md`
- `docs/05_MULTI_AGENT_RUNTIME.md`
- `AGENTS.md`

It specifically consumes and tests against:
- `docs/planning/2026-03-24_DMP_V1_SPEC.md`
- `docs/planning/2026-03-24_DMP_V2_NORMATIVE_SPEC.md`
- `docs/planning/2026-03-26_DMP_BINDING_SURFACE_DECISION.md`
- `docs/planning/2026-03-26_COGNITIVE_WORKFLOW_UPDATE.md`
- `docs/planning/2026-03-26_COGNITIVE_WORKFLOW_IMPLEMENTATION_MAP.md`
- `docs/planning/2026-03-26_COGNITIVE_WORKFLOW_BOUNDARY_RULES.md`
- `docs/planning/2026-03-26_CALENDAR_HORIZON_OWNERSHIP.md`

## Global tranche rules

1. Gate 56 is a readiness and coherence gate. No DMP v2 producer promotion may begin until Gate 56 passes.
2. Gate 57 may make DMP v2 canonical, but it may not silently delete every v1 surface in the same gate.
3. Gate 58 is the retirement gate. If a v1 compatibility surface is still needed after Gate 57, it must be explicit, temporary, and named.
4. All work remains one gate per branch, one leaf at a time, merge to `main` only after the gate is green.
5. If Gate 56 concludes that DMP v2 is **not yet future-proof**, Gate 57 is blocked and the gate must instead emit a corrected bounded promotion plan.
6. Normative and guardrail docs must agree on what is canonical, what is compatibility-only, and what is archived. If they do not, Gate 56 must resolve that before promotion.
7. Legacy planning artefacts may be archived or stubbed, but must never be deleted without an authoritative pointer.
8. No hidden mixed-mode runtime is allowed after Gate 57. If v1 survives past Gate 57, it must be compatibility-only and proven not to be the canonical producer path.
9. The goal is to avoid any future need for "DMP v3 because we forgot something obvious". Future-proofing is therefore a first-class pass criterion.

## Gate 56 — DMP v2 readiness / future-proof / governance audit

Status: complete on `main`

### Objective

Audit DMP v2, the normative/guardrail stack, AGENTS guidance, and legacy planning surfaces to prove whether DMP v2 is strong enough to become the long-lived canonical protocol without immediate follow-on redesign.

### Why this gate exists

The repo now has richer workflow routing, hierarchy lineage, carry-horizon handoff, and vocabulary governance than it had when DMP v2 was first written. Before promotion, we must prove that the protocol and docs still fit the repo we actually have.

### Scope

- inventory every DMP v1 and v2 producer/consumer surface;
- audit the DMP v2 outer envelope and block model against the current workflow and known near-future modules;
- audit `docs/01`–`docs/05`, `AGENTS.md`, DMP planning docs, and any legacy planning artefacts for contradictions, ambiguity, or stale guidance;
- archive or stub legacy planning docs where needed;
- produce an explicit readiness verdict and exact Gate 57/58 pass criteria.

### Definition of done

A frozen readiness note proves one of two outcomes:
- **promotion-ready**: DMP v2 is future-proof enough to become canonical, and Gate 57 may proceed; or
- **promotion-blocked**: specific bounded issues must be corrected first, with no hand-wavey "we’ll fix it later" language.

## Gate 57 — DMP v2 canonical producer promotion

Status: complete on `main`

### Objective

Make DMP v2 the canonical live producer surface across runtime, imported-module emissions, replay/API-facing packet generation, and canonical tests/fixtures.

### Why this gate exists

The repo cannot carry two indefinitely competing packet contracts without undermining modularity. Once Gate 56 proves readiness, Gate 57 promotes DMP v2 deliberately rather than by drift.

### Scope

- make runtime stage packet emission native-v2 rather than “produce v1, then upgrade”;
- migrate imported-module packet emission to v2-first production;
- migrate fixtures, tests, API/replay surfaces, and docs so v2 is the canonical producer contract;
- if any v1 consumer must temporarily remain, keep a minimal compatibility shim with explicit scope and retirement criteria.

### Definition of done

DMP v2 is the documented and tested canonical producer surface. Any surviving v1 surface is compatibility-only, narrowly scoped, and explicitly temporary.

## Gate 58 — DMP v1 retirement and mixed-mode cleanup

Status: complete on `main`

### Objective

Remove DMP v1 producer codepaths, v1-only fixtures/tests/docs, and mixed-mode ambiguity once Gate 57 proves canonical v2 production.

### Why this gate exists

Gate 57 makes v2 canonical. Gate 58 finishes the job so the repo no longer has two protocols “floating around”.

### Scope

- remove v1 producer codepaths and temporary adapters no longer needed;
- remove or archive v1-only tests, fixtures, and docs;
- update normative/planning/agent docs so they describe only the surviving reality;
- prove that no meaningful runtime dependency still requires DMP v1.

### Definition of done

The repo has one canonical DMP surface: v2. No mixed-mode wording or hidden v1 dependency remains.

## Execution order

1. Gate 56 — readiness/future-proof/governance audit
2. Gate 57 — canonical producer promotion
3. Gate 58 — v1 retirement and cleanup

No later DMP gate may begin until the current gate is complete, validated, and merged.

## Expected outputs

- one gate-specific working branch per gate;
- one gate note and supporting audit/implementation notes per gate;
- one bounded leaf pack with allowed touches and validation commands;
- authoritative archival pointers for any retired planning artefacts;
- explicit pass/fail wording for future-proofing and retirement readiness.
