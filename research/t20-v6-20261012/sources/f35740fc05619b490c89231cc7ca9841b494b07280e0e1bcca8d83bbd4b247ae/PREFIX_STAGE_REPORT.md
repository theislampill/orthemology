# Independent productive-prefix successor audit

## Disposition and exact object

PASS for the 24 new targets. The finite-prefix evaluator realizes the previously sealed tagged observer pointwise and is jointly primitive recursive under one fixed jointly primitive-recursive matrix premise. No hidden future-input dependency or off-by-one defect was found.

Archive: `private-locator:04c1a32aa15eb8ce9d4b`

SHA256: `f9a1a33ffd9ad62b711674caed952e26d403dc55084a26faa3bb8285469cfe6d`

Author receipt: `receipts/20260930T154454Z/RESULT.json`

SHA256: `506f25fd9b149b43b15a5f5980a22da6eefbf4cb340270ac7c7c5e5a4c507bda`

The archive was compared with every sealed-v2 file. All 23 prior source hashes matched the prior independent tagged audit and were not rebuilt or recounted. Only PrefixBits, FiniteSelector, SelectorPrimrec, PrefixObserver, PrefixPrimrec and PrefixControls were rebuilt, followed by a generated audit restricted to the 24 new names. Fresh outputs reside in `prefix-build`; imports use that directory, the already independently rebuilt tagged dependencies, and the exact pinned official Mathlib/package caches.

`audit_prefix.py`, `prefix-audit.log`, `prefix-receipts/` and `PREFIX_STAGE_AUDIT_RESULT.json` record the work. Seven build commands returned exit 0, using Lean 4.19.0 commit `6caaee842e94`, `-j1`, and Mathlib `c44e0c8ee63ca166450922a373c7409c5d26b00b`. Every one of the 24 axiom readbacks lies within `{propext, Classical.choice, Quot.sound}`. Three independently added boundary/causality endpoints also compiled within that ceiling.

## Sentinel bit extraction and bounded selection

`readBit n word j` uses `word / 2^(n−j) % 2`. The correctness theorem explicitly assumes `j≤n` and an actual sentinel encoding of n+1 input bits. It does not make a false statement about a position beyond the given prefix. The proof peels the last bit using the sentinel append identity, with a separate endpoint case `j=n`.

`scannedBits` has exactly n+1 coordinates. `selector` is finite-list findIdx for the first false bit. If that first false lies at i≤n, selector returns i; if it has not yet appeared, selector returns n+1. The same finite result holds on allTrue for every n. There is no unbounded search in this implementation.

The PR proof uses arithmetic closure, finite list generation/map and list findIdx. It is a theorem of joint primitive recursiveness in the finite inputs, not a claim about primitive recursion of an arbitrary universal program interpreter.

## Actual output and index arithmetic

`pi3PrefixValue` first computes i from the supplied prefix. If `n≤i`, it echoes the current bit. This covers the all-true prefix, the part strictly before the delimiter, and the delimiter itself. Once `i<n`, it uses row stage `n−i−1` and copies the current bit only on that row's innovation.

The proof of `pi3PrefixValue_output` considers three distinct positions relative to a finite first zero: n<i, n=i, and i<n. In the tail case it establishes `i+1+(n−i−1)=n`, so the row's fresh tail bit is the actual current source coordinate. The allTrue input is handled separately and pointwise. Equality with the infinite semantic tagged observer therefore holds on every source stream, including the measure-zero branch.

The zero-defect equivalence follows by rewriting this exact output-map equality into the earlier actual-law theorem. It is not obtained by substituting an unconnected abstract mixture.

## Joint PR premise

The theorem requires a Primcodable parameter type and a fixed matrix family that is jointly primitive recursive in parameter, row, candidate and test. Primitive-recursive selection, the truncated tail-stage arithmetic, and the earlier jointly PR innovation function are composed explicitly. The result is jointly PR in parameter, stage and finite word.

This premise is substantive: decidability alone suffices for the semantic pointwise output theorem, but does not by itself establish joint primitive recursiveness. The source preserves that distinction.

## Controls and independent boundary evidence

The eight supplied controls are positive kernel-checked examples, not eight expected-failure compilation tests. They cover first/no/middle/last zero selection, a good row suppressing a bit, a bad row copying it, a true matrix with zero defect, and a split matrix with positive defect. All eight reproduced.

`prefix-sources/PrefixBoundaryWitnesses.lean` adds:

- `wrong_tail_stage_changes_first_bit`: using row stage n−i instead of n−i−1 changes the first tail output for a matrix with witness s=1; correct output is 1, incorrect output 0
- `no_future_input_use`: for all matrices and all source pairs agreeing through n, the actual semantic tagged observer's output at n agrees, derived pointwise through the finite-prefix realization
- `boundary_before_and_at`: an all-true one-bit prefix and a two-bit prefix ending in its first zero exercise the no-selector/at-selector boundary

These compiled with fresh prefix outputs and no additional axioms. The negative variant is an explicit countermodel, not a mutation to the sealed source.

## Exclusions

The six modules define and qualify a numeric finite-prefix function. They do not compile this Pi3 construction into the recovered LOOP AST, certify Python resource-meter acceptance, prove the byte/numeric codec, construct an effective index-map theorem, or prove PR completeness or hierarchy hardness. The prior Sigma2 AST compiler is a distinct result and cannot be silently applied as a proof of the complete tagged Pi3 AST compiler.
