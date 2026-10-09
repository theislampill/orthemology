# Retained first-run arithmetic obstacle

The first execution of check_multiroot.py stopped at the assertion that the upper endpoint of a 12-term logarithm enclosure was no greater than the exact rational chi-square bound. No assertion from the preceding route-law or rational inequality grid failed.

The code uses powers-of-two range reduction. A logarithm very close to zero can be written as the difference of two log terms near log 2. Twelve retained terms then give an absolute enclosure wider than the extremely small KL-to-chi-square gap in a highly saturated case. An interval that straddles a target inequality is inconclusive, not a counterexample.

The revised control retains the 12-term first attempt and records every parameter tuple for which it needs a 32-term refinement. The final report must be read for the outcome; this note itself does not declare that the rerun passes.

Initial exception:

    File "check_multiroot.py", line 127
        assert hi<=chi(q0,q1)<=const(r,k)
    AssertionError

The analytic proof did not change in response. No floating-point replacement or tolerance was introduced.
