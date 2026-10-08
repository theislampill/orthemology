# T20 exact HasE scalar-fusion reduction

The unchanged literal HasE identity between compiled `x` and compiled `x+0` remains **OPEN**. This source-only candidate establishes an exact conditional equivalence, including both constructive directions and fixed proof polynomials. It does not supply an inhabitant of either side.

## Exact statement

Let `p = variableExpr.closed`, `q = redundantExpr.closed`, and `T = N → N`, all from the unchanged inherited compiler. Define

    B = Id_T(p,q)
    W(q) = Πn:N. ∀α. Πf:(α→α). Πa:α. Id_α(n f a,(q n) f a)
    c₃ = abstract (abstract (abstract I)) = K (K (K I)).

The following four propositions are equivalent in the unchanged HasE judgement:

1. Some closed polynomial inhabits B.
2. The literal polynomial I inhabits B.
3. Some closed polynomial inhabits W(q).
4. The literal polynomial c₃ inhabits W(q).

The source uses the exact compiler endpoints. `p = I` is a proved equality of polynomial syntax. The result does not substitute semantic representatives for p or q.

## What each direction does

- Forward: from an existing identity proof, use the actual J motive with the endpoint at coordinate 4 inside the scalar body. Its reflexive base has the exact witness c₃. The original J polynomial contracts to c₃ by the existing K rules.
- Reverse: first work under a local variable `w:W(q)`. Eliminate w at the three term arguments, then apply the original typed piExt/allExt rules. An explicit J step adjusts the literal I-application endpoint. Close over w and only then apply the supplied closed witness. No general HasE weakening theorem is assumed.
- Separate canonicalisation: every already supplied closed HasE identity proof can be replaced by I at the same type and endpoints. All twenty HasE typing constructors are covered by scope/formation arguments. Soundness is used only to recover conversion of the existing proof polynomial to I; no semantic endpoint-reflection rule is added.

This eliminates arbitrary proof-polynomial choice from the selected question. It does not bound typing-derivation search or establish a decision procedure.

## Verification scope

Four new modules, three expanded statement/motive/canonicalisation contracts and all 77 declarations (56 theorems and 21 definitions) passed fresh Lean 4.19.0 checks with `--trust=0`. The axiom union is `propext` and `Quot.sound`.

Five deliberate type-mismatch controls reject dropping the fusion premise, changing an endpoint, replacing HasE by current Has, replacing c₃ by a two-abstraction witness, and feeding semantic validity to the canonicalisation theorem. These are interface controls, not noninhabitation results. Two original RED contracts separately reject the absent new declarations.

Independent review passed for this exact conditional result, including twelve additional reviewer examples and direct source/object provenance checks. Details are summarised in `REVIEW_SUMMARY.md`. The original identity remains OPEN. No full generic Church parametricity, graph projection-fusion theorem, modified calculus or compiler, or HasC-to-HasE inclusion is asserted.

## Portable replay

Inputs:

- The unchanged `Sixteenth_Orthemology_Proof_Source_Recovered_v1` package bound by `PREDECESSOR_CLOSURE.json`.
- Official Lean 4.19.0 Linux x86_64, commit `6caaee842e9495688c1567e78c0e68dbb96942aa`.
- The exact nine dependency revisions in `lake-manifest.json`, prepared with the official pinned Mathlib cache for the four roots listed in `PREDECESSOR_CLOSURE.json`. Prepared object identities are in `DEPENDENCY_OBJECTS.json`; this is not a Mathlib source cold build.
- Python 3, Git, and a fresh output directory outside all inputs.

Run:

    python3 replay.py --predecessor PREDECESSOR --lean LEAN_EXECUTABLE --dependencies DEPENDENCY_DIRECTORY --output NEW_OUTPUT

The fixed-scope recipe checks all supplied identities, freshly compiles the 82 required inherited source modules as dependencies, compiles the four new modules, and runs the expanded contracts, all-declaration audit and intended rejections. It performs no installation or network access, and does not run old control suites. Old T16 scientific replay registry status remains NOT_RUN.

Only source, contracts, dependency/source hashes and this portable recipe are included. Original owner-private provisioning/execution receipts, absolute execution paths, toolchains, caches and compiled objects are kept separately.
