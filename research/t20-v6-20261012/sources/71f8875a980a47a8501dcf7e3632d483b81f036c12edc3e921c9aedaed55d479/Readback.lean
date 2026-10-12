import ContinuumAuditRestoration
import RepairEndpointCells
import EmpiricalRepairCost
import EmpiricalFourthMoment
import EmpiricalExpectedCost
set_option pp.universes true
set_option pp.explicit true
#check Orthemology.Tranche3.empiricalWeight
#print Orthemology.Tranche3.empiricalWeight
#print axioms Orthemology.Tranche3.empiricalWeight
#check Orthemology.Tranche3.empiricalRepair
#print Orthemology.Tranche3.empiricalRepair
#print axioms Orthemology.Tranche3.empiricalRepair
#check Orthemology.Tranche3.bitValue
#print Orthemology.Tranche3.bitValue
#print axioms Orthemology.Tranche3.bitValue
#check Orthemology.Tranche3.count_prefix_real
#print Orthemology.Tranche3.count_prefix_real
#print axioms Orthemology.Tranche3.count_prefix_real
#check Orthemology.Tranche3.empiricalWeight_mem
#print Orthemology.Tranche3.empiricalWeight_mem
#print axioms Orthemology.Tranche3.empiricalWeight_mem
#check Orthemology.Tranche3.empiricalRepair_coherent
#print Orthemology.Tranche3.empiricalRepair_coherent
#print axioms Orthemology.Tranche3.empiricalRepair_coherent
#check Orthemology.Tranche3.source_bit_expectation
#print Orthemology.Tranche3.source_bit_expectation
#print axioms Orthemology.Tranche3.source_bit_expectation
#check Orthemology.Tranche3.empiricalWeight_converges
#print Orthemology.Tranche3.empiricalWeight_converges
#print axioms Orthemology.Tranche3.empiricalWeight_converges
#check Orthemology.Tranche3.interior_empirical_strict_restoration
#print Orthemology.Tranche3.interior_empirical_strict_restoration
#print axioms Orthemology.Tranche3.interior_empirical_strict_restoration
#check Orthemology.Tranche3.LiteralRepairGood
#print Orthemology.Tranche3.LiteralRepairGood
#print axioms Orthemology.Tranche3.LiteralRepairGood
#check Orthemology.Tranche3.positive_weight_punctured_cell
#print Orthemology.Tranche3.positive_weight_punctured_cell
#print axioms Orthemology.Tranche3.positive_weight_punctured_cell
#check Orthemology.Tranche3.zero_weight_unique
#print Orthemology.Tranche3.zero_weight_unique
#print axioms Orthemology.Tranche3.zero_weight_unique
#check Orthemology.Tranche3.one_weight_unique
#print Orthemology.Tranche3.one_weight_unique
#print axioms Orthemology.Tranche3.one_weight_unique
#check Orthemology.Tranche3.below_one_punctured_cell
#print Orthemology.Tranche3.below_one_punctured_cell
#print axioms Orthemology.Tranche3.below_one_punctured_cell
#check Orthemology.Tranche3.constantBits
#print Orthemology.Tranche3.constantBits
#print axioms Orthemology.Tranche3.constantBits
#check Orthemology.Tranche3.constantBits_count
#print Orthemology.Tranche3.constantBits_count
#print axioms Orthemology.Tranche3.constantBits_count
#check Orthemology.Tranche3.constantBits_mass
#print Orthemology.Tranche3.constantBits_mass
#print axioms Orthemology.Tranche3.constantBits_mass
#check Orthemology.Tranche3.empiricalRepair_constant
#print Orthemology.Tranche3.empiricalRepair_constant
#print axioms Orthemology.Tranche3.empiricalRepair_constant
#check Orthemology.Tranche3.EmpiricalFailure
#print Orthemology.Tranche3.EmpiricalFailure
#print axioms Orthemology.Tranche3.EmpiricalFailure
#check Orthemology.Tranche3.empiricalFailure_measurable
#print Orthemology.Tranche3.empiricalFailure_measurable
#print axioms Orthemology.Tranche3.empiricalFailure_measurable
#check Orthemology.Tranche3.constant_prefix_failure
#print Orthemology.Tranche3.constant_prefix_failure
#print axioms Orthemology.Tranche3.constant_prefix_failure
#check Orthemology.Tranche3.constant_prefix_probability
#print Orthemology.Tranche3.constant_prefix_probability
#print axioms Orthemology.Tranche3.constant_prefix_probability
#check Orthemology.Tranche3.empirical_failure_probability_lower
#print Orthemology.Tranche3.empirical_failure_probability_lower
#print axioms Orthemology.Tranche3.empirical_failure_probability_lower
#check Orthemology.Tranche3.empirical_expected_failure_lower
#print Orthemology.Tranche3.empirical_expected_failure_lower
#print axioms Orthemology.Tranche3.empirical_expected_failure_lower
#check Orthemology.Tranche3.centeredTotal
#print Orthemology.Tranche3.centeredTotal
#print axioms Orthemology.Tranche3.centeredTotal
#check Orthemology.Tranche3.centeredMoment
#print Orthemology.Tranche3.centeredMoment
#print axioms Orthemology.Tranche3.centeredMoment
#check Orthemology.Tranche3.expectation_add
#print Orthemology.Tranche3.expectation_add
#print axioms Orthemology.Tranche3.expectation_add
#check Orthemology.Tranche3.expectation_mul
#print Orthemology.Tranche3.expectation_mul
#print axioms Orthemology.Tranche3.expectation_mul
#check Orthemology.Tranche3.expectation_const
#print Orthemology.Tranche3.expectation_const
#print axioms Orthemology.Tranche3.expectation_const
#check Orthemology.Tranche3.centeredTotal_step
#print Orthemology.Tranche3.centeredTotal_step
#print axioms Orthemology.Tranche3.centeredTotal_step
#check Orthemology.Tranche3.centeredMoment_step
#print Orthemology.Tranche3.centeredMoment_step
#print axioms Orthemology.Tranche3.centeredMoment_step
#check Orthemology.Tranche3.centeredMoment_one_step
#print Orthemology.Tranche3.centeredMoment_one_step
#print axioms Orthemology.Tranche3.centeredMoment_one_step
#check Orthemology.Tranche3.centeredMoment_two_step
#print Orthemology.Tranche3.centeredMoment_two_step
#print axioms Orthemology.Tranche3.centeredMoment_two_step
#check Orthemology.Tranche3.centeredMoment_four_step
#print Orthemology.Tranche3.centeredMoment_four_step
#print axioms Orthemology.Tranche3.centeredMoment_four_step
#check Orthemology.Tranche3.centered_moments
#print Orthemology.Tranche3.centered_moments
#print axioms Orthemology.Tranche3.centered_moments
#check Orthemology.Tranche3.centered_fourth_le
#print Orthemology.Tranche3.centered_fourth_le
#print axioms Orthemology.Tranche3.centered_fourth_le
#check Orthemology.Tranche3.repairRadius
#print Orthemology.Tranche3.repairRadius
#print axioms Orthemology.Tranche3.repairRadius
#check Orthemology.Tranche3.empirical_good_of_error
#print Orthemology.Tranche3.empirical_good_of_error
#print axioms Orthemology.Tranche3.empirical_good_of_error
#check Orthemology.Tranche3.empirical_centered_identity
#print Orthemology.Tranche3.empirical_centered_identity
#print axioms Orthemology.Tranche3.empirical_centered_identity
#check Orthemology.Tranche3.empirical_bad_fourth
#print Orthemology.Tranche3.empirical_bad_fourth
#print axioms Orthemology.Tranche3.empirical_bad_fourth
#check Orthemology.Tranche3.empirical_failure_probability_upper
#print Orthemology.Tranche3.empirical_failure_probability_upper
#print axioms Orthemology.Tranche3.empirical_failure_probability_upper
#check Orthemology.Tranche3.empirical_probability_spending
#print Orthemology.Tranche3.empirical_probability_spending
#print axioms Orthemology.Tranche3.empirical_probability_spending
#check Orthemology.Tranche3.empirical_expected_failure_upper
#print Orthemology.Tranche3.empirical_expected_failure_upper
#print axioms Orthemology.Tranche3.empirical_expected_failure_upper
