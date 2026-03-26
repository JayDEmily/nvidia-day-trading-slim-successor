# 2026-03-26 DMP Binding Surface Decision

Status: Gate 54 decision surface; complete on `main` once merged
Authority: subordinate to `docs/01_NORMATIVE.md`; bounded decision artefact for the cognitive-workflow modification tranche

## Decision

For the cognitive-workflow modification tranche closed through Gate 54:

- **DMP v1 remains the canonical live runtime packet producer surface.**
- **DMP v2 remains an implemented secondary migration/inspection surface derived from v1 packets.**
- **No partial DMP v2 producer promotion is authorised inside Gates 51–55.**

## Why this decision is correct now

1. The live runtime still produces `DmpPacket` packets first via `build_dmp_packet(...)`.
2. The runtime and imported-module paths generate DMP v2 packets by upgrading those v1 packets via `upgrade_v1_packet_to_v2(...)`.
3. The current trader-thinking workflow gates already modify hierarchy, carry routing, and vocabulary. Coupling those semantic changes to a transport promotion would blur root-cause attribution when behaviour drifts.

## Live binding inventory

### Canonical producer surfaces

- `src/nvda_desk/schemas/dmp.py`
- `src/nvda_desk/services/cognition_runtime.py::_build_stage_packets`
- imported-module emissions that expose `.packet` as the first-class packet surface

### Secondary migration / inspection surfaces

- `src/nvda_desk/schemas/dmp_v2.py`
- `src/nvda_desk/services/cognition_runtime.py::_build_stage_packets_v2`
- imported-module emissions that expose `.packet_v2` derived from `.packet`

## Explicit non-goals

- treating DMP v2 as already canonical just because v2 packets exist
- removing v1 packet production during Gates 51–55
- adding direct `build_dmp_v2_packet(...)` producer paths to runtime services as a side effect of workflow work

## Promotion rule

If the repo later chooses DMP v2 as the canonical live producer contract, that promotion must happen in a dedicated successor gate that:

- rewrites the producer path explicitly
- proves backward-compatibility or documents intentional breakage
- updates docs, fixtures, and tests together
- removes mixed-mode ambiguity rather than deepening it
