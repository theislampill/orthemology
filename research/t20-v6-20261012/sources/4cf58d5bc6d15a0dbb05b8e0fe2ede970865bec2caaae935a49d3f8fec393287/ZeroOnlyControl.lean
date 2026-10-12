import IndependentControls
import JointInductionInitiality

namespace IndependentRecursorReview
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl
open SourceRigidity RigidityInitiality
open JointCompletion JointCompletion.InductionComputation
open JointCompletion.RecursorUniqueness
open P01AC.Intensional.Plus (PolyConvPlus polyConv_inclusion)
open ClosedScalarInstances (scalarLeft)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

def constantZero : Poly := .app (.atom .k) zero

theorem constant_zero_typed : HasJ [] constantZero NT := by
  have hN := N_form CtxJ.nil
  have hK := HasJ.k hN hN (form_arr hN (form_arr hN hN))
  exact app_has (form_arr hN (form_arr hN hN)) (form_arr hN hN) hK (zero_has_N .nil)

theorem constant_zero_seed_law :
    HasJ [] ident (.identity N (.app constantZero zero) zero) := by
  have hl := app_has (form_arr (N_form .nil) (N_form .nil)) (N_form .nil)
    constant_zero_typed (zero_has_N .nil)
  exact identityIntro_raw (.identity (N_form .nil) hl (zero_has_N .nil))
    hl (zero_has_N .nil) (.k zero zero)

theorem identity_seed_law :
    HasJ [] ident (.identity N (.app ident zero) zero) := by
  have hl := app_has (form_arr (N_form .nil) (N_form .nil)) (N_form .nil)
    (i_T .nil) (zero_has_N .nil)
  exact identityIntro_raw (.identity (N_form .nil) hl (zero_has_N .nil))
    hl (zero_has_N .nil) (.i zero)

/-- Shared zero equations alone do not imply typed function uniqueness.
Soundness is used only in this independent negative scope control. -/
theorem zero_laws_insufficient : ¬ ∃ e, HasJ [] e (.identity NT constantZero ident) := by
  rintro ⟨e, he⟩
  have hOne : HasJ [] (inputNumeral 1) N := .hasBase (EffectiveNumerals.old_numeral_has 1)
  have hr : HasJ [] ident (ResultAt constantZero) :=
    ExtractionFidelity.identity_sym .nil (form_arr (N_form .nil) (N_form .nil))
      constant_zero_typed (i_T .nil) he
  have hpoint := rigidity_pointwise .nil constant_zero_typed hOne hr
  have hleft := app_has (form_arr (N_form .nil) (N_form .nil)) (N_form .nil)
    constant_zero_typed hOne
  have cp : PolyConvPlus (scalarLeft (.app constantZero (inputNumeral 1))) (iterationPoly 0) :=
    (PolyConvPlus.app (PolyConvPlus.app (polyConv_inclusion (.k zero (inputNumeral 1)))
      (.refl _)) (.refl _)).trans (ClosedChurchIdentity.numeral_observation 0)
  have impossible : (0 : Nat) = 1 := DependentExtraction.identity_implies_count_eq
    hleft hOne cp (ClosedChurchIdentity.numeral_observation 1) hpoint
  exact Nat.zero_ne_one impossible

#print axioms zero_laws_insufficient
end IndependentRecursorReview
