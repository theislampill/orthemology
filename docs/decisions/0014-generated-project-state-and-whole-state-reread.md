# Decision 0014 — Generated project state and whole-state reread

**Date:** 2026-07-20 · **Authority:** R4 owner authorization · **Status:** adopted in a **candidate revision requiring independent review** · **Reopens nothing.**

## Problem

VERSION, README, STATUS, OPEN-DECISIONS, the primary document headers, the burden ledgers, and the source-status summaries were each maintained by hand and drifted independently. At the R4 baseline: VERSION said R2; all four primary headers said R2; README named decisions 0001–0008 while 0009–0010 existed and claimed seven examples while eight existed; OPEN-DECISIONS still assigned classical-source verification to the owner after R3 withdrew it; the R3 burden ledger said "5 owner-assigned" and enumerated six. A project whose subject matter is false closure and stale state cannot fix this by hand-editing the numbers again.

## Decision

### 1. One canonical machine-readable state source

`docs/current-state.yaml` has two blocks:

- **`authored`** — facts requiring judgment: revision label, primary document paths, terminology/empirical/license/citation status, owner-only burdens, research residuals **each with a trigger**, open formal parameters, and the exact per-lane claim-status wording.
- **`derived`** — everything countable or hashable from the tree: decision IDs and count, schema/example/validator/fixture counts, PDF paths with hashes and page counts, terminology freeze hashes, source-status summary, tracked-file count, generating commit.

`scripts/generate_current_state.py` recomputes `derived` and **preserves `authored` verbatim**; `--check` fails on drift.

### 2. Public surfaces are checked against it

`scripts/validate_current_state.py` (CI) enforces: VERSION and every primary document header name the current revision; README's decision range and example count match the tree; OPEN-DECISIONS contains exactly the authored owner-only burdens and no ordinary-research burden; STATUS carries the authored terminology/empirical/license wording; no public surface asserts a numbered release, DOI, or peer review; every research residual has a trigger; and **the recorded terminology freeze hashes match the packet files on disk**.

That last check exists because of finding **SELF-1**: the R2 and R3 closeout prose (and three R3 documents) reported the pilot-0 v1 freeze hash as `ece0412f…` while the committed `FREEZE-HASH.txt` recorded `988a6522498df73ad1c7b0f73961a054ff20862d50fff6d644d0274877412772` and `freeze_pilot0.py --check` passed against it throughout. The packet was never wrong; the prose was, and nothing could catch it because no check compared prose to packet. Now one does.

### 3. Whole-state reread after any transition

Adopted from the bounded `daee-epistemics` import set: **after any burden disposition, source-status transition, analysis-version change, or canonical-artifact change, reread and validate the whole live project state before claiming closure** — not only at final closure. Operationally this means `generate_current_state.py && validate_current_state.py` run after every such change and in CI, alongside the existing Definition-13 closure floor in cross-record semantics.

## Consequences

Counts and statuses stop being independently editable prose. The R2/R3 historical documents keep their bodies; their stale numbers are superseded by this generated state rather than rewritten. Ordinary research burdens are structurally separated from owner-only ones, so the owner list cannot silently inflate again.
