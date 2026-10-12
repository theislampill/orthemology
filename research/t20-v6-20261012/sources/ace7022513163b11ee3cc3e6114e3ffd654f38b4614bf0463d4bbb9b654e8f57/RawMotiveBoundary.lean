import UArrowAndCompilerControls
import ExtensionalRepairSoundness

/- Target-specific rule stress test. The inherited all-rule F/G soundness is
   used exactly as proved. No soundness of the new open-term model is asserted. -/
namespace P01AC.ExtensionalRepair.RawMotiveBoundary
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)
open P01AC.EffectiveCompleteness
open P01AC.UnaryIdentity
open P01AC.UnaryIdentity.IntensionalBoundary
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

def EndN : Ty := arr N N
def p : Poly := variableExpr.closed
def q : Poly := redundantExpr.closed
def p0 : Term := eval p zeroEnv
def q0 : Term := eval q zeroEnv
def B : Ty := .identity EndN p q
def endpointMotive : Ty := .identity .raw (.var 1) q

/-- Both stress-test contexts are genuinely formed in the actual source grammar. -/
theorem B_formed_old : Form [] B := identity_formed variableExpr redundantExpr
theorem assumed_context_formed : CtxE [B] :=
  .ext .nil (form_inclusion B_formed_old)
theorem assumed_identity_variable : HasE [B] (.var 0) (wk B) :=
  has_inclusion (.var (P01AC.form_wk B_formed_old .nil B_formed_old) .zero)
theorem theta_context_formed : CtxE (theta [] EndN p) :=
  ctx_inclusion (P01AC.ctx_theta .nil
    (form_arr (N_form .nil) (N_form .nil)) variableExpr.closed_has)

/-- The proof coordinate DOES erase legitimately in exactly this context. -/
theorem theta_proof_coordinate_raw : HasE (theta [] EndN p) (.var 0) .raw := by
  have hA : Form [] EndN := form_arr (N_form .nil) (N_form .nil)
  have hhead := P01AC.form_theta_head .nil hA variableExpr.closed_has
  have hi := P01AC.form_wk hhead (.ext .nil hA) hhead
  have hv := has_inclusion (Has.var hi Lookup.zero)
  exact HasE.proofErase (.raw theta_context_formed) (form_inclusion hi) hv

theorem typed_related (ρ : OEnv) : F EndN ρ zeroEnv p0 q0 :=
  ((identityCheck_iff_F_identity variableExpr redundantExpr).mp checker_accepts ρ).1

theorem p_self (ρ : OEnv) : F EndN ρ zeroEnv p0 p0 :=
  P01AC.unary_fundamental variableExpr.closed_has ⟨rfl,rfl⟩

theorem endpoint_environments (ρ : OEnv) :
    E [EndN] ρ (cons p0 zeroEnv) (cons q0 zeroEnv) :=
  ⟨⟨rfl,rfl⟩,typed_related ρ⟩

/-- The unknown endpoint is a function, not an untyped quotation of its code. -/
theorem no_endpoint_raw : ¬ HasE [EndN] (.var 0) .raw := by
  intro h
  have hr := ExtensionalRepair.unary_fundamental h
    (endpoint_environments (fun _ => rawPER))
  exact endpoints_not_convertible hr

theorem theta_environments (ρ : OEnv) :
    E (theta [] EndN p) ρ
      (cons .i (cons p0 zeroEnv)) (cons .i (cons q0 zeroEnv)) := by
  refine ⟨endpoint_environments ρ, ?_⟩
  refine ⟨?_, Conv.refl _, Conv.refl _⟩
  change F (wk EndN) ρ (cons p0 zeroEnv)
    (eval (pren Nat.succ p) (cons p0 zeroEnv)) p0
  rw [eval_ren]
  exact p_self ρ

/-- The same obstruction holds in the ACTUAL two-coordinate J motive context:
    var 0 is the proof; var 1 is the endpoint. All HasE derivations are covered. -/
theorem no_theta_endpoint_raw : ¬ HasE (theta [] EndN p) (.var 1) .raw := by
  intro h
  have hr := ExtensionalRepair.unary_fundamental h
    (theta_environments (fun _ => rawPER))
  exact endpoints_not_convertible hr

/-- Hence Id_Raw(endpoint,q) is not a legal motive for this J instance. -/
theorem endpoint_motive_not_formed : ¬ FormE (theta [] EndN p) endpointMotive := by
  intro h
  cases h with
  | identity _ hp _ => exact no_theta_endpoint_raw hp

theorem assumed_identity_environment (ρ : OEnv) :
    E [B] ρ (cons .i zeroEnv) (cons .i zeroEnv) :=
  ⟨⟨rfl,rfl⟩,(identityCheck_iff_F_identity variableExpr redundantExpr).mp checker_accepts ρ⟩

/-- Even adding the original typed identity as an assumption does not permit
    any proof polynomial to reflect it into Raw identity. -/
theorem no_raw_reflection_under_assumption (r : Poly) :
    ¬ HasE [B] r (.identity .raw p q) := by
  intro h
  have hr := ExtensionalRepair.unary_fundamental h
    (assumed_identity_environment (fun _ => rawPER))
  have hc : Conv (eval p (cons .i zeroEnv)) (eval q (cons .i zeroEnv)) := hr.1
  unfold p q at hc
  rw [P01AC.BooleanPrimitive.eval_closed (has_scoped variableExpr.closed_has)
      (cons .i zeroEnv) zeroEnv,
    P01AC.BooleanPrimitive.eval_closed (has_scoped redundantExpr.closed_has)
      (cons .i zeroEnv) zeroEnv] at hc
  exact endpoints_not_convertible hc

#print axioms no_endpoint_raw
#print axioms assumed_identity_variable
#print axioms theta_context_formed
#print axioms theta_proof_coordinate_raw
#print axioms no_theta_endpoint_raw
#print axioms endpoint_motive_not_formed
#print axioms no_raw_reflection_under_assumption
end P01AC.ExtensionalRepair.RawMotiveBoundary
