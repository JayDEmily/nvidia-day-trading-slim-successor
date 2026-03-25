"""Deterministic replay and stack-comparison harness.

This service replays a checked scenario pack through the Desk Cognition runtime,
applies stack definitions plus coefficient overrides, aggregates stable metrics,
and serialises deterministic comparison reports.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import cast

from nvda_desk.config import Settings
from nvda_desk.schemas.calibration import (
    CoefficientAuditPacket,
    CoefficientSet,
    ComparisonMetrics,
    ComparisonReport,
    ReplayFixturePack,
    ReplayPacketLineage,
    ReplayRunResult,
    ReplayScenarioRecord,
    StackDefinition,
    StackVersusStackSummary,
    WalkForwardSliceDefinition,
)
from nvda_desk.schemas.cognition import (
    InventoryState,
    MarketRegimeContextInput,
    OptionsFlowContextInput,
    OptionsFlowMicroSnapshot,
    PinProgressionPoint,
    ReviewExplanationOutput,
    StrikeClusterObservation,
    TemporalContextInput,
    TenorCurvePoint,
)
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime


class ReplayComparisonService:
    """Run deterministic replay comparisons across explicit stack definitions."""

    def __init__(self, settings: Settings):
        self._runtime = DeskCognitionRuntime(settings)

    def load_stack_definitions(self, path: str | Path) -> dict[str, StackDefinition]:
        """Load stack definitions from a JSON file and index them by stack id."""

        raw = json.loads(Path(path).read_text())
        payload = raw if isinstance(raw, dict) else {"stack_definitions": raw}
        definitions = [StackDefinition.model_validate(item) for item in payload.get("stack_definitions", [])]
        return {definition.stack_id: definition for definition in sorted(definitions, key=lambda item: item.stack_id)}

    def load_fixture_pack(self, path: str | Path) -> ReplayFixturePack:
        """Load a deterministic replay fixture pack from JSON."""

        raw = json.loads(Path(path).read_text())
        return ReplayFixturePack.model_validate(raw)

    def compare_from_fixture_pack(self, path: str | Path) -> tuple[list[ReplayRunResult], ComparisonReport]:
        """Load a fixture pack and run deterministic comparison in one call."""

        fixture_pack = self.load_fixture_pack(path)
        return self.compare(
            fixture_pack_id=fixture_pack.fixture_pack_id,
            scenarios=fixture_pack.scenarios,
            coefficient_sets=fixture_pack.coefficient_sets,
            stack_definitions=fixture_pack.stack_definitions,
            walk_forward_slices=fixture_pack.walk_forward_slices,
        )

    def compare(
        self,
        *,
        fixture_pack_id: str | None,
        scenarios: list[ReplayScenarioRecord],
        coefficient_sets: list[CoefficientSet],
        stack_definitions: list[StackDefinition],
        walk_forward_slices: list[WalkForwardSliceDefinition] | None = None,
    ) -> tuple[list[ReplayRunResult], ComparisonReport]:
        """Run deterministic comparisons and return run-level results plus report."""

        ordered_scenarios = sorted(scenarios, key=lambda item: (item.ts, item.scenario_id))
        ordered_sets = sorted(coefficient_sets, key=lambda item: item.set_id)
        stack_index = {definition.stack_id: definition for definition in sorted(stack_definitions, key=lambda item: item.stack_id)}
        runs: list[ReplayRunResult] = []
        for coefficient_set in ordered_sets:
            stack_definition = stack_index[coefficient_set.stack_id]
            for scenario in ordered_scenarios:
                runs.append(self._run_one(coefficient_set, stack_definition, scenario))

        scenario_ids = [scenario.scenario_id for scenario in ordered_scenarios]
        overall_reports = {
            coefficient_set.set_id: self._aggregate_runs(
                [run for run in runs if run.coefficient_set_id == coefficient_set.set_id]
            )
            for coefficient_set in ordered_sets
        }
        slice_reports: dict[str, dict[str, ComparisonMetrics]] = {}
        for slice_definition in sorted(walk_forward_slices or [], key=lambda item: item.slice_id):
            slice_reports[slice_definition.slice_id] = {
                coefficient_set.set_id: self._aggregate_runs(
                    [
                        run
                        for run in runs
                        if run.coefficient_set_id == coefficient_set.set_id
                        and run.scenario_id in set(slice_definition.scenario_ids)
                    ]
                )
                for coefficient_set in ordered_sets
            }
        stack_vs_stack_summary = self._stack_vs_stack_summary(ordered_sets, overall_reports)
        return runs, ComparisonReport(
            fixture_pack_id=fixture_pack_id,
            scenario_ids=scenario_ids,
            reports=overall_reports,
            slice_reports=slice_reports,
            stack_vs_stack_summary=stack_vs_stack_summary,
        )

    def serialize_report(self, report: ComparisonReport, output_path: str | Path) -> str:
        """Serialise a comparison report to stable JSON and write it to disk."""

        serialised = json.dumps(report.model_dump(mode="json"), indent=2, sort_keys=True)
        Path(output_path).write_text(serialised + "\n")
        return serialised + "\n"

    def _run_one(
        self,
        coefficient_set: CoefficientSet,
        stack_definition: StackDefinition,
        scenario: ReplayScenarioRecord,
    ) -> ReplayRunResult:
        payload = scenario.payload
        applied_module_weights = self._merge_weights(
            stack_definition.module_weights,
            coefficient_set.module_weights,
        )
        applied_sub_coefficients = self._merge_weights(
            stack_definition.sub_coefficients,
            coefficient_set.sub_coefficients,
        )
        temporal_input = TemporalContextInput(
            ts=self._coerce_datetime(payload["ts"]),
            next_expiry=self._optional_datetime(payload.get("next_expiry")),
            next_event_at=self._optional_datetime(payload.get("next_event_at")),
            prior_session_return_pct=self._get_float(payload, "prior_session_return_pct", 0.0),
            intraday_move_pct=self._get_float(payload, "intraday_move_pct", 0.0),
        )
        regime_input = MarketRegimeContextInput(
            nvda_return_pct=self._get_float(payload, "nvda_return_pct"),
            nq_return_pct=self._get_float(payload, "nq_return_pct"),
            es_return_pct=self._get_float(payload, "es_return_pct"),
            sox_return_pct=self._get_float(payload, "sox_return_pct"),
            breadth_score=self._get_float(payload, "breadth_score"),
            concentration_score=self._get_float(payload, "concentration_score"),
            vix_level=self._override_float("vix_level", payload, applied_sub_coefficients, 1.0),
            vvix_level=self._get_float(payload, "vvix_level"),
            us10y=self._get_float(payload, "us10y"),
            us2y=self._get_float(payload, "us2y"),
            usdjpy=self._get_float(payload, "usdjpy"),
        )
        options_input = OptionsFlowContextInput(
            spot_price=self._get_float(payload, "spot_price"),
            front_dte=self._get_int(payload, "front_dte"),
            next_dte=self._get_int(payload, "next_dte"),
            front_atm_iv=self._override_float("front_atm_iv", payload, applied_sub_coefficients, 1.0),
            next_atm_iv=self._get_float(payload, "next_atm_iv"),
            put_call_skew=self._get_float(payload, "put_call_skew"),
            gamma_pressure_score=self._override_float("gamma_pressure_score", payload, applied_sub_coefficients, 1.0),
            call_put_imbalance=self._get_float(payload, "call_put_imbalance"),
            oi_concentration=self._get_float(payload, "oi_concentration"),
            atm_straddle_value=self._get_float(payload, "atm_straddle_value"),
            front_realised_vol=self._get_float(payload, "front_realised_vol", 0.0),
            next_realised_vol=self._get_float(payload, "next_realised_vol", 0.0),
            vix_level=self._override_float("vix_level", payload, applied_sub_coefficients, 1.0),
            vvix_level=self._get_float(payload, "vvix_level", 0.0),
            spot_to_pin_distance_pct=self._get_float(payload, "spot_to_pin_distance_pct", 0.0),
            call_oi_near_spot=self._get_float(payload, "call_oi_near_spot", 0.0),
            put_oi_near_spot=self._get_float(payload, "put_oi_near_spot", 0.0),
            front_volume_near_spot=self._get_float(payload, "front_volume_near_spot", 0.0),
            next_volume_near_spot=self._get_float(payload, "next_volume_near_spot", 0.0),
            vanna_proxy=self._get_float(payload, "vanna_proxy", 0.0),
            charm_proxy=self._get_float(payload, "charm_proxy", 0.0),
            repeated_snapshot_sequence=[
                OptionsFlowMicroSnapshot.model_validate(item)
                for item in cast(list[dict[str, object]], payload.get("repeated_snapshot_sequence", []))
            ],
            tenor_iv_curve=[
                TenorCurvePoint.model_validate(item)
                for item in cast(list[dict[str, object]], payload.get("tenor_iv_curve", []))
            ],
            pin_progression_sequence=[
                PinProgressionPoint.model_validate(item)
                for item in cast(list[dict[str, object]], payload.get("pin_progression_sequence", []))
            ],
            nearby_strike_clusters=[
                StrikeClusterObservation.model_validate(item)
                for item in cast(list[dict[str, object]], payload.get("nearby_strike_clusters", []))
            ],
        )
        runtime_result = self._runtime.run(
            temporal_input=temporal_input,
            regime_input=regime_input,
            options_flow_input=options_input,
            inventory_state=InventoryState.model_validate(payload["inventory_state"]),
            risk_budget_remaining_pct=self._get_float(payload, "risk_budget_remaining_pct"),
            stack_id=stack_definition.stack_id,
            coefficient_set_id=coefficient_set.set_id,
        )
        active_playbook_ids = self._apply_stack_playbook_filter(
            runtime_result.execution.active_playbook_ids,
            stack_definition=stack_definition,
        )
        veto_observed = not active_playbook_ids
        veto_expected = scenario.expectation.expected_veto
        playbook_precision = self._playbook_precision(
            expected_playbooks=scenario.expectation.expected_playbooks,
            active_playbook_ids=active_playbook_ids,
        )
        review_completeness = self._review_completeness(
            expected_stages=scenario.expectation.expected_review_stages,
            runtime_review=runtime_result.review,
        )
        contradiction_count = len(runtime_result.review.contradictions)
        contradiction_rate = round(
            contradiction_count / max(len(scenario.expectation.expected_review_stages), 1),
            4,
        )
        score_components = self._score_components(
            active_playbook_ids=active_playbook_ids,
            permission_state=runtime_result.posture.permission_state.value,
            target_fresh_deployable_pct=runtime_result.execution.target_fresh_deployable_pct,
            applied_module_weights=applied_module_weights,
            applied_sub_coefficients=applied_sub_coefficients,
        )
        replay_score = round(
            score_components["base_capital"]
            * score_components["execution_weight"]
            * score_components["playbook_weight"]
            * score_components["sub_coefficient_scalar"]
            * score_components["permission_scalar"],
            4,
        )
        return ReplayRunResult(
            coefficient_set_id=coefficient_set.set_id,
            stack_id=stack_definition.stack_id,
            scenario_id=scenario.scenario_id,
            permission_state=runtime_result.posture.permission_state.value,
            active_playbook_ids=active_playbook_ids,
            target_fresh_deployable_pct=runtime_result.execution.target_fresh_deployable_pct,
            replay_score=replay_score,
            veto_expected=veto_expected,
            veto_observed=veto_observed,
            veto_correct=1.0 if veto_observed == veto_expected else 0.0,
            contradiction_count=contradiction_count,
            contradiction_rate=contradiction_rate,
            playbook_precision=playbook_precision,
            review_completeness=review_completeness,
            conflict_count=len(runtime_result.review.conflict_tags),
            coefficient_audit=CoefficientAuditPacket(
                stack_id=stack_definition.stack_id,
                enabled_playbooks=stack_definition.enabled_playbooks,
                disabled_playbooks=stack_definition.disabled_playbooks,
                applied_module_weights=applied_module_weights,
                applied_sub_coefficients=applied_sub_coefficients,
                scoring_components=score_components,
            ),
            review=runtime_result.review,
            imported_module_citations=runtime_result.review.imported_module_citations,
            imported_module_maturity_counts=runtime_result.review.imported_module_maturity_counts,
            packet_lineage=ReplayPacketLineage(
                replay_trace_id=(
                    f"replay-trace::{stack_definition.stack_id}::"
                    f"{coefficient_set.set_id}::{scenario.scenario_id}"
                ),
                review_packet_id=runtime_result.stage_packet_ids["review"],
                decision_packet_id=runtime_result.stage_packet_ids["execution"],
                packet_lineage=list(runtime_result.packet_lineage),
                stage_packet_ids=runtime_result.stage_packet_ids,
            ),
        )

    def _aggregate_runs(self, runs: list[ReplayRunResult]) -> ComparisonMetrics:
        if not runs:
            return ComparisonMetrics(
                run_count=0,
                veto_rate=0.0,
                veto_correctness_rate=0.0,
                mean_fresh_deployable_pct=0.0,
                mean_replay_score=0.0,
                mean_contradiction_rate=0.0,
                mean_playbook_precision=0.0,
                review_completeness_rate=0.0,
                active_playbook_rate=0.0,
                mean_active_playbook_count=0.0,
                mean_conflict_count=0.0,
            )
        count = float(len(runs))
        return ComparisonMetrics(
            run_count=len(runs),
            veto_rate=round(sum(1.0 if run.veto_observed else 0.0 for run in runs) / count, 4),
            veto_correctness_rate=round(sum(run.veto_correct for run in runs) / count, 4),
            mean_fresh_deployable_pct=round(sum(run.target_fresh_deployable_pct for run in runs) / count, 4),
            mean_replay_score=round(sum(run.replay_score for run in runs) / count, 4),
            mean_contradiction_rate=round(sum(run.contradiction_rate for run in runs) / count, 4),
            mean_playbook_precision=round(sum(run.playbook_precision for run in runs) / count, 4),
            review_completeness_rate=round(sum(run.review_completeness for run in runs) / count, 4),
            active_playbook_rate=round(sum(1.0 if run.active_playbook_ids else 0.0 for run in runs) / count, 4),
            mean_active_playbook_count=round(sum(float(len(run.active_playbook_ids)) for run in runs) / count, 4),
            mean_conflict_count=round(sum(float(run.conflict_count) for run in runs) / count, 4),
        )

    def _stack_vs_stack_summary(
        self,
        coefficient_sets: list[CoefficientSet],
        reports: dict[str, ComparisonMetrics],
    ) -> list[StackVersusStackSummary]:
        summaries: list[StackVersusStackSummary] = []
        ordered_sets = sorted(coefficient_sets, key=lambda item: item.set_id)
        for index, left in enumerate(ordered_sets):
            for right in ordered_sets[index + 1 :]:
                left_report = reports[left.set_id]
                right_report = reports[right.set_id]
                summaries.append(
                    StackVersusStackSummary(
                        left_set_id=left.set_id,
                        right_set_id=right.set_id,
                        left_stack_id=left.stack_id,
                        right_stack_id=right.stack_id,
                        delta_mean_replay_score=round(left_report.mean_replay_score - right_report.mean_replay_score, 4),
                        delta_veto_correctness_rate=round(
                            left_report.veto_correctness_rate - right_report.veto_correctness_rate,
                            4,
                        ),
                        delta_mean_playbook_precision=round(
                            left_report.mean_playbook_precision - right_report.mean_playbook_precision,
                            4,
                        ),
                        delta_mean_fresh_deployable_pct=round(
                            left_report.mean_fresh_deployable_pct - right_report.mean_fresh_deployable_pct,
                            4,
                        ),
                    )
                )
        return summaries

    def _merge_weights(self, baseline: dict[str, float], overrides: dict[str, float]) -> dict[str, float]:
        merged = dict(sorted(baseline.items()))
        merged.update(dict(sorted(overrides.items())))
        return merged

    def _apply_stack_playbook_filter(
        self,
        active_playbook_ids: list[str],
        *,
        stack_definition: StackDefinition,
    ) -> list[str]:
        filtered = list(active_playbook_ids)
        if stack_definition.enabled_playbooks:
            allowed = set(stack_definition.enabled_playbooks)
            filtered = [playbook_id for playbook_id in filtered if playbook_id in allowed]
        if stack_definition.disabled_playbooks:
            blocked = set(stack_definition.disabled_playbooks)
            filtered = [playbook_id for playbook_id in filtered if playbook_id not in blocked]
        return filtered

    def _playbook_precision(self, *, expected_playbooks: list[str], active_playbook_ids: list[str]) -> float:
        expected = set(expected_playbooks)
        active = set(active_playbook_ids)
        if not expected and not active:
            return 1.0
        if not active:
            return 0.0
        return round(len(expected & active) / len(active), 4)

    def _review_completeness(
        self,
        *,
        expected_stages: list[str],
        runtime_review: ReviewExplanationOutput,
    ) -> float:
        expected = set(expected_stages)
        actual = {packet.stage for packet in runtime_review.stage_reason_packets}
        if not expected:
            return 1.0
        packet_fraction = len(expected & actual) / len(expected)
        packet_present = 1.0 if runtime_review.review_packet else 0.0
        return round(packet_fraction * packet_present, 4)

    def _score_components(
        self,
        *,
        active_playbook_ids: list[str],
        permission_state: str,
        target_fresh_deployable_pct: float,
        applied_module_weights: dict[str, float],
        applied_sub_coefficients: dict[str, float],
    ) -> dict[str, float]:
        playbook_weights = [applied_module_weights.get(playbook_id, 1.0) for playbook_id in active_playbook_ids]
        playbook_weight = sum(playbook_weights) / len(playbook_weights) if playbook_weights else 0.0
        sub_coefficient_scalar = (
            sum(applied_sub_coefficients.values()) / len(applied_sub_coefficients)
            if applied_sub_coefficients
            else 1.0
        )
        permission_scalar = {
            "block": 0.0,
            "derisk": 0.6,
            "allow": 1.0,
        }[permission_state]
        return {
            "base_capital": round(target_fresh_deployable_pct / 100.0, 4),
            "execution_weight": round(applied_module_weights.get("execution_expression", 1.0), 4),
            "playbook_weight": round(playbook_weight, 4),
            "sub_coefficient_scalar": round(sub_coefficient_scalar, 4),
            "permission_scalar": round(permission_scalar, 4),
        }

    def _override_float(
        self,
        field_name: str,
        payload: dict[str, object],
        applied_sub_coefficients: dict[str, float],
        default_weight: float,
    ) -> float:
        weight = applied_sub_coefficients.get(field_name, default_weight)
        return self._get_float(payload, field_name) * weight

    def _get_float(self, payload: dict[str, object], field_name: str, default: float | None = None) -> float:
        value = payload.get(field_name, default)
        if value is None:
            raise TypeError(f"scenario field {field_name} is required")
        return float(cast(float | int | str, value))

    def _get_int(self, payload: dict[str, object], field_name: str) -> int:
        value = payload.get(field_name)
        if value is None:
            raise TypeError(f"scenario field {field_name} is required")
        return int(cast(float | int | str, value))

    def _coerce_datetime(self, value: object) -> datetime:
        if not isinstance(value, str):
            raise TypeError("scenario ts must be an ISO datetime string")
        return datetime.fromisoformat(value)

    def _optional_datetime(self, value: object) -> datetime | None:
        if value is None:
            return None
        return self._coerce_datetime(value)
