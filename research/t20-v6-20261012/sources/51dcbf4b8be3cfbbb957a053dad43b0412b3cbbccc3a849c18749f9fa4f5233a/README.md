# Correction audit transport

Read RESULT.md for the complete scoped proof and prior-coverage comparison. The addition is an application to the actual OU→normalized-power operator, not a new general kernel-audit or Bayes theorem.

Run from any working directory:

    PYTHONDONTWRITEBYTECODE=1 python3 /path/to/packet/verify.py --output-dir /path/to/replay

Dependencies: Python 3, SymPy, NumPy. The checked environment used Python 3.12.14, SymPy 1.14.0, NumPy 2.3.5; the exact observed version is in each replay result. No dependencies are installed by the checker. Standard and optimized Python run the same explicit checks.

The standalone replay checks all ten copied input hashes and performs 55 mathematical/implementation controls, producing 65 total checks. Add --check-originals only when the original sibling workspace packets remain present; that adds ten original-byte checks, producing 75 checks. Missing originals under that option are a failure, not silently ignored. The ordinary standalone replay needs only this packet and its dependencies.

The three numerical checks call the byte-for-byte inherited gaussian_step.py. They are explicitly labelled floating-point controls. All other mathematical controls use exact SymPy rational/symbolic algebra. No universal proof, stable inverse, finite-dimensional all-law representation, or numerical error certificate is inferred from finite examples.

INPUT_BINDINGS.json pins the predecessor snapshots. SOURCE_READING.json records the bounded reading and prior-coverage findings. AUTHOR_FREEZE.json pins the finished author-stage packet, excluding itself and replay output directories. The result is ready for a separate review decision; no independent-review claim is made here.

No predecessor was changed. No protected edit, integration, commit, publication, or T20 closure is performed or requested.
