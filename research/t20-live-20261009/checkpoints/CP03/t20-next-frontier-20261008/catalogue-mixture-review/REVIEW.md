# Independent catalogue-mixture sampling review

8 October 2026 UTC. Reviewed author manifest SHA-256 `4cc3ee6c2eef3ea291e020bd3a62638694c2ed3f492ad32519cb4fb3a3932ea1`. All eight listed author file lengths and hashes were checked, copied, and checked again after replay. No author or prior frozen-stage file was edited.

## Conclusion

No scoped mathematical blocker was found. The known-catalogue contrast construction, Hoeffding confidence radius, Bernstein derivative calibration allowance, strict support threshold, disclosed 40,000-group example, and separated unknown-label obstruction are correct under their stated assumptions.

The review also proves two useful extensions in `REVIEW_EXTENSIONS.md`: unequal independent within-group propensities retain the same calibration allowance when each has a certified error bound; an independently certified conditional joint-law TV deviation adds an oscillation-times-TV allowance. These are separate reviewer results, not silent changes to the frozen author's model. Neither relaxes the independent-groups requirement of the concentration proof.

## Main mathematical checks

### Exact contrast inversion

The count statistic `(S)_r/(R)_r` has expectation `theta^r` for conditionally iid Bernoulli repetitions. With `R=N−1`, substituting these statistics into each catalogue Lagrange polynomial gives an unbiased estimate of its corresponding weight at nominal calibration. The Bernstein coefficients are exactly these count contrasts, not the polynomial's values on an equally spaced grid. The identity `sum_i b_i(s)=1` explains the raw vector's exact unit sum even when individual estimates are negative or exceed one.

Enumerating all possible counts gives the genuine finite range width `B_i`. Coordinate dependence is harmless for a union bound. Independence across groups, including any shared random calibration effects, is a different matter and is explicitly assumed.

### Concentration and support

The supplied exponential-tilting derivation has the correct constant: the tilted variance is at most `B_i^2/4`; integrating twice bounds the centered log mgf by `lambda^2 B_i^2/8`; independence and exponential Markov give the two-sided exponent `−2nt^2/B_i^2`. The zero-range case is treated separately. A union bound at `log(2N/delta)` is valid even if conservative.

The mean-value calibration term is bounded by `D_i beta`. The Bernstein adjacent-difference formula gives `D_i=R max_s|b_i(s+1)−b_i(s)|`, an exact rational global derivative bound. No grid-only numerical maximum is used. Telescoping route-success products and then occurrence-level failure products justifies the port-error bound, including multiplicities and its cap at one, provided the route law and independence model actually hold.

If every positive weight is at least `w_min` and the total simultaneous error is strictly below `w_min/2`, thresholding the raw estimates at `w_min/2` recovers the support on that event. The strict sample-size inequality is correct. Clipping is harmless for this threshold, while renormalization is rightly left unclaimed. Exact recovery concerns the discrete support, not arbitrary real weight values. For the single-label catalogue no observations are necessary.

### Numeric example and failure controls

For codes `(1,3/4,9/16)`, independent inversion of the full binomial count-probability matrix recovers the displayed contrast rows, range widths `(6,50/3,32/3)`, and derivative certificates `(12,100/3,64/3)`.

At `delta=1/20`, `w_min=1/3`, `beta<=1/1000`, and `n=40000` two-repeat groups, the maximum calibration allowance is `1/30`. The remaining half-floor margin is `2/15`; the exact check `5/288<(2/15)^2` and a finite Taylor proof of `exp(5)>120` certify the sampling term. This is 80,000 endpoint observations under a sufficient design, not an actual experiment or optimal sample count.

The large-calibration counterexample genuinely converges to the wrong catalogue support. The tie example is appropriately distinguished: convergence to the threshold does not imply eventual selection of neither label. The shared-latent-across-all-groups example has the correct endpoint covariance `1/64` and limiting contrast variance `1/4`, so correct marginal group laws cannot replace independent groups.

### Unknown labels and total variation

Adding one fresh high-index route to every component makes every label new while multiplying all scalar nodes by `1−eta`. It preserves the weights and any prescribed internal separation strictly below the baseline gap for sufficiently small `eta`. Common-uniform Bernoulli coupling gives full group mismatch probability at most `R eta` and total variation at most `M eta` for a fixed finite collection of groups with `M` endpoints.

The two-support testing argument therefore lower-bounds the worst error by `(1−M eta)/2`. Taking successively rarer routes establishes a supremum error at least one half for each fixed finite budget over any class containing this baseline and its perturbations. The statement correctly uses a baseline with separation slack; it does not assert existence for infeasible combinations of component count and prescribed separation. Randomized estimators do not escape the two-point inequality, since their independent randomization is another common Markov kernel.

This is an obstruction to uniform exact-label recovery at the fixed calibration. It does not prohibit pointwise consistency, approximate node recovery, stronger interventions, or finite-catalogue recovery, and does not contradict exact-population identifiability. Internal separation compares labels present together; it does not isolate a label from all possible alternatives.

## Independent evidence

The frozen author's fifteen exact rational control families replay successfully, including identical regenerated JSON. Five reviewer control families pass:

1. Twenty catalogues inverted directly from complete binomial probability matrices, independently of the author's polynomial implementation.
2. One hundred sixty-eight unequal-propensity groups computed by exact Poisson-binomial convolution, validating the new adjacent-difference sensitivity bound.
3. Fifty-six conditional joint-law contamination checks validating calibration plus `B_i` times TV bias.
4. Twenty-seven exact finite binomial tails compared with rigorously bounded exponential expressions, including nontrivial bounds. This is stronger evidence than the author's deliberately loose single tail example, but remains finite checking.
5. The disclosed 40,000-group budget independently recomputed, its new joint-law allowance `gamma<=1/20000` checked, and a two-group rare-route TV control.

All computations use integer/rational standard-library arithmetic. They are finite controls of separately assessed general proofs, not Monte Carlo experiments, measured calibration, a formal kernel theorem, or universal tests by enumeration.

## Evidence boundaries

The eligible-histogram scalar injection and grouped model remain imported from frozen earlier stages. Calibration bounds, catalogue completeness, route/episode/group independence, and joint-law TV certificates require independent warrant. The probability bounds do not establish these premises, physical mechanisms, underived ownership, original efficacy, or completeness of actual productive reality. Classical interpolation, concentration and testing are not claimed as new general results. No priority assessment or active-time floor is certified.

## Portable replay

From this review directory:

`PYTHONDONTWRITEBYTECODE=1 PYTHONOPTIMIZE=0 python frozen/exact_controls.py`

`PYTHONDONTWRITEBYTECODE=1 PYTHONOPTIMIZE=0 python independent_checks.py`

`python verify_receipt.py`

Python 3 standard library only. The frozen author script rewrites its local `frozen/results/exact_controls.json`; the reproduced bytes match the original manifest. No original author file, network resource, package installation, Lean environment, or sibling import is needed for replay.

The mathematical predecessor binds to grouped-author manifest `baf29c6df8ba1047782a03f794409bf03a0bfe8394f04845bb2b876b6bcc75f6` and grouped-review receipt `9294b54421ca4f9c431dae254bc1126134e0fb5d349018f488a00b4180243673`. This review is later than, and separate from, the intermediate checkpoint already being assembled. No packaging, integration, acceptance, or closure authority is exercised here.
