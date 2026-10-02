import TotalVariation
import P02A2.Observation

open Set MeasureTheory Filter
open scoped ENNReal

namespace OrthemologyMeasure

variable {Ω α : Type*} [MeasurableSpace Ω] [MeasurableSpace α]
variable (μ ν : Measure Ω) [IsFiniteMeasure μ] [IsFiniteMeasure ν]

noncomputable def observedSupport (f : Ω → α) : Set Ω :=
  f ⁻¹' P02A2.positive (μ.map f)

noncomputable def commonObservedSupport (f : Ω → α) : Set Ω :=
  observedSupport μ f ∪ observedSupport ν f

theorem observedSupport_measurable [MeasurableSingletonClass α]
    {f : Ω → α} (hf : Measurable f) : MeasurableSet (observedSupport μ f) :=
  (P02A2.positive_measurable (μ.map f)).preimage hf

theorem commonObservedSupport_measurable [MeasurableSingletonClass α]
    {f : Ω → α} (hf : Measurable f) :
    MeasurableSet (commonObservedSupport μ ν f) :=
  (observedSupport_measurable μ hf).union (observedSupport_measurable ν hf)

/-- Adding the other law's countable positive support changes no event under this law. -/
theorem observedSupport_ae_common_left [MeasurableSingletonClass α]
    {f : Ω → α} (hf : Measurable f) :
    observedSupport μ f =ᵐ[μ] commonObservedSupport μ ν f := by
  have hs : observedSupport μ f ⊆ commonObservedSupport μ ν f := subset_union_left
  apply ae_eq_set.mpr
  constructor
  · rw [Set.diff_eq_empty.mpr hs]
    exact measure_empty
  · let C := P02A2.positive (μ.map f) ∪ P02A2.positive (ν.map f)
    have hc : C.Countable := (P02A2.positive_countable (μ.map f)).union
      (P02A2.positive_countable (ν.map f))
    change μ (f ⁻¹' (C \ P02A2.positive (μ.map f))) = 0
    rw [← Measure.map_apply hf (hc.measurableSet.diff
      (P02A2.positive_measurable (μ.map f)))]
    exact P02A2.countable_sdiff_positive_null (μ.map f) hc

theorem observedSupport_ae_common_right [MeasurableSingletonClass α]
    {f : Ω → α} (hf : Measurable f) :
    observedSupport ν f =ᵐ[ν] commonObservedSupport μ ν f := by
  simpa only [commonObservedSupport, union_comm] using
    observedSupport_ae_common_left ν μ hf

theorem ae_iInter {ι : Type*} [Countable ι] {A B : ι → Set Ω}
    (h : ∀ n, A n =ᵐ[μ] B n) : (⋂ n, A n) =ᵐ[μ] (⋂ n, B n) := by
  filter_upwards [ae_all_iff.mpr h] with ω hω
  apply propext
  constructor
  · intro hx
    exact mem_iInter.mpr (fun i => Eq.mp (hω i) (mem_iInter.mp hx i))
  · intro hx
    exact mem_iInter.mpr (fun i => Eq.mpr (hω i) (mem_iInter.mp hx i))

section History
variable {Q : ℕ → Type*} [∀ n, MeasurableSpace (Q n)]
  [∀ n, MeasurableSingletonClass (Q n)]

noncomputable def ownResidual (Y : ∀ n, Ω → Q n) : Set Ω :=
  (⋂ n, P02A2.Observation.event μ Y n) \ P02A2.Observation.fullEvent μ Y

noncomputable def commonResidual (Y : ∀ n, Ω → Q n) : Set Ω :=
  (⋂ n, commonObservedSupport μ ν (Y n)) \
    commonObservedSupport μ ν (P02A2.Observation.history Y)

theorem commonResidual_measurable {Y : ∀ n, Ω → Q n}
    (hY : ∀ n, Measurable (Y n)) : MeasurableSet (commonResidual μ ν Y) := by
  exact (MeasurableSet.iInter fun n => commonObservedSupport_measurable μ ν (hY n)).diff
    (commonObservedSupport_measurable μ ν (P02A2.Observation.history_measurable hY))

theorem ownResidual_ae_common_left {Y : ∀ n, Ω → Q n}
    (hY : ∀ n, Measurable (Y n)) :
    ownResidual μ Y =ᵐ[μ] commonResidual μ ν Y := by
  exact ae_eq_set_diff
    (ae_iInter μ fun n => observedSupport_ae_common_left μ ν (hY n))
    (observedSupport_ae_common_left μ ν (P02A2.Observation.history_measurable hY))

theorem ownResidual_ae_common_right {Y : ∀ n, Ω → Q n}
    (hY : ∀ n, Measurable (Y n)) :
    ownResidual ν Y =ᵐ[ν] commonResidual μ ν Y := by
  exact ae_eq_set_diff
    (ae_iInter ν fun n => observedSupport_ae_common_right μ ν (hY n))
    (observedSupport_ae_common_right μ ν (P02A2.Observation.history_measurable hY))

/-- Stability of the actual law-dependent infinite residual via one common measurable event. -/
theorem residual_eventTV_bound {Y : ∀ n, Ω → Q n}
    (hY : ∀ n, Measurable (Y n)) :
    |(μ (ownResidual μ Y)).toReal - (ν (ownResidual ν Y)).toReal| ≤ eventTV μ ν := by
  have hm := measure_congr (ownResidual_ae_common_left μ ν hY)
  have hn := measure_congr (ownResidual_ae_common_right μ ν hY)
  rw [hm, hn]
  exact measurable_event_le_eventTV μ ν _ (commonResidual_measurable μ ν hY)

end History
end OrthemologyMeasure

#print axioms OrthemologyMeasure.observedSupport_ae_common_left
#print axioms OrthemologyMeasure.ownResidual_ae_common_left
#print axioms OrthemologyMeasure.residual_eventTV_bound
