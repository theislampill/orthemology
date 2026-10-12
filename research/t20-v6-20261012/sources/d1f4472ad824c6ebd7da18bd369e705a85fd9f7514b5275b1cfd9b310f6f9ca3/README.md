# Fixed-marginal constrained correction: portable evidence

This preserves the accepted additive fixed-marginal correction, its frozen ordinary review, and the participating root algebra. All 48 files in the three original folders are unchanged, including the review's exact author snapshot, proof reports, primary-source locators, freezes, manifests, binding records, checker scripts and recorded outputs. ORIGINAL_BINDINGS.json and PRESERVATION_SCOPE.json record custody and the bounded result. No raw third-party PDFs or private notes are included. Historical absolute paths inside unchanged custody records are provenance only; portable replay does not use them.

## What the result establishes

The author report gives the full constrained tangent gradient, a coercive weak multiplier solve, and a globally convergent exact Gaussian construction. General nonlinear PDE existence and uniqueness remain outside the result. The review reports no blocking mathematical finding within the stated hypotheses. It also clarifies that conditional reaction recentering is marginal-feasible but not the full constrained optimum. The rate-six Gaussian entropy inequality, Dc >= 6 E, was supplied by the reviewer and is participating work, not independent certification by its originator. The root algebra is participating as well.

The 50 final separate-reviewer controls include checks of that participating extension; the count must not be read as 50 independently originated results. The initial reviewer script and its 39 passing controls remain under snapshots/. An initial recentering label was corrected before review freeze; the final checker explicitly separates feasibility from the optimality gap. The original record is retained, not silently replaced.

## Replay

Use Python 3 with SymPy; this archive was tested using Python 3.12.14 and SymPy 1.14.0. requirements.txt records the tested SymPy version. No network access or original workspace is needed once dependencies are available.

From the extracted archive root, use fresh output directories outside the evidence tree:

    python3 replay.py --output-dir private-locator:fa08a2597b58379b8cd7
    python3 -O replay.py --output-dir private-locator:9e4908da5f4218924702

To replay the normal and optimized inventory-tampering controls on disposable copies:

    python3 test_inventory.py --output private-locator:cdf3408ae27872875201

For inventory and pins alone (Python standard library only):

    python3 replay.py --inventory-only

Each replay runs unchanged direct-author and reviewer-snapshot controls (43 each), the final reviewer checker (50), and root participating algebra (8). These are overlapping checks, not an aggregate theorem count. Historical 49-control author records include six optional original-location checks; those six are not replayed portably, while their retained snapshot identities are checked. The original six live bindings were verified during packaging. Output receipts retain interpreter and dependency versions and report byte equality against saved records. Mathematical records are compared independently of version-label fields so a label change is not confused with a changed control result.

The wrapper verifies the exact file inventory and every file's size/SHA-256, along with author/review pins, both source manifests, author snapshot agreement and root custody. It rejects changed, missing, extra, duplicate-entry and symlink content. Its failure gates remain active under -O; it explicitly checks the root JSON because that historical script uses an assert. Outputs are required to be outside the evidence tree so a replay cannot overwrite retained records.

MANIFEST.json covers every archive file except itself. External archive SHA-256 and the packaging receipt provide the outer identity; the self-contained manifest is an integrity inventory, not a signature against someone who rewrites the entire archive. Retained manifests were not amended. PACKAGING_VALIDATION.json records staging-copy checks; the separate outer receipt records fresh-extraction replay of the final archive.

## Limits

Symbolic controls supplement ordinary Hilbert, regularity, inequality and ODE proofs; they are not a formal-kernel proof or general PDE certification. Primary-source reading records preserve bounded locators and attribution only. Packaging adds no new literature-reading or priority claim, mathematical review, owner-acceptance decision, protected edit, integration, new research duration, or programme closure.
