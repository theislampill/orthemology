# Independent PR #30 / PR #31 integration review

8 October 2026. **Disposition: HOLD combined merge clearance. PR #31 has a demonstrated required-CI failure. No repository or GitHub changes were made by this review.**

## What was independently checked

This review read live GitHub PR metadata, the main branch, commit/tree/parent metadata, compare ancestry, exact-head CI records, PR31 workflow job steps and the decoded PR-job log. It inspected the supplied patch, its change manifest, relevant executable/navigation changes, and the existing report-generation code on GitHub. It read prior review receipts as inherited evidence, not as new executions.

Fresh offline checks matched all ten launch inputs and the original patch identity. All 1,016 patch paths matched the manifest. For each of the 990 new files, the complete payload was recovered from the diff and matched its declared size, SHA-256 and Git blob OID. The 26 modified-file full postimages were not reconstructed locally; GitHub’s exact root-tree match binds the published endpoint to the package’s recorded endpoint. There are no deleted files in that delta.

This is a bounded integration/currentness review, not a fresh reading of every source or a reproof of all mathematics. The earlier PR30 whole-diff review remains inherited. Its 54 commits were not all newly reviewed line by line. A container Git clone failed because GitHub DNS resolution was unavailable; no full local checkout replay is claimed. GitHub connector access succeeded. The supplied local Codex execution handback was not separately opened on the owner’s computer.

## Live boundaries

| Boundary | Commit | Tree / relationship |
|---|---|---|
| main | `19de267cd41d2a5eeeb3eaf0b91562f706e2a916` | `08a6452e50e8e4791d02410d1c1732875e520f2e`; final Sixth |
| PR30 | `fd0903d99d657c35e32fddcc8864d2a77930cf40` | `e7b47c7e3dc18685c33904181d9d31d7cd75495f`; 54 commits ahead of main, zero behind |
| PR31 | `deaa6c1c76a2165f1a18396d47b1b384e311e833` | `32e607c34ed32e9f90fed13bdde294fbc47ca7c2`; immediate parent is PR30 head |

PR30 was open, unmerged and non-draft; PR31 was open, unmerged and draft. Both target main. PR31 inherits the entire PR30 history; it is not a disjoint patch to merge onto the old Sixth tree. The reviews endpoints contained no submitted GitHub reviews for either PR; this does not negate privately recorded model-assisted reviews and does not supply human approval.

PR30’s exact-head `validate` runs 37439428355 and 37439360263 both succeeded. Its checked history/current CI produced no new blocker in this bounded pass. That statement is not blanket independent scientific certification or owner merge authority.

PR31’s PR run 37767773066 and push run 37767662383 both completed with failure at step 34, “Recursive path-aware mutation testing (per-family scope printed)”. The following report-contract, final manifest, PDF clean-rebuild and successor-integrity steps were skipped. Successful infrastructure provisioning is not a successful PDF rebuild.

## Finding P31-01 — generated Task 14 report drift [merge-blocking]

The decoded log from job 113279512088 records:

```
2026-10-08T11:14:11.8509898Z PASS: Task 14 accounted for 77 explicit variants through 154 separate control/mutation command(s).
2026-10-08T11:14:11.8510235Z FAIL: derived Task 14 report has drifted: docs/project-closure/r7e-sol/R7E-SOL-ADVERSARIAL-REPORT.md
2026-10-08T11:14:11.8510472Z TOTAL: 1 failures
```

The published report also records 77 passing variants and zero unjustified survivors. The demonstrated failure is therefore the report equality gate, not an observed rejection of a mathematical theorem. The unchanged generator recomputes the report from executable results, including exact validator/input/observation bindings, and compares the entire text with the committed report. It provides `--write-adversarial-report` and writes only if other gates pass.

The patch modifies code/governance inputs but does not modify either `scripts/validate_recursive_mutations.py` or the generated Task14 report. This establishes that Codex reproduced a prepared tree whose report is now rejected by CI. It does not establish which individual report fields differ. A digest-only explanation is plausible, but must be demonstrated by the regeneration diff; it is not yet verified here.

**Repair:** use the existing generator, inspect every changed report field, refresh only affected derived surfaces/manifests, execute the failing check and `tests/test_task14_adversarial_program.py`, then obtain successful required CI on the actual corrective head/merge candidate. Retain failed evidence. No weakened gate or new historical-science campaign is justified by this failure alone.

## Merge disposition and subsequent order

Do not merge PR31 at `deaa6c1...`. For the requested combined update, keep both PRs unmerged until the corrective result is reviewed. This packet deliberately contains no present merge-authorisation prompt.

After the correction is independently reviewed and CI is successful, the straightforward two-PR route is PR30 first, then PR31, using history-preserving merge commits rather than squashing/rebasing the inherited 54 commits. Recheck live branch rules and exact approved heads before any action. Confirm main contains PR30’s head after its merge; re-evaluate PR31 against that new main. If up-to-date checks require an ancestry-only update, preserve the accepted content tree and obtain checks for the actual resulting candidate. Do not bypass protection or infer success from old-head CI. Stop on conflict or unexpected content drift. Read back final main’s commit, tree, ancestry and CI before informing Dot.

This is a proposed later sequence, not authority to run it now. An alternative single merge of an encompassing descendant would also need explicit owner direction and correct disposition of PR30; do not silently change the agreed workflow.

## Scientific and publication boundary

The merged content, whenever approved, is the frozen 7 October through-T20 snapshot. Later Oct8 checkpoints are privately retained in the launch, not integrated by this patch. T20 remains active. Repository acceptance cannot certify its historical six-hour floor, metaphysical premises, all source interpretations or external scholarly validation.

## Reproducible evidence locators

- PR30: https://github.com/theislampill/orthemology/pull/30
- PR31: https://github.com/theislampill/orthemology/pull/31
- Exact parent/tree: https://api.github.com/repos/theislampill/orthemology/git/commits/deaa6c1c76a2165f1a18396d47b1b384e311e833
- PR30 checks: https://api.github.com/repos/theislampill/orthemology/commits/fd0903d99d657c35e32fddcc8864d2a77930cf40/check-runs
- Failed PR job: https://github.com/theislampill/orthemology/actions/runs/37767773066/job/113279512088
- Failed push job: https://github.com/theislampill/orthemology/actions/runs/37767662383/job/113279152545
- Generator: https://github.com/theislampill/orthemology/blob/deaa6c1c76a2165f1a18396d47b1b384e311e833/scripts/validate_recursive_mutations.py
- Workflow: same commit, `.github/workflows/validate.yml`, recursive mutation/report-contract steps.
- Frozen source: `Orthemology_Codex_FastPath_Launch_v2_20261008.zip`, `inputs/Orthemology_T16_T20_Consolidated_v1_20261007.zip`, `integration/final-patch/`.
- Fresh offline check record: `evidence/LOCAL_BYTE_REVIEW.json` in the companion review bundle.
- Merge-method reference: GitHub official documentation, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github (consulted 8 October 2026). Standard merge commits preserve the source commits; squash/rebase change that history. Repository-specific live rules still govern.
