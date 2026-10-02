import Mathlib.MeasureTheory.Measure.Typeclasses.SFinite
import Mathlib.MeasureTheory.Measure.AbsolutelyContinuous
import Mathlib.MeasureTheory.Measure.Restrict
import Mathlib.Tactic

open MeasureTheory Set
open scoped ENNReal

namespace Orthemology.Tranche2

/-- A dominated family of experiments can assign positive probability to exact
identification of at most countably many parameter values through one measurable
readout. Domination is an explicit premise, not a claimed property of arbitrary
infinite Bernoulli streams. -/
theorem countable_positive_exact_identification
    {Ω Θ : Type*} [MeasurableSpace Ω] [MeasurableSpace Θ]
    [MeasurableSingletonClass Θ]
    (μ : Measure Ω) [SFinite μ] (ν : Θ → Measure Ω)
    (readout : Ω → Θ) (hreadout : Measurable readout)
    (success : Θ → Set Ω)
    (hcorrect : ∀ θ, success θ ⊆ {ω | readout ω = θ})
    (hdom : ∀ θ, ν θ ≪ μ) :
    Set.Countable {θ | 0 < ν θ (success θ)} := by
  apply (Measure.countable_meas_level_set_pos (μ := μ) hreadout).mono
  intro θ hθ
  change 0 < μ {ω | readout ω = θ}
  by_contra hzero
  have hz : μ {ω | readout ω = θ} = 0 := by
    exact le_antisymm (le_of_not_gt hzero) (zero_le _)
  have hv : ν θ {ω | readout ω = θ} = 0 := hdom θ hz
  have hs : ν θ (success θ) = 0 := measure_mono_null (hcorrect θ) hv
  exact (ne_of_gt hθ) hs

/-- Finite-information use case: the domination hypothesis is only required
on the event F where informative probing eventually stops. -/
theorem countable_positive_identification_on_event
    {Ω Θ : Type*} [MeasurableSpace Ω] [MeasurableSpace Θ]
    [MeasurableSingletonClass Θ]
    (μ : Measure Ω) [IsFiniteMeasure μ] (ν : Θ → Measure Ω)
    (F : Set Ω) (hF : MeasurableSet F)
    (readout : Ω → Θ) (hreadout : Measurable readout)
    (success : Θ → Set Ω)
    (hsF : ∀ θ, success θ ⊆ F)
    (hcorrect : ∀ θ, success θ ⊆ {ω | readout ω = θ})
    (hdom : ∀ θ, (ν θ).restrict F ≪ μ.restrict F) :
    Set.Countable {θ | 0 < ν θ (success θ)} := by
  have h := countable_positive_exact_identification
    (μ.restrict F) (fun θ => (ν θ).restrict F) readout hreadout success hcorrect hdom
  have heq : ∀ θ, (ν θ).restrict F (success θ) = ν θ (success θ) := by
    intro θ
    rw [Measure.restrict_apply' hF]
    rw [Set.inter_eq_left.mpr (hsF θ)]
  simpa only [heq] using h

end Orthemology.Tranche2

namespace Orthemology.Tranche2

/-- Every mixture of measures dominated componentwise by a common family is
dominated by any positive-weight mixture of that family. This is the finite-
transcript representation route, independent of a chosen true parameter. -/
theorem common_components_dominated
    {Ω I : Type*} [MeasurableSpace Ω]
    (κ family : I → Measure Ω) (w : I → ℝ≥0∞)
    (hw : ∀ i, w i ≠ 0) (hfamily : ∀ i, family i ≪ κ i) :
    Measure.sum family ≪ Measure.sum (fun i => w i • κ i) := by
  apply Measure.absolutelyContinuous_sum_left
  intro i
  exact (hfamily i).trans ((Measure.absolutelyContinuous_smul (hw i)).trans
    (Measure.absolutelyContinuous_sum_right i Measure.AbsolutelyContinuous.rfl))

/-- Countable exact-identification obstruction for a common finite-information
component representation. S-finiteness of the reference mixture is explicit. -/
theorem countable_positive_identification_from_components
    {Ω Θ I : Type*} [MeasurableSpace Ω] [MeasurableSpace Θ]
    [MeasurableSingletonClass Θ]
    (κ : I → Measure Ω) (family : Θ → I → Measure Ω) (w : I → ℝ≥0∞)
    (hw : ∀ i, w i ≠ 0)
    [SFinite (Measure.sum (fun i => w i • κ i))]
    (hfamily : ∀ θ i, family θ i ≪ κ i)
    (readout : Ω → Θ) (hreadout : Measurable readout)
    (success : Θ → Set Ω)
    (hcorrect : ∀ θ, success θ ⊆ {ω | readout ω = θ}) :
    Set.Countable {θ | 0 < Measure.sum (family θ) (success θ)} := by
  exact countable_positive_exact_identification
    (Measure.sum (fun i => w i • κ i)) (fun θ => Measure.sum (family θ))
    readout hreadout success hcorrect
    (fun θ => common_components_dominated κ (family θ) w hw (hfamily θ))

end Orthemology.Tranche2

#print axioms Orthemology.Tranche2.countable_positive_exact_identification
#print axioms Orthemology.Tranche2.countable_positive_identification_on_event
#print axioms Orthemology.Tranche2.common_components_dominated
#print axioms Orthemology.Tranche2.countable_positive_identification_from_components
#check Orthemology.Tranche2.countable_positive_identification_from_components
