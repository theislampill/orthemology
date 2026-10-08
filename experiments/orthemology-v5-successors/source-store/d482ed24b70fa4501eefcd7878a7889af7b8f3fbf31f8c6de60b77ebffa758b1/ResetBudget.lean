import DependentHellinger

/-!
# Finite-horizon composition of interruptible phase budgets

The process keeps full exit probability and resets local likelihood memory on
exit. The proof is an induction on finite horizon; rank bounds later-phase cost.
The local budget interface is instantiated by killed Hellinger mass separately.
-/

noncomputable section
open scoped BigOperators
open Finset

namespace Orthemology.Tranche2
variable {Phase Θ : Type*} {Obs : Phase → Θ → Type*} [∀ p a, Fintype (Obs p a)]

abbrev PhaseHistory (p : Phase) := List (Σ a : Θ, Obs p a)

def continuingKernel (K : (p : Phase) → (θ a : Θ) → Obs p a → ℝ)
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool) (p : Phase) (θ a : Θ) (y : Obs p a) : ℝ :=
  if stay p a y then K p θ a y else 0

def resetCost (K : (p : Phase) → (θ a : Θ) → Obs p a → ℝ)
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool)
    (next : (p : Phase) → (a : Θ) → Obs p a → Phase)
    (π : (p : Phase) → PhaseHistory (Obs := Obs) p → Θ) (cost : Phase → Θ → ℝ) (θ : Θ) :
    ℕ → (p : Phase) → PhaseHistory (Obs := Obs) p → ℝ
  | 0, _, _ => 0
  | n+1, p, h =>
      cost p (π p h) * dHistoryMass (continuingKernel K stay p) θ h +
      ∑ y : Obs p (π p h), if stay p (π p h) y then
        resetCost K stay next π cost θ n p (⟨π p h,y⟩::h)
      else (dHistoryMass (continuingKernel K stay p) θ h * K p θ (π p h) y) *
        resetCost K stay next π cost θ n (next p (π p h) y) []

/-- A stateful budget, with all exit mass retained in the recurrence. -/
theorem resetCost_bound
    (K : (p : Phase) → (θ a : Θ) → Obs p a → ℝ)
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool)
    (next : (p : Phase) → (a : Θ) → Obs p a → Phase)
    (π : (p : Phase) → PhaseHistory (Obs := Obs) p → Θ) (cost : Phase → Θ → ℝ) (θ : Θ)
    (hK : ∀ p η a y, 0 ≤ K p η a y)
    (hNorm : ∀ p a, ∑ y, K p θ a y = 1)
    (rank : Phase → ℕ)
    (hRank : ∀ p a y, stay p a y = false → 0 < K p θ a y → rank (next p a y) < rank p)
    (V : (p : Phase) → PhaseHistory (Obs := Obs) p → ℝ) (hV : ∀ p h, 0 ≤ V p h)
    (hStep : ∀ p h,
      cost p (π p h) * dHistoryMass (continuingKernel K stay p) θ h +
        (∑ y : Obs p (π p h), if stay p (π p h) y then V p (⟨π p h,y⟩::h) else 0) ≤ V p h)
    (C : ℝ) (hC : 0 ≤ C) (hRoot : ∀ p, V p [] ≤ C)
    (n : ℕ) (p : Phase) (h : PhaseHistory (Obs := Obs) p) :
    resetCost K stay next π cost θ n p h ≤
      V p h + (rank p : ℝ) * C * dHistoryMass (continuingKernel K stay p) θ h := by
  have hcont : ∀ p η a y, 0 ≤ continuingKernel K stay p η a y := by
    intro p η a y
    unfold continuingKernel
    split_ifs <;> first | exact hK p η a y | exact le_rfl
  induction n generalizing p h with
  | zero =>
    simp only [resetCost]
    exact add_nonneg (hV p h) (mul_nonneg (mul_nonneg (Nat.cast_nonneg _) hC)
      (dHistoryMass_nonneg _ (hcont p) θ h))
  | succ n ih =>
    let m := dHistoryMass (continuingKernel K stay p) θ h
    have hm : 0 ≤ m := dHistoryMass_nonneg _ (hcont p) θ h
    have hchild : ∀ y : Obs p (π p h),
        (if stay p (π p h) y then resetCost K stay next π cost θ n p (⟨π p h,y⟩::h)
        else (m * K p θ (π p h) y) * resetCost K stay next π cost θ n (next p (π p h) y) []) ≤
        (if stay p (π p h) y then V p (⟨π p h,y⟩::h) else 0) +
          (rank p : ℝ) * C * m * K p θ (π p h) y := by
      intro y
      cases hs : stay p (π p h) y
      · simp only [hs, Bool.false_eq_true, ↓reduceIte, zero_add]
        by_cases hp : 0 < K p θ (π p h) y
        · have hr := hRank p (π p h) y hs hp
          have hrReal : (rank (next p (π p h) y) : ℝ) + 1 ≤ (rank p : ℝ) := by exact_mod_cast hr
          have hi := ih (next p (π p h) y) []
          simp only [dHistoryMass, mul_one] at hi
          have hc : resetCost K stay next π cost θ n (next p (π p h) y) [] ≤ (rank p : ℝ) * C := by
            have hroot := hRoot (next p (π p h) y)
            have hmul := mul_le_mul_of_nonneg_right hrReal hC
            nlinarith
          have hh := mul_le_mul_of_nonneg_left hc (mul_nonneg hm (hK p θ (π p h) y))
          nlinarith
        · have hz : K p θ (π p h) y = 0 := le_antisymm (le_of_not_gt hp) (hK p θ (π p h) y)
          simp [hz]
      · simp only [hs, ↓reduceIte]
        have hi := ih p (⟨π p h,y⟩::h)
        simpa only [dHistoryMass, continuingKernel, hs, ↓reduceIte, m, mul_assoc] using hi
    calc
      resetCost K stay next π cost θ (n+1) p h =
          cost p (π p h) * m + ∑ y : Obs p (π p h),
            (if stay p (π p h) y then resetCost K stay next π cost θ n p (⟨π p h,y⟩::h)
             else (m * K p θ (π p h) y) * resetCost K stay next π cost θ n (next p (π p h) y) []) := rfl
      _ ≤ cost p (π p h) * m + ∑ y : Obs p (π p h),
          ((if stay p (π p h) y then V p (⟨π p h,y⟩::h) else 0) +
            (rank p : ℝ) * C * m * K p θ (π p h) y) :=
        add_le_add_left (Finset.sum_le_sum (fun y _ => hchild y)) _
      _ = (cost p (π p h) * m + ∑ y : Obs p (π p h),
          if stay p (π p h) y then V p (⟨π p h,y⟩::h) else 0) + (rank p : ℝ) * C * m := by
        rw [Finset.sum_add_distrib, ← Finset.mul_sum, hNorm, mul_one]
        ring
      _ ≤ V p h + (rank p : ℝ) * C * m := add_le_add_right (hStep p h) _

/-- Global bound independent of horizon. No terminal-phase conditioning occurs. -/
theorem resetCost_root_bound
    (K : (p : Phase) → (θ a : Θ) → Obs p a → ℝ)
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool)
    (next : (p : Phase) → (a : Θ) → Obs p a → Phase)
    (π : (p : Phase) → PhaseHistory (Obs := Obs) p → Θ) (cost : Phase → Θ → ℝ) (θ : Θ)
    (hK : ∀ p η a y, 0 ≤ K p η a y)
    (hNorm : ∀ p a, ∑ y, K p θ a y = 1)
    (rank : Phase → ℕ)
    (hRank : ∀ p a y, stay p a y = false → 0 < K p θ a y → rank (next p a y) < rank p)
    (V : (p : Phase) → PhaseHistory (Obs := Obs) p → ℝ) (hV : ∀ p h, 0 ≤ V p h)
    (hStep : ∀ p h,
      cost p (π p h) * dHistoryMass (continuingKernel K stay p) θ h +
        (∑ y : Obs p (π p h), if stay p (π p h) y then V p (⟨π p h,y⟩::h) else 0) ≤ V p h)
    (C : ℝ) (hC : 0 ≤ C) (hRoot : ∀ p, V p [] ≤ C)
    (n : ℕ) (p : Phase) :
    resetCost K stay next π cost θ n p [] ≤ ((rank p : ℝ)+1)*C := by
  have hb := resetCost_bound K stay next π cost θ hK hNorm rank hRank V hV hStep C hC hRoot n p []
  simp only [dHistoryMass, mul_one] at hb
  have hr := hRoot p
  nlinarith

end Orthemology.Tranche2
