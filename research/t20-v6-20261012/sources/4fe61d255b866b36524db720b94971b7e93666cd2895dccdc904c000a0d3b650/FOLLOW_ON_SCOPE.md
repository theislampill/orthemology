# Scope and inherited next-principle pointer

10 October 2026. This is a bounded read-only check of the retained pinned source, not a new successor grammar or a proposed axiom implementation.

The concrete countermodel separates the current HasE proof calculus from stronger intended semantics. The inherited paired relational semantics already contains a generic cross-carrier uniformity condition:

- `hase-imported-compiler-transport-20261010/sources/P01PER.lean`: `P01R.Parametric` quantifies over all endpoint PERs P,Q and every respectful `Link P Q`; `AllPER` includes this endpoint-uniformity requirement.
- `.../AllPredicates.lean`: the actual `P01AC.F_all` has two endpoint-uniformity clauses through `G` over all P,Q,Link P Q, in addition to unary instances. `G_all` includes heterogeneous link preservation.
- `.../P01CurryParametricity.lean`: `P01R.curry_fundamental` supplies this semantic preservation for the separately named actual Curry-System-F Has grammar and its compiler.
- `.../ExtensionalRepairSoundness.lean`: actual HasE has a proved fundamental theorem into the inherited F/G interpretation. Thus the new countermodel does not refute the inherited intended semantics or its soundness theorem.

What is absent from the inspected actual `ExtensionalRepairSyntax.lean` is a source rule converting cross-carrier graph/fold preservation into an internal typed identity. Relative to HasPlus, HasE adds exactly the displayed piExt and allExt schemas. These compare endpoints at a common displayed type; neither consumes an algebra-morphism commuting square or creates cross-instance projection identities.

A generic fold-naturality principle, if independently specified and justified in an intended successor, is a sufficient place to look. In ordinary notation its relevant shape says that a map h commuting with steps and respecting seeds also commutes with the Church fold: h(n f a) = n g(h a), at the appropriate internal identity type. This is only an explanatory schema here, not a new source rule, checked successor definition, or assertion of necessity among all possible repairs.

The already frozen `hase-internal-graph-20261010` supplies actual typed graph lift/seed and commuting-square computations. The already frozen `hase-graph-bridge-assembly-20261010/GraphBridgeAssembly.lean` supplies the conditional source theorem `scalar_fusion_from_bridges` from the two exact formed projection identities. The new countermodel shows these two bridge obligations cannot both be inhabited by the current HasE. At the displayed countervaluation, the state projection tracks one step but the atom scalar projection compares one step with zero, so that particular scalar transport fails.

A bounded search of the retained pinned source closure found existing grammars Has, HasPlus and HasE, and semantic relational/uniformity machinery; it did not identify a separately named source successor already internalizing generic fold/graph naturality. This is not a repository-wide or literature-wide absence claim. Check the user's authoritative current programme/branch before designing any successor.

Closed-source Church identity/count results remain valid. Their source terms belong to the same original calculus and satisfy its existing standardness theorem. The countermodel adds a non-source-definable semantic N value to refute a proof universally quantified over n. Thus per-closed-term proofs do not yield the one internal universal proof. This records the exact verified boundary and is not a claim of field-novel incompleteness theory.

## Additional existing named certificate calculus

A subsequent currentness check inspected `homogeneous-per-root-20261010/inherited/UnaryCertificateSyntax.lean`, the separately supplied original T16 source. It already defines `P01AC.UnaryCertificate.HasC`, with the eighteen original Has rules plus a `certified` rule for the existing finite unary certificate checker. It does not contain HasE's piExt/allExt rules, and its conversion premises are the original P01DF.PolyConv. Thus HasC is an existing separate certificate calculus, not a new rule designed here and not a HasE extension by inclusion.

The original-identity noninhabitation above is now directly checked in `OriginalIdentityNoninhabitation.lean` using retained `forward_fixed`, without needing the later four-way theorem. Combining it with any separately verified HasC inhabitant of the same literal identity excludes an endpoint/type-preserving translation of that inhabitant into HasE. The currentness coordinator reports the existing `UnaryCertificateSoundness.strict_current_extension` supplies that positive identity; its acquisition/replay is outside this bounded file's own inspected source set. Do not infer any converse translation or claim every HasC/HasE judgement is comparable.
