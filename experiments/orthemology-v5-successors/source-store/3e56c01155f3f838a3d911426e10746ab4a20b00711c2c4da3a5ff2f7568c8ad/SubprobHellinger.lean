import HellingerTree

noncomputable section
open scoped BigOperators
open Finset

namespace Orthemology.Tranche2

lemma affinity_sq_le_mass_product {B : Type*} [Fintype B] (p q : B → ℝ)
    (hp : ∀ y, 0 ≤ p y) (hq : ∀ y, 0 ≤ q y) :
    affinity p q ^ 2 ≤ (∑ y, p y) * (∑ y, q y) := by
  have h := Finset.sum_mul_sq_le_sq_mul_sq Finset.univ
    (fun y => Real.sqrt (p y)) (fun y => Real.sqrt (q y))
  simpa only [affinity, Real.sq_sqrt, hp, hq] using h

lemma affinity_le_one_subprob {B : Type*} [Fintype B] (p q : B → ℝ)
    (hp : ∀ y, 0 ≤ p y) (hq : ∀ y, 0 ≤ q y)
    (hsp : ∑ y, p y ≤ 1) (hsq : ∑ y, q y ≤ 1) : affinity p q ≤ 1 := by
  have hs := affinity_sq_le_mass_product p q hp hq
  have hq0 : 0 ≤ ∑ y, q y := Finset.sum_nonneg (fun y _ => hq y)
  have hprod : (∑ y, p y) * (∑ y, q y) ≤ 1 := by
    calc
      _ ≤ 1 * (∑ y, q y) := mul_le_mul_of_nonneg_right hsp hq0
      _ ≤ 1 := by simpa using hsq
  nlinarith

lemma affinity_lt_one_of_mass_lt_right {B : Type*} [Fintype B] (p q : B → ℝ)
    (hp : ∀ y, 0 ≤ p y) (hq : ∀ y, 0 ≤ q y)
    (hsp : ∑ y, p y ≤ 1) (hsq : ∑ y, q y < 1) : affinity p q < 1 := by
  have hs := affinity_sq_le_mass_product p q hp hq
  have hq0 : 0 ≤ ∑ y, q y := Finset.sum_nonneg (fun y _ => hq y)
  have hprod : (∑ y, p y) * (∑ y, q y) < 1 := by
    calc
      _ ≤ 1 * (∑ y, q y) := mul_le_mul_of_nonneg_right hsp hq0
      _ < 1 := by simpa using hsq
  nlinarith

def killedLaw {B : Type*} (p : B → ℝ) (keep : B → Bool) (y : B) : ℝ :=
  if keep y then p y else 0

lemma killedLaw_nonneg {B : Type*} (p : B → ℝ) (keep : B → Bool)
    (hp : ∀ y, 0 ≤ p y) (y : B) : 0 ≤ killedLaw p keep y := by
  unfold killedLaw
  split_ifs <;> first | exact hp y | exact le_rfl

lemma killedLaw_le {B : Type*} (p : B → ℝ) (keep : B → Bool)
    (hp : ∀ y, 0 ≤ p y) (y : B) : killedLaw p keep y ≤ p y := by
  unfold killedLaw
  split_ifs <;> first | exact le_rfl | exact hp y

lemma killedLaw_sum_le {B : Type*} [Fintype B] (p : B → ℝ) (keep : B → Bool)
    (hp : ∀ y, 0 ≤ p y) : ∑ y, killedLaw p keep y ≤ ∑ y, p y :=
  Finset.sum_le_sum (fun y _ => killedLaw_le p keep hp y)

lemma killedLaw_affinity_le {B : Type*} [Fintype B] (p q : B → ℝ) (keep : B → Bool) :
    affinity (killedLaw p keep) (killedLaw q keep) ≤ affinity p q := by
  apply Finset.sum_le_sum
  intro y _
  unfold killedLaw
  split_ifs <;> simp only [Real.sqrt_zero, zero_mul, le_refl]
  exact mul_nonneg (Real.sqrt_nonneg _) (Real.sqrt_nonneg _)

lemma killedLaw_affinity_formula {B : Type*} [Fintype B] (p q : B → ℝ) (keep : B → Bool) :
    affinity (killedLaw p keep) (killedLaw q keep) =
      ∑ y, if keep y then Real.sqrt (p y) * Real.sqrt (q y) else 0 := by
  apply Finset.sum_congr rfl
  intro y _
  unfold killedLaw
  split_ifs <;> simp

variable {Θ B : Type*} [Fintype B]

theorem hellinger_subprob_tree_budget [DecidableEq Θ] (K : Θ → Θ → B → ℝ)
    (hK : ∀ θ a y, 0 ≤ K θ a y)
    (hSub : ∀ θ a, ∑ y, K θ a y ≤ 1)
    (θ σ : Θ) (π : List (Θ × B) → Θ)
    (hMLE : ∀ h, π h = σ → historyMass K θ h ≤ historyMass K σ h)
    (n : ℕ) (h : List (Θ × B)) :
    (1-affinity (K θ σ) (K σ σ)) * selectedCost K θ σ π n h +
      leafAffinity K θ σ π n h ≤ historyAffinity K θ σ h := by
  let d := 1-affinity (K θ σ) (K σ σ)
  have hd : 0 ≤ d := sub_nonneg.mpr
    (affinity_le_one_subprob _ _ (hK θ σ) (hK σ σ) (hSub θ σ) (hSub σ σ))
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
          (affinity_le_one_subprob _ _ (hK θ (π h)) (hK σ (π h))
            (hSub θ (π h)) (hSub σ (π h)))
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


theorem selectedCost_subprob_uniform_bound [DecidableEq Θ] (K : Θ → Θ → B → ℝ)
    (hK : ∀ θ a y, 0 ≤ K θ a y)
    (hSub : ∀ θ a, ∑ y, K θ a y ≤ 1)
    (θ σ : Θ) (π : List (Θ × B) → Θ)
    (hMLE : ∀ h, π h = σ → historyMass K θ h ≤ historyMass K σ h)
    (hDef : affinity (K θ σ) (K σ σ) < 1) (n : ℕ) :
    selectedCost K θ σ π n [] ≤ 1 / (1-affinity (K θ σ) (K σ σ)) := by
  have hpos := sub_pos.mpr hDef
  have hb := hellinger_subprob_tree_budget K hK hSub θ σ π hMLE n []
  have hn := leafAffinity_nonneg K θ σ π n []
  have hroot : historyAffinity K θ σ [] = 1 := by simp [historyAffinity, historyMass]
  rw [hroot] at hb
  apply (le_div_iff₀ hpos).mpr
  nlinarith

end Orthemology.Tranche2
