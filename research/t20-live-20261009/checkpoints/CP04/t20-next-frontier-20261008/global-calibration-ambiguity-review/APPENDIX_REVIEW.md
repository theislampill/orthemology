# Independent digest-bound review of the efficiency appendix

## Verdict and exact scope

PASS. The clipped-map lower bound, sufficient catalogue construction, and fixed-confidence polynomial-budget equivalence in the supplied appendix are mathematically correct in the stated conditional endpoint model. No unresolved correction remains.

This review binds these final source bytes:

- `../global-calibration-ambiguity/POLYNOMIAL_EFFICIENCY_APPENDIX.md`: SHA-256 `4242d8cbcc9fd576266e2ee01f902b45c93e6701b5c01d07a5a0c3909f97f0f4`
- Main model and theorem dependency, `../global-calibration-ambiguity/RESULT.md`: SHA-256 `ec620e491fd1c58cdc9dc0bcc8700784b79b4b399247ca1e2a235438138cf827`
- Author appendix controls, `../global-calibration-ambiguity/efficiency_controls.py`: SHA-256 `968268172209211e9c7dff218cc3a9acc97f6f765aac53d8569992dd1a239a6f`
- Author control output, `../global-calibration-ambiguity/results/efficiency_controls.json`: SHA-256 `1f410340c77564bf6d9aad1a3e6af66afb04275694fadb4d379e0f32b8b0ffc2`

The complete appendix was read, its proof independently rederived, its controls inspected and replayed from a review-only copy, and separate controls implemented. This binding is separate from the main review and does not alter that receipt. It conveys mathematical assessment, not release, protected integration, or T20 closure authority.

## Independent proof assessment

### Clipped static maps and the geometric inequality

For each fixed nonnegative error allowance, the two clipped maps are respectively the minimum and maximum of continuous strictly increasing functions. Strict monotonicity follows because, at two ordered inputs, each of the candidate functions increases strictly; this property is preserved by the minimum or maximum. The stated sandwich bounds establish range, endpoint preservation, and the uniform error band even when `x±eta` by itself lies outside `[0,1]`.

The identity `d(x)<=x/(2k+1)` is equivalent to `u^k[(k+1)-ku]<=1`. Its derivative is `k(k+1)u^(k-1)(1-u)`, so the maximum occurs at `u=1`. This geometric step and its constant are correct.

When `d<=eta`, the boundary maps are unchanged and their full Bernoulli kernels coincide. When `d>eta`, the actual rates are exactly `x±eta`, both in range, and the common boundary no-hit probability lies between the two new probabilities. Consequently their nonnegative difference is at most `(1-x-eta)^k`. The geometric inequality gives `x+eta>2(k+1)eta`, and `1-z<=exp(-z)` supplies the claimed uniform exponential bound. This argument also covers `eta=0`; at or above the main threshold the stronger exact equality obstruction applies.

### Adaptive testing lower bound

Under a shared random seed, identical histories select identical commands. Coupling until the first outcome mismatch and applying the finite-budget union bound yields the claimed transcript total-variation bound for every randomized adaptive protocol with at most `N` endpoint observations. Success at both adjacent counts forces TV at least `1-2delta`, including when all nonreturns and abstentions count as failure. The resulting lower bounds `N>=(1-2delta)exp[2k(k+1)eta]` and its catalogue specialization are correct. They are deliberately weak near `eta=0` and are not expected-stopping-time bounds.

### Upper construction and constants

Under `eta<=1/(16M)`, choosing `x=max{1/M,8M eta}` indeed gives `1/M<=x<=1/2`, `eta<=x/(8M)`, and unclipped survival endpoints `0<A<=B<1` with `B>=1/2`.

Bernoulli's inequality gives

`g >= B^(M-1)[x-eta-2(M-1)eta/B]`.

Using `B>=1/2` replaces the bracket by at least `x-(4M-3)eta`. This is greater than or equal to `x/2`, since `(4M-3)/(8M)<1/2`. The logarithm bound then yields `g>=(x/2)exp[-2(M-1)x]`. The earlier interval-ordering proof applies verbatim because these are positive endpoints below one with a positive final gap.

Substituting the gap bound into two-sided Hoeffding gives the stated sufficient budget with coefficient 8. The simplification uses `x^-2<=M^2` and `x<=1/M+8M eta`, giving the coefficient `8e^4` and exponent `32M(M-1)eta`. All constants and inequality directions check out.

### Polynomial-budget equivalence

With fixed `delta` in `(0,1/2)` and a budget `C M^p` for all sufficiently large `M`, the clipped-map lower bound implies the displayed logarithmic bound on `eta_M`, hence `eta_M=O(log(M)/M^2)`. Conversely, every eventual bound `eta_M<=c log(M)/M^2` eventually falls within the upper construction's domain. Its budget is at most the stated constant times `M^(32c+2)`, up to the ceiling.

The author explicitly uses an eventual, fixed-confidence definition. This correctly excludes claims about every exceptional small `M`, an error sequence varying with `M`, optimal constants, or an optimal polynomial exponent. The earlier `M^-2` scale is therefore correctly separated from the universal polynomial-budget scale. In particular, `M^-2` must not be presented as the universal tolerance for all polynomial procedures.

## Resolved confidence-domain clarification

Before final freeze, the author changed Section 2 from “any target error delta>0” to “any target error 0<delta<1/2.” An exact comparison against the previously reviewed appendix confirmed that this phrase was the only change. The initial appendix digest was `39b1d8758a0d633ad37008e132d81312742e0a4a30c1d1f7945fbaed65bb4fb7`; the final binding above is `4242d8cbcc9fd576266e2ee01f902b45c93e6701b5c01d07a5a0c3909f97f0f4`. This makes the inherited confidence domain explicit and prevents applying the logarithmic budget outside that domain. No inequality, theorem, or algorithm changed. Both the author replay and the independent appendix controls were rerun successfully against the final bytes; all reported counts below refer to those fresh runs. The main source, main review, and main receipt remain unchanged.

## Controls independently executed

1. The supplied `efficiency_controls.py` was copied into `replayed_appendix_controls/` and run there. **33,840 exact-rational assertions passed**. The reproduced JSON is byte-identical to the author's final output. The reviewer did not reproduce or rely on any earlier failed run. The author reported correcting an initially strict domain comparison at `eta=0`; the inspected final non-strict comparison is correct.
2. The independently written `appendix_independent_controls.py` passed **22,073 assertions**. It checks clipped-map domains, monotonicity, endpoint preservation, the geometric error envelope, modified-region probability ordering, exponential kernel bounds, catalogue gap inequalities, and the sufficient-budget simplification.
3. Exact-rational controls use counts through 24 plus 32, 48, and 64 for clipped maps; catalogue sizes through 48 plus 64 and 127 for the upper construction; and additional interpolation/error levels. Separate 110-digit Decimal diagnostics check exponential and logarithmic inequalities.
4. A different history-adaptive protocol was exactly enumerated for counts 1, 3, 10, and 20 with depths 1, 3, and 4. Its clipped-map laws normalize, satisfy the exponential transcript-TV bound, and coincide at the critical allowance.

These are finite diagnostics supplementing the general proof, with no simulated observations. The independent program and detailed counts are bound in `APPENDIX_REVIEW_RECEIPT.json`. The main review artifacts and all author sources were checked for unchanged digests before this receipt was written. All reviewer writes stayed in this sibling review directory.

## Exclusions

No claim is made about sharp minimax constants or intermediate exponents, optimal confidence dependence, expected stopping budgets, varying-confidence asymptotics, count mixtures, enriched joint/multi-root observation kernels, empirical or physical calibration validity, causal identification, external priority, source admissibility, protected integration, or T20 closure. The result is conditional on the complete Bernoulli endpoint observation model and its allowed class of different static nuisance maps across worlds.
