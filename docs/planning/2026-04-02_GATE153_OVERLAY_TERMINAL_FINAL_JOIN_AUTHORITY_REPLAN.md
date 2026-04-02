# 2026-04-02 Gate 153 Overlay, Terminal-Risk Application, and Final-Join Authority Replan

Status: complete on `main`

## Purpose

Replace the thin Gate 147 planning with deterministic authority law for the downstream risk seam. Gate 153 freezes three things only:
1. the exhaustive overlap-class set currently declared in code;
2. the non-equivalence boundary between overlay evaluation, terminal-risk application, and final join;
3. the honest architecture boundary that keeps this corrective pack in seam-hardening territory rather than pretending it already built an independent parallel risk lane or final arbiter.

## Scope boundary

Gate 153 is planning-only. It does not change runtime semantics, packet carriage, or the declared overlap enum. It freezes the proof burden that later coding leaves must satisfy before they can claim this seam is reconciled.

No new governed vocabulary is admitted in Gate 153.

## Frozen authorities re-read for Gate 153

- `docs/01_NORMATIVE.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/05_GUARDRAILS.md`
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `docs/planning/2026-04-01_GATE147_OVERLAY_EVALUATION_AND_TERMINAL_RISK_APPLICATION.md`
- `docs/planning/2026-04-02_GATE151_FIELD_LEVEL_OWNERSHIP_AND_CONSUMER_MIGRATION.md`
- `docs/planning/2026-04-02_GATE152_STAGE5_STAGE6_AUTHORITY_REPLAN.md`
- `src/nvda_desk/schemas/cognition.py`
- `src/nvda_desk/services/risk_gateway.py`
- `src/nvda_desk/services/cognition_runtime.py`
- `src/nvda_desk/services/review_explanation.py`
- `tests/test_gate147_overlay_terminal_risk_runtime.py`
- `tests/test_gate148_review_trace_replay_runtime.py`
- compatibility-heavy runtime expectation tests that still read `final_risk_join`

## Exhaustive overlap-class table

The current repo declares exactly seven `TerminalRiskOverlapClass` values. Gate 153 freezes that set and the minimum proof obligation for each class.

| Overlap class | Overlay action before terminal application | Posture permission state required on current baseline | Terminal final decision required | Proof outcome later coding must show | Downstream interpretation law |
|---|---|---|---|---|---|
| `overlay_allow_no_terminal_override` | `allow` | not `block`, not `derisk`-forcing | `allow` | prove terminal application preserved overlay permission and final join only recorded compatibility effect | review and bounded trace may show agreement, but must not infer that terminal application and final join are the same object |
| `overlay_derisk_no_terminal_override` | `derisk` | not `block` | `derisk` | prove terminal application preserved overlay derisk decision without posture supersession | downstream readers may treat the final execution effect as derisked, but the authority source remains the overlay decision carried through terminal application |
| `overlay_block_no_terminal_override` | `block` | any posture state that does not supersede the block further | `block` | prove overlay alone can block without a posture-originated supersession class being fabricated | later review must distinguish market-risk or conflict-driven block from posture-originated block |
| `posture_derisk_supersedes_overlay_allow` | `allow` | `derisk` | `derisk` | prove terminal application changed the final decision because posture refused to allow full deployment | downstream readers must attribute the final risk effect to posture authority, not to overlay caution |
| `posture_block_supersedes_overlay_allow` | `allow` | `block` | `block` | prove terminal application blocked an otherwise-allowed overlay outcome because posture was already blocking | final join compatibility may collapse execution to blocked, but the reason source remains posture-over-overlay supersession |
| `posture_block_supersedes_overlay_derisk` | `derisk` | `block` | `block` | prove posture can hard-block even when overlay already derisked | downstream review must not summarise this as mere derisk alignment |
| `posture_block_aligns_with_overlay_block` | `block` | `block` | `block` | prove the aligned block case without erasing the fact that both authorities independently blocked | later readers may report agreement, but must not discard the duplicate authority origin |

**Gate 153 law:** later coding leaves may add runtime tests for additional scenarios, but they may not silently add or remove overlap classes without an explicit receipt-level amendment.

## Overlay, terminal application, and final join non-equivalence matrix

| Surface | What it is authoritative for | What it is not authoritative for | Where it currently lives | Consumer consequence |
|---|---|---|---|---|
| `overlay_risk_decision` | the pure output of `RiskGatewayService.evaluate_overlay(...)`; permission before posture-terminal supersession | final applied execution effect; post-join compatibility state | `stage_local_handoff.overlay_risk_decision`, top-level `review_packet["overlay_risk_decision"]`, bounded trace `overlay_risk_decision` | use when asking what overlay alone decided |
| `terminal_risk_application` | the bounded seam that combines overlay decision with posture permission into the terminal `final_decision` plus `overlap_classes` | mutation of execution payload fields; compatibility wrappers for legacy readers | `stage_local_handoff.terminal_risk_application`, top-level `review_packet["terminal_risk_application"]`, bounded trace `terminal_risk_application` | use when asking why the terminal permission differs or aligns |
| `final_risk_join` | compatibility wrapper created by `apply_final_join(...)` that mutates execution fields after terminal permission is already known | independent arbitration authority; reconstruction of overlay-versus-terminal reasoning by itself | `execution.final_risk_join`, top-level `review_packet["final_risk_join"]`, many legacy runtime tests | use when asking what execution effect was applied for continuity reasons, not when asking who owned the permission decision |

### Agreement-versus-non-equivalence rules

1. `terminal_risk_application.final_decision.action` and `final_risk_join.action` should agree on the current baseline, because final join consumes the terminal decision.
2. Agreement on action does **not** make the surfaces equivalent. `final_risk_join` remains a compatibility wrapper around execution mutation, not a preserved reasoning seam.
3. `overlay_risk_decision.action` may differ lawfully from `terminal_risk_application.final_decision.action` in the exact supersession classes frozen above.
4. `terminal_risk_application` is the only preserved surface that records both the overlay input and the terminal final decision together with the overlap classes.
5. `final_risk_join` may remain visible to downstream review and parity tests while still being compatibility-only.
6. Later review or replay work must not infer independent arbiter semantics from `final_risk_join.lineage_tags` alone.

## Architecture boundary statement

Gate 153 keeps this corrective pack on the seam-hardening side of the boundary.

It does **not** claim that the repo has implemented:
- an independent parallel risk lane;
- a final arbiter that separately audits candidate intent, capital, and exposure before permissioning execution;
- a portfolio-aware replacement engine;
- or a redesigned dynamic-coefficient architecture.

What Gate 153 does claim is narrower and honest:
- the current serial runtime has a preserved overlay decision;
- it has a preserved terminal-risk application seam;
- it still ends in a compatibility-oriented `apply_final_join(...)` mutation path;
- later work may harden interpretation, consumer routing, and compatibility retirement, but that still is not the larger architecture redesign.

## Consequences handed to later gates

- Gate 154 must treat `review_explanation.py`, bounded trace, trace schema, and legacy expectation tests as consumers of **three distinct meanings**, not one blended risk blob.
- Gate 155 must route the deferred larger architecture questions explicitly instead of letting Gate 153 be misread as their closure.
- Gate 156 must verify that the final closeout language still describes `final_risk_join` as compatibility-only and does not silently upgrade it into an arbiter.

## Definition of done recorded by Gate 153

Gate 153 is complete only because the receipt now freezes:
- the exhaustive seven-class overlap table;
- the three-surface non-equivalence matrix;
- the explicit statement that this corrective pack remains seam hardening rather than larger risk-lane redesign.
