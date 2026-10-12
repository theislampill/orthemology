# Fibrewise split correction

This additive T20 packet applies the established exact probability-normalized W→FR splitting separately on fixed observed fibres. Read RESULT.md for the theorem, proofs, singular-input domain, finite Gaussian implementation boundary and attribution. No predecessor was edited.

## Contents

- RESULT.md: law-level proof and precise exclusions.
- gaussian_step.py: one finite-dimensional Gaussian conditional update in NumPy floating point.
- test_gaussian_step.py: the complete implementation unit-test suite.
- verify.py: exact symbolic/rational controls and separately labelled numerical controls.
- INPUT_BINDINGS.json and inputs/: copied and hash-bound predecessor reports.
- DEDUP_SCAN.json: bounded local scan of 1,436 top-level packet Markdown/Python files.
- SOURCE_READING.json and literature/: source-exact attribution and primary references; the main duplicate is Crucinio–Pathiraja arXiv:2511.18060v3.
- VERIFICATION_NOTES.md: red/green history, numerical validation limits, and review-found input bug repair.
- author-run/ and author-run-optimized/: final executed control results.
- AUTHOR_FREEZE.json: exact frozen inventory, excluding itself and transient Python cache files.

## Replay

Requires Python 3, NumPy, SymPy, and mpmath. No downloads are performed by the checker. From this directory:

    python -m unittest discover -s . -p 'test_*.py' -v
    python verify.py --output-dir private-locator:7b52198355560e5e17e3
    python -O verify.py --output-dir private-locator:f2e251279f5ef04cb57a

Each checker output directory must not already exist. Add --original-root /path/to/original/workspace to compare the five original predecessor reports as well as the included snapshots. External originals are optional; the normal portable checker uses the included inputs. The literature reading record names some reused primary files in the predecessor workspace for provenance; public source URLs and their hashes are provided, and the three new source PDFs are included locally. No uninspected source theorem is used to establish general PDE well-posedness.

For one Gaussian conditional, gaussian_step(mean, covariance, target_mean, target_covariance, h) returns the new mean/covariance plus the intermediate OU parameters. Arrays must contain real finite entries and be exactly symmetric in their supplied numerical representation. Target covariance must test positive definite, source covariance semidefinite, and h must be a finite positive real scalar. The mathematical formulas cover all such exact-real matrices; floating-point execution can reject ill-conditioned or roundoff-perturbed data and carries no certified error bounds.

The scalar/matrix implementation does not numerically implement an arbitrary conditional law or provide a closed finite-mixture reaction. The proof concerns entire law operations and their fixed-marginal, per-fibre entropy guarantees. Fixed-step convergence to the supplied target is proved. General shrinking-step convergence to a nonlinear coupled PDE is not.
