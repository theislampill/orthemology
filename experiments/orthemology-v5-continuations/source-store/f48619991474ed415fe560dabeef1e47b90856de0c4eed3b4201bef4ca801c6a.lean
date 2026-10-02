import BernoulliTailMonotonicity

open scoped BigOperators
open Orthemology.Tranche2

namespace Orthemology.Tranche3
noncomputable section

/-- Exact tail checks, not numerical root approximations, certify finite-sample
coverage. Endpoint exceptions retain the degenerate count cases. -/
def TailBracket (n : ℕ) (beta : ℝ) (lower upper : Bits n → ℝ) : Prop :=
  (∀ w, 0 ≤ lower w ∧ lower w ≤ upper w ∧ upper w ≤ 1) ∧
  (∀ w, lower w = 0 ∨ bernoulliUpper n (countOnes n w) (lower w) ≤ beta) ∧
  (∀ w, upper w = 1 ∨ bernoulliLower n (countOnes n w) (upper w) ≤ beta)

/-- Coverage for the actual n-bit iid Bernoulli mass and every real parameter,
including zero and one. No grid restriction or caller-supplied coverage bound. -/
theorem bernoulli_interval_coverage (n : ℕ) (a beta : ℝ)
    (ha0 : 0 ≤ a) (ha1 : a ≤ 1) (hb : 0 ≤ beta)
    (lower upper : Bits n → ℝ) (hc : TailBracket n beta lower upper) :
    (∑ w, if a < lower w ∨ upper w < a then bernoulliMass n a w else 0) ≤ 2*beta := by
  apply tail_inversion_coverage (bernoulliMass n a) (countOnes n)
    (bernoulliMass_nonneg n a ha0 ha1) beta hb a lower upper
  · intro w hw
    rcases hc.2.1 w with h | h
    · linarith
    · rw [← bernoulliUpper_as_tail]
      exact (bernoulliUpper_mono n _ a (lower w) ha0 hw.le
        ((hc.1 w).2.1.trans (hc.1 w).2.2)).trans h
  · intro w hw
    rcases hc.2.2 w with h | h
    · linarith
    · rw [← bernoulliLower_as_tail]
      exact (bernoulliLower_antitone n _ (upper w) a
        ((hc.1 w).1.trans (hc.1 w).2.1) hw.le ha1).trans h

end
end Orthemology.Tranche3

#print axioms Orthemology.Tranche3.bernoulli_interval_coverage
