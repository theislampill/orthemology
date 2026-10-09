# Replaying bounded-count noise-aware recovery

`RESULT.md` gives the result and applicability limits. `THEOREMS.md` supplies the
confidence proof, finite rational-arithmetic target, calibration-error budget and
link to the separately reviewed lower bound.

From this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python src/test_robust_masks.py
PYTHONDONTWRITEBYTECODE=1 python src/export_results.py
```

Eleven control groups pass. The exported rational example is a synthetic
bounded-error panel, not empirical data. The twelve budget cases are conservative
analytical sample budgets; those trial counts were not simulated or performed.

In the retained common evidence layout, `src/verify_evidence.py` checks the bound
inputs, runs the tests in an isolated copied layout, and compares deterministic
exports. There are no external runtime dependencies beyond the Python standard
library. Only successor results and temporary copies are written.

The independent review is retained in `../noise-aware-review/REVIEW.md` with its
frozen sources, interval/convolution cross-checks and receipt. Its separate
`RESTRICTED_MASK_LOWER_BOUND.md` matches the exponent of K for the fixed-p mask
family, including adaptive allocation with fixed total budget. It is not a
universal lower bound on all possible experiments.

The interpretation still needs a valid K, a correct productive-route class,
calibration and dependence assumptions, and admitted source-level interventions.
No arithmetic or statistical certificate supplies those premises. Earlier
productive-identifiability and single-calibration-design packages remain frozen.
