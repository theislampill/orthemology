import PruningKernel
import EndComponents
import FiniteReachability
import ExecutablePruning
import GenericFiniteQueryLocality
import GenericFiniteQueryMeasure
import PolicyRowEvaluator
import PolicyTranscriptFiber
import FeedbackRequests
import ProductObservationLaw
import IndependentProductFamilies
import GenericQueryReference
import PolicyRowLaw
import FeedbackFiberProbability
import HistoryPathConsistency
import KilledQueryLaw
import PolicyCylinderProbability
import PolicyObservedLaw
import PolicyTraceBinding
import KilledAdaptiveHistory
import RecurrentSupport
import KilledRecurrentTransfer
import MarkovSupportAdapter
import MarkovKilledBridge
import KilledLawControls
import ResidualSeedPosterior
import PosteriorFeedbackProduct
import MarkovSeedPosterior
set_option pp.universes true
set_option pp.explicit true
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
#check @Orthemology.Tranche2.PolicyEmbedding.FlatStack
#print axioms Orthemology.Tranche2.PolicyEmbedding.FlatStack
#check @Orthemology.Tranche2.PolicyEmbedding.RowOracle
#print axioms Orthemology.Tranche2.PolicyEmbedding.RowOracle
#check @Orthemology.Tranche2.PolicyEmbedding.actionMeasure
#print axioms Orthemology.Tranche2.PolicyEmbedding.actionMeasure
#check @Orthemology.Tranche2.PolicyEmbedding.actionMeasure_probability
#print axioms Orthemology.Tranche2.PolicyEmbedding.actionMeasure_probability
#check @Orthemology.Tranche2.PolicyEmbedding.actionMeasure_singleton
#print axioms Orthemology.Tranche2.PolicyEmbedding.actionMeasure_singleton
#check @Orthemology.Tranche2.PolicyEmbedding.stackMeasure
#print axioms Orthemology.Tranche2.PolicyEmbedding.stackMeasure
#check @Orthemology.Tranche2.PolicyEmbedding.stackMeasure_probability
#print axioms Orthemology.Tranche2.PolicyEmbedding.stackMeasure_probability
#check @Orthemology.Tranche2.PolicyEmbedding.feedbackLaw
#print axioms Orthemology.Tranche2.PolicyEmbedding.feedbackLaw
#check @Orthemology.Tranche2.PolicyEmbedding.feedbackLaw_probability
#print axioms Orthemology.Tranche2.PolicyEmbedding.feedbackLaw_probability
#check @Orthemology.Tranche2.PolicyEmbedding.sourceFamily
#print axioms Orthemology.Tranche2.PolicyEmbedding.sourceFamily
#check @Orthemology.Tranche2.PolicyEmbedding.sourceRead
#print axioms Orthemology.Tranche2.PolicyEmbedding.sourceRead
#check @Orthemology.Tranche2.PolicyEmbedding.sourceRead_measurable
#print axioms Orthemology.Tranche2.PolicyEmbedding.sourceRead_measurable
#check @Orthemology.Tranche2.PolicyEmbedding.transcriptSample
#print axioms Orthemology.Tranche2.PolicyEmbedding.transcriptSample
#check @Orthemology.Tranche2.PolicyEmbedding.transcriptSample_eq_source
#print axioms Orthemology.Tranche2.PolicyEmbedding.transcriptSample_eq_source
#check @Orthemology.Tranche2.PolicyEmbedding.transcriptSamples_independent
#print axioms Orthemology.Tranche2.PolicyEmbedding.transcriptSamples_independent
#check @Orthemology.Tranche2.PolicyEmbedding.feedbackLaw_left_marginal
#print axioms Orthemology.Tranche2.PolicyEmbedding.feedbackLaw_left_marginal
#check @Orthemology.Tranche2.PolicyEmbedding.feedbackLaw_right_marginal
#print axioms Orthemology.Tranche2.PolicyEmbedding.feedbackLaw_right_marginal
#check @Orthemology.Tranche2.PolicyEmbedding.transcriptSample_marginal
#print axioms Orthemology.Tranche2.PolicyEmbedding.transcriptSample_marginal
#check @Orthemology.Tranche2.PolicyEmbedding.feedbackCompatible_probability
#print axioms Orthemology.Tranche2.PolicyEmbedding.feedbackCompatible_probability
#check @Orthemology.Tranche2.PolicyEmbedding.FeedbackKey
#print axioms Orthemology.Tranche2.PolicyEmbedding.FeedbackKey
#check @Orthemology.Tranche2.PolicyEmbedding.feedbackKey
#print axioms Orthemology.Tranche2.PolicyEmbedding.feedbackKey
#check @Orthemology.Tranche2.PolicyEmbedding.feedbackKeys
#print axioms Orthemology.Tranche2.PolicyEmbedding.feedbackKeys
#check @Orthemology.Tranche2.PolicyEmbedding.feedbackKeys_length
#print axioms Orthemology.Tranche2.PolicyEmbedding.feedbackKeys_length
#check @Orthemology.Tranche2.PolicyEmbedding.actionCount_cons
#print axioms Orthemology.Tranche2.PolicyEmbedding.actionCount_cons
#check @Orthemology.Tranche2.PolicyEmbedding.outsideCount_cons
#print axioms Orthemology.Tranche2.PolicyEmbedding.outsideCount_cons
#check @Orthemology.Tranche2.PolicyEmbedding.inside_key_bound
#print axioms Orthemology.Tranche2.PolicyEmbedding.inside_key_bound
#check @Orthemology.Tranche2.PolicyEmbedding.outside_key_bound
#print axioms Orthemology.Tranche2.PolicyEmbedding.outside_key_bound
#check @Orthemology.Tranche2.PolicyEmbedding.feedbackKeys_nodup
#print axioms Orthemology.Tranche2.PolicyEmbedding.feedbackKeys_nodup
#check @Orthemology.Tranche2.PolicyEmbedding.requestKey
#print axioms Orthemology.Tranche2.PolicyEmbedding.requestKey
#check @Orthemology.Tranche2.PolicyEmbedding.requestKey_zero
#print axioms Orthemology.Tranche2.PolicyEmbedding.requestKey_zero
#check @Orthemology.Tranche2.PolicyEmbedding.requestKey_succ
#print axioms Orthemology.Tranche2.PolicyEmbedding.requestKey_succ
#check @Orthemology.Tranche2.PolicyEmbedding.requestKey_injective
#print axioms Orthemology.Tranche2.PolicyEmbedding.requestKey_injective
#check @Orthemology.Tranche2.PolicyEmbedding.readFeedback
#print axioms Orthemology.Tranche2.PolicyEmbedding.readFeedback
#check @Orthemology.Tranche2.PolicyEmbedding.readFeedback_key
#print axioms Orthemology.Tranche2.PolicyEmbedding.readFeedback_key
#check @Orthemology.Tranche2.PolicyEmbedding.feedbackCompatible_iff_requests
#print axioms Orthemology.Tranche2.PolicyEmbedding.feedbackCompatible_iff_requests
#check @Orthemology.Tranche2.PolicyEmbedding.requestKey_branch
#print axioms Orthemology.Tranche2.PolicyEmbedding.requestKey_branch
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
#check @Orthemology.Tranche2.FiniteAlphabetQuery.advance
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.advance
#check @Orthemology.Tranche2.FiniteAlphabetQuery.run
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.run
#check @Orthemology.Tranche2.FiniteAlphabetQuery.Bounded
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.Bounded
#check @Orthemology.Tranche2.FiniteAlphabetQuery.bounded_prefix_locality
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.bounded_prefix_locality
#check @Orthemology.Tranche2.FiniteAlphabetQuery.bounded_prefix_equivalence
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.bounded_prefix_equivalence
#check @Orthemology.Tranche2.FiniteAlphabetQuery.prefixOracle
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.prefixOracle
#check @Orthemology.Tranche2.FiniteAlphabetQuery.prefixOracle_agrees
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.prefixOracle_agrees
#check @Orthemology.Tranche2.FiniteAlphabetQuery.bounded_trace_factorisation
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.bounded_trace_factorisation
#check @Orthemology.Tranche2.FiniteAlphabetQuery.counter_monotone
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.counter_monotone
#check @Orthemology.Tranche2.FiniteAlphabetQuery.bounded_iff_eventually_no_query
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.bounded_iff_eventually_no_query
#check @Orthemology.Tranche2.FiniteAlphabetQuery.Oracle
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.Oracle
#check @Orthemology.Tranche2.FiniteAlphabetQuery.Trace
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.Trace
#check @Orthemology.Tranche2.FiniteAlphabetQuery.measurable_advance_joint
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.measurable_advance_joint
#check @Orthemology.Tranche2.FiniteAlphabetQuery.measurable_run
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.measurable_run
#check @Orthemology.Tranche2.FiniteAlphabetQuery.measurable_trajectory
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.measurable_trajectory
#check @Orthemology.Tranche2.FiniteAlphabetQuery.boundedTrace
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.boundedTrace
#check @Orthemology.Tranche2.FiniteAlphabetQuery.measurable_boundedTrace
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.measurable_boundedTrace
#check @Orthemology.Tranche2.FiniteAlphabetQuery.measurable_prefixOracle
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.measurable_prefixOracle
#check @Orthemology.Tranche2.FiniteAlphabetQuery.prefixInput
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.prefixInput
#check @Orthemology.Tranche2.FiniteAlphabetQuery.measurable_prefixInput
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.measurable_prefixInput
#check @Orthemology.Tranche2.FiniteAlphabetQuery.finiteTrajectory
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.finiteTrajectory
#check @Orthemology.Tranche2.FiniteAlphabetQuery.measurable_finiteTrajectory
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.measurable_finiteTrajectory
#check @Orthemology.Tranche2.FiniteAlphabetQuery.bounded_event_prefix
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.bounded_event_prefix
#check @Orthemology.Tranche2.FiniteAlphabetQuery.trajectory_prefix_on_bounded
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.trajectory_prefix_on_bounded
#check @Orthemology.Tranche2.FiniteAlphabetQuery.restricted_observable_factorisation
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.restricted_observable_factorisation
#check @Orthemology.Tranche2.FiniteAlphabetQuery.absolutelyContinuous_of_singletons
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.absolutelyContinuous_of_singletons
#check @Orthemology.Tranche2.FiniteAlphabetQuery.prefixSymbols
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.prefixSymbols
#check @Orthemology.Tranche2.FiniteAlphabetQuery.measurable_prefixSymbols
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.measurable_prefixSymbols
#check @Orthemology.Tranche2.FiniteAlphabetQuery.traceLaw
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.traceLaw
#check @Orthemology.Tranche2.FiniteAlphabetQuery.input_prefix_map
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.input_prefix_map
#check @Orthemology.Tranche2.FiniteAlphabetQuery.bounded_trace_law_factorisation
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.bounded_trace_law_factorisation
#check @Orthemology.Tranche2.FiniteAlphabetQuery.bounded_trace_domination
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.bounded_trace_domination
#check @Orthemology.Tranche2.FiniteAlphabetQuery.restrict_iUnion_domination
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.restrict_iUnion_domination
#check @Orthemology.Tranche2.FiniteAlphabetQuery.finiteQueryTrace
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.finiteQueryTrace
#check @Orthemology.Tranche2.FiniteAlphabetQuery.measurable_finiteQueryTrace
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.measurable_finiteQueryTrace
#check @Orthemology.Tranche2.FiniteAlphabetQuery.finite_query_trace_domination
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.finite_query_trace_domination
#check @Orthemology.Tranche2.FiniteAlphabetQuery.iidOracle
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.iidOracle
#check @Orthemology.Tranche2.FiniteAlphabetQuery.iidOracle_probability
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.iidOracle_probability
#check @Orthemology.Tranche2.FiniteAlphabetQuery.prefixSymbols_singleton_preimage
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.prefixSymbols_singleton_preimage
#check @Orthemology.Tranche2.FiniteAlphabetQuery.iidOracle_prefix_nonzero
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.iidOracle_prefix_nonzero
#check @Orthemology.Tranche2.FiniteAlphabetQuery.finite_query_domination_by_iid_rival
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.finite_query_domination_by_iid_rival
#check @Orthemology.Tranche2.FiniteAlphabetQuery.positive_finite_query_event_transfers
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.positive_finite_query_event_transfers
#check @Orthemology.Tranche2.PolicyEmbedding.observedHistory_drop
#print axioms Orthemology.Tranche2.PolicyEmbedding.observedHistory_drop
#check @Orthemology.Tranche2.PolicyEmbedding.reconstructPrefix
#print axioms Orthemology.Tranche2.PolicyEmbedding.reconstructPrefix
#check @Orthemology.Tranche2.PolicyEmbedding.observedHistory_prefix_from_last
#print axioms Orthemology.Tranche2.PolicyEmbedding.observedHistory_prefix_from_last
#check @Orthemology.Tranche2.PolicyEmbedding.measure_eq_of_prefix_maps
#print axioms Orthemology.Tranche2.PolicyEmbedding.measure_eq_of_prefix_maps
#check @Orthemology.Tranche2.PolicyEmbedding.FamilyValue
#print axioms Orthemology.Tranche2.PolicyEmbedding.FamilyValue
#check @Orthemology.Tranche2.PolicyEmbedding.familyValueMeasurable
#print axioms Orthemology.Tranche2.PolicyEmbedding.familyValueMeasurable
#check @Orthemology.Tranche2.PolicyEmbedding.productFamily
#print axioms Orthemology.Tranche2.PolicyEmbedding.productFamily
#check @Orthemology.Tranche2.PolicyEmbedding.independent_product_families
#print axioms Orthemology.Tranche2.PolicyEmbedding.independent_product_families
#check @HiddenParity.Stochastic.AlivePrefix
#print axioms HiddenParity.Stochastic.AlivePrefix
#check @HiddenParity.Stochastic.alivePrefixDecidable
#print axioms HiddenParity.Stochastic.alivePrefixDecidable
#check @HiddenParity.Stochastic.killedHistory
#print axioms HiddenParity.Stochastic.killedHistory
#check @HiddenParity.Stochastic.measurable_alivePrefix
#print axioms HiddenParity.Stochastic.measurable_alivePrefix
#check @HiddenParity.Stochastic.killedHistory_measurable
#print axioms HiddenParity.Stochastic.killedHistory_measurable
#check @HiddenParity.Stochastic.killedReadout_history_agreement
#print axioms HiddenParity.Stochastic.killedReadout_history_agreement
#check @HiddenParity.Stochastic.traceLaw_killed_history_readout
#print axioms HiddenParity.Stochastic.traceLaw_killed_history_readout
#check @HiddenParity.Stochastic.canonical_killed_historyLaw_eq
#print axioms HiddenParity.Stochastic.canonical_killed_historyLaw_eq
#check @HiddenParity.Stochastic.Controls.A
#print axioms HiddenParity.Stochastic.Controls.A
#check @HiddenParity.Stochastic.Controls.Y
#print axioms HiddenParity.Stochastic.Controls.Y
#check @HiddenParity.Stochastic.Controls.pathP
#print axioms HiddenParity.Stochastic.Controls.pathP
#check @HiddenParity.Stochastic.Controls.pathQ
#print axioms HiddenParity.Stochastic.Controls.pathQ
#check @HiddenParity.Stochastic.Controls.outside_receipt_differs
#print axioms HiddenParity.Stochastic.Controls.outside_receipt_differs
#check @HiddenParity.Stochastic.Controls.killed_outside_receipt_equal
#print axioms HiddenParity.Stochastic.Controls.killed_outside_receipt_equal
#check @HiddenParity.Stochastic.Controls.active_prefix_retained
#print axioms HiddenParity.Stochastic.Controls.active_prefix_retained
#check @HiddenParity.Stochastic.Controls.killed_flag_visible
#print axioms HiddenParity.Stochastic.Controls.killed_flag_visible
#check @HiddenParity.Stochastic.Controls.validReceiptDifference
#print axioms HiddenParity.Stochastic.Controls.validReceiptDifference
#check @HiddenParity.Stochastic.Controls.retained_receipt_not_erased
#print axioms HiddenParity.Stochastic.Controls.retained_receipt_not_erased
#check @HiddenParity.Stochastic.Controls.action_history_preserved
#print axioms HiddenParity.Stochastic.Controls.action_history_preserved
#check @HiddenParity.Stochastic.Controls.queryEverywhere
#print axioms HiddenParity.Stochastic.Controls.queryEverywhere
#check @HiddenParity.Stochastic.Controls.takeReceipt
#print axioms HiddenParity.Stochastic.Controls.takeReceipt
#check @HiddenParity.Stochastic.Controls.queried_unstopped_states_differ
#print axioms HiddenParity.Stochastic.Controls.queried_unstopped_states_differ
#check @HiddenParity.Stochastic.Controls.queried_stopped_readout_equal
#print axioms HiddenParity.Stochastic.Controls.queried_stopped_readout_equal
#check @HiddenParity.Stochastic.zero_query_run_agreement
#print axioms HiddenParity.Stochastic.zero_query_run_agreement
#check @HiddenParity.Stochastic.run_counter_zero_iff
#print axioms HiddenParity.Stochastic.run_counter_zero_iff
#check @HiddenParity.Stochastic.killedReadout
#print axioms HiddenParity.Stochastic.killedReadout
#check @HiddenParity.Stochastic.killedReadout_oracle_independent
#print axioms HiddenParity.Stochastic.killedReadout_oracle_independent
#check @HiddenParity.Stochastic.killedReadout_measurable
#print axioms HiddenParity.Stochastic.killedReadout_measurable
#check @HiddenParity.Stochastic.killed_traceLaw_factorization
#print axioms HiddenParity.Stochastic.killed_traceLaw_factorization
#check @HiddenParity.Stochastic.killed_traceLaw_eq
#print axioms HiddenParity.Stochastic.killed_traceLaw_eq
#check @HiddenParity.Stochastic.HistoryStays
#print axioms HiddenParity.Stochastic.HistoryStays
#check @HiddenParity.Stochastic.historyStays_measurable
#print axioms HiddenParity.Stochastic.historyStays_measurable
#check @HiddenParity.Stochastic.killedHistory_alive_iff
#print axioms HiddenParity.Stochastic.killedHistory_alive_iff
#check @HiddenParity.Stochastic.killedHistory_all_alive_iff
#print axioms HiddenParity.Stochastic.killedHistory_all_alive_iff
#check @HiddenParity.Stochastic.killedHistory_records_of_stays
#print axioms HiddenParity.Stochastic.killedHistory_records_of_stays
#check @HiddenParity.Stochastic.aliveHistoryEvent
#print axioms HiddenParity.Stochastic.aliveHistoryEvent
#check @HiddenParity.Stochastic.aliveHistoryEvent_measurable
#print axioms HiddenParity.Stochastic.aliveHistoryEvent_measurable
#check @HiddenParity.Stochastic.aliveHistoryEvent_preimage
#print axioms HiddenParity.Stochastic.aliveHistoryEvent_preimage
#check @HiddenParity.Stochastic.canonical_history_event_eq_on_component
#print axioms HiddenParity.Stochastic.canonical_history_event_eq_on_component
#check @HiddenParity.Stochastic.canonical_history_restrict_eq
#print axioms HiddenParity.Stochastic.canonical_history_restrict_eq
#check @HiddenParity.Stochastic.SurvivingRecurrent
#print axioms HiddenParity.Stochastic.SurvivingRecurrent
#check @HiddenParity.Stochastic.survivingRecurrent_measurable
#print axioms HiddenParity.Stochastic.survivingRecurrent_measurable
#check @HiddenParity.Stochastic.canonical_surviving_recurrent_eq
#print axioms HiddenParity.Stochastic.canonical_surviving_recurrent_eq
#check @HiddenParity.Stochastic.ParitySuccess
#print axioms HiddenParity.Stochastic.ParitySuccess
#check @HiddenParity.Stochastic.paritySuccess_measurable
#print axioms HiddenParity.Stochastic.paritySuccess_measurable
#check @HiddenParity.Stochastic.matching_model_even_on_positive_surviving_recurrence
#print axioms HiddenParity.Stochastic.matching_model_even_on_positive_surviving_recurrence
#check @HiddenParity.Stochastic.currentState
#print axioms HiddenParity.Stochastic.currentState
#check @HiddenParity.Stochastic.erasePairSources
#print axioms HiddenParity.Stochastic.erasePairSources
#check @HiddenParity.Stochastic.pairPolicy
#print axioms HiddenParity.Stochastic.pairPolicy
#check @HiddenParity.Stochastic.pairPolicy_source
#print axioms HiddenParity.Stochastic.pairPolicy_source
#check @HiddenParity.Stochastic.pairPolicy_measurable
#print axioms HiddenParity.Stochastic.pairPolicy_measurable
#check @HiddenParity.Stochastic.canonical_markov_history_step
#print axioms HiddenParity.Stochastic.canonical_markov_history_step
#check @HiddenParity.Stochastic.realRows
#print axioms HiddenParity.Stochastic.realRows
#check @HiddenParity.Stochastic.realRows_nonnegative
#print axioms HiddenParity.Stochastic.realRows_nonnegative
#check @HiddenParity.Stochastic.realRows_normalized
#print axioms HiddenParity.Stochastic.realRows_normalized
#check @HiddenParity.Stochastic.realRows_match
#print axioms HiddenParity.Stochastic.realRows_match
#check @HiddenParity.Stochastic.markovHistoryLaw
#print axioms HiddenParity.Stochastic.markovHistoryLaw
#check @HiddenParity.Stochastic.markov_killed_historyLaw_eq
#print axioms HiddenParity.Stochastic.markov_killed_historyLaw_eq
#check @HiddenParity.Stochastic.markov_history_restrict_eq
#print axioms HiddenParity.Stochastic.markov_history_restrict_eq
#check @HiddenParity.Stochastic.markov_matching_parity_valid
#print axioms HiddenParity.Stochastic.markov_matching_parity_valid
#check @HiddenParity.ResidualSeed.SurvivesHistory
#print axioms HiddenParity.ResidualSeed.SurvivesHistory
#check @HiddenParity.ResidualSeed.markovSeedPosterior
#print axioms HiddenParity.ResidualSeed.markovSeedPosterior
#check @HiddenParity.ResidualSeed.markov_observed_prefix_mass
#print axioms HiddenParity.ResidualSeed.markov_observed_prefix_mass
#check @HiddenParity.ResidualSeed.markov_common_residual_seed
#print axioms HiddenParity.ResidualSeed.markov_common_residual_seed
#check @HiddenParity.ResidualSeed.restart_pairPolicy_agrees
#print axioms HiddenParity.ResidualSeed.restart_pairPolicy_agrees
#check @HiddenParity.ResidualSeed.markov_restartPolicy_measurable
#print axioms HiddenParity.ResidualSeed.markov_restartPolicy_measurable
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
#check @Orthemology.Tranche2.PolicyEmbedding.Input
#print axioms Orthemology.Tranche2.PolicyEmbedding.Input
#check @Orthemology.Tranche2.PolicyEmbedding.historyTrajectory
#print axioms Orthemology.Tranche2.PolicyEmbedding.historyTrajectory
#check @Orthemology.Tranche2.PolicyEmbedding.private_transcript_cylinder_probability
#print axioms Orthemology.Tranche2.PolicyEmbedding.private_transcript_cylinder_probability
#check @Orthemology.Tranche2.PolicyEmbedding.historyTrajectory_coordinate_measurable
#print axioms Orthemology.Tranche2.PolicyEmbedding.historyTrajectory_coordinate_measurable
#check @Orthemology.Tranche2.PolicyEmbedding.historyTrajectory_measurable
#print axioms Orthemology.Tranche2.PolicyEmbedding.historyTrajectory_measurable
#check @Orthemology.Tranche2.PolicyEmbedding.observedTraceLaw
#print axioms Orthemology.Tranche2.PolicyEmbedding.observedTraceLaw
#check @Orthemology.Tranche2.PolicyEmbedding.history_marginal_formula
#print axioms Orthemology.Tranche2.PolicyEmbedding.history_marginal_formula
#check @Orthemology.Tranche2.PolicyEmbedding.history_marginal_eq_all_query
#print axioms Orthemology.Tranche2.PolicyEmbedding.history_marginal_eq_all_query
#check @Orthemology.Tranche2.PolicyEmbedding.observed_prefix_map_from_last
#print axioms Orthemology.Tranche2.PolicyEmbedding.observed_prefix_map_from_last
#check @Orthemology.Tranche2.PolicyEmbedding.observedTraceLaw_eq_all_query
#print axioms Orthemology.Tranche2.PolicyEmbedding.observedTraceLaw_eq_all_query
#check @Orthemology.Tranche2.PolicyEmbedding.History
#print axioms Orthemology.Tranche2.PolicyEmbedding.History
#check @Orthemology.Tranche2.PolicyEmbedding.Stack
#print axioms Orthemology.Tranche2.PolicyEmbedding.Stack
#check @Orthemology.Tranche2.PolicyEmbedding.EvalState
#print axioms Orthemology.Tranche2.PolicyEmbedding.EvalState
#check @Orthemology.Tranche2.PolicyEmbedding.selected
#print axioms Orthemology.Tranche2.PolicyEmbedding.selected
#check @Orthemology.Tranche2.PolicyEmbedding.query
#print axioms Orthemology.Tranche2.PolicyEmbedding.query
#check @Orthemology.Tranche2.PolicyEmbedding.actionCount
#print axioms Orthemology.Tranche2.PolicyEmbedding.actionCount
#check @Orthemology.Tranche2.PolicyEmbedding.step
#print axioms Orthemology.Tranche2.PolicyEmbedding.step
#check @Orthemology.Tranche2.PolicyEmbedding.step_preserves_seed
#print axioms Orthemology.Tranche2.PolicyEmbedding.step_preserves_seed
#check @Orthemology.Tranche2.PolicyEmbedding.step_history_length
#print axioms Orthemology.Tranche2.PolicyEmbedding.step_history_length
#check @Orthemology.Tranche2.PolicyEmbedding.step_inside_row_independent
#print axioms Orthemology.Tranche2.PolicyEmbedding.step_inside_row_independent
#check @Orthemology.Tranche2.PolicyEmbedding.step_outside_coordinate_only
#print axioms Orthemology.Tranche2.PolicyEmbedding.step_outside_coordinate_only
#check @Orthemology.Tranche2.PolicyEmbedding.policyRun
#print axioms Orthemology.Tranche2.PolicyEmbedding.policyRun
#check @Orthemology.Tranche2.PolicyEmbedding.actionAt
#print axioms Orthemology.Tranche2.PolicyEmbedding.actionAt
#check @Orthemology.Tranche2.PolicyEmbedding.query_counter_eq_outside_actions
#print axioms Orthemology.Tranche2.PolicyEmbedding.query_counter_eq_outside_actions
#check @Orthemology.Tranche2.PolicyEmbedding.historyMeasurableSpace
#print axioms Orthemology.Tranche2.PolicyEmbedding.historyMeasurableSpace
#check @Orthemology.Tranche2.PolicyEmbedding.selected_measurable
#print axioms Orthemology.Tranche2.PolicyEmbedding.selected_measurable
#check @Orthemology.Tranche2.PolicyEmbedding.query_measurable
#print axioms Orthemology.Tranche2.PolicyEmbedding.query_measurable
#check @Orthemology.Tranche2.PolicyEmbedding.step_measurable
#print axioms Orthemology.Tranche2.PolicyEmbedding.step_measurable
#check @Orthemology.Tranche2.PolicyEmbedding.rowMass
#print axioms Orthemology.Tranche2.PolicyEmbedding.rowMass
#check @Orthemology.Tranche2.PolicyEmbedding.rowMass_nonneg
#print axioms Orthemology.Tranche2.PolicyEmbedding.rowMass_nonneg
#check @Orthemology.Tranche2.PolicyEmbedding.rowMass_pos
#print axioms Orthemology.Tranche2.PolicyEmbedding.rowMass_pos
#check @Orthemology.Tranche2.PolicyEmbedding.rowMass_normalized
#print axioms Orthemology.Tranche2.PolicyEmbedding.rowMass_normalized
#check @Orthemology.Tranche2.PolicyEmbedding.rowPMF
#print axioms Orthemology.Tranche2.PolicyEmbedding.rowPMF
#check @Orthemology.Tranche2.PolicyEmbedding.rowMass_coordinate
#print axioms Orthemology.Tranche2.PolicyEmbedding.rowMass_coordinate
#check @Orthemology.Tranche2.PolicyEmbedding.rowMeasure
#print axioms Orthemology.Tranche2.PolicyEmbedding.rowMeasure
#check @Orthemology.Tranche2.PolicyEmbedding.rowMeasure_probability
#print axioms Orthemology.Tranche2.PolicyEmbedding.rowMeasure_probability
#check @Orthemology.Tranche2.PolicyEmbedding.rowMeasure_full_support
#print axioms Orthemology.Tranche2.PolicyEmbedding.rowMeasure_full_support
#check @Orthemology.Tranche2.PolicyEmbedding.rowMeasure_coordinate
#print axioms Orthemology.Tranche2.PolicyEmbedding.rowMeasure_coordinate
#check @Orthemology.Tranche2.PolicyEmbedding.rowOracle_finite_prefix_positive
#print axioms Orthemology.Tranche2.PolicyEmbedding.rowOracle_finite_prefix_positive
#check @Orthemology.Tranche2.PolicyEmbedding.initialState
#print axioms Orthemology.Tranche2.PolicyEmbedding.initialState
#check @Orthemology.Tranche2.PolicyEmbedding.initialState_measurable
#print axioms Orthemology.Tranche2.PolicyEmbedding.initialState_measurable
#check @Orthemology.Tranche2.PolicyEmbedding.seedLaw
#print axioms Orthemology.Tranche2.PolicyEmbedding.seedLaw
#check @Orthemology.Tranche2.PolicyEmbedding.seedLaw_probability
#print axioms Orthemology.Tranche2.PolicyEmbedding.seedLaw_probability
#check @Orthemology.Tranche2.PolicyEmbedding.historyReadout
#print axioms Orthemology.Tranche2.PolicyEmbedding.historyReadout
#check @Orthemology.Tranche2.PolicyEmbedding.historyReadout_measurable
#print axioms Orthemology.Tranche2.PolicyEmbedding.historyReadout_measurable
#check @Orthemology.Tranche2.PolicyEmbedding.traceLaw_historyReadout
#print axioms Orthemology.Tranche2.PolicyEmbedding.traceLaw_historyReadout
#check @Orthemology.Tranche2.PolicyEmbedding.traceAction
#print axioms Orthemology.Tranche2.PolicyEmbedding.traceAction
#check @Orthemology.Tranche2.PolicyEmbedding.historyAction
#print axioms Orthemology.Tranche2.PolicyEmbedding.historyAction
#check @Orthemology.Tranche2.PolicyEmbedding.traceAction_measurable
#print axioms Orthemology.Tranche2.PolicyEmbedding.traceAction_measurable
#check @Orthemology.Tranche2.PolicyEmbedding.historyAction_measurable
#print axioms Orthemology.Tranche2.PolicyEmbedding.historyAction_measurable
#check @Orthemology.Tranche2.PolicyEmbedding.action_readout_on_run
#print axioms Orthemology.Tranche2.PolicyEmbedding.action_readout_on_run
#check @Orthemology.Tranche2.PolicyEmbedding.traceLaw_actionReadout
#print axioms Orthemology.Tranche2.PolicyEmbedding.traceLaw_actionReadout
#check @Orthemology.Tranche2.PolicyEmbedding.actionLaw
#print axioms Orthemology.Tranche2.PolicyEmbedding.actionLaw
#check @Orthemology.Tranche2.PolicyEmbedding.traceLaw_action_eq_canonical
#print axioms Orthemology.Tranche2.PolicyEmbedding.traceLaw_action_eq_canonical
#check @Orthemology.Tranche2.PolicyEmbedding.outsideCount
#print axioms Orthemology.Tranche2.PolicyEmbedding.outsideCount
#check @Orthemology.Tranche2.PolicyEmbedding.feedback
#print axioms Orthemology.Tranche2.PolicyEmbedding.feedback
#check @Orthemology.Tranche2.PolicyEmbedding.observedHistory
#print axioms Orthemology.Tranche2.PolicyEmbedding.observedHistory
#check @Orthemology.Tranche2.PolicyEmbedding.observedHistory_length
#print axioms Orthemology.Tranche2.PolicyEmbedding.observedHistory_length
#check @Orthemology.Tranche2.PolicyEmbedding.policyRun_eq_observedHistory
#print axioms Orthemology.Tranche2.PolicyEmbedding.policyRun_eq_observedHistory
#check @Orthemology.Tranche2.PolicyEmbedding.ActionCompatible
#print axioms Orthemology.Tranche2.PolicyEmbedding.ActionCompatible
#check @Orthemology.Tranche2.PolicyEmbedding.FeedbackCompatible
#print axioms Orthemology.Tranche2.PolicyEmbedding.FeedbackCompatible
#check @Orthemology.Tranche2.PolicyEmbedding.observedHistory_fiber
#print axioms Orthemology.Tranche2.PolicyEmbedding.observedHistory_fiber
#check @Orthemology.Tranche2.PolicyEmbedding.policyRun_transcript_fiber
#print axioms Orthemology.Tranche2.PolicyEmbedding.policyRun_transcript_fiber
#check @HiddenParity.ResidualSeed.normalized_product_rectangle
#print axioms HiddenParity.ResidualSeed.normalized_product_rectangle
#check @HiddenParity.ResidualSeed.FeedbackEvent
#print axioms HiddenParity.ResidualSeed.FeedbackEvent
#check @HiddenParity.ResidualSeed.feedbackEvent_measurable
#print axioms HiddenParity.ResidualSeed.feedbackEvent_measurable
#check @HiddenParity.ResidualSeed.posterior_input_product
#print axioms HiddenParity.ResidualSeed.posterior_input_product
#check @HiddenParity.ResidualSeed.posterior_seed_feedback_pushforward
#print axioms HiddenParity.ResidualSeed.posterior_seed_feedback_pushforward
#check @HiddenParity.ResidualSeed.unusedOracleTail
#print axioms HiddenParity.ResidualSeed.unusedOracleTail
#check @HiddenParity.ResidualSeed.unusedOracleTail_measurable
#print axioms HiddenParity.ResidualSeed.unusedOracleTail_measurable
#check @HiddenParity.ResidualSeed.posterior_seed_unused_tail_product
#print axioms HiddenParity.ResidualSeed.posterior_seed_unused_tail_product
#check @Orthemology.Tranche2.infinite_product_coordinate_law
#print axioms Orthemology.Tranche2.infinite_product_coordinate_law
#check @Orthemology.Tranche2.infinite_product_coordinates_independent
#print axioms Orthemology.Tranche2.infinite_product_coordinates_independent
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
#check @Orthemology.Tranche2.RecurrentSupport.Recurs
#print axioms Orthemology.Tranche2.RecurrentSupport.Recurs
#check @Orthemology.Tranche2.RecurrentSupport.recurrentSet
#print axioms Orthemology.Tranche2.RecurrentSupport.recurrentSet
#check @Orthemology.Tranche2.RecurrentSupport.mem_recurrentSet
#print axioms Orthemology.Tranche2.RecurrentSupport.mem_recurrentSet
#check @Orthemology.Tranche2.RecurrentSupport.exists_recurrent
#print axioms Orthemology.Tranche2.RecurrentSupport.exists_recurrent
#check @Orthemology.Tranche2.RecurrentSupport.recurrentSet_nonempty
#print axioms Orthemology.Tranche2.RecurrentSupport.recurrentSet_nonempty
#check @Orthemology.Tranche2.RecurrentSupport.eventually_mem_recurrentSet
#print axioms Orthemology.Tranche2.RecurrentSupport.eventually_mem_recurrentSet
#check @Orthemology.Tranche2.RecurrentSupport.recurrentSet_subset_of_eventually_mem
#print axioms Orthemology.Tranche2.RecurrentSupport.recurrentSet_subset_of_eventually_mem
#check @Orthemology.Tranche2.RecurrentSupport.exactRecurrentEvent
#print axioms Orthemology.Tranche2.RecurrentSupport.exactRecurrentEvent
#check @Orthemology.Tranche2.RecurrentSupport.tailEvent
#print axioms Orthemology.Tranche2.RecurrentSupport.tailEvent
#check @Orthemology.Tranche2.RecurrentSupport.exact_event_eventually_mem
#print axioms Orthemology.Tranche2.RecurrentSupport.exact_event_eventually_mem
#check @Orthemology.Tranche2.RecurrentSupport.exact_event_finitely_many_outside
#print axioms Orthemology.Tranche2.RecurrentSupport.exact_event_finitely_many_outside
#check @Orthemology.Tranche2.RecurrentSupport.exact_event_eq_iUnion_tail
#print axioms Orthemology.Tranche2.RecurrentSupport.exact_event_eq_iUnion_tail
#check @Orthemology.Tranche2.RecurrentSupport.measurable_recurrence
#print axioms Orthemology.Tranche2.RecurrentSupport.measurable_recurrence
#check @Orthemology.Tranche2.RecurrentSupport.measurable_exactRecurrentEvent
#print axioms Orthemology.Tranche2.RecurrentSupport.measurable_exactRecurrentEvent
#check @Orthemology.Tranche2.RecurrentSupport.measurable_tailEvent
#print axioms Orthemology.Tranche2.RecurrentSupport.measurable_tailEvent
#check @Orthemology.Tranche2.RecurrentSupport.exists_positive_recurrent_support
#print axioms Orthemology.Tranche2.RecurrentSupport.exists_positive_recurrent_support
#check @Orthemology.Tranche2.RecurrentSupport.exists_positive_tail_index
#print axioms Orthemology.Tranche2.RecurrentSupport.exists_positive_tail_index
#check @Orthemology.Tranche2.RecurrentSupport.exists_measurable_positive_recurrent_support
#print axioms Orthemology.Tranche2.RecurrentSupport.exists_measurable_positive_recurrent_support
#check @Orthemology.Tranche2.RecurrentSupport.support_subset_of_positive_exact_event
#print axioms Orthemology.Tranche2.RecurrentSupport.support_subset_of_positive_exact_event
#check @Orthemology.Tranche2.RecurrentSupport.abstract_self_verifying_support
#print axioms Orthemology.Tranche2.RecurrentSupport.abstract_self_verifying_support
#check @HiddenParity.ResidualSeed.CompatibleSeeds
#print axioms HiddenParity.ResidualSeed.CompatibleSeeds
#check @HiddenParity.ResidualSeed.compatibleSeedsDecidable
#print axioms HiddenParity.ResidualSeed.compatibleSeedsDecidable
#check @HiddenParity.ResidualSeed.PrefixEvent
#print axioms HiddenParity.ResidualSeed.PrefixEvent
#check @HiddenParity.ResidualSeed.CanonicalInput
#print axioms HiddenParity.ResidualSeed.CanonicalInput
#check @HiddenParity.ResidualSeed.RowLikelihood
#print axioms HiddenParity.ResidualSeed.RowLikelihood
#check @HiddenParity.ResidualSeed.normalizedRestriction
#print axioms HiddenParity.ResidualSeed.normalizedRestriction
#check @HiddenParity.ResidualSeed.seedPosterior
#print axioms HiddenParity.ResidualSeed.seedPosterior
#check @HiddenParity.ResidualSeed.commonSeedPosterior
#print axioms HiddenParity.ResidualSeed.commonSeedPosterior
#check @HiddenParity.ResidualSeed.compatibleSeeds_measurable
#print axioms HiddenParity.ResidualSeed.compatibleSeeds_measurable
#check @HiddenParity.ResidualSeed.prefixEvent_measurable
#print axioms HiddenParity.ResidualSeed.prefixEvent_measurable
#check @HiddenParity.ResidualSeed.prefixEvent_fiber
#print axioms HiddenParity.ResidualSeed.prefixEvent_fiber
#check @HiddenParity.ResidualSeed.fixed_seed_likelihood
#print axioms HiddenParity.ResidualSeed.fixed_seed_likelihood
#check @HiddenParity.ResidualSeed.seed_history_joint_probability
#print axioms HiddenParity.ResidualSeed.seed_history_joint_probability
#check @HiddenParity.ResidualSeed.prefix_probability
#print axioms HiddenParity.ResidualSeed.prefix_probability
#check @HiddenParity.ResidualSeed.restricted_seed_law
#print axioms HiddenParity.ResidualSeed.restricted_seed_law
#check @HiddenParity.ResidualSeed.rowLikelihood_ne_top
#print axioms HiddenParity.ResidualSeed.rowLikelihood_ne_top
#check @HiddenParity.ResidualSeed.seedPosterior_eq_common
#print axioms HiddenParity.ResidualSeed.seedPosterior_eq_common
#check @HiddenParity.ResidualSeed.canonicalInput_probability
#print axioms HiddenParity.ResidualSeed.canonicalInput_probability
#check @HiddenParity.ResidualSeed.positive_prefix_compatible_seeds
#print axioms HiddenParity.ResidualSeed.positive_prefix_compatible_seeds
#check @HiddenParity.ResidualSeed.rowLikelihood_pos
#print axioms HiddenParity.ResidualSeed.rowLikelihood_pos
#check @HiddenParity.ResidualSeed.surviving_model_prefix_positive
#print axioms HiddenParity.ResidualSeed.surviving_model_prefix_positive
#check @HiddenParity.ResidualSeed.commonSeedPosterior_probability
#print axioms HiddenParity.ResidualSeed.commonSeedPosterior_probability
#check @HiddenParity.ResidualSeed.posterior_equality_of_positive_prefixes
#print axioms HiddenParity.ResidualSeed.posterior_equality_of_positive_prefixes
#check @HiddenParity.ResidualSeed.restartPolicy
#print axioms HiddenParity.ResidualSeed.restartPolicy
#check @HiddenParity.ResidualSeed.restartPolicy_measurable
#print axioms HiddenParity.ResidualSeed.restartPolicy_measurable
#check @HiddenParity.ResidualSeed.compatible_append
#print axioms HiddenParity.ResidualSeed.compatible_append
#check @HiddenParity.ResidualSeed.observed_prefix_mass_eq_input
#print axioms HiddenParity.ResidualSeed.observed_prefix_mass_eq_input
#check @HiddenParity.ResidualSeed.empty_prefix_seedPosterior
#print axioms HiddenParity.ResidualSeed.empty_prefix_seedPosterior
#check @HiddenParity.ResidualSeed.impossible_prefix_seedPosterior
#print axioms HiddenParity.ResidualSeed.impossible_prefix_seedPosterior
