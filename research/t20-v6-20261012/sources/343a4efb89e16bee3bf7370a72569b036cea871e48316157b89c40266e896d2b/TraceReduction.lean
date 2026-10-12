import Std
namespace TraceReduction

-- New real-created token, faithful total history, and distinction from the
-- solo total suffice. This is set-membership, not a physical conservation law.
theorem new_created_token_forces_total_difference {Token : Type}
    (solo joint extra : Token → Prop)
    (retained : ∀ x, extra x → joint x)
    (new_token : ∃ x, extra x ∧ ¬ solo x) :
    ∃ x, joint x ∧ ¬ solo x := by
  obtain ⟨x, hx, hnot⟩ := new_token
  exact ⟨x, retained x hx, hnot⟩

-- Empty background/current production episode. With fixed background S,
-- one must additionally show that the extra token is not already in S.
theorem fixed_manifestation_disjoint_retained_gives_growth {Token : Type}
    (own peer solo joint : Token → Prop)
    (solo_exact : ∀ x, solo x ↔ own x)
    (peer_nonempty : ∃ x, peer x)
    (disjoint : ∀ x, peer x → ¬ own x)
    (retained : ∀ x, peer x → joint x) :
    ∃ x, joint x ∧ ¬ solo x := by
  obtain ⟨x, hx⟩ := peer_nonempty
  refine ⟨x, retained x hx, ?_⟩
  intro hs
  exact disjoint x hx ((solo_exact x).mp hs)

-- CND supplies disjointness only after the source-owned entire contribution
-- interpretation is justified. It does not produce those witnesses itself.
theorem cnd_disjoins_entire_owned_tokens {Agent Token : Type}
    (Entire : Agent → Token → Prop) (a b : Agent) (ha : a ≠ b)
    (CND : ∀ g h x, Entire g x → Entire h x → g = h)
    (ca cb : Token → Prop)
    (ownedA : ∀ x, ca x → Entire a x)
    (ownedB : ∀ x, cb x → Entire b x) :
    ∀ x, ca x → ¬ cb x := by
  intro x hca hcb
  exact ha (CND a b x (ownedA x hca) (ownedB x hcb))

-- Arbitrary signed projection permits interaction/cancellation while the
-- real occurrence history retains more entries. No physical units assumed.
theorem signed_interaction_equal_projection_distinct_history :
    ((1 : Int) + 1 + (-1) = 1) ∧ ([1,1,-1] : List Int) ≠ [1] := by decide

end TraceReduction
#print axioms TraceReduction.new_created_token_forces_total_difference
#print axioms TraceReduction.fixed_manifestation_disjoint_retained_gives_growth
#print axioms TraceReduction.cnd_disjoins_entire_owned_tokens
#print axioms TraceReduction.signed_interaction_equal_projection_distinct_history
