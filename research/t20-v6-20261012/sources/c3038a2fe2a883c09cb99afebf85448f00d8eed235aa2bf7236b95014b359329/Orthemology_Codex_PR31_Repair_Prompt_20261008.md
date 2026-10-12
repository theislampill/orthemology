# Codex — repair PR #31’s demonstrated CI blocker; do not restart or merge

I authorise a narrow corrective commit on the existing `theislampill/orthemology` PR #31 branch, followed by a normal push and updated review handback. This is not permission to merge either PR, start another integration, rewrite history, or broaden the research snapshot.

Continue from your preserved worktree and receipts. The reviewed starting head is `deaa6c1c76a2165f1a18396d47b1b384e311e833`, tree `32e607c34ed32e9f90fed13bdde294fbc47ca7c2`, whose parent is PR #30 head `fd0903d99d657c35e32fddcc8864d2a77930cf40`. Fetch the live branch once. Preserve and inspect any intervening changes rather than resetting them. Do not reapply the original patch to an already patched tree.

Independent review found that both initial PR #31 CI runs failed at “Recursive path-aware mutation testing”:
- PR run 37767773066, job 113279512088.
- Push run 37767662383, job 113279152545.

The inspected PR job log ends with:

    PASS: Task 14 accounted for 77 explicit variants through 154 separate control/mutation command(s).
    FAIL: derived Task 14 report has drifted: docs/project-closure/r7e-sol/R7E-SOL-ADVERSARIAL-REPORT.md
    TOTAL: 1 failures

The exact published tree matches the supplied patch: this is not evidence of a bad patch application. The report is absent from the patch’s change list; its generator is unchanged. The cause of each changed report field still needs to be established from the regenerated diff. Do not merely assume all changes are hashes.

## Bounded repair

1. Keep the failed CI evidence and existing successful focused receipts. In the existing pinned Python environment and a native-Linux worktree, inspect the generator and report, then use its real supported entry point:

       python -B scripts/validate_recursive_mutations.py --write-adversarial-report

   The generator permits writing only after its executable gates pass. Do not edit the expected report by hand, disable the comparison, change accepted outcomes, loosen validators or remove tests. If generation fails substantively, investigate that exact failure rather than forcing a refresh.

2. Inspect the report diff. Explain every changed field, distinguishing regenerated validator/input/observation bindings from actual changes in cases, outcomes, scope or prose. Preserve the source and claim content of the frozen research snapshot. A semantic change requires a specific explanation and review; do not conceal it as metadata.

3. Stage the intended change and refresh only dependent generated state and the release manifest using the repository’s existing tools and dependency order. Check for remaining drift. Do not add a new registry, rewrite historical receipts, or update frozen source manifests whose payloads did not change.

4. Run the affected checks, including:

       python -B scripts/validate_recursive_mutations.py
       python -B tests/test_task14_adversarial_program.py

   Also run the existing affected state/convergence and manifest checks. Carry the unchanged scientific evidence at its original scope; do not reprove the tranches or rebuild the old replay adapters. The required GitHub workflow must remain intact, including its later PDF and T07–T20 successor checks, which the failed runs skipped.

5. Commit the correction as a descendant of the existing PR #31 head and push normally to the same branch. Its new tree is expected to differ from `32e607...`; report the new exact head/tree and the narrow diff from `deaa6c1...`. Do not amend the immutable original patch or pretend its old review covers new bytes.

Return the correction diff, generator/check outcomes, new head/tree, and new CI links/results. Avoid repeated polling; a pending-CI handback is acceptable but is not merge acceptance. Stop and explain before any substantial new campaign, unrelated repairs or costly environment reconstruction.

Leave PR #30 and main unchanged. Keep PR #31 draft and auto-merge disabled. T20 remains ACTIVE; this task still publishes only the frozen 7 October snapshot, not the later research checkpoints. Return for independent review before either merge.
