# Independent dependent-index review

## Status

**The sealed five-module dependent extension survives independent fresh compilation, exact type/axiom readback and adversarial semantic review within its explicitly restricted raw-index scope. No defect was found in the stated scoped claims.** This is a bounded independent research/code review, not canonical adoption, original-U11 closure or a novelty judgment.

Inputs were copied from `private-locator:2f5cad8da7ca52b2ae7a` into this review's `sources` directory. `RESULT.json` records exact hashes, provenance and fresh object hashes for 27 implementation/import modules: five new modules plus 22 local predecessor dependencies. Lean 4.19.0 commit `6caaee842e94`, binary SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`, and Mathlib `c44e0c8ee63ca166450922a373c7409c5d26b00b` were used. Local predecessor source was rebuilt; only pinned library dependencies were reused read-only. Every Lean invocation used `-j1`. Canonical main remains `03e2604dfcef278b01c60d19b05370fcec4194b6`.

`AUDIT_TARGETS.json`, `AXIOMS.json` and `readbacks.log` currently record 135 explicit type/axiom readbacks: all 114 author declarations, including 69 theorem declarations, plus 21 independently added declarations, including 16 theorem controls. The independently observed axiom sets match the author receipt for all 114 author targets. The observed axiom union is `propext`, `Quot.sound`, `Classical.choice`; no additional axiom was observed. The syntax and typing inductives were also printed in full.


### Sealed input identities

- Archive: `P01_Raw_Index_Dependent_Successor_2026-09-30.zip`, 3,119,921 bytes, SHA256 `dec5951de21c2ef0918f9eb6da130907e4dba4df213dd84ef04209aa251840cc`
- Authoritative receipt: `qualification-final/QUALIFICATION.json`, SHA256 `adfb079b27c5d918e561fa688eb52ca4906a38d7ce703d1e301e5646b84bc29e`
- Manifest SHA256: `fe87d7e9a9dcf2e0d06c285f5e46fa3bc286de18094b988d04ce327ff1a4eec0`

Final main-source SHA256 values:

- `P01DependentModel.lean`: `f2017f4ff67c81eb2d1cb6d4ed3b7efea3e686567409e9d07531a61f6b6d5e59`
- `P01DependentSubstitution.lean`: `74eec27e534d5b3fe69b0543d343043483288011d7edc85a424cc8458e91a610`
- `P01DependentFundamental.lean`: `82cd316ba5a0c4efbfb7bbc8ce5e69659e33cb7227d1d4effbaddb3d2f1d66aa`
- `P01DependentControls.lean`: `6f1afe90be0a46d00763808013733f068a65b4f0fd34d215fb101f0db313856c`
- `P01DependentRepresentation.lean`: `e7c7bd5d62f361f4f8a283e1fe442341e87f0200f0494cb2553af4da3a0ff737`

## Semantic scope and noncircularity

`Ty` is finite syntax: parameter, bottom, All, raw, identity, arrow, Pi and Sigma. `Has` has 15 constructors for raw terms, original finite typing, I/K/S, All introduction/elimination, application, Pi introduction/elimination, Sigma introduction/projection, identity introduction, J and raw conversion. None takes arbitrary semantic validity, an arbitrary family, desired parametricity or uniformity as a premise. The semantic `IndexFamily.coherent` and `Model.identity` fields are constructed recursively; they are not user-supplied evidence in the typing grammar.

All introduction is legitimate here because there is no free typed-term context in `Has`: index variables always range over the raw PER, and the derivation is uniform over type-parameter environments. The fundamental theorem discharges endpoint membership and cross-endpoint uniformity by its induction hypothesis in explicitly extended relation environments. `raw_variable_not_arbitrary_parameter` independently verifies that a raw index variable cannot be asserted at an arbitrary type parameter. This should not be confused with an unrestricted generalization rule for the earlier contextual Curry calculus.

The important restriction is structural: every dependent Pi and Sigma binds the raw `Conv` PER. Identity tests raw conversion of two evaluated polynomials. Heterogeneous links are arbitrary for type parameters, but not for the dependent index sort. Arrow domains may be arbitrary generated types; this does not turn dependent Pi/Sigma domains into arbitrary types.

## Substitution and coherence

Index substitution lifts polynomial substitutions under Pi/Sigma and leaves All's separate type sort alone. Type substitution lifts free type parameters under All and also lifts free *term indices in substituted types* under Pi/Sigma. The two lifts are both present. Interpretation commutes with arbitrary substitutions by recursion over generated type syntax; equality concerns the full object-and-relation model, not only unary membership.

Two independent concrete equalities cover nested All/Pi capture. Three independently mutated copies provide negative controls: deleting the index lift fails `interpret_liftIndices`; deleting the type lift fails `interpret_liftTypes`; dropping J's proof-coordinate transport fails the fundamental theorem at the final relation. See `MUTATION_CONTROLS.json` and `mutations/`. Those failures are expected stress tests, not failures of the reviewed sources.

## Genuine dependent nonvacuity

The author's anchored identity fibre is inhabited at index I and empty at SKK, using the already proved raw nonconvertibility of I and SKK. Its represented dependent Sigma has an explicit pair inhabitant.

The independent controls strengthen this beyond a nonempty Sigma with an empty fibre elsewhere. Let B(x) = Id(x,I) → Id(x,I). I inhabits every B(x), and K I inhabits Pi x.B(x). Nevertheless the fibres really differ: K SKK belongs to B(SKK) because its identity domain is empty, while K SKK does not belong to B(I). `varying_body_nonconstant` proves inequality of these actual PERs. Thus the interpreted dependent Pi can be inhabited with genuinely nonconstant fibres.

The independent `mixed_all_typed` and `mixed_all_self_typed` controls additionally inhabit and self-instantiate `All A. Pi x. A → Id(x,I) → A`. Its body simultaneously contains bound-type polymorphism and genuine raw-index dependency. This is actual syntax-directed instantiation with a dependent impredicative type argument.

## Two-coordinate J

J's motive environment is ordered as proof at index zero, endpoint at index one, then the ambient index environment. The proof obtains `Conv x y` and `Conv p I` from identity membership. It transports the motive from `(I,x,eta)` to `(p,y,eta)`, reversing the latter conversion for the proof coordinate. The represented `jPoly` reduces to the base term at both compared environments, and raw compatibility finishes the relational conclusion.

The independent `two_coordinate_j_typed` and soundness control use distinct syntax for I, I I and I (I I), with a motive mentioning both bound coordinates. The negative proof-coordinate mutation leaves the motive at `(I,y,eta)` and is rejected. No raw bracket-abstraction congruence or eta rule was added.

## Countermodel blocking unrestricted indices

A legitimate respectful diagonal link on the nonempty polymorphic identity PER relates I and SKK, although canonical `Conv` does not. Consequently Id(I,I) is inhabited while Id(SKK,I) is empty. `heterogeneous_index_transport_fails` supplies the concrete counterexample, and the independent `no_unrestricted_link_index_transport` refutes *every* proposed uniform transport principle over all PERs and respectful links for these raw-identity fibres.

This blocks promotion of the current construction to unrestricted heterogeneous typed indices without changing or restricting the equality/fibre semantics. It is not a missing proof that should be filled with an unrestricted transport assumption. The separate omitted-coherence counterexample correctly shows that a naive dependent product relation can fail even symmetry.

## Original-core bridge and remaining boundary

The independently compiled representation module supplies a real bridge to P01D.Ty/Tm and DependentEnvelope. The context carrier is the raw index environment and its relation is pointwise Conv. `candidateTm` retains the literal Poly code and derives its validity from the new fundamental theorem; it does not accept validity as an extra premise. `candidateEnvelope` has a literal code-binding equality.

For Pi/Sigma, `candidateBinder` maps the actual intrinsic context extension to cons of the bound index and ambient environment. Since every term belongs to rawPER, `candidate_fibre` proves equality of the intrinsic fibre and the recursively generated body PER. The Pi/Sigma theorems then prove equality of actual contextual types. Identity is equal to the repaired core's identityTy on the two raw-index terms. All is equal to allTy of a generated AllFormation; the old explicit uniformity premise is discharged by `candidate_all_uniformity` for every Has derivation, not assumed. The lambda and All introduction/elimination code equalities and tracked index-substitution equations are literal. The later type-instantiation representation identifies the generated type with pullback along the actual intrinsic typeInstance substitution. Both index and type substitution fundamental corollaries are included in the final readbacks.

The representation does not give a complete syntax-to-syntax equivalence, a surjective classification of intrinsic Ty/Tm, or a new parser/checker. It does not show that arbitrary proof-carrying intrinsic terms arise from Has. No explicit general rule-by-rule contextual J representation square is supplied; the new J soundness and the original intrinsic J are independently available.

Those P01D owners belong to the previously repaired shadow core. Even a successful code-preserving representation into that core would be meaningful U11 progress but would not establish semantic equality with canonical unary `Code`, `dependentPi`, `dependentSigma` or `equalityCode`. Canonical U11 asks for a full contextual dependent calculus, substitutions, dependent eliminators, judgmental equalities and an exact universe-closure account. The current raw-index syntax fragment is more restricted. No arbitrary ambient sections, universe self-reification, same-level Type:Type, decidable conversion/kernel or full heterogeneous dependent fundamental theorem is established. The raw constructor admits arbitrary SKI terms, so this new typing relation must not inherit the earlier finite System-F strong-normalization or marker-freedom claims. The supplied substitution theorems are model-level commutation and tracking results; no complete contextual judgmental-equality calculus is thereby inferred.

## Audit integrity

No author source or canonical file was modified. Initial independent-control namespace elaboration errors are retained in `preseal/evidence/IndependentDependentControls-attempt1.lean` and the corresponding failed receipt; only subsequent zero-exit versions receive successful credit. The pre-seal snapshot is retained separately and receives no final-package currentness credit.

`ARCHIVE_IDENTITY.json` verifies all 178 ZIP member names are safe and unique, all 177 manifest-bound payload hashes and lengths match, every current author payload agrees with the seal, and all 27 independently rebuilt source files match their sealed copies. The final source/axiom check is in `INPUT_IDENTITY.json`; its nine actual read-only library dependencies were individually checked for pinned revisions and clean tracked source. The earlier independent P01 receipt also agrees on all 22 imported local dependency hashes. `SOURCE_HYGIENE.json` records a comment/string-aware scan with no proof placeholder, user-axiom, unsafe or native-decide code token in the five main modules. The scan is supplemental to the kernel evidence.

The author qualification's 31 pre-audit modules include the same 27 implementation/import modules plus three promised-target contracts and an audit-support module. This independent review instead uses direct kernel type/axiom readbacks and its own controls; it does not conflate the two module counts. The compiler, Lean kernel, operating system and pinned compiled library dependencies remain trusted. This is not external specialist peer review.
