# Exact source-family computability bridge

## Result

The additive `FamilyComputability.lean` proves, without added hypotheses,

- `primrec_encode_inputNumeral : Primrec (fun n => Encodable.encode (inputNumeral n))`
- `primrec_encode_programType (f : PR 2) : Primrec (fun e => Encodable.encode (FullPERTests.programType f e))`
- `computable_encode_programType (f : PR 2) : Computable (fun e => Encodable.encode (FullPERTests.programType f e))`

The encoding is **exactly the existing `EncodedCertificateSyntax.lean` instance**. There is no new source encoding and hence no unstated transport. Public theorem statements mention the actual source syntax. Arithmetic constructor equations are proved by `rfl`; no generated private instance names occur in this work.

`CodeBoundary.lean` then uses the proved computable family map and Mathlib `REPred` preimage closure to show unconditionally:

- `¬ REPred (fun c => ∃ A : Ty, encode A = c ∧ Holds A)`
- `¬ REPred (fun c => ∃ A : Ty, encode A = c ∧ FormE [] A ∧ Holds A)`

Thus semantic non-enumerability now holds on the actual natural-number source codes, including the formed-type restriction.

## Proof mechanism

1. The original numeral is `abstract (abstract (iterationPoly n))`. Its exact unnormalised source syntax obeys `inputNumeral (n+1) = Poly.app numeralStep (inputNumeral n)`, where `numeralStep` is a fixed explicit SKI polynomial. This is a syntactic equality, not semantic conversion.
2. The actual derived app, pi, and identity constructor code equations are exposed and checked against the existing instance.
3. Mathlib primitive recursion builds the actual numeral code from its literal base and fixed constructor step. All remaining operations in `programType` are composition of these primitive-recursive arithmetic constructors and constants. The PR program `f` is fixed; uniform compilation over arbitrary PR syntax is not claimed.
4. The semantic boundary uses the exact injectivity of `Encodable.encode` and the retained actual `exists_non_re_formed_family`, so no source-syntax `Primcodable` instance is assumed.

## Scope and remaining dependency

This closes the **actual source family map** obligation. It does not prove the actual certificate checker or decoder Mathlib-computable, does not infer r.e. from executable Lean or Encodable, and does not establish source derivability r.e. That checker bridge remains the next dependency before semantic-versus-syntactic incompleteness may be concluded by this route. No conditional checker theorem is substituted for it.

The source codec is a retained dependency from the active, now representation-stable codec packet; this increment does not certify that entire packet or assume that packet has completed independent review. No existing source, codec, or frozen core was edited. No adoption, integration, or T20 closure is claimed.

## Verification

Run `python hase-source-family-computability-20261010/verify.py` from the workspace. It checks pinned retained inputs and all imported objects before and after replay, then compiles four selected new modules into a fresh directory with Lean 4.19.0 `--trust=0`. It does not rebuild the full baseline.

Positive controls cover numeral bases and two exact successors; distinct numeral-0/numeral-1 codes; distinct actual programType codes at machine indices 0 and 1 for every fixed f; and app-versus-Pi constructor-tag discrimination. Two intentionally false files must fail: a changed app tag and a changed numeral-step constructor.

`FamilyAudit.lean` checks the central theorem dependencies against the allowlist `propext`, `Classical.choice`, `Quot.sound`; no custom axiom or `sorryAx` is allowed. It also checks the arithmetic executable definitions have no unsafe or partial dependencies. This is distinct from, and does not replace, the proved Mathlib `Primrec`/`Computable` statements.

## Preserved diagnostics

`diagnostics/FamilyComputability.01.lean` and `.log` retain the first failed attempt: unresolved dotted constructor types and attempts to use definitional reduction through well-founded bracket abstraction. The corrected proof names the constructors and uses the retained abstraction equations.

`diagnostics/CodeBoundary.01.lean` and `.log` retain the first semantic-boundary attempt: field notation chose `Partrec.of_eq`, which requests equality of partial computations, instead of `REPred.of_eq`, which transports predicate equivalence. The fix explicitly names `REPred.of_eq`.

`diagnostics/Inspect.lean` and `.log` retain the inspection attempt, including the incorrect namespace guesses `Primrec.natPair` and `Primrec.computable`; actual public APIs are `Primrec₂.natPair` and `Primrec.to_comp`. All failures and the intentional negative controls remain additive evidence.
