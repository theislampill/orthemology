# Actual HasE admits arbitrary contextual type-parameter substitution

## Exact result and sufficient hypotheses

`P01AC.ExtensionalRepair.Structural.MixedSubstitution Γ Δ σ τ` requires:

1. `∀ n, FormE Δ (τ n)`: every type-parameter image has actual-E formation in the target telescope.
2. `∀ {n A}, Lookup Γ n A → HasE Δ (σ n) (mixed σ τ A)`: every term-variable image has actual-E typing at the simultaneously transformed dependent lookup type.

With `CtxE Δ`, the new `form_mixed` and `has_mixed` send arbitrary actual `FormE Γ A` and `HasE Γ p A` to `FormE Δ (mixed σ τ A)` and `HasE Δ (psub σ p) (mixed σ τ A)`. The source derivation already certifies its source context. These are the literal existing `mixed` and `psub`, not replacement definitions. No original-Has requirement occurs in the interface. Type images can mention every target term variable and arbitrary open type parameters.

`TypeSubstitution Γ Δ τ` specializes to identity term images. Its precise context-compatibility condition is `Lookup Γ n A → HasE Δ (.var n) (tsubst τ A)`. The theorems `form_tsubst` and `has_tsubst` then preserve formation and typing while leaving the polynomial literally unchanged.

The context-compatibility premise is important. Arbitrary types formed in a full target telescope cannot simply be substituted uniformly into every declaration of a source telescope: declarations live in their respective tails. The theorem does not claim an unchecked `Γ.map (tsubst τ)` is well formed. For an empty source context compatibility is vacuous (`has_closed_tsubst`), and the top-instantiation map below constructs compatibility automatically for an arbitrary dependent telescope.

A finite replacement list with the inherited Bottom default supplies the total formation field through `finite_type_images`. The total-function presentation therefore does not require an infinitely specified family of independent proof obligations for finite replacements. Unused term-variable images are unrestricted.

## Actual dependent typing consequence

`TypeSubstitution.top` proves, from arbitrary `FormE Γ A`, the map from `twkTel Γ` back to `Γ` replacing type parameter zero by A and decrementing the older parameters. It supplies genuine actual-E lookup typings by the existing literal cancellation `tinst (twk C) A = C`.

Consequently:

- `form_tinst`: `FormE (twkTel Γ) B → FormE Γ A → FormE Γ (tinst B A)`.
- `has_tinst`: `HasE (twkTel Γ) p B → FormE Γ A → HasE Γ p (tinst B A)`.
- `allElim_formed`: `HasE Γ p (.all B) → FormE Γ A → HasE Γ p (tinst B A)`.

The last theorem derives the explicit result-formation premise of the actual `HasE.allElim` rule. It changes no constructor. The replacement A may itself be genuinely term-dependent, and its formation need not exist in original Form. This is a concrete strengthening beyond the retained original-Has `form_tinst`/`has_tinst` results.

## Composition with dependent term substitution

`MixedSubstitution.comp` certifies the ordinary literal composition of both maps. It transforms term images by `psub` and type images by `mixed`.

More specifically, `TypeSubstitution.thenTerm` and `has_type_then_term` directly invoke the freshly checked actual-E `form_subst`/`has_subst` from the prior dependent-term packet. The exact square is:

`subst δ (tsubst τ A) = mixed δ (fun n => subst δ (τ n)) A`.

The term map must act inside the injected target-dependent type images. It would be incorrect to retain unchanged τ. `TypedSubstitution.thenType` proves the reverse-order map, and `has_mixed_identity_types` recovers the prior pure-term conclusion as the literal identity-type-map specialization. These are syntactic equalities of the retained type language, not raw conversion and not reflected object-language equality.

## Full rule and binder coverage

The proof uses the actual mutual `FormE.rec` with all 7 formation and all 20 typing constructors, including Pi extensionality and All extensionality. Its structure ports and credits the retained original-Has proof in `AllStructural.lean`, with actual-E structural lemmas from the prior packets.

- Pi/Sigma lift σ to `pup σ` and every τ image to `wk (τ n)`.
- All leaves polynomial images unchanged and lifts τ to `tup τ`.
- J uses the actual two-extension identity telescope, twice lifting σ and twice weakening τ.
- Finite typing maps the literal finite replacement table.
- Both extensionality rules retain endpoint typings, formation, proof evidence, and every explicit scope condition. The new small `form_scoped` proof derives type-image scope from actual-E formation; the existing `tyScoped_mixed` then transports these conditions.
- Conversion uses the unchanged eight-rule `PolyConvPlus` relation and its checked substitution theorem.

The actual-E formation-scope lemma is new, not an inherited alias. Its identity case reuses inherited `ClosedProofCanonicalisation.has_scope`; the earlier original-Form `form_scoped` cannot be substituted for it.

## Discriminating controls

`TypeSubstitutionControls.lean` proves two distinct controls.

1. The genuine target-dependent type image `Id_raw(var 0,var 0)` is formed in `[raw]`. Substituting it for an open type parameter in an actual typed `All(α → α)` source crosses both All and Pi. The correct Pi codomain mentions the old target variable at index 1. The incorrect unlifted result is proved unequal. Applying the prior dependent-term theorem with `var 0 ↦ I` then produces `All(Id_raw(I,I) → Id_raw(I,I))`. Keeping the injected type images unchanged is also proved to give a different literal type.

2. Let `E = Id_N(I,SKK)` and `D = Id_E(I,I)`, using the retained actual-E Church identity witness. `beyond_original_image_formed` proves actual `FormE [] D`, while `beyond_original_image_not_formed` proves `¬ Form [] D`. Substituting D for the open parameter of the typed polymorphic identity produces actual `HasE [] I (All(D → D))`. `beyond_original_result_not_typed` proves no original-Has polynomial inhabits that result. This excludes a hidden restriction to old Form/Has. Choosing E alone would not establish the same formation-level discriminator, so the control deliberately uses D.

The exclusions are positive proofs of negation, not inferences from failed typechecking. The actual HasE, original Has, and independently studied HasC are not identified.

## Ancestry and boundaries

An independent read-only source audit found arbitrary original-Has mixed substitution and top type instantiation in the retained `AllStructural.lean`; actual-E type renaming/weakening and dependent term substitution existed separately. No predecessor actual-E general type/mixed substitution theorem was found in the inspected chains. The prior dependent-term packet explicitly left this independent sort unchanged.

This closes the stated structural interface gap for the pinned actual calculus. It does not establish full relational parametricity, reflection, UIP, Sigma eta, datatype initiality, premise-free rigidity, T21, integration, or programme closure. It does not replace a target or claim that arbitrary context rewrites are valid.

## Reproduction and integrity

Run `bash hase-type-parameter-substitution-20261010/check.sh`. It compiles only the three additive modules with the installed Lean 4.19.0 and `--trust=0`, reusing existing compiled dependencies. No baseline rebuild or protected repository edit is needed. `validation/build.log` is clean.

`validation/SOURCE_HASHES.json` pins the new Lean modules and replay script plus the literal grammar, algebra, original proof, actual-E structural chain, dependent-term packet, and concrete discriminator sources used. `validation/PRESERVATION_CHECK.json` checks the preceding dependent-term source pins remain unchanged.

The main structural and application theorems and the ordinary dependent-image controls use only standard Lean `propext` and `Quot.sound`. The separately identified inherited Church discriminator additionally uses `Classical.choice`. No new axioms or `sorryAx` occur. Independent replay and adversarial controls are recorded by the separate reviewer.
