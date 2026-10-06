import Refutation
open OrthemicCertificate.Signed
private def bitEval (n : Nat) : Bool := decide (n = 0)
example : rejectCheck bitEval (.literal 0 true) .leaf = false := by decide
example : rejectCheck bitEval (.literal 1 true) .leaf = true := by decide
example : rejectCheck bitEval (.disj (.literal 1 true) (.literal 2 true)) (.left .leaf) = false := by decide
example : rejectCheck bitEval (.disj (.literal 1 true) (.literal 0 true)) (.both .leaf .leaf) = false := by decide
example : rejectCheck bitEval (.disj (.literal 1 true) (.literal 2 true)) (.both .leaf .leaf) = true := by decide
example : rejectCheck bitEval (.conj (.literal 0 true) (.literal 1 true)) (.left .leaf) = false := by decide
example : rejectCheck bitEval (.conj (.literal 0 true) (.literal 1 true)) (.right .leaf) = true := by decide
example : refute bitEval (.literal 0 true) = none := by decide
example : refute bitEval (.literal 1 true) = some .leaf := by decide
#print axioms refutation_sound
#print axioms refutation_complete
#print axioms refute_checked
