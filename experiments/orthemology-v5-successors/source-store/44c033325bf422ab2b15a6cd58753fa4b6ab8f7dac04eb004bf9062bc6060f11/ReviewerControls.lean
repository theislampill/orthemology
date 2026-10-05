import LawCompletionCompact
import LawCompletionCounterexample
import LawCompletionBranches

set_option autoImplicit false

namespace LawCompletion.IndependentReview

open Set Filter
open scoped Topology

/-- Complete bounded continuity cannot replace compactness in the uniform conclusion. -/
theorem removing_compactness_breaks_uniform :
    ¬ (SingletonSurvival ControlA.law none → UniformAttraction ControlA.law none) := by
  intro h
  exact ControlA.not_pointwise_attraction
    (uniform_pointwise ControlA.law none (h ControlA.singleton_survival))

/-- Unique compatible realization does not imply singleton survival without the compact bridge. -/
theorem removing_compactness_breaks_survivor_equivalence :
    ¬ (UniqueBackward ControlB.law → ∃ z, SingletonSurvival ControlB.law z) := by
  intro h
  exact ControlB.not_singleton_survival (h ControlB.unique_backward)

/-- The successor map has no compatible infinite backward realization. -/
theorem successor_has_no_backward : ¬ ∃ b : ℕ → ℕ, Backward Nat.succ b := by
  rintro ⟨b, hb⟩
  have hdepth : ∀ n : ℕ, b n + n = b 0 := by
    intro n
    induction n with
    | zero => omega
    | succ n ih =>
        have hstep := hb n
        change b n = b (n + 1) + 1 at hstep
        omega
  have hbad := hdepth (b 0 + 1)
  omega

/-- At-most-one is vacuous here; the checked UniqueBackward predicate includes existence. -/
theorem existence_cannot_be_deleted :
    (∀ b c : ℕ → ℕ, Backward Nat.succ b → Backward Nat.succ c → b = c) ∧
    ¬ UniqueBackward Nat.succ := by
  constructor
  · intro b c hb _
    exact False.elim (successor_has_no_backward ⟨b, hb⟩)
  · rintro ⟨b, hb, _⟩
    exact successor_has_no_backward ⟨b, hb⟩

/-- An arbitrary predecessor of a survivor need not itself survive, even on a finite carrier. -/
theorem arbitrary_preimage_step_fails :
    let f : Bool → Bool := fun _ => false
    Survives f false ∧ f true = false ∧ ¬ Survives f true := by
  dsimp
  refine ⟨fixed_survives (fun _ : Bool => false) false rfl, rfl, ?_⟩
  intro h
  obtain ⟨y, hy⟩ := h 1
  simp at hy

#check removing_compactness_breaks_uniform
#print axioms removing_compactness_breaks_uniform
#check removing_compactness_breaks_survivor_equivalence
#print axioms removing_compactness_breaks_survivor_equivalence
#check successor_has_no_backward
#print axioms successor_has_no_backward
#check existence_cannot_be_deleted
#print axioms existence_cannot_be_deleted
#check arbitrary_preimage_step_fails
#print axioms arbitrary_preimage_step_fails

end LawCompletion.IndependentReview
