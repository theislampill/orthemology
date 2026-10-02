import GenericQueryReference

noncomputable section
open MeasureTheory ProbabilityTheory Finset
open scoped BigOperators ENNReal

namespace Orthemology.Tranche2.PolicyEmbedding
variable {A Y : Type*} [Fintype A] [Fintype Y] [DecidableEq A]

def rowMass (P : A → Y → ℝ) (w : A → Y) : ℝ := ∏ a, P a (w a)

omit [Fintype Y] [DecidableEq A] in
lemma rowMass_nonneg (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (w : A → Y) :
    0 ≤ rowMass P w := Finset.prod_nonneg (fun a _ => hP a _)

omit [Fintype Y] [DecidableEq A] in
lemma rowMass_pos (P : A → Y → ℝ) (hP : ∀ a y, 0 < P a y) (w : A → Y) :
    0 < rowMass P w := Finset.prod_pos (fun a _ => hP a _)

lemma rowMass_normalized (P : A → Y → ℝ) (hN : ∀ a, ∑ y, P a y = 1) :
    ∑ w : A → Y, rowMass P w = 1 := by
  classical
  unfold rowMass
  rw [← Fintype.prod_sum]
  simp_rw [hN]
  simp

def rowPMF (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) : PMF (A → Y) := by
  classical
  exact PMF.ofFintype (fun w => ENNReal.ofReal (rowMass P w)) (by
    rw [← ENNReal.ofReal_sum_of_nonneg (fun w _ => rowMass_nonneg P hP w), rowMass_normalized P hN]
    exact ENNReal.ofReal_one)

/-- Summing over unobserved row coordinates returns exactly the chosen action's
law. Counterfactual coordinates are not additional policy observations. -/
theorem rowMass_coordinate [DecidableEq Y] (P : A → Y → ℝ) (hN : ∀ a, ∑ y, P a y = 1) (a : A) (y : Y) :
    (∑ w : A → Y, if w a = y then rowMass P w else 0) = P a y := by
  classical
  let q : A → Y → ℝ := fun b z => if b = a then (if z = y then P b z else 0) else P b z
  have hrow : ∀ w, rowMass q w = if w a = y then rowMass P w else 0 := by
    intro w
    by_cases hw : w a = y
    · rw [if_pos hw]
      apply Finset.prod_congr rfl
      intro b _
      by_cases hb : b = a
      · subst b
        simp [q,hw]
      · simp [q,hb]
    · rw [if_neg hw]
      apply Finset.prod_eq_zero (Finset.mem_univ a)
      simp [q,hw]
  have hsum : ∀ b, (∑ z, q b z) = if b = a then P a y else 1 := by
    intro b
    by_cases hb : b = a
    · subst b
      simp [q]
    · simp [q,hb,hN]
  calc
    _ = ∑ w : A → Y, rowMass q w := Finset.sum_congr rfl (fun w _ => (hrow w).symm)
    _ = ∏ b, ∑ z, q b z := (Fintype.prod_sum q).symm
    _ = _ := by simp_rw [hsum]; simp

variable [MeasurableSpace Y] [MeasurableSingletonClass Y]

def rowMeasure (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) : Measure (A → Y) :=
  (rowPMF P hP hN).toMeasure

instance rowMeasure_probability (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) : IsProbabilityMeasure (rowMeasure P hP hN) := by
  unfold rowMeasure
  infer_instance

theorem rowMeasure_full_support (P : A → Y → ℝ) (hP : ∀ a y, 0 < P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (w : A → Y) :
    rowMeasure P (fun a y => (hP a y).le) hN {w} ≠ 0 := by
  unfold rowMeasure
  rw [PMF.toMeasure_apply_singleton _ w (measurableSet_singleton w)]
  change ENNReal.ofReal (rowMass P w) ≠ 0
  exact ne_of_gt (ENNReal.ofReal_pos.mpr (rowMass_pos P hP w))

/-- The chosen coordinate has exactly its declared feedback marginal. -/
theorem rowMeasure_coordinate (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (a : A) (y : Y) :
    rowMeasure P hP hN {w | w a = y} = ENNReal.ofReal (P a y) := by
  classical
  unfold rowMeasure
  rw [PMF.toMeasure_apply_fintype]
  have he : (∑ w : A → Y, {w | w a = y}.indicator (rowPMF P hP hN) w) =
      ∑ w : A → Y, ENNReal.ofReal (if w a = y then rowMass P w else 0) := by
    apply Finset.sum_congr rfl
    intro w _
    by_cases hw : w a = y
    · rw [Set.indicator_of_mem (show w ∈ {w : A → Y | w a = y} from hw), if_pos hw]
      rfl
    · rw [Set.indicator_of_not_mem (show w ∉ {w : A → Y | w a = y} from hw), if_neg hw, ENNReal.ofReal_zero]
  rw [he, ← ENNReal.ofReal_sum_of_nonneg (fun w _ => by
    split_ifs <;> first | exact rowMass_nonneg P hP w | exact le_rfl)]
  rw [rowMass_coordinate P hN a y]

/-- The actual rival row law supplies every positive finite-prefix atom required
by the finite-query transfer theorem. -/
theorem rowOracle_finite_prefix_positive [Inhabited Y]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 < P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (N : ℕ) (w : Fin N → (A → Y)) :
    ((FiniteAlphabetQuery.iidOracle (rowMeasure P (fun a y => (hP a y).le) hN)).map
      (FiniteAlphabetQuery.prefixSymbols N)) {w} ≠ 0 :=
  FiniteAlphabetQuery.iidOracle_prefix_nonzero _ (rowMeasure_full_support P hP hN) N w

end Orthemology.Tranche2.PolicyEmbedding
