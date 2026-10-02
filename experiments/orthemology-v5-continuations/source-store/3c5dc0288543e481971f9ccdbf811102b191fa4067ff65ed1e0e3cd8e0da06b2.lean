import dependencies.StatisticalRepair
import Mathlib.Topology.Instances.ENNReal.Lemmas

/-!
# Finite transcript-tree Hellinger budget

Shared causal selection generates each child from the same recorded history.
The branch identity is derived from actual kernel products. No supermartingale
decrement or conditional expectation formula is assumed as an input.
-/

noncomputable section
open scoped BigOperators
open Finset

namespace Orthemology.Tranche2

lemma affinity_sq_distance {B : Type*} [Fintype B] (p q : B → ℝ)
    (hp : ∀ y, 0 ≤ p y) (hq : ∀ y, 0 ≤ q y)
    (hsp : ∑ y, p y = 1) (hsq : ∑ y, q y = 1) :
    ∑ y, (Real.sqrt (p y) - Real.sqrt (q y)) ^ 2 = 2 - 2 * affinity p q := by
  calc
    (∑ y, (Real.sqrt (p y) - Real.sqrt (q y)) ^ 2) =
        ∑ y, (p y + q y - 2 * (Real.sqrt (p y) * Real.sqrt (q y))) := by
      apply Finset.sum_congr rfl
      intro y _
      nlinarith [Real.sq_sqrt (hp y), Real.sq_sqrt (hq y)]
    _ = 2 - 2 * affinity p q := by
      simp only [Finset.sum_sub_distrib, Finset.sum_add_distrib, ← Finset.mul_sum,
        hsp, hsq, affinity]
      ring

lemma affinity_le_one {B : Type*} [Fintype B] (p q : B → ℝ)
    (hp : ∀ y, 0 ≤ p y) (hq : ∀ y, 0 ≤ q y)
    (hsp : ∑ y, p y = 1) (hsq : ∑ y, q y = 1) : affinity p q ≤ 1 := by
  have hn : 0 ≤ ∑ y, (Real.sqrt (p y) - Real.sqrt (q y)) ^ 2 :=
    Finset.sum_nonneg (fun y _ => sq_nonneg _)
  rw [affinity_sq_distance p q hp hq hsp hsq] at hn
  linarith

lemma affinity_lt_one {B : Type*} [Fintype B] (p q : B → ℝ)
    (hp : ∀ y, 0 ≤ p y) (hq : ∀ y, 0 ≤ q y)
    (hsp : ∑ y, p y = 1) (hsq : ∑ y, q y = 1) (hne : p ≠ q) :
    affinity p q < 1 := by
  classical
  obtain ⟨y, hy⟩ : ∃ y, p y ≠ q y := by
    by_contra! h
    exact hne (funext h)
  have hroot : Real.sqrt (p y) - Real.sqrt (q y) ≠ 0 := by
    intro h
    have heq : Real.sqrt (p y) = Real.sqrt (q y) := sub_eq_zero.mp h
    apply hy
    have hsq := congrArg (fun x : ℝ => x^2) heq
    simpa only [Real.sq_sqrt (hp y), Real.sq_sqrt (hq y)] using hsq
  have hs : 0 < ∑ z, (Real.sqrt (p z) - Real.sqrt (q z)) ^ 2 :=
    Finset.sum_pos' (fun z _ => sq_nonneg _) ⟨y, Finset.mem_univ _, sq_pos_of_ne_zero hroot⟩
  rw [affinity_sq_distance p q hp hq hsp hsq] at hs
  linarith

variable {Θ B : Type*} [Fintype B]

/-- Histories are newest first; each record contains the actually chosen experiment. -/
def historyMass (K : Θ → Θ → B → ℝ) (θ : Θ) : List (Θ × B) → ℝ
  | [] => 1
  | (a,y) :: h => historyMass K θ h * K θ a y

def historyAffinity (K : Θ → Θ → B → ℝ) (θ σ : Θ) (h : List (Θ × B)) : ℝ :=
  Real.sqrt (historyMass K θ h) * Real.sqrt (historyMass K σ h)

omit [Fintype B] in
lemma historyMass_nonneg (K : Θ → Θ → B → ℝ) (hK : ∀ θ a y, 0 ≤ K θ a y)
    (θ : Θ) (h : List (Θ × B)) : 0 ≤ historyMass K θ h := by
  induction h with
  | nil => norm_num [historyMass]
  | cons ay h ih => exact mul_nonneg ih (hK θ ay.1 ay.2)

omit [Fintype B] in
lemma historyAffinity_nonneg (K : Θ → Θ → B → ℝ) (θ σ : Θ) (h : List (Θ × B)) :
    0 ≤ historyAffinity K θ σ h := mul_nonneg (Real.sqrt_nonneg _) (Real.sqrt_nonneg _)

lemma historyAffinity_branch_sum (K : Θ → Θ → B → ℝ)
    (hK : ∀ θ a y, 0 ≤ K θ a y) (θ σ a : Θ) (h : List (Θ × B)) :
    ∑ y, historyAffinity K θ σ ((a,y)::h) =
      historyAffinity K θ σ h * affinity (K θ a) (K σ a) := by
  unfold historyAffinity
  simp only [historyMass]
  rw [affinity, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro y _
  rw [Real.sqrt_mul (historyMass_nonneg K hK θ h),
    Real.sqrt_mul (historyMass_nonneg K hK σ h)]
  ring

/-- Sum of actual true-model masses at leaves n steps beyond h. -/
def levelMass (K : Θ → Θ → B → ℝ) (θ : Θ) (π : List (Θ × B) → Θ) :
    ℕ → List (Θ × B) → ℝ
  | 0, h => historyMass K θ h
  | n+1, h => ∑ y, levelMass K θ π n ((π h,y)::h)

theorem levelMass_normalized (K : Θ → Θ → B → ℝ)
    (hNorm : ∀ θ a, ∑ y, K θ a y = 1) (θ : Θ) (π : List (Θ × B) → Θ)
    (n : ℕ) (h : List (Θ × B)) : levelMass K θ π n h = historyMass K θ h := by
  induction n generalizing h with
  | zero => rfl
  | succ n ih =>
    simp only [levelMass, ih, historyMass, ← Finset.mul_sum, hNorm, mul_one]

/-- Exact finite-horizon expected number of selections of one candidate. -/
def selectedCost [DecidableEq Θ] (K : Θ → Θ → B → ℝ) (θ σ : Θ)
    (π : List (Θ × B) → Θ) : ℕ → List (Θ × B) → ℝ
  | 0, _ => 0
  | n+1, h => (if π h = σ then historyMass K θ h else 0) +
      ∑ y, selectedCost K θ σ π n ((π h,y)::h)

/-- The Hellinger affinity of the actual finite continuation transcripts. -/
def leafAffinity (K : Θ → Θ → B → ℝ) (θ σ : Θ) (π : List (Θ × B) → Θ) :
    ℕ → List (Θ × B) → ℝ
  | 0, h => historyAffinity K θ σ h
  | n+1, h => ∑ y, leafAffinity K θ σ π n ((π h,y)::h)

lemma leafAffinity_nonneg (K : Θ → Θ → B → ℝ) (θ σ : Θ)
    (π : List (Θ × B) → Θ) (n : ℕ) (h : List (Θ × B)) :
    0 ≤ leafAffinity K θ σ π n h := by
  induction n generalizing h with
  | zero => exact historyAffinity_nonneg K θ σ h
  | succ n ih => exact Finset.sum_nonneg (fun y _ => ih _)

omit [Fintype B] in
lemma mass_le_affinity_of_le (K : Θ → Θ → B → ℝ)
    (hK : ∀ θ a y, 0 ≤ K θ a y) (θ σ : Θ) (h : List (Θ × B))
    (hle : historyMass K θ h ≤ historyMass K σ h) :
    historyMass K θ h ≤ historyAffinity K θ σ h := by
  have hm := historyMass_nonneg K hK θ h
  have hr := Real.sqrt_le_sqrt hle
  have hs := mul_le_mul_of_nonneg_left hr (Real.sqrt_nonneg (historyMass K θ h))
  have hsq := Real.sq_sqrt hm
  unfold historyAffinity
  nlinarith

/-- Finite-tree budget derived from actual branch laws and the local MLE rule. -/
theorem hellinger_tree_budget [DecidableEq Θ] (K : Θ → Θ → B → ℝ)
    (hK : ∀ θ a y, 0 ≤ K θ a y)
    (hNorm : ∀ θ a, ∑ y, K θ a y = 1)
    (θ σ : Θ) (π : List (Θ × B) → Θ)
    (hMLE : ∀ h, π h = σ → historyMass K θ h ≤ historyMass K σ h)
    (n : ℕ) (h : List (Θ × B)) :
    (1-affinity (K θ σ) (K σ σ)) * selectedCost K θ σ π n h +
      leafAffinity K θ σ π n h ≤ historyAffinity K θ σ h := by
  let d := 1-affinity (K θ σ) (K σ σ)
  have hd : 0 ≤ d := sub_nonneg.mpr
    (affinity_le_one _ _ (hK θ σ) (hK σ σ) (hNorm θ σ) (hNorm σ σ))
  change d * selectedCost K θ σ π n h + leafAffinity K θ σ π n h ≤ _
  induction n generalizing h with
  | zero => simp [selectedCost, leafAffinity]
  | succ n ih =>
    have hstep : d * (if π h = σ then historyMass K θ h else 0) +
        historyAffinity K θ σ h * affinity (K θ (π h)) (K σ (π h)) ≤
          historyAffinity K θ σ h := by
      by_cases heq : π h = σ
      · rw [if_pos heq, heq]
        have hm := mass_le_affinity_of_le K hK θ σ h (hMLE h heq)
        have hdscale := mul_le_mul_of_nonneg_left hm hd
        dsimp [d] at hdscale ⊢
        nlinarith
      · rw [if_neg heq, mul_zero, zero_add]
        exact mul_le_of_le_one_right (historyAffinity_nonneg K θ σ h)
          (affinity_le_one _ _ (hK θ (π h)) (hK σ (π h))
            (hNorm θ (π h)) (hNorm σ (π h)))
    calc
      d * selectedCost K θ σ π (n+1) h + leafAffinity K θ σ π (n+1) h =
          d * (if π h = σ then historyMass K θ h else 0) +
          ∑ y, (d * selectedCost K θ σ π n ((π h,y)::h) +
            leafAffinity K θ σ π n ((π h,y)::h)) := by
        simp only [selectedCost, leafAffinity, mul_add, Finset.mul_sum, Finset.sum_add_distrib]
        ring
      _ ≤ d * (if π h = σ then historyMass K θ h else 0) +
          ∑ y, historyAffinity K θ σ ((π h,y)::h) := by
        exact add_le_add_left (Finset.sum_le_sum (fun y _ => ih _)) _
      _ = d * (if π h = σ then historyMass K θ h else 0) +
          historyAffinity K θ σ h * affinity (K θ (π h)) (K σ (π h)) := by
        rw [historyAffinity_branch_sum K hK]
      _ ≤ historyAffinity K θ σ h := hstep

theorem selectedCost_uniform_bound [DecidableEq Θ] (K : Θ → Θ → B → ℝ)
    (hK : ∀ θ a y, 0 ≤ K θ a y)
    (hNorm : ∀ θ a, ∑ y, K θ a y = 1)
    (θ σ : Θ) (π : List (Θ × B) → Θ)
    (hMLE : ∀ h, π h = σ → historyMass K θ h ≤ historyMass K σ h)
    (hne : K θ σ ≠ K σ σ) (n : ℕ) :
    selectedCost K θ σ π n [] ≤ 1 / (1-affinity (K θ σ) (K σ σ)) := by
  have hpos : 0 < 1-affinity (K θ σ) (K σ σ) := sub_pos.mpr
    (affinity_lt_one _ _ (hK θ σ) (hK σ σ) (hNorm θ σ) (hNorm σ σ) hne)
  have hb := hellinger_tree_budget K hK hNorm θ σ π hMLE n []
  have hn := leafAffinity_nonneg K θ σ π n []
  have hroot : historyAffinity K θ σ [] = 1 := by simp [historyAffinity, historyMass]
  rw [hroot] at hb
  apply (le_div_iff₀ hpos).mpr
  nlinarith

/-- Supremum of all finite expected counts is still bounded. Its interpretation
as infinite expected count uses the standard monotone-count construction. -/
theorem selectedCost_iSup_bound [DecidableEq Θ] (K : Θ → Θ → B → ℝ)
    (hK : ∀ θ a y, 0 ≤ K θ a y)
    (hNorm : ∀ θ a, ∑ y, K θ a y = 1)
    (θ σ : Θ) (π : List (Θ × B) → Θ)
    (hMLE : ∀ h, π h = σ → historyMass K θ h ≤ historyMass K σ h)
    (hne : K θ σ ≠ K σ σ) :
    (⨆ n, ENNReal.ofReal (selectedCost K θ σ π n [])) ≤
      ENNReal.ofReal (1 / (1-affinity (K θ σ) (K σ σ))) := by
  exact iSup_le (fun n => ENNReal.ofReal_le_ofReal
    (selectedCost_uniform_bound K hK hNorm θ σ π hMLE hne n))

end Orthemology.Tranche2
