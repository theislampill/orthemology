/- Expected rejection: interface control, not a mathematical independence proof. -/
import EffectiveRuleBoundary
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC P01AC.EffectiveCompleteness

example {g o : Nat → Nat} {G O : Term} (hg : Represents g G) (c : Nat) :
    IdentityValid (tester G O (numeral c)) (constantRaw (numeral 0)) ↔
      ∀ n, o (run g c n) = 0 := by
  exact @original_identity_iff_run_zero g o G O hg c
