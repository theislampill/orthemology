import RestrictedCompiler
import verification.KernelAudit
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.IdentityComplexity P01AC.BooleanPrimitive
open P01AC.RestrictedIdentity
open P01F (cons)
example (e f : Expr 2) (h : FragmentValid e f) : Has [] (.atom .i) (.identity (Curried 2) e.closed f.closed) := h
