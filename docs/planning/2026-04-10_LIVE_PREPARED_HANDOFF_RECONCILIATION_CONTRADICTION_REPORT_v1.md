# 2026-04-10_LIVE_PREPARED_HANDOFF_RECONCILIATION_CONTRADICTION_REPORT_v1

Status: closed contradiction report retained as evidence for Gate 255.

## Known contradiction

The prepared handoff includes a later `AGENTS.md` that adds a hard authority reference to `docs/08_GITHUB_OR_CHATGPT_GITHUB_INTERACTIONS.md`.

Observed truth:
- the prepared handoff contains `AGENTS.md`
- the prepared handoff does not contain `docs/08_GITHUB_OR_CHATGPT_GITHUB_INTERACTIONS.md`
- the live repo does not contain `docs/08_GITHUB_OR_CHATGPT_GITHUB_INTERACTIONS.md`

Why this is not safe to auto-resolve:
- importing the prepared `AGENTS.md` verbatim would create a dangling authority reference on a GitHub-mutation surface;
- trimming the prepared `AGENTS.md` would falsify the locked Gate 253 doctrine content;
- fabricating `docs/08...` would invent authority not present in either source tree.

## Resolution chosen for Gate 255

- keep the live repo `AGENTS.md` unchanged;
- import the rest of the prepared repo-tree state that remains lawful without the missing `docs/08...` file;
- adapt imported governance tests that hard-code the prepared Gate 253/254 `AGENTS.md` state;
- record the deferment explicitly in the import manifest, Gate 255 proof, and closeout receipts.

## Additional same-file conflict scan

No additional same-file semantic conflict was found in the live-vs-prepared overlap scan.
The only overlap with the live post-Gate-235 corrective commit was `tests/test_gate134_bounded_trace_reporting.py`, and the prepared change only broadened later-state tolerance.
