# 2026-03-25 Remaining Ready Import Gate Plan

Status: Active support note for Gate 27 planning reset  
Version: v1.0  
Authority: Subordinate to `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md` and `docs/planning/2026-03-24_CANONICAL_VISION_EXTENSION_LEAVES_v3.json`.

## 0. Purpose

This note freezes the exact partition of the **61** `ready_for_contract_import` canonical items that remain after Gate 23 on the persisted `main` branch.

Gate 27 exists to do three things only:
1. retire the never-leafed Gate 24–26 placeholder rows from the earlier outlook;
2. partition the remaining **61** ready items exactly once across deterministic gates;
3. hand the next executable tranche to the leaf ledger with no orphan items and no overlap.

The source backlog is `docs/planning/2026-03-23_EXECUTABLE_IMPORT_BACKLOG.json`.

## 1. Partition checks

- Ready-for-contract-import source count: **61**
- Closed on `main` through Gate 39: **61**
- Remaining planned from Gate 40 onward: **0**
- Assigned through Gates 28–39: **61**
- Duplicate assignments: **0**
- Unassigned ready items: **0**

## 2. Role mix of the remaining 61

- `expression_execution` — **16**
- `market_regime_context` — **14**
- `options_flow_context` — **9**
- `playbook_eligibility` — **7**
- `posture_risk_permission` — **7**
- `review_explanation` — **7**
- `temporal_context` — **1**

## 3. Gate-by-gate allocation

### Gate 28 — Import remaining-ready ingress substrate contracts *(complete on `main`)*

Bring the temporal flag, spot, macro, peer, VWAP, and realised-volatility ingress substrate into typed contract form.

- Planned item count: **7**
- Entry rule: Gate 27 complete and merged.
- Exit rule: All seven ingress substrate modules exist as typed contract surfaces with explicit external-feed fences and no named-playbook widening.

| Canonical ID | Slug | Grammar role | Priority |
|---|---|---|---|
| `archive-module-006` | `event_flag_capture` | `temporal_context` | `10` |
| `archive-module-001` | `spot_data_capture` | `market_regime_context` | `20` |
| `archive-module-002` | `vwap_accumulator` | `market_regime_context` | `20` |
| `archive-module-008` | `vwap_roc` | `market_regime_context` | `20` |
| `archive-module-007` | `peer_equity_capture` | `market_regime_context` | `20` |
| `archive-module-005` | `macro_data_capture` | `market_regime_context` | `20` |
| `archive-module-009` | `realized_volatility_engine` | `market_regime_context` | `20` |

### Gate 29 — Import remaining-ready market-context synthesis contracts *(complete on `main`)*

Convert the market-context synthesis layer into typed contracts above the ingress substrate.

- Planned item count: **7**
- Entry rule: Gate 28 complete and merged.
- Exit rule: All seven market-context synthesis modules exist as typed contracts with explicit upstream provenance and no execution-chain leakage.

| Canonical ID | Slug | Grammar role | Priority |
|---|---|---|---|
| `archive-module-013` | `macro_signal_score` | `market_regime_context` | `20` |
| `archive-module-014` | `peer_divergence` | `market_regime_context` | `20` |
| `archive-module-018` | `volume_spike_filter` | `market_regime_context` | `20` |
| `legacy-module-006` | `macro_adaptive_weighting_filter` | `market_regime_context` | `20` |
| `legacy-module-008` | `asia_precursor_context_filter` | `market_regime_context` | `20` |
| `archive-module-022` | `engine_score` | `market_regime_context` | `20` |
| `archive-module-052` | `run_signal_scan` | `market_regime_context` | `20` |

### Gate 30 — Import remaining-ready options ingress and primary flow contracts *(complete on `main`)*

Convert the options-capture and primary options-flow analytics layer into typed contracts.

- Planned item count: **7**
- Entry rule: Gate 29 complete and merged.
- Exit rule: All seven options-ingress and primary flow modules exist as typed contracts with explicit chain/metadata/feed fences.

| Canonical ID | Slug | Grammar role | Priority |
|---|---|---|---|
| `archive-module-003` | `options_data_capture` | `options_flow_context` | `30` |
| `archive-module-004` | `options_metadata_capture` | `options_flow_context` | `30` |
| `archive-module-011` | `gamma_pressure` | `options_flow_context` | `30` |
| `archive-module-010` | `iv_vs_rv_analysis` | `options_flow_context` | `30` |
| `archive-module-016` | `skew_inflection` | `options_flow_context` | `30` |
| `archive-module-012` | `vol_corridor` | `options_flow_context` | `30` |
| `archive-module-019` | `vix_spread_detector` | `options_flow_context` | `30` |

### Gate 31 — Import remaining-ready higher-order context composites *(complete on `main`)*

Convert the context-composite and scanner bridge modules that sit above the primary context layers and feed later eligibility decisions.

- Planned item count: **4**
- Entry rule: Gate 30 complete and merged.
- Exit rule: All four higher-order composite modules exist as typed contracts and remain descriptive rather than promotional.

| Canonical ID | Slug | Grammar role | Priority |
|---|---|---|---|
| `legacy-module-005` | `options_behaviour_cluster` | `options_flow_context` | `30` |
| `archive-module-021` | `execution_context_score` | `options_flow_context` | `30` |
| `legacy-module-004` | `compression_regime_detector` | `playbook_eligibility` | `50` |
| `legacy-module-003` | `obv_vi_flow_confirmation` | `playbook_eligibility` | `50` |

### Gate 32 — Import remaining-ready archetype and entry-gate bridge contracts *(complete on `main`)*

Convert the archetype and entry-gate bridge surfaces that open the playbook-eligibility chain.

- Planned item count: **3**
- Entry rule: Gate 31 complete and merged.
- Exit rule: The three bridge modules exist as typed contracts with explicit dependence on upstream context outputs and no new playbook invention.

| Canonical ID | Slug | Grammar role | Priority |
|---|---|---|---|
| `archive-module-020` | `archetype_matcher` | `playbook_eligibility` | `50` |
| `archive-module-048` | `archetype_tagger` | `playbook_eligibility` | `50` |
| `archive-module-023` | `entry_gate` | `playbook_eligibility` | `50` |

### Gate 33 — Import remaining-ready ladder and execution-readiness overlays *(complete on `main`)*

Convert the ladder-construction and execution-readiness overlay modules that prepare expression surfaces without widening into broker truth claims.

- Planned item count: **4**
- Entry rule: Gate 32 complete and merged.
- Exit rule: All four ladder and readiness overlays exist as typed contracts with explicit advisory-only honesty.

| Canonical ID | Slug | Grammar role | Priority |
|---|---|---|---|
| `archive-module-024` | `ladder_constructor` | `playbook_eligibility` | `50` |
| `archive-module-026` | `fill_bias_adjuster` | `playbook_eligibility` | `50` |
| `archive-module-044` | `vvix_ladder_shaper` | `market_regime_context` | `20` |
| `legacy-module-002` | `volatility_sentiment_index` | `posture_risk_permission` | `40` |

### Gate 34 — Import remaining-ready posture and permission core contracts *(complete on `main`)*

Convert the posture and permission core that scores conflicts, model confidence, and conviction before execution.

- Planned item count: **3**
- Entry rule: Gate 33 complete and merged.
- Exit rule: All three posture core modules exist as typed contracts and remain clearly non-approved advisory surfaces.

| Canonical ID | Slug | Grammar role | Priority |
|---|---|---|---|
| `archive-evaluator-eval02` | `signal_conflict_detector` | `posture_risk_permission` | `40` |
| `archive-module-051` | `model_confidence_scorer` | `posture_risk_permission` | `40` |
| `archive-module-043` | `conviction_tier_allocator` | `posture_risk_permission` | `40` |

### Gate 35 — Import remaining-ready execution orchestration core contracts *(complete on `main`)*

Convert the execution-orchestration core while keeping broker and runtime orchestration surfaces dry-run and fenced.

- Planned item count: **6**
- Entry rule: Gate 34 complete and merged.
- Exit rule: All six orchestration modules exist as typed contracts with broker and runtime honesty kept explicit.

| Canonical ID | Slug | Grammar role | Priority |
|---|---|---|---|
| `archive-module-027` | `entry_planner` | `expression_execution` | `60` |
| `archive-module-028` | `position_allocator` | `expression_execution` | `60` |
| `archive-module-029` | `order_simulator` | `expression_execution` | `60` |
| `archive-module-054` | `broker_adapter` | `expression_execution` | `60` |
| `archive-module-053` | `run_trading_bot` | `expression_execution` | `60` |
| `archive-module-050` | `execution_tags` | `expression_execution` | `60` |

### Gate 36 — Import remaining-ready execution state and ledger spine contracts *(complete on `main`)*

Convert the execution-state and ledger spine needed before exits and review surfaces can be imported honestly.

- Planned item count: **4**
- Entry rule: Gate 35 complete and merged.
- Exit rule: All four state-spine modules exist as typed contracts with explicit preview-state honesty.

| Canonical ID | Slug | Grammar role | Priority |
|---|---|---|---|
| `archive-module-030` | `execution_log_writer` | `expression_execution` | `60` |
| `archive-module-031` | `position_book` | `expression_execution` | `60` |
| `archive-module-037` | `trade_logger` | `expression_execution` | `60` |
| `archive-module-032` | `unrealized_tracker` | `expression_execution` | `60` |

### Gate 37 — Import remaining-ready exit, re-entry, and continuity contracts *(complete on `main`)*

Convert the exit, re-entry, and ladder-continuity chain above the execution-state spine.

- Planned item count: **6**
- Entry rule: Gate 36 complete and merged.
- Exit rule: All six exit and continuity modules exist as typed contracts with no booked-fill or live-broker theatre.

| Canonical ID | Slug | Grammar role | Priority |
|---|---|---|---|
| `archive-module-035` | `dynamic_partial_exit_model` | `expression_execution` | `60` |
| `archive-module-034` | `take_profit` | `expression_execution` | `60` |
| `archive-module-033` | `trailing_stop` | `expression_execution` | `60` |
| `archive-module-036` | `trade_reentry_marker` | `expression_execution` | `60` |
| `archive-module-045` | `fill_feedback_router` | `expression_execution` | `60` |
| `archive-module-047` | `ladder_continuity_tracker` | `expression_execution` | `60` |

### Gate 38 — Import remaining-ready review ledger and attribution spine contracts *(complete on `main`)*

Convert the review-ledger and attribution spine that later diagnostics and feedback overlays depend on.

- Planned item count: **4**
- Entry rule: Gate 37 complete and merged.
- Exit rule: All four review-spine modules exist as typed descriptive contracts with explicit preview-ledger honesty.

| Canonical ID | Slug | Grammar role | Priority |
|---|---|---|---|
| `archive-module-039` | `profit_loss_ledger` | `review_explanation` | `70` |
| `archive-module-038` | `module_trace_attribution` | `review_explanation` | `70` |
| `archive-evaluator-eval01` | `module_score_attributor` | `review_explanation` | `70` |
| `archive-module-041` | `daily_summary` | `review_explanation` | `70` |

### Gate 39 — Import remaining-ready review overlays and feedback-chain contracts *(complete on `main`)*

Convert the remaining review overlays, diagnostics, and feedback modules after the review spine is available.

- Planned item count: **6**
- Entry rule: Gate 38 complete and merged.
- Exit rule: All six review-overlay modules exist as typed descriptive contracts and the 61-item remaining-ready backlog is fully exhausted.

| Canonical ID | Slug | Grammar role | Priority |
|---|---|---|---|
| `archive-module-040` | `variant_trace_logger` | `review_explanation` | `70` |
| `archive-evaluator-eval04` | `variant_performance_tracker` | `review_explanation` | `70` |
| `archive-evaluator-eval06` | `feedback_summary_writer` | `review_explanation` | `70` |
| `archive-evaluator-eval03` | `macro_alignment_checker` | `posture_risk_permission` | `40` |
| `archive-evaluator-eval05` | `confidence_divergence_logger` | `posture_risk_permission` | `40` |
| `archive-module-049` | `tail_hedge_injector` | `posture_risk_permission` | `40` |

## 4. Stop rules carried forward

- No named-playbook expansion inside Gates 28–39.
- No live-broker or booked-PnL theatre.
- No silent approval-state promotion.
- No new backlog item may be inserted into this tranche without reopening Gate 27 explicitly.

## 5. Next explicit downstream placeholder

Gate 39 exhausts the remaining-ready programme exactly once. The next downstream placeholder is **Gate 40 — named-playbook expansion programme**.
