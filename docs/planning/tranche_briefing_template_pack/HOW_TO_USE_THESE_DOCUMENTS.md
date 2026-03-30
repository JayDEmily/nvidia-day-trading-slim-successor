# How to use these documents

## What this pack is for

This pack is a reusable planning kit.

Its normal use case is:
- a **planning thread** reads the repo and writes a tranche brief;
- a **coding thread** executes that brief gate by gate;
- the repo is then packaged as a full-history zip so the next thread starts from durable evidence instead of chat memory.

## Ordered workflow

1. Read the repo's normative stack.
2. Read `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`.
3. Read `AGENTS.md`.
4. Read `PLANS.md`.
5. Read the active vocabulary authority.
6. Read the active packet or contract authority.
7. Trace the live workflow surfaces that the new tranche will affect.
8. Populate the generic gate template, leaves template, execution-log template, and document-touch checklist using repo-specific truth only.
9. Create or update one active gate master, one active leaves ledger, and one active execution log.
10. Hand that pack to the coding thread.
11. The coding thread executes one gate at a time on one work branch at a time.

In brainstorming mode, optimise the planning brief for candidate edge and asymmetry before writing implementation-readiness commentary unless the operator explicitly asks for readiness.

## Do not fill blanks

If a planning thread does not know:
- the source of truth for a concept,
- the canonical workflow position of a change,
- the packet or contract shape,
- the vocabulary term to use,
- or the exact files/surfaces affected,

then the thread must inspect the repo and resolve that gap before writing the brief.

Do not paper over unknowns with vague wording.
Do not leave a coding thread to invent architecture during execution.

## Minimum coding-thread bootstrap

```bash
git init
python -m venv .venv
. .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .[dev]
```

If the repo uses a stricter bootstrap such as `uv sync --extra dev`, follow the repo's own doctrine instead.

The important point is: the package must be installed in a repo-local environment so tests run against the live source tree without relying on `PYTHONPATH` hacks. The template pack should still declare exact validation commands even when a planning thread used a temporary bootstrap during inspection.

## Gate execution loop

For each gate:

1. Create a fresh work branch from `main`.
2. Read the gate MD and the leaves for that gate literally.
3. Complete only the leaves assigned to that gate.
4. Run the declared validation commands in the repo-local environment.
5. Update the control surfaces together:
   - `PLANS.md`
   - active gate master
   - active leaves ledger
   - active execution log
6. Merge to `main` only after the gate is green.
7. Create a fresh full-history zip from that exact green repo state.

## Evidence rule

A gate is not done until all of the following exist in the same reply or handover artefact:
- branch name;
- commit hash on the work branch;
- commit hash on `main` after merge;
- exact validation commands;
- observed test results;
- a fresh full-history zip with `.git` included.

## Packaging rule

Exclude only repo-local runtime junk such as:
- `.venv/`
- `__pycache__/`
- `.pytest_cache/`
- `.ruff_cache/`
- `.mypy_cache/`

Do not exclude `.git/`.

## Example final zip command

```bash
zip -r repo_full_handover.zip . -x '.venv/*' '__pycache__/*' '.pytest_cache/*' '.ruff_cache/*' '.mypy_cache/*'
```

## Success condition

The brief is good when a coding thread can execute it without inventing:
- repo intent,
- vocabulary,
- packet rules,
- workflow placement,
- or definition of done.


## Document-touch checklist

Every new planning pack must include an explicit document-touch checklist.
It is the written answer to: which frozen law surfaces were checked, which live router surfaces were checked, and which surfaces must be updated if execution proceeds.


## Execution-thread re-read requirement

Before coding starts, reread the vocabulary authority named in the active gates master and reread the packet/data contract authority named in the active gates master. If no active pack exists yet, use the baseline repo authorities named in `AGENTS.md` and `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`.
