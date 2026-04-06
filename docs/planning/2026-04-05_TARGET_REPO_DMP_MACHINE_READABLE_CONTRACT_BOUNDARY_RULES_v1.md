# 2026-04-05_TARGET_REPO_DMP_MACHINE_READABLE_CONTRACT_BOUNDARY_RULES_v1

Status: Gate 204 planning authority; machine-readable schema/example/validator boundary for later DMP failure-pack work.

## Purpose

Decide when later DMP failure-pack artefacts require no machine-readable contract, schema only, schema plus example, or schema plus example plus validator, using repo-native consumers and proof burden rather than standalone-repo habit.

## Contract-boundary outcomes

| Outcome | When it is allowed | What it must contain | What it must not claim |
|---|---|---|---|
| `planning_only` | the artefact is still a planning table, proof-order note, or receipt field list with no machine consumer | prose doc only | machine-read stability or schema-level validation |
| `schema_only` | the repo needs a named deterministic field set before examples or validators would add value | one repo-native schema surface and bounded field meanings | that the family is implementation-ready |
| `schema_plus_example` | later authors need one canonical dossier/example shape to avoid free-form drift across families | schema plus at least one checked-in example instance | validator-level admission or CI enforcement |
| `schema_plus_example_plus_validator` | the artefact will be parsed, enforced in pytest/CI, or emitted by more than one producer/consumer path | schema, canonical example, and one validator/test surface | blind expansion of DMP v2 schema-core |

## Decision criteria

A later DMP artefact reaches `schema_only` only when all of the following are true:

- the artefact names a reusable repo-native contract rather than a one-off receipt row;
- more than one later document or test would otherwise hand-write the same field list;
- the contract can be tied to an existing repo-native owner surface.

A later DMP artefact reaches `schema_plus_example` only when all of the following are true:

- the contract is reusable;
- shape drift would be likely without one canonical instance;
- inline-versus-reference choice, stage-link mapping, or failure assertion packaging would remain ambiguous without an example.

A later DMP artefact reaches `schema_plus_example_plus_validator` only when all of the following are true:

- later tests, CI, or runtime/review tooling will parse the artefact;
- the repo has a named consumer or promotion gate that depends on the artefact;
- failure to validate would create false packet evidence rather than a merely untidy planning note.

## Gate 204 decisions for the first later artefacts

### Family-selection tables
The Gate 204 family-selection and priority tables remain `planning_only`.
They explain what later packet work should do, but they are not themselves packet dossiers.

### Per-family DMP failure-pack dossier
The first reusable per-family dossier is planned as `schema_plus_example`.
A validator is not justified until a later gate proves that the dossier will be parsed or checked in CI.

### Packet-lineage assertion bundle
If a later gate wants one machine-readable assertion bundle covering packet ids, dependency ids, and stage-link expectations, the minimum admitted boundary is `schema_plus_example_plus_validator` because that surface would exist only to be parsed and checked.

### Receipt and proof-order closeout surfaces
Receipts, execution-log lines, and proof-order notes remain `planning_only` unless a later gate proves there is an actual parser or promotion consumer.

## Repo-native stop rules

- Do not add new machine-readable schema merely because the standalone repo had one.
- Do not add a validator before there is a named repo-native consumer.
- Do not redesign the `dmp.v2` envelope or block taxonomy in order to host a failure-pack dossier.
- Do not place packet-law meaning in fixtures alone without a governing prose or schema surface.
- Do not claim `DV` / `PV` repo-native DMP v2 schema-core terms are verified; they remain unknown / not verified unless later evidence proves otherwise.

## Preferred placement rule

When later contract work crosses the machine-readable boundary, the preferred placement order is:

1. repo-native schema under `src/nvda_desk/schemas/` when the artefact becomes part of durable repo contract law;
2. checked-in example under fixtures or an explicitly named planning/example lane;
3. validator/test only after the consumer and proof burden are explicit.

## What later work must not do

- jump straight from prose planning to validator code with no canonical example;
- create schema code for a one-off gate receipt;
- import standalone contract JSON blindly into the repo;
- treat examples as optional when the later family would otherwise be shape-ambiguous.
