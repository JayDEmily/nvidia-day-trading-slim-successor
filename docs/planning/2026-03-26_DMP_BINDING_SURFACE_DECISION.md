# 2026-03-26 DMP Binding Surface Decision

Status: historical Gate 54 freeze note; superseded by Gates 56–58
Authority: subordinate to `docs/01_NORMATIVE.md`; historical decision artefact retained for lineage

## Historical Gate 54 decision

For the workflow-modification tranche closed through Gate 54:

- **DMP v1 remained the canonical live runtime packet producer surface.**
- **DMP v2 remained an implemented secondary migration/inspection surface derived from v1 packets.**
- **No partial DMP v2 producer promotion was authorised inside Gates 51–55.**

## Why this decision is correct now

1. The live runtime still produces `DmpPacket` packets first via `build_dmp_packet(...)`.
2. The runtime and imported-module paths generate DMP v2 packets by upgrading those v1 packets via `upgrade_v1_packet_to_v2(...)`.
3. The current trader-thinking workflow gates already modify hierarchy, carry routing, and vocabulary. Coupling those semantic changes to a transport promotion would blur root-cause attribution when behaviour drifts.

## Historical Gate 54 inventory

### Canonical producer surfaces at the time

- `src/nvda_desk/schemas/dmp.py`
- `src/nvda_desk/services/cognition_runtime.py::_build_stage_packets`
- imported-module emissions that exposed `.packet` as the first-class packet surface

### Secondary migration / inspection surfaces at the time

- `src/nvda_desk/schemas/dmp_v2.py`
- runtime and imported-module upgrade helpers that produced secondary v2 packets from canonical v1 packets

## Explicit non-goals

- treating DMP v2 as already canonical just because v2 packets exist
- removing v1 packet production during Gates 51–55
- adding direct `build_dmp_v2_packet(...)` producer paths to runtime services as a side effect of workflow work

## Historical promotion rule

If the repo later chose DMP v2 as the canonical live producer contract, that promotion had to happen in a dedicated successor gate that:

- rewrites the producer path explicitly
- proves backward-compatibility or documents intentional breakage
- updates docs, fixtures, and tests together
- removes mixed-mode ambiguity rather than deepening it


## Historical supersession note

This Gate 54 freeze applied only to the workflow-modification tranche through Gate 55. Gates 56–58 later promoted DMP v2 to the canonical live producer surface and retired DMP v1 as a live runtime dependency.
