# Replay and scope

Use Python 3 and SymPy. The author executions used Python 3.12.14 and SymPy 1.14.0.

    python check_exact.py --output-dir /absolute/path/to/a/fresh-output-directory

The script refuses an existing output directory and writes EXACT_CHECKS.json only after all controls pass. It performs no network operation and never writes a predecessor. The portable run has 85 checks: 79 symbolic controls plus six copied-input hash checks. Compare its output with portable-author-run/EXACT_CHECKS.json when using the recorded runtime versions.

Optionally check the original inspected files as well:

    python check_exact.py --output-dir /absolute/fresh/output --original-root private-locator:8f24556a330b05a11a95

The original-root run has 91 checks, adding six checks that those original files remain unchanged. The historical author-run report records that execution. Original-root paths need not exist when replaying a copied packet; use the portable command there.

The ordinary universal proofs are in RESULT.md. The exact algebra checks are controls, not a numerical simulation or a proof of the Łojasiewicz inequality, Tarski–Seidenberg or Sard theorem. Input bindings record bounded local ancestry. No source paper is redistributed. No formal-kernel, independent-review, protected-integration or programme-closure status is conferred by a passing run.

FROZEN_MANIFEST.json hashes the author packet after verification. New review or replay outputs belong outside that frozen directory; the manifest cannot grant closure authority.
