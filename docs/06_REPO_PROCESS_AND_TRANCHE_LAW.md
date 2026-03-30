# 06_REPO_PROCESS_AND_TRANCHE_LAW

## Purpose

This file freezes the repo process law for planning, execution, control-surface routing, and tranche closeout.

It exists so new threads do not reconstruct process from chat memory, stale status notes, or improvised local convention.

## Scope

This document governs:
- planning mode;
- execution mode;
- document roles and authority classes;
- when a new gates/leaves pack must be created;
- when an existing active pack must be updated instead;
- required document-touch discipline;
- anti-drift closeout expectations.

It does not redefine runtime behaviour, market logic, packet schemas, or test expectations outside their existing normative authorities.

## Document roles

### Frozen process and repo-law surfaces
- `docs/01_NORMATIVE.md`
- `docs/02_OPERATING_MODEL.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`
- `docs/05_GUARDRAILS.md`
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `AGENTS.md` except when operator behaviour or required reading order genuinely changes

### Live routing surface
- repo-root `PLANS.md`

### Active work-pack surfaces
- one active gates master under `docs/planning/`
- one active leaves ledger under `docs/planning/`
- one active execution log under `docs/planning/`
- one bounded-scope note under `docs/planning/` only if repo-root `PLANS.md` names one

### Historical evidence surfaces
- closed predecessor packs under `docs/planning/`
- `docs/status/*`
- `docs/legacy/*`

Historical evidence may remain in-repo, but it is never active authority unless repo-root `PLANS.md` names it explicitly.

## Planning mode

Planning mode is used when the repo needs one of the following:
- a new feature or architecture tranche;
- a new testing or proof tranche;
- a new governance or documentation tranche;
- a reset caused by audit findings, drift, or control-surface contradiction.

Planning mode must produce:
1. one gates master, or an explicit amendment to the currently active gates master;
2. one supporting leaves JSON ledger, or an explicit amendment to the currently active leaves ledger;
3. one execution log surface, even if it starts receipt-empty;
4. one document-touch list stating which live docs must change if execution proceeds.

Planning mode must answer, explicitly:
- why the tranche exists;
- where it sits in the repo workflow;
- what is in scope and out of scope;
- what is retained, retired from authority, amended, or added;
- what tests or proof slices are required before a gate may be called complete.

## Execution mode

Execution mode is used only for an approved active gate.

Before execution starts, the thread must read:
1. `docs/01_NORMATIVE.md`
2. `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
3. repo-root `PLANS.md`
4. the active gates master named by `PLANS.md`, if one exists
5. the active leaves ledger named by `PLANS.md`, if one exists
6. the active execution log named by `PLANS.md`, if one exists
7. the bounded-scope note named by `PLANS.md`, if one exists

Execution mode must obey:
- one leaf at a time;
- one gate at a time;
- one branch per gate;
- no next gate until the current gate is actually closed.

## Tranche creation versus tranche amendment

Create a new planning pack when:
- there is no active pack;
- the work changes category materially, such as feature work vs testing-governance work;
- the old pack is honestly closed and retained only as evidence;
- the new work would otherwise force the old pack to carry unrelated scope.

Amend the existing active pack when:
- the new work remains inside the active tranche purpose;
- the existing pack is still active;
- the gate numbering and leaf sequencing remain coherent;
- no new pack is required to keep routing truthful.

Never create a new pack merely to avoid editing the active one.
Never amend an old closed pack merely because it is nearby.

## Document-touch discipline

If a change affects repo law, update the normative/process surfaces.
If a change affects the current active tranche state, update the active pack and router surfaces.
If a change affects proof order or test expectations, update the test doctrine or active tranche docs that govern that proof.
If a change affects none of those, do not spray edits across the repo.

Every planning pack must include an explicit document-touch checklist.

## Control-surface routing law

`PLANS.md` is a router only.
It must not become a running diary of tranche history.
It may name:
- the active pack, if one exists;
- the latest closed pack retained as evidence, if that helps onboarding;
- the active bounded-scope note, if one exists;
- the canonical gate map.

If no active pack exists, `PLANS.md` must say so explicitly.

## Anti-drift closeout law

A gate is not closed until the following move together on the same branch:
1. repo-root `PLANS.md`
2. the canonical gate map
3. the active leaves ledger
4. the active execution log

If any one of those still points at the older active gate, the gate is not closed.

## Template law

Planning threads must start from the repo-native template pack under `docs/planning/tranche_briefing_template_pack/`.

Templates are mandatory scaffolding, not decorative examples.
Any new planning pack must either:
- be created from those templates; or
- preserve all mandatory sections and fields frozen by those templates.

## Stop conditions

Stop and ask for clarification when:
- the active control surfaces contradict each other materially;
- the active pack does not say what gate is active;
- the leaves ledger cannot be mapped to the active gates master;
- required inputs for a gate are missing and cannot be derived lawfully;
- the requested work would require pretending a closed gate is still active.

Do not stop for minor wording cleanup, small stale sentences in historical evidence, or routine closeout edits that the active pack already makes clear.
