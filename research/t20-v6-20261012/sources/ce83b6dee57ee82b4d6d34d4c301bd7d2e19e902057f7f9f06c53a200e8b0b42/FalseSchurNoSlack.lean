import Mathlib.Data.Real.Basic
import Mathlib.Data.Matrix.Block
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

set_option linter.unusedSectionVars false
open Matrix
namespace FullFunctionalSchur

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

def Positive (A : Matrix ι ι ℝ) : Prop := ∀ u : ι → ℝ, u ≠ 0 → 0 < u ⬝ᵥ A *ᵥ u

def extendA (A : Matrix ι ι ℝ) (v : ι → ℝ) (d : ℝ) : Matrix (ι ⊕ Unit) (ι ⊕ Unit) ℝ :=
  fromBlocks A (fun i _ => v i) (fun _ j => v j) (fun _ _ => d)

def extendB (B : Matrix ι ι ℝ) (w : ι → ℝ) : Matrix (ι ⊕ Unit) (ι ⊕ Unit) ℝ :=
  fromBlocks (B + vecMulVec w w) (fun i _ => -w i) (fun _ j => -w j) (fun _ _ => 1)

theorem quadratic_extend (A : Matrix ι ι ℝ) (v u : ι → ℝ) (d t : ℝ) :
    Sum.elim u (fun _ : Unit => t) ⬝ᵥ extendA A v d *ᵥ Sum.elim u (fun _ : Unit => t) =
      u ⬝ᵥ A *ᵥ u + 2 * t * (u ⬝ᵥ v) + d * t^2 := by
  simp only [extendA, fromBlocks_mulVec, Function.comp_def, Sum.elim_inl, Sum.elim_inr]
  simp only [sumElim_dotProduct_sumElim, dotProduct_add]
  have hc : (fun i (_ : Unit) => v i) *ᵥ (fun _ => t) = t • v := by
    ext i
    simp [mulVec, dotProduct, mul_comm]
  rw [hc, dotProduct_smul]
  simp only [smul_eq_mul]
  simp only [mulVec, dotProduct, Fintype.sum_unique, mul_comm t, mul_comm (v _)]
  ring

theorem symmetric_pair (A : Matrix ι ι ℝ) (hA : Aᵀ = A) (u w : ι → ℝ) :
    w ⬝ᵥ A *ᵥ u = u ⬝ᵥ A *ᵥ w := by
  rw [dotProduct_mulVec, ← mulVec_transpose, hA, dotProduct_comm]

theorem completed_square (A : Matrix ι ι ℝ) (hA : Aᵀ = A)
    (v w u : ι → ℝ) (hAw : A *ᵥ w = v) (t : ℝ) :
    Sum.elim u (fun _ : Unit => t) ⬝ᵥ extendA A v (v ⬝ᵥ w) *ᵥ
      Sum.elim u (fun _ : Unit => t) =
      (u + t • w) ⬝ᵥ A *ᵥ (u + t • w) + t^2 := by
  rw [quadratic_extend, mulVec_add, mulVec_smul, dotProduct_add, add_dotProduct,
    add_dotProduct, dotProduct_smul, dotProduct_smul, smul_dotProduct, smul_dotProduct]
  rw [symmetric_pair A hA u w, hAw, dotProduct_comm w v]
  simp only [smul_eq_mul]
  ring

theorem positive_nonneg (A : Matrix ι ι ℝ) (hA : Positive A) (u : ι → ℝ) :
    0 ≤ u ⬝ᵥ A *ᵥ u := by
  by_cases hu : u = 0
  · simp [hu]
  · exact le_of_lt (hA u hu)

theorem extend_positive (A : Matrix ι ι ℝ) (hAs : Aᵀ = A) (hAp : Positive A)
    (v w : ι → ℝ) (hAw : A *ᵥ w = v) :
    Positive (extendA A v (v ⬝ᵥ w)) := by
  intro x hx
  let u : ι → ℝ := fun i => x (Sum.inl i)
  let t : ℝ := x (Sum.inr ())
  have he : x = Sum.elim u (fun _ : Unit => t) := by
    funext i
    cases i with
    | inl i => rfl
    | inr i => cases i; rfl
  rw [he, completed_square A hAs v w u hAw t]
  by_cases ht : t = 0
  · have hu : u ≠ 0 := by
      intro hu
      apply hx
      rw [he, hu, ht]
      ext i
      cases i <;> rfl
    simpa [ht] using hAp u hu
  · exact add_pos_of_nonneg_of_pos (positive_nonneg A hAp _) (sq_pos_of_ne_zero ht)

theorem extendA_symmetric (A : Matrix ι ι ℝ) (hA : Aᵀ = A) (v : ι → ℝ) (d : ℝ) :
    (extendA A v d)ᵀ = extendA A v d := by
  ext i j
  cases i <;> cases j <;> simp [extendA, transpose_apply]
  exact congrFun (congrFun hA _) _

theorem extendB_symmetric (B : Matrix ι ι ℝ) (hB : Bᵀ = B) (w : ι → ℝ) :
    (extendB B w)ᵀ = extendB B w := by
  ext i j
  cases i <;> cases j <;> simp [extendB, transpose_apply, vecMulVec, mul_comm]
  exact congrFun (congrFun hB _) _

theorem extendA_action (A : Matrix ι ι ℝ) (v u : ι → ℝ) (d t : ℝ) :
    extendA A v d *ᵥ Sum.elim u (fun _ : Unit => t) =
    Sum.elim (A *ᵥ u + t • v) (fun _ : Unit => v ⬝ᵥ u + d*t) := by
  ext i
  cases i <;> simp [extendA, mulVec, dotProduct, Finset.mul_sum, mul_comm]

theorem extendB_action (B : Matrix ι ι ℝ) (w u : ι → ℝ) (t : ℝ) :
    extendB B w *ᵥ Sum.elim u (fun _ : Unit => t) =
    Sum.elim (B *ᵥ u + (w ⬝ᵥ u - t) • w) (fun _ : Unit => t - w ⬝ᵥ u) := by
  ext i
  cases i with
  | inl i =>
    simp [extendB, mulVec, dotProduct, vecMulVec, add_mul, Finset.sum_add_distrib,
      ← Finset.mul_sum, mul_assoc]
    ring
  | inr i =>
    simp [extendB, mulVec, dotProduct, Finset.sum_neg_distrib]
    ring

theorem extend_inverse_action (A B : Matrix ι ι ℝ)
    (hB : Bᵀ = B) (hAB : A * B = 1) (v : ι → ℝ) (x : ι ⊕ Unit → ℝ) :
    extendA A v (1 + v ⬝ᵥ B *ᵥ v) *ᵥ (extendB B (B *ᵥ v) *ᵥ x) = x := by
  let u : ι → ℝ := fun i => x (Sum.inl i)
  let t : ℝ := x (Sum.inr ())
  have he : x = Sum.elim u (fun _ : Unit => t) := by
    funext i
    cases i with
    | inl i => rfl
    | inr i => cases i; rfl
  have hAv : A *ᵥ (B *ᵥ v) = v := by rw [mulVec_mulVec, hAB, one_mulVec]
  have hAu : A *ᵥ (B *ᵥ u) = u := by rw [mulVec_mulVec, hAB, one_mulVec]
  have hBu : v ⬝ᵥ B *ᵥ u = (B *ᵥ v) ⬝ᵥ u := by
    rw [dotProduct_mulVec, ← mulVec_transpose, hB]
  rw [he, extendB_action, extendA_action, mulVec_add, mulVec_smul, hAu, hAv]
  ext i
  cases i with
  | inl i => simp only [Sum.elim_inl, Pi.add_apply, Pi.smul_apply, smul_eq_mul]; ring
  | inr i =>
    simp only [Sum.elim_inr, dotProduct_add, dotProduct_smul, smul_eq_mul, hBu]
    ring

theorem extend_inverse (A B : Matrix ι ι ℝ)
    (hB : Bᵀ = B) (hAB : A * B = 1) (v : ι → ℝ) :
    extendA A v (1 + v ⬝ᵥ B *ᵥ v) * extendB B (B *ᵥ v) = 1 := by
  apply Matrix.ext_of_mulVec_single
  intro j
  rw [← mulVec_mulVec, extend_inverse_action A B hB hAB, one_mulVec]

end FullFunctionalSchur
