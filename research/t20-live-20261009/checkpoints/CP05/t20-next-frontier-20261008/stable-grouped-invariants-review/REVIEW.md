# Independent review: stable grouped calibration invariants

8 October 2026 UTC.

Status: FINAL PASS on the author payloads identified in FINAL_BINDINGS.json. The final authored deliverables have been inspected, their exact controls independently replayed, and the synthetic observation histogram independently transformed back into its factorial moments. No frozen source has been modified by this review. All files created by this review are confined to this sibling directory.

## Final verdict

The proposed core theorem and the optional matched-weight extension are mathematically sound under the stated promises. In particular, a known finite count ceiling, a known positive lower bound on every supported component weight (including count zero), a shared static calibration value in the stated interior band, held-count conditionally independent repetitions, and independent groups jointly support the explicit finite-sample guarantee. No exact real-equality oracle is needed by the grid estimator.

The following presentational points were raised during review and are resolved in the bound final text:

1. The final main theorem restricts 0 < delta <= 1/2, making its O(M^(8C) log(1/delta)) statement uniform over the declared range. On all 0 < delta < 1 the corresponding expression would instead be O(M^(8C) [1 + log(1/delta)]).
2. The final text explicitly gives the rational-delta power-of-two logarithm upper bound, avoiding an exact ceiling comparison at an unknown transcendental boundary.
3. The rounded-weight l1 bound is non-strict and expressly includes zero error for s=1.
4. The missing-count-ceiling obstruction now keeps t fixed and compares pure count n with an equal-weight mixture on {n,n+1}. Its group total variation is at most R(1-t)t^n/2. The frozen changing-rate example is not incorrectly imported under a separately retained fixed rate window.
5. The initial control script omitted math.prod. The failure was retained and disclosed, the import was fixed, and the entire final thirteen-family script passes independent replay. This was a harness defect, not a changed mathematical constant.

## Core proof audit

### Uniform atom floor and gap

Set a = 3/(2M), so 0 < a <= 1/2. Concavity of log on [1/2,1] gives log(1-a) >= 2a log(1/2). Multiplication by M gives (1-3/(2M))^M >= 1/8. Thus every scalar atom t^j, 0 <= j <= M, lies in [1/8,1].

For any two distinct counts, the smallest adjacent difference is bounded below by

(1-t)t^j >= [1/(2M)] [1/8] = 1/(16M).

The argument also covers the scalar atom 1 for count zero. It requires the count-zero empty-inventory convention rather than an endpoint ambiguity; the calibration band here is strictly interior.

### Hausdorff matching and primitive recovery

Put epsilon_0 = 1/(32M^2). If two atom supports are at Hausdorff distance h < epsilon_0, their minimum within-support separation and 2h < 1/(16M) imply unique bijective nearest matching. Ordered matching follows from the separation. An atom at 1 cannot be matched to a positive-count atom: the latter is at most 1-1/(2M). Thus zero presence agrees.

For matched positive counts j_i and ell_i, put u = -log(t), v = -log(s). Since all atoms are at least 1/8, the logarithm is 8-Lipschitz on their interval, so |j_i u - ell_i v| <= 8h. Since ell_i,ell_k <= M,

|(j_i ell_k - j_k ell_i) u| <= 16Mh < 1/(2M) <= u.

The determinant is an integer, hence zero. With at least one positive count, all positive count ratios agree. Reduction by each support's gcd therefore gives the same increasing primitive vector. A singleton positive support always gives (1). If no positive count is present, matching and zero presence imply both targets are the empty primitive vector with the zero flag set. Hence different targets require Hausdorff distance at least epsilon_0.

### Moment separation

More generally, let epsilon <= epsilon_0 and suppose the two supports have Hausdorff distance at least epsilon. There is an atom a in one support at distance at least epsilon from every atom of the other support B. Form

P(z) = product_(b in B) (z-b)^2.

Its degree is at most 2C, it vanishes on B, and it is nonnegative. If the first measure gives a weight at least w/2 to a, its integral of P is at least (w/2) epsilon^(2|B|), which is at least (w/2) epsilon^(2C). The polynomial coefficient l1 norm is at most product_(b in B)(1+b)^2 <= 4^C. Both zeroth moments are exactly one, so the constant coefficient contributes nothing to their difference. Therefore some moment order 1,...,2C differs by at least

D(epsilon) = (w/2) epsilon^(2C) / 4^C.

This proof does not assume signs of moment differences, because nonnegative annihilation is established before the coefficient triangle inequality.

### Rational grid approximation

For Q = ceil(32C/D), retain the true count support. Floor the first s-1 weights to multiples of 1/Q and put the leftover mass on the last weight. Their l1 change is at most 2(s-1)/Q <= 2(C-1)/Q (strict in the first bound when s>1; zero when s=1). The first s-1 rounded weights remain at least w-1/Q >= w/2; the last increases and remains at least w. In particular the grid includes an approximation to every promised true world, even when one or more true weights equal w exactly.

The survival interval has width 1/M. Rounding t downward to the grid with step 1/(MQ) changes t by less than that step and keeps it in the interval. For moment order r <= 2C and count j <= M, the derivative of t^(rj) is at most rj <= 2CM. The survival-rounding contribution to a moment is at most 2C/Q. Total moment error is therefore at most 4C/Q <= D/8.

All enumerated supports, weights, survival values, predicted moments, empirical factorial moments, and discrepancy comparisons are rational. A finite lexicographic tie-break suffices. The algorithm does not compute logarithms, Hausdorff matching, unknown true atoms, or integer relations in approximate real numbers; those occur only in its correctness proof.

### Concentration and selection

For a group sum S from R = 2C repeats, the statistic (S)_r/(R)_r = binom(S,r)/binom(R,r) lies in [0,1] and has expectation m_r. Hoeffding and the union bound give

P(max_(1 <= r <= 2C) |hat m_r - m_r| > D/8) <= 4C exp(-n D^2/32).

Thus n >= 32 D^(-2) log(4C/delta) suffices. The true-world grid approximation is within D/8 of its population moments, and on the confidence event it is within D/4 of the empirical vector. A discrepancy minimizer is no worse, and is therefore within 3D/8 of the true population vector. Since 3D/8 < D, the selected candidate has the correct primitive vector and zero flag. The endpoint count is 2Cn. Exact absolute counts and exact arbitrary real weights are not certified.

## Optional matched-weight extension

Let A=(32M)^(C-1), B=C(16M)^(C-1), epsilon=min(epsilon_0, alpha/(2B)), D=D(epsilon), and tau=min(D/8, alpha/(6A)). Choose Q=ceil(4C/tau) and n >= log(4C/delta)/(2 tau^2). The same rounding argument gives an admissible grid approximation within tau, and the same selection proof gives selected population moments within 3tau.

Because 3tau < D, the general annihilator argument forces Hausdorff distance h < epsilon; unique rank matching and target equality follow. For the true support q_1,...,q_s, let L_i be its Lagrange polynomial. The minimum gap 1/(16M) gives coefficient l1 norm at most (32M)^(s-1) <= A. Product-rule differentiation on [0,1] gives sup |L_i'| <= (s-1)(16M)^(s-1) <= B; when s=1 the derivative is exactly zero. Integrating L_i against the moment difference contributes at most 3A tau, while moving matched candidate nodes to true nodes contributes at most Bh. Consequently every matched weight, including a present count-zero mass, is estimated within

3A tau + Bh <= alpha.

This is an approximate-weight result; it does not turn sampled data into exact arbitrary real mixture weights.

## Reproducible independent controls

Run `python exact_checks.py` in this directory. The adjacent `exact_checks.json` records:

- 252 endpoint floor/gap worlds for M=3,...,128;
- 28,905 exact rational support/calibration pair comparisons for M=3,...,6;
- a distinct-dilation equality with supports {2,4} and {3,6} at survivals (23/25)^3 and (23/25)^2;
- 18 exact squared-annihilator controls, including count-zero cases;
- 30 exact grid-rounding controls, including the optional weight extension;
- 140 exact factorial-moment identities;
- 30 exact Lagrange coefficient/derivative certificates.

All independent controls passed on the initial review run. The final author script was additionally copied into author_replay/, run with all thirteen families passing, and its two generated JSON artifacts matched the author outputs byte-for-byte. These are finite regression checks and do not replace the general proofs above.

WITNESS_REPLAY.md records all five actual synthetic integer group-count frequencies and the full observation-to-factorial calculation. Starting independently from that histogram gives (89/200, 44807/200000, 25364801/200000000, 15697326743/200000000000). The concrete rounded candidate satisfies the lower weight floor, rate grid, sample budget, and 2tau acceptance radius. Its nonzero rounding and exact rational residual were independently recomputed. No endpoint samples were collected and no full-grid minimizer was executed.

Run `python verify_review.py` to recheck all bound author files, the nineteen inherited payloads and three separately recorded inputs, author-output replay identity, and the histogram/candidate arithmetic. Hash agreement certifies unchanged bytes, not independent rereading or re-execution of every predecessor artifact.

## Scope boundary

The finite-sample result is conditional on the stated model and promises. It does not certify independent groups, within-group conditional independence, latent-count persistence, common calibration across labels or groups, the count ceiling, or the weight floor from the same data. It identifies anonymous primitive multiplicity ranks and optionally estimates their weights. It does not establish absolute count scales, route identities, physical bearers, or metaphysical conclusions. No frozen integration or formal verification is asserted.

## Final digest binding

The full list of fourteen bound author payloads is in FINAL_BINDINGS.json. Central SHA-256 identities are:

- RESULT.md: 26d166457d00adf2bae099a0eed045b156a4efc3a645243eb988ead693cd973b
- WEIGHT_ESTIMATION.md: fe92baa99af6213fc6bab026d2d74d3dfb318cf63dc2d2ce3170d3c73a77f32f
- NEGATIVE_CONTROLS.md: 5c91827dfe28897c73e2606397edc86886f034f832c2ece3493dd05cc9a0f639
- exact_controls.py: bb247d16c51a1427fa13226c396bedc3fbab02d1062e353382deabee587c57b9
- results/GRID_WITNESS.json: 521dc54a035408817863d03ad46ce871e47a402b5d056d25dc9916384fe03677

This verdict is confined to those bytes and mathematical claims. No remaining substantive or boundary defect was found. The reviewer did not independently obtain the external primary-paper bodies mentioned in the author's ancestry note; the used concentration identity and constants are reproduced in the inspected inherited text, and the new proof is self-contained. No field-wide novelty, actual process validation, formal kernel proof, efficient runtime, absolute-count recovery, protected integration, or task closure is certified.
