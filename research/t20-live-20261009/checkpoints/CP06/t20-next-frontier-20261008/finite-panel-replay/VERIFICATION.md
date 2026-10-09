# Verification scope

The proof in RESULT.md is the certificate. Each inequality is explicit and uniform in the unknown positive integer m; no numerical scan is used as proof.

An auxiliary exact-arithmetic check may confirm the displayed rational identities for selected positive integers n. Such checks are arithmetic smoke tests only, not empirical validation, exhaustion of an unbounded count range, or an independent proof audit.

Review priorities:

1. Face observations identify the same marginal u for every route only under shared marginal calibration and mutual route independence.
2. Replay must observe the 00 cell of the same A-at-t and B-at-t gate variables.
3. The smaller-count argument uses Holder followed by strict convexity, with the inequality directions as written.
4. In the larger-count argument, the factors multiplied by lower bounds are positive: s>0, 1-A>0, and w>=0.
5. Integrality supplies c<=n/(n+1); the t choice and positive gap do not depend on m.
6. The result concerns an accessible calibrated t or an existential latent-coordinate panel. Unknown nominal commands remain a separate problem.
7. The copula perturbation certifies valid global threshold distributions but refutes global independence certification from this finite panel.
8. The delta_n margin is conditional on three exact equalities; noisy data need a separate joint perturbation analysis.

## Completed arithmetic smoke check

Python Fraction arithmetic checked every integer n=1,...,10000 for the displayed identities

    D=(n^2+7n+4)/[9(n+1)^3],
    (1-A)(1+W)-1=delta_n

at c=n/(n+1), as well as D>0, delta_n>0, and A<1. All checks passed. The symbolic derivation in RESULT.md, rather than this finite range, establishes the general claim.

The author froze RESULT.md for independent review with SHA256

    327b6fb25944ac90e7ecd6010a427993b69400fbdc9b79928d731120b6d62243

No empirical or end-to-end experimental validation was performed.
