# Skyline count separates the retained-interior hard pair, with a proved variance bound

8 October 2026 UTC. Prospective mathematical follow-on only. Historical floor remains UNVERIFIED. No empirical, Lean, physical-access, protected-integration, or closure claim is made. Frozen predecessors are unchanged.

## Result and observation contract

Use the two worlds in the retained-interior and full-face packets: P0 has n independent product-uniform points; P1 has m=n+1 independent points with CDF F_c(x,y)=1−(1−xy)^c, c=n/m. A point is a route's two thresholds. One ideal retained-interior observation is the whole endpoint function, with the same threshold vector throughout. Almost surely it determines precisely the finite Pareto-minimal antichain. Its cardinality K is observable in this ideal channel. Dominated points and hence total route count are not generally determined. No finite-probe or physical precision guarantee is inferred.

Write H_j=Σ_{i=1}^j 1/i and H_j^(2)=Σ_{i=1}^j 1/i². Then

    E0 K = H_n,
    E1 K = H_n + δ_n,
    δ_n = (H_n−1)/(n²−1),                         n>1,
    δ_1 = (ζ(2)−1)/2.                              (1)

In particular δ_n>0, and δ_n is asymptotic to log(n)/n². This ordinary count observable differs even away from an exclusive support event.

The Joe indicators need not be independent. Nevertheless the following variance bound is proved below:

    Var0 K = V_n := H_n−H_n^(2),
    Var1 K ≤ W_n := V_m+H_m²−(H_n+δ_n)²
                  ≤ V_m+2H_n/m+1/m².              (2)

Thus both variances are O(log n). Equations (1) and (2), not the mean gap alone, give a valid count-based testing upper bound of O(n^4/log n) independent ideal retained vectors for any fixed error tolerance. This is not an optimality claim and not an upper bound on the number of endpoint probes.

## 1. Exact expectation

For N iid points from an absolutely continuous joint CDF F with density f, a specified point at (x,y) is minimal iff none of the other N−1 points lies in its lower rectangle. Boundaries have probability zero. Linearity and conditioning give

    E K = N ∫_[0,1]² f(x,y)[1−F(x,y)]^(N−1) dx dy. (3)

For any nonnegative integrand g(xy), the substitution z=xy followed by Tonelli gives

    ∫_[0,1]² g(xy) dx dy = ∫_0^1 (−log z)g(z) dz. (4)

For P0, f=1 and F=xy, so the integral is n∫(−log z)(1−z)^(n−1)dz=H_n. To verify the last identity without an unevaluated special function, set t=1−z, expand −log(1−t)=Σ_{k≥1}t^k/k, and telescope nΣ_{k≥1}1/[k(n+k)]=H_n. Nonnegative terms justify interchange.

For P1, f_c=c(1−xy)^(c−2)(1−cxy). Since mc=n, (3) becomes

    E1 K = n∫_0^1 (−log z)(1−z)^(n−2)(1−cz)dz. (5)

For n>1 the two constituent integrals are

    A = ∫(−log z)(1−z)^(n−2)dz = H_(n−1)/(n−1),
    C = ∫z(−log z)(1−z)^(n−2)dz
      = A−H_n/n = (H_n−1)/[n(n−1)].

Consequently E1 K=n(A−cC). Substitution H_(n−1)=H_n−1/n gives E1 K−H_n=(1−c)(H_n−1)/(n−1), proving (1).

At n=1, the integrand in (5) is (−log z)(1−z/2)/(1−z). Since (1−z/2)/(1−z)=[1+1/(1−z)]/2, expansion of 1/(1−z) and ∫z^k(−log z)dz=1/(k+1)² gives E1 K=(1+ζ(2))/2. This also proves finiteness at the exceptional exponent n−2=−1. There is no substitution of n=1 into the n>1 quotient.

## 2. Stochastic order and the record coupling

On the open square,

    ∂² log f_c(x,y)/∂x∂y
       = (2−c)/(1−xy)² − c/(1−cxy)² ≥ 0.          (6)

For 0<c≤1, 1−xy≤1−cxy, so the expression is at least 2(1−c)/(1−cxy)². This proves the monotone-likelihood-ratio property in y as x increases. Dividing f_c(x,y) by its x-marginal density does not affect that property. For x'<x, the conditional-density ratio h_x(y)/h_x'(y) is nondecreasing. Its total integral under h_x' equals one, so the ratio crosses one at most once, from below to above; integrating on initial intervals proves that the conditional CDF G_x(y) is no larger than G_x'(y). Therefore conditional Y is stochastically increasing with x. This argument concerns x strictly inside (0,1), which suffices almost surely.

Condition on the ordered X values X_(1)<…<X_(m). Their concomitant Y_i are independent, with respective conditional CDFs G_i=G_{X_(i)}. This follows directly by conditioning independent labeled pairs on their X values and applying the sorting permutation. Let U_1,…,U_m be independent uniforms, independent of those ordered X values, and construct Y_i=Q_i(U_i) using generalized inverse CDFs. Stochastic order gives Q_j(u)≤Q_i(u) whenever j<i.

If some j<i has U_j≤U_i, then

    Y_j=Q_j(U_j)≤Q_j(U_i)≤Q_i(U_i)=Y_i.

Hence a strict lower record at i among the Y's implies a strict lower record at i among the U's. Equalities have probability zero. With I_i and J_i the respective record indicators, this gives simultaneously

    I_i≤J_i for every i,  K=Σ I_i ≤ R_m:=Σ J_i.    (7)

Sorting by increasing X turns Pareto minima exactly into lower Y records. Thus (7) is a coupling of the actual Joe skyline count with the ordinary independent-uniform record count, not an assertion that Joe record indicators are independent.

For completeness, J_i are independent Bernoulli(1/i): the sequential relative ranks of a continuous iid sequence are independent uniforms on {1,…,i}. Indeed each sequence of such insertion ranks corresponds bijectively to a permutation, and all m! permutations are equally likely. A lower record is relative rank 1. Therefore E R_m=H_m and Var R_m=V_m.

## 3. Variance without a false independence assumption

The pointwise inequality K≤R_m yields E1 K²≤E R_m²=V_m+H_m². Subtracting the exact squared mean gives

    Var1 K ≤ V_m+H_m²−(H_n+δ_n)² = W_n
           ≤ V_m+H_m²−H_n²
           = V_m+2H_n/m+1/m².                    (8)

This proves (2), and in fact W_n=V_m+O(log(n)/n). A second-moment bound alone is O((log n)²); subtracting the known squared mean is essential to obtain O(log n) variance. This does not assert covariance signs or independence of the Joe record indicators.

As a separate consistency check, D=R_m−K satisfies 0≤D≤m−1 and E D=1/m−δ_n≥0. For n>1 the last inequality follows directly from H_n−1≤n−1, and for n=1 from ζ(2)<2. Thus the exact mean obeys the stochastic domination proved above.

Under P0 the ordered Y's are iid uniforms independent of the X order, so the same insertion-rank argument gives the exact baseline variance in (2). At n=1, K under P1 is 1 plus a Bernoulli(δ_1), so its exact variance is δ_1(1−δ_1); (2) remains a valid, looser bound.

## 4. A justified sample comparison, and its limits

Take s independent fresh retained vectors, observing the full ideal endpoint function separately for each and hence K_1,…,K_s. Decide P1 iff their average is at least H_n+δ_n/2. Chebyshev gives

    P0(error) ≤ 4 V_n/(s δ_n²),
    P1(error) ≤ 4 W_n/(s δ_n²).                    (9)

Thus for 0<α<1 it suffices to take

    s ≥ ceil(4 max(V_n,W_n)/(α δ_n²)).             (10)

Since V_n and W_n are O(log n), while δ_n∼log n/n², (10) is O_α(n^4/log n). If confidence dependence matters, independent groups each with the constant-error bound in (10), followed by majority vote, give logarithmic dependence on 1/α by the elementary binomial tail bound. No sharper concentration claim for Joe records is needed here.

The strongest bound comparator is the existing full-face-threshold-kl-rate/RESULT.md, sections 1 and 6, bound in SOURCE_AUDIT.md. For this same hard pair it proves D_n=KL(P1_minima||P0_minima)∼1/(2n^4), hence

    E1[N] ≥ (2+o(1)) n^4 kl(1−α,α),

for fixed 0<α<1/2 and unconditional terminal correctness, with N counting every independent retained vector started. The comparator covers exact two-coordinate-minimum readout and arbitrarily long adaptive face-only words, including fair charging of a vector from its first observation even if its word never finishes. It is stronger than the older two-face-probe restriction.

The present fixed-budget ideal skyline test uses precisely the same hard pair, independent fresh vectors, fixed error α<1/2, and counts all s vectors it starts. It terminates after s ideal observations with the unconditional error bounds (9). Thus O_α(n^4/log n) is a genuine asymptotic improvement in independent-vector cost over that Ω_α(n^4) face-only lower bound, not just over the older two-probe interface. This consumes the existing comparator theorem; it does not establish that theorem anew. There is no contradiction: retained-interior skyline readout contains information beyond the two coordinate minima.

Neither ideal channel's exact real-valued observation is asserted to be a finite physical operation. This comparison does not show a finite-cost endpoint instrument achieves the skyline scale, nor that skyline count is optimal, nor that n^4/log n is a lower bound. Exact readout, retained state, noiseless endpoint semantics, and independent resets remain explicit mathematical assumptions. The face-only started-vector and terminal-correctness requirements are preserved rather than replaced with conditional-on-termination accuracy or uncharged repeated access.

The rare-event certificate and any factorial skyline-support bound concern other statistics or events. They are not needed to prove (1)–(10). A positive mean gap alone would not justify the claimed sample scale; the coupling and variance argument are indispensable. The count statistic still cannot identify how many dominated routes were present in any one vector.

## 5. Verification, attribution, and boundaries

The parent supplied the expectation candidate, the TP2 direction to investigate, and the warning not to infer rates from a mean gap or assume independent record indicators. This packet independently verifies the exact expectation, derives the pointwise quantile-record coupling, and uses the exact mean to prove the variance and testing bounds. The parent independently suggested the same coupling and supplied the simpler, sharper second-moment subtraction used in (8); this is shared derivation rather than duplicate independent credit. The sibling retained-skyline-likelihood worker was notified of this result; its likelihood and support calculations are separate and are not credited again here.

CONTROL_RESULTS.json and controls.py contain deterministic arithmetic and quadrature checks, including normalization/expectation checks, exact rational identities at finitely many n, n=1, an ordered-quantile record coupling check, and deliberately wrong candidate comparisons. They are not empirical simulations or formal proofs. The written arguments above carry the general claims. No external bibliographic novelty, kernel assurance, physical oracle access, actual route architecture, or T20 closure is asserted. The inherited historical floor remains UNVERIFIED.
