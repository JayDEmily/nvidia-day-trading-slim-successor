# Consolidation Workflow

The vocabulary workflow is a **feeder process only**.

## Allowed flow

1. harvest candidate terms from current repo surfaces and bounded planning artefacts;
2. reconcile them against the canonical vocabulary file;
3. classify each candidate as exactly one of:
   - `enrich_existing`
   - `add_new`
   - `alias_only`
   - `quarantine`
4. regenerate the canonical vocabulary file from current live architecture;
5. run enforcement tests.

## Guardrails

- never merge a stale harvested payload blindly;
- never let one label point to two different contract surfaces;
- never treat compatibility labels as canonical runtime truth;
- never let a new family, setup variant, execution expression, horizon, or workflow-routing concept land without a canonical vocabulary entry.

## Three-ledger split

The workflow keeps three distinct language ledgers:

1. **formal primitives / contracts**
2. **desk-compression phrases**
3. **repo labels / code slugs**

They may map to each other. They must not silently collapse into each other.


## Gate 55 alignment notes

Gate 55 extends canonical ownership to:

- Step 0 calendar/horizon routing terms;
- candidate family generation terms;
- carry handoff and carry-branch terms;
- generic family / setup-variant / execution-expression governance labels.
