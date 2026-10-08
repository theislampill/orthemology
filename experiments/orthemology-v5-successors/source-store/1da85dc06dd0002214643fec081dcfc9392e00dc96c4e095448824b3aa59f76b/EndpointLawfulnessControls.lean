import HiddenChangeSemanticEndpoint
open HiddenChange HiddenParity MeasureTheory
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport
open HiddenParity.Stochastic
namespace EndpointLawfulness
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

universe uZ
theorem forbidden_winsAll : WinsAll.{uZ} forbiddenEven
    (by decide +kernel : Admissible forbiddenEven).1 0 (Measure.dirac ()) choosesForbidden (0,0) :=
  (winsAll_iff_fixed_indices _ _ _ _ _ (measurable_of_countable _) _).mpr forbidden_wins

theorem forbidden_not_lawful : ¬ AllHistoryLawful forbiddenEven 0 choosesForbidden := by
  intro h
  exact excluded_action (h () [])

theorem forbidden_not_semantic_winner :
    ¬ LawfulMeasurableWinner.{0,uZ} forbiddenEven
      (by decide +kernel : Admissible forbiddenEven).1 0 (Measure.dirac ()) choosesForbidden (0,0) := by
  intro h
  exact forbidden_not_lawful h.2.1
end EndpointLawfulness
