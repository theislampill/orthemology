import RestrictedCompiler
import verification.KernelAudit
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.IdentityComplexity P01AC.BooleanPrimitive
open P01AC.RestrictedIdentity
open P01F (cons)
example (e : Expr 0) : Has [] e.closed (Curried 1) := e.closed_has
