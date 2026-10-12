# Explicit polynomial scale independent audit

This review concerns freeze-explicit-scale-v1, author manifest SHA256 e277c93ba09fe5f83e0cf1253a9040ea77496e107da27e658f248aaa1334dedd. PASS_SCOPED. All 11 frozen modules and the independent numeric/readback module passed; four source mutations were rejected. Accepted logs contain no error, sorryAx or PANIC. Final status is recorded in RESULT.json. All earlier seals remain separate and unchanged.

## What this successor closes

The four-coordinate polynomial AND example now has a defined arithmetic radius in its kernel endpoint, rather than only an existential radius obtained from continuity. The exact radius is

    delta = 1/[1 + sum_j 2*(B_j+1)/H_j].

There are exactly twenty rows: four normalized quadratic gains, four normalized nonlinear gains, four candidate barycentric weights, four baseline coordinates, and four complementary baseline coordinates. Each has an exact identity H_j+epsilon*R_j(epsilon), with H_j>0 and a proved coefficient bound |R_j|<=B_j on [0,1].

This is a new conservative explicit formula. It is not silently equated with the earlier ordinary minimum-of-four-bounds formula. The mixed-rank successor still has its own existential radius.

## Literal argument and actual constraints

PolynomialBounds proves the sum-of-absolute-coefficients bound and binds the coefficient arrays to the actual polynomial remainders in both score gains. Barycentric remainders are bounded by |linear coefficient|+|quadratic coefficient|, and baseline remainders by the absolute direction coordinate.

ConstraintBounds proves positivity of delta, delta<=1 and the strict inequality delta<H_j/[2(B_j+1)] for every row. The added one in B_j+1 avoids a zero denominator even for a zero remainder budget. The outer one makes the inverse denominator strictly larger than each summand. These statements also handle empty or singleton generic finite index types correctly; the application has twenty rows.

For 0<epsilon<delta, the finite-family theorem makes every actual normalized constraint positive. Multiplying the first eight by epsilon squared recovers strict actual score gains. Positive barycentric weights give literal hull membership; their inequalities additionally force the output itself into the open cube. The baseline is in the open cube from its own eight constraints.

The final intrinsic-interior wrapper quantifies over every real coherent interior context and every transverse direction. Its scale is the specific Data.delta expression. It concludes open-cube membership of both forecasts, candidate membership in the actual four-vertex hull and both true Bregman comparisons at all four truths. Candidate intrinsicInterior membership is not a separately exposed conclusion.

The validity assumptions are essential. The formula is defined on all Data values in Lean's total real arithmetic, but the positive-radius and strict-repair guarantees require the explicit valid context and nonzero transverse variance. It is not an unguarded procedure for invalid contexts or tangent disturbances.

## Quantitative binding and tests

The independent exact-rational evaluator recomputes all twenty heads, budgets, remainders and actual constraints. Across 558 parameter/direction configurations it verifies the strict radius bounds, 44,640 remainder-budget checks and 11,160 exact constraint identities. At epsilon=0.999*delta every constraint is positive, the candidate is in the actual hull and both forecasts are in the open cube. Near-boundary contexts, tiny transverse components and large tangent components are included.

At the rational context s=1/4, z=w=1/2 and direction (1,0,0,0), the evaluator obtains

    delta = 31562496/25265441833.

An independent Lean fixture evaluates the literal Data.delta to that same rational. This is a concrete source/formula cross-check; it is not a universal compiler or Python semantic-refinement claim.

Four source mutations test omission of coefficient absolute values, multiplication by the head instead of division in the radius, an incorrect quadratic score-remainder coefficient, and an incorrect barycentric quadratic coefficient. Independent exact controls exhibit why a signed coefficient sum or inverted head scaling is unsound. Mutation proof failures are retained separately from accepted proof logs.

## Formal and computational scope

The accepted closure is independently replayed under pinned Lean 4.19.0 and clean Mathlib c44e0c8ee63ca166450922a373c7409c5d26b00b, with no author oleans on LEAN_PATH. Passing logs must have no error, sorryAx or PANIC. Actual theorem types, arithmetic definitions and standard-axiom dependencies are read back.

All formula operations are finite arithmetic and absolute values; on rational inputs the radius is a positive rational expression. The formal function itself is Real-valued in a noncomputable section. This package does not claim an extracted executable Lean rational implementation, runtime efficiency, an optimal radius, or a general effective remainder modulus for arbitrary C3 score generators.

The only auditor-wrapper corrections were explicit normalization of positive rational absolute values and qualification of a library lemma name. Those development logs are labeled and retained. No author-source change was needed, and no PANIC diagnostic is accepted.

This advances the example's constructive quantitative boundary while preserving its fixed truth model, supplied score pair and ordinary/kernel distinctions. It does not authenticate external norms or evidence, classify arbitrary joint truth hulls, or change canonical research state.
