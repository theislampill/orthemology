import AtomicApproximationFixtures

namespace IndependentAtomicAudit
open Set MeasureTheory
open scoped ENNReal
open Orthemology.Frontier.MealyMeasure
open Orthemology.Frontier.MealyMeasure.Fixtures

/-- Distinct finite descriptions may denote precisely the same infinite output. -/
theorem duplicate_descriptions_same_stream :
    ([] : List Bool) ≠ [false] ∧ atomCandidatesEqual zeroMachine () [] [false] = true := by
  constructor
  · simp
  · apply (atomCandidatesEqual_spec zeroMachine () [] [false]).mpr
    funext n
    rfl

theorem copy_has_no_positive_singletons : P02A2.positive (law copyMachine ()) = ∅ := by
  apply Set.eq_empty_iff_forall_not_mem.mpr
  intro y hy
  have hs : ({y} : Set Cantor) ⊆ P02A2.positive (law copyMachine ()) :=
    Set.singleton_subset_iff.mpr hy
  have hz : law copyMachine () {y} = 0 := measure_mono_null hs copy_atomic_mass_zero
  exact (ne_of_gt hy) hz

/-- Every enumeration index can be skipped; another positive result cannot be promised. -/
theorem atomless_enumeration_always_skips (n : ℕ) : enumerateAtoms copyMachine () n = none := by
  cases h : enumerateAtoms copyMachine () n with
  | none => rfl
  | some p =>
    obtain ⟨u,r⟩ := p
    have hp := (enumerateAtoms_sound copyMachine () n u r h).1
    rw [copy_has_no_positive_singletons] at hp
    exact hp.elim

theorem copy_partial_measure_zero (N : ℕ) : partialPointMeasure copyMachine () N Set.univ = 0 := by
  rw [partialPointMeasure_eq_restrict, Measure.restrict_apply MeasurableSet.univ, Set.univ_inter]
  exact measure_mono_null (partialAtomSet_subset_positive copyMachine () N) copy_atomic_mass_zero

/-- Perfect atomic approximation can still leave the entire diffuse probability law. -/
theorem atomic_approximation_not_full_law (N : ℕ) :
    law copyMachine () Set.univ = 1 ∧ partialPointMeasure copyMachine () N Set.univ = 0 :=
  ⟨measure_univ, copy_partial_measure_zero N⟩

theorem atomless_residual_exact_zero (N : ℕ) : residualMassQ copyMachine () N = 0 := by
  have h := residualMassQ_correct copyMachine () N
  have hz : law copyMachine () (P02A2.positive (law copyMachine ()) \ partialAtomSet copyMachine () N) = 0 :=
    measure_mono_null Set.diff_subset copy_atomic_mass_zero
  rw [hz, ENNReal.toReal_zero] at h
  exact_mod_cast h

#print axioms duplicate_descriptions_same_stream
#print axioms atomless_enumeration_always_skips
#print axioms atomic_approximation_not_full_law
#print axioms atomless_residual_exact_zero
end IndependentAtomicAudit
