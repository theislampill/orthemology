/- Deliberately rejected interface use; not an independence proof. -/
import EffectiveBooleanInterfaces
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.IdentityComplexity
open P01AC.BooleanIdentity P01AC.BooleanPrimitive
example (left right : Term) (ρ : OEnv) (η : Env) (hr : F B ρ η right right) :
  F B ρ η left right ↔ Conv (observe left) (observe right) :=
  @boolean_related_iff_observation left right ρ η hr hr
