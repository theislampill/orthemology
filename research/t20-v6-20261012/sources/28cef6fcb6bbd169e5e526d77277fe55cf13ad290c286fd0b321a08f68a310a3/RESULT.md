# Full dependent term substitution is admissible for actual HasE

## Exact interface and theorem

`P01AC.ExtensionalRepair.Structural.TypedSubstitution Γ Δ σ` has one field:

`∀ {n A}, Lookup Γ n A → HasE Δ (σ n) (subst σ A)`.

This is a typed simultaneous substitution between dependent telescopes. Every image is typed by the actual HasE judgement at the simultaneously substituted lookup type. Images need not have original Has typing. Unused out-of-scope indices impose no requirements; lookup typing implies precisely the finite scope condition needed by all derivations.

The new theorems are:

- `form_subst`: `FormE Γ A → CtxE Δ → TypedSubstitution Γ Δ σ → FormE Δ (subst σ A)`.
- `has_subst`: `HasE Γ p A → CtxE Δ → TypedSubstitution Γ Δ σ → HasE Δ (psub σ p) (subst σ A)`.

Source well-formedness is already carried by the supplied source derivation. The target is an arbitrary actual-E telescope, not restricted to a context formed by original Has. The theorem is dependent term substitution with identity on the independent type-parameter sort; it includes source All binders, but does not claim a new arbitrary mixed term-and-type substitution theorem.

## Complete rule coverage

`HasEDependentSubstitution.lean` uses the actual mutual FormE/HasE recursor, including every source constructor and both extensionality rules. It constructs typed substitution lifts rather than treating maps as renamings.

- At a term binder, `TypedSubstitution.lift` uses the already certified actual-E weakening theorem, with the substituted declaration's actual FormE proof.
- At an All binder, `TypedSubstitution.twk` uses lookup inversion, inherited actual-E type weakening, and the existing syntactic substitution/type-renaming commutation law.
- J uses the real twice-lifted map into the transformed equality telescope.
- Pi extensionality transports both endpoint typings, body/family/identity formation, the pointwise proof, all three term-scope requirements, and both type-scope requirements.
- All extensionality transports its body under the type-weakened telescope and retains every endpoint, formation, proof, and scope premise.
- Conversion uses the previously certified eight-rule `polyConvPlus_subst`; no conversion rule is changed.

No new axiom, typing constructor, semantic reflection, UIP, proof irrelevance, equality reflection, or object-language extensionality assumption is introduced.

## Useful dependent application

`DependentBranchApplication.lean` proves actual-E single substitution, dependent pair substitution, and the full-E counterpart of the retained Sigma branch lemma:

Given `CtxE Γ`, an arbitrary `HasE (B :: A :: Γ) d (branchType P)`, `HasE Γ a A`, and `HasE Γ b (inst B a)`, obtain

`HasE Γ (branchAt d a b) (inst P (pairPoly a b))`.

The pair substitution, branch type and branch application are the same literal polynomials used by `SigmaCompletion.branch_has` in `hase-sigma-elimination-equivalence-20261010/Constructive.lean`. The new interface does not secretly require original Has for the context, branch, or either dependent component. This removes that precise structural restriction. It adds no Sigma eta premise or theorem and does not claim unrestricted Sigma elimination.

## A genuinely discriminating input and result

`ExtensionalSubstitutionControl.lean` reuses the retained actual HasE proof of `E := Id_N(I,SKK)`, supplied by `ClosedChurchIdentity.Controls.source_equal_raw_distinct`.

It constructs the dependent source telescope `[Id_E(x,x), E]`, maps both variables to I using actual-E evidence, and applies the new simultaneous substitution theorem to its dependent second variable. The result is an actual HasE proof of `Id_E(I,I)`.

This is more than constructor provenance:

- `no_original_image` proves that no original-Has polynomial inhabits E, using the retained original closed-identity-to-conversion theorem and the retained raw nonconversion of I and SKK.
- `substituted_result_not_original` proves that no original-Has polynomial inhabits the result either: its original formation would already require an original proof of E.

The exclusions are proved, not inferred from a failed type check. They do not assert that every E derivation lies outside Has.

## Ancestry, novelty, and remaining boundaries

A retained-source search found original-Has dependent substitution in `TypedStructural.lean` and the later original-Has mixed substitution in `AllStructural.lean`. The actual-E structural packet supplied type renaming, term renaming, weakening, scope and conversion substitution, but no actual-E general typed substitution. The new proof ports and credits that existing machinery. In particular, `has_scoped` is only a one-line alias of the inherited `ClosedProofCanonicalisation.has_scope`.

The original-Has restriction for dependent branch substitution was a repairable proof limitation, not a failure of the actual HasE calculus. Other original-Has-only theorems are not silently generalized: their individual constructions may still require explicit ports from Form/Has to FormE/HasE. No full relational parametricity, new datatype identity, new eliminator, or calculus extension follows automatically from this structural admissibility result.

## Reproduction and verification

Run `bash hase-dependent-substitution-20261010/check.sh`. It compiles the three frozen new modules with Lean 4.19.0 and `--trust=0`, reusing the retained checked objects. It does not rebuild every inherited prerequisite. The two structural/application modules import only the existing actual-E structural chain; the concrete control additionally imports the retained Church identity controls.

`validation/build.log` is clean. The main structural and branch theorems depend only on standard Lean `propext` and `Quot.sound`; the concrete control also inherits `Classical.choice`. No `sorryAx` or new axioms appear. `validation/SOURCE_HASHES.json` records source and immediate dependency hashes; `validation/PRESERVATION_CHECK.json` checks existing source/manifest pins. Independent replay and adversarial controls are recorded separately by the reviewer.
