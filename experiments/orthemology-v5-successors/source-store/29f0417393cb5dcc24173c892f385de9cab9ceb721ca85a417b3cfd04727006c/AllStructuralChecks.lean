/- Direct syntax-only checks of contextual dependent mixed substitution. -/
import AllStructural
namespace P01AC.StructuralChecks
open OrthemologyV2 OrthemologyV3 P01D P01R

private theorem target_ctx : Ctx [Ty.raw] := .ext .nil (.raw .nil)
private theorem target_var : Has [Ty.raw] (.var 0) .raw :=
  .var (.raw target_ctx) .zero

def dependentReplacement : Ty := .identity .raw (.var 0) (.var 0)

theorem dependentReplacement_formed : Form [Ty.raw] dependentReplacement :=
  .identity (.raw target_ctx) target_var target_var

/-- The concrete replacement really depends on the target context. -/
theorem dependentReplacement_not_closed : ¬ TyScoped 0 dependentReplacement := by
  intro h
  exact Nat.not_lt_zero 0 h.2.1

/-- A finite context map to a context-dependent replacement; no closedness premise. -/
theorem dependent_mixed_map :
    MixedSub [Ty.raw] [Ty.param 0] [.atom .i] [dependentReplacement] := by
  constructor
  · apply MixedTerms.cons (.nil target_ctx) (.param .nil)
    exact .identityIntro dependentReplacement_formed target_var target_var (.refl _)
  · intro n hn
    cases n with
    | zero => exact dependentReplacement_formed
    | succ n => simp only [List.length_cons, List.length_nil] at hn; omega

private theorem source_var : Has [Ty.param 0] (.var 0) (.param 0) :=
  .var (.param (.ext .nil (.param .nil))) .zero

/-- Literal term and type preservation for the genuinely open replacement. -/
theorem dependent_mixed_preserves : Has [Ty.raw] (.atom .i) dependentReplacement :=
  dependent_mixed_map.has source_var

/-- The unused identity tail is still atom zero. -/
theorem finite_identity_tail : images (identityImages 1) 1 = .atom .zero := rfl

theorem finite_identity_not_total_identity : images (identityImages 1) ≠ Poly.var := by
  intro h
  have he := congrFun h 1
  cases he

/-- All elimination preserves an open target-dependent replacement literally. -/
theorem dependent_all_elimination_map :
    MixedSub [Ty.raw] (twkTel [Ty.raw]) (identityImages 1) [dependentReplacement] := by
  exact MixedSub.allElim target_ctx dependentReplacement_formed 0 (Nat.le_refl 0)

#print axioms P01AC.form_trename
#print axioms P01AC.has_trename
#print axioms P01AC.form_rename
#print axioms P01AC.has_rename
#print axioms P01AC.form_mixed
#print axioms P01AC.has_mixed
#print axioms P01AC.MixedSub.form
#print axioms P01AC.MixedSub.has
#print axioms P01AC.MixedSub.lift
#print axioms P01AC.MixedSub.twk
#print axioms P01AC.MixedSub.theta
#print axioms P01AC.MixedSub.comp
#print axioms P01AC.MixedSub.id
#print axioms P01AC.MixedSub.allElim
#print axioms P01AC.form_tinst
#print axioms P01AC.has_tinst
#print axioms P01AC.mixed_finite_identity
#print axioms P01AC.TypedSub.form
#print axioms P01AC.TypedSub.has
#print axioms P01AC.TypedSub.comp
#print axioms P01AC.TypedSub.id
#print axioms P01AC.StructuralChecks.dependent_mixed_preserves
#print axioms P01AC.StructuralChecks.dependent_all_elimination_map
end P01AC.StructuralChecks
