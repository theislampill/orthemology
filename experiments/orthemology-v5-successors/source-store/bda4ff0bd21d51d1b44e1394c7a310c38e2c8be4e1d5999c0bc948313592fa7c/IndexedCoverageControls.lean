import IndexedCoverage
open OrthemicCertificate.Signed
private def localCheck (n : Nat) (r : Refutation) : Bool :=
  rejectCheck (fun x : Nat => decide (x = 0)) (.literal n true) r
-- Complete two-position evidence passes.
example : indexedCheck localCheck 0 [1,2] [(0,.leaf),(1,.leaf)] = true := by decide
-- Omission, duplicate, skipped/out-of-range and extra indices all fail.
example : indexedCheck localCheck 0 [1,2] [(0,.leaf)] = false := by decide
example : indexedCheck localCheck 0 [1,2] [(0,.leaf),(0,.leaf)] = false := by decide
example : indexedCheck localCheck 0 [1,2] [(0,.leaf),(2,.leaf)] = false := by decide
example : indexedCheck localCheck 0 [1,2] [(0,.leaf),(1,.leaf),(2,.leaf)] = false := by decide
example : indexedCheck localCheck 0 [1,2] [(1,.leaf),(0,.leaf)] = false := by decide
-- A true member cannot be rejected by a leaf, even with perfect indexing.
example : indexedCheck localCheck 0 [1,0] [(0,.leaf),(1,.leaf)] = false := by decide
#print axioms indexedCheck_indices
#print axioms indexedCheck_sound
#print axioms indexedCandidate_correct
