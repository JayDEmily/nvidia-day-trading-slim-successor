# Canonical Target Decision

## Decision
The canonical working tree remains `nvidia_day_trading_v1_20260318/`.

## Why
This tree already contains the strongest doctrine/backlog/legacy-extraction surface. The executable surface from `nvidia_day_trading_v1_20260318_impl_pass5.zip` has now been merged **into this tree** rather than replacing it.

## Merge rule
- Doctrine/docs/backlog from the canonical tree win by default.
- Executable code, tests, Alembic scaffold, Makefile, and environment files are imported from `impl_pass5` where absent.
- README stays the richer current version unless executable details force an update.
- Raw archive material remains quarantined as evidence or config salvage, not runtime truth.

## Imported executable files from `impl_pass5`
- `.env.example`
- `.gitignore`
- `Makefile`
- `uv.lock`
- `alembic.ini`
- `docker-compose.yml`
- `alembic/`
- `src/`
- `tests/`

## Not imported from `impl_pass5`
- `var/*.db` and other generated runtime artefacts

## Verification note
Executable tests were **not re-run successfully in this pass** because the current sandbox lacks the required installed Python dependencies for the imported code.
