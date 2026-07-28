# Decision 0029 — Live candidate state and public-status generation

**Date:** 2026-07-21 · **Authority:** R7D owner authorization (Opus candidate pass) · **Status:** proposed-candidate · **Reopens nothing:** Decisions 0001–0028 stand.

**Provenance:** OPUS CANDIDATE — REQUIRES FRESH FABLE REVIEW BEFORE MERGE.

## Problem

The R7C audit found the candidate/public state stale and over-stated (B1–B4, probe
P1): `CANDIDATE-STATE.yaml` recorded `pr: "9-child"` and named neither PR #10 nor
its head `3cce235`, and omitted the dynamic-companion PDF, yet
`validate_candidate_state.py` passed — it never checked the overlay against the live
topology. The historical index called the unmerged R7/R7B/R7C closure dirs
`current`. Public prose said "**Every designed study is READY TO RUN**" while the
canonical packet index has mixed states (TERM-P0-V2 is human-review; the Pilot 1 /
confirmatory templates are DRAFT). README/CONTRIBUTING described fixtures as
"checking consistency," a phrase the project has repeatedly disowned.

## Decision

**1. Authoritative candidate overlay.** `docs/current-candidate-state.yaml` is the
generated-reviewed overlay: exact PR chain (#8 → #9 → #10 → R7D child), branches,
bases, **heads** (PR #10 = `3cce235`, verified live), draft/open states, candidate
decisions `0020–0029`, candidate documents/PDFs (**including** the companion PDF),
CI, provenance (R7 Opus-substituted; R7B/R7C/R7D Opus-requested = surfaced), and
`merged: false`. `docs/current-state.yaml` remains the derived working-tree state and
is **not** a claim of merged main.

**2. Stale-overlay gate.** `validate_candidate_state.py` now fails unless the overlay
names PR #10 and its **exact** head, its candidate-decision set equals the set of
`pr:`-bearing rows in `decision-status.yaml` (no drift), it lists the companion PDF,
and it declares merged/independent-signoff/ready-for-merge all false.

**3. Candidate-current status.** The historical index gains `current-candidate`; the
unmerged R7/R7B/R7C/R7D closure dirs are reclassified from `current` to
`current-candidate`. No unmerged Opus candidate artifact may read as merged current
state.

**4. Public readiness from the packet index.** `validate_public_readiness.py` (CI)
derives the allowed public readiness statements from `experiments/experiment-status.yaml`
and **bans scalar "every packet/study is READY TO RUN"** when packet states differ.
Per-packet public wording must be exact: FCSP-2/ER-2 READY_TO_RUN; FCSP-1/ER-1
historical DETERMINISTICALLY_VALIDATED; TERM-P0-V2 READY_FOR_HUMAN_MATCHING_REVIEW;
Pilot 1 / confirmatory DRAFT; no run; no external registration; no term adoption.

**5. Conformance, not consistency.** Public prose replaces "check/show consistency"
with the bounded phrase "internally conformance-checked over the declared schemas,
examples, fixtures, and adversarial operators."

**6. Semantic decision references.** `validate_decision_references.py` (CI)
distinguishes syntactic existence from semantic correctness against an explicit
reference registry: `Inst_A` / `O*(m; A)` → Decision 0001 (not 0005); symbol
normalization → Decision 0005; anti-reification and successor/lineage transport →
their actual loci.

## Non-claims

Bookkeeping and integrity gates only. Reopens no settled Decision, adopts no
terminology, runs no experiment, makes no theological or empirical claim, and merges
or promotes nothing. It makes the candidate/merged boundary and the public readiness
surfaces machine-checkable so a fresh Fable review can integrate honestly.
