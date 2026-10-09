# A uniformly stable replay-panel certificate and a bounded-sample reference test

8 October 2026 UTC. New prospective scratch sibling, separate from the frozen finite-panel-replay packet and excluded from the sixth checkpoint being assembled. This is a conditional mathematical result and a sampling theorem under declared assumptions, not a physical experiment, empirical validation, protected integration, or T20 closure.

## 1. Result

Fix a positive integer n. Set

    t = 1/[3(n+1)],
    A0 = B0 = (1-t)^n,
    Q0 = (1-t^2)^n,
    J0 = (1-t)^(2n),
    epsilon_n = 1/[10000(n+1)^2].

Consider any alternative positive integer count m, with no upper bound on m, satisfying the shared-marginal, route-independence, and same-gate replay contracts in section 2. Write A,B for its two face-absence probabilities at (t,1),(1,t), Q for its fresh diagonal absence at (t,t), and J for the joint absence in a paired replay of those two faces.

**Uniform four-coordinate certificate.** If

    max(|A-A0|, |B-B0|, |Q-Q0|, |J-J0|) <= epsilon_n,

then m=n. In particular every wrong-count alternative in the stated class has at least one discrepancy strictly exceeding epsilon_n. This is a single explicit rational radius, uniform over all positive integer counts and all allowed heterogeneous within-route laws. Errors in all four probabilities are allowed at once.

**Bounded-sample reference test.** For any 0<alpha<1, take

    N >= ceil[2 epsilon_n^(-2) log(8/alpha)]
      = ceil[200000000 (n+1)^4 log(8/alpha)].

Use N independent same-gate replay pairs to estimate A,B,J and N independent fresh diagonal trials to estimate Q, with the same fixed distribution and calibration laws in the two batches. Accept the specified reference vector only if all four empirical probabilities are within epsilon_n/2 of its four coordinates. Then:

- At the exact reference vector, acceptance probability is at least 1-alpha.
- At every wrong-count alternative satisfying the contracts, acceptance probability is at most alpha, uniformly over unbounded m.

This is a test of a given reference vector against the wrong-count class. It is not a total count estimator for every dependent-gate model: a model with m=n but a different response vector can be rejected. Acceptance does not establish global gate independence or validate the model assumptions. The stated sample bound is deliberately very conservative and makes no practical-efficiency or optimality claim.

## 2. Observation and sampling contracts

The reference contains n mutually independent AB route occurrences with independent A/B gates and known true rates a,b. An alternative contains a fixed finite integer m of mutually independent route pairs. Different routes may have different A/B dependence laws, but every route shares the same coordinate-only A marginal calibration and the same coordinate-only B marginal calibration. Both calibrations preserve endpoints.

At the tested command t, each route has a valid joint Bernoulli pair (A_j(t),B_j(t)). The very same pair law must underlie the fresh diagonal observation and paired replay. Within a replay, probes (t,1) and (1,t) reuse the same realized gate pair, with no state mutation or redrawing between them. Retaining only the inventory or marginal laws is insufficient. Fixed threshold pairs with command-independent laws supply the required semantics.

The finite command t is a true reference-rate coordinate. Operational use requires known/selectable calibrated commands realizing a=b=t. Under arbitrary unknown nominal homeomorphisms this remains a latent-coordinate statement, not an automatic command-selection or calibration-inversion procedure.

For the finite-sample result, the route-pair vector is independently drawn afresh between experimental replicates from one fixed law. The same law, route count, calibrations, and per-route couplings apply in the replay and diagonal batches. Within a replay pair the latent vector is retained. The simplest design takes the two batches independently as well. Independence among A-absence, B-absence, and joint-absence indicators within one replay pair is neither true in general nor assumed.

No route-specific marginal calibrations, dependence between distinct routes, random inventories, selection-biased samples, drifting distributions, or replacement of same-gate replay by fresh redraws are covered. The frozen SHARED_MARGINAL_BOUNDARY.md gives a concrete wrong-count alias if common marginals are dropped.

## 3. Common reduction and a safe neighborhood

For a candidate count m, the two face observations and common marginals force

    p=A^(1/m),   q=B^(1/m),
    u=1-p,      v=1-q.

Let x_j be the route's joint success probability at (t,t). Set

    y_j=1-x_j,
    z_j=1-u-v+x_j,
    s=1-u-v=p+q-1.

Valid tables and mutual route independence give

    Q=product_j y_j,
    J=product_j z_j,
    y_j+z_j=p+q.

Elementary Bernoulli bounds at the reference give

    A0=B0 >= 1-nt >= 2/3,
    Q0 >= 1-nt^2 >= 35/36,
    J0=A0^2 >= 4/9.

For Q0, use n/(n+1)^2<=1/4. Since epsilon_n<=1/40000<1/12, every probability vector in the stated box, and every line segment to its center, has A,B>1/2 and all four coordinates >1/3. All coordinates remain in [0,1] because the objects under comparison are probabilities.

For m>=2, roots of A,B satisfy p>=sqrt(A), q>=sqrt(B), so

    0 < sqrt(2)-1 < s <= 1.

This verifies the positivity needed below uniformly in m.

## 4. Every larger count remains excluded under all four errors

Assume m>n, hence m>=2. Put w=1-Q. Since x_j>=0 and product_j(1-x_j)=Q,

    sum_j x_j >= 1-Q=w.

Expanding with s>0 gives the necessary lower bound

    J=product_j(s+x_j)
      >= s^m+(1-Q)s^(m-1)
       = F_m(A,B,Q).

### 4.1 Uniform reference gap

At A=A0, B=B0, Q=Q0, the exact-certificate proof supplies

    F_m(A0,B0,Q0) >= (1+delta_n)J0,

where

    delta_n = n(n^2+7n+4)
              / [(n+1)(9(n+1)^2+n)(3n+2)^2].

This is a bound on F_m itself, not merely an inferred gap in a hypothetical J. To see its origin directly, let c=n/m, p0=(1-t)^c, u0=1-p0, d=u0/p0, and s0=1-2u0. The exact proof gives

    F_m(A0,B0,Q0)/J0
       = (1-d^2)^m[1+(1-Q0)/s0]
      >= (1-A_*)(1+W)
       = 1+delta_n,

with

    A_* = n^2/[(n+1)(3n+2)^2],
    W   = n/[9(n+1)^2+n].

Here c<=n/(n+1), d<=ct/(1-t), integer Bernoulli's inequality, and 1-Q0>=W supply the bound, with positive factors. No differentiability of the calibration maps is involved.

Write k=n+1. Since n^2+7n+4>=k^2, 9k^2+n<=10k^2, and (3n+2)^2<=9k^2,

    delta_n >= n/(90k^3) >= 1/(180k^2).

Consequently the baseline residual satisfies

    F_m(A0,B0,Q0)-J0 >= delta_n J0 >= 1/(405k^2).

### 4.2 Uniform derivative bounds

Only the explicit function F_m is differentiated. Its derivative with respect to A is

    partial_A F_m
      = A^(1/m-1)
        [s^(m-1)+(1-Q)(1-1/m)s^(m-2)].

On the safe neighborhood, A>=1/2, 0<s<=1, 0<=1-Q<=1, and m>=2. Therefore

    0<=partial_A F_m<=4,
    0<=partial_B F_m<=4,
    |partial_Q F_m|=s^(m-1)<=1.

The line-segment mean-value bound gives

    |F_m(A,B,Q)-F_m(A0,B0,Q0)|
      <=4|A-A0|+4|B-B0|+|Q-Q0|.

Allowing the J error as well, the necessary residual F_m-J changes by at most 10 epsilon_n. Thus throughout the box,

    F_m(A,B,Q)-J
      >= [1/405-1/1000]/k^2
       = 119/[81000k^2] > 0.

This contradicts J>=F_m. Every m>n is therefore excluded simultaneously.

## 5. Every smaller count remains excluded under all four errors

This section is vacuous for n=1. Suppose 1<=m<n, and c=n/m>1.

Generalized Holder applied to the y_j,z_j tables gives the necessary inequality

    Q^(1/m)+J^(1/m) <= A^(1/m)+B^(1/m).

Use its scaled residual

    R_m(A,B,Q,J)
      = m[A^(1/m)+B^(1/m)-Q^(1/m)-J^(1/m)] >= 0.

Scaling is useful: the magnitude of each coordinate derivative is

    x^(1/m-1) <= 1/x <= 3

on the safe neighborhood. Hence the four-coordinate perturbation of R_m is at most 12 epsilon_n, with no remaining factor m or 1/m.

### 5.1 Quantitative baseline convexity gap

Put p=1-t, x_plus=1-t^2, x_minus=(1-t)^2. Their midpoint is p and their half-separation is d=t(1-t). For f(x)=x^c on [x_minus,x_plus],

    f''(x)=c(c-1)x^(c-2)
            >= c(c-1)(1-t)^(2n).

Indeed if 1<c<2, then x^(c-2)>=1; if c>=2, use x>=(1-t)^2 and c<=n. Taylor's integral remainder or the elementary strong-convexity bound therefore gives

    x_plus^c+x_minus^c-2p^c
      >= c(c-1)t^2(1-t)^(2n+2).

Multiplying by m and using

    mc(c-1)=n(c-1)>=n/(n-1)>1,
    (1-t)^(n+1)>=(1-(n+1)t)=2/3,

yields

    -R_m(A0,B0,Q0,J0)
      >= t^2(1-t)^(2n+2)
      >= 4/[81k^2].

Throughout the box it follows that

    R_m(A,B,Q,J)
      <= [-4/81+3/2500]/k^2
       = -9757/[202500k^2] < 0.

This contradicts the necessary Holder inequality. Together with section 4 it proves the four-coordinate certificate, including n=1.

## 6. A finite-sample reference test

For replay replicate i, retain its latent vector while probing (t,1) and (1,t). Let X_i,Y_i be the two binary absence indicators and Z_i=X_iY_i. The three means estimate A,B,J. These indicators are dependent within a replicate, which causes no issue: each coordinate separately is an iid Bernoulli sequence across the N independent replicates.

Separately run N independent fresh diagonal trials, with binary absence indicators D_i of mean Q. Define

    hat A = mean(X_i),   hat B = mean(Y_i),
    hat J = mean(Z_i),   hat Q = mean(D_i).

For each coordinate, Hoeffding's Bernoulli inequality gives

    P(|hat p-p|>h) <= 2 exp(-2Nh^2).

Taking h=epsilon_n/2 and a union bound over all four coordinates yields

    P(max_i |hat p_i-p_i|>epsilon_n/2)
      <= 8 exp(-N epsilon_n^2/2) <= alpha

at the stated N. Independence between the four estimators is not required for this union bound.

Accept the specified reference if

    max_i |hat p_i-p0_i| <= epsilon_n/2.

Equivalently, all four reference coordinates must lie in their simultaneous intervals [hat p_i-epsilon_n/2, hat p_i+epsilon_n/2], clipped to [0,1].

At the exact reference, simultaneous estimation accuracy implies acceptance. Under any wrong-count alternative, simultaneous accuracy and acceptance together would imply max_i|p_i-p0_i|<=epsilon_n, contradicting the deterministic certificate. Thus both advertised error statements follow.

The design uses 2N independent latent-vector replicates: N retained-threshold pairs plus N diagonal trials, totaling 3N endpoint-probe evaluations. The very large sufficient bound is an existence guarantee, not a recommended practical sampling budget. The test uses empirical proportions and a known rational tolerance; it requires no exact-probability equality oracle.

A rejection says that the specific reference response vector failed this test. It does not by itself show m!=n, identify another count, diagnose which structural assumption failed, or prove any physical or metaphysical conclusion.

## 7. Scope, sharp boundaries, and attribution

The frozen finite-panel-replay/RESULT.md establishes the exact certificate and the F_m baseline gap. Its reviewed SHARED_MARGINAL_BOUNDARY.md shows that dropping common marginal calibrations permits an exact larger-count alias at this very panel. Its copula perturbation preserves all panel observations while changing unseen dependence; allowing a positive error box does not cure that nonidentifiability.

The parent proposed the F_m perturbation route, derivative bounds, scaled smaller-count residual, simple 1/[10000(n+1)^2] radius, and simultaneous-estimation design. This work independently checks the inequalities and constants, states the model contracts, and supplies the complete conditional robustness and sampling arguments. Standard Holder, convexity, Bernoulli, and Hoeffding inequalities are not claimed as novel.

The conclusion is reference-model separation of wrong counts within a declared class. It does not validate shared marginals, mutual route independence, no-mutation replay, stable sampling laws, known calibration, or the existence of productive occurrences. It is neither a universal model test nor an automatically calibrated total count estimator. No empirical intervention, nominal-calibration inversion, global independence certification, protected integration, T20 closure, or elapsed research duration is asserted.
