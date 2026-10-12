import Mathlib.Tactic

/-!
Independent local lemmas for the sparse-prior ordinary review.

These lemmas establish the exact literal report readout and acceptance separation.
They do not formalise the countable Bayes rule, probability model, lifetime overlap
bounds, convergence criterion, or full theorem.
-/

namespace SparsePriorReview

noncomputable section

def D0 (a e q : ℝ) : ℝ := q ^ 2 - 1 / 4 - a * e * (1 + e)
def D1 (a e q : ℝ) : ℝ := (1 - q) ^ 2 - 1 / 4 + a * e * (1 - e)

def Accepted (a e q : ℝ) : Prop := D0 a e q ≤ 0 ∧ D1 a e q ≤ 0

theorem readout_D0 (a e : ℝ) :
    D0 a e (1 / 2 + e * a) = -(e ^ 2 * a * (1 - a)) := by
  unfold D0
  ring

theorem readout_D1 (a e : ℝ) :
    D1 a e (1 / 2 + e * a) = -(e ^ 2 * a * (1 - a)) := by
  unfold D1
  ring

theorem exact_readout_accepted (a e : ℝ) (ha : 0 ≤ a) (ha1 : a ≤ 1) :
    Accepted a e (1 / 2 + e * a) := by
  have hp : 0 ≤ e ^ 2 * a * (1 - a) :=
    mul_nonneg (mul_nonneg (sq_nonneg e) ha) (sub_nonneg.mpr ha1)
  constructor
  · rw [readout_D0]
    linarith
  · rw [readout_D1]
    linarith

/-- The 2-separated support permits no report accepted at two support points. -/
theorem separated_acceptance_disjoint (a b e q : ℝ)
    (hb : 0 < b) (hab : 2 * b ≤ a)
    (he : 0 < e) (he4 : e ≤ 1 / 4) :
    ¬ (Accepted a e q ∧ Accepted b e q) := by
  intro h
  have he1 : 0 ≤ 1 - e := by linarith
  have hthree : 0 < 1 - 3 * e := by linarith
  have hleft : 0 ≤ (a - 2 * b) * (1 - e) :=
    mul_nonneg (sub_nonneg.mpr hab) he1
  have hright : 0 < b * (1 - 3 * e) := mul_pos hb hthree
  have hinner : 0 < a * (1 - e) - b * (1 + e) := by
    nlinarith
  have hp : 0 < e * (a * (1 - e) - b * (1 + e)) := mul_pos he hinner
  have hsum : D0 b e q + D1 a e q =
      2 * (q - 1 / 2) ^ 2 + e * (a * (1 - e) - b * (1 + e)) := by
    unfold D0 D1
    ring
  have hs : 0 ≤ (q - 1 / 2) ^ 2 := sq_nonneg _
  have hbad : D0 b e q + D1 a e q ≤ 0 := add_nonpos h.2.1 h.1.2
  rw [hsum] at hbad
  linarith

end

end SparsePriorReview

#print axioms SparsePriorReview.exact_readout_accepted
#print axioms SparsePriorReview.separated_acceptance_disjoint
