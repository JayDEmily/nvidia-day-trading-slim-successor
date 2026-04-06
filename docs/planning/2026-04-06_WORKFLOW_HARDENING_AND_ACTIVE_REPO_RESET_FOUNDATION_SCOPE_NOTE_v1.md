# 2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_SCOPE_NOTE_v1

## Purpose

State the bounded scope of the post-Gate-205 governance-hardening tranche so later execution does not quietly absorb runtime work, test-audit decisions, or slim-repo cutover work into the wrong pack.

## In-scope

- creation and routing of the new post-Gate-205 active planning pack;
- contradiction freeze across the current router, gate map, template pack, README, and Makefile;
- consolidation of router and doctrine surfaces;
- rewrite of the tranche template pack to match current GitHub-native workflow law;
- explicit planning/evidence taxonomy;
- operator-surface alignment and the later slim active-repo cutover brief.

## Out of scope

- runtime logic under `src/nvda_desk/`;
- data, packet, schema, DB, API, or Alembic changes;
- substantive test keep/retire/rewrite decisions;
- execution of later evidence-collection or coding work;
- creation of the slim active-repo successor itself.

## Stop conditions

Stop and emit an updated contradiction report before continuing if:
- `PLANS.md` and the canonical gate map disagree materially about whether this pack is active;
- a later gate tries to introduce runtime or packet changes without explicit re-scope;
- the template-pack rewrite cannot be made consistent with current repo law without first changing docs/06 or AGENTS materially;
- the Makefile/operator-surface work would require speculative toolchain changes rather than bounded workflow alignment;
- the cutover brief cannot define objective entry criteria for the later slim active-repo tranche.

## Success condition

This tranche succeeds when the repo can truthfully say:
- one active pack exists again;
- the router/doctrine/template/operator surfaces agree on how future work is planned and executed;
- the next substantive pack can begin from repo-native documents rather than from chat memory.
