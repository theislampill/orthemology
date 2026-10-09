import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Algebra.Order.Field.Rat

/-!
# A finite independent Bernoulli assignment model

An assignment records success (`true`) or failure (`false`) at each route.
Its mass is the product of its coordinate masses.  Events are evaluated by
summing those masses over all actual assignments.  In particular, the
all-failure event factorises by a theorem, not by its definition.
-/

namespace RouteProbability

open scoped BigOperators

variable {R : Type*} [Fintype R] [DecidableEq R]

/-- Product mass of an actual success/failure assignment; `p` gives failure probabilities. -/
def bernoulliWeight (p : R → ℚ) (ω : R → Bool) : ℚ :=
  ∏ r, if ω r then 1 - p r else p r

/-- The finite assignment masses are nonnegative for valid coordinate probabilities. -/
theorem bernoulliWeight_nonneg (p : R → ℚ)
    (hp0 : ∀ r, 0 ≤ p r) (hp1 : ∀ r, p r ≤ 1) (ω : R → Bool) :
    0 ≤ bernoulliWeight p ω := by
  unfold bernoulliWeight
  have h : ∀ s : Finset R, 0 ≤ ∏ r ∈ s, if ω r then 1 - p r else p r := by
    intro s
    induction s using Finset.induction_on with
    | empty => simp
    | @insert r s hrs ih =>
      rw [Finset.prod_insert hrs]
      apply mul_nonneg _ ih
      split
      · exact sub_nonneg.mpr (hp1 r)
      · exact hp0 r
  exact h Finset.univ

/-- The weights of all assignments sum to one. -/
theorem sum_bernoulliWeight (p : R → ℚ) :
    (∑ ω : R → Bool, bernoulliWeight p ω) = 1 := by
  unfold bernoulliWeight
  rw [← Fintype.prod_sum (fun (r : R) (b : Bool) => if b then 1 - p r else p r)]
  simp

/-- Summing the actual assignments in which every selected route fails
recovers the product of their failure probabilities. -/
theorem sum_bernoulliWeight_all_false (p : R → ℚ) (C : Finset R) :
    (∑ ω : R → Bool,
      if (∀ r ∈ C, ω r = false) then bernoulliWeight p ω else 0) =
      ∏ r ∈ C, p r := by
  classical
  have hfactor (ω : R → Bool) :
      (if (∀ r ∈ C, ω r = false) then bernoulliWeight p ω else 0) =
        ∏ r, if (r ∈ C → ω r = false) then
          (if ω r then 1 - p r else p r) else 0 := by
    rw [Fintype.prod_ite_zero]
    rfl
  simp_rw [hfactor]
  rw [← Fintype.prod_sum (fun (r : R) (b : Bool) =>
    if (r ∈ C → b = false) then (if b then 1 - p r else p r) else 0)]
  have hsum (r : R) :
      (∑ b : Bool, if (r ∈ C → b = false) then
        (if b then 1 - p r else p r) else 0) =
        if r ∈ C then p r else 1 := by
    by_cases hr : r ∈ C <;> simp [hr]
  simp_rw [hsum]
  exact Fintype.prod_ite_mem C p

end RouteProbability
