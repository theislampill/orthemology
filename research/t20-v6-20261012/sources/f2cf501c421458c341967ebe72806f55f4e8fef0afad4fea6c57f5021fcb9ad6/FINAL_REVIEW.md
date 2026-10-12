# Digest-bound independent mathematical review

Date: 2026-10-09 UTC.

Verdict: **PASS within the explicit mathematical scope below. No unresolved material defect found in the reviewed final report.** This is ordinary mathematical review plus exact executable controls. It is not proof-assistant certification, field-priority certification, repository authorization, release readiness, or T20 closure.

## Immutable review target

Author report: `nonseparable-bayes-repair-20261009/RESULT.md`

SHA-256: `a9b3f91f320ee752ee732dc85af793f8a4736a98c01035fb5b197dfe2bf7eecb`

Author control source: `nonseparable-bayes-repair-20261009/verify.py`

SHA-256: `3609259ad8ca9a594ba2efb7f045db19e4d5e9bea52c96c8790c0639b987de93`

Author execution log and independent rerun log both have SHA-256:

`6f7f23dc0f9184fe57f97dd540502f8b399ff5085534fd9b865790da56daf341`

The author report and source are copied into this review directory as `REVIEWED_AUTHOR_RESULT.md` and `REVIEWED_AUTHOR_VERIFY.py`. Those snapshots match the reviewed digests. Changing the report or source invalidates this review's automatic applicability to the changed item.

## Independence and method

Before reading the author's draft, I derived the C1 classification, strict-convexity equivalence, divergence and Hessian formulas, global-forward flow proof, finite-boundary restrictions, and a separate open-box proof. I wrote the initial independent analysis and exact symbolic controls. I subsequently coordinated specific scope findings, including a box-compatible restricted-null-likelihood counterexample and the coordinate-free corollary. The resulting `INDEPENDENT_ANALYSIS.md` marks these later additions. This is an independent derivation with disclosed later coordination, not an assertion of wholly blind review.

I then read the full frozen author report and control source, checked every substantive theorem and example claim, independently executed the unchanged author control source, and compared its output byte-for-byte with the author's complete log. I reran my separate controls after the final wording changes.

Results:

- Author controls: all 55 exact controls passed, SymPy 1.14.0; independent rerun exited successfully and exactly matches the author's log.
- Separate reviewer controls: all 28 exact controls passed, SymPy 1.14.0. These include independent quadratic formulas, truth-state derivatives, strict-convexity/Hessian-degeneracy controls, a different box-compatible bump witness, and a trace-positive symmetric-matrix example.
- These finite-dimensional and symbolic examples supplement the written proofs. They do not computationally certify the general theorems.

## Claims accepted

1. **C1 classification on the positive cone.** The equivalence between all-input first-argument normalization projection, tangent-gradient constancy along rays, and F(sp)=s f(p)+a(s) is proved correctly. The definition makes existence an asserted property, rather than assuming arbitrary open-simplex projections exist. The canonical choice f=F restricted to the simplex fixes a uniquely.
2. **Convexity qualifications.** Both convexity and strict convexity are equivalent to the corresponding properties of f and a. Strict convexity is correctly separated from pointwise Hessian positivity.
3. **Divergence and Hessian formulas.** The split D_F(sp,tq)=s D_f(p,q)+D_a(s,t), full Hessian quadratic form, radial identity H_F(sp)p=a''(s)1, and block-diagonal mass/simplex metric all follow with the stated regularity.
4. **Boundary treatment.** A finite continuous extension supports boundary first arguments and the unique normalized minimum over the closed simplex. The proof correctly obtains a strict supporting inequality from an interior point to any distinct boundary point without assuming strict convexity along boundary faces. Boundary second arguments remain separately restricted.
5. **Dynamics.** Under positive tangent Hessian and a''>0, the canonical inverse-Hessian field is radial, has a unique global forward solution already at C2, and converges to normalization. The exponential bounds have the correct directions. The score derivative and its integrated mass-repair accounting are correct. The derivative identity itself is correctly labeled generic/inherited.
6. **Nonentropy example.** The quadratic perspective is genuinely nonseparable and has coherent Brier geometry while implementing normalization. The comparison with the ambient Euclidean generator and the stronger same-coherent-value affine gauge are correct. The rational null and informative channel calculations check exactly.
7. **Quantifier and orientation controls.** All-input scalar neutrality is correctly distinguished from coherent-prior attenuation tests. The author's positive-part affine quartic bump is C3, convex, preserves Hessian positivity, passes the restricted tests and reverse normalization, and fails forward normalization at the stated interior-box witness. Its stated actual forward minimizer is correct. Bounded finite-channel inputs probe only mass at most one, as qualified in the final report.
8. **Separate box theorem.** The proof explicitly uses connected fixed-mass sections containing a uniform anchor. The convexity, Hessian, and forward-flow conclusions are valid on the box at admissible points; no unproved cone extension is used.
9. **Coordinate-free transport.** The nonempty open convex cone with a strictly positive linear functional gives a connected base and the same classification. Treating the Hessian as V->V* makes the covector-driven field intrinsic. Positive-definite symmetric/Hermitian matrices with trace normalization are valid conditional examples; no categorical Bayes action or ungrounded substantive positivity claim is imported.

## Review-driven precision changes verified

The initial reviewed report hash was `823bbffdbae1be3764094caf084c41001f7fad5b47d5d886aebf949239b2ff71`. Before acceptance I requested two clarifications:

- The strict-propriety identity now explicitly uses r,p in the simplex interior and assumes finite vertex first arguments, avoiding an undefined boundary second argument.
- The final separable second-derivative argument now explicitly invokes the older C2 separable hypotheses rather than appearing to differentiate arbitrary C1 functions twice.

The author also made the general cone explicitly nonempty and recorded the valid bounded finite-channel extension of the attenuation counterexample. I inspected these revised passages and verified the final digest given above. The control source did not change during this final revision.

## Limits that must remain attached

- The classifier assumes normalization for every input in the declared domain (or an equivalent all-input condition). Restricted coherent-prior probability-likelihood tests do not imply behavior above mass one.
- Positive-definite Hessian assumptions are required for the stated inverse-Hessian dynamics. Strict convexity alone does not suffice; the quartic radial negative control is decisive.
- The flow is global **forward**. Backward completeness is not generally true and is not asserted by the reviewed report.
- Finite continuous boundary first arguments do not supply gradients or losses with boundary second arguments. Zero-likelihood reports require additional definitions or assumptions.
- Coordinate-free normalization does not identify arbitrary noetic tensors with a positive cone or supply empirical, psychological, theological, or metaphysical warrant.
- The perspective divergence identity has published ancestry, as the author's Section 12 and the root's targeted primary-source note record. I make no exhaustive literature or novelty claim.
- No protected source, repository implementation, formal state, release, or T20 closure was modified or authorized by this review.
