"""Documentation hygiene checks for stable versus dated doc placement."""

from pathlib import Path

DOCS_ROOT = Path('docs')


def test_no_dated_historical_markdown_files_live_at_docs_root() -> None:
    dated_root_docs = sorted(
        path.name
        for path in DOCS_ROOT.glob('20*.md')
        if path.is_file()
    )
    assert dated_root_docs == []


def test_build_plan_is_explicitly_archived_context() -> None:
    build_plan = (DOCS_ROOT / 'BUILD_PLAN.md').read_text()
    assert 'archived context only' in build_plan.lower()
    assert 'repo-root `PLANS.md`' in build_plan
    assert '`docs/01_NORMATIVE.md`' in build_plan


def test_status_and_legacy_readmes_exist() -> None:
    assert (DOCS_ROOT / 'status' / 'README.md').exists()
    assert (DOCS_ROOT / 'legacy' / 'README.md').exists()
