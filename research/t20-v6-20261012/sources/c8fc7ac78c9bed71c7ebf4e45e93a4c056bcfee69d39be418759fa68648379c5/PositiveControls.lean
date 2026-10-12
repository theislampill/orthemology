import RationalShiftRealisation
open RationalBinaryWeights OrthemologyTagged OrthemologyTagged.UnaryPrefix
example : closedDigit 1 1 0 = true := by decide
example : closedDigit 1 2 0 = true := by decide
example : closedDigit 1 2 1 = false := by decide
example : closedDigit 0 3 19 = false := by decide
example : prefixValue (fun _ _ _ => 1) (fun _ => false) 0 0 2 = 0 := by decide
example : suffixWord 2 10 0 = 6 := by decide
example : suffixWord 2 10 5 = 1 := by decide
example : prefixValue (fun _ _ w => w) (fun _ => false) 0 2 10 = 6 := by decide
example : prefixValue (fun _ _ _ => 1) (fun _ => true) 0 2 10 = 0 := by decide
example (F : ℕ → ℕ → ℕ → ℕ) (D : ℕ → Bool) (a : ℕ) :
 P02A2.ObserverCore.output (prefixValue F D a) allTrue = allTrue :=
 prefixValue_allTrue F D a
