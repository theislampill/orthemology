import CandidateWitnesses
open P02A2.ObserverCore P02A2.CandidateSource P02A2.CandidateWitnesses
example : exec (noFoundGuard (matrixCall trueMatrixCode 3 0) (.constant 2)) zeroStore 3 = 0 := by
  rw [candidate_retains_first_success.2]
  decide
