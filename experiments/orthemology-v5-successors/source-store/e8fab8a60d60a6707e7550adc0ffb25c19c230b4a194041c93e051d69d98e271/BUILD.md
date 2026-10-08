# Portable SOURCE recipe

This packet contains sources and historical evidence only. No installation, downloads, dependency rebuilding or proof execution is needed during repository integration. Integration checks exact source/projection identities and cheap recipe guards. Optional future mathematical reproduction is explicit and writes only a fresh external directory.

1. Supply an already installed official Linux Lean 4.19.0 executable through LEAN419. Required executable SHA-256: 92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023. This exact binary pin is the tested platform boundary; other platform binaries require a separately reviewed recipe rather than weakening the identity check.
2. Choose a nonexistent output directory whose parent already exists. It must be outside this source tree and the compiler tree. Existing paths, symlink-resolved input-tree paths and missing parents are refused.
3. Run from any directory, supplying the script path as needed:

    python3 formal/replay.py --lean "$LEAN419" --cache "$EXISTING_PREPARATION" --output ../fresh-math122-output

Both historical author and independent Lean runs used -j1 --trust=0. The derived recipe preserves the author flags and all theorem/control checks. New selected-manifest checks do not claim manuscript-source or attribution verification. Any newly produced receipt is a new run and must not reuse historical acceptance labels without inspection.

## Independent review sources

The review/ directory carries exact reviewer Lean modules and selected historical findings/type/axiom evidence. These files were checked in the stated original independent runs. The author recipe does not automatically replay reviewer-authored extra theorems; no such claim is made. To reproduce them, after a successful author build, set LEAN_PATH to its fresh objects directory, plus the same official dependency search roots for math122. Compile the review module with the pinned compiler, explicit --trust=0 and --root set to this package's review/ directory, writing -o only into a separate new external review directory. Run its readback source against that isolated output plus the author/dependency paths. Do not count import/elaboration errors as successful negative controls.

This is a reproduction recipe, not a claim that the public derivative harness or full independent campaign was newly executed during curation. No source input, cache or existing output directory may be changed.

## Explicit additional-review command shape

PACKET is this packet's absolute path; AUTHOR_OUT is a completed fresh author output; REVIEW_OUT must be a new external directory. The canonical-path guard below creates REVIEW_OUT only after checking absence, symlinks and all protected input trees. Set REVIEW_LEAN_PATH to REVIEW_OUT followed by AUTHOR_OUT/objects and the same official cache object roots used by the author recipe, separated by the platform path separator. Do not add arbitrary unverified directories. Then run:

    (
    set -eu
    python3 - "$PACKET" "$AUTHOR_OUT" "$REVIEW_OUT" "$LEAN419" "$EXISTING_PREPARATION" <<'PY_GUARD'
from pathlib import Path
import os, sys
def guarded_output(requested, protected):
    # Check both the user's lexical path and its actual filesystem destination.
    requested = Path(requested)
    if requested.exists() or requested.is_symlink():
        raise RuntimeError('Refusing an existing output path or symlink')
    lexical = Path(os.path.abspath(requested))
    output = requested.resolve()
    for raw in protected:
        raw = Path(raw)
        lexical_root = Path(os.path.abspath(raw))
        actual_root = raw.resolve()
        if lexical.is_relative_to(lexical_root) or output.is_relative_to(actual_root):
            raise RuntimeError('Output must be outside every protected input tree')
        # Internal cache aliases are allowed. Escaping aliases are unsupported,
        # including a dependency directory symlink into a separate object store.
        if actual_root.is_dir():
            for parent, directories, files in os.walk(actual_root, followlinks=False):
                for name in directories + files:
                    item = Path(parent) / name
                    if item.is_symlink() and not item.resolve().is_relative_to(actual_root):
                        raise RuntimeError('Escaping symlinked input layout is unsupported')
    if not output.parent.is_dir():
        raise RuntimeError('Output parent must already exist')
    return output

packet, author, requested, lean = map(Path, sys.argv[1:5])
protected = [packet, author, lean.parent.parent, lean.resolve().parent.parent]
protected += [Path(p) for p in sys.argv[5:]]
if any(not p.is_dir() for p in protected):
    raise SystemExit('Expected existing input directory is absent')
out = guarded_output(requested, protected)
out.mkdir()
PY_GUARD
    LEAN_PATH="$REVIEW_LEAN_PATH" "$LEAN419" --trust=0 --root="$PACKET/review" -o "$REVIEW_OUT/ReviewerCounterchecks.olean" "$PACKET/review/ReviewerCounterchecks.lean"
    LEAN_PATH="$REVIEW_LEAN_PATH" "$LEAN419" --trust=0 "$PACKET/review/ReviewerExtraReadback.lean"
    )

Run each command only if the preceding command succeeded. The review source directory remains read-only. These commands reproduce the additional-review module/readback; they do not repeat historical source-body custody checks or authenticate any interpretation.

## Exact preparation and optional rational checks

EXISTING_PREPARATION contains PREPARATION_RECEIPT.json at SHA-256 4b1c06c026eb6a7e15e6699e67b7322f8514f36fadba9c58e9975e5b0d0dfcf7 and dependencies/<package>/.lake/build/lib/lean. Mathlib revision is c44e0c8ee63ca166450922a373c7409c5d26b00b. This is an existing external cache, not a download recipe.

Optional exact Python checks use only the standard library and write new external receipts:

    python3 -B check_copy_controls.py --output ../new-author-copy-check.json
    python3 -B review/independent_counterchecks.py --output ../new-review-counterchecks.json

Existing, dangling-symlink and source-package output paths are refused. These are distinct finite enumerations and any new receipts must retain that scope. Integration needs only hashes, syntax and refusal checks; it must not silently rerun these or Lean as a broad scientific campaign. The reviewer module's twelve theorems and readbacks are separate from the author's nineteen; the guarded command shape above reproduces that extra module only.

## V5 output-guard correction

This active successor replaces the affected v4 execution recipe without changing v4's sealed bytes or any scientific computation/proof. Both lexical and canonical output paths are checked. Directory/file symlink ancestors inside supplied cache/compiler/predecessor trees are inspected without following directory links: aliases staying within the same protected tree are allowed; escaping layouts are refused before creating output. This prevents writing through a cache/dependencies alias into an external object store. Use this v5 recipe and its manifest rather than the older v4 command sequence. No scientific replay is required for this guard-only change.
