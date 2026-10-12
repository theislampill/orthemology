# Independent review: finite coded mixed transformations

Disposition: PASS for the frozen packet's stated scope. No correctness defect found. This is independent review evidence, not authority to integrate sources or close a larger audit.

Reviewed author: `private-locator:b666aef3749a95964e8c`.
Reviewer: `private-locator:93f779c5ca4388e064bf`.
Candidate: `hase-coded-mixed-transformations-20261010`.
The candidate `validation/INPUT_PINS.json` and `validation/AUTHOR_REPLAY.json` were frozen and remained unchanged. Exact hashes, commands, source/object/log records, and boundaries are in `REVIEW_RECEIPT.json` and `SELECTIVE_REPLAY.json`.

## Evidence

- Independently replayed the 12 selected predecessor modules and all 9 candidate modules, from copies in the review directory, using Lean 4.19.0 with `--trust=0`. All 21 passed without warnings, errors, or `sorryAx`.
- All 4 author false controls rejected again.
- Added 18 source-equation theorems importing only retained `AllSyntax`; these cannot use candidate exactness theorems. All passed by kernel reflexivity.
- Added 16 direct code/environment equations, using definitions and retained codec arithmetic rather than candidate transformation exactness. All passed. This includes an entire `mixedCode` reduction on arbitrary genuine parameter codes in the empty Bottom-default environment.
- Added 10 independently chosen false source equations. Each rejected specifically because reflexivity failed, with no parser/import/identifier failure counted as a rejection.
- Audited all 67 explicitly named candidate helper theorems, not merely the 12 central interfaces in the author's audit. Every dependency axiom was within `propext`, `Classical.choice`, `Quot.sound`.
- Verified all 2,867 candidate pins before and after, plus 5 review boundary pins: the frozen pin file, frozen author receipt, and retained `AllSyntax`, `SubstitutionSyntax`, and `FiniteBridge` sources. All 15 final candidate module/helper/control files appear in the frozen input pins. Source/object binding for the three retained source files agrees with their prior trust-zero prerequisite replay and the current pinned imported objects.
- No broad baseline rebuild, protected source modification, candidate edit, commit, push, publication, or active rule-template inspection occurred.

## Semantic inspection

### Two independent binder sorts

Read the retained `AllSyntax` definitions and the actual TypeCode renaming/substitution definitions in retained `FiniteBridge`, with `SubstitutionSyntax` checked as the direct retained import boundary.

The candidate tracks the actual equations:

- `pi` and `sigma` recurse with the original environment on the domain, and with `pup` on term images plus `wk` on stored type images on the codomain. Free term variables in type images shift; type parameters do not.
- `all` preserves the term environment and performs `tup` on type images: a new parameter zero, `twk` on prior stored images, and the correct updated tail shift.
- The independent crossed-binder witness includes `all`, `pi`, and `sigma` together, a stored type containing both free term variables and a free type parameter, a nontrivial term substitution image, and bound term zero/one. It validates the combined shifts rather than isolated closed examples.
- Finite Bottom-default images and single-instantiation shifted-parameter tails remain different under two nested `all` binders. Empty finite images still produce Bottom beyond the newly bound parameters.

### Realizers and encoding

The natural operations inspect/rebuild the actual retained pairing codec. No replacement source `Encodable`, source `Primcodable`, or arbitrary function-environment computability assumption is introduced. The environment arguments are finite lists plus explicit modes/shifts; ordinary Mathlib primitive recursion/composition gives their primitive-recursive witnesses. The decreasing-code fold filters candidate children and is total on malformed natural inputs; the structural exactness proofs show that all genuine recursive children survive.

`trename` leaves embedded polynomials literally unchanged, lifts only under `all`, and uses the same renaming in both `pi`/`sigma` branches. `twk` is the corresponding successor specialization.

`TypeCode` is handled directly as its own four-constructor datatype. The substitution proof uses actual `upSub`, and instantiation uses actual `singleSub`; nested capture controls validate the type-variable shifts.

`fin` compiles arrow through actual `arr`, namely `pi` with `wk` on the codomain. The direct code-step control preserves this actual constructor equation. Since genuine finite TypeCode translations contain no free term variables, a concrete `fin` output alone would not distinguish omitted weakening; the separate open `arr` witness and false weakening equation supply that discriminating source control. `finSupport` uses maximum at arrow and saturating decrement at every `all`, verified with nested/all-bound and mixed-branch examples.

## Negative controls

Independent false equations reject:

1. A parameter fallback instead of Bottom under nested type binders.
2. Failure to lift polynomial images under `pi`.
3. Failure to weaken open stored type images under `sigma`.
4. Applying term weakening to a stored image under `all`.
5. Lifting polynomial substitution under `all`.
6. Changing term variables during type renaming.
7. Capture of a free TypeCode parameter under two `all` binders.
8. Missing one nested support decrement.
9. Compiling finite arrow with `sigma`.
10. Omitting the term weakening required by actual open `arr`.

These are false source-equation controls; they are not claims of exhaustive mutation testing. Initial review-fixture punctuation errors were corrected before acceptance; the syntax-attempt log is retained and is not proof evidence.

## Accepted scope and remaining boundary

The packet discharges primitive-recursive, exact-on-genuine-input code realizers for finite type renaming, simultaneous finite term/type substitution, type instantiation, Bottom-default type images, actual TypeCode substitution/instantiation, `fin`, and `finSupport`.

It does not establish arbitrary function-environment computability, correctness on every malformed code against the operational decoder, natural-number telescope transport beyond the explicitly stated `List Nat` theorem, a complete Joint/E certificate checker, actual derivability r.e., source adoption, or T20 closure. The separate active rule-template work is outside this review.
