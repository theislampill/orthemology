import PruningKernel
import EndComponents
import FiniteReachability
import ExecutablePruning
import MarkovSupportAdapter
import ControlTests
import AdapterTests
import CoBuchiSpecialisation
import SCCPruning
import SCCParity
import SCCControls
set_option pp.universes true
set_option pp.explicit true
#check @HiddenParity.Controls.exitKernel
#print axioms HiddenParity.Controls.exitKernel
#check @HiddenParity.Controls.candidate_zero_exit
#print axioms HiddenParity.Controls.candidate_zero_exit
#check @HiddenParity.Controls.rival_has_exit
#print axioms HiddenParity.Controls.rival_has_exit
#check @HiddenParity.Controls.exact_internal_support
#print axioms HiddenParity.Controls.exact_internal_support
#check @HiddenParity.Controls.normalized_adapter_target
#print axioms HiddenParity.Controls.normalized_adapter_target
#check @HiddenParity.Controls.normalized_adapter_rival_empty
#print axioms HiddenParity.Controls.normalized_adapter_rival_empty
#check @HiddenParity.coBuchiPriority
#print axioms HiddenParity.coBuchiPriority
#check @HiddenParity.coBuchi_even_minimum_iff
#print axioms HiddenParity.coBuchi_even_minimum_iff
#check @HiddenParity.coBuchi_valid_iff
#print axioms HiddenParity.coBuchi_valid_iff
#check @HiddenParity.coBuchi_odd_layer_iff
#print axioms HiddenParity.coBuchi_odd_layer_iff
#check @HiddenParity.coBuchi_badPair_iff
#print axioms HiddenParity.coBuchi_badPair_iff
#check @HiddenParity.Controls.One
#print axioms HiddenParity.Controls.One
#check @HiddenParity.Controls.Two
#print axioms HiddenParity.Controls.Two
#check @HiddenParity.Controls.Three
#print axioms HiddenParity.Controls.Three
#check @HiddenParity.Controls.Four
#print axioms HiddenParity.Controls.Four
#check @HiddenParity.Controls.half
#print axioms HiddenParity.Controls.half
#check @HiddenParity.Controls.half_eq
#print axioms HiddenParity.Controls.half_eq
#check @HiddenParity.Controls.sourceOne
#print axioms HiddenParity.Controls.sourceOne
#check @HiddenParity.Controls.succOne
#print axioms HiddenParity.Controls.succOne
#check @HiddenParity.Controls.sameRow
#print axioms HiddenParity.Controls.sameRow
#check @HiddenParity.Controls.cascadePriority
#print axioms HiddenParity.Controls.cascadePriority
#check @HiddenParity.Controls.cascade_first_round
#print axioms HiddenParity.Controls.cascade_first_round
#check @HiddenParity.Controls.cascade_second_round
#print axioms HiddenParity.Controls.cascade_second_round
#check @HiddenParity.Controls.cascade_output
#print axioms HiddenParity.Controls.cascade_output
#check @HiddenParity.Controls.zeroSource
#print axioms HiddenParity.Controls.zeroSource
#check @HiddenParity.Controls.zeroSucc
#print axioms HiddenParity.Controls.zeroSucc
#check @HiddenParity.Controls.revealRow
#print axioms HiddenParity.Controls.revealRow
#check @HiddenParity.Controls.revealPriority
#print axioms HiddenParity.Controls.revealPriority
#check @HiddenParity.Controls.rival_initially_unmatched
#print axioms HiddenParity.Controls.rival_initially_unmatched
#check @HiddenParity.Controls.rival_newly_matches
#print axioms HiddenParity.Controls.rival_newly_matches
#check @HiddenParity.Controls.rival_first_round
#print axioms HiddenParity.Controls.rival_first_round
#check @HiddenParity.Controls.rival_second_round
#print axioms HiddenParity.Controls.rival_second_round
#check @HiddenParity.Controls.rival_output
#print axioms HiddenParity.Controls.rival_output
#check @HiddenParity.Controls.cycleSource
#print axioms HiddenParity.Controls.cycleSource
#check @HiddenParity.Controls.cycleSucc
#print axioms HiddenParity.Controls.cycleSucc
#check @HiddenParity.Controls.cycleRow
#print axioms HiddenParity.Controls.cycleRow
#check @HiddenParity.Controls.cycle23
#print axioms HiddenParity.Controls.cycle23
#check @HiddenParity.Controls.cycle21
#print axioms HiddenParity.Controls.cycle21
#check @HiddenParity.Controls.cycle01
#print axioms HiddenParity.Controls.cycle01
#check @HiddenParity.Controls.higher_odd_cycle_retained
#print axioms HiddenParity.Controls.higher_odd_cycle_retained
#check @HiddenParity.Controls.cobuchi_21_cycle_rejected
#print axioms HiddenParity.Controls.cobuchi_21_cycle_rejected
#check @HiddenParity.Controls.wrong_01_encoding_distinguished
#print axioms HiddenParity.Controls.wrong_01_encoding_distinguished
#check @HiddenParity.Controls.singleSource
#print axioms HiddenParity.Controls.singleSource
#check @HiddenParity.Controls.singleSucc
#print axioms HiddenParity.Controls.singleSucc
#check @HiddenParity.Controls.exitRow
#print axioms HiddenParity.Controls.exitRow
#check @HiddenParity.Controls.oppositePriority
#print axioms HiddenParity.Controls.oppositePriority
#check @HiddenParity.Controls.sameSingleRow
#print axioms HiddenParity.Controls.sameSingleRow
#check @HiddenParity.Controls.full_row_difference_retains_target
#print axioms HiddenParity.Controls.full_row_difference_retains_target
#check @HiddenParity.Controls.equal_row_odd_rival_rejects
#print axioms HiddenParity.Controls.equal_row_odd_rival_rejects
#check @HiddenParity.Controls.splitSource
#print axioms HiddenParity.Controls.splitSource
#check @HiddenParity.Controls.splitSucc
#print axioms HiddenParity.Controls.splitSucc
#check @HiddenParity.Controls.splitRow
#print axioms HiddenParity.Controls.splitRow
#check @HiddenParity.Controls.splitPriority
#print axioms HiddenParity.Controls.splitPriority
#check @HiddenParity.Controls.split_first_round
#print axioms HiddenParity.Controls.split_first_round
#check @HiddenParity.Controls.split_recomputed_components
#print axioms HiddenParity.Controls.split_recomputed_components
#check @HiddenParity.Controls.split_output
#print axioms HiddenParity.Controls.split_output
#check @HiddenParity.Controls.empty_input
#print axioms HiddenParity.Controls.empty_input
#check @HiddenParity.Controls.emptySucc
#print axioms HiddenParity.Controls.emptySucc
#check @HiddenParity.Controls.openSucc
#print axioms HiddenParity.Controls.openSucc
#check @HiddenParity.Controls.empty_successors_rejected
#print axioms HiddenParity.Controls.empty_successors_rejected
#check @HiddenParity.Controls.no_closed_component_rejected
#print axioms HiddenParity.Controls.no_closed_component_rejected
#check @HiddenParity.usedStates
#print axioms HiddenParity.usedStates
#check @HiddenParity.Edge
#print axioms HiddenParity.Edge
#check @HiddenParity.Reach
#print axioms HiddenParity.Reach
#check @HiddenParity.IsEndComponent
#print axioms HiddenParity.IsEndComponent
#check @HiddenParity.usedStates_mono
#print axioms HiddenParity.usedStates_mono
#check @HiddenParity.edge_mono
#print axioms HiddenParity.edge_mono
#check @HiddenParity.reach_mono
#print axioms HiddenParity.reach_mono
#check @HiddenParity.endComponent_union_of_common_state
#print axioms HiddenParity.endComponent_union_of_common_state
#check @HiddenParity.endComponentFamily
#print axioms HiddenParity.endComponentFamily
#check @HiddenParity.endComponent_output_iff
#print axioms HiddenParity.endComponent_output_iff
#check @HiddenParity.IsTargetState
#print axioms HiddenParity.IsTargetState
#check @HiddenParity.targetStates
#print axioms HiddenParity.targetStates
#check @HiddenParity.targetStates_exact
#print axioms HiddenParity.targetStates_exact
#check @HiddenParity.output_components_state_disjoint
#print axioms HiddenParity.output_components_state_disjoint
#check @HiddenParity.edgeDecidable
#print axioms HiddenParity.edgeDecidable
#check @HiddenParity.CheckedEndComponent
#print axioms HiddenParity.CheckedEndComponent
#check @HiddenParity.checkedEndComponentDecidable
#print axioms HiddenParity.checkedEndComponentDecidable
#check @HiddenParity.checkedEndComponent_iff
#print axioms HiddenParity.checkedEndComponent_iff
#check @HiddenParity.endComponentDecidable
#print axioms HiddenParity.endComponentDecidable
#check @HiddenParity.executableMECs
#print axioms HiddenParity.executableMECs
#check @HiddenParity.executableMECs_eq
#print axioms HiddenParity.executableMECs_eq
#check @HiddenParity.matchDecidable
#print axioms HiddenParity.matchDecidable
#check @HiddenParity.minimumDecidable
#print axioms HiddenParity.minimumDecidable
#check @HiddenParity.ExecutableBadPair
#print axioms HiddenParity.ExecutableBadPair
#check @HiddenParity.executableBadPairDecidable
#print axioms HiddenParity.executableBadPairDecidable
#check @HiddenParity.executableStep
#print axioms HiddenParity.executableStep
#check @HiddenParity.executableStep_eq
#print axioms HiddenParity.executableStep_eq
#check @HiddenParity.executableIterate
#print axioms HiddenParity.executableIterate
#check @HiddenParity.executableIterate_eq
#print axioms HiddenParity.executableIterate_eq
#check @HiddenParity.executableOutput
#print axioms HiddenParity.executableOutput
#check @HiddenParity.executable_output_eq
#print axioms HiddenParity.executable_output_eq
#check @HiddenParity.executable_output_iff_maximal_valid
#print axioms HiddenParity.executable_output_iff_maximal_valid
#check @HiddenParity.executableTargetStates
#print axioms HiddenParity.executableTargetStates
#check @HiddenParity.executable_targetStates_exact
#print axioms HiddenParity.executable_targetStates_exact
#check @HiddenParity.FiniteReachability.grow
#print axioms HiddenParity.FiniteReachability.grow
#check @HiddenParity.FiniteReachability.mem_grow
#print axioms HiddenParity.FiniteReachability.mem_grow
#check @HiddenParity.FiniteReachability.subset_grow
#print axioms HiddenParity.FiniteReachability.subset_grow
#check @HiddenParity.FiniteReachability.saturate
#print axioms HiddenParity.FiniteReachability.saturate
#check @HiddenParity.FiniteReachability.subset_saturate
#print axioms HiddenParity.FiniteReachability.subset_saturate
#check @HiddenParity.FiniteReachability.saturate_eq_of_stable
#print axioms HiddenParity.FiniteReachability.saturate_eq_of_stable
#check @HiddenParity.FiniteReachability.saturate_stable
#print axioms HiddenParity.FiniteReachability.saturate_stable
#check @HiddenParity.FiniteReachability.saturate_sound
#print axioms HiddenParity.FiniteReachability.saturate_sound
#check @HiddenParity.FiniteReachability.reachable
#print axioms HiddenParity.FiniteReachability.reachable
#check @HiddenParity.FiniteReachability.reachable_iff
#print axioms HiddenParity.FiniteReachability.reachable_iff
#check @HiddenParity.RationalKernel
#print axioms HiddenParity.RationalKernel
#check @HiddenParity.internalSuccessors
#print axioms HiddenParity.internalSuccessors
#check @HiddenParity.mem_internalSuccessors
#print axioms HiddenParity.mem_internalSuccessors
#check @HiddenParity.NoExit
#print axioms HiddenParity.NoExit
#check @HiddenParity.noExitDecidable
#print axioms HiddenParity.noExitDecidable
#check @HiddenParity.zeroExitPairs
#print axioms HiddenParity.zeroExitPairs
#check @HiddenParity.mem_zeroExitPairs
#print axioms HiddenParity.mem_zeroExitPairs
#check @HiddenParity.noExit_iff_internal_mass_one
#print axioms HiddenParity.noExit_iff_internal_mass_one
#check @HiddenParity.noExit_internal_nonempty
#print axioms HiddenParity.noExit_internal_nonempty
#check @HiddenParity.matching_noExit
#print axioms HiddenParity.matching_noExit
#check @HiddenParity.noExit_internal_eq_candidate_support
#print axioms HiddenParity.noExit_internal_eq_candidate_support
#check @HiddenParity.MarkovQualifying
#print axioms HiddenParity.MarkovQualifying
#check @HiddenParity.markovQualifying_iff
#print axioms HiddenParity.markovQualifying_iff
#check @HiddenParity.markovTargetStates
#print axioms HiddenParity.markovTargetStates
#check @HiddenParity.markovTargetStates_exact
#print axioms HiddenParity.markovTargetStates_exact
#check @HiddenParity.ComponentFamily
#print axioms HiddenParity.ComponentFamily
#check @HiddenParity.Match
#print axioms HiddenParity.Match
#check @HiddenParity.IsMinimum
#print axioms HiddenParity.IsMinimum
#check @HiddenParity.Valid
#print axioms HiddenParity.Valid
#check @HiddenParity.match_mono
#print axioms HiddenParity.match_mono
#check @HiddenParity.minimum_unique
#print axioms HiddenParity.minimum_unique
#check @HiddenParity.exists_minimum
#print axioms HiddenParity.exists_minimum
#check @HiddenParity.valid_avoids_odd_minimum
#print axioms HiddenParity.valid_avoids_odd_minimum
#check @HiddenParity.MaximalComponent
#print axioms HiddenParity.MaximalComponent
#check @HiddenParity.maximalComponents
#print axioms HiddenParity.maximalComponents
#check @HiddenParity.mem_maximalComponents
#print axioms HiddenParity.mem_maximalComponents
#check @HiddenParity.component_has_maximal
#print axioms HiddenParity.component_has_maximal
#check @HiddenParity.component_subset_of_intersects_maximal
#print axioms HiddenParity.component_subset_of_intersects_maximal
#check @HiddenParity.BadPair
#print axioms HiddenParity.BadPair
#check @HiddenParity.step
#print axioms HiddenParity.step
#check @HiddenParity.mem_step
#print axioms HiddenParity.mem_step
#check @HiddenParity.step_subset
#print axioms HiddenParity.step_subset
#check @HiddenParity.step_preserves
#print axioms HiddenParity.step_preserves
#check @HiddenParity.stable_maximal_valid
#print axioms HiddenParity.stable_maximal_valid
#check @HiddenParity.iterate
#print axioms HiddenParity.iterate
#check @HiddenParity.iterate_subset
#print axioms HiddenParity.iterate_subset
#check @HiddenParity.iterate_preserves
#print axioms HiddenParity.iterate_preserves
#check @HiddenParity.iterate_eq_of_stable
#print axioms HiddenParity.iterate_eq_of_stable
#check @HiddenParity.iterate_stable
#print axioms HiddenParity.iterate_stable
#check @HiddenParity.output
#print axioms HiddenParity.output
#check @HiddenParity.MaximalValid
#print axioms HiddenParity.MaximalValid
#check @HiddenParity.output_iff_maximal_valid
#print axioms HiddenParity.output_iff_maximal_valid
#check @HiddenParity.valid_covered_by_output
#print axioms HiddenParity.valid_covered_by_output
#check @HiddenParity.SCCControls.deadSource
#print axioms HiddenParity.SCCControls.deadSource
#check @HiddenParity.SCCControls.deadSucc
#print axioms HiddenParity.SCCControls.deadSucc
#check @HiddenParity.SCCControls.first_dead_cleanup
#print axioms HiddenParity.SCCControls.first_dead_cleanup
#check @HiddenParity.SCCControls.second_dead_cleanup
#print axioms HiddenParity.SCCControls.second_dead_cleanup
#check @HiddenParity.SCCControls.dead_source_cascade_rejected
#print axioms HiddenParity.SCCControls.dead_source_cascade_rejected
#check @HiddenParity.SCCControls.reverseSource
#print axioms HiddenParity.SCCControls.reverseSource
#check @HiddenParity.SCCControls.reverseSucc
#print axioms HiddenParity.SCCControls.reverseSucc
#check @HiddenParity.SCCControls.first_reverse_cleanup
#print axioms HiddenParity.SCCControls.first_reverse_cleanup
#check @HiddenParity.SCCControls.second_reverse_cleanup
#print axioms HiddenParity.SCCControls.second_reverse_cleanup
#check @HiddenParity.SCCControls.stable_scc_split
#print axioms HiddenParity.SCCControls.stable_scc_split
#check @HiddenParity.SCCControls.empty_successor_rejected
#print axioms HiddenParity.SCCControls.empty_successor_rejected
#check @HiddenParity.SCCControls.missing_source_rejected
#print axioms HiddenParity.SCCControls.missing_source_rejected
#check @HiddenParity.SCCControls.empty_input
#print axioms HiddenParity.SCCControls.empty_input
#check @HiddenParity.SCCControls.same_state_pairs_form_one_component
#print axioms HiddenParity.SCCControls.same_state_pairs_form_one_component
#check @HiddenParity.SCCControls.closed_cycle_retained
#print axioms HiddenParity.SCCControls.closed_cycle_retained
#check @HiddenParity.SCCControls.parity_cascade
#print axioms HiddenParity.SCCControls.parity_cascade
#check @HiddenParity.SCCControls.newly_matching_rival
#print axioms HiddenParity.SCCControls.newly_matching_rival
#check @HiddenParity.SCCControls.higher_odd_cycle_retained
#print axioms HiddenParity.SCCControls.higher_odd_cycle_retained
#check @HiddenParity.SCCControls.cobuchi_bad_cycle_rejected
#print axioms HiddenParity.SCCControls.cobuchi_bad_cycle_rejected
#check @HiddenParity.SCCControls.graph_splits_after_parity_deletion
#print axioms HiddenParity.SCCControls.graph_splits_after_parity_deletion
#check @HiddenParity.SCCControls.full_row_difference_retains
#print axioms HiddenParity.SCCControls.full_row_difference_retains
#check @HiddenParity.SCCControls.matching_odd_rival_rejects
#print axioms HiddenParity.SCCControls.matching_odd_rival_rejects
#check @HiddenParity.SCCControls.normalized_candidate_target
#print axioms HiddenParity.SCCControls.normalized_candidate_target
#check @HiddenParity.SCCControls.normalized_rival_exit
#print axioms HiddenParity.SCCControls.normalized_rival_exit
#check @HiddenParity.SCCPruning.BadWithin
#print axioms HiddenParity.SCCPruning.BadWithin
#check @HiddenParity.SCCPruning.badWithinDecidable
#print axioms HiddenParity.SCCPruning.badWithinDecidable
#check @HiddenParity.SCCPruning.parityStep
#print axioms HiddenParity.SCCPruning.parityStep
#check @HiddenParity.SCCPruning.parityStep_eq
#print axioms HiddenParity.SCCPruning.parityStep_eq
#check @HiddenParity.SCCPruning.parityIterate
#print axioms HiddenParity.SCCPruning.parityIterate
#check @HiddenParity.SCCPruning.parityIterate_eq
#print axioms HiddenParity.SCCPruning.parityIterate_eq
#check @HiddenParity.SCCPruning.parityOutput
#print axioms HiddenParity.SCCPruning.parityOutput
#check @HiddenParity.SCCPruning.parityOutput_eq
#print axioms HiddenParity.SCCPruning.parityOutput_eq
#check @HiddenParity.SCCPruning.parityOutput_exact
#print axioms HiddenParity.SCCPruning.parityOutput_exact
#check @HiddenParity.SCCPruning.targetStates
#print axioms HiddenParity.SCCPruning.targetStates
#check @HiddenParity.SCCPruning.targetStates_eq
#print axioms HiddenParity.SCCPruning.targetStates_eq
#check @HiddenParity.SCCPruning.targetStates_exact
#print axioms HiddenParity.SCCPruning.targetStates_exact
#check @HiddenParity.SCCPruning.markovTarget
#print axioms HiddenParity.SCCPruning.markovTarget
#check @HiddenParity.SCCPruning.markovTarget_eq
#print axioms HiddenParity.SCCPruning.markovTarget_eq
#check @HiddenParity.SCCPruning.markovTarget_exact
#print axioms HiddenParity.SCCPruning.markovTarget_exact
#check @HiddenParity.SCCPruning.Keep
#print axioms HiddenParity.SCCPruning.Keep
#check @HiddenParity.SCCPruning.keepDecidable
#print axioms HiddenParity.SCCPruning.keepDecidable
#check @HiddenParity.SCCPruning.step
#print axioms HiddenParity.SCCPruning.step
#check @HiddenParity.SCCPruning.step_subset
#print axioms HiddenParity.SCCPruning.step_subset
#check @HiddenParity.SCCPruning.step_preserves
#print axioms HiddenParity.SCCPruning.step_preserves
#check @HiddenParity.SCCPruning.iterate
#print axioms HiddenParity.SCCPruning.iterate
#check @HiddenParity.SCCPruning.iterate_subset
#print axioms HiddenParity.SCCPruning.iterate_subset
#check @HiddenParity.SCCPruning.iterate_preserves
#print axioms HiddenParity.SCCPruning.iterate_preserves
#check @HiddenParity.SCCPruning.iterate_eq_of_stable
#print axioms HiddenParity.SCCPruning.iterate_eq_of_stable
#check @HiddenParity.SCCPruning.iterate_stable
#print axioms HiddenParity.SCCPruning.iterate_stable
#check @HiddenParity.SCCPruning.cluster
#print axioms HiddenParity.SCCPruning.cluster
#check @HiddenParity.SCCPruning.mem_cluster
#print axioms HiddenParity.SCCPruning.mem_cluster
#check @HiddenParity.SCCPruning.cluster_subset
#print axioms HiddenParity.SCCPruning.cluster_subset
#check @HiddenParity.SCCPruning.anchor_mem_cluster
#print axioms HiddenParity.SCCPruning.anchor_mem_cluster
#check @HiddenParity.SCCPruning.reach_restrict
#print axioms HiddenParity.SCCPruning.reach_restrict
#check @HiddenParity.SCCPruning.component_subset_cluster
#print axioms HiddenParity.SCCPruning.component_subset_cluster
#check @HiddenParity.SCCPruning.stable_cluster_component
#print axioms HiddenParity.SCCPruning.stable_cluster_component
#check @HiddenParity.SCCPruning.stable_cluster_maximal
#print axioms HiddenParity.SCCPruning.stable_cluster_maximal
#check @HiddenParity.SCCPruning.mecs
#print axioms HiddenParity.SCCPruning.mecs
#check @HiddenParity.SCCPruning.mem_mecs_iff
#print axioms HiddenParity.SCCPruning.mem_mecs_iff
#check @HiddenParity.SCCPruning.mecs_card_le
#print axioms HiddenParity.SCCPruning.mecs_card_le
#check @HiddenParity.SCCPruning.mecs_eq_executable
#print axioms HiddenParity.SCCPruning.mecs_eq_executable
