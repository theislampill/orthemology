import ResetTrajectory

noncomputable section
open scoped BigOperators
open Finset

namespace Orthemology.Tranche2
variable {Phase Θ : Type*} {Obs : Phase → Θ → Type*}
    [Fintype Phase] [Fintype Θ] [∀ p a, Fintype (Obs p a)]

def resetFutureCost
    (K : (p : Phase) → (θ a : Θ) → Obs p a → ℝ)
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool)
    (next : (p : Phase) → (a : Θ) → Obs p a → Phase)
    (π : (p : Phase) → PhaseHistory (Obs := Obs) p → Θ) (cost : Phase → Θ → ℝ) (θ : Θ) :
    ℕ → ResetState (Obs := Obs) → ℝ
  | 0, _ => 0
  | n+1, s => cost s.1 (π s.1 s.2) + ∑ y : Obs s.1 (π s.1 s.2),
      K s.1 θ (π s.1 s.2) y * resetFutureCost K stay next π cost θ n (resetUpdate stay next π s y)

omit [Fintype Phase] [Fintype Θ] in
/-- The unnormalised likelihood-tree budget is exactly current true-model mass
multiplied by the normalized Markov future-cost recurrence, including zero-mass
histories. No likelihood division is used. -/
theorem resetCost_eq_mass_future
    (K : (p : Phase) → (θ a : Θ) → Obs p a → ℝ)
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool)
    (next : (p : Phase) → (a : Θ) → Obs p a → Phase)
    (π : (p : Phase) → PhaseHistory (Obs := Obs) p → Θ) (cost : Phase → Θ → ℝ) (θ : Θ)
    (n : ℕ) (p : Phase) (h : PhaseHistory (Obs := Obs) p) :
    resetCost K stay next π cost θ n p h =
      dHistoryMass (continuingKernel K stay p) θ h * resetFutureCost K stay next π cost θ n ⟨p,h⟩ := by
  induction n generalizing p h with
  | zero => simp [resetCost, resetFutureCost]
  | succ n ih =>
    simp only [resetCost, resetFutureCost, ih, mul_add, Finset.mul_sum]
    rw [mul_comm (cost p (π p h))]
    congr 1
    apply Finset.sum_congr rfl
    intro y _
    cases hs : stay p (π p h) y <;>
      simp [hs, resetUpdate, dHistoryMass, continuingKernel, mul_assoc]

end Orthemology.Tranche2
