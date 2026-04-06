PYTHON ?= .venv/bin/python
BLACK ?= $(PYTHON) -m black
RUFF ?= $(PYTHON) -m ruff
MYPY ?= $(PYTHON) -m mypy
PYTEST ?= $(PYTHON) -m pytest
UVICORN ?= $(PYTHON) -m uvicorn
ALEMBIC ?= $(PYTHON) -m alembic
UV ?= uv
PYTEST_ARGS ?=

.PHONY: help install refresh-registry-artifacts gate-e-check gate-f-check gate-proof format format-check test test-unit lint typecheck check run-api init-db seed-dev db-up db-down migrate alembic-sql

help:
	@printf '%s\n' \
		"install      sync the repo-local dev environment" \
		"test         repo-wide pytest run" \
		"test-unit    compatibility alias for the repo-wide pytest run" \
		"gate-proof   targeted pytest slice; pass PYTEST_ARGS='tests/test_...'" \
		"check        broad proof path: format, lint, typecheck, and repo-wide pytest" \
		"run-api      start the local FastAPI app"

install:
	$(UV) sync --extra dev

refresh-registry-artifacts:
	$(PYTHON) -m nvda_desk.services.import_registry

gate-e-check:
	$(PYTEST) -q tests/test_real_data_loader.py

gate-f-check:
	$(PYTEST) -q tests/test_replay_compare_runtime.py

test:
	$(PYTEST) -q

# Compatibility alias until the repo maintains a true unit-only selection.
test-unit: test

gate-proof:
	@test -n "$(PYTEST_ARGS)" || (echo "Set PYTEST_ARGS to a targeted pytest path or expression." && exit 2)
	$(PYTEST) -q $(PYTEST_ARGS)

format:
	$(BLACK) src tests scripts alembic

format-check:
	$(BLACK) --check src tests scripts alembic

lint:
	$(RUFF) check src tests

typecheck:
	$(MYPY) src tests

check: format-check lint typecheck test

init-db:
	$(PYTHON) -m nvda_desk.cli init-db

seed-dev:
	$(PYTHON) -m nvda_desk.cli seed-dev

run-api:
	$(UVICORN) nvda_desk.main:app --host 127.0.0.1 --port 8000 --reload

db-up:
	docker compose up -d db

db-down:
	docker compose down

migrate:
	mkdir -p var
	$(ALEMBIC) upgrade head

alembic-sql:
	mkdir -p var
	$(ALEMBIC) upgrade head --sql > var/alembic_offline.sql
