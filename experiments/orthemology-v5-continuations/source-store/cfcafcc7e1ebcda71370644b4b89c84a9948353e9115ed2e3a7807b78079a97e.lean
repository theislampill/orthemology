import SubprobHellinger

noncomputable section
open scoped BigOperators
open Finset

namespace Orthemology.Tranche2
variable {Θ : Type*} {B : Θ → Type*} [∀ a, Fintype (B a)]

/-- Histories are newest first; each record contains the actually chosen experiment. -/
def dHistoryMass (K : (θ a : Θ) → B a → ℝ) (θ : Θ) : List (Sigma B) → ℝ
  | [] => 1
  | ⟨a,y⟩ :: h => dHistoryMass K θ h * K θ a y

def dHistoryAffinity (K : (θ a : Θ) → B a → ℝ) (θ σ : Θ) (h : List (Sigma B)) : ℝ :=
  Real.sqrt (dHistoryMass K θ h) * Real.sqrt (dHistoryMass K σ h)

omit [(a : Θ) → Fintype (B a)] in
lemma dHistoryMass_nonneg (K : (θ a : Θ) → B a → ℝ) (hK : ∀ θ a y, 0 ≤ K θ a y)
    (θ : Θ) (h : List (Sigma B)) : 0 ≤ dHistoryMass K θ h := by
  induction h with
  | nil => norm_num [dHistoryMass]
  | cons ay h ih => exact mul_nonneg ih (hK θ ay.1 ay.2)

omit [(a : Θ) → Fintype (B a)] in
lemma dHistoryAffinity_nonneg (K : (θ a : Θ) → B a → ℝ) (θ σ : Θ) (h : List (Sigma B)) :
    0 ≤ dHistoryAffinity K θ σ h := mul_nonneg (Real.sqrt_nonneg _) (Real.sqrt_nonneg _)

lemma dHistoryAffinity_branch_sum (K : (θ a : Θ) → B a → ℝ)
    (hK : ∀ θ a y, 0 ≤ K θ a y) (θ σ a : Θ) (h : List (Sigma B)) :
    ∑ y, dHistoryAffinity K θ σ (⟨a,y⟩::h) =
      dHistoryAffinity K θ σ h * affinity (K θ a) (K σ a) := by
  unfold dHistoryAffinity
  simp only [dHistoryMass]
  rw [affinity, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro y _
  rw [Real.sqrt_mul (dHistoryMass_nonneg K hK θ h),
    Real.sqrt_mul (dHistoryMass_nonneg K hK σ h)]
  ring

/-- Sum of actual true-model masses at leaves n steps beyond h. -/
def dLevelMass (K : (θ a : Θ) → B a → ℝ) (θ : Θ) (π : List (Sigma B) → Θ) :
    ℕ → List (Sigma B) → ℝ
  | 0, h => dHistoryMass K θ h
  | n+1, h => ∑ y, dLevelMass K θ π n (⟨π h,y⟩::h)

theorem dLevelMass_normalized (K : (θ a : Θ) → B a → ℝ)
    (hNorm : ∀ θ a, ∑ y, K θ a y = 1) (θ : Θ) (π : List (Sigma B) → Θ)
    (n : ℕ) (h : List (Sigma B)) : dLevelMass K θ π n h = dHistoryMass K θ h := by
  induction n generalizing h with
  | zero => rfl
  | succ n ih =>
    simp only [dLevelMass, ih, dHistoryMass, ← Finset.mul_sum, hNorm, mul_one]

/-- Exact finite-horizon expected number of selections of one candidate. -/
def dSelectedCost [DecidableEq Θ] (K : (θ a : Θ) → B a → ℝ) (θ σ : Θ)
    (π : List (Sigma B) → Θ) : ℕ → List (Sigma B) → ℝ
  | 0, _ => 0
  | n+1, h => (if π h = σ then dHistoryMass K θ h else 0) +
      ∑ y, dSelectedCost K θ σ π n (⟨π h,y⟩::h)

/-- The Hellinger affinity of the actual finite continuation transcripts. -/
def dLeafAffinity (K : (θ a : Θ) → B a → ℝ) (θ σ : Θ) (π : List (Sigma B) → Θ) :
    ℕ → List (Sigma B) → ℝ
  | 0, h => dHistoryAffinity K θ σ h
  | n+1, h => ∑ y, dLeafAffinity K θ σ π n (⟨π h,y⟩::h)

lemma dLeafAffinity_nonneg (K : (θ a : Θ) → B a → ℝ) (θ σ : Θ)
    (π : List (Sigma B) → Θ) (n : ℕ) (h : List (Sigma B)) :
    0 ≤ dLeafAffinity K θ σ π n h := by
  induction n generalizing h with
  | zero => exact dHistoryAffinity_nonneg K θ σ h
  | succ n ih => exact Finset.sum_nonneg (fun y _ => ih _)

omit [(a : Θ) → Fintype (B a)] in
lemma dMass_le_affinity_of_le (K : (θ a : Θ) → B a → ℝ)
    (hK : ∀ θ a y, 0 ≤ K θ a y) (θ σ : Θ) (h : List (Sigma B))
    (hle : dHistoryMass K θ h ≤ dHistoryMass K σ h) :
    dHistoryMass K θ h ≤ dHistoryAffinity K θ σ h := by
  have hm := dHistoryMass_nonneg K hK θ h
  have hr := Real.sqrt_le_sqrt hle
  have hs := mul_le_mul_of_nonneg_left hr (Real.sqrt_nonneg (dHistoryMass K θ h))
  have hsq := Real.sq_sqrt hm
  unfold dHistoryAffinity
  nlinarith

theorem dependent_hellinger_tree_budget [DecidableEq Θ] (K : (θ a : Θ) → B a → ℝ)
    (hK : ∀ θ a y, 0 ≤ K θ a y)
    (hSub : ∀ θ a, ∑ y, K θ a y ≤ 1)
    (θ σ : Θ) (π : List (Sigma B) → Θ)
    (hMLE : ∀ h, π h = σ → dHistoryMass K θ h ≤ dHistoryMass K σ h)
    (n : ℕ) (h : List (Sigma B)) :
    (1-affinity (K θ σ) (K σ σ)) * dSelectedCost K θ σ π n h +
      dLeafAffinity K θ σ π n h ≤ dHistoryAffinity K θ σ h := by
  let d := 1-affinity (K θ σ) (K σ σ)
  have hd : 0 ≤ d := sub_nonneg.mpr
    (affinity_le_one_subprob _ _ (hK θ σ) (hK σ σ) (hSub θ σ) (hSub σ σ))
  change d * dSelectedCost K θ σ π n h + dLeafAffinity K θ σ π n h ≤ _
  induction n generalizing h with
  | zero => simp [dSelectedCost, dLeafAffinity]
  | succ n ih =>
    have hstep : d * (if π h = σ then dHistoryMass K θ h else 0) +
        dHistoryAffinity K θ σ h * affinity (K θ (π h)) (K σ (π h)) ≤
          dHistoryAffinity K θ σ h := by
      by_cases heq : π h = σ
      · rw [if_pos heq, heq]
        have hm := dMass_le_affinity_of_le K hK θ σ h (hMLE h heq)
        have hdscale := mul_le_mul_of_nonneg_left hm hd
        dsimp [d] at hdscale ⊢
        nlinarith
      · rw [if_neg heq, mul_zero, zero_add]
        exact mul_le_of_le_one_right (dHistoryAffinity_nonneg K θ σ h)
          (affinity_le_one_subprob _ _ (hK θ (π h)) (hK σ (π h))
            (hSub θ (π h)) (hSub σ (π h)))
    calc
      d * dSelectedCost K θ σ π (n+1) h + dLeafAffinity K θ σ π (n+1) h =
          d * (if π h = σ then dHistoryMass K θ h else 0) +
          ∑ y, (d * dSelectedCost K θ σ π n (⟨π h,y⟩::h) +
            dLeafAffinity K θ σ π n (⟨π h,y⟩::h)) := by
        simp only [dSelectedCost, dLeafAffinity, mul_add, Finset.mul_sum, Finset.sum_add_distrib]
        ring
      _ ≤ d * (if π h = σ then dHistoryMass K θ h else 0) +
          ∑ y, dHistoryAffinity K θ σ (⟨π h,y⟩::h) := by
        exact add_le_add_left (Finset.sum_le_sum (fun y _ => ih _)) _
      _ = d * (if π h = σ then dHistoryMass K θ h else 0) +
          dHistoryAffinity K θ σ h * affinity (K θ (π h)) (K σ (π h)) := by
        rw [dHistoryAffinity_branch_sum K hK]
      _ ≤ dHistoryAffinity K θ σ h := hstep


theorem dSelectedCost_subprob_uniform_bound [DecidableEq Θ] (K : (θ a : Θ) → B a → ℝ)
    (hK : ∀ θ a y, 0 ≤ K θ a y)
    (hSub : ∀ θ a, ∑ y, K θ a y ≤ 1)
    (θ σ : Θ) (π : List (Sigma B) → Θ)
    (hMLE : ∀ h, π h = σ → dHistoryMass K θ h ≤ dHistoryMass K σ h)
    (hDef : affinity (K θ σ) (K σ σ) < 1) (n : ℕ) :
    dSelectedCost K θ σ π n [] ≤ 1 / (1-affinity (K θ σ) (K σ σ)) := by
  have hpos := sub_pos.mpr hDef
  have hb := dependent_hellinger_tree_budget K hK hSub θ σ π hMLE n []
  have hn := dLeafAffinity_nonneg K θ σ π n []
  have hroot : dHistoryAffinity K θ σ [] = 1 := by simp [dHistoryAffinity, dHistoryMass]
  rw [hroot] at hb
  apply (le_div_iff₀ hpos).mpr
  nlinarith

end Orthemology.Tranche2
