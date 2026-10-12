# Independent review: completion and Bayesian conditioning

10 October 2026 UTC. **PASS within the stated finite mathematical scope.** No blocking proof error or counterexample was found. This review preserves the author packet byte-for-byte and does not authorize protected edits, integration, programme/T20 closure, empirical interpretation, or a literature-priority claim.

## 1. Precisely reviewed bytes and evidence

The author confirmed the freeze before pinning and replay. Reviewed packet: `completion-bayes-commutation-20261010`.

- `RESULT.md`: SHA-256 `3ae148739d915bcc9dc8d59c934b3a33ff46c79ef34407e4b47c1432ecef86a2`
- `MANIFEST.json`: SHA-256 `6ac3dfba213dfa10b606c8b6e16287568222cc8433923a638dc243226c337d53`
- All 14 author-manifest members passed length and digest checks.
- All 6 directly bound original files matched the preserved snapshots at review time.
- The author's 24 exact assertion groups were replayed off-packet. Regenerated control JSON and stdout were byte-identical; stderr was empty.
- A separately written verifier, importing no author code, passed 15 independent exact assertion groups. It includes a symbolic sweep of 242 likelihood arrays and a 26-array zero-dimensional sweep.

The review independently checked the ordinary arguments in the frozen result and the cited portions of its direct input snapshots: the normalized-posterior dichotomy, finite facial closure and entropy completion/continuity, zero-likelihood model criterion, and feasibility-face criterion. It does not claim transitive executable replay or independent-review credit for whole inherited packets.

## 2. Main classification: proof audit

The theorem is correct under its stated assumptions: a nonempty finite atom set, mass retained in the observable space, a fixed strictly positive reference, a minimal affine statistic representation, and a nonzero nonnegative likelihood. The equality being tested is equality of laws, rather than just equality of posterior moments.

### Composition criterion

Commutation on all strictly positive inputs implies both required ingredients. Model inputs are fixed by completion, so their conditioned laws must remain in the closed model. Equal-record positive inputs have the same completion, so their conditioned retained records agree. Conversely, descent of the conditioned record and model membership identify the two composed laws by uniqueness of the completion. No implicit linearity or continuity of a posterior decoder is used.

### Inherited normalized-posterior dichotomy

The cited proof is valid for positive inputs alone. For a kernel direction h, perturbing a strictly positive law within its moment fibre gives

    M D_L h = (L^T h) M B_L(p).

If any kernel direction has nonzero likelihood mass, the posterior record is constant throughout the positive simplex. Taking positive inputs to a point mass at each supported atom forces all supported columns to agree. Otherwise all kernel directions are killed by M D_L, yielding the multiplier/stabilizer alternative. The constant mass coordinate makes the rank-one and identical-column formulations equivalent.

### Facial support and logarithmic restriction

For a full-support exponential-family input, the conditioned support is exactly supp L, and its log-density relative to the fixed reference differs from log L by a retained affine function. Thus the inherited saturated-face and restricted-log criterion is applied in precisely its valid domain.

When all supported columns coincide, a saturated face carrying only that column is necessarily a single vertex. Saturation requires every duplicate atom there, and the restricted-log condition requires identical positive likelihood values across that entire fibre. A partially included duplicate fibre, unequal duplicate weights, and a full fibre at a nonvertex are correctly excluded.

### Stabilizer sufficiency, including zeros

The stabilizer is a unital finite-dimensional pointwise algebra contained in the retained space. Polynomial interpolation on the finite set of likelihood values produces both its support indicator and the restricted logarithm. The support indicator exposes the required saturated face; the interpolated logarithm supplies the model condition. There is no logarithm of zero or unjustified extension off the support. When L is positive everywhere, the exposed face is simply the whole polytope.

These steps prove the claimed algebra-or-entire-vertex-fibre classification, independently of the positive reference.

## 3. Boundary inputs and the stronger feasibility contract

Every law with a given mean is supported on that mean's minimal face. Its completion is positive on every supplied column on that face. Hence supp p is contained in supp R_r(p). This includes duplicate and nonvertex supplied columns.

For a boundary input with positive actual branch mass, both Bayesian denominators at the limiting input are strictly positive. Continuity of the entropy selector and of normalization on that open denominator domain therefore justifies the positive-input limiting argument. The proof does not take a zero-denominator posterior limit or insert an arbitrary impossible-branch law.

For equality of the partial operations on the entire simplex, the domains must agree as well. In the algebra case, L is retained, so completion preserves its exact expectation. Feasibility and branch mass then agree.

For the remaining vertex case, all-input feasibility becomes constant on moment fibres. The inherited feasibility theorem supplies a nonnegative retained witness with exactly the vertex-fibre support. A retained function is constant on that fibre, so the witness is a positive scalar multiple of its indicator. Multiplying any retained function by that indicator yields a scalar multiple of the same retained indicator; hence it lies in the stabilizer. This correctly eliminates all genuinely extra vertex cases. Exact branch-mass preservation is a consequence of the resulting classification, not a premise silently included in the Boolean contract.

The geometric complement argument is also sound. If the nonempty complement is a saturated exposed face F and all other supplied columns are at v, its exposing hyperplane contains aff F and excludes v. Thus v is outside aff F, P is the pyramid conv(F union {v}), and dim P = dim F + 1. The affine apex indicator exists whether or not F is a simplex and whether or not columns repeat. The empty-complement case is handled separately by the constant indicator.

## 4. Interpretation guard: existential compatibility

An elementary consequence worth making explicit is

    supp R_r(p) = union {supp q : q is a probability law and Mq = Mp}.

Every member of the fibre has support within the minimal-face support; the completion itself is a member of that fibre and has the full support. Consequently, for any nonnegative likelihood, including the zero likelihood,

    alpha_L(R_r(p)) > 0
      iff some law q with Mq = Mp has alpha_L(q) > 0.

Thus an extra branch absent from the particular input law is still compatible with the retained record. Completion does not make an event possible that the record rules out for every representing law. Existential compatibility does not establish actual-input positive probability, universal feasibility throughout the fibre, or preservation of the branch probability. The diagonal countercontrol explicitly has both a feasible and an infeasible input in the same fibre. This corollary is an elementary interpretation of the inherited support result, with no novelty claim or change to author bytes.

## 5. Independent exact controls

### Non-simplex, nonuniform, nonproduct reference, with duplicates

The independently chosen columns are (0,0),(0,0),(0,1),(1,0),(1,1), with reference weights (1,4,3,3,5). The aggregate square reference (5,3,3,5) has odds ratio 25/9, so neither uniformity nor product-reference completion is being assumed.

Unnormalized full-support model members are

    q_num = (1,4,3V,3U,5UV),   U,V > 0.

The two independent kernel directions are (1,-1,0,0,0) and (1,0,-1,-1,1). Adding arbitrary small multiples gives every positive input in each model member's moment fibre. Posterior-record equality is tested by exact polynomial numerator identities in both tilt parameters and both kernel parameters. Model membership is checked independently by explicit square supports, the duplicate ratio, and the square odds identity.

All 242 nonzero arrays in {0,1,2}^5 matched the theorem: 10 commute, comprising 2 positive constants and 8 full-vertex-fibre weights. The other 232 fail. This is a symbolic all-positive-prior calculation for these 242 likelihoods, not a sampled-prior fit.

Additional exact controls show:

- With L the duplicated (0,0)-vertex event, the opposite diagonal has actual branch mass zero, while its completion has mass 5/16. Another law in the same fibre has mass 1/2.
- The possible boundary vertex posterior completes to the reference split (1/5,4/5), even when the original posterior used only one duplicate atom.
- A positive same-record perturbation changes vertex-event mass from 20/64 to 21/64 without changing the commuting vertex posterior.
- Likelihood weights (1,2) on the duplicated vertex produce conditioned reference proportions (1/9,8/9), which disagree with the completion's (1/5,4/5). Partial support also fails.
- A local edge likelihood preserves exact branch mass and the closed model but changes the retained conditioned mean of a general input, so commutation fails.

### Other domains

- Columns -1,0,0,1 and reference (2,3,5,2) show that a full duplicate fibre at a nonvertex is still not an exception: its conditioned law and its completion have the same mean but different supports.
- With d=0 and reference (1,3,5), all 26 nonzero ternary likelihoods were checked directly; only the 2 positive constants commute. The entire atom set is the sole vertex fibre, so the two theorem alternatives coincide.
- The zero likelihood produces no normalized branch and remains outside the stated nonzero theorem.
- A nonsimplex square pyramid with a duplicated apex verifies the complementary-face case beyond a simplex: the apex indicator is retained and stabilizing. Independent symbolic identities establish posterior-record descent and exact branch mass for likelihoods constant on the base and on the apex, including zero-block limits.
- All 961 pairs of nonempty atom supports and nonempty event supports on the duplicated square preserve every actually possible branch under the explicitly computed minimal-face support.

## 6. Qualifications and disposition

No author correction is required. The final interaction-space specialization is read in the inherited declared range that includes unary observables (1 <= k < m); it is not a claim that d=0 has additional point-revealing exceptions. The theorem itself treats d=0 correctly.

The general theorem rests on the ordinary finite proofs audited above. The controls are finite examples and symbolic calculations in declared models, not a formal-kernel proof, a statistical robustness guarantee, a fitting algorithm, a psychological claim, or evidence that an actual implementation made a substitution. This review adds no field-wide novelty or programme-closure status.

The accompanying replay preserves both packets and regenerates all author controls and independent controls outside them. At the end of the independent run, all pinned author bytes and bound snapshots were checked again and remained unchanged.
