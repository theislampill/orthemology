# Independent review — Orthemology PR #33
**9 October 2026 · publication/integration review · exact-head verdict**

## Verdict

**RECOMMEND OWNER-AUTHORISED MERGE** of PR #33 at:

```text
Repository: theislampill/orthemology
PR:         https://github.com/theislampill/orthemology/pull/33
Branch:     integration/orthemology-t20-live-checkpoints-01-23-20261009
Base/main:  3a0bdeaa1394c656245cae9599adcb143e885059
Head:       76a3218eea53a2484a1c11be4ccd6f3b541ab333
Repo tree:  906b592fb2591ed918c5f0caf485ef79dca513ab
```

No unresolved merge-blocking defect was found in the reviewed publication delta. The earlier HOLD at `aba0bce3d651ab7f09cb9aa6a31c395e31e900fc` is superseded by this exact-head review. The conclusion is not based merely on a green badge or the implementer's assertion that repairs were made.

This is a recommendation to the owner, **not an executed merge, a GitHub review submission, T20 closure, or acceptance of every scientific conclusion in the archives**. A new head or base invalidates automatic reuse of the verdict; review the intervening delta and its relevant checks.

## 1. Object being reviewed

The PR publishes selected research and evidence from 23 numbered live T20 checkpoints plus the unnumbered S01 warranted-discrimination/Lean supplement. It follows the existing 7 October integrated state and preserves T20 as ACTIVE. It does not replace the canonical frozen research registries or claim that the latest ongoing research has all reached GitHub.

The complete base-to-head change is 2,070 paths: **2,067 added publication files and three modified pre-existing files**, with no deletion from the reviewed base. The PR reports two commits and 274,082 additions against four removed lines. Line counts are bookkeeping, not measures of scientific accomplishment.

The newer CP24, guarded-verification, constructive-witness and shared-proof-cost returns are outside this PR. Their non-inclusion is an explicit cutoff, not an undisclosed integration failure.

## 2. How the review was performed

The supplied 8 October review and handoff records and both complete conversation files were read, with the second conversation taking chronological precedence. Additional exact Library artifacts were recovered, including the live integration handoff, original CP23 ZIP and the earlier PR33 review/repair packet.

A direct Git clone could not be obtained because this container could not resolve GitHub. The connected GitHub reader remained available. Instead of inventing a checkout or treating a partial API diff as complete, I used a stronger source-preservation path for the new subtree:

1. Independently reconstructed the original public selection from the saved checkpoint sources.
2. Applied the exact inspected publication-only transformations: bounded path redactions, markup repairs, omissions, typed aliases, upstream-reference ownership and licence restoration.
3. Reconstructed the CP23 and root navigation records and checked their individual Git blob identities.
4. Computed Git's path/mode/content Merkle tree over **all 2,067 reconstructed files**.
5. Compared the result with the immutable subtree returned by GitHub for the reviewed head.

The entire subtree matches:

```text
research/t20-live-20261009
99d0b4a3f923dd6a9ce89a8ad3916181a6c96b6f
```

All CP01–CP23 child trees and the S01/supplement tree also match. The retained subtree contains **15,784,107 uncompressed file bytes**. This is full publication identity verification, not a sample or a filename-count comparison. The corresponding SHA-256 source-to-public bindings are in `evidence/FINAL_PUBLIC_PROJECTION.json`; child-tree and final-tree evidence is in `evidence/PUBLICATION_RECONSTRUCTION.json`.

This method proves identity of the reconstructed content, paths and recorded Git modes under the standard Git object-hash assumption. It does **not** establish that every theorem is correct, that all source quotations are authentic, or that every original execution receipt was independently replayed here.

## 3. Repair findings and disposition

### R33-F01 — broken external-owner references: resolved

The earlier failed workflow stopped at the internal-reference gate. Six CP21 references concerned files belonging to the external `Nakammura/spinoza-ethica-lean` source, not files in Orthemology's public tree. The repair now identifies the external owner at commit `6d4c0461265e50a3bbedb640fe60d9ad292b50a7`.

Three JSON path fields become upstream URL fields for the specific affected records. One redundant path field is removed where a pinned URL already exists. Two Markdown references now identify upstream coverage/gap registers. The changes are narrow; the source's meaning and research verdicts are not silently rewritten. The public INDEX documents the field transformations. These files participate in the exact tree match, and the new reference gate passes.

### R33-F02 — private linkage metadata in the public projection: resolved at current head

The repaired projection uses **207 consistent typed aliases across 37 retained files**. Fifty-seven distinct aliases are used. Ten additional original occurrences were contained in two delivery-only records now withheld. Equality relationships, including uses as JSON keys, are preserved; the aliases are expressly not usable retrieval locators.

A fresh scan of every current public file found no remaining original-pattern Library, message or 32-hex conversation-file identifiers. The private source-to-alias map is retained in this owner-only packet. Two CP21/CP22 delivery records are absent from the public projection but preserved in the original ZIPs. Scientific sources were not deleted to avoid the privacy issue.

**History qualification:** a corrective commit does not remove the prior public commit. These identifiers were linkage metadata, not demonstrated credentials. This review does not certify that previous history, caches or external copies no longer contain them. A requirement to remove historical exposure would be a separate owner decision, not something this patch secretly accomplishes.

### R33-F03 — missing upstream licence: resolved

The original 1,188-byte licence was restored at:

```text
checkpoints/CP21/spinoza-formal-transfer-screen-20261009/sources/LICENSE
SHA-256: 47b99d4833f7c801c29bdf0e0c8488a6e9f5f5fd26d0a54a816982b783b7e837
Git blob: 9ab7646d2f3262fdb9be15ba6082a8df662a801e
```

It matches the original checkpoint member and the notice preserved by the prior independent reviewer. This fixes the identified omission. It is not a blanket legal opinion on every historical source in the research corpus.

### R33-F04 — generated state and release accounting: resolved within CI-verified scope

The derived state and release manifest were regenerated for the repaired publication. Current tracked-file accounting is 9,707. The current source-tree digest recorded in `docs/current-state.yaml` is:

```text
9c74d9d7cfe4f54933246b75ed90f80a4984e06163f546d09dcaef95d2ebeb41
```

The state change is accounting, not a philosophical or research-status upgrade. The release-manifest and successor-integrity gates both pass on the reviewed head. I did not locally rerun the entire 9,707-file repository checker; that complete-workflow execution is GitHub CI evidence, explicitly distinguished from the local subtree reconstruction.

## 4. No hidden broad repository change

GitHub root-tree and nested `docs`/`provenance` comparisons show that the pre-existing changes are restricted to:

- `.gitattributes`: one exact-path `-text` rule, plus its comment/spacing, preserving the original CRLF source-ledger bytes in CP19;
- `docs/current-state.yaml`: derived digest and tracked-file count;
- `docs/provenance/RELEASE-MANIFEST.sha256`: generated inventory/hashes.

All other pre-existing root entries and subtrees match the reviewed base. In particular, `.github`, `scripts`, `tests`, `theory`, `experiments`, the old research/provenance trees, dependency lock, and public authored status surfaces were not weakened or rewritten to make CI green. The provenance subtree differs only in the release manifest.

The original small publication repairs also remain narrow: CP02's relative link, CP04's unavailable historical-link display, CP05's formula quoting, and explicit private machine-prefix redactions. They are not revised scientific propositions. Sixty event/session JSONL files stay private; this is a documented publication boundary.

## 5. Current-head CI, not old-head evidence

Direct GitHub job reads returned completed success for both runs:

| Event | Run | Job | Result |
|---|---:|---:|---|
| Pull request | 37941131473 | 113855486206 | Success |
| Push | 37941124544 | 113855460724 | Success |

Each returned 74 successful step records. The previously uncompleted gates are now explicitly successful, including:

- internal reference resolution;
- release manifest matching the tree;
- exact PDF clean rebuild, committed-byte equality and text-structure QA;
- Seventh–Twentieth successor source/status integrity.

The old failed runs `37933144539` and `37932931210` are historical evidence for why the repair was needed, not evidence that the repaired head still fails. Conversely, the new success does not erase the old failure or turn packaging into a scientific proof.

No downloadable artifacts were returned for the inspected PR run. The evidence here is direct run/job/step metadata, not a fabricated downloaded CI log. See `evidence/CI_OBSERVATION.json`. The GitHub review and inline-thread lists were empty when read; this report is an independent deliverable to the owner, not a claim that an external human reviewer approved the PR.

## 6. Scientific and publication boundaries checked

The root README, INDEX and CP23 publication guide consistently state ACTIVE status and preserve the split between original evidence and public projections. They acknowledge that historical manifests may reference omitted files or original hashes and that the public projection is not a self-contained replay package.

The CP23 boundary is particularly important: its recorded Lean result concerns the support/cost-pair frontier theorem. The separate certificate-compilation results have written proofs and finite tests with tree-versus-shared-DAG limitations; that publication does not claim a new Lean certificate for the entire compiler or an unrestricted HasE decision procedure. Internal AI reviews are not presented as external specialist peer review.

The restored prior verdicts and source records can remain contested research. A faithful research publication need not wait until every philosophical question is closed. Equally, merger does not make a defeasible common-source appraisal into an unconditional theorem about reality.

## 7. Additional fresh checks in this handoff session

These are supplemental evidence, not substitutes for the PR review:

- All supplied and recovered ZIPs were CRC-tested and recursively inventoried, including nested archive members. Original input hashes were retained.
- The initial live-integration package verifier passed its source/archive checks; its private helper is not part of the published repository workflow.
- CP23, CP24 and the three later research returns passed their integrity-only portable verifiers. Those commands executed no research code or Lean.
- The independent deep-dive's 56 Python tests passed; exact regenerated diagnostic output matched its canonical bytes; before/after source trees were identical. This is fresh finite/rational diagnostic execution only.

No fresh Lean kernel replay, whole-repository local test run, new Arabic scan collation, external expert review or empirical validation is claimed.

## 8. Merge conditions and non-blocking follow-through

The owner may authorise merge of the exact reviewed head provided the branch/base and successful checks remain current and GitHub reports no unresolved merge conflict or newly applicable blocker. The merge operation should use an expected-head guard rather than blindly merging whatever the branch later points to.

After merger, record the actual merge commit and update the *publication* locator. Leave T20 ACTIVE, leave the historical active-time uncertainty unchanged, and do not automatically integrate CP24 or later work. Those later packages need their own source-bound successor publication and review. Their research may continue under the existing mandate while publication is being considered.

There is no need to repeat all historical Lean suites merely because this preservation PR is merged. A later changed proof, source interpretation, authority boundary or build dependency should receive the appropriate scoped review. That is different from granting immunity to the old science.

### Retained original whitespace advisories — not a new repair failure

The complete additive PR retains the original, disclosed strict-whitespace advisories: 198 trailing-whitespace notices (including 38 original CSV CRLF lines) and two blank-at-end-of-file notices. These counts are from the current PR receipt, not a new local whole-repository `git diff --check` execution. The seven affected files were not rewritten in the repair. Its strict and permitted repair-delta checks are reported passing. Preserve the deliberate source-byte boundary rather than silently normalising proof or CSV bytes merely to remove an advisory.

The affected paths, relative to `research/t20-live-20261009/checkpoints/`, are:

```text
CP04/t20-next-frontier-20261008/action-genus-scope-audit/EXACT_EVIDENCE.md
CP04/t20-next-frontier-20261008/productive-sufficiency-scope/inherited/SourceIdentityDerived.lean
CP04/t20-next-frontier-20261008/productive-sufficiency-scope/review/replay/inherited/SourceIdentityDerived.lean
CP06/t20-next-frontier-20261008/bounded-interaction-detection/CORROBORATING_UNARY_CHECK.md
CP11/t20-next-frontier-20261008/skyline-probability-prior-art-review/REVIEW.md
CP19/independent-five-front-supplement/extracted/T20_Independent_Five_Front_Supplement/SOURCE_LEDGER.csv
CP22/READ_FIRST.md
```

## Evidence locators

GitHub PR and commit metadata: `https://github.com/theislampill/orthemology/pull/33` and immutable head/base listed above. Full published subtree: `https://github.com/theislampill/orthemology/tree/76a3218eea53a2484a1c11be4ccd6f3b541ab333/research/t20-live-20261009`.

Original inputs and nested hashes: `../inventory/INPUT_IDENTITIES.json`, `../inventory/ARCHIVE_MEMBERS.jsonl`. Current complete publication match: `evidence/PUBLICATION_RECONSTRUCTION.json`, `evidence/FINAL_PUBLIC_PROJECTION.json`. Execution evidence: `evidence/CI_OBSERVATION.json`, `evidence/deep_dive_fresh_replay/`, and the `fresh_integrity_*` receipts. Later-state details: `../guides/06_POST_CP23_FRONTIER.md`.
