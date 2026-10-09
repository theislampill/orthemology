# Prospective finite interaction panel and integer recovery

8 October 2026, 14:06 UTC. Sent for adversarial verification; not yet a reviewed theorem.

For H_c(z)=1-(1-z)^c, c>0, define E_c(z)=z H'_c(z)/H_c(z). Put u=1-z. Differentiating log E_c with respect to u yields a positive denominator times u^c-1-c(u-1). Strict convexity/concavity of u^c makes this sign positive for c>1 and negative for0<c<1. Therefore g(s)=log H_c(exp s) has second derivative sign1-c. On a strictly ordered interior2x2 product grid, the cross difference of log H_c(a_i b_j) has that same strict sign. Consequently det[H_c(a_i b_j)] has sign1-c; it vanishes only at c=1.

Given isolated interaction values Z_ij=(1-a_i b_j)^n for a promised positive integer multiplicityn, candidate m>0 yields matrix[1-Z_ij^(1/m)]=[H_(n/m)(a_i b_j)]. Its determinant sign is sign(m-n). Thus a nondegenerate finite exact panel identifiesn even though its individual calibration factors still have reciprocal-scaling ambiguity.

Potential approximate-oracle algorithm: compare only at half-integer candidate cuts m=k+1/2, never equal to integern. Each determinant is then nonzero, so refining valid Cauchy intervals eventually determines its sign. Doubling upper cuts untilpositive, then binarysearching the integer interval, recoversn after finitely many sign decisions without a real-equality test. This is a computability claim to check, not a fixed-noise or uniform finite-sample guarantee. A promised positive interaction and the exact model are essential; no procedure for deciding absence n=0 is supplied. Raw log-mask transforms must stay away from log0, and finite roots/calibrations must be strictly ordered inside the interval.
