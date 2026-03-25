# 2026-03-26 Cognitive Workflow Boundary Rules

Status: complete on `main`
Version: v1.0
Gate: Gate 51
Purpose: freeze the boundary rules that stop the cognitive workflow modification from drifting into cross-stage leakage or hidden loops.
Authority boundary: subordinate to the normative docs, the frozen audit findings, and `docs/planning/2026-03-26_COGNITIVE_WORKFLOW_IMPLEMENTATION_MAP.md`.

## Boundary rule 1 — Step 0 routes; it does not analyse setups

Calendar/horizon ownership decides whether the system is evaluating intraday deployment or carry-horizon decisioning. It may select the route, but it may not classify playbook families, issue risk permission, or choose an execution expression.

## Boundary rule 2 — Step 1 remains first analytical truth

Temporal context owns clock/calendar truth plus behavioural phase classification from primitive temporal observables. It must not consume downstream regime/options/posture verdicts and must not infer carry policy.

## Boundary rule 3 — Posture/risk is permission, not opportunity generation

Posture/risk may permit, downgrade, block, or hedge-require opportunities. It must not pretend to own candidate-family generation or setup-variant selection.

## Boundary rule 4 — Candidate-family generation begins only after posture/risk permission is known

Candidate family generation belongs to the playbook-selection slot and begins only after the system has state plus permission context. It may consume upstream stage outputs and registry constraints, but it must not mutate upstream truth.

## Boundary rule 5 — Setup-variant selection is narrower than family generation

The same playbook-selection slot may narrow a candidate family into a setup variant. It must not jump directly into execution sizing, and it must not bypass explicit execution-expression logic.

## Boundary rule 6 — Execution expression is expression only

Execution may choose size, laddering, invalidation shape, hedge policy, and options-versus-spot expression. It must not reopen family generation, rewrite setup selection, or back-propagate new verdicts into temporal/regime/options/posture stages.

## Boundary rule 7 — Carry begins only at an explicit handoff boundary

Carry-horizon decisioning begins only when the runtime explicitly routes into the carry branch. It may consume a typed close-state handoff plus held-position/inventory context. It must not be reached through hidden temporal or execution side effects.

## Boundary rule 8 — Review/explanation explains; it does not optimise

Review/explanation reconstructs why the routed path happened. It may not silently change prior-stage truth, promote blocked alternatives, or act as a hidden optimiser.

## Invalid cross-stage leakage examples

### Invalid example A — Step 1 reading options-flow verdicts
Temporal context may reuse primitive price/volume/chain-adjacent observables if contractually allowed, but it may not ingest `OptionsFlowContextOutput` and then pretend the result is still first-stage truth.

### Invalid example B — Posture/risk choosing a family directly
Posture may say “no new risk”, “reduced risk”, or “hedge required”. It may not choose “negative gamma flush” or “VWAP gravity reversion” as the live family. That belongs downstream in candidate-family generation.

### Invalid example C — Execution deciding to carry because ladder state feels good
Execution expression may define how an intraday setup is expressed. It may not independently decide weekend/event carry. Carry begins only after explicit handoff to the carry branch.

### Invalid example D — Carry branch reclassifying temporal phase
Carry may use close-state summaries, but it may not rewrite temporal phase truth after the intraday chain has closed.

## Practical boundary summary

The legal flow is:

`Step 0 route -> temporal -> regime -> options/flow -> posture/risk -> candidate families -> setup variant -> execution expression -> explicit carry handoff if relevant -> review`

The illegal flow is any shortcut that:
- skips posture/risk before candidate generation;
- lets execution reopen setup selection;
- lets carry masquerade as an intraday family;
- or lets downstream verdicts leak back into Step 1.
