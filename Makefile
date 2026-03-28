PYTHON ?= .venv/bin/python
BLACK ?= $(PYTHON) -m black
RUFF ?= $(PYTHON) -m ruff
MYPY ?= $(PYTHON) -m mypy
PYTEST ?= $(PYTHON) -m pytest
UVICORN ?= $(PYTHON) -m uvicorn
ALEMBIC ?= $(PYTHON) -m alembic
UV ?= uv

.PHONY: install refresh-registry-artifacts gate-e-check gate-f-check format format-check test test-unit lint typecheck check run-api init-db seed-dev db-up db-down migrate alembic-sql

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

test-unit: test

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
