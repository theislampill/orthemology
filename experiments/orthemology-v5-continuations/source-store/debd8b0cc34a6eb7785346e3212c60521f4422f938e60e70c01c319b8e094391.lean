import RankTransport
import LowerEnvelopeBudget
import PERRefinement
import PERPotentialFormula
import MealyRefinement
import MealySharpness
import GuardedRefinement
import BlockMismatch

open Orthemology.Frontier

#print liftedRank_step
#print axioms liftedRank_step
#print liftedRank_run_bound
#print axioms liftedRank_run_bound
#print target_after_liftedRank
#print axioms target_after_liftedRank
#print matched_run
#print axioms matched_run
#print restoration_transport
#print axioms restoration_transport
#print exists_policy_run
#print axioms exists_policy_run
#print PER.potential_strict
#print axioms PER.potential_strict
#print PER.potential_le
#print axioms PER.potential_le
#print PER.strict_chain_length
#print axioms PER.strict_chain_length
#print PER.stabilization_bound
#print axioms PER.stabilization_bound
#print Mealy.stabilization_bound
#print axioms Mealy.stabilization_bound
#print Mealy.bound_iff_infinite
#print axioms Mealy.bound_iff_infinite
#print Mealy.approx_iff_words
#print axioms Mealy.approx_iff_words
#print Mealy.distinguishing_words
#print axioms Mealy.distinguishing_words
#print Mealy.Fixtures.two_state_requires_three
#print axioms Mealy.Fixtures.two_state_requires_three
#print Mealy.Fixtures.three_state_requires_five
#print axioms Mealy.Fixtures.three_state_requires_five
#print axioms RankFixtures.overlap_coverage
#print axioms RankFixtures.overlap_lifted_ranks
#print axioms RankFixtures.stale_coverage_fails

#print Mealy.surviving_input_words_bound
#print axioms Mealy.surviving_input_words_bound
#print Mealy.surviving_uniform_fraction_bound
#print axioms Mealy.surviving_uniform_fraction_bound
#print BoundedPaths.mem_words_succ
#print axioms BoundedPaths.mem_words_succ
#print Mealy.deterministic_domain_closed
#print axioms Mealy.deterministic_domain_closed

#print PER.potential_formula
#print axioms PER.potential_formula

#print Mealy.sharp_family_all_sizes
#print axioms Mealy.sharp_family_all_sizes
#print Mealy.sharp_every_cardinality
#print axioms Mealy.sharp_every_cardinality
#print Mealy.one_state_sharp
#print axioms Mealy.one_state_sharp

#print BoundedPaths.card_all_words
#print axioms BoundedPaths.card_all_words
#print axioms BoundedPaths.length_of_mem_words
#print axioms BoundedPaths.words_subset_all

#print Mealy.guardedApprox_eq
#print axioms Mealy.guardedApprox_eq
#print Mealy.guarded_sharp_every_cardinality
#print axioms Mealy.guarded_sharp_every_cardinality

#print lowerRank_step
#print axioms lowerRank_step
#print badVisits_add_rank_le
#print axioms badVisits_add_rank_le
#print eventually_no_bad_of_budget
#print axioms eventually_no_bad_of_budget
#print lowerRank_preserves_eventual_good
#print axioms lowerRank_preserves_eventual_good

#print LowerBudgetFixtures.arbitrarily_late_bad_visit
#print axioms LowerBudgetFixtures.arbitrarily_late_bad_visit
#print axioms LowerBudgetFixtures.stale_bad_reflection_fails
