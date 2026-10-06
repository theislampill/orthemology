import Mathlib.Data.ENNReal.Real
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Tactic
noncomputable section
open scoped ENNReal
namespace Orthemology.AffineTail

/-- Constants for optimizing a linear charged-interval budget. -/
def offset (D lam α β A c : ℝ) : ℝ :=
  (D/lam)*((α*(1+Real.log (2*A)/c)+β)*Real.log 2+Real.log 2)
def slope (D lam α c : ℝ) : ℝ := (D/lam)*(α*Real.log 2/c+1)

theorem optimized_affine_tail
    (f : ℝ → ℝ≥0∞) (D lam α β A c : ℝ)
    (hD : 0 < D) (hlam : 0 < lam) (hα : 0 ≤ α) (hβ : 0 ≤ β)
    (hA : 1 ≤ A) (hc : 0 < c)
    (htail : ∀ N : ℕ, 1 ≤ N → ∀ t : ℝ, 0 ≤ t →
      f t ≤ ENNReal.ofReal (A*Real.exp (-c*(N:ℝ)) +
        Real.exp ((α*(N:ℝ)+β)*Real.log 2-lam*t/D))) :
    ∀ u : ℝ, 0 ≤ u →
      f (offset D lam α β A c+slope D lam α c*u) ≤ ENNReal.ofReal (Real.exp (-u)) := by
  intro u hu
  have hAp : 0 < A := by linarith
  have hlog : 0 < Real.log (2*A) := Real.log_pos (by nlinarith)
  have hlog2 : 0 < Real.log 2 := Real.log_pos (by norm_num)
  let x := (Real.log (2*A)+u)/c
  have hx : 0 < x := div_pos (by linarith) hc
  let N := Nat.ceil x
  have hN : 1 ≤ N := Nat.ceil_pos.mpr hx
  have hNx : (N:ℝ) ≤ x+1 := (Nat.ceil_lt_add_one hx.le).le
  have hxN : x ≤ (N:ℝ) := Nat.le_ceil x
  have hcN : Real.log (2*A)+u ≤ c*(N:ℝ) := by
    have hh := (div_le_iff₀ hc).mp hxN
    nlinarith
  have ht : 0 ≤ offset D lam α β A c+slope D lam α c*u := by
    dsimp [offset,slope]
    positivity
  apply (htail N hN _ ht).trans
  have hexp : Real.exp (-Real.log 2-u) = Real.exp (-u)/2 := by
    rw [sub_eq_add_neg, Real.exp_add, Real.exp_neg, Real.exp_log (by norm_num : (0:ℝ)<2)]
    ring
  have hfirst : A*Real.exp (-c*(N:ℝ)) ≤ Real.exp (-u)/2 := by
    have hlogmul : Real.log (2*A)=Real.log 2+Real.log A :=
      Real.log_mul (by norm_num) hAp.ne'
    have hh : Real.log A-c*(N:ℝ) ≤ -Real.log 2-u := by rw [hlogmul] at hcN; linarith
    have he := Real.exp_le_exp.mpr hh
    rw [Real.exp_sub, Real.exp_log hAp,hexp] at he
    simpa [Real.exp_neg,div_eq_mul_inv] using he
  have htime : lam*(offset D lam α β A c+slope D lam α c*u)/D =
      (α*(x+1)+β)*Real.log 2+Real.log 2+u := by
    dsimp [offset,slope,x]
    field_simp
    ring
  have hsecond : Real.exp ((α*(N:ℝ)+β)*Real.log 2-
      lam*(offset D lam α β A c+slope D lam α c*u)/D) ≤ Real.exp (-u)/2 := by
    rw [htime,← hexp]
    apply Real.exp_le_exp.mpr
    have hn := mul_le_mul_of_nonneg_left hNx hα
    have hh := mul_le_mul_of_nonneg_right hn hlog2.le
    nlinarith
  apply ENNReal.ofReal_le_ofReal
  linarith

#print axioms optimized_affine_tail
end Orthemology.AffineTail
