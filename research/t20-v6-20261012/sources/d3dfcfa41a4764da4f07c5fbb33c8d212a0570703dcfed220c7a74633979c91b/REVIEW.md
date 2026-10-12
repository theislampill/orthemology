# Independent review: genuine initial law, immediate loss of joint representability

10 October 2026 UTC. Independent mathematical and exact-control review of the frozen author packet. No source integration, protected-file edit, publication, or closure action is performed.

## Verdict

PASS for the ordinary mathematical claim in the frozen RESULT.md, with no mathematical blocker found. For each supplied continuous, locally bounded-degree SOS schedule depending on a fixed finite controlled subspace, with positive-time cumulative quadratic coercivity there, and with at least two hidden coordinates, the construction gives a full strictly square-positive normalized coordinatewise C1 hierarchy path whose initial full moment record has an actual probability representative and whose full record has no positive representative at any positive time. The elementary autonomous example is coordinatewise C-infinity up to time zero.

The initial record is indeterminate. This verdict does not cover a determinate initial joint record, a law-level evolution required to be the tilt of the supplied initial law, or kernel verification of the signed-measure and analytic arguments. The optional polynomial separator is proved to exist; its coefficients and degree are not computed.

Reviewed RESULT.md SHA-256:

    c6dc162591a6827b8ae09a3b0be902ee53573435ae5b4f4ecfb1fc66ed835ada

Reviewed author FROZEN_MANIFEST.json SHA-256:

    264f821d1d49047f8d2baed466e35edf8d6d877a5105e03319aea94703824ea8

All 19 frozen-manifest entries and all 12 original/source-copy bindings were verified. The packet was copied before replay. The original author files remain untouched.

## 1. Signed representation: all degrees, not a finite prefix

The finite-difference operator has the correct sign, factorial, radius exponent, and tensor-product convention. For total degree n, its beta moment is one exactly at beta=alpha and zero at every other beta of total degree at most n. Zero components of alpha cause no exception: their one-point factor at zero and the convention 0^0=1 give the intended moments.

Every support point satisfies Euclidean norm at most nR. Summing absolute coefficients gives the displayed 2^n/alpha! factor. The choice R_n >= 2^n n^(n-1) B_n, together with R_n>=1, implies the bound 2^(-n) for every radial degree m<n. This remains valid for n=1 and for a zero residual block. Taking the least eligible integer is well defined; rational input moments produce rational residuals and finite-block weights.

For complete clarity, the positive measure |rho_0|+sum |rho_n| has finite total mass and every radial moment: for each fixed degree m, the blocks n<=m are finitely many finite-support measures and the remaining integrals are bounded by a geometric series. It dominates the variation of the signed sum. It therefore justifies the series/integral exchange for each monomial by absolute integrability. Future blocks have zero lower moments, so the degree-m corrected moment persists in the infinite limit. No step assumes that a finite computed prefix is the infinite measure.

The blockwise positive and negative sums are valid positive measures even if atoms overlap between different blocks. They are not asserted to be the mutually singular Jordan parts of the final signed measure. Each positive-degree block has zero mass, so its negative mass is half its variation. Thus N(1)<=1/2, P(1)=1+N(1), and P-N has every prescribed moment. Applied to Lambda, N cannot vanish, since otherwise Lambda would be a positive measure contradicting its negative value on F>=3/4. Consequently 1<C<=3/2 is correct.

## 2. Inherited functional and product positivity

I read the entire ordinary full-functional proof, including the exceptional monomial order, global midpoint precedence, Schur-completion induction, full-polynomial passage, and witness bound. That proof supplies one full-algebra Lambda, not a family of unrelated truncations. The nonnegative witness has Lambda(F)=1+1+1-4=-1 and F>=3/4 everywhere. The actual bound could be improved, but the stated bound suffices.

Tensoring Lambda with the extra Gaussian hidden coordinates preserves strict square positivity. A nonzero polynomial retains a nonzero polynomial in the first two hidden coordinates on a nonempty open set of the additional coordinates. Lambda is strictly positive on its square there, and Gaussian mass of the open set is positive. All hidden evaluations are finite polynomial expressions, so there is no illicit infinite operation inside Lambda.

The domination statement is exactly square-order domination: P(q^2)=Lambda(q^2)+N(q^2)>=Lambda(q^2). It is not a claim of positivity on all pointwise nonnegative polynomials, measure-order domination of Lambda, or an operator strong-commutation conclusion.

The frozen packet separately identifies the later full-functional Lean report and receipt. This review does not rerun that kernel build. Their presence does not formalize the present signed-measure construction or hierarchy path.

## 3. Active moment-equivalent measures and genuine initial law

The continuous lognormal moment exp(m^2/2) and the bilateral discrete lognormal moment agree for every nonnegative integer m by completing the square and shifting the summation index by the integer m. The bilateral Gaussian series is finite. The product extension with ordinary Gaussians preserves all joint active moments and all absolute polynomial moments.

The Borel set E is the union of the hyperplanes z_1=exp(j). It carries beta and has alpha mass zero. The continuous alpha has positive density on z_1>0. Multiplication by exp(-K_t), positive everywhere for every finite t, preserves both the singularity and the positive density on that half-space.

At t=0, replacement of beta by alpha is legitimate only after the hidden evaluation, which leaves a polynomial in z. Then Lambda_k+N_k=P_k gives the actual probability alpha tensor (P_k/C). Its total mass is C/C=1 and its absolute polynomial moments are finite. The distinct probability beta tensor (P_k/C) has the same full moments, proving the expressly stated indeterminacy.

The same P_k, N_k, alpha, and beta work for every supplied schedule in the stated class; no part of their construction depends on the schedule.

## 4. Full strict positivity, time regularity, and normalized equation

For any nonzero joint polynomial p, a hidden-monomial coefficient is a nonzero active polynomial. Its nonvanishing set intersects the open half-space z_1>0 in a nonempty open set. On that set Lambda_k(p(z,.)^2)>0. Its integral against alpha_t is strictly positive. The N_k term is nonnegative everywhere. Thus every nonzero polynomial square has strictly positive A_t and L_t values for every time, including zero. No topological support assertion about P_k is required.

The normalizer a(t)=[alpha_t(1)+n_0 beta_t(1)]/C is strictly positive at every finite time and equals one at zero. Local degree and coefficient bounds for the continuous schedule supply polynomial majorants for differentiated integrands. SOS positivity gives exp(-K_t)<=1. Both active measures have every absolute polynomial moment. Dominated differentiation therefore gives A'_t(p)=-A_t(g_t p), including the right derivative at zero, and continuity of that derivative. The quotient rule yields precisely the stated plus sign on L_t(g_t)L_t(p).

For g=z^2, all repeated derivatives require only additional polynomial moments, so coordinatewise C-infinity on the half-line is valid. The proof does not assert a convergent Taylor series or a measure formula extending to negative time.

## 5. No joint representative at any positive time

Fix one arbitrary positive time. From K_t>=c|z|^2, the known active radial moments and monotone convergence imply that any hypothetical positive representative nu of A_t satisfies integral exp(c|z|^2) dnu<=1. The constants are correct: the bound is (1+n_0)/C=1. The measure nu is introduced only inside this contradiction argument.

The F-weighted active projection sigma is a finite positive measure because F>=3/4 and its polynomial moments exist. Its Gaussian absolute moment is controlled at exponent c/2 by Cauchy-Schwarz using the genuine polynomial moment F^2 and the established exp(c|z|^2) moment. The exponent reduction is essential and is handled correctly.

For every active polynomial q, sigma(q)=A_t(qF)=[-alpha_t(q)+N_k(F)beta_t(q)]/C. Thus its moments match the explicit signed measure w_t. The sign in front of alpha_t is negative because Lambda_k(F)=-1; N_k(F) is finite and nonnegative. The variation of w_t has a finite Gaussian moment at exponent c, hence at the common exponent c/2.

A finite signed measure with a positive Gaussian absolute moment is determined by all polynomial moments: for each Fourier parameter, the absolute exponential series is dominated by a constant times exp(b|z|^2). Termwise integration is valid, equal moments imply equal Fourier transforms, and ordinary Fourier uniqueness identifies the measures. No unproved determinacy claim about the hidden law or the initial law is used.

Identification would force sigma=w_t, but w_t(E complement)=-alpha_t(R^r)/C<0. This contradicts positivity. The argument works for every positive time individually, with its own c(t); no uniform lower bound as t tends to zero is required. Since L_t(1)=1, excluding positive probability representatives excludes every positive representing measure.

## 6. Separator and consequences

Polynomial density in L2(alpha_t+beta_t) follows from the same Gaussian argument: a polynomial-orthogonal L2 function gives a finite signed measure with a positive Gaussian absolute moment after halving the exponent. Fourier uniqueness then forces it to vanish. This argument uses the full moment family, not a finite approximation test.

A compactly supported continuous function in the strip 1<z_1<e is zero beta_t-almost everywhere and nonzero in L2(alpha_t). L2 polynomial approximation gives L1 convergence of squares. The density of w_t relative to alpha_t+beta_t is bounded, so the negative integral of its squared target persists for some polynomial q. Therefore q^2 F is a pointwise nonnegative polynomial with negative L_t value. This is an existential, time-dependent separator with no computed degree bound.

The true measure tilt of alpha tensor (P_k/C) remains a genuine probability path and is also strictly square-positive: P_k dominates Lambda_k on squares and the active density is positive on an open half-space. It is different from the escape path at every positive time by the latter's nonrepresentability. In the autonomous example, the unnormalized difference is exactly (beta_t-alpha_t) tensor N_k / C. Moment equivalence makes every derivative of this difference at zero vanish. The same holds for the mass normalizers, so normalization preserves the equal jets.

The main counterpath does not use the positive-time persistence theorem. The one-hidden-coordinate threshold comparison in the consequences invokes the already accepted one-hidden results; this review does not independently re-audit that separate theorem. Neither the earlier coordinate-positive counterpaths nor their determinate scalar initial variant are credited with full square positivity.

## 7. Fresh exact controls and mutations

The author's frozen check_controls.py was run in an isolated copy, with the source-root override pointing to the retained originals. It passed 7,888 assertions.

The separately written independent_controls.py uses tensor products of repeated one-dimensional forward-difference convolutions, rather than importing the author's difference implementation. It independently computes the inherited Lambda prefix using rational Gaussian elimination, rather than the inherited inverse-update routine. It passed 16,597 exact assertions, including:

- Multidimensional finite-difference identities in dimensions 1, 2, and 3 through total degree 6, at radii 1, 3, and 11.
- Exact absolute radial majorants, using the l1 norm as an upper bound on the Euclidean norm.
- The complete signed correction construction through degree 8, with every corrected moment checked, every lower-degree tail bound checked, and every block's mass and P-N identities checked.
- The actual witness value and positive-measure witness inequalities.
- The classical lattice square-completion identity and normalized hierarchy algebra.

Eight distinct mutation variants were rejected: omission of alpha!, a wrong power of the radius, reversed correction sign, omission of the large-radius requirement, stopping the correction series after degree 8, subtracting rather than adding N, omission of C, and the wrong normalizer-derivative sign. The stopped series has eight nonzero degree-9 residuals, giving a concrete diagnostic against promoting a finite prefix into the full theorem.

These controls supplement the reviewed ordinary proof; they do not establish the infinite signed series, arbitrary-time hierarchy, or nonrepresentability by sampling.

## Scope retained

No finding requires alteration of the frozen author packet. This is independent ordinary mathematical review and bounded exact replay. It establishes neither formal-kernel verification of the analytic construction, a determinate-initial counterexample, literature priority, final integration, nor project closure.
