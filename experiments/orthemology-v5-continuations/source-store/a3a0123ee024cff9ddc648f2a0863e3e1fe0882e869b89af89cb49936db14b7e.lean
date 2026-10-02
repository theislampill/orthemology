import ResetBudget
import StoppedPhasePolicy

noncomputable section
open scoped BigOperators
open Finset

namespace Orthemology.Tranche2
variable {Θ : Type*} {B : Θ → Type*} [Fintype Θ] [∀ a, Fintype (B a)] [DecidableEq Θ]

def weightedHellinger (K : (θ a : Θ) → B a → ℝ) (θ : Θ) (w : Θ → ℝ)
    (h : List (Sigma B)) : ℝ := ∑ σ, w σ * dHistoryAffinity K θ σ h

omit [DecidableEq Θ] in
omit [(a : Θ) → Fintype (B a)] in
lemma weightedHellinger_nonneg (K : (θ a : Θ) → B a → ℝ) (θ : Θ) (w : Θ → ℝ)
    (hw : ∀ σ, 0 ≤ w σ) (h : List (Sigma B)) : 0 ≤ weightedHellinger K θ w h :=
  Finset.sum_nonneg (fun σ _ => mul_nonneg (hw σ) (dHistoryAffinity_nonneg K θ σ h))

omit [(a : Θ) → Fintype (B a)] [DecidableEq Θ] in
lemma weightedHellinger_root (K : (θ a : Θ) → B a → ℝ) (θ : Θ) (w : Θ → ℝ) :
    weightedHellinger K θ w [] = ∑ σ, w σ := by
  simp [weightedHellinger, dHistoryAffinity, dHistoryMass]

omit [DecidableEq Θ] in
/-- The local drift is derived from the actual killed experiment kernels. The
coefficient condition is a finite numerical certificate, not a stochastic
convergence assumption. It permits zero coefficients for non-live candidates. -/
theorem weightedHellinger_step (K : (θ a : Θ) → B a → ℝ)
    (hK : ∀ θ a y, 0 ≤ K θ a y) (hSub : ∀ θ a, ∑ y, K θ a y ≤ 1)
    (θ : Θ) (π : List (Sigma B) → Θ) (w cost : Θ → ℝ)
    (hw : ∀ σ, 0 ≤ w σ)
    (hMLE : ∀ h, dHistoryMass K θ h ≤ dHistoryMass K (π h) h)
    (hWeight : ∀ h, cost (π h) ≤ w (π h) * (1-affinity (K θ (π h)) (K (π h) (π h))))
    (h : List (Sigma B)) :
    cost (π h) * dHistoryMass K θ h + ∑ y, weightedHellinger K θ w (⟨π h,y⟩::h) ≤
      weightedHellinger K θ w h := by
  let a := π h
  let H := fun σ => dHistoryAffinity K θ σ h
  let r := fun σ => affinity (K θ a) (K σ a)
  have hH : ∀ σ, 0 ≤ H σ := fun σ => dHistoryAffinity_nonneg K θ σ h
  have hr : ∀ σ, r σ ≤ 1 := fun σ => affinity_le_one_subprob _ _ (hK θ a) (hK σ a) (hSub θ a) (hSub σ a)
  have hm := dMass_le_affinity_of_le K hK θ a h (hMLE h)
  have h1 := mul_le_mul_of_nonneg_right (hWeight h) (dHistoryMass_nonneg K hK θ h)
  have h2 := mul_le_mul_of_nonneg_left hm (mul_nonneg (hw a) (sub_nonneg.mpr (hr a)))
  have hterm : cost a * dHistoryMass K θ h ≤ w a * H a * (1-r a) := by
    dsimp [a, H, r] at *
    nlinarith
  have hsum : w a * H a * (1-r a) ≤ ∑ σ, w σ * H σ * (1-r σ) :=
    Finset.single_le_sum (fun σ _ => mul_nonneg (mul_nonneg (hw σ) (hH σ)) (sub_nonneg.mpr (hr σ))) (Finset.mem_univ a)
  have hbranch : (∑ y, weightedHellinger K θ w (⟨a,y⟩::h)) = ∑ σ, w σ * H σ * r σ := by
    simp only [weightedHellinger]
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro σ _
    rw [← Finset.mul_sum, dHistoryAffinity_branch_sum K hK]
    dsimp [H, r]
    ring
  change cost a * dHistoryMass K θ h + _ ≤ _
  rw [hbranch]
  have hid : (∑ σ, w σ * H σ * (1-r σ)) + (∑ σ, w σ * H σ * r σ) = weightedHellinger K θ w h := by
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro σ _
    dsimp [H]
    ring
  linarith

omit [Fintype Θ] [DecidableEq Θ] in
/-- Deficit weights discharge the finite coefficient certificate whenever each
positive cost has strictly positive residual Hellinger deficit. -/
theorem deficit_weight_certificate (r cost : Θ → ℝ)
    (hcost : ∀ σ, 0 ≤ cost σ) (hr : ∀ σ, 0 < cost σ → r σ < 1) (σ : Θ) :
    let w := fun σ => if 0 < cost σ then cost σ / (1-r σ) else 0
    0 ≤ w σ ∧ cost σ ≤ w σ * (1-r σ) := by
  dsimp only
  split_ifs with hp
  · have hd := sub_pos.mpr (hr σ hp)
    constructor
    · exact div_nonneg (hcost σ) hd.le
    · rw [div_mul_cancel₀ _ hd.ne']
  · have hz : cost σ = 0 := le_antisymm (le_of_not_gt hp) (hcost σ)
    simp [hz]

end Orthemology.Tranche2
