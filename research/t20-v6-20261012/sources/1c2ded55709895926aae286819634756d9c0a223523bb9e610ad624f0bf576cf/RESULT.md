# Coercive energy moments: a direct inherited representation corollary

10 October 2026 UTC. Additive ordinary mathematical clarification within ACTIVE T20. This note transports two already proved and independently reviewed local lemmas. It is not a new representation theorem, independent review of this note, protected integration, formal verification, field-priority claim, or programme closure.

## 1. Answer and exact statement

**Yes.** Let L be a real linear functional on R[x_1,...,x_d], with L(1)=1 and L(q²)≥0 for every polynomial q. Let H be a coercive SOS polynomial. Suppose that, for finite M≥1 and a>0,

    L(H^n) ≤ M n! a^n,                 n=0,1,2,... .       (1)

Then L has exactly one representing Borel probability measure μ on R^d. Every polynomial is absolutely μ-integrable, and

    ∫ exp(sH) dμ ≤ M/(1−as),           0≤s<1/a.           (2)

No certificate H²−c|x|² SOS, no polynomial automorphism, no coordinate Carleman hypothesis, and no initially given vector measure are needed. SOS is more than this static conclusion needs: existence uses only the even-power instances of (1), compact fibres of H, and square positivity of L. For the stated nonnegative coercive H, uniqueness follows by compact-sublevel exhaustion after existence. In fact the even-power version works for any coercive real polynomial H, using exponential |H| integrability and a constant shift only after obtaining the measure.

The cases of zero weighted square moments cause no division. If a=0 is admitted, L(H²)=0 implies L(Hp)=0 for all p by Cauchy–Schwarz. The compact algebraic-set theorem applied to (H) gives a measure on the compact zero set of H, and compact-support determinacy gives uniqueness. If this zero set is empty, no normalized L with those hypotheses exists.

## 2. Deduplication and the one-line bridge

The exact existence input is Lemma F in `coercive-square-positivity-20261010/RESULT.md`, §3. Its static hypotheses are:

    all sets {H=r} are compact;
    for one b>0 and every polynomial q, some finite C_q satisfies
    0≤L(q²H^(2n))≤C_q (2n)! b^(−2n) for every n≥0.       (3)

The lemma starts with an abstract square-positive functional, not a represented measure. It was independently reviewed in `coercive-square-positivity-independent-review-20261010/REVIEW.md`, §3, with a PASS for exactly that construction.

The unweighted assumption (1) supplies every missing weighted bound algebraically. Cauchy–Schwarz for L, applied to q² and H^(2n), gives

    0≤L(q²H^(2n))
       ≤sqrt(L(q⁴)) sqrt(L(H^(4n)))
       ≤sqrt(M L(q⁴)) sqrt((4n)!) a^(2n)
       ≤sqrt(M L(q⁴)) (2n)! (2a)^(2n).                 (4)

The last inequality is the elementary identity and estimate

    (4n)!/((2n)!)² = binomial(4n,2n) ≤ 2^(4n).

Thus (3) holds with b=1/(2a) and C_q=sqrt(M L(q⁴)). The value of b is common to every q. The constant C_q is allowed to depend on q, precisely as required. Coercivity makes every fibre compact. Lemma F therefore supplies existence immediately.

This is the actual increment of the note: recognizing that the already available weighted scalar/fibre lemma applies to the unweighted factorial bound through (4). The earlier central-even-time-derivative argument was one way to obtain (3); it is not part of the static lemma's premises and need not survive gradient transport.

## 3. Why that existence invocation crosses the semantic gap legitimately

Here is the inherited construction in enough detail to identify what is being used.

For each q, the scalar sequence L(q²H^n) is Hamburger-positive, since testing a one-variable square v² amounts to L((qv(H))²)≥0. Hamburger's theorem gives a positive scalar measure ν_(q²) on R. Estimate (3), summed as a cosh series, gives this measure an exponential absolute moment at every rate below b; it is consequently unique.

Polarization defines finite signed scalar measures ν_p with moments L(pH^n). Exponential-tail signed uniqueness proves linearity in p, agreement with the positive construction for p=q², and the identity

    ν_(Hp)(dr) = r ν_p(dr).                            (5)

For every Borel set B, p↦ν_p(B) is a square-positive functional. Its Cauchy–Schwarz inequality gives

    |ν_p(B)|² ≤ ν_(p²)(B) ν_1(B),

so ν_p is absolutely continuous with respect to ν_1. Choose Radon–Nikodym densities for the countable monomial basis. Remove one null set containing the exceptions for those densities, rational-polynomial square positivity, and the monomial identities (5). Finite-dimensional continuity in the coefficients extends square positivity to every real polynomial. Outside that one null set the resulting functional ℓ_r satisfies

    ℓ_r(1)=1,   ℓ_r(q²)≥0,   ℓ_r((H−r)p)=0.            (6)

Schmüdgen's compact algebraic-set moment theorem supplies a measure representing ℓ_r on {H=r}. Its exact primary statement is Corollary 12.34(iv), printed p.14 of [the author's revised Chapter 12](https://arxiv.org/pdf/2309.10052). The ideal need not be real radical. An empty fibre cannot support a normalized functional of this kind.

For a globally nonnegative polynomial P, fibre existence implies ℓ_r(P)≥0. Integrating its already constructed scalar density gives L(P)≥0. Haviland's theorem now yields the vector measure representing L. No measurable selection of fibre measures is needed; their existence is used only for this positivity implication. No coordinate-operator strong commutation, spectral-domain invariance, or application of L to an arbitrary pointwise nonnegative comparison is assumed.

Hamburger and Haviland are Theorems 3.8 and 1.12 of [Schmüdgen, The Moment Problem](https://www.imath.kiev.ua/~golub/ref2/The-Moment-Problem.pdf). The local lemma, its complete proof, and its independent review are inherited, not presented as newly established here.

## 4. Uniqueness is also inherited, with its premises now met

After representation has been obtained, H≥0 pointwise permits monotone convergence of the exponential series. This proves (2). The static determinacy lemma in `tensor-realizability-extension-20261010/RESULT.md`, §4, now applies. Its compact-sublevel argument was checked in `tensor-realizability-independent-review-20261010/REVIEW.md`, §3.

For clarity, suppose μ and μ′ represent L. Both obey (2). Fix s with 0<s<1/a. For each polynomial p and 0<r<s/2, Cauchy–Schwarz under either actual measure gives

    ∫|p| exp(rH) dμ
       ≤sqrt(L(p²)) sqrt(∫exp(2rH)dμ)<∞,

and likewise for μ′. Therefore the signed measure

    τ_p = H_*(pμ−pμ′)

has an exponential absolute moment. Its every scalar polynomial moment vanishes, because pH^n is an ordinary polynomial whose integrals agree. A finite signed measure with an exponential absolute moment and zero polynomial moments is zero: its Jordan parts have the same moments, and scalar Carleman determinacy identifies them. One inspected primary statement of scalar Carleman is Theorem 24, printed p.24, in [Putinar–Schmüdgen, Multivariate Determinateness](https://arxiv.org/pdf/0810.0840v1).

Hence, for every R and every p,

    ∫_{H≤R} p dμ = ∫_{H≤R} p dμ′.                     (7)

Both restricted measures are carried by the same compact set {H≤R}. Coordinate polynomials contain constants and separate its points. Stone–Weierstrass and finite measure uniqueness identify the restrictions. Exhaustion as R→∞ gives μ=μ′.

In the broader even-power variant, the represented measures satisfy ∫cosh(sH)dμ<∞ for s<1/a and hence have exponential |H| moments. The same signed-pushforward proof works; coercivity still makes {H≤R} compact. This explains precisely why the SOS property is unnecessary for the static result itself.

## 5. What this changes, and what it does not establish

For the energy-controlled gradient hierarchy, the already proved estimate

    A_t(H^n)≤n!t^(−n)

and square positivity give the present theorem at each positive time after normalization: L_t=A_t/A_t(1), M=A_t(1)^(−1), a=1/t. Consequently **positive-time existence and joint determinacy** need no extra radial SOS certificate whenever H itself is coercive and SOS. After existence,

    ∫exp(sH)dν_t ≤ 1/(1−s/t),        0≤s<t,

for the finite measure representing A_t. This conclusion is a direct application of inherited results plus (4).

It does not automatically replace every use of the radial certificate in the existing full reverse-lift proof. In particular, exponential H tails need not imply exponential |x| tails. The Fourier-Taylor and analytic-continuation proof of the transport PDE used the latter. Removing that hypothesis from the entire gradient/transport theorem requires a separate justified polynomial-to-smooth-test argument or another dynamical identification route. Static determinacy alone does not prove such a passage. No full unrestricted coercive-gradient reverse-lift claim is made here.

The polynomial-automorphism example H=x²+(y−x^m)², m>2, already shows why coordinate Carleman and linear radial exponential tails are the wrong necessary conditions. Its inherited joint-determinacy proof is compatible with the present corollary; it is not a new example or a proof of arbitrary transport.

If coercivity/compact fibres are dropped, the statement fails: set H=0 and use a normalized square-positive non-moment functional on R[x,y]. It satisfies (1) for all n but is not representable. The inherited exact source is Schmüdgen 2017, Proposition 13.5, printed p.319. This does not counter the coercive statement and was not recomputed as a new counterexample campaign.

## 6. Evidence status

The bounded local deduplication included the requested polynomial-transport, changing-objective square-positivity, energy-controlled gradient, multivariate non-moment control, and their directly relevant predecessors/reviews. Source statements above were rechecked in parsed primary PDFs. No new independent review, formal proof-kernel run, visual PDF verification, or comprehensive literature survey is claimed. Exact input hashes and a small integer check of the sole additional factorial comparison are retained separately. Those finite checks supplement the universal algebraic proof; they do not certify the imported measure theorems.
