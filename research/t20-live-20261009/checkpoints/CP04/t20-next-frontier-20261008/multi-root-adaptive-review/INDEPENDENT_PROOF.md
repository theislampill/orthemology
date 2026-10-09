# Independent review of the arbitrary-rate multi-root bound

8 October 2026. This is a mathematical review of a new sibling result. No predecessor is edited, and no model-to-world validation or integration is implied.

## Verdict on the proposed statement

The stated hard pair and constant are valid for every integer r >= 2 and total route bound L >= r+1, with k=floor((L-1)/r). The full response menu may include arbitrary issued profiles and arbitrary root-specific survival rates in [0,1], chosen adaptively, provided that every incidence at a given root has the same chosen rate and the stated fresh conditional independent-route response law holds.

The exact conclusion is

    N >= kl(1-delta,delta) / C(r,k),
    C(r,k) = [2/(k(k+3))] [4/(k+1)^2] [4/(k+2)^2]^(r-2).

It concerns fixed total budgets and worst-case per-model error at most delta. Matching order in log(1/delta) requires delta bounded away from 1/2, for example 0 < delta <= 1/4. A claim uniform over the entire interval 0 < delta < 1/2 would not follow and should not be made.

## Independent reconstruction of the hard pair

Let H0 contain k distinct singleton routes at each of the r roots. Let H1 add one route with the full positive support. All routes have no absence guards and emit the same designated nonempty effect or fixed nonempty effect bundle. They use rk and rk+1 routes respectively, so both satisfy the single total bound L. The construction does not use a bound of L separately at every root. Since k >= 1, every root occurs in both inventories.

On a proper issued profile the extra route is disabled, and all remaining enabled routes are shared between H0 and H1. Consequently the entire endpoint laws coincide. This includes an empty issued profile if the menu allows it.

At the full profile, write a_i for the common survival rate at root i, u_i=1-a_i, and z=product_i a_i. Independent route responses give the no-effect probabilities

    q0 = product_i u_i^k,
    q1 = q0(1-z).

The endpoint is exactly binary: either the empty output or the fixed bundle. Reading the full endpoint, rather than only an absence bit, therefore cannot improve discrimination of this pair.

If any a_i=0, z=0 and q0=q1. If any a_i=1, its at least one singleton succeeds surely, so q0=q1=0. Thus every boundary-rate vector gives identical laws at the full profile. Boundary vectors need not give identical laws for arbitrary unrelated inventories; this assertion is only for the specified pair.

## Interior divergence inequality, factor by factor

Suppose all a_i are strictly between zero and one. Both q0 and q1 lie strictly between zero and one. Applying log x <= x-1 in the two Bernoulli terms yields

    KL(Ber(q0) || Ber(q1))
      <= (q0-q1)^2 / [q1(1-q1)]
      = q0 z^2 / [(1-z)(1-q1)].

Two lower denominator bounds are valid simultaneously:

    1-z >= 1-a_2 = u_2,
    1-q1 >= 1-q0 >= 1-u_1^k
           = a_1 sum_{j=0}^{k-1} u_1^j.

Substitution and cancellation give

    KL <= A_k(u_1) B_k(u_2) product_{i=3}^r D_k(u_i),

where

    A_k(u) = u^k(1-u) / sum_{j=0}^{k-1}u^j,
    B_k(u) = u^(k-1)(1-u)^2,
    D_k(u) = u^k(1-u)^2.

There is no uncancelled incidence factor or hidden dependence between these bounds.

For A_k, arithmetic-geometric mean gives

    sum_{j=0}^{k-1}u^j >= k u^((k-1)/2),
    A_k(u) <= u^((k+1)/2)(1-u)/k.

The maximum of u^alpha(1-u), for alpha>0, occurs at u=alpha/(alpha+1) and is at most 1/(alpha+1). With alpha=(k+1)/2, this gives

    A_k(u) <= 2/[k(k+3)].

For B_k, when k>=2 the maximizer is u=(k-1)/(k+1), and the maximum is

    [(k-1)/(k+1)]^(k-1) 4/(k+1)^2
      <= 4/(k+1)^2.

For k=1, B_1(u)=(1-u)^2 <= 1 = 4/(1+1)^2, including its boundary supremum. No 0^0 convention is required. The AM-GM step for A_1 is the one-term equality 1=1; its bound is valid (and deliberately loose).

For D_k, k>=1, the maximizer is u=k/(k+2), and the maximum is

    [k/(k+2)]^k 4/(k+2)^2 <= 4/(k+2)^2.

Multiplying these bounds proves C(r,k), including r=2 where the D-product is empty. The formula is not claimed for r=1; the separate one-root result covers that case.

## Arbitrary adaptive actions and the confidence factor

A measurable randomized policy uses the same action-selection kernel under the two models after any fixed common history. An action consists of an issued profile and a root-rate vector, and may range over a continuum. Conditioning on it, the endpoint KL is at most C(r,k), including proper profiles and boundary rates where it is zero. The per-step endpoint laws have common support. The likelihood factorization or KL chain rule therefore gives

    KL(full transcript under H0 || full transcript under H1) <= N C(r,k).

Include the policy's randomization and final decision in the transcript if needed. Their conditional kernels are common to the two hypotheses, so they add no KL. No finite discretization of the rate set is used in this argument. A procedure that always stops by N can be padded with zero-information trials; an expected-budget procedure without a deterministic horizon is not covered by this statement.

Let E be the event that the final output identifies H0. Per-model correctness gives P0(E)>=1-delta and P1(E)<=delta. Coarsening the transcript to this event gives

    KL(transcript) >= kl(P0(E),P1(E)) >= kl(1-delta,delta).

The second inequality follows from monotonicity of binary KL on p>q: it increases with p and decreases with q. If an event probability is zero at the wrong endpoint, the divergence is infinite and the conclusion is immediate. For 0<delta<1/2,

    kl(1-delta,delta) = (1-2delta) log((1-delta)/delta).

For delta<=1/4 this is at least (1/2)log(1/(2delta)), and hence at least (1/4)log(1/delta). As delta approaches 1/2 it tends to zero while log(1/delta) tends to log 2. Thus the confidence qualification is substantive.

The reciprocal constant is exactly

    1/C(r,k) = k(k+3)(k+1)^2(k+2)^(2r-4) / [2 * 4^(r-1)].

For fixed r, k is of order L, and this expression is of order L^(2r). More explicitly, k>=L/(4r) for every L>=r+1, so

    1/C(r,k) >= L^(2r) / [2 * 4^(r-1) * (4r)^(2r)].

This establishes the count exponent uniformly over the admitted total bounds without treating L as a per-root count.

## Exact scope of the inherited matching upper

The inherited noise-aware theorem uses its total-count parameter K=L. Set p=1/(2L). Its actions issue each nonempty profile S and choose each nonempty attenuation mask V within S, giving rate p on V and rate zero elsewhere while keeping the issued profile and its guards fixed. This is a subset of the new trial menu.

It recovers the full anonymous direct-route histogram with positive support, disjoint absence guard and nonempty output subset under the stipulated independent-route endpoint law. There are

    G = 3^r-2^r actuator settings,
    Q = G(2^m-1) retained absence coordinates,
    epsilon = (1/(2L))^r / (16 * 2^r).

One paired full-endpoint observation supplies every effect-query indicator at that setting. Thus the total budget is G times the repetitions per setting, not Q times that number. Under exact calibration a sufficient total is

    G * ceil[128 * (16 L^2)^r * log(2Q/delta)].

The inherited exact rational log enclosure certifies integer rounding; it does not impose an additional asymptotic sample factor. Correlation among different query indicators within the same trial is allowed. Fresh sampling with the stated conditional law is still necessary.

With fixed r and fixed m (or a fixed declared observation class), this is O(L^(2r) log(1/delta)) for 0<delta<1/2. Combined with the new lower bound, the order matches for 0<delta<=delta0<1/2. If m varies, retain its dependence through log(2Q/delta). The r-dependent setting count and constants are not uniform polynomial-in-r bounds.

The lower hard pair is an unguarded single-bundle subfamily, so it lower-bounds any full guarded multi-effect recovery procedure whose target class contains it. Conversely, the upper theorem does not automatically apply to every alternative response model, observation interface, correlated-route model, calibration-error model, or mixture task. Their assumptions and targets must be checked separately.

## Review exclusions

This review establishes no optimal constants, expected-stopping-time result, route-addressable-gating result, mixture-recovery upper bound, unbounded-root-dimension complexity, physical actuator separability, causal applicability, metaphysical conclusion, protected integration, or T20 closure.
