# A second-order whole grouped correction with positive laws, descent, and exact source-audit covariance

11 October 2026 UTC. Additive research after the frozen consolidation cutoff. Source files, frozen v2, and intermediate v3 are unchanged. This is an author derivation with executable controls, not independent review, a formal-kernel proof, production integration, an R3 recovery, or a programme-closure decision. Actual run timestamps are in the receipts; no retrospective research-duration claim is made.

## Result and why this gap was selected

The inherited fixed-group classification supplies the whole gradient system, but its numerical corollary only supplies arbitrary internal descent maps and optional first-order consistency. The fixed-loss arbitrary-order packet expressly excludes the order of moving positions. Recovered Pro I–L similarly leaves convergence order open. The interface left unestablished in these inspected bodies is therefore **a whole moving-state update that satisfies the actual grouped audit contract**, rather than another fixed-loss rational approximation.

The construction below meets that interface. It advances each group's complete internal state by an executable second-order energy-descending method, then reweights group masses using the **average of the old and new group losses**. Positive reciprocal quadratic factors suffice. The key exact identity is

    E_new − E_old
      = Σ_g (m'_g−m_g)(V_g+V'_g)/2
        + Σ_g (m'_g+m_g)(V'_g−V_g)/2 ≤ 0.                 (A)

The first term is a covariance descent; the second is nonpositive group by group. Trapezoidal accumulation of the changing loss gives second order for the entire joint flow. Using only the new losses, even after a second-order position solve, generally drops the mass update to first order. This is proved by an exact quadratic control and observed in the nonlinear grouped benchmark.

The construction is not an exact-flow oracle: a general finite-dimensional discrete-gradient equation, its explicit local contraction bounds and residual requirements are given below; a quartic specialization has a finite exact-rational bisection algorithm; and a genuinely grouped nonlinear example reduces its internal solve to a uniquely bracketed scalar equation. In the grouped example the conditional weights, all positions, and the group masses move.

### Inherited versus added

- The metric, energy classification E=C+Σ m_g V_g, grouped flow, audit action, and source-provenance guards are inherited from `grouped-source-audit-gradient-20261011` and recovered Pro I/J. The fixed-partition theorem is not reproved or renamed here.
- Positive law reconstruction, decreasing-factor covariance descent, the rational first-order repair, and its realizability/rank distinction belong to `gradient-discretization-fidelity-20261010`, Pro K, and their reviewers.
- Reciprocal Taylor P₂ positivity and scalar second-order accuracy are inherited from `positive-high-order-correction-20261011`; this report does not claim them as new.
- The Gonzalez midpoint discrete gradient, symmetric consistency, implicit solution issues, and dissipative use are classical. Gonzalez's 1996 paper, §§3.2–3.4, especially formula (3.7), is the direct source for the discrete-gradient formula used here. [Author-hosted primary paper](https://web.ma.utexas.edu/users/og/PUBLICATIONS/paper_DisHamSys.pdf). Dissipative Riemannian discrete gradients are already treated in the 2018 paper, §3 and Proposition 1. [Primary paper](https://arxiv.org/pdf/1804.08104). General discrete-gradient existence and implementation require hypotheses; they are not automatically supplied by an energy identity. [Primary analysis](https://arxiv.org/html/1805.06444v3).
- Symmetric splitting would give another classical route using suitable substeps; Strang's construction is established ancestry, not a new numerical discovery. [Original article](https://epubs.siam.org/doi/10.1137/0705041). The chosen endpoint-average coupling uses one complete internal update and does not require a Strang exact-flow oracle.
- The added project interface is the joined endpoint-average coupling, explicit whole-state order/descent/audit proof, executable qualifications, and the distinction between moving-law coordinate/W₁ accuracy and fixed-support TV accuracy. No field-priority claim is made. The exact product identity itself is elementary.

`SOURCE_BINDINGS.json` records exact byte bindings and honest read scopes. `OVERLAP_SCAN.json` records a bounded substring scan of all 44 geometry-register sources, separately from substantive reading. No hit for the listed numerical-method terms occurred; this does not establish exhaustive corpus or literature novelty. The inaccessible reported R3 contributes no proof or implementation here.

**Reported successor and priority qualification.** The user-supplied Pro continuation reported a second-order construction preserving laws, descent, and audit commutation, but its exact R3 proof and implementation remain unrecovered. That report may overlap with the present whole-state construction; the extent of overlap and priority within T20 are unknown. This packet establishes an inspectable result from the available source owners and its own derivation. It does not establish that it is the first T20 result with those properties, nor treat the absent R3 body as a verified proof or as evidence that no such result existed.

## 1. Exact inherited domain and target equation

Fix finite retained origin labels partitioned into nonempty groups I_g, g=1,…,G, and α>0. Every token weight is positive. Write

    w_i=m_g r_i,    Σ_g m_g=1,    Σ_(i∈I_g) r_i=1.

Each position x_i lies in a connected open Euclidean domain X_i. Keep the labels and the partition; do not merge coincident positions. The inherited metric and permitted energy are

    g=(1/α)Σ_g dm_g²/m_g + Σ_g m_g h_g,
    h_g=(1/α)Σ_(i∈I_g) dr_i²/r_i + Σ_(i∈I_g) r_i |dx_i|²,
    E=C+Σ_g m_g V_g(r_g,x_g).                              (1)

A positive group audit multiplies all labels in I_g by a_g>0:

    T_a(m,r,x)=(B_a m,r,x),    (B_a m)_g=a_g m_g/Σ_k a_k m_k.

The objective, grouping, metric rule, retained catalogue, external time schedule if present, and algorithmic choices are unchanged by that audit. The exact autonomous negative gradient is

    ydot_g=−grad_(h_g)V_g(y_g),
    mdot_g=−α m_g[V_g(y_g)−Σ_k m_k V_k(y_k)],              (2)

where y_g=(r_g,x_g). Internal dynamics are independent of group masses; conditional weights may evolve nonlinearly and positions within the group may interact. An arbitrary finer token audit does not have this property.

### Positive coordinates without a positivity projection

Within a group with k labels choose one fixed reference label k and set

    q_i=log(r_i/r_k),  i<k,
    r_i=exp(q_i)/(1+Σ_(j<k)exp(q_j)),
    r_k=1/(1+Σ_(j<k)exp(q_j)).

For k=1 there is no q coordinate. Let u_g=(q_g,x_g) and φ_g(u_g)=V_g(r(q_g),x_g). The internal equation becomes

    udot_g=f_g(u_g)=−K_g(u_g) ∇φ_g(u_g),                 (3)

where the block-diagonal positive mobility is

    K_q=α[diag(1/r_1,…,1/r_(k−1))+(1/r_k)11ᵀ],
    K_x=diag_i((1/r_i)I_(dim X_i)).                       (4)

Indeed the Fisher metric in q coordinates is (1/α)[diag(r̂)−r̂r̂ᵀ]; its inverse is (4). Position and conditional coordinates have no cross metric block. Every finite q gives strictly positive conditional weights. The chart is R^(k−1)×∏X_i; it does not include zero conditional weights. Mobility can diverge as a conditional weight approaches zero.

The fixed reference label and coordinate units are part of the method. General discrete-gradient schemes can depend on this chart; no coordinate-free or arbitrary relabelling invariance is asserted. The source-audit action leaves the chart coordinates unchanged, which is the symmetry required here.

## 2. One executable whole-state step

Fix h>0. Choose internal maps u'_g=U_(g,h)(u_g), independently of all group masses, with

    φ_g(u'_g)≤φ_g(u_g),
    U_(g,h)(u)=u+h f_g(u)+(h²/2) Df_g(u)f_g(u)+O(h³)     (5)

uniformly on the specified compact interior region. Section 3 gives actual such maps and solver conditions, rather than leaving (5) as an oracle.

Set

    v_g=φ_g(u_g),       v'_g=φ_g(u'_g),
    c_g=(v_g+v'_g)/2,  b=min_(all retained g) c_g,
    z_g=αh(c_g−b),
    A_g=1/P₂(z_g),      P₂(z)=1+z+z²/2,
    m'_g=m_g A_g/Σ_k m_k A_k,
    w'_i=m'_g r_i(u'_g),    i∈I_g.                       (6)

An equally valid variant uses A_g=exp(−αh c_g), evaluated after subtracting any common baseline for numerical stability. It is an explicit scalar operation, not a request for the exact joint flow. Both variants are used in the controls.

### Positive law and exact audit square

Finite c and h imply 0<A_g≤1 in the rational variant, and A_g>0 in the exponential variant. The normalizer is finite and positive. Thus m', r', and every w'_i are positive and normalized. The reconstructed law

    μ'=Σ_i w'_i δ_(x'_i)

is a genuine probability on the declared common measurable position carrier. For the polynomial and Wasserstein statements below, assume all X_i lie in one R^d. If positions have different types or dimensions, retain the declared tagged carrier and use the coordinate statements unless an observation map and metric have been supplied. In the common Euclidean case all polynomial square tests are nonnegative by representation. Positions are in their declared domains because the internal solver enforces that condition. Distinctness of positions is not implied.

An audit changes only m. The same internal iterates, losses, baseline, factors, and selected h are obtained. Therefore

    U_h(T_a z)=T_a(U_h z)                                (7)

by commutation of positive diagonal reweightings. This statement includes solver branch selection, error tolerances, acceptance tests, precision choices if they affect the mathematical map, and any adaptive grid: they must be invariant under the admitted audit. They may depend on any retained internal state and on external time. A mass-weighted global error or energy line search need not be invariant.

### Whole-energy descent and strictness

Let d_g=v'_g−v_g≤0. The elementary discrete product identity gives exactly

    E'−E=(m'−m)·c + (m'+m)·d/2.

Because A_g is a strictly decreasing function of c_g for h>0,

    (m'−m)·c=Cov_m(c,A)/E_m A
      =[1/(2E_m A)]Σ_(g,k) m_gm_k(c_g−c_k)(A_g−A_k)≤0.  (8)

The second term is nonpositive separately in each group. This proves (A) without requiring the ordering of the *final* losses to match the ordering of their averages. It also shows that any θ-convex endpoint average c=(1−θ)v+θv', 0≤θ≤1, would give descent by a corresponding product identity. The midpoint θ=1/2 is what supplies second-order accumulated loss in general.

For P₂ the reaction term can be written without a covariance shorthand. With P_g=P₂(z_g) and Z=Σm_g/P_g, it equals

    −(αh/Z) Σ_(g<k) m_gm_k(c_g−c_k)²
             [1+(z_g+z_k)/2]/(P_gP_k).

Every multiplier is nonnegative, supplying a fully explicit rational dissipation term alongside the internal losses.

For an exactly solved positive-mobility discrete-gradient internal step on the certified local branch, or with an explicit verified stationary-input zero-increment rule, equality holds iff every internal gradient vanishes and every group loss agrees. Those are exactly the stationary states of (2). In fact internal zero loss change forces the discrete gradient, hence the increment, to vanish; covariance equality forces common c. The converse uses the stated branch selection. Approximate solves retain the advertised inequality only under the extra checks in §3; no exact equality classification is exported to arbitrary rounded iterates.

For the exponential variant there is a stronger exact accounting identity. Put

    J(m',m)=KL(m'||m)+KL(m||m').

Since log(m'_g/m_g)=−αh c_g−log Z,

    (m'−m)·c=−J(m',m)/(αh).                              (9)

Together with the internal discrete-gradient identity below, this is an explicit reaction-plus-internal dissipation budget for the complete numerical transition.

## 3. Actual internal method, local existence, and finite-solver requirements

Assume φ∈C³ and K∈C², positive definite, on the chart neighborhood. Put δ=v−u and a=(u+v)/2. The classical Gonzalez discrete gradient is

    Dφ(u,v)=∇φ(a)
       + [φ(v)−φ(u)−∇φ(a)·δ] δ/|δ|²,   δ≠0,
    Dφ(u,u)=∇φ(u).                                      (10)

It obeys Dφ(u,v)·(v−u)=φ(v)−φ(u) and is symmetric in its two arguments. Solve

    δ=−h K(u+δ/2) Dφ(u,u+δ).                            (11)

This is a finite-dimensional equation using values and first derivatives of φ and values of K. No flow evaluation or time integral occurs in the update. Any solution with its segment in the chart satisfies

    φ(u+δ)−φ(u)=−h DφᵀK(u+δ/2)Dφ≤0.                    (12)

For (6) using this exact solve, the exponential whole-energy identity becomes

    E'−E=−J(m',m)/(αh)
           −(h/2)Σ_g (m'_g+m_g) Dφ_gᵀK_g Dφ_g.         (13)

Unrestricted nonlinear equations need not have a unique acceptable root for an arbitrarily large step. Energy dissipation conditional on a root is not an all-step existence theorem.

An independent reader identified a sharp branch guard: for φ(x)=−x²/2, K=1, u=0, h=2, every v solves (11). Choosing v≠0 strictly lowers the energy from a stationary input. Thus arbitrary large-step root choice does not preserve stationary states, despite satisfying (12). The certified local branch, or the explicit stationary-input rule, is essential to the preceding equality characterization. This correction does not affect the descent inequality or the local-order proof.

### An explicit local contraction certificate

Choose R>0 with the closed ball B(u,R) lying inside the chart. Bound on that ball

    |∇φ|≤M₁,   ||∇²φ||≤M₂,   ||∇³φ||≤M₃,
    ||K||≤K₀,  ||DK||≤K₁.

All norms are Euclidean/operator norms, with the third derivative viewed as a trilinear form. Set

    D₀=M₁+M₃R²/24,
    L_D=M₂/2+M₃R/6,
    Q_h=h[(K₁/2)D₀+K₀ L_D].

The sufficient conditions

    h K₀D₀≤R,      Q_h<1                               (14)

make the right side of (11) a contraction of the closed increment ball |δ|≤R into itself. Therefore it has exactly one root there and Picard iteration from δ₀=0 converges to that root. Other roots outside the certified ball are irrelevant to this selected local branch.

For completeness, if e(δ)=φ(u+δ)−φ(u)−∇φ(u+δ/2)·δ, midpoint cancellation and the third-derivative bound give

    |e(δ)|≤M₃|δ|³/24,
    |∇_δe(δ)|≤M₃|δ|²/8.

The operator derivative of δ/|δ|² has norm 1/|δ|². Thus the correction in (10) has derivative norm at most M₃|δ|/6, including its zero derivative at δ=0. This proves the displayed D₀ and L_D bounds and then (14). The existence argument is constructive once these bounds and function evaluations are supplied; an abstract C³ hypothesis does not itself compute them.

### Order of the internal solve

Formula (10) gives Dφ(u,u+δ)=∇φ(u+δ/2)+O(|δ|²). On the local branch δ=O(h), (11) therefore reads

    δ=h f(u+δ/2)+O(h³)
      =h f(u)+(h/2)Df(u)δ+O(h³).

Substitution yields δ=h f(u)+(h²/2)Df(u)f(u)+O(h³), which is (5). The remainder and local stability are uniform on any compact interior region with the stipulated bounds. This is a direct order argument; no order conclusion is inferred merely from energy descent.

### Finite nonlinear solves must satisfy two obligations

Let a computed increment have residual

    ρ=δ+h K(u+δ/2)Dφ(u,u+δ).

On the contraction ball,

    |δ−δ_exact|≤|ρ|/(1−Q_h).                            (15)

A uniform O(h³) increment error preserves whole-system second order. Separately, exact descent is retained if

    Dφ·ρ≤θ h DφᵀK Dφ,       0≤θ<1,                     (16)

or if a validated direct test establishes φ(u+δ)≤φ(u). The sufficient norm form |ρ|≤θ h λ_min(K)|Dφ| also gives (16). An absolute residual tolerance alone need not certify descent near a stationary point. At a verified stationary input the zero increment is the exact solution. Approximate evaluation must not falsely certify that condition.

The solve, its bounds, and the descent acceptance test use internal quantities, so they can preserve (7). A criterion weighted by the audited masses generally cannot. Exact rational arithmetic is used in the quartic implementation below; the transcendental benchmark uses high-precision arithmetic and explicitly reports residuals. Its numerical checks are not interval-certified real-arithmetic equalities. Floating-point underflow can destroy literal positivity; log-domain normalization, adequate precision, or exact/validated arithmetic is an implementation obligation, not a consequence of (6).

## 4. Second order for the whole joint flow

Assume first that the autonomous exact solution and its nearby numerical states lie in a fixed compact interior chart region over 0≤t≤T. There all derivatives and local Lipschitz constants needed above are bounded. Assume the local internal branch is used, with exact solves or uniformly O(h³) endpoint perturbations satisfying descent separately.

The exact mass solution along the independent internal trajectories is

    m_g(h) ∝ m_g(0) exp[−α∫₀ʰ φ_g(u_g(s)) ds].           (17)

For an internal second-order endpoint, smoothness and the trapezoidal error give

    h c_g = ∫₀ʰ φ_g(u_g(s)) ds + O(h³).                  (18)

In the exponential variant, (18) immediately gives local O(h³) in all mass coordinates. In the P₂ variant,

    log P₂(z)=z−z³/6+O(z⁴),
    log A_g=−αh(c_g−b)+O(h³).                           (19)

The common baseline cancels from the mass log-odds. On the compact region c_g−b is uniformly bounded, so the O(h³) estimate is uniform, including tied or switching minima. Only the Lipschitz estimate |min c−min c̃|≤max|c−c̃| is needed; differentiability of the minimum is not assumed. Normalization is smooth with a positive denominator. Thus the **entire** step in (u,m), and hence in (r,x,w), has local error O(h³).

The exact local internal branch and mass update have Lipschitz constant 1+Ch on a compact neighborhood. The usual error recurrence gives

    max_(t_n≤T) |z_n−z(t_n)| ≤ C_T Σ_j h_j³
                             ≤ C_T T (max_j h_j)².      (20)

Here the final time and compact-region constants are fixed. For inexact internal solves use stability of the exact map and add their uniform O(h_j³) endpoint perturbations to the recurrence; the finite-solver map need not itself be differentiable. A prescribed mesh or an audit-invariant adaptive mesh works. Adaptive meshes are compared at the same actual accumulated times. An unbounded number of steps with finite total time does not prove continuation past that time.

Replacing P₂ by P_p with p>2 does not raise the whole method's order: the internal update and trapezoidal quadrature still have generally nonzero cubic local errors. A single atom with V=x²/2 already has midpoint multiplier

    (1−h/2)/(1+h/2) = exp(−h)−h³/12+O(h⁴).

There is no mass-selection error to hide the second-order limitation.

### A useful autonomous continuation condition

There is a concrete sufficient way to discharge the compactness premise. For each group assume its initial sublevel

    {u_g : φ_g(u_g)≤φ_g(u_g(0))}

is a compact subset of its chart. Exact internal descent and the checked numerical descent keep every u_g in this set. Use a compact neighborhood inside the chart to get a common positive contraction step threshold. The exact internal ODE is also forward complete under these hypotheses.

Let all encountered group losses lie in [L,U], M=U−L. For P₂, 1≤P₂(z)≤exp z for z≥0. Every unnormalized one-step mass factor consequently lies in [exp(−αhM),1]. Cancellation of intermediate normalizers gives, at any finite total time t_n,

    m_g^n ≥ m_g^0 exp(−αM t_n)>0.                        (21)

The same estimate holds for the exponential variant after subtracting b. This supplies a real finite-horizon interior control, invariant under every positive group audit apart from its explicitly changed initial mass. It is stronger than asserting that a decreasing *weighted* energy alone confines all groups; a small group mass could otherwise hide a large internal loss.

These conditions are sufficient, not necessary. The grouped benchmark below has an unconstrained common-translation coordinate but still admits a direct finite-horizon bound. In general descent cannot replace domain control: x'=−1 for V(x)=x on X=(0,1) reaches the excluded boundary in finite time while its loss decreases.

## 5. Executable instances and exact countercontrols

### Finite rational quartic algorithm, without a root oracle

For a singleton group with V(x)=x⁴/4 and K=1, (11) is the scalar equation

    F(v)=v−u+(h/4)(v³+v²u+vu²+u³)=0.

Its derivative is

    F'(v)=1+(h/4)(3v²+2uv+u²)≥1.

For u>0, F(−u)=−2u<0 and F(u)=h u³>0, so the unique root lies in [−u,u]. Negative u is handled by odd symmetry; u=0 is stationary. Consequently every midpoint in the maintained bracket satisfies |v|≤|u| and hence V(v)≤V(u).

`quartic_internal` uses exact fractions and bisection in v/u∈[−1,1]. It stops when the physical bracket width is at most h³/100. The returned midpoint has a certified root error at most h³/200, and endpoint descent holds independently of the stopping accuracy. With rational inputs, the endpoint-average losses, P₂ factors, normalized weights, and every recomputed polynomial moment are rational. This is a finite algorithm for each positive rational h, including large h; no Newton success flag, transcendental evaluation, or exact implicit-root oracle is required. Small h supplies the order statement, not a claim of large-step accuracy or good bit complexity.

The exact-fraction controls use three particles, nontrivial audits, and both quadratic and quartic internal maps. They check the complete audit square, energy descent, positivity/normalization, finite root-error brackets, and representative polynomial squares. The universal square-positivity claim comes from the actual positive-law representation, not from the finite list of tests.

A further exact-rational control exercises the genuinely multidimensional Gonzalez correction: φ(u)=|u|⁴/4 in R², K=I, u=(1,1/2), R=1/2, h=1/32. On the certified ball, |u|≤2 gives M₁=8, M₂=12, M₃=12, K₀=1, K₁=0, so hK₀D₀=65/256≤1/2 and Q_h=7/32<1. For midpoint a and increment δ the discrete gradient simplifies exactly to |a|²a+(a·δ)δ/4. The finite Picard run checks its exact chain identity, remains in the certified ball, and checks both residual accuracy and the relative descent condition (16), with θ=1/2. This tests the general local-solver construction beyond scalar secant formulas.

### Whole-order negative control with a second-order position map

Take two singleton groups, α=1, initial weights (1/2,1/2), positions (1,0), and V(x)=x²/2. Set γ=(1−h/2)/(1+h/2). The exact first mass at time h is

    m_exact(h)=1/[1+exp((1−exp(−2h))/4)].

Our endpoint-average P₂ update uses c₁=(1+γ²)/4, c₂=0 and has

    m_average(h)−m_exact(h)=−7h³/192+O(h⁴).

If instead one uses the final loss alone, c₁=γ²/2, the error is

    m_final_only(h)−m_exact(h)=h²/8+O(h³).

Thus a second-order state solve plus a second-order *frozen-loss* selection formula does not by itself integrate the joint flow at second order. The loss must be accumulated with appropriate time accuracy. Both formulas remain positive and descending; those properties do not diagnose the order loss.

A separate exact rational control chooses h=m₁/2. An audit a=(2,1) changes h from 1/4 to 1/3 and changes the corrected position from 7/9 to 5/7. A weight-only audit of the already updated state cannot produce that change. Audit-invariant step selection is essential even with the improved formula.

### Genuinely grouped nonlinear example with a unique scalar solve

Let I₁={1,2}, I₂={3}, α=1, q=log(r/(1−r)), d=x₂−x₁, z=x₃, and

    φ₁(q,x₁,x₂)=(q²+d²)/2,   φ₂(z)=z²/2,
    κ(q)=1/[r(1−r)]=2+2cosh q.

The grouped metric gives the actual full internal equations

    qdot=−κ(q)q,       xdot₁=d/r,
    xdot₂=−d/(1−r),   zdot=−z.                          (22)

In particular rdot=−q; this is a nonlinear conditional-weight evolution, not the r=1/2 invariant subfamily. The first energy is nonlinear in r and couples the two positions.

Both φ functions are quadratic in the chosen chart, so the Gonzalez correction vanishes. Put s=(q+q')/2. The q equation is

    s[1+(h/2)κ(s)]=q.                                   (23)

The left side has derivative

    1+h[1+cosh s+s sinh s]≥1,

is odd and onto R, and therefore has one root. For q>0 the root lies in [0,q]; for q<0 use odd symmetry. Bisection is globally bracketed for every finite h≥0. Once s is found, let r_s=sigmoid(s), κ_s=κ(s), and

    γ=(1−hκ_s/2)/(1+hκ_s/2),
    d'=γd,       d_mid=(d+d')/2,
    x'₁=x₁+h d_mid/r_s,
    x'₂=x₂−h d_mid/(1−r_s),
    q'=2s−q,     z'=[(1−h/2)/(1+h/2)]z.                 (24)

These solve the entire internal midpoint equation, after which (6) gives group masses. All slots are computable from one scalar bisection and explicit formulas. For this example the exact internal root exists at every h, though large steps may cross q=0 or collide positions and should not be interpreted as accurate trajectories.

The benchmark starts with m=(0.4,0.6), (q,x₁,x₂,z)=(0.7,−0.6,1.4,0.9), and T=0.5. Its loss ordering changes during the interval, so the minimum baseline is not artificially assumed to stay on one branch. A separate reference uses the separated continuous equations:

    T=∫_(q_T)^(q₀) du/[κ(u)u],
    d_T=(d₀/q₀)q_T,
    x₁(T)=x₁(0)+(d₀/q₀)[F(q₀)−F(q_T)],
    F(u)=u−log(1+exp u),
    I₁=[1+(d₀/q₀)²][H(q₀)−H(q_T)]/2,
    H(u)=(u/2)tanh(u/2)−log cosh(u/2),
    I₂=z₀²[1−exp(−2T)]/4,
    m(T)∝(m₁(0)exp(−I₁),m₂(0)exp(−I₂)).                (25)

Here q_T is independently bracketed between q₀exp(−κ(q₀)T) and q₀exp(−4T); x₂=x₁+d_T and z=z₀exp(−T). This reference follows a quadrature identity different from the numerical update. It is used for diagnostics, not as an oracle inside the scheme.

The 80-decimal author run reports second-order whole-coordinate convergence for both positive mass rules over n=8,16,32,64,128; the observed successive orders are approximately 2.0033, 2.0008, 2.0002, 2.00005. The same internal solver with final-loss-only P₂ factors gives approximately 0.9451, 0.9738, 0.9872, 0.9937. Complete values, separate group-mass and conditional-weight errors, nonlinear residuals, energy budgets, and reference values are recorded in `CHECKS_FINAL_NORMAL.json`. Earlier `CHECKS_NORMAL.json` and `CHECKS_EXPANDED.json` retain actual development-stage runs; they are not additional independent evidence. These are high-precision diagnostics; the analytical convergence statement is the proof in §4.

## 6. Domain, observation, zero-audit, and time boundaries

### The convergence topology is consequential

Equation (20) is a finite labelled-coordinate statement. On a bounded position region it implies order two for every fixed C¹ observable with bounded derivative there, in particular any fixed polynomial moment. For two labelled laws μ=Σw_iδ_(x_i), ν=Σv_iδ_(y_i), couple common label masses first and then unmatched mass. If the union of positions has diameter D,

    W₁(μ,ν)≤Σ_i w_i |x_i−y_i| +(D/2)Σ_i|w_i−v_i|.     (26)

Hence the whole scheme is globally order two in W₁ on the stated finite-horizon compact region. No uniform bound over unbounded polynomial degree or unrestricted laws is implied.

It is **not** globally or locally second order in total variation for moving atomic laws. A single quadratic Dirac started at 1 has exact position exp(−h) and midpoint position γ. For 0<h<2,

    log γ=log(1−h/2)−log(1+h/2)<−h,

so the two positions differ and their TV distance is exactly 1. Repeating n steps with h=T/n gives γ^n<exp(−T), hence TV remains 1 at the fixed terminal time for every n with h<2. This does not conflict with high-order TV for inherited fixed-state reweighting: the support has now moved.

Nor does coordinate order two automatically imply W₂ order two for variable masses. An exact countercontrol uses two stationary labelled positions 0 and 1, constant per-label losses 0 and 1, and initial masses 1/2. At T=1, n P₂ steps give the second mass 1/[1+P₂(1/n)^n], versus 1/(1+e) exactly. Their difference is

    e/[6(1+e)²] n^(−2)+O(n^(−3)).

TV and W₁ equal this positive mass error; W₂ is its square root and therefore has exact generic order one. This is already inside the present allowed class, without any position-solver error. The present W₁/observable result is the honest full-law interface.

### Positivity does not mean fixed rank or a quotient-law gradient

For one common quadratic loss, h=2 makes γ=0 and collapses every position to the minimizer in one midpoint step. All label masses remain positive. In the grouped example q=0 and h=1/2 collapse a pair's separation. Thus no unconditional rank preservation, injectivity, collision avoidance, or inverse-on-range theorem is included. Smaller steps and separated compact configuration regions can retain separation, but their guards must be supplied.

The algorithm is on retained labelled product states. At a collision, the unlabelled law need not retain the origin distinction needed by the audit, and the inherited metric does not become a nondegenerate law metric merely by pushing the labels forward. General grouped V may itself depend on retained conditional labels. Keeping those labels is a substantive contract, not redundant storage.

### Zero masses and zero likelihoods

The Riemannian theorem is interior. A finite positive step never creates or deletes a label; it cannot reconstruct an erased source alternative. If one formally allows m_g=0 while retaining its internal record, (6) preserves that zero and still defines a probability on the surviving groups, but (1) is no longer a positive metric there. This is an algebraic extension, not the same gradient theorem. Conditional r_i=0 is outside the logit chart and can make the position mobility singular.

An audit deleting a whole group can retain the algebraic commutation identity if the full original internal catalogue, baseline, step selection, and branches are retained. If deleted groups are removed before recomputing b, P₂ may change the surviving factors; the inherited zero-audit/minimum-baseline counterexample already proves that failure. Exponential factors avoid that particular baseline problem but still do not restore erased labels or justify audit-dependent steps. No division by a zero likelihood is authorized by this construction.

### Predetermined time-dependent energies

For a smooth externally supplied V_g(t,y_g), freeze each group potential at t+h/2 and apply the entire construction (internal solve and endpoint-average masses) using that same frozen potential. If the schedule and choices are audit invariant, the discrete audit square is unchanged. On a compact region with the necessary uniform time/space derivatives, midpoint freezing gives local O(h³) for the prescribed nonautonomous equation: expansion of F(t+h/2,z) contributes h²F_t/2 along with h²F_zF/2.

The exact descent claim is then for the frozen midpoint energy. The actual time-dependent energy obeys the discrete work identity

    E(t+h,z')−E(t,z)
      =[E(t+h,z')−E(t+h/2,z')]
       +[E(t+h/2,z')−E(t+h/2,z)]
       +[E(t+h/2,z)−E(t,z)].                            (27)

The middle term is nonpositive; the other two are external work at fixed endpoint states and need not be. Even the constant-in-state energy E(t,z)=t increases by h while its gradient vanishes. No unconditional physical-time energy decrease is claimed. Frozen-time coercivity or observed energy decrease also does not imply global continuation; the inspected nonnegative moving-gradient escape result already supplies an exact finite-time failure. The compact-horizon and time-schedule guards must remain attached.

### Remaining limits

This is not an arbitrary interacting cross-group energy integrator with universal audit covariance; the inherited classification excludes that claim. It is not a full non-Gaussian constrained-marginal PDE construction, an infinite-support algorithm from finite moments, a stiffness or complexity guarantee, or an arbitrary-order method. Correct numerical source-audit transport does not identify loss with epistemic warrant, supply likelihood calibration, or establish empirical independence of sources.

## 7. Evidence and replay

Run from the workspace root, with Python 3, SymPy, and mpmath installed:

    python t20-depth-reassessment-20261011/joint_correction/check_joint.py \
      --output /a/new/path/CHECKS.json

The program refuses to overwrite an existing result. It uses explicit exceptions rather than Python assertions. Exact-source hash checks, symbolic identities, exact-fraction structural controls, and high-precision convergence diagnostics are tagged separately in the output. An optimized run, if present, only verifies that check execution survives Python -O; it is not a second independent mathematical review.

The contribution is one bounded whole-dynamics interface with qualifications, not a theorem-count expansion. Its practical acceptance test is simultaneous: an actual internal state transition, certified or appropriately qualified internal descent and solve accuracy, positive law reconstruction, correct changing-loss accumulation, a declared error topology, and an exact audit square under the actual retained source action.
