# Exact moment dynamics for changing polynomial objectives

10 October 2026 UTC. Additive ordinary mathematical research. The parent proposed the uniform SOS-domination and backward-integration repair; the parent and investigator participated in its development and independently checked the Fourier-test continuation route. This is not independent review. The frozen autonomous packets remain unchanged. No field-priority, protected-edit, formal-kernel, empirical, or closure claim is made.

## 1. Result and exact time-dependent hypotheses

Fix 1≤d<∞ and 0<T≤∞. Let h_t(x) be a real polynomial in x for every t∈[0,T). On each compact time interval [0,H]⊂[0,T), assume there is a common finite degree bound D and continuous coefficient functions in that finite polynomial basis. Also assume there are constants c_H>0 and C_H≥0 such that, for every t∈[0,H],

    h_t(x)+C_H−c_H|x|² is a sum of polynomial squares.     (D)

No differentiability of the coefficients in time is required. The SOS decomposition itself need not be selected continuously or computably; its existence at each time is enough. The constants are uniform on the time window, including time zero. Pointwise coercivity of h_t alone is not substituted for (D).

Let L_t be real linear functionals on R[x_1,…,x_d]. Require that each monomial coordinate is C¹ on [0,T), with continuous right derivative at zero, and that

    L_t(1)=1,        L_t(q²)≥0 for every real q,
    L_t′(p)=−L_t(h_t p)+L_t(h_t)L_t(p),  p∈R[x].          (H)

**Theorem V.** There is exactly one probability μ on R^d, with every absolute polynomial moment finite, for which

    H_t(x)=∫_0^t h_u(x)du,
    L_t(p)=∫p(x)e^(−H_t(x))dμ / ∫e^(−H_t(x))dμ.          (1)

Every positive-time full moment record is determinate. Conversely every such initial μ gives a path satisfying (H) on the supplied time domain. For a fixed valid initial moment record, the admissible paths are in bijection with its full representing-law fibre. Thus the path identifies one actual law even when the initial moments alone do not.

If the prescribed energy family continues for all t≥0 and satisfies the same local-window assumptions, any finite-horizon path extends uniquely along that family. No continuation beyond an unspecified future energy schedule is asserted.

This covers continuously moving coercive quadratics, including h_t(x)=|x−b(t)|² for continuous b. It also permits higher-degree changing energies when (D) holds. It does not prove the same statement for every smooth time-varying coercive polynomial. The autonomous arbitrary-coercive theorem and this nonautonomous SOS-domination theorem have different hypotheses.

## 2. First-derivative inequalities replace even-time derivatives

Fix H<T and write c=c_H, C=C_H and g_t=h_t+C on [0,H]. Constants cancel from the normalized equation. Define

    a(t)=exp(−∫_0^t L_u(g_u)du),       A_t(p)=a(t)L_t(p).

Continuous coefficients and finitely many moment coordinates make L_t(g_t) continuous. Thus a is C¹, strictly positive, a(0)=1, and

    A_t′(p)=−A_t(g_t p).                                (2)

Only first derivatives are used. Put R=|x|² and a_n(t)=A_t(R^n). Since R^n is SOS, square positivity gives a_n≥0. The product of two SOS polynomials is SOS. Therefore (D) gives

    A_t(R^n(g_t−cR))≥0,
    a_n′(t)≤−c a_(n+1)(t)≤0,   n≥0.                   (3)

In particular 0<a_0(t)=a(t)≤1. These inequalities are obtained algebraically before any representing measure exists. We do not apply a merely square-positive functional to an arbitrary pointwise nonnegative polynomial.

Fix 0<δ≤s≤H. For b_n(v)=a_n(s−v), 0≤v≤δ, equation (3) gives b_n′≥c b_(n+1). Repeated integration and b_n(v)≥b_n(0) yield, for every N,

    Σ_(n=0)^N (cδ)^n a_n(s)/n! ≤ a_0(s−δ).               (4)

Explicitly, after N substitutions the residual term is

    c^N/(N−1)! ∫_0^δ (δ−v)^(N−1) b_N(v)dv,

which is at least (cδ)^N b_N(0)/N!. This proves (4), with N=0 following from monotonicity. Setting δ=s gives

    0≤a_n(s)≤n!/(cs)^n.                                (5)

There is no differentiation of h_t, no claim of higher time regularity, and no sign assertion for A_t″(q²). Those assertions would generally be false.

## 3. Positive-time vector measures and uniform Gaussian bounds

The multinomial expansion makes R^n−x_i^(2n) SOS. For s>0,

    0≤L_s(x_i^(2n))≤n!/[a(s)(cs)^n].                    (6)

Since n!≤n^n and a(s)>0, every marginal Hamburger Carleman series diverges. The classical multivariate Nussbaum–Carleman theorem therefore supplies a unique representing probability ρ_s on R^d. An inspected primary statement is Putinar–Schmüdgen, *Multivariate Determinateness*, Theorem 25 and its following attribution, printed p. 24, https://arxiv.org/pdf/0810.0840 . Its hypotheses are full square positivity and all marginal Carleman conditions; it does not assume a representing vector measure.

Set ν_s=a(s)ρ_s, the unique positive finite measure representing A_s. By monotone convergence of the exponential series and the full partial-sum estimate (4),

    ∫e^(csR)dν_s≤1.                                    (7)

On every compact interior time interval J=[η,H′] with η>0 and H′<H, the common rate r=cη>0 therefore gives

    ν_t(R^d)≤1,       ∫e^(r|x|²)dν_t≤1,    t∈J.          (8)

For every integer k≥0, the radial moment bound and Cauchy–Schwarz imply

    ∫|x|^k dν_t ≤ sqrt(k!) r^(−k/2),   t∈J.              (9)

Here k=0 is just the mass bound. The Gaussian integrability is derived from the hierarchy. It is not a tail assumption on an initial law, and no initial law has yet been selected.

## 4. Polynomial evolution extends to Fourier tests

We give this step explicitly because polynomial moment equations alone need not identify a measure evolution.

Fix ξ∈R^d and define

    P_N(x)=Σ_(k=0)^N (iξ·x)^k/k!,
    F_t(ξ)=∫e^(iξ·x)dν_t,
    G_t(ξ)=∫g_t(x)e^(iξ·x)dν_t.

Real functionals are extended complex-linearly. The real-variable Taylor remainder for e^(iy) satisfies

    |e^(iy)−Σ_(j=0)^(k−1)(iy)^j/j!|≤|y|^k/k!.           (10)

On J the polynomial coefficients give a finite bound |g_t(x)|≤B(1+|x|^D). Equations (9)–(10) show that A_t(P_N) converges uniformly on J to F_t(ξ), while A_t(g_tP_N) converges uniformly to G_t(ξ). For k=N+1, the derivative-side error is at most

    B|ξ|^k/k! [sqrt(k!)r^(−k/2)
                  +sqrt((k+D)!)r^(−(k+D)/2)].            (11)

Both terms tend to zero. For the second, the ratio of consecutive bounds is

    (|ξ|/sqrt(r)) sqrt(k+D+1)/(k+1) → 0.

The function-side estimate is the D=0 version. The convergence is also uniform for ξ in a compact set. Thus no integration of a divergent origin moment series is involved.

For each fixed polynomial P_N, (2) says

    dA_t(P_N)/dt=−A_t(g_tP_N).

Both sides are continuous in t. Uniform convergence of functions and first derivatives gives

    F_t′(ξ)=−G_t(ξ),   t∈J.                              (12)

In particular the relevant Fourier transforms are jointly continuous in t and ξ, by the uniform-on-compact series limits. No measurability or continuity of a chosen family of representing measures was silently assumed.

## 5. Compact tests identify the actual reaction equation

For φ∈C_c∞(R^d), its Fourier transform is integrable, and Fourier inversion writes φ as an integral of the tests in Section 4. On J,

    |F_t(ξ)|≤1,
    |G_t(ξ)|≤∫g_t dν_t=A_t(g_t)=−a′(t).

The last expression is nonnegative and uniformly bounded on J: g_t is pointwise nonnegative by (D), and the coefficients and moment coordinates are continuous. Therefore Fourier inversion, Fubini, and dominated differentiation give

    d/dt ∫φ dν_t = −∫g_t φ dν_t.                         (13)

The right side is continuous. This is a proved weak reaction equation, not an assumed law-level dynamics.

We also need its elementary time-dependent test rule. If ψ_t∈C_c∞ has a common compact spatial support, is C¹ in t in the uniform norm there, and its time derivative is a compact smooth spatial test, then

    d/dt ∫ψ_t dν_t = ∫(∂_tψ_t−g_tψ_t)dν_t.              (14)

To verify it, split the difference quotient into the change of ψ and the change of ν. Uniform differentiation of ψ, the bounded masses, and continuity from (13) for the fixed test ∂_tψ_t handle the first part. Equation (13) for the fixed test ψ_t handles the second. This does not require a general measurable-kernel construction.

For 0<s<t<H and a fixed φ∈C_c∞ choose

    ψ_u(x)=φ(x) exp(∫_s^u g_v(x)dv),   s≤u≤t.

On its compact support the exponent and all spatial derivatives are bounded on the time interval. Continuous polynomial coefficients make ψ_u uniformly C¹ in u, with ∂_uψ_u=g_uψ_u. Hence (14) gives

    ∫φ e^(∫_s^t g_u du)dν_t = ∫φ dν_s.                  (15)

The positive measures on both sides are locally finite; compact smooth tests determine them. Consequently

    ν_t=e^(−∫_s^t g_u du)ν_s,
    ν_s=e^( ∫_s^t g_u du)ν_t.                            (16)

The second equality includes finiteness of the inverse-weighted measure because its identified value is the already finite ν_s. Thus the full actual laws, rather than only their polynomial moments, obey the declared changing-objective update.

## 6. Recovering the initial law without initial representability

Fix s>0. Since g_u(x)≥0, the weights exp(∫_v^s g_u(x)du) increase pointwise as v↓0. Equation (16), monotone convergence, and coordinate continuity give

    ∫e^(∫_0^s g_u du)dν_s = lim_(v↓0)a(v)=1,
    ∫q²e^(∫_0^s g_u du)dν_s
        =lim_(v↓0)A_v(q²)=L_0(q²).                       (17)

Therefore

    μ=e^(∫_0^s g_u du)ν_s                                (18)

is a probability with every polynomial square integrable. The inequality |p|≤(1+p²)/2 and polarization recover all absolute and signed polynomial moments. There is no mass loss, infinite initial measure, or assumed initial representative.

Equation (16) now gives ν_t=e^(−∫_0^t g_u du)μ at every positive t in the window. Dividing by its mass removes the added constant C and gives (1), including zero by (17).

If two laws generated the same full path, their normalized laws at any positive time would have the same moment record. That record is determinate by Section 3, so those tilted laws coincide. Undoing the known positive likelihood and normalizing recovers the same initial probability. This proves uniqueness and independence of the positive time or time-window constants used in the construction. Overlapping finite windows therefore recover one common μ.

Conversely, for any initial μ with all polynomial moments finite, (D) implies H_t(x)≥−Ct on a finite window. Thus e^(−H_t) is bounded above there, and every weighted polynomial integral is finite. The bounded polynomial coefficients provide an integrable polynomial bound for its time derivative, so dominated differentiation proves (H) and C¹ regularity through zero. This also proves existence for every law in an initial moment fibre. Positive-time determinacy and reversible normalization make the law-to-path correspondence injective, yielding the stated classification.

## 7. Changing quadratics and the retained failed proof step

For any continuous b:[0,T)→R^d and h_t(x)=|x−b(t)|², choose on a finite window

    c=1/2,       C=max_(0≤t≤H)|b(t)|².

Then

    h_t+C−(1/2)|x|²
       =(1/2)|x−2b(t)|²+C−|b(t)|²                       (19)

is SOS for each t. More generally, continuously varying positive-definite quadratic forms have a uniform positive smallest eigenvalue on each compact window; completing the square and choosing a sufficiently large constant gives (D). The theorem therefore handles genuinely changing quadratic shapes and centres, not only scalar reparametrizations of one fixed energy.

The earlier central-even-derivative obstruction remains correct. For h_t(x)=(x−t)² and μ=(δ_(−1)+δ_0)/2, the actual tilt has changing atom ratio e^(−t−t²). Its unnormalized second derivative contains h_t²−∂_t h_t, not just h_t².

The failure persists even with the particular SOS shift used by the repair. On [0,1/5] choose C=1/25 and c=1/2 in (19). At the interior time t=1/10, for g_t=h_t+C,

    g_t(−1)²−∂_t g_t(−1)=−51/80,
    g_t(0)²−∂_t g_t(0)=−79/400.

Both atom weights are positive, so the shifted A_t″(1) is strictly negative. The radial inequalities (3) nevertheless hold. Thus the new proof succeeds where the old even-time-derivative sign argument fails; it does not retract that exact countercontrol or reinterpret it as a failure of realizability.

## 8. Scope and inheritance

The finite-channel ancestor explicitly allows externally changing objective covectors and continuous moment paths across switches. The previous additive result already covers finite switching among distinct coercive energies by applying the autonomous theorem segment by segment and using determinate switch records. This packet addresses a genuinely continuous changing-objective interface under (D), rather than repeating that composition corollary.

The autonomous arbitrary-coercive result uses a different central-time and compact-fibre argument. That argument cannot simply be differentiated through time-dependent h_t. Here full polynomial-square positivity, an explicit uniform SOS radial certificate, and first-derivative inequalities supply Gaussian integrability instead. Merely knowing each h_t is coercive does not supply that certificate, and no such unrestricted nonautonomous theorem is claimed.

Classical Nussbaum–Carleman existence, Fourier inversion, and ordinary measure identification remain external mathematical ingredients. The backward inequalities, uniform Fourier approximation bounds, compact integrating-factor argument, and initial recovery are written out for this application. No computational complexity, finite square-test cutoff, empirical verification, noetic identification, hidden-label recovery, or metaphysical conclusion is asserted. The tensor record is the symmetric moment hierarchy of a fixed finite-dimensional numerical vector.

The copied ancestry and its hashes are in INPUT_BINDINGS.json. Exact executed controls supplement, rather than establish, the universal proof; they test the Volterra/simplex factors, radial SOS algebra, moving-quadratic reaction identities, compact integrating-factor cancellation, and the retained strict negative-even-derivative example. No general measure-reconstruction implementation or proof-kernel verification is claimed.

The author run passed 23 exact checks, including five input-integrity checks; the remaining checks are the focused algebraic controls described above. See check_controls.log and CONTROL_RESULTS.json.
