/- Simultaneous typed equality and Raw discrimination in one literal,
   faithfully satisfiable source context. The context assumption is visible. -/
import ConditionalOriginalRefutation
import PositiveTransfer
import FaithfulRawNoConfusion

namespace OriginalRawSeparator.Contextual
open P01AC P01D OrthemologyV2 OrthemologyV3 P01R
open JointCompletion (CtxJ FormJ HasJ)
open FullPER.Application (originalP originalQ originalIdentity emptyEnv emptyEnv_admissible)
open OriginalRawSeparator.Conditional
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

theorem noConfusion_subst (σ : Nat → Poly) : subst σ NoConfusion = NoConfusion := rfl

theorem originalIdentity_subst (σ : Nat → Poly) :
    subst σ originalIdentity = originalIdentity := by
  simp only [originalIdentity, subst, subst_arr, P01AC.BooleanPrimitive.N_subst,
    P01AC.BooleanPrimitive.psub_closed originalP_closed,
    P01AC.BooleanPrimitive.psub_closed originalQ_closed]

theorem context_formed : CtxJ [NoConfusion] :=
  .ext .nil (.formBase (P01AC.ExtensionalRepair.form_inclusion (noConfusion_form .nil)))

/-- The retained positive source construction weakens into the exact context. -/
theorem typed_identity : ∃ p, HasJ [NoConfusion] p originalIdentity := by
  obtain ⟨p,hp⟩ := RigidityInitiality.FullE.PositiveCompletion.joint_compiler_identity
  refine ⟨pren Nat.succ p, ?_⟩
  have h := JointCompletion.Structural.has_wk hp CtxJ.nil
    (FormJ.formBase (P01AC.ExtensionalRepair.form_inclusion (noConfusion_form .nil)))
  simpa only [wk, originalIdentity_subst] using h

def rawNegationWitness : Poly := .app (pren Nat.succ witness) (.var 0)

/-- The actual variable at index zero is the visible no-confusion assumption. -/
theorem raw_negation : HasJ [NoConfusion] rawNegationWitness (arr RawIdentity .bottom) := by
  have c : Ctx [NoConfusion] := .ext .nil (noConfusion_form .nil)
  have nc : FormJ [NoConfusion] NoConfusion :=
    .formBase (P01AC.ExtensionalRepair.form_inclusion (noConfusion_form c))
  have rv : HasJ [NoConfusion] (.var 0) NoConfusion := .var nc .zero
  have wh : HasJ [NoConfusion] (pren Nat.succ witness)
      (arr NoConfusion (arr RawIdentity .bottom)) := by
    have h := JointCompletion.Structural.has_wk (HasJ.hasBase witness_has) CtxJ.nil
      (FormJ.formBase (P01AC.ExtensionalRepair.form_inclusion (noConfusion_form .nil)))
    simpa only [wk, subst_arr, noConfusion_subst, rawIdentity_subst, subst] using h
  have result : FormJ [NoConfusion] (arr RawIdentity .bottom) :=
    .formBase (P01AC.ExtensionalRepair.form_inclusion
      (P01AC.form_arr (rawIdentity_form c) (.bottom c)))
  have h := HasJ.piElim (JointCompletion.Structural.has_form wh)
    (show FormJ [NoConfusion] (inst (wk (arr RawIdentity .bottom)) (.var 0)) by
      simpa only [inst_wk] using result) wh rv
  simpa only [inst_wk] using h

/-- One explicit same-environment realization of the source assumption. -/
def satisfyingEnv : FullPER.Env := FullPER.cons OpenTermStandardness.T.i FullPER.zeroEnv

theorem satisfying_environment :
    FullPER.E [NoConfusion] emptyEnv satisfyingEnv satisfyingEnv := by
  refine ⟨⟨rfl,rfl⟩, ?_⟩
  exact JointRawNoConfusion.faithful_candidate_total emptyEnv FullPER.zeroEnv
    OpenTermStandardness.T.i OpenTermStandardness.T.i

/-- This is context-relative consistency, not merely the closed-Bottom theorem. -/
theorem no_bottom (p : Poly) : ¬ HasJ [NoConfusion] p .bottom := by
  intro hp
  exact JointCompletion.fundamental hp emptyEnv satisfyingEnv satisfyingEnv
    emptyEnv_admissible satisfying_environment

/-- All three facts concern one unchanged HasJ context and the literal endpoints. -/
theorem contextual_discrimination :
    (∃ p, HasJ [NoConfusion] p originalIdentity) ∧
    (∃ r, HasJ [NoConfusion] r (arr RawIdentity .bottom)) ∧
    (∀ p, ¬ HasJ [NoConfusion] p .bottom) :=
  ⟨typed_identity, ⟨rawNegationWitness, raw_negation⟩, no_bottom⟩

#print axioms typed_identity
#print axioms raw_negation
#print axioms satisfying_environment
#print axioms no_bottom
#print axioms contextual_discrimination
end OriginalRawSeparator.Contextual
