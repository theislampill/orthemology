# Unrestricted-rank reverse lift for the radial quartic gradient hierarchy

10 October 2026 UTC. Additive ordinary mathematical research within ACTIVE T20. The parent proposed the radial-gradient candidate and participated in its proof development. This author packet is not independent review. No protected edit, integration, formal-kernel verification, field-priority claim, empirical/noetic identification, or T20 closure is asserted.

## 1. Result and exact hypotheses

Fix a finite dimension d≥1 and a nontrivial horizon 0<T≤∞. Put

    R(x)=|x|²,       F(x)=R(x)²/4,       b(x)=−∇F(x)=−R(x)x.

Let L_t be real linear functionals on all of P=R[x_1,…,x_d], for 0≤t<T. Assume that each polynomial coordinate is C¹, including a continuous right derivative at zero, and that for every p,q∈P,

    L_t(1)=1,               L_t(q²)≥0,
    L'_t(p)=−L_t(R x·∇p)−(1/4)L_t(R²p)
                               +(1/4)L_t(R²)L_t(p).        (H)

There is **no rank assumption**, no initial representing measure assumption, and no initial Carleman, compact-support, or exponential-tail assumption.

**Theorem.** There is exactly one Borel probability μ on R^d, with every absolute polynomial moment finite, such that the entire supplied path is

    Φ_t(x)=x/sqrt(1+2tR(x)),
    K_t(x)=R(x)/8 · [1−1/(1+2tR(x))],
    E_t(x)=exp(−K_t(x)),       Z_t=∫E_t dμ,
    L_t(p)= ∫p(Φ_t(x))E_t(x)dμ(x) / Z_t.                  (1)

At t=0 these formulas mean Φ_0=id, K_0=0, Z_0=1. Every positive-time full moment record is determinate. Its representing probability is carried by the **open** ball |y|²<1/(2t); its topological support is contained in the closed ball and can meet the boundary sphere as a limit set. In particular the boundary sphere has zero measure. The distinction between concentration in an open ball and topological support is important.

Conversely every probability μ with all absolute polynomial moments gives such a normalized square-positive C¹ hierarchy for all t≥0. For a fixed valid initial full moment functional c, all admitted paths with L_0=c are in bijection with the entire representing-law fibre of c. Thus initial moments determine a unique admitted path exactly when c is determinate. Different initial laws in one fibre give different full records at every positive time. Every supplied finite-horizon path has a unique extension to all t≥0 under this fixed generator.

For initially finite full Hankel rank, the entire path is consequently the unique finite-atomic evolution with constant rank, **without** a full-path rank promise. This is a particular nonlinear gradient model, not a result for all coercive polynomial gradients.

## 2. Ancestry and the actual increment

The directly inspected, hash-bound predecessors in INPUT_BINDINGS.json remain unchanged.

- complete-flow-finite-rank-20261010/RESULT.md, §9, already proves a forward-complete, lower-bounded-killing reverse lift under a locally uniform finite **full-path** rank bound. It explicitly includes the one-dimensional quartic gradient example and the same characteristic and weight formulas. Those formulas and the finite-rank theorem are inherited, not new credit here.
- joint-atomic-gradient-lift-20261010/RESULT.md connects that finite-rank theorem to genuine finite-dimensional atomic gradient geometry. It expressly leaves unrestricted-rank nonlinear gradient hierarchies unproved.
- polynomial-transport-continuation-20261010/RESULT.md already removes rank assumptions for supplied bounded-degree polynomial-automorphism characteristic paths whose pulled-back killing meets V. Our Φ_t is nonpolynomial at t>0, has a proper bounded image, and is not such an automorphism. That theorem cannot be applied directly.
- tensor-realizability-extension-20261010/RESULT.md and time-varying-square-positivity-20261010/RESULT.md supply prior pure-killing reverse-existence arguments, square-positive radial reasoning, Carleman existence, and initial-law-fibre distinctions. Their generators do not contain the present nonlinear transport.
- diffusive-coercive-realizability-20261010/RESULT.md supplies an analogous separation of positive-time existence, law-level PDE identification, and tight initial recovery for a different diffusion generator. We reuse that order of proof rather than assuming a measure PDE at the outset.

A bounded search of top-level RESULT.md reports for radial moment/gradient transport, geometric radial bounds, and unrestricted-rank gradient language located these ancestors but no existing instance of the theorem proved here. This is a local deduplication check, not an exhaustive literature search.

The incremental bridge is the geometric radial estimate in §3. It produces compact positive-time measures from the abstract full-square-positive hierarchy, so the finite-rank assumption is unnecessary for this specific nonlinear gradient system. Sections 5–7 then identify one initial law and exclude spurious boundary inflow.

## 3. Abstract radial inequalities and a geometric bound

All constructions in this section precede any representing measure. Set

    a(t)=exp(−(1/4)∫_0^t L_u(R²)du),
    A_t(p)=a(t)L_t(p),       a_n(t)=A_t(R^n),   n≥0.

The integral is finite on compact time intervals by coordinate continuity. Thus a>0, a(0)=1, and every A-coordinate is C¹. Unnormalization gives, with Gp=−R x·∇p−R²p/4,

    A'_t(p)=A_t(Gp).

Every R^n is SOS by its multinomial expansion, so a_n≥0. Euler's identity x·∇R^n=2nR^n gives the exact recurrence

    a_n'=−2n a_(n+1)−(1/4)a_(n+2),       n≥0.           (2)

In particular a_0=a is nonincreasing, 0<a≤1, and every a_n is nonincreasing. For j≥1 and 0≤s<t<T, integration gives

    a_j(s)≥2j∫_s^t a_(j+1)(u)du.                       (3)

For n≥2, apply (3) successively with j=1,…,n−1 over nested time intervals, dropping only nonnegative endpoint terms. The resulting simplex has volume (t−s)^(n−1)/(n−1)!, while the product of coefficients is 2^(n−1)(n−1)!. Monotonicity gives a_n(u)≥a_n(t) for its innermost time u≤t. Therefore

    a_1(s)≥[2(t−s)]^(n−1)a_n(t),       n≥1.             (4)

For n=1 this is simply monotonicity. Setting s=0 is legitimate because all these coordinates are C¹ through zero. With M=A_0(R)=L_0(R)≥0,

    0≤a_n(t)≤M(2t)^(1−n),        n≥1, t>0.             (5)

Only first derivatives and positivity of polynomial squares have been used. No assertion that a square-positive functional is positive on every nonnegative polynomial is needed. The factorial cancellation is exact; (5) is a geometric bound in moment degree, stronger than a factorial Carleman bound.

If M=0, (5) makes all positive radial moments at positive times zero. The following existence argument includes this case by interpreting zero even moments as infinite Carleman terms; it yields δ_0 at every time. There is no division by M or a possibly zero radial moment.

## 4. Positive-time existence, determinacy, and compact concentration

Fix t>0. R^n−x_i^(2n) is SOS, so

    0≤L_t(x_i^(2n))≤a_n(t)/a(t)
                      ≤[2tM/a(t)](2t)^(−n).            (6)

When M>0 and the moment is nonzero, its negative 1/(2n) power is at least

    sqrt(2t) · [2tM/a(t)]^(−1/(2n)),

which tends to sqrt(2t)>0. Every coordinate Carleman series therefore diverges. A zero even moment contributes +∞ in the usual convention.

The classical Nussbaum–Carleman existence-and-determinacy theorem supplies a unique representing probability ρ_t for L_t. Crucially, that theorem starts with a full positive-semidefinite multisequence and marginal Carleman conditions; it does not assume a vector measure. The primary statement is Putinar–Schmüdgen, *Multivariate Determinateness*, Theorem 25 and the following Nussbaum attribution, printed p.24, https://arxiv.org/pdf/0810.0840v1 . For d=1, use Hamburger existence plus Carleman uniqueness. The inherited primary PDF and its p.24 extraction are hash-bound; that page and the current primary web PDF statement were checked for this packet.

Put ν_t=a(t)ρ_t. It is the unique finite positive measure representing A_t. Let B=1/(2t). For any r>B, (5) and Markov's inequality give

    ν_t({R≥r})≤a_n(t)/r^n≤M B^(n−1)/r^n →0.

Taking a countable sequence r↓B shows ν_t({R>B})=0. Thus all positive-time laws have topological support in the closed ball R≤1/(2t). This step alone does **not** exclude mass on its boundary; §7 will do so.

On every interior time interval J=[s,t] with s>0, all ν_u have mass ≤1 and are supported in the same compact ball B_s={R≤1/(2s)}. Coordinate continuity and Stone–Weierstrass imply weak continuity of u↦ν_u there: approximate any continuous function on B_s uniformly by polynomials and use the uniform mass bound. This derives continuity of the actual laws, rather than assuming a measurable or continuous choice of representatives.

## 5. The polynomial hierarchy implies the actual weak PDE

Fix an interior compact interval J and a common ball B_s as above. We extend the integrated polynomial equation to smooth compactly supported tests.

For ξ∈R^d let P_N(x)=Σ_(j=0)^N(iξ·x)^j/j!. On B_s these polynomials and their first spatial derivatives converge uniformly to e^(iξ·x) and its derivatives. For instance ∂_iP_N=iξ_iP_(N−1), and the oscillatory exponential Taylor remainder for real ξ·x is bounded by |ξ·x|^(N+1)/(N+1)!. Since b and F are bounded on B_s, GP_N converges uniformly there to (i b·ξ−F)e^(iξ·x).

Apply the integrated identity

    ν_v(P_N)−ν_u(P_N)=∫_u^v ν_r(GP_N)dr

and let N→∞. Uniform mass bounds justify the limit. The result is the Fourier-test identity. Its right integrand is continuous by the weak continuity already proved.

For φ∈C_c∞(R^d), its Fourier transform satisfies ∫(1+|ξ|)|φ̂(ξ)|dξ<∞. On B_s the absolute generator integrand is at most sup_B_s|b|·|ξ|+sup_B_s F. Fourier inversion and Fubini therefore give

    ν_v(φ)−ν_u(φ)=∫_u^v ν_r(b·∇φ−Fφ)dr.              (7)

The right side has a continuous integrand. This is the weak conservative equation

    ∂_tν=−div(bν)−Fν

on positive times, derived from polynomial data only after representation was established. In particular no nonpolynomial flow substitution was made into an abstract functional.

We also use the following time-dependent test rule. If ψ_r is C¹ in time and smooth in space with a common compact support, with ψ_r, ∂_rψ_r and ∇ψ_r continuous uniformly there, then

    dν_r(ψ_r)/dr=ν_r(∂_rψ_r+b·∇ψ_r−Fψ_r).             (8)

To prove it, split the difference quotient into change of ψ and change of measure. Uniform differentiation of ψ and the bounded masses handle the first part; weak continuity handles its fixed limit ∂_rψ_r. Equation (7) handles the second part with ψ_r frozen at that time. This proves (8) without a general measure-transport theorem.

## 6. Explicit forward characteristics identify the positive-time evolution

The vector field b=−Rx is smooth and forward complete. Its explicit flow and integrated killing are Φ_τ and K_τ in (1), for τ≥0. Indeed

    R(Φ_τ(x))=R(x)/(1+2τR(x)),
    ∂_τΦ_τ(x)=−R(Φ_τ(x))Φ_τ(x),
    ∂_τK_τ(x)=F(Φ_τ(x)),
    Φ_(τ+σ)=Φ_τ∘Φ_σ,
    K_(τ+σ)(x)=K_σ(x)+K_τ(Φ_σ(x)).                    (9)

Thus E_(τ+σ)=E_σ(E_τ∘Φ_σ). These are direct identities, not a general completeness assumption smuggled in for polynomial fields.

For a bounded smooth terminal test f and fixed 0<s<t<T, define

    U(r,x)=E_(t−r)(x) f(Φ_(t−r)(x)),       s≤r≤t.

The identities (9), differentiated at a short initial step, imply the backward equation

    ∂_rU+b·∇U−FU=0.                                   (10)

All derivatives needed here are smooth on compact time-space sets, including at r=t. Choose a smooth compact cutoff χ equal to one on a neighborhood of B_s. Apply (8) to χU. On the supports of all ν_r the cutoff is one and its gradient is zero, so the integrand in (8) vanishes by (10). Consequently, for every f∈C_c∞,

    ν_t(f)=ν_s(E_(t−s) f∘Φ_(t−s)).

Compact smooth tests determine finite measures, yielding the exact law-level identity

    ν_t=(Φ_(t−s))_*[E_(t−s)ν_s],       0<s<t<T.         (11)

The cutoff is on the known common compact support of the measures; the nonpolynomial U is used only after (7) has extended the test algebra. This avoids the polynomial-automorphism restriction of the earlier theorem.

## 7. Recover the initial law and exclude an independent inflow

Coordinate continuity near zero bounds L_s(R^m) uniformly for every fixed m. In particular the represented probabilities ρ_s are tight as s↓0. Choose a sequence s_j↓0 with ρ_(s_j) converging weakly to a probability μ. Such a subsequence exists by the usual tightness compactness theorem on R^d. Since a(s_j)→1, the finite measures ν_(s_j) have the same weak limit.

Lower semicontinuity of each nonnegative radial power gives every radial moment of μ finite. Every polynomial p is uniformly integrable along this sequence: for degree m choose an integer k with 2k>m and use the uniform R^k bound to control the tails of |p|. More explicitly, outside |x|≤N, N≥1, |p(x)|≤C(1+|x|^m)≤2C N^(m−2k)|x|^(2k). Compact cutoffs, weak convergence and this bound show

    ∫p dμ=lim_j L_(s_j)(p)=L_0(p).                     (12)

Thus μ has all absolute polynomial moments and represents the initial functional. This proves existence; it does not assert that the initial moment record is determinate.

Fix t>0 and f∈C_c∞. For large j, s_j<t. The kernels

    g_j(x)=E_(t−s_j)(x) f(Φ_(t−s_j)(x))

are uniformly bounded by ||f||∞ because 0<E_τ≤1. They converge locally uniformly to g(x)=E_t(x)f(Φ_t(x)), which is bounded and continuous. Tightness of ν_(s_j), together with this uniform bound and local uniform convergence, permits passage through the varying integrands: on a fixed compact set use local uniform convergence and weak convergence; outside it use uniformly small mass. Passing (11) to the limit gives

    ν_t=(Φ_t)_*(E_t μ),       0<t<T.                    (13)

The same single subsequence proves (13) for every fixed t; no t-dependent choice of μ is made. Taking masses gives a(t)=Z_t, hence (1), and (12) supplies t=0.

For t>0 the map Φ_t is a homeomorphism from R^d onto the open ball

    O_t={y:|y|²<1/(2t)},

with inverse

    Ψ_t(y)=y/sqrt(1−2t|y|²),       y∈O_t.               (14)

Also E_t(x)>0 at every finite x. Thus (13) is injective on finite input measures: equality of outputs permits inverse pushforward by Ψ_t to identify E_tμ, then multiplication by the positive Borel function 1/E_t identifies μ. Its unboundedness causes no issue for equality of known positive measures; the inverse integrals are finite for actual inputs. In particular every candidate tight initial limit is the same μ. There is no independent hidden law entering from infinity.

Formula (13) further proves ν_t(O_t)=a(t), so its boundary sphere has zero measure. The topological support may still meet that sphere if the initial support is unbounded; we do not claim it lies in a strictly smaller compact ball.

The normalized map μ↦(Φ_t)_*(E_tμ)/∫E_t dμ is also injective on probabilities. If two normalized outputs agree, inverse pushforward gives E_tμ/Z_μ=E_tμ'/Z_μ'. Division by E_t gives proportional probability measures, whose total masses force the proportionality constant to be one. This stronger fixed-time injectivity is what identifies initial-law fibres in §9.

## 8. Converse and regularity through zero

Let μ be any probability with all absolute polynomial moments finite. For all t≥0, 0<E_t≤1 and |Φ_t(x)|≤|x|. Hence all weighted polynomial integrals in (1) are finite, and Z_t is strictly positive. On a compact time interval, a polynomial p of degree m satisfies

    |p(Φ_t(x))|≤C(1+|x|^m),
    |(b·∇p)(Φ_t(x))|≤C'(1+|x|^(m+2)),
    |F(Φ_t(x))p(Φ_t(x))|≤C''(1+|x|^(m+4)).

The last two terms dominate the time derivative of p(Φ_t)E_t. They are μ-integrable and independent of t on the chosen window. Dominated differentiation, with the continuous right derivative at zero, therefore gives

    dν_t(p)/dt=ν_t(b·∇p−Fp),       Z'_t=−ν_t(F).

The same domination and pointwise continuity give continuous derivatives. Normalizing by Z_t gives exactly (H), with normalization and every square test automatic from the positive law. This constructs the global path from each μ without a compact-support or initial tail-growth restriction.

## 9. Classification, finite initial rank, and actual gradient scope

The reverse and converse statements give a bijection between admitted paths and initial laws with all polynomial moments. Restricting to a fixed initial full moment functional gives precisely its representing-law fibre. By positive-time determinacy and normalized-map injectivity, different laws in that fibre have different full moment records at each t>0, even though their initial records agree. Initial moment determinacy is therefore exactly the condition for path uniqueness from the initial functional alone.

Any existing path on a nontrivial horizon identifies its unique μ, so (1) extends it to every t≥0. Any competing extension satisfies the same theorem and must have that μ, proving unique continuation of the supplied path. This does not conflate a supplied path with an unspecified member of an indeterminate initial fibre.

If the initial full Hankel rank is finite r, square positivity gives its unique r-atomic representing law by the inherited finite GNS theorem. Applying (1), its atoms move by Φ_t and have normalized positive weights proportional to their initial weights times E_t. Injectivity of Φ_t prevents collisions, and every weight stays positive at finite time. The full rank therefore remains r. Here the local uniform path rank bound is a **conclusion**, unlike the predecessor's hypothesis. No fixed truncated-rank condition is substituted for finite full rank.

This is genuinely a nonlinear gradient model: b=−∇F for F=|x|⁴/4. For a represented path the hierarchy gives the exact dissipation identity

    dL_t(F)/dt=−L_t(|∇F|²)−[L_t(F²)−L_t(F)²]
              =−L_t(R³)−Var_(ρ_t)(F)≤0.               (15)

For finite initial laws, the inherited atomic metric

    G((u,v),(u,v))=Σ_j u_j²/w_j+Σ_j w_j|v_j|²,
    Σ_j u_j=0,

makes these forced atom/weight equations the genuine negative gradient of Σ_jw_jF(x_j), as already proved by the joint-atomic ancestor. Removing the path-rank hypothesis in this particular example does not require reproving that metric theorem. For arbitrary infinite laws this packet establishes the measure dynamics and (15), not a new infinite-dimensional smooth Riemannian-manifold theorem.

### A direct large-time consequence

For every t>0, positive-time concentration gives

    0≤L_t(F)≤1/(16t²),        L_t(R)≤1/(2t).

Thus the probability laws converge weakly to δ_0 as t→∞. These uniform bounds follow from the shrinking ball, with no rate assertion for reconstruction of the initial law.

In initial coordinates, the normalized reweighted law E_tμ/Z_t converges in total variation to

    exp(−R/8)μ / ∫exp(−R/8)dμ.

Indeed K_t(x)→R(x)/8 pointwise, 0<E_t≤1, and dominated convergence gives L¹(μ) convergence of the weights and convergence of the strictly positive normalizers. Positions nevertheless collapse under Φ_t. Consequently every finite-time transition retains injective information, while the common weak limit δ_0 does not. These are elementary consequences of (1), not a separate convergence campaign or a stable inverse claim.

## 10. Limits and exact evidence

The characteristic map is nonpolynomial and forward-only onto a proper ball. On a nonzero ray its coordinates are bounded nonconstant functions of the starting coordinate, so cannot be polynomials. Its inverse exists only on O_t and blows up toward the boundary. Thus neither the polynomial-automorphism route nor two-sided complete-flow surjectivity applies.

The proof's crucial hypothesis remains full square positivity throughout time, with the exact hierarchy and C¹ boundary regularity. It does not derive positivity from arbitrary initial data, replace it by a finite collection of tests, or assert unrestricted reverse existence for every nonlinear or coercive gradient. Compactification here comes from the explicit coefficient 2n in (2). No general nonlinear-flow claim follows merely from naming characteristics or from differentiating energy.

Nor is every compact law in the closed ball a valid positive-time output: sphere mass is impossible, and even an interior law must have an inverse-weighted pullback that normalizes and possesses all polynomial moments. Injectivity is only an inverse on the actual range, not global surjectivity onto compact laws or a stable/effective reconstruction result.

The executable controls in check_exact.py verify radial generator identities, the nested-simplex factorial cancellation, flow/radius/killing/cocycle identities, backward-test cancellation, normalized finite-law algebra, inverse-image formulas, and the dissipation identity. They also retain exact controls for initial moment-fibre ambiguity and for the failure of polynomial-map/onto assumptions. These finite algebraic checks supplement the written universal argument; they do not prove it by enumeration or in a formal kernel. EXACT_CHECKS.json and AUTHOR_RECEIPT.json record the executed evidence and source preservation.
