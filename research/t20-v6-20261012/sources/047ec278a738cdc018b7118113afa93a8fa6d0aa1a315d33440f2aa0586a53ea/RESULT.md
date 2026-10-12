# One hidden coordinate: a whole-law lift under cumulative quadratic damping

10 October 2026 UTC. Additive ordinary mathematical research. The parent proposed the nonautonomous gap, the local Volterra-remainder bridge, the signed-projection identification, and the conditional-determinacy discriminator. This investigator supplied and checked the detailed arguments and controls. These are author-side contributions, not independent review. No protected file, accepted predecessor, integration target, or closure status is changed.

## 1. The statement

Let x=(z,y)∈R^r×R with r≥1, and let 0<T≤∞. On [0,T), let Q_t be a continuous real symmetric positive-semidefinite r×r matrix. Put

    g_t(z)=zᵀQ_tz,   R(z)=|z|²,
    K_(s,t)(z)=∫_s^t g_u(z)du,   K_t=K_(0,t).

Assume that for every t>0 there is c(t)>0 such that

    K_t(z)−c(t)R(z) is SOS.                           (C)

Equivalently, ∫₀ᵗQ_u du is positive definite. No regularity of c, uniform ellipticity of Q, or lower bound c(t)/t near zero is assumed. The controlled subspace is fixed; the energy never depends on y.

Let L_t be real linear functionals on all R[z,y], with all monomial coordinates C¹ through zero, normalized and square-positive, satisfying

    L_t(1)=1,  L_t(q²)≥0,
    L_t′(p)=−L_t(g_t p)+L_t(g_t)L_t(p).               (H)

No representing measure at any time is assumed.

**Theorem.** There exists μ∈P∞(R^(r+1)), a probability with every absolute polynomial moment, such that for every 0≤t<T and every polynomial p,

    L_t(p)=∫p e^(−K_t)dμ / ∫e^(−K_t)dμ.              (1)

More strongly, for any fixed s∈(0,T), every representative ρ of L_s gives a whole-path lift by

    μ=a(s)e^(K_s)ρ,
    a(t)=exp(−∫₀ᵗ L_u(g_u)du).                     (2)

This is a bijection from the representing-measure fibre of L_s onto the set of whole-path lifts. Its inverse is the normalized tilt at s. In particular, a path has a unique lift exactly when its full moment record is determinate at one, equivalently every, positive time. Positive-time determinacy is not assumed and is not automatic.

For μ,ν∈P∞ define finite signed measures on R^r by

    m_(μ,j)=π_z*(y^j μ),  j=0,1,2,… .               (3)

Two initial laws generate the same full hierarchy path exactly when

    m_(μ,j)=m_(ν,j) for every j≥0.                  (E)

In fact equality of their normalized full moment record at any one positive time is equivalent to (E). The relation is independent of the particular schedule Q satisfying (C), as long as the controlled subspace is the same.

Consequently every admissible path has a unique continuation **as moment coordinates** along a supplied continuous PSD quadratic schedule in the same z variables. Its initial-law lift need not be unique. Nothing here selects an unspecified future energy or gives uniqueness after changing the controlled subspace or adding dependence on y.

The r=0 edge is the scalar Hamburger problem: g=0 forces a stationary path; any representing probability of L₀ is a lift. Its law need not be unique. The rest of the proof assumes r≥1.

## 2. Inherited bounds and positive-time existence

Define a and A_t=a(t)L_t as in (2). These are well-defined using only the supplied first derivatives and continuity of Q. Then

    A_t′(p)=−A_t(g_t p),   A_t(1)=a(t),
    a(0)=1,   0<a(t)≤1.                              (4)

The exact finite backward Volterra expansion from the cumulative predecessor gives, for every polynomial q and N≥0,

    A₀(q²)≥∑_(n=0)^N A_t(q²K_t^n)/n!.

Because K_t−c(t)R is SOS and products of SOS polynomials are SOS,

    K_t^n−c(t)^nR^n
      =(K_t−c(t)R)∑_(j=0)^(n−1)K_t^(n−1−j)(c(t)R)^j

is SOS. Thus

    ∑_(n=0)^N c(t)^n A_t(q²R^n)/n!≤A₀(q²).          (5)

In particular A_t(z_i^(2n))≤n!c(t)^(−n), and the r controlled marginal moment sequences satisfy Carleman's divergent-series condition after division by a(t). Since r=d−1, Putinar–Schmüdgen, *Multivariate Determinateness*, Theorem 25, printed p.24, supplies a representative of L_t for every t>0. The theorem starts from full positive semidefiniteness and requires Carleman in d−1 marginals for existence; it does not claim uniqueness without an additional condition. The predecessor's version-specific source and exact p.24 text are retained in the input bindings.

If ν_t is **any** finite positive representative of A_t, monotone convergence in (5) gives

    ∫q²e^(c(t)R)dν_t≤A₀(q²).                        (6)

No representative has been selected as a function of time. For each fixed q and n, q²R^n g_u is SOS, so

    dA_u(q²R^n)/du=−A_u(q²R^n g_u)≤0.               (7)

Fix an interior window J=[η,H]⊂(0,T). Set c=c(η)>0. Equations (5) and (7) imply, uniformly for u∈J,

    0≤A_u(q²R^n)≤n!c^(−n)A₀(q²),                  (8)
    ∫q²e^(cR)dν_u≤A₀(q²)                          (9)

for every representative ν_u. These are weighted Gaussian estimates only in z. No Gaussian or Carleman estimate for y has been introduced.

## 3. The nonautonomous local bridge, including both time orderings

Let C≥0 satisfy Q_u≤CI for u∈J. Such a C exists by compactness and coefficient continuity. Hence B=CR and B−g_u are SOS. For any m≥1 and times u₁,…,u_m∈J,

    B^m−∏_(j=1)^m g_(u_j)
      =∑_(i=1)^m B^(m−i)(B−g_(u_i))∏_(j<i)g_(u_j)   (10)

is SOS. Multiplying by q² and applying (8) gives

    0≤A_v(q²∏g_(u_j))
      ≤C^m A_v(q²R^m)
      ≤m!(C/c)^m A₀(q²)                             (11)

for all v,u_j∈J. This is an SOS comparison, rather than an unsupported inference from pointwise nonnegativity.

For s≤t in J, write δ=t−s, K=K_(s,t), and Δ_m={s≤u₁≤⋯≤u_m≤t}. Repeated fundamental-theorem-of-calculus substitutions give the two **finite exact** identities, for every polynomial p and m≥1:

    A_s(p)=∑_(k=0)^(m−1) A_t(pK^k)/k! + E_m⁻,
    E_m⁻=∫_(Δ_m) A_(u_m)(p∏_(j=1)^m g_(u_j))du;     (12)

    A_t(p)=∑_(k=0)^(m−1) (−1)^k A_s(pK^k)/k! + E_m⁺,
    E_m⁺=(−1)^m∫_(Δ_m) A_(u₁)(p∏_(j=1)^m g_(u_j))du. (13)

The backward remainder is evaluated at the latest simplex time u_m; the forward remainder is evaluated at the earliest time u₁. For (12), expand an intermediate A_v using A_v=A_t+∫_v^t A_w(g_w·)dw. For (13), expand it using A_v=A_s−∫_s^v A_w(g_w·)dw. At each substitution all previously selected g's are frozen polynomials. The terminal integrands are symmetric because polynomial multiplication commutes, so cube partitioning gives the factor 1/k!. No matrix-commutativity assumption is involved.

At each finite m, all integrands use one finite-dimensional polynomial space and are jointly continuous in their time variables. Thus ordinary Fubini and coefficientwise integration are valid. No infinite-series claim enters (12) or (13).

For p=q², (11) and vol(Δ_m)=δ^m/m! give

    0≤E_m⁻≤A₀(q²)(Cδ/c)^m,
    |E_m⁺|≤A₀(q²)(Cδ/c)^m.                          (14)

If Cδ<c, both remainders tend to zero. If C=0, g vanishes on J and the identities are immediate.

### Backward weighting of an arbitrary endpoint representative

Let ν_t represent A_t. The nonnegative series and (12)–(14) show

    ∫q²e^K dν_t=∑_(k≥0)A_t(q²K^k)/k!=A_s(q²).      (15)

Thus e^Kν_t has finite mass and all squared polynomial moments. Since |p|≤(1+p²)/2, it has every absolute polynomial moment. Polarization

    p=((p+1)²−(p−1)²)/4

then shows that e^Kν_t represents A_s.

### Forward weighting of an arbitrary starting representative

Let ν_s represent A_s. Since 0≤K≤CδR and Cδ<c, (9) gives an integrable majorant q²e^K. The absolute value of every partial exponential sum is at most e^K. Dominated convergence and (13)–(14) therefore give

    ∫q²e^(−K)dν_s
      =∑_(k≥0)(−1)^k A_s(q²K^k)/k!=A_t(q²).         (16)

Polarization gives every polynomial. Hence e^(−K)ν_s represents A_t.

The forward argument is essential. Backward weighting alone would show that an endpoint representative extends to earlier times, but would not show that an arbitrarily chosen earlier representative gives the already prescribed later moments. Equations (15)–(16) prove both directions without positive-time joint determinacy.

## 4. Patching and the boundary at zero

Any compact interval [s,t]⊂(0,T) has a finite partition with all lengths satisfying Cδ<c, using one earlier interior η≤s and the uniform constants above. Apply (15) or (16) successively. At each intermediate time the propagated measure is a representative, and so (9) applies to it automatically. Multiplication of likelihoods yields

    ν_u=e^(K_s−K_u)ν_s                              (17)

as a representative of A_u for every u∈(0,T), for any one fixed representative ν_s of A_s. This constructs a consistent family from that one measure; it does not assert that independently selected representatives at different times coincide.

Let u↓0 through times below s. Because every g_t≥0, K_s−K_u increases pointwise to K_s. For every polynomial q, (17), monotone convergence, and boundary continuity give

    ∫q²e^(K_s)dν_s=lim_(u↓0)A_u(q²)=A₀(q²).         (18)

For q=1 the mass is one. Set μ=e^(K_s)ν_s. Equation (18), |p|≤(1+p²)/2, and polarization show μ∈P∞ and ∫p dμ=L₀(p). Equation (17) gives

    A_u(p)=∫p e^(−K_u)dμ

for every positive u, and (18) gives the same at zero. The normalizer is exactly a(u). This proves (1) and the existence assertion.

Conversely, any μ∈P∞ produces an admissible path. On every compact time window e^(−K_t)≤1 and |g_t|≤CR. An integrable polynomial majorant controls each derivative of ∫p e^(−K_t)dμ, including the right derivative at zero. Dominated differentiation gives (H) and coordinate C¹ regularity. The denominator is strictly positive at each finite time.

If μ lifts the specified path, its normalizer Z(t)=∫e^(−K_t)dμ obeys Z′=−L_t(g_t)Z and Z(0)=1. Therefore Z=a. Its positive-time tilt and (2) are inverse maps. This proves the asserted bijection of representative fibres and whole-path lifts. In particular all positive-time fibres have the same cardinality; determinacy at one time is equivalent to determinacy at every positive time and to uniqueness of the whole-path lift.

## 5. Exact law equivalence: the controlled-variable signed moment measures

The measures in (3) are finite signed measures because ∫|y|^j dμ<∞. They retain the distribution of the controlled coordinates together with every hidden conditional moment.

First assume (E). Every polynomial has a finite expansion p(z,y)=∑_j p_j(z)y^j. Since K_t depends only on z,

    ∫p e^(−K_t)dμ=∑_j∫p_j(z)e^(−K_t(z))dm_(μ,j)(z).

All terms are absolutely integrable. Condition (E) makes them identical for μ and ν, including p=1. Hence their normalized paths coincide for any supplied nonnegative z-only schedule.

For the converse, an even stronger statement is useful. Suppose the normalized full moment records of two P∞ laws coincide at a single s>0. Write ρ_μ=e^(−K_s)μ/Z_μ and ρ_ν=e^(−K_s)ν/Z_ν for those probability laws. For every j≥0 consider

    σ_(μ,j)=π_z*(y^jρ_μ),  σ_(ν,j)=π_z*(y^jρ_ν).

They have the same z-polynomial moments. They also have Gaussian total-variation control: with c=c(s),

    ∫e^(cR)d|σ_(μ,j)|
      ≤Z_μ^(−1)∫|y|^j e^(cR−K_s)dμ
      ≤Z_μ^(−1)∫|y|^j dμ<∞,                       (19)

and likewise for ν. The inequality uses the usual bound of weighted pushforward variation by the pushforward of |y|^jρ.

A finite signed measure on R^r with such an exponential bound is determined by its polynomial moments. Indeed e^(|ξ||z|) is integrable for every ξ; dominated Taylor expansion computes its Fourier transform from those moments. Equal moments give equal Fourier transforms, and uniqueness of the Fourier transform of finite signed measures gives equal measures. Consequently σ_(μ,j)=σ_(ν,j) for every j.

Removing their common positive factor gives

    m_(μ,j)/Z_μ=m_(ν,j)/Z_ν.                         (20)

This multiplication by e^(K_s) is legitimate for signed measures because both resulting measures have finite total variation, bounded by their original |y|^j moments divided by Z. For j=0, taking total mass in (20) gives Z_μ=Z_ν. Thus (E) holds. In particular equality of an entire normalized path implies (E).

No uniqueness of the joint law on (z,y) was used. The uniquely determined objects were signed measures on the controlled z-space. This distinction is what permits identification of moment paths despite hidden-law ambiguity.

## 6. Continuation and a useful sufficient uniqueness criterion

Let a path be given on [0,T), and extend the supplied Q continuously and PSD to [0,T′), T′>T, in the same z coordinates. Existing cumulative positivity persists at all later times because the added quadratic is PSD. Any lift μ defines an extension by (1). Any two lifts satisfy (E), so they define the same extended moment coordinates. Conversely any admissible extension has a lift by this theorem, and its restriction is a lift of the original path. Thus the moment-coordinate extension is unique in the full normalized square-positive class.

There is also a useful sufficient criterion for a particular path to have a unique law. The conditional-determinacy principle is classical, with a precise primary disintegration treatment in Putinar–Schmüdgen, Section 8, Proposition 28 and Theorem 31 (printed pp.29–31); the application here uses the already identified signed measures (E). Theorem 31 itself assumes a strictly determinate base; here that extra zero-time hypothesis is unnecessary because equality of the entire signed projections has already been proved (or the classical mechanism can be applied at positive time). Suppose one lift μ disintegrates as

    μ(dz,dy)=m_(μ,0)(dz) κ_z(dy),

and κ_z is a determinate one-variable moment law for m_(μ,0)-almost every z. If another lift ν exists, (E) fixes its z marginal. Its conditional y moments equal those of κ_z almost everywhere for every j; a countable union of null sets gives one common full-measure set on which all moments agree. All conditional absolute moments are finite there by global polynomial integrability. Conditional determinacy then identifies the conditional laws and hence ν=μ.

This is a sufficient criterion only. No necessity statement requiring a measurable selection of alternate conditional laws is made. It is the conditional hidden moment problem that matters; hidden marginal determinacy is not necessary.

### A unique joint law with a moment-indeterminate hidden marginal

Let Z be standard Gaussian, let Y=e^Z, and let μ be the law of (Z,Y). All mixed absolute polynomial moments are finite. The hidden Y marginal is the standard lognormal and is moment-indeterminate. Nevertheless μ is the unique law in its class (E), since its conditionals are point masses.

There is an elementary direct check. Here

    m₀=γ,   m₁=e^zγ,   m₂=e^(2z)γ.

Any ν with these three signed projections satisfies

    ∫(y−e^z)²dν
      =∫y²dν−2∫e^z y dν+∫e^(2z)dν=0.

All terms are finite: the cross term is integrable by Cauchy–Schwarz from ∫y²dν<∞ and ∫e^(2z)dν=∫e^(2z)dγ<∞. The three projection identities make the right side e²−2e²+e². Thus ν is supported on y=e^z, and m₀ fixes its law exactly. For example g_t(z)=(1+t)z² is a nonconstant admissible schedule and yields a unique whole-path lift, even though every positive-time hidden marginal remains a nondegenerate lognormal and therefore moment-indeterminate.

### Ambiguous lifts really occur

The inherited lognormal Stieltjes pair

    f(y)=exp(−(log y)²/2)/(y√(2π)), y>0,
    ν_±(dy)=f(y)[1±(1/2)sin(2πlog y)]dy

has the same moments of all nonnegative integer orders and consists of distinct laws. Let η_±=(ν_±+γ₁)/2 and μ_±=γ_r⊗η_±. These are distinct full-support laws in P∞ with the same measures m_j, so they generate the same full hierarchy for every schedule in this theorem. No positive-time joint determinacy can be inferred just from the one-hidden-coordinate hypothesis.

## 7. A genuinely partial, nonautonomous control

Take r=2 and one hidden coordinate y, with

    g_t(z₁,z₂)=(z₁+t z₂)²,
    Q_t=[[1,t],[t,t²]],
    K_t=t z₁²+t²z₁z₂+(t³/3)z₂².

Every Q_t has rank one, while det(∫₀ᵗQ_u du)=t⁴/12>0 for t>0. The inherited explicit certificate is

    c(t)=t³/[4(t²+3)],
    a_t=3t(t²+4)/[4(t²+3)],
    K_t−c(t)(z₁²+z₂²)
      =a_t[z₁+2t(t²+3)z₂/(3(t²+4))]²
        +t⁵z₂²/[12(t²+3)(t²+4)].                    (21)

There is no cumulative coercivity in the full (z₁,z₂,y) space, because every energy vanishes on the y axis. Thus the full-dimensional V_c theorem does not apply. Nor is this a fixed autonomous partial quadratic. The present theorem applies and recovers one whole-path law for every admissible full hierarchy. Choosing γ₂⊗η_± above makes the absence of universal law identification explicit in the very same nonautonomous example. Also Q₀Q₁≠Q₁Q₀: the local proof depends on commutativity of scalar polynomial multiplication, not commutativity of the quadratic matrices.

## 8. Scope, inheritance, and separate generalization

The new bridge here is the exact two-direction nonautonomous local exponential identity with a controlled Volterra remainder, followed by propagation of **every** positive-time representative. The cumulative weighted bounds and d−1-marginal existence theorem are inherited. The autonomous analyticity argument is neither used nor credited again. Full-dimensional Fourier uniqueness is not applied to the joint measure.

The exact signed-projection relation and its schedule-independent continuation consequence are proved in Sections 5–6. The conditional-determinacy principle is classical and is applied here after the signed-projection identification; it is not claimed as a new general criterion. The elementary lognormal ambiguity and the active rotating/rank-one example come from the accepted predecessor ingredients; their role here is to discriminate existence from identification in the new nonautonomous setting.

GENERAL_SOS_BRIDGE.md separately proves a broader fixed-controlled-subspace statement for continuous, locally degree-bounded SOS polynomials g_t(z) satisfying the same partial cumulative certificate. It uses Fourier uniqueness only for the signed projections on z, where the weighted Gaussian estimate is available. Its proof does not use the quadratic domination g_t≤CR or the local remainder decay, and those quadratic estimates must not be applied to higher-degree energies.

The arguments concern full commutative polynomial moment hierarchies, not finite cutoffs. They provide no effective reconstruction, hidden-law selection algorithm, empirical identification claim, field-priority claim, or proof-kernel certification. The accumulated certificate must hold from zero to every positive time. Cross-hidden energies, moving controlled subspaces, and unspecified future schedules are outside these claims. Only ordinary universal proofs, supported by finite exact controls, are asserted.

SHARP_HIDDEN_BOUNDARY.md separately proves that two or more hidden coordinates admit a strictly square-positive nonmoment hierarchy for every supplied schedule in the broader SOS class, by tensoring the bound full nonmoment functional with a genuine Gaussian-killed active measure. That construction is a new author-side application of the inherited full-functional input, not a claim that the input itself is a probability law.
