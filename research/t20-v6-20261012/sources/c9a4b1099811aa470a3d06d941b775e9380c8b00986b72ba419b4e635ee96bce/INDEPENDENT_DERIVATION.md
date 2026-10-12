# Independent derivation: finite-distance Fisher boundary transport

10 October 2026 UTC. Scoped ordinary mathematical review. This document records independent checks of the proposed transport, before inspecting the author's finished result. It is not a final-byte acceptance, a new moment-indeterminacy theorem, a formal-kernel result, a protected edit, or programme closure.

## Inherited inputs and actual geometric structure

The laws ν± and their common moments m_r=exp(r²/2), distinctness, absence of positive exponential moments, and separated positive-time mean germs are inherited from measure-moment-continuation-boundary-20261009/RESULT.md, §§2 and 4–6. The reverse-damped inputs μ±=T_aν± and their endpoint role are inherited from exponential-tail-effectivity-20261010/RESULT.md, §6. They receive no new-result credit here.

The actual finite exponential-leaf formulas read in leafwise-noetic-geometry-20261010/RESULT.md, §§6–8, are z=∇A_r(θ), Cov=Hess A_r, and Hess ψ_r=Cov⁻¹, with the reference class retained. The present half-line calculation must establish its own domain and regularity; it cannot import the finite theorem's full natural-parameter domain or global moment-polytope conclusion.

The inherited local-Hessian repair source, noetic-gradient-transport-20261009/INHERITED_HESSIAN_SOURCE.md, Setup and S1–S2, uses D_F(x,y)=F(x)−F(y)−dF_y(x−y), with forecast in the second argument. Its local compatibility statement does not identify whole generators from one-point Hessian agreement. information-geometry-transport-20261009/RESULT.md, §2, explicitly demands Hessian comparison at all points for a Bregman contract. Those geometric distinctions already exist and remain intact.

## Direct half-line calculation

For either source law ν set

    Z(v)=∫exp(−vx)dν, A(v)=log Z(v),
    ν_v=exp(−vx)ν/Z(v), q(v)=−A′(v), V(v)=A″(v), v≥0.

For every n, differentiation on [0,a] is justified by the inherited finite nth and subsequent moments. Consequently Z and A have continuous derivatives of every finite order through the right endpoint v=0; this is one-sided C∞, not analyticity. The normalized derivative identities give

    q′=−V, V=E_v[X²]−E_v[X]²>0,
    V(0)=exp(2)−exp(1)>0.

The strict inequality follows because ν_v has the same null sets as its nondegenerate, positive-density base ν. If D=Z(a)>0, then Z(v)≥D and

    0<V(v)≤E_v[X²]≤m₂/D, 0≤v≤a.

The path's Fisher length is therefore at most a√(m₂/D). Approaching v=0 on this one leaf is Cauchy in the induced length metric. Finite distance does not identify endpoints belonging to different laws or leaves.

For a concrete common-space realization take s(v)=√(dν_v/dx) in L²(dx). Its derivative is −(x−q(v))s(v)/2. Thus 4∥s′(v)∥²=V(v)>0. Every higher derivative is a degree-at-most-n polynomial in x, with smooth bounded parameter-dependent coefficients on [0,a], times s(v). Squared domination by C_n(1+x^(2n))dν/dx proves one-sided L²-C∞ regularity. The two endpoint vectors remain distinct: the squared norm of their difference is the strictly positive integral

    ∫f(x)[√(1+sin(2πlog x)/2)−√(1−sin(2πlog x)/2)]² dx.

This realization requires no declaration that all positive densities are an open Hilbert manifold.

## Mean-coordinate sign and Bregman orientation

On a small common mean interval (q₀−ε,q₀], q₀=exp(1/2), the inverse v=v(q) exists and is one-sided C∞ since q′=−V never vanishes. The natural parameter conjugate to q is η=−v. Define

    Φ(q)=−v(q)q−A(v(q)).

Then Φ′=−v and Φ″=1/V>0. In particular Φ(q₀)=Φ′(q₀)=0. The Fisher metric changes coordinates as V(v)dv²=Φ″(q)dq².

For v,w on the same source leaf, direct integration of the logarithmic density ratio gives

    KL(ν_v || ν_w)=(w−v)q(v)−A(v)+A(w)
                   =D_A(w,v)=D_Φ(q(v),q(w)).

All terms are finite, even with v or w zero, because every ν_v has finite mean. Reversing the first two parameters in D_A is necessary; D_A(v,w) is the opposite KL orientation. Cross-source KL is not represented by either source-specific one-dimensional potential.

## Jets, germs, and analytic scope

Since Z±(0)=1 and Z±^(n)(0+)=(-1)^n m_n, the full one-sided A, q, V, inverse-v, Φ and Φ″ jets agree between sources. The inverse jets are obtained recursively using q′(0)≠0; a finite derivative order uses only finitely many cumulants. Bregman two-variable jets agree at the endpoint pair in their respective common affine coordinates. This does not say that jets at distinct positive parameter values agree.

Nevertheless V+ and V− cannot agree on any right neighborhood of zero. Two integrations using A±(0)=0 and A′±(0)=−q₀ would identify the Laplace transforms there, contradicting the inherited separated Laplace/mean continuation germs. If Φ″+ and Φ″− agreed on a mean neighborhood of q₀, integration using Φ′±(q₀)=0 would give v+=v−, and Φ±(q₀)=0 would then identify the duals and A germs. Thus these mean-coordinate metric germs also differ. Equality of the Bregman germs would identify the metric germs by differentiation along the diagonal, so they differ as well.

The common formal Taylor series for Z at zero has radius zero, since m_n/n! has nth root diverging. An analytic A or V extension would give analytic Z by integration and exponentiation, which is impossible. An analytic Φ or Φ″ extension with its positive endpoint Hessian would, by analytic inversion of η=Φ′(q), reconstruct an analytic A, also impossible. These claims concern the specified natural and mean affine coordinates. Every positive smooth one-dimensional Riemannian metric is locally flattened by arc length, so the result is not an intrinsic obstruction to choosing an analytic metric coordinate.

For the original reverse-damped μ=T_aν,

    log Z_μ(u)=A(u+a)−log D.

The endpoint value −log D is retained history and can differ across the two sources. Only centered log partitions have the stipulated common zeroth jet. Additive constants cancel from both Hessians and Bregman divergences.

## Credit and limits

The parent supplied the finite-distance bound, endpoint-variance check, and participating proof in fisher-boundary-root-20261010/GEOMETRIC_TRANSPORT.md. The present reviewer independently derived the sign/orientation and germ arguments and checked the source hypotheses. The author remains responsible for the proposed deliverable and controls. Root participation is not relabeled as independent review.

The result is a faithful statistical/Fisher-Hessian transport test of a moment/jet representation. It is not metric-completion collapse, equality or nonisometry of abstract unmarked Riemannian germs, a cognitive-state identification, empirical or normative warrant, an optimization recommendation, or a new proof of the already inherited equal-moment obstruction.
