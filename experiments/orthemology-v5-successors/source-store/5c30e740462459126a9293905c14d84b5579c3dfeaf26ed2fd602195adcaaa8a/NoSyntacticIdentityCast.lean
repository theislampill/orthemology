import PolynomialTestBoundary
import verification.KernelAudit
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive P01AC.RestrictedIdentity
open P01AC.PolynomialTestBoundary
open P01F (cons)
example (s t : Root 2) (h : ∀ v, s.denote v = t.denote v) : Has [] (.atom .i) (.identity (Curried 2) s.closed t.closed) := (F_identity_iff_denote s t).mpr h
