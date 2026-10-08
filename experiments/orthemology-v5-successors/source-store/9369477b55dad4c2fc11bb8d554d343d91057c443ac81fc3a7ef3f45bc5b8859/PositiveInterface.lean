import RestrictedCompiler
import verification.KernelAudit
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.IdentityComplexity P01AC.BooleanPrimitive
open P01AC.RestrictedIdentity
open P01F (cons)
example (e f : Expr 2) : FragmentValid e f ↔ ∀ v, e.denote v = f.denote v  := fragment_valid_iff_denote e f
example (e : Expr 2) : Has [] e.closed (Curried 2) := e.closed_has
