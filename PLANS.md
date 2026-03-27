# PLANS.md

## Purpose

This file is the canonical repo-root execution pointer.

## Active execution control surfaces

The governing canonical gate authority remains:
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`

The bounded-scope note remains:
- `docs/planning/2026-03-24_CANONICAL_VISION_EXTENSION_EXECUTION_PLAN_v3.md`

The canonical leaf ledger remains:
- `docs/planning/2026-03-24_CANONICAL_VISION_EXTENSION_LEAVES_v3.json`

The sequential execution log remains:
- `docs/planning/2026-03-24_CANONICAL_VISION_EXTENSION_EXECUTION_LOG_v3.md`

The completed successor modification pair that closed Gates 51–58 remains:
- `docs/planning/2026-03-26_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v1.md`
- `docs/planning/2026-03-26_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v1.json`

The active successor modification pair from Gate 59 onward is:
- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v6.md`
- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v6.json`

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
- Gates 59–74 — complete on `main`

## Sequential execution rule

Active work proceeds one leaf at a time, one gate at a time, with the execution log carrying the receipts once execution begins.

## Anti-drift closeout rule

Before any later gate can be treated as active, the closing pass for the current gate must update all of the following together in the same branch: `PLANS.md`, the active gate map, the active leaf ledger, and the active execution log. If any one of those four surfaces still points at an older gate, the gate is not closed.

## Current repo state

The persisted `main` baseline is now closed through Gate 74 and records Gate 7 explicitly as baseline leaf `LEAF-G7-BASELINE`. Gates 46–74 are merged on `main`, which means the repo now has:
- the frozen pre-implementation audit in-repo;
- registry-v2 hierarchy with native family/setup-variant lineage;
- formal close-state to carry-horizon handoff for overnight, weekend, and event carry;
- explicit `session_clock` compatibility over canonical `temporal_state`;
- DMP v2 promoted as the canonical live producer surface;
- DMP v1 retired from live runtime dependency and retained only as archived historical context;
- vocabulary governance aligned to family / setup-variant / execution-expression / horizon ownership plus workflow-routing terms such as Step 0 calendar/horizon and carry handoff;
- Gate 59 doctrine rebase complete on `main`, with the V6 pair now the single active successor authority for Gates 60–79;
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
- the attached `_v4_5` salvage artefacts preserved in-repo under `docs/legacy/` as provenance only.

The next authored gate is Gate 74 in the V6 successor pack. No missing `v4` or `v5` draft is required to execute that stack.
