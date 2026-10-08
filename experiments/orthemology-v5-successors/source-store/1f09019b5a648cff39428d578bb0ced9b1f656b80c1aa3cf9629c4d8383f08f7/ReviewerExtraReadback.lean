import ReviewerCounterchecks
set_option pp.universes true
set_option pp.explicit true
#eval IO.println "EXTRA_BEGIN off_support_zero"
#check @ReviewerCounterchecks.off_support_zero
#print axioms ReviewerCounterchecks.off_support_zero
#eval IO.println "EXTRA_END off_support_zero"
#eval IO.println "EXTRA_BEGIN full_copy_normalization"
#check @ReviewerCounterchecks.full_copy_normalization
#print axioms ReviewerCounterchecks.full_copy_normalization
#eval IO.println "EXTRA_END full_copy_normalization"
#eval IO.println "EXTRA_BEGIN full_copy_tv"
#check @ReviewerCounterchecks.full_copy_tv
#print axioms ReviewerCounterchecks.full_copy_tv
#eval IO.println "EXTRA_END full_copy_tv"
#eval IO.println "EXTRA_BEGIN pushforward_expectation"
#check @ReviewerCounterchecks.pushforward_expectation
#print axioms ReviewerCounterchecks.pushforward_expectation
#eval IO.println "EXTRA_END pushforward_expectation"
#eval IO.println "EXTRA_BEGIN optimal_bounded"
#check @ReviewerCounterchecks.optimal_bounded
#print axioms ReviewerCounterchecks.optimal_bounded
#eval IO.println "EXTRA_END optimal_bounded"
#eval IO.println "EXTRA_BEGIN optimal_attains"
#check @ReviewerCounterchecks.optimal_attains
#print axioms ReviewerCounterchecks.optimal_attains
#eval IO.println "EXTRA_END optimal_attains"
#eval IO.println "EXTRA_BEGIN copied_optimal_attains"
#check @ReviewerCounterchecks.copied_optimal_attains
#print axioms ReviewerCounterchecks.copied_optimal_attains
#eval IO.println "EXTRA_END copied_optimal_attains"
#eval IO.println "EXTRA_BEGIN zero_is_not_injective"
#check @ReviewerCounterchecks.zero_is_not_injective
#print axioms ReviewerCounterchecks.zero_is_not_injective
#eval IO.println "EXTRA_END zero_is_not_injective"
#eval IO.println "EXTRA_BEGIN mask_conditioning_complete"
#check @ReviewerCounterchecks.mask_conditioning_complete
#print axioms ReviewerCounterchecks.mask_conditioning_complete
#eval IO.println "EXTRA_END mask_conditioning_complete"
#eval IO.println "EXTRA_BEGIN not_both_two_thirds"
#check @ReviewerCounterchecks.not_both_two_thirds
#print axioms ReviewerCounterchecks.not_both_two_thirds
#eval IO.println "EXTRA_END not_both_two_thirds"
#eval IO.println "EXTRA_BEGIN missing_upper_bound_counterexample"
#check @ReviewerCounterchecks.missing_upper_bound_counterexample
#print axioms ReviewerCounterchecks.missing_upper_bound_counterexample
#eval IO.println "EXTRA_END missing_upper_bound_counterexample"
#eval IO.println "EXTRA_BEGIN missing_lower_bound_counterexample"
#check @ReviewerCounterchecks.missing_lower_bound_counterexample
#print axioms ReviewerCounterchecks.missing_lower_bound_counterexample
#eval IO.println "EXTRA_END missing_lower_bound_counterexample"
