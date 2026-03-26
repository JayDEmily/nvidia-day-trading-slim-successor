# 2026-03-26 Cognitive Workflow Modification Gates v1

Status: Gates 51–55 complete on `main`; successor pack closed through Gate 55
Version: v1.2

Historical note: the DMP assumptions in this pack were later superseded by the dedicated Gates 56–58 DMP promotion pack.

## Purpose

This document defines the **next bounded modification tranche** driven by `docs/planning/2026-03-26_COGNITIVE_WORKFLOW_UPDATE.md`.

This is **not** a repo rewrite. It is a controlled modification of the current deterministic desk-cognition architecture so that the runtime natively reflects the updated trader-thinking workflow:

`calendar/horizon -> temporal phase -> regime -> options/flow -> posture/risk permission -> candidate families -> setup variant -> execution expression -> carry branch if relevant -> review/explanation`

## Position in the planning stack

This gate pack is the **successor modification planning surface** prepared after Gates 47–50. Gate 51 is now closed on `main`; Gates 52–55 remain planned and bounded by this artefact.

## Governing inputs

- `docs/01_NORMATIVE.md`
- `docs/02_OPERATING_MODEL.md`
- `docs/03_DATA_AND_PACKAGING.md`
- `docs/04_ANALYSIS_AND_WORKBENCH.md`
- `docs/05_MULTI_AGENT_RUNTIME.md`
- `AGENTS.md`
- `docs/planning/2026-03-26_COGNITIVE_WORKFLOW_UPDATE.md`
- `docs/planning/2026-03-24_DMP_V1_SPEC.md`
- `docs/planning/2026-03-24_DMP_V2_NORMATIVE_SPEC.md`
- `docs/audit/2026-03-25_preimplementation_audit/AUDIT_FINDINGS.md`
- `docs/audit/2026-03-25_preimplementation_audit/AUDIT_PLANNING_INPUT.md`

## Global tranche rules

1. This tranche is a **modification**, not a greenfield redesign.
2. The binding seven-stage runtime order remains authoritative unless a gate explicitly changes it and proves the change.
3. Modules remain interchangeable **only within their grammar slot**.
4. Shared primitive inputs are allowed; downstream verdict loops are forbidden.
5. Weekend / overnight / event carry remains a distinct horizon branch and must not be collapsed back into ordinary intraday playbook selection.
6. Raw and derived surfaces remain separated.
7. Step 0 calendar/horizon ownership must be explicit; it may not remain an implied side-effect split across temporal and carry code.
8. No gate may silently promote DMP v2 as the canonical live runtime transport. Any DMP promotion must be explicit, bounded, and proven.
9. Execution discipline remains one-branch-per-gate:
   - create a dedicated working branch for the gate
   - complete all gate leaves on that branch
   - pass targeted validation and required full-suite checks
   - merge to `main`
   - only then open the next gate branch
10. No gate may proceed if its predecessor is incomplete, unmerged, or contradicted by current audit findings.

## Non-goals for this tranche

- inventing a huge unbounded library of trader setups in one pass
- replacing typed payloads with loose dict payloads
- treating DMP v2 as already live without explicit promotion
- collapsing carry logic back into temporal or eligibility logic
- rewriting historical planning artefacts instead of adding controlled successor docs

---

## Gate 51 — Cognitive workflow implementation map

Status: complete on `main`

### Objective
Translate the cognitive workflow update into a repo-owned implementation map with explicit stage ownership, explicit boundaries, and explicit non-goals.

### Why this gate exists
The workflow update is conceptually correct, but until the stage ownership map is pinned, downstream implementation can drift into overlapping responsibilities.

### Scope
- pin ownership of each workflow branch to the appropriate runtime stage
- define where candidate family generation actually lives
- define what information may pass from posture/risk into family/variant/expression selection
- define what may pass into the carry branch at close / out-of-hours boundaries
- freeze non-goals so the tranche cannot inflate into a rewrite

### Definition of done
A reviewed implementation map exists that shows, stage by stage, how the updated trader-thinking workflow is realised without violating current normative constraints.

### Gate 51 outputs

- `docs/planning/2026-03-26_GATE51_COGNITIVE_WORKFLOW_IMPLEMENTATION_MAP.md`
- `docs/planning/2026-03-26_COGNITIVE_WORKFLOW_IMPLEMENTATION_MAP.md`
- `docs/planning/2026-03-26_COGNITIVE_WORKFLOW_BOUNDARY_RULES.md`
- `docs/planning/2026-03-26_CALENDAR_HORIZON_OWNERSHIP.md`

---

## Gate 52 — Native playbook hierarchy implementation

Status: complete on `main`

### Objective
Move the runtime from a legacy-compatible flat-playbook bridge toward a native hierarchy:

`family -> setup_variant -> execution_expression -> horizon`

### Why this gate exists
The current runtime carries hierarchy in schema and planning language, but operationally still behaves like a small set of flat leaf rules.

### Scope
- make family / setup variant / execution expression native runtime concepts
- preserve compatibility for the currently live seven rules during transition
- update registry, runtime selection, explanation lineage, and fixtures accordingly
- keep candidate-generation and final expression logic deterministic and inspectable

### Definition of done
The runtime selects through hierarchical playbook structures natively, while legacy compatibility remains explicit and tested rather than accidental.

---

## Gate 53 — Carry / weekend / event-horizon formalisation

Status: complete on `main`

### Objective
Formalise the handoff between intraday cognition and carry-horizon decisioning, with explicit treatment of weekend and event carry.

### Why this gate exists
Carry logic exists, but the handoff from intraday close-state to overnight/weekend/event carry still needs a more explicit typed and documented contract.

### Scope
- define close-state -> carry-state handoff packet
- define weekend, ordinary overnight, and event-carry taxonomy
- define the held-position / inventory context required by carry decisioning
- define allowed carry actions and downgrade/override rules
- ensure review/explanation can reconstruct why carry was allowed, downgraded, or blocked

### Definition of done
Carry-horizon decisioning is formally typed, bounded, and explained without being muddled with ordinary intraday playbook selection.

---

## Gate 54 — DMP binding-surface decision

Status: next planned gate

### Objective
Make the DMP binding decision explicit for this tranche and prevent mixed-mode ambiguity.

### Why this gate exists
The repo contains live DMP v1 runtime production plus DMP v2 draft/migration surfaces. That is useful, but dangerous if left ambiguous during workflow modification.

### Scope
- inventory all live runtime DMP binding surfaces
- prove whether the tranche stays on DMP v1 or deliberately promotes DMP v2
- if promotion is chosen, close Gate 54 with a bounded successor promotion pack rather than smuggling implementation into unrelated workflow leaves
- update docs/tests so the chosen decision is explicit and enforceable
- forbid accidental partial migration or hidden mixed-mode assumptions

### Default planning assumption
Unless a dedicated gate explicitly proves otherwise, this tranche proceeds with:

- **DMP v1 as the canonical live runtime packet surface**
- **DMP v2 retained as draft/migration surface only**

### Definition of done
The repo can no longer be misread as “already on DMP v2” if it is not, and any future DMP v2 promotion path is clearly bounded.

---

## Gate 55 — Vocabulary/governance alignment

Status: complete on `main`

### Objective
Align vocabulary governance with the workflow modification only after stage ownership, hierarchy, carry taxonomy, and DMP decision are pinned.

### Why this gate exists
Language drift becomes architecture drift. But vocabulary governance is only useful after the authoritative stage boundaries and term ownership are fixed.

### Scope
- align family / setup variant / execution expression / horizon terms
- align code slugs and planning labels with canonical terminology
- preserve controlled aliases and deprecations
- block conflicting duplicate labels through tests and governance docs

### Definition of done
The repo has one authoritative vocabulary/governance surface for the updated workflow, and future additions cannot silently introduce conflicting labels.

---

## Execution order

1. Gate 51 — complete on `main`
2. Gate 52 — complete on `main`
3. Gate 53 — complete on `main`
4. Gate 54 — next planned gate
5. Gate 55

No later gate may begin until the current gate is complete, validated, and merged.

## Expected outputs of this planning pack

- one gate-specific working branch per gate during execution
- one supporting implementation note per gate
- one leaf pack with bounded touches and validation commands
- updated explanation/review traces where hierarchy or carry routing changes
- explicit DMP decision artefacts, not implied assumptions
- gate-specific or neutral test filenames for new checks; reuse of older gate-numbered tests must be explicitly justified rather than left ambiguous

## Audit checkpoints to retain throughout execution

- **Known true / Ruled out / Next gate** must be updated at each gate closeout.
- Each gate must state whether it changed:
  - stage ownership
  - data-in / data-out contract
  - DMP packet expectations
  - carry-horizon routing
  - vocabulary ownership

## Final note

This gate pack exists to stop the repo from drifting into a half-updated trader-thinking wrapper around old leaf logic. The goal is a bounded, testable modification path that deepens the cognition workflow without sacrificing deterministic structure.
