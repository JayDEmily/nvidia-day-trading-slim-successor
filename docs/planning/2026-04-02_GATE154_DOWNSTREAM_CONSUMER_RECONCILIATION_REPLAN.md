# 2026-04-02 Gate 154 Downstream Consumer Reconciliation Replan

Status: complete on `main`

## Purpose

Replace the over-broad Gate 148 planning with an exact downstream consumer plan. Gate 154 names the real consumer set, distinguishes direct seam readers from indirect daily-review infrastructure, and freezes the residual compatibility dependencies that later coding must either migrate or defer explicitly.

## Scope boundary

Gate 154 is planning-only. It does not migrate any consumer in code. It freezes the consumer set and the migration/defer law so later execution cannot claim broader review, trace, replay, or legacy reconciliation than the repo has actually touched.

No new governed vocabulary is admitted in Gate 154.

## Frozen authorities re-read for Gate 154

- `docs/01_NORMATIVE.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/05_GUARDRAILS.md`
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `docs/planning/2026-04-01_GATE142_OVERWRITE_AND_OWNERSHIP_INVENTORY.md`
- `docs/planning/2026-04-01_GATE148_REVIEW_TRACE_REPLAY_AND_LEGACY_EXPECTATION_RECONCILIATION.md`
- `docs/planning/2026-04-02_GATE151_FIELD_LEVEL_OWNERSHIP_AND_CONSUMER_MIGRATION.md`
- `docs/planning/2026-04-02_GATE153_OVERLAY_TERMINAL_FINAL_JOIN_AUTHORITY_REPLAN.md`
- `src/nvda_desk/services/review_explanation.py`
- `src/nvda_desk/testing/bounded_trace_review.py`
- `src/nvda_desk/schemas/trace_review.py`
- `src/nvda_desk/services/review_packets.py`
- `src/nvda_desk/api/app.py`
- runtime expectation tests that still read `final_risk_join`, `stage_reason_packets`, or preserved-seam review fields directly

## Exact downstream consumer set

| Consumer | Consumer class | Inputs currently read | Migration verdict now | Notes |
|---|---|---|---|---|
| `ReviewExplanationService.evaluate(...)` top-level review packet | direct review consumer | nested `posture`, `eligibility`, `execution`; top-level `admissibility_surface`, `candidate_ownership`, `overlay_risk_decision`, `terminal_risk_application`, `stage_local_handoff`, and compatibility `final_risk_join` | **migrate in future coding gate** | this is the main direct consumer because it chooses what the operator sees in review packets |
| `ReviewExplanationOutput.stage_reason_packets` | direct review summary consumer | final stage summary still keyed off `execution.final_risk_join` when present | **retain for now, future migrate** | summary packets still end in `final_risk_join`; later work must decide whether a terminal-risk-application stage summary is also required |
| `BoundedTraceRunResult` population in `bounded_trace_review.py` | direct bounded-trace consumer | `eligibility.admissibility_surface`, `execution.candidate_ownership`, `stage_local_handoff.overlay_risk_decision`, `stage_local_handoff.terminal_risk_application`, plus `execution.final_risk_join.action` for `final_risk_action` | **migrate in future coding gate** | bounded trace already reads preserved seams directly but still keeps a compatibility-derived `final_risk_action` field |
| bounded-trace markdown renderer | direct review-like consumer | run-level `admissibility_surface`, `candidate_ownership`, `overlay_risk_decision`, `terminal_risk_application`, `final_risk_action` | **migrate in future coding gate** | rendered narrative can still blur terminal decision and final join unless interpretation law is applied |
| `BoundedTraceRunResult` / `BoundedTraceReviewReport` schema | direct schema consumer | explicit preserved-seam fields plus `final_risk_action` shorthand | **retain schema, future tighten semantics** | field set is already broader than Gate 148 title admitted, but `final_risk_action` stays compatibility-derived |
| `tests/test_gate148_review_trace_replay_runtime.py` | direct legacy expectation consumer | asserts top-level review packet seam fields and compares terminal final decision to `final_risk_join.action` | **retain as legacy parity expectation** | this test is useful evidence but not proof that replay or all legacy consumers were migrated |
| `tests/test_gate121_final_risk_gateway_join.py`, `tests/test_gate103_raw_prepared_parity.py`, `tests/test_gate97_runtime_invariants.py`, `tests/test_gate99_runtime_transitions.py` | direct compatibility expectation consumers | `execution.final_risk_join`, top-level review `final_risk_join`, stage order ending in `final_risk_join` | **retain, explicit compatibility dependency** | these are real downstream consumers and must be named rather than hidden under “legacy expectations” |
| `ReviewPacketService.daily_packet(...)` in `review_packets.py` | indirect daily-review infrastructure | daily account state, positions, pnl, event lists; **no stage-local seam fields** | **defer, no migration required in this pack** | Gate 151 was correct: this service is downstream review infrastructure, not a direct stage-local seam reader |
| `/review/daily-packet` and `/review/module-health/{module_id}` routes in `api/app.py` | indirect API infrastructure | daily-review and module-health packets only; **no stage-local seam fields** | **defer, no migration required in this pack** | mention only to stop later gates from over-claiming API reconciliation |

## Residual compatibility dependency law

| Residual dependency | Where it still appears | Why it is compatibility-only now | Retirement condition |
|---|---|---|---|
| `final_risk_join` as top-level review packet field | `review_explanation.py` and many runtime tests | it records execution effect after terminal permission is already known; Gate 153 froze that it is not independent arbiter authority | later coding may retire or demote it only after preserved terminal-risk fields exist everywhere current readers rely on the shorthand |
| `final_risk_join` as final stage in `stage_reason_packets` | `review_explanation.py`, `tests/test_gate121_final_risk_gateway_join.py`, `tests/test_gate97_runtime_invariants.py` | stage summaries still end on compatibility execution effect rather than preserved terminal seam | retirement requires an explicit replacement summary rule and updated stage-order expectations |
| `BoundedTraceRunResult.final_risk_action` | `bounded_trace_review.py`, markdown renderer, Gate 148 runtime test | shorthand is still populated from `execution.final_risk_join.action` | retirement requires a terminal-risk-native replacement or an explicit rename that preserves operator clarity |
| parity tests comparing terminal action to final join action | Gate 148 runtime tests and parity expectations | these prove continuity, not authority | retirement requires a conscious shift from parity tests to authority-aware assertions |

**Gate 154 law:** a consumer is not "reconciled" merely because preserved-seam fields were exposed nearby. Reconciliation requires that the consumer’s own authoritative inputs and residual compatibility dependencies are named explicitly.

## Honest migration end-state

Gate 154 does **not** claim that replay or every legacy consumer is already migrated.

It claims only this:
- the exact direct consumer set is now named;
- indirect daily-review infrastructure is explicitly separated from true seam readers;
- every residual compatibility dependency now has a retain / migrate / defer verdict and a retirement condition.

That means later coding can proceed honestly, but it still must choose between:
- migrating more consumers to preserved seam surfaces;
- retaining compatibility fields for continuity;
- or deferring specific consumers to a later pack.

## Consequences handed to later gates

- Gate 155 must route follow-on work for compatibility retirement, review-stage semantics, and any deferred replay or expectation work explicitly.
- Gate 156 must confirm the closeout language does not repeat Gate 148’s earlier over-claim that review, trace, replay, and legacy reconciliation are all already done.

## Definition of done recorded by Gate 154

Gate 154 is complete only because the receipt now freezes:
- the exact direct-versus-indirect downstream consumer set;
- the residual compatibility dependency law;
- the honest migration end-state that stops later gates from over-claiming replay or API reconciliation.
