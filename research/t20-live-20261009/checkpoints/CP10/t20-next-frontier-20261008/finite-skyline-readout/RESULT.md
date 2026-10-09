# Finite noiseless probes implement the skyline-count test

8 October 2026 UTC. Bounded mathematical follow-on. Historical floor remains UNVERIFIED. No protected integration, archive mutation, physical-instrument guarantee, empirical evidence, or closure claim.

## Result

The ideal skyline-count test in ../skyline-count-information/RESULT.md can be implemented with finitely many adaptive noiseless endpoint probes on each retained vector. At fixed per-world error tolerance, it retains the O(n^4/log n) independent-vector upper bound. Each vector costs at most O(n log n) endpoint probes and O((log n)^2) probes in expectation. These are different resources: this does not establish an improved total-probe bound over the full face-only experiment, prove optimality, or remove the known-hard-pair calibration assumption.

The parent's grid-collision/extraction candidate is valid. This packet supplies its deterministic proof, exact resolution arithmetic and exhaustive small-grid controls. The sibling count packet supplies the ideal-test means and variance bounds, not independently re-proved here.

## 1. Observation contract and deterministic quantization

For a finite multiset S of N points (X_i,Y_i) in [0,1]^2, the retained endpoint oracle is

    B(a,b) = 1 iff some i has X_i <= a and Y_i <= b.

All queries for one vector use exactly the same S. A complemented no-hit instrument can be converted by flipping its bit. Resets for the statistical test are independent. Arbitrary dependence between X_i and Y_i within a route is allowed in the extraction and collision arguments; the collision argument uses independence across routes and the specified marginal bounds. The ideal-count variance bound additionally uses the particular Joe law, not arbitrary dependence.

Fix an integer L >= 1. Define Q_L(x)=ceil(Lx), with Q_L(0)=0, and take grid endpoints j/L for j=0,...,L. Then

    x <= j/L iff Q_L(x) <= j.

Thus grid queries are exactly an oracle for the quantized multiset S_L={(Q_L(X_i),Q_L(Y_i))}. Count distinct Pareto-minimal locations, treating duplicate points as a single location. Write K and K_L for the counts before and after quantization. This convention agrees almost surely with route-record count under the continuous laws used below.

Always K_L <= K. To prove it, take any minimal quantized location q and an original point p mapping to it. In a finite set, p has an original minimal ancestor r<=p. Monotonicity of Q gives Q(r)<=q. Minimality of q forces Q(r)=q. Hence every quantized minimum is the image of an original minimum; the image-to-minimum map is surjective onto quantized minima, which proves the cardinality bound. Equality need not hold when bins collide; the controls retain explicit strict-loss examples.

If no two labeled points share a coordinate bin in either coordinate, Q preserves all pairwise strict coordinate orders, and thus preserves all dominance comparisons and K_L=K. This condition is sufficient, not necessary. The singleton bin {0} causes no issue; it has zero mass under the statistical laws below.

## 2. Exact finite extraction, including ties and endpoints

Use integer indices throughout. Set b=L and an empty output list. While b>=0:

1. Query B(L/L,b/L). If it is zero, terminate.
2. By monotone binary search on indices 0,...,L, find the least a with B(a/L,b/L)=1. The upper endpoint is already known true.
3. By monotone binary search on indices 0,...,b, find the least y with B(a/L,y/L)=1. Its upper endpoint is already known true.
4. Append (a,y), set b=y-1, and repeat.

The pair (a,y) is occupied. Some point supplies the step-3 hit. Its first coordinate cannot be less than a, by step 2 and y<=b, and its second cannot be less than y, by step 3. It is globally minimal: a point dominating it would lie within the current y<=b range and contradict one of those minimality assertions. Equal locations count only once.

Conversely, among points with second coordinate <=b, the chosen pair is the one with least first coordinate and, among ties, least second coordinate. Any remaining global minimum must have second coordinate <y; points with second coordinate >=y and first coordinate >=a are dominated by the recorded pair, and points with first coordinate <a and second coordinate <=b do not exist. Previously excluded points have second coordinate >b and cannot dominate a subsequently recorded point. Updating b=y-1 therefore excludes exactly the part of the remaining search region that cannot contain another unreported minimum. Inductively all and only global minima are output, in strictly increasing first and strictly decreasing second coordinate order. A y=0 minimum ends the loop without a negative-coordinate query. Empty S terminates at the first miss. Points at 0 and 1, coordinate ties, and duplicate locations are all covered by this proof.

Let d_L=ceil(log_2(L+1)). Each binary search uses at most d_L new queries, so the number T of actual endpoint queries obeys

    T <= K_L+1+2 K_L d_L <= 1+N(1+2d_L).

The bound includes every existence probe and a possible terminal miss. Reusing cached answers could reduce it; no such reduction is required. A binary search with a singleton range uses zero new queries. Thus the uniform cost statement is O((K_L+1) log(L+1)), including L=1. Actual-route N is n in world 0 and m in world 1; the common bound uses m.

## 3. Collision probability for the hard pair

The two known hypotheses are:

- P0: N=n iid product-uniform points;
- P1: N=m=n+1 iid points with joint CDF F_c(x,y)=1-(1-xy)^c, c=n/(n+1).

Under P1 either coordinate has CDF H_c(t)=1-(1-t)^c. For the jth nonzero bin, its mass is

    p_j = ((L-j+1)/L)^c - ((L-j)/L)^c <= L^(-c),

because for 0<c<=1 the increment (r+1)^c-r^c is at most 1 for integer r>=0. The zero bin has mass 0. Uniform bin masses are 1/L<=L^(-c). For two independent routes in either world, the chance of a same-bin collision in a fixed coordinate is sum_j p_j^2 <= max_j p_j <= L^(-c). No independence between the two coordinates is invoked.

A union bound over two coordinates and choose(N,2) route pairs gives

    P(K_L != K) <= N(N-1)L^(-c) <= m(m-1)L^(-c).

For R fresh retained vectors, couple their ideal counts and their grid-extracted counts by using the same underlying points. Then, under either hypothesis,

    P(any extracted count differs) <= R m(m-1)L^(-c).

This last union bound itself does not need independence between vectors; independent resets are needed for the ideal statistical test. This is a probability-of-error guarantee, not deterministic recovery of arbitrary real thresholds or of the full unquantized antichain coordinates.

## 4. Exact grid resolution and combined test

Choose alpha>0 and eta>0 with alpha+eta<1. For n>1 put

    delta=(H_n-1)/(n^2-1), V_j=H_j-H_j^(2),
    W_n=V_(n+1)+H_(n+1)^2-(H_n+delta)^2.

For n=1 put delta=(zeta(2)-1)/2, retaining the same V and W definitions. The count packet proves E0 K=H_n, E1 K=H_n+delta, Var0 K=V_n and Var1 K<=W_n. Take the positive integer

    R = max(1, ceil(4 max(V_n,W_n)/(alpha delta^2))).

Any certified integer upper bound on this expression also suffices. For n>=2 and rational alpha the expression is rational and can be evaluated with exact integer/fraction arithmetic; n=1 may use rigorous bounds on zeta(2), or the direct safe choice below. Set

    A=m(m-1)R/eta,
    L=max(1,ceil(A^(1/c)))=max(1,ceil(A^((n+1)/n))).

The equality is mathematical, not an instruction to trust a floating-point power and ceil. For rational A=p/q>0, the least acceptable positive integer L is found by integer doubling and binary search for

    L^n q^(n+1) >= p^(n+1).

This implements the ceiling exactly and verifies the bound without rounding risk. The included controls implement it. For n=1 an entirely rational safe vector budget is R=ceil(16/alpha): here delta>1/4 (zeta(2)>3/2), and the true Bernoulli variance is <=1/4, so Chebyshev gives error <=16/R. This option avoids evaluation of zeta(2) to set R, though the exact midpoint threshold can instead be replaced by any rigorously chosen separating threshold.

Extract K_L on each of the R vectors and decide P1 iff its sample average is at least H_n+delta/2. Couple this with the ideal-count decision using the same vectors. On the event that all counts match, both decisions agree exactly, including the convention at equality. Therefore each world's error is at most alpha+eta. In particular, for desired error epsilon in (0,1), use alpha=eta=epsilon/2. No unobserved original count is used by the implemented decision.

The decision threshold also admits a finite exact implementation: for n>=2 it is rational. At n=1, since all ideal/grid counts are integers 1 or 2, one may use threshold 1+1/8, delta>1/4, and R>=ceil(16/alpha). Under P0 the count is identically 1 even after quantization. Under P1 the ideal mean exceeds 1+1/4; Chebyshev with variance <=1/4 bounds the ideal error by 16/R (and hence <=alpha). The same eta coupling applies. This avoids requiring an exact transcendental comparator.

## 5. Resource accounting and scope

For fixed alpha,eta and n tending to infinity, the sibling proof gives R=O(n^4/log n). Then log L=O(log n). The deterministic per-vector query bound is O(m log L)=O(n log n). Since K_L<=K pointwise,

    E0 T <= 1+(1+2d_L)H_n,
    E1 T <= 1+(1+2d_L)(H_n+delta).

Thus expected probes per vector are O(log n log L)=O((log n)^2). For this R, total probes are O(n^5) in the worst case and O(n^4 log n) in expectation. These are upper bounds, not lower bounds or optimal rates. They do not establish a smaller total-probe complexity than the face-only experiment. Rational endpoint precision is finite but grows with L: O(log L) bits per grid index, aside from arithmetic and exact-response requirements. Query count does not charge physical precision, computation, state retention, or reset costs.

The strongest independent-vector comparator is ../full-face-threshold-kl-rate/RESULT.md, sections 1 and 6. For this same hard pair, its forward KL for the exact pair of coordinate minima satisfies D_n~1/(2n^4), and every arbitrary-length adaptive face-only protocol with a common policy, independent fresh vectors, unconditional terminal error at most epsilon<1/2 in both worlds, and all started vectors charged satisfies E1 N >= kl(1-epsilon,epsilon)/D_n = Omega_epsilon(n^4). This includes exact-minimum readout and is stronger than the older two-face-probe restriction. Our finite interior protocol uses the same pair and independent resets, always terminates, charges all R started vectors, and meets unconditional error epsilon with alpha=eta=epsilon/2. Its O_epsilon(n^4/log n) vector count therefore genuinely improves that face-only independent-vector lower-bound scale. It consumes the existing comparator theorem without re-proving or duplicating credit for it. Interior probes are the changed observation interface; no total-probe improvement follows. SOURCE_AUDIT.md binds the inspected source versions.

The protocol presupposes the named pair (including n and c), independently refreshed vectors, noiseless arbitrary rational endpoint access on the retained vector, and exact comparisons. It is not uniform over unknown calibrations, does not address noise or finite laboratory resolution, and does not recover dominated routes from a single skyline. It recovers a quantized minimal antichain deterministically and transfers the count test with controlled distributional failure probability. No numerical experiment substitutes for the proofs.

## 6. Deterministic checks

controls.py exhaustively checks extraction for all multisets of 0 through 4 points in grids {0,...,L}^2 for L=1,2,3,4: respectively 70, 715, 4,845 and 23,751 cases. Every extracted antichain equals direct dominance enumeration and every query count respects the displayed bound. A further 23,751 fine-grid multisets test K_L<=K and equality on the collision-free subset (250 cases), including endpoints and ties. Forty-eight rational parameter cases verify the exact integer resolution and minimality of L. CONTROL_RESULTS.json records PASS and strict-loss counterexamples to unconditional count preservation. These finite checks complement the general proofs; they do not prove the statistical laws empirically or give kernel assurance.
