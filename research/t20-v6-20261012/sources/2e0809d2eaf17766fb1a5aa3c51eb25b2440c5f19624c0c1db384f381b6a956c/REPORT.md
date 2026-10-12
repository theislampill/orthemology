# Geometry boundary delta audit

## Scope and decision

This independent review concerns freeze-boundary-v2, manifest SHA256 8e1f85d527f74b8176975d814ab67a4091499988bfeed30b87eb398f37494c8a. The earlier polynomial AND audit seal is unchanged. PASS_SCOPED. Four kernel modules passed fresh replay, all four source mutations were rejected, and the exact critical/mixed-rank checks passed. Final records are in RESULT.json.

The review establishes two useful additions: a kernel-bound zero-optimum LP with actual finite-epsilon nonlinear failure, and an ordinary coupled-hull rescue with rank-one/rank-three blocks and no free singleton coordinates. The source distinguishes these evidence levels correctly.

## Critical score data and exact failure

CriticalZero defines the actual scalar Bregman divergence for a globally positive-curvature quartic potential. Its first and second derivatives are proved; the curvature is 12(t-1/3)^2+2/3, so the full endpoint neighborhood is regular. Exact gain identities apply to every real correction b, not merely to a numerical optimizer.

The independent kernel theorem `actual_four_rows` binds all four LP rows to the actual score gains for the baseline (1/2+epsilon,1/2) and coherent candidate q=1/2+epsilon/2+epsilon^2*b. The rows, in G0,G1,F0,F1 order, are (1/4-b,1/4+b,3/4-b,b-1/4). At b=1/4 they are (0,1/2,1/2,0). The half-and-half dual weights on rows G0 and F1 give objective zero and cancel the correction coefficient exactly. Independent `critical_generic_dual_bound` checks this certificate through the generic finite-LP library.

Thus the zero optimum belongs to the actual Taylor data. It is not an unconnected finite array. The no-exact-repair theorem simultaneously excludes every q in [0,1] satisfying even the necessary G truth-zero and F truth-one comparisons, for every real 0<epsilon<=1/100. Therefore full all-state weak repair is impossible, including endpoint candidates. The independent combined theorem records zero optimum and nonlinear failure together.

The obstruction proof is stronger than a formal Taylor sign heuristic: it uses exact polynomial identities at a rational envelope, a proved positive remainder on the whole epsilon interval, and monotonicity of the actual nonlinear endpoint loss. Independent symbolic identities and 64 exact rational envelope checks supplement the kernel result.

## Generic finite LP certificates

The generic library proves weak duality under nonnegative weights, unit mass and a balance identity for every correction vector. A negative dual objective excludes nonnegative primal margins; a nonpositive objective excludes strictly positive primal margins. It does not prove finite-LP strong duality, attainment, the optimized-regret asymptotic, or the analytic localization of actual repair points. Those remain the separately reviewed ordinary variational theorem.

Exact controls demonstrate why the three dual premises matter: deleting nonnegativity, unit mass or balance individually can make the claimed upper bound false. A fourth control checks that changing the critical final-row sign falsely permits a positive margin. Kernel source mutations change that row, the epsilon range, the cubic generator coefficient, and the generic bound by an unjustified +1; all were rejected in the final replay.

## A regular positive comparator

The original odds-curvature positive comparator is endpoint-singular and does not alone meet the full-neighborhood hypotheses of the general variational theorem. Independent review supplied the entire analytic potential exp(4(t-1/2))/16. At 1/2 its curvature and curvature derivative are 1 and 4, giving exactly the same four LP rows and zero optimum as the polynomial failure example. Its logarithmic curvature slope is 4 everywhere, which satisfies the global isolated rank-one criterion because 4s(1-s)<=1. It therefore has exact common weak repairs throughout the attained box.

The frozen v2 ordinary notes incorporate this correction. ZERO_SUCCESS_COMPARATOR.md gives the full argument. This is an ordinary application of the reviewed rank-one theorem, not a new kernel exponential-repair result.

## Mixed rank result

MIXED_RANK_REVIEW.md verifies the six literal Boolean vertices, rank-four affine hull, rank-one/rank-three tangent blocks, all-context coefficient inequalities, all transverse directions and actual convex-hull admissibility. The high-block-only normal case is covered by exact constant quadratic gains, not by assuming the duplicate-block disturbance is nonzero.

The initial product argument required correction: an interior high-block baseline is not itself a Boolean truth. The frozen v2 argument now uses barycentric averaging, which is sound. An explicit barycentric right inverse independently verifies local coupled-hull feasibility. Exact tests check 12 leading-gain identities, 12 pure-high-normal identities, a product averaging identity, and 492 positive rational cases, including 164 high-block-only normal cases. Three deletion controls detect omitted high normal projection, misuse of the old free-coordinate correction, and substituting an interior point for a listed truth.

The mixed-rank result remains ordinary mathematics in this seal. Any later mixed-rank kernel successor needs its own immutable review.

## Changed frontier

1. Hessian compatibility and dependency-block data remain first-order information. They do not classify exact nonlinear repair on arbitrary coupled hulls, even when the remaining block has rank three and no singleton freedom
2. The actual joint truth polytope matters. The coupled hull and the product of its projections share the same affine/block/Hessian data and score generators but have opposite exact-repair answers
3. After first-order compatibility, positive second-order margin gives local strict repair and negative margin excludes local weak repair under the ordinary variational hypotheses. Generic finite certificates now have kernel-checked algebraic support
4. Zero second-order margin is a genuine boundary: both exact success and exact failure occur within globally smooth positive-curvature potentials with the same critical LP data. Higher-order or exact information is necessary there

The general second-order asymptotic remains ordinary. This return does not claim a complete arbitrary-hull classification, historical novelty, canonical adoption, empirical authority of supplied scores or truth models, or completion of the research tranche.

## Execution notes

All frozen files are copied and hash-verified before replay. Passing local modules use only Mathlib as an external import root, and only the usual propext, Classical.choice and Quot.sound axioms. Replay uses the pinned Lean 4.19.0 and clean Mathlib c44e0c8ee63ca166450922a373c7409c5d26b00b source tree, with no author oleans on the search path.

An initial independent rational-test helper accidentally converted constant truth-potential values to floating point, causing spurious tiny-scale failures. It was corrected to explicit Fraction arithmetic, and type assertions now enforce exact gains and no symbolic Float atoms. A separate JSON serialization issue for symbolic integer normals was corrected. Both historical logs are retained under evidence/development. Neither required a source-theorem change. Final accepted checks use exact arithmetic throughout.
