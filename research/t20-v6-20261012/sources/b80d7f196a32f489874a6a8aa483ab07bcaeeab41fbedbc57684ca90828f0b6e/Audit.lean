import PrefixTail
import TaggedRows
import TaggedMass
import Pi3Law
import PrefixBits
import FiniteSelector
import SelectorPrimrec
import PrefixObserver
import PrefixPrimrec
import PrefixControls
set_option pp.universes true
#check @OrthemologyTagged.dropBits_measurable
#print axioms OrthemologyTagged.dropBits_measurable
#check @OrthemologyTagged.prefixSet_measurable
#print axioms OrthemologyTagged.prefixSet_measurable
#check @OrthemologyTagged.finite_tail_prefix_event
#print axioms OrthemologyTagged.finite_tail_prefix_event
#check @OrthemologyTagged.combined_card
#print axioms OrthemologyTagged.combined_card
#check @OrthemologyTagged.restricted_tail_singleton
#print axioms OrthemologyTagged.restricted_tail_singleton
#check @OrthemologyTagged.fair_restrict_singleton
#print axioms OrthemologyTagged.fair_restrict_singleton
#check @OrthemologyTagged.restricted_tail_law
#print axioms OrthemologyTagged.restricted_tail_law
#check @OrthemologyTagged.tagEvent_measurable
#print axioms OrthemologyTagged.tagEvent_measurable
#check @OrthemologyTagged.tagEvent_spec
#print axioms OrthemologyTagged.tagEvent_spec
#check @OrthemologyTagged.tag_measurable
#print axioms OrthemologyTagged.tag_measurable
#check @OrthemologyTagged.tail_measurable
#print axioms OrthemologyTagged.tail_measurable
#check @OrthemologyTagged.tail_tag
#print axioms OrthemologyTagged.tail_tag
#check @OrthemologyTagged.tag_injective
#print axioms OrthemologyTagged.tag_injective
#check @OrthemologyTagged.tag_mem
#print axioms OrthemologyTagged.tag_mem
#check @OrthemologyTagged.tagged_on
#print axioms OrthemologyTagged.tagged_on
#check @OrthemologyTagged.tagged_allTrue
#print axioms OrthemologyTagged.tagged_allTrue
#check @OrthemologyTagged.exists_tag_or_allTrue
#print axioms OrthemologyTagged.exists_tag_or_allTrue
#check @OrthemologyTagged.tagEvents_disjoint
#print axioms OrthemologyTagged.tagEvents_disjoint
#check @OrthemologyTagged.tagged_measurable
#print axioms OrthemologyTagged.tagged_measurable
#check @OrthemologyTagged.allTrue_not_tag
#print axioms OrthemologyTagged.allTrue_not_tag
#check @OrthemologyTagged.selector_cover_ae
#print axioms OrthemologyTagged.selector_cover_ae
#check @OrthemologyTagged.fairCantor_sum_restrict
#print axioms OrthemologyTagged.fairCantor_sum_restrict
#check @OrthemologyTagged.tagged_branch_law
#print axioms OrthemologyTagged.tagged_branch_law
#check @OrthemologyTagged.tagged_mixture_law
#print axioms OrthemologyTagged.tagged_mixture_law
#check @OrthemologyTagged.tag_mass
#print axioms OrthemologyTagged.tag_mass
#check @OrthemologyTagged.weights_sum
#print axioms OrthemologyTagged.weights_sum
#check @OrthemologyTagged.weight_ne_zero
#print axioms OrthemologyTagged.weight_ne_zero
#check @OrthemologyTagged.tagged_mass
#print axioms OrthemologyTagged.tagged_mass
#check @OrthemologyTagged.weighted_full_mass_iff
#print axioms OrthemologyTagged.weighted_full_mass_iff
#check @OrthemologyTagged.defect_zero_iff_mass_one
#print axioms OrthemologyTagged.defect_zero_iff_mass_one
#check @OrthemologyTagged.tagged_zero_defect_iff
#print axioms OrthemologyTagged.tagged_zero_defect_iff
#check @OrthemologyTagged.pi3Observer_measurable
#print axioms OrthemologyTagged.pi3Observer_measurable
#check @OrthemologyTagged.pi3_zero_defect_iff
#print axioms OrthemologyTagged.pi3_zero_defect_iff
#check @OrthemologyTagged.pi3_defect_nonnegative
#print axioms OrthemologyTagged.pi3_defect_nonnegative
#check @OrthemologyTagged.pi3_positive_defect_iff
#print axioms OrthemologyTagged.pi3_positive_defect_iff
#check @OrthemologyTagged.sentinel_prefix_bit_value
#print axioms OrthemologyTagged.sentinel_prefix_bit_value
#check @OrthemologyTagged.readBit_prefix
#print axioms OrthemologyTagged.readBit_prefix
#check @OrthemologyTagged.scannedBits_prefix
#print axioms OrthemologyTagged.scannedBits_prefix
#check @OrthemologyTagged.selector_on_tag
#print axioms OrthemologyTagged.selector_on_tag
#check @OrthemologyTagged.selector_before_tag
#print axioms OrthemologyTagged.selector_before_tag
#check @OrthemologyTagged.selector_allTrue
#print axioms OrthemologyTagged.selector_allTrue
#check @OrthemologyTagged.readBit_primrec
#print axioms OrthemologyTagged.readBit_primrec
#check @OrthemologyTagged.scannedBits_eq_map
#print axioms OrthemologyTagged.scannedBits_eq_map
#check @OrthemologyTagged.scannedBits_primrec
#print axioms OrthemologyTagged.scannedBits_primrec
#check @OrthemologyTagged.selector_primrec
#print axioms OrthemologyTagged.selector_primrec
#check @OrthemologyTagged.tag_before
#print axioms OrthemologyTagged.tag_before
#check @OrthemologyTagged.tag_at
#print axioms OrthemologyTagged.tag_at
#check @OrthemologyTagged.tag_after
#print axioms OrthemologyTagged.tag_after
#check @OrthemologyTagged.pi3PrefixValue_output
#print axioms OrthemologyTagged.pi3PrefixValue_output
#check @OrthemologyTagged.finite_prefix_zero_defect_iff
#print axioms OrthemologyTagged.finite_prefix_zero_defect_iff
#check @OrthemologyTagged.pi3PrefixValue_primrec
#print axioms OrthemologyTagged.pi3PrefixValue_primrec
#check @OrthemologyTagged.selector_zero_first
#print axioms OrthemologyTagged.selector_zero_first
#check @OrthemologyTagged.selector_no_zero
#print axioms OrthemologyTagged.selector_no_zero
#check @OrthemologyTagged.selector_middle_zero
#print axioms OrthemologyTagged.selector_middle_zero
#check @OrthemologyTagged.selector_last_zero
#print axioms OrthemologyTagged.selector_last_zero
#check @OrthemologyTagged.good_row_suppresses_bit
#print axioms OrthemologyTagged.good_row_suppresses_bit
#check @OrthemologyTagged.bad_row_copies_bit
#print axioms OrthemologyTagged.bad_row_copies_bit
#check @OrthemologyTagged.true_matrix_zero_defect
#print axioms OrthemologyTagged.true_matrix_zero_defect
#check @OrthemologyTagged.split_matrix_positive_defect
#print axioms OrthemologyTagged.split_matrix_positive_defect
