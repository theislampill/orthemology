# P1: exact expression-stack and meter correspondence


## Fixed source

`source/prcodec.py`, SHA-256 `dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c`, identical to the independent-review literal snapshot.

The core slice is Meter (122–132) and eval_expr (134–159). Dictionary lookup/update are abstracted according to run (161–183); parser and whole-run results remain outside P1.

## Domain and observations

Expressions are finite, well-formed trees using exactly the ten decoded tags, natural-valued constants and register indices, and correct arities. Values and dictionary keys are nonnegative exact built-in Python ints, not bools, subclasses or user objects. Meter limits are None or nonnegative exact built-in ints and starting steps are exact built-in nonnegative Python ints too. The model admits arbitrarily large natural integers; it does not promise physical allocation success.

An expression work item is a pair (expression, ready flag). Work and value stack tops are list heads, reversing Python list-end stack orientation. Binary children execute left then right and reduction pops right then left. Every popped work item ticks before tag dispatch. Leaf constants use the generic bit check; variables do not. Compound entry ticks then schedules children and the ready item. The ready item ticks again. Binary operations check their result after computing it. pow2 checks exponent+1 before the shift and has no generic postcheck. Distinct step-limit, integer-storage, exponent-storage and malformed-stack faults are retained. A separate mathematical transition fuel is never identified with Python meter limits.

Successful execution uses the full syntax-derived pop/tick cost. Resource faults short-circuit earlier: the local runSteps theorem uses that cost as its available transition count, while preserving the actual earlier failure kind and visible count. No remaining work is executed after failure.

## Required universal results

1. Finite dictionary default-zero read and overwrite extensional correspondence to ObserverCore.Store.
2. The exact source-shaped expression machine, on an arbitrary tail of pending work and arbitrary existing values, executes one expression using its recursive tick cost and leaves precisely its value on the old value stack, or returns the same modeled meter fault as the recursive reference.
3. The recursive reference and every successful complete machine evaluation return ObserverCore.evalExpr of the corresponding expression.
4. Successful meter.steps is initial steps plus cost (leaf 1, unary 2+child, binary 2+left+right). No valid expression causes value-stack underflow or final stack-invariant failure.
5. Adequate input-dependent limits give successful evaluation in the ideal no-host-fault model. Any two successful budget settings return the same value; no continued-success monotonicity theorem or uniform fixed budget is promised.
6. Source-shape pinning and a correspondence map cover every inspected branch. Adversarial controls detect reordered operands, skipped ready ticks, checked register reads, an incorrect power guard, and malformed source changes.

## Residual endpoints

A Lean model plus a source/AST checksum is not a verified CPython frontend. Translation from decoded Python tuples, Python built-in integer/list/dictionary primitives, byte parser behavior, generic Python exceptions, allocation/time/OS failure and the CPython execution engine remain explicit trusted or unproved endpoints. No statement-meter, parser, all-invalid-encoding, arbitrary-direct-AST or fixed-resource all-input claim is made. Existing runFuel/callFuel results receive no new credit.

## Finite-budget interpretation

The compositional `neededBits` function takes a recursive maximum of widths at source check sites (and exponent+1 at power prechecks). It returns zero for register reads. The bounds are mathematical witnesses, not a cheap or host-safe preflight procedure: computing them can itself require large ideal arithmetic. A theorem that the ideal model has adequate finite bounds does not promise that a physical Python process can allocate those values or finish before an external timeout.
