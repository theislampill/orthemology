import Mathlib.Algebra.MvPolynomial.Basic
import Mathlib.Algebra.MvPolynomial.Eval
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Linarith

noncomputable section
namespace TruncatedMoment
open MvPolynomial
abbrev Poly := MvPolynomial (Fin 3) ℝ

def exponent (a b c : ℕ) : Fin 3 →₀ ℕ :=
  Finsupp.single 0 a + Finsupp.single 1 b + Finsupp.single 2 c

def term (a b c : ℕ) (r : ℝ) : Poly := monomial (exponent a b c) r

theorem exponent_add (a b c d e f : ℕ) :
    exponent a b c + exponent d e f = exponent (a+d) (b+e) (c+f) := by
  ext i
  fin_cases i <;> simp [exponent]

theorem exponent_eq_iff (a b c d e f : ℕ) :
    exponent a b c = exponent d e f ↔ a=d ∧ b=e ∧ c=f := by
  simp [Finsupp.ext_iff, Fin.forall_fin_succ, exponent]

theorem term_mul (a b c d e f : ℕ) (r s : ℝ) :
    term a b c r * term d e f s = term (a+d) (b+e) (c+f) (r*s) := by
  simp [term, monomial_mul, exponent_add]

/-- A real linear coefficient functional. Its asserted positivity is restricted to
squares of quadratics; its zero-valued continuation beyond degree four is not positive. -/
noncomputable def Lambda : Poly →ₗ[ℝ] ℝ :=
  lcoeff ℝ (exponent 0 0 0) +
  (4:ℝ) • (lcoeff ℝ (exponent 2 0 0) + lcoeff ℝ (exponent 0 2 0) + lcoeff ℝ (exponent 0 0 2)) +
  (50:ℝ) • (lcoeff ℝ (exponent 4 0 0) + lcoeff ℝ (exponent 0 4 0) + lcoeff ℝ (exponent 0 0 4)) +
  lcoeff ℝ (exponent 2 2 0) + lcoeff ℝ (exponent 2 0 2) + lcoeff ℝ (exponent 0 2 2) +
  (3/2:ℝ) • lcoeff ℝ (exponent 1 1 1)

/-- The ten coefficients range independently over all real numbers. -/
def quadratic (c a b d u v w r s t : ℝ) : Poly :=
  term 0 0 0 c + term 2 0 0 a + term 0 2 0 b + term 0 0 2 d +
  term 1 0 0 u + term 0 1 1 v + term 0 1 0 w + term 1 0 1 r +
  term 0 0 1 s + term 1 1 0 t

theorem Lambda_quadratic_square (c a b d u v w r s t : ℝ) :
    Lambda (quadratic c a b d u v w r s t ^ 2) =
    c^2 + 8*c*(a+b+d) + 50*(a^2+b^2+d^2) + 2*(a*b+a*d+b*d) +
    (4*u^2+3*u*v+v^2) + (4*w^2+3*w*r+r^2) + (4*s^2+3*s*t+t^2) := by
  simp only [quadratic, pow_two, add_mul, mul_add, term_mul, map_add]
  norm_num [Lambda, term, LinearMap.add_apply, LinearMap.smul_apply,
    lcoeff_apply, coeff_monomial, exponent_eq_iff]
  ring

/-- The nonnegative Choi--Lam witness, represented as an actual multivariate polynomial. -/
def witness : Poly :=
  term 0 0 0 1 + term 1 1 1 (-4) + term 2 2 0 1 + term 2 0 2 1 + term 0 2 2 1

theorem Lambda_witness : Lambda witness = -2 := by
  norm_num [witness, Lambda, term, coeff_monomial, exponent_eq_iff]

end TruncatedMoment
