# R5 — Read-Only Reproduction Report (Phase A)

Date: 2026-07-20. Session surfaced model: `claude-fable-5`; no substitution
observed. Historical attributed model observations preserved, unadjudicated.

## A1. Topology

- Live `main` = `21d8a8dd18acc058aaf18dd403a91ae38ae3adfb` — equals the
  supplied archive's recorded source revision; archive SHA-256
  `6081e0ff…8cb46` matches the audit record. Tracked files: 280 (matches).
- Branch protection: required check `validate`, strict, force-pushes and
  deletions disabled. Latest `main` Actions run 29763093416: success.
- Decision range 0001–0015; manifest and sidecars as committed at `21d8a8dd`.

## A2. Complete existing suite

Every step of `.github/workflows/validate.yml` (26 steps) run in order from
the fresh clone with Python 3.11.9 and the pinned dependency line:
**0 failures** — including the recursive mutation suite (1,813 mutants,
1,546 schema-killed, 248 semantic-killed, 19 declared-equivalent survivors
with reasons) and the deterministic PDF byte-equality rebuild.

## A3. Independent-audit finding matrix

| # | Audit finding | Classification | Evidence |
|---|---|---|---|
| 1 | STATUS.md still says candidate / requires independent review | **reproduced** | STATUS.md line 5: "CANDIDATE PASS, REQUIRES INDEPENDENT REVIEW … not independently signed off" |
| 2 | all five primary headers say review pending | **reproduced** | each header carries "candidate revision pending independent review" |
| 3 | PDFs reproduce the stale status lines | **reproduced** | text extraction of the committed PDFs contains the candidate wording |
| 4 | registry says ATH-3 = COMPILATION_MEDIATED | **reproduced** | `references/source-status.yaml` ATH-3 row |
| 5 | Atharī front matter says the Majmūʿ formula is PRIMARY_TEXT_EXACT | **reproduced** | front-matter status block, line 3 |
| 6 | Decision 0013 still names the Majmūʿ formula as exact | **reproduced** | 0013 Consequences: "reserved for … the *Majmūʿ* vol-12 formula" |
| 7 | private records function as evidence in the manuscript | **reproduced** | 14 phrase hits (casebook / Branch 11 / transcript-verified / real and recurrent / observational support / corroboration / 33-case / fifty governed stops) |
| 8 | fresh-review durable state still says merge pending | **reproduced** | `AUTONOMOUS-REVIEW-STATE.json` unresolved_findings: "merge … pending" — a stale pre-merge snapshot |
| 9 | no final merged-main verification record exists | **reproduced** | no `docs/project-closure/r5/` record; sign-off does not name the merge commit |
| 10 | CHANGELOG has no R4 entry | **reproduced** | latest heading is R3 |
| 11 | Decisions 0011–0014 carry candidate-status headers | **reproduced** | each header says adopted "in a candidate revision requiring independent review" while `decision-status.yaml` says adopted |
| 12 | CONCRETE-AND-SOUND-REASON.md ends with the withdrawn duplicate fragment | **reproduced** | final bullet withdraws "objective given `A`" then re-splices "objective given `A` and the governance data…" |
| 13 | current validators nevertheless pass | **reproduced** | 26/26 green at `21d8a8dd` (A2) — the false-closure coexistence the audit names |

Major findings M1–M5 (no review-state contract; one-directional source
validation; decision-header status unvalidated; claim-shape declaration
escape hatches; misleading `all 8 expected schemas present` wording) are all
**reproduced** by inspection of the respective validators.

Root cause note (one sentence, for the record): the R4 recovery review
synchronized every surface a validator checked and did not extend the
validator set to the review-state surfaces it was itself changing — exactly
the class Decision 0014's whole-state-reread rule warns about; R5 makes those
surfaces machine-checked.

No repair was begun before this report was written.
