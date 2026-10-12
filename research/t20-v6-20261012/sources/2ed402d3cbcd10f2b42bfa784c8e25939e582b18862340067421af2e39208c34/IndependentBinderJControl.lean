import IndependentScopeControl
namespace FullEIndependentReview
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open RigidityInitiality SourceRigidity
open HasEDependentSubstitutionControls (proofId)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- The ambient context itself requires actual E, independently of the R assumption. -/
theorem nonoriginal_context : CtxE [proofId] := .ext .nil (RigidityInitiality.FullE.has_form seed)
theorem context_not_original : ¬ Ctx [proofId] := by
  intro h
  cases h with
  | ext _ hD => exact HasETypeSubstitutionControls.beyond_original_image_not_formed hD

def ambientId : Ty := .identity proofId (.var 0) (.var 0)
def contextFamily : Ty := wk ambientId

theorem context_variable : HasE [proofId] (.var 0) proofId := by
  have hD := RigidityInitiality.FullE.has_form seed
  have h := HasE.var (RigidityInitiality.FullE.form_wk hD .nil hD) (Lookup.zero (A := proofId) (Γ := []))
  simpa only [wk, proofId_subst] using h

theorem ambientId_formed : FormE [proofId] ambientId := by
  have hD := RigidityInitiality.FullE.has_form context_variable
  exact .identity hD context_variable context_variable

theorem ambientId_seed : HasE [proofId] ident ambientId :=
  .identityIntro ambientId_formed context_variable context_variable (.refl _)

theorem contextFamily_formed : FormE [N, proofId] contextFamily :=
  RigidityInitiality.FullE.form_wk ambientId_formed nonoriginal_context
    (RigidityInitiality.FullE.N_form nonoriginal_context)

theorem contextFamily_at (n : Poly) : inst contextFamily n = ambientId := inst_wk ambientId n

theorem contextFamily_successor : successorFamily contextFamily = contextFamily := by
  simp only [successorFamily, contextFamily, wk, subst_comp]
  congr 1

theorem context_step : HasE [proofId] (abstract ident) (dependentStepType contextFamily) := by
  have h := HasE.piIntro
    (FormE.pi (RigidityInitiality.FullE.N_form nonoriginal_context)
      (RigidityInitiality.FullE.form_arr contextFamily_formed contextFamily_formed))
    (HasE.i contextFamily_formed (RigidityInitiality.FullE.form_arr contextFamily_formed contextFamily_formed))
    (scoped_abstract (show Scoped 2 ident from trivial))
  simpa only [dependentStepType, contextFamily_successor] using h

/-- Tests binding R then n while preserving the old ambient proof variable. -/
theorem ambient_uniform_section :
    HasE [proofId] (abstract (sectionPoly (pren Nat.succ ident) (pren Nat.succ (abstract ident))))
      (arr Rigidity (.pi N contextFamily)) :=
  RigidityInitiality.FullE.rigidity_implies_section nonoriginal_context contextFamily_formed
    ((contextFamily_at zero).symm ▸ ambientId_seed) context_step

theorem binder_indices : shiftedFamily contextFamily =
    .identity proofId (.var 2) (.var 2) := by
  simp only [shiftedFamily, contextFamily, ambientId, wk, subst, proofId_subst, psub, pup, pren]

theorem unshifted_capture_is_wrong : shiftedFamily contextFamily ≠
    .identity proofId (.var 1) (.var 1) := by
  rw [binder_indices]
  intro h
  cases h

/-- A separate genuinely dependent motive for J over the E-only carrier. -/
def jFamily : Ty := .identity (wk proofId) (.var 0) (.var 0)

theorem jFamily_formed : FormE [proofId, proofId] jFamily := by
  have hD := RigidityInitiality.FullE.has_form context_variable
  have hv : HasE [proofId, proofId] (.var 0) (wk proofId) :=
    .var (RigidityInitiality.FullE.form_wk hD nonoriginal_context hD) .zero
  exact .identity (RigidityInitiality.FullE.form_wk hD nonoriginal_context hD) hv hv

theorem jFamily_at (x : Poly) : inst jFamily x = .identity proofId x x := by
  simp only [jFamily, inst, subst, subst_wk_cancel, subst_id, psub, cons]

/-- Uses the port's actual two-binder J transport, in a context excluded from Ctx. -/
theorem j_transport_control : HasE [proofId] (jPoly ident (.var 0) ident) ambientId := by
  have hj := RigidityInitiality.FullE.transport_source nonoriginal_context
    (RigidityInitiality.FullE.has_form context_variable) jFamily_formed
    context_variable context_variable ambientId_seed
    (show HasE [proofId] ident (inst jFamily (.var 0)) from by
      simpa only [jFamily_at, ambientId] using ambientId_seed)
  simpa only [jFamily_at, ambientId] using hj

/-- J erasure is conversion in the unchanged calculus, not reflected equality. -/
theorem erased_j_control : HasE [proofId] ident ambientId := by
  have hj := RigidityInitiality.FullE.transport_has_erased nonoriginal_context
    (RigidityInitiality.FullE.has_form context_variable) jFamily_formed
    context_variable context_variable ambientId_seed
    (show HasE [proofId] ident (inst jFamily (.var 0)) from by
      simpa only [jFamily_at, ambientId] using ambientId_seed)
  simpa only [jFamily_at, ambientId] using hj

#print axioms ambient_uniform_section
#print axioms context_not_original
#print axioms binder_indices
#print axioms j_transport_control
#print axioms erased_j_control
end FullEIndependentReview
