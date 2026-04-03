# YYYY-MM-DD_<TRANCHE_NAME>_GATES_v2.md

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

## Governing inputs

- `docs/01_NORMATIVE.md`
- `docs/02_OPERATING_MODEL.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`
- `docs/05_GUARDRAILS.md`
- `AGENTS.md`
- `PLANS.md`
- `<current vocabulary authority>`
- `<current packet/data contract authority>`
- `<current active gate map>`
- `<current active test doctrine>`
- `<workflow code surfaces touched by this tranche>`

## Workflow placement

State exactly where this tranche sits in the repo workflow.
State why the chosen gate count preserves granularity for this tranche rather than copying a fixed number from another pack.

Answer explicitly:
- Is this upstream information authority, bounded derivation, downstream consumer logic, or review/audit infrastructure?
- What must consume it later?
- What must not consume raw outputs directly?

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

## Testing and promotion discipline

- Repo-local environment required: `<e.g. .venv>`
- Minimum validation slice:
  - `<command>`
  - `<command>`
- A gate is not complete until:
  - tests ran green;
  - `PLANS.md`, gate map, active leaves ledger, and active execution log all moved together;
  - a new full-history zip was created from the exact green repo state.

## Gates

Repeat the gate block as many times as needed. Gate count is variable; preserve granularity instead of forcing a fixed count.

### Gate <N>: <title>

**Objective**
- <what must become true>

**In-scope surfaces**
- `<file or code surface>`
- `<file or code surface>`

**Definition of done**
- <observable close condition 1>
- <observable close condition 2>
- <observable close condition 3>

### Gate <N+1>: <title>

**Objective**
- <what must become true>

**In-scope surfaces**
- `<file or code surface>`
- `<file or code surface>`

**Definition of done**
- <observable close condition 1>
- <observable close condition 2>
- <observable close condition 3>
