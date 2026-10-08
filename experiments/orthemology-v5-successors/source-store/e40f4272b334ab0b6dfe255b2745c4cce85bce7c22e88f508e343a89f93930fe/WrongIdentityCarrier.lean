/- Deliberate rejected interface use. This is not a logical independence proof. -/
import EffectivePartialObserver
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.IdentityComplexity

example {p q : Poly} (hp : Has [] p C) (hq : Has [] q C) :
    (∀ r : REnv, G (.identity .raw p q) r zeroEnv zeroEnv .i .i) ↔
      CanonicalTests p q := identity_valid_iff_canonical_tests hp hq
