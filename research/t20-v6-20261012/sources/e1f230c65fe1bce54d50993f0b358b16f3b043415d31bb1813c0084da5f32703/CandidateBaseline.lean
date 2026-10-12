import CandidateWitnesses
open P02A2.ObserverCore P02A2.CandidateSource P02A2.CandidateWitnesses
example : exec (sourceCandidate boundedMatrix 3 0 (.constant 2)) zeroStore 3 = 2 :=
  candidate_checks_inclusive_test_bound.1
example : exec (sourceCandidate trueMatrixCode 3 0 (.constant 2)) zeroStore 3 = 0 :=
  candidate_retains_first_success.1
