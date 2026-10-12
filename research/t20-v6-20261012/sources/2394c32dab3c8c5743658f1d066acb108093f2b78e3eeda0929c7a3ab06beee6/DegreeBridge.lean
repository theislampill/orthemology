import TruncatedMoment
import Mathlib.Algebra.MvPolynomial.Degrees
import Mathlib.Algebra.BigOperators.Fin

noncomputable section
namespace TruncatedMoment
open MvPolynomial

theorem exponent_coordinates (m : Fin 3 →₀ ℕ) :
    m = exponent (m 0) (m 1) (m 2) := by
  ext i
  fin_cases i <;> simp [exponent]

theorem exponent_sum (a b c : ℕ) :
    (exponent a b c).sum (fun _ n => n) = a+b+c := by
  rw [Finsupp.sum_fintype _ _ (by simp)]
  simp [Fin.sum_univ_succ, exponent]
  omega

theorem small_exponent_cases (a b c : ℕ) (h : a+b+c ≤ 2) :
    (a=0 ∧ b=0 ∧ c=0) ∨ (a=2 ∧ b=0 ∧ c=0) ∨ (a=0 ∧ b=2 ∧ c=0) ∨
    (a=0 ∧ b=0 ∧ c=2) ∨ (a=1 ∧ b=0 ∧ c=0) ∨ (a=0 ∧ b=1 ∧ c=1) ∨
    (a=0 ∧ b=1 ∧ c=0) ∨ (a=1 ∧ b=0 ∧ c=1) ∨ (a=0 ∧ b=0 ∧ c=1) ∨
    (a=1 ∧ b=1 ∧ c=0) := by omega

theorem coeff_large_exponent (p : Poly) (h : p.totalDegree ≤ 2)
    (a b c : ℕ) (habc : ¬ a+b+c ≤ 2) : p.coeff (exponent a b c) = 0 := by
  by_contra hc
  have hle := le_totalDegree (mem_support_iff.mpr hc)
  rw [exponent_sum] at hle
  omega

/-- Every actual polynomial of total degree at most two has the ten displayed coefficients. -/
theorem quadratic_parameterization (p : Poly) (h : p.totalDegree ≤ 2) :
    p = quadratic
      (p.coeff (exponent 0 0 0)) (p.coeff (exponent 2 0 0))
      (p.coeff (exponent 0 2 0)) (p.coeff (exponent 0 0 2))
      (p.coeff (exponent 1 0 0)) (p.coeff (exponent 0 1 1))
      (p.coeff (exponent 0 1 0)) (p.coeff (exponent 1 0 1))
      (p.coeff (exponent 0 0 1)) (p.coeff (exponent 1 1 0)) := by
  ext m
  obtain ⟨a,b,c,hm⟩ : ∃ a b c, m = exponent a b c := ⟨m 0,m 1,m 2,exponent_coordinates m⟩
  subst m
  by_cases habc : a+b+c ≤ 2
  · rcases small_exponent_cases a b c habc with hcase | hcase | hcase | hcase | hcase | hcase | hcase | hcase | hcase | hcase
    all_goals rcases hcase with ⟨rfl,rfl,rfl⟩
    all_goals norm_num [quadratic, term, coeff_monomial, exponent_eq_iff]
  · rw [coeff_large_exponent p h a b c habc]
    have hn : ¬ (a=0 ∧ b=0 ∧ c=0) ∧ ¬ (a=2 ∧ b=0 ∧ c=0) ∧ ¬ (a=0 ∧ b=2 ∧ c=0) ∧
      ¬ (a=0 ∧ b=0 ∧ c=2) ∧ ¬ (a=1 ∧ b=0 ∧ c=0) ∧ ¬ (a=0 ∧ b=1 ∧ c=1) ∧
      ¬ (a=0 ∧ b=1 ∧ c=0) ∧ ¬ (a=1 ∧ b=0 ∧ c=1) ∧ ¬ (a=0 ∧ b=0 ∧ c=1) ∧
      ¬ (a=1 ∧ b=1 ∧ c=0) := by omega
    rcases hn with ⟨h0,h1,h2,h3,h4,h5,h6,h7,h8,h9⟩
    simp [quadratic, term, coeff_monomial, exponent_eq_iff, eq_comm,
      h0,h1,h2,h3,h4,h5,h6,h7,h8,h9]

end TruncatedMoment
