# Verification boundaries and reproducible arithmetic

The written RESULT.md proves the all-count separation theorem and the conditional finite-sample test. The independent adversarial mathematical review is finite-panel-replay-robustness-review/REVIEW.md. It reports PASS and binds the exact author hash. The executable script is supplementary and is not kernel verification or a machine check of the entire proof.

Run from the parent base directory:

    python finite-panel-replay-robustness/exact_controls.py

The retained stdout is EXACT_CONTROLS_OUTPUT.txt. The run used Python 3.12.14 and SymPy 1.14.0 and passed 29 exact controls plus six frozen-artifact SHA256 bindings. It checked the delta identity; algebraic margins used to bound the reference probabilities and delta; both final residual constants; the derivative formulas; the scaled convexity factor, midpoint, and half-gap; the sampling coefficient and Hoeffding union-bound equality; and the n=1 specialization.

There is no arbitrary numerical grid or finite exhaustion of unknown m in this script. Uniformity over all m, inequality directions and domain restrictions, the probabilistic gate interpretation, stationarity, and the sampling/error guarantees are mathematical claims established by the written argument and assessed in the independent review.

The entire frozen finite-panel-replay/MANIFEST.sha256 was also checked with sha256sum -c and all entries passed. This robustness sibling has not modified those files and is explicitly excluded from the sixth checkpoint being assembled.

## Review priorities

1. Common marginals and mutual route independence must justify the face-root reduction and both products.
2. Fresh diagonal and paired replay must use the same fixed Bernoulli-pair law; replay must reuse the realized gates without mutation.
3. The entire interpolation segment must satisfy A,B>1/2, all coordinates>1/3, 0<s<=1, and 0<=Q<=1.
4. The F_m gap must bound F_m itself, and derivative bounds must not hide an m-dependent factor.
5. Scaled Holder residuals use a 12 epsilon perturbation; unscaled residuals must not be mixed with that bound.
6. Smaller-count strong convexity and n=1 vacuity must be checked separately.
7. Hoeffding is applied across iid replicates for each statistic; independence of the within-replay three statistics is not assumed.
8. The test targets a fixed exact reference vector. Same-count nonreference alternatives can be rejected.
9. Known/selectable true-rate commands and model contracts are hypotheses, not conclusions or automatically established calibrations.
10. The sample constant is intentionally severe; no practical-efficiency, optimality, empirical-validation, or closure claim follows.
