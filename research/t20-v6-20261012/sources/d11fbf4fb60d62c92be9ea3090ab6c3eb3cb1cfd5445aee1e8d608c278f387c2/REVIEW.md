# Independent review: actual-HasE mixed type-and-term substitution

Verdict: PASS for the three frozen author modules and the bounded structural conclusions below. No protected source was edited, no baseline was rebuilt, and no integration or programme-closure decision was made.

## Exact interface and improvement

`Structural.MixedSubstitution Γ Δ σ τ` requires actual `FormE Δ (τ n)` for every type image and actual `HasE Δ (σ n) (mixed σ τ A)` for each dependent source lookup `Lookup Γ n A`. Given `CtxE Δ`, `form_mixed` and `has_mixed` preserve arbitrary actual formation and typing under the existing literal `mixed` and `psub`. The source derivation certifies its own source context. No original `Ctx`, `Form`, or `Has` premise is hidden in the map or theorem.

The type images may genuinely mention target terms, including terms in a dependent actual-E-only target telescope. Formation supplies their term-scope obligations; merely scoped raw types do not suffice. The calculus permits arbitrary open type-parameter indices, as in its unchanged `FormE.param` constructor. The theorem does not grant unrestricted context rewriting: each source lookup must remain typed after simultaneous substitution. In particular, mapping a full-target-relative replacement uniformly over every declaration of a telescope would ignore declaration tails and is not justified.

`TypeSubstitution` specializes to identity term images while retaining lookup compatibility. `TypeSubstitution.top` constructs this compatibility automatically for the map `twkTel Γ → Γ` replacing the newest parameter by an arbitrary `FormE Γ A`. Thus `form_tinst`, `has_tinst`, and `allElim_formed` are genuine actual-E corollaries. The last derives the old rule's explicit result-formation premise; it does not alter that rule. Finite type-image lists use the inherited Bottom padding.

The retained `AllStructural.lean` already proves mixed substitution for original `Has`, so this is a port and strengthening to actual E, not a newly invented substitution algebra. The prior actual-E dependent-term packet leaves independent type parameters unchanged. The new result supplies that missing sort. Actual-E `form_scoped` is a new short mutual induction reusing the inherited actual-E polynomial scope theorem.

## Grammar, binders, and delicate rules

I inspected the pinned `ExtensionalRepairSyntax.lean`, original `AllStructural.lean`, inherited `AllSyntax`/`AllMixedAlgebra`, actual-E structural sources, and the prior dependent-term interface. The new core uses actual `FormE.rec` and explicitly covers all seven formation and twenty typing constructors. A fresh Lean metadata check independently confirms two context constructors, seven formation constructors, twenty typing constructors, and the unchanged eight-rule `PolyConvPlus` conversion relation.

- Under Pi or Sigma, term images become `pup σ` and every type image becomes `wk (τ n)`. Lookup transport uses actual-E weakening at the transformed declaration.
- Under All, polynomial images are unchanged and type images become `tup τ`, protecting bound type parameter zero and shifting older parameters. Context lookup is inverted through `twkTel`, then transported by actual-E type weakening.
- The two sorts are independently capture avoiding: fresh controls prove the correct type/term indices after crossing All and Pi, and prove both captured alternatives unequal.
- J forms the real target equality telescope, lifts the term map twice, and weakens type images twice. The motive/result equations are the retained literal algebra, not a reflected equality.
- Pi extensionality transports domain/body/Pi/family/identity formation, both endpoint typings, and the pointwise proof. It retains all three polynomial scopes and both type scopes, using actual type-image formation to justify scope under the lifted map.
- All extensionality transports its body and evidence under the type-weakened target and lifted type map. It retains all endpoint, formation, evidence, and polynomial/type scope premises.
- Finite typing maps the finite replacement list. Pi abstraction uses the existing abstraction naturality theorem. Conversion and identity introduction use the unchanged `PolyConvPlus` substitution theorem.

The dependency audit verifies the core reaches the real mutual recursor and actual PiExt, AllExt, J, and conversion constructors, both binder-lift maps, the theta lift, and `form_scoped`. It also verifies that the proof's transitive dependencies contain no original `Has`/`Form`/`Ctx`, original mixed-substitution theorem/interface, or the checked semantic fundamental theorems. Ordinary Lean equality/function extensionality in retained substitution algebra adds no object-language Raw equality reflection, UIP, or new source rule.

## Composition and independent positive controls

The author proves mixed-map composition, identity-type specialization recovering the prior term-substitution result, both orders of term/type transport, and the exact type-then-term equation

`subst δ (tsubst τ A) = mixed δ (fun n => subst δ (τ n)) A`.

Term substitution must act on the injected type images. The author proves a concrete wrong-unchanged-image result unequal.

Four independently authored positive modules and a dependency audit supplement the author's three modules:

1. `IndependentMixedControls` explicitly builds a real PiExt proof at a free type parameter and a real AllExt proof whose body is that PiExt input. General type substitution transports this derivation to the formed target image `Id_raw(var 0,var 0)` in `[raw]`, across both binders. The resulting Pi codomain refers to target index 1. Actual dependent-term substitution subsequently closes the image endpoints at I. It also proves an out-of-scope identity type cannot be FormE in `[raw]` and rejects both capture alternatives by proved inequalities.
2. `IndependentJConversion` explicitly constructs actual J followed by actual conversion in a nonempty parameterized source context. A non-renaming term map sending the variable to I, together with the target-term-dependent image above, transports the derivation into `[raw]`. Thus J's type-image weakening is exercised with genuinely nonclosed images.
3. `IndependentDependentTarget` lets `E = Id_N(I,SKK)` and `D = Id_E(I,I)`, using the retained extensional witness and original-Has noninhabitation theorem. It builds `[D]`, then a genuinely dependent two-declaration telescope `[Id_(wk D)(var 0,var 0), D]`. It substitutes an identity type over the newest target variable into the real PiExt/AllExt source. Positive negation proofs show neither target telescope is an original `Ctx`, and no original `Has` derivation can produce any type in the two-declaration target. The type image is genuinely term-dependent and not a renamed type parameter. This is unavailable through the old type-renaming or original-Has-only interfaces.
4. `IndependentInstantiationComposition` checks top instantiation and result-formation-free All elimination in that same dependent actual-E-only telescope, at the type image depending on its newest variable. It also composes the non-renaming mixed map with actual dependent term substitution and applies the composite to the J/conversion input.
5. `DependencyAudit` checks the exact grammar counts, transitive structural dependencies/axioms, and one direct use of each intended PiExt, AllExt, J, and conversion constructor in the independently built inputs.

The author's controls also prove a closed discriminator: `FormE [] D` while `¬ Form [] D`, and `HasE [] I (All(D → D))` while no original-Has polynomial inhabits that result. These are proofs of negation, not conclusions inferred from a typechecker rejection.

## Six adversarial interface controls

The following intentionally invalid modules each fail at the intended type mismatch:

- `MissingTypeFormationMustFail`: type-image scope cannot replace actual FormE formation.
- `UnshiftedTypeImageMustFail`: lifting under a term binder cannot retain unweakened type images.
- `UnliftedAllMapMustFail`: lifting under All cannot retain the unlifted type map.
- `MissingLookupCompatibilityMustFail`: the empty-source map cannot discharge an arbitrary source telescope's lookup obligations.
- `UnchangedImageCompositionMustFail`: term-after-type composition cannot silently keep target-dependent type images unchanged.
- `OriginalHasSubstituteMustFail`: the old Has-only substitution theorem cannot consume an arbitrary actual HasE derivation.

These rejection tests establish interface boundaries, not general nonderivability. The substantive nonformation/noninhabitation claims are separately kernel-checked positive theorems.

## Frozen sources and reproducibility

Author hashes:

- `HasEMixedSubstitution.lean`: `ef218f67761ff75d7a5a68cb97f03f6699c1a3eb2a9a91625719939272df652e`
- `TypeSubstitutionApplications.lean`: `701a3e5d84e9dcf3e5607ce2be886a6e2c7ecd17dc38c672a3418594691c3bd8`
- `TypeSubstitutionControls.lean`: `a781b181d745e877b147e700619d3de54864bbefc1fb6f0ef0af768637849391`

Run `python3 hase-mixed-substitution-independent-review-20261010/replay.py`. It creates a fresh output directory, compiles the three exact author sources plus the five independent positive/audit modules with existing Lean 4.19.0 `--trust=0`, and checks all six expected failures. It verifies 1,138 inherited/author source-manifest hash bindings before and after, checks the frozen author copies, checks source proof-escape tokens, and records exact commands, source/object/log hashes, resolved direct import objects, and axiom output in `REVIEW_RECEIPT.json`. It reuses retained compiled prerequisites; it does not claim to rebuild or independently reprove the entire inherited dependency chain. Exploratory logs and `fresh-lib` are not final replay evidence.

All successful modules are warning-free with no `sorryAx`. General mixed substitution, its applications, ordinary dependent-image controls, J/conversion, and map composition use only `propext` and `Quot.sound`. The identified inherited Church discriminator and controls using its actual-E-only context additionally inherit `Classical.choice`.

This review supports admissibility of contextual mixed substitution and its stated corollaries for the pinned actual calculus. It does not prove full calculus completion, unrestricted context rewriting, Raw equality reflection, UIP, Sigma eta, relational parametricity, premise-free rigidity, or an inhabitant of the previously uninhabited original target.
