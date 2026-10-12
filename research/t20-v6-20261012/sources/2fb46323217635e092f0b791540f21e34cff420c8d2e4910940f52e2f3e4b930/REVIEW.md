# Independent review: determinate initial data and the positivity boundary

10 October 2026 UTC. Reviewer: `private-locator:8d3789be9075d330f594`.

**Disposition: PASS for the frozen RESULT and DIAGNOSTIC identified below, after one citation-only correction. No mathematical correction is required.**

This is an independent ordinary mathematical and source review, with independently written exact finite controls. Participating root notes were not used as review evidence. The author retains ownership of the construction and identifies the participating origin of the explicit atom computation and diagnostic. This review makes no formal-kernel, field-priority, canonical-integration, algorithmic-complexity, or numerical-measure-reconstruction claim.

## 1. Exact accepted inputs

- `determinate-initial-positivity-20261010/RESULT.md`
  - SHA-256: `cafc520026c66f94442346ff308ed4e202d70e10be8963b8a24ad17bda4e1e0a`
- `determinate-initial-positivity-20261010/DIAGNOSTIC.md`
  - SHA-256: `5d0e97c5f4e50ac7981765292b6aa161076a4d0b6af7fbc46aa18e40bd89c2b2`

Byte-identical copies are in `author_snapshot/`; `INPUT_BINDINGS.json` records sizes, hashes, and the predecessor classification binding. The initially reviewed RESULT hash was `83c6dda6b1709c707f0854a4b6c7ee20facb7af3409b2ebf8cb29b3a453554ed`. The author changed only the sentence describing the Jablonski–Jung–Stochel support statement: its cited pages say no finite accumulation, rather than describing entire-function zero sets. The mathematical arguments and DIAGNOSTIC were unchanged. The corrected sentence was verified in the accepted bytes.

The classification `realizable-moment-dynamics-20261010/RESULT.md` remains at SHA-256 `c5aeeeed56b5bf5edfa9b87570249f142e3d1be9c06218d8007013c66f5eb688`. Its admissible class requires positive-time realizability; the new counterexample does not belong to that class.

## 2. Determinate counterexample

### Initial law and exact hypotheses

The lognormal moment formula follows by completing the square in its Gaussian logarithm. The discrete probability proportional to `sum exp(-k^2/2) delta_(exp k)` has the same entire integer moment sequence: `rk-k^2/2 = r^2/2-(k-r)^2/2`, and integer translation preserves the absolutely convergent sum. Its atomic nature distinguishes it from the continuous lognormal law. This establishes Stieltjes indeterminacy before extremal theory is used.

The source checks in `SOURCE_CHECKS.md` verify that the Krein representative for this Stieltjes-indeterminate sequence is N-extremal, supported on the half-line, has no finite support accumulation, and has zero in its support. Thus its zero atom has positive mass. Its first moment excludes unit mass there. Berg–Christensen Theorem 7 applies to this indeterminate N-extremal probability and removes the **entire** atom. The result is Hamburger determinate. Multiplication by the positive constant `1/(1-w)` preserves that property. Removing one point leaves infinite support. Hence the stated initial sequence has a positive, Hamburger-determinate representative; it is not merely a formal modification of the lognormal moments.

Neither an arbitrary lattice representative nor partial deletion would establish this conclusion. The result explicitly avoids those substitutions. The relevant primary page links and the distinction between full and partial deletion are recorded in the source report.

### Smoothness and all-grade positivity

For every fixed nonnegative integer grade, differentiation of `B_r(t)` is justified at positive times and at the right boundary by a higher finite lognormal moment. Iteration gives coordinatewise smoothness up to zero. The removed zero atom contributes a constant only to `a_0`, so `a_r'=-a_(r+1)` holds also for grade zero. No sequence-space norm or uniform-in-grade differentiability is assumed.

The bound `exp(-tx) >= 1-tx` supplies `B_0(t)-w > (1-w)/2` on the stated open interval. For every higher grade, the integrand is strictly positive almost everywhere. This proves strict positivity simultaneously for all coordinates and all times in the safe interval. The quotient by `a_0` is legitimate throughout it and gives the normalized hierarchy. The initial coordinates are exactly those of the atom-deleted law.

Scaling the trait by any positive lambda with `lambda H<T_0` preserves full moment determinacy by the invertible pushforward. It produces the counterexample on every prescribed finite horizon. There is no single globally coordinate-positive counterexample claimed. In the unscaled construction, dominated convergence, strict monotonicity and continuity give the unique finite crossing `B_0(t_*)=w`.

### Pointwise nonrealizability and scalar-path distinction

For each safe `s>0`, a hypothetical half-line probability representing all normalized coordinates would make `(B_0(s)-w)sigma_s+w delta_0` a positive measure with exactly the moments, including total mass, of the damped lognormal measure. The latter has a positive exponential moment of rate `s/2`. For positive half-line competitors the nonnegative exponential series transfers this bound by monotone convergence; the common locally convergent Laplace series and Laplace uniqueness identify the measures. Their zero-atom masses then contradict one another. This is an individual contradiction at **every** positive safe time, not a finite-grade or almost-everywhere test.

The signed scalar Laplace path therefore cannot be the transform of a positive initial law, even on an open subinterval: equality of such scalar paths would, by positive-time differentiation, represent the normalized moments there. Hamburger determinacy of the initial positive representative excludes other positive initial laws, but does not identify a signed measure from its moments. Consequently there is no conflict between the determinate initial sequence and the different signed scalar path with the same full boundary jet. The genuine tilt of the unique initial law gives the other strictly positive solution. The nonuniqueness assertion concerns the unrestricted coordinate-positive hierarchy, not the realizable class of the earlier classification.

## 3. Stieltjes-Carleman sufficient condition

The positive proof was checked independently, including its boundary and growth steps.

1. The derivative chain bootstraps coordinatewise regularity as in the classification. Backward Taylor remainders have nonnegative terms; letting the backward endpoint tend to zero gives `a_n(s)<=n!/s^n`. The same bounds uniformly on a compact interior neighborhood prove real analyticity by Taylor remainders.
2. For fixed `s>0`, the nonnegative coefficients `p_j=a_j(s)s^j/j!` have radius at least one. Local Taylor equality and the identity principle give their power series as `a_0(s(1-z))` on `0<=z<1`. Monotone convergence and boundary continuity make the coefficient sum one. Differentiating inside the disk, then letting `z` increase to one, gives every factorial moment `E[(N)_r]=s^r c_r`; all summands used in this limit are nonnegative.
3. A Poisson variable mixed by `sX` has the same factorial moments, and the finite Stirling identity gives the same raw moments `d_n`. No moment-generating function for X is being assumed.
4. To verify the partition bound, choose a distinguished member of each of k blocks. There are at most `binom(n,k)` choices of representatives and at most `n^(n-k)` assignments of the other elements. Every partition is counted. The probability moment inequality `c_k<=c_n^(k/n)` therefore gives `d_n<=[s c_n^(1/n)+n]^n`, including the harmless k=0 envelope term.
5. Probability Lp norm monotonicity makes `b_n=c_n^(-1/(2n))` nonincreasing. Its minimum with `sqrt(s)/sqrt(n)` is also nonincreasing, so Cauchy condensation is applicable to both series. The condensed lower-bound terms are the minimum of a divergent-sum sequence and the growing cap `2^(k/2)`. If capping occurs infinitely often, the capped terms themselves prevent convergence; otherwise the original divergent tail remains. This validates the transfer of the **Stieltjes** Carleman condition to `d_n`.
6. Stieltjes Carleman determinacy identifies the two half-line count laws. Their PGFs then identify `a_0(t)` with `E exp(-tX)` for `0<t<=s`. Both sides are analytic for positive time, giving equality over the entire connected time interval, with boundary equality by continuity and the other coordinates by differentiation. The case `c_1=0` has initial law `delta_0`; monotonicity forces `a_1=0` and the same conclusion.

Schmudgen's primary Theorem 1 at [arXiv:2011.04025v1, p.2](https://arxiv.org/pdf/2011.04025v1#page=2), in dimension one, explicitly supplies the invoked Stieltjes-Carleman criterion. The count law satisfies its positivity hypotheses because it is an actual probability on the nonnegative integers. Kuba–Panholzer is correctly treated as attribution for the related Hamburger transfer, not as a theorem allowing arbitrary determinate mixing laws. Its printed zero-intensity endpoint caveat is immaterial here because s is strictly positive.

The distinction from derivative-class or exponential-tail hypotheses is genuine. The sequence `(2n)!` is represented by the square of a mean-one exponential random variable. Stirling's formula makes its Stieltjes-Carleman terms asymptotic to `e/(2n)`, whereas the stronger derivative-class terms are asymptotic to `e^2/(4n^2)`. The counterexample's own Carleman terms decay like `exp(-n/4)` up to a factor tending to one, so its divergent-series hypothesis fails despite determinacy. No inconsistency remains between the positive and negative results.

## 4. Explicit atom mass and computability

For each N, the positive definite Gram matrix yields the constrained minimum by completing the square in the nonconstant coefficients. It equals the stated principal determinant ratio, or equivalently the reciprocal of the reproducing-kernel diagonal. Because the Krein measure is N-extremal, its orthonormal polynomials are complete in L2. Evaluation at its atom has representing vector `1_{0}/w`, with squared norm `1/w`; Parseval proves that the finite reciprocal kernel sums decrease to w. Thus the Gram minima really identify this atom, rather than only an upper bound on it.

The row and column factors in the two determinants cancel exactly. The denominator's powers begin at one, adding the factor `product x_i`; the remaining Vandermonde quotient is `product (x_i-1)`. Their ratio is therefore `product_(i=1)^N(1-q^i)`, with the empty product one. This checks the half-exponents and the determinant indexing.

For finite tails, `1-product(1-u_j)<=sum u_j`; taking a monotone limit and using `w_N<=1` gives `0<=w_N-w<=q^(N+1)/(1-q)`. The explicit geometric tail and computability of q give a computable real w. Also `1-w>=q>0`, so division in every `c_r` is effectively safe. The full sequence is uniformly computable in grade and requested precision.

Computability of the unique positive initial law and its genuine tilt uses the previously established, separately bound determinate-moment recovery result and its promised-domain representation. This packet does not itself reconstruct the extremal support or give a new universal reconstruction algorithm. Computable initial data do not repair the spurious signed path.

## 5. Finite-Hankel diagnostic

The shifted Hankel quadratic form integrates `x p(x)^2` against a strictly positive density on `(0,infinity)`, so it is strictly positive for each nonzero polynomial at every safe time. At time zero, the atom-deleted positive law still has infinite support, giving strict positivity of every fixed unshifted Hankel matrix as well. Coordinate continuity preserves each particular matrix's positive definiteness on some sufficiently short interval.

Conversely, at every positive safe time, semidefiniteness of both entire Hankel families would imply a Stieltjes representative, contrary to the pointwise atom argument. Thus some finite unshifted degree fails at each such time. Taking one fixed N at a time and using its lower-degree principal submatrices proves `d(t)>N` for all sufficiently small positive t. This is precisely `d(t)->infinity`; it supplies no rate or numerical detection algorithm.

The exact finite threshold follows from congruence of `G-w e_0e_0^T` to `I-w uu^T`, where `u=G^(-1/2)e_0`. Positive semidefiniteness is equivalent to `w e_0^T G^(-1)e_0<=1`. At zero the threshold is the finite product already checked above, strictly greater than its positive infinite-product limit. The degree-zero convention is correct. No issue is hidden by normalization because D(t) is positive.

## 6. Independently executed exact controls and preservation

`check_controls.py` was written independently for this review and executed with Python 3.12.14 and SymPy 1.14.0. It passed **594 exact assertions**, exited zero, and produced empty stderr. `CONTROL_RECEIPT.json` records actual start/end times, interpreter path and file hashes. Its stdout is `check_controls.log`.

The controls cover the lattice exponent identity, normalized hierarchy and atom recombination identities, rational Gram/Vandermonde ratios and constrained minima through degree seven, symbolic determinant ratios through degree three, exact rank-one PSD/negative examples, Stirling and partition formulas through degree sixteen, Poisson PGF identities and finite product tails. They do not approximate the lognormal integrals or claim to prove the universal statements by sampling. Source theorems, infinite-degree positivity and nonrealizability, series divergence, analyticity and computable-law recovery remain ordinary-proof obligations, addressed above and by the cited sources.

Replay from the workspace root:

`python determinate-initial-positivity-review-20261010/check_controls.py`

The result must match the stored stdout byte-for-byte. The author has no separate executable controls in its frozen two-file packet; these independently authored controls are the reproducible controls preserved with the review.

Only this separate review directory was written by this reviewer. Before review writes, 332 earlier files were hash-pinned, including 71 existing archives. `FINAL_VERIFICATION.json` records their unchanged status, final author/snapshot equality, and the accepted control/source artifacts. No predecessor result, earlier review, archive, protected source, baseline build or participating root note was changed. Final receipt hashes are in `REVIEW_RECEIPT.json`.

## 7. Final scope

Accepted: a Hamburger-determinate and uniformly computable initial sequence does not force a coordinate-positive finite-horizon hierarchy to remain realizable; Stieltjes-Carleman growth does force the genuine tilt; the explicit Krein atom product is correct; and fixed finite Hankel tests can remain positive initially while the full moment-image condition fails immediately.

Not claimed: a globally coordinate-positive counterexample on the full nonnegative half-line, a finite detection rate, a general moment decision algorithm, a replacement for positive-time realizability in the earlier classification, or formal certification. The independent review is complete for these two frozen deliverables.
