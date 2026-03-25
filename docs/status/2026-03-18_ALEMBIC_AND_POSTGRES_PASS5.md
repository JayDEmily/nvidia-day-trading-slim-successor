# 2026-03-18 Alembic and Postgres Pass 5

## Scope
Add the migration scaffold and Postgres promotion path on top of the lightweight local SQLite backbone.

## What changed
- Added `alembic.ini`.
- Added Alembic environment loader at `alembic/env.py`.
- Added initial migration at `alembic/versions/20260318_0001_initial.py`.
- Added `docker-compose.yml` with a local Postgres service.
- Added Make targets:
  - `db-up`
  - `db-down`
  - `migrate`
  - `alembic-sql`
- Updated `.env.example` to show both the lightweight SQLite default and the intended Postgres DSN.

## Verified
- `make check` -> pass
- `make migrate NVDA_DESK_DATABASE_URL=sqlite+pysqlite:///./var/alembic_verify.db` -> pass
- `make alembic-sql NVDA_DESK_DATABASE_URL=sqlite+pysqlite:///./var/alembic_verify_sql.db` -> pass
- generated offline SQL file:
  - `var/alembic_offline.sql`

## Not verified
- `docker compose up -d db` in this sandbox
- live Postgres connectivity in this sandbox

## Result
The repo now has a concrete migration path toward the intended Postgres/Alembic architecture instead of relying only on direct metadata creation.
