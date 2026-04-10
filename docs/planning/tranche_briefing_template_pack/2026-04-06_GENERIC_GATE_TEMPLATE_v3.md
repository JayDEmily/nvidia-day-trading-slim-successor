# YYYY-MM-DD_<TRANCHE_NAME>_GATES_v3.md

## Purpose

State the tranche purpose in one paragraph.

## Scope

In scope:
- <surface 1>
- <surface 2>

Out of scope:
- <surface 3>
- <surface 4>

## Supersession and active authority

- This document becomes the active gate authority for <Gate X> onward.
- It supersedes:
  - <older active pack if any>
- The latest closed pack remains evidence input only; it is not the structural template for this tranche.
- If no active pack exists yet, this tranche must be routed explicitly through repo-root `PLANS.md`, the canonical gate map, the leaves ledger, and the execution log before later gate work starts.

## Governing inputs

- `docs/01_NORMATIVE.md`
- `docs/02_OPERATING_MODEL.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`
- `docs/05_GUARDRAILS.md`
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `AGENTS.md`
- `PLANS.md`
- `<current vocabulary authority>`
- `<current packet/data contract authority>`
- `<current active gate map>`
- `<current active test doctrine>`
- `<workflow code surfaces touched by this tranche>`
- `<frozen decision register or handoff queue if this is an execution pack>`

## Workflow placement

State exactly where this tranche sits in the repo workflow.
State why the chosen gate count preserves granularity for this tranche rather than copying a fixed number from another pack.

Answer explicitly:
- Is this upstream information authority, bounded derivation, downstream consumer logic, review/audit infrastructure, or post-audit execution?
- What must consume it later?
- What must not consume raw outputs directly?
- Why does the tranche stop where it stops?

## Execution continuity model

Choose one and state it explicitly.

### Default model
- stop after each gate;
- await reverification before the next gate opens.

### Controlled continuity model
If this tranche may run several gates in one uninterrupted execution run, state all of the following:
- exact authorised gate sequence;
- pack-install and router-activation proof before Gate <N> opens;
- one leaf at a time / one gate at a time / one branch per gate still applies;
- whether merge to `main` is mandatory before the next gate opens;
- exact stop conditions that end the run immediately;
- broad-proof exclusions and widening rules; and
- exact final router state after the last authorised gate.

## Intent and workflow anchor

State the repo intent lens that governs this tranche.
If the repo has a workflow/cognition model, say how this tranche fits into that order.

## Retain / retire-from-authority / amend / add matrix

### Retain as canonical
- `<surface>`
- `<surface>`

### Retire from authority (compatibility-only unless later removed)
- `<surface>`
- `<surface>`

### Mandatory amendments
- `<surface>` because `<reason>`
- `<surface>` because `<reason>`

### New additions
- `<surface>`
- `<surface>`

## Vocabulary discipline

- Existing vocabulary authority must be read before writing any new planning term, file name, class name, field name, or gate title.
- Any new term must be explicitly proposed, narrowly defined, and admitted into the vocabulary authority before merge if the repo requires that.

## Packet / contract discipline

- `<packet/data contract>` is mandatory reading for any leaf that changes envelope shape, carriage, import/export, lineage, validation, or compatibility.
- External examples must not be copied verbatim unless they are already repo-native and compatibility-safe.

## Contradiction scan and state-integrity rules

- Record whether the active control surfaces agreed cleanly before planning began.
- If they did not, link the contradiction report and state what was resolved before this pack became active.
- Freeze the invariants this tranche will require at closeout:
  - `completed_leaf_ids` and `remaining_leaf_ids` are disjoint;
  - every referenced leaf id exists in the leaves ledger;
  - `active_gate = none` is lawful only when `remaining_leaf_ids` and `pending_gate_ids` are empty;
  - later-proof tests must permit later valid states or be retired/replaced during closeout.

## Document-touch checklist

Name the checklist file for this tranche and state which frozen and live control surfaces must move if execution proceeds.
If controlled continuity is authorised, the checklist must also name the pack-install proof, per-gate merge rule, stop rules, and final router state.

## Testing and promotion discipline

- Repo-local environment required: `<e.g. .venv>`
- Pack-install proof before Gate <N> opens:
  - `<command>`
- Minimum per-gate validation slice:
  - `<command>`
  - `<command>`
- A gate is not complete until:
  - tests ran green;
  - `PLANS.md`, gate map, active leaves ledger, and active execution log all moved together;
  - exact GitHub branch/commit/merge receipts were recorded for the gate closeout; and
  - a full-history zip was created only if the operator explicitly requested backup, offline handoff, or sandbox transfer packaging.

## Gates

Repeat the gate block as many times as needed. Gate count is variable; preserve granularity instead of forcing a fixed count.

### Gate <N>: <title>

**Objective**
- <what must become true>

**Owned scope units**
- `<decision row, file family, or bounded scope unit>`
- `<decision row, file family, or bounded scope unit>`

**In-scope surfaces**
- `<file or code surface>`
- `<file or code surface>`

**Allowed fallout repair scope**
- `<bounded fallout repair>`
- `<bounded fallout repair>`

**Stop conditions**
- `<condition that stops the gate>`
- `<condition that stops the pack if continuity is authorised>`

**Definition of done**
- <observable close condition 1>
- <observable close condition 2>
- <observable close condition 3>

### Gate <N+1>: <title>

**Objective**
- <what must become true>

**Owned scope units**
- `<decision row, file family, or bounded scope unit>`
- `<decision row, file family, or bounded scope unit>`

**In-scope surfaces**
- `<file or code surface>`
- `<file or code surface>`

**Allowed fallout repair scope**
- `<bounded fallout repair>`
- `<bounded fallout repair>`

**Stop conditions**
- `<condition that stops the gate>`
- `<condition that stops the pack if continuity is authorised>`

**Definition of done**
- <observable close condition 1>
- <observable close condition 2>
- <observable close condition 3>
