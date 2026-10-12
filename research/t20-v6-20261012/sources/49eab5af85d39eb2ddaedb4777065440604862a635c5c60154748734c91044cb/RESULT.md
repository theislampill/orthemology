# Every closed HasE Church input has an actual source scalar-fusion instance

10 October 2026. **A new source-derivability metatheorem is Lean checked. For every original polynomial n with a supplied derivation `HasE [] n N`, the original fixed polynomial `c3` applied to that same n inhabits the literal substituted body of the frozen `W originalQ`. The universal judgement `HasE [] c3 (W originalQ)` remains OPEN.**

## Exact source result

`ClosedScalarInstances.closed_scalar_instance_exact` proves:

```
{n : Poly} → HasE [] n N →
  HasE [] (.app c3 n)
    (inst (.all (.pi End (.pi A (Leaf FullPER.Application.originalQ)))) n)
```

`FullPER.Application.originalQ` is the original imported `redundantExpr.closed`, the same endpoint named q by the pinned LiteralScalarFusion source. `A`, `End`, `Leaf`, `W`, and `c3` are imported from the unchanged ScalarFusionCore source. Thus the displayed result type is literal substitution into the body of W at the original n, not an evaluated or recompiled replacement.

The intermediate theorem `scalar_identity` constructs

```
HasE [A, End] I (Id_A (n f a) ((originalQ n) f a))
```

with f and a the genuine open source coordinates 1 and 0. `closed_scalar_instance` then abstracts these coordinates and introduces All, obtaining the explicit finite proof polynomial `c2 = abstract² I`. A checked original K conversion changes c2 to the exact application `c3 n`.

## Why the construction is syntactic

1. `reify` maps the open SKI carrier back to actual source Poly: variables are retained; constants become source atoms; application is structural.
2. Induction on open Conv yields actual `PolyConvPlus` in `reify_conv`. The original atom/application bridge proves `reify_embed` and `reify_interp`, so packed source atoms and the entire original n remain present up to the original conversion relation.
3. `generic_conversion_reflect` reflects conversion at the generic variable valuation to source conversion. This is a syntax translation of the same compatible conversion, not a semantic-completeness principle.
4. The new whole-HasE full-PER soundness, inherited source scope, and environment independence for closed n give full Church membership of the generic interpretation of n. The frozen open-term `church_standard` supplies one finite iteration count and conversion on the genuine open f and a.
5. The finite iteration `iterationPoly k` has an elementary inherited Has derivation in `[A, End]`. Actual `HasE.conv` transports that typing to the original `n f a`; a second checked source conversion types `(originalQ n) f a`. Actual identity formation and identity introduction then apply.

Step 5 is important. No general HasE weakening or renaming theorem is assumed, and no Has derivation of arbitrary n is substituted for its supplied HasE derivation. The required open scalar typing is built from the independently typed iteration using a real conversion derivation. The inherited `ClosedProofCanonicalisation.has_scope` applies to all twenty HasE constructors; its existing `formed` theorem supplies result formation. Neither is claimed as new here.

The derivation-valued conclusion is constructive in the precise sense that a finite source derivation is proved to exist for each supplied closed derivation. The surrounding Lean proof uses the ordinary `propext`, `Classical.choice`, and `Quot.sound` axioms already present in the model. No executable proof-extraction algorithm or quantitative bound on the resulting derivation is claimed.

## Nonduplication check

The pinned ScalarFusionCore, ScalarFusionReverse, LiteralScalarFusion, ClosedProofCanonicalisation, EffectiveStandardness, and relevant inherited current-Has pointwise constructions were inspected.

- ScalarFusionCore and ScalarFusionReverse establish the conditional four-way reduction from a supplied function identity or supplied universal scalar witness. Their local scalar argument assumes a variable witness of W. They do not supply the closed-n source identity constructed here.
- ClosedProofCanonicalisation canonicalises the proof polynomial of an already supplied closed identity. It does not turn semantic endpoint agreement into an identity derivation. Its scope and formation lemmas are reused, not recreated or counted as new results.
- EffectiveStandardness plus the inherited unary fundamental theorem already gives observational standardness over the inherited closed raw carrier. That earlier conclusion is not new. It does not itself provide the generic-open PolyConvPlus reflection used here. We claim no logical independence from all conceivable consequences of the inherited calculus.
- Numeral instances are controls only. The final theorem quantifies over arbitrary HasE derivations, including any that use J, proof erasure or typed extensionality.

A transitive Lean dependency audit verifies that the final theorem uses the new full-PER fundamental theorem, open-term church_standard, generic conversion reflection, inherited scope, the original bridge and actual HasE conversion/identity/introduction constructors. It does not depend on inherited F/G, old semantic fundamental/soundness, EffectiveStandardness.semantic_church_standardness, or canonical_identity.

## Exact boundary

The quantifier over n is in the external Lean metatheorem, whose hypothesis is a closed source typing derivation. The construction gives one finite HasE proof for each such n. It does not construct the body under a source variable `n:N`, and no omega-rule turns the family into an outer Pi introduction. Therefore neither the universal `HasE [] c3 (W q)` nor its negation is proved. No source nonderivability, semantic completeness, general parametricity, or programme closure follows.

## Verification and preservation

Lean 4.19.0, `--trust=0`; no added axioms, admitted proofs, unsafe proofs, or evaluator oracles. The main new source and two controls compile cleanly. Reused source prerequisites are hash-checked against the reviewed 89-object closure; the separately reviewed FullPER, ScalarFusionCore, and Application objects are also hash-checked. There is no repeated 83-module build. ClosedProofCanonicalisation is freshly compiled from its exact pinned source as one additional inherited helper.

The two newly acquired inherited files are bound both to their SHA-256 source-store paths and Git blob IDs at commit `7efc6217c090b92d65f2c4cb8b011c18eb96bf7c`. ScalarFusionReverse is retained for inspection only and is not imported by the new theorem. `replay.py` verifies source/acquisition bindings, frozen prerequisite sources and receipt hashes, reused objects and the compiler, then builds the helper and three addition modules into a fresh output directory. It never writes to predecessor packages. Frozen model, compiler, graph and original source files are unchanged; no protected integration occurred.
