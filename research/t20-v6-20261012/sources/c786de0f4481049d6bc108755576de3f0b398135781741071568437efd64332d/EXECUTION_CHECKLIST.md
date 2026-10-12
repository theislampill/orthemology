# Exact integration checklist

This is the execution plan. Do not replace it with a new DAG. Use this privately; none of these launch files belongs in Git.

## 1. Package, with the standard-library Python already available

Set LAUNCH to this extracted launch root, PACK to the extracted parent root, REPO to the fresh feature worktree and LOGS to a private directory outside REPO. Quote all paths. `python3` below needs Python 3.11+; the launch review used Python 3.13.5. Do not substitute that for the repository's pinned CI environment.

```sh
cd "$LAUNCH"
python3 -S -B tools/verify_inputs.py > "$LOGS/inputs.log" 2>&1
# Continue only on exit 0; this verifies ten inputs, not their mathematical truth.
python3 -S -B tools/unpack_frozen.py \
  --archive inputs/Orthemology_T16_T20_Consolidated_v1_20261007.zip \
  --dest "$PRIVATE_PARENT/ortho-frozen" > "$LOGS/unpack.log" 2>&1
# PRIVATE_PARENT/ortho-frozen must not already exist.
# PACK=$PRIVATE_PARENT/ortho-frozen/Orthemology_T16_T20_Consolidated_v1_20261007
python3 -S -B "$PACK/verification/verify_native_integration.py" \
  --root "$PACK" > "$LOGS/native-bindings.json" 2> "$LOGS/native-bindings.err"
```

Run separately, checking each exit code; do not blindly paste a sequence that continues after failure. Required native terminal: `PASS_ARCHIVE_AND_NATIVE_INTEGRATION_BINDINGS`. The sealed source's `t20/sources/modal-union-v2/lean-v2/replay.sh` retains mode 0755 on Linux. No scientific suite runs during these checks.

## 2. Git preflight and application

First confirm live PR30, main and absence of a duplicate integration as the prompt specifies. Reuse a valid full-history clone via a new worktree or clone once. New feature branch name suggestion: `integration/orthemology-t17-t20-review-20261008`. Never reuse a partly modified destination silently.

```sh
git -C "$REPO" rev-parse --is-shallow-repository
git -C "$REPO" rev-parse HEAD 'HEAD^{tree}'
git -C "$REPO" branch --show-current
git -C "$REPO" status --porcelain --untracked-files=all
python3 -S -B "$PACK/integration/final-patch/apply_checked_patch.py" --repository "$REPO"
python3 -S -B "$PACK/integration/final-patch/apply_checked_patch.py" --repository "$REPO" --apply
git -C "$REPO" write-tree
```

Require non-shallow full history; head `fd0903d99d657c35e32fddcc8864d2a77930cf40`; base tree `e7b47c7e3dc18685c33904181d9d31d7cd75495f`; clean named feature branch before applying. Final tree must be `32e607c34ed32e9f90fed13bdde294fbc47ca7c2`. Do not create fake commits/history to make a gate pass. Do not run `git am` on this raw diff.

## 3. Focused repository checks, before committing

Use PY for the existing **Python 3.11.9 environment with requirements-ci.lock.txt**. Run from REPO; write each output to LOGS. This list follows the supplied clean-application/final affected receipts, rather than starting every old scientific runner.

| Check | Command |
|---|---|
| Current generated state | `"$PY" -B scripts/generate_current_state.py --check` |
| Repository hygiene | `"$PY" -B scripts/validate_repo.py` |
| Internal references | `"$PY" -B scripts/validate_internal_references.py` |
| Successor integrity/preservation | `"$PY" -B scripts/validate_v5_successors.py` |
| T20 frozen-data controls | `"$PY" -B tests/test_v5_twentieth_data.py` |
| T20 reader aliases | `"$PY" -B tests/test_v5_twentieth_reader_references.py` |
| T20 late-owner controls | `"$PY" -B tests/test_v5_twentieth_late_append.py` |
| Deterministic manifest regeneration | `"$PY" -B scripts/make_manifest.py` |
| No regenerated-content drift | `git diff --exit-code` |
| Exact staged-tree preservation | `git write-tree` |

The manifest command is the supplied idempotence check. It must leave the staged/worktree candidate identical; do not fix unexpected values by hand. Before applying, the branch was clean; after applying, the intended changes are staged. Thus `git diff --exit-code` tests unstaged drift without rejecting the intended patch.

Use a bounded timeout (120 seconds per repository check; 5 minutes total for this local check phase). On a slower/unavailable environment, stop the affected phase and report it; do not reinterpret a timeout as a passed or rejected scientific claim. If the pinned environment is unavailable, do not run these with a convenient different interpreter and call them pinned checks. Record NOT_RUN and use the draft PR's mandatory existing CI.

The patch and inherited inputs retain documented whitespace advisories. A global `git diff --check` warning is not permission to rewrite frozen scientific bytes. Inspect new actionable findings without starting a cosmetic cleanup campaign.

## 4. Publish and hand back

Record `git diff --cached --shortstat`, source head, exact tree and focused terminal outcomes. Commit with the configured identity; require the committed tree still equals the expected tree. Use the existing authenticated GitHub connection, not a credential workaround. Push only the new branch, and create one draft PR against main using the private prepared PR body. Verify remote head, PR head/base/draft state, and current CI. Return pending CI honestly instead of repeatedly polling.

The unchanged mandatory workflow, including Docker/Poppler PDF regeneration and native checks, remains the acceptance gate. A quick draft PR is not a promise of quick CI or a green merge. The external R00 review and owner's merge decision are still pending.
