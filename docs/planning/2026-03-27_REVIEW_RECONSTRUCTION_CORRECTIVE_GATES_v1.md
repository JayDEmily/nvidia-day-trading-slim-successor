# 2026-03-27 Review Reconstruction Corrective Gates v1

Status: complete on `main`; corrective tranche closed

Version: v1.1

## Purpose

This document defines a **tight corrective pass** after Gate 79.

The purpose of this tranche is **not** to reopen the cognitive-workflow successor pack. The adaptation law, runtime modifier plumbing, precursor stitching, and walk-forward harness are already materially implemented. The corrective seam is narrower and more important:

- schema-defined review/governance surfaces must be emitted by real producers rather than left as dead hooks
- event truth must remain rich enough to shape temporal semantics lawfully, not merely survive as a timestamp sidecar
- failure review must carry explicit evidence floors and deeper bounded classification
- horizon discovery must judge economic behaviour on more than one thin proxy
- event-source winner selection must become an explicit precedence engine rather than deterministic first-record selection

This tranche therefore reconstructs the **review-visible layer** of the existing law without redoing the whole runtime.

## Position in the planning stack

Gates 59–79 are treated as closed on `main`.

This corrective pack starts at **Gate 80** and exists only because the code audit found a bounded reconstruction seam after Gate 79. The corrective pack must be executed sequentially, one branch per gate, and must preserve the doctrine and ordering already frozen by the v6 successor pack.

## Governing inputs

- `docs/01_NORMATIVE.md`
- `docs/02_OPERATING_MODEL.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`
- `docs/05_GUARDRAILS.md`
- `docs/TESTING_AND_PROMOTION.md`
- `PLANS.md`
- `AGENTS.md`
- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v6.md`
- `docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v6.json`
- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`

## Corrective seam proven by current code

The corrective pass is grounded in current repo truth, not in generic preference:

- `ReviewExplanationOutput` exposes review/governance fields for `stability_scorecards`, `event_window_governance`, `precursor_governance`, `phase_carry_policy`, `event_options_stress_policy`, `review_eligibility`, and `candidate_governance`, but those surfaces are not emitted by the active review service (`src/nvda_desk/schemas/cognition.py:612-621`; `src/nvda_desk/services/review_explanation.py:120-180`).
- A direct runtime pass currently returns `stability_scorecards=[]` and `event_window_governance=None`, `precursor_governance=None`, `phase_carry_policy=None`, `event_options_stress_policy=None`, `review_eligibility=None`, `candidate_governance=None`, while still emitting `modifier_control_law` and `precursor_runtime_binding`.
- Temporal event semantics are still derived from `next_event_at` / `event_minutes_remaining` rather than from the richer live-event packet (`src/nvda_desk/services/temporal_context.py:66-70`, `161-184`).
- The live event packet is not yet as rich as the tranche language implies: `LiveEventReference` currently preserves `event_type`, `label`, `materiality_tier`, and provenance count, but not `event_class` or `semantic_phase` (`src/nvda_desk/schemas/events.py:384-396`; `src/nvda_desk/services/event_store.py:105-115`).
- Horizon “economic behaviour” consistency is currently reduced to spread in `mean_fresh_deployable_pct` (`src/nvda_desk/services/replay_compare.py:738-751`).
- Event ingestion still picks the winner as `ordered[0]` after sorting, while only recording conflict disposition in provenance metadata (`src/nvda_desk/services/event_ingestion.py:39-40`, `47-65`).

## Tranche doctrine

1. This is a bounded corrective pass, not a successor-pack rewrite.
2. The existing adaptation law remains authoritative; the task here is to make the emitted review/governance surfaces honest and complete.
3. Runtime must not invent aggregate evidence that does not exist. Where a surface requires multi-window or candidate-comparison evidence, the producer must bind to real replay/horizon artefacts rather than fabricate a one-snapshot substitute.
4. Schema-only hooks are forbidden. A typed field must either be produced from real evidence or be removed/relocated by explicit doctrine change. This corrective pack chooses **real producers**, not silent deletion.
5. Review-visible packets must be lineaged, typed, and reconstructable from existing runtime and replay artefacts.
6. Event semantics must be driven by preserved event truth, not by timestamp-only shortcuts when richer governed context is already available.
7. One branch per gate. Finish the gate, pass targeted validation, merge to `main`, and only then open the next gate branch.
8. Any gate that discovers the current schema location is wrong for a surface must record that explicitly and repair it in bounded form rather than leaving a misleading hook in place.

## Non-goals for this tranche

- reworking the deterministic cognition grammar order
- reopening baseline coefficient doctrine
- adding a master aggressiveness dial
- introducing unbounded event/news semantics
- changing broker/execution integration surfaces
- starting a new replay research program beyond what is required to make existing review outputs honest

---

## Gate 80 — Corrective tranche reset and anti-drift freeze

Status: complete on `main`

Depends on: closed Gate 79

### Objective

Freeze the corrective seam explicitly in doctrine, planning, and anti-drift tests so later gates repair only the missing review reconstruction layer.

### Why this gate exists

The repo does not need another sprawling tranche. It needs a precise reset that says which missing outputs are real defects, which are thinner-than-intended but acceptable, and which must remain out of scope for this corrective pass.

### Scope

- define the corrective tranche as a bounded post-Gate-79 pass
- record the exact missing review/governance surfaces and why they matter
- record that Gates 59–79 remain closed and are not reopened
- add anti-drift tests that fail if schema-declared review surfaces remain permanently unproduced without an explicit doctrine exception
- wire this corrective pair into `PLANS.md` and planning references without mutating the historical v6 pack

### Out of scope

- changing runtime law
- adding new feeds
- rewriting replay compare logic
- adding candidate search logic beyond governed surfaces

### Definition of done

The repo has one authoritative corrective plan, and anti-drift tests make it impossible to claim the review reconstruction layer is complete while the declared surfaces remain dead.

### Gate outputs

- corrective gates document
- corrective leaves JSON
- planning/anti-drift tests

### Gate 80 closeout note

Gate 80 is complete on `main`. The repo now carries one authoritative corrective reconstruction pair, the planning quartet points at that pair as the live post-Gate-79 control surface, `docs/05_GUARDRAILS.md` is deduplicated, stale V6 status drift is repaired, and targeted anti-drift tests now prove that Gate 80 closed without reopening Gates 59–79.

## Gate 81 — Live event richness preservation and temporal semantics consumption

Status: complete on `main`

Depends on: closed Gate 80

### Objective

Preserve the missing live-event semantics required by the tranche and consume that richer event truth in temporal context and review governance rather than reducing everything to `next_event_at`.

### Why this gate exists

The current code transports a live event packet, but temporal policy still reasons almost entirely from timestamp distance. Worse, the live packet itself currently drops `event_class` and `semantic_phase`, so the runtime cannot consume what it never preserved.

### Scope

- enrich `LiveEventReference` / `LiveEventSnapshot` with the missing governed fields needed by temporal and review surfaces
- keep timestamp back-compatibility while adding event-class and semantic-phase truth
- update temporal-context derivation so `event_proximity_state` and `event_window_state` can use the richer live-event packet when present
- emit typed `TemporalEventWindowSurface`
- emit typed `PrecursorGovernanceSurface`
- add runtime tests proving event richness affects semantics lawfully and remains lineaged

### Out of scope

- free-form news ontology growth
- new upstream sources
- modifier-policy redesign

### Definition of done

Live event truth is actually rich enough to support the promised semantics, and the runtime/review packet exposes event-window and precursor governance as typed surfaces.

### Gate outputs

- enriched event schemas/store conversion
- temporal-context updates
- review-governance surface emission
- targeted runtime tests

### Gate 81 closeout note

Gate 81 is complete on `main`. The live event packet now preserves `event_class` and `semantic_phase`, temporal context consumes rich live-event truth instead of timestamp-only shortcuts when the live packet is present, and review now emits typed `event_window_governance` plus `precursor_governance` surfaces.

## Gate 82 — Runtime posture-law review surface emission

Status: complete on `main`

Depends on: Gate 81

### Objective

Emit first-class typed review packets for phase/carry and event/options-stress posture law, sourced from the existing modifier/runtime truth rather than inferred after the fact.

### Why this gate exists

The modifier law is materially implemented, but the review-visible reconstruction of that law is incomplete. The repo currently applies phase/carry and event/options posture behaviour without emitting the corresponding typed surfaces promised by Gates 69 and 70.

### Scope

- derive `PhaseCarryoverPolicySurface` from temporal and modifier-runtime truth
- derive `EventOptionsStressPolicySurface` from temporal/options-flow/modifier truth
- ensure `modifier_control_law`, `phase_carry_policy`, and `event_options_stress_policy` are mutually consistent
- render those packets into `ReviewExplanationOutput` and `review_packet`
- add anti-drift tests proving the emitted review surfaces match the applied runtime law

### Out of scope

- changing the underlying modifier precedence rules
- adding new modifier bands
- revisiting baseline posture doctrine

### Definition of done

Any posture deformation now has an explicit first-class review surface explaining phase/carry and event/options-stress meaning, not just a downstream permission result.

### Gate outputs

- review-surface builder logic
- review packet updates
- runtime parity tests

### Gate 82 closeout note

Gate 82 is complete on `main`. Runtime now emits typed `phase_carry_policy` and `event_options_stress_policy` surfaces from applied posture law, and those surfaces remain consistent with the emitted `modifier_control_law` kill-switch path.

## Gate 83 — Aggregate review-governance surface builders and bindings

Status: complete on `main`

Depends on: Gate 82

### Objective

Create real producers for `stability_scorecards`, `ReviewEligibilitySurface`, and `CandidateGovernanceSurface`, bound to genuine replay/review evidence rather than fabricated runtime shorthand.

### Why this gate exists

These surfaces require aggregate evidence. A single runtime snapshot cannot honestly invent them, but leaving them as dead hooks is worse. The repo needs explicit builders and bindings that consume corridor, lineage, and horizon artefacts when that evidence exists.

### Scope

- build typed scorecard producers from real comparison/corridor evidence
- build `ReviewEligibilitySurface` from explicit evidence blocks, triggers, and governed outcomes
- build `CandidateGovernanceSurface` from promotion evidence and bounded candidate-comparison context
- bind those producers into review/horizon artefacts where the required evidence exists
- make absence explicit and governed when the required evidence packet is not present
- add tests that fail if these fields remain schema-only hooks

### Out of scope

- introducing a new free-form optimisation framework
- ad hoc candidate search
- inventing review evidence from one runtime decision

### Definition of done

The aggregate governance surfaces are emitted only from real evidence-bearing paths and are no longer passive schema placeholders.

### Gate outputs

- review-governance builder services
- replay/review bindings
- aggregate evidence tests

### Gate 83 closeout note

Gate 83 is complete on `main`. The previously dead aggregate governance hooks now emit through real evidence-bearing paths: runtime review surfaces populate `stability_scorecards`, `review_eligibility`, and `candidate_governance`, while candidate-governance release remains reserved unless promotion evidence is genuinely ready.

## Gate 84 — Failure-taxonomy and evidence-floor deepening

Status: complete on `main`

Depends on: Gate 83

### Objective

Deepen the Gate 77 failure packet so it emits an evidence floor and uses the bounded failure/resolution vocabulary in materially distinct ways.

### Why this gate exists

The current failure taxonomy is real but thin. `evidence_floor` is left `None`, and several bounded classes exist mostly as vocabulary rather than as exercised review outcomes.

### Scope

- populate `ReviewFailurePacket.evidence_floor` from real review evidence blocks
- deepen classifier logic for `SIZING_FAILURE`, `ONTOLOGY_FAILURE`, and `BAD_LUCK`
- tighten the distinction between blocked-trade, non-action, unresolved, and ontology-failure paths
- ensure economic-accountability tags stay aligned with the deeper failure packet
- add tests proving the new classes are reachable and bounded

### Out of scope

- expanding into free-text blame narratives
- changing review-governance doctrine
- adding speculative labels without evidence

### Definition of done

Failure packets carry explicit evidence floors and materially differentiated bounded classes, rather than shallow generic assignments.

### Gate outputs

- review failure-classifier updates
- evidence-floor binding logic
- targeted Gate 77 successor tests

### Gate 84 closeout note

Gate 84 is complete on `main`. `ReviewFailurePacket.evidence_floor` is now populated from governed review evidence, and the bounded Gate 77 taxonomy now materially reaches `SIZING_FAILURE`, `ONTOLOGY_FAILURE`, and `BAD_LUCK` rather than leaving them as decorative vocabulary.

## Gate 85 — Horizon economic-behaviour widening

Status: complete on `main`

Depends on: Gate 84

### Objective

Widen Gate 79 economic-behaviour consistency beyond fresh-deployable spread alone, using multiple bounded economic/review axes already present in repo vocabulary.

### Why this gate exists

The current harness is real, but its economic-consistency check is too thin relative to the tranche language. A single spread in `mean_fresh_deployable_pct` does not capture the broader economic/accountability behaviour the repo claims to judge.

### Scope

- define a bounded multi-axis economic-behaviour rule for horizon discovery
- incorporate additional axes such as replay score, deployability, contradiction rate, review completeness, and governed economic-accountability proxies where appropriate
- preserve deterministic walk-forward chronology and existing outcome vocabulary
- update fragility/ablation reporting to expose which economic axis failed
- add tests proving the widened rule can distinguish stable, offset-sensitive, and economically inconsistent outcomes

### Out of scope

- redesigning the whole harness
- introducing live-paper logic into replay compare
- free-form economic scoring

### Definition of done

Horizon discovery still stays deterministic and bounded, but “economic behaviour” now means more than one thin proxy.

### Gate outputs

- widened stability/economic comparison rules
- updated fragility/ablation reports
- successor Gate 79 tests

### Gate 85 closeout note

Gate 85 is complete on `main`. Horizon discovery now judges bounded multi-axis economic behaviour rather than fresh-deployable spread alone, and both fragility and ablation surfaces now expose the specific failed economic axes as compact review-safe hints.

## Gate 86 — Event-ingestion source precedence refinement and corrective closeout

Status: complete on `main`

Depends on: Gate 85

### Objective

Replace first-record winner selection with an explicit bounded source-precedence engine, then close the corrective tranche with end-to-end anti-drift proof.

### Why this gate exists

The current event-ingestion path preserves conflict visibility, which is good, but the actual winner path is still just `ordered[0]`. That is acceptable as scaffolding, not as final doctrine-compatible precedence law.

### Scope

- implement explicit winner selection using bounded precedence over confidence tier, freshness, source class, and outage status
- preserve visible conflict recording and provenance lineage
- keep deterministic tie-breaking where true ties remain after precedence application
- add end-to-end tests covering event ingestion through live-event snapshot, temporal semantics, review surfaces, and horizon/report closeout where relevant
- close the corrective pack in docs and planning once the emitted surfaces and precedence logic are proven

### Out of scope

- unbounded source-ranking heuristics
- adding new event feeds
- changing review doctrine beyond what this gate needs to close the corrective pass

### Definition of done

Event-source precedence is explicit and reviewable, and the corrective tranche closes with proof that the previously dead review surfaces are now either genuinely emitted from real evidence or intentionally absent by doctrine.

### Gate outputs

- explicit source-precedence engine
- end-to-end corrective tests
- closeout updates to planning docs

### Gate 86 closeout note

Gate 86 is complete on `main`. Event ingestion now resolves winners through explicit bounded precedence over outage state, freshness, confidence tier, and source class while preserving visible conflicts and lineage, and the corrective review-reconstruction tranche is closed through Gate 86 on `main`.
