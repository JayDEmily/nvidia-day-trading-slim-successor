# RUNBOOK

## Local bootstrap

```bash
make install
cp .env.example .env
make db-up
make migrate
make init-db
make seed-dev
make check
make run-api
```

## Useful commands

### Bring database up / down
```bash
make db-up
make db-down
```

### Run migrations
```bash
make migrate
make alembic-sql
```

### Initialise and seed deterministic dev data
```bash
make init-db
make seed-dev
```

### Run repo checks
```bash
make test-unit
make gate-e-check
make gate-f-check
make check
```

## SQLite deterministic override

For local deterministic paths without Docker Postgres:

```bash
NVDA_DESK_DATABASE_URL=sqlite+pysqlite:///./nvda_desk.db make init-db
NVDA_DESK_DATABASE_URL=sqlite+pysqlite:///./nvda_desk.db make seed-dev
NVDA_DESK_DATABASE_URL=sqlite+pysqlite:///./nvda_desk.db make test-unit
```

## Recovery / rollback

### Code rollback
- revert the offending change;
- restore the previous config or migration state;
- re-run `make check` and `make alembic-sql`.

### Trading-path rollback
- disable or avoid the live broker path;
- fall back to paper stub and replay only;
- retire or revise affected modules as needed;
- record the decision in `CHANGELOG.jsonl` and the relevant status note.

## Incident response priorities

1. stop execution paths;
2. preserve logs and DB state;
3. identify whether the issue is data, risk, broker, or logic;
4. reproduce under replay if possible;
5. only resume after an explicit decision.

## Kill-switch expectations

At minimum, the operator must be able to stop activity on:
- manual trigger;
- stale or corrupt data;
- broker disconnect;
- reject storm;
- loss-limit breach;
- market halt.
