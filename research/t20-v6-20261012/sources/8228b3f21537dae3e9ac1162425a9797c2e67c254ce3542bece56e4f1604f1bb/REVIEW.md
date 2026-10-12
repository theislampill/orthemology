# Independent review of the new open-term full-PER extension

## Verdict

**PASS for the concrete new whole-HasE full-PER interpretation and its stated semantic application.** No blocking mathematical, rule-coverage, source-binding, or kernel defect was found. This is an independently checked closure of the previously conditional model-extension obligation, not closure of the larger programme.

Exact reviewed source bindings:

- FullPER.lean: `2a0d01d92923a22c4b41f512e4c4b3524ea1c630d13478176c5c20d63afa7638`
- Application.lean: `6d57b65eb3c4ffc8b7c34ba66beea17b7705265dcc4fdd11e66b14d0c5702bb9`
- Unchanged ScalarFusionCore.lean: `975e2220158cf6b285cc994e36c408389a908c77e0f63bfa028c8cb416319618`

The core does not depend on the inherited F/G interpretation or its soundness theorem. In addition to source inspection, an independent command traversed checked kernel constant dependencies of six principal theorems and rejected both old F/G definitions, old soundness constants, and the old finite fundamental theorem. All six checks passed.

The literal source target `HasE [] c3 (W q)` remains OPEN. Semantic membership is not source derivability, and no completeness theorem is assumed.

## Frozen prerequisites

Read all three predecessor RESULT files: open-term standardness, imported compiler transport, and the Raw-motive boundary. The old F/G soundness theorem is evidence for its own interpretation only. It cannot certify this new interpretation.

An independent fresh-output replay has successfully compiled all 83 pinned original source modules, two missing Mathlib modules, and the four standardness/compiler-transport modules with Lean 4.19.0 `--trust=0`. Existing remaining third-party library objects were used read-only. Every file in each of the three predecessor manifests was rehashed; all matched. All 83 source hashes, Git-blob hashes, exact retained index paths, and import lists were independently checked. The source binding remains repository commit `7efc6217c090b92d65f2c4cb8b011c18eb96bf7c`; no new remote fetch or bootstrap verification of Lean is asserted. See PREREQUISITE_REBUILD.json and its log for exact scope.

## Semantic contract inspected

- Carrier: finite open SKI trees, retaining inert zero and one, imported unchanged from OpenTermStandardness. Source terms embed injectively, and the unchanged source conversion is preserved and reflected by the imported transport.
- Raw: the independently defined compatible SKI conversion Conv. No typed extensional equality is added as a raw equation.
- Parameters: arbitrary conversion-saturated PER relations, supplied with law proofs rather than restricted to syntactic type images.
- All: literal quantification over every SatPER. There is no hidden heterogeneous-link clause or syntax-generated universe restriction.
- Pi: full cross-argument relation, using a left-indexed dependent codomain; well-formed types are proved invariant across related environments, making the apparent left bias coherent.
- Sigma: projection PER. This is intentionally different from the inherited represented-pair interpretation. The source has introduction and projection rules, and does not demand a raw pair-eta law. The new model does not claim agreement with every old semantic clause.
- Identity: endpoint relatedness at the interpreted type plus conversion of both proof realizers to I. This makes proof erasure a genuine raw-conversion consequence without turning an endpoint into raw code.
- Bottom: empty relation.
- Telescopes: empty environment has exact zero padding; extended environments store a related head in the left tail's interpretation. ContextLaws explicitly prove reflexivity on valid environments, both endpoints, symmetry, and transitivity.

The unconditional mixed-substitution theorem is proved for every original Ty constructor. It correctly weakens type images under term binders and lifts type substitution under All. Formation law proofs then establish PER membership of arbitrary formed instantiating types; arbitrary All elimination packages that proved relation as a SatPER. No syntactic-type-universe fullness is inferred from closure alone.

## Rule-level audit

Dependent Pi and Sigma introduction/projection use the imported original abstraction and pair equations at arbitrary open valuations. Pi elimination applies the full related-argument relation directly.

J uses the actual `theta Γ A x`: proof coordinate zero, varying endpoint coordinate one. Its transport compares `(I,x)` with `(e,y)` in the same left base environment. The identity assumption supplies endpoint relatedness and e's conversion to I. Motive invariance is supplied by induction on the actual formation derivation, not a new premise admitted by the HasE grammar. The right output term remains related because transport changes the relation, and raw saturation handles both erased j realizers.

Pi extensionality obtains pointwise equality from h and uses q's self-related function membership to move from x to a related y; it therefore establishes the required cross-argument relation. All extensionality instantiates the one type-weakened body derivation at each arbitrary SatPER. Proof erasure chains the two conversions to I. Conversion uses the imported eight-constructor PolyConvPlus soundness, including atom/application packing.

Finite builtins are handled by a fresh induction on the actual seven-constructor FiniteDerives grammar. In particular All introduction ranges over arbitrary SatPERs, All elimination uses the newly proved finite-code interpretation laws, and reduction uses source-to-open conversion. The finite image environment uses the actual Bottom default beyond the finite table; no missing image law is assumed.

The two main mutual-recursion proofs enumerate all context, seven formation, and twenty typing constructors of the imported grammar. Some syntactic scope/formation premises are unnecessary for individual stronger semantic lemmas, but no source constructor is removed or replaced.

## Exact application and limits

Application.lean identifies the interpretation of the imported source N with the previously reviewed full-PER Church relation by definitional equality. Its N-to-N interpretation is the same ordinary extensional arrow PER. The actual variable and redundant compiler endpoints evaluate to I and the bound compiler q under arbitrary open-term valuations, using the imported kernel transport rather than a formula-only substitution.

The original identity is semantically inhabited by I, while the actual endpoints remain nonconvertible in raw SKI conversion. Every finite successor numeral inhabits N, and the empty context has an explicit admissible interpretation. `no_closed_bottom` applies the new full fundamental theorem, providing a non-collapse consistency control for actual HasE.

The exact imported W and c3 are used unchanged. In `scalar_target_valid`, every related Church pair n,m, every SatPER P, every related P-endomorphism pair f,g, and every related argument pair a,b is quantified. PER self-relatedness yields the left n/f/a instance, and the previously checked scalar conversion transports its right endpoint to q n f a. Both actual c3 applications contract to I. `scalar_target_fundamental` additionally handles arbitrary related outer environments by c3's closed evaluation independence. It remains a semantic Fundamental proposition, not a HasE derivation.

ScalarFusionCore was independently recompiled with `--trust=0`; its SHA-256 and Git-blob digest match the retained original binding and the author's fresh exact-pin acquisition response. Its imports are already in the verified source closure. LiteralScalarFusion.lean was not imported or replayed here. Its retained source defines q as `redundantExpr.closed`, which was inspected and matches Application.originalQ literally; no new kernel-imported alias theorem or replay of its four-way equivalence is claimed.

This result establishes that this concrete full-PER interpretation genuinely extends to the whole actual calculus. It does not assert completeness, derivability from semantic validity, equivalence to the older F/G model, uniqueness of the interpretation, fullness of arbitrary Henkin universes, or a result about every PER model. The carrier and raw conversion are fixed; endpoint typed equality does not collapse raw inequality.

## Independent controls and replay

The exact frozen core, scalar dependency, and application were independently compiled into the reviewer's fresh output with Lean 4.19.0 `--trust=0`. Every compilation exited 0. The core's seven axiom reports and application's seven reports contain only `propext`, `Classical.choice`, and `Quot.sound` or subsets. No postulates, admitted proofs, unsafe implementations, or proof-oracle shortcuts occur in the new author files.

IndependentControls.lean also compiled with `--trust=0`; nineteen selected controls have explicit axiom reports, plus helper lemmas. They establish:

1. Literal full SatPER quantification, with the empty PER showing `All X.X` empty.
2. Raw exactly equals independent Conv; identity proof objects exactly use the I conversion class in a trivial true identity.
3. Projection Sigma membership of an open generator, explicitly exposing this model's deliberate Sigma choice.
4. All elimination at every arbitrarily formed source type, including dependent types, with no finite-code restriction.
5. Exact Church interpretation and actual original typed/raw endpoint separation.
6. Explicit related endpoint and theta environments, and D-membership of both theta environments.
7. New-model all-rule proofs that neither the endpoint variable nor theta endpoint coordinate can be typed Raw, and that the displayed Raw endpoint motive is unformed.
8. The positive actual HasE derivation erasing theta's proof coordinate to Raw, and formation of a Raw identity motive inspecting that proof coordinate.
9. No Raw-reflection proof polynomial under an assumed original typed identity, using an explicit nonempty assumption environment and only the new fundamental theorem.
10. Exact proof-first/endpoint-second theta coordinate evaluations.

DependencyAudit.lean compiled with `--trust=0`. It traverses the kernel's checked dependency graph for `form_sound`, `has_sound`, `fundamental`, `formation_coherent`, `no_closed_bottom`, and `scalar_target_valid`. None depends on inherited P01AC.F/G, predicates, F/G fundamental/soundness theorems, or the inherited finite fundamental theorem. All dependency axioms lie in the three standard Lean axioms named above. This audit is environment inspection only and adds no axiom or mathematical theorem.

REVIEW_RECEIPT.json binds author sources, copied review sources, newly compiled objects, logs, controls, and the prerequisite receipt. The 89 prerequisite build objects were rehashed without repeating their build. All three predecessor manifests and 83 source bindings still match; the frozen author files are unchanged. A mechanical constructor check also confirms twenty actual HasE rules and twenty-nine arms in each mutual induction (two context, seven formation, twenty typing cases).

The fresh 83-source build is a verification operation, not an additional research contribution. Existing third-party library objects are reused, and Lean itself was not bootstrap-verified. No protected sources, repository files, or predecessor package files were changed. Reviewer additions are confined to this separate review directory.

**Disposition:** accept this bounded model-construction result and its exact semantic application. Retain `HasE [] c3 (W q)` and its negation as OPEN. No programme closure is authorized or claimed.
