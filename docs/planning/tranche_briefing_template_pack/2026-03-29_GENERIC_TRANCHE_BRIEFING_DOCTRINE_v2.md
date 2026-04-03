# Generic Tranche Briefing Doctrine v2

## Purpose

This document is the reusable reference doctrine for planning work in a repo that uses:
- a stable behavioural layer;
- a short active-plan pointer;
- one active gate master;
- one active supporting leaves ledger;
- one active execution log;
- explicit evidence before any gate is treated as complete.

It is intentionally generic.
It is designed to be copied into any repo that needs deterministic, low-drift planning for long-horizon work.
Gate counts and leaf counts remain variable; the invariant is preserved granularity, not a fixed cardinality.

## Core model

The control stack is:

1. **Normative documents** define the repo's intent, workflow, architecture, contracts, and non-negotiable rules.
2. **docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md** freezes planning mode, execution mode, and router law.
3. **AGENTS.md** defines stable behavioural guidance for the model/operator inside the repo.
4. **PLANS.md** points to the currently active tranche and nothing more.
5. **Gate master MD** defines the tranche contract gate by gate.
6. **Leaves JSON** defines the executable atoms and the proof required for each atom.
7. **Execution log** records receipts only.
8. **CHANGELOG** records what changed, not what should happen next.
9. **The template pack** is the durable structural source of truth; the latest closed pack is evidence input only.

A gate is not complete until:
- the code/docs for that gate are complete;
- the required tests ran green in a real repo-local environment;
- the planning control surfaces were updated together;
- a new full-history zip was created from that exact green repo state.

## Document roles

### 1. Normative documents
Use these to understand:
- the repo's intent;
- the workflow lens;
- the architecture boundaries;
- the data/packet contracts;
- the terminology rules.

These are not optional reading when the tranche affects behaviour, data flow, naming, or review semantics.

### 2. AGENTS.md
Purpose:
- stable behavioural layer;
- reading order;
- anti-drift rules;
- packaging/testing discipline;
- generic operator rules.

It should change rarely.
It should not become the active plan.

### 3. PLANS.md
Purpose:
- short repo-root execution pointer.

It should name only:
- the active gate map if one exists;
- the active gate master MD;
- the active leaves JSON;
- the active execution log;
- the next active gate;
- predecessor evidence only if still needed.

It should stay short.

### 4. Gate master MD
Purpose:
- the contract for the tranche.

It defines:
- why the tranche exists;
- which repo surfaces matter;
- what must be retained, retired from authority, amended, or added;
- gate sequence;
- gate-level definition of done;
- non-goals and drift fences.

### 5. Leaves JSON
Purpose:
- the atomic execution ledger.

A leaf tells the model:
- what to read first;
- what exact files/surfaces to touch;
- what exact action to perform;
- what must not be done;
- what exact tests/validation to run;
- what evidence must exist before the leaf is complete.

### 6. Execution log
Purpose:
- receipts only.

It should record:
- leaf id;
- gate id;
- branch;
- commit(s);
- commands run;
- observed results;
- any receipt-recovery note if reconstruction happened after the fact.

### 7. CHANGELOG
Purpose:
- machine-friendly or human-friendly change record.

It should not become the plan.

## Mandatory pre-write scan for every new tranche

Before writing a new gate master or leaves JSON, the model must inspect the following, in this order.

### A. Stable repo intent and workflow
Read the repo's normative stack, especially:
- intent / operating model;
- workflow or cognition lens;
- architecture boundaries;
- guardrails.

This step is mandatory whenever the tranche changes:
- behaviour;
- workflow order;
- signal routing;
- authority surfaces;
- runtime or review semantics.

### B. Active control surfaces
Read:
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `AGENTS.md`
- `PLANS.md`
- current active gate master
- current active leaves JSON
- current active execution log

This step is mandatory every time. If these surfaces disagree materially, emit a contradiction report before writing the new tranche.

### C. Vocabulary authority
Read the canonical vocabulary or equivalent naming authority every time you:
- create a new concept;
- rename a surface;
- write or amend a gate;
- write or amend a leaf;
- introduce new files, classes, or field names.

If a needed term does not exist:
- propose it explicitly;
- define it narrowly;
- ensure it does not collide with existing terms;
- add it to the vocabulary authority before merge if the repo's governance requires that.

### D. Packet / contract authority
Read the packet or data contract authority every time the tranche touches:
- packet schemas;
- envelope fields;
- lineage;
- validation surfaces;
- import/export format;
- interface compatibility.

### E. Live workflow surfaces
Read the existing code path that the new tranche will affect.
Do not plan in the abstract.
Trace the current workflow and identify:
- canonical surfaces to retain;
- compatibility-only surfaces to demote;
- thin chokepoints that would compress rich inputs too early;
- downstream consumers that must not read raw import-stage records.

### F. Test regime
Read the active testing doctrine and the specific existing tests around the affected surfaces before authoring the leaves.

## Gate versus leaf distinction

### Gate instructions
Use the gate master to define:
- the stage objective;
- why the chosen gate count preserves granularity for this tranche;
- the code/document surfaces in scope;
- the workflow position of the change;
- the retain/retire/amend/add matrix;
- the required authority docs;
- gate-level done criteria.

The gate should answer:
- What must be true when this gate is over?
- What must not happen while doing it?
- Which existing surfaces stay canonical?
- Which existing surfaces become compatibility-only?
- What evidence closes the gate?

### Leaf instructions
Use the leaves ledger to define:
- bounded units of work;
- why the chosen leaf count preserves granularity for this tranche;
- exact ordered actions;
- exact file/surface list;
- exact tests;
- exact evidence;
- exact closeout updates required.

The leaf should answer:
- What do I do first?
- On which files?
- In what order?
- What do I run to prove it?
- What counts as done?
- What planning surfaces must I update before I call it complete?

## Required emphasis for every new tranche

Every new tranche must make these explicit early, not buried later:
- the repo intent or workflow lens that governs the change;
- the contradiction report outcome when control surfaces initially disagree;
- the state-integrity invariants that the leaves ledger and tests must enforce;
- the vocabulary authority used for naming;
- the packet or contract authority used for data/interface work;
- the live workflow trace showing where the change sits;
- the retain/retire/amend/add matrix;
- the test and packaging evidence needed to close each gate.

## Anti-drift rules

- Do not fill blanks with guesses.
- Do not copy the structure of the latest closed pack forward when the template pack already covers that need.
- Do not leave `completed_leaf_ids` and `remaining_leaf_ids` overlapping.
- Do not let a request for multiple gates waive per-gate closeout.
- Do not invent architecture in the leaves.
- Do not let a rich upstream source be collapsed back into thin compatibility surfaces without an explicit bounded derivation step.
- Do not let a coding thread discover the packet contract during execution.
- Do not let vocabulary admission happen informally.
- Do not call a gate done without a fresh full-history zip.


## Document-touch checklist requirement

Every tranche must carry an explicit document-touch checklist.
If the checklist is absent, the planning pack is incomplete even if the gates and leaves look polished.


## Execution-thread reread requirement

Every approved planning pack must name the vocabulary authority and packet/data contract authority the execution thread must reread before implementation begins.
