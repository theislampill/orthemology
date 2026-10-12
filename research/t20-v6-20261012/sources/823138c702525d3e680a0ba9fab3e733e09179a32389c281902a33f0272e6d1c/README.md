# Correlated-target fixed-marginal correction

RESULT.md proves that the same inherited full constrained Gaussian metric corrects toward an arbitrary centred correlated Gaussian target with y-marginal N(0,1). The target-dependent conditional spatial score is included in the multiplier. The proof verifies the entire density tangent, obtains the exact coordinate flow, and proves global Gaussian convergence by compact KL sublevels without a new rate claim.

The exact control from I toward covariance [[1,1],[1,2]] creates target-directed cross covariance while retaining the entire y marginal. Cross covariance is not itself an extra conserved coordinate.

Replay:

    python3 verify.py --output-dir private-locator:d6808ce252611792fe1b

From this directory, add `--original-root ..` to verify the unchanged originals as well. Inputs include the previously frozen author and review results plus participating root checks. These are ordinary proofs with supplementary exact controls, not formal-kernel certification, general-law PDE uniqueness, or programme closure.
