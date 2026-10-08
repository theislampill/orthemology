import HiddenChangeNecessity

open HiddenChange HiddenParity MeasureTheory
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport
open HiddenParity.Stochastic

namespace NecessityReview
-- One internal positive receipt is insufficient: all P0 successors must remain in W.
def branching : HiddenChange.Input 2 1 where
  rows := #[1/2,1/2,1/2,1/2,1/2,1/2,1/2,1/2]
  priorities := #[0,0,0,0]
  menus := [⟨[0,1],0,[0]⟩,⟨[0,1],1,[0]⟩]
  interpretation := ⟨["zero","one"],["s","t"],["a"],"v1","state","exact","common"⟩
example : Admissible branching := by decide +kernel
example : 0 ∈ internalSucc branching 0 (0,0) := by decide +kernel
example : 1 ∈ succ branching 0 (0,0) := by decide +kernel
theorem chosen_receipt_not_safe : (0,0) ∉ uncertainAllowed branching Finset.univ {0} := by decide +kernel
example : (0,0) ∉ knownAllowed branching {0} := by decide +kernel

-- Equal support is weaker than full numerical equality. Candidate0 may be
-- good while its unequal-row rival has odd minimum.
def unequal : HiddenChange.Input 2 1 where
  rows := #[1/2,1/2,1/2,1/2,1/3,2/3,1/3,2/3]
  priorities := #[0,0,1,1]
  menus := [⟨[0,1],0,[0]⟩,⟨[0,1],1,[0]⟩]
  interpretation := ⟨["zero","one"],["s","t"],["a"],"v1","state","exact","common"⟩
example : Admissible unequal := by decide +kernel
example : ∀ e : Pair 2 1, succ unequal 0 e = succ unequal 1 e := by decide +kernel
theorem supports_differ_numerically : ¬ Match unequal.row 0 1 Finset.univ := by decide +kernel
example : UncertainGood unequal 0 Finset.univ := by decide +kernel
theorem rival_can_be_odd : ¬ EvenMinimum unequal 1 Finset.univ := by decide +kernel

-- Winning priorities do not supply authority to use an excluded action.
def forbiddenEven : HiddenChange.Input 1 2 where
  rows := #[1,1,1,1]
  priorities := #[1,0,1,0]
  menus := [⟨[0,1],0,[0]⟩]
  interpretation := ⟨["zero","one"],["s"],["odd","even"],"v1","state","exact","common"⟩
def choosesForbidden : Policy Unit 1 2 := fun _ _ => 1
example : Admissible forbiddenEven := by decide +kernel
example : uncertainRegion forbiddenEven = ∅ := by decide +kernel
example : ¬ PolicyLawful forbiddenEven 0 choosesForbidden := by
  intro h
  have hh := h () []
  change (1 : Action 2) ∈ commonMenu forbiddenEven 0 at hh
  have hn : (1 : Action 2) ∉ commonMenu forbiddenEven 0 := by decide +kernel
  exact hn hh

/-- A literal unlawful policy wins the actual fixed laws. This shows why the
separate lawfulness premise cannot be inferred from parity or omitted. -/
theorem forbidden_wins (κ : ChangeIndex) :
    ∀ᵐ H ∂fixedLaw forbiddenEven (by decide +kernel : Admissible forbiddenEven).1 κ 0
      (Measure.dirac ()) choosesForbidden, TaggedParity forbiddenEven (0,0) H := by
  unfold fixedLaw observedTraceLaw
  rw [ae_map_iff (historyTrajectory_measurable ∅ _
    (fixedPolicy_measurable κ 0 choosesForbidden (measurable_of_countable _))).aemeasurable
    (taggedParity_measurable forbiddenEven (0,0))]
  apply ae_of_all
  intro z
  let x := historyAction (0,(0,0)) (historyTrajectory ∅ (fixedPolicy κ 0 choosesForbidden) z)
  have hp : ∀ t, forbiddenEven.priority (x t).1 (x t).2 = 0 := by
    intro t
    dsimp [x]
    simp only [historyAction,historyTrajectory,observedHistory,List.headD_cons,
      fixedPolicy,pairPolicy,choosesForbidden]
    have hh : ∀ σ : Mode, ∀ s : State 1, forbiddenEven.priority σ (s,1) = 0 := by decide +kernel
    exact hh _ _
  have hr : ∀ e ∈ recurrentSet x, forbiddenEven.priority e.1 e.2 = 0 := by
    intro e he
    obtain ⟨t,ht⟩ := ((mem_recurrentSet x e).mp he).exists
    simpa only [ht] using hp t
  obtain ⟨e,he⟩ := recurrentSet_nonempty x
  exact ⟨0,⟨⟨e,he,hr e he⟩,fun e he => Nat.zero_le _⟩,rfl⟩

theorem forbidden_no_body : ¬ ∃ body : PositiveBody 1 2,
    positiveCheck forbiddenEven 0 body = true := by
  rw [positiveCheck_iff_region _ (by decide +kernel : Admissible forbiddenEven)]
  decide +kernel
theorem excluded_action : (1 : Action 2) ∉ commonMenu forbiddenEven 0 := by decide +kernel
end NecessityReview
#print axioms NecessityReview.forbidden_wins
#print axioms NecessityReview.forbidden_no_body
