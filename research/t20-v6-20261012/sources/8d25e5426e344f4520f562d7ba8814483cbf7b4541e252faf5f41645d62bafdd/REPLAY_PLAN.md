# Portable replay instructions

Requirements: Python 3 and SymPy 1.14.0. The included replay uses local exact arithmetic and retained text; no network or PDF is needed.

From a fresh extracted packet root:

    python verify_packet.py --output-dir private-locator:a978d6367c5ca43a25f1

The output directory must not exist and must be outside the immutable packet. The command verifies exhaustive payload hashes, both review scopes and source bindings, restores and checks the exact previous 43-file staging snapshot, executes all six original control scripts, compares stdout byte-for-byte with their preserved logs, and rechecks hashes afterward. It records stdout, stderr, exit codes, count markers and source checks in the requested external directory.

Expected suites: information 61; fixed-reference noetic 33; quadratic independent review 45; state-dependent obstruction 19; tensor continuation 21; tensor independent review 38. They overlap and should not be interpreted as an additive measure of theorem strength.

The original scope-A replay helper remains available as `geometry-transport-independent-review-20261009/verify_review.py`; the portable final verifier performs its artifact/source checks and runs the same three mathematical scripts alongside the three scope-B scripts.

Final preservation procedure: ZIP integrity and safe paths must be checked, fresh extraction must use a genuinely new directory, all checks must pass before and after execution, and an external receipt must bind the ZIP size/hash, final manifest, extraction path and actual replay outputs. The supplied external receipt records those operations for the delivered bytes. Any change invalidates automatic application of the old archive receipt; changes to reviewed targets also require applicable updated mathematical review.

The philosophical/source note has no independent mathematical certification script. Its retained byte bindings and witness metadata are checked as such. Replaying mathematics does not certify its interpretation, omitted scans or any actual normative authority. No closure, integration or owner acceptance is inferred.
