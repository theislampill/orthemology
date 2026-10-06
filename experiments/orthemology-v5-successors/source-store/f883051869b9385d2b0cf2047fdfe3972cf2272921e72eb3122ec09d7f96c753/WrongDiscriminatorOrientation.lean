/- Deliberately rejected interface use; not an independence proof. -/
import EffectiveBooleanInterfaces
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.IdentityComplexity
open P01AC.BooleanIdentity P01AC.BooleanPrimitive
example : Conv (.app (.app (.app discriminatorTerm (canonical 0)) .zero) .one) .one :=
  discriminator_obs (canonical_obs 0) .zero .one
