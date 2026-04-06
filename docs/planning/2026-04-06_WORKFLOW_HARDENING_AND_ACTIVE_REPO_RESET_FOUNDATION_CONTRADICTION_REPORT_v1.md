# 2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_CONTRADICTION_REPORT_v1

## Purpose

Record the material control-surface contradictions and workflow tensions that justify creating the post-Gate-205 governance-hardening pack.

## Verdict

Proceed with a new planning pack.

The contradictions below do not block Gate 206 bootstrap itself.
They do block truthful later execution if left unresolved.

## Contradictions and tensions

### 1. `PLANS.md` says no active pack exists, while the canonical gate map still carries stale “active” references to the closed 2026-04-05 successor pack

Current truth after Gate 205 closeout is:
- no active pack currently routed;
- the 2026-04-05 successor pack is closed evidence only.

But the current gate map still includes paired-file prose that labels the 2026-04-05 successor pack as active in places, even though its own current-active-gate line later says active gate none.

Resolution path:
- Gate 206 must route the new pack explicitly.
- Gate 207 must remove stale active-pack references from the gate map header/paired-file text.

### 2. Live workflow law is GitHub-native, but the template pack still encodes routine zip handoff as the default completion model

Current live law:
- GitHub branch/commit/merge history is the primary routine execution ledger.
- Routine zip packaging is retired except for backup, offline handoff, sandbox transfer, or explicit operator request.

Template-pack drift:
- README, how-to, doctrine, and leaves template still describe fresh full-history zips as a routine default or required closeout path.

Resolution path:
- Gate 208 must rewrite the template pack to match current repo law.

### 3. `PLANS.md` is supposed to be a router only, but it currently still behaves partly like a historical diary

Current law:
- `PLANS.md` is a router only.
- It should not become a running diary of tranche history.

Current state:
- `PLANS.md` still carries large historical marker piles and repeated predecessor evidence blocks that exceed a short router role.

Resolution path:
- Gate 207 must reduce `PLANS.md` back to a genuinely short router.

### 4. `AGENTS.md` and `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md` are directionally aligned, but the authority split is still noisier than necessary

Current law:
- `AGENTS.md` governs agent behaviour.
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md` governs planning mode, execution mode, and tranche law.

Current state:
- the split mostly exists, but parts of the execution workflow still appear in both places and leave too much overlap for future drift.

Resolution path:
- Gate 207 must reduce AGENTS to the behavioural layer and let docs/06 carry the detailed process law.

### 5. The testing doctrine prefers bounded proof slices, but the operator-facing build surface still reads as blunt for governance work

Current doctrine:
- testing should follow the repo’s real bug surface;
- broad blind execution is not the preferred default for every task.

Current operator surface:
- the Makefile still exposes `make test` as broad `pytest -q` and `make check` as `format-check lint typecheck test`.
- This is not a direct contradiction to the doctrine, but it is an operator-surface tension for future governance gates.

Resolution path:
- Gate 210 must decide whether wording, target naming, or auxiliary guidance is enough, without destabilising the live build spine.

## Blocker classification

- Bootstrap blocker: no
- Later-pack clarity blocker: yes
- Runtime blocker: no
- Future planning drift blocker: yes

## Required repairs by gate

- Gate 206: activate the new pack and freeze the contradiction state
- Gate 207: router/doctrine consolidation
- Gate 208: template-pack GitHub-native rewrite
- Gate 209: active-vs-evidence taxonomy hardening
- Gate 210: README/Makefile alignment and slim active-repo cutover criteria
