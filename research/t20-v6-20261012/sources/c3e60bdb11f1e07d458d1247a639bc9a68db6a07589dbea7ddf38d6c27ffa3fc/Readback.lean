import StatisticalRepair
import RobustBinaryRepair
import CertifiedRepairCoverage
import RationalRepairCertificate
import RandomisedRepairRegret
import FiniteTailCoverage
import BernoulliTailMonotonicity
import BernoulliIntervalCoverage
import BernoulliPrefixLaw
import AnytimeRepairCoverage
import RationalTailReference
import ExecutableAuditRepair
import AuditContractBinding
set_option pp.universes true
set_option pp.explicit true
#check Orthemology.Tranche2.affinity
#print Orthemology.Tranche2.affinity
#print axioms Orthemology.Tranche2.affinity
#check Orthemology.Tranche2.errorP
#print Orthemology.Tranche2.errorP
#print axioms Orthemology.Tranche2.errorP
#check Orthemology.Tranche2.errorQ
#print Orthemology.Tranche2.errorQ
#print axioms Orthemology.Tranche2.errorQ
#check Orthemology.Tranche2.minimum_le_test_error
#print Orthemology.Tranche2.minimum_le_test_error
#print axioms Orthemology.Tranche2.minimum_le_test_error
#check Orthemology.Tranche2.sqrt_product_min_max
#print Orthemology.Tranche2.sqrt_product_min_max
#print axioms Orthemology.Tranche2.sqrt_product_min_max
#check Orthemology.Tranche2.affinity_sq_le_twice_error_sum
#print Orthemology.Tranche2.affinity_sq_le_twice_error_sum
#print axioms Orthemology.Tranche2.affinity_sq_le_twice_error_sum
#check Orthemology.Tranche2.affinity_error_lower_bound
#print Orthemology.Tranche2.affinity_error_lower_bound
#print axioms Orthemology.Tranche2.affinity_error_lower_bound
#check Orthemology.Tranche2.affinity_nonneg
#print Orthemology.Tranche2.affinity_nonneg
#print axioms Orthemology.Tranche2.affinity_nonneg
#check Orthemology.Tranche2.affinity_tensor
#print Orthemology.Tranche2.affinity_tensor
#print axioms Orthemology.Tranche2.affinity_tensor
#check Orthemology.Tranche2.Bits
#print Orthemology.Tranche2.Bits
#print axioms Orthemology.Tranche2.Bits
#check Orthemology.Tranche2.bitsFintype
#print Orthemology.Tranche2.bitsFintype
#print axioms Orthemology.Tranche2.bitsFintype
#check Orthemology.Tranche2.coinMass
#print Orthemology.Tranche2.coinMass
#print axioms Orthemology.Tranche2.coinMass
#check Orthemology.Tranche2.bernoulliMass
#print Orthemology.Tranche2.bernoulliMass
#print axioms Orthemology.Tranche2.bernoulliMass
#check Orthemology.Tranche2.coinMass_nonneg
#print Orthemology.Tranche2.coinMass_nonneg
#print axioms Orthemology.Tranche2.coinMass_nonneg
#check Orthemology.Tranche2.bernoulliMass_nonneg
#print Orthemology.Tranche2.bernoulliMass_nonneg
#print axioms Orthemology.Tranche2.bernoulliMass_nonneg
#check Orthemology.Tranche2.bernoulliMass_sum
#print Orthemology.Tranche2.bernoulliMass_sum
#print axioms Orthemology.Tranche2.bernoulliMass_sum
#check Orthemology.Tranche2.coin_affinity
#print Orthemology.Tranche2.coin_affinity
#print axioms Orthemology.Tranche2.coin_affinity
#check Orthemology.Tranche2.bernoulli_affinity
#print Orthemology.Tranche2.bernoulli_affinity
#print axioms Orthemology.Tranche2.bernoulli_affinity
#check Orthemology.Tranche2.symmetric_coin_affinity_sq
#print Orthemology.Tranche2.symmetric_coin_affinity_sq
#print axioms Orthemology.Tranche2.symmetric_coin_affinity_sq
#check Orthemology.Tranche2.symmetric_bernoulli_test_lower_bound
#print Orthemology.Tranche2.symmetric_bernoulli_test_lower_bound
#print axioms Orthemology.Tranche2.symmetric_bernoulli_test_lower_bound
#check Orthemology.Tranche3.excessZero
#print Orthemology.Tranche3.excessZero
#print axioms Orthemology.Tranche3.excessZero
#check Orthemology.Tranche3.excessOne
#print Orthemology.Tranche3.excessOne
#print axioms Orthemology.Tranche3.excessOne
#check Orthemology.Tranche3.RobustGood
#print Orthemology.Tranche3.RobustGood
#print axioms Orthemology.Tranche3.RobustGood
#check Orthemology.Tranche3.robustReport
#print Orthemology.Tranche3.robustReport
#print axioms Orthemology.Tranche3.robustReport
#check Orthemology.Tranche3.robustValue
#print Orthemology.Tranche3.robustValue
#print axioms Orthemology.Tranche3.robustValue
#check Orthemology.Tranche3.excessZero_expand
#print Orthemology.Tranche3.excessZero_expand
#print axioms Orthemology.Tranche3.excessZero_expand
#check Orthemology.Tranche3.excessOne_expand
#print Orthemology.Tranche3.excessOne_expand
#print axioms Orthemology.Tranche3.excessOne_expand
#check Orthemology.Tranche3.robustGood_iff_endpoints
#print Orthemology.Tranche3.robustGood_iff_endpoints
#print axioms Orthemology.Tranche3.robustGood_iff_endpoints
#check Orthemology.Tranche3.robustReport_mem
#print Orthemology.Tranche3.robustReport_mem
#print axioms Orthemology.Tranche3.robustReport_mem
#check Orthemology.Tranche3.robust_crossing
#print Orthemology.Tranche3.robust_crossing
#print axioms Orthemology.Tranche3.robust_crossing
#check Orthemology.Tranche3.robustValue_le_max
#print Orthemology.Tranche3.robustValue_le_max
#print axioms Orthemology.Tranche3.robustValue_le_max
#check Orthemology.Tranche3.robust_repair_exists_iff
#print Orthemology.Tranche3.robust_repair_exists_iff
#print axioms Orthemology.Tranche3.robust_repair_exists_iff
#check Orthemology.Tranche3.robustValue_polynomial
#print Orthemology.Tranche3.robustValue_polynomial
#print axioms Orthemology.Tranche3.robustValue_polynomial
#check Orthemology.Tranche3.robustReport_unique
#print Orthemology.Tranche3.robustReport_unique
#print axioms Orthemology.Tranche3.robustReport_unique
#check Orthemology.Tranche3.covered_certificate_sound
#print Orthemology.Tranche3.covered_certificate_sound
#print axioms Orthemology.Tranche3.covered_certificate_sound
#check Orthemology.Tranche3.width_sufficient
#print Orthemology.Tranche3.width_sufficient
#print axioms Orthemology.Tranche3.width_sufficient
#check Orthemology.Tranche3.robustValue_lower_width
#print Orthemology.Tranche3.robustValue_lower_width
#print axioms Orthemology.Tranche3.robustValue_lower_width
#check Orthemology.Tranche3.width_necessary
#print Orthemology.Tranche3.width_necessary
#print axioms Orthemology.Tranche3.width_necessary
#check Orthemology.Tranche3.IntervalCoverage
#print Orthemology.Tranche3.IntervalCoverage
#print axioms Orthemology.Tranche3.IntervalCoverage
#check Orthemology.Tranche3.AllCertificatesSound
#print Orthemology.Tranche3.AllCertificatesSound
#print axioms Orthemology.Tranche3.AllCertificatesSound
#check Orthemology.Tranche3.coverage_subset_sound
#print Orthemology.Tranche3.coverage_subset_sound
#print axioms Orthemology.Tranche3.coverage_subset_sound
#check Orthemology.Tranche3.certificate_failure_measure_le
#print Orthemology.Tranche3.certificate_failure_measure_le
#print axioms Orthemology.Tranche3.certificate_failure_measure_le
#check Orthemology.Tranche3.rationalReport
#print Orthemology.Tranche3.rationalReport
#print axioms Orthemology.Tranche3.rationalReport
#check Orthemology.Tranche3.rationalValue
#print Orthemology.Tranche3.rationalValue
#print axioms Orthemology.Tranche3.rationalValue
#check Orthemology.Tranche3.RationalValid
#print Orthemology.Tranche3.RationalValid
#print axioms Orthemology.Tranche3.RationalValid
#check Orthemology.Tranche3.rationalCertificate
#print Orthemology.Tranche3.rationalCertificate
#print axioms Orthemology.Tranche3.rationalCertificate
#check Orthemology.Tranche3.rationalReport_cast
#print Orthemology.Tranche3.rationalReport_cast
#print axioms Orthemology.Tranche3.rationalReport_cast
#check Orthemology.Tranche3.rationalValue_cast
#print Orthemology.Tranche3.rationalValue_cast
#print axioms Orthemology.Tranche3.rationalValue_cast
#check Orthemology.Tranche3.rationalValid_cast
#print Orthemology.Tranche3.rationalValid_cast
#print axioms Orthemology.Tranche3.rationalValid_cast
#check Orthemology.Tranche3.rationalCertificate_sound
#print Orthemology.Tranche3.rationalCertificate_sound
#print axioms Orthemology.Tranche3.rationalCertificate_sound
#check Orthemology.Tranche3.rationalCertificate_reject_iff
#print Orthemology.Tranche3.rationalCertificate_reject_iff
#print axioms Orthemology.Tranche3.rationalCertificate_reject_iff
#check Orthemology.Tranche3.reportMean
#print Orthemology.Tranche3.reportMean
#print axioms Orthemology.Tranche3.reportMean
#check Orthemology.Tranche3.reportVariance
#print Orthemology.Tranche3.reportVariance
#print axioms Orthemology.Tranche3.reportVariance
#check Orthemology.Tranche3.reportMean_mem
#print Orthemology.Tranche3.reportMean_mem
#print axioms Orthemology.Tranche3.reportMean_mem
#check Orthemology.Tranche3.reportVariance_nonneg
#print Orthemology.Tranche3.reportVariance_nonneg
#print axioms Orthemology.Tranche3.reportVariance_nonneg
#check Orthemology.Tranche3.reportVariance_identity
#print Orthemology.Tranche3.reportVariance_identity
#print axioms Orthemology.Tranche3.reportVariance_identity
#check Orthemology.Tranche3.expected_excess_decomposition
#print Orthemology.Tranche3.expected_excess_decomposition
#print axioms Orthemology.Tranche3.expected_excess_decomposition
#check Orthemology.Tranche3.randomised_regret_lower_bound
#print Orthemology.Tranche3.randomised_regret_lower_bound
#print axioms Orthemology.Tranche3.randomised_regret_lower_bound
#check Orthemology.Tranche3.upperTail
#print Orthemology.Tranche3.upperTail
#print axioms Orthemology.Tranche3.upperTail
#check Orthemology.Tranche3.lowerTail
#print Orthemology.Tranche3.lowerTail
#print axioms Orthemology.Tranche3.lowerTail
#check Orthemology.Tranche3.upperTail_superuniform
#print Orthemology.Tranche3.upperTail_superuniform
#print axioms Orthemology.Tranche3.upperTail_superuniform
#check Orthemology.Tranche3.lowerTail_superuniform
#print Orthemology.Tranche3.lowerTail_superuniform
#print axioms Orthemology.Tranche3.lowerTail_superuniform
#check Orthemology.Tranche3.tail_inversion_coverage
#print Orthemology.Tranche3.tail_inversion_coverage
#print axioms Orthemology.Tranche3.tail_inversion_coverage
#check Orthemology.Tranche3.BitsLE
#print Orthemology.Tranche3.BitsLE
#print axioms Orthemology.Tranche3.BitsLE
#check Orthemology.Tranche3.bitsLE_refl
#print Orthemology.Tranche3.bitsLE_refl
#print axioms Orthemology.Tranche3.bitsLE_refl
#check Orthemology.Tranche3.countOnes
#print Orthemology.Tranche3.countOnes
#print axioms Orthemology.Tranche3.countOnes
#check Orthemology.Tranche3.countOnes_mono
#print Orthemology.Tranche3.countOnes_mono
#print axioms Orthemology.Tranche3.countOnes_mono
#check Orthemology.Tranche3.coinExpectation
#print Orthemology.Tranche3.coinExpectation
#print axioms Orthemology.Tranche3.coinExpectation
#check Orthemology.Tranche3.coinExpectation_step
#print Orthemology.Tranche3.coinExpectation_step
#print axioms Orthemology.Tranche3.coinExpectation_step
#check Orthemology.Tranche3.coinExpectation_mono_parameter
#print Orthemology.Tranche3.coinExpectation_mono_parameter
#print axioms Orthemology.Tranche3.coinExpectation_mono_parameter
#check Orthemology.Tranche3.bernoulliUpper
#print Orthemology.Tranche3.bernoulliUpper
#print axioms Orthemology.Tranche3.bernoulliUpper
#check Orthemology.Tranche3.bernoulliLower
#print Orthemology.Tranche3.bernoulliLower
#print axioms Orthemology.Tranche3.bernoulliLower
#check Orthemology.Tranche3.bernoulliUpper_mono
#print Orthemology.Tranche3.bernoulliUpper_mono
#print axioms Orthemology.Tranche3.bernoulliUpper_mono
#check Orthemology.Tranche3.bernoulliLower_antitone
#print Orthemology.Tranche3.bernoulliLower_antitone
#print axioms Orthemology.Tranche3.bernoulliLower_antitone
#check Orthemology.Tranche3.bernoulliUpper_as_tail
#print Orthemology.Tranche3.bernoulliUpper_as_tail
#print axioms Orthemology.Tranche3.bernoulliUpper_as_tail
#check Orthemology.Tranche3.bernoulliLower_as_tail
#print Orthemology.Tranche3.bernoulliLower_as_tail
#print axioms Orthemology.Tranche3.bernoulliLower_as_tail
#check Orthemology.Tranche3.TailBracket
#print Orthemology.Tranche3.TailBracket
#print axioms Orthemology.Tranche3.TailBracket
#check Orthemology.Tranche3.bernoulli_interval_coverage
#print Orthemology.Tranche3.bernoulli_interval_coverage
#print axioms Orthemology.Tranche3.bernoulli_interval_coverage
#check Orthemology.Tranche3.bitsMeasurableSpace
#print Orthemology.Tranche3.bitsMeasurableSpace
#print axioms Orthemology.Tranche3.bitsMeasurableSpace
#check Orthemology.Tranche3.bitsMeasurableSingletonClass
#print Orthemology.Tranche3.bitsMeasurableSingletonClass
#print axioms Orthemology.Tranche3.bitsMeasurableSingletonClass
#check Orthemology.Tranche3.observedPrefix
#print Orthemology.Tranche3.observedPrefix
#print axioms Orthemology.Tranche3.observedPrefix
#check Orthemology.Tranche3.observedPrefix_measurable
#print Orthemology.Tranche3.observedPrefix_measurable
#print axioms Orthemology.Tranche3.observedPrefix_measurable
#check Orthemology.Tranche3.prefixDecoder
#print Orthemology.Tranche3.prefixDecoder
#print axioms Orthemology.Tranche3.prefixDecoder
#check Orthemology.Tranche3.observedPrefix_eq_iff
#print Orthemology.Tranche3.observedPrefix_eq_iff
#print axioms Orthemology.Tranche3.observedPrefix_eq_iff
#check Orthemology.Tranche3.observedPrefix_singleton_preimage
#print Orthemology.Tranche3.observedPrefix_singleton_preimage
#print axioms Orthemology.Tranche3.observedPrefix_singleton_preimage
#check Orthemology.Tranche3.sourceCoin
#print Orthemology.Tranche3.sourceCoin
#print axioms Orthemology.Tranche3.sourceCoin
#check Orthemology.Tranche3.sourceCoinMeasure
#print Orthemology.Tranche3.sourceCoinMeasure
#print axioms Orthemology.Tranche3.sourceCoinMeasure
#check Orthemology.Tranche3.sourceCoin_probability
#print Orthemology.Tranche3.sourceCoin_probability
#print axioms Orthemology.Tranche3.sourceCoin_probability
#check Orthemology.Tranche3.auditSourceLaw
#print Orthemology.Tranche3.auditSourceLaw
#print axioms Orthemology.Tranche3.auditSourceLaw
#check Orthemology.Tranche3.auditSource_probability
#print Orthemology.Tranche3.auditSource_probability
#print axioms Orthemology.Tranche3.auditSource_probability
#check Orthemology.Tranche3.sourceCoin_singleton
#print Orthemology.Tranche3.sourceCoin_singleton
#print axioms Orthemology.Tranche3.sourceCoin_singleton
#check Orthemology.Tranche3.decoder_product
#print Orthemology.Tranche3.decoder_product
#print axioms Orthemology.Tranche3.decoder_product
#check Orthemology.Tranche3.auditSource_prefix_mass
#print Orthemology.Tranche3.auditSource_prefix_mass
#print axioms Orthemology.Tranche3.auditSource_prefix_mass
#check Orthemology.Tranche3.auditSource_word_event
#print Orthemology.Tranche3.auditSource_word_event
#print axioms Orthemology.Tranche3.auditSource_word_event
#check Orthemology.Tranche3.auditSource_interval_failure
#print Orthemology.Tranche3.auditSource_interval_failure
#print axioms Orthemology.Tranche3.auditSource_interval_failure
#check Orthemology.Tranche3.tailSpending
#print Orthemology.Tranche3.tailSpending
#print axioms Orthemology.Tranche3.tailSpending
#check Orthemology.Tranche3.tailSpending_nonneg
#print Orthemology.Tranche3.tailSpending_nonneg
#print axioms Orthemology.Tranche3.tailSpending_nonneg
#check Orthemology.Tranche3.double_tailSpending
#print Orthemology.Tranche3.double_tailSpending
#print axioms Orthemology.Tranche3.double_tailSpending
#check Orthemology.Tranche3.spending_partial_sum
#print Orthemology.Tranche3.spending_partial_sum
#print axioms Orthemology.Tranche3.spending_partial_sum
#check Orthemology.Tranche3.spending_total_le
#print Orthemology.Tranche3.spending_total_le
#print axioms Orthemology.Tranche3.spending_total_le
#check Orthemology.Tranche3.auditSource_anytime_coverage
#print Orthemology.Tranche3.auditSource_anytime_coverage
#print axioms Orthemology.Tranche3.auditSource_anytime_coverage
#check Orthemology.Tranche3.auditSource_all_certificates_sound
#print Orthemology.Tranche3.auditSource_all_certificates_sound
#print axioms Orthemology.Tranche3.auditSource_all_certificates_sound
#check Orthemology.Tranche3.rationalMass
#print Orthemology.Tranche3.rationalMass
#print axioms Orthemology.Tranche3.rationalMass
#check Orthemology.Tranche3.rationalCount
#print Orthemology.Tranche3.rationalCount
#print axioms Orthemology.Tranche3.rationalCount
#check Orthemology.Tranche3.rationalCount_eq
#print Orthemology.Tranche3.rationalCount_eq
#print axioms Orthemology.Tranche3.rationalCount_eq
#check Orthemology.Tranche3.rationalUpper
#print Orthemology.Tranche3.rationalUpper
#print axioms Orthemology.Tranche3.rationalUpper
#check Orthemology.Tranche3.rationalLower
#print Orthemology.Tranche3.rationalLower
#print axioms Orthemology.Tranche3.rationalLower
#check Orthemology.Tranche3.rationalMass_cast
#print Orthemology.Tranche3.rationalMass_cast
#print axioms Orthemology.Tranche3.rationalMass_cast
#check Orthemology.Tranche3.rationalUpper_cast
#print Orthemology.Tranche3.rationalUpper_cast
#print axioms Orthemology.Tranche3.rationalUpper_cast
#check Orthemology.Tranche3.rationalLower_cast
#print Orthemology.Tranche3.rationalLower_cast
#print axioms Orthemology.Tranche3.rationalLower_cast
#check Orthemology.Tranche3.lowerBisect
#print Orthemology.Tranche3.lowerBisect
#print axioms Orthemology.Tranche3.lowerBisect
#check Orthemology.Tranche3.upperBisect
#print Orthemology.Tranche3.upperBisect
#print axioms Orthemology.Tranche3.upperBisect
#check Orthemology.Tranche3.lowerBisect_invariant
#print Orthemology.Tranche3.lowerBisect_invariant
#print axioms Orthemology.Tranche3.lowerBisect_invariant
#check Orthemology.Tranche3.upperBisect_invariant
#print Orthemology.Tranche3.upperBisect_invariant
#print axioms Orthemology.Tranche3.upperBisect_invariant
#check Orthemology.Tranche3.rationalCount_le
#print Orthemology.Tranche3.rationalCount_le
#print axioms Orthemology.Tranche3.rationalCount_le
#check Orthemology.Tranche3.rationalMass_zero_of_count_pos
#print Orthemology.Tranche3.rationalMass_zero_of_count_pos
#print axioms Orthemology.Tranche3.rationalMass_zero_of_count_pos
#check Orthemology.Tranche3.rationalMass_one_of_count_lt
#print Orthemology.Tranche3.rationalMass_one_of_count_lt
#print axioms Orthemology.Tranche3.rationalMass_one_of_count_lt
#check Orthemology.Tranche3.rationalUpper_zero
#print Orthemology.Tranche3.rationalUpper_zero
#print axioms Orthemology.Tranche3.rationalUpper_zero
#check Orthemology.Tranche3.rationalLower_one
#print Orthemology.Tranche3.rationalLower_one
#print axioms Orthemology.Tranche3.rationalLower_one
#check Orthemology.Tranche3.referenceLower
#print Orthemology.Tranche3.referenceLower
#print axioms Orthemology.Tranche3.referenceLower
#check Orthemology.Tranche3.referenceUpper
#print Orthemology.Tranche3.referenceUpper
#print axioms Orthemology.Tranche3.referenceUpper
#check Orthemology.Tranche3.referenceLower_check
#print Orthemology.Tranche3.referenceLower_check
#print axioms Orthemology.Tranche3.referenceLower_check
#check Orthemology.Tranche3.referenceUpper_check
#print Orthemology.Tranche3.referenceUpper_check
#print axioms Orthemology.Tranche3.referenceUpper_check
#check Orthemology.Tranche3.bernoulli_tails_cover
#print Orthemology.Tranche3.bernoulli_tails_cover
#print axioms Orthemology.Tranche3.bernoulli_tails_cover
#check Orthemology.Tranche3.outer_tail_brackets_ordered
#print Orthemology.Tranche3.outer_tail_brackets_ordered
#print axioms Orthemology.Tranche3.outer_tail_brackets_ordered
#check Orthemology.Tranche3.reference_tailBracket
#print Orthemology.Tranche3.reference_tailBracket
#print axioms Orthemology.Tranche3.reference_tailBracket
#check Orthemology.Tranche3.rationalSpending
#print Orthemology.Tranche3.rationalSpending
#print axioms Orthemology.Tranche3.rationalSpending
#check Orthemology.Tranche3.rationalSpending_cast
#print Orthemology.Tranche3.rationalSpending_cast
#print axioms Orthemology.Tranche3.rationalSpending_cast
#check Orthemology.Tranche3.rationalSpending_bounds
#print Orthemology.Tranche3.rationalSpending_bounds
#print axioms Orthemology.Tranche3.rationalSpending_bounds
#check Orthemology.Tranche3.auditRepair
#print Orthemology.Tranche3.auditRepair
#print axioms Orthemology.Tranche3.auditRepair
#check Orthemology.Tranche3.AuditRepairFailure
#print Orthemology.Tranche3.AuditRepairFailure
#print axioms Orthemology.Tranche3.AuditRepairFailure
#check Orthemology.Tranche3.executable_auditRepair_anytime_sound
#print Orthemology.Tranche3.executable_auditRepair_anytime_sound
#print axioms Orthemology.Tranche3.executable_auditRepair_anytime_sound
#check Orthemology.Tranche3.auditRepairFailure_measurable
#print Orthemology.Tranche3.auditRepairFailure_measurable
#print axioms Orthemology.Tranche3.auditRepairFailure_measurable
#check Orthemology.Tranche3.auditCharge
#print Orthemology.Tranche3.auditCharge
#print axioms Orthemology.Tranche3.auditCharge
#check Orthemology.Tranche3.expectedAuditCharge
#print Orthemology.Tranche3.expectedAuditCharge
#print axioms Orthemology.Tranche3.expectedAuditCharge
#check Orthemology.Tranche3.selector_score_identity
#print Orthemology.Tranche3.selector_score_identity
#print axioms Orthemology.Tranche3.selector_score_identity
#check Orthemology.Tranche3.expectedAuditCharge_coherent
#print Orthemology.Tranche3.expectedAuditCharge_coherent
#print axioms Orthemology.Tranche3.expectedAuditCharge_coherent
#check Orthemology.Tranche3.contract_regret_identity
#print Orthemology.Tranche3.contract_regret_identity
#print axioms Orthemology.Tranche3.contract_regret_identity
#check Orthemology.Tranche3.auditSource_next_joint
#print Orthemology.Tranche3.auditSource_next_joint
#print axioms Orthemology.Tranche3.auditSource_next_joint
#check Orthemology.Tranche3.accepted_contract_score
#print Orthemology.Tranche3.accepted_contract_score
#print axioms Orthemology.Tranche3.accepted_contract_score
#check Orthemology.Tranche3.expected_not_realised_control
#print Orthemology.Tranche3.expected_not_realised_control
#print axioms Orthemology.Tranche3.expected_not_realised_control
