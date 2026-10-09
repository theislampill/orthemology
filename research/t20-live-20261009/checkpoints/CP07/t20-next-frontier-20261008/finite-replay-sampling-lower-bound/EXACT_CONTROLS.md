# Exact and certified-algebraic controls

The retained author run passes 2,043 assertions across 27 families. It uses Python Fraction arithmetic only, 128-step rational root brackets, certified rational logarithm enclosures from the atanh series, and outward 96-bit dyadic rounding to keep interval operations tractable. No floating-point comparisons, empirical sampling or Monte Carlo simulation support any assertion.

Forty-two actual Joe instances, n=1,...,40,64,100, check:

- The face bounds and reference-cell floor, full-support alternative pair and matching fresh/face defining powers.
- Strict positive concavity and replay gaps, the Taylor remainder bound, difference-of-powers bound and Delta<=4/[25(n+1)^2].
- Certified actual KL intervals, their chi-squared upper bound and the stated uniform constant 3136/[625(n+1)^4].

Six rational alpha values check the binary-KL closed form and the explicit small-alpha logarithmic lower comparison.

Three finite adaptive prefix trees use a labeled rational full-support surrogate pair to test information bookkeeping exactly. Common action kernels and fresh endpoint draws cancel in every path likelihood ratio; expected pair-outcome coefficients equal the Joe-surrogate expected pair count times its pair probabilities. Certified event KL satisfies data processing. These surrogate controls do not replace the actual Joe proof; their purpose is to check adaptive allocation and cost orientation without pretending the irrational hard-pair law is rational.

Further controls verify the no-information fair-guess boundary and that nontermination cannot be counted as terminal correctness. The general potentially infinite stopping proof is analytic, using finite-prefix events and monotone convergence; finitely many trees do not certify an arbitrary policy.

The result JSON retains outward-rounded exact rational enclosures, selected probabilities and named assertions. Finite controls are diagnostics, not proofs for every n, every alpha or every stopping rule. The direct proofs are in RESULT.md.
