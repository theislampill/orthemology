import IdentityChecker
import verification.KernelAudit
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.RestrictedIdentity P01AC.RestrictedIdentityV2
example (p : Sparse 1) (v : Fin 1 → Nat) (h : MvPolynomial.eval v (polynomial p) = 0) : zeroTest p = true := (zeroTest_iff_eval_zero p v).mpr h
