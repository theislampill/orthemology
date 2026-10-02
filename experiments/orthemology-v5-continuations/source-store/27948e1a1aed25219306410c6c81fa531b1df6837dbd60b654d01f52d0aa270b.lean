import RecursivePhysicalBudget

noncomputable section
open Finset
open scoped BigOperators
attribute [local instance] Classical.propDecidable
namespace Orthemology.Tranche3
open Orthemology.Tranche2

section Continuation
variable {Phase Θ : Type*} {Obs : Phase → Θ → Type*} [∀ p a, Fintype (Obs p a)]

/-- A state-dependent continuation budget replaces the coarse rank times a
single global constant. All exit mass remains in the original recurrence. -/
theorem resetCost_continuation_bound
    (K : (p : Phase) → (θ a : Θ) → Obs p a → ℝ)
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool)
    (next : (p : Phase) → (a : Θ) → Obs p a → Phase)
    (π : (p : Phase) → PhaseHistory (Obs := Obs) p → Θ) (cost : Phase → Θ → ℝ) (θ : Θ)
    (hK : ∀ p η a y, 0 ≤ K p η a y)
    (hNorm : ∀ p a, ∑ y, K p θ a y = 1)
    (I : Phase → Prop)
    (hNext : ∀ p a y, I p → stay p a y = false → 0 < K p θ a y → I (next p a y))
    (V : (p : Phase) → PhaseHistory (Obs := Obs) p → ℝ) (hV : ∀ p, I p → ∀ h, 0 ≤ V p h)
    (hStep : ∀ p, I p → ∀ h,
      cost p (π p h) * dHistoryMass (continuingKernel K stay p) θ h +
        (∑ y : Obs p (π p h), if stay p (π p h) y then V p (⟨π p h,y⟩::h) else 0) ≤ V p h)
    (D : Phase → ℝ) (hD : ∀ p, I p → 0 ≤ D p)
    (hExit : ∀ p a y, I p → stay p a y = false → 0 < K p θ a y →
      V (next p a y) [] + D (next p a y) ≤ D p)
    (n : ℕ) (p : Phase) (h : PhaseHistory (Obs := Obs) p) (hp : I p) :
    resetCost K stay next π cost θ n p h ≤
      V p h + D p * dHistoryMass (continuingKernel K stay p) θ h := by
  have hcont : ∀ p η a y, 0 ≤ continuingKernel K stay p η a y := by
    intro p η a y
    unfold continuingKernel
    split_ifs <;> first | exact hK p η a y | exact le_rfl
  induction n generalizing p h with
  | zero =>
    simp only [resetCost]
    exact add_nonneg (hV p hp h) (mul_nonneg (hD p hp)
      (dHistoryMass_nonneg _ (hcont p) θ h))
  | succ n ih =>
    let m := dHistoryMass (continuingKernel K stay p) θ h
    have hm : 0 ≤ m := dHistoryMass_nonneg _ (hcont p) θ h
    have hchild : ∀ y : Obs p (π p h),
        (if stay p (π p h) y then resetCost K stay next π cost θ n p (⟨π p h,y⟩::h)
        else (m * K p θ (π p h) y) * resetCost K stay next π cost θ n (next p (π p h) y) []) ≤
        (if stay p (π p h) y then V p (⟨π p h,y⟩::h) else 0) +
          D p * m * K p θ (π p h) y := by
      intro y
      cases hs : stay p (π p h) y
      · simp only [hs, Bool.false_eq_true, ↓reduceIte, zero_add]
        by_cases hpos : 0 < K p θ (π p h) y
        · have hnext := hNext p (π p h) y hp hs hpos
          have hi := ih (next p (π p h) y) [] hnext
          simp only [dHistoryMass, mul_one] at hi
          have hc := hi.trans (hExit p (π p h) y hp hs hpos)
          have hh := mul_le_mul_of_nonneg_left hc (mul_nonneg hm (hK p θ (π p h) y))
          nlinarith
        · have hz : K p θ (π p h) y = 0 := le_antisymm (le_of_not_gt hpos) (hK p θ (π p h) y)
          simp [hz]
      · simp only [hs, ↓reduceIte]
        have hi := ih p (⟨π p h,y⟩::h) hp
        simpa only [dHistoryMass, continuingKernel, hs, ↓reduceIte, m, mul_assoc] using hi
    calc
      resetCost K stay next π cost θ (n+1) p h =
          cost p (π p h) * m + ∑ y : Obs p (π p h),
            (if stay p (π p h) y then resetCost K stay next π cost θ n p (⟨π p h,y⟩::h)
             else (m * K p θ (π p h) y) * resetCost K stay next π cost θ n (next p (π p h) y) []) := rfl
      _ ≤ cost p (π p h) * m + ∑ y : Obs p (π p h),
          ((if stay p (π p h) y then V p (⟨π p h,y⟩::h) else 0) +
            D p * m * K p θ (π p h) y) :=
        add_le_add_left (Finset.sum_le_sum (fun y _ => hchild y)) _
      _ = (cost p (π p h) * m + ∑ y : Obs p (π p h),
          if stay p (π p h) y then V p (⟨π p h,y⟩::h) else 0) + D p * m := by
        rw [Finset.sum_add_distrib, ← Finset.mul_sum, hNorm, mul_one]
        ring
      _ ≤ V p h + D p * m := add_le_add_right (hStep p hp h) _
end Continuation

section Bellman
variable {Phase : Type*} [Fintype Phase]

/-- Longest total phaseCost budget over an acyclic admissible phase chain. The
rank certifies termination; it is not multiplied into the resulting bound. -/
def phaseChainBudget (rank : Phase → ℕ) (edge : Phase → Phase → Prop)
    (hRank : ∀ p q, edge p q → rank q < rank p) (phaseCost : Phase → ℝ) (p : Phase) : ℝ :=
  phaseCost p + Finset.sup' Finset.univ ⟨p,mem_univ p⟩ (fun q =>
    if _h : edge p q then phaseChainBudget rank edge hRank phaseCost q else 0)
termination_by rank p
decreasing_by exact hRank p q _h

def phaseContinuationBudget (rank : Phase → ℕ) (edge : Phase → Phase → Prop)
    (hRank : ∀ p q, edge p q → rank q < rank p) (phaseCost : Phase → ℝ) (p : Phase) : ℝ :=
  Finset.sup' Finset.univ ⟨p,mem_univ p⟩ (fun q =>
    if edge p q then phaseChainBudget rank edge hRank phaseCost q else 0)

lemma phaseChainBudget_eq (rank : Phase → ℕ) (edge : Phase → Phase → Prop)
    (hRank : ∀ p q, edge p q → rank q < rank p) (phaseCost : Phase → ℝ) (p : Phase) :
    phaseChainBudget rank edge hRank phaseCost p = phaseCost p + phaseContinuationBudget rank edge hRank phaseCost p := by
  rw [phaseChainBudget]
  rfl

lemma phaseContinuationBudget_nonneg (rank : Phase → ℕ) (edge : Phase → Phase → Prop)
    (hRank : ∀ p q, edge p q → rank q < rank p) (phaseCost : Phase → ℝ) (p : Phase) :
    0 ≤ phaseContinuationBudget rank edge hRank phaseCost p := by
  have hself : ¬ edge p p := fun h => (Nat.lt_irrefl _) (hRank p p h)
  have hh := Finset.le_sup' (s := Finset.univ) (f := fun q =>
    if edge p q then phaseChainBudget rank edge hRank phaseCost q else 0) (mem_univ p)
  simpa only [if_neg hself] using hh

lemma phaseChainBudget_nonneg (rank : Phase → ℕ) (edge : Phase → Phase → Prop)
    (hRank : ∀ p q, edge p q → rank q < rank p) (phaseCost : Phase → ℝ)
    (hl : ∀ p, 0 ≤ phaseCost p) (p : Phase) :
    0 ≤ phaseChainBudget rank edge hRank phaseCost p := by
  rw [phaseChainBudget_eq]
  exact add_nonneg (hl p) (phaseContinuationBudget_nonneg rank edge hRank phaseCost p)

lemma phaseChainBudget_le_continuation (rank : Phase → ℕ) (edge : Phase → Phase → Prop)
    (hRank : ∀ p q, edge p q → rank q < rank p) (phaseCost : Phase → ℝ)
    (p q : Phase) (he : edge p q) :
    phaseChainBudget rank edge hRank phaseCost q ≤ phaseContinuationBudget rank edge hRank phaseCost p := by
  have hh := Finset.le_sup' (s := Finset.univ) (f := fun q =>
    if edge p q then phaseChainBudget rank edge hRank phaseCost q else 0) (mem_univ q)
  simpa only [if_pos he] using hh

/-- The chain dynamic program is no larger than the old rank/global cap. -/
theorem phaseChainBudget_le_rank_bound (rank : Phase → ℕ) (edge : Phase → Phase → Prop)
    (hRank : ∀ p q, edge p q → rank q < rank p) (phaseCost : Phase → ℝ)
    (C : ℝ) (hC : 0 ≤ C) (hlocal : ∀ p, phaseCost p ≤ C) (p : Phase) :
    phaseChainBudget rank edge hRank phaseCost p ≤ ((rank p : ℝ) + 1) * C := by
  induction hp : rank p using Nat.strong_induction_on generalizing p with
  | h n ih =>
    rw [phaseChainBudget_eq]
    have hd : phaseContinuationBudget rank edge hRank phaseCost p ≤ (rank p : ℝ) * C := by
      apply Finset.sup'_le
      intro q _
      split_ifs with he
      · have hr := hRank p q he
        have hi := ih (rank q) (by omega) q rfl
        have hrr : (rank q : ℝ) + 1 ≤ (rank p : ℝ) := by exact_mod_cast hr
        exact hi.trans (mul_le_mul_of_nonneg_right hrr hC)
      · exact mul_nonneg (Nat.cast_nonneg _) hC
    rw [hp] at hd
    nlinarith [hlocal p]
/-- The dynamic program is the least additive phase budget satisfying the
local charge and every edge inequality. This is optimality only within that
specified certificate class, not optimality over statistical controllers. -/
theorem phaseChainBudget_le_supersolution (rank : Phase → ℕ) (edge : Phase → Phase → Prop)
    (hRank : ∀ p q, edge p q → rank q < rank p) (phaseCost bound : Phase → ℝ)
    (hroot : ∀ p, phaseCost p ≤ bound p)
    (hedge : ∀ p q, edge p q → phaseCost p + bound q ≤ bound p) (p : Phase) :
    phaseChainBudget rank edge hRank phaseCost p ≤ bound p := by
  induction hp : rank p using Nat.strong_induction_on generalizing p with
  | h n ih =>
    rw [phaseChainBudget_eq]
    have hd : phaseContinuationBudget rank edge hRank phaseCost p ≤ bound p - phaseCost p := by
      apply Finset.sup'_le
      intro q _
      split_ifs with he
      · have hr := hRank p q he
        have hi := ih (rank q) (by omega) q rfl
        linarith [hedge p q he]
      · linarith [hroot p]
    linarith

end Bellman
end Orthemology.Tranche3
