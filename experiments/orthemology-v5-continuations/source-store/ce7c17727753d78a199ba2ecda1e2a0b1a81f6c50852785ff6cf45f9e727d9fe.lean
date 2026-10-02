import RobustBinaryRepair
import Mathlib.MeasureTheory.Measure.MeasureSpaceDef

open MeasureTheory Set

namespace Orthemology.Tranche3

/-- One pathwise simultaneous interval coverage event. -/
def IntervalCoverage {Ω : Type*} (a : ℝ) (lower upper : Ω → ℕ → ℝ) : Set Ω :=
  {w | ∀ n, lower w n ≤ a ∧ a ≤ upper w n}

/-- Every certificate that is issued on this path is sound. Uncertified
opportunities are not silently counted as successful repair. -/
def AllCertificatesSound {Ω : Type*} (a : ℝ)
    (lower upper disturbance tolerance : Ω → ℕ → ℝ) : Set Ω :=
  {w | ∀ n, robustValue (lower w n) (upper w n) (disturbance w n) ≤ tolerance w n →
    let q := robustReport (lower w n) (upper w n) (disturbance w n)
    0 ≤ q ∧ q ≤ 1 ∧ excessZero a (disturbance w n) q ≤ tolerance w n ∧
      excessOne a (disturbance w n) q ≤ tolerance w n}

/-- Pathwise safety requires only coverage on this path. There is no sampling,
independence, optional-stopping or termination assumption in this implication. -/
theorem coverage_subset_sound {Ω : Type*} (a : ℝ)
    (lower upper disturbance tolerance : Ω → ℕ → ℝ)
    (valid : ∀ w n, 0 ≤ lower w n ∧ upper w n ≤ 1 ∧
      0 ≤ disturbance w n ∧ disturbance w n ≤ 1/4) :
    IntervalCoverage a lower upper ⊆ AllCertificatesSound a lower upper disturbance tolerance := by
  intro w hw n hn
  exact covered_certificate_sound a
    (fun (_ : Unit) n => lower w n) (fun (_ : Unit) n => upper w n)
    (fun (_ : Unit) n => disturbance w n) (fun (_ : Unit) n => tolerance w n)
    (fun _ n => hw n) (fun _ n => valid w n) () n hn

/-- Any established simultaneous coverage error bound transfers unchanged to
all certified repairs, including data-dependent selection among them.
This is a measure bound (valid even as an outer-measure bound); it does not
establish the statistical coverage premise. -/
theorem certificate_failure_measure_le {Ω : Type*} [MeasurableSpace Ω]
    (μ : Measure Ω) (a : ℝ) (lower upper disturbance tolerance : Ω → ℕ → ℝ)
    (valid : ∀ w n, 0 ≤ lower w n ∧ upper w n ≤ 1 ∧
      0 ≤ disturbance w n ∧ disturbance w n ≤ 1/4) :
    μ (AllCertificatesSound a lower upper disturbance tolerance)ᶜ ≤
      μ (IntervalCoverage a lower upper)ᶜ := by
  apply measure_mono
  exact compl_subset_compl.mpr (coverage_subset_sound a lower upper disturbance tolerance valid)

end Orthemology.Tranche3

#print axioms Orthemology.Tranche3.coverage_subset_sound
#print axioms Orthemology.Tranche3.certificate_failure_measure_le
