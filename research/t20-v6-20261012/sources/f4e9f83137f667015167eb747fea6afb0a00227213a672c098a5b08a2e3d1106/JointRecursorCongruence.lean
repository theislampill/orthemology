import JointInductionLaws

namespace JointCompletion.RecursorUniqueness
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl
open SourceRigidity RigidityInitiality InductionComputation
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- Congruence for an actual source arrow. The type need not be old-E formed. -/
theorem arrow_congr {Γ : Tel} {A B : Ty} {f x y e : Poly}
    (hc : CtxJ Γ) (hA : FormJ Γ A) (hB : FormJ Γ B)
    (hf : HasJ Γ f (arr A B)) (hx : HasJ Γ x A) (hy : HasJ Γ y A)
    (he : HasJ Γ e (.identity A x y)) :
    HasJ Γ ident (.identity B (.app f x) (.app f y)) := by
  let M : Ty := .identity (wk B) (pren Nat.succ (.app f x))
    (.app (pren Nat.succ f) (.var 0))
  have ca := CtxJ.ext hc hA
  have hAw := form_wk hA hc hA
  have hBw := form_wk hB hc hA
  have hfw : HasJ (A :: Γ) (pren Nat.succ f) (arr (wk A) (wk B)) := by
    simpa only [wk, subst_arr] using has_wk hf hc hA
  have hv : HasJ (A :: Γ) (.var 0) (wk A) := .var hAw .zero
  have hfx := app_has (form_arr hA hB) hB hf hx
  have hM : FormJ (A :: Γ) M := .identity hBw (has_wk hfx hc hA)
    (app_has (form_arr hAw hBw) hBw hfw hv)
  have at_eq (v : Poly) : inst M v = .identity B (.app f x) (.app f v) := by
    simp only [M, inst, subst, subst_wk_cancel, subst_id, psub, cons]
    simp only [pren, psub_comp, psub, cons, psub_id]
  have base := identityIntro_raw (.identity hB hfx hfx) hfx hfx (.refl _)
  have h := transport_has_erased hc hA hM hx hy he ((at_eq x).symm ▸ base)
  simpa only [at_eq] using h

/-- Literal ordinary successor algebra law, with no comparison hypothesis. -/
def successorLawFamily (P : Ty) (s u : Poly) : Ty :=
  .identity (successorFamily P)
    (.app (pren Nat.succ u) (.app succPoly (.var 0)))
    (.app (.app (pren Nat.succ s) (.var 0))
      (.app (pren Nat.succ u) (.var 0)))

theorem comparison_at (P : Ty) (u v n : Poly) :
    inst (comparisonFamily P u v) n =
      .identity (inst P n) (.app u n) (.app v n) := by
  simp only [comparisonFamily, inst, subst, psub, cons, pren, psub_comp, psub_id]

theorem successor_law_at (P : Ty) (s u n : Poly) :
    inst (successorLawFamily P s u) n =
      .identity (inst P (.app succPoly n))
        (.app u (.app succPoly n)) (.app (.app s n) (.app u n)) := by
  simp only [successorLawFamily, inst, subst, psub, cons, pren, psub_comp,
    psub_id, successorFamily_at]
  rw [P01AC.BooleanPrimitive.psub_closed (P01AC.has_scoped succ_has)]
  change (inst (successorFamily P) n).identity _ _ = _
  rw [successorFamily_at]
  rfl

theorem section_value {Γ : Tel} {P : Ty} {u n : Poly}
    (hc : CtxJ Γ) (hP : FormJ (N :: Γ) P)
    (hu : HasJ Γ u (.pi N P)) (hn : HasJ Γ n N) :
    HasJ Γ (.app u n) (inst P n) :=
  .piElim (.pi (N_form hc) hP) (Structural.form_inst hc hP hn) hu hn

/-- The common curried successor operation respects identity at each fiber. -/
theorem dependent_step_congr {Γ : Tel} {P : Ty} {s n x y e : Poly}
    (hc : CtxJ Γ) (hP : FormJ (N :: Γ) P)
    (hs : HasJ Γ s (dependentStepType P)) (hn : HasJ Γ n N)
    (hx : HasJ Γ x (inst P n)) (hy : HasJ Γ y (inst P n))
    (he : HasJ Γ e (.identity (inst P n) x y)) :
    HasJ Γ ident (.identity (inst P (.app succPoly n))
      (.app (.app s n) x) (.app (.app s n) y)) := by
  have hPn := form_inst_source hc hP hn
  have hQn := form_inst_source hc (successorFamily_form hc hP) hn
  have hs' := section_value hc (pi_body_form (has_form hs)) hs hn
  have hs'' : HasJ Γ (.app s n) (arr (inst P n) (inst P (.app succPoly n))) := by
    change HasJ Γ (.app s n) (inst (arr P (successorFamily P)) n) at hs'
    have eqt : inst (arr P (successorFamily P)) n =
        arr (inst P n) (inst (successorFamily P) n) := subst_arr _ _ _
    simpa only [eqt, successorFamily_at] using hs'
  exact arrow_congr hc hPn (by simpa only [successorFamily_at] using hQn)
    hs'' hx hy he

theorem section_at_variable {Γ : Tel} {P : Ty} {u : Poly}
    (hc : CtxJ Γ) (hP : FormJ (N :: Γ) P)
    (hu : HasJ Γ u (.pi N P)) :
    HasJ (N :: Γ) (.app (pren Nat.succ u) (.var 0)) P := by
  have cn := CtxJ.ext hc (N_form hc)
  have hn : HasJ (N :: Γ) (.var 0) N := .var (N_form cn) .zero
  have hP' := shifted_family_form hc hP (N_form hc)
  have hu' : HasJ (N :: Γ) (pren Nat.succ u) (.pi N (shiftedFamily P)) := by
    simpa only [wk, subst, N_subst, shiftedFamily] using has_wk hu hc (N_form hc)
  simpa only [shifted_at_var] using section_value cn hP' hu' hn

end JointCompletion.RecursorUniqueness
