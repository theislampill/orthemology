# Independent review: unrestricted-rank radial quartic gradient reverse lift

10 October 2026 UTC. Bounded independent mathematical review and finite exact controls. This review does not edit protected inputs, integrate a theorem, certify a formal kernel, claim field priority, or close T20.

## Verdict and reviewed increment

PASS for the explicit radial quartic generator and the full supplied-path hypotheses. The author proves reverse existence of an actual initial probability from a normalized, full-square-positive, coordinatewise C¹ all-polynomial path. The proof does not assume a representing measure, any finite-rank path bound, or any initial tail condition. This is a genuine strengthening over the inspected finite-rank nonlinear-gradient ancestor. The exact characteristic formula itself was already in that ancestor.

The author proof and controls are bound by AUTHOR_SNAPSHOT_BINDINGS.json; the executed review and source-preservation evidence are bound by REVIEW_RECEIPT.json. This review uses the classical multivariate Carleman existence theorem as an explicit dependency, rather than claiming to independently reprove that classical theorem. The inspected source statement is the archived Putinar–Schmüdgen printed p.24, Theorem 25 and following Nussbaum attribution. The author's claim to have checked its current web PDF is not needed or independently certified here.

The earlier polynomial-automorphism theorem is inapplicable: the positive-time radial flow has a proper bounded image, is nonpolynomial, and has a nonpolynomial inverse only on its image. The present proof never substitutes that inverse into an abstract polynomial functional. It first produces positive-time measures and identifies their actual weak PDE.

## 1. Radial estimate before measure existence

Set R=|x|², F=R²/4, b=−Rx and a=exp(−∫L(F)), with A=aL. Each polynomial coordinate of A is C¹ and a>0. Since R^n is a finite sum of polynomial squares, full square positivity gives a_n=A(R^n)≥0. Unnormalization and Euler's identity give exactly

    a_n'=−2n a_(n+1)−a_(n+2)/4.

In particular every a_n is nonincreasing, including a_0=a≤1. No merely pointwise-nonnegative, non-SOS polynomial is fed into an unrepresented functional.

For j≥1, integrating and discarding nonnegative endpoint and killing terms gives a_j(s)≥2j∫_s^t a_(j+1)(u)du. Repeating from j=1 to n−1 produces the coefficient 2^(n−1)(n−1)! times a nested time simplex. Its volume is (t−s)^(n−1)/(n−1)!, and monotonicity bounds its last integrand below by a_n(t). Thus the coefficient is exactly [2(t−s)]^(n−1), proving

    a_n(t)≤L_0(R)(2t)^(1−n), n≥1.

This works through t=0 because only integration of first derivatives is used. It does not assume higher time derivatives or analyticity. When L_0(R)=0 the same inequality sets every positive radial moment to zero at positive times; no division by that value occurs.

## 2. Full positive-time existence and compact support

The polynomial R^n−x_i^(2n) is SOS: its multinomial expansion has nonnegative coefficients on even monomials. Thus each marginal even moment is geometrically bounded after division by a(t)>0. Its negative 1/(2n) root stays bounded below by a positive number for large n unless it vanishes, in which case the Carleman convention is +∞. Therefore all marginal Carleman series diverge.

The cited multivariate theorem starts from a positive-semidefinite full multisequence and yields existence as well as determinacy; it is not only a uniqueness theorem for an already assumed measure. In dimension one, Hamburger existence and Carleman determinacy supply the same conclusion. In the zero-radial case the measure is directly δ_0. This resolves the central multivariate moment-existence obligation.

For the measure ν_t representing A_t, the bound for all n implies

    ν_t(R≥r)≤L_0(R)(2t)^(1−n)r^(−n)→0

whenever r>1/(2t). Hence its topological support lies in the closed ball R≤1/(2t). This uses the full hierarchy, not any finite list of moments. On [s,t] with s>0, all measures share one compact support and have mass at most one. Uniform polynomial approximation plus coordinate continuity therefore proves weak continuity of the measures.

The closed-ball statement at this stage is exactly right. It alone cannot exclude sphere mass. The later characteristic formula proves concentration in the open ball and zero sphere mass, while allowing the topological support to meet the sphere as a limit set of images of unbounded initial support.

## 3. Extending the polynomial equation to the measure PDE

The author's Fourier argument is sufficient and avoids an unproved C¹ polynomial-density invocation. On the common compact ball, the finite Taylor polynomials of e^(iξ·x) and their first spatial derivatives converge uniformly. The identity ∂_iP_N=iξ_iP_(N−1) controls the gradient. Consequently both P_N and G P_N converge uniformly, where G=b·∇−F and b,F are bounded on this ball.

Passing the integrated polynomial identity through these uniform limits yields the Fourier-test identity. For compact smooth φ, its Fourier transform is integrable with a factor 1+|ξ|. The generator bound is a constant times 1+|ξ|, so Fourier inversion and Fubini are justified. The resulting compact-test weak equation is precisely

    ∂_tν=−div(bν)−Fν.

No missing divergence term occurs in this conservative test-generator convention. The test equation is first proved for fixed compact smooth tests; its time-dependent extension follows by splitting a difference quotient and using bounded masses, uniform time differentiation and the already proved weak continuity.

## 4. Positive-time characteristics and initial recovery

The radial flow, its semigroup identity, integrated killing derivative and killing cocycle are correct. With a terminal smooth test f, U(r,x)=E_(t−r)(x)f(Φ_(t−r)(x)) solves the backward equation. Multiplying U by a fixed compact cutoff equal to one near the known common support places it in the proved test class. The cutoff's gradient is zero wherever the measures live, so no additional term survives. This proves the full measure identity from s to t. A general unbounded-coefficient transport uniqueness theorem is not needed.

Near zero, continuity of L_s(R) gives tightness of the represented probabilities. Every higher radial moment is uniformly bounded on a short compact time interval. A tight subsequence therefore tends weakly to a probability μ, and higher radial bounds provide uniform integrability for every polynomial. In particular μ has all absolute polynomial moments and represents L_0. Weak convergence alone would not prove this; the author's tail estimate explicitly supplies the needed step.

For each fixed t>0, the kernels E_(t−s)(x)f(Φ_(t−s)(x)) are bounded by ||f||∞ and converge locally uniformly as s↓0. A compact cutoff and uniform tightness allow passage through these varying kernels. Thus the same μ represents the entire supplied path, with a(t)=∫E_t dμ. There is no demand for uniform convergence in x over the whole unbounded initial space.

The map Φ_t is a homeomorphism onto the open ball, and E_t is positive at every finite point. Inverse pushforward and division by E_t identify μ uniquely from the unnormalized positive-time law. Although the inverse weight is unbounded near the sphere, equality of known positive measures can be multiplied by that positive Borel function; the actual inverse integrals are finite because the inputs are finite. The normalized map is also injective on probabilities: division yields proportional initial measures, and total mass fixes the factor. This proves unique selected initial law and excludes a separate boundary-inflow degree of freedom.

## 5. Converse, initial-law fibres and finite rank

For arbitrary initial probability μ with all polynomial moments, |Φ_t(x)|≤|x| and 0<E_t≤1. The integrand for a degree-m polynomial and its derivative have fixed polynomial bounds of degrees at most m+4 on each time window. Dominated differentiation therefore proves the hierarchy and continuous right derivatives at zero. The normalizer is finite and strictly positive.

Consequently the representing-law fibre of an initial functional is exactly the admitted-path fibre. The theorem does not declare arbitrary square-positive initial functionals representable, and initial moments alone need not select a unique path. Once a positive-time record is supplied, compact-support determinacy and normalized-map injectivity identify its unique initial law. A supplied nontrivial finite-horizon path therefore extends uniquely under this fixed generator.

A represented initial law has finite full Hankel rank r exactly when its support consists of r points. One elementary direction is polynomial separation: any N distinct support points admit a separating linear form; its powers through N−1 have a positive-definite Gram matrix, because a nonzero polynomial of that degree cannot vanish at all N separated values. This bounds the support cardinality by the rank. The converse is a Vandermonde evaluation argument. Positive weights and flow injectivity preserve those r support points at every finite time. Therefore the author truly removes the future full-rank promise for initially finite-rank paths. No claim about a fixed truncated Hankel matrix replaces this statement.

The inherited finite-atomic metric applies once this representation is forced. For infinite laws, the packet proves the measure equation and energy dissipation; it does not claim a new infinite-dimensional smooth Riemannian structure. The dissipation −L(R³)−Var(F) has the correct transport and replicator terms.

The final shrinking-ball corollary is also valid: L_t(R)≤1/(2t), L_t(F)≤1/(16t²), and the represented laws converge weakly to δ_0. In initial coordinates, E_t→exp(−R/8) with 0<E_t≤1. Dominated convergence gives L¹ convergence of these weights, their normalizers tend to a strictly positive limit, and the normalized initial-coordinate laws converge in total variation. This does not contradict finite-time injectivity because the spatial flow collapses only in the infinite-time limit.

## 6. Scope and nonclaims

The result concerns the exact nonlinear radial quartic gradient and full positivity at all supplied times. It does not imply the same reverse lift for all coercive polynomial gradients, all polynomial drifts, truncated positivity, finite-data measurements, or initial full square positivity alone. The flow is injective but not onto R^d at positive times. Arbitrary closed-ball laws, especially laws charging its sphere, need not be attainable. There is no stability, algorithmic reconstruction, or two-sided complete-flow claim.

The independent checker verifies 106 finite exact controls, including the general symbolic radial recurrence, semigroup/cocycle/inverse formulas, all-homogeneous-degree backward cancellation, dimensions 1–3 gradient/SOS identities, normalized two-atom algebra, and seven nonzero-residual formula mutations. These supplement the universal written proof and are not a formal proof of the infinite hierarchy. Author replay, source hashes and complete frozen-input binding are recorded separately.
