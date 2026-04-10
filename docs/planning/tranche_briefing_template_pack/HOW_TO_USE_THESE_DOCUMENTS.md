# How to use these documents

## What this pack is for

This pack is a reusable planning kit.

Its normal use case is:
- a **planning thread** reads the repo and writes a tranche brief;
- a **coding thread** executes that brief gate by gate;
- GitHub branch, commit, and merge history carries the routine execution ledger for each gate; and
- a full-history zip is created only when the operator explicitly requests backup, offline handoff, or sandbox transfer packaging.

The pack also supports a second lawful mode:
- a **controlled continuity execution pack** may authorise a coding thread to carry several gates in sequence without operator relay between each gate, but only when the pack says so explicitly.

## Ordered workflow

1. Read the repo's normative stack.
2. Read `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`.
3. Read `AGENTS.md`.
4. Read `PLANS.md`.
5. Read the active vocabulary authority.
6. Read the active packet or contract authority.
7. Trace the live workflow surfaces that the new tranche will affect.
8. Run a contradiction scan across the active control surfaces and emit a contradiction report before planning continues if the surfaces disagree materially.
9. Populate the generic gate template, leaves template, execution-log template, and document-touch checklist using repo-specific truth only.
10. Choose variable gate and leaf counts that preserve granularity for the actual tranche rather than copying a fixed cardinality from another pack.
11. Decide whether the pack is:
    - default stop-after-each-gate; or
    - a controlled continuity execution pack.
12. If controlled continuity is used, author the exact gate sequence, pack-install proof, per-gate merge rule, stop conditions, and final router state explicitly.
13. Create or update one active gate master, one active leaves ledger, and one active execution log.
14. Hand that pack to the coding thread.
15. The coding thread executes one gate at a time on one work branch at a time, even if the pack has authorised continuity.

In brainstorming mode, optimise the planning brief for candidate edge and asymmetry before writing implementation-readiness commentary unless the operator explicitly asks for readiness.

## Do not fill blanks

If a planning thread does not know:
- the source of truth for a concept;
- the canonical workflow position of a change;
- the packet or contract shape;
- the vocabulary term to use;
- the exact files/surfaces affected;
- the exact decision rows or execution families owned by a leaf; or
- the exact proof slice and stop conditions;

then the thread must inspect the repo and resolve that gap before writing the brief.

Do not paper over unknowns with vague wording.
Do not leave a coding thread to invent architecture during execution.

## Minimum coding-thread bootstrap

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .[dev]
```

If the repo uses a stricter bootstrap such as `uv sync --extra dev`, follow the repo's own doctrine instead.

The important point is: the package must be installed in a repo-local environment so tests run against the live source tree without relying on `PYTHONPATH` hacks. The template pack should still declare exact validation commands even when a planning thread used a temporary bootstrap during inspection.

## Pack-install requirement

If no active pack exists yet, the coding thread must install the new planning pack first.
That install must:
- import the pack artefacts into repo truthfully;
- update the router quartet together;
- run the pack-install proof;
- record the environment fact used for proof; and
- stop before Gate <N> if the install proof fails.

## Gate execution loop

For each gate:

1. Create a fresh work branch from `main`.
2. Read the gate MD and the leaves for that gate literally.
3. Complete only the leaves assigned to that gate, one leaf at a time.
4. Touch only the files and bounded fallout scope the leaves authorise.
5. Run the declared validation commands in the repo-local environment.
6. Update the control surfaces together:
   - `PLANS.md`
   - active gate master
   - active leaves ledger
   - active execution log
7. Merge to `main` only after the gate is green when the pack says merge is required before the next gate.
8. Record the exact work-branch commit, merge commit where relevant, validation commands, and observed results in the execution log.
9. Create a fresh full-history zip only if the operator explicitly requested backup, offline handoff, or sandbox transfer packaging.
10. If the pack is default stop-after-gate, stop.
11. If the pack is controlled continuity, continue only if no proof failed and no declared stop condition fired.

## Evidence rule

A gate is not done until all of the following exist in the same reply or handover artefact:
- branch name;
- commit hash on the work branch;
- exact validation commands;
- observed test results;
- synchronised routing/control-surface updates;
- merge commit hash on `main` when a merge has already occurred;
- merge type when a merge occurred; and
- a fresh full-history zip with `.git` included only when the operator explicitly requested backup, offline handoff, or sandbox transfer packaging.

## Packaging rule

Exclude only repo-local runtime junk such as:
- `.venv/`
- `__pycache__/`
- `.pytest_cache/`
- `.ruff_cache/`
- `.mypy_cache/`

Do not exclude `.git/`.

## Optional final zip command

```bash
zip -r repo_full_handover.zip . -x '.venv/*' '__pycache__/*' '.pytest_cache/*' '.ruff_cache/*' '.mypy_cache/*'
```

## Success condition

The brief is good when a coding thread can execute it without inventing:
- repo intent;
- vocabulary;
- packet rules;
- workflow placement;
- decision-row ownership;
- allowed fallout scope; or
- definition of done.

## Document-touch checklist

Every new planning pack must include an explicit document-touch checklist.
It is the written answer to: which frozen law surfaces were checked, which live router surfaces were checked, which template-source surfaces were checked, which continuity rules were checked, and which surfaces must be updated if execution proceeds.

## Execution-thread reread requirement

Before coding starts, reread the vocabulary authority named in the active gates master and reread the packet/data contract authority named in the active gates master.
If no active pack exists yet, use the baseline repo authorities named in `AGENTS.md` and `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`.
