/- Deliberately rejected interface use; not an independence proof. -/
import EffectiveBooleanInterfaces
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.IdentityComplexity
open P01AC.BooleanIdentity P01AC.BooleanPrimitive
example (f : PR 2) (e n : Nat) :
  Conv (observationAt (simFamily f e) n) (pick (decide (f.denote (inputs e n) ≠ 0)) .zero .one) :=
  simFamily_obs f e n
