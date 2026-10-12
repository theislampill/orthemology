# Explicit arithmetic scale for the polynomial AND repair

2026-10-01. A bounded quantitative refinement of the four-coordinate polynomial AND theorem. The mixed rank-one/rank-three theorem retains its separately stated existential scale.

## What is defined

For a valid context/direction, collect twenty scalar constraints:

- The four normalized quadratic score gains
- The four normalized nonlinear score gains
- The four candidate barycentric coordinates
- The four baseline coordinates
- One minus each of the four baseline coordinates

Each constraint has the exact form H_j+epsilon R_j(epsilon), where H_j>0. The score constraints multiply this expression by epsilon² to recover the actual score gains. Each remainder has an explicitly proved bound |R_j(epsilon)|≤B_j on0≤epsilon≤1. For score remainders B_j is the sum of absolute values of the actual polynomial coefficients; the barycentric and baseline bounds are similarly finite arithmetic expressions.

Define the single radius

    delta = 1 / [1 + Σ_(j=1..20) 2(B_j+1)/H_j].

The kernel proves delta>0, delta≤1, and delta<H_j/[2(B_j+1)] for every constraint. Consequently every0<epsilon<delta makes all twenty constraints positive.

## Actual conclusion

ExplicitANDScale.intrinsic_explicit_strict_repair accepts a point in the literal intrinsicInterior of the actual four-vertex AND hull and a transverse direction. Its radius is the defined arithmetic function above, rather than an existential choice obtained from continuity. It proves for every real scale in that interval:

1. The baseline is in the open forecast cube
2. The explicit candidate is in the actual convex hull
3. The candidate is also in the open forecast cube
4. Both genuine derivative-based Bregman scores strictly improve at all four truth states

The candidate and score functions are exactly those of the already sealed polynomial construction. No new norm family, truth model, installation or canonical adoption is introduced. With rational context and direction coordinates the radius is a positive rational expression, because its definition uses only finite arithmetic and absolute values. No efficiency or optimal-radius claim is made.

## Formal closure and limits

The additional modules are PolynomialBounds, ConstraintBounds, ExplicitANDScale and ScaleReadback. The original polynomial source closure supplies the actual gain identities, positive leading terms, gradient bindings and hull interface. All coefficient bounds and the finite-family radius argument are proved in Lean.

This is a computable conservative scale for this explicit polynomial example. It is not a general effective remainder modulus for arbitrary C³ generators, nor a formalization of the general optimized-regret asymptotic. The candidate conclusion is hull membership plus open-cube membership; literal intrinsicInterior membership of the candidate is not a separately exposed conclusion.

An initial development run triggered diagnostics from Lean4.19's default definitional simplifier while still producing a checked theorem. Those diagnostics were not accepted as a clean return: the affected tactic calls were replaced by direct polynomial identities, and the final replay gate rejects PANIC diagnostics in addition to errors and sorryAx. The preserved earlier seals were not edited.
