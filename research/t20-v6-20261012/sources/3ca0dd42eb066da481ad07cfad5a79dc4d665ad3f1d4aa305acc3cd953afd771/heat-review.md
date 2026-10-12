# Heat transport obstruction: independent bounded review

10 October 2026 UTC. Additive mathematical and source review. The assignment supplied the proposed dilation and heat-functional constructions; the reviewer independently checked the source pages, hypotheses, algebra, and proofs. This is a review of the stated constructions, not a blind rediscovery claim. No existing packet was edited. No field-priority, publication, formal-kernel, empirical, or T20-closure claim is made.

## 1. Conclusions and limits

1. The precise uniform-time assertion in Curto–di Dio–Korda–Magron, arXiv:2211.04416v3, Corollary 3.22, printed p. 20, is contradicted by spatially dilating the Choi–Lam polynomial. Its SOS entry times are exactly 1/(9a²), for a>0, and hence have no finite uniform upper bound.
2. This does not contradict the pointwise assertion of Theorem 3.21. Every member of the counterexample family individually has a finite entry time. No conclusion about the entire paper or all its other results follows from this bounded check.
3. For the pure heat hierarchy, normalization, full square positivity at every time, and coordinatewise smoothness do not imply a representing probability. There are all-time normalized heat paths with every nonzero square strictly positive at every positive time, yet with no representing measure throughout a nontrivial initial time interval.
4. Consequently the damping theorem's reverse-existence and negative-square-witness conclusions cannot be transported to the pure heat generator by simply retaining these positivity/regularity hypotheses.
5. The counterexample starts with a nonmoment functional. When the initial functional is representable, the heat hierarchy is its Gaussian-convolution moment path. Distinct moment-equivalent initial laws remain distinct but moment-equivalent at every heat time, so positive-time determinacy and unique underlying-law selection also do not transfer.

## 2. Source identity and exact scope

Source: Raúl E. Curto, Philipp J. di Dio, Milan Korda, Victor Magron, *Time-dependent moments from partial differential equations and the time-dependent set of atoms*, https://arxiv.org/pdf/2211.04416v3 . The local supplied PDF identifies itself on its first page as v3, dated 26 August 2026. It has 27 pages; SHA-256:

    a01ce0c1b9d2f5cbdf6f55c655d03ddeb70179b29549f7fba5bc0f43f729be78

The reviewer read the relevant extracted definitions and statements and visually inspected the rendered printed pages 14 and 20. The inspected renderings are copied under source-checks/. The heat normalization is ∂t p=Δp, with heat kernel variance 2t per coordinate; it is not the generator Δ/2. The paper defines Pos(n,d) as all globally nonnegative real polynomials of degree at most d. In particular Pos(3,4) consists of inhomogeneous polynomials in three variables, not homogeneous ternary quartic forms.

Theorem 3.12, printed pp. 13–14, uses

    f(x,y,z)=1−4xyz+x²y²+x²z²+y²z²

and gives exact SOS entry time 1/9. Theorem 3.21, printed pp. 17–20, quantifies a finite time separately for each f in Pos(3,4). Corollary 3.22, printed p. 20, instead quantifies one finite τ for every member of Pos(3,4). Its proof asserts continuity of the entry-time function and invokes a compact base of the cone. There is no coefficient normalization, spatial normalization, lower degree restriction, or exclusion of constants in the printed corollary or the definition of the cone.

The explicit-version arXiv URL did not load in the reviewer's web fetch, so no separate network retrieval of that version is claimed. The version-specific assertion is based on the supplied PDF and its hash, not on a search-engine snippet. The arXiv abstract record was separately discoverable. No exhaustive version or later-correction search was performed.

## 3. Independent threshold derivation

Let H_t=e^(tΔ), interpreted on polynomials by its finite exponential series. Direct differentiation gives

    H_t f = f +4t(x²+y²+z²)+12t².                 (1)

The polynomial f is nonnegative: applying AM–GM to 1, x²y², x²z², y²z² gives a sum at least 4|xyz|, and hence at least 4xyz.

Here is a necessity proof independent of the source's displayed Gram matrix. Suppose H_t f=Σj q_j² for t≥0. Every q_j has degree at most two, since highest-degree homogeneous squares cannot cancel. The zero x⁴, y⁴, and z⁴ coefficients force the x², y², and z² coefficients of each q_j to vanish. Consequently write

    q_j=c_j+u_j x+v_j y+w_j z+A_j xy+B_j xz+C_j yz.

Treat each coefficient collection as a finite vector indexed by j. Coefficient comparison gives

    ||u||²=||v||²=||w||²=4t,
    ||A||²=||B||²=||C||²=1,
    <u,C>+<v,B>+<w,A>=−2.

Cauchy–Schwarz therefore implies 2≤6√t, so t≥1/9. This argument uses every possible SOS decomposition, with no assumption that a chosen Gram sparsity pattern is exhaustive.

At the threshold the exact identity is

    H_(1/9)f =31/27 +(xy−2z/3)²+(xz−2y/3)²+(yz−2x/3)².  (2)

For t≥1/9, subtracting (2) from (1) leaves

    4(t−1/9)(x²+y²+z²)+12(t²−1/81),

which is SOS. Thus the threshold is exactly 1/9, including its endpoint.

## 4. Dilation refutes the uniform statement

For a>0 set S_a p(x)=p(ax) and f_a=S_a f. Spatial substitution preserves nonnegativity and is an invertible linear change of variables, so p is SOS if and only if S_a p is SOS. The relation ΔS_a=a² S_aΔ gives

    H_t S_a=S_a H_(a²t).                            (3)

Therefore the exact entry time is

    T(f_a)=1/(9a²).                                 (4)

Every f_a is still in Pos(3,4), and f_a has constant coefficient one. For every proposed finite τ, choose a>0 so small that a²τ<1/9. Then H_τ f_a is not SOS. This directly contradicts the finite uniform inclusion in Corollary 3.22 under its printed quantifiers.

The proof's continuity assertion fails concretely: f_a tends coefficientwise to 1 as a decreases to zero, T(1)=0, but T(f_a) tends to infinity. A positive rescaling of a polynomial does not change its SOS entry time. Thus imposing a continuous amplitude normalization, such as unit coefficient norm, does not repair this failure. For a compact cone base cut out by a strictly positive linear functional ℓ, the normalized family f_a/ℓ(f_a) tends to 1/ℓ(1), with exactly the same divergent times. The issue survives this compact-base reformulation. A restriction that controls spatial scale would be an additional hypothesis, not an interpretation of the printed corollary.

This review does not conclude that the pointwise Theorem 3.21 is false. Formula (4) is fully consistent with its quantifier order.

### General fixed-time obstruction

Let Pos(n,2m) and SOS(n,2m) be distinct. No fixed finite t≥0 can satisfy H_t Pos(n,2m)⊆SOS(n,2m). For if t>0 did, applying the inclusion to S_a p and undoing the dilation would put H_(a²t)p in SOS for every a>0 and every p in Pos. As a decreases to zero these polynomials converge coefficientwise to p. The bounded-degree SOS cone is closed, so p would itself be SOS. The case t=0 is immediate.

For completeness, closedness here can be seen without an unbounded-degree argument. Use an orthonormal basis v of degree-at-most-m polynomials in L² of a ball. For any convergent sequence p_j=vᵀQ_jv with Q_j positive semidefinite, tr(Q_j)=∫p_j is bounded. The positive semidefinite Q_j consequently have a convergent subsequence. Its limit represents the polynomial limit as SOS. This argument is restricted to the fixed finite-dimensional degree space.

## 5. Full-functional heat obstruction

Fix n≥2 and a real linear functional Λ on the entire polynomial algebra R[x_1,…,x_n] with

    Λ(1)=1,    Λ(q²)≥0 for every polynomial q,

but with no positive representing measure. Such full functionals are classical. A precisely inspected source is Schmüdgen, *The Moment Problem* (2017), Proposition 13.5, printed p. 319, which gives a square-positive nonmoment functional on R[x,y] and the extension to higher dimensions. A nonzero square-positive functional can be normalized because Cauchy–Schwarz forces it to vanish identically if its value at 1 vanishes. Haviland's Theorem 1.12, printed pp. 17–18, implies that some globally nonnegative polynomial P has Λ(P)<0. Source: https://www.imath.kiev.ua/~golub/ref2/The-Moment-Problem.pdf . These existence facts are external inputs, not consequences of finite numerical controls.

Define, for every t≥0,

    L_t(p)=Λ(H_t p).                                (5)

This is well-defined on every polynomial because the heat series terminates. Every coordinate is polynomial in t and hence smooth, and

    L_t(1)=1,       dL_t(p)/dt=L_t(Δp).              (6)

### All-time square positivity, in fact strict at positive times

The following finite identity holds for every polynomial q:

    H_t(q²)=Σ_α (2t)^|α|/α! · (H_t ∂^α q)².         (7)

Only finitely many multi-indices contribute. To derive it, use independent variables x,y and restrict to the diagonal only after applying operators. Under restriction, Δ becomes Δ_x+Δ_y+2Σ_i ∂x_i∂y_i. These constant-coefficient operators commute. Expanding the mixed exponential and applying the two heat factors to q(x)q(y) gives (7).

For t≥0 the right side is a finite SOS, so L_t(q²)≥0. If q is nonzero, choose a nonzero coefficient c_α x^α of maximal total degree m. Its m-th derivative ∂^α q=α!c_α is a nonzero constant. For t>0, this term alone gives

    L_t(q²)≥(2t)^m α! c_α²>0.                       (8)

For a nonzero constant q this is simply Λ(q²)=q²>0. Thus every finite moment matrix is positive definite at positive times. Strict square positivity is not being mistaken for positivity on every globally nonnegative polynomial.

### Nonrepresentation on a genuine interval

Write

    L_t(P)=−η+Σ_(j=1)^r c_j t^j,
    η=−Λ(P)>0,  c_j=Λ(Δ^jP)/j!,
    B=Σ_(j=1)^r |c_j|,
    ε=η/[2(B+η)].                                  (9)

Then 0<ε≤1/2. For 0≤t≤ε, the nonconstant contribution has absolute value at most Bt≤Bε<η/2. Hence L_t(P)<−η/2<0 throughout [0,ε]. Since P is globally nonnegative, no positive measure represents any of those functionals. The path nevertheless satisfies every square test for every t≥0, and strictly every nonzero square for t>0.

No nonrepresentation assertion is made for later times outside the established interval. The argument does not require a common negative witness for all time, nor does it claim that heat can never render a particular nonmoment functional representable.

### Any prescribed finite horizon, with a different initial functional

The comparison author's stable draft adds a useful correctly quantified strengthening. For a>0 put Λ_a=Λ∘S_a and P_a=S_(1/a)P. Then Λ_a is normalized and square-positive, P_a is nonnegative, and (3) gives

    Λ_a(H_t P_a)=Λ(H_(t/a²)P).                       (10)

Given any finite H>0, choose a²>H/ε. The right side is negative throughout [0,H]. This constructs a heat path with nonrepresentability on the whole requested horizon, while maintaining all-time square positivity and strict positive-time square positivity. The initial functional depends on H. It does not construct one fixed path proved nonrepresentable for all time. Identity (10) was independently checked symbolically and algebraically.

## 6. Consequences for transporting the damping results

The frozen coercive damping theorem assumes

    L'_t(p)=−L_t(hp)+L_t(h)L_t(p)

and obtains representation from full dynamic square positivity. Its time-dependent successor additionally uses an explicit uniform SOS radial domination hypothesis. Their proofs derive growth control from their stated damping equations. They do not claim an arbitrary-generator reverse-existence principle.

The path (5) proves that replacing this equation by the pure heat hierarchy (6) destroys that reverse implication. In particular no search for a pair (t,q) with L_t(q²)<0 can detect this heat path's nonrepresentability: no such pair exists, even with unrestricted time and degree. This is an obstruction to transferring the witness theorem, not an error in the witness theorem under its original damping promises. It is stronger than a finite truncation counterexample because every polynomial square is nonnegative at every time.

The initial functional in this construction is not representable. That boundary fact must remain explicit. The construction alone does not challenge a theorem that separately assumes a valid initial law.

## 7. Valid-initial-law and uniqueness controls

Unlike the polynomial multiplication in the damping hierarchy, Δ lowers degree. For any initial full functional Λ, equation (6) has exactly the solution (5): prove this by induction on polynomial degree, integrating the already uniquely determined coordinate L_t(Δp), which has degree two lower. No moment assumption is needed for this algebraic uniqueness.

If Λ is represented by a probability μ having all polynomial moments, then L_t is represented by μ*γ_(2t), where γ_(2t) is the centered Gaussian with covariance 2t I. Convolution preserves finiteness of all absolute polynomial moments. Thus initial representability suffices for all-time representability under heat, and the full moment path is uniquely determined by the initial full moment record.

This still does not select a unique law from a moment-indeterminate initial record. If distinct probabilities μ,ν have the same full moments, their convolutions with γ_(2t) have the same full moments for every t≥0 by the polynomial heat formula. They remain distinct: equality after convolution would imply equality of their characteristic functions after cancelling exp(−t|ξ|²), which never vanishes, and hence μ=ν. Consequently their common heat moment record remains indeterminate at every positive time. Gaussian smoothing does not imply Gaussian tail integrability of an arbitrary convolved initial law.

This independently explains why the damping theorem's positive-time determinacy and pathwise selection of one actual initial law do not transfer to heat. It also prevents overreading the nonmoment-path obstruction as a failure of forward Gaussian convolution for valid laws.

## 8. Evidence and stopping boundary

INPUT_BINDINGS.json records hashes of the inspected source PDF/text and relevant frozen project proofs. check_controls.py and CONTROL_RESULTS.json contain exact symbolic algebra tests: heat formulas, threshold decomposition, scaling covariance, multi-index square-product identities, hierarchy identities, and finite-degree moment-indeterminacy transport identities. These controls supplement the universal proofs; no finite test certifies an infinite family of square tests or the external representation theorems.

The stable comparison draft read during this review is moment-evolution-source-comparison-20261010/RESULT.md, SHA-256 c9170636819e8c10b3a94362bc446e5b4424b2a149079f4fc4b1eaeb339b30ac. Its heat and uniform-time conclusions agree with this review. The parent subsequently added two bounded review tasks. Their separate verdicts are in AFFINE_EXTENSION_REVIEW.md and TRUNCATED_DIAGNOSTIC_REVIEW.md: the affine-plus-killing corollary passes under its stated V hypotheses, and the exact rational truncated backward-heat diagnostic passes with its finite-dimensional scope retained.

The review stops at these explicit conclusions. It does not review every argument of Theorem 3.21, validate every downstream corollary, adjudicate scholarly priority, publish a criticism, edit protected project material, or infer a broad literature conclusion from a local contradiction.

Final execution: 63 exact controls passed, comprising 52 algebraic/finite-dimensional controls and 11 bound-input integrity checks. The separate copied truncated author script also passed in the isolated replay directory and reproduced its frozen result byte-for-byte. A first test harness run needed rational-expression cancellation rather than expansion alone to recognize an already correct symbolic identity; no mathematical formula changed. REVIEW_RECEIPT.json records the final reviewed inputs, results, and scope exclusions.
