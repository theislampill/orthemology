import P02A2.MeasureCore
import Mathlib.MeasureTheory.Measure.Typeclasses.NoAtoms

open Set MeasureTheory
open scoped ENNReal

namespace OrthemologyMeasure

variable {X Y : Type*} [MeasurableSpace X] [MeasurableSpace Y]

/-- Event-supremum convention for total variation, without the factor two of signed variation. -/
noncomputable def eventTV (μ ν : Measure X) : ℝ :=
  sSup (Set.range fun s : {s : Set X // MeasurableSet s} =>
    |(μ s.val).toReal - (ν s.val).toReal|)

theorem eventTV_range_bddAbove (μ ν : Measure X) [IsFiniteMeasure μ]
    [IsFiniteMeasure ν] :
    BddAbove (Set.range fun s : {s : Set X // MeasurableSet s} =>
      |(μ s.val).toReal - (ν s.val).toReal|) := by
  refine ⟨(μ univ).toReal + (ν univ).toReal, ?_⟩
  rintro r ⟨s, rfl⟩
  have ha := ENNReal.toReal_nonneg (a := μ s.val)
  have hb := ENNReal.toReal_nonneg (a := ν s.val)
  have hau := ENNReal.toReal_mono (measure_ne_top μ univ)
    (measure_mono (subset_univ s.val))
  have hbu := ENNReal.toReal_mono (measure_ne_top ν univ)
    (measure_mono (subset_univ s.val))
  exact abs_sub_le_iff.mpr ⟨by linarith, by linarith⟩

theorem measurable_event_le_eventTV (μ ν : Measure X) [IsFiniteMeasure μ]
    [IsFiniteMeasure ν] (s : Set X) (hs : MeasurableSet s) :
    |(μ s).toReal - (ν s).toReal| ≤ eventTV μ ν := by
  exact le_csSup (eventTV_range_bddAbove μ ν) ⟨⟨s, hs⟩, rfl⟩

theorem eventTV_le_iff (μ ν : Measure X) [IsFiniteMeasure μ]
    [IsFiniteMeasure ν] (δ : ℝ) :
    eventTV μ ν ≤ δ ↔ ∀ s : Set X, MeasurableSet s →
      |(μ s).toReal - (ν s).toReal| ≤ δ := by
  constructor
  · intro h s hs
    exact (measurable_event_le_eventTV μ ν s hs).trans h
  · intro h
    apply csSup_le
    · exact ⟨_, ⟨⟨∅, MeasurableSet.empty⟩, rfl⟩⟩
    · rintro r ⟨s, rfl⟩
      exact h s.val s.property

theorem eventTV_nonnegative (μ ν : Measure X) [IsFiniteMeasure μ]
    [IsFiniteMeasure ν] : 0 ≤ eventTV μ ν := by
  simpa using measurable_event_le_eventTV μ ν ∅ MeasurableSet.empty

/-- Measurable observation cannot increase full-law event total variation. -/
theorem eventTV_map_le (μ ν : Measure X) [IsFiniteMeasure μ]
    [IsFiniteMeasure ν] {f : X → Y} (hf : Measurable f) :
    eventTV (μ.map f) (ν.map f) ≤ eventTV μ ν := by
  apply (eventTV_le_iff _ _ _).mpr
  intro s hs
  rw [Measure.map_apply hf hs, Measure.map_apply hf hs]
  exact measurable_event_le_eventTV μ ν (f ⁻¹' s) (hf hs)

/-- The actual positive-singleton defect is one-Lipschitz in event total variation. -/
theorem defect_eventTV_bound [MeasurableSingletonClass X]
    (μ ν : Measure X) [IsFiniteMeasure μ] [IsFiniteMeasure ν] :
    |P02A2.defect μ - P02A2.defect ν| ≤ eventTV μ ν := by
  let C : Set X := P02A2.positive μ ∪ P02A2.positive ν
  have hc : C.Countable := (P02A2.positive_countable μ).union
    (P02A2.positive_countable ν)
  have hm : P02A2.mass μ = μ C :=
    P02A2.mass_eq_countable_superset μ hc subset_union_left
  have hn : P02A2.mass ν = ν C :=
    P02A2.mass_eq_countable_superset ν hc subset_union_right
  have he := measurable_event_le_eventTV μ ν C hc.measurableSet
  unfold P02A2.defect
  rw [hm, hn]
  have algebra : (1 - (μ C).toReal) - (1 - (ν C).toReal) =
      -((μ C).toReal - (ν C).toReal) := by ring
  rw [algebra, abs_neg]
  exact he

end OrthemologyMeasure

#print axioms OrthemologyMeasure.eventTV_range_bddAbove
#print axioms OrthemologyMeasure.measurable_event_le_eventTV
#print axioms OrthemologyMeasure.eventTV_le_iff
#print axioms OrthemologyMeasure.eventTV_map_le
#print axioms OrthemologyMeasure.defect_eventTV_bound
