import NontrivialFixture
set_option autoImplicit false

noncomputable section
namespace Orthemology.Eighth.SemanticControls.LiteralAssessment
open HiddenParity HiddenParity.Sufficiency HiddenParity.Stage
open Orthemology.RuntimeBridge.PhaseUpdate

/-- The retained full-support cycle is fallback-independent. -/
theorem full_cycle_fallback (a b : Bool) (n : ℕ) :
    cycleAction (Finset.univ : Finset Bool) a n = cycleAction Finset.univ b n := by
  simp only [cycleAction,dif_pos Finset.univ_nonempty]

theorem full_cycle_distinct :
    cycleAction (Finset.univ : Finset Bool) false 0 ≠ cycleAction Finset.univ false 1 := by
  intro h
  simp only [cycleAction,dif_pos Finset.univ_nonempty] at h
  have hi := (Fintype.equivFin (Finset.univ : Finset Bool)).symm.injective (Subtype.ext h)
  have hv := congrArg Fin.val hi
  norm_num at hv

/-- There are exactly two possible Boolean orientations; this does not select one. -/
theorem full_cycle_one (fallback : Bool) :
    cycleAction (Finset.univ : Finset Bool) fallback 1 = !initialCandidate := by
  rw [full_cycle_fallback fallback false 1]
  have h := full_cycle_distinct
  change initialCandidate ≠ cycleAction (Finset.univ : Finset Bool) false 1 at h
  cases hc : initialCandidate <;> cases hd : cycleAction (Finset.univ : Finset Bool) false 1 <;>
    simp_all

theorem full_component (B : Finset Bool) :
    IsEndComponent Prod.fst (internalSuccessors fixtureKernel B)
      (Finset.univ : Finset (Bool × Bool)) := by
  refine ⟨Finset.univ_nonempty,?_,?_,?_⟩
  · intro e he; simp
  · intro e he y hy
    exact Finset.mem_image.mpr ⟨(y,false),Finset.mem_univ _,rfl⟩
  · intro s hs t ht
    exact Relation.ReflTransGen.single ⟨(s,false),Finset.mem_univ _,rfl,by simp⟩

/-- On an off-path singleton-support/opposite-candidate cell, the parity
condition is vacuous, so the full pair set also qualifies. -/
theorem opposite_singleton_full_qualifies (θ : Bool) :
    MarkovQualifying fixtureKernel Prod.fst {θ} actionPriority (!θ)
      Finset.univ (Finset.univ : Finset (Bool × Bool)) := by
  refine ⟨Finset.Subset.refl _,?_,full_component {θ},?_⟩
  · intro e he y hy; simp
  · intro σ hσ hm
    have hs : σ = θ := Finset.mem_singleton.mp hσ
    have hd := fixture_match_eq (!θ) σ Finset.univ Finset.univ_nonempty hm
    rw [hs] at hd
    cases θ <;> simp at hd

/-- Exact retained-target specifications do not determine a unique off-path
entry for the frozen all-action-menu fixture. This is a uniqueness obstruction,
not a proof that a particular retained choice is undecidable. -/
theorem off_path_target_not_unique (θ : Bool) :
    ∃ E F : Finset (Bool × Bool), E ≠ F ∧
      MarkovQualifying fixtureKernel Prod.fst {θ} actionPriority (!θ) Finset.univ E ∧
      MarkovQualifying fixtureKernel Prod.fst {θ} actionPriority (!θ) Finset.univ F ∧
      usedStates Prod.fst E = Finset.univ ∧ usedStates Prod.fst F = Finset.univ := by
  refine ⟨goodPairs (!θ),Finset.univ,?_,goodPairs_qualifying {θ} (!θ),
    opposite_singleton_full_qualifies θ,goodPairs_states (!θ),?_⟩
  · intro he
    have hm : (false,θ) ∈ goodPairs (!θ) := he.symm ▸ Finset.mem_univ _
    have hh := (mem_goodPairs (!θ) (false,θ)).mp hm
    cases θ <;> simp at hh
  · ext s
    simp only [usedStates,Finset.mem_image,Finset.mem_univ,true_and,iff_true]
    exact ⟨(s,false),rfl⟩

end Orthemology.Eighth.SemanticControls.LiteralAssessment
