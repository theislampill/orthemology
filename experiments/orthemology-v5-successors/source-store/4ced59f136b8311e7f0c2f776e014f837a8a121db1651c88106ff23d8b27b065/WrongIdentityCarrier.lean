/- Expected rejection: interface control, not a mathematical independence proof. -/
import EffectiveRuleBoundary
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC P01AC.EffectiveCompleteness

example {g o : Nat → Nat} {G O : Term} (hg : Represents g G) (ho : Represents o O)
    (c : Nat) (h : ∀ n, o (run g c n) = 0) :
    ∀ r : REnv, P01AC.G (.identity .raw (tester G O (numeral c))
      (constantRaw (numeral 0))) r zeroEnv zeroEnv .i .i := by
  exact (original_identity_iff_run_zero hg ho c).mpr h
