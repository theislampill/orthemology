# Exact two-dimensional panel complexity and bounded adaptive support

8 October 2026 UTC. Scratch-only mathematical successor. Earlier files and frozen predecessors are preserved. No repository integration, empirical validation, physical-access claim, or T20 closure is made.

## 1. Result and assumptions

A route with threshold t=(x,y) responds at command q=(a,b) exactly when x<=a and y<=b. The endpoint is the OR over a finite inventory of routes. A panel labels finitely many commands in [0,1]^2 positive or negative. All commands interrogate the same unchanged threshold vector, with separately readable, nonlatched noiseless bits. Coordinate-separable AND-route semantics is essential.

For a consistent finite panel, discard positive commands dominated by other positive commands, and write the remaining distinct minimal positive antichain as

    (a_1,b_1),...,(a_p,b_p),  a_1<...<a_p, b_1>...>b_p.

For each negative z=(u,v), define

    j(z)=max({i:a_i<=u} union {0}),
    k(z)=min({i:b_i<=v} union {p+1}).

Consistency is equivalent to j(z)<k(z) for every negative, or equivalently no positive command lies coordinatewise below a negative. Retain only negatives with 1<=j<k<=p, and associate the integer interval {j,...,k-1} of possible cuts. Let tau be the minimum number of cuts hitting every such interval; tau=0 for an empty family.

**Exact deterministic theorem.** The least number of threshold routes realizing the labels is

    d=0 if p=0; otherwise d=1+tau.                         (1)

Here thresholds may be anywhere in [0,1]^2, so the statement includes boundary commands and exact equality. An inconsistent panel has no realization; formula (1) is not applied to it.

**Sharp probe bound.** To force at least m>=1 routes, a finite panel needs at least m positive commands and m-1 negative commands, hence at least 2m-1 probes. Strict interior staircases attain this bound. The bound concerns the number of observations within one retained vector, including repeated queries if any; repetition cannot help.

**Bounded adaptive support theorem.** Fix n>=1 and a common measurable, possibly randomized policy of depth at most 2n on one unchanged vector. Under the target law, there are exactly n independent routes, each assigning positive probability to every nonempty open rectangle in (0,1)^2. Under the source law, there are any fixed k>=1 routes with an arbitrary joint law supported on ((0,1]^2)^k. The policy's exogenous random seed has the same law in both worlds and is independent of the vector. Then

    Law_source(transcript) << Law_target(transcript).     (2)

In particular, an (n+1)-route law cannot give positive probability to a transcript event that has zero probability under the n-route full-support law with at most 2n probes. The transcript may include commands, stopping, outputs, and the seed itself. Measurability is required; neither continuity of command selection nor a finite set of possible commands is required.

The source law needs neither independence, full support, nor continuous margins. The target law needs full product support; independence of full-support route laws is a sufficient way to obtain it. Continuous full-support independent route laws, including the inherited uniform/Joe laws, meet these conditions. Atomless coordinate margins and null-equality arguments are unnecessary. Allowing mass on the upper boundary is harmless; allowing source threshold coordinates equal to zero can invalidate (2).

At 2n+1 fixed strict interior probes, the inherited staircase event is positive under n+1 independent full-support routes and impossible under n routes. Thus 2n+1 is exactly the smallest bounded depth that can create this one-sided support separation in two dimensions under these laws.

## 2. Proof of the deterministic formula

A positive q dominated by another positive q' (q'<=q) imposes no extra requirement, by monotonicity. After removing such points and duplicates, any two minimal positives are incomparable. Their first coordinates are therefore strictly increasing and their second coordinates strictly decreasing. Every original positive lies above a minimal one. A negative is compatible with these positives exactly when it dominates none of them, which is exactly j<k. The construction below proves sufficiency as well as necessity.

For one route, the indices i of minimal positives it covers form a consecutive interval: x<=a_i selects a suffix, while y<=b_i selects a prefix. Empty coverage is allowed. Suppose a collection of r routes covers all p minimal positives and avoids all negatives. Its coverage intervals cover {1,...,p}. Starting with the leftmost uncovered index, choose among intervals containing that index one with largest right endpoint, and assign the still-uncovered consecutive block through that endpoint to it. Repeat. Each selected route is used at most once because all earlier selected intervals end before the next uncovered index. This yields a partition into at most r nonempty consecutive blocks, each contained in the coverage interval of an original route.

For a block [l,h], its coordinatewise meet is

    c_[l,h]=(a_l,b_h).

A route covering the block has threshold <=c_[l,h]. If a negative dominated c_[l,h], that route would also hit the negative. Therefore each selected block corner avoids every negative. Conversely the route with threshold exactly c_[l,h] covers that block, and avoids all negatives whenever none dominates the corner. It covers precisely that block among the minimal positives.

A negative z dominates c_[l,h] exactly when l<=j(z) and h>=k(z). A partition has a block satisfying these two inequalities exactly when there is no cut between indices j and k, that is, no chosen cut in {j,...,k-1}. Negatives with j=0 or k=p+1 cannot dominate any block corner. Thus an admissible partition is exactly a set of cuts hitting every retained interval.

Any realizing r-route inventory yields a partition with at most r blocks and hence tau<=r-1. Conversely a minimum hitting set yields tau+1 blocks whose corner routes realize every original label. This proves (1) when p>0. With no positives, the empty route inventory realizes every negative, proving d=0. These arguments use the literal <= success convention, without discarding equality cases.

For completeness, tau is computed by the usual interval greedy rule: take an interval with smallest right endpoint, select that endpoint, discard every interval hit, and repeat. The selected witness intervals are pairwise disjoint: a later unhit interval cannot extend left of the previously selected endpoint while having right endpoint at least that endpoint. Any hitting set must hit each witness interval separately. The greedy set therefore attains the lower bound. Equivalently, tau equals the largest number nu of pairwise-disjoint negative-obligation intervals, so d=1+nu when positives exist. This standard interval duality gives a finite checkable certificate on both sides: block-corner routes certify the upper bound, and disjoint negative-obligation intervals certify the lower bound. This optimization fact is not needed to establish the partition equivalence.

## 3. Sharpness and what “needs m positives” means

Let P and N be the original numbers of positive and negative probes, counting repetitions. For nonempty positives, p<=P and tau<=N, since picking one cut from every retained interval always suffices. Also d<=p by taking a route at each minimal positive. Consequently

    d<=min(P,N+1), and d>=m implies P>=m, N>=m-1.          (3)

This is a necessity claim, not a claim that every panel with those label counts forces m routes. No-positive panels have d=0. In particular a consistent panel with L probes has d<=floor((L+1)/2) whenever it has a positive.

For sharpness choose any strictly interior staircase with m points q_i=(a_i,b_i), and query also r_i=(a_i,b_(i+1)) for i=1,...,m-1. Label all q_i positive and all r_i negative. Every connector contributes the singleton cut interval {i}. Thus tau=m-1 and d=m, using exactly 2m-1 probes. One explicit choice is a_i=i/(m+1), b_i=(m+1-i)/(m+1). This includes m=1, when there is one positive and no negative.

The lower bound is a property of two-dimensional upper rectangles. It is not a bound for arbitrary monotone Boolean success functions, context-dependent gates, refreshed vectors, latched outputs, noisy bits, or route mutation.

## 4. Open realizations, boundary cases, and exact route counts

A finite consistent panel is called boundary-admissible here if every positive has both coordinates strictly positive and no negative is (1,1). Every panel produced by a nonempty inventory with thresholds in (0,1]^2 is boundary-admissible: a hit requires both command coordinates positive, and every route hits (1,1).

**Open realization lemma.** If such a panel has deterministic minimum d and r>=max(1,d), it has a nonempty open set of realizing threshold vectors in ((0,1)^2)^r.

When positives exist, take the d block corners from section 2. Every corner has strictly positive coordinates. For each corner c and negative z, at least one coordinate of c is strictly greater than the corresponding coordinate of z. There are only finitely many corner-negative pairs. Move both coordinates of every corner downward by a sufficiently small positive epsilon: less than every corner coordinate, and less than one selected positive gap for every corner-negative pair. This puts the thresholds in the open square, strictly below the coordinates of every positive in their blocks, while retaining a strict nonhit coordinate for every negative. Every intended hit and miss therefore survives throughout a sufficiently small open neighborhood of the constructed vector. Other positive commands lie above their minimal witnesses and also remain strictly hit.

To reach exactly r>d routes, add thresholds strictly above one constructed witness in both coordinates and strictly below 1. These routes are dominated in their effects: every command they hit is also hit by that witness. All negatives remain strictly missed. Choosing these inequalities with positive gaps gives a joint open neighborhood for the full r-route vector, rather than relying on exact duplicate thresholds, an event that might have zero probability.

When there are no positives, every negative differs from (1,1). For each negative choose a coordinate less than 1. Finiteness permits epsilon>0 such that (1-epsilon,1-epsilon) strictly exceeds that selected coordinate for every negative. Put all r thresholds in a sufficiently small open neighborhood of this point. Then all routes miss every negative. An empty panel is included.

This proves the lemma, including face commands, repeated commands, equality between an original threshold and a queried coordinate, and positive commands at (1,1). No source threshold is inferred or estimated from observations. The existence proof is enough.

The restrictions are real. A deterministic threshold (0,0) can hit command (0,0), while a target law supported in the open square (for example, uniform) never does; this gives a one-probe failure if the source may use zero coordinates. An empty source inventory can miss (1,1), whereas every nonempty target inventory hits it. Such source models are outside theorem (2). A panel with a negative (1,1) still has combinatorial minimum zero if it has no positives, but cannot be padded to a positive inventory. Combinatorial zero-route realizability and positive-inventory open realizability must not be conflated.

## 5. Measurable adaptive policies and support inclusion

Represent all exogenous policy randomization by a seed S in a standard Borel space, with probability law rho independent of the route vector and common to the worlds. Once S=s is fixed, the policy is a deterministic binary decision tree of depth at most L=2n. At each node its next command is a measurable function of s and preceding bits. Stopping is also measurable. Pad stopped paths with a common dummy symbol to obtain a finite collection of possible bit/stop words. This padding does not query a vector again or change the route count.

For a fixed s and leaf b, the actual commands along that leaf form a fixed finite labelled panel with at most 2n probes. If the leaf is realized by any allowed source vector, it is consistent and boundary-admissible. Equation (3) implies its minimum d is at most n: d>=n+1 would require at least 2n+1 probes. The open realization lemma then provides a nonempty open set of n-route target vectors yielding exactly that labelled panel. They follow the same adaptive path because the policy has the same fixed seed and every preceding bit agrees. Every nonempty open set in the product contains a product of nonempty open rectangles. Independence and per-route full support give this product positive target probability. Therefore

    K_source(s,b)>0 implies K_target(s,b)>0,              (4)

where K denotes the conditional probability of the leaf given s. Indeed the argument applies even to a source-realizable leaf of zero source probability. Threshold equalities cause no problem: the new open realization can lie elsewhere.

Let E be any measurable event in the full transcript, possibly including the seed. The transcript at a given seed and leaf is a measurable deterministic function T(s,b). Its probability is

    P_i(E)=integral sum_b 1_E(T(s,b)) K_i(s,b) rho(ds).    (5)

The finite-leaf kernels are measurable because the command policies and coordinate comparisons are measurable. If P_target(E)=0, each nonnegative summand vanishes for rho-almost every s. By (4), the corresponding source summands also vanish almost everywhere. Equation (5) gives P_source(E)=0. This proves (2) without any measurable choice of realizing thresholds, uniform lower probability bound, or conditioning on a positive-probability exact seed value. Projection gives the same result when the seed or commands are not shown.

A common randomized Markov policy on standard Borel command spaces admits this seed formulation; alternatively the seed formulation can be taken as the explicit policy contract. A world-dependent policy, a seed correlated with the vector, route-identity access, or additional informative observations is outside this statement.

Under independent full-support laws supported in the open square for both n and n+1 routes, the two bounded-depth transcript laws are in fact mutually absolutely continuous. The displayed theorem gives the larger-to-smaller direction. For the reverse, any realized n-route panel has deterministic minimum at most n; open realization and dominated padding to n+1 work at every finite depth, and the same seedwise integration applies. Only the larger-to-smaller direction needs the 2n cap. More generally the upper-count source direction in (2) holds for every fixed finite k>=1, not just n+1.

## 6. Sharp separation and relation to the inherited hard pair

Use the m=n+1 staircase from section 3. Its all-positive-q/all-negative-r event requires m distinct routes. It is impossible with n routes. The open realization lemma with r=m shows that it has positive probability under any m independent open-square-full-support route laws. This is a fixed, nonadaptive 2n+1-probe construction.

The inherited retained-interior packet specializes this to independent uniform baseline thresholds and iid Joe alternative thresholds with CDF F_c(a,b)=1-(1-ab)^c, c=n/(n+1). Its strict positive density on the open square supplies full support. It also gives the exact m! product-of-box-masses probability for that law. Those probability formulas need not be rederived for the minimality theorem; the new contribution is the matching lower probe bound and adaptive support transport.

The earlier full-face-threshold KL packet concerns a different, face-only channel and remains unchanged. Absolute continuity below 2n+1 does not imply finite KL, a bounded likelihood ratio, any quantitative error or sample-rate bound, or favorable computational complexity. Equivalent distributions can still have infinite KL. No sample-rate or philosophical conclusion is drawn here.

## 7. Three dimensions: the two-dimensional bound fails

For three-coordinate AND routes, take positive commands

    (2/3,1/3,1/3), (1/3,2/3,1/3), (1/3,1/3,2/3)

and negative command (1/3,1/3,1/3). The coordinatewise meet of every pair of positives is exactly the negative. A route hitting any pair therefore hits the negative, a contradiction. Three distinct routes are necessary. They are sufficient, and robustly so, using thresholds

    (1/2,1/6,1/6), (1/6,1/2,1/6), (1/6,1/6,1/2).

All required inequalities have strict slack. Thus four probes force three routes and give a positive/zero event under independent full-support three-route/two-route laws. This is less than 2m-1=5 for m=3. The one-dimensional order of a two-dimensional antichain and its interval-cover structure do not extend to this configuration.

## 8. Evidence, exact assurance level, and limits

The formula, open realization lemma, adaptive absolute continuity, sharpness, and three-dimensional counterexample above are written mathematical proofs. No new Lean theorem or other proof-assistant artifact is supplied. The predecessor's kernel-checked witness injection proves its own staircase obstruction; it does not kernel-check the new minimality or adaptive theorems.

controls.py independently enumerates upper-rectangle union functions by breadth-first OR construction and computes their exact minimum route counts. It compares those values with an independently enumerated interval hitting-set formula for every ternary-labelled partial panel on 3x3 and 4x3 grids. It also checks interval greedy against exhaustive hitting sets through p=5, and exhaustively enumerates ternary panels on the 2x2x2 cube. These are bounded deterministic controls, not a replacement for the proofs, not tests of arbitrary real measurable policies, and not empirical sampling. All checks passed: 19,683 panels on 3x3; 531,441 on 4x3; 1,099 interval families; and 6,561 panels on the 2x2x2 cube. The 2D grids attain minimum panel sizes 1, 3, 5 for exact minimum route counts 1, 2, 3; the cube attains 1, 3, 4. CONTROL_RESULTS.json and CONTROL_RUN.log contain exact counts and the code digest. Every continuous threshold has the same finite-grid hit mask as a grid threshold or an inactive route, so the brute-force comparator exhausts the finite-grid model rather than just a chosen threshold subset.

CURRENT_SOURCE_BINDINGS.json binds the two predecessor results actually read and the generated artifacts. Existing SOURCE_BINDINGS.json and earlier event records are preserved as historical records. New events describe only this resumed work prospectively; no historical activity duration, uninterrupted research time, or prior execution is certified. No public literature search or field-wide novelty claim is made. The argument uses elementary interval covering, finite monotonicity, open-set support, and conditional integration.
