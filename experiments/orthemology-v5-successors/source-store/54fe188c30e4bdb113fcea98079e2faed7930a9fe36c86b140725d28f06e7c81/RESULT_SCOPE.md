# Finite typed-telescope nucleus

Status: implemented candidate undergoing independent source/kernel review. No canonical adoption or full dependent-type-theory closure is claimed.

## Mathematical result

The new parallel calculus has finite typed telescopes, arbitrary PER-valued parameters, Raw, dependent Pi, represented Sigma, and typed proof-irrelevant identity. Its terms remain the accepted finite SKI polynomials. An opaque finite All leaf retains the accepted recursive interpretation of a finite impredicative type; the finite macro exposes ordinary arrows as nondependent Pi.

`TypedSyntax.lean` defines only syntactic formation and typing evidence. A rule cannot accept an arbitrary coherent family, semantic membership certificate, fundamental theorem, or semantic conversion oracle. The mutually inductive finite evidence includes explicit formation certificates and scoped conversion targets. The chosen rules retain literal K-priority abstraction and the original source conversion relation.

`TypedPredicates.lean` first defines F on raw type syntax, then G using the already-defined F, then D/E/H on telescope syntax. These predicates exist even at malformed syntax and invalid environments. Lawfulness is not asserted there. Finite valuations are total evaluator environments whose unused tail is zero padded.

`TypedSoundness.lean` proves the formation and typing conclusions with Lean's generated mutual recursors. Smaller formation conclusions retain hereditary child laws; smaller endpoint typing conclusions discharge typed-identity coherence. The checked result includes:

- Endpoint PER symmetry, transitivity, and source-conversion saturation
- Unary transport along the same-endpoint telescope relation E
- H endpoint validity, endpoint-equivalence respect, and diagonal agreement with E
- Heterogeneous G endpoint restriction and term respectfulness
- Two-sided G invariance under independent left/right E changes
- Strong diagonal identity at related, possibly unequal valuations
- The universal fundamental theorem for every admitted typing derivation

The generic law records in the implementation are induction conclusions and helper-lemma arguments. They are never accepted by the formation or typing constructors. PER/Link records and intrinsic terms are constructed from the derived laws afterward.

## Substitution and exact representation

`TypedAlgebra.lean` proves literal capture-avoiding algebra and scope laws. `TypedStructural.lean` derives simultaneous formation/typing renaming, weakening, and term substitution. Its finite typed substitution lists supply one component at the declaration already instantiated by earlier components, and unused images are the atom zero. These lists preserve formation and typing at the literal `psub`/type-substitution endpoints, including the two lifts in J.

`TypedRepresentation.lean` proves validity and relational preservation of finite substitutions and represents the resulting contexts, types, terms, and substitutions in the accepted P01D structures. The represented term code is literally the original polynomial; substitution codes and target PERs satisfy exact equalities.

`TypedContextualJ.lean` additionally uses the accepted contextual `P01D.j` itself. It maps its two-coordinate identity context relation to E, builds its motive from the derived type transport theorem, and proves exact target-type and source-code correspondence. This is more than a generic Tm wrapper around a J example.

## Required controls

`TypedPositiveControls.lean` derives the previously unavailable arbitrary-parameter pair, its abstraction, and the literal motive that inspects both the endpoint and shifted proof coordinate. The J instance works with endpoint values I and SKK and a proof value I I. The accepted identity PER relates the endpoints although raw conversion does not. A separate raw example supplies two genuinely different inhabited fibres; the result is not qualified by empty domains alone.

`TypedNegativeControls.lean` uses lawful nonfunctional links to show that cross-links and one endpoint equality do not imply the other endpoint equality. The exact G identity predicate retains both. It also refutes universal typed-variable-to-Raw coercion, records necessary endpoint/proof-coordinate J transport facts, and shows failure when either coordinate obligation is dropped. The accepted I/SKK raw-fibre obstruction remains unchanged.

## Exact restricted legacy comparison

`TypedLegacy.lean` proves the literal-code embedding for explicit old-rule derivation trees with a whole-tree bounded-support/translation certificate. The rule tree is Type-valued and includes every old constructor; its erasure proves the unchanged P01DF.Has judgement. Retaining an explicit tree is essential because Lean proof irrelevance makes the constructor provenance of a Prop-valued Has proof unobservable.

The restriction excludes old All introduction/elimination at every depth. Every type/motive occurrence must translate; All subtrees translate only when their whole subtree is in the old finite embedding image. Every term occurrence is bounded by its corresponding finite all-Raw telescope, with binder depth accounted for. The finite-constant constructor can still carry any accepted finite impredicative derivation.

The induction keeps the source polynomial literally unchanged. It proves equal interpreted PERs and agreement of heterogeneous predicates when the two valuations are pointwise source-convertible. An internal syntactic Raw-access condition handles J's identity-typed proof coordinate through the admitted proof-erasure rule; the public theorem specializes to the promised all-Raw telescope. Explicit negative theorems reject both All rules, the old dependent polymorphic type, and an All-rule derivation even when its final type is finite-representable. No broad legacy embedding or recoverable provenance of an arbitrary erased Prop proof is claimed.

## Boundaries

This calculus has no new dependent All binder or All introduction/elimination rules. Closed finite constants may use the accepted finite impredicative derivations, and arbitrary PER parameters may include accepted AllPERs. Neither fact restores dependent All or its accepted raw-index self-instantiation inside this new judgement.

Identity is equality in the selected PER with proof values convertible to I. It is proof-irrelevant at this model level. It is not source conversion reflection, higher/intensional identity structure, or numerical identity of real bearers.

No raw eta or abstraction congruence is added to source conversion. Canonical unary carrier equalities previously refuted remain refuted. There is no universe decoder, Type:Type, full-section reification, full normalization, parser/frontend correctness, full U11 result, or canonical adoption claim. This is a source/kernel qualification; it is not human-specialist or empirical scientific validation.
