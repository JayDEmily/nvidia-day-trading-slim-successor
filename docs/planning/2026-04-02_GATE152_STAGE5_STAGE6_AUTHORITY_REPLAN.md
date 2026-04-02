# 2026-04-02 Gate 152 Stage 5 / Stage 6 Authority Replan

Status: complete on `main`

## Purpose

Replace the thin Gate 146 leafing with explicit Stage 5 admissibility law, Stage 6 candidate-ownership law, and downstream interpretation rules so later coding gates cannot collapse the two stages back into one vague "candidate list" story.

## Scope boundary

Gate 152 is planning-only. It does not change runtime semantics, packet shape, or review rendering.

No new governed vocabulary is admitted in Gate 152.

## Observed code constraints frozen before replanning

- `PlaybookEligibilityService.evaluate(...)` builds the Stage 5 candidate pool, watch-only pool, no-trade reasons, and `EligibilityAdmissibilitySurface`.
- `ExecutionExpressionService.evaluate(...)` consumes the Stage 5 result, adjudicates only `PlaybookDecision.ELIGIBLE` candidates, derives the lead candidate if one exists, and emits `ExecutionCandidateOwnershipSurface`.
- `ExecutionExpressionService._candidate_ownership_surface(...)` copies `admissibility_surface.admissible_playbook_ids` and `watch_only_playbook_ids` when the Stage 5 surface is present; Stage 6 therefore does not invent its own admitted pool on the observed Gate 151 baseline.
- On the observed baseline, a non-empty Stage 6 adjudication always yields `lead_playbook_id = active_playbook_ids[0]`; a no-lead state occurs only for posture-blocked, watch-only, or no-admitted-candidate paths.
- Review and bounded trace already expose both `admissibility_surface` and `candidate_ownership`, but compatibility-heavy nested packets remain present and later gates must interpret them honestly.

The current domain model note in `docs/03_DOMAIN_MODEL.md` remains accurate. Gate 152 adds proof law, not new packet semantics.

## Stage 5 admissibility case table

Stage 5 owns admission, watch status, and no-trade vetoes only. It does **not** own ranking, contradiction resolution, or lead selection.

| Case | Trigger on observed baseline | Stage 5 authoritative outputs | Stage 6 consequence that must remain distinct |
|---|---|---|---|
| Blocked by posture | `posture.permission_state == block` | `admissibility_surface.permission_state = block`; `no_trade_reasons` includes `permission_blocked`; all `admissible_*` collections empty | Stage 6 must return no lead and record that execution was skipped after the posture block rather than pretending a candidate was ranked |
| Blocked by event or venue veto | `_no_trade_reasons(...)` emits `event_window_veto`, `macro_event_window_veto`, `company_event_window_veto`, `expiry_event_window_veto`, `venue_session_distortion`, or `options_surface_event_suppressed` | `admissibility_surface.no_trade_reasons` records the veto family and the admitted pools stay empty | Stage 6 must treat this as no admitted candidate rather than as a watch-only continuation |
| Watch-only, no admission | setup-variant evaluator returns `PlaybookDecision.WATCH_ONLY` such as `leadership_not_clean_enough`, `hostile_flush_context`, `pin_active_but_flow_destabilising`, `compression_ready_but_posture_derisk`, `supportive_options_need_more_confirmation`, `term_structure_dislocation_needs_iv_confirmation`, `skew_reversal_visible_but_posture_derisk`, or `skew_pressure_visible_needs_reversal_confirmation` | `watch_family_ids`, `watch_setup_variant_ids`, and `watch_only_playbook_ids` may be populated while all `admissible_*` pools remain empty | Stage 6 may render watch-only execution scaffolding, but it must not promote a lead candidate from the watch-only pool |
| Single admitted candidate | one or more evaluators return exactly one `PlaybookDecision.ELIGIBLE` path | `admissible_*` pools contain the admitted family, setup-variant, and playbook ids; watch-only pools may still be non-empty separately | Stage 6 may adjudicate and select a lead, but the fact of admission remains Stage 5 truth |
| Multiple admitted candidates | more than one eligible playbook enters the pool, as already shown by Gate 119's multi-candidate adjudication scenarios | Stage 5 stops at the admitted pool and does not rank or tiebreak it | Stage 6 must prove how the admitted pool is ordered, resolved, or left without promotion if the architecture ever changes later |
| No-lead / stand-aside with no admitted candidate | no variant reaches `ELIGIBLE` and the watch-only pool may also be empty | admitted pools empty; watch pools may be empty or non-empty | Stage 6 must distinguish "watch-only but not promoted" from "no admitted candidate exists" instead of flattening both into generic non-action prose |

## Stage 6 candidate-ownership and contradiction proof table

Stage 6 owns ranking, contradiction resolution, and whether the admitted pool yields a lead. It does **not** own the existence of the Stage 5 pool itself.

| Case | Trigger on observed baseline | Stage 6 authoritative outputs | Required proof law for later coding gates |
|---|---|---|---|
| Execution skipped after posture block | Stage 5 is blocked before execution synthesis | `candidate_ownership.lead_playbook_id = None`; `candidate_ownership.notes` includes `execution_skipped_after_posture_block`; adjudication list empty | Must be tested as a Stage 6 no-run path, not a failed ranking path |
| Watch-only candidates not promoted | Stage 5 provides `watch_only_playbook_ids` with no admitted playbook ids | `entry_style = watch_only`; `candidate_ownership.lead_playbook_id = None`; notes include `watch_only_candidates_not_promoted_to_execution` | Must be tested separately from blocked and stand-aside paths |
| Single candidate clear | adjudication length is one | `contradiction_resolution = single_candidate_clear`; one adjudicated playbook; lead is that playbook | Must remain the simplest positive path and not stand in for multi-candidate proof |
| Mixed context resolved by score | more than one candidate is adjudicated and either families, action biases, or contradiction tags differ | `contradiction_resolution = mixed_context_resolved_by_score`; ordered `candidate_adjudication` proves the winner | Must prove score-driven resolution explicitly and not rely on registry order by accident |
| Registry-priority tiebreak | top two adjudicated candidates have equal score | `contradiction_resolution = registry_priority_tiebreak`; lead is the lower registry-priority candidate id | Must be proven separately from score wins |
| Score-ranked candidate pool | more than one candidate exists but the pool is same-family / same-action / no contradiction-tag context | `contradiction_resolution = score_ranked_candidate_pool` | This branch exists in code even if not yet covered by a dedicated runtime receipt; later execution work must either exercise it or explain why it stays unreachable |
| No admitted candidate promoted | Stage 5 admitted pool empty and watch pool empty | `entry_style = stand_aside`; `candidate_ownership.lead_playbook_id = None`; notes include `no_admitted_candidate_promoted` | Must not be collapsed into blocked or watch-only outcomes |

## Stage 5 and Stage 6 agreement-versus-non-equivalence table

| Relationship | Must agree | May differ / must not be inferred | Downstream interpretation rule |
|---|---|---|---|
| Permission gate | Stage 6 must inherit the Stage 5 permission decision; it may not silently reopen a blocked Stage 5 pool | none | `admissibility_surface.permission_state` answers whether the pool was open at all |
| Admitted playbook pool | On the observed baseline, `candidate_ownership.admitted_playbook_ids` is copied from `admissibility_surface.admissible_playbook_ids`; Stage 6 must not invent new admitted ids | ordering and later adjudication metadata may differ | read `admissibility_surface` for membership truth and `candidate_ownership` for what Stage 6 did with that membership |
| Watch-only pool | Stage 6 must inherit the Stage 5 watch-only ids when no admitted pool exists | Stage 6 may add the explicit non-promotion note and watch-only execution scaffolding | read `admissibility_surface.watch_only_playbook_ids` to know what was watch-only; read `candidate_ownership.notes` to know why it was not promoted |
| Ranking and tiebreak | no Stage 5 equivalent exists | `adjudicated_playbook_ids`, `lead_playbook_id`, and `contradiction_resolution` are Stage 6-only truths | later review and trace work must not back-project ranking semantics into Stage 5 |
| No-lead paths | Stage 5 may produce no admitted pool, a watch-only-only pool, or a blocked pool | Stage 6 expresses which non-lead branch actually occurred: blocked, watch-only-not-promoted, or stand-aside | later consumers must not treat all `lead_playbook_id = None` cases as interchangeable |
| Compatibility nested packets | nested `eligibility` and `execution` packets still carry broad compatibility lists | those nested packets are not the bounded authority surfaces by themselves | later consumer migration must prefer top-level `admissibility_surface` and `candidate_ownership` when the question is ownership law rather than legacy packet parity |

## Authoritative versus compatibility-only surfaces after Gate 152

### Authoritative for this boundary

- `EligibilityAdmissibilitySurface`
- `ExecutionCandidateOwnershipSurface`
- `ReviewExplanationOutput.review_packet["admissibility_surface"]`
- `ReviewExplanationOutput.review_packet["candidate_ownership"]`
- `BoundedTraceRunResult.admissibility_surface`
- `BoundedTraceRunResult.candidate_ownership`

### Compatibility-only or broader-than-authority

- Stage 5 compatibility lists such as `add_candidates`, `hold_candidates`, `trim_candidates`, `reduce_candidates`, `hedge_candidates`, `probe_candidates`, `watch_only_candidates`
- broad nested `review_packet["eligibility"]` and `review_packet["execution"]`
- later `final_risk_join` compatibility fields, which answer a different question than Stage 5 / Stage 6 ownership

## Downstream interpretation rules frozen here

1. Ask `admissibility_surface` when the question is "what was admitted or watch-only before Stage 6 ranking?"
2. Ask `candidate_ownership` when the question is "how did Stage 6 adjudicate the admitted pool, or why was nothing promoted?"
3. Do not infer Stage 5 truth from `lead_playbook_id` alone.
4. Do not infer Stage 6 ranking from Stage 5 compatibility lists alone.
5. Treat nested `eligibility` and `execution` packets as compatibility-rich context, not as the sole authority for this boundary.

## Residual-gap handoff to later gates

### Gate 153 input

Gate 153 must treat the Stage 5 / Stage 6 boundary as fixed and then decide how overlay, terminal-risk application, and `final_risk_join` interact without reopening Stage 5 ownership by implication.

### Gate 154 input

Gate 154 must update downstream consumers to read the bounded authority surfaces explicitly where the question is ownership, while preserving compatibility expectations where the question is parity or historical continuity.

### Gate 155 input

Gate 155 must route any future retirement conditions for Stage 5 / Stage 6 compatibility lists so those retirements are explicit and test-backed rather than assumed.

## Gate 152 closeout decision

Gate 152 closes as planning complete because the repo now has:
- explicit Stage 5 case law for blocked, event-veto, watch-only, admitted, multi-candidate, and no-lead states;
- explicit Stage 6 contradiction and non-promotion proof law, including score resolution and registry-priority tiebreaks;
- an agreement-versus-non-equivalence table that tells later review and trace work how to read the two surfaces without conflating them.
