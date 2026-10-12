import OriginalIdentityNoninhabitation
import ReviewControls

namespace ReviewHenkinIdentity
open P01AC P01D
open P01AC.ExtensionalRepair (HasE FormE)
open P01AC.EffectiveCompleteness (N)
open P01AC.UnaryIdentity.IntensionalBoundary (variableExpr redundantExpr)

def literalIdentity : Ty := .identity (arr N N) variableExpr.closed redundantExpr.closed

theorem same_identity : HomogeneousOriginalIdentity.originalIdentity =
    FullPER.Application.originalIdentity := rfl

theorem literal_identity_formed : FormE [] literalIdentity :=
  .identity
    (P01AC.ExtensionalRepair.form_inclusion
      (P01AC.ExtensionalRepair.ExactScalarFusion.T_form P01AC.Ctx.nil))
    (P01AC.ExtensionalRepair.has_inclusion variableExpr.closed_has)
    (P01AC.ExtensionalRepair.has_inclusion redundantExpr.closed_has)

/-- Independent complementary model argument for the exact identity target. -/
theorem no_internal_identity_negation (p : Poly) :
    ¬ HasE [] p (arr literalIdentity .bottom) := by
  intro h
  have hp := FullPER.fundamental h FullPER.Application.emptyEnv
    FullPER.zeroEnv FullPER.zeroEnv FullPER.Application.emptyEnv_admissible ⟨rfl,rfl⟩
  rw [FullPER.F_arr] at hp
  exact hp _ _ (FullPER.Application.original_identity_inhabited
    FullPER.Application.emptyEnv FullPER.zeroEnv)

theorem literal_original_identity_independent :
    (∀ p : Poly, ¬ HasE [] p
      (.identity (arr N N) variableExpr.closed redundantExpr.closed)) ∧
    (∀ p : Poly, ¬ HasE [] p
      (arr (.identity (arr N N) variableExpr.closed redundantExpr.closed) .bottom)) :=
  ⟨HomogeneousOriginalIdentity.literal_original_identity_uninhabited,
    no_internal_identity_negation⟩

#print axioms same_identity
#print axioms literal_identity_formed
#print axioms no_internal_identity_negation
#print axioms literal_original_identity_independent
end ReviewHenkinIdentity
