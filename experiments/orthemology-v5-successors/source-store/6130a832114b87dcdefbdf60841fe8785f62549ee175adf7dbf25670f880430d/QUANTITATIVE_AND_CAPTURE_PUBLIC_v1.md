# Quantitative independence, bounded capture, and positive controls

4 October 2026 UTC. Ordinary-mathematics addendum to the independent review of finitely additive concentration. These are standard consequences and controls, not new probability-theory priority claims. No code or implementation is supplied.

## 1. The weakest useful bounded-capture premise

The concentration argument makes μ(X_0∈I)=0 for every fixed bounded interval I under exact fresh Gaussian innovation blocks extending arbitrarily far into the past. Consequently, a single independently warranted bounded-capture premise

μ(X_0∈I)=p>0

already contradicts that package. Full terminal tightness is a convenient sufficient condition, not the logically weakest assumption. Tightness is useful for the maximal-distance theorem below because it supplies captures with probabilities arbitrarily close to one.

A finite-valued real state does not by itself give positive probability to any preselected bounded interval under finite additivity. The accepted uniform-anchor construction shows precisely this. Nor does observing one realised value establish a positive probability claim without an appropriate probability model. This is a specification-level test of a capture guarantee, not an automatically valid empirical estimator or a sampling claim.

## 2. Total variation lower bound

Fix a common terminal law for X_0. For each positive integer n, let P_n be the actual joint law of (Y_n,Z_n), where the block recurrence gives X_0=Y_n+Z_n and the marginal of Z_n is the ordinary N(0,n) law. Let Q_n be a probability law on the same measurable pair-event domain satisfying the independent concentration theorem. A natural benchmark has the same two marginals and rectangle independence. Define

d_TV(P_n,Q_n)=sup_E |P_n(E)−Q_n(E)|.

This convention has maximum value 1 for probability laws, including finitely additive laws. It is half the alternative total-variation norm convention sometimes used for signed measures.

For a bounded interval I and E_I={(y,z):y+z∈I}, measurability and the recurrence give P_n(E_I)=p_I:=P(X_0∈I). The proved concentration bound gives Q_n(E_I)≤q_n(length(I))≤length(I)/sqrt(2πn). Therefore

d_TV(P_n,Q_n) ≥ p_I−q_n(length(I))
                 ≥ p_I−length(I)/sqrt(2πn).                 (TV)

If the right-hand side is negative, the independent trivial bound d_TV≥0 applies. This is a direct separating-event bound; it does not require a coupling characterization of total variation, Radon–Nikodym derivatives, or countable additivity of P_n.

For one fixed interval of positive mass p_I, (TV) gives liminf_n d_TV(P_n,Q_n)≥p_I. If the common terminal-position law is tight, then for each ε>0 choose one bounded interval I_ε with p_(I_ε)≥1−ε. Hold that interval fixed while n→∞. Its length is finite, so

liminf_n d_TV(P_n,Q_n)≥1−ε.

Letting ε decrease to zero and using d_TV≤1 proves d_TV(P_n,Q_n)→1. No rate uniform over all terminal laws follows from tightness alone. A supplied capture interval and mass give the explicit finite-n lower bound in (TV).

The theorem compares the actual state–block law with independence benchmarks over increasingly remote horizons. It does not say the increments cease to be iid among themselves. Mutual iid noise and arbitrarily strong state–block dependence can coexist, as the anchored backward-sum control demonstrates.

### Benchmark existence and nonuniqueness

If the state marginal ν_n is countably additive, the usual product ν_n⊗γ_n is the canonical countably additive benchmark.

If ν_n is a real-valued finitely additive probability on the full Borel σ-algebra of R, at least one suitable benchmark on B(R²) can be defined by

Q_n(E)=∫_fa [γ_n({z:(y,z)∈E})] dν_n(y).

For Borel E the bracketed section-probability function is a bounded Borel function, by the ordinary measurability theorem for integration against γ_n. The outer finitely additive integral is defined by uniformly approximating bounded Borel functions by Borel simple functions. Positivity and normalization make this a well-defined bounded positive linear functional. Disjoint-event section probabilities add pointwise, proving finite additivity of Q_n. For a rectangle A×B the integral is ν_n(A)γ_n(B), so both marginals and rectangle independence are exact.

This construction specifies an order of integration. It does not assert that every finitely additive product extension is identical, nor that all Borel values follow from rectangles by a countably additive uniqueness theorem. For an event algebra smaller than the full Borel domain, do not silently use this existence construction; either verify the needed domain and integration hypotheses or keep a lawful comparison Q_n as an explicit assumption.

## 3. Adaptive finite-range search does not restore a fixed-budget guarantee

Consider the pointwise procedure that successively checks |X_0|≤1, |X_0|≤2, and so on, stopping at the first successful bound. Every real-valued sample eventually passes. Under the finitely additive diffuse-position construction, however, each event of success by a fixed integer budget M is {|X_0|≤M} and has probability zero.

Thus pointwise finite termination and positive success probability at some fixed finite budget come apart for this law. The termination event is the entire sample space and has probability one, whereas each fixed-budget success event has probability zero. There is no contradiction: continuity from below for this increasing sequence is exactly what finite additivity does not supply.

This is an analytic observation about the given event structure. It is not a newly implemented search algorithm, proof of a finite expected runtime, license to exchange a random stopping stage with a countable union, or evidence that a final finitely additive sampler exists. Prior P02/Tenth distinctions between existence, effective names, finite witnesses, and exact queries remain the owners of those general cautions; the present use is specific to this path-law control.

## 4. Two standard positive controls

### Contractive Gaussian autoregression

Let 0<|a|<1 and let ξ_t be ordinary countably additive iid N(0,1) noise for t∈Z. Define

X_t=Σ_(j≥0) a^j ξ_(t−1−j).

The sum of variances is Σ_j a^(2j)=1/(1−a²)<∞. The independent centered series converges in L² and almost surely for each t. Since there are only countably many t, one can choose a common probability-one event carrying every such series and recurrence. This countable-intersection step is justified here by the countably additive law.

The process is stationary Gaussian with variance 1/(1−a²) and satisfies X_(t+1)=aX_t+ξ_t. Every X_s with s≤t is measurable with respect to innovations indexed below t, so full past information is independent of innovations indexed at least t.

The n-step relation is

X_0=a^n X_−n+Σ_(j=0)^(n−1) a^j ξ_(−1−j).

The innovation variance is (1−a^(2n))/(1−a²), which stays bounded instead of growing as n. Therefore the accumulating-variance premise of the random-walk obstruction fails. There are infinitely many nonzero coefficients in the state representation; whether these are actual productive contributions in a metaphysical application is an additional interpretation, not a consequence of the series.

### Nonstationary entrance law for deterministic translation

Let X_t=t for all integer t and let ξ_t=1. The point mass on this whole path is a countably additive probability satisfying X_(t+1)=X_t+1 at every time. Its marginals are δ_t and form a nonstationary bi-infinite entrance law for the transition x↦x+1.

There is no countably additive translation-invariant probability on Z: invariance would make all singleton masses equal; positive common mass violates finite normalization, and zero common mass violates countable normalization. This absence of a stationary probability does not exclude the displayed nonstationary entrance law.

The Gaussian impossibility above is stronger in its own stated class because it did not assume stationarity. The deterministic example fails the spreading innovation-law premise, and the autoregression fails unbounded variance accumulation. Neither is a counterexample to the concentration theorem.

## 5. Ownership and disposition

P02 `proofs/U05_MEASURE_CORE.md`, M2-05, already fixes the same TV normalization and proves its support-defect control. M2-01, M2-02, and M2-06 already police countable operations, event repertoires, and the gap from measure existence to effective sampling. Tenth `research/finite-limit-warrants/PRIOR_OWNERSHIP.md` and the accompanying finite-warrant study already distinguish finite usable evidence from exact infinite-state queries.

The quantitative state–block separation is a standard anti-concentration application to this newly assessed bridge. The two-sided AR(1) process and deterministic entrance law are standard controls, not newly discovered examples. Targeted prior-owner inspection found no exact programme owner of this Gaussian TV-to-one application, but no exhaustive mathematical priority claim is made.

**Independent mathematical disposition:** accept the bounded-capture refinement, (TV), its tight-terminal TV-to-one consequence, the stated Borel benchmark construction, and the two positive controls. Retain all declared probability, measurability, and interpretation limits. No source synopsis or primary quotation is added by this addendum.
