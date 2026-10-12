import MomentRecovery
import Counterexample
import Checks

-- Explicit foundation audit for every local named definition and theorem.
#print axioms FiniteMoment.moment
#print axioms FiniteMoment.record
#print axioms FiniteMoment.recoveryCoefficient
#print axioms FiniteMoment.recover
#print axioms FiniteMoment.determinant_ne_zero
#print axioms FiniteMoment.record_eq_vecMul
#print axioms FiniteMoment.recover_eq_vecMul
#print axioms FiniteMoment.recover_record
#print axioms FiniteMoment.record_recover
#print axioms FiniteMoment.recordLinearEquiv
#print axioms FiniteMoment.weight_eq_sum_moments
#print axioms FiniteMoment.weights_eq_of_moments_eq
#print axioms FiniteMoment.record_injective
#print axioms FiniteMoment.all_moments_eq_of_record_eq
#print axioms FiniteMoment.observable_reconstruction
#print axioms FiniteMoment.higher_moment_reconstruction
#print axioms FiniteMoment.vector_observable_reconstruction
#print axioms FiniteMomentRecovery.FourPoint.x
#print axioms FiniteMomentRecovery.FourPoint.wPlus
#print axioms FiniteMomentRecovery.FourPoint.wMinus
#print axioms FiniteMomentRecovery.FourPoint.moment
#print axioms FiniteMomentRecovery.FourPoint.law
#print axioms FiniteMomentRecovery.FourPoint.support_pairwise_distinct
#print axioms FiniteMomentRecovery.FourPoint.support_in_unit_interval
#print axioms FiniteMomentRecovery.FourPoint.wPlus_positive
#print axioms FiniteMomentRecovery.FourPoint.wMinus_positive
#print axioms FiniteMomentRecovery.FourPoint.wPlus_total
#print axioms FiniteMomentRecovery.FourPoint.wMinus_total
#print axioms FiniteMomentRecovery.FourPoint.moment_zero_plus
#print axioms FiniteMomentRecovery.FourPoint.moment_one_plus
#print axioms FiniteMomentRecovery.FourPoint.moment_two_plus
#print axioms FiniteMomentRecovery.FourPoint.moments_zero_one_two
#print axioms FiniteMomentRecovery.FourPoint.moments_agree_through_two
#print axioms FiniteMomentRecovery.FourPoint.moment_three_plus
#print axioms FiniteMomentRecovery.FourPoint.moment_three_minus
#print axioms FiniteMomentRecovery.FourPoint.third_moment_difference
#print axioms FiniteMomentRecovery.FourPoint.third_moments_differ
#print axioms FiniteMomentRecovery.FourPoint.weights_differ
#print axioms FiniteMomentRecovery.FourPoint.law_at_support
#print axioms FiniteMomentRecovery.FourPoint.law_plus_at_zero
#print axioms FiniteMomentRecovery.FourPoint.law_minus_at_zero
#print axioms FiniteMomentRecovery.FourPoint.laws_differ
#print axioms FiniteMomentRecovery.FourPoint.positive_probability_counterexample
