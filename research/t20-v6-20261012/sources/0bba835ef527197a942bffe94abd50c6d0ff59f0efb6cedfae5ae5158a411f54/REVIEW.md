# Independent review: action length and polynomial moment tails

10 October 2026 UTC. Ordinary mathematical review of the additive T20 successor, separate from its author and the parent who proposed the ensemble argument. No protected integration, external peer review, formal-kernel verification, philosophical identification, or programme-closure authority is supplied.

Verdict: ACCEPTED within the stated forward-law and declared-action scope. No mathematical blocker remains. The unconditional conclusion starts at every positive time. Finite initial polynomial energy suffices to include time zero; arbitrary initial probabilities can have infinite initial action length.

Exact reviewed author identity:

- Directory: `full-law-gradient-action-tail-20261010`
- RESULT.md SHA-256: `07f993085f5e0066db587c0ef4fd9efd06c302179845007b886d3dcd8cafc352`
- Author snapshot digest: `eb5f5453dcc43b21b7d061ad6dbd2f4d3e8467440c771841156f2eea384649cc`
- Author manifest SHA-256: `6241879639beda1506d1ec3772aa1403f6f2963320695d146a4ee10bed1cfcdd`

## 1. Inherited inputs and scope

I read the frozen successor in full and checked the relevant ancestor proof and its review. The ancestor owns the characteristic representation of a supplied Borel probability, the selected critical level c*, the whole-law limit, and uniform positive-time bounds for each polynomial moment. The present review does not replace these hypotheses with a claim that every abstract formal hierarchy has such a representing law.

At positive times the polynomial hierarchy may be differentiated with p=F, so

    E' = -μ_t(|∇F|²) - μ_t(F²) + μ_t(F)² = -D.

The supporting basin argument matters: for almost every occupied initial label, F(Φ_t(x)) decreases to c(x)≥c*. Therefore F≥c* under the physical law at every finite time. Strictly positive finite-time reweighting leaves lower-level null basins null. The inequality u=F-c*≥0 is not deduced merely from a small positive mean h.

The limiting law is carried by the compact critical level {∇F=0,F=c*}. This may contain a continuum. Nothing in the argument requires finitely many critical points, isolated critical points, local minima, or a finite-atomic law.

## 2. Uniform analytic strip and ensemble inequality

The compact level L={F=c*} is the correct object to cover, including its noncritical points. The local analytic gradient inequality is available at each point; at regular points a positive local gradient bound also suffices. After restricting the energy gap to at most one, replacing the finitely many exponents by their maximum with 1/2 weakens each right-hand side. The finite minimum of the positive constants remains positive.

The thin-strip claim is justified by compactness, not assumed. If no strip lay in the open finite cover, a sequence of uncovered points with nonnegative energy gaps tending to zero would lie in the compact sublevel {F≤c*+1}. A convergent subsequence would land on L, contradicting that the cover is open and contains L. Consequently one κ>0 and θ∈[1/2,1) work everywhere in 0≤F-c*≤ε.

For h≤ε/2, write a=2θ∈[1,2). On the low part u≤ε the gradient square bounds κ²u^a. On the high part u≥ε,

    (F-E)²=(u-h)² ≥ u²/4 ≥ ε^(2-a)u^a/4.

The endpoint u=ε belongs to both bounds and causes no omission. Integrating the resulting pointwise inequality gives D≥C μ_t(u^a), with C=min{κ²,ε^(2-a)/4}. Convex Jensen has the required direction μ_t(u^a)≥μ_t(u)^a=h^a. These nonintegral powers are integrable because u≥0 and u^a≤1+u². Thus the claimed ensemble inequality is correct.

The reaction term is essential. In the double-well control, a mixture of its stationary minimum and stationary maximum has zero gradient contribution but strictly positive h and variance. Deleting variance would make the proposed bound false even for arbitrarily small h.

I independently opened the cited primary paper. Its Lemma 2.1 on printed page 533 supplies exactly the local real-analytic gradient inequality used here. The finite-cover and probability arguments above are deductions in this packet, rather than statements imported from an infinite-dimensional theorem. [Absil, Mahony and Andrews (2005)](https://sites.uclouvain.be/absil/Publi/Convergence_SIOPT/13-60526.pdf).

## 3. Energy rates, zero branch, and action length

For h>0 the dissipation identity and D≥Ch^(2θ) give

    -(h^(1-θ))' = (1-θ)h^(-θ)D
                 ≥ sqrt(C)(1-θ)sqrt(D).

Integrating first on a finite positive-h interval and then taking its terminal limit gives the stated tail bound. Since h decreases to zero, the desingularizing power also tends to zero. If h reaches zero, monotonicity and nonnegativity make it identically zero thereafter. Its positive-time derivative is then zero, so D=0 and both gradient and centered reaction vanish almost everywhere. The law is stationary at that critical level. The frozen report now explicitly avoids evaluating the negative comparison power at h(T)=0.

The exponential case θ=1/2 and algebraic case θ>1/2 have the correct coefficients and signs. The algebraic length exponent is (1-θ)/(2θ-1), rather than the energy exponent 1/(2θ-1). Exact monomial controls saturate the particle tail-length formula for several nonquadratic exponents.

The controlled object is the length of the displayed pair v=-∇F and α=E-F, with unit transport and reaction coefficients. Its squared action density is exactly D. On finite positive distinct atoms this equals Σ_j (w'_j)²/w_j + Σ_j w_j|X'_j|². For general laws it is a specified admissible action representation. No minimization over all admissible representations is used, and no smooth infinite-dimensional manifold, intrinsic metric equality, or all-rank metric completion is established.

For any 0<a<T, Cauchy–Schwarz and the dissipation identity give

    ∫_a^T sqrt(D) ≤ sqrt((T-a)(E(a)-E(T))).

This controls the finite positive-time portion, while the analytic bound controls the infinite tail. If μ(F)<∞, the global lower bound m=min F and F(Φ_t(x))≤F(x) give an integrable bound for the absolute energy integrand, after shifting by m. The weights are bounded on bounded time intervals and their normalizer tends to one. Hence E(t)→μ(F) as t↓0. Passing a↓0 proves the finite-energy initial-length assertion. No finite initial gradient-square or initial variance assumption is necessary. This is a sufficient condition; the report correctly does not assert necessity.

## 4. Polynomial observable bounds

The cometric is a positive semidefinite bilinear form because it is the L² inner product of (∇p,p-μ_t(p)) and (∇q,q-μ_t(q)). Therefore |B_t(p,F)|²≤B_t(p,p)D, with μ'_t(p)=-B_t(p,F). This is ordinary Hilbert-space Cauchy–Schwarz; it does not require inverting a moment matrix.

For fixed p and t0>0, the ancestor's terminal-energy envelope bounds μ_s(|∇p|²+p²) uniformly for all s≥t0. Both summands are nonnegative polynomials, and the denominator has the inherited positive lower bound after energy normalization. Consequently one finite M_p bounds B_s(p,p) throughout that interval. Integrating the derivative estimate to infinity and using the already proved polynomial moment limit yields exactly the report's inequality (4). Additive constants disappear from the exact cometric and derivative. No uniformity over all degrees or initial laws is claimed.

## 5. Heavy-tail countercontrol, independently checked

The energy density ρ(y)=1/[y(log y)²] on [e,∞) is normalized: its distribution function is 1-1/log y. Its energy mean is infinite. For example, y=e^z transforms the energy integral into ∫_1^∞ e^z/z² dz; the elementary exponential-series bound e^z≥z³/6 makes divergence explicit.

Pushing this probability by x=√(2y) produces the stated initial law. For F=x²/2, the exact flow has physical energy qY with q=e^(-2t). Accumulated killing is sY with s=(1-q)/2 and s'=q. The tilted law ν_s is therefore correct. At s>0 its moments are finite. Writing M(s)=E_sY and V(s)=Var_sY gives M'=-V and the full identity

    -E'(t)=2qM(s)+q²V(s).

In particular, the reaction contribution alone is q²V(s), with no missing factor of two or transport scaling.

For 0<s≤1/(2e²), the original low-event mass on [e,e²] is 1/2 and its tilt factor is at least exp(-1/2). Since the normalizer is at most one, ν_s(L)≥exp(-1/2)/2. On H=[1/s,2/s], the tilt is at least exp(-2) and

    ∫_H ρ(y)dy = log(2)/[log(1/s) log(2/s)]
                ≥ log(2)/log²(2/s).

The intervals are disjoint and separated by at least 1/(2s), including the extremal permitted s. In Var(Y)=E[(Y-Y')²]/2, the two ordered events H×L and L×H cancel the factor 1/2. A valid explicit constant is

    V(s) ≥ exp(-5/2)log(2)/[8s²log²(2/s)].

Thus q√V(s)dt=√V(s)ds and the initial length dominates a positive multiple of ∫_(0+) ds/[s log(2/s)], which diverges. The positive-time tail remains finite. There is no conflict with the ancestor's finite integral of E-c*: integrability of energy does not force initial action length to be finite when E(0)=∞.

This initial law does not have all polynomial moments. Any supplied all-moment initial law has finite polynomial energy, and therefore falls within the finite-length-from-zero conclusion. The different all-moment lognormal Fisher-boundary path also remains outside this counterexample's asserted scope. The example establishes infinite length of this chosen trajectory, not infinite distance between its endpoints after optimizing over other paths.

## 6. Executed evidence and preservation

Before copying, all 13 author payload hashes, the author manifest hash, and its snapshot digest were independently verified. The six original bindings and all 14 payload files in the earlier nonconvex limit packet were checked unchanged. The final frozen RESULT.md was read after the author supplied its identities.

The copied author checker was run with the six originals (31 checks) and portably without originals (25 checks). Both fresh reports were byte-identical to the corresponding frozen author reports. The independent checker passed 29 exact controls, including the exact high-event probability, event separation, three-point variance pair factor, full quadratic dissipation, an adversarial stationary two-level law, strict convex Jensen direction, polynomial cometric Cauchy–Schwarz, finite-atomic metric agreement, both comparison branches, and monomial tail equalities. These are symbolic identities and bounded controls, not enumeration of all coercive polynomials or formal-kernel verification of the universal proof.

The parent independently proposed and checked parts of the argument; that assistance was not counted as independent review evidence. I derived the inequalities and constants separately, checked the final written proof, and executed the separate controls. Two pre-freeze clarity suggestions were incorporated by the author: the explicit h(T)=0 comparison branch and reconciliation with all-moment initial hierarchies. No author or predecessor file was edited by this reviewer.

`REVIEW_RECEIPT.json` records the exact bindings and execution facts. `REVIEW_MANIFEST.json` binds the review packet. `check_review.py` supplies a fresh replay outside all frozen directories. T20 remains open; this acceptance is ordinary mathematical review only.
