# 2026-03-26 Cognitive Workflow Implementation Map

Status: complete on `main`
Version: v1.0
Gate: Gate 51
Purpose: pin explicit ownership for each branch of the updated trader-thinking workflow without rewriting the seven-stage runtime spine.
Authority boundary: this file is subordinate to `docs/01_NORMATIVE.md` through `docs/05_MULTI_AGENT_RUNTIME.md`, the frozen audit findings, and the active successor authority `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v6.md`.

## Governing inputs

- `docs/01_NORMATIVE.md`
- `docs/02_OPERATING_MODEL.md`
- `docs/03_DATA_AND_PACKAGING.md`
- `docs/05_MULTI_AGENT_RUNTIME.md`
- `docs/audit/2026-03-25_preimplementation_audit/AUDIT_FINDINGS.md`
- `docs/audit/2026-03-25_preimplementation_audit/AUDIT_PLANNING_INPUT.md`
- `docs/planning/2026-03-26_COGNITIVE_WORKFLOW_UPDATE.md`
- `docs/planning/2026-03-26_COGNITIVE_WORKFLOW_BOUNDARY_RULES.md`
- `docs/planning/2026-03-26_CALENDAR_HORIZON_OWNERSHIP.md`

## Gate 51 decision summary

Gate 51 closes with the following explicit implementation-map decisions:

1. **Step 0 calendar/horizon routing is real, but it is not a hidden eighth analysis stage.**
   It is a runtime ownership/routing concern that chooses intraday seven-stage traversal versus carry-horizon evaluation.
2. **Step 1 temporal context remains the first analytical stage.**
   It owns clock/calendar truth plus behavioural phase classification from primitive temporal observables.
3. **Candidate family generation belongs inside the playbook-selection grammar slot, not inside temporal, regime, options, or posture.**
4. **Setup-variant selection remains part of the same playbook-selection slot.**
   It narrows candidate families into one live deterministic pattern.
5. **Execution expression belongs to the execution stage, not the candidate-generation stage.**
6. **Carry/overnight/weekend/event-carry decisioning remains a separate horizon branch.**
   It may consume a typed close-state handoff and held-position context, but it is not an intraday family or execution-expression variant.
7. **Review/explanation remains the final reconstruction surface.**
   It explains why the route, family, setup, expression, and carry outcome were selected or blocked.

## Workflow-to-stage ownership map

| Workflow element | Owning runtime surface | What it may consume | What it must not consume / do |
|---|---|---|---|
| Step 0 calendar / horizon routing | runtime orchestration and explicit calendar/horizon ownership surface | timestamps, session-calendar facts, event schedule, expiry calendar, market-hours facts, held-position/carry-evaluation trigger facts | must not behave like a hidden eighth analytical stage; must not classify setups or issue risk permission verdicts |
| Step 1 temporal context | `TemporalContextService` / temporal-state classifier | clock/calendar truth, primitive temporal observables, event/expiry proximity, recent path tags | must not consume later-stage regime/options/posture verdicts; must not decide carry policy |
| Step 2 market regime context | market-regime context stage | cross-asset and tape/regime primitives plus temporal output | must not select playbook families on its own; must not bypass posture/risk |
| Step 3 options / flow context | options-flow context stage | raw chain-derived options features plus temporal/regime context where contractually allowed | must not become the posture/risk gate; must not directly choose execution expression |
| Step 4 posture / risk permission | posture/risk stage | temporal, regime, options/flow outputs plus explicit risk controls | must not generate final execution expression; must not own carry-horizon routing |
| Step 5 candidate family generation | playbook-selection grammar slot (current `playbook_eligibility` layer, to be deepened in later gates) | temporal, regime, options/flow, posture/risk outputs, registry hierarchy, horizon constraints | must not bypass posture permission; must not own execution sizing/laddering; must not write carry policy |
| Step 6 setup variant selection | same playbook-selection grammar slot as candidate family generation | surviving candidate families, stage outputs, hierarchy constraints | must not issue broker-style execution plans directly; must not mutate upstream stage truth |
| Step 7 execution expression | execution-expression / execution-planning stage | selected family + setup variant, posture/risk permissions, execution templates, market-liquidity constraints | must not reopen candidate-family selection; must not rewrite temporal or carry classification |
| Step 8 carry / overnight / weekend / event branch | carry-horizon runtime and carry services | typed close-state handoff, held-position / inventory context, next-session calendar, event-carry facts, carry overrides | must not be treated as an intraday leaf; must not be selected implicitly by temporal phase alone |
| Step 9 review / explanation | review / attribution stage | full routed cognition path, selected family/setup/expression, blocked alternatives, carry decision trail | must not act as a hidden optimiser or rewrite prior-stage outcomes |

## Candidate-family ownership decision

Candidate family generation is owned by the **playbook-selection grammar slot**.

That means:
- temporal, regime, and options/flow classify state;
- posture/risk grants or withholds permission;
- the playbook-selection slot generates candidate families that are plausible under those state and permission constraints;
- the same slot narrows candidates into a selected setup variant;
- execution then chooses how to express the selected setup.

This avoids two bad architectures:
1. stuffing family generation into posture/risk, which would muddle permission with opportunity generation;
2. stuffing family generation into execution, which would turn execution into a de facto selector rather than an expresser.

## Carry-branch ownership decision

Carry-horizon decisioning is owned by the **carry branch**, not by intraday temporal, eligibility, or execution.

The carry branch may consume a typed handoff containing:
- close-state temporal summary;
- regime summary;
- options/flow summary;
- posture/risk carry permissions and overrides;
- held-position and inventory context;
- event and next-session calendar facts.

The carry branch must not require the intraday engine to invent a fake “carry playbook family” just to route into weekend or event decisions.

## Explicit non-goals pinned by Gate 51

Gate 51 does **not**:
- add a new eighth analytical stage;
- rewrite the seven-stage runtime order;
- promote DMP v2 as canonical transport;
- populate the full future family library;
- merge carry logic back into temporal or playbook eligibility;
- replace typed payloads with loose dictionaries.

## Implementation consequences for later gates

- Gate 52 may refactor the playbook-selection slot into a richer native hierarchy because Gate 51 has now pinned where family and setup selection belong.
- Gate 53 may formalise carry handoff because Gate 51 has now pinned what may legitimately pass into the carry branch.
- Gate 54 may make the DMP binding decision explicit without confusion about stage ownership.
- Gate 55 may align vocabulary because the owner of each workflow concept is now explicit.
