# Constructive substitution in the existing dependent judgement

Both universal transformations of the unchanged `P01DF.Has` judgement have been kernel-checked:

- `Has p A → Has (psub σ p) (substIndex σ A)` for every `σ : Nat → Poly`.
- `Has p A → Has p (substType τ A)` for every `τ : Nat → Ty`.

They are named `P01DF.Syntactic.has_index_substitution` and `P01DF.Syntactic.has_type_substitution`. The exact signatures are also checked independently of proof elaboration by `AdmissibilityContract.lean`. The type-substitution result preserves the original polynomial literally, including a composite finite atom.

The completed result fills the existing raw-index successor's expressly excluded syntactic substitution-admissibility obligation. Its contribution is completion and uniform proof reuse within this project. No claim of new general type theory or complete project closure is made. Independent source review and a separate source-only kernel rebuild accept the frozen candidate; see `review/REVIEW.md`.

## What the proof does

### Literal algebra and index certificates

`SubstitutionSyntax.lean` proves equalities of the existing finite syntax, rather than equalities only of interpretations. It derives polynomial lifting/composition; index identity and composition; type renaming and substitution composition; the two-sort interchange square; and the three specialized instantiation squares for term instantiation, type instantiation, and J motives.

The mixed square is exactly:

`substIndex σ (substType τ A) = substType (fun n => substIndex σ (τ n)) (substIndex σ A)`.

Thus index substitution also acts on raw indices in inserted type images. Keeping the images unchanged is generally false and has a concrete disequality control.

Index admissibility is induction over all fifteen existing Has constructors. The finite case reuses the original FiniteDerives proof because index substitution fixes embedded finite types and opaque atoms. Pi introduction uses the previously accepted literal abstraction-naturality theorem. J substitutes its motive with `pup (pup σ)`, retaining both proof and endpoint coordinates while shifting outer images correctly. The seven existing PolyConv constructors are preserved by polynomial substitution. No extra conversion rule is introduced.

### Arbitrary type certificates

The type theorem avoids an invalid atom-expansion argument. It does not inspect the incoming Has proof. Instead, it uses the existing unconditional All introduction and elimination rules.

Define `finitePrefix n τ k` to be `τ k` when `k < n`, and `param (k−n)` otherwise. For every body, even before imposing a support bound, the checked finite-prefix identity equates:

`instantiateType (substType (liftTypes (finitePrefix n (fun k => τ (k+1)))) A) (τ 0)`

with `substType (finitePrefix (n+1) τ) A`.

At zero the composed substitution returns τ0. At successor k, the inserted image has been raised by `renameType succ`; the later single instantiation cancels that raising and returns the earlier image untouched. This is why a free `param 0` inside τ1 survives the subsequent τ0 elimination.

Induction on n therefore transforms any `Has p A` into `Has p (substType (finitePrefix n τ) A)`: introduce one All, apply the induction hypothesis with τ's tail, then eliminate with the unshifted external image τ0. Expanded, this is n introductions followed by eliminations at τ(n−1), …, τ0.

A structural free-type bound takes k+1 at `param k`, maximum at arrows, predecessor under All, and the unchanged body bound under Pi/Sigma. It is zero for bottom, raw and identity. Agreement below that bound implies literal equality of substitutions, using the appropriate existing lift under each binder sort. Choosing n as this bound yields the full arbitrary-substitution theorem, with no closed-image premise.

## Checked reuse and controls

`SubstitutionControls.lean` checks:

- A raw-index shift under Pi preserves the bound zero; the unlifted alternative is unequal.
- Open All/Pi certificates with free variables of both sorts acquire the exact capture-avoiding type.
- τ1 = param0 remains param0 after the later τ0 elimination; recursive replacement gives different syntax.
- A J motive contains proof, endpoint and outer-index coordinates. The correct double lift is checked, and one-lift/coordinate-confusion alternatives are unequal.
- An opaque `atom SKK` is type-substituted into genuinely dependent Sigma/All types. It remains unequal to a polynomial-level SKK application tree.
- An open Sigma pair changes both its literal source polynomial and dependent type, and its transformed proof immediately supplies the existing Sigma projection rule.
- The opaque finite certificate composes with the accepted dependent-polymorphic certificate and open pair through ordinary Has application. The composed source really changes under a concrete substitution.
- The existing candidate envelope retains the exact substituted polynomial. The transformed Sigma certificate also enters the already accepted scoped canonical Sigma admission theorem.

General index composition, type composition and the correctly ordered mixed transformation return reusable original-Has proofs as well.

## Evidence and limits

The restored toolchain is Lean 4.19.0, binary SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`, with the retained Mathlib revision `c44e0c8ee63ca166450922a373c7409c5d26b00b`. The actual 28-module dependency closure was reconstructed by original filename and exact accepted hash, then compiled serially. Every import exited 0. Fifteen pre-existing linter warnings are retained without modifying accepted sources. These dependency rebuilds are not new theorem credit.

The five new proof/control/check modules all exit 0. The independent rebuild also passed these five modules, all 28 accepted dependencies and eleven additional controls, including nested inserted binders, sparse support, noncommuting composition and J underneath Pi. Definition readbacks show the unchanged Poly, Ty, PolyConv, Has and substitution operations. The new universal theorems and their substantive integration controls depend only on the standard logical axioms `propext` and `Quot.sound`; no custom axioms or admitted holes occur. Compiler workers remain 1, each module has a 180-second cap, and default heartbeat/recursion limits are unchanged.

The retained initial contract fails as expected because the two new theorem names are absent from the original imports. Development failures concerning the reserved identifier `prefix`, explicit arithmetic unfolding, and the existing irreducible abstraction definition were repaired locally; their full diagnostics and exits remain available. No mathematical target or accepted definition was changed to address them.

The result concerns finite raw-index Poly/Ty syntax with arbitrary total substitution maps. It does not supply general typed contexts, new formation/coherence premises, equality reflection, abstraction congruence, eta or atom-expansion rules. It does not repair unrestricted recursive canonical Code equality, which remains refuted. It is not a universal serialized certificate transformer, normalization result, parser theorem, physical-provenance claim, or actual-source warrant. Existing exclusion results remain unchanged.
