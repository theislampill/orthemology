# A discrete realizability gap and an exact rational particle repair

10 October 2026 UTC. Additive ordinary mathematical research within ACTIVE T20. The parent proposed the Dirac test, finite-atom extension, rational reweighting and quartic guard and participated in the derivation. This author packet is not independent review. No protected edit, integration, formal-kernel certification, historical priority, actual DAEE implementation defect, empirical/noetic identification, or programme closure is asserted.

## 1. Increment and inherited scope

For the polynomial hierarchy

    L'(p)=L(b·∇p)−L(Fp)+L(F)L(p),       b=−∇F,

the predecessors establish continuous-time law realizability and finite-atomic gradient geometry under their respective hypotheses. Those results do not make raw forward Euler of every moment realizable. In fact, at any finite positive atomic law with at least one moving atom, **every positive Euler step fails full square positivity**. A Dirac already detects the failure with a quadratic square.

A constructive alternative moves the particles, reweights them by positive decreasing functions of the new potential values, and recomputes moments. The rational reweight below makes this entire operation exactly rational for rational polynomial data. It preserves a positive law at every step, decreases the potential under an explicit transport-step condition, preserves rank under an injectivity condition, and has the correct first-order hierarchy. These are one-step structural statements, not global numerical-convergence results.

`INPUT_BINDINGS.json` binds unchanged copies of the three directly read ancestors:

- `joint-atomic-gradient-lift-20261010/RESULT.md` owns the genuine metric and continuous equations x'_i=−∇F(x_i), w'_i=−w_i(F_i−E), together with the full-rank and finite-chart qualifications.
- `radial-quartic-gradient-reverse-lift-20261010/RESULT.md` owns the unrestricted-rank reverse lift for F=|x|⁴/4, the exact continuous characteristics and their range. Its full square positivity is a path hypothesis, not a discrete preservation theorem.
- `two-atom-moving-moment-chart-20261010/RESULT.md` owns the open rank-two chart in the first three moments. Euler in that chart followed by law reconstruction is a different method from Euler of every moment.

`DEDUP.json` records a bounded search of 1,082 top-level packet Markdown/Python files. No prior instance of this raw-Euler obstruction or this particle-step repair was located. This is local deduplication, not an exhaustive history or literature search. Positive tilting, gradient descent and Hermite interpolation are inherited/classical mechanisms; the contribution is this explicit discrete fidelity application and its exact controls.

## 2. The Dirac obstruction is exact and has no positive threshold

Let L(p)=p(x), b=b(x)≠0, and define the raw Euler functional

    Λ_τ(p)=L(p)+τ[L(b·∇p)−L(Fp)+L(F)L(p)],   τ>0.

The selection terms cancel at a Dirac, so Λ_τ(p)=p(x)+τ b·∇p(x). In one dimension,

    m₀⁺=1,  m₁⁺=x+τb,  m₂⁺=x²+2τxb,
    m₂⁺−(m₁⁺)²=−τ²b²<0.

In any dimension the second-moment covariance matrix is −τ²bbᵀ. Equivalently, for the polynomial

    q(y)=b·(y−x)−τ|b|²,

q(x)=−τ|b|² and ∇q=b, hence

    Λ_τ(q²)=τ²|b|⁴−2τ²|b|⁴=−τ²|b|⁴<0.

No nonnegative representing measure exists. Reducing τ only reduces the size of the negative certificate; it never changes its sign. The exact moved Dirac δ_(x+τb) instead contributes the missing τ²bbᵀ to its second moment and has zero covariance. This explains how a locally first-order accurate tangent step can leave the curved moment image.

For F(x)=x⁴/4, x=1 and τ=1/4, raw Euler gives m₁=3/4, m₂=1/2 and variance −1/16. It even gives Λ_τ(F)=0<F(1)=1/4. Thus a decreased scalar potential is not a realizability certificate. The correctly moved Dirac has m₂=9/16 and F(3/4)=81/1024. This illustrative τ is not asserted to pass the more conservative executable guard in §6.

## 3. Every moving finite atomic law has the same full-hierarchy failure

First merge repeated positions and drop zero masses. Write μ=Σ_(i=1)^r w_iδ_(x_i), with distinct x_i, w_i>0, Σw_i=1, F_i=F(x_i), b_i=−∇F(x_i), E=Σw_iF_i, and A_i=1−τ(F_i−E). Then

    Λ_τ(p)=Σ_i w_i[A_i p(x_i)+τ b_i·∇p(x_i)].

Suppose b_j≠0. Choose a linear form ℓ separating the finite support and put

    e_j(y)=∏_(i≠j) [ℓ(y)−ℓ(x_i)]/[ℓ(x_j)−ℓ(x_i)],
    a_j=∇e_j(x_j),
    q(y)=e_j(y)²[1−(2a_j+C b_j)·(y−x_j)].

At x_j, q=1 and ∇q=−C b_j. At every other support point both q and ∇q vanish because of the squared Lagrange factor. Its degree is at most 2r−1, including r=1. Choose

    C=(|A_j|+1)/(2τ|b_j|²).

Then

    Λ_τ(q²)=w_j[A_j−2τC|b_j|²]
            =w_j[A_j−|A_j|−1]<0.

Thus every τ>0 fails full square positivity whenever at least one atom moves. A truncation containing this witness needs moments only through degree 4r−2; smaller truncations need not expose it. For rational polynomial data and rational τ, a rational separating ℓ exists and this witness can be constructed rationally.

For completeness, if all b_i=0, Λ_τ is the signed atomic functional Σw_iA_i ev_(x_i). It is square-positive exactly when all A_i≥0. Necessity follows by evaluating e_i², and sufficiency follows directly from nonnegative masses. Its mass is one because Σw_iA_i=1. This includes stationary equal-energy states, where Euler does nothing, and pure-selection steps that remain positive for sufficiently small τ. The result does not say every Euler scheme fails on every state.

In particular, the rank-two chart in the third ancestor is open in its three retained coordinates. A small Euler step in those coordinates may remain there and reconstruct a valid two-atom law. Recomputed higher moments then generally differ from their raw Euler values. Our obstruction does not identify that different, chart-reconstructed method with full-hierarchy Euler, and diagnoses no inspected implementation.

## 4. A law-valued split step with two positive reweight options

From a supplied finite positive law, choose τ>0 and set

    y_i=x_i−τ∇F(x_i),     f_i=F(y_i),     c=min_i f_i.

The primary exact-rational rule is

    d_i=1+τ(f_i−c),     a_i=1/d_i,
    Z=Σ_i w_i a_i,      v_i=w_i a_i/Z,
    μ⁺=Σ_i v_iδ_(y_i),  L⁺(p)=Σ_i v_i p(y_i).          (R)

Since d_i≥1, all factors, Z and v_i are strictly positive, and Σv_i=1. Thus L⁺ is square-positive on **all** polynomials by construction, with no step restriction for this positivity assertion. Collisions can lower the true rank, but cannot invalidate the law. Repeated labels at the same point receive the same factor and can be aggregated before or after the step with identical results.

The exact-real exponential alternative replaces a_i with exp(−τf_i). It has the same positivity and the same first-order field. It is the exact fixed-position replicator substep after the explicit position step, not the exact combined continuous flow. Rule (R) is a rational approximation to that selection substep; it is not an exact replicator solution. The exponential option is not used for the executable rational controls.

Both rules are invariant under adding a constant to F: the gradient is unchanged; (R) uses differences from c; exponential factors acquire one common multiplier that normalization removes. The minimum shift is chosen to guarantee positive rational denominators even when F takes negative values.

### Potential descent, with an actual-segment hypothesis

Assume F is C² near each segment [x_i,y_i] and, on each such segment,

    Hess F(z) ≤ L_i I,       L_i≥0,       τL_i≤2.

Taylor's formula with integral remainder gives

    F(y_i)≤F(x_i)−τ(1−τL_i/2)|∇F(x_i)|².

A Hessian value only at x_i is not this bound. A bound on a region not containing the actual segments is also insufficient. Averaging with the unchanged old weights proves E_transport=Σw_i f_i≤E_old.

For either reweight rule, a_i is decreasing in f_i. The pairwise covariance identity yields

    E_new−E_transport
      =[Σ_i w_i f_i a_i−(Σ_i w_i f_i)(Σ_i w_i a_i)]/Z
      =(1/(2Z))Σ_(i,j)w_iw_j(f_i−f_j)(a_i−a_j)≤0.

For (R) this is the exact rational identity

    E_new−E_transport
      =−(τ/Z)Σ_(i<j) w_iw_j(f_i−f_j)²/(d_i d_j).       (D)

For τ>0 and positive weights, the selection stage is strictly decreasing exactly when not all f_i agree. The transport stage is strictly decreasing if some nonzero gradient has τL_i<2. Combining the two stages proves the stated descent, but gives no guarantee of a global minimizer for nonconvex F.

### No collisions under an injectivity bound

Let C be a convex region containing the starting positions, with F C² near C and Hess F≤L I there, L≥0. For x,z∈C and T(x)=x−τ∇F(x),

    [T(x)−T(z)]·(x−z)≥(1−τL)|x−z|².

This follows by integrating the Hessian along [x,z]. Therefore τL<1 implies

    |T(x)−T(z)|≥(1−τL)|x−z|,

so distinct atoms remain distinct. An operator-norm Hessian bound is a sufficient stronger hypothesis; the upper quadratic-form bound already suffices. If the same C also contains the transport segments, one common bound proves descent and injectivity. Otherwise the segment and chord hypotheses must be checked separately.

When one common region contains the transport segments and τL<1, total potential equality occurs exactly when all gradients vanish and all occupied potential values agree. These are exactly the inherited continuous stationary states, and exactly the fixed points of either split step under these conditions. This does not make every stationary state a global or local minimum.

With distinct output positions and strictly positive weights, full Hankel rank remains r by the inherited finite-support interpolation fact. For a fixed known τ, potential F and reweighting rule, on the declared injective domain the entire law update is injective on its actual range: invert T on the output support, then recover old weights for (R) as

    w_i=v_i d_i / Σ_j v_j d_j.

The d_i are known from the output support and τ. The exponential counterpart multiplies by exp(τf_i). This is an inverse-on-range statement, with no global surjectivity, efficient inverse, conditioning or stability assertion. It does not compare runs using different state-dependent choices of τ.

## 5. First-order consistency, with the test and initial law fixed

Fix a finite law and a polynomial p. For τ↓0, finite-dimensional Taylor expansion gives

    p(y_i)=p(x_i)+τb_i·∇p(x_i)+O(τ²),
    f_i=F_i+O(τ),     c=min_i F_i+O(τ).

The minimum estimate uses |min u_i−min v_i|≤max_i|u_i−v_i|, so no differentiability of a tied minimum is assumed. If c₀=min F_i, then

    a_i=1−τ(F_i−c₀)+O(τ²),
    Z=1−τ(E−c₀)+O(τ²),
    v_i=w_i−τw_i(F_i−E)+O(τ²).

The c₀ terms cancel. Exponential factors give the same normalized expansion. Hence for either rule

    L⁺(p)=L(p)+τ[L(b·∇p)−L(Fp)+L(F)L(p)]+O(τ²).

Equivalently the position and weight coordinates have the first-order vector field of the inherited atomic gradient metric. For F polynomial the local exact atomic ODE is smooth, so the coordinate one-step local error is O(τ²). No uniform remainder over all polynomial degrees, all initial laws, all times or an unbounded state region is claimed. This is consistency/local error, not a proved global error bound or convergence theorem for iterated numerical trajectories.

## 6. A fully rational, explicitly guarded quartic instance

For the exact normalization F(x)=x⁴/4 and b(x)=−x³, let M=max_i|x_i|. If M>0 use a rational step

    0<τ≤1/(6M²).

On [−M,M], Hess F=3x²≤3M²=L, so τL≤1/2. Also

    y=x(1−τx²),       5/6≤1−τx²≤1.

Thus each transport segment stays in [−M,M], |y|≤|x|, and T'(x)=1−3τx²≥1/2. The same explicit region proves descent and no collision. Formula (R) and every recomputed polynomial moment are rational for rational positive weights, rational positions, rational τ and rational test coefficients. No exponential evaluation, irrational atom reconstruction, rounding tolerance or unproved Hessian oracle is needed for this instance. If M=0, the merged law is δ₀ and the step is stationary for every positive τ.

`quartic_rational_step` in the verifier implements this guard with exact fractions and rejects floats, nonpositive/non-normalized weights, nonpositive τ and guard violations. It merges duplicate input positions and retains τ, the potential/rule identifiers and the certified interval as transition metadata. The guard is sufficient, not necessary; rejection does not prove the underlying step is invalid. Exact arithmetic avoids floating-point underflow in these controls, but no bit-complexity or large-scale efficiency claim is made.

The executable controls include the rational law (1/3)δ_(-1)+(2/3)δ_2 with τ=1/24 and a three-atom example, checking positive normalization, separate-stage descent, inverse weight recovery, a positive Gram factorization and preserved rank. A large-step quartic countercontrol remains a positive Dirac while increasing F, and a quadratic step at τL=1 collapses distinct atoms while remaining a positive law. These distinguish unconditional realizability from conditional descent and rank retention.

## 7. Literature boundary and evidence

Vikas, Wang, Passalacqua and Fox, *Development of High-Order Realizable Finite-Volume Schemes for Quadrature-Based Moment Method* (AIAA 2010-1080), abstract and §§2.5–2.5.1, were inspected. Their realizability mechanism uses a nonnegative effective velocity distribution for a spatial finite-volume scheme. That scheme and its step conditions are not the present raw derivative-of-evaluation update. [Primary PDF](https://cfd.ku.edu/papers/AIAA-2010-1080.pdf).

Chu, Endeve, Hauck and Mezzacappa, *Realizability-Preserving DG-IMEX Method for the Two-Moment Model of Fermion Transport* (2018), abstract only, was inspected. Its claim combines a model-specific closure, limiter, CFL condition and IMEX stages for a bounded fermion distribution. We do not transfer its guarantees here. In particular a convex-combination/SSP argument relying on a realizable forward-Euler base has no positive base-step threshold supplied by our moving finite-atom hierarchy. This is not an impossibility theorem for all higher-order methods or all SSP formulations. [Primary record](https://arxiv.org/abs/1809.06949).

`check_exact.py` uses exact rational arithmetic and symbolic polynomial identities, with no floating-point controls. It verifies both the Dirac and explicit Hermite witnesses, the positive rational repair, minimum-tie cases, stage dissipation, constant-shift invariance, exact inverse weights, local consistency and step-condition countercontrols. It checks copied input hashes and optionally unchanged original inputs. Finite checks supplement the written universal proofs; they do not establish them by enumeration or in a formal kernel. `author-run/EXACT_CHECKS.json` records author execution; review and preservation, if supplied, remain separate.

Replay with Python 3 and SymPy:

    python check_exact.py --output-dir /a/fresh/output/directory

Use `--original-root /path/to/workspace` to additionally verify the three original reports. The output directory must not already exist. All files created by this packet are additive.
