# Preparation-side proof and check notes

These are review notes, not an independent referee report.

## Corrections that matter to the claims

- State correspondence and output correctness are separate obligations. The revised exact continuation theorem carries both; a state-correct implementation with an inverted display is not accepted.
- A change of coordinates preserves the formal transition correspondence but need not be a physically available or cheap transformation.
- Behavioural equivalence obtained through retraining is not automatically migration of an existing execution. Current state, order and effects still require a transfer argument.
- The export obstruction ranges over complete exported information. An uncounted side channel, decoder memory or prior correlated receiver state changes its premise.
- Packing applies to a finite-dimensional Euclidean encoding with full bounded observation balls. It does not compare arbitrary analogue and digital capacities by raw parameter count.
- The trace-TV bound requires conditional closeness on every common history, not just average benchmark accuracy.
- The bistable witness uses a controlled sign reset and a specified relaxation equation. Neither is inferred from “fluidic,” “analogue” or the published bubble apparatus. A physical finite-duration reset must justify the sampled map.
- A positive inward-flow margin establishes the model's invariant regions. The readout is restricted to settled times; no unmodelled switching-transient guarantee is asserted.
- Pure migration uses the identity reference, with Lipschitz bound one. A contraction bound for a compute step cannot silently be applied to migration.
- The zero-failure result bounds the chance of a false acceptance across a fixed test family. It is not posterior probability, not an adaptive-test guarantee, and not evidence that physical trials occurred.

## Numerical harness repair during preparation

An initial Edition 3 run passed 41/42 checks. The finite-trace TV test used a chained floating-point comparison that added the tolerance to both adjacent quantities, causing harmless rounding in the product/union-bound comparison to fail. The root cause was reproduced at the one-step boundary. The check was corrected to compare the two mathematical inequalities separately, each with an explicit numerical tolerance. No theorem premise or expected mathematical result was weakened. Subsequent complete ordinary and optimised runs passed 42/42, including fresh runs from the released package files.

## Layout review repairs

The contents page was compacted without changing body text size; two inherited appendix page breaks and an oversized keep-space request were removed to avoid near-empty pages. Ragged-right cells replaced problematic justified narrow-table cells. The final 58-page version was re-rendered and reviewed after those edits.

## Outstanding substantive work

A calibrated physical pair and actual stateful handover; support-removal measurement; a matched held-out study of assessment utility; a method-specific NS transfer with a measured or certified advantage; and external domain review remain outstanding. None is implied by a passing build or finite checker.
