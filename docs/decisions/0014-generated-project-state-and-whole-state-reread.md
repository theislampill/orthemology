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

---

## Amendment (2026-07-20, R4 independent review) — convergent drift key and exact surface validation

The body above is preserved as adopted. This amendment replaces one derived field and strengthens the surface checks; everything else stands.

### A1. Why the original derived block could not converge

The original `derived` block recorded `source_commit_at_generation = git rev-parse HEAD` inside the tracked state file, and `--check` demanded exact file equality. Committing a regenerated file necessarily creates a **new** HEAD, so the stored value was stale again on the very commit that contained it. Exact equality between a commit hash and a value embedded inside that same commit is a self-referential, non-convergent contract — the CI failure on the R4 candidate head was a structural consequence of the design, not an operational slip, and repeated regenerate-and-commit cycles could never have fixed it.

### A2. The new invariant

`derived.source_tree_digest` = SHA-256 over the concatenation of sorted records `relative-path NUL file-sha256 LF`, one per git-tracked file in the declared source-input set. The inclusion/exclusion policy is machine-readable in `docs/project-state-inputs.yaml`. The digest is a pure function of file **contents**, never of git HEAD, so committing the regenerated state cannot invalidate it. No commit hash appears anywhere in the state file; informational commit provenance lives in git history and in the PDF source sidecars.

### A3. How source, generated-surface, and artifact changes are distinguished

- **Source inputs** (everything tracked and not excluded): any content change alters the digest and forces a state regeneration.
- **Generated surfaces with their own drift checks** (`docs/generated/`, the release manifest, `docs/current-state.yaml` itself): excluded from the digest; each is guarded by its own generator `--check` or `git diff` gate, so tampering is still caught — by the responsible check, not by a cycle.
- **Built artifacts** (`artifacts/`): excluded from the digest; their identities are recorded as explicit hashes in `derived.pdfs` and enforced by the PDF byte-equality rebuild check.
- **Closure/review reports** (`docs/project-closure/`): excluded because they report the derived state rather than defining it.

### A4. Convergence is machine-proven, not asserted

`scripts/validate_state_convergence.py` (CI) builds a throwaway git repository from the tree and proves: regenerate → commit → `--check` passes **on the commit containing the regenerated file**; the check is idempotent; tampering with a declared source input fails the check; mutating a digest-excluded generated file does not trip the digest.

### A5. Exact public-surface validation replaces fuzzy matching

Owner-only burdens now carry stable IDs (`OWNER-LICENSE`, `OWNER-CITATION-IDENTITY`, `OWNER-EMPIRICAL-EXECUTION`, `OWNER-EXTERNAL-PUBLICATION`, `OWNER-PRIVATE-MATERIAL`, `OWNER-PAID-SOURCE`) in `authored.owner_only_burdens`. `OPEN-DECISIONS.md` marks each burden with `<!-- owner-burden:ID -->`; `validate_current_state.py` now enforces exact ID-set equality (missing, extra, and duplicate burdens all fail) and verbatim authored titles on the marker lines. README's decision range and example count and STATUS's per-lane claim wording are validated through explicit `<!-- state:... -->` marker blocks by exact comparison, not substring search. The whole-state reread rule (§3 above) is unchanged.
