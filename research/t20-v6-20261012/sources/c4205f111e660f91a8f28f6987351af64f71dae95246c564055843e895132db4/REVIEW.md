# Independent review: effective polynomial separator search

10 October 2026 UTC. Separate ordinary mathematical review and bounded exact
controls. No change to the frozen main proof, protected sources, integration
status, or closure status.

## Verdict and target

PASS. The mathematical effectivity argument is sound for the explicitly specified
one-active/two-hidden-coordinate path with g(z)=z², at each supplied rational
t>0. The final reviewed target and file hashes are recorded in
TARGET_BINDING.json. This review does not assert that the generic separator
search or active-moment interval routine has been implemented or run.

The original draft had a wording error: q itself need not be nonnegative.
The nonnegative separator is H(z,u,v)=q(z)²F(u,v). I requested that correction,
the exclusion of the zero square from strict positivity, and an explicit final
division step if the output is to include an interval for L_t(H) itself.
All three narrow amendments now appear in the bound target, with the original
preimage preserved and before/after hashes recorded in the author's
REVIEW_AMENDMENT_RECEIPT.json. The final corrected target has SHA-256
dbfb6e5190a12d943c4f2530350ad66760f1f093fe631b3c6884de5ab38d00d5.
The corrections were made directly by this reviewer under root authorization;
they are not silently attributed to the author.

The main frozen proof remains RESULT.md SHA-256
c6dc162591a6827b8ae09a3b0be902ee53573435ae5b4f4ecfb1fc66ed835ada.
Its existence, density, and square-positivity arguments are inherited rather
than inferred from the finite controls in this review.

## 1. Actual computable hidden construction

The ordinary Schur source is a total rational recurrence. Its monomial index
and inverse use finite integer arithmetic. Midpoint precedence ensures that
each new off-diagonal entry refers only to earlier diagonal entries. The new
inverse matrix is produced by rational addition and multiplication, with no
unknown inversion, inequality, or limiting equality test. Every requested
monomial therefore requires a finite initial segment of a single fixed
dyadic-rational functional. This does not rely on the noncomputable definition
used by a separate Lean presentation.

At each signed-block stage, all residuals are exact rationals and there are
finitely many of them. Their absolute values, the required integer ceiling,
and the strict-growth constraint are decidable. Equal support points must be
combined before taking the positive and negative parts of each block; the
actual control algorithm does this. Exact rational sign tests then produce
the finite negative part. There is no Jordan-decomposition problem for an
unknown infinite measure: N is the sum of the negative parts of the specified
finite blocks, as the frozen proof requires.

For a monomial y^alpha, |y^alpha|≤|y|^|alpha|. Once n>M≥deg p, each monomial in
p is covered by the inherited block inequality. Summing coefficient absolute
values gives B_p 2^(-M). The constant monomial is included through radial degree
zero; the zero polynomial can simply return value zero. Signed coefficients
cause no gap because the estimate is absolute. All finite approximants are
rational. These facts prove a uniform computable Cauchy name for N(p).

For F, the coefficient absolute sum is 4 and degree is 6. Each negative block
is a positive measure and F≥3/4, so N_≤M(F) increases to N(F). The one-sided
interval and its width 4·2^(-M) are therefore correct. Each positive-degree
block has signed mass zero, so its negative mass is half its variation. The
sharper remaining-mass bound is exactly 2^(-M-1), not 2^(-M).

## 2. Active integral and series tails

Completing the Gaussian square gives

    exp(mx-x²/2) = exp(m²/2) exp(-(x-m)²/2).

For R>m≥0, the two omitted tails are bounded by twice the upper Gaussian tail
at R−m. The stated Chernoff bound therefore proves (3.1), including the
negative tail, whose shifted threshold is actually R+m and is no larger.
The derivative formula is

    f'(x) = (m−2t exp(2x)−x) f(x).

The displayed derivative majorant follows on [−R,R] for t≥0. It supplies an
effective Lipschitz constant and hence an elementary Riemann-sum error bound.
Together with interval evaluation of exp and π, this is a genuine computation
of the integral, rather than an appeal to black-box quadrature or weak
computability of the lognormal law.

There is no hidden undecidable threshold choice. For example, when an error
2^(-k) is requested with k≥0, the integer R=2m+2k+4 makes (3.1) smaller than
that error using e>2. A rational derivative majorant is obtained by replacing
exp(2R) by 3^(2R) and exp(mR) by 3^(mR), since R,m are integers and e<3.
A sufficiently fine rational mesh can then be chosen by integer arithmetic.
These deliberately loose bounds prove totality, not practical performance.

For the discrete numerator, |j|≥4m implies mj≤m|j|≤j²/4. Dropping the
nonpositive damping term gives exp(−j²/4). If the first omitted positive
index is J+1, successive comparison terms have ratio at most
exp(−(2J+3)/4). The bilateral geometric tail constant (3.3) is correct.
The same estimate with m=t=0 handles S. Its j=0 summand is one, so S≥1.
Division by S therefore has a supplied lower bound. The potentially tiny
active integrals need not be tested for exact equality with zero.

Expanding q² has finite rational support. Error allocation according to the
absolute values of its coefficients makes the corresponding integral values
uniformly computable even when the expansion has cancellation.

## 3. Normalization and interval output

The factors C cancel exactly in every normalized monomial coordinate. Both
active probability laws have second moment exp(2), and x↦exp(−tx) is convex
for t≥0. Jensen's inequality gives the two lower bounds in (4.2), with the
correct direction. Since n_0≥0, the denominator is positive with a computable
lower bound; no division by a merely presumed nonzero computable real occurs.

One entirely rational alternative lower bound is 3^(−ceil(9t)), using e<3,
exp(2)<9, and the alpha term alone. It is positive for every rational t≥0.
The given sharper computable bound is also sufficient.

For H=q²F, the numerator is W=−I_t(q²)+N(F)J_t(q²). Its minus sign uses the
inherited value Lambda(F)=−1. The normalization denominator remains
D=I_0+n_0J_0; it is not I_0+N(F)J_0. The proof keeps those quantities separate.

An upper-negative rational enclosure [w_lo,w_hi] for W is enough to certify
the sign symbolically. If the deliverable must enclose L_t(H) itself, obtain
any finite rational interval [d_lo,d_hi] containing D with d_lo>0. Then

    L_t(H) belongs to [w_lo/d_lo, w_hi/d_hi],

whose upper endpoint is strictly negative. This extra step terminates by the
effective denominator bound. The normalization need not be approximated
while searching for a candidate.

## 4. Existence, rationalization, and terminating dovetail

The frozen proof supplies a real-coefficient polynomial with W_t(q)<0 at
each t>0. The relevant L² density argument is justified by a positive
Gaussian moment of alpha_t+beta_t, followed by the signed Fourier-uniqueness
argument; it does not hold by merely assuming all lognormal moments exist
at t=0. The restriction t>0 is essential here.

At any fixed finite degree, W is a quadratic form with finite real entries,
so it is continuous in the coefficient vector. Strict negativity is open,
and rational vectors are dense. Therefore a rational-coefficient witness
exists. Neither a modulus for the existential density approximation nor an
effective choice of its approximating sequence is needed by the exhaustive
search.

A fully definite schedule is: at stage s, examine the first s rational
polynomials, requesting each W interval with width at most 2^(−s); accept
the first upper-negative interval. Each stage is a finite list of terminating
computations. A negative candidate has a finite enumeration index and a
strict sign margin, so one sufficiently late stage accepts. Earlier zero
candidates cannot block it. This proves totality for rational t>0 without
deciding equality or nonnegativity of arbitrary computable reals.

The returned H is rational-coefficient and globally nonnegative because
q²≥0 and F≥3/4. It cannot be an SOS polynomial if its L_t value is negative,
because the inherited path is strictly positive on every nonzero square.
There is no contradiction with strict square positivity.

## 5. Exact controls and limits

check_effectivity.py passed 7,206 exact assertions in its initial run. The
final run and exact count are recorded in EXACT_RESULTS.json. Controls include:

- All supplied input bindings and all 19 frozen-main manifest entries.
- The actual inherited Schur inverse through index 15 and its dyadic entries.
- An independently assembled forward-difference signed construction through
  degree 8, including exact corrections and all required lower-degree bounds.
- Hidden-polynomial tail constants, monotone F prefixes, and the sharper mass
  tail; the F check includes two blocks strictly beyond its degree.
- Gaussian square completion and derivative algebra, discrete exponent and
  geometric comparisons, normalization cancellation, and signed interval
  division.
- A toy dovetail schedule that bypasses an exact-zero first candidate. The
  toy values are expressly not evaluations of the actual path.

These finite controls do not prove the infinite theorem by sampling. No
generic active-integral enclosure implementation, actual separator search,
computed q, formal-kernel proof, representability decision procedure, or
runtime bound is claimed by these controls.

## 6. Additional semantic boundary: degree growth near zero

The phrase “no uniform degree bound” can be sharpened for this path. Put
B=N(F). Since P=Lambda+N, B−1=P(F)≥(3/4)P(1)>0. At t=0,

    W_0(q) = (B−1) integral q² d alpha.

For each fixed degree D this quadratic form is positive definite on the
finite-dimensional coefficient space, because alpha has positive density on
(0,infinity). Its finite matrix is continuous in t. Positive definiteness is
an open condition, so W_t remains positive definite for all sufficiently
small t≥0 on that degree-D space. Hence no degree-D separator can work there.
The minimal q degree in this q²F family necessarily tends to infinity as t tends to
zero from above. This is an ordinary consequence, not a quantitative rate.

The total search still gives a computable witness degree for each rational
t>0; “no degree bound” should not be interpreted as noncomputability of that
per-input output. The review covers only this fixed explicit path and does
not transfer effectivity to arbitrary supplied noncomputable schedules,
unknown positive hierarchies, or moment-representability problems in general.

Root subsequently supplied and this reviewer independently verified the stronger
finite-dimensional corollary in finite-prefix-realizability-delay-20261010:
every fixed total-degree prefix remains genuinely finitely atomically
representable for a sufficiently short initial interval. This proves degree
divergence for every nonnegative-polynomial separator, not only q²F. Its full
convex-cone proof and separate review are retained with that addendum; it is not
an inference from the q²F argument alone. No effective time threshold is given.
