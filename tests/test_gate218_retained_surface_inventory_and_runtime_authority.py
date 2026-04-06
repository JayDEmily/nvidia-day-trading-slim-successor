"""Gate 218 retained-surface inventory and runtime-authority checks."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = REPO_ROOT / "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_RETAINED_SURFACE_MANIFEST_AND_CUTOVER_RULES_v1.md"


def test_gate218_leaf1_retained_inventory_baseline_is_frozen() -> None:
    manifest = MANIFEST.read_text(encoding="utf-8")

    assert "## Gate 218 successor inventory freeze" in manifest
    assert "Exact tracked top-level tree frozen on `work/gate-218-retained-surface-inventory-and-runtime-authority-20260406`" in manifest

    for entry in [
        ".env.example",
        ".gitignore",
        "AGENTS.md",
        "CHANGELOG.jsonl",
        "Makefile",
        "PLANS.md",
        "README.md",
        "alembic/",
        "alembic.ini",
        "backlog/",
        "config/",
        "data/",
        "docker-compose.yml",
        "docs/",
        "fixtures/",
        "hypothesis/",
        "pyproject.toml",
        "schemas/",
        "scripts/",
        "src/",
        "tests/",
        "uv.lock",
    ]:
        assert f"- `{entry}`" in manifest

    assert "No required runtime, doctrine, operator, fixture, or test surface named in the abstract retain list was missing" in manifest
    assert "`backlog/` is present in the successor repo" in manifest
    assert "`docs/audit/`, `docs/legacy/`, and `docs/status/` are present in the successor repo" in manifest
    assert "`hypothesis/` is present and tracked in the successor repo" in manifest
    assert "`docs/BUILD_PLAN.md`, `docs/RUNBOOK.md`, `docs/reference/`, and `docs/vocabulary/` are present and retained" in manifest
    assert "`.git/` is repo metadata" in manifest
    assert "`.pytest_cache/` is an untracked local cache" in manifest
