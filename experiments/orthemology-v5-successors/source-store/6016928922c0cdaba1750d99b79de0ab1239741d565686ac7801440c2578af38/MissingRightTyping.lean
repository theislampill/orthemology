/- Deliberately rejected interface use; not an independence proof. -/
import EffectiveBooleanInterfaces
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.IdentityComplexity
open P01AC.BooleanIdentity P01AC.BooleanPrimitive
example (p q : Poly) (hp : Has [] p CB) : BoolValid p q ↔ BoolTests p q :=
  @bool_valid_iff_tests p q hp hp
