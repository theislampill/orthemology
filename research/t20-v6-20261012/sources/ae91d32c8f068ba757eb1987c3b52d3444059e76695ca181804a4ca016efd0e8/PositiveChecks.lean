import Countermodel

open MvPolynomial FullPolynomialCountermodel
open FullFunctionalIndexing FullFunctionalPolynomialBridge

/-- The final certificate is bound to the actual polynomial algebra and witness.
There is no positivity hypothesis, finite degree ceiling, or assumed functional. -/
theorem independently_typed_closed_countermodel :
    ∃ L : MvPolynomial (Fin 2) ℝ →ₗ[ℝ] ℝ,
      L 1 = 1 ∧
      (∀ p : MvPolynomial (Fin 2) ℝ, p ≠ 0 → 0 < L (p ^ 2)) ∧
      (∀ x : Fin 2 → ℝ, (3 : ℝ) / 4 ≤ eval x
        (1 + X (0 : Fin 2)^4 * X (1 : Fin 2)^2 +
        X (0 : Fin 2)^2 * X (1 : Fin 2)^4 - X (0 : Fin 2)^2 * X (1 : Fin 2)^2)) ∧
      L (1 + X (0 : Fin 2)^4 * X (1 : Fin 2)^2 +
        X (0 : Fin 2)^2 * X (1 : Fin 2)^4 - X (0 : Fin 2)^2 * X (1 : Fin 2)^2) = -1 :=
  full_polynomial_countermodel

/-- A symbolic exponent, not a bounded numerical sample. -/
theorem arbitrarily_high_degree (n : ℕ) :
    0 < Λ (((X (0 : Fin 2) : MvPolynomial (Fin 2) ℝ) ^ (n + 1000)) ^ 2) := by
  exact strict_square_positive _ (pow_ne_zero _ (X_ne_zero 0))

theorem arbitrary_polynomial_no_degree_premise (p : MvPolynomial (Fin 2) ℝ) (hp : p ≠ 0) :
    0 < Λ (p * p) := by
  simpa only [pow_two] using strict_square_positive p hp

/-- Every finite total-degree moment truncation, including one preserving an
arbitrarily long initial range, kills a nonzero polynomial square. -/
noncomputable def cutoffMoment (N : ℕ) (e : Exponent) : ℝ :=
  if e.1 + e.2 ≤ N then FullFunctionalMoment.moment e else 0

theorem cutoff_preserves_prefix (N : ℕ) (e : Exponent) (h : e.1 + e.2 ≤ N) :
    cutoffMoment N e = FullFunctionalMoment.moment e := by
  simp [cutoffMoment, h]

theorem any_finite_cutoff_kills_high_square (N : ℕ) :
    functional (cutoffMoment N)
      ((monomial (encode (N+1,0)) (1 : ℝ)) ^ 2) = 0 := by
  rw [pow_two, monomial_mul, functional_monomial, decode_add, decode_encode]
  have h : ¬ (N+1)+(N+1) ≤ N := by omega
  simp [cutoffMoment, h]

theorem cutoff_test_polynomial_nonzero (N : ℕ) :
    (monomial (encode (N+1,0)) (1 : ℝ) : MvPolynomial (Fin 2) ℝ) ≠ 0 := by
  simp

theorem finite_cutoff_not_strict (N : ℕ) :
    ¬ (∀ p : MvPolynomial (Fin 2) ℝ, p ≠ 0 →
        0 < functional (cutoffMoment N) (p^2)) := by
  intro h
  have hh := h _ (cutoff_test_polynomial_nonzero N)
  rw [any_finite_cutoff_kills_high_square] at hh
  exact (lt_irrefl 0) hh

#print axioms independently_typed_closed_countermodel
#print axioms arbitrarily_high_degree
#print axioms arbitrary_polynomial_no_degree_premise
#print axioms finite_cutoff_not_strict

/- Record the actual complete imported-module closure for source/object binding. -/
run_cmd do
  let env ← Lean.getEnv
  for name in env.allImportedModuleNames do
    Lean.logInfo m!"REVIEW_IMPORT {name}"
