# Independent review: closed-source scalar-fusion instances

## Verdict and precise scope

**PASS for the bounded source-derivability theorem.** For any original polynomial `n` and supplied actual `HasE [] n N` proof, the frozen original polynomial `c3` applied to that same `n` has the literal substituted body of the original `W originalQ`. This is actual source typing, beyond semantic validity and beyond numeral-only tests.

The reviewed main source is `ClosedScalarInstances.lean`, SHA-256 `57fd4fdc378db98dc7dda8ac443871a398765761b694c7135b9a20eb67349535`. The exact final statement is:

```
{n : Poly} → HasE [] n N →
  HasE [] (.app c3 n)
    (inst (.all (.pi End (.pi A (Leaf FullPER.Application.originalQ)))) n)
```

**The universal bound-variable source judgment `HasE [] c3 (W originalQ)` and its negation remain OPEN.** The outer quantification over `n` is in the Lean metatheorem, with a closed typing hypothesis. It does not provide a derivation under the source context `[N]`; no omega-rule, completeness theorem, or universal source introduction is available from this family alone.

The conclusion is an inhabitant of the inductive source typing proposition, with an explicit source witness polynomial. The proof depends on `propext`, `Classical.choice`, and `Quot.sound`. It establishes source derivability for every supplied closed input. It is not an implemented executable numeral extractor, a serialized derivation tree, or a quantitative derivation bound. “Constructive” should only be read in the bounded sense of proving the actual source judgment rather than its semantic interpretation; “source-derivability theorem” is the less ambiguous description.

## Source fidelity and mathematical audit

1. `reify` retains every generic source variable, maps the five source constants back to atoms, and preserves application structurally. `reify_conv` is induction on the actual seven-constructor open compatible conversion. `reify_embed` uses the unchanged source atom/application bridge; it does not silently identify packed source atoms with polynomial application. `reify_interp` accounts for every source polynomial constructor. The resulting generic-valuation reflection has no axiom dependency. An independent control proves the full equivalence between actual `PolyConvPlus p q` and open conversion at the generic variable valuation, for arbitrary `p,q` without a scope restriction.

2. `closed_church` uses the inherited all-rule `has_scope` theorem to obtain scope zero from actual `HasE [] n N`, proves environment independence by structural induction on that same polynomial, and invokes the separately reviewed new `FullPER.fundamental`. The explicit admissible empty environment is supplied. No inherited `Has` typing of arbitrary `n` replaces the `HasE` hypothesis.

3. Frozen open-term standardness yields one finite count whose application law holds at genuinely open `f` and `a`. Generic reflection returns actual source conversion between the unchanged `n f a` and the finite iteration. Scalar fusion is separately reflected at those same generic coordinates. The original compiler endpoint is `redundantExpr.closed`; its independently reviewed exact transport is used, not a formula-level replacement or an unproved alias.

4. The finite iteration is independently typed in the original `Has` grammar in `[A, End]`, using the source variables at indices zero and one. The original inclusion embeds this into `HasE`. Actual `HasE.conv` transports its type back to the original left endpoint, then across the scalar conversion to the original right endpoint. Scope of both endpoints is separately proved, using closedness of `n` and the inherited closed typing of the original compiler. No weakening or renaming theorem for arbitrary `HasE` derivations is assumed.

5. Formation and identity introduction use the actual endpoint typing proofs. The identity witness is source `I`; two actual `piIntro` steps abstract the `a` and `f` coordinates, and `allIntro` introduces the type parameter. All explicit formation and scope premises remain present. The new `scalarInstance_exact` theorem verifies capture-avoiding substitution into the literal frozen `W` body. The reviewer independently proved that equation by unfolding source substitution, rather than accepting a new family name as evidence of agreement.

6. The final witness is the exact application `c3 n`. The reviewer independently checked the syntactic shapes `c2 = K (K I)` and `c3 = K c2`, and the original K-conversion from `c3 n` to `c2`. The final source conversion is used in the correct reverse direction to type the requested witness. The type instantiation and polynomial conversion are separate, explicit obligations.

## Inherited overlap and limits

The relevant inherited files were inspected and their pinned bindings checked:

- `EffectiveStandardness.lean` already proves uniform observational standardness for the inherited closed raw F/G carrier. That conclusion is not new. It does not itself supply this generic-open source-conversion reflection or the present arbitrary-HasE instance theorem. This review makes no claim that the new theorem is logically independent of all possible consequences of the inherited development.
- `ScalarFusionCore.lean` provides the fixed source syntax, basic typing, and a conditional forward construction from an already supplied function identity.
- `ScalarFusionReverse.lean` constructs its scalar body under an assumed source variable witness of `W`, then derives the conditional reverse and four-way equivalence. It does not supply that witness and does not already prove the new unconditional closed-input instance family.
- `LiteralScalarFusion.lean` binds `q` literally to `redundantExpr.closed` and specializes the conditional equivalences. Its definitions were inspected; this review does not claim a fresh replay of that entire module or of `ScalarFusionReverse`.
- `ClosedProofCanonicalisation.lean` already supplies all-rule source scope and result formation. Its semantic theorem only canonicalizes an already supplied closed identity proof; it does not create endpoint identities from semantic membership. Only its existing scope and formation helpers are dependencies of the new result. No new credit is assigned to them.

The new contribution is the generic-open reflection bridge and its composition with the reviewed all-HasE full-PER standardness machinery and actual source rules to obtain the closed-input source judgments. Numeral examples serve only as nonvacuity controls.

## Independent verification

Lean 4.19.0 with `--trust=0` independently compiled the exact pinned canonicalisation helper, the frozen main file, both author control files, and two reviewer files. Every final compilation exited zero. The reviewer outputs are separate from all author and predecessor directories. No protected source, original repository file, or predecessor package was changed.

The 89 previously reviewed prerequisite objects were rehashed against their original replay receipt and reused, together with the three separately reviewed `FullPER`, `ScalarFusionCore`, and `Application` objects. All 83 pinned original source hashes, the three predecessor package manifests and their file entries, and the model source/object bindings were rechecked. The two additional inherited acquisitions match both retained connector content and Git blob IDs at commit `7efc6217c090b92d65f2c4cb8b011c18eb96bf7c`. The helper's exact source SHA is `c773b21488efd769d57b3f92ea81b5d3c1cf50de15c7cf4fb1dfd30fa8dc45d8`; the reverse module's is `6a03e72fe6e087c98b97d0f881f6f1dc7960c2a46b89f7f1351394ff3b410b65`.

An initial acquired-file check caught one extra terminal blank line in each of those two files. The author restored exact acquisition bytes before the frozen compilation; both bindings now match. No mathematical defect was involved. Reviewer controls initially needed explicit simplification of the well-founded source abstraction rather than definitional `rfl`; those test elaboration failures were corrected, and final logs contain no errors or `sorryAx`.

`IndependentControls.lean` contains 18 theorems and two helper definitions. Eleven selected controls have printed axiom reports. They check generic conversion equivalence, arbitrary variable preservation, atom packing, the exact original q/endpoints, literal W shape and independently recomputed instantiation, original witness syntax/conversion, the theorem for all supplied closed source inputs, the external-family shape, an actual open typing of the source numeral variable, impossibility of typing that variable in the empty context, nonliteral I-wrapped numeral instances, non-inhabitation of closed Bottom, and preserved raw separation of original p and q.

`DependencyAudit.lean` traverses checked kernel dependencies of seven principal new theorems. It rejects old F/G interpretations, old semantic fundamental/soundness, inherited closed-raw standardness, semantic proof canonicalisation, and the conditional scalar forward theorem. It confirms the actual new full-PER fundamental dependency, the original scope/formation helpers, generic-open reflection, open standardness, and original `HasE.conv`, identity, Pi, and All introduction constructors. It rejects all axioms outside the three ordinary Lean axioms above. This inspection command is evidence about checked dependencies; it adds no theorem, oracle, or axiom.

The frozen compiler binary was hash-checked, not bootstrap verified. Existing third-party library objects remain reused. No repeated 83-module build, fresh universal source derivability, or programme closure is claimed.

## Disposition

Accept and preserve this bounded closed-input source-derivability addition. Keep the internal bound-variable universal scalar-fusion target explicitly open. Exact source, object, log, author manifest, and predecessor receipt hashes are recorded in `REVIEW_RECEIPT.json`.
