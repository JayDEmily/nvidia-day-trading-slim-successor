# 2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_RETAINED_SURFACE_MANIFEST_AND_CUTOVER_RULES_v1

## Purpose

Freeze the retained-versus-archive surface rules for the slim successor repo so the cutover does not rely on loose intuition about what “slim” means.

## Source-cut rule

The only lawful source-cut for this successor pack is source-repo `main` commit:

- `8f9c706093045a8bb333cc19e93d4021c326f761`

No later runtime, schema, DB, API, or governance changes may be mixed into the cutover source before the successor repo is created.

## Retain in the slim successor repo

Retain surfaces required for live execution, doctrine, ongoing planning, and the first substantive test audit:

### Frozen doctrine and behaviour
- `docs/01_NORMATIVE.md`
- `docs/02_OPERATING_MODEL.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`
- `docs/05_GUARDRAILS.md`
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `docs/TESTING_AND_PROMOTION.md`
- `AGENTS.md`
- `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md` (using the rescoped rewrite, not the older source-repo text)

### Operator and routing surfaces
- repo-root `PLANS.md`
- successor canonical gate map
- `README.md`
- `Makefile`
- `CHANGELOG.jsonl`

### Runtime and support surfaces
- `src/`
- `tests/`
- `fixtures/`
- `config/`
- `scripts/`
- `data/`
- `alembic/`
- `alembic.ini`
- `schemas/`
- `pyproject.toml`
- `uv.lock`
- `.env.example`
- `.gitignore`
- `docker-compose.yml`

### Planning surfaces required for future work
- `docs/planning/tranche_briefing_template_pack/`
- the successor active pack surfaces
- the Gate 210 cutover brief as retained evidence input
- `2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_07_SOURCE_DIFF_AND_AGENTS_READ_TRIGGER_NOTE_v1.md` as installation evidence input

## Leave behind in the source archive/evidence repo

Leave behind surfaces whose role is archive, historical evidence, or source-only provenance:

- closed planning packs not intentionally retained as evidence input in the slim repo
- closed execution logs, closeout receipts, contradiction reports, scope notes, salvage matrices, indexes, and cross-reference notes from earlier packs
- `docs/audit/`
- `docs/legacy/`
- `docs/status/`
- historical patch and provenance artefacts surrounding earlier recovery work
- `backlog/` unless a later successor pack proves it is required for live execution

## Manifest rules

- Retain or exclude by authority role, not sentiment or age alone.
- Do not delete a surface from the source repo merely because it is excluded from the slim repo.
- Do not retain a closed historical planning pack as active material in the slim repo.
- If a retained test, script, or fixture points to an excluded archive-only planning surface, that dependency must be recorded as an audit finding rather than silently patched over.
- If a retained runtime or test surface requires a source-only archive artefact to remain truthful, the successor cutover is incomplete.

## What later work must not do

- claim that the slim repo is valid without proving parity against the frozen source-cut commit;
- treat the absence of historical planning docs as proof that the retained runtime/test surfaces are self-sufficient;
- use “we can always look in the old repo” as a substitute for naming a required retained surface explicitly.
