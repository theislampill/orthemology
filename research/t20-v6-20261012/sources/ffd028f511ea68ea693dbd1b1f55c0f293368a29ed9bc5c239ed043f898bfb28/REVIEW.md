# Independent review: realizable moment dynamics

Date: 2026-10-10 UTC. Reviewer: review_realizable_moment_dynamics.

## Verdict and evidence boundary

PASS for the ordinary mathematical classification and its expressly stated stronger hypothesis, on the final byte bindings in REVIEW_RECEIPT.json. No formal-kernel certification, protected-source modification, integration, closure, empirical identification, or field-priority claim is made. The author and parent supplied a participating candidate proof. This reviewer independently derived its key bounds and identification argument before reading the authored RESULT.md, then read the authored proof end-to-end. Root appraisal was not treated as independent review evidence.

The inheritance review covered the measure-moment ancestor's sections 2, 5–6 and scope/ownership discussion, plus the determinate-moment-effectivity statement, corollaries, and limitations. The classification is stronger than the inspected ancestors' exhibited solutions: it exhausts the declared admissible moment-image solution class. This is only a bounded project-relative comparison.

## Independent mathematical checks

1. Normalization is legitimate. Coordinate continuity makes the integral of m1 finite on every compact subinterval. The exponential integrating factor is strictly positive with value one at zero. Because m0=1, the factor is consistently a0. Product differentiation gives a_r'=-a_(r+1), including at zero.
2. Regularity does bootstrap. Induct simultaneously over all coordinates: if every a_r is C^k, each derivative -a_(r+1) is C^k. Thus every coordinate is C^(k+1). At zero this is the continuous right-derivative version. No uniform norm or infinite-dimensional differentiability is tacitly assumed.
3. Backward Taylor signs and remainder are correct. Applied to v↦a_r(t-v), every derivative is a_(r+k)(t-v), hence all Taylor coefficients and the integral remainder are nonnegative. Every partial sum is bounded by a_r(t-b). In particular a_n(t)≤n!a0(t-b)/b^n. Passing b↑t uses endpoint continuity and a0(0)=1, giving a_n(t)≤n!/t^n.
4. Bounds suffice for local analyticity. On a small closed interval around s>0 with left endpoint at least s/2, the (N+1)-st derivative is bounded by (N+1)!(2/s)^(N+1). The Taylor remainder is at most (2|δ|/s)^(N+1). Restricting |δ|<s/2 and keeping the segment inside (0,T) proves a0 analytic locally. This works arbitrarily close to either endpoint without asserting uniform analyticity at zero. Higher a_r are derivatives of a0.
5. The exponential-tail bound uses an actual representing measure. At one s>0, λ_s=a0(s)ρ_s has moments a_r(s). Nonnegative series and backward partial-sum bounds give ∫exp(bx)dλ_s≤a0(s-b), for every 0<b<s; the analogous x^r bound also holds. Realizability has not been replaced by mere positivity.
6. Shifted Laplace analyticity holds for all positive arguments. For u>0, the exponential rate s-u is strictly less than s, so G_s(u)=∫exp((s-u)x)dλ_s is finite. On a small neighborhood, choose an additional positive margin below rate s. Absolute exponential-series domination and that margin justify both analyticity and each polynomial-weighted derivative. Negative rates use only finiteness of λ_s.
7. Identity propagation is not an infinite-time representation theorem. At s, G_s and a0 have identical full jets and are analytic. Local equality extends across the connected interval (0,T) by the ordinary real-analytic identity argument. The proof does not assume a completely monotone function on a finite interval is globally a Laplace transform.
8. Zero-time recovery preserves mass and every moment. As u↓0 the nonnegative integrands x^r exp((s-u)x) increase. Their integral limit is a_r(0) by coordinate continuity. In particular μ=exp(sx)λ_s has mass one and all finite required moments. This is the decisive step preventing loss of mass or an infinite initial measure.
9. Converses and uniqueness hold. For any initial law in the fibre, domination by the next moment proves A_r'=-A_(r+1), including the one-sided zero derivative; higher moments supply every higher derivative. Positive finite-time normalizers allow quotient differentiation. If two laws yield the same path, integrating -m1 determines the same normalizer. Equal Laplace transforms on a nonempty interval determine equal finite measures by analyticity, endpoint mass, and compactification/polynomial uniqueness.
10. Bijection and horizon claims are exact. The result covers every T in (0,∞], not T=0. Recovery from any finite nontrivial interval yields one initial law, whose damping extends to all later finite times. The extension stays in the specified class, and any other extension would recover that same law. No assertion concerns infinite-time endpoint regularity.
11. Positive-time separation and mean-interval separation are justified. Positive-time exponential tails make the full sequence determinate. A common sequence at a positive time gives a common tilted law; exponential untwisting and normalization recover the same initial law. Common mean functions on an open interval make their normalizers proportional there; analytic continuation and unit zero limits remove the proportionality. This does not assert means differ at every individual time.
12. The one-interior-time strengthening is supported. Nonnegative coordinates everywhere plus realizability at exactly one positive time suffice for every preceding step, and imply initial validity as a conclusion. No measurable family of representing measures is needed. The proof does not establish that initial validity alone can replace that positive-time premise under positivity.

## Countercontrols and scope

The flat perturbation is coordinatewise C∞ with exactly the valid determinate δ0 initial sequence, but its second unnormalized moment is negative for 0<t<1/2. Its quotient solves the hierarchy and differs from the constant δ0 solution. Therefore uniqueness is false for the unrestricted smooth sequence hierarchy even at determinate data. It does not refute the realizable classification.

The linear a0=(T-t)/T example has nonnegative coordinates but negative variance. Its initial sequence is already invalid. RESULT.md explicitly states this and does not use it as an independence proof under a valid-initial-data hypothesis. This qualification is essential and retained.

The effective corollary correctly uses the previous uniform named determinate-moment theorem. The new classification supplies uniqueness of all admissible solutions; it does not add a determinacy decision, nonsingleton selection, stability bound, signed-parameter domain, or practical algorithm.

## Executed evidence

The independent script check_independent.py passed 542 exact rational/sign checks: finite-law normalization, quotient hierarchy, semigroup composition, exponential untwisting, the flat-control sign, the invalid linear-control variance, and the zero-radius coefficient ratio in the determinate boundary example. These are separate finite controls, not a finite proof of the universal theorem.

The unchanged author script passed all 1,519 exact controls in a copied snapshot. Its first relocation attempt failed because it expects original ancestor files as sibling paths; copying the bound ancestor RESULT files into that expected layout resolved this packaging dependency without changing the script or any author bytes. The successful replay is recorded in author_replay.log. All copied ancestor contents are checked against the declared source bindings. This is a replay-layout detail, not a mathematical or executable-control failure.

Exact final hashes are recorded in REVIEW_RECEIPT.json. The verdict is confined to those bound bytes. Earlier protected sources were read only; this reviewer writes only this additive review directory.
