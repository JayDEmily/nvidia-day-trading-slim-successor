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

## Research-mode versus reporting-mode law

When the operator is brainstorming, researching, or asking for strategy discovery, the default mode is research-mode ideation.

Research-mode ideation must:
- seek asymmetry, dislocation, hidden causal structure, and candidate edge first;
- avoid polluting idea generation with implementation-readiness, promotion, or live-operability caveats unless the operator asks for those judgments;
- treat current code-state caveats as reporting material, not ideation material, unless the operator explicitly requests a current-state trace.

When the operator asks what the repo does today, what a current run outputs, whether a gate is complete, or whether a surface is live-ready, the mode is reporting.

Reporting must:
- describe current repo truth exactly;
- keep readiness, completeness, and evidence caveats inside reporting answers;
- avoid muting or watering down later research-mode ideation because of those reporting constraints.

## Document roles

### Frozen process and repo-law surfaces
- `docs/01_NORMATIVE.md`
- `docs/02_OPERATING_MODEL.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`
- `docs/05_GUARDRAILS.md`
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `AGENTS.md` for behavioural authority and required reading order only

`AGENTS.md` must point here for detailed workflow law.
Repo execution and closeout command choices are gate-specific and should be defined in the active pack or test doctrine rather than restated in `AGENTS.md`.

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

## Planning and evidence taxonomy

Use one taxonomy across the repo:
- active pack authority: the gates master, leaves ledger, execution log, and any bounded-scope note or contradiction report named by repo-root `PLANS.md`; this is the only live planning authority under `docs/planning/`
- latest closed pack retained as evidence: the most recent fully closed planning pack kept near the router for closeout evidence, operator comparison, and successor-pack context; not active authority
- latest closed predecessor evidence: the closed pack immediately before the latest retained pack; predecessor context only, not active authority
- older historical planning material: earlier closed planning artefacts that remain under `docs/planning/`; historical context only unless repo-root `PLANS.md` routes them as active
- evidence-input-only material: companion artefacts such as closeout receipts, indexes, cross-references, salvage matrices, and other pack-local evidence notes; informative only unless repo-root `PLANS.md` explicitly names one as an active surface

This taxonomy is semantic before it is physical.
Do not perform a mass archive move merely to make the tree feel cleaner.
Physical planning-tree restructuring is deferred unless a later tranche proves the routed taxonomy can no longer keep authority, retained evidence, and older history distinct.

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
4. one document-touch list stating which live docs must change if execution proceeds;
5. one explicit contradiction report when material control surfaces disagree before planning can continue.

Planning mode must answer, explicitly:
- why the tranche exists;
- where it sits in the repo workflow;
- what is in scope and out of scope;
- what is retained, retired from authority, amended, or added;
- which vocabulary authority execution must read for this tranche;
- which packet/data contract authority execution must read for this tranche;
- what tests or proof slices are required before a gate may be called complete;
- why the chosen gate count and leaf count preserve granularity for this tranche rather than copying a fixed cardinality from another pack;
- whether execution mode is default stop-after-each-gate or an explicitly authorised controlled continuity run;
- if controlled continuity is authorised, the exact gate sequence, pack-install proof, per-gate merge rule, stop conditions, and final router state after the last authorised gate; and
- why the leaves are closed-world enough that the execution thread does not need to invent missing file scope, missing decision rows, missing fallout scope, or missing proof commands.

## Execution mode

Execution mode is used only for an approved active gate or for a controlled continuity sequence that an approved active pack has already authorised explicitly.

Before execution starts, the thread must read:
1. `docs/01_NORMATIVE.md`
2. `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
3. `docs/TESTING_AND_PROMOTION.md`
4. repo-root `PLANS.md`
5. the active gates master named by `PLANS.md`, if one exists
6. the active leaves ledger named by `PLANS.md`, if one exists
7. the active execution log named by `PLANS.md`, if one exists
8. the bounded-scope note named by `PLANS.md`, if one exists
9. the active vocabulary authority named by the active gates master; the baseline authority is `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`
10. the active packet/data contract authority named by the active gates master; the baseline authority is `docs/03_DOMAIN_MODEL.md`

Execution mode must obey:
- one leaf at a time;
- one gate at a time;
- one branch per gate;
- no next gate until the current gate is actually closed;
- default rule: stop after each gate and await reverification unless the active pack explicitly authorises controlled continuity;
- a request to complete multiple gates does not waive per-gate sequencing, validation, routing updates, closeout, or proof.

## Controlled continuity execution packs

A pack may authorise a continuous run across several gates only when all of the following are explicit in the active pack:
- the exact authorised gate sequence;
- the exact pack-install and router-activation proof before the first gate opens;
- the rule that each gate still works one leaf at a time;
- the rule that each gate still closes truthfully on its own branch;
- whether merge to `main` is mandatory before the next gate opens;
- the exact stop conditions that end the run immediately;
- the exact broad-proof exclusions and widening rules;
- the final router state after the last authorised gate; and
- the explicit boundary on what must not be touched, such as source/archive repo mutation, unrelated runtime surfaces, or a later unplanned pack.

Controlled continuity is therefore a pack-level exception surface, not a general relaxation of repo law.
It reduces operator relay burden, but it does not waive the per-gate integrity rules.
If any proof slice fails or any declared stop condition fires, the run stops immediately and the next gate does not open.

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
For new and modified boundary work, `docs/TESTING_AND_PROMOTION.md` checkpoint-integrity rules are live authority: runtime checkpoints, observable checkpoint truth, negative proof, and structured docstrings are mandatory forward-only.
If a change affects none of those, do not spray edits across the repo.

Every planning pack must include an explicit document-touch checklist.
Tests added for planning governance should prefer state-integrity invariants over brittle lists of historically allowed transient strings.
If a pack uses controlled continuity, the checklist must also show that the continuity rule, stop rule, and final router state were reviewed and authored explicitly.

## Control-surface routing law

`PLANS.md` is a router only.
It must not become a running diary of tranche history.
It may name:
- the active pack, if one exists;
- the latest closed pack retained as evidence, if that helps onboarding;
- the latest closed predecessor evidence, if that helps immediate predecessor traceability;
- the active bounded-scope note, if one exists;
- the canonical gate map.

If no active pack exists, `PLANS.md` must say so explicitly.
It must also keep active authority, retained evidence, and older historical material distinguishable without forcing readers to reconstruct the tree from chat or commit archaeology.

## GitHub-native execution ledger law

GitHub branch, commit, and merge history is the primary execution ledger for normal gate work.
GitHub history does not replace repo-root `PLANS.md`, the canonical gate map, the active leaves ledger, the active execution log, or closeout receipts retained under `docs/planning/`.

Routine zip handoff is deprecated for ordinary execution.
Zip handoff remains allowed for backup, offline handoff, sandbox transfer, or explicit operator request.

A gate is still not closed until the planning quartet and control surfaces move together on the same branch.
The repo must not create duplicate exchange-log notes, git-log notes, or similar governance artefacts that merely restate GitHub-visible branch or commit history.

## Anti-drift closeout law

A gate is not closed until the following move together on the same branch:
1. repo-root `PLANS.md`
2. the canonical gate map
3. the active leaves ledger
4. the active execution log

If any one of those still points at the older active gate, the gate is not closed.
If a pack authorises controlled continuity, the quartet must still close each gate before the next gate opens.
After the last authorised gate, the quartet must also show the final router result exactly: either a new active pack, or no active pack currently routed.

## Template law

Planning threads must start from the repo-native template pack under `docs/planning/tranche_briefing_template_pack/`.

Templates are mandatory scaffolding, not decorative examples.
The latest closed pack is evidence input, not the structural template for the next pack.
Any new planning pack must either:
- be created from those templates; or
- preserve all mandatory sections and fields frozen by those templates.

The template pack must support both:
- default per-gate execution packs; and
- controlled continuity execution packs where the operator wants one approved run to carry several gates without relay churn.

## Closed-world leaf requirement

A leaf is not sufficiently authored if the execution thread still has to invent:
- which exact files it owns;
- which exact decision rows, test families, or scope units it owns;
- which fallout repairs are allowed;
- which fallout repairs are forbidden;
- which proof command is authoritative; or
- which stop conditions require replanning.

The burden sits on planning, not on execution, to make the leaf executable without improvising architecture or widening scope by vibe.

## State-integrity law

The planning/control surfaces must satisfy all of the following:
- `completed_leaf_ids` and `remaining_leaf_ids` are disjoint;
- every id named in `completed_leaf_ids` or `remaining_leaf_ids` exists in the leaves map;
- `active_gate = none` is lawful only when `remaining_leaf_ids` and `pending_gate_ids` are empty;
- a closed pack must not leave incomplete leaf statuses behind;
- later-proof tests must either permit later valid states or be retired/replaced during closeout.

## Stop conditions

Stop and emit a contradiction report before continuing when:
- the active control surfaces contradict each other materially;
- the active pack does not say what gate is active;
- the active pack does not name its vocabulary authority or packet/data contract authority cleanly;
- the leaves ledger cannot be mapped to the active gates master;
- required inputs for a gate are missing and cannot be derived lawfully;
- the requested work would require pretending a closed gate is still active; or
- a controlled continuity pack tries to open a later gate even though the current gate failed proof or hit a declared stop condition.

Do not stop for minor wording cleanup, small stale sentences in historical evidence, or routine closeout edits that the active pack already makes clear.
