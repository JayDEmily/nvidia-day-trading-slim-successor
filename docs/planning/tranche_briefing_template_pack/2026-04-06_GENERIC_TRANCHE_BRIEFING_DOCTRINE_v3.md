# Generic Tranche Briefing Doctrine v3

## Purpose

This document is the reusable reference doctrine for planning work in a repo that uses:
- a stable behavioural layer;
- a short active-plan pointer;
- one active gate master;
- one active supporting leaves ledger;
- one active execution log;
- explicit evidence before any gate is treated as complete; and
- optional controlled continuity packs that can lawfully reduce operator relay burden without waiving per-gate integrity.

It is intentionally generic.
It is designed to be copied into any repo that needs deterministic, low-drift planning for long-horizon work.
Gate counts and leaf counts remain variable; the invariant is preserved granularity, not a fixed cardinality.

## Core model

The control stack is:

1. **Normative documents** define the repo's intent, workflow, architecture, contracts, and non-negotiable rules.
2. **docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md** freezes planning mode, execution mode, router law, and continuity law.
3. **AGENTS.md** defines stable behavioural guidance for the model/operator inside the repo.
4. **PLANS.md** points to the currently active tranche and nothing more.
5. **Gate master MD** defines the tranche contract gate by gate.
6. **Leaves JSON** defines the executable atoms, their owned scope, their proof, their stop rules, and any allowed fallout repairs.
7. **Execution log** records receipts only.
8. **CHANGELOG** records what changed, not what should happen next.
9. **The template pack** is the durable structural source of truth; the latest closed pack is evidence input only.
10. **GitHub branch, commit, and merge history** is the default routine execution ledger for ordinary gate work.

A gate is not complete until:
- the code/docs for that gate are complete;
- the required tests ran green in a real repo-local environment;
- the planning control surfaces were updated together;
- the exact GitHub branch/commit receipts were recorded in the execution log; and
- a full-history zip was created only if the operator explicitly requested backup, offline handoff, or sandbox transfer packaging.

## Two pack classes

### 1. Planning / bootstrap / audit packs
These packs freeze truth, classify surfaces, reconcile contradictions, or queue later execution.
They usually stop after each gate.
Their leaves should still be closed-world, but they typically do not mutate the governed runtime or retained-test surface deeply.

### 2. Execution packs
These packs perform the already-decided work.
They may be authored either as:
- default per-gate execution packs, or
- controlled continuity execution packs.

A controlled continuity execution pack is lawful only when the gate master and leaves ledger explicitly authorise a named gate sequence, per-gate merge rule, stop conditions, and final router state.

## Document roles

### Normative documents
Use these to understand:
- the repo's intent;
- the workflow lens;
- the architecture boundaries;
- the data/packet contracts; and
- the terminology rules.

These are not optional reading when the tranche affects behaviour, data flow, naming, review semantics, or gate law.

### AGENTS.md
Purpose:
- stable behavioural layer;
- reading order;
- anti-drift rules;
- generic operator rules.

It should change rarely.
It should not become the active plan or a second detailed process-law file.

### PLANS.md
Purpose:
- short repo-root execution pointer.

It should name only:
- the active gate map if one exists;
- the active gate master MD;
- the active leaves JSON;
- the active execution log;
- the active bounded-scope note;
- predecessor evidence only if still needed.

If no active pack exists, a new pack must be created and routed explicitly before later gate execution begins.
It should stay short.

### Gate master MD
Purpose:
- the contract for the tranche.

It defines:
- why the tranche exists;
- which repo surfaces matter;
- what must be retained, retired from authority, amended, or added;
- gate sequence;
- whether execution is default stop-after-gate or controlled continuity;
- gate-level definition of done;
- non-goals and drift fences.

### Leaves JSON
Purpose:
- the atomic execution ledger.

A leaf tells the execution thread:
- what to read first;
- what exact files/surfaces to touch;
- what exact decision rows, test families, or scope units it owns;
- what exact action to perform;
- what fallout repair is allowed;
- what must not be done;
- what exact tests/validation to run;
- what stop conditions require replanning; and
- what evidence must exist before the leaf is complete.

### Execution log
Purpose:
- receipts only.

It should record:
- pack-install receipt when a new pack becomes active;
- leaf id;
- gate id;
- branch;
- commit(s);
- merge type where relevant;
- commands run;
- observed results;
- whether the next gate opened or the run stopped;
- any receipt-recovery note if reconstruction happened after the fact.

### CHANGELOG
Purpose:
- machine-friendly or human-friendly change record.

It should not become the plan.

## Mandatory pre-write scan for every new tranche

Before writing a new gate master or leaves JSON, the planning thread must inspect the following, in this order.

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
- write or amend a leaf; or
- introduce new files, classes, or field names.

If a needed term does not exist:
- propose it explicitly;
- define it narrowly;
- ensure it does not collide with existing terms; and
- add it to the vocabulary authority before merge if the repo's governance requires that.

### D. Packet / contract authority
Read the packet or data contract authority every time the tranche touches:
- packet schemas;
- envelope fields;
- lineage;
- validation surfaces;
- import/export format; or
- interface compatibility.

### E. Live workflow surfaces
Read the existing code path or current control path that the new tranche will affect.
Do not plan in the abstract.
Trace the current workflow and identify:
- canonical surfaces to retain;
- compatibility-only surfaces to demote;
- thin chokepoints that would compress rich inputs too early;
- downstream consumers that must not read raw import-stage records;
- exact execution families or decision rows if this is a post-audit execution pack.

### F. Test regime
Read the active testing doctrine and the specific existing tests around the affected surfaces before authoring the leaves.
If the tranche is a retained-test execution pack, read the frozen decision register and handoff queue before deciding any gate count or leaf count.

## Gate versus leaf distinction

### Gate instructions
Use the gate master to define:
- the stage objective;
- why the chosen gate count preserves granularity for this tranche;
- the code/document surfaces in scope;
- the workflow position of the change;
- the retain/retire/amend/add matrix;
- the required authority docs;
- the execution continuity model;
- gate-level done criteria; and
- the final router state after the tranche closes.

The gate should answer:
- What must be true when this gate is over?
- What must not happen while doing it?
- Which existing surfaces stay canonical?
- Which existing surfaces become compatibility-only?
- What evidence closes the gate?
- May the execution thread continue to the next gate automatically, or must it stop?

### Leaf instructions
Use the leaves ledger to define:
- bounded units of work;
- why the chosen leaf count preserves granularity for this tranche;
- exact owned scope;
- exact ordered actions;
- exact file/surface list;
- exact tests;
- exact stop rules;
- exact evidence; and
- exact closeout updates required.

The leaf should answer:
- What do I do first?
- On which files?
- Against which exact decision rows or scope units?
- In what order?
- What fallout am I allowed to repair?
- What do I run to prove it?
- What stops me immediately?
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
- the test and closeout evidence needed to close each gate;
- the execution continuity model; and
- the final router state after the pack closes.

## Anti-drift rules

- Do not fill blanks with guesses.
- Do not copy the structure of the latest closed pack forward when the template pack already covers that need.
- Do not leave `completed_leaf_ids` and `remaining_leaf_ids` overlapping.
- Do not let a request for multiple gates waive per-gate closeout.
- Do not invent architecture in the leaves.
- Do not let a rich upstream source be collapsed back into thin compatibility surfaces without an explicit bounded derivation step.
- Do not let a coding thread discover the packet contract during execution.
- Do not let vocabulary admission happen informally.
- Do not call a gate done without synchronized control-surface closeout and exact GitHub branch/commit receipts.
- Do not treat routine zip packaging as mandatory default closeout evidence.
- Do not author a controlled continuity pack unless the leaves are closed-world enough that the execution thread does not have to improvise its scope.

## Document-touch checklist requirement

Every tranche must carry an explicit document-touch checklist.
If the checklist is absent, the planning pack is incomplete even if the gates and leaves look polished.

## Execution-thread reread requirement

Every approved planning pack must name the vocabulary authority and packet/data contract authority the execution thread must reread before implementation begins.
If no active pack exists yet, use the baseline repo authorities named in `AGENTS.md` and `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`.
