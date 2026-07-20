# R5 — Final Merged-Main Verification Record

**FINAL (2026-07-20).** Completed from live remote facts after the R5 merge
and post-merge verification, in a follow-up protected PR per Decision 0016 §6:
this record names the *previous, already-verified* merge commit — never its
own containing commit, which lives in ordinary Git history.

## R4 merge (verified by the R5 pass before the R5 merge)

| Item | Value |
|---|---|
| R4 PR | #3 (`closure/r4-semantic-contract-source-integrity`) |
| Final R4 PR head | `e8dae7d2f842ee7b64c8d43930c31277e1dfe7c3` |
| R4 merge commit | `21d8a8dd18acc058aaf18dd403a91ae38ae3adfb` (merged 2026-07-20T17:17:15Z; merge commit; protected CI; no force-push/rewrite) |
| `main` Actions run at that commit | 29763093416 — success |
| R5 fresh-clone re-verification of that commit | 26/26 workflow steps, 0 failures; clean tree |
| Sign-off | `docs/project-closure/r4-fresh-fable-review/FABLE-REVIEW-SIGNOFF.md` |

## R5 merge (verified)

| Item | Value |
|---|---|
| R5 branch | `closure/r5-final-public-state-evidence-boundary` |
| R5 PR | #4 |
| Final R5 PR head | `f10ee6e7cab0d0a0357af6ad175851a6ebd276ac` |
| R5 merge commit | `87e10d5f5d50479e01dc5664e3ac57cd07b11164` (merged 2026-07-20T18:27:32Z; merge commit through protection; no force-push, no history rewrite) |
| Required check at PR head | `validate` — success (merge state CLEAN) |
| `main` Actions run at the merge commit | 29767836405 — success |
| Pre-merge fresh clone of the PR head | 28/28 workflow steps, 0 failures; clean tree |
| Post-merge fresh clone of `main` @ `87e10d5f` | 28/28 workflow steps, 0 failures; clean tree |
| Release manifest at the merge commit | 297 entries; file SHA-256 `a6307d136289a8a1366031ef5cd52f72dd47f1bfe1feb65342717fb64002a132` |
| PDFs at the merge commit (source revision `28d694c4f4fe…`, double-build byte-identical, 68 pages rendered and inspected) | orthemma-ortheme-systems-draft.pdf — 31 pp — `58537760834cfc1939415196618f5e3f09a0005e333eec2de30d4ff58e2877f7`; orthemic-core-reference-draft.pdf — 20 pp — `63e13101f5ce4e262b5b3db3de7cd9709dc48b432fb7a89c02ff8b080c6a88ac`; orthability-ground-of-intelligibility-draft.pdf — 10 pp — `f45927b79ff8cb7481feea47f7426efcac2456ca12b3cd1c948699253136226e`; orthability-divine-speech-athari-draft.pdf — 7 pp — `019c497b59da7f0abe0d307fee346bdd980507e361ba50e3ef81f822346f264d` |

Provenance: both merges executed by the fresh Fable 5 R4/R5 sessions
(surfaced `claude-fable-5` at every phase boundary; no substitution observed
in either session). The historical R4 model-provenance disagreement remains
preserved as two attributed observations, unadjudicated.
