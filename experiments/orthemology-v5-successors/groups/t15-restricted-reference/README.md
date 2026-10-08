# Restricted reference interfaces

These finite reference executions are separate from the complete Lean theorem, the written finite-grid proof and the global complexity classifications. No parser or implementation-refinement theorem equates their representations.

**Finite execution evidence:** all three linked reference suites completed with FINITE_ONLY status. Counts below come from the selected fresh receipts and their hash-bound logs or verified runtime output.

| Reference suite | Actual completed checks |
| --- | --- |
| [Strict JSON reference](../../suites/t15-json-reference.json) | 22 test methods and 2 prescribed CLI examples |
| [Univariate reference](../../suites/t15-univariate-reference.json) | 15 test methods |
| [Runtime agreement](../../suites/t15-runtime-agreement.json) | 720 generated pairs; 720 verified Lean rows; 2160 Boolean observations |

The runtime comparison used seed 151005 and arities 0, 1, 2, 3, 4, 5. It observed 546 equal and 174 unequal pairs, 174 checked distinguishing witnesses, and 87360 direct expression evaluations. The Lean observations came from a fresh source closure. These counts do not add independence or establish a parser/refinement theorem.

## Strict canonical structural JSON reference checker

The Python reference validates its exact canonical decoded JSON object schema and implements the mask/coefficient method with separately tested malformed-input and finite-witness behavior.

Decoded Python JSON values follow exact field/order/natural-number restrictions, excluding booleans.

Standard json decoding is not a proved duplicate-key-rejecting parser. No formal serialization/refinement theorem connects the Python representation to the more permissive typed Lean certificate lists.

Exact source: [certificate_checker.py](../../source-store/8f5ba88d07447c8c92d49161f82118f805cae707404b477c81936828103d60ef/certificate_checker.py).

## Finite Python/Lean restricted-runtime agreement

Deterministic finite generated expressions are compared through successful Lean observations and direct Python evaluation; actual generated counts are recorded by the run output.

Exact source checker, generated cases and successful Lean output before verification.

Finite computation, not a universal theorem or implementation-refinement proof. Historical counts and interpreter patch versions are not fresh results.

Exact source: [check_runtime_agreement.py](../../source-store/dd69712d1a7b79bdb5fcb55c855c4c13a00725dda1cd8f4dfcdc4544afcbe8fd/check_runtime_agreement.py).

## Univariate root-extension reference checker

The separate reference uses exact integer-polynomial tails and root bounds: unequal tails yield a checked witness at their bound, while equal tails require only the finite prefix. This implements the written inclusive 0..M criterion without repeating redundant tail checks.

Exact tagged old/test source representation and source-bound certificate-checker dependency.

No Lean proof of this implementation or arbitrary extension grammar. Resource exhaustion is not an inequality verdict.

Exact source: [root_extension_checker.py](../../source-store/bd796dc6d0157d0b8a125cc3b394a866812567f12ce132ee11d2fa3844e081d9/root_extension_checker.py).

## Complete source-prescribed checks

The canonical JSON reference has ten author and twelve independent test methods. The univariate implementation has eight author and seven independent test methods. Runtime generation requests 120 expression pairs at each arity zero through five; a successful Lean execution must precede verification of its generated observations. Final receipts must use the actual generated case, Boolean-observation, numerical-evaluation and distinguishing-witness counts.

Natural constants and indices are checked structurally; Boolean values are rejected as natural scalars. Lean certificate lists may admit redundant/reordered/split coefficient representations when aggregate equality and every mask are covered. The strict Python decoded-object schema instead requires its canonical representation. Standard JSON decoding and this structural verifier are distinct boundaries.

The univariate root grammar is one old expression or one root equality test of two pure arithmetic expressions. The inclusive finite test 0..M uses integer coefficient aggregation and the exact polynomial-tail construction; it supplies no particular hardness arity at least two. Resource exhaustion remains inconclusive.
