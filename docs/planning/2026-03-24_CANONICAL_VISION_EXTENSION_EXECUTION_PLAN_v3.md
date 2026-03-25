# 2026-03-24 Canonical Vision Extension Scope Note

Status: Active bounded-scope note  
Version: v6.1 (filename retained for continuity)  
Authority: Subordinate to `docs/01_NORMATIVE.md` and supplementary to `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`. This file is **not** the governing gate authority.  
Baseline: `PLANS.md` records Gates 0 through 23 complete on `main`, Gate 27 complete on `main` as the planning reset, Gates 28 through 39 complete on `main`, and Gates 40 through 44 complete on `main`, with Gate 45 left as the next downstream placeholder only.  
Correction scope: this file now exists to explain scope boundaries only. Exact gate sequencing and gate-to-leaf linkage live in the gate map plus leaf ledger. Gate 40 through Gate 44 are now closed and Gate 45 remains unleafed.

## 0. Purpose

This note explains why the active extension slice is intentionally bounded to the remaining **61** `ready_for_contract_import` canonical items on the persisted `main` branch.

The active executable path is bounded to:
1. one administrative planning reset at Gate 27 that retires the stale Gate 24–26 placeholder rows;
2. one deterministic ingress substrate tranche for temporal, spot, macro, peer, VWAP, and realised-volatility capture;
3. one market-context synthesis tranche above that substrate;
4. one options-ingress and primary flow tranche;
5. one higher-order context-composite tranche;
6. one archetype and entry-gate bridge tranche;
7. one ladder and execution-readiness overlay tranche;
8. one posture and permission core tranche;
9. one execution-orchestration core tranche;
10. one execution-state and ledger-spine tranche;
11. one exit, re-entry, and continuity tranche;
12. one review-ledger and attribution spine tranche;
13. one review-overlay and feedback-chain tranche;
14. an explicit stop point before Gate 40 named-playbook expansion.

Exact gate control now lives in:
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_EXTENSION_LEAVES_v3.json`
- `docs/planning/2026-03-24_CANONICAL_VISION_EXTENSION_EXECUTION_LOG_v3.md`
- `docs/planning/2026-03-25_REMAINING_READY_IMPORT_GATE_PLAN.md`

## 1. Baseline facts

- Gates 0–23 are complete on `main` as the persisted rebuild, registry, substrate, execution-chain, and review-chain baseline.
- Gate 7 is complete on `main` as the doctrine-freeze, pointer-reconciliation, and V3-promotion baseline, and is now recorded explicitly as baseline leaf `LEAF-G7-BASELINE`.
- Gate 27 is complete on `main` as the planning-reset leaf that retires the stale Gate 24–26 placeholder rows and partitions the remaining ready backlog cleanly.
- The current live playbook family is:
  - `continuation_ladder`
  - `compression_breakout`
  - `pin_reversion`
  - `negative_gamma_flush`
- The current stack/config family is:
  - `StackDefinition`
  - `CoefficientSet`
- The source backlog recorded `61` items marked `ready_for_contract_import`; Gates 28 through 39 now close all `61` of them on `main`, leaving `0` items in the remaining-ready tranche.
- The active slice must deepen the runtime without silently widening into named-playbook invention or a second programme.

## 2. Binding doctrine for this bounded slice

1. The trader cognition order remains binding: temporal → regime → options/flow → posture/risk → playbook eligibility → expression/execution → review.
2. Runtime decision-making must remain deterministic and must not depend on an LLM.
3. `StackDefinition` and `CoefficientSet` remain the canonical stack/config surfaces unless a higher-precedence authority renames them everywhere.
4. `DMP` is the internal deterministic packet boundary. `MCP` remains an external AI-tool boundary only.
5. New named playbook expansion must not begin before the 61-item remaining-ready programme is exhausted or intentionally re-planned.
6. Imported modules must not be labelled `approved` or treated as live-trading-ready without the existing promotion evidence rules.
7. Every leaf must end with exact evidence, exact tests or validations, and an honest stop condition.
8. Leaves that touch live runtime behaviour, replay behaviour, or promotion-state surfaces must run the full suite before merge.
9. If a selected item requires live vendor integration, new ontology work, or hidden side-state to continue honestly, execution stops and the item remains fenced.

## 3. Bounded slice summary

The active slice is intentionally narrow:

- **Gate 27 planning reset:** retire stale placeholder rows and freeze the exact Gate 28–39 partition.
- **Gate 28:** complete the ingress substrate tranche.
- **Gate 29:** complete the market-context synthesis tranche.
- **Gate 30:** complete the options-ingress and primary-flow tranche.
- **Gate 31:** complete on `main`; higher-order context composites now proven in frozen order.
- **Gates 32–34:** complete on `main`; archetype/entry bridges, readiness overlays, and posture core now proven in frozen order.
- **Gates 35–39:** complete on `main`; the orchestration core, state spine, exit chain, review spine, and final feedback-overlay tranche are now proven in frozen order.
- **Gate 40:** next downstream placeholder only; named-playbook expansion remains explicitly out of scope until a new planning decision is made.

This note does **not** govern the exact gate split. The gate map does that.  
This note does **not** reopen the 32 `needs_scope_definition` items. Those remain outside this remaining-ready tranche.  
This note does **not** authorise named-playbook expansion. Gate 40 remains a downstream placeholder only.

## 4. What this note deliberately does not do

This note must not:
- override the gate map;
- duplicate the full leaf ledger;
- imply that the remaining 61 items are already implemented;
- turn historical archive hygiene into forward implementation;
- smuggle the 32 scope-definition items or named-playbook invention into the current tranche.

## 5. Paired planning surfaces

Use the files below together:

1. `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md` — governing gate authority
2. `docs/planning/2026-03-24_CANONICAL_VISION_EXTENSION_LEAVES_v3.json` — leaf-level implementation ledger
3. `docs/planning/2026-03-24_CANONICAL_VISION_EXTENSION_EXECUTION_LOG_v3.md` — execution receipts
4. `docs/planning/2026-03-24_CANONICAL_VISION_EXTENSION_EXECUTION_PLAN_v3.md` — this bounded-scope note
5. `docs/planning/2026-03-25_REMAINING_READY_IMPORT_GATE_PLAN.md` — exact Gate 28–39 item partition
