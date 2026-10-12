import SCCRegionControls

namespace IndependentSCCRegionReview
open HiddenParity
open HiddenParity.SCCRegion
open HiddenParity.SCCRegion.ExtraControls

-- The equality theorem has no nonemptiness, semantic winning or target premise.
theorem arbitrary_fuel_refinement (n : ℕ) (B : Finset M) :
    computedRegion kernel menu sharedEven n B =
      Necessity.computedRegion kernel menu sharedEven n B :=
  computedRegion_eq kernel menu sharedEven n B

theorem zero_fuel_is_not_the_public_certificate :
    computedRegion kernel menu sharedEven 0 Finset.univ = ∅ ∧
    winningRegion kernel menu sharedEven Finset.univ = Finset.univ := by
  constructor
  · rfl
  · exact shared_even_action_retained

theorem keep_the_rival_quantifier :
    winningRegion kernel menu opposite Finset.univ = ∅ :=
  incompatible_rival_minima_reject

theorem no_odd_visit_coBuchi_substitution :
    HiddenParity.SCCRegion.winningRegion
      Necessity.Controls.cycleKernel Necessity.Controls.cycleMenu
      (Necessity.Controls.cyclePriority 3) Finset.univ = Finset.univ :=
  HiddenParity.SCCRegion.Controls.higher_odd_recurs_and_wins

theorem empty_live_support_not_a_witness :
    computedRegion kernel menu sharedEven 5 ∅ = ∅ := by decide

#print axioms arbitrary_fuel_refinement
#print axioms zero_fuel_is_not_the_public_certificate
#print axioms keep_the_rival_quantifier
#print axioms no_odd_visit_coBuchi_substitution
#print axioms empty_live_support_not_a_witness
end IndependentSCCRegionReview
#print axioms HiddenParity.SCCRegion.winning_policy_mem_winningRegion
#print axioms HiddenParity.SCCRegion.computed_losing_excludes_common_policy
#print axioms HiddenParity.SCCRegion.computedRegion_fuel_irrelevant
