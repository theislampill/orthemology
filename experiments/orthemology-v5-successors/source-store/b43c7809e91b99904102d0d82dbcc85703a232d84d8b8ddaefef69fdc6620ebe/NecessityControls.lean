import HiddenChangeNecessity

open HiddenChange MeasureTheory
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport
open HiddenParity HiddenParity.Stochastic HiddenParity.ResidualSeed
open HiddenParity.ResidualSeed.Continuation HiddenParity.Adaptive
open scoped ENNReal

namespace HiddenChangeNecessityTests

def singletonInput (a b : ℕ) : HiddenChange.Input 1 1 where
  rows := #[1,1]
  priorities := #[a,b]
  menus := [⟨[0,1],0,[0]⟩]
  interpretation := ⟨["zero","one"],["s"],["a"],"v1","state","exact","common"⟩

theorem singleton_admissible (a b : ℕ) : Admissible (singletonInput a b) := by
  change Admissible (singletonInput 0 0)
  decide +kernel

/-- The common-menu policy has no extra stochastic or semantic fields. -/
def solePolicy : Policy Unit 1 1 := fun _ _ => 0

example : PolicyLawful (singletonInput 0 0) 0 solePolicy := by
  intro r h
  have hs : currentState 0 h = 0 := Subsingleton.elim _ _
  rw [hs]
  change (0 : Action 1) ∈ commonMenu (singletonInput 0 0) 0
  decide +kernel

example : 0 ∈ policyUncertainRegion (singletonInput 0 0) (singleton_admissible 0 0).1
    0 (Measure.dirac ()) solePolicy := initial_mem_policyUncertainRegion _ _ _ _ _ (measurable_of_countable _)

-- Equality |h|=N is already post-switch, including the zero-length prefix.
example : 0 ∈ policyKnownRegion (singletonInput 0 0) (singleton_admissible 0 0).1
    0 (Measure.dirac ()) solePolicy := by
  apply (mem_policyKnownRegion _ _ _ _ _ _).mpr
  refine ⟨0,[],by simp,?_,rfl⟩
  rw [PositivePrefix,fixed_prefix_probability _ _ _ _ _ _ (measurable_of_countable _)]
  norm_num [CompatibleSeeds,ActionCompatible,fixedPrefixLikelihood]
  exact fun i => Fin.elim0 i

-- The exact fixed-mode condition, not just no-change parity, is necessary.
example {R : Type*} [MeasurableSpace R] (ρ : Measure R) [IsProbabilityMeasure ρ]
    (π : Policy R 1 1) (hπ : Measurable (fun z : R × PublicHistory 1 1 => π z.1 z.2))
    (hLaw : PolicyLawful (singletonInput 0 1) 0 π) :
    ¬ ∀ κ, ∀ᵐ H ∂fixedLaw (singletonInput 0 1) (singleton_admissible 0 1).1 κ 0 ρ π,
      TaggedParity (singletonInput 0 1) (0,0) H :=
  computed_exclusion_forbids_winner _ (singleton_admissible 0 1) _ ρ π hπ hLaw (0,0) (by decide +kernel)

example {R : Type*} [MeasurableSpace R] (ρ : Measure R) [IsProbabilityMeasure ρ]
    (π : Policy R 1 1) (hπ : Measurable (fun z : R × PublicHistory 1 1 => π z.1 z.2))
    (hLaw : PolicyLawful (singletonInput 0 0) 0 π)
    (hWin : ∀ κ, ∀ᵐ H ∂fixedLaw (singletonInput 0 0) (singleton_admissible 0 0).1 κ 0 ρ π,
      TaggedParity (singletonInput 0 0) (0,0) H) :
    ∃ body : PositiveBody 1 1, positiveCheck (singletonInput 0 0) 0 body = true :=
  winning_policy_has_positive_body _ (singleton_admissible 0 0) _ ρ π hπ hLaw (0,0) hWin

-- Positive past mass does not imply positivity of an unselected action branch.
def twoActions : Policy Unit 1 2 := fun _ _ => 0
example : ¬ PositiveSelected (0 : State 1) (Measure.dirac ()) twoActions [] (0,1) := by
  simp [PositiveSelected,SelectedSeeds,CompatibleSeeds,ActionCompatible,pairPolicy,twoActions]

theorem all_even_wins : ∀ κ, ∀ᵐ H ∂fixedLaw (singletonInput 0 0) (singleton_admissible 0 0).1
    κ 0 (Measure.dirac ()) solePolicy, TaggedParity (singletonInput 0 0) (0,0) H := by
  intro κ
  apply ae_of_all
  intro H
  have hprio : ∀ g : TaggedPair 1 1, (singletonInput 0 0).priority g.1 g.2 = 0 := by decide +kernel
  obtain ⟨g,hg⟩ := recurrentSet_nonempty (historyAction (0,(0,0)) H)
  refine ⟨0,⟨⟨g,hg,hprio g⟩,?_⟩,rfl⟩
  intro e _
  exact Nat.zero_le _

example : ∃ body : PositiveBody 1 1, positiveCheck (singletonInput 0 0) 0 body = true :=
  winning_policy_has_positive_body _ (singleton_admissible 0 0) _ (Measure.dirac ()) solePolicy
    (measurable_of_countable _) (by
      intro r h
      change (0 : Action 1) ∈ commonMenu (singletonInput 0 0) (currentState 0 h)
      have hs : currentState 0 h = 0 := Subsingleton.elim _ _
      rw [hs]
      decide +kernel) (0,0) all_even_wins

theorem noChange_only_wins : ∀ᵐ H ∂fixedLaw (singletonInput 0 1) (singleton_admissible 0 1).1
    none 0 (Measure.dirac ()) solePolicy, TaggedParity (singletonInput 0 1) (0,0) H := by
  apply (fixedLaw_physical_parity_iff _ _ _ _ _ _ (measurable_of_countable _) _).mpr
  apply ae_of_all
  intro H
  have hprio : ∀ e : Pair 1 1, (singletonInput 0 1).priority 0 e = 0 := by decide +kernel
  obtain ⟨e,he⟩ := recurrentSet_nonempty (historyAction (0,0) H)
  refine ⟨0,⟨⟨e,he,hprio e⟩,?_⟩,rfl⟩
  intro f _
  exact Nat.zero_le _

theorem noChange_only_no_body : ¬ ∃ body : PositiveBody 1 1,
    positiveCheck (singletonInput 0 1) 0 body = true := by
  rw [positiveCheck_iff_region _ (singleton_admissible 0 1)]
  decide +kernel

-- The original late prefix need not survive stationary mode1.
def lateInput : HiddenChange.Input 2 1 where
  rows := #[0,1,0,1, 1,0,0,1]
  priorities := #[0,0,0,0]
  menus := [⟨[0,1],0,[0]⟩,⟨[0,1],1,[0]⟩]
  interpretation := ⟨["zero","one"],["start","tail"],["a"],"v1","state","exact","common"⟩
theorem lateValid : lateInput.Valid := (by decide +kernel : Admissible lateInput).1
def latePolicy : Policy Unit 2 1 := fun _ _ => 0
def lateHistory : PairHistory 2 1 := [((0,0),1)]

theorem late_positive : PositivePrefix lateInput lateValid (some 1) 0 (Measure.dirac ()) latePolicy lateHistory := by
  rw [PositivePrefix,fixed_prefix_probability _ _ _ _ _ _ (measurable_of_countable _)]
  norm_num [CompatibleSeeds,ActionCompatible,pairPolicy,currentState,erasePairSources,latePolicy,
    lateHistory,fixedPrefixLikelihood,fixedMode,lateInput,OrthemicCertificate.Input.row,Fin.prod_univ_succ]

example : ¬ PositivePrefix lateInput lateValid (some 0) 0 (Measure.dirac ()) latePolicy lateHistory := by
  rw [PositivePrefix,fixed_prefix_probability _ _ _ _ _ _ (measurable_of_countable _)]
  norm_num [CompatibleSeeds,ActionCompatible,pairPolicy,currentState,erasePairSources,latePolicy,
    lateHistory,fixedPrefixLikelihood,fixedMode,lateInput,OrthemicCertificate.Input.row,Fin.prod_univ_succ]

example : 1 ∈ policyKnownRegion lateInput lateValid 0 (Measure.dirac ()) latePolicy :=
  (mem_policyKnownRegion _ _ _ _ _ _).mpr ⟨1,lateHistory,by decide,late_positive,rfl⟩

end HiddenChangeNecessityTests

#check HiddenChange.winning_policy_has_positive_body
#check HiddenChange.all_adversary_winner_has_positive_body
#check HiddenChange.computed_exclusion_forbids_winner
#print axioms HiddenChange.winning_policy_has_positive_body
#print axioms HiddenChange.all_adversary_winner_has_positive_body
#print axioms HiddenChange.computed_exclusion_forbids_winner
#print axioms HiddenChange.policyKnownRegion_postfixed
#print axioms HiddenChange.policyUncertainRegion_postfixed
#print axioms HiddenChange.fixedPhysicalLaw_recurrent_component
#print axioms HiddenChange.selected_uncertainAllowed
#print axioms HiddenChange.positive_compatible_recurrent_even
