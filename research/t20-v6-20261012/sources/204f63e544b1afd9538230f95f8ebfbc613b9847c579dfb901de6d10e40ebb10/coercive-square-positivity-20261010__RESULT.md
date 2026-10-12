# Square positivity forces exact dynamics for every coercive polynomial

10 October 2026 UTC. Additive ordinary mathematical result. The preceding tensor-realizability packet is frozen and unchanged. The parent proposed the central-even-derivative route; the parent and investigator independently developed the scalar-measure/Radon–Nikodym bridge below. The static representation theorems are classical and explicitly identified. Participating proof development is not independent review. No field-priority, protected-edit, formal-kernel, empirical, or T20-closure claim is made.

## 1. The formerly open bridge closes

Fix 1≤d<∞, a real polynomial h on R^d with h(x)→∞ as |x|→∞, and 0<T≤∞. Let L_t be a real linear functional on R[x_1,…,x_d], coordinatewise C¹ on [0,T), including continuous right derivatives at zero. Suppose

    L_t(1)=1,
    L_t(q²)≥0 for every real polynomial q,
    L_t′(p)=−L_t(hp)+L_t(h)L_t(p) for every p.              (H)

**Theorem G.** There exists exactly one probability μ on R^d with all absolute polynomial moments finite such that

    L_t(p)=∫p e^(−t h)dμ / ∫e^(−t h)dμ,
    0≤t<T, p∈R[x].                                       (1)

Every positive-time full moment record is determinate. The path extends uniquely to all t≥0. For a fixed valid initial record, paths satisfying (H) are in bijection with its full representing-law fibre. Initial representability is not an assumption of the theorem: it follows from the path hypotheses.

There is no assumption that h, h+C, or h+C−c|x|² is a sum of squares. The prior quadratic/SOS-domination theorem is thus a special case. Full square positivity at every time remains essential. The theorem concerns a commutative polynomial moment functional, equivalently symmetric tensor moments of a finite-dimensional numerical vector; it is not an assertion about arbitrary ordered or noncommutative tensors.

The proof has two genuinely distinct steps. The hierarchy and square positivity give strong scalar growth along h at every interior time, without assuming any vector measure. These scalar measures then produce positive functionals on compact algebraic level sets of h, where a classical existence theorem applies. A theorem that already assumes a vector measure is not used to supply the missing existence.

## 2. Central Taylor positivity and interior analyticity

Add a constant to h if desired; normalized dynamics are unchanged. Define the positive factor and unnormalized functional

    a(t)=exp(−∫_0^t L_v(h)dv),      A_t(p)=a(t)L_t(p).

As in the frozen predecessor, coordinate regularity bootstraps through the finite polynomial equations to C∞, with

    A_t′(p)=−A_t(hp),      A_t^(k)(p)=(−1)^k A_t(h^k p).   (2)

No positivity of h is needed in this section. For a fixed polynomial q put f_q(t)=A_t(q²). Square positivity gives

    f_q^(2n)(t)=A_t((q h^n)²)≥0.                          (3)

Fix an interior s and b>0 with [s−b,s+b]⊂(0,T). Taylor's formula of order 2N+1 for v↦f_q(s+v) and v↦f_q(s−v), both on [0,b], has nonnegative integral remainder: each next derivative is f_q^(2N+2) at the respective intermediate time. Adding cancels all odd powers and gives

    Σ_(n=0)^N b^(2n) A_s(q²h^(2n))/(2n)!
      ≤ [A_(s+b)(q²)+A_(s−b)(q²)]/2 =: C_q(s,b).         (4)

In particular

    0≤A_s(q²h^(2n))≤C_q(s,b)(2n)! b^(−2n).               (5)

The same b works for every polynomial q, although C_q depends on q. This is a central-time estimate. It does not assert an origin Taylor radius or an exponential initial law.

For completeness these bounds also prove interior real analyticity without representability. On a compact neighborhood of s choose b uniformly so that all v±b remain in a larger interior compact interval, and let M_q bound f_q there. Then (5) bounds all even derivatives uniformly. Cauchy–Schwarz for the positive functional A_v gives

    |A_v(q²h^(2n+1))|²
       ≤ A_v(q²h^(2n)) A_v(q²h^(2n+2)).

Consequently all odd derivative magnitudes are at most

    sqrt(2) M_q (2n+1)! b^(−(2n+1)).

Here sqrt((2n)!(2n+2)!)≤sqrt(2)(2n+1)!. Taylor remainders tend to zero for increments smaller than b. Thus every f_q is analytic in the interior, and p=((p+1)²−(p−1)²)/4 gives analyticity of every A_t(p). This analytic conclusion holds for any real polynomial h, even without compact fibres; measure existence requires the next step.

## 3. A static positive-functional representation lemma

**Lemma F.** Let Λ:R[x]→R be square-positive with Λ(1)>0. Suppose every real level set K_r={x:h(x)=r} is compact and, for some b>0 and each polynomial q, there is a finite C_q such that

    0≤Λ(q²h^(2n))≤C_q(2n)! b^(−2n),  n≥0.                (6)

Then Λ has a finite positive representing measure on R^d, with every polynomial absolutely integrable. No representing measure is assumed anywhere in the construction below.

### 3.1 Scalar measures exist before the vector measure

For each q, the univariate sequence s_n=Λ(q²h^n) is Hamburger-positive: for every real univariate polynomial v,

    Σ_(i,j)v_i v_j s_(i+j)=Λ((q v(h))²)≥0.

The classical one-variable Hamburger existence theorem supplies a finite positive measure ν_(q²) on R whose n-th moment is s_n. Its mass is Λ(q²), possibly zero. For 0<c<b, (6) and monotone convergence give

    ∫cosh(c r)dν_(q²)(r)
       ≤ C_q Σ_(n≥0)(c/b)^(2n) < ∞,

so ∫e^(c|r|)dν_(q²)<∞. These scalar measures are unique. Indeed an exponential absolute moment gives the Hamburger Carleman condition; any competing positive representative has the same cosh integral by its nonnegative series and therefore the same exponential bound.

We will also use the signed version: two finite signed measures with exponential absolute moments and the same polynomial moments are equal. Their difference has zero moments; its positive and negative Jordan parts have equal moments and exponential tails. Hamburger Carleman uniqueness identifies those positive parts. This avoids presuming a vector measure or applying a multivariate theorem prematurely.

### 3.2 Polarization produces consistent signed measures

For every real polynomial p define

    ν_p = [ν_((p+1)²)−ν_((p−1)²)]/4.                      (7)

It is a finite signed measure with an exponential absolute moment and

    ∫r^n dν_p(r)=Λ(p h^n),  n≥0.                         (8)

Signed uniqueness proves real linearity in p. It also shows that when p=q², the signed definition agrees with the positive measure already constructed. Finally

    ν_(hp) = r ν_p                                        (9)

as finite signed measures. The two sides have the same moments, and multiplication by r preserves an exponential absolute moment after decreasing its rate slightly. Thus (9) is legitimate, not just a formal identity of moments.

For any Borel set B, the map p↦ν_p(B) is a square-positive linear functional. Its Cauchy–Schwarz inequality gives

    |ν_p(B)|² ≤ ν_(p²)(B) ν_1(B).                         (10)

Hence ν_p is absolutely continuous with respect to the positive finite measure ν_1. This holds for every real p, including p² itself. It rules out hidden weighted mass on ν_1-null sets.

### 3.3 A single null set suffices for real polynomial functionals

For each coordinate monomial x^α choose a real Radon–Nikodym derivative f_α=dν_(x^α)/dν_1. There are only countably many α. Remove a common ν_1-null set so that all these functions are finite and f_0=1.

For each rational-coefficient polynomial q, the finite quadratic combination of the f_α representing q² is the density of the positive measure ν_(q²), so it is nonnegative almost everywhere. There are countably many such q. Remove their exceptional null sets too.

Write the fixed real polynomial h=Σ_β h_βx^β. For each monomial x^α, (9) gives the almost-everywhere relation

    Σ_β h_β f_(α+β)(r) = r f_α(r).                      (11)

There are countably many α and only finitely many coefficients in h, even when those coefficients are irrational. Remove this final countable family of null sets.

For every remaining r define the real-linear functional

    ℓ_r(Σ_α p_αx^α)=Σ_α p_α f_α(r).

It has ℓ_r(1)=1. It is nonnegative on squares with rational coefficients. For each fixed finite polynomial support, this is a finite quadratic form in its coefficients; continuity and density of rational coefficients give ℓ_r(q²)≥0 for all real q. Equation (11), extended linearly over the finite support of p, gives

    ℓ_r((h−r)p)=0 for every real polynomial p.             (12)

Thus the same full-measure set supports normalized, square-positive functionals annihilating the full ideal (h−r). No uncountable intersection of full-measure sets has been taken.

### 3.4 Compact algebraic fibres supply the missing existence

The exact imported result is Schmüdgen's compact algebraic-set moment theorem: if the real zero set Z(I) of an ideal I⊂R[x] is compact, every square-positive linear functional annihilating I is represented by a positive measure on Z(I). In the author's revised Chapter 12 it is Corollary 12.34(iv), printed p. 14: https://arxiv.org/pdf/2309.10052 . It assumes a functional, not an already existing measure. The ideal need not be real radical.

Apply it to I=(h−r) and ℓ_r. Its real zero set is K_r, compact by assumption. The resulting measure has mass ℓ_r(1)=1. In particular the fibre cannot be empty at any r in our full-measure set. Equivalently one can use the preordering generated by h−r and r−h: (12) kills every nonconstant-generator term, and square positivity handles the remaining sum of squares. Compact preordering positivity is precisely the hypothesis of the author's Theorem 12.29. For an empty fibre the Positivstellensatz puts −1 in that preordering, contradicting normalization.

For any globally nonnegative real polynomial P, it now follows that ℓ_r(P)≥0 at every remaining r. By the definition of the densities and (8) at n=0,

    Λ(P)=ν_P(R)=∫ℓ_r(P)dν_1(r)≥0.                        (13)

Haviland's theorem supplies a positive measure representing Λ on R^d. Its mass is Λ(1), and the theorem gives integrability of every polynomial. This completes Lemma F.

No measurable family of fibre measures was selected or integrated. We use their existence only to establish the pointwise polynomial inequality in (13). The measurable integrands there are the explicitly constructed finite combinations of Radon–Nikodym densities.

The other imported existence statements are Hamburger's theorem and Haviland's theorem, checked in Schmüdgen, *The Moment Problem* (2017), Theorems 3.8 and 1.12 respectively: https://www.imath.kiev.ua/~golub/ref2/The-Moment-Problem.pdf . Scalar Carleman uniqueness is classical and was already explicitly sourced in the frozen predecessor. These are the precise external mathematical dependencies; they are not certified by the finite controls below.

## 4. Applying the lemma and recovering zero

For each s∈(0,T), set Λ=A_s. Its mass a(s)>0, its squares are nonnegative, and (4)–(5) give (6). Coercivity makes every K_r compact. Lemma F therefore supplies a probability representing L_s, without initially presuming representability at any time.

Now use the frozen full-vector exhaustion theorem. To check its boundary premises explicitly, shift h so that h≥0. Positive-time representatives give

    A_t(q²h^n)≥0 for every q,n and t>0.

Continuity of each polynomial coordinate gives the same inequality at zero. Thus the frozen theorem's joint cone premise holds on [0,T), and one positive-time representative is available. Its backward Taylor and monotone boundary recovery produce one probability μ with all the prescribed initial moments and the path (1). Coercive positive-time determinacy gives its uniqueness and the global continuation and fibre-classification conclusions.

There is no circular use of the earlier theorem: Lemma F first proves interior representation from square positivity alone. Only afterward do actual measures justify positivity of odd powers q²h^(2n+1). We never infer that positivity from h≥0 as a pointwise polynomial inequality before obtaining a representing measure.

This completes Theorem G. It also extends the predecessor's conditional negative-square semidecision to any fixed coercive polynomial with computable coefficients: under exact hierarchy/regularity promises and uniformly computable rational-time coordinate evaluations on a supplied rational horizon, failure of representability somewhere implies a strict rational-time, rational-polynomial square witness somewhere. The same dovetailed error-enclosure search applies. This is a corollary of the theorem, not a new detection-time or degree bound, validity decision, or measure-reconstruction algorithm.

## 5. A coercive energy excluded by the old SOS certificate

Use the classical ternary homogeneous Motzkin polynomial

    M(x,y,z)=x⁴y²+x²y⁴+z⁶−3x²y²z²,
    h(x,y,z)=M(x,y,z)+x²+y²+z².                           (14)

AM–GM applied to x⁴y², x²y⁴, and z⁶ proves M≥0; their product is (x²y²z²)³. Hence h≥x²+y²+z² and h is coercive.

Nevertheless M is not a sum of polynomial squares. Since M is homogeneous of degree six, a putative sum-of-squares representation would give a representation by homogeneous cubic squares. Zero x⁶ and y⁶ coefficients force the x³ and y³ coefficients of every cubic to vanish. Zero x⁴z² and y⁴z² coefficients then force x²z and y²z coefficients to vanish. Zero x²z⁴ and y²z⁴ similarly eliminate xz² and yz². The coefficient of x²y²z² is now the sum of the squares of the xyz coefficients, hence nonnegative, contradicting its value −3.

For arbitrary constants C and c, the degree-six homogeneous part of h+C−c(x²+y²+z²) remains M. In a polynomial sum of squares, its top nonzero homogeneous part is a sum of homogeneous squares: highest-degree terms cannot cancel across real squares. Thus no such expression is SOS, and in particular h+C is never SOS.

Theorem G covers this h under full dynamic square positivity. The old SOS-domination certificate does not. Pointwise h≥|x|² was insufficient to apply a square-positive functional to that comparison before representation existed. The new compact-fibre bridge removes precisely that gap. This is a classical Motzkin control used to distinguish hypotheses, not a claim that the polynomial is new or that every previous polynomial-coordinate corollary has been classified.

## 6. Why the geometric hypothesis matters

The central analytic bounds alone cannot imply vector representability. In d≥2 there are classical normalized square-positive polynomial functionals that have no representing measure. Taking h=0 and L_t equal to any such functional gives a stationary hierarchy satisfying all square tests and the central estimates, with no representing vector law. Its sole nonempty fibre is the noncompact whole space.

For a precise cited existence source, Schmüdgen 2017 Proposition 13.5 constructs an explicit square-positive non-moment functional on R[x,y]. Only that stated counterexample existence is needed here; it is not rederived or treated as one of our executed controls. Positive normalization is legitimate: a nonzero square-positive functional has positive value at 1, since Cauchy–Schwarz would otherwise make it zero.

Coercivity is a sufficient geometric condition for Theorem G, not a claimed necessary condition for every polynomial or every initial record. The static bridge needs compact level sets, whereas the inherited global forward-domain and uniqueness conclusions additionally use lower-bounded coercive damping. We do not extend those global conclusions to arbitrary unbounded-below energies merely because their individual level sets happen to be compact.

Initial moment indeterminacy also remains possible. The theorem forces a single law for each complete path; it does not force all laws sharing an initial moment record to be equal. The frozen signed-lognormal quadratic control already separates equal boundary jets and equal scalar energy profiles from different full-vector continuations.

## 7. Inheritance and evidence limits

The frozen packet is copied and hash-bound under inputs/. Its quadratic theorem, general representable-path exhaustion, compact-sublevel law uniqueness, boundary recovery, and countercontrols are unchanged. This successor removes its still-open general-coercive-polynomial square-positivity restriction, using the central estimate and a fully specified scalar-to-vector existence bridge.

The classical ownership is explicit: Hamburger and Haviland supply existence, scalar Carleman supplies exponential-tail uniqueness, and Schmüdgen's compact algebraic-set theorem supplies the fibre step. The parent and investigator participated in the new dynamic assembly and independently reached its measure-valued polarization route. No broad literature or field-novelty claim follows from this targeted check. In particular, the earlier Putinar–Schmüdgen determinacy theorem for an already given vector measure is not presented as a solution of this existence problem.

All dimensions are finite and all square tests are required. The infinite list consists of polynomial/tensor grades of a fixed numerical state, not infinitely many independent hidden variables. No finite sampling, noise model, truncation guarantee, noetic identification, psychological interpretation, source warrant, or metaphysical conclusion is asserted.

The exact controls in check_controls.py test central parity and remainder-kernel identities, odd derivative factorial bounds, finite-atomic signed-measure polarization and Borel-set Cauchy–Schwarz, fibre densities and reconstruction, the Motzkin coefficient elimination, and input integrity. They supplement the ordinary proof; they do not prove the representation theorems, implement a general Radon–Nikodym construction, or certify a formal proof kernel.

The author execution passed 761 exact checks; see check_controls.log and CONTROL_RESULTS.json.
