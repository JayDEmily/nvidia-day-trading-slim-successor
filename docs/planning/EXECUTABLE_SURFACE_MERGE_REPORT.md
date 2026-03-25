# Executable Surface Merge Report

## Source
- canonical tree: `nvidia_day_trading_v1_20260318/`
- executable import source: `nvidia_day_trading_v1_20260318_impl_pass5.zip`

## Outcome
The executable surface has been merged into the canonical tree.

## Added to canonical tree
- root runtime/support files (`Makefile`, `.env.example`, `.gitignore`, `uv.lock`, `alembic.ini`, `docker-compose.yml`)
- `alembic/`
- `src/nvda_desk/`
- `tests/`

## Preserved from canonical tree
- all legacy extraction docs under `docs/legacy/`
- all planning docs under `docs/planning/`
- richer current `README.md`

## File-level comparison after merge
- previously only in `impl_pass5`: generated `var/*.db` files only (not imported)
- previously only in canonical tree: legacy extraction docs and master migration plan
- common files with meaningful differences: `README.md`, `CHANGELOG.jsonl`

## Status
The repo now represents both doctrine and executable surfaces in one tree.
