# Credal vertex transport stops at nonlinear geometric correction

11 October 2026 UTC. Focused additive T20 composition check. Ordinary proofs and executable mathematical controls, no protected edits, integration, independent review, formal certification, or programme closure.

## 1. Result and exact scope

The classical finite-vertex rule in `cumulative-credal-audit-coupling-20261011/REPORT.md` requires a **common nonnegative linear branch map followed by normalization**. The normalized power reaction is not such a map. A finite credal polytope cannot generally be transported by correcting its vertices and taking their convex hull. In the three-state example below this operation misses attainable corrected laws; the exact image is nonconvex, and even its convex hull has infinitely many exposed points.

This is a set-valued representation consequence, not merely another demonstration of nonaffinity. Nonaffinity alone would not establish it: every positive binary interval does transport exactly to the interval between its corrected endpoints, although mixture weights change. We prove the sharp positive-segment exception and give two exact constructive representations. The actual Gaussian OU–reaction split also fails endpoint-hull transport, by a separate argument on its own domain.

The three-state fixture and the disjoint-support simplex exception were suggested by the parent. The parent also suggested inverse-reaction membership; the author independently obtained the same representation and the positive-segment classification, and supplied the curved-hull proof and controls. No field novelty is claimed.

## 2. Reaction domain and the exact three-state obstruction

For a finite state space, fix a strictly positive probability reference π and 0<a<1. Define

    R_a^π(p)_i = π_i^(1−a) p_i^a / Z(p),
    Z(p) = Σ_i π_i^(1−a) p_i^a.

This is precisely the finite-space specialization of the normalized density reaction in `fibrewise-split-correction-20261011/RESULT.md` §3. It is **not** a three-state realization of that report's Gaussian OU step. Z(p)>0 for every probability vector, including supported boundary vectors. The finite-state map is invertible, with inverse R_(1/a)^π, and preserves supports.

Take uniform π, a=1/2, and

    p=(1/2,1/4,1/4), q=(1/4,1/2,1/4), K=[p,q].

Both corrected endpoints have third coordinate 1/(2+sqrt(2)). The midpoint m=(3/8,3/8,1/4) has corrected third coordinate 1/(1+sqrt(6)), which is strictly smaller: sqrt(6)>1+sqrt(2), because 6>3+2sqrt(2), equivalently 9>8. Thus R(m) lies outside [R(p),R(q)]. Every law here is strictly positive. No audit nullity, support change, or numerical approximation is involved.

More strongly, write an output as (x,y,z), and d=x−y. The inverse-square formula and the fixed incoming third coordinate give

    x²+y²=3z², x+y+z=1,
    z=g(d)=(sqrt(6+5d²)−1)/5.

As the input traverses K, d continuously and strictly monotonically traverses the interval between the endpoint values. For the parameterization ((1+t)/4,(2−t)/4,1/4), set A=sqrt(1+t), B=sqrt(2−t). Then d=(A−B)/(A+B+1), and d'=[(2B+1)A'−(2A+1)B']/(A+B+1)²>0 because A'>0 and B'<0. Since

    g''(d)=6/(6+5d²)^(3/2)>0,

the output is a strictly convex graph in affine (d,z) coordinates. Its chord contains interior points not on the graph, so the exact image is nonconvex. At every point d₀ its tangent gives a linear functional z−g'(d₀)d uniquely minimized there over the entire graph and its convex hull. Consequently every graph point is exposed in that hull. There are infinitely many exposed points, so the hull is not a finite polytope either.

Hence three different objects must not be conflated: the attainable corrected family R(K), its conservative convex hull, and the finite hull of corrected input vertices. The last is not even an outer bound in this fixture. The first two are distinct, and neither has the claimed finite-vertex form.

## 3. Sharp exception for every strictly positive segment

**Proposition.** For positive probability vectors p,q, fixed positive π, and 0<a<1,

    R_a^π([p,q]) = [R_a^π(p),R_a^π(q)]

if and only if the coordinate ratios p_i/q_i take at most two distinct values.

**Sufficiency.** One ratio means p=q. With two ratios, partition coordinates into their two ratio classes B₁,B₂. Every input on the segment has fixed conditional profile r_j inside each block and variable block masses t_j, t₁+t₂=1. Let c_j=Σ_(i∈B_j) π_i^(1−a)r_ji^a>0. Correction preserves fixed corrected profiles in each block and sends their odds to

    β₁/β₂ = (c₁/c₂)(t₁/t₂)^a.

This is strictly increasing, continuous, and maps the input block-mass interval onto the interval between its endpoint images. The corresponding output laws form exactly the endpoint segment, with different barycentric weights in general.

**Necessity.** Parameterize inputs q+t(p−q), 0≤t≤1, and put u_i=p_i/q_i−1. The unnormalized output coordinate functions are

    F_i(t)=π_i^(1−a)q_i^a(1+t u_i)^a.

If the normalized outputs lie in an affine line, the vector F(t), obtained by multiplying by its positive normalizer, lies in the linear span of two fixed endpoint vectors. Therefore the scalar coordinate functions F_i span a function space of dimension at most two. For m distinct values of u, the m functions (1+t u)^a are linearly independent. Indeed, a linear dependence differentiated at t=0 for k=0,…,m−1 gives a Vandermonde system with entries u^k; the nonzero factors a(a−1)…(a−k+1) can be canceled. Distinct u make that system invertible. Thus m≤2. This proves the criterion. □

The fixture has ratios 2,1/2,1 and violates the criterion. Any positive binary interval satisfies it. The proof does not claim a classification of all higher-dimensional polytopes, all exponents, or support-changing segments. In particular a=1 is the identity and is deliberately excluded.

**Disjoint-support simplex exception.** More generally, let v_j be probability vectors with pairwise disjoint supports and K=conv{v_j}. For any a>0,

    R_a^π(Σ_j λ_j v_j)=Σ_j β_j R_a^π(v_j),
    β_j=λ_j^a Z_j / Σ_k λ_k^a Z_k,
    Z_j=Σ_i π_i^(1−a)v_ji^a.

Every β in the simplex is attained by λ_j proportional to (β_j/Z_j)^(1/a). Thus the finite vertex-hull rule is exact on this full fixed-profile simplex. This is sufficient, not necessary; the positive binary interval is another exception. Disjoint supports matter: overlapping mixture components do not permit splitting the power of a total density into powers of components.

## 4. The actual Gaussian split also fails the vertex-hull rule

Use the exact inherited Φ=R_(1/2)D_(log 2), π=N(0,1), on P₂(R), and the credal segment

    C=conv{δ_−1,δ_+1}.

Every member is in the inherited finite-second-moment domain. The endpoints correct to Q_±=N(±2/7,6/7). The corrected midpoint S is symmetric under z↦−z. If S belonged to conv{Q_−,Q_+}, symmetry would force its coefficient to be 1/2: reflection interchanges the distinct endpoints, so subtracting the two representations gives (2β−1)(Q_−−Q_+)=0.

But the inherited `law-sample-semantics-20261011/RESULT.md` proves S differs from (Q_−+Q_+)/2. Its density is proportional to

    exp(−7z²/12) sqrt(cosh(2z/3)),

whereas the equal mixture of corrected endpoints is proportional to

    exp(−7z²/12) cosh(z/3).

Their logarithmic second derivatives at zero are −17/18 and −19/18. They cannot agree after normalization. Hence S is outside the corrected endpoint hull. This turns the inherited nonaffinity fixture into the required set-image exclusion using symmetry; it does not claim new ownership of that fixture. No claim that this full Gaussian image or its convex hull has infinitely many extreme points is needed or proved here.

## 5. Exact constructive representations, with audit correlation intact

A finite parameter description need not be a finite-vertex description **after** correction. Given a supplied joint polytope K=conv{v₁,…,v_n}, retain its simplex parameter λ and evaluate the actual correction on the complete model v(λ)=Σλ_i v_i. The exact corrected family is {Φ(v(λ)):λ∈Δ}; it must not be replaced by convex combinations of Φ(v_i). Finite source parameters can therefore describe a nonlinear continuum exactly as a formula, without giving a finite list of corrected vertices or a generic efficient optimization algorithm.

For finite reaction, there is a direct membership representation:

    y∈R_a^π(K) iff y∈Δ and R_(1/a)^π(y)∈K.

If K={p∈Δ: A p≤b}, this becomes the finite homogeneous nonlinear inequalities

    Σ_i (A_ji−b_j) π_i^(1−1/a) y_i^(1/a) ≤ 0, for every j.

Equality constraints can be represented by paired inequalities. For a=1/2 these are quadratic constraints; they describe the actual nonconvex image, not its convex hull. General real exponents give exact formulas, not a claim of exact finite-bit arithmetic or tractable generic optimization. Recovering original parameters is only on the valid image. For the full Gaussian split the inherited inverse exists on its exact-law image, but arbitrary-law finite numerical evaluation or stable deconvolution is not supplied.

Preserve **one common model parameter through the whole history**. If a source audit is the declared linear branch M, use v(λ)↦Mv(λ), its mass m(λ), and its normalized state together before geometric correction, restricting to parameters with m(λ)>0; null branches have no conditioned state. The classical vertex rule remains valid at that linear normalization stage. Retain or rederive the same λ's mass if the evidence-normalizer contract is required; corrected-law normalization is not the original audit probability.

If an audit is transported after correction, the inherited `correction-audit-transport-20261011/RESULT.md` gives, for the full split under its inherited hypotheses (in particular a bounded positive pointwise Borel likelihood L and an incoming law r∈P₂),

    Φ(B_L r)=B_(ℓ_r^a)Φ(r), ℓ_r(z)=E_r[L(X)|Z=z].

The factor is paired with **that same r=v(λ)**. Replacing the family of pairs (Φ(v(λ)),ℓ_(v(λ))) by independent ranges would recreate the source-audit coupling defect. Subsequent audits require the updated model's conditional factor. Pure finite reaction has the simpler inherited identity R_a B_L=B_(L^a)R_a, with audit normalizers still accounted for separately. Neither identity licenses model reselection or independent recombination of uncertainty coordinates.

These representations retain only numerical model correlations. If distinct source histories had already been mapped to one numerical law, no injective law correction restores omitted source identity or basing. No actual cognitive episode, duty, warrant gain, target authentication, or theological conclusion follows.

## 6. Branchwise audit transport is not automatically an observation instrument

The parent suggested this additional finite-state composition guard. Fix a finite outcome set and strictly positive likelihoods L_o(i), with Σ_o L_o(i)=1 at each latent state i. Each branch transports through reaction as the Bayes map B_(L_o^a). These maps can all be represented by **one same-outcome passive stochastic observation channel on the corrected finite-state simplex**, valid for every positive corrected prior, if and only if there are constants c_o>0 such that

    Σ_o c_o L_o(i)^a=1 for every i.

Indeed two strictly positive likelihood vectors give the same normalized Bayes map on every positive prior exactly when they are proportional: comparing output coordinate odds cancels the positive prior odds and fixes every pairwise likelihood ratio. Therefore any realizing channel must have rows M_o(i)=c_o L_o(i)^a. The displayed equations are precisely its column-normalization conditions, and are sufficient as well. This is a finite positive linear-feasibility condition for the specified outcome labels; it is not an impossibility assertion for every conceivable larger experiment.

For the parent's exact countercontrol, take a=1/2, L_1=(1/4,1/2,3/4), L_0=1−L_1. The first and third state equations force c_1=c_0=c. The middle state forces c=1/sqrt(2). Either endpoint then has column sum (1+sqrt(3))/(2sqrt(2))≠1: equality would imply sqrt(3)=sqrt(8)−1, whose square forces sqrt(2)=3/2, impossible. Thus every transported branch is a perfectly valid positive Bayes map, but the whole named collection has no same-outcome channel realization on all corrected priors.

The same fixture in fact excludes every a>0 except a=1. Endpoint subtraction forces equal scales; comparison with the middle state would then require (1/4)^a+(3/4)^a=2(1/2)^a. Strict concavity for 0<a<1 and strict convexity for a>1 both exclude this equality. At a=1 the original channel itself works. Therefore universal same-outcome compatibility across all finite positive observation channels holds among positive exponents exactly at a=1. This short extension was also suggested by the parent; it concerns normalized branch maps, without asserting event-probability preservation away from the identity.

In this counterexample, dividing the powered likelihoods by their statewise sum enforces column normalization but changes their Bayes maps, because that divisor is nonconstant across states. Adding a residual failure outcome after uniformly scaling all original rows is possible in a finite model; it changes the outcome contract. Neither operation is the requested same-outcome transport. Even when constants exist, equality of corrected branch posteriors alone does not equate their occurrence probabilities with the original audit's occurrence probabilities.

The complete-instrument versus isolated-branch distinction is already explicit in `fixed-channel-review-20261010/RESULT.md` §3 and its inherited source. `correction-audit-transport` already owns proportional multipliers, conditional responses and separate masses. This section applies those requirements to the powered likelihood family; it does not show that an inspected implementation actually misuses them, or infer new evidence/warrant from geometric correction. The criterion here concerns pure finite reaction, not a claim that the full Gaussian split admits prior-independent branch factors.

## 7. Prior ownership and verification boundary

Inspected principal owners are hash-bound in INPUT_BINDINGS.json:

- cumulative-credal-audit-coupling: the coupled-model collision, classical common-linear vertex rule and normalizer pairing;
- fibrewise-split-correction: the normalized reaction, exact OU split and overlapping-mixture obstruction;
- law-sample-semantics: full-split nonaffinity and the exact Gaussian fixture;
- correction-audit-transport: exact-law injectivity, model-dependent audit response, actual-image inversion and separate evidence masses.

A bounded top-level RESULT/REPORT scan for credal, polytope, vertex, convex hull and related block terms, followed by relevant-section inspection, found different owners: fixed-channel-review treats Bayes-stable convex sets and their block decomposition; completion-bayes-commutation and face-stratified-noetic-geometry treat exponential completion and moment-polytope faces; reference-bregman-classification treats reference-dependent divergence contraction. None of those inspected sections establishes this corrected credal-image classification. This is not an exhaustive corpus or external priority search. The formulas and mechanisms are elementary/inherited; the bounded contribution is their exact composition consequence and its declared exceptions.

`python3 verify.py` provides symbolic radical/derivative identities, the curved-arc supporting geometry, inverse membership, two-block and disjoint-support controls, the Vandermonde determinant, inherited actual-Gaussian curvature control, and same-outcome instrument obstruction. Proofs establish the universal claims; selected cases do not substitute for them. CHECKS.json records the passing run of 86 assertion groups, including eight input-hash checks. This is author verification, not independent review.
