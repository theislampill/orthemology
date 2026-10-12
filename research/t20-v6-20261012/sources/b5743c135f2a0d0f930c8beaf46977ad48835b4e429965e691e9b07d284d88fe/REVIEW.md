# Independent review: diffusion with quadratic killing

10 October 2026 UTC. Separate ordinary mathematical review of Theorem D and its whole proof. This reviewer did not develop the author's initial result, did not edit the author packet, and did not perform protected integration, outreach, or closure. Suggestions about the radial zero case and maximum-principle barrier were sent only after independently deriving them; the received draft already contained both arguments. The independent controls were authored separately, before inspecting the author's control program.

## Review outcome

The mathematical argument in Sections 1–10 is accepted within its stated scope: constant Euclidean diffusion, coercive quadratic killing, a fixed finite spatial dimension, a full normalized polynomial-square-positive hierarchy, and the stated coordinatewise C¹ regularity through time zero. No substantive mathematical defect was found. Acceptance is ordinary mathematical review, not a Lean or other proof-kernel claim, not field-priority certification, and not permission for integration or closure.

The final review receipt identifies the exact frozen author artifacts and separately records fresh control results. Those hashes, rather than a mutable filename alone, delimit this review.

## 1. Algebra before any measure exists

For R=|x|², define a=exp(−∫L(R)) and A=aL. Because R is SOS, L(R)≥0, hence 0<a≤1 and a′=−A(R). The unnormalized hierarchy is A′(p)=A(Δp−Rp). The chain rule gives ΔRⁿ=2n(2n+d−2)Rⁿ⁻¹ for every n≥1 and d≥1, including the edge n=1. Thus a_n=A(Rⁿ) obeys a_n′=b_n a_{n−1}−a_{n+1}, with b_n=2n(2n+d−2)>0. Every a_n is nonnegative because every Rⁿ is an explicit multinomial SOS.

The log-convex inequality a_n²≤a_{n−1}a_{n+1} is valid without an assumed measure. Odd n uses ordinary functional Cauchy–Schwarz. Even n uses Cauchy–Schwarz on the finite direct sum of polynomial spaces, with the lists x_iR^{k−1} and x_iR^k. Positive semidefiniteness of that direct sum follows immediately by summing its square forms. This handles both parities rather than silently assuming Stieltjes representation.

The ε point-evaluation regularization is legitimate as a static argument: it adds ε to every radial moment and remains square-positive. Discrete convexity of log(a_n+ε), followed by ε↓0, proves both interpolation inequalities, including zero moments. For n=1 the lower interpolation is simply the equality a_0=a_0; no ambiguous 0⁰ operation is needed.

## 2. Zero cases and scalar comparison

If an interior a_n vanishes, interpolation forces a_1=0. Each A(x_i²)=0, so functional Cauchy–Schwarz forces A(x_i p)=0 for every p. Consequently every positive-degree radial moment vanishes. But the radial recurrence then gives a_1′=2d a_0>0, whereas differentiability at an interior minimum gives a_1′=0. All a_n with n≥1 are therefore strictly positive at positive interior times. Taking their nth roots is justified.

Using 0<a_0≤1 in the two interpolation inequalities gives a_n′≤b_n a_n^{1−1/n}−a_n^{1+1/n}. Accordingly u_n=a_n^{1/n} satisfies u_n′≤(b_n−u_n²)/n. The exact singular upper solution is √b_n coth(√b_n(t−s)/n). For any fixed positive s, u_n is finite near s, while that upper solution diverges at s. Start comparison at s+ε, then let ε↓0; finally let s↓0. This never assigns an infinite value to the hierarchy or assumes an initial high-moment bound uniform in n.

The resulting bound is a_n(t)≤[n M coth(Mt)]ⁿ, where M=max(2,√(2d)). Indeed √b_n/n≤M and z coth(zt) is increasing in z>0. The constants are uniform in n and on any fixed compact positive-time window. They are dimension-dependent, as the theorem permits; no dimension-free estimate is asserted. The factorial relaxation nⁿ≤eⁿn! is valid and yields a_n≤n!Bⁿ.

## 3. Genuine reverse existence

Rⁿ−x_i^{2n} is a multinomial SOS. The preceding bound therefore controls every marginal even moment of L_t. Its reciprocal-root lower bound has order n^{-1/2}; the marginal Carleman series diverges. Full square positivity plus those conditions supplies both existence and uniqueness of a probability representative. No measure is inserted before this step.

The exact external dependency was checked directly in Putinar–Schmüdgen, *Multivariate Determinateness*, [arXiv:0810.0840v1](https://arxiv.org/pdf/0810.0840v1), printed page 24, Theorem 25 and the following Nussbaum statement. The theorem starts with a positive-semidefinite sequence; it does not assume vector representability. The d=1 case is Hamburger existence plus Carleman uniqueness. The review uses only this bounded part of the source, not a claim about its other results.

With ν_t=a(t)ρ_t, monotone convergence of the positive exponential series gives a common Gaussian exponential moment on each interior time window. The estimate ∫|x|^k dν_t≤√(k!)B^{k/2} follows by Cauchy–Schwarz and ν_t(1)≤1. Thus both representation and the tail control needed later have been proved before Fourier or kernel reasoning starts.

## 4. Polynomial equations really yield the Fourier PDE

Taylor polynomials of exp(iξ·x) converge uniformly after integration, simultaneously on compact ξ sets and interior time windows. Multiplication by R costs two powers in the moment estimate. The killing remainder is bounded by |ξ|^k√((k+2)!)B^{(k+2)/2}/k!, whose consecutive-term ratio tends to zero. The Laplacian identity is ΔP_N=−|ξ|²P_{N−2} for N≥2. Hence both the functions and their first time derivatives converge uniformly.

The standard uniform-derivative convergence theorem therefore gives ∂_tF=Δ_ξF−|ξ|²F. Factors x_i and x_ix_j in the same approximation give joint continuity of the required spatial derivatives; fixed-measure dominated differentiation identifies them. This establishes a classical bounded solution. It does not assume weak continuity of an arbitrary family of measures, nor attempt an uncontrolled moment-series expansion at time zero.

## 5. Kernel normalization and unbounded-domain uniqueness

Completing the square in the kernel gives mass C_τexp(−v_τ|y|²/2), conditional mean c_τy, and conditional covariance v_τI, with v=tanh(2τ), c=sech(2τ), C=cosh(2τ)^{-d/2}. Consequently its Fourier transform is Cexp(−v(|y|²+|ξ|²)/2+icξ·y). This normalization was independently derived and checked against the one-dimensional formula in Agrachev–Boscain–Gauthier–Rossi, [arXiv:0806.0734v2](https://arxiv.org/pdf/0806.0734v2), Section 4.1.1, printed pages 18–19, at λ=1. Tensoring gives the stated d-dimensional form. The source is only a normalization dependency here.

The identities v′=2c², c′=−2cv, C′/C=−dv, and c²+v²=1 verify the Fourier PDE directly. Integrating this expression against ν_s is legitimate through τ=0 because ν_s has all moments. On compact ξ and time sets the derivatives are bounded by integrable polynomials in y. The candidate solution remains bounded by ν_s(1)≤1.

Uniqueness is correctly proved in the bounded class, rather than asserted for arbitrary solutions of an unbounded-domain heat equation. For either real component of the difference, W=εexp(2d(t−s))(1+|ξ|²) has nonnegative residual under ∂_t−Δ_ξ+|ξ|². On each sufficiently large finite ball it dominates the bounded lateral data and zero initial data. The finite-cylinder maximum principle applies with bounded coefficients. For a fixed point let ε↓0, choosing the radius large enough each time. This proves uniqueness and the actual positive-time measure evolution by Fourier uniqueness. No decay of the unknown solution at spatial infinity is needed.

## 6. Recovery at time zero

Continuity of each radial coordinate gives bounded second moments near zero, hence tightness of the representing probabilities. A weakly convergent subsequence exists and has probability limit μ. Since a(t)→1, the finite measures ν_t have the same subsequential limit. Higher radial moments supply polynomial uniform integrability. For a degree-m polynomial, choose 2k>m; outside a ball its growth is bounded by a constant times the 2kth radial moment times a negative power of the radius. Compact cutoffs, weak convergence, and this tail bound identify every initial moment, while lower semicontinuity supplies finiteness of all limiting moments.

The proof does not mistake agreement of moments for uniqueness at this boundary. It first passes the represented evolution to the boundary. For fixed t>0 and ξ, the endpoint Fourier kernel at t−s converges uniformly in y to the kernel at t, because its time derivatives are polynomial times a Gaussian with a common positive rate on [t/2,t]. Weak convergence can therefore be applied to this bounded continuous test. It follows that ν_t=K_t^*μ for every positive t using one subsequence.

Finally the Fourier factorization isolates the transform of exp(−v_t|y|²/2)μ at the nondegenerate argument c_tξ. Every outside factor is nonzero for finite t. Finite-measure Fourier uniqueness recovers this weighted input, and positivity of its weight recovers μ. The normalized map is also injective on probabilities: it recovers the normalized weighted input, after which inverse weighting and renormalization recover the probability. Integrability of the inverse weight is only claimed for actual inputs. This order correctly separates initial existence from initial-law identification.

## 7. Converse, continuation, and limitations

For any initial probability having all polynomial moments, the Gaussian conditional expectation of a polynomial is a finite polynomial in y with smooth coefficients through zero. On finite nonnegative time windows the killing weight is at most one; its derivatives introduce only polynomial factors. This justifies differentiation under the initial law through zero. The spatial kernel PDE and Gaussian integration by parts give ν′(p)=ν(Δp−Rp) for positive times, and the polynomial limit supplies the endpoint identity. Division by the strictly positive mass gives the normalized hierarchy.

The construction exists for every nonnegative finite time. Determinacy of positive-time records and injectivity of normalized evolution establish the unique continuation of an already supplied nontrivial path, as well as the bijection between paths and laws in a fixed initial moment fibre. This does not assert that the initial moment record itself is determinate. Scaling x=(κ/λ)^{1/4}y and τ=√(κλ)t correctly reduces κΔ−λ|x|² for κ,λ>0 to the reviewed case.

The proof does not cover arbitrary coercive polynomial killing, nonlinear or variable diffusion, nonautonomous generators, a finite truncation of the hierarchy, a stable or computable inverse, or any priority claim. The heat-only obstruction remains consistent: without killing the negative quadratic Riccati term disappears. For δ_0, a_1′(0)=2d>0 and a_0″(0)=−2d<0 explicitly invalidate both naive pure-killing transplants.

## 8. Executed checks and their boundary

The independently authored exact program executes 133 algebraic controls: coordinate radial identities; both even-index direct-sum components; radial-coordinate SOS expansions; scalar Riccati and monotonicity algebra; dimension-ratio identity; Gaussian square completion; formal arbitrary-dimension Fourier and spatial Mehler PDEs; the maximum-principle barrier; one-dimensional monomials through degree 10; selected genuinely mixed two-dimensional monomials; and both failed-transplant signs. Its output and script digest are preserved in INDEPENDENT_RESULTS.json.

Two review-script development failures are retained. The first omitted a hyperbolic simplification in the assertion helper; the second passed a SymPy Poly to an expression-only simplifier. Neither was a mathematical residual or an author-proof failure. The repaired helper simplifies hyperbolic identities and converts Poly objects to expressions. A fresh successful run is retained separately. The frozen author's controls are independently replayed from a separate copy; their exact outcome is recorded in REVIEW_RECEIPT.json.

These finite calculations support the independently checked algebra. They do not machine-verify interpolation for every functional, the Carleman theorem, tight compactness, Fourier uniqueness, dominated convergence, or the maximum principle. Those are the ordinary mathematical proof and explicitly identified classical dependencies above. No Lean invocation or formal-kernel success is claimed.
