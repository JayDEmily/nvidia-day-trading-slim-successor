# 2026-03-24 Canonical Vision Gate Map

Status: Active canonical gate authority  
Version: v1.7  
Authority: Subordinate to `docs/01_NORMATIVE.md`; governing gate-level control surface for the active planning stack.  
Paired files:
- `docs/planning/2026-03-24_CANONICAL_VISION_EXTENSION_EXECUTION_PLAN_v3.md` — bounded-scope note only
- `docs/planning/2026-03-24_CANONICAL_VISION_EXTENSION_LEAVES_v3.json` — canonical leaf ledger
- `docs/planning/2026-03-24_CANONICAL_VISION_EXTENSION_EXECUTION_LOG_v3.md` — sequential execution receipts
- `docs/audit/2026-03-25_preimplementation_audit/AUDIT_FINDINGS.md` — frozen audit findings input
- `docs/audit/2026-03-25_preimplementation_audit/AUDIT_PLANNING_INPUT.md` — audit-produced planning consequences

## 0. Purpose

This file is the canonical gate-level control surface for the active planning stack.

It exists to do five things only:
1. record the completed baseline;
2. define the active executable gate;
3. map the active gate to exact leaf IDs;
4. define downstream leafed gates for the next bounded architecture tranche;
5. state the binding gate-entry, gate-exit, and merge rules.

The bounded-scope note explains why the current slice is intentionally narrow.  
The leaf ledger holds leaf-level implementation detail.  
The execution log holds receipts.

## 1. Completed baseline

The repo is already past the rebuild baseline. The gate map begins from that truth rather than replaying it as future work.

| Gate | Status | Meaning now | Evidence surface |
|---|---|---|---|
| Gate 0 | complete on `main` | normative alignment reset and truthful downstream reopening completed | `72a144d` |
| Gates 1–6 | complete on `main` | rebuild baseline exists as historical leaf execution plus the fresh rebuild runtime spine | `docs/planning/2026-03-23_CANONICAL_DESK_REBUILD_*`, fresh rebuild commits `71ad9da`, `c10978d`, `e0af6c4`, `06dacbb`, `e6f8813` |
| Gate 7 | baseline leaf `LEAF-G7-BASELINE` complete on `main` | doctrine freeze, pointer reconciliation, V3 insertion, V3 promotion, and Gate-7 truth amendment completed | `9bc768d`, `04daf33`, `b4846e2`, `ae3e248`, `ec888e9`, `4e7f3b9` |
| Gates 8–23 | complete on `main` | the runtime-spine, registry, tranche-A, substrate, execution-chain, and review-chain imports are closed on the persisted branch | commits `b634dfa` through `85958cc` plus paired receipts in the execution log |
| Gates 24–26 | superseded placeholder rows | these were provisional downstream placeholders only and never received executable leaves on the persisted branch | retired administratively by `LEAF-G27-001` |
| Gate 27 | planning leaf `LEAF-G27-001` complete on `main` | retires the stale placeholder rows and partitions the remaining 61 ready items across Gates 28–39 with exact leaf linkage | `LEAF-G27-001`, `docs/planning/2026-03-25_REMAINING_READY_IMPORT_GATE_PLAN.md` |
| Gates 28–39 | complete on `main` | the remaining-ready contract-import programme is closed in frozen order across ingress substrate, context, bridge, readiness, posture, orchestration, state spine, exit chain, review spine, and feedback overlays | `docs/planning/2026-03-25_GATE28_*` through `docs/planning/2026-03-25_GATE39_*`, paired tests, and receipts in the execution log |
| Gate 40 | `LEAF-G40-001` complete on `main` | replaces the hard clock bucket with signal-aware temporal state while keeping the outward stage payload stable | `docs/planning/2026-03-25_GATE40_TEMPORAL_STATE_REPLACEMENT.md`, `tests/test_temporal_context_signal_state.py` |
| Gates 41–42 | `LEAF-G41-001`, `LEAF-G42-001` complete on `main` | split the signal workbook into raw-versus-derived authority layers and freeze the dense options/raw-baseline capture policy | `docs/planning/2026-03-25_GATE41_RAW_DERIVED_SIGNAL_WORKBOOK.md`, `docs/planning/2026-03-25_GATE42_VOLUME_BASELINE_AND_OPTIONS_RAW_CAPTURE.md`, `docs/planning/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3.xlsx` |
| Gates 43–44 | `LEAF-G43-001`, `LEAF-G44-001` complete on `main` | add the first three options-first playbooks and prove the DMP wrapper remains stable after the temporal/options expansion | `docs/planning/2026-03-25_GATE43_OPTIONS_FIRST_PLAYBOOK_EXPANSION.md`, `docs/planning/2026-03-25_GATE44_DMP_COMPATIBILITY_AND_PLAYBOOK_AUDIT.md`, registry/runtime tests |

Current active gate on the current planning branch: **Gate 46**.

## 2. Active executable gate

One leaf at a time. One gate at a time. Downstream leaves may be planned, but execution must not start until the current gate is complete, logged, and merged.

| Gate | Leaf IDs | Purpose | Entry rule | Exit rule | Next gate |
|---|---|---|---|---|---|
| Gate 46 | `LEAF-G46-001`, `LEAF-G46-002`, `LEAF-G46-003` | freeze the pre-implementation audit into the authoritative tree, retire the Gate 45 placeholder, install the Gate 46–50 planning pack, and add planning-integrity checks | Gate 44 complete on `main`; audit findings exist in a bounded artefact set | audit artefacts live under `docs/audit/2026-03-25_preimplementation_audit/`, the planning quartet points to Gates 46–50, and planning tests prove the pack is coherent | Gate 47 |

## 3. Downstream gate map

The gates below are leafed but not yet executed. They must remain bounded to the audited architecture questions and must not silently widen into speculative runtime invention.

| Gate | Leaf IDs | Planning purpose | Indicative primary surfaces |
|---|---|---|---|
| Gate 47 | `LEAF-G47-001`–`LEAF-G47-005` | replace the flat playbook registry with registry-v2 hierarchy: family, setup variant, execution expression, horizon, and bounded compatibility bridge | `config/playbook_registry.example.yaml`, `docs/planning/2026-03-24_PLAYBOOK_REGISTRY_SPEC.md`, `src/nvda_desk/services/playbook_eligibility.py`, replay fixtures, registry tests |
| Gate 48 | `LEAF-G48-001`–`LEAF-G48-005` | formalise the intraday close-state to carry-horizon handoff for overnight, weekend, and event-carry decisions | `src/nvda_desk/schemas/cognition.py`, `src/nvda_desk/schemas/overnight.py`, `src/nvda_desk/services/carry_replay.py`, carry tests |
| Gate 49 | `LEAF-G49-001`–`LEAF-G49-004` | make an explicit decision about outward `session_clock` compatibility versus `temporal_state`-named surfaces | `src/nvda_desk/schemas/market.py`, `src/nvda_desk/services/market_state.py`, `src/nvda_desk/api/app.py`, `src/nvda_desk/services/replay.py`, legacy tests/docs |
| Gate 50 | `LEAF-G50-001`–`LEAF-G50-005` | rebase vocabulary governance onto the current architecture and enforce canonical labels/aliases | vocabulary workflow import, canonical vocabulary file, enforcement tests, planning/runtime label surfaces |

## 4. Global execution rules

1. One leaf at a time.
2. One gate at a time.
3. The next gate must not begin until the prior gate is complete in the leaf ledger, recorded in the execution log, and merged to `main`.
4. Leaves that touch live runtime behaviour, replay behaviour, or promotion-state surfaces must run the full suite before merge.
5. The gate map governs gate structure only. It does not replace the leaf ledger or execution receipts.
6. The bounded-scope note may explain scope boundaries, but it must not silently override this gate map.
7. Gate 45 is retired as a placeholder and must not be revived as a vague catch-all row.
8. Gate 46 exists to freeze the audit and planning pack only; it must not smuggle in runtime refactors that belong to Gates 47–50.
