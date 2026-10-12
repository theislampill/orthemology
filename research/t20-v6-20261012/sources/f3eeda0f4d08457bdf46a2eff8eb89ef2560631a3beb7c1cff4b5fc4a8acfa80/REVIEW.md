# PR #33 — independent integration review

**Recommendation: HOLD this revision for three bounded publication fixes and a successful required CI run.**

Reviewed head: `aba0bce3d651ab7f09cb9aa6a31c395e31e900fc`. Base: `3a0bdeaa1394c656245cae9599adcb143e885059`. The PR is open and unmerged; main still points to the base. No remote write, review submission, merge or Dot update was performed.

This is a review of integrating CP01–CP23 plus unnumbered S01, not a re-adjudication of T20 or a fresh theorem-validation campaign. T20 remains active.

## Positive result: the received research was not silently rewritten

I independently checked the 24 supplied source archives and their 2,978 members, reconstructed the approved publication, and compared calculated Git object identities to the actual GitHub tree. Every checkpoint subtree and the complete 2,068-file publication root match:

`a1c05328da48bc6cfc1ff62035aff60155edf26f`

The four generated navigation records were also reconstructed and matched by blob identity. This is exhaustive byte/path/mode correspondence for that subtree, rather than a sample of filenames or trust in Codex's manifest. It proves preservation of the selected bytes; it does not prove the research's conclusions.

The initial projection reconciliation is 1,954 unchanged public files, 60 approved JSONL omissions, and seven changed old public files (five research files plus two navigation records). CP23 adds 105 source projections and two navigation records. The final total is 2,064 projected research files plus four navigation records. All original source archives remain separate private inputs.

The old repository modifications are restricted to the approved `.gitattributes` entry, derived project-state bookkeeping and the release manifest. Existing scientific source/status owners are unchanged. The CSV's CRLF-preservation rule and approved CP08 scratch-prefix repair are present.

A direct container clone failed on DNS. The independent audit therefore reconstructed the publication from the actual mounted source archives and matched its complete tree to GitHub's live content-addressed tree. I did not run the complete repository suite locally. Remote job statuses and the failing job log were separately read through the GitHub connector.

## PR33-R1 — required CI is now failing

Both original runs have finished with failure:

- PR validation: https://github.com/theislampill/orthemology/actions/runs/37933144539
- Push validation: https://github.com/theislampill/orthemology/actions/runs/37932931210

Both stop at step 41, **Internal references resolve (no ghost script/fixture citations)**. In the PR job log, `tests/test_internal_references.py:284`, test `test_unchanged_real_repository_production_validator_passes`, reports three missing paths. These are upstream Spinoza repository paths, not missing Orthemology research:

| Upstream path | Public source locations |
| --- | --- |
| `docs/auxiliary_axioms.md` | CP21 `REFERENCE_ONLY_CODE.json:43`; `spinoza-formal-transfer-screen-20261009/READING_LEDGER.json:96` |
| `docs/coverage.md` | CP21 `spinoza-formal-transfer-screen-20261009/sources/README.md:14` |
| `docs/gaps.md` | The same README, line 138 |

Their declared owner is `Nakammura/spinoza-ethica-lean`, at `6d4c0461265e50a3bbedb640fe60d9ad292b50a7`. `UPSTREAM_REFERENCE_FINDINGS.json` supplies the exact public paths and corresponding pinned upstream URLs.

The first link repair escaped Markdown link syntax, but this second checker also scans bare path strings. Escaping a bracket therefore did not address the failure. The repair must express the external source ownership accurately in the public projection or use a genuinely bounded existing source-context mechanism. Preserve the original records privately and record the projected change. Do not create dummy files in Orthemology's docs directory, suppress the research subtree, or weaken the validator.

The exact PDF rebuild and final Seventh–Twentieth successor integrity step are **SKIPPED**, not passed. Earlier infrastructure provisioning is not a completed PDF rebuild. Earlier hygiene, state, Task 14 and other successful checks retain their limited scopes.

## PR33-R2 — private delivery/linkage metadata remains published

The declared boundary and PR description say delivery metadata stays outside Git. Nevertheless, these files are in the exact live publication:

- `research/t20-live-20261009/checkpoints/CP21/prior-checkpoint-identities/T20_Resumed_Research_Intermediate_Checkpoint20_20261009.LIBRARY_DELIVERY.json`
- `research/t20-live-20261009/checkpoints/CP22/prior-checkpoint-identities/T20_Resumed_Research_Intermediate_Checkpoint21_20261009.LIBRARY_DELIVERY.json`

They contain delivery-message and uploaded-file linkage records. Other otherwise useful research/provenance files also retain literal private Library/file/message IDs. The scoped scan finds 217 opaque identifier occurrences on 214 lines across 39 files: 18 message identifiers, 191 Library-file identifiers, and eight conversation-file identifiers. `PRIVATE_METADATA_FINDINGS.json` lists paths, lines and types **without reproducing the values**.

This is not evidence of a leaked password or that those opaque IDs grant access. It is an unnecessary publication of custody/delivery metadata contrary to the stated boundary. The two delivery records should remain in the original private archives. In remaining necessary reports, replace private linkage values with explicit neutral aliases or public archive/member hash references while preserving distinctions and source relationships. Do not remove a substantive proof, result or source merely because it contains a metadata ID.

The original automated handoff selection admitted these files. Thus this finding is not simply a Codex deviation; the handoff also needed a stronger final boundary review. New public projections require new hashes, and original source/replay hashes must retain their original scope.

These files are already on the public PR commit. A corrective commit cleans the new head but does not erase earlier Git history. No force-push or history rewrite is authorised by this review; any such request needs a separate owner decision. The findings do not establish a credential compromise.

## PR33-R3 — restore the omitted upstream licence notice

CP21 publishes six upstream Lean source files and associated documents. `REFERENCE_ONLY_CODE.json:4` says the original MIT licence is retained, and its lines 70–74 name and hash the source `LICENSE`. The private CP21 archive does contain it. The public projection does not contain it or its copyright/permission notice.

The supplied source's own licence says its copyright and permission notice shall be included with copies or substantial portions of the software. Restore the notice alongside this copied component; no new licensing investigation or re-reading of Spinoza is required. The exact file is included here as `UPSTREAM_LICENSE_TO_RESTORE.txt`:

- Original length: **1,188 bytes**.
- SHA-256: `47b99d4833f7c801c29bdf0e0c8488a6e9f5f5fd26d0a54a816982b783b7e837`.
- Destination: `research/t20-live-20261009/checkpoints/CP21/spinoza-formal-transfer-screen-20261009/sources/LICENSE`.
- Upstream: https://github.com/Nakammura/spinoza-ethica-lean/blob/6d4c0461265e50a3bbedb640fe60d9ad292b50a7/LICENSE

This is restoration of one third-party notice, not selection of a licence for Orthemology as a whole. The archived original and the live pinned upstream blob agree.

## Narrow closure conditions

Keep the same branch and PR. Correct the four external-reference occurrences, remove/sanitise the identified private metadata without losing source distinctions, restore the exact notice, and update only the affected projection inventories/navigation, derived state and release manifest. Preserve all unmodified source bytes and all prior approvals.

Run the failed internal-reference test and validator locally along with affected source/projection/privacy checks and the existing focused integrity checks. Then push the small repair commit and let required CI run normally. Do not relax gates or replace skipped jobs with claims based on the old head. Reuse unchanged checks where their scopes and inputs remain identical; do not re-execute the T20 research.

Before recommendation changes to merge, the new head needs successful required CI, including the previously skipped PDF and final successor gates, and a review of the small repair delta. Do not append later checkpoints while repairing this frozen review boundary unless the owner separately expands scope.

## Limits

This review authenticates and examines the integration, its publication boundary and live workflow evidence. It is AI-assisted review, not human specialist certification. No new Lean replay, philosophical verification, empirical replication, exhaustive licence inventory or general secrets clearance is claimed. The absence of a literal regex match alone is not universal privacy clearance.
