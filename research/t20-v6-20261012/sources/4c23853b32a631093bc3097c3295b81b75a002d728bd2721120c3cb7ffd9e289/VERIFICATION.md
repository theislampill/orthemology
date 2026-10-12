# Proof-obligation verification

Status: ordinary author verification, 10 October 2026. No independent review, kernel certificate, protected integration, or closure authority.

- Arbitrary measurable-space result: only finite countably additive measures are used, so the Radon–Nikodym theorem is available. No singleton or topological-support arguments occur before the Polish specialization.
- Normalization: G gives finite positive mass at every probability. General updates require an explicit finite positive normalizer.
- Face forward direction: full strict convex coefficient t is handled, density bound 1/t is valid, and a bounded measurable everywhere version is chosen. Perturbed densities are bounded away from zero for each epsilon.
- TV convergence: the perturbed posterior equals (q+epsilon p)/(1+epsilon), so its distance to q tends to zero exactly; no weak/TV interchange is used.
- Face to absolute-continuity heredity: truncated normalized densities have positive mass, a_n increases to one, the mixture coefficient a_n/(2n) lies strictly between zero and one, and residual measures are nonnegative probabilities. The L1 error bound is 2(1-a_n).
- Reverse bounded update: choose t=Z/(2M), so t in (0,1) and t dq/dp<=1/2. This avoids a degenerate coefficient at an essentially constant likelihood.
- Fixed-reference counterexample: D(mu) is TV closed by testing each mu-null event; mixture positivity establishes its face property. Lebesgue singletons exclude every Dirac. The weak concentration law is normalized and its TV distance to delta_0 is one.
- Weak closure implies TV closure: bounded test integral error is at most 2||h||_infinity d_TV, so the implication has the correct direction.
- Allowed Diracs: F is the inverse image of closed C under the continuous Dirac map. Topological support is p-conull by second countability.
- Restriction at x: all conditioning sets are positive-mass balls, never null singletons. Their shrinking support gives weak convergence by continuity at x, without uniform continuity on the entire noncompact space.
- Arbitrary P(F) approximation: Borel disjointification of countably many balls gives measurable maps; finite atomic approximants are in C by convexity; tail mass controls TV; bounded convergence handles the final weak limit. Neither compactness nor a finitely supported representation of every law is assumed.
- P(F) closedness: the bounded continuous distance function has zero integral exactly at laws carried by the closed set. Uniqueness is read back through Dirac membership.
- Reciprocal boundary: L(x)=x on (0,1] has positive finite normalizer at every prior but no prior with a uniform posterior, because its inverse density is nonintegrable. This concerns surjectivity, not stability.
- Scope: universal likelihoods, full ambient probability space, named topology and declared law-level operations remain explicit. Restricted evidence, moment-record sufficiency, computation and normative claims are not inferred.

No executable theorem checker was run. Artifact hashes provide integrity only, not mathematical truth.
