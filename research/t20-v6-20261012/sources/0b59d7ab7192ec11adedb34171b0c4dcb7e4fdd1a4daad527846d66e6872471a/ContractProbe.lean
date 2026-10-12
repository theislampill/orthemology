import AnalyticHinge

namespace IndependentAnalyticContract
noncomputable section
open scoped ENNReal

/-- The original initial half-bound implies the author's all-index half-bound. -/
theorem all_half_from_initial (a : ℕ → ℝ)
    (ha0 : a 0 ≤ (1 / 2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i / 2) :
    ∀ i, a i ≤ (1 / 2 : ℝ) := by
  intro i
  induction i with
  | zero => exact ha0
  | succ i ih =>
      have h := hsep i
      linarith

/-- Exact match of the real-p score notation with the formal factorization. -/
theorem score_factor (u p : ℝ) (hu : 0 < u) (k : ℕ) :
    u ^ ((k : ℝ) + p) = u ^ p * u ^ k := by
  rw [Real.rpow_add hu, Real.rpow_natCast]
  ring

/-- The terminal theorem has the literal infinite binomial expression as its
left side, not an assumed risk bound or a finite enumeration. -/
theorem expanded_contract (a : ℕ → ℝ) (p : ℝ)
    (hp : 0 < p) (ha : ∀ i, 0 < a i)
    (ha0 : a 0 ≤ (1 / 2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i / 2) :
    (∑' n : ℕ, ∑' i : ℕ, ENNReal.ofReal
      (∑ k ∈ Finset.range ((n+1)+1), (((n+1).choose k : ℕ) : ℝ) *
        min ((a i)^p * (a i)^k * (1-a i)^((n+1)-k))
            ((a (i+1))^p * (a (i+1))^k * (1-a (i+1))^((n+1)-k)))) < ⊤ ↔
      Summable (fun i : ℕ => ((a (i+1))^p/a i) * Real.log (a i/a (i+1))) := by
  simpa only [SparsePriorAnalytic.overlapTotal, SparsePriorAnalytic.binaryOverlap]
    using SparsePriorAnalytic.overlapTotal_finite_iff_summable a hp ha
      (all_half_from_initial a ha0 hsep) hsep

/-- The originally assigned p=1 spacing criterion is an actual specialization. -/
theorem p_one_contract (a : ℕ → ℝ)
    (ha : ∀ i, 0 < a i) (ha0 : a 0 ≤ (1 / 2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i / 2) :
    SparsePriorAnalytic.overlapTotal a 1 < ⊤ ↔
      Summable (fun i : ℕ => (a (i+1)/a i) * Real.log (a i/a (i+1))) := by
  simpa only [Real.rpow_one] using
    SparsePriorAnalytic.overlapTotal_finite_iff_summable a (by norm_num : (0 : ℝ) < 1)
      ha (all_half_from_initial a ha0 hsep) hsep

#print axioms score_factor
#print axioms expanded_contract
#print axioms p_one_contract
end
end IndependentAnalyticContract
