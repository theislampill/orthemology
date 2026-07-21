# Decision 0026 — Candidate state and pre-merge decision status

**Date:** 2026-07-21 · **Authority:** R7C owner authorization (Opus candidate pass) · **Status:** proposed-candidate · **Reopens nothing:** Decisions 0001–0025 stand.

**Provenance:** OPUS CANDIDATE — REQUIRES FRESH FABLE REVIEW BEFORE MERGE.

## Problem

The R7B audit (B17/B18/B20) found an integrity contradiction: `decision-status.yaml`
marked Decisions 0023–0025 `adopted` while their bodies say "OPUS CANDIDATE —
REQUIRES FRESH FABLE REVIEW BEFORE MERGE"; `current-state.yaml` is authored as
merged R6 (review/signoff pointers R4/R6) yet its derived decision IDs include the
unmerged candidate decisions; and the historical index calls R7/R7B "current". An
Opus candidate pass was, in effect, presenting its own unreviewed decisions as
adopted. **`main` (43fee0f5, R6) contains only decisions 0001–0019** — everything
from 0020 onward is in the unmerged PR chain.

## Decision

**1. Honest decision-status vocabulary.** `docs/decision-status.yaml` uses:

- `adopted-merged` — on protected `main` (0001–0019);
- `adopted-with-superseded-clause` — merged, with a superseded clause (0009);
- `proposed-candidate` — in the unmerged PR chain (PR #8: 0020–0022; PR #9:
  0023–0025; R7C grandchild: 0026+). **Not merged.**
- `superseded` / `historical` / `rejected` — reserved for lifecycle transitions.

Every candidate row records its `pr`. **An Opus candidate pass MUST NOT mark a
`proposed-candidate` decision `adopted-merged`.** Only a fresh Fable review +
protected merge promotes a decision to `adopted-merged`.

**2. Merged state vs candidate overlay.** `docs/current-state.yaml` remains the
generated derived state of the working tree; it is **not** a claim that its
contents are on `main`. The authoritative merged base and the candidate layering
are recorded in `docs/project-closure/r7c/CANDIDATE-STATE.yaml`: merged base
(`main` 43fee0f5), the PR chain (#8 → #9 → R7C grandchild), the candidate
decisions/documents/PDFs, the validation state, the provenance (R7 Opus-
substituted; R7B/R7C Opus-requested), and `merged: false`. README/STATUS carry an
explicit **candidate-overlay** note; nothing claims the candidate work is on main.

**3. Gate.** `scripts/validate_candidate_state.py` (CI) fails on: a candidate
decision marked `adopted-merged`; a candidate decision file missing the CANDIDATE
label; an R7/R7B/R7C closure artifact classified merged/adopted; the overlay
claiming `merged: true` or independent sign-off; or a stale merged-base/PR/head
pointer.

## Non-claims

This decision changes bookkeeping and integrity gates only. It reopens no settled
Decision, adopts no terminology, runs no experiment, and makes no theological or
empirical claim. It does not itself merge or promote anything — it makes the
candidate/merged boundary machine-checkable so that a fresh Fable review can
promote decisions honestly.
