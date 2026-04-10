# 2026-04-10_TESTING_DOCTRINE_08_PATH_CLEANUP_CONTRADICTION_REPORT_v1

Status: closed contradiction report retained as evidence for Gate 256.

## Contradiction addressed

The repo carried an unnumbered testing doctrine file while also carrying later historical evidence that referenced an unresolved numbered `08` doctrine path for GitHub/ChatGPT interactions.

Observed truth before Gate 256:
- the tracked testing doctrine file still lived outside the numbered `08` slot;
- `docs/08_TESTING_AND_PROMOTION.md` did not exist yet;
- the retired numbered GitHub/ChatGPT interactions path was not a tracked repo file;
- some live and historical surfaces still described the old numbered-08 confusion.

## Resolution

- rename the testing doctrine file to `docs/08_TESTING_AND_PROMOTION.md`;
- update repo doctrine/read-stack references to the numbered `08` testing path;
- retire the old numbered GitHub/ChatGPT interactions path from repo references entirely;
- do not create a new numbered doctrine file for GitHub or ChatGPT interactions.

## Result

The numbered doctrine stack is now coherent through `docs/08_TESTING_AND_PROMOTION.md`, and the old deferred-path confusion is retired.
