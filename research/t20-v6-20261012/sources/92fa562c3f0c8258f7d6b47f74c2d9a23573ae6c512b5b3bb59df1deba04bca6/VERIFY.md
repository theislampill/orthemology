# Exact-base patch verification

The patch targets fd0903d99d657c35e32fddcc8864d2a77930cf40 only. Start from a fresh local clone with that exact HEAD. Do not apply it on a moved branch or overwrite local work; reconcile any upstream drift separately.

First run `python apply_checked_patch.py --repository /path/to/fresh-clone` for a read-only preimage/application check. Create an isolated named feature branch first, for example `git switch -c integration/t20-review`. Add `--apply` only when ready to modify that branch's worktree and index. Applying on main, master or detached HEAD is refused; a read-only check on main is permitted. The helper checks the complete patch digest, clean state, changed-file preimages, Git applicability, final postimages and reviewed candidate tree. It does not commit or contact a remote.

Use the repository's exact Python 3.11.9 and unchanged requirements-ci.lock.txt. The source-preservation tests and production successor validator are ordinary bounded integrity checks. The existing workflow remains the authoritative full check list. No historical Lean replay or new scientific campaign is required merely to apply the archive patch.

The local preparation cannot perform the mandatory exact Docker/Poppler PDF clean rebuild. The separate carried-artifact verification establishes unchanged source/artifact identities at its stated scope and does not replace that gate. Do not install a substitute renderer or report the full workflow as green without the required supported environment. Subsequent authorized PR CI must run the unchanged mandatory gate.

The separate final verification record names initial failures, bounded corrections, final affected passes, the prior whole-diff review at fadbecad, the independent successor delta/preservation review, and fresh successor clean-apply results. Those outcomes apply to the exact tree/digests in PATCH_MANIFEST.json. Original scientific execution, source reading, receiving-integration status and owner adoption remain distinct.

This packet is the full current patch against fd0903d. Apply it once to a clean base, not on top of the earlier checkpoint patch. The earlier complete packet remains a separate local historical checkpoint. The source-context append retains 262 results, 3,828 sources, 37 suites and 44 native receipts. See VERIFICATION.json for distinct inherited and current evidence scopes.
