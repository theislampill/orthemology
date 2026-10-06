# Independent source correspondence review

Accepted against P1_v3 after exact manifest verification and fresh source-bound Lean checks. See ACCEPTANCE.md and REVIEW_RECEIPT.json for the accepted scope and evidence identities.

## Domain

The admission condition must describe finite immutable correctly aritied tuples, natural exact built-in integer constants and register indices, exact built-in natural-key/natural-value dictionaries, None/nonnegative exact-integer budgets, and a nonnegative exact-integer starting count. It is a theorem precondition; Python's `eval_expr` and `Meter` do not validate it. Both bool and int subclasses are excluded, as are callbacks/custom dictionaries and concurrent mutation. Ordinary Python tuples may contain malformed nodes even when enclosed in a `Program`; `Program.__post_init__` does not certify the body.

## Rule-by-rule findings

- Meter tick increments the mutable count first, then compares strictly greater than the limit. The model stores the incremented count even on failure. A start already above its limit fails at start+1, not at start.
- The width test uses natural bit length. Zero has width zero. The generic width check appears only at constants and binary results; variables bypass it. Finite dictionary default-zero lookup and overwrite are modeled extensionally; insertion order and duplicate list representations are intentionally unobserved.
- Work-list heads correspond to Python list ends. Children are pushed in reversed order, producing left-before-right execution. Ready visits still tick. Leaves ignore the ready flag, matching Python's dispatch before `if not ready`.
- Binary ready reduction pops right then left and passes left/right to the operator. Natural subtraction models `max(0,a-b)`. Division by zero returns zero; modulo by zero returns the numerator. Comparisons return 0 or 1.
- Binary arithmetic runs before generic width checking. This is materially different from a host-safe preallocation guard; MemoryError or similar host exceptions may occur earlier than the modeled rejection.
- Power pops one value, checks exponent+1 against max_bits before shifting, and raises the distinct exponent-storage error. It has no generic postcheck. Natural power result width is exponent+1.
- The universal local theorem quantifies arbitrary pending work and preexisting values. Exactly syntax-cost work pops stop before touching the pending tail. Failure equality keeps category/count, not merely assert unsuccessful execution.
- The final wrapper inspects an empty pending work list and singleton values; Python itself exits when its work list is empty, then checks singleton values. The local theorem establishes the relevant exit correspondence on valid expression inputs. The model's additional work-list test is harmless on that domain.
- Empty-work step stuttering is a mathematical fuel convenience; source execution has already exited. The local theorem chooses exactly the source pop count before any such stuttering, so no additional source tick is implied.

## Excluded branches and state

Unknown executable tags, underflow and malformed arities are outside the admitted expression domain. The independent controls separately observe unknown tags with/without children, negative and bool literals, extra/missing children, and negative shifts. They demonstrate why a universal claim about arbitrary Python direct ASTs would be false, rather than extending the accepted theorem. Work/value list contents at exception time are not exposed by eval_expr and are not part of the modeled observation; fault category and meter count are.

No initial argument, loop-index write or final output lookup width invariant is inferred. No parser/serializer, statement runner, wrapper/trace return shape, invalid syntax, or host-exception correctness theorem is obtained. The source hash and Python AST fingerprints pin control flow but do not verify an extraction frontend. Built-in arithmetic, tuple/list/dictionary semantics, the Python engine and physical resources remain residual endpoints.

## Independent finite evidence

The independent oracle is recursive, whereas the source algorithm is iterative. Across 266,760 exact-source cases, all return values, modeled error messages and visible meter counts agree. Boundary-instrumented source behavior preserves 1,593 arbitrary existing-stack/pending-tail examples. All 28 executable lines reachable on admitted inputs are observed, including both zero-divisor branches and width/step error boundaries. Eighteen independent source mutants are distinguishable by fixed witnesses; the malformed-tuple tick-before-tag witness is explicitly outside the formal input domain and used solely to pin source order.

This is finite corroboration. It is not a machine-checked Python frontend or a universal Python/Lean relation.
