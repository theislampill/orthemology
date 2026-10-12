# Exact Gaussian restriction of transport and centred reaction

11 October 2026 UTC. Additive ordinary mathematics within ACTIVE T20. This is an author-side proof and exact-control packet, not independent review, a formal-kernel proof, protected-source integration, empirical identification or programme closure. The parent supplied the Gaussian metric candidate, quadratic-flow test and curvature question. The investigator supplies the full-tangent minimization proof and scope checks; the comparison of overlapping transport/reaction channels was developed jointly.

## 1. Result and inheritance

Let G be the family of one-dimensional nondegenerate Gaussian probabilities N(m,v), m in R and v>0. Declare the unit-coefficient transport-plus-centred-reaction tangent norm by minimizing E[u²+α²] over all fields producing the specified density derivative, with Eα=0. Its exact restriction to G is the smooth positive Riemannian metric

    g = dm²/(1+v) + dv²/[2v(v+2)].                       (1)

This is a minimization over fields realizing the full density tangent, not merely the first two moment changes. Both transport and reaction can produce the same Gaussian tangent directions. Their cometrics add; adding the two metrics would give the wrong answer.

For every quadratic F(x)=κx²/2+βx+γ, the actual full-law correction

    ∂tρ = ∂x(ρF′) − (F−EρF)ρ                           (2)

is tangent to G and equals its genuine negative g-gradient for the restricted energy EρF. Conversely, among polynomial F, no polynomial of degree at least three has a Gaussian-tangent field at even one nondegenerate Gaussian state. Coercive quadratics have exact global forward Gaussian trajectories. Concave quadratics have only a finite integrability interval in general. Section 7 extends the full-tangent result to multivariate Gaussians with a positive covariance-tensor metric and exact, possibly noncommuting, quadratic flow.

The nine direct input reports are copied and hash-bound in INPUT_BINDINGS.json. Their claims remain inherited:

- joint-atomic-gradient-lift-20261010 already owns the genuine moving-atom Riemannian realization and the observable cometric E[p′q′]+Cov(p,q). spherical-atomic-source-interface-20261010 owns the exact fixed-atomic-path action minimization and its local-speed comparison. full-law-gradient-action-tail-20261010 owns action and moment-tail controls for the represented general-law evolution. None of these inspected passages calculates the Gaussian tangent infimum.
- noetic-gradient-transport-20261009 owns a fixed-reference quadratic Hessian quotient geometry and explicitly preserves the programme's older genuine Hessian/Bregman repair geometry. Those positive results are not replaced or downgraded here.
- tensor-moment-continuation-20261009 and leafwise-noetic-geometry-20261010 own Fisher-only moment mobility, finite-support/exponential-family restrictions and conditional Hessian mean-coordinate geometry. face-stratified-noetic-geometry-20261010 owns its finite exponential-leaf boundary extension. The present Gaussian norm has an additional spatial transport channel.
- gaussian-observation-realisation-20261010 concerns Fisher lengths, one-sided likelihood domination, nested observation histories and non-Gaussian failure branches for a fixed target. Equation (2) changes locations as well as weights. Gaussian invariance for this deterministic law evolution does not supply that report's complete observation experiment or remove its failure-branch obstruction.

A bounded scan of 169 then-available top-level RESULT.md reports, recorded in DEDUP_SCAN.json, found these antecedents and the concurrently developed finite-polynomial-state-no-go report, whose Gaussian quadratic formula is a scope control. The local addition here is the full Gaussian tangent minimization, its overlapping-channel interpretation and polynomial tangency boundary. This is not a project-wide or historical priority claim. Gaussian integration, Riemannian gradients and spherical transport/reaction geometry are classical.

## 2. Precise tangent contract

Write

    ρ(x) = (2πv)^(-1/2) exp[−(x−m)²/(2v)],   ξ=x−m.

A Gaussian coordinate tangent h=(M,V) has density derivative

    σ_h/ρ = M ξ/v + V(ξ²−v)/(2v²).                     (3)

An admissible representing pair is u,α in L²(ρ), with Eρα=0, satisfying

    σ_h = −∂x(ρu)+ρα                                  (4)

as distributions on R, tested initially against C∞ compactly supported functions. Define

    ||h||² = inf { Eρ[u²+α²] : (u,α) satisfies (4) }.   (5)

This declaration needs no smooth manifold of all probability laws and no global distance identification. The family G itself is the explicit smooth half-plane R×(0,∞). The minimizer below proves that (5) is a finite, positive quadratic form on every tangent and varies smoothly.

Polynomial tests of degree at most two are allowed in (4) by an actual approximation argument. Let χ be smooth, compactly supported, one on [−1,1], and put f_R(x)=χ(x/R)f(x). For every polynomial f of degree at most two, Gaussian tails give f_R→f and f_R′→f′ in L²(ρ). Since σ_h/ρ is also in L²(ρ), Cauchy–Schwarz gives convergence of both sides of

    ∫f_R σ_h dx = Eρ[f_R′u+f_Rα].

Thus ∫fσ_h=Eρ[f′u+fα]. No unproved integration by parts with an arbitrary L² field is needed.

## 3. Full-density minimality, with a unique minimizing pair

Take the centred quadratic potential

    f=aξ+b(ξ²−v),      u_*=f′=a+2bξ,      α_*=f.

Its density tangent is

    [−∂x(ρf′)+ρf]/ρ
      = a(1+v)ξ/v + b(v+2)(ξ²−v)/v.                   (6)

Comparing with (3), the pair realizes exactly h when

    a=M/(1+v),       b=V/[2v(v+2)].                    (7)

All fields involved are in L²(ρ), and Ef=0. The Gaussian identities Eξ=Eξ³=0, Eξ²=v and Eξ⁴=3v² give

    E[(f′)²+f²] = a²(1+v)+2b²v(v+2)
                 = M²/(1+v)+V²/[2v(v+2)].            (8)

Now let any other admissible pair be (u_*+w,α_*+η). Its difference satisfies −∂x(ρw)+ρη=0 and Eη=0. The cutoff argument of §2 applied to f proves

    E[f′w+fη]=0.

Consequently the exact Pythagorean identity is

    E[u²+α²] = E[(f′)²+f²] + E[w²+η²].                (9)

It proves the lower bound for every admissible full-tangent representation, attainability, and uniqueness of the minimizing pair up to ρ-almost-everywhere equality. Formula (1) follows by polarization. In particular, inversion of a two-moment matrix alone is not the proof: equation (6) proves that its optimal candidate realizes the entire density tangent, and (9) excludes a cheaper unobserved density realization.

The dual quadratic form is, consistently with the inherited cometric,

    g^*(a dm+b dv,a dm+b dv)
      = (1+v)a²+2v(v+2)b²
      = E[(f′)²]+Var(f),   f=aξ+b(ξ²−v).              (10)

Here dm and dv are differentials at the chosen state; the variance differential is represented by ξ²−v, up to the constant gauge.

## 4. Why the cometrics add

For this Gaussian tangent, the unique finite-L² pure-transport representative is

    u_T=M+Vξ/(2v),

and its squared cost is M²+V²/(4v). To see uniqueness, a difference obeys ∂x(ρw)=0, so ρw is constant as a distribution. A nonzero constant gives E[w²]=infinity. Pure reaction has α_R=σ_h/ρ and cost M²/v+V²/(2v²). Therefore the separate Gaussian metrics and their cometrics are

    g_T=diag(1,1/(4v)),       g_T^*=diag(1,4v),
    g_R=diag(1/v,1/(2v²)),    g_R^*=diag(v,2v²).

The minimizing pair of §3 splits the same full Gaussian tangent into

    (M_T,V_T)=(a,4bv),       (M_R,V_R)=(av,2bv²).

These are each Gaussian tangent vectors and sum to (M,V). Directly minimizing g_T(h_T,h_T)+g_R(h_R,h_R) subject to h_T+h_R=h gives the parallel combination

    g=(g_T^*+g_R^*)^(-1).                              (11)

The full-space proof (9) additionally excludes improvement by components whose individual tangents leave the Gaussian family and cancel outside it. Formula (11) is therefore exact here, not an assumed restriction rule for arbitrary statistical submanifolds.

At v=1 and h=(1,0), the exact combined squared norm is 1/2: u=1/2 and α=ξ/2 share the displacement. Naively adding the two squared norms would give 2. In the positive distinct-atomic stratum the spatial and weight coordinates were separate. For Gaussians their effects overlap in both mean and variance. That explains why simply reusing the atomic block-sum expression in Gaussian parameter coordinates fails.

## 5. Genuine gradients and the exact polynomial boundary

For a smooth J(m,v), metric duality, not just decrease of J, gives

    grad_g J=((1+v)J_m, 2v(v+2)J_v).                  (12)

Indeed pairing (12) with any h=(M,V) in (1) gives J_m M+J_v V. Its representing potential is f=J_m ξ+J_v(ξ²−v), with coefficients evaluated at the current state. The negative flow is consequently the steepest-descent field for this metric, and along every local solution

    dJ/dt=−(1+v)J_m²−2v(v+2)J_v².                    (13)

There is no assertion of all-time existence for an arbitrary smooth J on an open half-plane.

For F(x)=κx²/2+βx+γ, the restricted expected energy is

    E_F(m,v)=κ(m²+v)/2+βm+γ.

The resulting exact negative gradient is

    m′=−(1+v)(κm+β),       v′=−κv(v+2).              (14)

Since F−EF=(κm+β)ξ+(κ/2)(ξ²−v), its minimizing negative-gradient fields are precisely u=−F′ and α=−(F−EF). Equations (6) and (14) therefore verify the full PDE (2), not just its first two moments. The dissipation identity is

    −E_F′=(1+v)(κm+β)²+(κ²/2)v(v+2)
          = E[(F′)²]+Var(F).                          (15)

For the converse, let F have degree n≥3 and leading coefficient c≠0. At any Gaussian state the full density field in (2) has ratio

    σ_F/ρ=F″−(x−m)F′/v−F+EF.

Its coefficient of x^n is −c(1+n/v), which cannot vanish when v>0. Thus its degree is exactly n, while every Gaussian tangent score (3) has degree at most two. It is not tangent. Together with (14), this proves the iff for polynomial F, including constant and affine cases. No classification of nonpolynomial potentials is claimed.

The Gaussian gradient of the restricted expected value of a higher-degree polynomial is still defined, but it does not equal the full field (2). Replacing the full law by the Gaussian with its current first two moments would be an additional approximation, not this exact invariant-family theorem.

In fact, Gaussian integration by parts shows that this restricted gradient matches the full field's instantaneous first-two-moment velocities at a Gaussian, even for higher-degree polynomials. For example, at N(0,v) and F=x⁴/4, both give m′=0 and v′=−3v²(v+2). Nevertheless the difference between the full density score and the Gaussian score with those velocities is

    −(1/v+1/4)(x⁴−6vx²+3v²),

which is nonzero and has zero pairing with 1,x,x². Thus agreement of those moment derivatives alone would miss the failure of Gaussian invariance. The full-density calculation is essential.

## 6. Exact trajectories and their existence interval

For κ≠0 write F(x)=κ(x−c)²/2+C, where c=−β/κ. Given N(m_0,v_0), let

    z=e^(−κt),       D(t)=1+(v_0/2)(1−z²).

On the interval D(t)>0, the exact solution is

    v(t)=v_0 z²/D(t),
    m(t)=c+(m_0−c)z/D(t).                             (16)

This is verified independently of moment closure: the characteristic flow is x↦c+z(x−c), and its accumulated killing factor on the initial coordinate is

    exp[−Ct−q(t)(x−c)²],       q(t)=(1−z²)/4.

Multiplying a Gaussian by this quadratic exponential and completing the square gives initial-coordinate variance v_0/D and mean c+(m_0−c)/D. Pushing forward by the characteristic gives (16). The normalizer is

    Z(t)=exp(−Ct)D(t)^(-1/2)
          exp[−q(t)(m_0−c)²/D(t)].                   (17)

Differentiation checks (14) and the initial conditions. These equations are smooth on R×(0,∞), so ordinary local ODE uniqueness proves uniqueness of the Gaussian trajectory on its maximal interval; no uniqueness theorem for every abstract moment hierarchy is imported.

- If κ>0, D(t)≥1 for t≥0, and the Gaussian trajectory exists for every finite forward time. It has positive variance at each such time and converges weakly to δ_c as t→infinity. The limiting law lies outside G. For κ=1,c=C=0, equation (14) is m′=−(1+v)m, v′=−2v−v², and E_F=(m²+v)/2.
- If κ<0, D(t)>0 exactly for 0≤t<t_*, where t_*=[log(1+2/v_0)]/(2|κ|). At t_* the weighted Gaussian integral is infinite: its quadratic confinement has disappeared, and a constant or nonzero linear exponential on the whole real line is not integrable. The variance in (16) diverges as t↑t_*. There is no global-forward Gaussian probability claim in this case.
- If κ=0, F=βx+γ and v(t)=v_0, m(t)=m_0−β(1+v_0)t. Exponential tilting by exp(−βtx), followed by translation x↦x−βt, proves this formula and gives a finite normalizer at every finite time. Constants produce the stationary law.

## 7. Multivariate covariance-tensor corollary

The same positive construction extends to G_d={N(m,Σ): m in R^d, Σ symmetric positive definite}. Retain a fixed Euclidean spatial norm and the unit reaction coefficient. Matrices below act in those spatial coordinates; the identity matrix records that supplied transport metric. Orthogonal coordinate changes preserve these displayed formulas. Arbitrary coordinate rescalings require transforming the transport metric rather than keeping the identity unchanged.

A tangent is (h,B), with B symmetric. Write ξ=x−m and use the Frobenius pairing tr(AB) for symmetric matrices. Its density score is

    σ_(h,B)/ρ = hᵀΣ^(-1)ξ
       + [ξᵀΣ^(-1)BΣ^(-1)ξ−tr(Σ^(-1)B)]/2.

For a vector a and symmetric A, the centred quadratic potential

    f=aᵀξ+ξᵀAξ−tr(AΣ)

has fields u=∇f=a+2Aξ and α=f. Direct differentiation gives the entire Gaussian density tangent with

    h=(I+Σ)a,
    B=L_Σ(A),       L_Σ(A)=2(AΣ+ΣA+ΣAΣ).              (18)

The Gaussian moment identities give

    E[|∇f|²+f²]
      =aᵀ(I+Σ)a+4tr(A²Σ)+2tr(AΣAΣ)
      =aᵀ(I+Σ)a+tr(A L_Σ(A)).                        (19)

For completeness, the quadratic fourth-moment term follows from
E[ξ_iξ_jξ_kξ_l]=Σ_ijΣ_kl+Σ_ikΣ_jl+Σ_ilΣ_jk, obtained by differentiating the Gaussian moment generating function exp(tᵀΣt/2). The linear/quadratic cross term has zero expectation by central symmetry.

The operator L_Σ is self-adjoint and positive definite on symmetric matrices. In an orthonormal eigenbasis Σ=diag(λ_i), with all λ_i>0,

    (L_Σ(A))_ij=2(λ_i+λ_j+λ_iλ_j)A_ij.

Each multiplier is positive. Hence every full Gaussian tangent has a unique such potential, with a=(I+Σ)^(-1)h and A=L_Σ^(-1)(B). Compact radial cutoffs of f converge together with their gradients in Gaussian L². The identical zero-tangent orthogonality argument of §3 proves minimality among all L²(R^d;R^d) transport fields and centred L² reactions, with no restriction to polynomial fields or separately Gaussian component tangents. The exact metric is

    g_Σ((h,B),(k,C))
      =hᵀ(I+Σ)^(-1)k+tr(B L_Σ^(-1)(C)).              (20)

In the displayed eigenbasis its covariance squared norm is

    sum_i B_ii²/[2λ_i(λ_i+2)]
      +sum_(i<j) B_ij²/[λ_i+λ_j+λ_iλ_j].              (21)

The off-diagonal term is counted twice by the Frobenius sum over all i,j. Formula (21) respects that convention; treating the upper-triangular entries as an unweighted Frobenius basis would lose a factor of two. Smoothness of inversion on the positive-definite operator cone proves a smooth finite-dimensional Riemannian metric, of dimension d+d(d+1)/2.

The same overlapping-channel decomposition has mean cometrics I and Σ, and covariance cometrics 2(AΣ+ΣA) and 2ΣAΣ, respectively. Their sum is (18). This is a genuine covariance-tensor extension of (1), not an assertion that all tensor descriptors close on all laws.

For F(x)=xᵀQx/2+bᵀx+c with Q symmetric, metric duality and the full quadratic density calculation give

    m′=−(I+Σ)(Qm+b),
    Σ′=−(QΣ+ΣQ+ΣQΣ).                                (22)

In particular, the covariance equation is not replaced by −2ΣQ−ΣQΣ when Q and Σ do not commute. For P=Σ^(-1), differentiation yields

    P′=PQ+QP+Q,
    P(t)=exp(tQ)P(0)exp(tQ)+(exp(2tQ)−I)/2.           (23)

These formulas apply while P(t) stays positive definite. The mean equation is then a linear ODE with smooth time coefficients. For Q positive semidefinite, both the first term of P(t) and the positive-semidefinite second term show P(t)>0 for every finite t≥0, so the Gaussian flow exists globally forward. For general Q no unconditional global assertion is made. Completing the square along the affine characteristic flow gives the same Gaussian evolution on its normalizable interval; the 1D concave example in §6 shows why that interval cannot be suppressed.

## 8. Bounded geometric diagnostics

The coordinate change r=arcosh(v+1)/sqrt(2), r>0, gives

    g=dr²+sech(sqrt(2)r)dm².

For a metric dr²+A(r)²dm², its Gaussian curvature is −A″/A. With A=sqrt(sech(sqrt(2)r)), direct differentiation yields

    K=3/[2(v+1)²]−1/2.                                (24)

It is positive for 0<v<sqrt(3)−1, zero at that value, and negative above it. This is a check that the explicit finite geometry is nonflat, not a new curvature theory or a claim about the curvature of the whole probability space. At fixed m, the path from v_1 to v_2 has length |r(v_2)−r(v_1)|, minimal among Gaussian paths with those endpoints because any such path has length at least its total radial displacement. The excluded v=0 boundary is at finite distance along this path, so G is not metrically complete.

Relative to the ordinary flat coordinate connection in (m,v), this metric is not a Hessian: a C³ potential with g_ij=∂i∂jψ would require ∂v g_mm=∂m g_mv, while the two sides are −(1+v)^(-2) and zero. This is only a statement about that fixed affine coordinate structure. It does not rule out another Hessian structure or coordinate system. In particular it does not contradict the inherited genuine Hessian/Bregman or Fisher/exponential-family results. Nonzero curvature alone would not rule out a Hessian metric.

Neither this local norm calculation nor (24) identifies intrinsic Gaussian endpoint distances with an unrestricted transport/reaction distance between the same measures. Ambient paths may leave the family. No geodesic convexity, global optimality, or all-laws smooth-manifold claim is needed here.

## 9. Relation to finite polynomial descriptors and application scope

The finite record (m,E[X²]) determines the full law only under the explicit Gaussian-family restriction, since v=E[X²]−m²>0. Every higher Gaussian moment is then a polynomial in m,v, by expansion of (m+ξ)^n and the Gaussian even-moment formula. This exact closure relies on state-space information additional to those two numbers for a general law. It is compatible with the concurrent finite-polynomial-state-no-go result; no arbitrary finite descriptor for every initial law is supplied.

The construction supplies a genuine positive finite-dimensional correction geometry for this specified law family, with its actual full-law gradient on the invariant quadratic class. It does not identify an actual noetic bearer, mental state, cognitive mechanism, truthful recognition, source authority, warrant or metaphysical necessity with these coordinates. It does not claim that selecting an energy or its decreasing trajectory makes the energy epistemically appropriate. Those are separate substantive questions.

## 10. Classical source interface and verification

The unit/unit centered gradient is classical spherical Hellinger–Kantorovich geometry. Kondratyev and Vorotnikov, *Spherical Hellinger-Kantorovich gradient flows*, arXiv:1809.03430v2, Introduction and Remark 1.1, displays the transport term and mean-centred reaction for a variational derivative. Its analytic theorems assume bounded-domain/torus density settings and a strictly negative density derivative of the fitness. The linear-density energy ∫Fρ on R does not satisfy those hypotheses. We use the source for ancestry and normalization correspondence; §§2–6 supply the Gaussian claims directly. [Primary source](https://arxiv.org/html/1809.03430v2).

SOURCE_READING.json records the focused primary reading. The retained source-interface report gives the additional convention and domain qualifications; no global dynamic/static theorem is silently transferred from it.

Run `python3 verify.py --output-dir private-locator:39866fa4df145aa06ba3`. Exact symbolic/rational checks cover the Gaussian density tangent, admissible potential, action, cometric, polynomial null-field orthogonality, channel decomposition, gradient duality, quadratic/quartic distinction, closed-form trajectories, normalizer, curvature, finite boundary and coordinate-Hessian obstruction. Input snapshots are hash-checked. The optional `--original-root ..` additionally checks the inspected originals. Finite checks corroborate, and do not replace, the all-L² minimization proof, cutoff limit, or arbitrary-degree theorem. Author verification and a later independent review are separate evidence objects.
