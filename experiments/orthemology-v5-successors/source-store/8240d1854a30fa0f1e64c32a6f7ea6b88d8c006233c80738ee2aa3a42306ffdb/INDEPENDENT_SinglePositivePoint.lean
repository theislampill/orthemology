import IdentityChecker
import verification.KernelAudit
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.RestrictedIdentity P01AC.RestrictedIdentityV2
example (p q : MvPolynomial (Fin 1) Nat) (h : MvPolynomial.eval (fun _ => 1) p = MvPolynomial.eval (fun _ => 1) q) : p = q := nat_polynomial_eq_of_positive_eval h
