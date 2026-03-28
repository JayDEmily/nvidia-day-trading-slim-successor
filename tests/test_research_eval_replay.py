"""Gate 79 replay/research wrapper tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import cast

from sqlalchemy.orm import Session, sessionmaker

from nvda_desk.schemas.calibration import (
    GroupReviewHorizonResult,
    HorizonDiscoveryOutcome,
    HorizonDiscoveryReport,
    OffsetComparisonOutcome,
    WalkForwardHarnessAuthorityPacket,
)
from nvda_desk.schemas.replay import ReplayHorizonDiscoveryResponse
from nvda_desk.services.replay import serialize_horizon_discovery_response
from nvda_desk.services.research import ResearchService


class _StubSessionFactory:
    def __call__(
        self,
    ) -> (
        None
    ):  # pragma: no cover - ResearchService methods under test do not hit the DB.
        raise RuntimeError("not used")


def test_horizon_discovery_response_serialises_stably(tmp_path: Path) -> None:
    response = ReplayHorizonDiscoveryResponse(
        fixture_pack_id="gate79-pack",
        authority=WalkForwardHarnessAuthorityPacket(
            harness_id="gate79-serialise",
            calibration_window=2,
            validation_window=1,
            candidate_forward_blocks=[2],
        ),
        report=HorizonDiscoveryReport(
            fixture_pack_id="gate79-pack",
            group_results=[
                GroupReviewHorizonResult(
                    surface_key="gamma_pressure",
                    outcome=HorizonDiscoveryOutcome.STABLE_HORIZON_FOUND,
                    smallest_stable_forward_block=2,
                    offset_outcome=OffsetComparisonOutcome.CONSISTENT,
                )
            ],
        ),
    )
    output_path = tmp_path / "gate79_harness.json"
    serialised = serialize_horizon_discovery_response(response, output_path)
    assert output_path.read_text() == serialised
    payload = json.loads(serialised)
    assert payload["fixture_pack_id"] == "gate79-pack"
    assert payload["report"]["group_results"][0]["smallest_stable_forward_block"] == 2


def test_research_summary_stays_bounded_to_context_not_promotion() -> None:
    service = ResearchService(cast(sessionmaker[Session], _StubSessionFactory()))
    report = HorizonDiscoveryReport(
        fixture_pack_id="gate79-pack",
        group_results=[
            GroupReviewHorizonResult(
                surface_key="stable_group",
                outcome=HorizonDiscoveryOutcome.STABLE_HORIZON_FOUND,
                smallest_stable_forward_block=2,
                offset_outcome=OffsetComparisonOutcome.CONSISTENT,
            ),
            GroupReviewHorizonResult(
                surface_key="unstable_group",
                outcome=HorizonDiscoveryOutcome.OFFSET_SENSITIVE,
                offset_outcome=OffsetComparisonOutcome.OFFSET_SENSITIVE,
            ),
            GroupReviewHorizonResult(
                surface_key="thin_group",
                outcome=HorizonDiscoveryOutcome.COVERAGE_INSUFFICIENT,
                offset_outcome=OffsetComparisonOutcome.FLAPPING,
            ),
        ],
    )
    summary = service.build_horizon_discovery_summary(report)
    assert summary.stable_surface_keys == ["stable_group"]
    assert summary.unstable_surface_keys == ["unstable_group"]
    assert summary.insufficient_surface_keys == ["thin_group"]
    assert "does not run unconstrained historical search" in summary.notes[0]
