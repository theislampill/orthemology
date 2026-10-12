# Joint atomic geometry: a genuine gradient lift of the finite-rank hierarchy

10 October 2026 UTC. Additive ordinary mathematical research within ACTIVE T20. Written proofs and executable exact controls. No protected edit, baseline rebuild, integration, independent-review status, formal-kernel verification, field-priority claim, empirical identification, or programme closure is asserted.

## 1. Result and ownership

Let F be a coercive real polynomial on R^d. A normalized, coordinatewise C1, full-square-positive polynomial hierarchy satisfying

    L'_t(p) = -L_t(∇F·∇p) - L_t(Fp) + L_t(F)L_t(p)       (H)

and a locally uniform bound on its **full** Hankel rank is exactly one finite-atomic negative-gradient trajectory, on the smooth manifold of distinct positive atoms modulo permutations. Its metric is

    G((u,v),(ũ,ṽ)) = Σ_j u_j ũ_j/w_j + Σ_j w_j v_j·ṽ_j,
    Σ_j u_j = Σ_j ũ_j = 0.                               (G)

The representation, rank constancy and uniqueness are inherited from `complete-flow-finite-rank-20261010/RESULT.md`, §9. The present contribution is their explicit connection to a genuine Riemannian gradient system, its exact moment cometric and finite tensor-coordinate realization, with the boundary and convergence qualifications made explicit. Merely differentiating L(F) would not supply this representation or geometry.

The exact equations and squared speed are

    x'_j = -∇F(x_j),
    w'_j = -w_j(F(x_j)-E),        E = Σ_j w_j F(x_j),
    -E' = ||grad_G E||_G² = ||(w',x')||_G²
        = Σ_j w_j |∇F(x_j)|² + Var_w(F(x_j)).             (D)

This proves existence, uniqueness and forward completeness within the declared stratum, not global minimization for nonconvex F. Finite-time transitions are injective and preserve the number of atoms; asymptotic collapse may lose that information. For λ-strongly convex F, E−min F decays at least as exp(−2λt), all positions converge to the unique minimizer, and the law converges to its Dirac mass, even though no finite-time rank drops.

### Direct inheritance

The nine inspected predecessor reports are copied and hash-bound in `INPUT_BINDINGS.json`.

- `complete-flow-finite-rank-20261010`, §§3–5 and 9, owns finite GNS representation, local atomic charts, Hermite velocity recovery, the forward-completeness/lower-killing reverse lift, the coercive gradient specialization, and injectivity versus surjectivity.
- `continuous-signed-finite-rank-20261010` owns the prior killing-only bounded-full-rank reverse lift and finite GNS machinery. `transport-rank-boundary-20261010` owns the escape/inflow countercontrols showing why rank and moment smoothness alone are insufficient.
- `tensor-moment-continuation-20261009`, §§2–4, owns evolving Fisher replicator dynamics, covariance mobility, exponential tilting and interpolation closure for **known fixed support**. Its N−1 bound is not a moving unknown-support bound.
- `noetic-gradient-transport-20261009` owns the fixed-reference quadratic quotient geometry. `state-dependent-gradient-obstruction-20261009` and `leafwise-noetic-geometry-20261010` own the state-dependent Fisher and coarse-fibre obstructions and conditional exponential-leaf remedies. We do not transfer their finite-channel sufficiency claims to moving atoms.
- `face-stratified-noetic-geometry-20261010` owns a fixed observable-polytope exponential-family boundary analysis. Colliding spatial atoms and zero masses in the present moving-support metric are different boundary mechanisms.
- `moment-evolution-source-comparison-20261010`, §4, already supplies an affine-transport reverse lift under uniform SOS radial killing. This stronger route applies to strongly convex quadratic F and need not assume a bounded-rank path: after the law is forced, finite initial support implies the finite trajectory. That inherited special-case assurance is not generalized here to arbitrary nonlinear coercive gradients.

The gradient/transport/reaction structure is classical; §10 gives cautious source attribution. The finite-moment argument below is elementary interpolation applied to the inherited Hermite construction, not a claim to invent Prony recovery or information geometry. This is a bounded comparison of these inspected reports, not an exhaustive priority search. The participating companion `two-atom-moving-moment-chart-20261010/RESULT.md` gives an explicit rank-two univariate chart and rational quadratic closure; its separate checks are not part of the check count here.

## 2. The smooth state and its metric

Fix r≥1 and d≥1. Let M_r=Δ_r°×Conf_r(R^d), where Conf_r consists of pairwise distinct labelled points (x_1,…,x_r). A tangent is (u,v), with Σu_j=0 and v_j∈R^d. Formula (G) is smooth and positive definite: since each w_j>0, zero squared norm forces u=v=0. For r=1 the weight tangent is zero and the position metric is Euclidean.

The permutation group S_r simultaneously permutes weight-position pairs. Distinct positions make its action free; the finite action is proper. Therefore Q_r=M_r/S_r is a smooth manifold of dimension r(d+1)−1. The invariant metric descends uniquely so the quotient projection is a local isometry, without any division by r!. In d=1 the labelled space has ordering components, which cause no problem for the quotient.

The map (w,x)↦Σw_jδ_(x_j) identifies Q_r bijectively with probabilities having exactly r distinct atoms. Its smooth structure and metric are those transported from the quotient; no ambient infinite-dimensional manifold assertion is needed. A trajectory can be labelled globally once its initial labels are chosen; other continuous labels differ by one fixed permutation, since distinct continuous paths cannot switch labels without meeting.

For E(w,x)=Σw_jF(x_j),

    dE(u,v)=Σ_j F(x_j)u_j+Σ_j w_j∇F(x_j)·v_j.

The vector

    grad_G E=((w_j(F(x_j)−E))_j,(∇F(x_j))_j)              (1)

is tangent and pairs with every tangent as dE, because Σu_j=0. Positive definiteness proves uniqueness. Thus this is a genuine gradient, not an arbitrary field fitted to a decreasing scalar. It is permutation equivariant and induces the gradient on Q_r. Completing the square also shows -grad_G E uniquely minimizes V↦dE(V)+(1/2)G(V,V) over tangents. This is the precise steepest-descent characterization for the declared metric. Changing the coefficients of the transport and reaction blocks would change their relative speeds.

## 3. From abstract hierarchy to the gradient trajectory

“Full-square-positive” means L_t(q²)≥0 for every polynomial q, not strictly positive for every nonzero q: finite atomic laws have nontrivial null polynomials. Assume L_t(1)=1, every polynomial coordinate is C1 on [0,T), (H) holds for every polynomial, and for every H<T there is a finite uniform full Hankel-rank bound R_H on [0,H]. A bound on one truncated matrix or an initial finite-rank condition alone does not replace this path hypothesis.

Coercivity and continuity give m=inf F>−∞ and compact sublevels. Along X'=-∇F(X), dF(X)/dt=−|∇F(X)|²≤0. Every solution through any point remains in a compact sublevel, so local polynomial ODE existence and uniqueness extend it through every finite future time. Thus b=-∇F is forward complete and k=F is bounded below: exactly (C+) and (K−) of the inherited §9 theorem.

That theorem supplies r=rank H(L_0), distinct initial points z_j, and positive a_j summing to one, with

    X_j(t)=Φ_t(z_j),
    K_j(t)=∫_0^t F(X_j(s)) ds,
    W_j(t)=a_j exp(−K_j(t))/Σ_l a_l exp(−K_l(t)),
    L_t(p)=Σ_j W_j(t)p(X_j(t)).                           (2)

At every finite time the weights are positive, positions are distinct, and full rank is r. Equation (1) identifies this **forced representation** as the unique negative-gradient trajectory on Q_r from its initial functional. Conversely any finite initial law gives (2), satisfies (H), and has constant full rank, so supplies an admitted abstract path and its genuine gradient lift on every forward horizon.

The inherited endpoint step is essential. On maximal-rank intervals finite moment charts and Hermite tests recover the atom velocities and mass rates. To exclude entry from infinity at a left endpoint, unnormalize A_t=ρ(t)L_t, with ρ=exp(−∫L(F)). A lower killing bound gives each backwards-tracked atom mass a positive lower bound; the bounded second coordinate A_t(|x|²) then bounds its location. This gives a finite positive endpoint. Forward completeness prevents right-endpoint escape. These arguments close maximal-rank components and exclude hidden births and deaths; energy differentiation alone cannot do that.

No uniqueness outside the locally bounded-full-rank class is asserted. The theorem does not show that every hierarchy from initially finite rank obeys that path bound. It does supply a unique global admitted continuation of any supplied finite-horizon admitted path, since (2) exists for all t≥0.

## 4. Exact moment cometric and finite tensor realization

For a polynomial p put f_p(μ)=L_μ(p). The same pairing yields

    grad_G f_p=((w_j(p(x_j)−L_μ(p)))_j,(∇p(x_j))_j).

Consequently the observable cometric is

    B_μ(p,q)=G(grad f_p,grad f_q)
            =L_μ(∇p·∇q)+L_μ(pq)−L_μ(p)L_μ(q).           (3)

Constants are an irrelevant cotangent gauge, but not the whole kernel. In fact B_μ(p,p)=0 exactly when p has one common value at all atoms and ∇p vanishes at every atom. This is precisely df_p=0 on the atomic tangent space. The polynomial cometric is semidefinite with this jet-kernel; on the actual moment image the kernel is its conormal, and quotienting it gives the positive cotangent metric. Equation (H) is exactly L'_t(p)=−B_(μ_t)(p,F), and -E'=B(F,F). This is intrinsic to a represented atomic law, not an invertible infinite matrix on arbitrary formal sequences.

Let Ψ_r retain all monomial moments of total degree at most 2r−1. Then Ψ_r is injective on laws with at most r atoms, and is a smooth embedding of Q_r onto its exact-r image. This sufficient bound is not claimed optimal.

**Injectivity.** The difference of two such laws is signed and supported on a union of at most 2r points. Choose a linear form ℓ separating that union. A Lagrange polynomial in ℓ, of degree at most 2r−1, isolates the signed mass of any union point. Equality of the retained moments therefore forces every mass difference to vanish.

**Immersion.** At an r-atom state choose a separating ℓ and define

    e_j(x)=∏_(l≠j)(ℓ(x)−ℓ(x_l))/(ℓ(x_j)−ℓ(x_l)).

If a tangent (u,v) annihilates all retained differentials, test with p_ji(x)=(x_i−x_ji)e_j(x)². This has degree ≤2r−1, vanishes at every atom, and has gradient the i-th coordinate vector at atom j and zero at the other atoms. Hence df_(p_ji)(u,v)=w_jv_ji=0, so v=0. The degree-(2r−2) tests e_j² now give u_j=0. For r=1 use e_1=1 and only position tangents. Thus dΨ_r is injective.

**Smooth local inverse and embedding.** Where ℓ separates r atoms, B=(L(ℓ^(a+b)))_(0≤a,b<r) is positive definite. Its inverse and moments through degree 2r−1 recover the degree-r monic annihilator. Its simple roots vary smoothly; Vandermonde systems recover weights and each spatial coordinate from L(x_iℓ^a), 0≤a<r. For r≥2 these have degree ≤r≤2r−1; r=1 is immediate. The formulas apply to all exact-r laws in an ambient moment neighborhood where B stays positive and the roots stay simple. They give a local smooth inverse in the subspace topology, hence an embedding onto the actual image. This is the inherited atomic-chart argument with its degree budget explicit.

Push G through Ψ_r to get a positive metric g_r on N_r=Ψ_r(Q_r). The decoded objective e_r=E∘Ψ_r^(-1) is smooth and

    Ψ_r(μ_t)'=−grad_(g_r)e_r(Ψ_r(μ_t)).                  (4)

For deg F>2r−1 this objective need not be linear in the retained entries; the recovered law supplies it. The coordinate cometric (3) appears to require moments up to degree 4r−2, but the reconstruction supplies them as smooth functions on N_r. This is exact autonomous closure on that constrained rank-r image, not all-laws truncation closure. The redundant ambient cometric matrix has rank r(d+1)−1, not full ambient rank. No unconstrained moment-space metric, unknown-rank inference, finite-sample reconstruction, stability, optimal cutoff, or algorithmic cost guarantee is asserted.

For a simple omitted-coordinate control, ½δ_(-1)+½δ_1 and ⅕δ_(-2)+⅘δ_(1/2) both have m_0=1,m_1=0,m_2=1 and rank two, but m_3=0 and −3/2 respectively. Thus even a rank-two promise does not make degree-two retention injective.

## 5. Dissipation, strictness and stationary nonminima

Every admitted trajectory satisfies

    E(t)+∫_s^t[Σ_j w_j|∇F(x_j)|²+Var_w(F(x_j))]du=E(s).

Since weights are positive, dissipation vanishes exactly when all atoms are critical points of F with the same F-value. This is grad_G E=0, and autonomous ODE uniqueness then makes the trajectory stationary. A nonstationary trajectory has E'<0 at every finite time.

An exact r=2 coercive nonminimum is

    F(x,y)=(x²−1)²+(y²−1)²,
    μ=wδ_(0,1)+(1−w)δ_(0,−1),       0<w<1.

Both gradients vanish and both energies equal 1, so μ is stationary with full rank two. Move the positions to (ε,±1), keeping their weights. Then E=(1−ε²)²<1 for 0<ε²<2. These are arbitrarily nearby distinct-atom states, so this stationary law is not even a local minimum. Global value zero is available at a mixture of (1,1) and (1,−1).

A state in Q_r is a local minimum of E if and only if every position is a local minimum of F and their F-values coincide. Necessity follows by varying one position at fixed positive mass and then varying mass between fixed positions. For sufficiency choose disjoint neighborhoods of those positions where each F≥c; nearby positive mixtures have E≥c. For r>1 such a minimum cannot be strict, because weights can vary at fixed positions. At any stationary state the second variation is Σ_j w_jv_j^T Hess F(x_j)v_j; pure-weight and mixed blocks vanish.

## 6. Boundaries, merging, and metric incompleteness

**Finite times.** If two positions met, local ODE uniqueness backwards along their existing common finite segment would identify their starting points. Formula (2) has finite integrals on every finite interval, excluding weight extinction. Thus the trajectory remains in Q_r.

**Coincident labels.** Distinctness is essential to law-level identification. At equal positions, transferring mass between positive labels has positive G-cost but zero change of law. Different velocities with zero weighted sum likewise can have zero first-order law change. Permutations do not remove these continuous redundancies.

For a coincident block define W=Σw_j, U=Σu_j and V=(Σw_jv_j)/W. Cauchy–Schwarz gives

    Σu_j²/w_j≥U²/W,       Σw_j|v_j|²≥W|V|².

The minimal cost at a specified merged tangent is attained by u_j=(w_j/W)U and v_j=V. The negative-gradient field has precisely these proportions at equal positions. Thus aggregation is dynamically consistent and internal mass ratios stay fixed; redundant initial atoms can be merged into their true-rank stratum. This does not make the unreduced metric nondegenerate on laws at a collision.

**Zero weights.** With q_j=2√w_j the weight block is Σdq_j², with Σq_j²=4, and the position block is Σ(q_j²/4)|dx_j|². At q_j=0 the position label becomes invisible and its block degenerates. The original u_j²/w_j cannot simply be evaluated there. Drop zero masses to obtain the lower-rank law and its own stratum. No smooth Riemannian structure across all ranks is asserted.

At two fixed distinct positions, weights cos²θ and sin²θ have squared speed 4 for 0<θ<π/2. Thus a zero-weight boundary is at finite length. Fixed positive weights and positions approaching collision also give finite length. Metric/geodesic completeness and forward completeness of this particular gradient field are different assertions.

**No global distance identification.** Q_1 has Euclidean intrinsic distance |x−y| between δ_x and δ_y. But the mass-one curve cos²θδ_x+sin²θδ_y, 0≤θ≤π/2, has pure-reaction action length π with the same unit-coefficient continuity/reaction action. Any distance infimizing that action over all probability paths is at most π between those endpoints. For |x−y|>π this is strictly smaller than the intrinsic Q_1 distance. Its interior has rank two, which the Q_1 distance forbids. This direct admissible-path bound needs no formula for the exact ambient distance. Equality of a fixed-path infinitesimal action, when established, does not imply equality of global endpoint distances.

## 7. Long-time information and the convex specialization

For arbitrary coercive polynomial F, all positions stay in a common compact set, the finite union of initial sublevels. Each f_j(t)=F(X_j(t)) decreases to a finite c_j and ∫_0^∞|∇F(X_j)|²<∞. The derivative of this integrand is bounded on the compact set, so it is uniformly continuous and tends to zero. Indeed otherwise positive-height spikes and uniform continuity would give disjoint intervals of fixed positive integral, contradicting integrability.

Put c*=min c_j. If c_j>c*, choose l with c_l=c*. Eventually f_j−f_l≥(c_j−c*)/2, and

    W_j/W_l=(a_j/a_l)exp(−∫_0^t(f_j−f_l))

tends exponentially to zero, hence W_j→0. It follows E(t)→c*. Every subsequential law limit is supported on critical points with F-value c*: take a subsequence where all compact positions and weights converge, discard higher-c_j zero weights, and use ∇F(X_j)→0. This does not assert c*=min F, nor require an unproved assertion that every general nonconvex particle or same-energy weight converges.

Now assume Hess F≥λI everywhere, λ>0. There is a unique minimizer x*, with F*=F(x*). Strong convexity and completing the square give F(x)−F*≤|∇F(x)|²/(2λ). Combining this with (D) gives

    0≤E(t)−F*≤exp(−2λt)(E(0)−F*).                       (5)

Strong monotonicity gives d|X_j−x*|²/dt≤−2λ|X_j−x*|², hence

    |X_j(t)−x*|≤exp(−λt)|z_j−x*|.                       (6)

Thus μ_t→δ_(x*) and all polynomial moments converge to its moments. Bound Hess F on a compact convex hull containing x* and the trajectories. Then F(X_j)−F*≤C_jexp(−2λt), so I_j=∫_0^∞(F(X_j)−F*)dt is finite and

    W_j(t)→a_j exp(−I_j)/Σ_l a_l exp(−I_l)>0.             (7)

The rank drop in the limit is therefore due to limiting collision, even though all labelled limiting masses are positive. If r>1, F* is the infimum of E on Q_r but is not attained there: r distinct points cannot all be the unique minimizer. This is compatible with finite-time constant rank. These are elementary classical strong-convexity deductions; they do not claim geodesic λ-convexity of E for G or transfer to nonconvex F.

## 8. Exact quadratic and quartic controls

For F(x)=x²/2,

    X_j(t)=z_j exp(−t),
    K_j(t)=z_j²(1−exp(−2t))/4,
    W_j(t)=a_j exp(−K_j(t))/Σ_l a_l exp(−K_l(t)).

Finite-time position differences are exp(−t)(z_i−z_j)≠0. The map is invertible by z_j=exp(t)X_j(t) and undoing the positive weight factors. Its position inverse expands errors by exp(t). Nonetheless all laws tend to δ_0, while W_j tends to normalized a_jexp(−z_j²/4). This is an exact finite-time versus limiting-information distinction, not a general conditioning theorem.

For arbitrary r the Gram determinant on {1,x,…,x^(r−1)} is

    (∏_j W_j) exp(−r(r−1)t) ∏_(i<j)(z_i−z_j)².

It is positive at finite times and tends to zero if r>1. For r=2 this is W_1W_2(z_1−z_2)²exp(−2t).

The inherited quartic control F=x⁴/4 gives X=z/√(1+2z²t) and K=z²(1−1/(1+2z²t))/8. At t>0 its spatial image is only (−1/√(2t),1/√(2t)), with inverse y/√(1−2ty²). Thus a forward transition is injective with inverse on its image, not necessarily onto all later finite laws. This qualification and control are explicitly inherited from §9.

For the quadratic control specifically, the already-existing affine/SOS theorem listed in §1 can force the law without the present path-rank promise. The general nonlinear-polynomial lift in §3 still retains that promise. The control is not evidence that initial finite rank alone suffices for arbitrary F.

## 9. What has been upgraded

Using p=F in (H) formally gives -E'=L(|∇F|²)+L(F²)−L(F)²≥0 from square positivity. That alone does not give:

1. A unique representing law at each time, with constant finite rank.
2. A smooth state manifold and positive metric, including the permutation quotient.
3. The gradient identity for every tangent variation, rather than only one scalar derivative.
4. The cometric (3), finite tensor realization (4), and conjugacy on the constrained moment image.
5. Forward completeness, no finite-time births/deaths/collisions, and injectivity.
6. The stationary criterion, stationary nonminimum, or qualified convex convergence compatible with limiting rank loss.

Items 1 and 5 are inherited reverse-lift/ODE results; the addition is their constructive integration with items 2–4 and their interaction with item 6. The Euclidean position metric is additional declared structure, not determined by the Fisher mass block. Nonlinear reparametrization requires transporting that metric rather than imposing Euclidean form again. Objective descent is numerical and criterion-relative, not simultaneous improvement of every truth-state loss. This does not authenticate any source, justify a target, identify an actual cognitive or metaphysical bearer, prove correction efficacy or warrant, establish unrestricted infinite-rank uniqueness, or provide a closure decision.

## 10. Classical source correspondence and verification

The transport/reaction geometry belongs to the Hellinger–Kantorovich / Wasserstein–Fisher–Rao literature. Liero, Mielke and Savaré, *Optimal Transport in Competition with Reaction: The Hellinger–Kantorovich Distance and Geodesic Curves* (2016), describe a dynamical Onsager operator combining transport and reaction. Their abstract/introduction were consulted for attribution; global metric results are not imported to identify our intrinsic fixed-rank distance with theirs. [Primary paper](https://doi.org/10.1137/15M1041420), [institution-hosted preprint](https://publications.imp.fu-berlin.de/2181/1/1509.00068arXiv_Liero_Mielke_Savare.pdf).

Kondratyev and Vorotnikov, *Spherical Hellinger-Kantorovich gradient flows*, arXiv:1809.03430v2, Introduction and Remark 1.1, display the formal mass-one gradient

    grad E(μ)=−div(μ∇(δE/δμ))+μ(δE/δμ−∫δE/δμ dμ).

For ∫F dμ its negative matches div(μ∇F)−(F−E)μ with the same displayed unit coefficients. Their solvability hypotheses include bounded-domain/torus density settings and strict density derivative f_u<0. Our linear potential has f_u=0 and atomic laws on R^d, so their nonlinear solvability and convergence theorems are **not** used. Their Remark 1.3 cautions that a similar-looking equation need not have an appropriate variational derivative; our finite-dimensional pairing proves that derivative directly. Naming conventions and overall metric normalization vary, so the explicit coefficients (G) govern this result. [Primary source, Remark 1.1 and surrounding assumptions](https://arxiv.org/html/1809.03430v2).

`check_exact.py` verifies metric inversion and pairing, cometric algebra, permutation invariance, Hermite tests, finite-moment Jacobian rank, the omitted-coordinate control, stationary nonminimum and collision-kernel controls, square-root/finite-length identities, and quadratic/quartic trajectory, weight, dissipation and Gram determinants. Finite tests supplement the universal proofs rather than establish them by enumeration. `author-run/EXACT_CHECKS.json` records the author execution. Copied ancestry inputs are checked on every run; an optional original-root check verifies the inspected predecessors remain unchanged. Independent review and preservation, if supplied later, are separate.
