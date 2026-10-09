# Independent review: arbitrary adaptive pure-count sample bound

8 October 2026 UTC. Scope: the mathematical appendix `../calibration-design-frontier/ARBITRARY_RATE_COUNT_BOUND.md`, its declared model, and its comparison with the local noise-aware predecessor. No author files were edited or frozen. This is an independent mathematical review, not physical validation, a kernel formalization, field-wide priority research, protected integration, owner acceptance, or T20 closure.

## Verdict

**PASS, with both requested statement clarifications applied and re-read.** The appendix proves a fixed-budget arbitrary-rate adaptive lower bound and a matching-order fixed-rate upper bound for one fixed unknown pure count. The inequalities and displayed numerical constants are correct. The calibration ambiguity is valid for the stated single command and unknown calibration model; it is not an arbitrary-multirate impossibility result.

1. The author now writes `0 < delta < 1/2` in the theorem. The displayed logarithm is undefined at delta = 0; that endpoint can separately be described as impossible for any finite budget. Negative error parameters are not meaningful.
2. The calibration corollary now explicitly retains fresh conditional Bernoulli trials at a fixed unknown actual rate in the stated interval. This is the interpretation under which the argument was reviewed. A conditionally bounded drifting rate also admits a suitable martingale concentration proof, but merely having correct unconditional endpoint marginals does not supply concentration. The fixed-world impossibility construction already satisfies the fixed-rate interpretation.

These were clarifications of the confidence domain and sampling model, not failures of the mathematical core. Both were independently verified in the revised appendix, SHA-256 e68242d3052342b2c2cf029b3e9d65d3402e7005d6179f8a335ec1e5ad52daad. The initial and final reviewed hashes are tracked in `REVIEW_RECEIPT.json`. There are no unresolved mathematical findings.

## 1. Scalar inequality: every step checked

Set n = K − 1 ≥ 1 and t = 1 − x. For 0 < t < 1, the two hard alternatives have no-effect parameters u = t^n and v = t^(n+1), both strictly interior. Applying log z ≤ z − 1 separately to the two Bernoulli terms gives

D(Ber(u) || Ber(v)) ≤ (u − v)^2 / [v(1 − v)].

Cancellation is valid in the interior and yields exactly

t^(n−1)(1−t) / (1 + t + ⋯ + t^n).

For n = 1 this is (1−t)/(1+t) ≤ 1 = 2/[n(n+1)]. For n ≥ 2, AM–GM applied to the n+1 positive terms gives their sum at least (n+1)t^(n/2). Division therefore leaves t^((n−2)/2)(1−t)/(n+1). At n = 2 its numerator is 1−t ≤ 1 = 2/n. For n > 2, differentiating the numerator gives its unique interior maximum at t = (n−2)/n, of value (2/n)((n−2)/n)^((n−2)/2) ≤ 2/n. The claimed bound 2/[n(n+1)] follows.

The boundary rates must be treated directly, rather than substituted into the divided expression: x = 0 gives a deterministically absent effect under both positive counts; x = 1 gives a deterministically present effect under both. Both relative entropies are zero. In particular the n = 1 rational upper envelope tends to 1 as t approaches zero, even though the actual boundary divergence is zero. This harmless looseness does not invalidate the uniform inequality.

## 2. Adaptive experiment and testing reduction

The model needs a single parameter-independent measurable policy, whose next action is based on earlier chosen rates, earlier endpoints, and private randomness independent of the unknown count. No additional hypothesis-dependent side information is available. Conditional on that history and the chosen rate, the next endpoint has exactly the declared Bernoulli law. This is enough; endpoints need not be independent unconditionally after adaptive action selection.

The proof can include the independent random seed in the transcript. Alternatively, use the equivalent common behavioral action-selection kernels. Their relative-entropy contributions vanish. The response contribution at every step is at most 2/[n(n+1)], irrespective of the chosen action. Integrating over actions in the continuum [0,1] changes none of this. The chain rule gives

D(P_n || P_(n+1)) ≤ 2N/[n(n+1)].

A final randomized decision can also be included as a common zero-divergence channel. Finite-horizon laws for these two positive counts are mutually absolutely continuous: interior actions have the same two-point support, and boundary actions have the same deterministic support. The KL calculation therefore has no hidden singular boundary case.

For E = {decision equals n}, uniform multiclass correctness gives P_n(E) ≥ 1−delta and P_(n+1)(E) ≤ delta. Data processing to the indicator of E yields the binary divergence lower bound. For p > q,

∂_p kl(p,q) = log[p(1−q)/(q(1−p))] > 0,
∂_q kl(p,q) = (q−p)/[q(1−q)] < 0.

Consequently the minimum over p ≥ 1−delta and q ≤ delta is kl(1−delta,delta), equal to (1−2delta)log((1−delta)/delta). Rearranging gives the stated lower bound. For delta ≤ 1/4, use 1−2delta ≥ 1/2 and 1−delta ≥ 1/2 to obtain the simpler displayed bound.

The fixed N premise is honored throughout. The appendix does not rely on optional stopping or claim an expected-sample guarantee. The order statement is valid uniformly for any fixed delta_max < 1/2, with constants allowed to depend on delta_max. It is not uniform as delta approaches 1/2.

At delta = 0, mutual absolute continuity prevents a finite transcript from identifying both positive hard alternatives perfectly. Thus the intuitive infinite-budget limit is correct, and the revised finite formula now excludes zero explicitly.

## 3. Upper bound, constants, and K = 2

At x = 1/K, consecutive catalogue means differ by t^j/K. Since 0 < t < 1, the minimum is at j = K−1. Writing m = K−1,

(1 + 1/m)^m ≤ Σ_(r=0)^m 1/r! < 3.

For completeness, the last strict bound follows from r! ≥ 2^(r−1) for r ≥ 2, with strict inequality for r ≥ 3, so Σ_(r=2)^∞ 1/r! < 1. Therefore the minimum gap is strictly greater than 1/(3K).

If the empirical no-effect mean is within 1/(6K) of the correct mean, nearest-mean decoding is correct. Hoeffding gives a failure probability at most 2exp(−N/(18K²)), because 2(1/(6K))² = 1/(18K²). Taking the indicated ceiling controls the error by delta. The guarantee is separately uniform for each true count; it does not require a union bound over K+1 potential truths. H_0 has no-effect probability 1, so it is included without a statistical or tie-breaking defect.

For K = 2 the hard pair is counts 1 and 2; the per-trial bound is 1, nominal t is 1/2, and the actual minimum mean gap is 1/4 > 1/6. Every displayed lower, upper, and calibration constant remains valid. K = 1 is rightly excluded from this theorem: one exact endpoint at x = 1 separates its only two counts perfectly.

## 4. Calibration allowance and fixed-command collision

For a fixed actual rate x_actual with |x_actual − 1/K| ≤ eta and both rates in [0,1], the telescoping product identity gives

|(1−x_actual)^j − (1−1/K)^j| ≤ j eta ≤ K eta.

At eta ≤ 1/(12K²), this bias is at most 1/(12K). Sampling error below 1/(12K) leaves total deviation below 1/(6K), hence correct nominal nearest-mean decoding. The coefficient 72 follows from 2(1/(12K))² = 1/(72K²).

The sufficient statement can even allow a fixed unknown joint nuisance chosen before the experiment and then condition on it, provided the fresh-trial law holds conditionally and its rate remains within the interval. It does not follow from marginal calibration promises under arbitrary cross-trial dependence. A simple warning control is Y_1 = ⋯ = Y_N = Z with Z Bernoulli(q): all marginals are right, but the empirical mean does not concentrate.

For the obstruction, t ∈ [1/2,1), exponent (K−1)/K ∈ (0,1), and x' = 1−t^((K−1)/K) lies strictly between zero and 1/K. Thus both actual rates are admissible. Their no-effect means are exactly identical, so their full independent repeated-endpoint laws coincide for every N. A decision rule therefore has worst-case error at least 1/2 across the two worlds. The actual rate must be unknown to the decoder; if it were supplied as observed side information, the two worlds would no longer be observationally identical.

Let L = −log t. Then d_K = t(exp(L/K)−1). The lower bound uses exp(v)−1 ≥ v, L ≥ 1/K and t ≥ 1/2, giving d_K ≥ 1/(2K²). The upper bound uses exp(v)−1 ≤ v exp(v), t exp(L/K) = t^((K−1)/K) ≤ 1, and L ≤ 1/(K−1), giving d_K ≤ 1/[K(K−1)] ≤ 2/K². At K = 2, d_K = sqrt(1/2)−1/2, safely inside the stated interval.

The two comparisons establish the order K^−2 of a sufficient allowance and an obstruction for this tuned command, with a constant-factor gap. They do not establish a sharp allowable eta. They also do not extend the obstruction to every calibration-error model, all panels, or adaptive multi-rate procedures; the appendix explicitly preserves this distinction.

## 5. What is new relative to the named predecessor

The predecessor `noise-aware-calibration/THEOREMS.md`, section “Matching restricted-family lower bound,” and the independent proof `noise-aware-review/RESTRICTED_MASK_LOWER_BOUND.md` explicitly restricted their lower bound to nonzero mask rate p = 1/(2K), fixed r and fixed confidence. That proof permitted adaptive mask selection but expressly did not cover arbitrary nonzero rates or general confidence dependence.

At r = 1, its hard pair is the same adjacent positive-count pair and its lower bound is order K². Its upper bound already establishes order K² log(1/delta) for that fixed-rate instrument. The present appendix's genuine local extension is the uniform per-observation information inequality and hence a lower bound against arbitrary adaptive exact-rate selection, together with logarithmic confidence dependence. The nearest-mean construction is a particularly direct pure-count upper bound, not a previously absent K² upper exponent. The calibration collision supplies a separate fixed-command necessity-scale statement.

This comparison establishes novelty relative to these inspected local artifacts only. No general literature priority claim has been assessed or is warranted by this review.

## 6. Independent controls and reproducibility

Run `python check_adaptive_count.py` from this directory. The script is independent of author implementation code and writes `results/INDEPENDENT_CONTROLS.json`. Recorded results:

- 26,035 exact rational uniform-envelope and squared AM–GM checks, including n = 1, 2, 4096 and rates extremely close to both boundaries.
- 30 exact rational chi-square/algebra identity checks with independent 100-digit KL evaluation.
- 1,110 high-precision actual-KL attacks over multiple scales, through n = 1,000,000.
- 251 exact fixed-rate minimum-gap checks, plus exact product-bias and decoder-margin controls at K ≤ 50.
- 252 high-precision calibration identity and d_K-bound checks, through K = 10^12.
- 48 exact-probability enumerations of full randomized adaptive transcripts. Policies include endpoint-dependent choices, independent hidden seeds made explicit in the transcript, and both boundary rates. Direct transcript divergence agrees with the independently accumulated chain-rule value and obeys the uniform bound.
- The confidence simplification and both Hoeffding exponent constants pass.

All controls pass. Finite exact checks and numerical attacks are implementation/arithmetic evidence, not proof of an all-K theorem. The general conclusion rests on the symbolic argument reviewed above. No samples were collected and no real calibration was tested.
