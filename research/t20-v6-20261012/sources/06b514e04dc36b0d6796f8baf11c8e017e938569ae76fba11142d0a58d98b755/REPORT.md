# Independent successor audit

## Disposition

**The scoped P01 effect/coupling successor, P03 native-tree decoder successor, and five newly added measure modules survive this independent review and fresh rebuild. No mathematical or implementation defect was found in their stated bounded claims.** This is a shadow audit against canonical commit `03e2604dfcef278b01c60d19b05370fcec4194b6`, not canonical adoption, historical obligation closure, a novelty judgment, or completion of the wider research campaign.

The strongest useful improvements are:

- P01 supplies an actual normalized rational coupling matrix with exact marginals and a single witness before universal relation quantification. Its original-language theorem has no valuation premise, while a genuinely non-diagonal open-expression witness rules out an empty-support explanation
- P03 proves an independent declarative native-tree grammar sound and complete, including arbitrary field order, with outcome equality covering refusal. All 188 archived concrete comparisons independently reproduce
- The measure additions correctly establish a fixed-finite-horizon identifiability obstruction, additive law-dependent pattern measures, and a general-space distinction between singleton mass and measure-algebra atoms

## Reproduction and evidence

Independent builds use the native Lean 4.19.0 executable, commit `6caaee842e94`, SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`, and Mathlib `c44e0c8ee63ca166450922a373c7409c5d26b00b`. All nine package revisions were checked against the parent's lock, with no tracked modifications. Compiled pinned Mathlib/standard-library dependencies were reused read-only; no whole cache was copied. Every relevant local predecessor dependency and successor source was copied into an independent source directory and rebuilt to a new local object directory. The original successor objects were not used as imports.

| Tranche | Fresh local modules | Target type/axiom readbacks | Primary evidence |
|---|---:|---:|---|
| P01 | 27, including eight successor modules and 19 imported local dependencies | 151 successor declarations | `p01/RESULT.json` and `p01/evidence/IndependentAudit.stdout` |
| P03 | 24, including two original owners | 30 designated targets | `p03/RESULT.json` and `p03/evidence/IndependentAudit.stdout` |
| Measure | 18, including thirteen frontier modules and five local P02/Q8 dependencies | 84 theorem targets | `measure/RESULT.json` and `measure/evidence/IndependentAudit.stdout` |

The observed axiom union in every tranche is limited to `propext`, `Quot.sound`, and `Classical.choice`. The native semantic-soundness corollary has only `propext` and `Quot.sound`. `SOURCE_HYGIENE.json` additionally records a comment/string-aware scan of the 45 main source modules: no proof placeholder, user axiom, `unsafe`, or `native_decide` code token. This scan is supplementary, not proof evidence.

P01's count is **151 declarations, including 107 theorem declarations**, not 151 new mathematical theorems. The measure receipt's 84 targets retain the six explicitly acknowledged overlapping helpers. The five specifically requested newly reviewed measure modules contain 33 theorem declarations; no duplicate historical credit is inferred.

Archive verification in `ARCHIVE_IDENTITY.json` checks all listed payload bytes and hashes, member-name uniqueness, path safety, and fresh-build source agreement:

- P01: `P01_Recursive_Curry_Effect_Successor_2026-09-30.zip`, SHA256 `e4698d9acf9f2b3ab637c0b35bbfb361b8c31a58368bef4ddbace53693867f24`, 150 members, 149 manifest-bound payload members plus its manifest
- P03: `P03_Qualified_Native_Refinement_20260930.zip`, SHA256 `42205fffc4dddfc239d916f1255c4861b530e66a44242cbb50f3c942ab4741dc`, 1,370 members, 1,366 manifest-bound payload members plus four declared control files

P01 v3 and v4 have identical eight source hashes and identical 151-target audit bytes. V4 strengthens qualification-driver/compiler/path bindings; it does not extend the theorem scope. The authoritative P01 receipt is `qualification-v4/QUALIFICATION.json`, SHA256 `298833a96a6f03b97985c0f3d1fbdcbf5926fe3027f9fe19e4dbde6b82a9c413`. In the sealed P03 package, the authoritative receipt is `fresh-build-final/RECEIPT.json`, not the historical `fresh-build-3` label; its SHA256 is `e2c9e3eb72e15cf86157465a06b9b64b15abff463baaec80d34a215a48175fa1`. The measure input receipt matches the supplied SHA256 `597aaf1951ad1458685b4c67a6a6c807ee5032e3e08617e984ef068a53eeeba4`.

## P01: statement and construction audit

### Exact original grammar, rather than a replacement typing relation

`P01EffectSeeds.lean` retains the original `Weight` record and recursively embeds original `MExpr` constructors. `erase_embed` is literal equality of original raw expressions, including leaves and weights. `original_effect_embeds` covers all five original `EffectDerives` rules. The imported `EffectsAndDependence.lean`, `FiniteBridge.lean`, and `InternalPolymorphism.lean` bytes were independently checked against canonical source.

The contextual extension adds polynomial leaves only through actual `FiniteDerives` or `P01F.Has` proofs. It does not license arbitrary polynomial leaves by fiat. The Curry theorem compiles variables, application and abstraction, with the abstraction case proving both endpoint membership and cross-endpoint related application. Type abstraction shifts the context; the explicit fixed-assumption counterexample checks that an unshifted generalization rule is not silently admitted.

The recursive interpretation covers `TypeCode.var`, bottom, arrow, and All. Its renaming and substitution laws are proved by constructor induction, and the fundamental theorem covers all seven original `FiniteDerives` rules, including reduction through the unchanged source `Conv`. All uniformity is discharged by the induction hypotheses at the required endpoint/relation extensions. It is not an external premise asserting the desired fundamental theorem.

### Genuine finite probability laws

For each expression, `Seed` is a finite product. A mixture gets `Fin p.den` and both child coordinates; application gets separate child coordinates. `seedInhabited` supplies an explicit inhabitant using `p.positiveDen`, so normalization cannot hide an empty sample space. Uniform seed mass is the exact rational reciprocal of its positive cardinality.

`pushMass` sums weights of every seed reaching a raw term. It aggregates collisions rather than counting distinct outputs uniformly. The proofs establish nonnegativity, normalization, exact support equivalence with original `Outcome`, and both marginal equalities for `jointMass`. Unused mixture-branch coordinates integrate to one. `output_mass_mixture` gives precisely `p.num/p.den` and `(p.den-p.num)/p.den`; `output_mass_application` gives product weights of the independently sampled child seeds.

These are exact rational laws of the newly constructed seed interpretation. They do not constitute equality to an independently existing, fully formalized canonical probability interpreter. The literal original-language embedding and original support theorem are the exact links supplied.

### Quantifier order and nonvacuity

In `P01FiniteCoupling.lean:171–189`, `common_coupling` constructs `outputCoupling e θ η` before `∀ r`. It has two exact marginals, nonnegative entries, and zero entries off the finite output supports. `coupling_total` separately establishes joint mass one. The witness depends on the fixed expression and two valuations; it does **not** depend on the relation environment.

For open expressions, relation support is correctly conditional on `ValRelated Γ r θ η`. Some choices of context, relation and valuations can fail that premise; the theorem does not claim otherwise. The original closed-language result at lines 211–231 removes that premise altogether, using exact original outcomes and the finite fundamental theorem. Because embedded closed runs ignore valuations, this particular coupling is diagonal in raw outputs.

The separate `P01CouplingWitness.lean` example is genuinely non-diagonal: left mass of I is 1, right masses of I and S K K are each 1/2, and joint mass at `(I,S K K)` is 1/2. Its input valuations are related for **every** relational environment at the polymorphic identity type. Thus the example is neither empty-support reasoning nor an empty conditional domain. I inhabits that polymorphic type; All X.X is separately shown empty. I and S K K are related at a nonempty type while source raw conversion distinguishes them.

### Independent stress controls

`p01/sources/IndependentEffectControls.lean` is separate audit work, not a modification or extension of the sealed successor. Its thirteen freshly compiled controls check:

- zero and full weights select exactly the surviving branch
- 2/4 has the same output law as 1/2
- coincident branch outputs accumulate to mass one
- repeating the same effect syntax in application still samples its two occurrences independently: a cross-output receives mass 1/4
- independent resampling between compared runs is not generally a valid relational coupling: a contextual fair I/S K K effect at a raw-PER type has product mass 1/4 on a forbidden off-diagonal pair, whereas the shared-seed coupling gives that pair zero mass

The last control makes the correlation assumption operationally substantive. Independence **within** each run and shared randomness **between** compared runs are different requirements. Initial audit-probe elaboration failures are preserved under `p01/evidence/IndependentEffectControls-attempt*`; only the final zero-exit source/object/readback receives credit. No sealed source was changed to make these controls pass.

### Scope that must remain open

The result concerns the same finite, fixed-weight expression under two valuations. It is not a theorem about arbitrary pairs of distributions, arbitrary program pairs, value-dependent bind, unbounded recursion, continuous laws, code-dependent weights, or independent cross-run randomness. “Recursive” here refers to interpretation by recursion on finite syntax, not unrestricted program recursion. PER domains need not be finite.

The observational conclusion assumes explicitly specified relation-respecting observers; raw representation tests can distinguish the demonstrated laws. The result does not prove a general weighted-Hall criterion, a relation-wise-to-common coupling quantifier swap, the full dependent Pi/Sigma/Id/All recursive model, raw conversion reflection, or equality with canonical unary `Code` semantics.

## P03: native-tree decoder audit

### Independent grammar and exact fields

`WireValue` is a finite native-tree model, not raw bytes or a CPython heap. It distinguishes natural and negative integers, booleans, null, strings, arrays, and ordered object field lists. Retaining a field list is important: duplicate fields are present until explicitly refused.

`decodeProof` has exact literal tags and exact schemas for all seven proof constructors. `exactFields` checks no duplicates and an exact key permutation. Type/term decoding enforces exact arity and scalar constructor. `NativeProofRep` states key-multiset permutations, actual field memberships, exact type/term trees, and recursive child grammar without mentioning decoder or checker acceptance. It is not a disguised acceptance premise.

`decodeProof_sound` gives the grammar from a parse. `NativeProofRep.decode_complete` accepts every grammar-valid field ordering with enough structural fuel, including recursively reordered children. Determinism follows from completeness. The universal root duplicate rejection theorem has no successful-parse premise; recursive grammar soundness also precludes successful parses with nested duplicate proof fields.

### Refusal is preserved at the correct boundary

`nativeCheck_representation_equivalence` assumes a grammar representation and native-tree shape bounds, then equates the **entire** `Option` outcome with `sourceCheck`, not just successful results. Its refused-source case does not assume source acceptance. Empty traces can decode syntactically and still fail the independent semantic checker, as explicit controls demonstrate.

The source-checker refinement remains acceptance-directed toward the erased target checker: malformed trace contents can erase to an accepted target certificate, so reverse acceptance is not valid. The native representation equivalence does not erase this distinction.

### Exporter remains separate

`partialConstructorExport` retains a separate 512-unit constructor-work gate after source checking. `native_checker_partial_export_square` requires successful partial export; it does not derive exporter success from checking. The balanced identity witness is accepted at 7,916 input nodes while its export work is 1,022, and the partial exporter refuses it. Name/row/text-byte/host limits of the full textual exporter remain outside this constructor-level result.

### Independent concrete replay

`native-case-replay/RESULT.json` records an independent replay of all 188 archived raw fixtures against the exact source `reference.py`, whose bytes equal canonical source, followed by newly compiled Lean equality theorems against this audit's fresh model objects. Every accepted result matches the exact returned term and type; every refusal matches `none`.

Results: **54 accepted, 134 refused; all 188 comparisons pass.** The 147 duplicate-free fixtures also agree with actual native `reference.check`. The 41 duplicate-bearing fixtures are passed to strict raw JSON with duplicates preserved; no `dict(fields)` conversion erases them first.

Coverage is 52 root field-order cases, 20 missing fields, 20 same-value duplicates, 20 conflicting duplicates, 7 extra fields, 28 wrong rule kinds/names, 17 malformed types, 11 trace cases, 6 wrong roots, 6 malformed children, and 1 nested duplicate. These are finite execution comparisons, not a proof of every raw-runtime behavior.

### Remaining boundary

No theorem verifies UTF-8/JSON lexing/parsing, actual CPython execution, mutable capture or races, aliases as heap identity, cycles, subclasses, callbacks, hostile/foreign native objects, host allocation/stack failures, arbitrary API calls, or the full textual exporter. Lists and tuples are identified as tree arrays. Decoder proofs plus 188 tests must not be promoted into universal raw-JSON or CPython refinement. Historical source-model documentation and older receipts are retained history; the native extension has its own scope and current final receipt.

## Measure: the five newly reviewed modules

- **FinitePrefixBoundary (9 theorem declarations):** the explicit truncation map preserves each prefix through a fixed horizon N and pushes fair Cantor law onto a finite carrier. The truncated law has positive-singleton defect zero, fair Cantor has defect one, and their event-supremum TV distance is one
- **PatternAdditivity (4):** the law-specific atomic-pattern pushforward is additive for finite measures and countably many measurable observations with measurable singleton codomains; nonnegative real scaling is also proved. The common-support comparison is justified almost everywhere, so this does not secretly posit a universal pointwise classifier. Countability is substantive because the simultaneous exceptional-set union must remain null
- **NoUniversalClassifier (5):** a measurable law-blind single-point Boolean classifier valid for every probability law would be true at every point by testing Dirac laws, contradicting fair Cantor law. The randomized-test version uses the same Dirac argument for a measurable nonnegative success function and is equally sound. This does not exclude law-informed procedures or arbitrary infinite-observation mechanisms
- **PrefixMixture (8):** mixing fair Cantor and the N-truncated law realizes every defect r in [0,1], with the same prefix distributions through N. The probability and defect conclusions retain the necessary r ≤ 1 hypothesis
- **PointAtomBoundary (7):** an actual countable-cocountable sigma algebra and countably additive 0/1 law are constructed. On an uncountable carrier, including the explicitly supplied real carrier, the whole space is a measure-algebra atom despite null singletons and positive-singleton defect one

Two quantifier/terminology guards are mandatory:

1. The finite-prefix construction is **for every chosen finite horizon N, an alternative law depending on N**. It is not a different fixed Cantor law sharing every finite-dimensional marginal simultaneously. The full collection of finite-dimensional laws determines the Cantor law
2. TV here means the supremum of absolute differences over measurable events, with probability-law range [0,1]. On general measurable spaces, the repository formula is a **positive-singleton defect**, not unrestricted diffuse or nonatomic mass

The last counterexample is the classical construction in [Fremlin, Measure Theory, §211R](https://www1.essex.ac.uk/maths/people/fremlin/chap21.pdf), PDF page 7 / zero-based page 6. The source was independently opened and checked: §211R defines the same sigma algebra and 0/1 measure and explicitly describes its purely atomic but non-point-supported character. No novelty credit is assigned.

## Final limits

This review adds independent machine and semantic evidence within the precise scopes above. It does not replace external expert peer review or an integration workflow. The compiler, Lean kernel, operating system, and pinned compiled library dependencies remain trusted. Original source owners, canonical working tree, historical statuses, and package sources were not modified. Relevant failed independent probe attempts are preserved as diagnostics and excluded from successful evidence.
