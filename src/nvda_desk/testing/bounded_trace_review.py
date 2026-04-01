"""Helpers for bounded real-data sibling scenario review.

This module turns one small checked-in sibling-scenario pack into deterministic
runtime traces and a simple human-readable report. The outputs are semantic
review evidence only. They do not become runtime authority or tuning evidence
on their own.
"""

from __future__ import annotations

import json
from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.schemas.trace_review import (
    BoundedTraceFixturePack,
    BoundedTraceReviewReport,
    BoundedTraceRunResult,
)
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.testing.canonical_runtime_harness import CanonicalRuntimeHarnessService


class BoundedTraceReviewService:
    """Load bounded trace scenarios, run the runtime, and render a compact report."""

    def __init__(self, settings: Settings):
        self._runtime = DeskCognitionRuntime(settings)
        self._harness = CanonicalRuntimeHarnessService()

    def load_fixture_pack(self, path: str | Path) -> BoundedTraceFixturePack:
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        return BoundedTraceFixturePack.model_validate(raw)

    def run_fixture_pack(self, path: str | Path) -> BoundedTraceReviewReport:
        pack = self.load_fixture_pack(path)
        runs = [self._run_one(pack, scenario) for scenario in pack.scenarios]
        narrative = [
            f"{run.scenario_id}: permission={run.permission_state}; playbooks={run.active_playbook_ids or ['none']}; final_risk={run.final_risk_action or 'none'}; deploy={run.target_fresh_deployable_pct:.4f}; overlay={(run.overlay_risk_decision.action.value if run.overlay_risk_decision is not None else 'none')}; terminal={(run.terminal_risk_application.final_decision.action.value if run.terminal_risk_application is not None else 'none')}"
            for run in runs
        ]
        return BoundedTraceReviewReport(
            pack_id=pack.pack_id,
            scenario_ids=pack.scenario_ids,
            runs=runs,
            narrative_summary=narrative,
        )

    def serialize_report(self, report: BoundedTraceReviewReport, path: str | Path) -> str:
        serialised = json.dumps(report.model_dump(mode="json"), indent=2, sort_keys=True)
        Path(path).write_text(serialised + "\n", encoding="utf-8")
        return serialised + "\n"

    def render_markdown_report(self, report: BoundedTraceReviewReport) -> str:
        lines = [
            "# Bounded Trace Scenario Review",
            "",
            f"Pack: `{report.pack_id}`",
            "",
            "| Scenario | Desk window | Event window | Permission | Playbooks | Final risk | Deploy % | Human read |",
            "| --- | --- | --- | --- | --- | --- | ---: | --- |",
        ]
        for run in report.runs:
            playbooks = ", ".join(run.active_playbook_ids) if run.active_playbook_ids else "none"
            lines.append(
                f"| {run.scenario_id} | {run.desk_window} | {run.event_window_state} | {run.permission_state} | {playbooks} | {run.final_risk_action or 'none'} | {run.target_fresh_deployable_pct:.4f} | {run.expected_human_read} |"
            )
        lines.append("")
        lines.append("## Simplified narrative")
        lines.append("")
        for line in report.narrative_summary:
            lines.append(f"- {line}")
        lines.append("")
        lines.append("## Preserved seam snapshot")
        lines.append("")
        for run in report.runs:
            admitted = (
                ", ".join(run.admissibility_surface.admissible_playbook_ids)
                if run.admissibility_surface is not None and run.admissibility_surface.admissible_playbook_ids
                else "none"
            )
            lead_owner = (
                run.candidate_ownership.lead_playbook_id
                if run.candidate_ownership is not None and run.candidate_ownership.lead_playbook_id is not None
                else "none"
            )
            overlay = run.overlay_risk_decision.action.value if run.overlay_risk_decision is not None else "none"
            terminal = (
                run.terminal_risk_application.final_decision.action.value
                if run.terminal_risk_application is not None
                else "none"
            )
            lines.append(
                f"- {run.scenario_id}: admitted={admitted}; lead_owner={lead_owner}; overlay={overlay}; terminal={terminal}"
            )
        lines.append("")
        return "\n".join(lines)

    def _run_one(self, pack: BoundedTraceFixturePack, scenario) -> BoundedTraceRunResult:
        harness = self._harness.build(
            dataset_id=pack.pack_id,
            snapshot=scenario.prepared_snapshot,
            regime_input=scenario.regime_input,
            inventory_state=scenario.inventory_state,
            risk_budget_remaining_pct=scenario.risk_budget_remaining_pct,
            fixture_id=scenario.scenario_id,
        )
        result = self._runtime.run(
            temporal_input=harness.temporal_input,
            regime_input=harness.regime_input,
            options_flow_input=harness.options_flow_input,
            inventory_state=harness.inventory_state,
            risk_budget_remaining_pct=harness.risk_budget_remaining_pct,
        )
        effective_surfaces: dict[str, float | bool | None] = {}
        resolved_surfaces = (
            result.review.effective_policy.resolved_surfaces
            if result.review.effective_policy is not None
            else []
        )
        for resolved in resolved_surfaces:
            key = resolved.target_surface.value if hasattr(resolved.target_surface, 'value') else str(resolved.target_surface)
            if resolved.effective_numeric_value is not None:
                effective_surfaces[key] = resolved.effective_numeric_value
            else:
                effective_surfaces[key] = resolved.effective_boolean_value
        return BoundedTraceRunResult(
            scenario_id=scenario.scenario_id,
            desk_window=result.temporal.desk_window,
            event_window_state=result.temporal.event_window_state,
            event_minutes_remaining=result.temporal.event_minutes_remaining,
            options_behavior_cluster=result.options_flow.options_behavior_cluster,
            permission_state=result.posture.permission_state.value,
            active_playbook_ids=result.execution.active_playbook_ids,
            final_risk_action=(result.execution.final_risk_join.action.value if result.execution.final_risk_join is not None else None),
            target_fresh_deployable_pct=result.execution.target_fresh_deployable_pct,
            effective_surfaces=effective_surfaces,
            admissibility_surface=result.eligibility.admissibility_surface,
            candidate_ownership=result.execution.candidate_ownership,
            overlay_risk_decision=(
                result.stage_local_handoff.overlay_risk_decision
                if result.stage_local_handoff is not None
                else None
            ),
            terminal_risk_application=(
                result.stage_local_handoff.terminal_risk_application
                if result.stage_local_handoff is not None
                else None
            ),
            summary=result.review.summary,
            expected_human_read=scenario.expected_human_read,
        )
