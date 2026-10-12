# Realizable moment-hierarchy solutions are exactly initial-law tilt continuations

10 October 2026 UTC. Additive ordinary mathematical research. The parent proposed the classification and its main positivity/analyticity route; this packet supplies the complete proof, controls, and scope qualifications. No protected edit, canonical integration, closure, formal-kernel, empirical, or field-priority claim is made.

## 1. The classification

Let P∞ be the Borel probabilities on [0,∞) with finite moments of every nonnegative integer order. Fix 0<T≤∞. A coordinatewise C¹ path on [0,T) means each coordinate is continuous there, is C¹ in the interior, and has a continuous right derivative at zero. No norm on the sequence space and no uniform-in-grade derivative hypothesis is supplied.

**Theorem R.** Suppose m_r:[0,T)→R, r≥0, are coordinatewise C¹, m_0=1, and

    m_r′(t)=−m_(r+1)(t)+m_1(t)m_r(t)                 (1)

for every r, including the right derivative at zero. Suppose also that, for every t, the full sequence (m_r(t)) is represented by some probability in P∞. Then there is one and only one μ∈P∞ such that

    m_r(t)= [∫x^r exp(−t x)dμ]/[∫exp(−t x)dμ]       (2)

for every r and every 0≤t<T. In particular μ represents the initial moment sequence. Conversely, every representing initial μ gives an admissible path (2).

Consequently, for any fixed valid initial moment sequence c, its entire set of admissible coordinatewise C¹ solutions is in bijection with its full Stieltjes moment fibre

    F_c={μ∈P∞ : ∫x^r dμ=c_r for all r}.

Thus determinacy is exactly uniqueness in this solution class. Indeterminacy is the complete source of nonuniqueness, not merely a sufficient recipe for exhibiting two solutions. Every such finite-horizon solution extends to all t≥0 by its uniquely recovered μ. This is a classification of entire paths: (1) alone does not select which point of F_c is the actual initial law.

## 2. Unnormalization and regularity bootstrap

Set

    a_0(t)=exp(−∫_0^t m_1(v)dv),   a_r(t)=a_0(t)m_r(t).

The notation is consistent at r=0 because m_0=1. On every compact time interval the integral is finite; a_0>0 and a_0(0)=1. Equation (1) gives, including at the right boundary,

    a_r′=−a_(r+1),   a_r≥0.                           (3)

Starting with C¹ coordinates, (3) inductively gives C^k regularity for every finite k: if all a_r are C^k, the derivative of a_r equals the C^k coordinate −a_(r+1), hence a_r is C^(k+1). Thus

    a_r^(k)= (−1)^k a_(r+k)                           (4)

on [0,T) in the one-sided boundary sense. This is a coordinatewise induction; it makes no assertion about a Banach-space vector field.

For 0<b<t<T, Taylor's formula with integral remainder applied backwards gives

    a_r(t−b)
      = Σ_(k=0)^N b^k a_(r+k)(t)/k!
        + ∫_0^b (b−v)^N a_(r+N+1)(t−v)dv/N! .        (5)

All terms are nonnegative. In particular

    a_n(t)≤n! a_0(t−b)/b^n.

Letting b increase to t and using continuity at zero yields the especially simple bound

    0≤a_n(t)≤n!/t^n,   n≥0, 0<t<T.                  (6)

The convention at n=0 is a_0(t)≤1. Positivity has produced local uniform control that was not an input assumption.

## 3. Interior analyticity and exponential tails

Fix s∈(0,T). On a sufficiently small closed neighborhood of s contained in (0,T), every z is at least s/2. By (4) and (6),

    |a_0^(k)(z)|=a_k(z)≤k!(2/s)^k.

The order-N Taylor remainder about s at s+δ is therefore at most (2|δ|/s)^(N+1), when the intervening segment remains in that neighborhood. For sufficiently small |δ| this tends to zero. Hence a_0 is real analytic throughout (0,T), and all a_r are analytic by (4).

Now choose any one s∈(0,T), and let ρ_s represent (m_r(s)). Define the finite positive measure

    λ_s=a_0(s)ρ_s.

Its moments are a_r(s). By (5) with r=0 and monotone convergence of the nonnegative exponential series, for every 0<b<s,

    ∫exp(bx)dλ_s
      =Σ_(k≥0) b^k a_k(s)/k!
      ≤a_0(s−b)<∞.                                  (7)

More generally the same argument gives ∫x^r exp(bx)dλ_s≤a_r(s−b). In particular λ_s has exponential integrability at every rate strictly less than s. No measurable choice of representing measures as s varies is needed: we have selected exactly one measure at exactly one positive time.

## 4. Analytic identification and recovery of the initial law

For u>0 define

    G_s(u)=∫exp((s−u)x)dλ_s.

This is finite on the entire positive half-line by (7); when s−u≤0 only finiteness of λ_s is needed. It is real analytic there. Indeed, near any u_0>0 choose 0<d<u_0; the absolutely summed Taylor integrand is bounded by exp((s−u_0+d)x), whose exponent is strictly less than s and hence integrable. Termwise integration of the absolutely convergent exponential series proves local analyticity. Polynomial derivative factors are also integrable by leaving a further strictly positive exponential margin. Thus

    G_s^(r)(u)= (−1)^r ∫x^r exp((s−u)x)dλ_s.

At u=s its derivatives equal (−1)^r a_r(s)=a_0^(r)(s). Two real-analytic functions with the same full derivative sequence agree in a neighborhood. They consequently agree throughout the connected interval (0,T): a nonzero real-analytic difference has isolated zeros near each nonzero Taylor coefficient, so an interval of zeros cannot have an interior boundary. We obtain

    a_r(u)=∫x^r exp((s−u)x)dλ_s,   0<u<T.             (8)

This is also the requested semigroup consistency. For any positive t,u<T the representing unnormalized laws obey λ_u=exp((t−u)x)λ_t; uniqueness of these representatives follows from the exponential-moment argument in §5. The analytic proof establishes all links at once instead of choosing a chain of local neighborhoods.

As u decreases to zero, the integrands in (8) increase. Monotone convergence and coordinatewise continuity at zero give

    ∫x^r exp(sx)dλ_s=lim_(u↓0)a_r(u)=a_r(0)=m_r(0).

In particular the r=0 integral equals one. Therefore

    μ(dx)=exp(sx)λ_s(dx)                              (9)

is a probability with every required finite initial moment. Equation (8) gives a_r(t)=∫x^r exp(−tx)dμ throughout (0,T), and the same identity at zero follows from (9). Division by a_0 gives (2). There is no loss of mass in the boundary passage.

Conversely, for any μ∈P∞, dominated convergence yields A_r′=−A_(r+1) for A_r(t)=∫x^r exp(−tx)dμ, including the right derivative at zero, where |(exp(−h x)−1)/h|≤x for h>0 supplies the domination. Repeated differentiation uses the higher finite moments. A_0>0 at every finite t, so its normalized coordinates are C∞, are realizable, and satisfy (1). This construction supplies the global extension claimed in §1.

## 5. Uniqueness details and exact consequences

We use only the following elementary uniqueness facts, which also occur in the measure-continuation ancestor.

**Laplace uniqueness.** If two finite positive measures on [0,∞) have identical Laplace transforms at every t>0 and equal mass, push them forward by y=exp(−x) to (0,1], then extend by zero mass at 0. Their polynomial moments agree, since the n-th moment is the original transform at n. Polynomial approximation of continuous functions on [0,1] gives equality of the finite measures. For completeness, Bernstein polynomials approximate any continuous f uniformly: split their binomial expectation into |K/n−y|<δ, bounded by the uniform modulus of f, and its complement, whose probability is at most 1/(4nδ²). Thus equal polynomial integrals imply equal continuous integrals, and the usual uniqueness of finite Borel measures on a compact interval applies. The Borel inverse x=−log y gives the original measures. Equality of transforms on any open positive interval already suffices, by the real-analytic identity argument above and continuity at zero.

**Exponential moments imply moment uniqueness.** If λ has ∫exp(bx)dλ<∞ for some b>0, any positive finite measure with the same moments has the same finite exponential integral by monotone convergence. Its Laplace transform near zero is therefore the same absolutely convergent moment series. Analytic continuation on t>0 and Laplace uniqueness give equality of the measures.

If two initial laws realize the same path, their normalizers equal the path's a_0, because A_0′/A_0=−m_1 and A_0(0)=1. They have equal Laplace transforms on (0,T), so are equal. This proves the bijection in §1 and independence of the choice in §3.

Further consequences:

1. Every positive-time moment sequence is determinate. The representing law has every exponential moment of rate b<t, by (7) divided by a_0(t). This is derived for arbitrary admissible hierarchy solutions, not only assumed tilt solutions.
2. Distinct solutions with the same initial sequence have distinct full moment sequences at every t>0. Equality at one positive time would determine the same tilted law; multiplying by exp(tx) and normalizing would recover the same initial law.
3. Equality of scalar mean paths on any nonempty open positive interval also forces equal initial laws: integrating the logarithmic-normalizer identity makes the transforms proportional there; analytic continuation and their unit values at zero set the proportionality constant to one. Thus distinct solution means disagree somewhere in every such interval, although they need not differ at each individual time.
4. Every finite derivative at zero is fixed by the common initial moments via (1), despite the possible multiplicity of admissible paths. The infinite initial jet does not select a representing law in an indeterminate fibre.
5. There is no finite-time obstruction to forward continuation in this class. A finite T was never required to reach infinity in the proof: recovery on any nontrivial interval gives a law whose normalized damped tilt exists at every later finite time.
6. Combined with the determinate-moment-effectivity ancestor, a uniformly named determinate initial sequence computes the unique admissible solution and all of its coordinates on finite nonnegative parameter intervals. The present classification itself asserts neither an effective selection from a nonsingleton fibre nor an algorithm for deciding determinacy.

## 6. What the hypotheses do and do not say

The actual proof needs slightly less than all-time realizability: m_0=1, (1), nonnegativity of every coordinate throughout [0,T), and a representing probability at one positive time suffice. Equations (3)–(9) then imply full all-time realizability and the theorem. This is a proved strengthening, not a claim that mere coordinate nonnegativity implies moment realizability. Initial validity alone has not been proved interchangeable with the single positive-time premise.

**Countercontrol A: positivity cannot simply be omitted, even with valid determinate initial data.** Fix 0<ε<1 and put

    f(0)=0,  f(t)=exp(−1/t) for t>0,
    a_0(t)=1−ε f(t),  a_r(t)=(−1)^r a_0^(r)(t),
    m_r(t)=a_r(t)/a_0(t).

The function f is C∞ and flat at zero: each derivative is exp(−1/t) times a polynomial in 1/t, and exp(−y)y^k→0 as y→∞. Hence a_0 is positive, m_0=1, all m_r(0)=0 for r≥1, and the hierarchy holds identically. These are exactly the determinate initial moments of δ_0. But

    a_1(t)=ε exp(−1/t)/t²>0,
    a_2(t)=ε exp(−1/t)(2t−1)/t⁴<0   for 0<t<1/2.

So the path differs from the constant δ_0 path immediately and is not realizable. Bare coordinatewise C∞ hierarchy dynamics remain nonunique even at a determinate initial point when the moment-image constraint is dropped.

**Countercontrol B: coordinate nonnegativity is weaker than realizability.** For 0≤t<T with finite T>0, take

    a_0(t)=(T−t)/T,   a_1(t)=1/T,   a_r(t)=0 for r≥2.

Then all a_r≥0 and a_r′=−a_(r+1). The normalized coordinates are m_0=1, m_1=1/(T−t), and m_r=0 for r≥2. They solve (1) and are all nonnegative, but m_2−m_1²<0, so no probability represents them at any time. This example has invalid initial moments and is not an independence proof of positive-time realizability under a valid initial-sequence hypothesis.

**Finite prefixes are not the hypothesis.** Pointwise realizability concerns the full infinite sequence. Checking a fixed number of coordinates, nonnegative entries, or finitely many positive moment matrices cannot be substituted without another theorem. The ancestor already supplies finite-prefix matched compactly supported laws with different future means.

## 7. Ownership, transport, and scope ceiling

The three inspected ancestors are copied byte-for-byte under inputs/ and hashed in INPUT_BINDINGS.json.

- measure-moment-continuation-boundary-20261009/RESULT.md, §§2, 5–6, owns the normalized tilt semigroup, coordinatewise smooth hierarchy, lognormal nonuniqueness pair, equal boundary jets, positive-time exponential determinacy, and full-law finite-update rule. It proves uniqueness in a specified density/logarithmic-ODE class, but does not classify all coordinatewise moment-image ODE solutions.
- fisher-endpoint-geometry-20261010/RESULT.md owns the Fisher/Hessian/Bregman endpoint transport and its distinction between actual metric germs and equal derivative records. It does not add a general moment-hierarchy classification.
- determinate-moment-effectivity-20261010/RESULT.md owns effective recovery from uniformly named determinate full moments and actual damped updates. Its whole-mean constancy equivalence concerns the family of actual initial-law tilts. It does not first prove that all admissible abstract hierarchy solutions belong to that family.

The project-relative addition is the exhaustion statement: positivity, realizability, and the hierarchy force one underlying initial law and its actual-update path. It closes the gap between exhibited nonuniqueness and a complete description of admissible dynamics. This bounded ancestry comparison is not an exhaustive literature survey or a claim of field novelty.

No niche representation theorem for completely monotone functions is invoked. In particular, no Bernstein–Widder theorem on an infinite time domain is imported into a finite-time problem. The proof instead uses the given positive-time representing measure, elementary Taylor remainders, monotone/dominated convergence, and the analytic and Laplace uniqueness arguments supplied above. The basic uniqueness of finite Borel measures from continuous integrals is the only ordinary measure-identification fact used without re-proving its full measure-theoretic construction.

For the continuation interface, the source is a law of a declared nonnegative numerical trait, the record is the product of all its raw moments, and the output is its declared mean or full raw-moment path. The theorem does not identify this infinite product with a finite episode or algebraic direct sum; it adds no source reliability, epistemic entitlement, hidden-label recovery, noetic realization, or metaphysical conclusion. It does not turn a nondescending update into a well-defined update on the entire moment quotient: the initial fibre still parameterizes the possible solutions.

## 8. Finite executed controls

check_controls.py verifies exact symbolic finite-atomic hierarchy identities, unnormalization, rational semigroup/recovery instances, finite backward-Taylor positivity, and both countercontrols. These finite checks supplement the universal ordinary proof. They do not prove it by finite sampling, implement a universal measure reconstruction, or certify formal-kernel correctness. Verification results are recorded separately in check_controls.log.
