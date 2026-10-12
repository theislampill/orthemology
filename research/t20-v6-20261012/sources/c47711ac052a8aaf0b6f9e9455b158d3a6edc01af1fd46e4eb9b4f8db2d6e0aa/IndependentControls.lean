import FullPER

/- Independent tests use only the new FullPER theorem for HasE soundness.
No inherited F/G soundness theorem is invoked in these controls. -/
namespace FullPER.Review
open P01AC (Ty Tel arr theta wk tinst)
open P01AC.ExtensionalRepair (FormE HasE CtxE)
open P01D (Poly)
open ImportedOpenTermTransport (interp)
open OpenTermStandardness (T Conv SatPER churchPER)
open P01AC.EffectiveCompleteness (N NBody)

set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

def emptyPER : SatPER where
  rel := fun _ _ => False
  symm := False.elim
  trans := fun h _ => h
  saturated := fun _ _ h => h

theorem all_ranges_over_every_per (B : Ty) (ρ : REnv) (η : Env) (u v : T) :
    F (.all B) ρ η u v ↔ ∀ P : SatPER, F B (cons P.rel ρ) η u v := Iff.rfl

theorem all_parameter_is_empty (ρ : REnv) (η : Env) (u v : T) :
    ¬ F (.all (.param 0)) ρ η u v := fun h => h emptyPER

theorem raw_is_independent_conversion (ρ : REnv) (η : Env) :
    F .raw ρ η = Conv := rfl

/-- Sigma is deliberately a projection PER, even on an open raw generator. -/
theorem open_sigma_control (ρ : REnv) (η : Env) (n : Nat) :
    F (.sigma .raw .raw) ρ η (.var n) (.var n) := ⟨.refl _, .refl _⟩

theorem identity_is_I_class (ρ : REnv) (η : Env) (u v : T) :
    F (.identity .raw (.atom .i) (.atom .i)) ρ η u v ↔ Conv u .i ∧ Conv v .i := by
  constructor
  · exact fun h => h.2
  · exact fun h => ⟨.refl _,h⟩

/-- No closed-world or finite-code restriction on the instantiating type. -/
theorem arbitrary_formed_instantiation {Γ A B} (ha : FormE Γ A)
    {ρ η} (r : admissible ρ) (d : D Γ ρ η) (u v : T)
    (h : F (.all B) ρ η u v) : F (tinst B A) ρ η u v := by
  rw [F_tinst]
  exact h (formation_per ha r d).object

def p : Poly := P01AC.UnaryIdentity.IntensionalBoundary.variableExpr.closed
def q : Poly := P01AC.UnaryIdentity.IntensionalBoundary.redundantExpr.closed
def EndN : Ty := arr N N

theorem p_exact (η : Env) : interp p η = .i := by
  unfold p interp
  rw [ImportedOpenTermTransport.original_p_poly_exact]
  rfl

theorem q_exact (η : Env) : interp q η = OpenTermStandardness.q := by
  unfold q interp
  rw [ImportedOpenTermTransport.original_q_poly_exact]
  exact ImportedOpenTermTransport.q_eval_independent η

theorem church_exact (ρ : REnv) (η : Env) : F N ρ η = churchPER.rel := by
  unfold N NBody
  simp only [F, F_arr]
  rfl

theorem original_typed (ρ : REnv) (η : Env) :
    F EndN ρ η (interp p η) (interp q η) := by
  rw [p_exact,q_exact]
  unfold EndN
  rw [F_arr,church_exact]
  exact OpenTermStandardness.identity_q_related

theorem original_raw_separated (η ξ : Env) : ¬ Conv (interp p η) (interp q ξ) := by
  rw [p_exact,q_exact]
  simpa only [ImportedOpenTermTransport.original_p_eval_exact,
    ImportedOpenTermTransport.original_q_eval_exact] using
    ImportedOpenTermTransport.original_raw_endpoints_still_distinct

def rawEnv : REnv := fun _ => Conv

theorem rawEnv_admissible : admissible rawEnv :=
  fun _ => ⟨Conv.symm,Conv.trans,fun a b h => a.symm.trans (h.trans b)⟩

def leftEnv : Env := cons (interp p zeroEnv) zeroEnv
def rightEnv : Env := cons (interp q zeroEnv) zeroEnv

theorem endpoint_environments : E [EndN] rawEnv leftEnv rightEnv :=
  ⟨⟨rfl,rfl⟩,original_typed rawEnv zeroEnv⟩

/-- An independent application of the NEW all-rule theorem. -/
theorem endpoint_not_raw : ¬ HasE [EndN] (.var 0) .raw := by
  intro h
  have c := fundamental h rawEnv leftEnv rightEnv rawEnv_admissible endpoint_environments
  exact original_raw_separated zeroEnv zeroEnv c

theorem theta_environments : E (theta [] EndN p) rawEnv
    (cons .i leftEnv) (cons .i rightEnv) := by
  refine ⟨endpoint_environments,?_⟩
  change F (wk EndN) rawEnv leftEnv
    (interp (P01D.pren Nat.succ p) leftEnv) (interp p zeroEnv) ∧ Conv T.i T.i ∧ Conv T.i T.i
  rw [interp_ren]
  change F (wk EndN) rawEnv (cons (interp p zeroEnv) zeroEnv)
    (interp p zeroEnv) (interp p zeroEnv) ∧ _
  rw [F_wk]
  exact ⟨(formation_per
    (P01AC.ExtensionalRepair.form_inclusion (P01AC.form_arr
      (P01AC.EffectiveCompleteness.N_form .nil) (P01AC.EffectiveCompleteness.N_form .nil)))
    rawEnv_admissible (show D [] rawEnv zeroEnv from rfl)).left
      (original_typed rawEnv zeroEnv),.refl _,.refl _⟩

theorem theta_endpoint_not_raw : ¬ HasE (theta [] EndN p) (.var 1) .raw := by
  intro h
  exact original_raw_separated zeroEnv zeroEnv
    (fundamental h rawEnv _ _ rawEnv_admissible theta_environments)

theorem raw_motive_not_formed : ¬ FormE (theta [] EndN p) (.identity .raw (.var 1) q) := by
  intro h
  cases h with
  | identity _ hp _ => exact theta_endpoint_not_raw hp

theorem theta_coordinates (η : Env) (a e : T) :
    interp (.var 0) (cons e (cons a η)) = e ∧
    interp (.var 1) (cons e (cons a η)) = a := ⟨rfl,rfl⟩

/-- The proof coordinate legitimately erases in the actual source grammar. -/
theorem theta_context_formed : CtxE (theta [] EndN p) :=
  P01AC.ExtensionalRepair.ctx_inclusion (P01AC.ctx_theta .nil
    (P01AC.form_arr (P01AC.EffectiveCompleteness.N_form .nil)
      (P01AC.EffectiveCompleteness.N_form .nil))
    P01AC.UnaryIdentity.IntensionalBoundary.variableExpr.closed_has)

theorem theta_proof_raw : HasE (theta [] EndN p) (.var 0) .raw := by
  have hA : P01AC.Form [] EndN := P01AC.form_arr
    (P01AC.EffectiveCompleteness.N_form .nil) (P01AC.EffectiveCompleteness.N_form .nil)
  have hhead := P01AC.form_theta_head .nil hA
    P01AC.UnaryIdentity.IntensionalBoundary.variableExpr.closed_has
  have hi := P01AC.form_wk hhead (.ext .nil hA) hhead
  have hv := P01AC.ExtensionalRepair.has_inclusion (P01AC.Has.var hi P01AC.Lookup.zero)
  exact HasE.proofErase (.raw theta_context_formed)
    (P01AC.ExtensionalRepair.form_inclusion hi) hv

theorem proof_sensitive_motive_formed :
    FormE (theta [] EndN p) (.identity .raw (.var 0) (.atom .i)) :=
  .identity (.raw theta_context_formed) theta_proof_raw (.rawAtom (.raw theta_context_formed))

theorem theta_both_environments_valid :
    D (theta [] EndN p) rawEnv (cons .i leftEnv) ∧
    D (theta [] EndN p) rawEnv (cons .i rightEnv) :=
  (context_sound theta_context_formed).ends rawEnv_admissible theta_environments

def B : Ty := .identity EndN p q

theorem assumption_environment : E [B] rawEnv (cons .i zeroEnv) (cons .i zeroEnv) :=
  ⟨⟨rfl,rfl⟩,original_typed rawEnv zeroEnv,.refl _,.refl _⟩

theorem no_raw_reflection_under_assumption (r : Poly) :
    ¬ HasE [B] r (.identity .raw p q) := by
  intro h
  exact original_raw_separated _ _
    (fundamental h rawEnv _ _ rawEnv_admissible assumption_environment).1

#print axioms all_ranges_over_every_per
#print axioms all_parameter_is_empty
#print axioms raw_is_independent_conversion
#print axioms open_sigma_control
#print axioms identity_is_I_class
#print axioms arbitrary_formed_instantiation
#print axioms original_typed
#print axioms original_raw_separated
#print axioms endpoint_not_raw
#print axioms theta_environments
#print axioms theta_endpoint_not_raw
#print axioms raw_motive_not_formed
#print axioms theta_coordinates
#print axioms theta_context_formed
#print axioms theta_proof_raw
#print axioms proof_sensitive_motive_formed
#print axioms theta_both_environments_valid
#print axioms assumption_environment
#print axioms no_raw_reflection_under_assumption
end FullPER.Review
