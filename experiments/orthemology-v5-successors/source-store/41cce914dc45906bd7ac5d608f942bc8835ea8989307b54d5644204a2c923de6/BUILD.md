# Portable joint SOURCE recipe

Use an existing official Linux Lean 4.19.0 executable at SHA-256 92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023. Supply the existing preparation root with PREPARATION_RECEIPT.json SHA-256 4b1c06c026eb6a7e15e6699e67b7322f8514f36fadba9c58e9975e5b0d0dfcf7 and official dependency roots dependencies/<package>/.lake/build/lib/lean. No Lake, installer, download or upstream build is invoked. Alternative platform binaries require a separate reviewed recipe; the tested binary pin is not silently weakened.

Cheap integration checks are hashes, exact diffs, Python AST/help and offline harness guards. They do not need proof compilation. Optional source-only reproduction:

    python3 -B reproduce.py ../fresh-joint-output --lean "$LEAN419" --cache "$EXISTING_PREPARATION"

Read-only source/compiler/cache identity checking without Lean:

    python3 -B reproduce.py --check-inputs --lean "$LEAN419" --cache "$EXISTING_PREPARATION"

Offline thirteen-test harness, using fresh temporary fixtures and no Lean:

    python3 -B -m unittest discover -s harness -p 'test_*.py'

The output directory must not exist, be a dangling symlink, or lie under the source package, compiler or cache; its parent must already exist. The runner compiles four exact component cores plus the joint source into that new directory, preserving original -j1 --trust=0 and explicit source-root flags. It checks all declarations/axioms, required calls in actual printed bodies, four exact decide-false diagnostics and unchanged imported-cache identity. A failed run gets its own failure receipt and is never overwritten.

The selected public contract checks exact included sources and external cache hashes. Original private report/specification/review-body custody bindings are historical references, not silently rerun. Curation invokes no Lean. Independent reviewer sources and their scoped PASS are selected under review/. Their original independent five-core rebuild remains distinct from any execution of the author recipe.

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
    LEAN_PATH="$REVIEW_LEAN_PATH" "$LEAN419" -j1 --trust=0 --root="$PACKET/review" -o "$REVIEW_OUT/IndependentJoiningTests.olean" "$PACKET/review/IndependentJoiningTests.lean"
    LEAN_PATH="$REVIEW_LEAN_PATH" "$LEAN419" -j1 --trust=0 "$PACKET/review/IndependentReadback.lean"
    LEAN_PATH="$REVIEW_LEAN_PATH" "$LEAN419" -j1 --trust=0 "$PACKET/review/IndependentRejectedClaims.lean" > "$REVIEW_OUT/rejected.log" 2>&1 && exit 1
    python3 - "$REVIEW_OUT/rejected.log" <<'PY_NEGATIVE'
from pathlib import Path
import sys
t=Path(sys.argv[1]).read_text()
assert t.count("error:")==6
assert t.count("tactic 'decide' proved that the proposition")==6
assert t.count("is false")==6
assert not any(x in t for x in ["unknown identifier", "failed to synthesize", "object file"])
PY_NEGATIVE
    )

Run each command only if the preceding command succeeded. The review source directory remains read-only. These commands reproduce the additional-review module/readback; they do not repeat historical source-body custody checks or authenticate any interpretation.

## V5 output-guard correction

This active successor replaces the affected v4 execution recipe without changing v4's sealed bytes or any scientific computation/proof. Both lexical and canonical output paths are checked. Directory/file symlink ancestors inside supplied cache/compiler/predecessor trees are inspected without following directory links: aliases staying within the same protected tree are allowed; escaping layouts are refused before creating output. This prevents writing through a cache/dependencies alias into an external object store. Use this v5 recipe and its manifest rather than the older v4 command sequence. No scientific replay is required for this guard-only change.
