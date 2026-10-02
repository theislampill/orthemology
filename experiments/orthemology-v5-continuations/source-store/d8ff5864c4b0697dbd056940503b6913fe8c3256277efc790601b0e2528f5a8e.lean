import StackActionLaw
import RecurrentSupport
import Mathlib.Probability.BorelCantelli

noncomputable section
open MeasureTheory ProbabilityTheory Filter Set
open scoped BigOperators ENNReal
open Orthemology.Tranche2 Orthemology.Tranche2.PolicyEmbedding

namespace HiddenParity.Adaptive
universe u v
variable {A Y : Type u} {R : Type v}
variable [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
variable [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
variable [MeasurableSpace Y] [MeasurableSingletonClass Y]

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] in
/-- Under the actual independent stack experiment, every positive-probability
symbol occurs infinitely in a fixed raw pair tape. No adaptive sample-count
conditioning is used. -/
theorem seeded_tape_positive_symbol_recurs
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (a : A) (y : Y) (hPos : 0 < P a y) :
    ∀ᵐ z ∂ρ.prod (stackMeasure P hP hN), ∃ᶠ n in atTop, seededStackCoordinate a n z = y := by
  let μ := ρ.prod (stackMeasure P hP hN)
  let events : ℕ → Set (R × FlatStack A Y) := fun n => {z | seededStackCoordinate a n z = y}
  have hMeas : ∀ n, MeasurableSet (events n) := fun n =>
    (measurableSet_singleton y).preimage (seededStackCoordinate_measurable a n)
  have hFun := (seededStackCoordinates_independent ρ P hP hN).precomp
    (show Function.Injective (fun n : ℕ => (a,n)) from fun _ _ h => congrArg Prod.snd h)
  have hInd : iIndepSet events μ := by
    rw [iIndepSet_iff_meas_biInter hMeas]
    intro I
    exact hFun.measure_inter_preimage_eq_mul I (fun _ _ => measurableSet_singleton y)
  have hMass : ∀ n, μ (events n) = ENNReal.ofReal (P a y) := by
    intro n
    change (ρ.prod (stackMeasure P hP hN)) (seededStackCoordinate a n ⁻¹' {y}) = _
    rw [← Measure.map_apply (seededStackCoordinate_measurable a n) (measurableSet_singleton y),
      seededStackCoordinate_law ρ P hP hN, actionMeasure_singleton]
  have hSum : (∑' n, μ (events n)) = ∞ := by
    simp_rw [hMass]
    exact ENNReal.tsum_const_eq_top_of_ne_zero (ENNReal.ofReal_pos.mpr hPos).ne'
  have hOne := measure_limsup_eq_one hMeas hInd hSum
  have hEvent : limsup events atTop = {z | ∃ᶠ n in atTop, seededStackCoordinate a n z = y} := by
    ext z
    simp only [limsup_eq_iInf_iSup_of_nat, Set.iInf_eq_iInter, Set.iSup_eq_iUnion,
      Set.mem_iInter, Set.mem_iUnion, Set.mem_setOf_eq, frequently_atTop, events, exists_prop]
  have hRecMeas : MeasurableSet {z : R × FlatStack A Y |
      ∃ᶠ n in atTop, seededStackCoordinate a n z = y} :=
    Orthemology.Tranche2.RecurrentSupport.measurable_recurrence
      (fun z n => seededStackCoordinate a n z) (fun n => seededStackCoordinate_measurable a n) y
  apply (ae_iff_measure_eq hRecMeas.nullMeasurableSet).mpr
  rw [measure_univ]
  rwa [hEvent] at hOne

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] in
/-- This probability-one raw-tape event is uniform over all pairs and symbols,
and does not depend on which causal policy later consumes them. -/
theorem seeded_all_tapes_recurrent
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) :
    ∀ᵐ z ∂ρ.prod (stackMeasure P hP hN),
      ∀ a y, 0 < P a y → ∃ᶠ n in atTop, seededStackCoordinate a n z = y := by
  apply ae_all_iff.mpr
  intro a
  apply ae_all_iff.mpr
  intro y
  by_cases h : 0 < P a y
  · exact (seeded_tape_positive_symbol_recurs ρ P hP hN a y h).mono (fun _ hx _ => hx)
  · exact ae_of_all _ (fun _ hx => (h hx).elim)

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] in
/-- Every actually sampled raw symbol lies in its row's positive support. -/
theorem seeded_all_tapes_supported
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) :
    ∀ᵐ z ∂ρ.prod (stackMeasure P hP hN), ∀ a n, 0 < P a (seededStackCoordinate a n z) := by
  classical
  have hZero : ∀ a n y, P a y = 0 →
      ∀ᵐ z ∂ρ.prod (stackMeasure P hP hN), seededStackCoordinate a n z ≠ y := by
    intro a n y hz
    rw [ae_iff]
    simp only [not_not]
    change (ρ.prod (stackMeasure P hP hN)) (seededStackCoordinate a n ⁻¹' {y}) = 0
    rw [← Measure.map_apply (seededStackCoordinate_measurable a n) (measurableSet_singleton y),
      seededStackCoordinate_law ρ P hP hN, actionMeasure_singleton, hz, ENNReal.ofReal_zero]
  have hAll : ∀ᵐ z ∂ρ.prod (stackMeasure P hP hN),
      ∀ a n y, P a y = 0 → seededStackCoordinate a n z ≠ y := by
    apply ae_all_iff.mpr
    intro a
    apply ae_all_iff.mpr
    intro n
    apply ae_all_iff.mpr
    intro y
    by_cases hz : P a y = 0
    · exact (hZero a n y hz).mono (fun _ h _ => h)
    · exact ae_of_all _ (fun _ h => (hz h).elim)
  filter_upwards [hAll] with z hz
  intro a n
  by_contra hn
  have hp : P a (seededStackCoordinate a n z) = 0 :=
    le_antisymm (le_of_not_gt hn) (hP a _)
  exact hz a n _ hp rfl

end HiddenParity.Adaptive
