# Independent review: finite typed-telescope nucleus

Disposition: **ACCEPTED for the frozen bounded typed-context nucleus**, with the precise legacy-tree clarification below. This is independent automated source/kernel review, not human-specialist validation, a general novelty certification, canonical adoption, or avenue9/U11 closure.

## Evidence and reproducibility

The implementation matches the substantive v4 design and its independent admission gate. Exact candidate, source, command, log, and control identities are bound in `VERIFICATION.json`, `SOURCE_IDENTITIES.json`, and `LOG_IDENTITIES.json`. The frozen design digest is `21a1016f067499fc087fe0eed26456517db20e3eb050189c9aa3160d549564f2`; the admission digest is `63f3b4803a6d59de4a5aadebd003df9469cd7e77414dc1a384abc8ea8bac3a86`.

All 47 candidate-manifest Lean modules, including 17 new modules, were reconstructed as exact source bytes and compiled in the separate review workspace. Inherited sources were checked against accepted recovery pins; the imported substitution algebra is exactly `ad4e0896abf3a7a3354a14db6743349421520d10eca0790cd632821ecd995649`. No precompiled candidate objects were imported. The existing restored Lean 4.19.0/Mathlib environment was used without downloads or installation, with one serial review lane, `-j1`, a 180-second limit per module, and default heartbeat/recursion limits. Lane ownership was coordinated to retain the global maximum of two compiler processes.

The complete 300-declaration readback compiled independently. A separate inherited `Lean.collectAxioms` gate checked all 300 named declarations transitively. The observed union was exactly `propext`, `Quot.sound`, and `Classical.choice`; there are no custom axioms, sorry dependencies, or unsafe substitutes in the qualified result. Exact theorem/definition contracts were inspected, rather than treating successful process exits as sufficient evidence.

Historical independent control attempts with elaboration errors are preserved with matching source hashes and logs. They are not accepted evidence. All final control/readback modules compile successfully.

## Syntax, construction order, and universal laws

`TypedSyntax` contains the declared Param/Bottom/AllFinite/Raw/Pi/Sigma/typed-Id grammar and every admitted typing constructor. Formation and typing premises are finite syntactic judgments, scope evidence, accepted finite derivations, or unchanged `PolyConv`. No constructor accepts semantic coherence, arbitrary membership, a fundamental theorem, or an unrestricted typed-to-Raw coercion.

`AllFinite C` denotes the accepted interpretation of `all C`; the finite macro exposes finite arrows as ordinary nondependent Pi. Typed variables use literal iterated weakening of declaration types. Raw is restricted to closed atoms, Raw applications/variables, and typed identity-proof erasure. Scoped conversion targets are necessary: an independent theorem proves that open conversion can expand closed I to the unscoped polynomial K I (var 0). Scope and result-formation regularity are derived for the admitted judgments.

`TypedPredicates` defines F structurally first, then G using existing F and smaller G subexpressions, then D/E/H on telescope syntax. These raw predicates do not assume PER or Link lawfulness. Valuations are genuinely finite, represented as zero-padded total evaluator environments.

`TypedSoundness.form_sound` and `has_sound` use generated mutual recursors over the finite judgments. Hereditary type laws are induction conclusions, retaining smaller child-formation results needed by term cases; they are not grammar premises. Id formation invokes smaller endpoint-typing conclusions. Pi/Sigma and typing cases consume smaller formation/typing conclusions. There is no circular call to a claimed semantic theorem on the current derivation.

The resulting universal `fundamental`, `unary_fundamental`, `strong_diagonal`, and `two_sided_invariance` have the required contracts. Strong diagonal quantifies related, potentially unequal valuations, not merely a valuation paired with itself. Context laws establish D/E validity and equivalence, H endpoint validity, two-sided closure, and diagonal agreement. `TypedBoundaryResults` packages derived PERs/Links and proves exact agreement with the accepted PiPER, represented SigmaPER, and IdPER constructors on valid fibres. It does not claim the previously refuted canonical unary carrier equalities.

## Identity and J

G at Id explicitly requires both within-endpoint equalities and both proof conversions to I. Neither equality is inferred from cross-Link relatedness. Formation-derived endpoint typing supplies unary transport of the equality predicates separately on each side.

The general `fundamental_j` constructs left and right E transports from base to point valuations. Each construction includes the identity-proof coordinate; the proof uses both endpoint equalities and both proof conversions. Two-sided motive invariance transports the base relation, and the unchanged literal J reductions supply source compatibility.

`TypedContextualJ` additionally invokes the actual accepted `P01D.j`, rather than only wrapping a J polynomial in a generic term record. It derives the contextual motive's coherence, maps the complete intrinsic identity-context relation to E, and proves literal source-code and target-type equalities.

## Literal substitution and representation

`TypedSub` is a finite component list, with each component typed at the declaration already substituted by its tail. `TypedSub.form` and `TypedSub.has` preserve the literal type substitution and `psub` endpoints, including lifted binders and both J coordinates. Renaming, weakening, substitution composition, and scope algebra are syntactic proofs.

A review finding was resolved before qualification: unused substitution images are atom zero, not an identity tail. Thus the empty substitution maps to exactly zeroEnv, finite context validity is preserved, and intrinsic `Sub.tracks` holds at every index. Independent tests bind this exact padding contract.

Contexts, types, terms, and substitutions map into P01D from the derived laws. `representedTerm_code` is literal equality with the original polynomial; represented substitution code and target type are exact. No arbitrary semantic Tm premise replaces syntax-generated typing.

## Exact legacy compatibility and scope clarification

The checked comparison is for **explicit restricted old-rule derivation trees**. `Legacy.Derivation` is Type-valued, mirrors every original P01DF.Has constructor, and `Derivation.erase` produces exactly the original Has judgment without changing the polynomial or type. `Restricted` recurses over this retained tree; `Restricted.raw_embed` maps it to the all-Raw typed telescope with the identical polynomial. Interpreted PERs are equal, and heterogeneous predicates agree at pointwise source-convertible valuations.

This representation corrects a material proof-irrelevance issue found during implementation/review. A Prop-valued Has proof cannot expose constructor provenance. No theorem here claims to inspect or recover the construction history of an arbitrary erased Has proof.

The restriction checks typing-tree polynomial occurrences, type/motive subexpressions, and displayed conversion endpoints at their binder depth. Original Prop-valued PolyConv evidence remains unchanged; its internal transitivity witnesses are neither inspected nor claimed to have recoverable provenance. Consequently “whole-tree support” refers to the retained typing-rule tree, not a census of every hidden conversion-proof witness. This compatibility theorem includes the fully bounded fragment required by the design.

Both All rules are excluded recursively, even when the final type is finite-representable. An old All subtree translates only through its entire finite embedding image; accepted finite constants may still carry finite impredicative derivations. The old dependent polymorphic type is explicitly excluded. A syntactic Raw-access helper uses admitted proof erasure for the legacy J proof coordinate; the public embedding specializes to the promised all-Raw telescope.

Independent legacy controls instantiate the proof-dependent J translation and prove that a closed final conclusion cannot qualify a retained tree containing an unscoped Raw premise. The comparison is neither a broad old-Has embedding nor a silent recovery of dependent All.

## Positive and negative controls

Checked positive controls include:

- The arbitrary-parameter open pair and literal closed bracket abstraction
- Related I/SKK inputs at the accepted non-raw-refining identity PER without raw conversion
- The exact two-coordinate J motive and literal base/point substitutions
- A concrete J instance with I/SKK endpoints and the nonliteral proof I I
- Two genuinely different, nonempty Raw fibres
- An independent pair test with distinct total/raw endpoint PERs and distinct valuations

Checked negative controls include:

- Independent lawful Links showing that either endpoint equality may fail despite both cross-links and the other equality
- Endpoint-restriction failure for a one-sided Id predicate
- Failure of arbitrary Raw-family transport and unformability of the offending typed-context raw Id
- Impossibility of universal parameter-variable-to-Raw typing
- Failure when J endpoint or proof-coordinate obligations are dropped
- Empty-context variable untypability and conversion scope necessity
- Preserved I/SKK source-conversion obstruction and typed Omega with no normal reduct

These are explicit proved counterexamples and contract tests; no mutation-suite run is claimed.

## Credit boundary

The accepted increment is the previously missing conjunction: syntax-generated arbitrary typed telescopes and dependent domains with the universal two-valuation fundamental theorem, literal typed substitution, exact intrinsic representation, and the declared restricted old-rule-tree comparison.

There is no new dependent All binder, broad old derivation embedding, dependent self-instantiation, raw eta, conversion reflection, higher/intensional identity theory, universe decoder, Type:Type, full-section reification, full normalization, parser/frontend correctness, canonical adoption, or full U11 result. The separately accepted unchanged-Has substitution theorem receives no duplicate completion credit. No canonical mutation, publication, or external contact was performed.
