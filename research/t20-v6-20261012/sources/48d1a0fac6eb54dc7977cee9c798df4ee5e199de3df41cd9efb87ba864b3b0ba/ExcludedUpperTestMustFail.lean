import CandidateWitnesses
open P02A2.ObserverCore P02A2.CandidateSource P02A2.CandidateWitnesses
example : exec (wrongTestBound (matrixCall boundedMatrix 3 0) (.constant 2)) zeroStore 3 = 2 := by
  rw [candidate_checks_inclusive_test_bound.2]
  decide
