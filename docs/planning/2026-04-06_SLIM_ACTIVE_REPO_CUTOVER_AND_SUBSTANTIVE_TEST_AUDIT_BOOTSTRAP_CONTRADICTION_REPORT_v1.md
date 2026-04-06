# 2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_CONTRADICTION_REPORT_v1

## Purpose

Record the material contradictions and routing tensions that justify creating the first slim-successor pack rather than reopening the source repo or improvising the substantive test audit from chat memory.

## Verdict

Proceed with a new successor-repo planning pack.

The contradictions below do not justify source-repo reactivation.
They do justify a distinct successor bootstrap pack with fresh gate numbering and an explicit retained-surface audit.

## Contradictions and tensions

### 1. The source repo truthfully routes no active pack, but Gate 210 says the first substantive work must start in the slim successor repo

Current source truth:
- Gate 210 is merged on `main`;
- source `PLANS.md` routes no active pack;
- Gate 210 explicitly says no new active planning pack may be opened in the source repo to sneak the cutover work in early.

Why this is material:
- creating the next active pack in the source repo would violate the cutover brief;
- leaving the successor pack undefined would force future threads back into chat-memory planning.

Resolution path:
- author the next pack as a successor-repo pack only;
- keep the source repo as archive/evidence host.

### 2. The cutover brief defines what the slim repo should contain, but not the exact retained-versus-archive manifest

Current truth:
- the source repo contains live runtime code, tests, fixtures, doctrine, and operator surfaces;
- it also contains a large historical planning tree and other evidence-only material that the cutover brief says should stay behind.

Why this is material:
- “slim repo” is not a lawful manifest by itself;
- future cutover work could become selective guesswork without an explicit retain/archive rule set.

Resolution path:
- Gate 217 must freeze retained-surface manifest rules against the exact source-cut commit;
- Gate 218 must inventory what actually moved.

### 3. The rescoped `07` runtime-surface ledger exists outside the source repo, while the source repo still carries the older version and `AGENTS.md` does not mention its read-trigger

Current truth:
- the uploaded rescoped `07` document adds classification/read-trigger, narrow-purpose, relation-to-stack, and maintenance-law sections;
- the source repo still carries the older `docs/07...` text; and
- source `AGENTS.md` does not yet tell Codex that `docs/07...` is specialised authority with a conditional read-trigger.

Why this is material:
- the first substantive test audit will inevitably touch runtime surface ownership, compatibility-carriage law, replay/bounded-trace seam interpretation, and downstream reader permissions;
- without deciding which `07` text governs the successor repo and without bridging that posture into `AGENTS.md`, test classification could cite the wrong authority boundary or skip the file entirely.

Resolution path:
- Gate 217 pack installation must replace `docs/07...` in the successor repo, record the source-versus-rewrite diff, and amend `AGENTS.md` with the specialised-authority read-trigger;
- Gate 218 must verify that the installed doctrine is the one the audit is actually using;
- this work must remain docs/governance-only, not a hidden runtime rewrite.

### 4. Gate 202 froze evidence-governance rules, but the repo still lacks test-native keep / retire / rewrite / move law

Current truth:
- Gate 202 provides scorecard, redundancy, proof-slice, and disagreement-memory law for evidence surfaces;
- the current repo still has no canonical successor-repo rule set for classifying retained tests.

Why this is material:
- the first substantive audit needs deterministic decision outcomes, not ad hoc judgements;
- without a test-native register, later threads could treat “planning test”, “runtime test”, “stale source-repo guard”, and “move-to-archive candidate” as interchangeable.

Resolution path:
- Gate 219 must freeze the retained test inventory and ownership mapping;
- Gate 220 must freeze the decision law and first-pass decision register.

### 5. Historical gate numbers 211-216 already exist as standalone evidence-only numbers, so reusing them would blur lineage

Current truth:
- Gate 211 was retained only as historical evidence;
- Gate 212 was retired from authority;
- Gates 213-216 were standalone source numbers already salvaged or subsumed into the earlier target-repo successor pack.

Why this is material:
- reusing 211-216 in the slim successor repo would force future readers to reconstruct whether a row refers to historical standalone material or current canonical successor work.

Resolution path:
- start the successor-repo pack at Gate 217;
- keep 211-216 reserved as historical evidence-only numbering.

## Blocker classification

- source-repo bootstrap blocker: yes
- successor-pack bootstrap blocker: no
- retained-surface clarity blocker: yes
- runtime blocker: no
- future audit drift blocker: yes

## Required repairs by gate

- Gate 217: successor bootstrap and cutover-source freeze
- Gate 218: retained-surface inventory and runtime-authority verification
- Gate 219: retained test inventory and ownership mapping
- Gate 220: keep / retire / rewrite / move decision law and first-pass register
- Gate 221: proof slice and successor execution-pack handoff
