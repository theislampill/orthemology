# Independent review: actual-HasE dependent term substitution

Verdict: PASS for the three frozen author modules and the bounded conclusions below. No protected source was edited or baseline rebuilt.

## Exact result and inheritance

`Structural.TypedSubstitution Γ Δ σ` requires, for every actual dependent `Lookup Γ n A`, an arbitrary `HasE Δ (σ n) (subst σ A)` derivation. With `CtxE Δ`, the new `form_subst` and `has_subst` preserve arbitrary `FormE Γ A` and `HasE Γ p A` under the literal existing `subst` and `psub` functions. The source context is certified by the supplied derivation; no additional original-Has or original-context assumption is hidden in the interface. Images outside the source telescope's finite scope remain unrestricted.

The inherited `AllStructural` mixed and finite substitution theorems concern original `Has`, not `HasE`. The inherited actual-E structural packet proves type renaming, term renaming, and weakening. Those results are reused for binder lifts; they are not mistaken for this general actual-E term-substitution theorem. The initially duplicated actual-E scope induction was replaced by a one-line reference to inherited `ClosedProofCanonicalisation.has_scope` before freeze.

This result is dependent simultaneous TERM substitution, including the formation/typing effects of its images. It does not assert new arbitrary type substitution or full relational parametricity.

## All-rule structural audit

The source grammar is the unchanged mutual `CtxE`/`FormE`/`HasE` grammar in the pinned `ExtensionalRepairSyntax.lean`: two context constructors, seven formation constructors, twenty typing constructors. `form_subst` uses its real mutual recursor and explicitly covers all twenty typing cases. The HasE theorem is then extracted from substitution of an actual `FormE.identity` derivation; it does not infer Has from HasE.

- The map's finite scope follows from actual-E typing of each lookup image.
- The dependent term lift uses actual-E weakening and `pup σ`. The newest variable is typed at the literally shifted substituted declaration.
- The All lift inverts lookup through `twkTel`, applies actual-E `has_twk`, and commutes term substitution with type renaming. Its polynomial images stay unchanged.
- J forms the real two-extension target telescope and lifts the substitution twice. `subst_motiveAt` checks the resulting motive instantiation.
- Pi introduction uses actual abstraction naturality plus scope transport.
- Pi extensionality retains all domain, body, Pi, identity-family, evidence, and identity-result formation/typing premises. Its body is transported with the lifted map; all three polynomial scopes and both type scopes are transported, including the bound body scope.
- All extensionality transports its body formation and evidence through the type-weakened substitution, keeps both endpoint typings and the identity-result formation, and transports all three polynomial scopes and the body type scope.
- Conversion is transported by the inherited proof for the unchanged eight-rule `PolyConvPlus` relation.

There is no new source constructor, axiom, admission, source equality reflection, or semantic-to-syntactic reflection. Ordinary Lean function extensionality in the branch substitution algebra proves equality of substitution functions; it does not add object-language extensionality. Main theorem dependencies are exactly `propext` and `Quot.sound`.

## Dependent branch application and compatibility

`DependentBranchApplication` proves actual-E lookup formation, a single substitution, formation and typing instantiation, a dependent two-component substitution, and the Sigma branch-substitution corollary. The latter accepts `CtxE Γ`, an arbitrary HasE branch in `B :: A :: Γ`, arbitrary `HasE Γ a A`, and arbitrary `HasE Γ b (inst B a)`. It returns the exact branch application at `inst P (pairPoly a b)`.

Independent `RetainedCompatibility` imports the reviewed prior `Constructive` module and proves literal definitional equality of its `SigmaCompletion.pairSub`, `branchType`, and `branchAt` with the new definitions. It also checks the exact retained branch interface with all context/typing inputs replaced by actual E evidence. Thus this is a real strengthening of that particular previously original-Has-only substitution lemma. It does not prove Sigma eta or a new general Sigma eliminator.

## Independent and adversarial controls

Four freshly compiled independent positive modules check:

1. Single substitution, dependent identity endpoints, map composition, term lifting, and type lifting, all with arbitrary actual-E inputs.
2. The branch theorem expressed without any author-defined branch aliases.
3. Explicitly constructed actual `HasE.piExt` and `HasE.allExt` input derivations, followed by substitution of an atom image for the source variable. These exercise real extensional constructors and a non-renaming map, not merely HasE-typed assumptions.
4. Literal compatibility with the retained Sigma branch syntax and interface.

Four intentionally invalid modules fail with the intended type mismatches:

- Scoped images without typed lookup images do not supply a typed substitution.
- An unlifted map does not substitute through a term binder.
- An unweakened map does not supply the All/type-weakened map.
- A second component at raw `B` cannot replace one required at dependent `inst B a`.

These failures test exact interface boundaries; they are not stronger nonderivability claims.

The separately authored and independently replayed `ExtensionalSubstitutionControl` goes further: it uses the retained actual-E proof of `Id_N(I,SKK)` as an image, substitutes into the genuinely dependent telescope `[Id_extId(x,x), extId]`, and derives the literal substituted proof identity. Its no-original-Has controls follow from retained original-identity conversion and the retained I/SKK raw nonconversion result. Thus this example cannot be explained by quietly restricting substitution images to old Has. Its additional `Classical.choice` dependency is inherited from that closed-Church example, not required by general substitution or the independent constructor controls.

## Frozen sources and replay

- `HasEDependentSubstitution.lean`: `9830e8dd5ffa26c1a28dfc85fd2f7660e6c56088ce4acae67035e3884cdbdfc3`
- `DependentBranchApplication.lean`: `408d8039de050dde3147ff8c7c4a390bbb8a4bae01edc57a8f6f53b943cada71`
- `ExtensionalSubstitutionControl.lean`: `19fbe7d978a9c34fe3235cd5973f53deb11c50ccba83f5fc1546b7d657b1c2dc`

Run `python3 hase-dependent-substitution-independent-review-20261010/replay.py`. It compiles the three exact author sources and four independent positive modules into a new fresh directory using pinned Lean 4.19.0 `--trust=0`, checks four expected failures, and verifies all author files and 1,111 inherited hash bindings before/after. Successful modules are warning-free and have no forbidden proof escapes or `sorryAx`. General substitution, its branch application, and all independent controls use at most `propext` and `Quot.sound`; only the concrete inherited Church discriminator also uses `Classical.choice`.

`REVIEW_RECEIPT.json` records commands, source/object/log hashes, exit codes, and the fresh output directory. `SOURCE_CONSTRUCTOR_COVERAGE.json` records the exact twenty constructors and all mutual proof cases. Exploratory logs and the initial scratch output directory are not accepted replay evidence.

The review certifies this bounded syntactic structural theorem and corollaries. It does not assert source completeness, premise-free rigidity, Sigma eta, global parametricity, integration, or programme closure.
