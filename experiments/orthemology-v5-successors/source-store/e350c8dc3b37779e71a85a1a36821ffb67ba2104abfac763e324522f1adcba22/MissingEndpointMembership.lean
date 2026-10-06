import RestrictedCompiler
import verification.KernelAudit
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.IdentityComplexity P01AC.BooleanPrimitive
open P01AC.RestrictedIdentity
open P01F (cons)
example {t u : Term} {n : Nat} {ρ : OEnv} (ht : NatObs t n) (hu : NatObs u n) : F N ρ zeroEnv t u := by
  exact same_index_related ht hu
