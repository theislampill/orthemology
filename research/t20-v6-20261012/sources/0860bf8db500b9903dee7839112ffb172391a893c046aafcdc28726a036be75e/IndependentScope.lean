import FixedTarget

namespace IndependentScope
open FixedTarget

def OneOwner (g : Agent) (_c : Emission) : Prop := g = .a

theorem one_owner_nonvacuous : CND OneOwner ∧ Entire OneOwner .a ∧ ¬ Entire OneOwner .b := by
  refine ⟨?_, ?_, ?_⟩
  · intro ag bg c ha hb
    exact ha.trans hb.symm
  · intro c
    rfl
  · intro h
    have bad : Agent.b = Agent.a := h .x0
    cases bad

-- The countermodel is inhabited and CND is neither universal nor inconsistent.
theorem exact_ownership_controls :
    CND Own ∧ ¬ CND DuplicateOwn ∧
    (¬ Entire Own .a ∧ ¬ Entire Own .b) :=
  ⟨emitted_token_cnd, duplicate_ownership_rejected, neither_owns_entire_emission_process⟩

-- Concrete (4,4) is feasible jointly in the bounded family, but not a bounded command.
theorem union_not_sum_closure :
    add target target = (⟨4,4⟩ : Vec) ∧ ¬ inCapacity (add target target) := by
  constructor
  · rfl
  · simp [inCapacity, add, target]

-- This is why the parametric all-Nat construction matters for concentration.
theorem generic_concentration (a b : Vec) :
    ∃ c : Vec, add c zero = add a b := every_nat_vector_constructive (add a b)

-- Two possible controls under concord do not entail rectangular sovereignty.
theorem concord_does_not_yield_rectangular_control :
    (∀ q : Bool, AdmissibleControlsA sat concord q) ∧ ¬ ControlsA sat false :=
  ⟨concordant_all_targets, saturation_cannot_force_false⟩

theorem actual_redundancy_is_not_indispensability :
    sat true true = true ∧ sat true false = true ∧
    ¬ IndispensableB sat true true false true := by
  exact ⟨rfl, rfl, saturation_no_actual_indispensability⟩

-- Whole outcome attribution and ownership of all emission tokens are separate.
theorem whole_target_cnd_does_not_follow_from_emission_cnd :
    CND Own ∧ ¬ CNDAt WholeSufficient :=
  ⟨emitted_token_cnd, sufficient_as_entire_breaks_whole_target_cnd⟩

#print axioms one_owner_nonvacuous
#print axioms exact_ownership_controls
#print axioms union_not_sum_closure
#print axioms generic_concentration
#print axioms concord_does_not_yield_rectangular_control
#print axioms actual_redundancy_is_not_indispensability
#print axioms whole_target_cnd_does_not_follow_from_emission_cnd
end IndependentScope
