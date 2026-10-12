# Exact replay

Run from any working directory:

    python /path/to/complete-flow-finite-rank-20261010/check_exact.py

Dependencies: Python 3 and SymPy (author run: SymPy 1.14.0). No network access, package installation, baseline build, or theorem-kernel run is performed by this script. It writes only `EXACT_CHECKS.json` in its own directory.

Retain these sibling predecessor files, at their original relative paths, because the final checks verify the SHA-256 bindings in `INPUT_BINDINGS.json`:

- continuous-signed-finite-rank-20261010/RESULT.md
- transport-rank-boundary-20261010/RESULT.md
- moment-evolution-source-comparison-20261010/RESULT.md
- bounded-energy-signed-continuation-20261010/RESULT.md
- tensor-realizability-extension-20261010/RESULT.md

The script performs exact symbolic controls and input-preservation checks. It does not formally verify the general theorems; their proofs are in RESULT.md. An independent reviewer and parent determine assessment and any integration separately.
