# Independent review: SOS-dissipative polynomial gradient reverse lift

10 October 2026 UTC. Ordinary scoped mathematical review. No protected changes, integration, audit-governor procedure, formal-kernel certificate, priority claim, or programme closure is asserted.

## Verdict and frozen boundary

PASS for the strengthened theorem with an additive radial constant D≥0, under exactly the frozen author hypotheses. The mechanism removes the full-path rank premise for the explicitly certified class; it does not establish a result for every coercive polynomial gradient.

The frozen RESULT.md SHA256 is d5ace0095fde0d5e997fdc06e458b75d1c033016fc9d104b5d5bf09588ded1f7. FROZEN_MANIFEST.json SHA256 is 8a0c2a6f8c5d2232f607b57feb8077352b83c74a8cc43fbd24db76a383634afc. AUTHOR_SNAPSHOT_BINDINGS.json binds every frozen author file and all 15 author input files. The two requested local wording corrections are present in these frozen bytes.

I read the accepted radial-quartic theorem and its independent review first, then the inherited diffusion interpolation proof, and independently derived the new coefficient and scalar comparison. The parent proposed the D extension. I supplied the shifted-quartic discriminator to the author and requested two local wording corrections before freeze. Those exchanges are disclosed; I did not author the main proof or simply replay its checker as my review.

## 1. Exact hypotheses and pre-representation algebra

The theorem fixes κ>0 and λ,D,C≥0 and requires actual SOS certificates for V=F+C and Q=x·∇F−κ|x|⁴+λ|x|²+D. Full square positivity, normalization, the exact all-polynomial hierarchy, and coordinatewise C¹ regularity through zero are supplied-path assumptions. No representing measure or rank premise is inserted at this stage.

Unnormalization A_t=a(t)L_t with a=exp(−∫L(V)) gives A′(p)=A(−∇F·∇p−Vp), a(0)=1, and 0<a≤1. For R=|x|² and a_n=A(R^n), the exact identity is

    a_n′=2nD a_(n−1)+2λn a_n−2κn a_(n+1)
          −2n A(R^(n−1)Q)−A(VR^n).

R powers and products of SOS polynomials are SOS. Therefore all a_n and both discarded quantities are nonnegative before representation. The inward coefficient is 2κn, the positive additive term is 2nD, and killing has the negative sign. Merely pointwise positivity of arbitrary polynomials is never silently substituted for square positivity.

The radial sequence is log-convex using polynomial Cauchy–Schwarz. Odd indices use R^j and R^(j+1); even indices use the direct-sum pairs x_iR^(j−1), x_iR^j. The inherited static perturbation A+ε ev_z, |z|=1, proves the interpolation inequalities even at zeros. Since a_0>0,

    a_(n−1)≤a_0^(1/n)a_n^((n−1)/n),
    a_(n+1)≥a_n^((n+1)/n)/a_0^(1/n).

At n=1 the first statement means a_0=a_0, without assigning an ambiguous value to zero raised to zero. Using a_0≤1 yields, on the positive set of u_n=a_n^(1/n),

    u_n′≤2D+2λu_n−2κu_n².

This scalar equation is independent of n. The coefficient cancellation, rather than energy decrease, is the key compactness mechanism.

## 2. Riccati comparison really handles zero moments

The roots u_n are continuous everywhere and C¹ wherever positive. Strict positivity is false in this class and is not needed. Compare u_n with the Riccati solution y(t;r) starting at r>u_n(0). That solution is strictly positive at every finite time. Every component where u_n>y lies inside the differentiable positive set of u_n. On a bounded time window, local Lipschitz continuity of f(y)=2D+2λy−2κy² gives (u_n−y)′≤K(u_n−y) there. Its left boundary has zero difference, so Gronwall excludes the component. There is no differentiation across a zero or diffusion-style argument claiming zeros are impossible.

With Δ=sqrt(λ²+4κD), the infinite-initial envelope is

    Y(t)=(λ+Δ coth(Δt))/(2κ),  Δ>0,
    Y(t)=1/(2κt),              Δ=0.

It solves Y′=2D+2λY−2κY² and dominates each finite-initial scalar solution strictly at t>0. Hence a_n(t)≤Y(t)^n for every n≥1. These statements follow from finite comparators, not an ODE initialized at infinity.

For D=0 the separate exponential clock agrees: c_n=e^(−2λnt)a_n, τ=(e^(2λt)−1)/(2λ), with τ=t at λ=0, satisfies dc_n/dτ≤−2κn c_(n+1). The nested-simplex factorials cancel exactly, yielding

    a_n(t)≤L_0(R)e^(2λt)Y(t)^(n−1).

The general bound and this refinement have different initial-moment dependence, and neither is incorrectly substituted for the other. D=0 forces ∇F(0)=0 because Q≥0, Q(0)=0, and ∇Q(0)=∇F(0). The general D≥0 theorem does not impose that artificial centering restriction.

## 3. Positive-time measures are proved, then the PDE

R^n−x_i^(2n) is SOS, so L_t(x_i^(2n))≤a(t)^(−1)Y(t)^n. The marginal Carleman terms are bounded below by a(t)^(1/(2n))/sqrt(Y(t)) when nonzero; zero even moments use the usual infinite-term convention. Thus each marginal series diverges.

The imported classical theorem supplies existence as well as determinacy from a positive-semidefinite full multisequence. The primary statement independently inspected is Putinar–Schmüdgen, [Multivariate Determinateness](https://arxiv.org/pdf/0810.0840v1), printed p.24, Theorem 25 and its following Nussbaum attribution. The archived page/PDF are pinned, and the same current primary-web statement was checked. In dimension one, Hamburger existence plus Carleman uniqueness provides the conclusion. This review does not pretend to reprove that specialized classical theorem.

Once ν_t=a(t)ρ_t is an actual measure, the geometric radial bound implies ν_t(R>Y(t))=0 by Markov's inequality and n→∞. On each positive-time compact interval, these finite measures have common compact support and mass at most one. Polynomial approximation and moment-coordinate continuity then prove weak continuity, so there is no unproved measurable selection of representing measures.

On that common compact set, the Taylor polynomials for exp(iξ·x) and their first spatial derivatives converge uniformly. The polynomial generator therefore converges uniformly as well, since b and V are bounded on the set. Passing the integrated hierarchy to Fourier tests and applying Fourier inversion to compact smooth tests gives

    ∂_tν=−div(bν)−Vν.

The conservative weak generator is b·∇−V; no divergence term is missing from that test convention. Integrability of (1+|ξ|)|φ̂(ξ)| justifies the Fourier/Fubini passage. The time-dependent compact-test rule follows by splitting the difference quotient and using the established weak continuity and uniform mass bound. Nonpolynomial functions enter only after representation and this test extension.

## 4. Completeness and injectivity do not require a polynomial inverse

Pointwise radial dissipativity gives R(Φ_t x)′≤2D+2λR−2κR². Finite-initial scalar comparison gives R(Φ_t x)<Y(t) for finite x and t>0. Dropping the negative term gives

    R(Φ_t x)≤e^(2λt)R(x)+2D∫_0^t e^(2λs)ds.

This linear-growth estimate in the initial radius prevents finite-time escape and establishes forward completeness. Smooth polynomial ODE theory gives smooth finite-time maps. Meeting trajectories have the same past by local reversed uniqueness along their already-existing trajectory segments. The Jacobian determinant is exp(∫div b)>0. Thus Φ_t is an injective local diffeomorphism and a diffeomorphism onto its open image O_t.

This is exactly the needed inverse statement. It neither asserts global backward completeness nor an inverse on all of R^d. O_t is a bounded proper image and need not equal the open comparison ball. A polynomial-automorphism theorem is consequently unavailable and is not used.

The positive weight E_t=exp(−∫V(Φ_s x)ds) is smooth on compact time-space sets and satisfies 0<E_t≤1, together with the flow/weight cocycles. The backward terminal function U(r,x)=E_(t−r)(x)f(Φ_(t−r)x) solves the backward equation. A fixed cutoff equal to one near the known common support places it in the proved test class; the cutoff derivative vanishes wherever the measures live. Hence

    ν_t=(Φ_(t−s))_*(E_(t−s)ν_s), 0<s<t.

This argument is a proved compact-test uniqueness calculation rather than an appeal to an unspecified transport theorem with unbounded coefficients.

## 5. Boundary recovery, all moments, and exact law classification

The original coordinate continuity bounds every fixed radial moment near zero. Second moments give tightness of the represented probabilities ρ_s. A single weakly convergent subsequence has a probability limit μ. Higher radial bounds give uniform integrability of each polynomial and show μ has all absolute polynomial moments and represents L_0. Weak convergence alone would be insufficient, but the explicit higher-moment tail estimate supplies the missing control.

For fixed t>0, the backward kernels E_(t−s_j)f∘Φ_(t−s_j) are uniformly bounded by ||f||∞ and converge locally uniformly. Tightness controls the complement of a fixed compact set. Passing the positive-time characteristic identity along the same subsequence therefore gives ν_t=(Φ_t)_*(E_tμ) for every fixed t, with the same μ. There is no uniform-in-space kernel claim or time-dependent choice of boundary law.

The image-only inverse recovers E_tμ from ν_t. Division by the positive Borel weight recovers μ, even if the reciprocal is unbounded: this is equality of known positive measures in the actual range. The normalized map is also injective because division yields proportional probabilities and their masses fix the factor. Positive-time laws are thus carried by O_t and put zero mass on the comparison sphere. Their topological support may meet that sphere as a limit set.

The converse uses the displayed linear-growth bound, not the false D=0 bound |Φ_t x|≤e^(λt)|x| in the D>0 case. Each polynomial test and its generator composition have a fixed polynomial bound in the initial x on finite time windows. All initial moments therefore justify dominated differentiation and continuous derivatives through zero. The constant C cancels on normalization, leaving exactly the required hierarchy.

These two directions identify each supplied path with one initial law and identify a fixed valid initial-moment path fibre with the whole representing-law fibre. Compact positive-time determinacy and normalized injectivity separate distinct initial laws at every positive time. A supplied nontrivial finite-horizon path consequently has a unique forward extension; an indeterminate initial moment record by itself does not choose that path.

For finite initial full Hankel rank r, the represented initial law has exactly r support points. One can see this directly by choosing a linear functional separating any N support points and applying a Vandermonde argument to its powers: N points force rank at least N. Conversely an r-point law has rank r. Positive finite-time weights and injective characteristics preserve those r distinct points. Thus future finite rank is a conclusion, not a restated hypothesis; no fixed truncated-rank condition is substituted.

## 6. Scope controls and energy

The nonconvex F=(R−1)²/4 satisfies κ=λ=1 and D=C=0 with Q=0. The logistic radius, nonpolynomial bounded-image flow, and stationary origin are correct. The normalized law δ_0 is stationary with energy 1/4 although the global minimum is 0 on the unit sphere. Hence the class does not inherit the radial predecessor's universal collapse or a generic global-minimization conclusion.

The shifted well F=(x−1)^4/4 has the explicit certificate

    xF′−x⁴/4+x²+1/4=(3/4)(x²−2x)²+(x−1/2)².

It has F′(0)=−1, so no D=0 certificate in these coordinates is possible. Its explicit characteristic starting at 0 moves immediately, although all initial positive radial moments vanish. This checks both genuine enlargement by D and the zero-safe comparison obligation. It is an example/control, not a new theorem separate from translated radial dynamics.

Energy dissipation is exactly −L(|∇F|²)−Var(F). The finite-atomic metric conclusion is inherited after representation is forced. No infinite-dimensional Riemannian-manifold theorem or general long-time optimality result is claimed. The radial certificate itself implies coercivity by integration along rays; no additional unannounced coercivity hypothesis is needed.

## 7. Evidence limits

The independent checker executes 138 exact finite symbolic and source-integrity checks, including 72 multivariate recurrence/Cauchy–Schwarz identities, finite Riccati flow/envelope/strict-gap identities, D=0 coefficient controls, the shifted zero-moment example, and nonconvex stationary controls. Deliberately mutated inward coefficients, deleted D terms, altered discriminants, and lost exponential prefactors have nonzero residuals. These finite checks supplement the universal analytical review; they do not prove an infinite hierarchy by sampling or constitute formal-kernel verification.

All 270 author controls were rerun in an isolated copy, producing byte-identical EXACT_CHECKS.json. The 138 independent controls were separately executed. The frozen-input manifest, replay logs, and REVIEW_RECEIPT.json record the exact reviewed bytes and old-source preservation; verify_review.py checks all bindings and replays both checkers in a fresh temporary tree. No author packet or inherited source is modified by this review.
