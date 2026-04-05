# 2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_SCOPE_NOTE_v1

Status: active bounded-scope note for the target-repo admitted-evidence successor planning pack; Gate 200 active on `work/gate-200-target-repo-admitted-evidence-successor-pack-20260405`.

## Why this pack is narrow

This pack exists because Gate 199 restored one canonical target repo, but the old standalone Gates 200-212 still contain useful intent that must be salvaged in the right order.
The lawful next move is to re-author that useful intent into a target-repo-native planning pack, not to resume the old sequence directly and not to revive dual-repo packaging.

## What this pack may do

- inspect and classify the target repo's admitted evidence baseline;
- plan future real-anchor collection and admission work;
- plan coverage review, redundancy rejection, semantic review, and disagreement memory;
- plan DMP packet failure-pack work against the repo's canonical DMP v2 contract;
- update routing/control surfaces so the repo has one truthful active pack again.

## What this pack may not do

- claim that any new real anchor exists;
- claim that any new sibling pack, replay upgrade, or DMP failure pack has already been authored;
- copy the standalone repo's schemas/examples/validators into this repo as if they were automatically canonical;
- reintroduce Gate 212 or any dual-repo convergence mechanism as the project endpoint;
- change runtime semantics under `src/` as part of Gate 200 bootstrap.

## Workflow truth preserved by this scope note

- `fixtures/real_data/gate_101_canonical_raw_runtime_bundle.json` remains the admitted raw anchor baseline.
- `fixtures/real_data/gate_e_prepared_runtime_fixture_pack.json` remains a checked-in derived runtime pack generated from the raw bundle by `src/nvda_desk/services/real_data_loader.py`.
- `fixtures/trace_review/gate_132_bounded_trace_fixture_pack.json` remains the bounded sibling scenario pack, not a substitute for new real anchors.
- `fixtures/replay/gate_f_replay_regression_fixture_pack.json` remains a replay evidence surface, not proof that the evidence portfolio is sufficient.
- `docs/planning/2026-03-24_DMP_V2_NORMATIVE_SPEC.md` remains the packet law for later DMP packet failure-pack work.

## Explicit exclusions

- SLV replay market-deepening implementation remains out of scope for this pack even though `docs/status/2026-03-19_SLV_MARKET_DEEPENING_PASS6.md` names it as a plausible future direction.
- UI/reporting redesign is excluded.
- New runtime-stage expansion is excluded.
- Retrofitting the old standalone planning repo into this repo is excluded.

## Anti-drift reminder

Do not let the old standalone planning artefacts masquerade as current target-repo truth.
Do not let the closed Gate 199 state be diluted by re-opening Phase 3 under a new name.
Do not let machine-readable examples or validators outrun the repo-native contract decisions they would have to obey.
