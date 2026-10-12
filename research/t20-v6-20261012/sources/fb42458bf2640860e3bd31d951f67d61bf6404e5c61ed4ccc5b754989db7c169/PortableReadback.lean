import GenericFiniteQueryLocality
import GenericFiniteQueryMeasure
import GenericQueryReference
import PolicyRowEvaluator
import PolicyTranscriptFiber
import PolicyRowLaw
set_option pp.universes true
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
#check @Orthemology.Tranche2.FiniteAlphabetQuery.prefixSymbols_singleton_preimage
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.prefixSymbols_singleton_preimage
#check @Orthemology.Tranche2.FiniteAlphabetQuery.iidOracle_prefix_nonzero
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.iidOracle_prefix_nonzero
#check @Orthemology.Tranche2.FiniteAlphabetQuery.finite_query_domination_by_iid_rival
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.finite_query_domination_by_iid_rival
#check @Orthemology.Tranche2.FiniteAlphabetQuery.positive_finite_query_event_transfers
#print axioms Orthemology.Tranche2.FiniteAlphabetQuery.positive_finite_query_event_transfers
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
#check @Orthemology.Tranche2.PolicyEmbedding.rowMeasure_full_support
#print axioms Orthemology.Tranche2.PolicyEmbedding.rowMeasure_full_support
#check @Orthemology.Tranche2.PolicyEmbedding.rowMeasure_coordinate
#print axioms Orthemology.Tranche2.PolicyEmbedding.rowMeasure_coordinate
#check @Orthemology.Tranche2.PolicyEmbedding.rowOracle_finite_prefix_positive
#print axioms Orthemology.Tranche2.PolicyEmbedding.rowOracle_finite_prefix_positive
