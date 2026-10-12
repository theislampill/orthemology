# Exact audit commutation does not preserve correction-path rectifiability

11 October2026 UTC. Root ordinary mathematical candidate; independent review pending. A direct continuation of the reviewed infinite-initial Fisher-length example, within the same probability-law and fixed-audit semantics. No source-warrant or empirical claim.

## Positive audit with a changed path-length class

Use the earlier p_0=1/2, p_n=1/[2n(n+1)], V_0=0, V_n=exp(n²), n≥1. Its normalized exponential-tilt orbit has infinite Fisher–Rao length in every initial neighborhood.

Fix L_0=1 and L_n=(n+1)/n³ for n≥1. This likelihood is strictly positive everywhere and bounded above by2. It does not delete support. Its normalizer is (1+ζ(4))/2, so the audited initial law is

    p'_0=1/(1+ζ(4)),
    p'_n=1/[(1+ζ(4))n⁴].

Every fixed-time audit square commutes exactly: B_L(S_t p)=S_t(B_L p), because both sides have density proportional to L exp(−tV) relative to p. Yet the audited exponential orbit has finite Fisher–Rao length on [0,T] for every finite T. Indeed p'_0>0 and sum_n sqrt(p'_n)<∞. With r_n(t)=sqrt(p'_n)exp(−tV_n/2), differentiation of r/||r|| and ||r||≥sqrt(p'_0) give

    length_FR ≤ (2/sqrt(p'_0)) sum_(n≥1) sqrt(p'_n)[1−exp(−TV_n/2)] <∞.

Thus exact audit/flow commutation, positivity and unchanged support do not preserve finite versus infinite length of the prescribed correction path. The audit changes the metric weighting of directions. It does not make the original infinite path cease to exist or alter the conclusion that endpoint intrinsic distance is finite. The inverse audit is unbounded; its domain must be checked separately, not treated as uniformly conditioned.

## Uniform two-sided likelihood bounds repair metric comparability

Suppose instead fixed L obeys 0<ell≤L≤u<∞ almost surely. For μ and ν=B_L μ, density dν/dμ lies between ell/u and u/ell. A Fisher tangent can be represented by score v with Eμv=0 and Eμv²<∞. Differentiating the normalized audit gives audited score v−Eνv. Its squared tangent norm is Varν(v). Since variance is min_c E[(v−c)²],

    (ell/u) Varμ(v) ≤ Varν(v) ≤ (u/ell) Varμ(v).

Hence every Fisher–Rao regular path on the common fixed-likelihood domain has audited speed between sqrt(ell/u) and sqrt(u/ell) times its original speed. For absolutely continuous paths, integration gives the same comparison of prescribed path lengths. More generally, the bounds imply global bi-Lipschitz comparability: integrate the upper tangent bound along a nonnegative square-root great-circle arc between any two laws to obtain d_FR(B_L μ,B_L ρ)≤sqrt(u/ell)d_FR(μ,ρ); applying the same argument to the inverse likelihood1/L gives the reverse bound. Taking suprema over finite path partitions then preserves rectifiability for arbitrary continuous paths, without inferring length solely from an almost-everywhere derivative. For merely positive bounded L without a uniform positive lower bound, the preceding exact counterexample shows that the lower comparison cannot be omitted.

This is a sufficient uniform repair, not a necessary condition on every particular path. A path-dependent weaker comparison may also suffice. The finite-state full-support setting automatically has positive minimum L for a fixed positive likelihood, whereas an infinite state space need not. No reduction of mathematical equivalence of operators to equivalence of their metric costs is justified without this extra structure.

## Ownership and boundary

The infinite initial orbit and the square-root summability bound are inherited from the immediately preceding root example and reviewer-contributed comparison. This note applies an explicit fixed likelihood to connect them, and proves the relevant tangent comparison. Classical Bayes reweighting and variance comparison supply the ingredients; no global novelty claim is made. General source reliability, epistemic improvement, and legitimacy of the likelihood remain independently warranted input conditions. T20 remains active.
