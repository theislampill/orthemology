/- Deliberately rejected interface use; not an independence proof. -/
import EffectiveBooleanInterfaces
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.IdentityComplexity
open P01AC.BooleanIdentity P01AC.BooleanPrimitive
example (f : PR 2) (e : Nat) :
  (∀ r, G (.identity .raw (simFamily f e) constantChoice) r zeroEnv zeroEnv .i .i) ↔
    ∀ n, f.denote (inputs n e) = 0 := original_identity_iff_all_zero f e
