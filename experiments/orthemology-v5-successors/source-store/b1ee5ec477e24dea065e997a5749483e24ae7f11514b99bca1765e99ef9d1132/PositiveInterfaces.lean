import PolynomialTestBoundary
import verification.KernelAudit
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive P01AC.RestrictedIdentity
open P01AC.PolynomialTestBoundary
open P01F (cons)
example (p q : Arithmetic 2) : Valid (.equal p q) (.old (.constant 0)) ↔ ∀ v, p.denote v ≠ q.denote v := root_equal_zero_iff p q
example (s : Root 0) : Has [] s.closed (Curried 0) := s.closed_has
example (s t : Root 2) : (∀ R : REnv, G (.identity (Curried 2) s.closed t.closed) R zeroEnv zeroEnv .i .i) ↔ ∀ v, s.denote v = t.denote v := G_identity_iff_denote s t
