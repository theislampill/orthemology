import SupportBridge

namespace T20IndependentReview
open T20Grounded

def E (s : Finset Bool) : Prop := false ∈ s
def O (s : Finset Bool) : Prop := false ∈ s ∧ true ∉ s

/-- Every epistemically minimal set contains an operationally minimal set. -/
theorem minimal_cover_without_monotonicity :
    ∀ s : Finset Bool, MinimalFor E s → ∃ c, c ⊆ s ∧ MinimalFor O c := by
  intro s hs
  have hsub : ({false} : Finset Bool) ⊆ s := by
    simpa [E] using hs.1
  refine ⟨{false}, hsub, ?_⟩
  constructor
  · simp [O]
  · intro t _ ht
    simpa [O] using ht.1

/-- Nonetheless adding the conflicting resource destroys direct operation. -/
theorem failed_larger_retained_profile :
    E ({false, true} : Finset Bool) ∧ ¬ O {false, true} := by
  simp [E, O]

theorem actual_upward_closure_missing :
    ¬ (∀ a b : Finset Bool, a ⊆ b → O a → O b) := by
  intro h
  have hgood : O ({false} : Finset Bool) := by simp [O]
  have hlarge := h {false} {false, true} (by simp) hgood
  exact failed_larger_retained_profile.2 hlarge

/-- The minimal-support representation really does misclassify the larger set. -/
theorem upward_completion_is_not_direct_operation :
    (∃ c, c ⊆ ({false, true} : Finset Bool) ∧ MinimalFor O c) ∧
      ¬ O {false, true} := by
  refine ⟨?_, failed_larger_retained_profile.2⟩
  refine ⟨{false}, by simp, ?_⟩
  exact ⟨by simp [O], fun t _ ht => by simpa [O] using ht.1⟩

#print axioms minimal_cover_without_monotonicity
#print axioms failed_larger_retained_profile
#print axioms actual_upward_closure_missing
#print axioms upward_completion_is_not_direct_operation
end T20IndependentReview
