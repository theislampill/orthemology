# PMR-007 Deep Round AN V2 — distinct fresh rereview

```text
candidate: PMR-007-ABPD-1 V2
review relation: distinct count-vector likelihood, exhaustive event-subset, and Kraft-code implementation in the same Pro program
external independence: false
disposition: PASS_WITH_NONBLOCKING_META_ABDUCTIVE_AND_MODEL_SCOPE_NOTES
```

The rereview did not import or call the primary checker. It used a separate
three-outcome denominator-five probability universe, multinomial count-vector
likelihoods, exhaustive event subsets, direct total-variation calculations,
and direct Kraft/prefix-code checks. Candidate G's exact P5/P6 statements were
checked against the frozen Candidate-G formal reconstruction.

```text
frozen hash rows:                                      8
frozen hash mismatches:                                0
Candidate-G source anchors:                            5
source-anchor failures:                                0

finite distributions:                                21
model pairs:                                         441
count vectors through sample length five:             56
prior values:                                          4
likelihood-parity prior instances:                 7,032
likelihood-parity failures:                            0
nonunit likelihood instances:                     43,872
zero-denominator cases retained as undefined odds: 11,970

total-variation/event-gap mismatches:                  0
distinct pairs without an event witness:               0

independently fixed support cases:                    75
support Bayes-factor failures:                         0

valid prefix-code reversals:                         PASS
misspecified-zero nonuniqueness control:             PASS
```

The rereview confirms:

```text
equal positive likelihood preserves prior odds;

finite registered distributions are predictively distinguishable exactly
when total-variation distance is positive, equivalently when some event has a
different probability;

an independently fixed support restriction can produce a nonunit Bayes factor;

raw two-hypothesis description-length ranking can be reversed by valid prefix
codes unless the coding policy is independently fixed;

eliminating one zero-support frozen model does not identify a unique rival;

Candidate G P5 remains the unmatched-rival burden and P6 remains a separate
meta-abductive burden.
```

The result remains standard finite Bayesian/probability/coding theory with zero
general mathematical novelty. It supplies an exact evidential gate for the
Candidate-G architecture comparison. It does not provide a canonical prior,
likelihood model, representation, coding language, or metaphysical bridge.
