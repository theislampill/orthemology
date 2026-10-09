# Probability prior art with an applicable fixed-count area-tail corollary

8 October 2026 UTC. Scratch-only, prospective mathematics. Historical floor remains UNVERIFIED. No external reproduction, protected integration, physical-access, empirical, kernel-verification, or closure claim is made.

## 1. Consequential finding

There is directly applicable probability literature. Last and Molchanov explicitly include Pareto minima among their Poisson hulls. Their theory gives the exact compensation K−λU for a Poisson uniform sample, its variance, and a joint exponential identity. This is more relevant here than an unrelated convex-hull CLT. See the primary texts and exact read boundaries in SOURCE_AUDIT.md.

A self-contained specialization and conditioning argument below gives, for BOTH fixed-count hard-pair worlds,

    E_j exp(nU/4) ≤ sqrt((m+1)/p_m),       j=0,1,
    m=n+1,    p_m=exp(−m)m^m/m!.                              (1)

Consequently, with B_m=2 log((m+1)/p_m),

    P_j(nU ≥ B_m+4x) ≤ exp(−x),       x≥0.                     (2)

Stirling gives B_m=3 log m+O(1). In particular every fixed raw moment satisfies

    E_j[(nU)^r] ≤ Σ_(q=0)^r binom(r,q) B_m^(r−q)4^q q!
                 =O_r((log m)^r),       r≥1.                  (3)

This strengthens the previously available first-moment/Markov localization. It does not establish a likelihood information rate, centered fourth-moment scale, or a CLT for the fixed-count compensation.

The exact sharper record identity E[2^(R_m)]=m+1 is used only to simplify (1); replacing it by exp(H_m) also works.

## 2. Primary-source theorem actually matched

Last–Molchanov, [Poisson hulls](https://arxiv.org/abs/2212.02150), published in Bernoulli 31(1), 359–387 (2025), explicitly treats Pareto minima in Example 2.15. Its Theorem 3.2 gives conditional Poisson points inside the hull; Lemma 4.4 identifies the estimator error as a compensated boundary sum; Theorem 5.1 gives its variance. Section 7 supplies quantitative normal-approximation bounds, whose terms still require evaluation for each application.

Last–Molchanov, [Efron type identities for stopping sets and Poisson hulls](https://arxiv.org/abs/2608.06038), August 2026 preprint, again includes Pareto minima in Example 8.4. Theorem 4.7 is the joint exponential identity used below. Corollary 4.8 gives mixed falling-factorial identities. The paper attributes an antecedent of the exponential identity to Zuyev (1999); no claim of first discovery is made here. This August preprint is public by the current research date, and is not represented as a peer-reviewed publication.

### Actual geometry and hypotheses

Our application uses X=[0,1]^2 and all Borel sets as its localizing ring, so all counting measures under consideration are finite. Let ∂η retain all coordinatewise-minimal points, with multiplicities. The hull [η] is the upper dominated region D with those minimal support points removed. Its complement Z is the undominated staircase together with the minimal points. Thus η(Z)=K, and for any absolutely continuous route law μ,

    μ(Z)=μ(E).

For μ uniform this equals U; for the Joe law it equals μ_c(E), generally NOT U.

This is an exact minimum-order match, requiring no reflection or exponential coordinate change. Boundary and vertex conventions are immaterial to area/probability mass because μ is absolutely continuous, but not to the count η(Z).

Here is a direct check of the required stopping-set property. Retaining η restricted to Z keeps precisely its minima. Replace all other points by arbitrary finitely many points in Z's complement. Each replacement is dominated by a retained minimum, so cannot be minimal or remove a retained minimum. The skyline and Z stay the same. This also works for the empty configuration, where Z=X. The construction is graph measurable since finite-point coordinate comparisons are Borel. The generator has thinning, retains multiplicities, is idempotent after removing any subset of dominated points, and is consistent when equal skylines receive the same added configuration. These verify the source hypotheses in this finite model; no unbounded/infinite-hull extension is used.

For a Poisson process of intensity λμ, λ>0, the total mass is finite. It is almost surely finite, and the source's square-integrability and exponential integrability requirements for constant test functions hold. An unbounded Joe density near the square's corner causes no failure: μ_c is a probability measure and hence λμ_c is finite. We do not use bounded-density hypotheses from unrelated geometric CLTs.

## 3. Exact Poisson identities and the fixed-count distinction

Write V=μ(E) for the complement mass, and keep μ fixed while varying λ. Theorem 4.7 specializes, for every t≥0, to

    E_(PPP(λμ)) exp[−tK+(1−exp(−t))λV]=1.                   (4)

Theorem 5.1 with the constant function gives

    E(K−λV)=0,    E[(K−λV)^2]=E K=λ E V.                    (5)

For uniform μ, λEV=λ∫_[0,1]^2 exp(−λxy)dxdy
=∫_0^λ (1−exp(−u))/u du ∼log λ. Thus (5) is an independently developed, exact Poisson counterpart of the fixed-count baseline's logarithmic compensated second moment. It is not the fixed-count theorem itself.

As another usable identity, Corollary 4.8 gives

    Σ_(i=0)^r (−1)^i binom(r,i) E[(K)_i (λV)^(r−i)]=0,
    r≥1,                                                        (6)

where (K)_i is the falling factorial. These are relationships among mixed moments, not by themselves numerical asymptotics of the fourth centered moment.

### Independent elementary check of (4)

The retained-skyline likelihood packet already proves the fixed-N ordered skyline density (N)_k product f(z_i) D^(N−k), D=1−V. Mix it with N~Poisson(λ). On stratum k≥1 the sum over N≥k gives

    q_(λ,k)(s)=λ^k product f(z_i) exp(−λV(s)).                 (7)

The empty skyline has mass exp(−λ), with K=0,V=1. Consequently the density ratio of PPP skylines at intensities λ exp(−t) and λ is exactly the integrand in (4), including the empty stratum. Both laws have the same support and normalize to one. This independently checks the specialized identity without assuming a nonexistent conditional independence between K and V.

### Why conditioning does not preserve the equalities

A Poisson law is a mixture over sample sizes. Its expectation identity does not generally remain an equality after conditioning on one size. For example, under n uniform points,

    E[K−(n+1)U]=H_n−H_(n+1)=−1/(n+1),

whereas the Poisson expression (5) has mean zero. We will condition a nonnegative quantity and explicitly pay the conditioning probability. No asymptotic variance, fourth-moment constant, or normal approximation is silently transferred.

## 4. Fixed-count hard-pair proof of (1)–(3)

The hard pair and facts consumed from accepted predecessor calculations are:

- P0: N=n iid uniform points.
- P1: N=m=n+1 iid points with F_c(x,y)=1−(1−xy)^c, c=n/m.
- f_c≥c on the open square, proved in retained-skyline-likelihood/RESULT.md.
- Under P1, K is coupled below R_m, the lower-record count of m iid continuous coordinates; under P0, K has the distribution R_n. These are the exact coupling/count facts in skyline-count-information/RESULT.md.

For the first auxiliary Poisson process take intensity m times uniform area, and condition its total N on n=m−1. For the second take intensity mμ_c, and condition its total on m. Conditional point laws are exactly P0 and P1, respectively. The two conditioning probabilities coincide:

    P(Poisson(m)=m−1)=P(Poisson(m)=m)=p_m>0.                 (8)

In the respective models put Z0=mU and Z1=mμ_c(E). Equation (4) at t=log 2 gives a nonnegative random variable with Poisson expectation one. Therefore, after conditioning,

    E_j exp[−(log 2)K+Zj/2] ≤1/p_m.                         (9)

This is an inequality: the other total-count events make nonnegative contributions to the unconditional expectation.

By Cauchy–Schwarz within each conditioned law,

    E_j exp(Zj/4)
      =E_j{exp[−(log 2)K+Zj/2]^(1/2) 2^(K/2)}
      ≤p_m^(−1/2) [E_j 2^K]^(1/2)
      ≤sqrt((m+1)/p_m).                                   (10)

For the final step, independent record indicators give

    E[2^(R_l)]=product_(a=1)^l (1+1/a)=l+1.

The P1 stochastic domination and the P0 exact record law justify the bound simultaneously. We do not assume independence of Joe record indicators or of K and U.

Finally Z0=mU≥nU, and Z1=mμ_c(E)≥mcU=nU. Monotonicity of the exponential in (10) proves (1). Markov's inequality proves (2). The tail in (2) says that nU is stochastically dominated by B_m+4T, where T is Exp(1); for thresholds below B_m use the trivial bound one. Expanding its rth moment gives (3). All statements hold for n≥1; the asymptotic notation concerns n→∞.

Count also has the simple uniform tail

    P_j(K≥log(m+1)/log 2+x/log 2)≤exp(−x),     x≥0,

by E_j 2^K≤m+1. Combining this with (2) localizes K+mU on a constant multiple of log m, with failure smaller than any prescribed inverse power of m by increasing that constant. Raw moment bounds E_j(K+mU)^r=O_r((log m)^r) follow as m/n≤2.

## 5. What this does and does not unlock

On the existing localized score-expansion domain, its deterministic remainder is bounded by 40(K/m+U)^3. Equation (3) and the count moments therefore imply

    E_j[ R^2 1{K/m≤1/2,U≤1/2} ]
      ≤1600 E_j(K/m+U)^6 =O((log m)^6/m^6).                (11)

Here R means the existing deterministic expansion residual on that domain only. The indicator is indispensable. The source identity and (11) do not bound the exact log likelihood on U→1, do not integrate its singular/boundary behavior, and do not evaluate KL or Hellinger information. They also do not give the sharper desired fourth moment of K−mU: raw moments of K+mU cannot be substituted for cancellation-sensitive moments.

The alternative-only K=m stratum, the finite precision/probe-cost contract, and calibration identifiability are untouched. The Joe corollary depends on the exact declared family and its proved domination; it is not a distribution-free result for unknown calibration. No optimal skyline test or sample lower bound is established here.

## 6. Other narrowly screened mappings

Fill–Naiman's [The Pareto Record Frontier](https://arxiv.org/abs/1901.05620) concerns fixed-n iid independent exponential coordinates. The transformation (u,v)=(exp(−x),exp(−y)) reverses order and maps its maxima/frontier to our uniform minima/staircase. Its frontier coordinate-sum extrema become extrema of −log(uv). Its Sections 3.1–3.3 prove an empty-orthant localization bound. However our U is the weighted exponential-coordinate mass ∫_RS exp(−x−y)dxdy, not the unweighted volume or the width statistic. No joint K,U moment/likelihood theorem was imported from it.

Baldin's [The wrapping hull and a unified framework for volume estimation](https://arxiv.org/abs/1703.01658), Section 4.1, concerns transfer of risks for a particular volume estimator under intersection-stable support classes. It does not state that arbitrary centered mixed skyline moments survive conditioning. Its transfer result was not used here. Convex-hull-specific volume CLTs were screened out for the same model-mismatch reason.

This bounded search stops at a direct applicable theorem and proved elementary fixed-count consequences. It is not a literature-exhaustiveness or field-wide novelty assessment.
