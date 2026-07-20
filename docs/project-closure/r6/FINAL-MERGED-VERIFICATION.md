# R6 — Final Merged-Main Verification Record

**FINAL (2026-07-20).** Completed from live remote facts after the R6 merge
and post-merge verification, in a follow-up protected PR (Decision 0016 §6
pattern: record N attests the previous, already-verified merge N−1 — never
its own containing commit, which lives in ordinary Git history; the
containing tree is attested by the source-tree digest and manifest).

## R5 merge (previously verified; see docs/project-closure/r5/FINAL-MERGED-VERIFICATION.md)

R5 PR #4 → merge commit `87e10d5f…`; follow-up PR #5 → `6df15cbd…` (= R6
starting `main`); both protected, both fresh-clone verified.

## R6 merge (verified)

| Item | Value |
|---|---|
| R6 branch | `closure/r6-experiment-readiness-sourcing-state` |
| R6 PR | #6 |
| Final R6 PR head | `ec78ec3bf7e6b58027b2cc3a8f0d9b3834a495fc` |
| R6 merge commit | `b33c671aaf592c3806dbde75e251558279885044` (merged 2026-07-20T19:51:17Z; merge commit through protection; no force-push, no history rewrite) |
| Required check at PR head | `validate` — success |
| `main` Actions run at the merge commit | 29773677574 — success |
| Pre-merge fresh clone of the PR head | 34/34 workflow steps, 0 failures; clean tree; R1–R5 history byte-unchanged |
| Post-merge fresh clone of `main` @ `b33c671a` | 34/34 workflow steps, 0 failures; clean tree |
| Clean lock-only environment | full suite green in a venv populated only from `requirements-ci.lock.txt` |
| Release manifest at the merge commit | 364 entries; file SHA-256 `6c8c913b834055121ba4caeb7af0a824dd3f1883fcd112b5e06b74ed6621dc9a` |
| PDFs (double-build byte-identical; all pages rendered and inspected incl. the new References pages) | orthemma-ortheme-systems-draft.pdf — 31 pp — `f23c4f74…`; orthemic-core-reference-draft.pdf — 20 pp — `93104aaf…`; orthability-ground-of-intelligibility-draft.pdf — 11 pp — `ca1f3d9b…`; orthability-divine-speech-athari-draft.pdf — 8 pp — `d80860cd…` |
| Experiment packets at the merge commit | FCSP-1 `READY_TO_RUN`/`PREREGISTRATION_READY` (freeze `59c5427b…`); ER-1 `READY_TO_RUN`/`PREREGISTRATION_READY` (freeze `fd319440…`); TERM-P0-V2 `READY_FOR_HUMAN_MATCHING_REVIEW` (v2.1 freeze `e5e65b2f…`); **no run exists; nothing externally registered** |

Provenance: executed by the fresh Fable 5 R6 session (surfaced
`claude-fable-5` at every phase boundary; no substitution observed). All
historical model observations remain preserved as attributed observations,
unadjudicated.
