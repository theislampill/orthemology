# Prospective multi-root arbitrary-rate lower-bound candidate

2026-10-08 12:41 UTC. Candidate sent to author for independent derivation; not yet a retained theorem or completed review.

For r>=2 and K>=1, let H0 contain K singleton routes for each of r roots, and H1 additionally contain one full-r support route. Observe only the common effect endpoint under the inherited independent route law. At the full issued profile, choose arbitrary root success rates a_i, write u_i=1-a_i, z=product a_i, q0=product u_i^K, q1=q0(1-z). These are failure probabilities. Proper subprofiles disable the extra full-support route and make the two response laws identical.

For strict interior rates, chi-square domination gives KL(Ber(q0)||Ber(q1)) <= q0*z²/[(1-z)(1-q1)]. Bound 1-z>=u2 and 1-q1>=1-u1^K=a1*sum_(j=0)^(K-1)u1^j. AM–GM bounds the sum below by K*u1^((K-1)/2). Therefore divergence is at most

[u1^((K+1)/2)*a1/K] [u2^(K-1)*a2²] product_(i=3)^r[u_i^K*a_i²]

<= C_r(K) := [2/(K(K+3))]*[4/(K+1)^2]*[4/(K+2)^2]^(r-2).

The elementary maximization bound used here is max u^p(1-u)^s <=(s/(p+s))^s for p>=0,s>0; first factor uses s=1,p=(K+1)/2. For boundary rates, a_i=0 makes z=0 and equal laws; a_i=1 makes q0=q1=0. Hence the uniform bound should hold throughout the cube.

Under a shared adaptive intervention policy, fresh conditional Bernoulli endpoint law and a fixed observation budget N, transcript KL<=N C_r(K), including arbitrary profiles and rates. A correct inventory test at error delta then needs N>=kl(1-delta,delta)/C_r(K), order K^(2r) log(1/delta) for fixed r and delta bounded away from1/2.

The total route budgets are rK and rK+1. Comparison with inherited upper bounds must use that total and verify identical instrument, output and calibration promises. This is not a lower bound for observing individual route/gate states, altered inventory, dependent response laws, unknown r, expected stopping time, or physical/epistemic validation.
