# Full tensor moment dynamics under polynomial damping

10 October 2026 UTC. Additive ordinary mathematical research. The parent and investigator independently reached the weighted-square exhaustion and compact-sublevel uniqueness arguments. The parent proposed the stronger quadratic square-positivity theorem; this packet checks and proves it. These are participating derivations, not independent review. No protected source is changed; no formal-kernel, empirical, field-priority, canonical-integration, or T20-closure claim is made.

## 1. Results and the actual tensor interface

Fix a finite dimension 1≤d<∞. Let P∞(R^d) be the Borel probability measures for which every coordinate monomial is absolutely integrable. Let h be a real polynomial bounded below on R^d. Adding a constant to h changes neither the normalized hierarchy nor the normalized tilt, so throughout the proofs shift h so that h≥0. For a multi-index α, write m_α(t), and let L_t be the real linear functional on R[x_1,…,x_d] with L_t(x^α)=m_α(t). The full symmetric tensor record and this full monomial record carry exactly the same information.

Fix 0<T≤∞. Require m_0=1 and coordinatewise C¹ regularity on [0,T): continuity at zero, ordinary C¹ in the interior, and a continuous right derivative at zero. The hierarchy is

    dL_t(p)/dt = −L_t(hp)+L_t(h)L_t(p),   p∈R[x].           (H)

For h=Σ_β h_β x^β this means

    m_α′ = −Σ_β h_β m_(α+β)+(Σ_β h_β m_β)m_α.

Every sum defining an individual equation is finite. No Banach sequence norm or uniform-in-grade differentiability is assumed. For h=|x|², the degree-r equation involves contractions of degree r+2. Signed coordinates are allowed; individual odd moments need not be nonnegative.

**Theorem E, exhaustion without coercivity.** If L_t is represented by a probability in P∞(R^d) at every time, then there exists one fixed μ∈P∞(R^d) such that

    L_t(p) = ∫p(x)e^(−t h(x))dμ / ∫e^(−t h(x))dμ          (1)

for every polynomial p and 0≤t<T. Conversely every μ∈P∞ gives such a path for every t≥0. The law μ need not be unique when h is not coercive. Every finite-horizon moment path nevertheless has a unique extension to all t≥0 in this class.

**Theorem C, coercive classification.** If additionally h(x)→∞ as |x|→∞, the law μ in (1) is unique. Every positive-time full moment record is determinate among probabilities on R^d. For a fixed valid initial full moment record c, the admissible hierarchy paths are in bijection with its entire representing-law fibre F_c. Thus uniqueness of the path from c is equivalent to multivariate moment determinacy of c. Different initial laws with the same initial moments have different full tensor records at every positive time.

Coercivity here does not require h to dominate |x| or |x|² at infinity. The proof uses compact sublevels and joint polynomial-weighted h data, rather than replacing the vector x by the scalar h(x).

**Theorem Q, square positivity forces realizability for quadratic damping.** For h=|x|², replace all-time representability by the weaker algebraic assumption

    L_t(q²)≥0 for every real polynomial q and every t.       (S)

Then the conclusions of Theorem C still hold. In particular an initial representing law need not be assumed: its existence follows from (H), (S), and boundary regularity. The assumption (S) is positivity of every finite moment matrix, with no fixed degree cutoff. In several variables it does not imply representability for an arbitrary isolated functional; the dynamics supply the missing positive-time growth bounds.

Theorem Q also holds, after a constant shift, if h−c|x|² is a sum of polynomial squares for some c>0. It transports through any polynomial change of coordinates having a polynomial inverse. Positive-definite quadratic forms with affine terms are therefore covered, as is the explicitly nonquadratic example x²+(y−x^k)².

## 2. Unnormalization and joint square bounds

Define

    a(t)=exp(−∫_0^t L_v(h)dv),       A_t(p)=a(t)L_t(p).

The integral is finite on every compact time interval; a>0, a(0)=1, and A_t(1)=a(t). Product differentiation gives

    dA_t(p)/dt = −A_t(hp).                                  (2)

An induction over all polynomials at once bootstraps coordinatewise C¹ to C∞, including the one-sided boundary interpretation, and gives

    (d/dt)^n A_t(p) = (−1)^n A_t(h^n p).                    (3)

Under representability and h≥0,

    B_(q,n)(t):=A_t(q²h^n)≥0,       B_(q,n)′=−B_(q,n+1)

for every q and every n≥0. Taylor expansion backwards from t to t−b, 0<b<t, has nonnegative terms and nonnegative integral remainder. Consequently

    Σ_(n=0)^N b^n A_t(q²h^n)/n! ≤ A_(t−b)(q²).             (4)

Taking just the n-th term and then b↑t proves

    0≤A_t(q²h^n)≤n! A_0(q²)/t^n.                         (5)

On a small closed neighborhood of s>0 with times at least s/2, (3) and (5) bound the n-th derivative of A_t(q²) by n!(2/s)^n A_0(q²). The Taylor remainders therefore tend to zero for sufficiently small increments. Thus every A_t(q²) is real analytic for t>0. Polarization,

    p = ((p+1)²−(p−1)²)/4,                                (6)

proves the same for every A_t(p). This handles signed polynomial observables without treating their values as nonnegative scalar moments.

The actual positivity premise used in this section is only A_t(q²h^n)≥0 for all q,n,t. For a general nonnegative polynomial h, positivity on squares alone does not automatically supply it. No sum-of-squares representation of an arbitrary nonnegative multivariate polynomial is presumed.

## 3. Recovering the vector law and every boundary moment

Select one time s∈(0,T) and one representing probability ρ_s there. Put λ_s=a(s)ρ_s. This is a finite positive measure on R^d representing A_s. There is no need to choose representatives measurably as time varies.

For every q and 0<b<s, monotone convergence of the nonnegative exponential series and (4) imply

    ∫q² e^(b h)dλ_s
       = Σ_(n≥0) b^n A_s(q²h^n)/n!
       ≤ A_(s−b)(q²)<∞.                                 (7)

For u>0 define

    G_q(u)=∫q² e^((s−u)h)dλ_s.

This is finite on the whole positive half-line. When s−u≤0, finiteness follows from the polynomial moment of λ_s. For a positive exponent, (7) applies. On every sufficiently small neighborhood of u, an additional positive exponential margin below s dominates the absolutely summed Taylor series and all h-polynomial derivative factors. Hence G_q is real analytic and

    G_q^(n)(s)=(−1)^n A_s(q²h^n).

It has the same Taylor series at s as the real-analytic function A_u(q²). The identity theorem on the connected interval (0,T) gives

    A_u(q²)=∫q² e^((s−u)h)dλ_s,   0<u<T.                  (8)

As u↓0, these nonnegative integrands increase. Monotone convergence and continuity of A_u(q²) at zero give

    ∫q² e^(s h)dλ_s=A_0(q²)<∞.                           (9)

For q=1 the right side is one. Thus

    μ(dx)=e^(s h(x))λ_s(dx)                               (10)

is a probability, with finite square moments for every polynomial. Every polynomial is absolutely integrable, since |p|≤(1+p²)/2. Polarization (6) gives all signed moments, both at zero and at positive times. Equations (8)–(10) yield A_t(p)=∫p e^(−t h)dμ and therefore (1). This recovers the actual vector measure and every initial mixed moment, with no mass lost at zero.

Conversely, for μ∈P∞ and h≥0 polynomial, |p|h^n is integrable for every n. The exponential is at most one for t≥0. Dominated convergence, including |(e^(−u h)−1)/u|≤h at zero, proves the derivative formulas and (H). The normalizer is strictly positive at every finite time. Thus every such law supplies a global admissible path.

This proves Theorem E's existence statement. It also establishes a useful weakening: the full cone inequalities A_t(q²h^n)≥0 at all times and representability at a single positive time suffice. Initial validity and all remaining times' representability then follow. This is a full joint cone condition, not coordinate nonnegativity.

## 4. Coercive damping determines the full vector measure

Here is the classical static determinacy mechanism in the form needed for this application.

**Lemma.** Let h≥0 be a coercive polynomial. If a finite positive measure λ on R^d has every absolute polynomial moment and ∫e^(b h)dλ<∞ for some b>0, then its full polynomial moment sequence is determinate.

**Proof.** Suppose λ′ has the same full polynomial moments. Nonnegative-series monotone convergence transfers exponential integrability:

    ∫e^(b h)dλ′=Σ_(n≥0)b^n∫h^n dλ′/n!=∫e^(b h)dλ.

For any real polynomial p, choose 0<r<b/2. Cauchy–Schwarz gives

    ∫|p|e^(r h)dλ ≤ (∫p²dλ)^(1/2)(∫e^(2r h)dλ)^(1/2)<∞,

and likewise for λ′. Define the finite signed measure on [0,∞)

    τ_p = h_*(pλ−pλ′).

It has an exponential absolute moment of rate r and every moment vanishes, because p h^n is a polynomial. Absolute convergence therefore makes its Laplace transform zero near zero. The transform is real analytic for all positive arguments, so it is zero there. Finite signed Laplace uniqueness implies τ_p=0.

For completeness, signed Laplace uniqueness follows by pushing the signed measure forward under z=e^(−u) to (0,1], extending it by zero mass at 0, and using its values at nonnegative integer Laplace arguments. Its polynomial integrals on [0,1] vanish. Uniform polynomial approximation and finite signed measure uniqueness force it to vanish. Continuity of the transform at zero supplies its mass if only positive arguments were given.

In particular, for every R and p,

    ∫_{h≤R}p dλ=∫_{h≤R}p dλ′.

The set K_R={h≤R} is compact. The restrictions of coordinate polynomials contain constants and separate points, so Stone–Weierstrass and finite measure uniqueness identify λ restricted to K_R with λ′ restricted to K_R. Letting R↑∞ identifies the full measures. □

Apply the lemma to λ_s using (7) with q=1. Every positive-time full record is determinate. If μ and ν produce the same hierarchy path, their normalizers both solve Z′=−L_t(h)Z, Z(0)=1. They therefore equal a(t). At a positive s the tilted laws have the same full moments and hence are equal. Multiplying by e^(s h) and the common normalizer gives μ=ν. This proves Theorem C and its fibre classification.

Only compactness of h-sublevels was used at the measure-identification step. The same proof works relative to a fixed closed support K when h≥0 on K and {x∈K:h(x)≤R} is compact. No radial growth exponent or quantitative coercivity modulus is needed.

## 5. Exact ambiguity when coercivity is absent

For h≥0 without coercivity, define μ∼_hν by

    h_*(pμ)=h_*(pν) for every real polynomial p.            (11)

These are finite signed pushforwards; absolute polynomial integrability makes them well-defined. Equivalently, all polynomial-weighted Laplace transforms ∫p e^(−t h)dμ agree for t≥0. Signed Laplace uniqueness proves the equivalence.

Two initial probabilities generate the same normalized full moment path on any interval [0,T), T>0, if and only if (11) holds. Indeed, a common path determines the common normalizer a(t), hence all its unnormalized weighted transforms on (0,T). Each such transform is analytic for t>0: |p| is integrable and h^n e^(−δh) is bounded. Identity propagation extends equality to all positive t, then Laplace uniqueness gives (11). The reverse implication follows directly from the integrals.

Thus the solution set from an initial moment record c is exactly F_c modulo ∼_h. This proves the unique global extension assertion in Theorem E: even when distinct laws lift a finite path, all their later polynomial moments coincide. It does not make an arbitrary selection of representing measures at successive times into a single measure trajectory.

There is also an exact pathwise uniqueness test. At any fixed s>0, the proof of Section 3 can start with *any* representative of the full moment record L_s. De-tilting it produces an initial law for the entire same path. Conversely every initial-law lift gives such a representative. Therefore the set of initial-law lifts of one path is in bijection with the moment fibre at s. A path has a unique underlying law exactly when its full moment record is determinate at one, equivalently every, positive time. Coercivity guarantees this; it is not logically necessary for every particular path.

Initial determinacy still implies a unique path when h is merely lower bounded. Its converse can fail: for constant h every moment path is constant, even if the initial record has several representing laws. One must distinguish uniqueness of a coordinate path from uniqueness of the law lifting that path.

## 6. Square positivity is sufficient for quadratic damping

Assume h=|x|² and (S), with no representing measure initially or at positive times. A product of sums of polynomial squares is again a sum of squares. Therefore q²h^n is a sum of squares for every q,n, so the positivity and backward Taylor argument of Section 2 applies. In particular

    0≤A_t(h^n)≤n!/t^n.                                  (12)

The multinomial expansion shows that h^n−x_i^(2n) is a sum of monomial squares with nonnegative coefficients. Thus, for each coordinate i and t>0,

    0≤L_t(x_i^(2n))≤n!/[a(t)t^n].                        (13)

Using n!≤n^n gives, whenever this moment is positive,

    L_t(x_i^(2n))^(−1/(2n))
       ≥ a(t)^(1/(2n)) sqrt(t/n)
       ≥ min{1,sqrt(a(t))} sqrt(t/n).

With the standard value +∞ for a vanishing even moment, the same lower bound holds. Consequently every marginal Carleman series diverges.

We use the classical multivariate Nussbaum–Carleman theorem: a positive semidefinite full d-sequence satisfying the Carleman condition in every coordinate has a unique representing positive measure on R^d. The normalized mass is one. An inspected primary source is Putinar–Schmüdgen, *Multivariate Determinateness*, Theorem 25 and its following paragraph, printed p. 24, https://arxiv.org/pdf/0810.0840 . The source attributes this all-marginal consequence to A. E. Nussbaum.

It follows that L_t has a unique representing probability at every positive t. Section 3 requires only one such time and the joint positivity already established. It recovers μ at zero and the complete exact tilt trajectory. Theorem C supplies the rest. This proves Theorem Q.

### A sum-of-squares coercive certificate

Suppose after shifting a constant that h−c|x|² is a sum of squares, c>0. Then h is a sum of squares, and so is h−cx_i². For n≥1,

    h^n−c^n x_i^(2n)
      =(h−cx_i²) Σ_(j=0)^(n−1) h^(n−1−j)(cx_i²)^j

is a sum of squares. The proof above gives

    L_t(x_i^(2n))≤n!/[a(t)(ct)^n],

which again supplies all marginal Carleman conditions. Also h≥c|x|², so the coercive uniqueness proof applies. This is an explicit sufficient algebraic certificate; it is not asserted for every coercive polynomial or every nonnegative polynomial.

### Polynomial changes of coordinates and slow radial growth

Let Φ:R^d→R^d be a polynomial bijection with polynomial inverse Ψ, and suppose h(x)=|Φ(x)|²+C. Define a functional in u-coordinates by K_t(q)=L_t(q∘Φ). This preserves square positivity and coordinatewise regularity. Constants cancel in (H), so K_t satisfies the quadratic hierarchy. Theorem Q gives its measure and trajectory. Pushing the measure through Ψ gives the full x-law, all x-moments are finite because Ψ is polynomial, and substituting p∘Ψ recovers every original polynomial observable. Thus the conclusion is about x, not only about Φ(x) or h(x).

For example, Φ(x,y)=(x,y−x^k), Ψ(u,v)=(u,v+u^k), k≥3. The energy

    h(x,y)=x²+(y−x^k)²

is coercive: h≤R implies |x|≤sqrt(R) and |y|≤sqrt(R)+R^(k/2). Along (x,y)=(r,r^k), however, h=r² while sqrt(x²+y²) grows like |r|^k. Hence h/|(x,y)|→0 for k>2. Linear radial exponential integrability is not a necessary hypothesis for either Theorem C or this transported Theorem Q.

## 7. Discriminating exact controls and failure boundaries

### A noncoercive unobserved direction

Let ν_± be the inherited lognormal Stieltjes pair on (0,∞): density

    f_±(y)=f(y)[1±(1/2)sin(2π log y)],
    f(y)=exp(−(log y)²/2)/(y sqrt(2π)).

They are distinct, have all moments equal to exp(n²/2), and every moment is finite. Let X have law (δ_0+δ_1)/2, independent of Y, and put μ_±=law(X,Y) with Y∼ν_±. For h(x,y)=x² the normalized x=1 weight is e^(−t)/(1+e^(−t)); the y law is unchanged. Every mixed moment is identical for the two paths, while the vector laws remain different at every time. The observed x moments evolve nontrivially. Thus all-time realizability and the full tensor hierarchy do not force a unique law for a degenerate quadratic energy.

### Even a coercive scalar energy profile does not recover the vector law

Take R with standard lognormal density f, and define two real-line laws X_± by

    P(X_±∈dr)       = (1/2)f(r)[1±ε sin(2π log r)]dr,
    P(X_±∈−dr)      = (1/2)f(r)[1∓ε sin(2π log r)]dr,
    r>0, ε=1/2.

Both are positive probability laws and have the same |X| distribution. Gaussian square completion gives, for every integer n≥0,

    E[R^n sin(2π log R)]
       =exp(n²/2−2π²)sin(2πn)=0.

Their even moments are exp(2n²), and all odd moments vanish. Thus they have the same full initial moment record. For the coercive quadratic h(x)=x², their entire scalar h-law, scalar normalizer, energy mean, and energy moments coincide at every time.

Their vector laws nevertheless differ. Positive damping is injective on measures, and Theorem C makes the tilted full moment records determinate. Thus their full x-moment records differ at every positive time. More concretely their first moments are opposite:

    E_t[X_±]=±ε E[R e^(−tR²)sin(2π log R)]/E[e^(−tR²)].

The signed pushforward under r↦r² of r sin(2π log r)f(r)dr is nonzero (its density has a fixed positive sign for 1<r<exp(1/2)). Its Laplace transform is analytic for t>0 and cannot vanish identically on any open interval. Therefore the displayed means disagree somewhere in every positive open interval. There is no claim they differ at every individual time.

This control specifically defeats the shortcut of applying only the scalar theorem to h(X). Even all initial x-moments plus the entire subsequent scalar h-profile fail to distinguish these two full-vector continuations. The joint polynomial-weighted transforms in Sections 2–4 are essential.

### Dropping square positivity allows spurious quadratic solutions

The inherited flat-function construction embeds directly into h=x². Put f(0)=0, f(t)=exp(−1/t) for t>0, and b(t)=1−εf(t), 0<ε<1. Define

    A_t(x^(2n))=(−1)^n b^(n)(t),     A_t(x^(2n+1))=0,
    L_t(p)=A_t(p)/b(t).

This is coordinatewise C∞, satisfies the quadratic hierarchy, and starts from the valid determinate δ_0 record. But

    A_t(x⁴)=ε exp(−1/t)(2t−1)/t⁴<0,   0<t<1/2.

It violates the square test q=x² and cannot be represented. Thus the raw hierarchy does not provide the positivity hypothesis for free. This is an adaptation of the retained countercontrol, not a new flat-function phenomenon.

### A lower bound gives a universal forward domain

For a polynomial unbounded below, the universal global conclusion is false. Take h(x)=x and μ({−n})=2^(−n−1), n≥0. All moments are finite and the law has a positive exponential absolute moment near zero. Its tilt exists on 0≤t<log 2, with

    Z(t)=1/(2−e^t),       E_t[X]=−e^t/(2−e^t).

It is an everywhere-realizable smooth hierarchy path on that horizon, but its mean diverges as t↑log 2. It cannot extend continuously across the endpoint, and the partition function diverges there. A lower bound on h guarantees the universal damping domain used in this packet. It is not claimed necessary for every individually chosen initial law.

### Quadratic geometry and finite records

For h(x)=xᵀQx+bᵀx+c with Q symmetric, positive-definite Q is covered by completing the square and an invertible affine change of coordinates. If Q is positive semidefinite and b lies in its range, h is lower bounded, but a nonzero kernel leaves unconstrained directions like the preceding noncoercive example. Such a particular path may still be determinate; degeneracy merely removes the universal guarantee. Indefinite Q or a linear component along its kernel can make h unbounded below.

The vector dimension is finite. Infinitely many tensor grades over R^d are not infinitely many independent coordinates. A polynomial in an infinite collection of independent variables depends on only finitely many of them; the hidden-direction obstruction prevents silently transferring the universal uniqueness guarantee to that setting.

All statements concern complete polynomial records and all square tests. Finitely many moments, finitely many positive moment matrices, or a scalar energy record are not these inputs. The retained compact finite-prefix controls already show why a universal fixed-grade recovery rule cannot be inferred. No new sampling or complexity campaign is proposed.

### A semidecision for spurious quadratic hierarchy paths

There is a precise effective corollary, not an efficiency assertion. Fix a supplied positive rational T (or T=∞). Suppose the exact quadratic hierarchy, normalization, and stated C¹ regularity are promised, and the real coordinates L_t(x^α) can be approximated uniformly in α and rational t∈[0,T), with certified errors. If the path fails representability at any time, Theorem Q implies that L_s(p²)<0 for some time s and real polynomial p. Time continuity and continuity in its finitely many coefficients give such a strict witness at a rational t∈(0,T) with a rational polynomial q. This also covers a failure first detected at zero by moving a sufficiently small distance to the right.

Enumerate rational times and rational polynomials and dovetail certified approximations to their finite quadratic forms L_t(q²). Output a pair only when an enclosing interval has strictly negative upper endpoint. The procedure is sound, and the preceding argument proves termination for every spurious path under these promises. On a realizable path it never reports a witness. No computable detection time, degree bound, validity decision, or generic search implementation is claimed. Exact hierarchy compliance is a premise: this is not a general moment-representability semidecision for arbitrary isolated positive semidefinite multisequences. The retained computable-positive-hierarchy packet owns the predecessor search for its particular scalar counterexample; this consequence extends the witness-existence guarantee to the present promised quadratic dynamic class.

## 8. Inheritance and scope

The copied and hashed inputs in INPUT_BINDINGS.json remain byte-for-byte unchanged.

- The scalar realizable-moment-dynamics result owns unnormalization, backward-Taylor positivity, analytic identification from a positive-time representative, boundary untwisting, and the scalar initial-fibre classification. Replacing x by h(x) alone inherits only the h-law. This packet supplies joint-square lifting to the original vector law and separates exhaustion from uniqueness when h leaves indeterminate directions.
- The tensor-moment-continuation result owns the finite-channel tensor hierarchy, finite-support interpolation, and exact continuation interface. It assumes fixed finite support and does not contain this unrestricted multivariate positive-time reconstruction.
- The measure-moment-continuation-boundary result owns compact polynomial determinacy, scalar normalized tilts, lognormal moment matching, equal zero jets, and scalar positive-time separation. Its compact argument is used on energy sublevels here, not silently imposed on the original unbounded state.
- The determinate-moment-effectivity result owns effective recovery from uniformly named determinate half-line moments. It is not a multivariate algorithm for the present hypothesis. This packet adds no effective measure-reconstruction, condition-number, or efficiency assertion. Its separate negative-square semidecision is conditional on exact hierarchy and computable evaluation promises.
- The determinate-initial-positivity result also proves a scalar sufficient condition: for linear h=x on [0,∞), coordinate nonnegativity plus valid initial Stieltjes-Carleman growth forces the exact tilt. Theorem Q assumes neither initial representation nor initial Carleman growth, while requiring the stronger all-time full square positivity. The determinate-initial-positivity and computable-positive-hierarchy results show that scalar coordinate positivity plus determinate initial moments need not preserve realizability, and supply a computable failure witness. They do not refute Theorem Q: positivity of *all polynomial squares* is substantially stronger than nonnegativity of scalar moment entries.

For external ancestry, Putinar–Schmüdgen, *Multivariate Determinateness* (arXiv:0810.0840), Section 8, Theorem 31 and Corollary 32, printed pp. 31–32, gives classical reduction from a strictly determinate base and determinate/compact fibres to multivariate determinacy. The static lemma above is an elementary exponential-integrability specialization, with a compact-sublevel proof written out. Section 6 supplies the classical existence/determinacy input used in Theorem Q. These static facts are not claimed new. The search was targeted to multivariate determinacy and these sections; it was not an exhaustive literature search for hierarchy classification.

The project-relative additions are the complete full-vector hierarchy exhaustion, its exact noncoercive law ambiguity, the coercive path classification, and the quadratic dynamic upgrade from full square positivity to actual laws. The stronger quadratic route was proposed by the parent. None of these upgrades creates a finite-dimensional closure, identifies the infinite tensor product with an algebraic direct sum, recovers hidden labels, certifies an empirical source, or establishes epistemic or metaphysical uniqueness. The state is a declared finite-dimensional numerical vector law and the admitted update is its specified polynomial damping. The observable algebra is commutative and its tensor moments are symmetric. This is not the full graded tensor algebra of ordered semantic slots or noncommutative relational tensors; any further noetic transfer would require an independently supplied moment-law interpretation.

## 9. Executed evidence

check_controls.py checks exact symbolic finite-atomic hierarchy identities for quadratic and triangular-polynomial energies, rational semigroup and recovery instances, sums-of-squares identities, polynomial-coordinate inverses, lognormal integer cancellation, the degenerate-direction control, the flat-square violation, the signed geometric blow-up formulas, and all bound input hashes. These are discriminating finite controls supplementing the ordinary universal proofs, not a universal reconstruction algorithm or proof by finite sampling. The author run passed 332 exact checks. Run and result information is recorded separately in check_controls.log and CONTROL_RESULTS.json.
