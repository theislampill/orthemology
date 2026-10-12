# Accumulated SOS damping forces probability-law realizability

10 October 2026 UTC. Additive ordinary mathematical continuation of Theorem V and its supplied polynomial-coordinate transport corollary. The parent proposed the backward Volterra cumulative-coercivity route and the polynomial rank-one example, and participated in developing and checking the proof. The investigator supplied the detailed proof and exact controls, including the uniform-interior monotonicity simplification. This author packet is not an independent review. Inherited arguments and attribution are identified below. No protected file is modified, and no field-priority, empirical, proof-kernel, or closure claim is made.

## 1. Result and exact hypotheses

Write R(x)=|x|² on R^d, with 1≤d<∞, and let 0<T≤∞. Let h_t(x) be real polynomials whose coefficients are continuous in time and whose degrees have a common finite bound on every compact window [0,H]⊂[0,T). On each such window suppose there is a continuous real scalar function β_H(t) such that

    g_t(x)=h_t(x)+β_H(t) is SOS for every 0≤t≤H.          (C1)

For every 0<t≤H also suppose there is a number c_H(t)>0 such that

    K_(0,t)(x)−c_H(t) R(x) is SOS,
    K_(s,t)(x)=∫_s^t g_u(x)du.                           (C2)

All polynomial integrals are coefficientwise. No continuous choice of an SOS decomposition, no regularity of c_H(t), and no positive lower bound on c_H(t)/t near zero is assumed. The scalar shift may depend on the chosen finite window. A constant shift is a special case. The condition is required from time zero to every positive time, not merely at one terminal time. No theorem under a sole terminal-time certificate is asserted here.

Let L_t be real linear functionals on all real polynomials, with each monomial coordinate C¹ through time zero (continuous right derivative there), satisfying

    L_t(1)=1,       L_t(q²)≥0 for every real polynomial q,
    L_t′(p)=−L_t(h_t p)+L_t(h_t)L_t(p).                  (M)

No representing measure at zero or at any other time is assumed.

**Theorem V_c.** Under (C1)–(C2) and (M), there is one uniquely determined probability μ on R^d with every absolute polynomial moment finite such that

    H_t(x)=∫_0^t h_u(x)du,
    L_t(p)= ∫p e^(−H_t)dμ / ∫e^(−H_t)dμ.                (1)

Every positive-time full moment record is determinate. Conversely, every probability μ with all absolute polynomial moments finite produces such a path for the supplied energy schedule. Thus for a fixed valid initial moment record, these full square-positive paths are in bijection with its entire representing-law fibre. The initial moment record itself need not be determinate; the full path identifies one law.

If the supplied energy family continues with (C1)–(C2), a path extends uniquely along that supplied family. Nothing here provides an unspecified future energy or a general theorem for all time-varying coercive polynomials.

This strictly relaxes the instantaneous radial SOS hypothesis of V: if g_t−cR is SOS uniformly on a window, then (C2) holds with c_H(t)=ct. The elementary fixed-degree SOS closure fact used only for this inclusion is justified below. Sections 8–9 instead exhibit instantaneous rank-one squares that admit no positive radial certificate at any time, while their accumulated energy has such a certificate at every positive time.

To justify the inclusion, a continuous coefficientwise integral of fixed-degree SOS polynomials is SOS: its Riemann sums are SOS, and that cone is closed. Here is a short closure proof. For degree at most 2m, write each SOS as z_m(x)^T Q z_m(x), where z_m is the vector of monomials of degree at most m and Q is positive semidefinite. Its square factors need no greater degree, since their leading square terms cannot cancel. The matrix B=∫_(unit ball) z_m z_m^T dx is positive definite. If SOS polynomials converge coefficientwise, their integrals, equal to trace(QB), stay bounded; positivity of B therefore bounds trace(Q), hence Q. A subsequence converges to a positive semidefinite Gram matrix for the limit. This proves closure and the integral claim without selecting the square factors continuously. The main proof below avoids this closure lemma entirely.

## 2. Unnormalization uses only first derivatives

Fix a finite window and suppress its subscript. Constants cancel in (M), so the same normalized equation holds with g_t. Define

    a(t)=exp(−∫_0^t L_u(g_u)du),       A_t(p)=a(t)L_t(p).

Because g has a bounded polynomial degree and continuous coefficients, L_t(g_t) is continuous. Therefore a is C¹ and strictly positive, a(0)=1, and for each fixed polynomial p,

    A_t′(p)=−A_t(g_t p).                                (2)

The functionals A_t are square-positive. Since g_t is SOS,

    A_t(g_t)≥0,       a′(t)≤0,       0<a(t)≤1.           (3)

Only the supplied coordinate first derivatives are used. No time derivative of g_t or of its chosen SOS factors is taken.

## 3. Exact finite Volterra expansion and its sign

For s≤t and any fixed polynomial p, the fundamental theorem of calculus gives

    A_s(p)=A_t(p)+∫_s^t A_u(g_u p)du.                   (4)

For m≥1 let Δ_m(s,t)={s≤u_1≤⋯≤u_m≤t}. Repeatedly apply (4), freezing the already selected polynomials g_(u_1),…,g_(u_j) when applying the moment equation at later times. For every integer N≥0 this gives the exact identity

    A_s(p)= Σ_(k=0)^N A_t(p K_(s,t)^k)/k! + E_(N+1),    (5)

    E_(N+1)=∫_(Δ_(N+1)(s,t))
              A_(u_(N+1))(p ∏_(j=1)^(N+1) g_(u_j)) du. (6)

For N=0, (6) is exactly the integral in (4). To pass from N to N+1, apply (4) to the fixed polynomial p∏g_(u_j), from its latest simplex time u_(N+1) to t. The terminal A_t term adds the next ordered-simplex integral, and the remaining integral is the next E.

At each finite N all these polynomials lie in one finite-dimensional space of degree at most deg(p)+(N+1)D. The joint integrands are continuous in the time variables: they are finite sums of continuous coefficient products and continuous moment coordinates. Thus their coefficientwise integrals, ordinary Fubini steps, and integration against the fixed linear functional A_t are legitimate. There is no infinite-series convergence assumption in (5).

Commutativity of polynomial multiplication makes the terminal integrand symmetric in its k time variables. Partitioning [s,t]^k into its k! ordering simplices (with diagonals of Lebesgue measure zero) gives exactly

    ∫_(Δ_k(s,t)) A_t(p∏g_(u_j))du
       = A_t(p(∫_s^t g_u du)^k)/k!.

This explains the factorial in (5); it is not an assumed commutation of time-varying differential operators.

Now take p=q². A product of finitely many SOS polynomials is SOS, since (Σf_i²)(Σr_j²)=Σ_(i,j)(f_i r_j)². Therefore every integrand in (6) is nonnegative by square positivity, without choosing the SOS factors continuously. We have proved

    A_s(q²) ≥ Σ_(k=0)^N A_t(q² K_(s,t)^k)/k!             (7)

for every finite N. No representing law, higher time regularity, or application of square positivity to an arbitrary pointwise nonnegative polynomial has been used.

We do not discard E_(N+1) in the limit or assert equality of the infinite series at this stage. Its nonnegative sign alone is sufficient for the next step.

## 4. Gaussian moments and representation at every positive time

Fix t>0 and abbreviate K=K_(0,t), c=c_H(t). Assumption (C2) makes K SOS, since K=(K−cR)+cR. For every integer n≥1,

    K^n−c^nR^n=(K−cR) Σ_(j=0)^(n−1) K^(n−1−j)(cR)^j

is SOS. The same is true after multiplication by q². Using s=0 in (7) yields the full radial partial-sum bound

    Σ_(n=0)^N c^n A_t(q²R^n)/n! ≤ A_0(q²).              (8)

In particular, for q=1,

    Σ_(n=0)^N c^n A_t(R^n)/n! ≤1,
    0≤A_t(R^n)≤n!c^(−n).                               (9)

Because R^n−x_i^(2n) is SOS by its multinomial expansion,

    0≤L_t(x_i^(2n))≤ n!/[a(t)c^n].                      (10)

The right side implies every marginal Carleman condition. Indeed, apart from the harmless convention that a zero moment contributes infinity, the inverse 2n-th roots are bounded below by a(t)^(1/(2n)) sqrt(c)/sqrt(n), using n!≤n^n. Their sum diverges.

The classical multivariate Nussbaum–Carleman theorem now supplies a representing probability ρ_t and identifies it uniquely. Its input is a full square-positive functional with all marginal Carleman conditions, not a pre-existing vector measure. A primary statement is Putinar–Schmüdgen, *Multivariate Determinateness*, Theorem 25 and the following attribution, printed p. 24, https://arxiv.org/pdf/0810.0840v1 . Define ν_t=a(t)ρ_t, the unique finite positive measure representing A_t.

Monotone convergence in (8) now gives, for every real polynomial q,

    ∫q² e^(cR)dν_t≤A_0(q²).                             (11)

In particular ∫e^(cR)dν_t≤1. This exponential integrability was derived algebraically before using a representing measure.

### Uniform interior bounds without extra certificate regularity

Fix J=[η,H′] with 0<η≤H′≤H. For each n, R^n g_t is SOS. Equation (2) therefore gives

    dA_t(R^n)/dt=−A_t(g_tR^n)≤0.

Use (9) at η with r=c_H(η)>0, and then use this monotonicity term by term. For all t∈J and all N,

    Σ_(n=0)^N r^n A_t(R^n)/n!≤1.

Consequently

    ν_t(R^d)≤1,       ∫e^(r|x|²)dν_t≤1,                 (12)
    ∫|x|^k dν_t≤sqrt(k!)r^(−k/2),   k=0,1,….           (13)

For (13), use the even radial moment bound and Cauchy–Schwarz, including the mass bound. This proof does not need continuity of c_H(t), closedness of the fixed-degree SOS cone, or a measurable choice of SOS decompositions.

## 5. Fourier identification of the law-level equation

We detail the inherited V mechanism to show that the weaker accumulated hypothesis supplies every needed estimate. On J, bounded polynomial coefficients give a finite B with

    |g_t(x)|≤B(1+|x|^D).

For fixed ξ∈R^d put P_N(x)=Σ_(j=0)^N(iξ·x)^j/j!, extending A_t complex-linearly. The real-variable Taylor remainder for exp(iy) obeys

    |e^(iy)−Σ_(j=0)^(k−1)(iy)^j/j!|≤|y|^k/k!.

With k=N+1, (13) gives uniform convergence of A_t(P_N) on J to

    F_t(ξ)=∫e^(iξ·x)dν_t,

and uniform convergence of A_t(g_tP_N) to

    G_t(ξ)=∫g_t(x)e^(iξ·x)dν_t.

The derivative-side error is at most

    B |ξ|^k/k! [sqrt(k!)r^(−k/2)
                    +sqrt((k+D)!)r^(−(k+D)/2)].         (14)

It tends to zero, since the second summand's successive ratio is

    (|ξ|/sqrt(r)) sqrt(k+D+1)/(k+1) →0;

the first is the case D=0. These estimates are uniform also for ξ in a compact set. Continuous coefficients and moments make A_t(g_tP_N) continuous in t. Uniform convergence of the functions and their first derivatives in (2) therefore proves

    dF_t(ξ)/dt=−G_t(ξ).                                 (15)

The same compact-uniform limits prove joint continuity in t and ξ of F and G. No unproved measurability of the family ν_t was assumed.

For φ∈C_c^∞(R^d), apply Fourier inversion after establishing (15). The frequency-independent bounds

    |F_t(ξ)|≤1,
    |G_t(ξ)|≤∫g_t dν_t=A_t(g_t)=−a′(t)

hold because g_t≥0 as an actual polynomial and ν_t is now a positive measure. The last quantity is bounded on J. The integrable Fourier transform of φ then permits Fubini and dominated differentiation, giving

    d/dt ∫φ dν_t=−∫g_t φ dν_t.                          (16)

Its right side is continuous, by the Fourier formula and dominated convergence. The order of these steps matters: one does not integrate the ξ-dependent Taylor error estimate over all frequencies.

## 6. Compact integrating factors, inverse weighting, and time zero

If ψ_u is a family of compact smooth spatial tests with common compact support, C¹ in time in the uniform norm, with each ∂_uψ_u also a compact smooth spatial test, then (16) gives

    d/du ∫ψ_u dν_u=∫(∂_uψ_u−g_uψ_u)dν_u.              (17)

For completeness, split the difference quotient into the change in ψ with ν at the new time and the change in ν with ψ frozen. Uniform differentiability of ψ and bounded masses handle the first part; continuity of ν against the fixed compact test ∂_uψ_u and equation (16) handle the remaining limits. This needs no global measure-valued differentiability premise.

Fix 0<s<t≤H and φ∈C_c^∞. Set

    ψ_u(x)=φ(x)exp(∫_s^u g_v(x)dv).

Its spatial support is fixed and compact. Continuous polynomial coefficients make it uniformly C¹ in time there, with ∂_uψ_u=g_uψ_u; its spatial derivatives are continuous and bounded on the chosen compact set. Equation (17) gives

    ∫φ e^(K_(s,t))dν_t=∫φ dν_s.

Both positive measures are locally finite, and compact smooth tests determine such measures. Hence

    ν_s=e^(K_(s,t))ν_t,
    ν_t=e^(−K_(s,t))ν_s.                               (18)

The first equality includes the finiteness of the inverse-weighted measure, since its value is the finite ν_s. It is not inferred from a formal inverse of a moment transformation.

Now fix t>0 and let s↓0. Since every g_u≥0, K_(s,t)(x) increases pointwise to K_(0,t)(x). From (18), monotone convergence and coordinate continuity at zero give

    ∫e^(K_(0,t))dν_t=lim_(s↓0)a(s)=1,
    ∫q²e^(K_(0,t))dν_t=lim_(s↓0)A_s(q²)=A_0(q²).       (19)

Define

    μ=e^(K_(0,t))ν_t.                                  (20)

It is a probability, and every q² is integrable with the prescribed initial value. For a polynomial p, |p|≤(1+p²)/2 gives absolute integrability. The identity p=((p+1)²−(p−1)²)/4 and (19) identify its signed moment as L_0(p). Thus zero-time representability is recovered rather than assumed; neither mass loss nor an infinite initial measure is left open.

For every positive t, (18)–(20) yield ν_t=e^(−K_(0,t))μ. Dividing by the mass cancels the scalar shift ∫β and proves (1). The construction gives the same μ whichever positive t is chosen.

If two probabilities generated the same full path, their normalized positive-time laws would share a determinate moment record and would coincide. Inverting the known positive likelihood and normalizing recovers the same initial probability. This proves uniqueness, including consistency between different local shifts or overlapping finite windows.

## 7. Converse and continuation

Let μ be any probability with every absolute polynomial moment finite. Since g=h+β≥0 on a finite window,

    e^(−H_t(x))≤exp(∫_0^H|β(u)|du),   0≤t≤H.

All weighted polynomial moments exist. Bounded coefficients give |h_t(x)|≤B(1+|x|^D); multiplying by the displayed uniform bound supplies an integrable polynomial majorant for each derivative of a weighted polynomial moment. Ordinary dominated differentiation, using only continuity of the coefficients, proves C¹ regularity through zero and equation (M). Normalization is legitimate because the denominator is positive.

The preceding proof establishes positive-time determinacy and law-to-path injectivity. Applying this construction to each representative of a fixed initial moment record proves the stated bijection. An extension along a supplied continuing schedule is obtained from the recovered μ by the same formula; any other square-positive extension has the same initial segment and hence the same μ. No finite moment cutoff or algorithmic reconstruction of μ is supplied.

## 8. A polynomial rank-one example outside instantaneous Theorem V

In R² let

    h_t(x,y)=g_t(x,y)=(x+t y)².

Every instantaneous g_t is a single square with rank-one quadratic form. Its accumulated energy is

    K_(0,t)=t x²+t²xy+(t³/3)y²,
    Q_t=[[t,t²/2],[t²/2,t³/3]],
    det(Q_t)=t⁴/12>0,       trace(Q_t)=t+t³/3>0.

For t>0 choose

    c(t)=det(Q_t)/trace(Q_t)=t³/[4(t²+3)],
    a_t=t−c(t)=3t(t²+4)/[4(t²+3)]>0.

There is the explicit SOS certificate

    K_(0,t)−c(t)(x²+y²)
      =a_t [x+2t(t²+3)y/(3(t²+4))]²
        + t⁵ y²/[12(t²+3)(t²+4)].                       (21)

Both displayed coefficients are positive. Positive real coefficients times squares are SOS after absorbing their square roots. The exact identity det(Q_t−c(t)I)=c(t)² is another certificate check. No spectral or semidefinite numerical tolerance is involved.

At any fixed time t, the null ray (x,y)=λ(−t,1) gives g_t=0. For every finite scalar C and every c>0,

    g_t+C−c(x²+y²)=C−c(1+t²)λ²

is eventually negative on that ray. Consequently no scalar shift can make the instantaneous radial hypothesis of V hold, even at a single time. This is a genuine strict extension, not a reparametrization of uniformly coercive instantaneous energies. Here c(t) is of order t³ near zero; there is no inherited lower bound of order t.

Indeed every nontrivial interval is cumulatively positive definite in this example: the Gramian over [s,t] has determinant (t−s)⁴/12. This extra interval property is not required by V_c.

### Rotating rank-one example

The initially proposed g_u(x,y)=(x cos u+y sin u)² also satisfies (C1)–(C2). Its integrated Gramian is

    Q_t=[[t/2+sin(2t)/4, (1−cos(2t))/4],
         [(1−cos(2t))/4, t/2−sin(2t)/4]],

with eigenvalues (t±|sin t|)/2. For every t>0, t>|sin t|, so c(t)=(t−|sin t|)/2 is positive and Q_t−c(t)I is positive semidefinite. A positive semidefinite real quadratic form is SOS by orthogonal diagonalization. Each instantaneous form still has a null line and fails any positive radial certificate after a scalar shift. The polynomial example (21) supplies the simpler exact-control benchmark.

## 9. Inherited polynomial-coordinate transport with the weaker certificate

Use the hypotheses of the supplied polynomial-coordinate transport packet: Φ_t and Ψ_t are mutually inverse polynomial automorphisms of R^d, Φ_0=id, their coefficients are C¹ in time, and both maps have common degree bounds on compact windows. Put

    v_t=(∂_tΦ_t)∘Ψ_t,       k_t=h_t∘Φ_t.

Suppose now that k_t satisfies (C1)–(C2), with the scalar shift and radial polynomial expressed in the pulled-back y coordinates. This replaces the earlier packet's instantaneous radial certificate.

For a normalized square-positive coordinatewise C¹ solution of

    L_t′(p)=L_t(v_t·∇p)−L_t(h_t p)+L_t(h_t)L_t(p),

define M_t(q)=L_t(q∘Ψ_t). Finite degree and coefficient regularity justify the ordinary finite-sum chain rule. Differentiating Ψ_t(Φ_t(y))=y gives

    ∂_t(q∘Ψ_t)+v_t·∇(q∘Ψ_t)=0.

Thus M_t satisfies the killing-only hierarchy for k_t, remains square-positive and normalized, and V_c applies. Consequently

    L_t(p)= ∫p(Φ_t(y)) exp(−∫_0^t k_u(y)du)dμ(y)
             / ∫exp(−∫_0^t k_u(y)du)dμ(y).              (22)

The converse follows from the same polynomial domination and differentiation argument. Every positive-time joint moment record is determinate: any other representative pushes back by the polynomial Ψ_t to a representative of the determinate M_t; polynomial absolute integrability follows from the even moments. Push forward again to identify the original representative. Gaussian integrability is asserted in the pulled-back coordinates, not automatically in the original nonlinear coordinates.

An explicit case outside both the instantaneous V hypothesis and the earlier transport packet's pulled-back instantaneous hypothesis is, for an integer m≥2,

    Φ_t(u,z)=(u,z+t u^m),    Ψ_t(x,y)=(x,y−t x^m),
    v_t(x,y)=(0,x^m),
    h_t(x,y)=[x+t(y−t x^m)]².

Here k_t(u,z)=(u+t z)², so (21) supplies precisely the cumulative pulled-back certificate. The flow is global and explicitly invertible; no general polynomial vector-field flow, nonpolynomial inverse, or finite-escape issue is being assumed away. The characteristic transfer itself is inherited and credited; the increment is its applicability to accumulated rather than instantaneous damping.

## 10. Boundaries, source inheritance, and evidence status

1. Square positivity is always used on an explicit SOS polynomial. Pointwise nonnegativity is not silently promoted to SOS. In particular, the Volterra remainder sign requires (C1), not only a nonnegative or coercive time integral.
2. The finite expansion is exact at every order and uses first derivatives only. Infinite-series equality is not assumed in obtaining the tail bound. Time derivatives of the energy would generally introduce extra terms and cannot replace this argument.
3. The theorem uses all polynomial-square tests and all moment equations. It supplies neither a finite test for realizability nor an effective oracle for the recovered law.
4. Cumulative rank in the energy is not a statement about the support or covariance of μ. For example μ=δ_b for any b∈R² yields L_t(p)=p(b) for either rank-one schedule above, with identically zero covariance. Its normalized hierarchy holds because its two reaction terms cancel. A law may remain on a point, line, or another thin support.
5. The mathematical hierarchy is conditional. No empirical observation model, psychological or noetic validation, hidden-label recovery, philosophical bearer identity, or physical applicability follows from resemblance to an accumulating-observation process.
6. Classical Nussbaum–Carleman representation and the Fourier/compact-test/initial-recovery method are inherited from V. The primary external theorem was re-inspected for this packet. The new proof step is the finite ordered Volterra SOS bound, its cumulative radial use, and the strict rank-one examples. The polynomial-coordinate transfer is inherited, with its weakened hypothesis proved here.

INPUT_BINDINGS.json binds copies of the immediate source results, their receipts, and inherited attribution records. SOURCE_CHECKS.md records the classical ingredient and local dependencies. The exact controls check source integrity, simplex symmetrization and residuals, radial SOS algebra, rank-one and integrated Gram identities, scalar-shift cancellation, characteristic pullback, atomic reaction identities, Fourier-error ratios, and the degenerate-support countercontrol. They supplement the universal written proof; they do not establish it by sampling or supply a proof-kernel verification. AUTHOR_RECEIPT.json records the actual executed checks and frozen file hashes. Independent assessment, if supplied separately, is not part of this author claim.
