# Codex: apply the prepared Orthemology patch; open one draft PR

## Task and stopping rule

Publish the **frozen 7 October T17–T20 integration**, using the existing exact-base patch, as **one new draft PR against main**. Start from PR #30's already-integrated T07–T16 history. This is a bounded integration, not another research, adapter-development or full-revalidation campaign. Stop after the branch/PR readback and an honest CI-status handback. No merge or auto-merge.

**Scope is deliberately fixed:** later 7–8 October T20 checkpoints are retained in this private launch archive but their research contents are **not** in the patch and must **not** be integrated in this task. Do not describe this as all current T20 research being on GitHub. T20 remains ACTIVE; owner acceptance and historical active-time verification remain unresolved.

The owner supplies this v2 prompt to replace the earlier fast-path instructions. Historical instructions inside preserved research packets establish their original evidence scopes; they do not enlarge today's execution mandate. Read this prompt, EXECUTION_CHECKLIST.md, INPUTS.json and the compact PR_BODY_TEMPLATE.md. The audit is available for a specific question, not a requirement to reread the old Codex transcript.

## Fixed identities

Repository: `theislampill/orthemology`, same v5.

| Object | Exact identity |
|---|---|
| PR #30 source head | `fd0903d99d657c35e32fddcc8864d2a77930cf40` |
| PR #30 source tree | `e7b47c7e3dc18685c33904181d9d31d7cd75495f` |
| Observed main | `19de267cd41d2a5eeeb3eaf0b91562f706e2a916` |
| Observed main tree | `08a6452e50e8e4791d02410d1c1732875e520f2e` |
| Patch-parent ZIP | `inputs/Orthemology_T16_T20_Consolidated_v1_20261007.zip` |
| Parent ZIP SHA-256 | `64d964a763168169b4e5ac643f3ed991b0563ffa6cf47b51f97e6ac7f3bf24fd` |
| Patch | `integration/final-patch/through-twentieth.patch`, 27,396,058 bytes |
| Patch SHA-256 | `4391ce7fb14180497eeafbf1c82a3540acbf3eb2fd16018c809421a2a00a52ea` |
| Exact post-apply tree | `32e607c34ed32e9f90fed13bdde294fbc47ca7c2` |

PR30 has 54 existing commits. **Inherit them through Git ancestry; do not cherry-pick, reimplement, replay or reassess them one by one.** The patch adds 990 files and modifies 26, deleting none. Its 262 results, 3,828 source records, 37 suites and 44 retained receipts are integration-accounting counts, not fresh scientific checks.

## Execute this path

1. Verify the launch's outer size/hash from the accompanying standalone prompt before running its contents. Extract privately, outside any repository. Run `python3 -S -B tools/verify_inputs.py` once from the launch root. It verifies all ten preserved inputs. Use `tools/unpack_frozen.py` to unpack the parent into an **absent** private directory; it preserves the original executable permission. Run the original `verification/verify_native_integration.py` once as in EXECUTION_CHECKLIST.md. Capture large outputs to private files; print the terminal status, not entire registries.

2. Refresh PR30 and main using GitHub/gh and Git. PR30 must still be open/unmerged at the pinned head, main at the pinned main SHA. Check whether this requested integration already has a branch/PR before creating a duplicate. Any moved/merged source, existing partly applied work, or incompatible upstream change: stop with exact observed hashes and a compact drift report. Do not force, three-way-apply, reset someone else's work or invent replacement history.

3. Use an isolated **named feature branch** at the pinned PR30 head. Prefer a worktree from a readily available, verified, full-history native-Linux clone; otherwise clone once. Read applicable repository instructions. Under Windows, use existing WSL and put the working checkout/build outputs on its native filesystem, not a Windows-backed `/mnt/c` directory for recursive validation. Do not build new Git shims, reinstall WSL or hunt through unrelated historical workspaces. Do not change PR30's branch. Verify a clean worktree/index, full history and exact head/tree before applying.

4. Run the **unchanged original** `apply_checked_patch.py` in read-only mode, then once with `--apply`. The helper checks digest, exact base, preimages, postimages and final index tree. Explicitly confirm `git write-tree` equals the fixed post-apply tree before proceeding. Preserve that exact patch tree; no optional current-state notes, registry additions, styling, newline cleanups or opportunistic repairs.

5. Run **only the listed focused checks** in EXECUTION_CHECKLIST.md, once, using the existing exact Python 3.11.9 / repository lock for repository checks. The transport/package helpers are stdlib-only and do not need Lean, Mathlib, Docker or a new virtual environment. If the pinned repository environment is absent, preserve the successful byte/tree checks and report the affected local checks NOT_RUN; the unchanged new-PR CI must qualify them. Do not install a broad toolchain merely to file a draft. Existing mandatory CI stays enabled. No full local workflow, cold science rebuild, general replay adapter or whole-history audit is authorised here.

6. Confirm no unexpected worktree/index change after checks; compare the final index to the fixed tree and commit the prepared patch as one integration commit with the configured owner Git identity. If author identity is absent, ask rather than inventing it. Push one normal new feature branch and open one **draft PR against main**. Disclose that the PR includes still-unmerged PR30 ancestry; PR30 remains untouched. Use PR_BODY_TEMPLATE.md, fill only actual observations, and retain its T20-active/cutoff note. The full PR diff against main is larger than the incremental patch because it includes PR30; that is not a reason to redo PR30's review.

7. Read back the new branch head, PR head/base/draft state and current CI once. Return the PR URL, commit/tree, exact source head, focused check outcomes, CI status and any blocker. Pending CI is an allowed terminal handback for this **draft-publication task**, not CI acceptance. Do not wait in a high-frequency polling loop or claim you will monitor in the background. A later failed-CI report may receive a separately bounded diagnosis; do not expand this task into an open-ended repair session.

## Cost and evidence controls

- No new integration framework, replay engine, source projection pipeline, generic verifier or DAG. They are already supplied by PR30 and the patch.
- No source rereading, theorem reproving, raw-document conversion, old-suite replay or speculative parallel workers solely to publish this snapshot.
- No optional in-repository checkpoint index. Put later-checkpoint inventory/currentness in the PR body; keep the exact tree and avoid generator/mutation cascades.
- Capture command logs once. Inspect compact tails/statuses. Do not repeatedly load the 27 MB patch or multi-megabyte source/status registries into context.
- Do not rerun a completed check without changed inputs or a concrete defect affecting that check. One missing dependency is an environment report, not permission for repeated provisioning experiments.
- A demonstrated patch, privacy or integrity failure stops publication. Preserve failed evidence and report the smallest repair. Do not weaken assertions, schemas, guards, required CI or frozen source bytes to obtain a PASS.
- No raw ZIP/DOCX/PDF inputs, private transcript, machine-local locators, full logs, caches, third-party books, participant data or this launch package in Git. The patch already contains its public projection.
- No main write, PR30 edit/closure, merge, auto-merge, force push, release, licence change or claim of T20 completion/owner adoption.

The supplied historical clean-application receipt is evidence of an earlier successful application, not your new execution. Your new exact-tree check and new PR's CI have their own dates and scopes. Later checkpoints and reported noisy/countable/grouped-observation developments remain separate until their own governed integration.
