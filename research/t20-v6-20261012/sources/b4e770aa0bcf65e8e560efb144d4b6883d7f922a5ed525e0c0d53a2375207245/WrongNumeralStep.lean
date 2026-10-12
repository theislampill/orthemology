import FamilyComputability
open P01D P01AC.EffectiveCompleteness SourceFamilyComputability
-- Intentionally wrong: a successor inserts the fixed compiled SKI step, not I.
example (n : Nat) : inputNumeral (n+1) = .app (.atom .i) (inputNumeral n) :=
  inputNumeral_succ n
