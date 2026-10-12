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
import PolicyCylinderProbability
import HistoryPathConsistency
import PolicyObservedLaw
import PolicyTraceBinding
import StackActionLaw
import RecurrentSupport
import RawTapeRecurrence
import SequentialTapeConsumption
import PruningKernel
import EndComponents
import RecurrentGraph
import KilledQueryLaw
import KilledAdaptiveHistory
import KilledRecurrentTransfer
import FiniteReachability
import ExecutablePruning
import MarkovSupportAdapter
import MarkovKilledBridge
import AdaptiveMarkovRecurrentGraph
import PolicyTailTransfer
import RelativeTailTransfer
import SafeSetTailTransfer
import SelfVerifyingSupport
import SeededPolicyNecessity
import FiniteChainAvoidance
import dependencies.StatisticalRepair
import HellingerTree
import SubprobHellinger
import DependentHellinger
import ResetBudget
import ResetLaw
import ResetTrajectory
import MarkovCharge
import FiniteChainTrajectory
import InfiniteRecurrence
import StationaryPairChain
import FairComponentParity
import CheckedTargetOperation
import StableSupportParityNecessity
import StageTargetOrExit
import ResidualSeedPosterior
import ConditionalPrefix
import ConditionalContinuationLaw
import PosteriorFeedbackProduct
import MarkovSeedPosterior
import ConditionalKilledContinuation
import LawfulRestart
import LawfulProbability
import ParityTailInvariance
import ConditionalAlmostSure
import SemanticWinning
import SemanticSafeActions
import HistoryStageSafety
import RegionAlgorithm
import GlobalParityNecessity
import RegionControls
import SCCPruning
import SCCParity
import SCCRegionAlgorithm
import SCCRegionControls
set_option pp.universes true
set_option pp.explicit true
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
#check @Orthemology.Tranche2.infinite_product_coordinate_law
#print axioms Orthemology.Tranche2.infinite_product_coordinate_law
#check @Orthemology.Tranche2.infinite_product_coordinates_independent
#print axioms Orthemology.Tranche2.infinite_product_coordinates_independent
#check @Orthemology.Tranche2.PolicyEmbedding.FamilyValue
#print axioms Orthemology.Tranche2.PolicyEmbedding.FamilyValue
#check @Orthemology.Tranche2.PolicyEmbedding.familyValueMeasurable
#print axioms Orthemology.Tranche2.PolicyEmbedding.familyValueMeasurable
#check @Orthemology.Tranche2.PolicyEmbedding.productFamily
#print axioms Orthemology.Tranche2.PolicyEmbedding.productFamily
#check @Orthemology.Tranche2.PolicyEmbedding.independent_product_families
#print axioms Orthemology.Tranche2.PolicyEmbedding.independent_product_families
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
#check @Orthemology.Tranche2.PolicyEmbedding.observedHistory_drop
#print axioms Orthemology.Tranche2.PolicyEmbedding.observedHistory_drop
#check @Orthemology.Tranche2.PolicyEmbedding.reconstructPrefix
#print axioms Orthemology.Tranche2.PolicyEmbedding.reconstructPrefix
#check @Orthemology.Tranche2.PolicyEmbedding.observedHistory_prefix_from_last
#print axioms Orthemology.Tranche2.PolicyEmbedding.observedHistory_prefix_from_last
#check @Orthemology.Tranche2.PolicyEmbedding.measure_eq_of_prefix_maps
#print axioms Orthemology.Tranche2.PolicyEmbedding.measure_eq_of_prefix_maps
#check @Orthemology.Tranche2.PolicyEmbedding.history_marginal_formula
#print axioms Orthemology.Tranche2.PolicyEmbedding.history_marginal_formula
#check @Orthemology.Tranche2.PolicyEmbedding.history_marginal_eq_all_query
#print axioms Orthemology.Tranche2.PolicyEmbedding.history_marginal_eq_all_query
#check @Orthemology.Tranche2.PolicyEmbedding.observed_prefix_map_from_last
#print axioms Orthemology.Tranche2.PolicyEmbedding.observed_prefix_map_from_last
#check @Orthemology.Tranche2.PolicyEmbedding.observedTraceLaw_eq_all_query
#print axioms Orthemology.Tranche2.PolicyEmbedding.observedTraceLaw_eq_all_query
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
#check @Orthemology.Tranche2.PolicyEmbedding.stackHistoryTrajectory
#print axioms Orthemology.Tranche2.PolicyEmbedding.stackHistoryTrajectory
#check @Orthemology.Tranche2.PolicyEmbedding.stackActionTrajectory
#print axioms Orthemology.Tranche2.PolicyEmbedding.stackActionTrajectory
#check @Orthemology.Tranche2.PolicyEmbedding.observedHistory_univ_oracle_irrelevant
#print axioms Orthemology.Tranche2.PolicyEmbedding.observedHistory_univ_oracle_irrelevant
#check @Orthemology.Tranche2.PolicyEmbedding.stackHistoryTrajectory_measurable
#print axioms Orthemology.Tranche2.PolicyEmbedding.stackHistoryTrajectory_measurable
#check @Orthemology.Tranche2.PolicyEmbedding.stackActionTrajectory_measurable
#print axioms Orthemology.Tranche2.PolicyEmbedding.stackActionTrajectory_measurable
#check @Orthemology.Tranche2.PolicyEmbedding.stackActionTrajectory_eq_historyAction
#print axioms Orthemology.Tranche2.PolicyEmbedding.stackActionTrajectory_eq_historyAction
#check @Orthemology.Tranche2.PolicyEmbedding.observedTraceLaw_univ_eq_stack
#print axioms Orthemology.Tranche2.PolicyEmbedding.observedTraceLaw_univ_eq_stack
#check @Orthemology.Tranche2.PolicyEmbedding.stackActionTrajectory_law
#print axioms Orthemology.Tranche2.PolicyEmbedding.stackActionTrajectory_law
#check @Orthemology.Tranche2.PolicyEmbedding.actionLaw_ae_of_stack
#print axioms Orthemology.Tranche2.PolicyEmbedding.actionLaw_ae_of_stack
#check @Orthemology.Tranche2.PolicyEmbedding.measurableSet_eventually_mem
#print axioms Orthemology.Tranche2.PolicyEmbedding.measurableSet_eventually_mem
#check @Orthemology.Tranche2.PolicyEmbedding.actionLaw_eventually_good_of_stack
#print axioms Orthemology.Tranche2.PolicyEmbedding.actionLaw_eventually_good_of_stack
#check @Orthemology.Tranche2.PolicyEmbedding.actionLaw_eventually_good_of_stack_fibers
#print axioms Orthemology.Tranche2.PolicyEmbedding.actionLaw_eventually_good_of_stack_fibers
#check @Orthemology.Tranche2.PolicyEmbedding.stack_coordinate_law
#print axioms Orthemology.Tranche2.PolicyEmbedding.stack_coordinate_law
#check @Orthemology.Tranche2.PolicyEmbedding.stack_coordinates_independent
#print axioms Orthemology.Tranche2.PolicyEmbedding.stack_coordinates_independent
#check @Orthemology.Tranche2.PolicyEmbedding.stack_coordinates_identDistrib
#print axioms Orthemology.Tranche2.PolicyEmbedding.stack_coordinates_identDistrib
#check @Orthemology.Tranche2.PolicyEmbedding.stack_coordinate_real_singleton
#print axioms Orthemology.Tranche2.PolicyEmbedding.stack_coordinate_real_singleton
#check @Orthemology.Tranche2.PolicyEmbedding.seededStackCoordinate
#print axioms Orthemology.Tranche2.PolicyEmbedding.seededStackCoordinate
#check @Orthemology.Tranche2.PolicyEmbedding.seededStackCoordinate_measurable
#print axioms Orthemology.Tranche2.PolicyEmbedding.seededStackCoordinate_measurable
#check @Orthemology.Tranche2.PolicyEmbedding.seededStackCoordinate_law
#print axioms Orthemology.Tranche2.PolicyEmbedding.seededStackCoordinate_law
#check @Orthemology.Tranche2.PolicyEmbedding.seededStackCoordinates_independent
#print axioms Orthemology.Tranche2.PolicyEmbedding.seededStackCoordinates_independent
#check @Orthemology.Tranche2.PolicyEmbedding.seededStackCoordinates_identDistrib
#print axioms Orthemology.Tranche2.PolicyEmbedding.seededStackCoordinates_identDistrib
#check @Orthemology.Tranche2.PolicyEmbedding.seededStackCoordinate_real_singleton
#print axioms Orthemology.Tranche2.PolicyEmbedding.seededStackCoordinate_real_singleton
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
#check @HiddenParity.Adaptive.seeded_tape_positive_symbol_recurs
#print axioms HiddenParity.Adaptive.seeded_tape_positive_symbol_recurs
#check @HiddenParity.Adaptive.seeded_all_tapes_recurrent
#print axioms HiddenParity.Adaptive.seeded_all_tapes_recurrent
#check @HiddenParity.Adaptive.seeded_all_tapes_supported
#print axioms HiddenParity.Adaptive.seeded_all_tapes_supported
#check @HiddenParity.Adaptive.countBefore
#print axioms HiddenParity.Adaptive.countBefore
#check @HiddenParity.Adaptive.countBefore_zero
#print axioms HiddenParity.Adaptive.countBefore_zero
#check @HiddenParity.Adaptive.countBefore_succ
#print axioms HiddenParity.Adaptive.countBefore_succ
#check @HiddenParity.Adaptive.countBefore_mono
#print axioms HiddenParity.Adaptive.countBefore_mono
#check @HiddenParity.Adaptive.countBefore_le_time
#print axioms HiddenParity.Adaptive.countBefore_le_time
#check @HiddenParity.Adaptive.recurrent_action_unbounded_count
#print axioms HiddenParity.Adaptive.recurrent_action_unbounded_count
#check @HiddenParity.Adaptive.recurrent_action_consumes_every_index
#print axioms HiddenParity.Adaptive.recurrent_action_consumes_every_index
#check @HiddenParity.Adaptive.stackReceipt
#print axioms HiddenParity.Adaptive.stackReceipt
#check @HiddenParity.Adaptive.recurrent_action_observes_recurrent_symbol
#print axioms HiddenParity.Adaptive.recurrent_action_observes_recurrent_symbol
#check @HiddenParity.Adaptive.historyReceipt
#print axioms HiddenParity.Adaptive.historyReceipt
#check @HiddenParity.Adaptive.stackReceipt_eq_historyReceipt
#print axioms HiddenParity.Adaptive.stackReceipt_eq_historyReceipt
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
#check @HiddenParity.Adaptive.retained_segment_reachable
#print axioms HiddenParity.Adaptive.retained_segment_reachable
#check @HiddenParity.Adaptive.recurrent_pairs_form_end_component
#print axioms HiddenParity.Adaptive.recurrent_pairs_form_end_component
#check @HiddenParity.Adaptive.measurable_recurrent_predicate
#print axioms HiddenParity.Adaptive.measurable_recurrent_predicate
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
#check @HiddenParity.Adaptive.stack_pair_source_next
#print axioms HiddenParity.Adaptive.stack_pair_source_next
#check @HiddenParity.Adaptive.supportSuccessors
#print axioms HiddenParity.Adaptive.supportSuccessors
#check @HiddenParity.Adaptive.canonical_markov_recurrent_end_component
#print axioms HiddenParity.Adaptive.canonical_markov_recurrent_end_component
#check @HiddenParity.Adaptive.canonical_markov_supported_path
#print axioms HiddenParity.Adaptive.canonical_markov_supported_path
#check @HiddenParity.Adaptive.markov_recurrent_end_component
#print axioms HiddenParity.Adaptive.markov_recurrent_end_component
#check @Orthemology.Tranche2.PolicyEmbedding.run_tail_finitely_queries
#print axioms Orthemology.Tranche2.PolicyEmbedding.run_tail_finitely_queries
#check @Orthemology.Tranche2.PolicyEmbedding.evaluator_positive_tail_transfers
#print axioms Orthemology.Tranche2.PolicyEmbedding.evaluator_positive_tail_transfers
#check @Orthemology.Tranche2.PolicyEmbedding.canonical_positive_tail_transfers
#print axioms Orthemology.Tranche2.PolicyEmbedding.canonical_positive_tail_transfers
#check @Orthemology.Tranche3.RelativeTransfer.absolutelyContinuous_of_atom_support
#print axioms Orthemology.Tranche3.RelativeTransfer.absolutelyContinuous_of_atom_support
#check @Orthemology.Tranche3.RelativeTransfer.iidOracle_prefix_atom
#print axioms Orthemology.Tranche3.RelativeTransfer.iidOracle_prefix_atom
#check @Orthemology.Tranche3.RelativeTransfer.iidOracle_prefix_domination
#print axioms Orthemology.Tranche3.RelativeTransfer.iidOracle_prefix_domination
#check @Orthemology.Tranche3.RelativeTransfer.relative_bounded_trace_domination
#print axioms Orthemology.Tranche3.RelativeTransfer.relative_bounded_trace_domination
#check @Orthemology.Tranche3.RelativeTransfer.relative_finite_query_domination
#print axioms Orthemology.Tranche3.RelativeTransfer.relative_finite_query_domination
#check @Orthemology.Tranche3.RelativeTransfer.positive_finite_query_event_relative
#print axioms Orthemology.Tranche3.RelativeTransfer.positive_finite_query_event_relative
#check @Orthemology.Tranche3.RelativeTransfer.rowMeasure_relative_support
#print axioms Orthemology.Tranche3.RelativeTransfer.rowMeasure_relative_support
#check @Orthemology.Tranche3.RelativeTransfer.canonical_positive_tail_relative
#print axioms Orthemology.Tranche3.RelativeTransfer.canonical_positive_tail_relative
#check @Orthemology.Tranche3.RelativeTransfer.canonical_positive_event_relative
#print axioms Orthemology.Tranche3.RelativeTransfer.canonical_positive_event_relative
#check @Orthemology.Tranche3.RelativeTransfer.alwaysIn
#print axioms Orthemology.Tranche3.RelativeTransfer.alwaysIn
#check @Orthemology.Tranche3.RelativeTransfer.measurable_alwaysIn
#print axioms Orthemology.Tranche3.RelativeTransfer.measurable_alwaysIn
#check @Orthemology.Tranche3.RelativeTransfer.zero_prefix_map
#print axioms Orthemology.Tranche3.RelativeTransfer.zero_prefix_map
#check @Orthemology.Tranche3.RelativeTransfer.zero_query_restricted_law_eq
#print axioms Orthemology.Tranche3.RelativeTransfer.zero_query_restricted_law_eq
#check @Orthemology.Tranche3.RelativeTransfer.all_inside_zero_queries
#print axioms Orthemology.Tranche3.RelativeTransfer.all_inside_zero_queries
#check @Orthemology.Tranche3.RelativeTransfer.canonical_event_eq_on_visited
#print axioms Orthemology.Tranche3.RelativeTransfer.canonical_event_eq_on_visited
#check @Orthemology.Tranche3.RelativeTransfer.canonical_positive_tail_on_safe_actions
#print axioms Orthemology.Tranche3.RelativeTransfer.canonical_positive_tail_on_safe_actions
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
#check @Orthemology.Tranche2.PolicyEmbedding.actionLaw_isProbability
#print axioms Orthemology.Tranche2.PolicyEmbedding.actionLaw_isProbability
#check @Orthemology.Tranche2.PolicyEmbedding.seeded_policy_self_verifying_necessity
#print axioms Orthemology.Tranche2.PolicyEmbedding.seeded_policy_self_verifying_necessity
#check @Orthemology.Tranche2.PolicyEmbedding.seeded_policy_kernel_nonempty
#print axioms Orthemology.Tranche2.PolicyEmbedding.seeded_policy_kernel_nonempty
#check @HiddenParity.Recurrence.FiniteChain
#print axioms HiddenParity.Recurrence.FiniteChain
#check @HiddenParity.Recurrence.avoid
#print axioms HiddenParity.Recurrence.avoid
#check @HiddenParity.Recurrence.avoid_nonnegative
#print axioms HiddenParity.Recurrence.avoid_nonnegative
#check @HiddenParity.Recurrence.avoid_le_one
#print axioms HiddenParity.Recurrence.avoid_le_one
#check @HiddenParity.Recurrence.avoid_succ_le
#print axioms HiddenParity.Recurrence.avoid_succ_le
#check @HiddenParity.Recurrence.avoid_antitone
#print axioms HiddenParity.Recurrence.avoid_antitone
#check @HiddenParity.Recurrence.avoid_lt_one_predecessor
#print axioms HiddenParity.Recurrence.avoid_lt_one_predecessor
#check @HiddenParity.Recurrence.reachable_avoids_lt_one
#print axioms HiddenParity.Recurrence.reachable_avoids_lt_one
#check @HiddenParity.Recurrence.exists_uniform_avoidance_bound
#print axioms HiddenParity.Recurrence.exists_uniform_avoidance_bound
#check @HiddenParity.Recurrence.avoid_add_bound
#print axioms HiddenParity.Recurrence.avoid_add_bound
#check @HiddenParity.Recurrence.avoid_blocks_bound
#print axioms HiddenParity.Recurrence.avoid_blocks_bound
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
#check @HiddenParity.Recurrence.transitionPMF
#print axioms HiddenParity.Recurrence.transitionPMF
#check @HiddenParity.Recurrence.transitionKernel
#print axioms HiddenParity.Recurrence.transitionKernel
#check @HiddenParity.Recurrence.transitionKernel_markov
#print axioms HiddenParity.Recurrence.transitionKernel_markov
#check @HiddenParity.Recurrence.transitionKernel_singleton
#print axioms HiddenParity.Recurrence.transitionKernel_singleton
#check @HiddenParity.Recurrence.lintegral_transition_ofReal
#print axioms HiddenParity.Recurrence.lintegral_transition_ofReal
#check @HiddenParity.Recurrence.pathAvoid
#print axioms HiddenParity.Recurrence.pathAvoid
#check @HiddenParity.Recurrence.pathAvoid_measurable
#print axioms HiddenParity.Recurrence.pathAvoid_measurable
#check @HiddenParity.Recurrence.pathAvoid_depends
#print axioms HiddenParity.Recurrence.pathAvoid_depends
#check @HiddenParity.Recurrence.lmarginal_current_if
#print axioms HiddenParity.Recurrence.lmarginal_current_if
#check @HiddenParity.Recurrence.lmarginal_pathAvoid
#print axioms HiddenParity.Recurrence.lmarginal_pathAvoid
#check @HiddenParity.Recurrence.trajectory_integral_prefix
#print axioms HiddenParity.Recurrence.trajectory_integral_prefix
#check @HiddenParity.Recurrence.trajectory_interval_avoidance_bound
#print axioms HiddenParity.Recurrence.trajectory_interval_avoidance_bound
#check @HiddenParity.Recurrence.AvoidInterval
#print axioms HiddenParity.Recurrence.AvoidInterval
#check @HiddenParity.Recurrence.avoidIntervalDecidable
#print axioms HiddenParity.Recurrence.avoidIntervalDecidable
#check @HiddenParity.Recurrence.pathAvoid_eq_ite
#print axioms HiddenParity.Recurrence.pathAvoid_eq_ite
#check @HiddenParity.Recurrence.avoidInterval_measurable
#print axioms HiddenParity.Recurrence.avoidInterval_measurable
#check @HiddenParity.Recurrence.pathAvoid_eq_indicator
#print axioms HiddenParity.Recurrence.pathAvoid_eq_indicator
#check @HiddenParity.Recurrence.interval_avoidance_probability_le
#print axioms HiddenParity.Recurrence.interval_avoidance_probability_le
#check @HiddenParity.Recurrence.ForeverAvoid
#print axioms HiddenParity.Recurrence.ForeverAvoid
#check @HiddenParity.Recurrence.forever_avoid_null
#print axioms HiddenParity.Recurrence.forever_avoid_null
#check @HiddenParity.Recurrence.target_recurs_almost_surely
#print axioms HiddenParity.Recurrence.target_recurs_almost_surely
#check @HiddenParity.Recurrence.all_states_recur_almost_surely
#print axioms HiddenParity.Recurrence.all_states_recur_almost_surely
#check @HiddenParity.Recurrence.StationaryChoices
#print axioms HiddenParity.Recurrence.StationaryChoices
#check @HiddenParity.Recurrence.pairChain
#print axioms HiddenParity.Recurrence.pairChain
#check @HiddenParity.Recurrence.pairChain_edge
#print axioms HiddenParity.Recurrence.pairChain_edge
#check @HiddenParity.Recurrence.positiveSuccessors
#print axioms HiddenParity.Recurrence.positiveSuccessors
#check @HiddenParity.Recurrence.pairChain_strongly_connected
#print axioms HiddenParity.Recurrence.pairChain_strongly_connected
#check @HiddenParity.Recurrence.actionFiber
#print axioms HiddenParity.Recurrence.actionFiber
#check @HiddenParity.Recurrence.actionFiber_nonempty
#print axioms HiddenParity.Recurrence.actionFiber_nonempty
#check @HiddenParity.Recurrence.uniformWeight
#print axioms HiddenParity.Recurrence.uniformWeight
#check @HiddenParity.Recurrence.uniformWeight_positive
#print axioms HiddenParity.Recurrence.uniformWeight_positive
#check @HiddenParity.Recurrence.uniformChoices
#print axioms HiddenParity.Recurrence.uniformChoices
#check @HiddenParity.Recurrence.pairReadout
#print axioms HiddenParity.Recurrence.pairReadout
#check @HiddenParity.Recurrence.pairReadout_measurable
#print axioms HiddenParity.Recurrence.pairReadout_measurable
#check @HiddenParity.Recurrence.operatingPairLaw
#print axioms HiddenParity.Recurrence.operatingPairLaw
#check @HiddenParity.Recurrence.operatingPairLaw_probability
#print axioms HiddenParity.Recurrence.operatingPairLaw_probability
#check @HiddenParity.Recurrence.stationary_component_all_pairs_recur
#print axioms HiddenParity.Recurrence.stationary_component_all_pairs_recur
#check @HiddenParity.Recurrence.PairParitySuccess
#print axioms HiddenParity.Recurrence.PairParitySuccess
#check @HiddenParity.Recurrence.stationary_component_parity
#print axioms HiddenParity.Recurrence.stationary_component_parity
#check @HiddenParity.Recurrence.uniform_component_parity
#print axioms HiddenParity.Recurrence.uniform_component_parity
#check @HiddenParity.Recurrence.endComponent_successor_congr
#print axioms HiddenParity.Recurrence.endComponent_successor_congr
#check @HiddenParity.Recurrence.realProbability
#print axioms HiddenParity.Recurrence.realProbability
#check @HiddenParity.Recurrence.realProbability_nonnegative
#print axioms HiddenParity.Recurrence.realProbability_nonnegative
#check @HiddenParity.Recurrence.realProbability_normalized
#print axioms HiddenParity.Recurrence.realProbability_normalized
#check @HiddenParity.Recurrence.positiveSuccessors_eq_internal
#print axioms HiddenParity.Recurrence.positiveSuccessors_eq_internal
#check @HiddenParity.Recurrence.uniformMarkovOperation
#print axioms HiddenParity.Recurrence.uniformMarkovOperation
#check @HiddenParity.Recurrence.matching_component_closed
#print axioms HiddenParity.Recurrence.matching_component_closed
#check @HiddenParity.Recurrence.qualifying_uniform_wins_matching
#print axioms HiddenParity.Recurrence.qualifying_uniform_wins_matching
#check @HiddenParity.Recurrence.qualifying_uniform_all_pairs_recur
#print axioms HiddenParity.Recurrence.qualifying_uniform_all_pairs_recur
#check @HiddenParity.Recurrence.computed_target_uniform_certificate
#print axioms HiddenParity.Recurrence.computed_target_uniform_certificate
#check @HiddenParity.Adaptive.markovPairLaw
#print axioms HiddenParity.Adaptive.markovPairLaw
#check @HiddenParity.Adaptive.stable_support_parity_qualifying_component
#print axioms HiddenParity.Adaptive.stable_support_parity_qualifying_component
#check @HiddenParity.Adaptive.stable_support_computed_targets_nonempty
#print axioms HiddenParity.Adaptive.stable_support_computed_targets_nonempty
#check @HiddenParity.Adaptive.stable_support_path_to_computed_target
#print axioms HiddenParity.Adaptive.stable_support_path_to_computed_target
#check @HiddenParity.Adaptive.support_preserving_policy_path_to_target
#print axioms HiddenParity.Adaptive.support_preserving_policy_path_to_target
#check @HiddenParity.Stage.liveUpdate
#print axioms HiddenParity.Stage.liveUpdate
#check @HiddenParity.Stage.mem_liveUpdate
#print axioms HiddenParity.Stage.mem_liveUpdate
#check @HiddenParity.Stage.liveUpdate_eq_iff_internal
#print axioms HiddenParity.Stage.liveUpdate_eq_iff_internal
#check @HiddenParity.Stage.liveUpdate_nonempty_of_true_positive
#print axioms HiddenParity.Stage.liveUpdate_nonempty_of_true_positive
#check @HiddenParity.Stage.liveUpdate_strict_of_noninternal
#print axioms HiddenParity.Stage.liveUpdate_strict_of_noninternal
#check @HiddenParity.Stage.ReachableExit
#print axioms HiddenParity.Stage.ReachableExit
#check @HiddenParity.Stage.SameSupportPrefix
#print axioms HiddenParity.Stage.SameSupportPrefix
#check @HiddenParity.Stage.winning_policy_target_or_exit
#print axioms HiddenParity.Stage.winning_policy_target_or_exit
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
#check @HiddenParity.ResidualSeed.Continuation.rowLikelihood_cons
#print axioms HiddenParity.ResidualSeed.Continuation.rowLikelihood_cons
#check @HiddenParity.ResidualSeed.Continuation.rowLikelihood_append
#print axioms HiddenParity.ResidualSeed.Continuation.rowLikelihood_append
#check @HiddenParity.ResidualSeed.Continuation.prefixEvent_append_subset
#print axioms HiddenParity.ResidualSeed.Continuation.prefixEvent_append_subset
#check @HiddenParity.ResidualSeed.Continuation.compatibleSeeds_append
#print axioms HiddenParity.ResidualSeed.Continuation.compatibleSeeds_append
#check @HiddenParity.ResidualSeed.Continuation.conditional_extension_probability
#print axioms HiddenParity.ResidualSeed.Continuation.conditional_extension_probability
#check @HiddenParity.ResidualSeed.Continuation.conditional_extension_eq
#print axioms HiddenParity.ResidualSeed.Continuation.conditional_extension_eq
#check @HiddenParity.ResidualSeed.Continuation.continuationHistory
#print axioms HiddenParity.ResidualSeed.Continuation.continuationHistory
#check @HiddenParity.ResidualSeed.Continuation.continuationHistory_measurable
#print axioms HiddenParity.ResidualSeed.Continuation.continuationHistory_measurable
#check @HiddenParity.ResidualSeed.Continuation.continuationHistory_length
#print axioms HiddenParity.ResidualSeed.Continuation.continuationHistory_length
#check @HiddenParity.ResidualSeed.Continuation.continuationHistory_drop
#print axioms HiddenParity.ResidualSeed.Continuation.continuationHistory_drop
#check @HiddenParity.ResidualSeed.Continuation.actual_history_eq_continuation_append
#print axioms HiddenParity.ResidualSeed.Continuation.actual_history_eq_continuation_append
#check @HiddenParity.ResidualSeed.Continuation.continuation_event_inter_prefix
#print axioms HiddenParity.ResidualSeed.Continuation.continuation_event_inter_prefix
#check @HiddenParity.ResidualSeed.Continuation.conditionalContinuationLaw
#print axioms HiddenParity.ResidualSeed.Continuation.conditionalContinuationLaw
#check @HiddenParity.ResidualSeed.Continuation.conditional_continuation_marginal
#print axioms HiddenParity.ResidualSeed.Continuation.conditional_continuation_marginal
#check @HiddenParity.ResidualSeed.Continuation.conditional_continuation_marginal_eq_restart
#print axioms HiddenParity.ResidualSeed.Continuation.conditional_continuation_marginal_eq_restart
#check @HiddenParity.ResidualSeed.Continuation.conditional_prefix_map_from_last
#print axioms HiddenParity.ResidualSeed.Continuation.conditional_prefix_map_from_last
#check @HiddenParity.ResidualSeed.Continuation.conditionalContinuationLaw_eq_restart
#print axioms HiddenParity.ResidualSeed.Continuation.conditionalContinuationLaw_eq_restart
#check @HiddenParity.ResidualSeed.Continuation.continuationReadout
#print axioms HiddenParity.ResidualSeed.Continuation.continuationReadout
#check @HiddenParity.ResidualSeed.Continuation.continuationReadout_measurable
#print axioms HiddenParity.ResidualSeed.Continuation.continuationReadout_measurable
#check @HiddenParity.ResidualSeed.Continuation.normalizedRestriction_map_preimage
#print axioms HiddenParity.ResidualSeed.Continuation.normalizedRestriction_map_preimage
#check @HiddenParity.ResidualSeed.Continuation.conditionalContinuationLaw_eq_conditioned_observation
#print axioms HiddenParity.ResidualSeed.Continuation.conditionalContinuationLaw_eq_conditioned_observation
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
#check @HiddenParity.ResidualSeed.Continuation.conditional_killed_continuation_eq
#print axioms HiddenParity.ResidualSeed.Continuation.conditional_killed_continuation_eq
#check @HiddenParity.ResidualSeed.Continuation.conditional_continuation_restrict_eq
#print axioms HiddenParity.ResidualSeed.Continuation.conditional_continuation_restrict_eq
#check @HiddenParity.ResidualSeed.Continuation.conditional_surviving_recurrent_eq
#print axioms HiddenParity.ResidualSeed.Continuation.conditional_surviving_recurrent_eq
#check @HiddenParity.ResidualSeed.Continuation.conditionalMarkovContinuationLaw
#print axioms HiddenParity.ResidualSeed.Continuation.conditionalMarkovContinuationLaw
#check @HiddenParity.ResidualSeed.Continuation.conditionalMarkovContinuationLaw_eq_restart
#print axioms HiddenParity.ResidualSeed.Continuation.conditionalMarkovContinuationLaw_eq_restart
#check @HiddenParity.ResidualSeed.Continuation.conditional_markov_killed_eq
#print axioms HiddenParity.ResidualSeed.Continuation.conditional_markov_killed_eq
#check @HiddenParity.ResidualSeed.Continuation.conditional_markov_surviving_recurrent_eq
#print axioms HiddenParity.ResidualSeed.Continuation.conditional_markov_surviving_recurrent_eq
#check @HiddenParity.Necessity.liveHistory
#print axioms HiddenParity.Necessity.liveHistory
#check @HiddenParity.Necessity.mem_liveHistory
#print axioms HiddenParity.Necessity.mem_liveHistory
#check @HiddenParity.Necessity.liveHistory_nil
#print axioms HiddenParity.Necessity.liveHistory_nil
#check @HiddenParity.Necessity.liveHistory_subset
#print axioms HiddenParity.Necessity.liveHistory_subset
#check @HiddenParity.Necessity.liveHistory_cons
#print axioms HiddenParity.Necessity.liveHistory_cons
#check @HiddenParity.Necessity.liveHistory_append
#print axioms HiddenParity.Necessity.liveHistory_append
#check @HiddenParity.Necessity.liveHistory_survives
#print axioms HiddenParity.Necessity.liveHistory_survives
#check @HiddenParity.Necessity.currentState_append
#print axioms HiddenParity.Necessity.currentState_append
#check @HiddenParity.Necessity.Lawful
#print axioms HiddenParity.Necessity.Lawful
#check @HiddenParity.Necessity.commonPosterior_ae_of_original
#print axioms HiddenParity.Necessity.commonPosterior_ae_of_original
#check @HiddenParity.Necessity.commonPosterior_compatible
#print axioms HiddenParity.Necessity.commonPosterior_compatible
#check @HiddenParity.Necessity.lawful_restart
#print axioms HiddenParity.Necessity.lawful_restart
#check @HiddenParity.Necessity.IllegalPrefixEvent
#print axioms HiddenParity.Necessity.IllegalPrefixEvent
#check @HiddenParity.Necessity.illegal_prefix_factorization
#print axioms HiddenParity.Necessity.illegal_prefix_factorization
#check @HiddenParity.Necessity.live_model_rowLikelihood_positive
#print axioms HiddenParity.Necessity.live_model_rowLikelihood_positive
#check @HiddenParity.Necessity.positive_prefix_mem_live
#print axioms HiddenParity.Necessity.positive_prefix_mem_live
#check @HiddenParity.Necessity.lawful_iff_illegal_prefix_probability_zero
#print axioms HiddenParity.Necessity.lawful_iff_illegal_prefix_probability_zero
#check @HiddenParity.Necessity.lawful_iff_positive_prefix_legal
#print axioms HiddenParity.Necessity.lawful_iff_positive_prefix_legal
#check @HiddenParity.Adaptive.recurs_shift_iff
#print axioms HiddenParity.Adaptive.recurs_shift_iff
#check @HiddenParity.Adaptive.recurrentSet_shift
#print axioms HiddenParity.Adaptive.recurrentSet_shift
#check @HiddenParity.Adaptive.paritySuccess_shift_iff
#print axioms HiddenParity.Adaptive.paritySuccess_shift_iff
#check @HiddenParity.ResidualSeed.Continuation.action_continuationReadout_shift
#print axioms HiddenParity.ResidualSeed.Continuation.action_continuationReadout_shift
#check @HiddenParity.ResidualSeed.Continuation.conditional_ae_of_prefix_imp
#print axioms HiddenParity.ResidualSeed.Continuation.conditional_ae_of_prefix_imp
#check @HiddenParity.ResidualSeed.Continuation.conditional_ae_tail_property
#print axioms HiddenParity.ResidualSeed.Continuation.conditional_ae_tail_property
#check @HiddenParity.ResidualSeed.Continuation.conditional_ae_parity
#print axioms HiddenParity.ResidualSeed.Continuation.conditional_ae_parity
#check @HiddenParity.ResidualSeed.Continuation.markov_restart_ae_of_prefix_imp
#print axioms HiddenParity.ResidualSeed.Continuation.markov_restart_ae_of_prefix_imp
#check @HiddenParity.ResidualSeed.Continuation.markov_restart_ae_tail_property
#print axioms HiddenParity.ResidualSeed.Continuation.markov_restart_ae_tail_property
#check @HiddenParity.ResidualSeed.Continuation.markov_restart_ae_parity
#print axioms HiddenParity.ResidualSeed.Continuation.markov_restart_ae_parity
#check @HiddenParity.ResidualSeed.Continuation.matching_rival_even_after_positive_prefix
#print axioms HiddenParity.ResidualSeed.Continuation.matching_rival_even_after_positive_prefix
#check @HiddenParity.Necessity.WinningPolicy
#print axioms HiddenParity.Necessity.WinningPolicy
#check @HiddenParity.Necessity.SemanticWinning
#print axioms HiddenParity.Necessity.SemanticWinning
#check @HiddenParity.Necessity.semanticRegion
#print axioms HiddenParity.Necessity.semanticRegion
#check @HiddenParity.Necessity.mem_semanticRegion
#print axioms HiddenParity.Necessity.mem_semanticRegion
#check @HiddenParity.Necessity.restartWinningPolicy
#print axioms HiddenParity.Necessity.restartWinningPolicy
#check @HiddenParity.Necessity.semanticWinning_at_positive_history
#print axioms HiddenParity.Necessity.semanticWinning_at_positive_history
#check @HiddenParity.Necessity.winningPolicy_pair_parity
#print axioms HiddenParity.Necessity.winningPolicy_pair_parity
#check @HiddenParity.Necessity.SemanticSafe
#print axioms HiddenParity.Necessity.SemanticSafe
#check @HiddenParity.Necessity.semanticAllowed
#print axioms HiddenParity.Necessity.semanticAllowed
#check @HiddenParity.Necessity.mem_semanticAllowed
#print axioms HiddenParity.Necessity.mem_semanticAllowed
#check @HiddenParity.Necessity.positive_action_branch_safe
#print axioms HiddenParity.Necessity.positive_action_branch_safe
#check @HiddenParity.Necessity.winning_policy_safe_at_same_support_history
#print axioms HiddenParity.Necessity.winning_policy_safe_at_same_support_history
#check @HiddenParity.Necessity.stack_history_succ
#print axioms HiddenParity.Necessity.stack_history_succ
#check @HiddenParity.Necessity.stack_history_compatible
#print axioms HiddenParity.Necessity.stack_history_compatible
#check @HiddenParity.Necessity.stack_liveHistory_of_same_prefix
#print axioms HiddenParity.Necessity.stack_liveHistory_of_same_prefix
#check @HiddenParity.Necessity.sameSupportPrefix_measurable
#print axioms HiddenParity.Necessity.sameSupportPrefix_measurable
#check @HiddenParity.Necessity.allowed_until_exit_measurable
#print axioms HiddenParity.Necessity.allowed_until_exit_measurable
#check @HiddenParity.Necessity.winningPolicy_safe_until_exit
#print axioms HiddenParity.Necessity.winningPolicy_safe_until_exit
#check @HiddenParity.Necessity.semantic_winning_target_or_exit
#print axioms HiddenParity.Necessity.semantic_winning_target_or_exit
#check @HiddenParity.Necessity.reachDecidable
#print axioms HiddenParity.Necessity.reachDecidable
#check @HiddenParity.Necessity.reachableExitDecidable
#print axioms HiddenParity.Necessity.reachableExitDecidable
#check @HiddenParity.Necessity.regionAllowed
#print axioms HiddenParity.Necessity.regionAllowed
#check @HiddenParity.Necessity.mem_regionAllowed
#print axioms HiddenParity.Necessity.mem_regionAllowed
#check @HiddenParity.Necessity.regionStep
#print axioms HiddenParity.Necessity.regionStep
#check @HiddenParity.Necessity.mem_regionStep
#print axioms HiddenParity.Necessity.mem_regionStep
#check @HiddenParity.Necessity.descend
#print axioms HiddenParity.Necessity.descend
#check @HiddenParity.Necessity.computedRegion
#print axioms HiddenParity.Necessity.computedRegion
#check @HiddenParity.Necessity.winningRegion
#print axioms HiddenParity.Necessity.winningRegion
#check @HiddenParity.Necessity.regionAllowed_mono
#print axioms HiddenParity.Necessity.regionAllowed_mono
#check @HiddenParity.Necessity.targetStates_mono
#print axioms HiddenParity.Necessity.targetStates_mono
#check @HiddenParity.Necessity.reachableExit_mono
#print axioms HiddenParity.Necessity.reachableExit_mono
#check @HiddenParity.Necessity.regionStep_subset
#print axioms HiddenParity.Necessity.regionStep_subset
#check @HiddenParity.Necessity.regionStep_mono
#print axioms HiddenParity.Necessity.regionStep_mono
#check @HiddenParity.Necessity.postfixed_subset_descend
#print axioms HiddenParity.Necessity.postfixed_subset_descend
#check @HiddenParity.Necessity.descend_eq_of_stable
#print axioms HiddenParity.Necessity.descend_eq_of_stable
#check @HiddenParity.Necessity.descend_stable
#print axioms HiddenParity.Necessity.descend_stable
#check @HiddenParity.Necessity.computedRegion_fixed_stage
#print axioms HiddenParity.Necessity.computedRegion_fixed_stage
#check @HiddenParity.Necessity.regionAllowed_congr_lower
#print axioms HiddenParity.Necessity.regionAllowed_congr_lower
#check @HiddenParity.Necessity.regionStep_congr_lower
#print axioms HiddenParity.Necessity.regionStep_congr_lower
#check @HiddenParity.Necessity.computedRegion_fuel_irrelevant
#print axioms HiddenParity.Necessity.computedRegion_fuel_irrelevant
#check @HiddenParity.Necessity.winningRegion_fixed
#print axioms HiddenParity.Necessity.winningRegion_fixed
#check @HiddenParity.Necessity.semanticAllowed_subset_regionAllowed
#print axioms HiddenParity.Necessity.semanticAllowed_subset_regionAllowed
#check @HiddenParity.Necessity.semanticRegion_postfixed
#print axioms HiddenParity.Necessity.semanticRegion_postfixed
#check @HiddenParity.Necessity.semanticRegion_subset_computedRegion
#print axioms HiddenParity.Necessity.semanticRegion_subset_computedRegion
#check @HiddenParity.Necessity.winning_policy_mem_winningRegion
#print axioms HiddenParity.Necessity.winning_policy_mem_winningRegion
#check @HiddenParity.Necessity.computed_losing_excludes_common_policy
#print axioms HiddenParity.Necessity.computed_losing_excludes_common_policy
#check @HiddenParity.Necessity.Controls.S
#print axioms HiddenParity.Necessity.Controls.S
#check @HiddenParity.Necessity.Controls.A
#print axioms HiddenParity.Necessity.Controls.A
#check @HiddenParity.Necessity.Controls.M
#print axioms HiddenParity.Necessity.Controls.M
#check @HiddenParity.Necessity.Controls.branchKernel
#print axioms HiddenParity.Necessity.Controls.branchKernel
#check @HiddenParity.Necessity.Controls.allMenu
#print axioms HiddenParity.Necessity.Controls.allMenu
#check @HiddenParity.Necessity.Controls.branchPriority
#print axioms HiddenParity.Necessity.Controls.branchPriority
#check @HiddenParity.Necessity.Controls.losing_child_rejects_parent
#print axioms HiddenParity.Necessity.Controls.losing_child_rejects_parent
#check @HiddenParity.Necessity.Controls.revealed_even_child_wins
#print axioms HiddenParity.Necessity.Controls.revealed_even_child_wins
#check @HiddenParity.Necessity.Controls.revealed_odd_child_loses
#print axioms HiddenParity.Necessity.Controls.revealed_odd_child_loses
#check @HiddenParity.Necessity.Controls.deadMenu
#print axioms HiddenParity.Necessity.Controls.deadMenu
#check @HiddenParity.Necessity.Controls.dead_successor_rejected
#print axioms HiddenParity.Necessity.Controls.dead_successor_rejected
#check @HiddenParity.Necessity.Controls.empty_support_rejected
#print axioms HiddenParity.Necessity.Controls.empty_support_rejected
#check @HiddenParity.Necessity.Controls.cycleKernel
#print axioms HiddenParity.Necessity.Controls.cycleKernel
#check @HiddenParity.Necessity.Controls.cycleMenu
#print axioms HiddenParity.Necessity.Controls.cycleMenu
#check @HiddenParity.Necessity.Controls.cyclePriority
#print axioms HiddenParity.Necessity.Controls.cyclePriority
#check @HiddenParity.Necessity.Controls.higher_odd_recurs_and_wins
#print axioms HiddenParity.Necessity.Controls.higher_odd_recurs_and_wins
#check @HiddenParity.Necessity.Controls.lower_odd_recurs_and_loses
#print axioms HiddenParity.Necessity.Controls.lower_odd_recurs_and_loses
#check @HiddenParity.Necessity.Controls.excess_fuel_same_output
#print axioms HiddenParity.Necessity.Controls.excess_fuel_same_output
#check @HiddenParity.Necessity.Controls.no_common_policy_at_bad_branch
#print axioms HiddenParity.Necessity.Controls.no_common_policy_at_bad_branch
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
#check @HiddenParity.SCCRegion.regionStep
#print axioms HiddenParity.SCCRegion.regionStep
#check @HiddenParity.SCCRegion.computedRegion
#print axioms HiddenParity.SCCRegion.computedRegion
#check @HiddenParity.SCCRegion.winningRegion
#print axioms HiddenParity.SCCRegion.winningRegion
#check @HiddenParity.SCCRegion.regionStep_eq
#print axioms HiddenParity.SCCRegion.regionStep_eq
#check @HiddenParity.SCCRegion.computedRegion_eq
#print axioms HiddenParity.SCCRegion.computedRegion_eq
#check @HiddenParity.SCCRegion.winningRegion_eq
#print axioms HiddenParity.SCCRegion.winningRegion_eq
#check @HiddenParity.SCCRegion.computedRegion_fuel_irrelevant
#print axioms HiddenParity.SCCRegion.computedRegion_fuel_irrelevant
#check @HiddenParity.SCCRegion.winning_policy_mem_winningRegion
#print axioms HiddenParity.SCCRegion.winning_policy_mem_winningRegion
#check @HiddenParity.SCCRegion.computed_losing_excludes_common_policy
#print axioms HiddenParity.SCCRegion.computed_losing_excludes_common_policy
#check @HiddenParity.SCCRegion.Controls.losing_child_rejects_parent
#print axioms HiddenParity.SCCRegion.Controls.losing_child_rejects_parent
#check @HiddenParity.SCCRegion.Controls.revealed_even_child_wins
#print axioms HiddenParity.SCCRegion.Controls.revealed_even_child_wins
#check @HiddenParity.SCCRegion.Controls.revealed_odd_child_loses
#print axioms HiddenParity.SCCRegion.Controls.revealed_odd_child_loses
#check @HiddenParity.SCCRegion.Controls.dead_successor_rejected
#print axioms HiddenParity.SCCRegion.Controls.dead_successor_rejected
#check @HiddenParity.SCCRegion.Controls.empty_support_rejected
#print axioms HiddenParity.SCCRegion.Controls.empty_support_rejected
#check @HiddenParity.SCCRegion.Controls.higher_odd_recurs_and_wins
#print axioms HiddenParity.SCCRegion.Controls.higher_odd_recurs_and_wins
#check @HiddenParity.SCCRegion.Controls.lower_odd_recurs_and_loses
#print axioms HiddenParity.SCCRegion.Controls.lower_odd_recurs_and_loses
#check @HiddenParity.SCCRegion.Controls.excess_fuel_same_output
#print axioms HiddenParity.SCCRegion.Controls.excess_fuel_same_output
#check @HiddenParity.SCCRegion.Controls.no_common_policy_at_bad_branch
#print axioms HiddenParity.SCCRegion.Controls.no_common_policy_at_bad_branch
#check @HiddenParity.SCCRegion.ExtraControls.S
#print axioms HiddenParity.SCCRegion.ExtraControls.S
#check @HiddenParity.SCCRegion.ExtraControls.A
#print axioms HiddenParity.SCCRegion.ExtraControls.A
#check @HiddenParity.SCCRegion.ExtraControls.M
#print axioms HiddenParity.SCCRegion.ExtraControls.M
#check @HiddenParity.SCCRegion.ExtraControls.kernel
#print axioms HiddenParity.SCCRegion.ExtraControls.kernel
#check @HiddenParity.SCCRegion.ExtraControls.menu
#print axioms HiddenParity.SCCRegion.ExtraControls.menu
#check @HiddenParity.SCCRegion.ExtraControls.opposite
#print axioms HiddenParity.SCCRegion.ExtraControls.opposite
#check @HiddenParity.SCCRegion.ExtraControls.sharedEven
#print axioms HiddenParity.SCCRegion.ExtraControls.sharedEven
#check @HiddenParity.SCCRegion.ExtraControls.incompatible_rival_minima_reject
#print axioms HiddenParity.SCCRegion.ExtraControls.incompatible_rival_minima_reject
#check @HiddenParity.SCCRegion.ExtraControls.shared_even_action_retained
#print axioms HiddenParity.SCCRegion.ExtraControls.shared_even_action_retained
#check @HiddenParity.SCCRegion.ExtraControls.stage_prunes_odd_but_keeps_even
#print axioms HiddenParity.SCCRegion.ExtraControls.stage_prunes_odd_but_keeps_even
