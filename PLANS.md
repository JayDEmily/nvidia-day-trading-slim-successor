# PLANS.md

## Purpose

This file is the canonical repo-root execution pointer.

## Active execution control surfaces

The governing canonical gate authority remains:
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`

The active governing pack is self-contained; there is no separate bounded-scope note for the financial-calendar tranche.

The active canonical leaf ledger is:
- `docs/planning/2026-03-29_FINANCIAL_CALENDAR_RUNTIME_INTEGRATION_LEAVES_v2.json`

The active sequential execution log is:
- `docs/planning/2026-03-29_FINANCIAL_CALENDAR_RUNTIME_INTEGRATION_EXECUTION_LOG_v2.md`

Completed predecessor modification pairs retained as in-repo evidence are:
- `docs/planning/2026-03-26_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v1.md`
- `docs/planning/2026-03-26_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v1.json`
- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v6.md`
- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v6.json`

The completed corrective reconstruction pair retained as predecessor evidence is:
- `docs/planning/2026-03-27_REVIEW_RECONSTRUCTION_CORRECTIVE_GATES_v1.md`
- `docs/planning/2026-03-27_REVIEW_RECONSTRUCTION_CORRECTIVE_LEAVES_v1.json`

The predecessor financial-calendar interstitial pack retained as Gate 88–90 evidence is:
- `docs/planning/2026-03-28_FINANCIAL_CALENDAR_INTERSTITIAL_GATES_v3.md`
- `docs/planning/2026-03-28_FINANCIAL_CALENDAR_INTERSTITIAL_LEAVES_v3.json`
- `docs/planning/2026-03-28_FINANCIAL_CALENDAR_INTERSTITIAL_EXECUTION_LOG_v1.md`

The active financial-calendar runtime-integration pack from Gate 91 onward is:
- `docs/planning/2026-03-29_FINANCIAL_CALENDAR_RUNTIME_INTEGRATION_GATES_v2.md`
- `docs/planning/2026-03-29_FINANCIAL_CALENDAR_RUNTIME_INTEGRATION_LEAVES_v2.json`
- `docs/planning/2026-03-29_FINANCIAL_CALENDAR_RUNTIME_INTEGRATION_EXECUTION_LOG_v2.md`
- `docs/planning/2026-03-29_FINANCIAL_CALENDAR_RUNTIME_INTEGRATION_README_v2.md`

`PLANS.md` remains short. Detailed execution logic lives in the planning files above.

## Binding execution status

- Gates 0–7 — completed baseline on `main`
- Gates 8–23 — complete on `main`
- Gates 24–26 — retired superseded planning placeholders (never leafed on the persisted main branch)
- Gate 27 — planning reset complete on `main`
- Gates 28–34 — complete on `main`
- Gates 35–39 — complete on `main`
- Gate 40 — complete on `main`
- Gates 41–44 — complete on `main`
- Gate 45 — retired placeholder on `main`
- Gates 46–50 — complete on `main`
- Gate 51 — complete on `main`
- Gate 52 — complete on `main`
- Gate 53 — complete on `main`
- Gates 54–55 — complete on `main`
- Gates 56–58 — complete on `main`
- Gates 59–79 — complete on `main`
- Gate 80 — complete on `main` (corrective tranche reset and anti-drift freeze)
- Gates 81–86 — complete on `main`
- Gate 87 — complete on `main` (audit-remediation and closeout-integrity sweep)
- Gate 88 — complete on `main` (financial-calendar workflow transition reset, authority disposition, vocabulary freeze, and planning-authority promotion)
- Gate 89 — complete on `main` (canonical crosswalk, retained-field freeze, repo-native DMP v2 reference-bundle lane, and validation proof)
- Gate 90 — complete on `main` (checked-in reference artefacts, repo manifest, provenance-bearing import seam, and non-behavioural proof)
- Gate 91 — complete on `main` (canonical projection into desk-calendar authority, canonical event truth, live-event richness, and precursor runtime surfaces)
- Gate 92 — planned; next active gate on `main` (temporal transition amendment, desk-calendar-aware carry routing, and bounded runtime projection)

## Sequential execution rule

Active work proceeds one leaf at a time, one gate at a time, with the execution log carrying the receipts once execution begins.

## Anti-drift closeout rule

Before any later gate can be treated as active, the closing pass for the current gate must update all of the following together in the same branch: `PLANS.md`, the active gate map, the active leaf ledger, and the active execution log. If any one of those four surfaces still points at an older gate, the gate is not closed. For the active financial-calendar pack, those surfaces are `PLANS.md`, `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`, `docs/planning/2026-03-29_FINANCIAL_CALENDAR_RUNTIME_INTEGRATION_LEAVES_v2.json`, and `docs/planning/2026-03-29_FINANCIAL_CALENDAR_RUNTIME_INTEGRATION_EXECUTION_LOG_v2.md`.

## Current repo state

The persisted `main` baseline is now closed through Gate 79 and records Gate 7 explicitly as baseline leaf `LEAF-G7-BASELINE`. Gates 46–79 are merged on `main`, which means the repo now has:
- the frozen pre-implementation audit in-repo;
- registry-v2 hierarchy with native family/setup-variant lineage;
- formal close-state to carry-horizon handoff for overnight, weekend, and event carry;
- explicit `session_clock` compatibility over canonical `temporal_state`;
- DMP v2 promoted as the canonical live producer surface;
- DMP v1 retired from live runtime dependency and retained only as archived historical context;
- vocabulary governance aligned to family / setup-variant / execution-expression / horizon ownership plus workflow-routing terms such as Step 0 calendar/horizon and carry handoff;
- Gate 59 doctrine rebase complete on `main`, with the V6 pair freezing the successor authority for Gates 60–79 before later corrective follow-on work;
- Gate 60 ontology freeze complete on `main`, with typed state-policy authority now fencing lawful mutable surfaces away from prohibited runtime variation;
- Gate 61 non-action/conflict law complete on `main`, with explicit stand-down, conflict, degradation, and override vocabulary exposed to review surfaces;
- Gate 62 stability/corridor law complete on `main`, with frozen scorecard axes, corridor algebra, persistence, and coverage surfaces exposed as typed contracts;
- Gate 63 review-eligibility law complete on `main`, with governed evidence floors, trigger classes, review outcomes, and bounded change budgets exposed as typed review hooks;
- Gate 64 candidate/adjudication law complete on `main`, with bounded candidate roles, adjudication disposition, and candidate governance hooks frozen before context plumbing;
- Gate 65 canonical event taxonomy complete on `main`, with bounded event classes, semantic phases, materiality tiers, and desk-relevant subclasses frozen before calendar or event-window plumbing;
- Gate 66 desk-calendar authority complete on `main`, with bounded venue/timezone/session/closure/bridge contracts now freezing US, Japan, Hong Kong, and Mainland China session truth before event-window or precursor wiring;
- Gate 67 temporal event-window authority complete on `main`, with bounded proximity/window/overlap/risk-timing/carry-sensitivity semantics now freezing what event timing words actually mean before precursor or posture-policy gates;
- Gate 68 precursor-universe authority complete on `main`, with bounded Asia/ex-US venue families, raw fields, derived fields, and session-alignment expectations now freezing what precursor context may lawfully enter later stitching or policy work;
- Gate 69 phase-and-carryover policy authority complete on `main`, with bounded day-phase states, carry-horizon states, no-action bias, and mutable-surface targeting now freezing ordinary session posture law before event-stress matrices;
- Gate 70 event/options-stress policy authority complete on `main`, with one bounded matrix now freezing imminent/live event risk, event suppression, negative-gamma stress, pin risk, expiry distortion, and explicit non-action boundaries before precedence law;
- Gate 71 modifier-control-law authority complete on `main`, with deterministic precedence, compatible-combination algebra, clamps, vetoes, and kill-switches now freezing how multiple active states resolve before event-source plumbing;
- Gate 72 event-ingestion and provenance authority complete on `main`, with one bounded source inventory and provenance contract now freezing freshness, confidence, conflict visibility, and outage fallback before shared event-store/query work;
- Gate 73 shared event-store/query authority complete on `main`, with one bounded nearby-event/query window, materiality filtering, lineage retrieval, and replay-consumer contract now freezing shared event truth before live cognition binding;
- Gate 74 live-event-richness authority complete on `main`, with bounded event identity, provenance, nearby summaries, and lineage now preserved additively through the live cognition packet;
- Gate 75 precursor stitching authority complete on `main`, with bounded venue ordering, freshness, contradiction, stale/degraded fallback, and pre-policy posture meaning now frozen before runtime packet binding;
- Gate 76 precursor runtime-binding authority complete on `main`, with one additive precursor packet now preserved through prepared runtime snapshots, cognition ingress, and review surfaces;
- Gate 77 review lineage/failure-taxonomy authority complete on `main`, with typed review lineage, failure, accountability, and promotion-evidence packets now frozen before runtime modifier integration;
- Gate 78 runtime modifier integration complete on `main`, with one typed modifier packet now preserving effective coefficients, kill-switches, stand-down outcomes, and modifier lineage through posture, execution, and review;
- Gate 79 walk-forward harness authority complete on `main`, with bounded window-generation, offset-comparison, discovery, fragility, ablation, and downstream-binding contracts now frozen for later testing without starting unconstrained historical search;
- Gate 80 corrective tranche reset complete on `main`, with the corrective reconstruction pair now inserted as the live post-Gate-79 planning surface, the authority docs cleaned, and anti-drift proof added without reopening Gates 59–79;
- Gate 87 audit-remediation closeout complete on `main`, with predecessor-pack evidence, review/runtime projector law, candidate-governance release conditions, widened economic thresholds, and repo-wide static hygiene now aligned with the audited truth state;
- the attached `_v4_5` salvage artefacts preserved in-repo under `docs/legacy/` as provenance only.

The V6 successor pack is closed through Gate 79 on `main`. Corrective review-reconstruction tranche (Gates 80–87) is complete on `main` and retained as predecessor evidence. The financial-calendar interstitial pack is retained as predecessor evidence through Gate 90 on `main`. The active post-Gate-90 planning authority is the financial-calendar runtime-integration pack, with Gate 91 complete on `main` and Gate 92 as the next executable gate on `main`.
