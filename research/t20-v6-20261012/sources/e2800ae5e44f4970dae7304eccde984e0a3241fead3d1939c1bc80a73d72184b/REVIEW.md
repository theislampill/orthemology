# Review of the fixed-entire-marginal endpoint action theorem

Date: 11 October 2026 UTC.

## Verdict and scope

**No blocking mathematical defect found in the frozen author result.** The stated compact product-torus theorem is supported: arbitrary compatible probability endpoints, including singular laws, admit finite action; the infimum is attained; its square root is a genuine finite metric with constant-speed minimizing geodesics; and nested dense continuous marginal-test minima converge to the whole-marginal minimum while retaining exact mass one.

This is a bounded ordinary mathematical review, not formal-kernel verification, exhaustive literature-priority review, authorization to integrate protected work, or a programme closure decision. The explicit sphere and mixture paths remain feasibility competitors; the review does not identify either one with the full transport-reaction minimizer.

Reviewed author folder: `fixed-marginal-endpoint-action-20261011/`.

- `RESULT.md`: `99f4d6e749b0f2856e1f23b7cd9d4e6cc53eed940ef5f6ec1a2ed0e325766304`
- `MANIFEST.json`: `d4b39b9888880b4a839a23e811bf8b15986c2f1961d8eece09fab19940f66387`
- `AUTHOR_FREEZE.json`: `73c74a071bf3b56e720806c4a28a3c5a3163a159cc8dac9c1d6d2dc7400da275`

The review was performed against those frozen files. No author file or inherited protected input was edited.

## Independence and participating inputs

The parent supplied the theorem proposal, a direct-method outline, a two-row control, and the cosine-squared mixture shortcut. The author supplied the detailed frozen proof. Therefore this is independent checking of supplied mathematics, not independent origination of the theorem or all proof ideas. The reviewer independently reconstructed the essential arguments, read the primary sources, inspected the frozen proof and verification code, replayed the controls, and wrote an additional 104-case finite-fibre control plus a finite-test leakage example.

The general closed-convex-set observation in the preliminary analytical notes is a parent-supplied participating observation. The frozen author theorem deliberately remains the fixed-marginal result; this review does not broaden its approved statement.

## Substantive checks

### 1. Measurable conditional construction and singular endpoints

The global reference measure λ=μ0+μ1 disintegrates as ν(dy)λy(dz), with λy having mass two. The author correctly retains that normalization. Global Borel RN functions fi give the conditional densities on one common ν-full set via a countable generating algebra and monotone-class argument. This resolves the joint-measurability issue that arbitrary fibrewise RN choices would leave open.

The affinity, angle, coefficient functions, and interpolated square root are jointly measurable. Their bounds justify dominated continuity and differentiation. The zero-angle limit gives a stationary fibre. For interior times both coefficients are positive; f0+f1=1 then gives positive square root λ-almost everywhere. A zero-density endpoint can have an unbounded actual reaction rate near it, but the endpoint slice is dt-null and the weighted square remains integrable. The factor α=2∂tu/u is correct for the actual-rate continuity equation. The resulting action is exactly 4∫θ²dν≤π², without a positive-volume-density or common-support assumption.

The simpler cosine-squared mixture proof is also valid. Weighted Cauchy-Schwarz yields its π² bound for arbitrary probability endpoints. It is an additional feasibility route, not an asserted minimizer.

### 2. Lower semicontinuity and control reconstruction

The dual formula in §3 is correct, including infinite-cost cases. Finiteness of the supremum gives a bounded functional on L²(η); Hilbert representation and equality against all continuous functions identify the vector measure with an L² density relative to η. Thus absolute continuity of the limiting momentum/source is proved, not assumed to survive weak-* convergence.

For each continuous dual field the expression is weak-* continuous, so the supremum is lower semicontinuous. The unit normalization in the formula, including the coefficient 2 in the dual pairing, is correct.

Minor expository note only: the sentence saying that the inequality “≤” follows by completing a square should be read as “the supremum is at most J.” The displayed equality and the subsequent density argument are correct. This is not a mathematical defect and does not require changing the frozen packet.

### 3. Compactness, time disintegration, continuity, and endpoints

There is no hidden temporal-disintegration gap. The proof begins with narrowly continuous probability curves, obtains a uniform one-half-Hölder bound against smooth tests, and applies Arzelà-Ascoli in a metric for the narrow topology. It therefore obtains the limiting continuous curve before taking the spacetime-control limit. Uniform narrow convergence identifies η=dt μt and preserves the endpoints and every-time marginal constraint.

Exact mass one gives ηn(Q)=1 and the combined vector-control total-variation bound √An. Weak-* convergence of those vector measures then passes the continuity equation. The lower-semicontinuity argument forces their limit to have the required L²(η) density; possible singular time-boundary flux/source cannot survive finite action. No regularity of ν is used. The compactness is narrow/weak-* compactness, not an assertion of compactness for the constrained metric topology.

### 4. Metric and geodesic claims

Smooth tests separate endpoint measures, so the test-function action bound proves definiteness. Time reversal proves symmetry. The compressed concatenation has energy a²/τ+b²/(1−τ), minimized at τ=a/(a+b); this proves the triangle inequality, with zero-distance cases handled by equality of endpoints.

The subarc replacement argument is valid because all intermediate measures remain in the same state space and attainment has already been proved for every pair in that space. Rescaling a restriction to unit time gives the factor (t−s), while compressing a replacement gives its reciprocal. Equality in the partition/Cauchy-Schwarz chain forces interval energy d²(t−s) and interval distance d(t−s). Thus every full action minimizer has the claimed constant-speed parametrization. The proof does not assume the reaction-only competitor is minimizing.

The comparison dS≤dν follows directly from inclusion of admissible classes using the same actual-rate action; no angular or static normalization is silently imported.

### 5. Finite tests versus an entire marginal

The finite-stage problems keep exact mass one, share a feasible full-marginal path, and have nested continuous state constraints. Each minimum is attained by the same compactness proof. Any fixed test eventually holds along the minimizing sequence and hence on a uniformly narrowly convergent subsequence. Uniform density of the test span identifies the limiting marginal at every time. Lower semicontinuity forces equality of the limiting minimum with the full-constraint minimum.

The qualifications in §7 are appropriate: only optimal-energy convergence and subsequential optimal limiting triples are claimed. No rate, finite stopping criterion, grid-consistency result, convergence to a unique selected minimizer, or strong convergence of velocity fields follows. Exact mass is part of this proof's stated hypothesis; the review does not claim it is logically necessary for every alternative compactness argument.

The reviewer's Fourier control gives a concrete boundary check. The probability density 1+ε sin(πt)cos(2π(N+1)y) keeps all Fourier moments through frequency N but changes the next moment by ε sin(πt)/2. It has finite reaction action and identical uniform endpoints. It is a feasible non-optimal path, not a counterexample to the minimizer convergence theorem.

## Primary-source and ownership checks

The directly inspected [2512.09250v1](https://arxiv.org/html/2512.09250v1), Definitions 1–2, §3 and Appendix C.1, uses half the present action at δ=1. Its attainment theorem has finitely many continuous affine constraints and a finite-feasibility premise. The author correctly provides a separate infinite-marginal argument.

The inspected [2402.15860v3](https://arxiv.org/html/2402.15860v3), Theorem 3.4, Lemma 3.8, Theorem 3.9, Remark 4.24 and Theorem 5.5, already contains finite-constraint attainment, constant-energy/metric structure, weighted-Sobolev projection, and a parallelizable-manifold extension. The author credits these antecedents. This supports the bounded scope distinction; it is not an exhaustive novelty search.

The inherited two-atom sphere example and the parent-supplied two-row example are identified as inherited/participating. In particular, the π²/3 example is an exact competitor action only; transport may lower the true optimum. The report does not conflate the endpoint theorem with the previous constrained KL-gradient result or with a nonlinear PDE/JKO theorem.

## Replay and independent controls

- All 15 files listed in the author manifest match both hashes and byte counts.
- The result and manifest match both author-freeze pins.
- Author verification was replayed in normal and optimized Python with original-input binding checks. Both runs pass and their output JSONs are identical.
- The 53 author checks comprise 37 algebraic controls and 16 input/freeze binding checks. They are not 53 mathematical theorems and do not mechanize the measure-theoretic proof.
- The reviewer-authored numerical controls cover 104 finite-fibre endpoint pairs and seven interior times per pair, including equal endpoints, disjoint support, zero entries, asymmetric overlap, and random sparse rows. Maximum mass/source/action/endpoint residuals are below 2.2×10⁻⁷⁰ with a 10⁻⁶⁰ tolerance. They independently verify normalization and boundary algebra, not infinite-dimensional existence.
- The additional Fourier example verifies that finitely many moments need not determine the full marginal.

Evidence is in `AUTHOR_INTEGRITY_REPLAY.json`, the two `author-replay-*/CHECKS.json` files, `independent_controls.py`, and `independent_controls_results.json`. The proof reconstruction and participating convex-set observation are retained separately in `PRE_REVIEW_ANALYTIC_CHECKS.md`.

## Handoff

The frozen author theorem is mathematically acceptable within its declared compact-domain, probability, actual-rate, and continuum-variational scope. No required correction or unresolved mathematical blocker was found. Any preservation, integration, or audit lifecycle decision remains with the parent and its governing process.
