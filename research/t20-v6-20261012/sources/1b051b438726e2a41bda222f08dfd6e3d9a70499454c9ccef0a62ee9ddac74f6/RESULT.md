# A finite-distance Fisher boundary need not preserve moment-state continuation

10 October 2026 UTC. Additive ordinary mathematical transport within ACTIVE T20. No protected edit, canonical integration, new tranche, formal-kernel certification, field-priority claim, sampling-optimization programme, empirical identification, or closure claim. The root proposed the transport and supplied a participating derivation; this packet develops the exact chart, Bregman, and boundary qualifications. Independent review, if completed, is a separate artifact.

## 1. Outcome and what is actually added

The inherited lognormal endpoint example has a stronger geometric property. Its two endpoint laws have:

- finite, strictly positive Fisher speed squared, and finite Fisher length from the reverse-damped original law;
- a one-sided smooth statistical immersion, with no vanishing or divergent metric coefficient at the endpoint;
- identical, uniformly computable full endpoint jets of their normalized log-partition functions, mean responses, variances, and mean-coordinate Hessian potentials;
- identical full endpoint jets of the associated Bregman divergences, while the actual metric, potential, and divergence germs differ.

Consequently, a finite nonsingular one-sided Fisher/Hessian geometry, even augmented by its complete endpoint derivative record, does not repair the failure of actual-update congruence of the moment-state representation. This is a conditional counterexample about the specified representation and continuation. It is **not** a failure of the full statistical state, its intrinsic metric completion, or its entire metric germ to distinguish the two laws.

The new-to-the-inspected-ancestors deduction is the exact geometric transport and resulting regularity-versus-continuation discriminator. The laws, equal moments, equal time jets, different futures, endpoint embedding, and nonanalyticity of the Laplace transform are already owned:

1. `measure-moment-continuation-boundary-20261009/RESULT.md`, §§2 and 4–6, proves the half-line tilt, its Fisher pairing, the lognormal Stieltjes pair, equal full moment/time jets, different mean germs, and zero Taylor radius of the endpoint Laplace transform.
2. `exponential-tail-effectivity-20261010/RESULT.md`, §6, already reverse-damps this pair into computable exponential-tail inputs, proves the finite computable endpoint records coincide, and identifies the resulting continuation-congruence loss. Its final ordinary independent review accepts that claim.
3. `leafwise-noetic-geometry-20261010/RESULT.md`, §§6–8, already supplies the finite-reference exponential-leaf remedy: covariance is the natural-coordinate metric, inverse covariance is the mean-coordinate Hessian metric, and the reference class is essential data. The present half-line boundary calculation does not import that packet's finite-support global mean-surjectivity theorem.
4. `information-geometry-transport-20261009/RESULT.md`, §2, fixes the Bregman orientation and distinguishes an all-points Hessian/divergence contract from a match at a point. The inherited local-Hessian repair source uses that orientation for finite proper losses. No proper-score repair theorem is transferred merely by reusing the word Hessian.

Those files are copied without changes in `inputs/` and bound in `INPUT_BINDINGS.json`. This is a targeted ownership comparison, not an exhaustive novelty survey.

## 2. Exact laws, endpoint, and reference data

Let ρ have density

    f(x) = exp(−(log x)²/2)/(x sqrt(2π)),  x > 0,

and set ε = 1/2 and

    dν_σ/dρ = 1 + σ ε sin(2π log x),  σ ∈ {+1,−1}.

The inherited proof gives distinct probability laws with strictly positive densities and

    m_r(ν_+) = m_r(ν_−) = exp(r²/2),  r = 0,1,2,… .       (1)

For either sign write

    L_σ(t) = ∫exp(−t x)dν_σ,
    F_σ(t) = log L_σ(t),
    p_σ,t = T_t ν_σ = exp(−t x)ν_σ/L_σ(t),  t ≥ 0,
    q_σ(t) = ∫x dp_σ,t,
    V_σ(t) = Var_(p_σ,t)(X).                              (2)

Fix a computable a > 0, D_σ = L_σ(a), and μ_σ = T_aν_σ. Then

    T_u μ_σ = p_σ,a+u,  u ≥ −a,
    log Z_(μ_σ)(u) = F_σ(a+u) − log D_σ.                  (3)

In particular u = −a corresponds to t = 0, while μ_σ itself is t = a. Both original μ_σ have a computable full moment name and a supplied common positive exponential bound, as proved in the endpoint ancestor. Their original moment records differ. Their endpoint moment records agree and are uniformly computable by (1).

The constants −log D_σ in (3) are retained as original-history data; they need not agree. It is the centered endpoint potentials F_σ, with F_σ(0) = 0, whose full jets agree. Metrics and Bregman divergences are insensitive to the additive constant, but the original normalizer is not being silently identified or discarded by this calculation.

For each σ the natural parameter η = −t has domain (−∞,0], not an open neighborhood of 0. Indeed the inherited lower density bound ν_σ ≥ ρ/2 and lognormal positive-exponential divergence give ∫exp(c x)dν_σ = ∞ for every c > 0. Therefore t < 0 cannot be admitted by normalization. “Nonsingular metric at the boundary” below does not mean “regular exponential family on an open domain containing the boundary.”

The two laws are not members of one common scalar exponential leaf: log(dν_+/dν_−) is bounded and nonconstant on (0,∞). If it equaled b+c x almost everywhere, boundedness would force c = 0, and continuity and nonconstancy would give a contradiction. Thus the full reference class modulo span{1,x} is different. Fixing one such class remains a legitimate leafwise remedy; forgetting it is a change of representation.

## 3. One-sided smooth Fisher geometry and finite distance

### Theorem G1

For each σ and each finite b > 0, the curve in (2) has all one-sided parameter derivatives at t = 0 and is a one-sided smooth Fisher immersion. Its induced metric is

    ds² = V_σ(t) dt²,
    F_σ′(t) = −q_σ(t),
    F_σ″(t) = V_σ(t),
    q_σ′(t) = −V_σ(t).                                   (4)

The metric coefficient is finite and strictly positive throughout [0,b], with

    V_σ(0) = exp(2) − exp(1) > 0,
    0 < V_σ(t) ≤ exp(2)/L_σ(b).                            (5)

The length of the parameter segment joining ν_σ and T_bν_σ is bounded by

    length ≤ b sqrt(exp(2)/L_σ(b)) < ∞.                   (6)

For b = a this gives the finite-length approach from μ_σ to its endpoint. It is a length bound for the stated curve, without a claim that the curve minimizes ambient Fisher distance.

**Proof.** For every r,k ≥ 0, differentiation of ∫x^r exp(−t x)dν_σ is justified by domination by x^(r+k), with one more finite moment available for the relevant difference quotient at 0. Thus L and all normalized moments are smooth in the one-sided sense. On [0,b], L_σ(t) ≥ L_σ(b) > 0, so division has no singularity. Logarithmic and quotient differentiation give (4). The tilted law has an everywhere positive density on (0,∞), so X is not almost surely constant and its variance is positive. Also

    V_σ(t) ≤ E_(p_σ,t)X² ≤ m_2(ν_σ)/L_σ(b),

which proves (5) and (6). Continuity and compactness further give a positive lower bound on V_σ on each such interval; no uniform lower bound over an unspecified family of laws is asserted.

For a direct statistical-geometry check, use the common ambient Hilbert space L²(ρ) and square-root densities

    s_σ(t,x) = sqrt(1+σ ε sin(2π log x))
               exp(−t x/2)/sqrt(L_σ(t)).

Their L² norms equal 1. Every k-th parameter derivative on [0,b] is bounded pointwise by a constant times (1+x^k), with its square integrable under ρ by (1). Difference quotients are controlled similarly with the next order. Dominated convergence therefore proves one-sided C∞ regularity in L², rather than just formal pointwise differentiation. The first derivative is

    ∂_t s_σ = −(x−q_σ(t))s_σ/2,
    4 ||∂_t s_σ||²_(L²(ρ)) = V_σ(t) > 0.                 (7)

With the Fisher convention h_p(ap,bp)=∫ab dp on zero-mean scores, (7) is exactly the pullback metric (4). The nonzero derivative makes this a one-dimensional immersion; it does not put all positive densities in an open Hilbert manifold. ∎

The same pairing shows that X−q is the Fisher gradient score of the supplied linear objective J(p)=E_pX. Hence t increasing is its negative-gradient path and its squared speed is V. Reversing from t=a to t=0 uses the opposite sign and is a finite-length path, not negative-objective descent. Neither direction is an assertion of truth, warrant, or cognitive realization.

### The endpoints are still different geometric states

In the common square-root embedding,

    ⟨s_+(0),s_−(0)⟩ = ∫sqrt(1−ε² sin²(2π log x))dρ < 1.  (8)

Strictness follows because the sine is nonzero on a set of positive ρ measure. Therefore the square-root endpoint densities have strictly positive L² separation. In addition 1/3 ≤ dν_+/dν_− ≤ 3, so both endpoint-to-endpoint KL divergences are finite and strictly positive. Neither this embedding nor metric completion itself identifies the endpoints. The identification is imposed by retaining only the equal moment/derivative record.

## 4. Exact mean-coordinate Hessian and Bregman transport

Let q_0 = exp(1/2). Choose b > 0. Since q_σ′ = −V_σ < 0, each q_σ maps [0,b] bijectively onto [q_σ(b),q_0]. On the common one-sided mean neighborhood

    I = (max{q_+(b),q_−(b)},q_0],

write t_σ(q) for its inverse. Repeated inverse differentiation is legitimate up to the endpoint because V_σ has a positive continuous limit there. Define

    ψ_σ(q) = −t_σ(q)q − F_σ(t_σ(q)).                     (9)

This is the local Legendre potential for A_σ(η)=F_σ(−η), using the actual mean q, rather than the negated mean. Direct differentiation gives

    ψ_σ′(q) = −t_σ(q),
    ψ_σ″(q) = 1/V_σ(t_σ(q)) > 0,
    V_σ(t)dt² = ψ_σ″(q)dq²,
    ψ_σ(q_0) = ψ_σ′(q_0) = 0.                            (10)

This is the precise one-dimensional counterpart of the inherited leafwise covariance/inverse-covariance geometry. No claim is made that I is the full realizable-mean interior or that a finite-support global theorem applies to this non-steep boundary.

Use the inherited Bregman orientation

    B_ψ(r,q) = ψ(r)−ψ(q)−ψ′(q)(r−q).                     (11)

For s,t ≥ 0 with their means in I, the density-ratio calculation gives

    KL(p_σ,s || p_σ,t)
       = (t−s)q_σ(s) − F_σ(s)+F_σ(t)
       = B_(ψ_σ)(q_σ(s),q_σ(t))
       = B_(F_σ)(t,s).                                   (12)

These are same-reference identities; the σ labels are not dropped. All terms are finite, including s=0 or t=0, because the first moments are finite. The reversal in natural-parameter Bregman arguments is essential. In particular,

    B_(F_σ)(t,0) = KL(ν_σ || p_σ,t) = F_σ(t)+t q_0,
    B_(F_σ)(0,t) = KL(p_σ,t || ν_σ) = −F_σ(t)−t q_σ(t),
    B_(ψ_σ)(q,q_0) = ψ_σ(q) = KL(p_σ,tσ(q) || ν_σ).       (13)

Thus the construction really supplies Fisher/Hessian and KL/Bregman structures; it does not merely attach those names to an arbitrary moment vector.

## 5. Identical full geometric jets, unequal actual germs

### Theorem G2

At t=0 the centered F_+,F_− have identical full one-sided jets; so do q_+,q_− and V_+,V_−. At q=q_0 the potentials ψ_+,ψ_− and metric coefficients ψ_+″,ψ_−″ have identical full one-sided jets. The two Bregman functions have identical full one-sided jets at (q_0,q_0).

Nevertheless, each of the following pairs has different one-sided germs: V_+(t),V_−(t); ψ_+(q),ψ_−(q); and ψ_+″(q),ψ_−″(q). In particular the two boundary-anchored divergences B_(ψ_σ)(q,q_0) differ somewhere in every sufficiently small left neighborhood of q_0.

**Proof of jet equality.** By (1),

    L_σ^(k)(0+) = (−1)^k exp(k²/2).

Logarithmic differentiation expresses every derivative of F at zero by a finite polynomial in moments, with L(0)=1. Differentiating (4) gives the q and V jets. Inverting q uses q′(0)=−V_0≠0. Every inverse-jet entry is a rational expression in finitely many q-jet entries, with powers of the same nonzero V_0 in the denominator. Equations (9)–(10) give the common ψ and ψ″ jets. Every mixed derivative of (11) is a finite expression in the corresponding ψ jets, so the bivariate boundary jets agree. These recursive formulas compute each requested derivative uniformly from the computable sequence (1); no effective recovery of a function from those jets is being assumed.

For example, with κ_3=m_3−3m_1m_2+2m_1³,

    F(0)=0,  F′(0)=−m_1,  F″(0)=V_0,
    V′(0)=−κ_3,
    ψ″(q_0)=1/V_0,  ψ‴(q_0)=−κ_3/V_0³,
    V_0=exp(2)−exp(1).

Taylor's theorem on one-sided compact intervals makes each difference flat at its endpoint: for every fixed N it is o(t^N), or o(|q−q_0|^N), as appropriate.

**Proof of unequal germs.** If V_+=V_− on a right neighborhood of zero, integrating twice with their common F(0)=0 and F′(0)=−q_0 gives F_+=F_− there. Their Laplace transforms would coincide on a positive interval. They are analytic on t>0, so the identity theorem and Laplace uniqueness, as proved in the ancestor, would give ν_+=ν_−, a contradiction.

If ψ_+″=ψ_−″ on a left neighborhood of q_0, integration with ψ_σ(q_0)=ψ_σ′(q_0)=0 gives ψ_+=ψ_− there. Their derivatives then give t_+(q)=t_−(q), and (9) recovers identical F functions on a right neighborhood of zero, the same contradiction. Equality of the ψ germs alone also implies equality of their derivatives and the same contradiction. Finally (13) makes the boundary-anchored Bregman claim exact. ∎

The comparison in mean coordinates uses the same numerical mean q on the two different source leaves. Those are generally different laws and different tilt parameters t_σ(q). This is a test of whether one metric/potential germ can be inferred from the endpoint record, not a claim that the full metric germs coincide or that those two laws are statistically equivalent. The coordinate q is the distinguished operational observable, so equality here is required in that fixed mean chart. Arbitrary one-dimensional Riemannian germs can be locally isometric after changing to arc length; no intrinsic nonisometry claim is made.

### Actual consequence for the representation

Let R(ν) be the full raw moment record, optionally augmented by the geometric endpoint jets just described. The augmented records of ν_+ and ν_− still coincide. There is therefore no rule that assigns from this record alone a mean-coordinate metric germ agreeing with both actual source-leaf Fisher metrics. The same holds for the calibrated potential or Bregman germ. A record-dependent single choice necessarily disagrees with at least one of these two allowed underlying states.

This is sharper than merely observing that q_+(t) and q_−(t) have equal jets: it excludes a proposed repair based on endpoint metric nonsingularity, finite metric distance, or completion of the derivative data. It does not exclude repair by retaining the full reference law, its leaf class together with adequate within-leaf state, or the original certified μ_σ and control history. The endpoint ancestor already shows that retaining the latter data computes later t>0 continuations.

For the given linear objective, each actual mean-coordinate metric yields the autonomous equation

    dq/dt = −1/ψ_σ″(q).

Each right-hand side is smooth and nonzero up to q_0 on its own side. The differing continuations do not violate uniqueness for one specified locally Lipschitz scalar vector field: the actual fields differ on every neighborhood, even though their full endpoint jets agree. No infinite-dimensional Lipschitz uniqueness theorem is being claimed or contradicted.

As a further finite-rank guard, for any d≥1 the endpoint covariance matrix of (X,…,X^d) is the same for both laws and is positive definite. Its entries are m_(i+j)−m_i m_j. For a nonzero coefficient vector, zero variance would require a nonconstant polynomial to be constant almost everywhere under an everywhere positive density, which is impossible. Thus every finite polynomial covariance block is nonsingular. This says nothing about bounded invertibility of an infinite covariance operator in an unspecified topology.

## 6. No analytic extension in the declared affine coordinates

### Theorem G3

None of L_σ, F_σ, q_σ, or V_σ admits a real-analytic extension through t=0 agreeing with its given right germ. Neither ψ_σ nor its mean-metric coefficient ψ_σ″ admits such an extension through q=q_0 in the declared mean affine coordinate.

**Proof.** The inherited Laplace Taylor coefficients have absolute terms at nonzero z proportional to

    exp(n²/2)|z|^n/n!,

whose successive ratio is |z|exp(n+1/2)/(n+1)→∞. Therefore their radius of convergence is zero. Any analytic extension of L would have these derivatives and hence a Taylor series of positive radius, a contradiction. An analytic extension of F would give L=exp(F). An analytic extension of q=−F′ or V=F″ could be integrated using the endpoint constants to give an analytic F. All are impossible.

If ψ had an analytic extension with ψ″(q_0)=1/V_0>0, then η=ψ′(q) would have an analytic inverse q=q(η) near η=0. The Legendre identity

    A(η)=η q(η)−ψ(q(η))

would extend A(η)=F(−η) analytically, again impossible. An analytic extension of ψ″ could be integrated twice with the endpoint constants to give such a ψ. ∎

This analyticity conclusion is tied to the specified natural/mean affine structures and statistical partition function. It is not a coordinate-free claim that a one-dimensional Riemannian metric can never be made analytic. Indeed the one-sided arc-length coordinate ℓ(t)=∫_0^t sqrt(V(s))ds makes its metric dℓ². No abstract smooth extension is ruled out, and no extension to t<0 as the same normalized exponential statistical family is asserted. Finite distance, smooth one-sided immersion, nonzero endpoint Hessian, and real-analytic statistical extension are distinct conditions.

## 7. Classical source checks, executed controls, and claim ceiling

The directly inspected primary technical source is Wainwright and Jordan, *Graphical Models, Exponential Families, and Variational Inference* (2008), §§3.2, 3.5.1, and 5.2.2, especially Proposition 3.1 and equations (5.10)–(5.12): https://www.cs.columbia.edu/~blei/fogm/2020F/readings/WainwrightJordan2008.pdf . These loci supply the classical exponential-family, covariance, and KL/Bregman ancestry. Their regular-family results use an open natural domain; our endpoint has a closed-sided domain and its derivative identities are proved directly by domination. No general mean-surjectivity or essential-smoothness theorem is imported. The source is the published primary work hosted by an academic course; the previously cited author-hosted URL returned a fetch error during this check. `PRIMARY_SOURCE_NOTES.json` records the exact inspected loci and this qualification.

The classical lognormal moment-indeterminacy and Laplace uniqueness ancestry is retained from the first ancestor rather than rebranded as a new probability theorem. Ordinary dominated convergence, inverse differentiation, the analytic inverse function theorem, and the identity theorem are the additional analytic tools used explicitly above.

`verify.py` checks the generic moment/cumulant signs, inverse mean-metric derivative formula, Bregman orientations and duality, normalizer translation, finite-polynomial covariance positivity in exact controls, and an elementary finite-support positive control. It also verifies source snapshot hashes. These bounded symbolic checks supplement the general ordinary proofs; they do not establish an infinite analytic theorem by enumeration or certify it in a proof kernel.

The outcome is a geometric boundary discriminator for one exact numerical continuation interface. It adds no account of source reliability, normative authority, mental states, empirical success, metaphysical uniqueness, or actual warrant. No protected source was edited and no T20 closure is asserted.
