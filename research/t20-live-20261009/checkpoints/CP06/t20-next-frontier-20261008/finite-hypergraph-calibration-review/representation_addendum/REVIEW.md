# Independent extension review: effective uniform calibration representation

8 October 2026 UTC. The mathematical representation corollary and the separate linear-record scope argument pass independent review. Exact accepted author bytes and the applicable scope qualification are recorded in REVIEW_RECEIPT.json. This extension leaves the earlier sealed three-artifact review and the superseding unary receipt unchanged.

## 1. The exact computational claim

The input is one consistent point-evaluation oracle for the same population response Q, accepting arbitrary rational command vectors and rational requested accuracies. Unit commands are allowed. The oracle is not assumed to supply a modulus or a uniform-norm name. The model and a positive interaction containing the target root are promises.

The previously reviewed boundary reconstruction is uniform in a new rational target point x. Its count searches and fixed auxiliary-point denominators can be cached. Known positive denominators eventually acquire positive rational lower bounds, after which interval arithmetic supplies any requested accuracy. Thus the reduction gives a rational-point evaluator for r_i relative to the supplied Q oracle. This is relative computability, not an assertion that an arbitrary physical response oracle is effectively obtainable.

The new algorithm may query additional command points as accuracy increases. A fixed finite record still cannot determine an arbitrary complete homeomorphism. A family of finite adaptive computations, one for each requested accuracy, can nevertheless produce a complete uniform Cauchy representation from an all-command oracle. Those are different representation contracts, and no finite-panel impossibility is contradicted.

## 2. Why the stopping rule certifies whole cells

At mesh points x_j=j/2^m, let [l_j,u_j] contain r(x_j), with width at most epsilon/8 and exact endpoint intervals. For every x in the j-th cell, monotonicity gives

    l_j <= r(x_j) <= r(x) <= r(x_(j+1)) <= u_(j+1).

Consequently the rational strict test

    max_j [u_(j+1)-l_j] < epsilon/2

certifies a range of width less than epsilon/2 on every entire cell. It is stronger than merely checking finitely many differences of approximate point estimates.

Every loop iteration is finite. Moreover,

    u_(j+1)-l_j <= r(x_(j+1))-r(x_j)+epsilon/4.

Uniform continuity on [0,1] implies the maximum true increment goes below epsilon/4 on sufficiently fine dyadic meshes. Hence the strict test eventually passes, even if the returned intervals take their worst allowed endpoint errors. The search does not require a previously supplied numerical modulus. No bound on its stopping mesh is uniform over arbitrary increasing homeomorphisms.

## 3. Prefix maxima and the strict homeomorphic output

Define a_j=max_(h<=j) l_h. Then

    l_j <= a_j <= r(x_j),

because every earlier lower endpoint is at most its earlier true value, which is at most r(x_j). Thus the a_j are nondecreasing, rational, and have endpoints zero and one.

On a cell, the polygonal interpolant a(x) lies between a_j and a_(j+1), hence within [l_j,u_(j+1)]. The true r(x) lies in that same interval. The certified cell width therefore proves

    ||a-r||_infinity < epsilon/2.

The proof does not need the potentially false stronger assertion a(x)<=r(x) between knots.

With eta=epsilon/4, let g(x)=(1-eta)a(x)+eta x. Every segment slope of a is nonnegative, so every segment slope of g is at least eta>0. Its endpoints remain fixed, and its rational knots define a strictly increasing homeomorphism. Since a and x both take values in [0,1],

    ||g-r||_infinity <= ||a-r||_infinity+eta < epsilon.

Taking epsilon=2^(-k), for k>=1, gives an effective uniform name. Evaluation at an arbitrary real x supplied by a Cauchy name follows: pick a sufficiently accurate polygonal approximation, compute its finite rational Lipschitz bound, and request enough precision in x to bound the remaining evaluation error. No calibration differentiability is involved.

## 4. A modulus qualification

The construction does not require an input modulus and does not give a world-independent one. It does, however, compute a function-specific modulus relative to the response oracle. This distinction matters for the final disclaimer.

If h=2^(-m) is the stopping mesh width, every cell has oscillation less than epsilon/2. Two points at distance at most h span at most two adjacent cells. Monotonicity therefore gives

    |x-y|<=h  implies  |r(x)-r(y)|<epsilon.

Thus the same finite certificate supplies a modulus value at each requested tolerance. The original unqualified sentence saying that no calibration modulus is certified was too broad. The correct statement is that no a priori or world-uniform calibration modulus is supplied or established. The finalized author file now makes this distinction explicitly. The sole sentence replacement was checked against the earlier supplied digest; it does not change the algorithm or its proof.

## 5. Linear-record scope

LINEAR_RECORD_SCOPE.md correctly avoids substituting log-rate coordinates for probability masses in the historical signed-law proposition. The calibration feasible domain is open. For every kernel vector, sufficiently small displacements in both directions remain feasible, proving span(F-F)=ker A. The usual annihilator/row-space criterion follows on that domain without a mass condition.

The AB, AC example has kernel vector (1,-1,-1), with nonzero coordinate sum, and positive scale factors (6/5,5/6,5/6) preserve its support products. A fictitious mass-zero restriction removes a genuine calibration gauge. Adding the row (1,1,1) is an additional product observation and yields full rank; it is not automatic normalization. The distinction between ordinary unsigned incidence and oriented difference incidence is also correct.

This addendum checks the mathematical transport against the already bound historical analysis and scope correction. It does not claim a new independent reading of the archived PDF or independent verification of every source-audit statement in author packaging that is outside this receipt.

## 6. Independent controls and limitations

The independent standard-library script runs 24 reconstructions for three rational polygonal homeomorphisms, four tolerances, and two certified interval styles. One fixture has a narrow steep central section, and another has a very flat initial section. Eight accepted panels have nonmonotone raw lower endpoints, exercising the prefix-max correction. Exact uniform errors are computed at the union of source and output breakpoints, where the piecewise-affine difference attains its extrema.

All 251 assertions pass. They include exact whole-function error bounds for both outputs, endpoint and monotonicity checks, certified modulus-distance checks, and ten monotone-discontinuity controls whose jumps correctly prevent the stopping certificate. The observed largest mesh exponent 12 and 25,852 point-evaluator calls are diagnostic fixture costs, not universal bounds.

These controls test the representation algorithm after pointwise calibration access has been established by the separately reviewed boundary proof. They do not pretend that the test harness reconstructs its fixture calibration directly from a physical response experiment. The general theorem rests on the preceding proof audit, not finite testing alone.

No finite Bernoulli-sample guarantee, fixed finite-panel whole-function identification, exact symbolic representation of arbitrary reals, physical calibration certification, protected integration, owner acceptance or T20 closure follows.
