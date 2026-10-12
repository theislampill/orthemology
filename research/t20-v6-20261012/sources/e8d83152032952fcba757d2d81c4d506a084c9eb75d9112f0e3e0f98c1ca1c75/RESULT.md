# Reverse existence for diffusion with quadratic killing

10 October 2026 UTC. Additive ordinary mathematical research. Earlier packets are copied and hash-bound, not changed. The parent independently checked the endpoint Fourier factorization, the maximum-principle barrier, and the order of the recovery argument; this is participating proof development, not independent review of the complete theorem. A separate narrow check of the radial argument is recorded separately. No protected edit, integration, field-priority, formal-kernel, empirical, or T20-closure claim is made.

## 1. Outcome and exact hypotheses

Fix 1≤d<∞ and 0<T≤∞. Write R(x)=|x|². Suppose real linear functionals L_t on R[x_1,…,x_d] have coordinatewise C¹ dependence on t∈[0,T), including continuous right derivatives at zero, and satisfy, for every real polynomial p and q,

    L_t(1)=1,                  L_t(q²)≥0,
    L_t′(p)=L_t(Δp−Rp)+L_t(R)L_t(p).                    (H)

**Theorem D.** There is exactly one probability μ on R^d, with all absolute polynomial moments finite, whose normalized quadratic-killed heat evolution gives the entire path (H). More explicitly, for t>0 put

    v_t=tanh(2t),       c_t=sech(2t),       C_t=(cosh(2t))^(−d/2),
    K_t(x,y)=(2π sinh(2t))^(−d/2)
       ×exp(−[cosh(2t)(|x|²+|y|²)−2x·y]/[2sinh(2t)]),
    ν_t(dx)=[∫K_t(x,y)dμ(y)]dx.

Then

    L_0(p)=∫p dμ,
    L_t(p)=∫p dν_t / ν_t(R^d),                    0<t<T. (1)

Every positive-time moment record has a unique representing probability. Conversely, every initial probability with all polynomial moments finite supplies a path satisfying (H), globally for t≥0. Thus any path on a nontrivial finite horizon extends uniquely, and paths with a fixed valid initial moment record are in bijection with that record's representing-law fibre. An indeterminate initial moment record need not determine a unique path.

In particular, the answer to the narrow question is positive. Representability is **not** installed by assuming a Feynman–Kac or Mehler formula for an abstract functional. It is first derived from a radial Riccati estimate and the classical Nussbaum–Carleman existence theorem. Kernel identification is a subsequent, separate argument.

This theorem is for constant Euclidean diffusion and the coercive quadratic killing R. It does not establish the claim for every coercive polynomial killing, arbitrary polynomial diffusion, or arbitrary nonautonomous generator. Full square positivity throughout the time interval is required; no finite square-test cutoff is claimed.

## 2. Unnormalization and the exact radial recurrence

Define

    a(t)=exp(−∫_0^t L_u(R)du),       A_t(p)=a(t)L_t(p),
    a_n(t)=A_t(R^n),                 n≥0.

These are defined before any measure. Each R^n is SOS by its multinomial expansion. Therefore a_n≥0, a_0=a>0, and

    A_t′(p)=A_t(Δp−Rp),
    a_0′=−a_1≤0,              a_0(0)=1,              0<a_0≤1.

For n≥1 the polynomial identity ΔR^n=2n(2n+d−2)R^(n−1) gives

    a_n′=b_n a_(n−1)−a_(n+1),       b_n=2n(2n+d−2)>0. (2)

The symbol b_n here is a constant, not a moment or a time-dependent root.

The positive diffusion term in (2) is essential. For the actual initial law δ_0, a_1′(0)=2d>0. Thus Theorem V's monotonic radial inequality cannot simply be carried over. Also A_0″(1)=−2d for this law: Theorem G's pure-killing even-time-derivative positivity is unavailable as well. Neither failed transplant disproves the present theorem.

## 3. Radial interpolation uses only polynomial squares

For any fixed t, square positivity gives Cauchy–Schwarz for the semidefinite bilinear form (f,g)↦A_t(fg). Its direct-sum version gives the same inequality for finite lists of polynomials.

For an odd index n=2k+1, apply Cauchy–Schwarz to R^k and R^(k+1). For an even index n=2k≥2, apply its direct-sum version to

    f_i=x_iR^(k−1),       g_i=x_iR^k,       1≤i≤d.

The relevant three sums are R^(2k−1), R^(2k), R^(2k+1). Hence in both cases

    a_n²≤a_(n−1)a_(n+1),                         n≥1.  (3)

No vector measure or unjustified positivity on all nonnegative polynomials has been used. Equivalently, the radial restriction is Stieltjes-positive, since A_t(v(R)²)≥0 and A_t(Rv(R)²)=Σ_i A_t((x_iv(R))²)≥0; but no univariate representation theorem is needed for (3).

To include possible zero moments, temporarily replace A_t by A_t+ε ev_z for a fixed |z|=1 and ε>0. All its radial moments a_n+ε are positive, and (3) makes their logarithms discretely convex. Comparing a point to the chord from index 0 to index n, then letting ε↓0, gives

    a_(n−1)≤a_0^(1/n)a_n^((n−1)/n),
    a_(n+1)≥a_n^((n+1)/n)/a_0^(1/n).                  (4)

For n=1 the first inequality is equality, including when a_1=0; its zero exponent is understood directly as that equality. The second inequality follows from the analogous chord comparison at index n between indices 0 and n+1. The regularization is only a static proof device; it is not asserted to solve the hierarchy.

In fact a_n(t)>0 for all n≥1 and every interior t>0. If a_n(t)=0, the same chord interpolation implies a_1(t)=0. Since a_1=Σ_i A_t(x_i²), all A_t(x_i²)=0. Cauchy–Schwarz then gives A_t(x_i p)=0 for every polynomial p, so all positive-degree radial moments vanish. Equation (2) at n=1 yields a_1′(t)=2d a_0(t)>0. This contradicts the zero derivative at an interior minimum of the nonnegative C¹ function a_1. This step justifies differentiating roots only in the interior, never unchecked across a zero.

## 4. The Riccati bound supplies the missing moment growth

Using (4) and 0<a_0≤1 in (2),

    a_n′≤b_n a_n^((n−1)/n)−a_n^((n+1)/n).

For t>0 put u_n(t)=a_n(t)^(1/n). The preceding positivity makes u_n C¹, and

    u_n′≤(b_n−u_n²)/n.                                (5)

For any 0<s<t<T the scalar comparison equation y′=(b_n−y²)/n has the infinite-initial-value upper barrier

    Y_s(t)=√b_n coth(√b_n(t−s)/n).

To see the comparison without assigning an infinite initial value, fix s and start at s+ε. As ε↓0 the barrier there exceeds the finite continuous u_n; ordinary scalar comparison then applies. A first upward crossing is impossible. Thus u_n(t)≤Y_s(t). Let s↓0 to obtain

    a_n(t)≤[√b_n coth(√b_n t/n)]^n.                    (6)

This bound is independent of the initial high moments, even though those moments may be arbitrarily large. The finite values of u_n near the fixed positive s, not any unproved bound at zero, justify the comparison.

Set M=max(2,√(2d)). Since

    √b_n/n=√(4+(2d−4)/n)≤M

and z↦z coth(zt) is increasing on z>0, (6) yields

    a_n(t)≤[n M coth(Mt)]^n.                           (7)

For completeness, the derivative sign is the sign of sinh(w)cosh(w)−w for w=zt; this expression is zero at zero and has derivative 2sinh²(w)≥0.

On an interior compact time window J=[η,H]⊂(0,T), put

    B=e M coth(Mη).

The elementary inequality n^n≤e^n n! gives

    a_n(t)≤n! B^n,                    n≥0, t∈J.        (8)

This is the new growth mechanism. It tolerates diffusion's positive lower-moment contribution instead of incorrectly discarding it.

## 5. Reverse existence at positive time

The multinomial expansion shows that R^n−x_i^(2n) is SOS. For each fixed t>0,

    0≤L_t(x_i^(2n))≤a_n(t)/a(t)
       ≤a(t)^(−1)[n M coth(Mt)]^n.

Consequently every marginal Carleman series diverges: its n-th term is at least a(t)^(1/(2n))/√[n M coth(Mt)], with a zero moment interpreted in the usual infinite-term sense.

The multivariate Nussbaum–Carleman theorem therefore supplies a **unique** representing probability ρ_t for L_t. The inspected primary statement is Putinar–Schmüdgen, *Multivariate Determinateness*, arXiv:0810.0840v1, Theorem 25 and the immediately following Nussbaum attribution, printed p.24: https://arxiv.org/pdf/0810.0840v1 . Its hypotheses are positive semidefiniteness and marginal Carleman conditions, not a pre-existing vector measure. For d=1 this is the usual Hamburger existence theorem followed by Carleman uniqueness.

Let ν_t=a(t)ρ_t. It is the unique finite positive measure representing A_t. Only now do we use measure notation for the abstract hierarchy. By (8), monotone convergence gives, for 0<r<1/B,

    ∫exp(r|x|²)dν_t≤Σ_(n≥0)(rB)^n=1/(1−rB),   t∈J.  (9)

Also Cauchy–Schwarz and (8) give

    ∫|x|^k dν_t≤√(k!) B^(k/2),               k≥0,t∈J. (10)

Thus Gaussian tail integrability is a consequence, not an initial assumption. The complete reverse-existence bridge at positive times is already established before the next section.

## 6. The abstract equations imply a bounded Fourier PDE

Define F_t(ξ)=∫exp(iξ·x)dν_t. We justify its equation from polynomial tests rather than assuming a measure PDE.

For P_N(x)=Σ_(j=0)^N(iξ·x)^j/j!, real-variable Taylor remainder gives

    |exp(iξ·x)−P_N(x)|≤|ξ|^(N+1)|x|^(N+1)/(N+1)!.

Together with (10), this proves uniform convergence A_t(P_N)→F_t(ξ) on J and compact ξ sets. Since ΔP_N=−|ξ|²P_(N−2), and multiplication by R only adds two powers of |x| to the error estimate, the derivatives

    dA_t(P_N)/dt=A_t(ΔP_N−RP_N)

also converge uniformly there to −|ξ|²F_t−∫R exp(iξ·x)dν_t. To make the shifted bound explicit, with k=N+1 the killing-side remainder is at most

    |ξ|^k √((k+2)!) B^((k+2)/2)/k!,

which tends to zero by the ratio test. The Laplacian-side error uses the same estimate with the lower truncation N−2 and no R factor.

The usual theorem on uniform convergence of functions and first derivatives gives time differentiability. Applying the same uniform polynomial approximation with the factors x_i and x_i x_j proves joint continuity of the first two ξ derivatives. Ordinary dominated differentiation in ξ, valid for each represented measure, identifies them. Hence F is a classical solution on every interior window of

    ∂_tF_t=Δ_ξF_t−|ξ|²F_t,                  |F_t(ξ)|≤a(t)≤1. (11)

No assumed measurable choice of representing laws is hidden here: their Fourier transforms and needed continuity have been derived from uniformly convergent polynomial expressions.

## 7. Identify the represented evolution, after existence

The explicit positive kernel in Section 1 can equivalently be written as

    K_τ(x,y)dx=C_τ exp(−v_τ|y|²/2)
       × Normal(c_τ y, v_τ I_d)(dx).                  (12)

Its Fourier transform in x is therefore

    Ψ_τ(ξ,y)=C_τ exp(−v_τ(|y|²+|ξ|²)/2+i c_τ ξ·y).   (13)

The classical Mehler formula is checked against the author-hosted arXiv:0806.0734v2 of Agrachev–Boscain–Gauthier–Rossi, Section 4.1.1, printed pp.18–19, taking their λ=1 and tensoring coordinates. This is a normalization check, not a reverse-existence theorem. See SOURCE_MANIFEST.json and READING_BOUNDARIES.md.

It is also easy to verify (13) directly: v′=2c², c′=−2cv, C′/C=−dv and c²+v²=1 give

    ∂_τΨ=(Δ_ξ−|ξ|²)Ψ,          Ψ_0(ξ,y)=exp(iξ·y).

Fix s>0 and define G_t(ξ)=∫Ψ_(t−s)(ξ,y)dν_s(y) for t≥s. Since ν_s has all moments, dominated differentiation makes this a classical solution of (11), continuous through s and with G_s=F_s. It is bounded in absolute value by 1.

Here is the required uniqueness argument, rather than an unexplained semigroup appeal. If H=F−G, each real or imaginary part h is a bounded classical solution of (11), zero at s. On [s,H_0]×R^d use the positive barrier

    W_ε(t,ξ)=ε exp(2d(t−s))(1+|ξ|²).

It satisfies

    (∂_t−Δ_ξ+|ξ|²)W_ε
       =εexp(2d(t−s))[(2d+1)|ξ|²+|ξ|⁴]≥0.

On a sufficiently large ball W_ε dominates the common bound for h and −h at the lateral boundary; it also dominates their zero initial values. The bounded-domain parabolic maximum principle gives |h|≤W_ε inside. For any fixed (t,ξ), send ε↓0, choosing the ball large enough each time. This proves h=0. The bounded-domain principle itself is the standard interior-maximum derivative argument, with an arbitrarily small strict time barrier if necessary; all coefficients are bounded on each ball.

Thus F_t=G_t for t≥s. Fourier uniqueness for finite measures now yields

    ν_t=K_(t−s)^*ν_s,                           0<s<t<T. (14)

Both sides are actual finite positive measures at this stage. We have proved the represented evolution, not merely matched polynomial moments.

## 8. Recover zero, then prove its law is unique

Near zero, continuity of the original moment coordinates gives a uniform bound for L_t(R^k) for every fixed k. In particular the probabilities ρ_t are tight as t↓0. Choose a sequence s_j↓0 with ρ_(s_j) converging weakly to some probability μ; as a(s_j)→1, ν_(s_j) has the same weak limit.

This μ represents L_0. Indeed the uniformly bounded higher radial moments make every polynomial uniformly integrable along the sequence. For a degree-m polynomial p, choose 2k>m and use |p(x)|≤C(1+|x|^m), with a higher radial moment controlling the tails. Truncation by continuous compact cutoffs, weak convergence, and this uniform tail bound give

    ∫p dμ=lim_j L_(s_j)(p)=L_0(p).

The same argument, or lower semicontinuity applied to every even radial power, gives all absolute polynomial moments of μ. This step proves existence only; it does not assert that the initial moment record is determinate.

For a fixed t>0 and fixed ξ, (13) implies uniform convergence

    Ψ_(t−s_j)(ξ,·)→Ψ_t(ξ,·)

as j→∞. One way to see uniformity is to differentiate the expression in τ on [t/2,t]: all y-dependent derivatives are a fixed-degree polynomial times a Gaussian with a common strictly positive rate, hence uniformly bounded. Passing (14) to the limit in Fourier form gives

    F_t(ξ)=∫Ψ_t(ξ,y)dμ(y),

so ν_t=K_t^*μ. This proves (1) on the whole given horizon using a single weak subsequence. It does not presume that moment convergence alone implies Fourier convergence at zero.

Finally, K_t^* is injective on finite measures. Formula (13) factors its Fourier transform as

    Fourier(K_t^*μ)(ξ)
      =C_t exp(−v_t|ξ|²/2)
         ×Fourier(exp(−v_t|y|²/2)μ)(c_t ξ).             (15)

For every finite t>0, C_t>0, c_t>0 and the Gaussian factor is nonzero. Fourier uniqueness therefore recovers the finite weighted input measure, and its strictly positive weight recovers μ. Hence all candidate weak boundary limits agree once their common positive-time evolution is known. The complete path selects one initial law even if L_0 alone admits many.

The normalized map is injective on probabilities too: from a normalized output, division by the output Gaussian Fourier factor recovers the probability proportional to exp(−v_tR/2)μ; multiplying by exp(v_tR/2) and normalizing recovers the original μ. Finiteness of that inverse weight is guaranteed for actual inputs, not imposed as an unsupported property of arbitrary candidate records. This is injectivity for exact full records in the stated range; no stable or computable inverse is claimed.

## 9. Converse, continuation, and the exact boundary with heat alone

For any probability μ with all polynomial moments finite, (12) defines positive ν_t of strictly positive mass

    a(t)=C_t∫exp(−v_tR/2)dμ,          a(0)=1.

For a polynomial p, the conditional Gaussian expectation in (12) is a polynomial in c_t y and v_t, with smoothly varying coefficients through t=0. Its derivatives, together with the weight derivatives, are bounded on finite time windows by an integrable polynomial in y. Differentiation under μ is therefore valid, including the right derivative at zero. Direct differentiation of the kernel, or its Gaussian polynomial identity, gives

    dν_t(p)/dt=ν_t(Δp−Rp).

For clarity, the kernel identity is ∂_tK_t=(Δ_x−R(x))K_t. Its Gaussian decay justifies integration by parts against each polynomial for t>0, and the preceding dominated polynomial limit supplies t=0. The mass equation is a′=−ν_t(R), so normalization gives exactly (H).

The construction exists for every t≥0. Positive-time determinacy and (15) make it the unique continuation of any given nontrivial path. All laws in one initial moment fibre give paths with the same initial record, while injectivity of the normalized evolution makes different laws give different positive-time records. This yields the claimed fibre classification.

The earlier heat-only obstruction remains intact: without −Rp the radial recurrence loses its −a_(n+1) term, and (5) loses its negative quadratic term. There is then no coming-down-from-large-moments estimate, and full square-positive non-moment heat paths can persist. Conversely, conjugating the oscillator operator by a Gaussian is not a legitimate shortcut on abstract polynomial functionals: the Gaussian is outside their declared domain. We only use Gaussian weights after representability has been proved.

A straightforward rescaling also covers κΔ−λ|x|² with constants κ,λ>0: set x=(κ/λ)^(1/4)y and τ=√(κλ)t. This does not extend the theorem to general nonquadratic killing.

## 10. Evidence and limits

The substantive new step relative to G/V and the heat comparison is Sections 2–5: a faithful radial recurrence, square-positive interpolation, a zero-safe Riccati comparison, and a moment-growth existence bridge in the presence of diffusion. Sections 6–9 supply the additional law-level identification and initial-law classification rather than silently inferring them from representability.

Classical ingredients are square-functional Cauchy–Schwarz, scalar ODE comparison, Nussbaum–Carleman, tight weak compactness, polynomial uniform integrability, elementary Gaussian integration, Fourier uniqueness, and the bounded-domain parabolic maximum principle. The specific estimates and safe order of use are written out. The inspected sources establish no priority claim for this assembly.

The exact controls test input hashes, radial polynomial identities, both log-convex Cauchy–Schwarz decompositions, the Riccati/barrier algebra, Gaussian-kernel identities and finite-degree moment evolution. They supplement the ordinary proof; they do not verify the universal analytic theorem, perform general measure reconstruction, or constitute a proof-kernel formalization. The concrete failed monotonicity and even-derivative transplants are retained as exact controls.

The separately completed bounded source comparison is copied under inputs/ and hash-bound. It checks the earlier heat/PDE papers and their specifically cited Schwartz-data existence theorem; none supplies this reverse implication. That is not a claim about all literature, nor independent validation of Theorem D. Its exact reading boundaries and source versions remain in `diffusive-moment-source-followup-20261010`.

The final author run passed 685 exact controls, including inherited/supplementary input integrity and pinned primary-source integrity. See CONTROL_RESULTS.json and check_controls.log.
