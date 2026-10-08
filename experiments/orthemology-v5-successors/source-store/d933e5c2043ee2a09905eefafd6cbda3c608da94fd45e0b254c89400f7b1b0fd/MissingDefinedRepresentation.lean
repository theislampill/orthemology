/- Deliberate rejected interface use. This is not a logical independence proof. -/
import EffectivePartialObserver
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.IdentityComplexity

example (U : Term) (H : Nat → Nat → Prop)
    (undefined : ∀ e n, ¬ H e n →
      ¬ Conv (.app (.app U (numeral e)) (numeral n)) (numeral 0))
    (e : Nat) : IdentityValid (universalTester U e) (constantRaw (numeral 0)) ↔
      ∀ n, H e n :=
  original_universal_identity_iff_total U H undefined undefined e
