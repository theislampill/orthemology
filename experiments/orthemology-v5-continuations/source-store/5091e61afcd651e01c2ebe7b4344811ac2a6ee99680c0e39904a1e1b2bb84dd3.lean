import AtomicReconstruction

namespace Orthemology.Frontier.MealyMeasure
open Set MeasureTheory Filter
open scoped ENNReal Topology BigOperators

variable {S : Type*} [Fintype S] [DecidableEq S] [Nonempty S]

/-- Finite rational partial masses converge to the known exact rational atomic mass. -/
theorem partialMassQ_tendsto (M : Mealy S) (s : S) :
    Tendsto (fun N => (partialMassQ M s N : ℝ)) atTop (𝓝 (P02A2.mass (law M s)).toReal) := by
  have hsum : (∑' n, law M s (atomSet M s n)) = P02A2.mass (law M s) := by
    rw [atomic_mass_eq_tsum_weights]
    congr 1
    funext n
    exact (atomWeight_measure M s n).symm
  have h := ENNReal.tendsto_nat_tsum (fun n => law M s (atomSet M s n))
  rw [hsum] at h
  have hr := (ENNReal.tendsto_toReal (measure_ne_top (law M s) (P02A2.positive (law M s)))).comp h
  have he : (fun N => (partialMassQ M s N : ℝ)) =
      fun N => (∑ n ∈ Finset.range N, law M s (atomSet M s n)).toReal := by
    funext N
    rw [ENNReal.toReal_sum (fun _ _ => measure_ne_top _ _)]
    simp [partialMassQ, atomWeightQ_correct]
  simpa only [he, Function.comp_def] using hr

/-- Exact residual masses decrease to zero; no claim of a total nth-positive-atom selector. -/
theorem residualMassQ_tendsto_zero (M : Mealy S) (s : S) :
    Tendsto (fun N => (residualMassQ M s N : ℝ)) atTop (𝓝 0) := by
  have h := (tendsto_const_nhds (x := (solveHitting M s : ℝ))).sub (partialMassQ_tendsto M s)
  simpa only [residualMassQ, Rat.cast_sub, solveHitting_correct, hittingReal,
    atomic_mass_eq_hitting_probability, sub_self] using h

/-- For every requested precision, some finite initial portion of the skipped enumeration
    leaves less than the rational error threshold. -/
theorem exists_residualMassQ_lt (M : Mealy S) (s : S) (k : ℕ) :
    ∃ N, residualMassQ M s N < 1 / (2 : ℚ)^k := by
  have hp : (0 : ℝ) < 1 / (2 : ℝ)^k := by positivity
  have h := (residualMassQ_tendsto_zero M s).eventually (gt_mem_nhds hp)
  obtain ⟨N,hN⟩ := h.exists
  refine ⟨N, ?_⟩
  apply (Rat.cast_lt (K := ℝ)).mp
  simpa only [Rat.cast_div, Rat.cast_one, Rat.cast_pow, Rat.cast_ofNat] using hN

/-- A terminating exact search for a finite atomic approximation at precision 2^(-k).
    The searched predicate is rational arithmetic on terminating finite programs. -/
def approximationCutoff (M : Mealy S) (s : S) (k : ℕ) : ℕ :=
  Nat.find (exists_residualMassQ_lt M s k)

theorem approximationCutoff_spec (M : Mealy S) (s : S) (k : ℕ) :
    0 ≤ residualMassQ M s (approximationCutoff M s k) ∧
      residualMassQ M s (approximationCutoff M s k) < 1 / (2 : ℚ)^k :=
  ⟨residualMassQ_nonneg M s _, Nat.find_spec (exists_residualMassQ_lt M s k)⟩

/-- The cutoff controls the actual measure omitted from the point-atomic restriction. -/
theorem approximationCutoff_measure_error (M : Mealy S) (s : S) (k : ℕ) :
    law M s (P02A2.positive (law M s) \ partialAtomSet M s (approximationCutoff M s k)) <
      (1/2 : ℝ≥0∞)^k := by
  apply (ENNReal.toReal_lt_toReal (measure_ne_top _ _)
    (ENNReal.pow_ne_top (by norm_num))).mp
  rw [← residualMassQ_correct]
  have h := (approximationCutoff_spec M s k).2
  have hr : (residualMassQ M s (approximationCutoff M s k) : ℝ) < 1 / (2 : ℝ)^k := by
    simpa only [Rat.cast_div, Rat.cast_one, Rat.cast_pow, Rat.cast_ofNat] using
      (Rat.cast_lt (K := ℝ)).mpr h
  simpa [ENNReal.toReal_pow, ENNReal.toReal_div, div_pow] using hr


omit [Nonempty S] in
theorem partialMassQ_mono (M : Mealy S) (s : S) : Monotone (partialMassQ M s) := by
  intro n m hnm
  apply Finset.sum_le_sum_of_subset_of_nonneg (Finset.range_mono hnm)
  intro i hi hiN
  exact atomWeightQ_nonneg M s i

omit [Nonempty S] in
theorem residualMassQ_antitone (M : Mealy S) (s : S) : Antitone (residualMassQ M s) := by
  intro n m hnm
  exact sub_le_sub_left (partialMassQ_mono M s hnm) _

/-- The returned cutoff is a modulus for every later partial approximation as well. -/
theorem approximationCutoff_uniform (M : Mealy S) (s : S) (k N : ℕ)
    (hN : approximationCutoff M s k ≤ N) :
    0 ≤ residualMassQ M s N ∧ residualMassQ M s N < 1 / (2 : ℚ)^k :=
  ⟨residualMassQ_nonneg M s N,
    (residualMassQ_antitone M s hN).trans_lt (approximationCutoff_spec M s k).2⟩

theorem approximationCutoff_uniform_measure_error (M : Mealy S) (s : S) (k N : ℕ)
    (hN : approximationCutoff M s k ≤ N) :
    law M s (P02A2.positive (law M s) \ partialAtomSet M s N) < (1/2 : ℝ≥0∞)^k := by
  apply (ENNReal.toReal_lt_toReal (measure_ne_top _ _)
    (ENNReal.pow_ne_top (by norm_num))).mp
  rw [← residualMassQ_correct]
  have h := (approximationCutoff_uniform M s k N hN).2
  have hr : (residualMassQ M s N : ℝ) < 1 / (2 : ℝ)^k := by
    simpa only [Rat.cast_div, Rat.cast_one, Rat.cast_pow, Rat.cast_ofNat] using
      (Rat.cast_lt (K := ℝ)).mpr h
  simpa [ENNReal.toReal_pow, ENNReal.toReal_div, div_pow] using hr

end Orthemology.Frontier.MealyMeasure
