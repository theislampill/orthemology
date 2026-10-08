/- Isolated bounded control: exact J transport to closed N -> N endpoints.
   The literal unary compiler x/x+0 target is not decided here. -/
import UArrowAndCompilerControls

namespace P01AC.ExtensionalRepair.InhabitedControl
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open Intensional.Plus (PolyConvPlus)

abbrev U : Ty := UArrowControl.U
abbrev E : Ty := UArrowControl.P
abbrev p : Poly := UArrowControl.p
abbrev q : Poly := UArrowControl.q
def Q : Ty := arr N N
def V : Ty := .sigma N E
/-- The specified body in [N,E], with no replacement of either endpoint. -/
def body : Poly := fstPoly (.app (.app (.var 0) (.atom .i))
  (pairPoly (inputNumeral 0) (.var 1)))
def H : Poly := abstract (abstract body)
def Fp : Poly := .app H p
def Fq : Poly := .app H q

theorem U_form {Γ : Tel} (hΓ : Ctx Γ) : Form Γ U :=
  .all hΓ (.param (ctx_twk hΓ))
theorem E_form {Γ : Tel} (hΓ : Ctx Γ) : Form Γ E :=
  .pi (U_form hΓ) (.raw (.ext hΓ (U_form hΓ)))
theorem Q_form {Γ : Tel} (hΓ : Ctx Γ) : Form Γ Q :=
  form_arr (N_form hΓ) (N_form hΓ)
theorem V_form {Γ : Tel} (hΓ : Ctx Γ) : Form Γ V :=
  .sigma (N_form hΓ) (E_form (.ext hΓ (N_form hΓ)))

theorem const_has (c : Term) : Has [] (.app (.atom .k) (.atom c)) E := by
  have ha : abstract (.atom c) = .app (.atom .k) (.atom c) := by
    simp [abstract, freeZero, drop, pren, psub]
  rw [← ha]
  exact .piIntro (E_form .nil) (.rawAtom (.raw (.ext .nil (U_form .nil))))
    (by rw [ha]; exact ⟨trivial, trivial⟩)
theorem p_has : Has [] p E := const_has .i
theorem q_has : Has [] q E := const_has .k

theorem ctxE : Ctx [E] := .ext .nil (E_form .nil)
theorem ctxNE : Ctx [N,E] := .ext ctxE (N_form ctxE)
theorem n_has : Has [N,E] (.var 0) N := .var (N_form ctxNE) .zero
theorem v_has : Has [N,E] (.var 1) E := .var (E_form ctxNE) (.succ .zero)
theorem zero_has : Has [N,E] (inputNumeral 0) N :=
  closed_has (inputNumeral_has 0) N_subst ctxNE
theorem pair_has : Has [N,E] (pairPoly (inputNumeral 0) (.var 1)) V :=
  .sigmaIntro (V_form ctxNE) (E_form ctxNE) zero_has v_has
theorem n_inst_has : Has [N,E] (.var 0) (arr (arr V V) (arr V V)) :=
  .allElim (N_form ctxNE) (V_form ctxNE)
    (form_arr (form_arr (V_form ctxNE) (V_form ctxNE))
      (form_arr (V_form ctxNE) (V_form ctxNE))) n_has
theorem i_has : Has [N,E] (.atom .i) (arr V V) :=
  .i (V_form ctxNE) (form_arr (V_form ctxNE) (V_form ctxNE))
theorem iteration_has : Has [N,E]
    (.app (.app (.var 0) (.atom .i)) (pairPoly (inputNumeral 0) (.var 1))) V :=
  app_has (form_arr (V_form ctxNE) (V_form ctxNE)) (V_form ctxNE)
    (app_has (form_arr (form_arr (V_form ctxNE) (V_form ctxNE))
      (form_arr (V_form ctxNE) (V_form ctxNE)))
      (form_arr (V_form ctxNE) (V_form ctxNE)) n_inst_has i_has) pair_has
theorem body_has : Has [N,E] body N :=
  .sigmaFst (N_form ctxNE) (V_form ctxNE) iteration_has
theorem inner_has : Has [E] (abstract body) Q :=
  .piIntro (Q_form ctxE) body_has (scoped_abstract (has_scoped body_has))
theorem H_has : Has [] H (arr E Q) :=
  .piIntro (form_arr (E_form .nil) (Q_form .nil)) inner_has
    (scoped_abstract (has_scoped inner_has))
theorem Fp_has : Has [] Fp Q :=
  app_has (form_arr (E_form .nil) (Q_form .nil)) (Q_form .nil) H_has p_has
theorem Fq_has : Has [] Fq Q :=
  app_has (form_arr (E_form .nil) (Q_form .nil)) (Q_form .nil) H_has q_has

theorem H_closed : Scoped 0 H := has_scoped H_has
theorem Fp_closed : Scoped 0 Fp := has_scoped Fp_has
theorem Fq_closed : Scoped 0 Fq := has_scoped Fq_has

/-- Exactly the retained J telescope: proof at 0, endpoint at 1. -/
def Θ : Tel := theta [] E p
def motive : Ty := .identity Q Fp (.app H (.var 1))
theorem theta_ctx : Ctx Θ := ctx_theta .nil (E_form .nil) p_has
theorem theta_endpoint_has : Has Θ (.var 1) E :=
  .var (E_form theta_ctx) (.succ .zero)
theorem theta_H_has : Has Θ H (arr E Q) :=
  closed_has H_has (fun _ => rfl) theta_ctx
theorem theta_Fp_has : Has Θ Fp Q :=
  closed_has Fp_has (fun _ => rfl) theta_ctx
theorem theta_Hendpoint_has : Has Θ (.app H (.var 1)) Q :=
  app_has (form_arr (E_form theta_ctx) (Q_form theta_ctx))
    (Q_form theta_ctx) theta_H_has theta_endpoint_has
theorem motive_form : Form Θ motive :=
  .identity (Q_form theta_ctx) theta_Fp_has theta_Hendpoint_has

theorem motive_at (y e : Poly) : motiveAt motive y e = .identity Q Fp (.app H y) := by
  simp only [motiveAt, motive, subst, psub, psub_closed Fp_closed,
    psub_closed H_closed, P01F.cons]
  rfl

theorem base_substitution : motiveAt motive p (.atom .i) = .identity Q Fp Fp :=
  motive_at p (.atom .i)
theorem target_substitution : motiveAt motive q (.atom .i) = .identity Q Fp Fq :=
  motive_at q (.atom .i)
theorem base_form : FormE [] (motiveAt motive p (.atom .i)) := by
  rw [base_substitution]
  exact form_inclusion (.identity (Q_form .nil) Fp_has Fp_has)
theorem target_form : FormE [] (motiveAt motive q (.atom .i)) := by
  rw [target_substitution]
  exact form_inclusion (.identity (Q_form .nil) Fp_has Fq_has)
theorem base_has : HasE [] (.atom .i) (motiveAt motive p (.atom .i)) := by
  rw [base_substitution]
  exact .identityIntro (form_inclusion (.identity (Q_form .nil) Fp_has Fp_has))
    (has_inclusion Fp_has) (has_inclusion Fp_has) (.refl Fp)

/-- The exact source-rule J transport, with the original U-arrow evidence. -/
theorem inhabited_endpoint_identity :
    HasE [] (jPoly (.atom .i) q (.atom .i)) (.identity Q Fp Fq) := by
  rw [← target_substitution]
  exact HasE.j (form_inclusion (E_form .nil)) (form_inclusion motive_form)
    (form_inclusion (.identity (E_form .nil) p_has q_has)) base_form target_form
    (has_inclusion p_has) (has_inclusion q_has) UArrowControl.u_arrow_identity base_has

/-- Positive, exact endpoint and statement controls. -/
theorem H_exact : H = abstract (abstract (fstPoly
    (.app (.app (.var 0) (.atom .i)) (pairPoly (inputNumeral 0) (.var 1))))) := rfl
theorem endpoints_exact : Fp = .app H (.app (.atom .k) (.atom .i)) ∧
    Fq = .app H (.app (.atom .k) (.atom .k)) := ⟨rfl,rfl⟩
theorem Q_inhabited : Has [] (.atom .i) Q := .i (N_form .nil) (Q_form .nil)

#print axioms H_has
#print axioms Fp_has
#print axioms Fq_has
#print axioms motive_form
#print axioms base_substitution
#print axioms target_substitution
#print axioms base_has
#print axioms inhabited_endpoint_identity
#print axioms H_exact
#print axioms endpoints_exact
#print axioms Q_inhabited
end P01AC.ExtensionalRepair.InhabitedControl
