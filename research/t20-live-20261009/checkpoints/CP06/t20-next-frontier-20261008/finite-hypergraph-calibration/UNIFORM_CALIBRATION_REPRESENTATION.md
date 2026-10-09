# Uniform approximation from an effective response oracle

This representation-level corollary uses a stronger oracle contract than a fixed finite panel. It does not mean that one fixed finite record determines an arbitrary complete calibration function.

## Oracle and prerequisites

Assume the fixed-inventory model and a promised positive interaction containing the root i. An **all-command point-evaluation oracle** accepts any rational command vector in [0,1]^R and any requested value accuracy, and returns a rational enclosure for the corresponding population Q value with certified width below that accuracy. All answers are consistent with the same fixed Q. Unit and zero commands are allowed, and new rational points may be queried as the algorithm proceeds. The input oracle does not directly supply a uniform-norm approximation or a modulus of continuity for Q.

The boundary procedure supplies, uniformly for any rational x in (0,1) and desired accuracy, a certified enclosure for r_i(x). Its positive support/count setup can be reused: after the finite count searches, either the unary formula or the ratio P_S(x,x_T)/P_T(x_T) evaluates each new point. Denominators at the fixed auxiliary interior levels are positive and effectively bounded away from zero by refinement. At x=0 and x=1 the values are known exactly.

This is a reduction relative to a supplied population response oracle. It does not assert that arbitrary physical response probabilities or calibration functions are computable without that oracle, and does not obtain such an oracle from finite samples.

## A finite algorithm for each requested uniform accuracy

Fix a rational 0<epsilon<1. For dyadic meshes x_j=j/2^m, j=0,...,2^m, obtain rational intervals [l_j,u_j] containing r_i(x_j), clipped to [0,1], of width at most epsilon/8. Use exact intervals [0,0] and [1,1] at the endpoints.

Increase m until the rational test

max_j (u_(j+1)-l_j) < epsilon/2

passes. This test certifies a bound on each whole mesh interval, not only on the sampled points: monotonicity gives r_i(x) in [l_j,u_(j+1)] whenever x_j<=x<=x_(j+1).

The search terminates. Continuity on the compact interval implies that the maximum true adjacent increment tends to zero on successively finer dyadic grids. Also

u_(j+1)-l_j <= r_i(x_(j+1))-r_i(x_j)+epsilon/4.

Eventually every true increment is less than epsilon/4, so the strict stopping test passes. No numerical modulus of continuity was supplied; the observed enclosure test provides the finite certificate for this particular function and tolerance. There is no uniform bound on the mesh or number of queries over arbitrary homeomorphisms.

## A rational polygonal output, including strict monotonicity

Set a_j=max_(h<=j) l_h and let a(x) be the polygonal interpolant through (x_j,a_j). The a_j are rational, nondecreasing, satisfy a_0=0,a_last=1, and obey a_j<=r_i(x_j). On each mesh interval both a(x) and r_i(x) lie in [l_j,u_(j+1)], so

sup_x |a(x)-r_i(x)| < epsilon/2.

If a strictly increasing approximant is desired, put eta=epsilon/4 and

g(x)=(1-eta)a(x)+eta x.

This is a rational polygonal increasing homeomorphism with fixed endpoints, and

sup_x |g(x)-r_i(x)| <= sup_x |a(x)-r_i(x)|+eta <epsilon.

Running the procedure for epsilon=2^(-k) produces a uniform Cauchy representation of the whole continuous calibration function relative to the response oracle. It also supports evaluation at arbitrary real inputs supplied by Cauchy names, using the effective polygonal approximants. Each requested accuracy uses finitely many queries, but later accuracies may introduce new commands.

This is not exact symbolic recovery from finitely many data, not a fixed-panel claim, not a finite-sample theorem, and not a uniform query/runtime bound. If continuity or monotonicity is dropped, the enclosure argument or its termination can fail. No a priori or world-uniform calibration modulus is supplied; the stopped mesh does certify a function-specific continuity scale relative to the oracle. No physical instrument or source interpretation is certified by this construction.
