# Actual Rule code maps and templates

This additive layer proves actual primitive-recursive realizers of all 63 retained
Rule constructors, against the unchanged derived Encodable representation.

- `RuleConclusionCode`: `conclusionCode : Nat → Nat`, `primrec_conclusionCode`,
  `conclusionCode_exact r : conclusionCode (encode r) = encode r.conclusion`.
- `RulePremisesCode`: `premisesCode : Nat → List Nat`, `primrec_premisesCode`,
  `premisesCode_exact r : premisesCode (encode r) = r.premises.map encode`.
- `RuleSideCode`: `checkSideCode : Nat → Bool`, `primrec_checkSideCode`,
  `checkSideCode_exact r : checkSideCode (encode r) = r.checkSide`.

All names are in `CodedRuleTemplates`. Side conditions instantiate the actual
proved finite, polynomial, lookup, Scoped and TyScoped realizers. There are no
checker-computability parameters and no source Primcodable assumption.

`PolyTemplates` and `TypeTemplates` provide exact arithmetic code realizers for
pairing, projections, J, sigma branch operations, motive/theta substitution,
dependent-step families and the full dependent-induction section combinator.
`RuleCodeBasics` uses the proved standard ListNat encoding transport for telescopes
and preserves every supplied finite-rule type image in its original order,
including entries unused by the finite type. `finite_premises_order` and
`finite_premises_length` assert this preservation for arbitrary finite rules.

The generator reads the retained `generated_rule_metadata.json`; each generated
constructor equation is separately kernel checked against `Rule.conclusion`,
`Rule.premises`, or `Rule.checkSide`. Thus parser/generator correctness is not a
logical assumption. Every branch also has a separate primitive-recursion proof.

## Replay

From `private-locator:8f24556a330b05a11a95`:

```
python hase-coded-rule-templates-20261010/verify.py
```

The verifier checks frozen inputs, regenerates the three map modules into a fresh
additive directory and compares bytes, freshly compiles the selected dependency
cone with Lean 4.19 `--trust=0`, checks runtime/axiom audits and requires six false
semantic controls to reject. It checks all pins again and emits a fresh receipt.
No retained baseline rebuild or protected-source change is performed.
`validation/CORE_SOURCE_FREEZE.json` preserves the first compiled source layer;
`validation/INPUT_PINS.json` and `AUTHOR_REPLAY.json` identify the complete replay.
Failed elaboration and parser attempts remain in `diagnostics`.

## Boundary

These are total arithmetic functions, exact on actual Rule encodings. Arbitrary
malformed codes are not claimed to match the operational decoder or validate
syntax. A canonical Rule validator and the recursive certificate-tree check are
separate requirements. This package alone does not prove source derivability r.e.,
semantic completeness, integration, or T20 closure.
