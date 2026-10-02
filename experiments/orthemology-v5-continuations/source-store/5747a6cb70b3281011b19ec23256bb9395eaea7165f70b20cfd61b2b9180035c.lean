import FrozenRotorProgress

noncomputable section
open MeasureTheory
namespace HiddenParity.Cost.FrontierControls
universe u w
open FiniteChainHitting

/-- The exact bad-to-good geometric test chain, including the p=0 boundary. -/
def geometricRows (p : ℝ) (hp : 0 ≤ p) (hp1 : p ≤ 1) : Rows Bool where
  row s t := if s then (if t then 1 else 0) else (if t then p else 1-p)
  nonneg s t := by cases s <;> cases t <;> simp <;> linarith
  normalized s := by cases s <;> simp

theorem geometric_survival_exact (p : ℝ) (hp : 0 ≤ p) (hp1 : p ≤ 1) (n : ℕ) :
    survive (geometricRows p hp hp1) (fun b : Bool => b=true) n false=(1-p)^n := by
  induction n with
  | zero => simp [survive]
  | succ n ih =>
      simp only [survive,Bool.false_eq_true,if_false]
      rw [Fintype.sum_bool]
      change p * survive (geometricRows p hp hp1) (fun b : Bool => b=true) n true +
        (1-p)*survive (geometricRows p hp hp1) (fun b : Bool => b=true) n false = _
      rw [ih,survive_of_goal (geometricRows p hp hp1) (fun b : Bool => b=true) n true rfl]
      ring

theorem zero_exit_keeps_survival_one (n : ℕ) :
    survive (geometricRows 0 (by norm_num) (by norm_num)) (fun b : Bool => b=true) n false=1 := by
  simpa using geometric_survival_exact 0 (by norm_num) (by norm_num) n

theorem positive_exit_survival_is_actual_probability (p : ℝ) (hp : 0 ≤ p) (hp1 : p ≤ 1) (n : ℕ) :
    (absorbedLaw (geometricRows p hp hp1) (fun b : Bool => b=true) n false).toMeasure {b | b≠true} =
      ENNReal.ofReal ((1-p)^n) := by
  rw [absorbedLaw_survival,geometric_survival_exact]

open HiddenParity.Sufficiency HiddenParity.Stochastic
/-- The concrete killed rotor law respects pre-stop before any receipt; the
result does not depend on an evaluation of its opaque finite enumeration. -/
theorem every_true_prestop_kills
    {State Action : Type u} {Model : Type w} [Fintype State] [Fintype Action]
    [DecidableEq State] [DecidableEq Action] [Inhabited State] [DecidableEq Model]
    [MeasurableSpace State] [MeasurableSingletonClass State]
    [MeasurableSpace Action] [MeasurableSingletonClass Action]
    (P : RationalKernel Model (State × Action) State) (σ : Model)
    (F : Finset (State × Action)) (fallback : Action) (s₀ s : State)
    (r : FrozenRotor.Residues F) (after : State × Action → State → Prop) :
    (FrozenRotor.kernel F fallback s₀ (fun _ => True) after P σ).row (some (s,r)) none=1 :=
  FrozenRotor.pre_stop_kills F fallback s₀ (fun _ => True) after P σ s r (Or.inr trivial)

end HiddenParity.Cost.FrontierControls
