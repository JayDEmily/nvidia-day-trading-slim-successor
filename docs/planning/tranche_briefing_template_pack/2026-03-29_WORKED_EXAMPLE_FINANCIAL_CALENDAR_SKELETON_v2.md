# Worked Example Skeleton: Financial Calendar Tranche

## What this is

This is not an active repo brief.
It is a skeleton showing how the generic template should be populated for a tranche that introduces a rich upstream financial-calendar source.

## Planning-thread framing

Assume you are a planning thread writing for a coding thread.
Your job is to read the repo first, then write a brief that tells the coding thread exactly:
- what the calendar source is;
- where it sits in the workflow;
- which surfaces remain canonical;
- which legacy compatibility surfaces must be retired from authority;
- how packet/contract rules constrain the work;
- what evidence closes each gate.

## Early questions the gate master must answer

1. Is the calendar source upstream information authority or downstream behavioural logic?
2. Which existing surfaces are canonical and must be retained?
3. Which thin compatibility surfaces must become compatibility-only?
4. Which packet contract governs import, lineage, and validation?
5. Which vocabulary terms are already approved?
6. Which runtime consumers may read bounded derived states, and which must not read raw imported records?

## Example retain / retire / amend / add matrix

### Retain as canonical
- event store
- live event snapshot
- bounded temporal context outputs

### Retire from authority
- timestamp-only compatibility wrappers
- thin "next event" hints as substitutes for richer event truth

### Mandatory amendments
- preserve richer imported fields through canonical projection
- prevent early collapse back into legacy thin surfaces
- tighten planning leaves so packet and vocabulary checks are explicit

### New additions
- reference-data import seam
- canonical projection crosswalk
- bounded review-proof tests

## Example leaf emphasis

A good leaf for this kind of tranche should explicitly say:
- which vocabulary terms were checked;
- which packet authority was read;
- which workflow surfaces were traced;
- what exact files will be touched;
- what exact tests will prove the change;
- whether the leaf closes a gate and therefore requires a fresh full-history zip.
