# Independent review of the arbitrary-coercive square-positivity extension

10 October 2026 UTC. Additive ordinary mathematical review. The previously accepted tensor packet is unchanged. This review supplies no formal-kernel, empirical, canonical-integration, or closure claim.

## 1. Verdict and candidate binding

**PASS. No substantive mathematical gap was found in Theorem G or Lemma F under their stated hypotheses. No mathematical correction was required.** In particular, the proof establishes vector-measure existence before using any predecessor theorem that requires it.

Reviewed candidate: `coercive-square-positivity-20261010/RESULT.md`.

    SHA-256: 204f63e544b1afd9538230f95f8ebfbc613b9847c579dfb901de6d10e40ebb10

The complete proof was independently read and checked. Its final change only records the executed author-control count. `author-snapshot/RESULT.md` retains the final byte-identical version. `REVIEW_RECEIPT.json` binds the review and executed evidence.

This reviewer received the proposed central-Taylor/fibre route, independently reconstructed it, and then reviewed the stable proof. This is an independent assessment of the assembled argument, not a blind review or a claim that the underlying classical mathematics is new.

## 2. Central estimates do not smuggle in localizing positivity

Before representation has been established, h≥0 pointwise would not justify Λ(q²h)≥0 for an arbitrary square-positive functional. The successor avoids that invalid step.

Its unnormalized derivatives satisfy

    (d/dt)^(2n) A_t(q²)=A_t((q h^n)²)≥0.

Taylor expansion through degree 2N+1 in both time directions has nonnegative next-derivative remainders. Adding the two expressions cancels every odd term. The resulting bound

    A_s(q²h^(2n))≤C_q(s,b)(2n)! b^(−2n)

is valid for an interior two-sided time interval. The common radius b is independent of q; the finite constant may depend on q. No initial exponential moment or origin Taylor radius is claimed.

The optional interior-analyticity argument is also valid. Positivity gives Cauchy–Schwarz between qh^n and qh^(n+1), controlling odd derivatives by adjacent even ones. The factorial comparison has the stated factor at most sqrt(2). Uniform estimates on a smaller time neighborhood make all Taylor remainders vanish. This statement holds without coercivity; it does not, by itself, prove vector representability.

## 3. Static Lemma F, audited in construction order

### 3.1 The first measures are only univariate

For each polynomial q, the sequence Λ(q²h^n) is Hamburger-positive because testing a univariate square amounts to testing (qv(h))² in the original algebra. Hamburger existence therefore supplies ν_(q²) on **all of R**. No support restriction to nonnegative energies, and no already existing vector law, is assumed.

The even factorial bound controls the cosh series. Consequently each ν_(q²) has an exponential absolute moment at every rate smaller than b. Zero mass causes no difficulty: the corresponding positive measure is zero. Scalar Carleman uniqueness applies, since the exponential bound gives even-moment Carleman terms bounded below by a positive multiple of 1/n.

The signed uniqueness argument is sound. A finite signed difference with zero moments and an exponential absolute moment has positive and negative Jordan parts with the same finite moments and exponential tails. Their common Hamburger moment problem is determinate, so those parts coincide and the difference vanishes.

### 3.2 Polarization gives actual equalities of measures

Polarization defines finite signed ν_p for every real polynomial p. Their moments are Λ(ph^n). Exponential-tail signed uniqueness then establishes real linearity and agreement with the positive construction when p is a square.

The relation ν_(hp)=rν_p is proved as equality of signed measures, rather than merely formal equality of moments. Multiplication by r leaves an exponential absolute moment after decreasing its rate, which is enough for the same uniqueness argument.

For every Borel B, p↦ν_p(B) is a genuine positive-on-squares linear functional. Its Cauchy–Schwarz inequality gives

    |ν_p(B)|²≤ν_(p²)(B)ν_1(B).

Hence ν_p≪ν_1 for each p. This rules out polynomial-weighted mass on a base-null set and justifies use of Radon–Nikodym densities. No polynomial-density theorem or unproved L² approximation is required.

### 3.3 A common null set really suffices

The construction uses three countable collections:

1. Densities for all coordinate monomials, including finiteness and the unit identity.
2. Nonnegativity of the densities for squares of rational-coefficient polynomials.
3. The h-multiplication identity for each monomial.

The polynomial algebra has a countable monomial basis. Although the fixed coefficients of h can be irrational, there are only finitely many of them, and the collection of monomial multiplication identities remains countable.

Outside the union of these exceptional null sets, the pointwise values define a real-linear functional ℓ_r. For each finite monomial support, square positivity is a finite quadratic form in its coefficients. Rational-coefficient positivity therefore extends to every real coefficient vector by ordinary continuity. The monomial h identities extend by finite real linearity to the whole ideal (h−r).

Thus, on one fixed full-measure set, all three required assertions hold simultaneously:

    ℓ_r(1)=1,  ℓ_r(q²)≥0 for every real q,
    ℓ_r((h−r)p)=0 for every real p.

No uncountable intersection of full-measure sets is used. These functionals need not be characters: conditional moments do not generally multiply. The proof does not assume that they do.

### 3.4 The compact-fibre theorem supplies existence, not only uniqueness

For each remaining r, the ideal I=(h−r) has compact real zero set by Lemma F's hypothesis. The cited compact algebraic-set theorem takes precisely a square-positive functional annihilating I and returns a representing measure on that zero set. It does not require that I be radical, that a vector law already exist, or that the coordinate multiplication operators already be jointly represented.

An empty fibre cannot support ℓ_r(1)=1. Hence empty fibres occur only in the discarded base-null set. In the coercive, shifted-nonnegative application, this also prevents negative energy values from retaining base mass, but that restriction is a conclusion rather than an input.

For any globally nonnegative polynomial P, existence of a fibre measure implies ℓ_r(P)≥0 at each good r. The function ℓ_r(P) is measurable and integrable because it is a finite linear combination of the already chosen monomial densities. Integrating gives Λ(P)≥0. Haviland then supplies a representing measure on R^d with all polynomial absolute integrals finite.

The argument does not select a measurable family of fibre measures or integrate such a family. It needs only their existence to obtain pointwise positivity. This is sufficient for the final Haviland application and avoids a measurable-selection gap.

## 4. The dynamic application and boundary are noncircular

At every positive time s, the central estimate gives Lemma F's hypotheses for A_s. Coercivity makes all level sets compact. Thus every interior L_s is represented before the older exhaustion theorem is invoked.

Only afterwards does the proof shift h to be nonnegative and infer A_t(q²h^n)≥0 from actual positive-time measures. Coordinate continuity supplies these inequalities at zero as well. The frozen joint-cone/one-positive-time version of the exhaustion theorem now has exactly its needed premises.

That inherited proof recovers total initial mass one and all signed mixed moments through its square-weighted monotone boundary argument. Coercive positive-time determinacy identifies the law underlying the complete path and yields the initial-fibre classification and unique global continuation.

Initial representability, initial Carleman growth, and a choice of an initial law are not covert assumptions. Conversely, uniqueness of the law for a complete path does not say that an indeterminate initial moment record has only one admissible path.

The static lemma assumes compact level sets. The full global theorem additionally uses lower-bounded coercive damping. The draft correctly avoids extending universal forward existence to unbounded-below energies merely because their individual fibres might be compact.

## 5. Discriminating controls and scope

The ternary homogeneous Motzkin example is valid. AM–GM gives M≥0, so h=M+|x|² is coercive. In a putative cubic-square representation of M, the zero pure and mixed coefficients eliminate the listed cubic coefficients in the stated order. The remaining x²y²z² coefficient is a sum of xyz-coefficient squares, contradicting −3.

Adding constants or changing a quadratic term leaves this degree-six obstruction intact. Thus h+C−c|x|² cannot be SOS for any constants C,c, and h+C is never SOS. This distinguishes the new theorem from the predecessor's constant-shift SOS-domination criterion. Pointwise h≥|x|² alone could not justify applying a merely square-positive functional to that inequality; the new existence bridge closes this specific gap.

The stationary h=0 countercontrol is also appropriate. A normalized square-positive non-moment functional gives an exact constant hierarchy and satisfies the central estimates, while its nonempty energy fibre is noncompact. This shows why central analyticity alone cannot replace the geometric premise.

The negative-square semidecision carries over with its explicit promises: exact hierarchy and regularity, known rational horizon, and uniformly certified rational-time coordinate evaluation. The theorem's contrapositive gives a strict square witness somewhere; finite-coefficient and time continuity give a rational witness. Dovetailed certified evaluations detect it. No total validity decision, computable detection bound, or measure-reconstruction algorithm follows.

All conclusions remain about finitely many numerical coordinates and their full commutative polynomial algebra. Infinitely many grades are not infinitely many independent variables, and neither scalar energy data nor a finite family of square tests replaces the full hypotheses.

## 6. Exact primary-source check

- [Schmüdgen, revised Chapter 12](https://arxiv.org/pdf/2309.10052), Corollary 12.34(iv), printed p. 14: the compact algebraic-set existence statement and its proof through the compact preordering theorem were inspected. It allows an arbitrary ideal, not only a radical ideal.
- [Schmüdgen, The Moment Problem](https://www.imath.kiev.ua/~golub/ref2/The-Moment-Problem.pdf), Theorem 3.8, printed p. 63: Hamburger existence from positive semidefiniteness; Theorem 1.12, printed pp. 17–18: Haviland existence with polynomial integrability; Proposition 13.5, printed p. 319: the positive non-moment functional used by the noncompact control. The relevant statements and surrounding proofs were inspected.

These are primary-text checks through parsed PDFs. No screenshot verification or local PDF hash is claimed. The classical representation results are imported, not proved by the finite controls. The assessment concerns project-relative dynamic assembly, not literature-wide novelty.

## 7. Execution and preservation

- Isolated fresh replay of the author checker: **761 exact checks passed**.
- Independently written controls: **394 exact checks passed**.
- Independent groups cover central parity, the even-remainder sign, signed energy values before support identification, measure polarization, Borel-set Cauchy–Schwarz, fibre ideal relations, real-coefficient square identities, recombination, nonmultiplicative fibre functionals, and the Motzkin coefficient obstruction.
- Six prior proof/review files were captured and their current originals rechecked byte-for-byte and by SHA-256. The prior tensor proof remains `449a28007af5a4d372d95be4d8f961a3ac577e723760f7a352327a05d4b6e17a`.
- The complete author receipt of the prior frozen packet, and the author receipt of this successor, were independently revalidated against their respective original files.

The author checker was run only in this separate review snapshot. No accepted predecessor or author candidate was edited. All new evidence is in this additive review directory.

These finite checks supplement the ordinary universal proof audit. They do not implement the abstract Radon–Nikodym construction or certify Hamburger, Haviland, the compact-fibre theorem, an infinite proof kernel, empirical correctness, source warrant, or metaphysical conclusions.
