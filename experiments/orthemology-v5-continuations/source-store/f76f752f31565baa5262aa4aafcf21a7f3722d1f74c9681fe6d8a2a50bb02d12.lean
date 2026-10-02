import ResetBudget

noncomputable section
open scoped BigOperators
open Finset

namespace Orthemology.Tranche2
variable {Phase Θ : Type*} {Obs : Phase → Θ → Type*} [∀ p a, Fintype (Obs p a)]

/-- Sum of full finite-path masses across both continuation and reset edges. -/
def resetLeafMass (K : (p : Phase) → (θ a : Θ) → Obs p a → ℝ)
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool)
    (next : (p : Phase) → (a : Θ) → Obs p a → Phase)
    (π : (p : Phase) → PhaseHistory (Obs := Obs) p → Θ) (θ : Θ) :
    ℕ → (p : Phase) → PhaseHistory (Obs := Obs) p → ℝ
  | 0, p, h => dHistoryMass (continuingKernel K stay p) θ h
  | n+1, p, h => ∑ y : Obs p (π p h), if stay p (π p h) y then
        resetLeafMass K stay next π θ n p (⟨π p h,y⟩::h)
      else (dHistoryMass (continuingKernel K stay p) θ h * K p θ (π p h) y) *
        resetLeafMass K stay next π θ n (next p (π p h) y) []

/-- Full exit mass is present, so the causal reset tree is normalized. -/
theorem resetLeafMass_normalized
    (K : (p : Phase) → (θ a : Θ) → Obs p a → ℝ)
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool)
    (next : (p : Phase) → (a : Θ) → Obs p a → Phase)
    (π : (p : Phase) → PhaseHistory (Obs := Obs) p → Θ) (θ : Θ)
    (hNorm : ∀ p a, ∑ y, K p θ a y = 1)
    (n : ℕ) (p : Phase) (h : PhaseHistory (Obs := Obs) p) :
    resetLeafMass K stay next π θ n p h = dHistoryMass (continuingKernel K stay p) θ h := by
  induction n generalizing p h with
  | zero => rfl
  | succ n ih =>
    simp only [resetLeafMass, ih]
    calc
      (∑ y : Obs p (π p h), if stay p (π p h) y then
          dHistoryMass (continuingKernel K stay p) θ (⟨π p h,y⟩::h)
        else (dHistoryMass (continuingKernel K stay p) θ h * K p θ (π p h) y) *
          dHistoryMass (continuingKernel K stay (next p (π p h) y)) θ []) =
        ∑ y : Obs p (π p h), dHistoryMass (continuingKernel K stay p) θ h * K p θ (π p h) y := by
          apply Finset.sum_congr rfl
          intro y _
          cases hs : stay p (π p h) y <;> simp [hs, dHistoryMass, continuingKernel]
      _ = _ := by rw [← Finset.mul_sum, hNorm, mul_one]

/-- Leaf-weighted total accumulated cost, using the same full branching law. -/
def resetLeafCost (K : (p : Phase) → (θ a : Θ) → Obs p a → ℝ)
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool)
    (next : (p : Phase) → (a : Θ) → Obs p a → Phase)
    (π : (p : Phase) → PhaseHistory (Obs := Obs) p → Θ) (cost : Phase → Θ → ℝ) (θ : Θ) :
    ℕ → (p : Phase) → PhaseHistory (Obs := Obs) p → ℝ → ℝ
  | 0, p, h, acc => acc * dHistoryMass (continuingKernel K stay p) θ h
  | n+1, p, h, acc => ∑ y : Obs p (π p h), if stay p (π p h) y then
        resetLeafCost K stay next π cost θ n p (⟨π p h,y⟩::h) (acc + cost p (π p h))
      else (dHistoryMass (continuingKernel K stay p) θ h * K p θ (π p h) y) *
        resetLeafCost K stay next π cost θ n (next p (π p h) y) [] (acc + cost p (π p h))

/-- The budget recurrence equals the expectation of accumulated cost under the
actual full finite tree. This is proved, not assumed as the semantic interface. -/
theorem resetLeafCost_eq_budget
    (K : (p : Phase) → (θ a : Θ) → Obs p a → ℝ)
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool)
    (next : (p : Phase) → (a : Θ) → Obs p a → Phase)
    (π : (p : Phase) → PhaseHistory (Obs := Obs) p → Θ) (cost : Phase → Θ → ℝ) (θ : Θ)
    (hNorm : ∀ p a, ∑ y, K p θ a y = 1)
    (n : ℕ) (p : Phase) (h : PhaseHistory (Obs := Obs) p) (acc : ℝ) :
    resetLeafCost K stay next π cost θ n p h acc =
      resetCost K stay next π cost θ n p h + acc * dHistoryMass (continuingKernel K stay p) θ h := by
  induction n generalizing p h acc with
  | zero => simp [resetLeafCost, resetCost]
  | succ n ih =>
    let m := dHistoryMass (continuingKernel K stay p) θ h
    have heq : ∀ y : Obs p (π p h),
        (if stay p (π p h) y then
          resetLeafCost K stay next π cost θ n p (⟨π p h,y⟩::h) (acc + cost p (π p h))
        else (m * K p θ (π p h) y) *
          resetLeafCost K stay next π cost θ n (next p (π p h) y) [] (acc + cost p (π p h))) =
        (if stay p (π p h) y then
          resetCost K stay next π cost θ n p (⟨π p h,y⟩::h)
        else (m * K p θ (π p h) y) * resetCost K stay next π cost θ n (next p (π p h) y) []) +
          (acc + cost p (π p h)) * m * K p θ (π p h) y := by
      intro y
      cases hs : stay p (π p h) y <;>
        simp only [hs, Bool.false_eq_true, ↓reduceIte, ih, dHistoryMass, continuingKernel]
      · ring
      · dsimp [m]
        ring
    calc
      resetLeafCost K stay next π cost θ (n+1) p h acc =
          (∑ y : Obs p (π p h), ((if stay p (π p h) y then
            resetCost K stay next π cost θ n p (⟨π p h,y⟩::h)
          else (m * K p θ (π p h) y) * resetCost K stay next π cost θ n (next p (π p h) y) []) +
            (acc + cost p (π p h)) * m * K p θ (π p h) y)) := by
        simp only [resetLeafCost]
        exact Finset.sum_congr rfl (fun y _ => heq y)
      _ = resetCost K stay next π cost θ (n+1) p h + acc * m := by
        rw [Finset.sum_add_distrib, ← Finset.mul_sum, hNorm, mul_one]
        simp only [resetCost]
        dsimp [m]
        ring

end Orthemology.Tranche2
