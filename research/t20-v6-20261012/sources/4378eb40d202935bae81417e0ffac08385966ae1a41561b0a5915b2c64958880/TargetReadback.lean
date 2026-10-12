import SelfVerifyingSupport
import SupportStageCertificate
import SupportFixtures
import FiniteLikelihood
import AdaptiveLikelihood
import LikelihoodProducts
import BlockController
import CanonicalBlockPolicy
import dependencies.StatisticalRepair
import HellingerTree
import BlockKernel
import HellingerPolicy
import SubprobHellinger
import StoppedBlock
import ResidualDeficit
import DependentHellinger
import StoppedPhasePolicy
import ResetBudget
import ResetLaw
import WeightedPotential
import ResetHellinger
import LiveSourceCertificate
import LiveStoppedController
import FiniteBudgetAlmostSure
import GuardedResetBudget
import GuardedResetHellinger
import GuardedLiveController
import StoppedActionCost
import ResetTrajectory
import ResetFutureCost
import MarkovCharge
import ResetExpectation
import TrajectoryBudget
import GeneratedLiveController
#check @Orthemology.Tranche2.AgreeOn
#print axioms Orthemology.Tranche2.AgreeOn
#check @Orthemology.Tranche2.SelfVerifying
#print axioms Orthemology.Tranche2.SelfVerifying
#check @Orthemology.Tranche2.prune
#print axioms Orthemology.Tranche2.prune
#check @Orthemology.Tranche2.mem_prune
#print axioms Orthemology.Tranche2.mem_prune
#check @Orthemology.Tranche2.prune_subset
#print axioms Orthemology.Tranche2.prune_subset
#check @Orthemology.Tranche2.agreeOn_mono
#print axioms Orthemology.Tranche2.agreeOn_mono
#check @Orthemology.Tranche2.prune_mono
#print axioms Orthemology.Tranche2.prune_mono
#check @Orthemology.Tranche2.selfVerifying_empty
#print axioms Orthemology.Tranche2.selfVerifying_empty
#check @Orthemology.Tranche2.selfVerifying_union
#print axioms Orthemology.Tranche2.selfVerifying_union
#check @Orthemology.Tranche2.selfVerifying_iff_fixed
#print axioms Orthemology.Tranche2.selfVerifying_iff_fixed
#check @Orthemology.Tranche2.pruneIter
#print axioms Orthemology.Tranche2.pruneIter
#check @Orthemology.Tranche2.pruneIter_step_subset
#print axioms Orthemology.Tranche2.pruneIter_step_subset
#check @Orthemology.Tranche2.pruneIter_subset_target
#print axioms Orthemology.Tranche2.pruneIter_subset_target
#check @Orthemology.Tranche2.selfVerifying_survives
#print axioms Orthemology.Tranche2.selfVerifying_survives
#check @Orthemology.Tranche2.pruneIter_fixed_propagates
#print axioms Orthemology.Tranche2.pruneIter_fixed_propagates
#check @Orthemology.Tranche2.pruneIter_card_bound_of_no_fixed
#print axioms Orthemology.Tranche2.pruneIter_card_bound_of_no_fixed
#check @Orthemology.Tranche2.pruneIter_exists_fixed
#print axioms Orthemology.Tranche2.pruneIter_exists_fixed
#check @Orthemology.Tranche2.pruneIter_card_fixed
#print axioms Orthemology.Tranche2.pruneIter_card_fixed
#check @Orthemology.Tranche2.supportKernel
#print axioms Orthemology.Tranche2.supportKernel
#check @Orthemology.Tranche2.supportKernel_selfVerifying
#print axioms Orthemology.Tranche2.supportKernel_selfVerifying
#check @Orthemology.Tranche2.supportKernel_greatest
#print axioms Orthemology.Tranche2.supportKernel_greatest
#check @Orthemology.Tranche2.supportKernel_nonempty_iff
#print axioms Orthemology.Tranche2.supportKernel_nonempty_iff
#check @Orthemology.Tranche2.StageWitness
#print axioms Orthemology.Tranche2.StageWitness
#check @Orthemology.Tranche2.RestrictedTargets
#print axioms Orthemology.Tranche2.RestrictedTargets
#check @Orthemology.Tranche2.selfVerifying_restrict_iff
#print axioms Orthemology.Tranche2.selfVerifying_restrict_iff
#check @Orthemology.Tranche2.StageCertificate
#print axioms Orthemology.Tranche2.StageCertificate
#check @Orthemology.Tranche2.stageCertificate_iff_witness
#print axioms Orthemology.Tranche2.stageCertificate_iff_witness
#check @Orthemology.Tranche2.selfVerifying_signal_refinement
#print axioms Orthemology.Tranche2.selfVerifying_signal_refinement
#check @Orthemology.Tranche2.supportKernel_signal_refinement
#print axioms Orthemology.Tranche2.supportKernel_signal_refinement
#check @Orthemology.Tranche2.supportKernel_target_enlargement
#print axioms Orthemology.Tranche2.supportKernel_target_enlargement
#check @Orthemology.Tranche2.Fixtures.cascadeSame
#print axioms Orthemology.Tranche2.Fixtures.cascadeSame
#check @Orthemology.Tranche2.Fixtures.cascadeGood
#print axioms Orthemology.Tranche2.Fixtures.cascadeGood
#check @Orthemology.Tranche2.Fixtures.cascade_no_nonempty_support
#print axioms Orthemology.Tranche2.Fixtures.cascade_no_nonempty_support
#check @Orthemology.Tranche2.Fixtures.cascade_kernel_empty
#print axioms Orthemology.Tranche2.Fixtures.cascade_kernel_empty
#check @Orthemology.Tranche2.Fixtures.cascade_first_round
#print axioms Orthemology.Tranche2.Fixtures.cascade_first_round
#check @Orthemology.Tranche2.Fixtures.cascade_second_round
#print axioms Orthemology.Tranche2.Fixtures.cascade_second_round
#check @Orthemology.Tranche2.Fixtures.informativeGood
#print axioms Orthemology.Tranche2.Fixtures.informativeGood
#check @Orthemology.Tranche2.Fixtures.informativeSame
#print axioms Orthemology.Tranche2.Fixtures.informativeSame
#check @Orthemology.Tranche2.Fixtures.informative_singleton_valid
#print axioms Orthemology.Tranche2.Fixtures.informative_singleton_valid
#check @Orthemology.Tranche2.Fixtures.informative_kernel
#print axioms Orthemology.Tranche2.Fixtures.informative_kernel
#check @Orthemology.Tranche2.Fixtures.informative_all_kernels_nonempty
#print axioms Orthemology.Tranche2.Fixtures.informative_all_kernels_nonempty
#check @Orthemology.Tranche2.Fixtures.informative_no_common_target
#print axioms Orthemology.Tranche2.Fixtures.informative_no_common_target
#check @Orthemology.Tranche2.logScore
#print axioms Orthemology.Tranche2.logScore
#check @Orthemology.Tranche2.finiteKL
#print axioms Orthemology.Tranche2.finiteKL
#check @Orthemology.Tranche2.finiteKL_eq_sum_klFun
#print axioms Orthemology.Tranche2.finiteKL_eq_sum_klFun
#check @Orthemology.Tranche2.finiteKL_nonneg
#print axioms Orthemology.Tranche2.finiteKL_nonneg
#check @Orthemology.Tranche2.finiteKL_pos
#print axioms Orthemology.Tranche2.finiteKL_pos
#check @Orthemology.Tranche2.logScore_self
#print axioms Orthemology.Tranche2.logScore_self
#check @Orthemology.Tranche2.logScore_integrable_comp
#print axioms Orthemology.Tranche2.logScore_integrable_comp
#check @Orthemology.Tranche2.logScore_expectation
#print axioms Orthemology.Tranche2.logScore_expectation
#check @Orthemology.Tranche2.logScore_strong_law
#print axioms Orthemology.Tranche2.logScore_strong_law
#check @Orthemology.Tranche2.sums_tendsto_atTop_of_average
#print axioms Orthemology.Tranche2.sums_tendsto_atTop_of_average
#check @Orthemology.Tranche2.logScore_sum_tendsto_atTop
#print axioms Orthemology.Tranche2.logScore_sum_tendsto_atTop
#check @Orthemology.Tranche2.finite_sum_tendsto_atTop_of_one
#print axioms Orthemology.Tranche2.finite_sum_tendsto_atTop_of_one
#check @Orthemology.Tranche2.sampled_logScore_tendsto_atTop
#print axioms Orthemology.Tranche2.sampled_logScore_tendsto_atTop
#check @Orthemology.Tranche2.sampled_logScore_tendsto_of_joint_independent
#print axioms Orthemology.Tranche2.sampled_logScore_tendsto_of_joint_independent
#check @Orthemology.Tranche2.prefixLikelihood
#print axioms Orthemology.Tranche2.prefixLikelihood
#check @Orthemology.Tranche2.prefixLikelihood_pos
#print axioms Orthemology.Tranche2.prefixLikelihood_pos
#check @Orthemology.Tranche2.log_prefixLikelihood
#print axioms Orthemology.Tranche2.log_prefixLikelihood
#check @Orthemology.Tranche2.log_prefixLikelihood_ratio
#print axioms Orthemology.Tranche2.log_prefixLikelihood_ratio
#check @Orthemology.Tranche2.inverse_prefixLikelihood_ratio
#print axioms Orthemology.Tranche2.inverse_prefixLikelihood_ratio
#check @Orthemology.Tranche2.sampled_false_likelihood_ratio_tendsto_zero
#print axioms Orthemology.Tranche2.sampled_false_likelihood_ratio_tendsto_zero
#check @Orthemology.Tranche2.blockCount
#print axioms Orthemology.Tranche2.blockCount
#check @Orthemology.Tranche2.count_tendsto_of_infinite
#print axioms Orthemology.Tranche2.count_tendsto_of_infinite
#check @Orthemology.Tranche2.blockCount_tendsto_of_selected_infinite
#print axioms Orthemology.Tranche2.blockCount_tendsto_of_selected_infinite
#check @Orthemology.Tranche2.likelihood_block_controller_eventually_good
#print axioms Orthemology.Tranche2.likelihood_block_controller_eventually_good
#check @Orthemology.Tranche2.greedyMax
#print axioms Orthemology.Tranche2.greedyMax
#check @Orthemology.Tranche2.greedyMax_ge
#print axioms Orthemology.Tranche2.greedyMax_ge
#check @Orthemology.Tranche2.historyCount
#print axioms Orthemology.Tranche2.historyCount
#check @Orthemology.Tranche2.candidateFor
#print axioms Orthemology.Tranche2.candidateFor
#check @Orthemology.Tranche2.canonicalHistory
#print axioms Orthemology.Tranche2.canonicalHistory
#check @Orthemology.Tranche2.canonicalSelected
#print axioms Orthemology.Tranche2.canonicalSelected
#check @Orthemology.Tranche2.canonicalHistory_eq_range_map
#print axioms Orthemology.Tranche2.canonicalHistory_eq_range_map
#check @Orthemology.Tranche2.historyCount_eq_blockCount
#print axioms Orthemology.Tranche2.historyCount_eq_blockCount
#check @Orthemology.Tranche2.canonicalSelected_maximizes
#print axioms Orthemology.Tranche2.canonicalSelected_maximizes
#check @Orthemology.Tranche2.candidateFor_prefix_local
#print axioms Orthemology.Tranche2.candidateFor_prefix_local
#check @Orthemology.Tranche2.greedyMax_measurable
#print axioms Orthemology.Tranche2.greedyMax_measurable
#check @Orthemology.Tranche2.candidateFor_measurable
#print axioms Orthemology.Tranche2.candidateFor_measurable
#check @Orthemology.Tranche2.measurable_countable_diagonal
#print axioms Orthemology.Tranche2.measurable_countable_diagonal
#check @Orthemology.Tranche2.canonicalSelected_measurable
#print axioms Orthemology.Tranche2.canonicalSelected_measurable
#check @Orthemology.Tranche2.canonical_block_policy_eventually_good
#print axioms Orthemology.Tranche2.canonical_block_policy_eventually_good
#check @Orthemology.Tranche2.affinity
#print axioms Orthemology.Tranche2.affinity
#check @Orthemology.Tranche2.errorP
#print axioms Orthemology.Tranche2.errorP
#check @Orthemology.Tranche2.errorQ
#print axioms Orthemology.Tranche2.errorQ
#check @Orthemology.Tranche2.minimum_le_test_error
#print axioms Orthemology.Tranche2.minimum_le_test_error
#check @Orthemology.Tranche2.sqrt_product_min_max
#print axioms Orthemology.Tranche2.sqrt_product_min_max
#check @Orthemology.Tranche2.affinity_sq_le_twice_error_sum
#print axioms Orthemology.Tranche2.affinity_sq_le_twice_error_sum
#check @Orthemology.Tranche2.affinity_error_lower_bound
#print axioms Orthemology.Tranche2.affinity_error_lower_bound
#check @Orthemology.Tranche2.affinity_nonneg
#print axioms Orthemology.Tranche2.affinity_nonneg
#check @Orthemology.Tranche2.affinity_tensor
#print axioms Orthemology.Tranche2.affinity_tensor
#check @Orthemology.Tranche2.Bits
#print axioms Orthemology.Tranche2.Bits
#check @Orthemology.Tranche2.bitsFintype
#print axioms Orthemology.Tranche2.bitsFintype
#check @Orthemology.Tranche2.coinMass
#print axioms Orthemology.Tranche2.coinMass
#check @Orthemology.Tranche2.bernoulliMass
#print axioms Orthemology.Tranche2.bernoulliMass
#check @Orthemology.Tranche2.coinMass_nonneg
#print axioms Orthemology.Tranche2.coinMass_nonneg
#check @Orthemology.Tranche2.bernoulliMass_nonneg
#print axioms Orthemology.Tranche2.bernoulliMass_nonneg
#check @Orthemology.Tranche2.bernoulliMass_sum
#print axioms Orthemology.Tranche2.bernoulliMass_sum
#check @Orthemology.Tranche2.coin_affinity
#print axioms Orthemology.Tranche2.coin_affinity
#check @Orthemology.Tranche2.bernoulli_affinity
#print axioms Orthemology.Tranche2.bernoulli_affinity
#check @Orthemology.Tranche2.symmetric_coin_affinity_sq
#print axioms Orthemology.Tranche2.symmetric_coin_affinity_sq
#check @Orthemology.Tranche2.symmetric_bernoulli_test_lower_bound
#print axioms Orthemology.Tranche2.symmetric_bernoulli_test_lower_bound
#check @Orthemology.Tranche2.affinity_sq_distance
#print axioms Orthemology.Tranche2.affinity_sq_distance
#check @Orthemology.Tranche2.affinity_le_one
#print axioms Orthemology.Tranche2.affinity_le_one
#check @Orthemology.Tranche2.affinity_lt_one
#print axioms Orthemology.Tranche2.affinity_lt_one
#check @Orthemology.Tranche2.historyMass
#print axioms Orthemology.Tranche2.historyMass
#check @Orthemology.Tranche2.historyAffinity
#print axioms Orthemology.Tranche2.historyAffinity
#check @Orthemology.Tranche2.historyMass_nonneg
#print axioms Orthemology.Tranche2.historyMass_nonneg
#check @Orthemology.Tranche2.historyAffinity_nonneg
#print axioms Orthemology.Tranche2.historyAffinity_nonneg
#check @Orthemology.Tranche2.historyAffinity_branch_sum
#print axioms Orthemology.Tranche2.historyAffinity_branch_sum
#check @Orthemology.Tranche2.levelMass
#print axioms Orthemology.Tranche2.levelMass
#check @Orthemology.Tranche2.levelMass_normalized
#print axioms Orthemology.Tranche2.levelMass_normalized
#check @Orthemology.Tranche2.selectedCost
#print axioms Orthemology.Tranche2.selectedCost
#check @Orthemology.Tranche2.leafAffinity
#print axioms Orthemology.Tranche2.leafAffinity
#check @Orthemology.Tranche2.leafAffinity_nonneg
#print axioms Orthemology.Tranche2.leafAffinity_nonneg
#check @Orthemology.Tranche2.mass_le_affinity_of_le
#print axioms Orthemology.Tranche2.mass_le_affinity_of_le
#check @Orthemology.Tranche2.hellinger_tree_budget
#print axioms Orthemology.Tranche2.hellinger_tree_budget
#check @Orthemology.Tranche2.selectedCost_uniform_bound
#print axioms Orthemology.Tranche2.selectedCost_uniform_bound
#check @Orthemology.Tranche2.selectedCost_iSup_bound
#print axioms Orthemology.Tranche2.selectedCost_iSup_bound
#check @Orthemology.Tranche2.sqrt_finset_prod
#print axioms Orthemology.Tranche2.sqrt_finset_prod
#check @Orthemology.Tranche2.affinity_product_coordinates
#print axioms Orthemology.Tranche2.affinity_product_coordinates
#check @Orthemology.Tranche2.blockCoordinate
#print axioms Orthemology.Tranche2.blockCoordinate
#check @Orthemology.Tranche2.blockMass
#print axioms Orthemology.Tranche2.blockMass
#check @Orthemology.Tranche2.blockCoordinate_nonneg
#print axioms Orthemology.Tranche2.blockCoordinate_nonneg
#check @Orthemology.Tranche2.blockCoordinate_sum
#print axioms Orthemology.Tranche2.blockCoordinate_sum
#check @Orthemology.Tranche2.blockMass_nonneg
#print axioms Orthemology.Tranche2.blockMass_nonneg
#check @Orthemology.Tranche2.blockMass_normalized
#print axioms Orthemology.Tranche2.blockMass_normalized
#check @Orthemology.Tranche2.blockCoordinate_affinity
#print axioms Orthemology.Tranche2.blockCoordinate_affinity
#check @Orthemology.Tranche2.blockMass_affinity
#print axioms Orthemology.Tranche2.blockMass_affinity
#check @Orthemology.Tranche2.blockMass_zero_of_unselected
#print axioms Orthemology.Tranche2.blockMass_zero_of_unselected
#check @Orthemology.Tranche2.blockMass_affinity_lt_one
#print axioms Orthemology.Tranche2.blockMass_affinity_lt_one
#check @Orthemology.Tranche2.treeMLE
#print axioms Orthemology.Tranche2.treeMLE
#check @Orthemology.Tranche2.treeMLE_maximizes
#print axioms Orthemology.Tranche2.treeMLE_maximizes
#check @Orthemology.Tranche2.treeMLE_expected_selections_bound
#print axioms Orthemology.Tranche2.treeMLE_expected_selections_bound
#check @Orthemology.Tranche2.affinity_self_one
#print axioms Orthemology.Tranche2.affinity_self_one
#check @Orthemology.Tranche2.supportBlockKernel
#print axioms Orthemology.Tranche2.supportBlockKernel
#check @Orthemology.Tranche2.supportBlock_expected_selections_bound
#print axioms Orthemology.Tranche2.supportBlock_expected_selections_bound
#check @Orthemology.Tranche2.affinity_sq_le_mass_product
#print axioms Orthemology.Tranche2.affinity_sq_le_mass_product
#check @Orthemology.Tranche2.affinity_le_one_subprob
#print axioms Orthemology.Tranche2.affinity_le_one_subprob
#check @Orthemology.Tranche2.affinity_lt_one_of_mass_lt_right
#print axioms Orthemology.Tranche2.affinity_lt_one_of_mass_lt_right
#check @Orthemology.Tranche2.killedLaw
#print axioms Orthemology.Tranche2.killedLaw
#check @Orthemology.Tranche2.killedLaw_nonneg
#print axioms Orthemology.Tranche2.killedLaw_nonneg
#check @Orthemology.Tranche2.killedLaw_le
#print axioms Orthemology.Tranche2.killedLaw_le
#check @Orthemology.Tranche2.killedLaw_sum_le
#print axioms Orthemology.Tranche2.killedLaw_sum_le
#check @Orthemology.Tranche2.killedLaw_affinity_le
#print axioms Orthemology.Tranche2.killedLaw_affinity_le
#check @Orthemology.Tranche2.killedLaw_affinity_formula
#print axioms Orthemology.Tranche2.killedLaw_affinity_formula
#check @Orthemology.Tranche2.hellinger_subprob_tree_budget
#print axioms Orthemology.Tranche2.hellinger_subprob_tree_budget
#check @Orthemology.Tranche2.selectedCost_subprob_uniform_bound
#print axioms Orthemology.Tranche2.selectedCost_subprob_uniform_bound
#check @Orthemology.Tranche2.StopObs
#print axioms Orthemology.Tranche2.StopObs
#check @Orthemology.Tranche2.stopObsFintype
#print axioms Orthemology.Tranche2.stopObsFintype
#check @Orthemology.Tranche2.stopCompleted
#print axioms Orthemology.Tranche2.stopCompleted
#check @Orthemology.Tranche2.stoppedMass
#print axioms Orthemology.Tranche2.stoppedMass
#check @Orthemology.Tranche2.stoppedMass_nonneg
#print axioms Orthemology.Tranche2.stoppedMass_nonneg
#check @Orthemology.Tranche2.stoppedMass_normalized
#print axioms Orthemology.Tranche2.stoppedMass_normalized
#check @Orthemology.Tranche2.survivalMass
#print axioms Orthemology.Tranche2.survivalMass
#check @Orthemology.Tranche2.survivalAffinity
#print axioms Orthemology.Tranche2.survivalAffinity
#check @Orthemology.Tranche2.residualActionAffinity
#print axioms Orthemology.Tranche2.residualActionAffinity
#check @Orthemology.Tranche2.stayMass
#print axioms Orthemology.Tranche2.stayMass
#check @Orthemology.Tranche2.survivalAffinity_cons
#print axioms Orthemology.Tranche2.survivalAffinity_cons
#check @Orthemology.Tranche2.survivalAffinity_product
#print axioms Orthemology.Tranche2.survivalAffinity_product
#check @Orthemology.Tranche2.survivalMass_cons
#print axioms Orthemology.Tranche2.survivalMass_cons
#check @Orthemology.Tranche2.survivalMass_product
#print axioms Orthemology.Tranche2.survivalMass_product
#check @Orthemology.Tranche2.survivalMass_le_one
#print axioms Orthemology.Tranche2.survivalMass_le_one
#check @Orthemology.Tranche2.survivalAffinity_eq_killed
#print axioms Orthemology.Tranche2.survivalAffinity_eq_killed
#check @Orthemology.Tranche2.stayMass_nonneg
#print axioms Orthemology.Tranche2.stayMass_nonneg
#check @Orthemology.Tranche2.stayMass_le_one
#print axioms Orthemology.Tranche2.stayMass_le_one
#check @Orthemology.Tranche2.stayMass_lt_one_of_exit
#print axioms Orthemology.Tranche2.stayMass_lt_one_of_exit
#check @Orthemology.Tranche2.mapped_prod_nonneg
#print axioms Orthemology.Tranche2.mapped_prod_nonneg
#check @Orthemology.Tranche2.mapped_prod_le_one
#print axioms Orthemology.Tranche2.mapped_prod_le_one
#check @Orthemology.Tranche2.mapped_prod_le_member
#print axioms Orthemology.Tranche2.mapped_prod_le_member
#check @Orthemology.Tranche2.survivalMass_lt_one_of_progress
#print axioms Orthemology.Tranche2.survivalMass_lt_one_of_progress
#check @Orthemology.Tranche2.survivalAffinity_lt_one_of_progress
#print axioms Orthemology.Tranche2.survivalAffinity_lt_one_of_progress
#check @Orthemology.Tranche2.residualActionAffinity_nonneg
#print axioms Orthemology.Tranche2.residualActionAffinity_nonneg
#check @Orthemology.Tranche2.residualActionAffinity_le_full
#print axioms Orthemology.Tranche2.residualActionAffinity_le_full
#check @Orthemology.Tranche2.survivalAffinity_lt_one_of_informative
#print axioms Orthemology.Tranche2.survivalAffinity_lt_one_of_informative
#check @Orthemology.Tranche2.certificate_implies_strict_residual
#print axioms Orthemology.Tranche2.certificate_implies_strict_residual
#check @Orthemology.Tranche2.dHistoryMass
#print axioms Orthemology.Tranche2.dHistoryMass
#check @Orthemology.Tranche2.dHistoryAffinity
#print axioms Orthemology.Tranche2.dHistoryAffinity
#check @Orthemology.Tranche2.dHistoryMass_nonneg
#print axioms Orthemology.Tranche2.dHistoryMass_nonneg
#check @Orthemology.Tranche2.dHistoryAffinity_nonneg
#print axioms Orthemology.Tranche2.dHistoryAffinity_nonneg
#check @Orthemology.Tranche2.dHistoryAffinity_branch_sum
#print axioms Orthemology.Tranche2.dHistoryAffinity_branch_sum
#check @Orthemology.Tranche2.dLevelMass
#print axioms Orthemology.Tranche2.dLevelMass
#check @Orthemology.Tranche2.dLevelMass_normalized
#print axioms Orthemology.Tranche2.dLevelMass_normalized
#check @Orthemology.Tranche2.dSelectedCost
#print axioms Orthemology.Tranche2.dSelectedCost
#check @Orthemology.Tranche2.dLeafAffinity
#print axioms Orthemology.Tranche2.dLeafAffinity
#check @Orthemology.Tranche2.dLeafAffinity_nonneg
#print axioms Orthemology.Tranche2.dLeafAffinity_nonneg
#check @Orthemology.Tranche2.dMass_le_affinity_of_le
#print axioms Orthemology.Tranche2.dMass_le_affinity_of_le
#check @Orthemology.Tranche2.dependent_hellinger_tree_budget
#print axioms Orthemology.Tranche2.dependent_hellinger_tree_budget
#check @Orthemology.Tranche2.dSelectedCost_subprob_uniform_bound
#print axioms Orthemology.Tranche2.dSelectedCost_subprob_uniform_bound
#check @Orthemology.Tranche2.dependentTreeMLE
#print axioms Orthemology.Tranche2.dependentTreeMLE
#check @Orthemology.Tranche2.dependentTreeMLE_maximizes
#print axioms Orthemology.Tranche2.dependentTreeMLE_maximizes
#check @Orthemology.Tranche2.stoppedFullKernel
#print axioms Orthemology.Tranche2.stoppedFullKernel
#check @Orthemology.Tranche2.stoppedPhaseKernel
#print axioms Orthemology.Tranche2.stoppedPhaseKernel
#check @Orthemology.Tranche2.stoppedPhaseKernel_nonneg
#print axioms Orthemology.Tranche2.stoppedPhaseKernel_nonneg
#check @Orthemology.Tranche2.stoppedPhaseKernel_subprob
#print axioms Orthemology.Tranche2.stoppedPhaseKernel_subprob
#check @Orthemology.Tranche2.stoppedPhaseKernel_affinity
#print axioms Orthemology.Tranche2.stoppedPhaseKernel_affinity
#check @Orthemology.Tranche2.stoppedPhase_historyMass_eq_full
#print axioms Orthemology.Tranche2.stoppedPhase_historyMass_eq_full
#check @Orthemology.Tranche2.stoppedPhase_MLE_eq_full
#print axioms Orthemology.Tranche2.stoppedPhase_MLE_eq_full
#check @Orthemology.Tranche2.stoppedPhase_expected_selections_bound
#print axioms Orthemology.Tranche2.stoppedPhase_expected_selections_bound
#check @Orthemology.Tranche2.PhaseHistory
#print axioms Orthemology.Tranche2.PhaseHistory
#check @Orthemology.Tranche2.continuingKernel
#print axioms Orthemology.Tranche2.continuingKernel
#check @Orthemology.Tranche2.resetCost
#print axioms Orthemology.Tranche2.resetCost
#check @Orthemology.Tranche2.resetCost_bound
#print axioms Orthemology.Tranche2.resetCost_bound
#check @Orthemology.Tranche2.resetCost_root_bound
#print axioms Orthemology.Tranche2.resetCost_root_bound
#check @Orthemology.Tranche2.resetLeafMass
#print axioms Orthemology.Tranche2.resetLeafMass
#check @Orthemology.Tranche2.resetLeafMass_normalized
#print axioms Orthemology.Tranche2.resetLeafMass_normalized
#check @Orthemology.Tranche2.resetLeafCost
#print axioms Orthemology.Tranche2.resetLeafCost
#check @Orthemology.Tranche2.resetLeafCost_eq_budget
#print axioms Orthemology.Tranche2.resetLeafCost_eq_budget
#check @Orthemology.Tranche2.weightedHellinger
#print axioms Orthemology.Tranche2.weightedHellinger
#check @Orthemology.Tranche2.weightedHellinger_nonneg
#print axioms Orthemology.Tranche2.weightedHellinger_nonneg
#check @Orthemology.Tranche2.weightedHellinger_root
#print axioms Orthemology.Tranche2.weightedHellinger_root
#check @Orthemology.Tranche2.weightedHellinger_step
#print axioms Orthemology.Tranche2.weightedHellinger_step
#check @Orthemology.Tranche2.deficit_weight_certificate
#print axioms Orthemology.Tranche2.deficit_weight_certificate
#check @Orthemology.Tranche2.reset_hellinger_budget
#print axioms Orthemology.Tranche2.reset_hellinger_budget
#check @Orthemology.Tranche2.liveTreeMLE
#print axioms Orthemology.Tranche2.liveTreeMLE
#check @Orthemology.Tranche2.liveTreeMLE_maximizes
#print axioms Orthemology.Tranche2.liveTreeMLE_maximizes
#check @Orthemology.Tranche2.LiveSelfVerifying
#print axioms Orthemology.Tranche2.LiveSelfVerifying
#check @Orthemology.Tranche2.live_certificate_implies_strict_residual
#print axioms Orthemology.Tranche2.live_certificate_implies_strict_residual
#check @Orthemology.Tranche2.greedyMax_mem
#print axioms Orthemology.Tranche2.greedyMax_mem
#check @Orthemology.Tranche2.greedyMax_live_mem
#print axioms Orthemology.Tranche2.greedyMax_live_mem
#check @Orthemology.Tranche2.live_stopped_controller_budget
#print axioms Orthemology.Tranche2.live_stopped_controller_budget
#check @Orthemology.Tranche2.finite_budget_eventually_avoids
#print axioms Orthemology.Tranche2.finite_budget_eventually_avoids
#check @Orthemology.Tranche2.expected_event_count_eq_tsum
#print axioms Orthemology.Tranche2.expected_event_count_eq_tsum
#check @Orthemology.Tranche2.finite_tree_budget_transfer
#print axioms Orthemology.Tranche2.finite_tree_budget_transfer
#check @Orthemology.Tranche2.resetCost_guarded_bound
#print axioms Orthemology.Tranche2.resetCost_guarded_bound
#check @Orthemology.Tranche2.resetCost_guarded_root_bound
#print axioms Orthemology.Tranche2.resetCost_guarded_root_bound
#check @Orthemology.Tranche2.guarded_reset_hellinger_budget
#print axioms Orthemology.Tranche2.guarded_reset_hellinger_budget
#check @Orthemology.Tranche2.guarded_live_stopped_controller_budget
#print axioms Orthemology.Tranche2.guarded_live_stopped_controller_budget
#check @Orthemology.Tranche2.stoppedActions
#print axioms Orthemology.Tranche2.stoppedActions
#check @Orthemology.Tranche2.stoppedActions_sublist
#print axioms Orthemology.Tranche2.stoppedActions_sublist
#check @Orthemology.Tranche2.plannedBadCount
#print axioms Orthemology.Tranche2.plannedBadCount
#check @Orthemology.Tranche2.stopped_bad_count_le_planned
#print axioms Orthemology.Tranche2.stopped_bad_count_le_planned
#check @Orthemology.Tranche2.plannedBadCount_pos_iff
#print axioms Orthemology.Tranche2.plannedBadCount_pos_iff
#check @Orthemology.Tranche2.livePlannedCost
#print axioms Orthemology.Tranche2.livePlannedCost
#check @Orthemology.Tranche2.livePlannedCost_nonneg
#print axioms Orthemology.Tranche2.livePlannedCost_nonneg
#check @Orthemology.Tranche2.livePlannedCost_positive
#print axioms Orthemology.Tranche2.livePlannedCost_positive
#check @Orthemology.Tranche2.stopped_bad_count_le_live_charge
#print axioms Orthemology.Tranche2.stopped_bad_count_le_live_charge
#check @Orthemology.Tranche2.ResetState
#print axioms Orthemology.Tranche2.ResetState
#check @Orthemology.Tranche2.resetStateMeasurableSpace
#print axioms Orthemology.Tranche2.resetStateMeasurableSpace
#check @Orthemology.Tranche2.resetUpdate
#print axioms Orthemology.Tranche2.resetUpdate
#check @Orthemology.Tranche2.observationPMF
#print axioms Orthemology.Tranche2.observationPMF
#check @Orthemology.Tranche2.resetTransitionPMF
#print axioms Orthemology.Tranche2.resetTransitionPMF
#check @Orthemology.Tranche2.resetTransitionKernel
#print axioms Orthemology.Tranche2.resetTransitionKernel
#check @Orthemology.Tranche2.resetTransitionKernel_markov
#print axioms Orthemology.Tranche2.resetTransitionKernel_markov
#check @Orthemology.Tranche2.markovKernelSequence
#print axioms Orthemology.Tranche2.markovKernelSequence
#check @Orthemology.Tranche2.markovKernelSequence_markov
#print axioms Orthemology.Tranche2.markovKernelSequence_markov
#check @Orthemology.Tranche2.markovTrajectory
#print axioms Orthemology.Tranche2.markovTrajectory
#check @Orthemology.Tranche2.markovTrajectory_probability
#print axioms Orthemology.Tranche2.markovTrajectory_probability
#check @Orthemology.Tranche2.markovTrajectory_finite_law
#print axioms Orthemology.Tranche2.markovTrajectory_finite_law
#check @Orthemology.Tranche2.resetFutureCost
#print axioms Orthemology.Tranche2.resetFutureCost
#check @Orthemology.Tranche2.resetCost_eq_mass_future
#print axioms Orthemology.Tranche2.resetCost_eq_mass_future
#check @Orthemology.Tranche2.markovExpectedCharge
#print axioms Orthemology.Tranche2.markovExpectedCharge
#check @Orthemology.Tranche2.pathCharge
#print axioms Orthemology.Tranche2.pathCharge
#check @Orthemology.Tranche2.pathCharge_measurable
#print axioms Orthemology.Tranche2.pathCharge_measurable
#check @Orthemology.Tranche2.pathCharge_succ
#print axioms Orthemology.Tranche2.pathCharge_succ
#check @Orthemology.Tranche2.lmarginal_next_coordinate
#print axioms Orthemology.Tranche2.lmarginal_next_coordinate
#check @Orthemology.Tranche2.lmarginal_current_plus
#print axioms Orthemology.Tranche2.lmarginal_current_plus
#check @Orthemology.Tranche2.lmarginal_pathCharge
#print axioms Orthemology.Tranche2.lmarginal_pathCharge
#check @Orthemology.Tranche2.markovTrajectory_expected_charge
#print axioms Orthemology.Tranche2.markovTrajectory_expected_charge
#check @Orthemology.Tranche2.resetTransition_lintegral
#print axioms Orthemology.Tranche2.resetTransition_lintegral
#check @Orthemology.Tranche2.resetFutureCost_nonneg
#print axioms Orthemology.Tranche2.resetFutureCost_nonneg
#check @Orthemology.Tranche2.markovExpectedCharge_eq_resetFuture
#print axioms Orthemology.Tranche2.markovExpectedCharge_eq_resetFuture
#check @Orthemology.Tranche2.trajectory_expected_charge_eq_resetCost
#print axioms Orthemology.Tranche2.trajectory_expected_charge_eq_resetCost
#check @Orthemology.Tranche2.trajectory_total_charge_bound
#print axioms Orthemology.Tranche2.trajectory_total_charge_bound
#check @Orthemology.Tranche2.trajectory_nat_charge_eventually_zero
#print axioms Orthemology.Tranche2.trajectory_nat_charge_eventually_zero
#check @Orthemology.Tranche2.generated_live_controller_eventually_good
#print axioms Orthemology.Tranche2.generated_live_controller_eventually_good

#print Orthemology.Tranche2.resetUpdate
#print Orthemology.Tranche2.markovTrajectory
#print Orthemology.Tranche2.plannedBadCount
