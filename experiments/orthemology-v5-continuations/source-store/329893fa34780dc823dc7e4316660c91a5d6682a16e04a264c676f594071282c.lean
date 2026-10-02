import MealySharpness

/-! Literal guarded refinement bridge. The displayed Köpf–Basin partial-partition
operator retains only pairs already in R: `R ∩ refine(R)`. Starting from top,
the guard is redundant because the actual approximants are decreasing. -/

namespace Orthemology.Frontier.Mealy
variable {S : Type*}

def guardedRefine (M : Mealy S) (R : PER S) : PER S where
  rel s t := R.rel s t ∧ (M.refine R).rel s t
  symm := by
    intro s t h
    exact ⟨R.symm h.1, (M.refine R).symm h.2⟩
  trans := by
    intro s t u h₁ h₂
    exact ⟨R.trans h₁.1 h₂.1, (M.refine R).trans h₁.2 h₂.2⟩

theorem guardedRefine_approx (M : Mealy S) (n : ℕ) :
    M.guardedRefine (M.approx n) = M.refine (M.approx n) := by
  apply PER.ext
  intro s t
  exact ⟨And.right, fun h => ⟨M.approx_decreasing n s t h, h⟩⟩

def guardedApprox (M : Mealy S) : ℕ → PER S
  | 0 => PER.universal
  | n+1 => M.guardedRefine (M.guardedApprox n)

/-- The literal guarded and unguarded source iterations agree at every finite stage. -/
theorem guardedApprox_eq (M : Mealy S) (n : ℕ) : M.guardedApprox n = M.approx n := by
  induction n with
  | zero => rfl
  | succ n ih =>
    change M.guardedRefine (M.guardedApprox n) = M.refine (M.approx n)
    rw [ih, guardedRefine_approx]

theorem guarded_stabilization_bound [Finite S] [Nonempty S] (M : Mealy S) :
    M.guardedApprox (2 * Nat.card S) = M.guardedApprox (2 * Nat.card S - 1) := by
  simpa only [guardedApprox_eq] using M.stabilization_bound

/-- Consequently the all-size lower bound applies literally to guarded refinement too. -/
theorem guarded_sharp_every_cardinality (m : ℕ) (hm : 0 < m) :
    ∃ (S : Type) (inst : Fintype S) (M : Mealy S) (s : S),
      @Fintype.card S inst = m ∧ (M.guardedApprox (2*m-2)).rel s s ∧
        ¬ (M.guardedApprox (2*m-1)).rel s s := by
  simpa only [guardedApprox_eq] using sharp_every_cardinality m hm

end Orthemology.Frontier.Mealy
