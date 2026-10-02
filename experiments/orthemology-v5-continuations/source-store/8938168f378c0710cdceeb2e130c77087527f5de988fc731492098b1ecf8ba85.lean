import CoverageBoundary
namespace IndependentCoverageControls
open Orthemology.Tranche3.CoverageBoundary
open Source Token

theorem computed_joint_requires_both :
    Provides {a,b} joint ∧ ¬Complete a joint ∧ ¬Complete b joint := by decide

theorem actual_evaluation_keeps_objective_correctness :
    output actual evaluation=some 4 ∧ (2+2:ℕ)=4 ∧ (2+2:ℕ)≠5 := actual_evaluation_correct

theorem connected_undirected_graph_does_not_expand_forward_closure :
    (∀ t,t=joint ∨ Needs joint t) ∧
    ¬∀ t,InEnvelope ({evaluation}:Set Token) Needs t := connected_does_not_give_prerequisite_scope

theorem direction_reversal_would_change_coverage :
    InEnvelope ({joint}:Set Token) Needs evaluation ∧
    ¬InEnvelope ({evaluation}:Set Token) Needs joint := by
  constructor
  · exact InEnvelope.prerequisite (InEnvelope.initial rfl) ⟨rfl,Or.inl rfl⟩
  · intro h
    have hh:=seed_evaluation_envelope_only joint h
    cases hh

theorem empty_seed_cannot_generate_anything {V : Type*} (req : V→V→Prop) (x : V) :
    ¬InEnvelope (∅:Set V) req x := by
  intro h
  exact envelope_least ∅ ∅ req (by simp) (by intro x y hx;exact hx.elim) x h

theorem universal_seed_needs_no_edges {V : Type*} (req : V→V→Prop) :
    ∀ x,InEnvelope (Set.univ:Set V) req x := fun _x => InEnvelope.initial trivial

theorem local_role_does_not_cover_all_tokens : Complete a evaluation ∧ ¬∀ t,Complete a t := by decide

theorem exists_bearer_can_withhold_exercise :
    SourceExists (fun _=>false) a ∧ ¬ExistsToken (fun _=>false) evaluation := by decide

theorem no_claim_of_two_complete_universal_sources : ¬∃ s,∀ t,Complete s t := no_universal_individual
end IndependentCoverageControls
