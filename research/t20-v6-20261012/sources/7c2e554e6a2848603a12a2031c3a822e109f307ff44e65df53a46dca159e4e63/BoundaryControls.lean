import StatisticalRepair
import RepairTestingBridge
import CountableIdentification
import Mathlib.MeasureTheory.Measure.Count
import Mathlib.MeasureTheory.Measure.Lebesgue.Basic
import Mathlib.SetTheory.Cardinal.Continuum

open MeasureTheory Set
open scoped ENNReal BigOperators
open Orthemology.Tranche2

namespace FreshProofAudit

/-- The quantitative necessary decoder bound is not sufficient for successful repair. -/
theorem decoder_radius_not_sufficient :
    |(((21 : ℝ)/32 - 1/2)/(1/4)) - 1/2| ≤ (1:ℝ)/8 ∧
      ¬ BinaryGood (1/2) (1/4) (21/32) := by
  norm_num [BinaryGood, abs_le]

/-- Strictly positive disturbance is essential to disjointness. -/
theorem zero_disturbance_common_repair (a : ℝ) : BinaryGood a 0 (1/2) := by
  constructor <;> dsimp [BinaryGood] <;> ring_nf <;> norm_num

/-- A fixed disturbance admits one successful action for a real interval of norms. -/
theorem nonshrinking_disturbance_common_repair (a : ℝ)
    (ha : (9:ℝ)/20 ≤ a) (hb : a ≤ (7:ℝ)/12) :
    BinaryGood a (1/4) (5/8) := by
  constructor <;> dsimp [BinaryGood] <;> nlinarith

/-- Tolerance proportional to disturbance permits the constant uninformed repair. -/
theorem linear_tolerance_common_repair (a e : ℝ) (ha0 : 0 ≤ a)
    (ha1 : a ≤ 1) (he0 : 0 ≤ e) :
    (1/2:ℝ)^2 ≤ a*(1/2+e)^2+(1-a)*(1/2)^2+e ∧
    (1-(1/2:ℝ))^2 ≤ a*(1/2-e)^2+(1-a)*(1/2)^2+e := by
  have h1 := mul_nonneg ha0 he0
  have h2 := mul_nonneg ha0 (sq_nonneg e)
  have h3 := mul_nonneg (sub_nonneg.mpr ha1) he0
  constructor <;> nlinarith

/-- The known correct norm gives a strict margin equal to a(1-a)e². -/
theorem known_norm_strict_repair (a e : ℝ) (ha0 : 0 < a)
    (ha1 : a < 1) (he0 : 0 < e) :
    (1/2+a*e)^2 < a*(1/2+e)^2+(1-a)*(1/2)^2 ∧
    (1-(1/2+a*e))^2 < a*(1/2-e)^2+(1-a)*(1/2)^2 := by
  have h : 0 < a*(1-a)*e^2 := mul_pos (mul_pos ha0 (sub_pos.mpr ha1)) (sq_pos_of_pos he0)
  constructor <;> nlinarith

/-- With no observations, fair randomization has exact testing risk 1/2;
the formal universal lower bound 1/4 is deliberately weaker, not an equality. -/
theorem zero_sample_fair_test :
    max (errorP (bernoulliMass 0 (1/4)) (fun _ => (1:ℝ)/2))
      (errorQ (bernoulliMass 0 (3/4)) (fun _ => (1:ℝ)/2)) = 1/2 := by
  change max (∑ _ : Unit, (1:ℝ) * (1-1/2)) (∑ _ : Unit, (1:ℝ) * (1/2)) = 1/2
  norm_num

/-- Revealing the parameter by an exact point observation is not dominated
by the usual continuous reference measure. -/
theorem exact_point_observation_not_dominated (a : ℝ) :
    ¬ Measure.dirac a ≪ (volume : Measure ℝ) := by
  intro h
  have hz : (volume : Measure ℝ) {a} = 0 := measure_singleton a
  have hd := h hz
  simpa using hd

/-- Shared output/readout is substantive: parameter-indexed readouts can
fake exact identification with a single identical law for every parameter. -/
theorem parameter_indexed_readout_is_vacuous (a : ℝ) :
    (Measure.dirac (0:ℝ)) {x : ℝ | (fun (_ : ℝ) => a) x = a} = 1 := by
  simp

/-- Without s-finiteness, counting measure dominates every probability law,
including all exact parameter-revealing point laws. -/
theorem every_measure_dominated_by_count (μ : Measure ℝ) :
    μ ≪ (Measure.count : Measure ℝ) := by
  intro s hs
  have he : s = ∅ := Measure.count_eq_zero_iff.mp hs
  simp [he]

/-- This reference is not s-finite, so it cannot instantiate the obstruction. -/
theorem real_counting_measure_not_sfinite :
    ¬ SFinite (Measure.count : Measure ℝ) := by
  intro h
  letI := h
  have hc := Measure.countable_meas_level_set_pos (μ := (Measure.count : Measure ℝ))
    (measurable_id : Measurable (id : ℝ → ℝ))
  have he : {t : ℝ | 0 < (Measure.count : Measure ℝ) {a : ℝ | id a = t}} = Set.univ := by
    ext t
    simp [Measure.count_singleton]
  rw [he] at hc
  exact Cardinal.not_countable_real hc

/-- Dropping strict positivity in the repair lower bound produces a false
statement: every alpha has zero repair failure at zero disturbance. -/
theorem zero_disturbance_zero_failure (n : ℕ) (a : ℝ) :
    repairFailure (bernoulliMass n a) a 0 (fun _ => (1:ℝ)/2) = 0 := by
  have h : BinaryGood a 0 ((1:ℝ)/2) := zero_disturbance_common_repair a
  simp only [repairFailure, h, if_true, mul_zero, Finset.sum_const_zero]

/-- There is no alternative s-finite reference that dominates the entire
continuum of exact parameter-revealing point laws. -/
theorem no_sfinite_reference_for_all_point_laws :
    ¬ ∃ μ : Measure ℝ, SFinite μ ∧ ∀ a : ℝ, Measure.dirac a ≪ μ := by
  rintro ⟨μ, hμ, hdom⟩
  letI := hμ
  have hc := countable_positive_exact_identification μ (fun a : ℝ => Measure.dirac a)
    id measurable_id (fun a : ℝ => {a}) (by intro a; simp) hdom
  have he : {a : ℝ | 0 < (Measure.dirac a) {a}} = Set.univ := by
    ext a
    simp
  rw [he] at hc
  exact Cardinal.not_countable_real hc

#print axioms zero_disturbance_zero_failure
#print axioms no_sfinite_reference_for_all_point_laws
#print axioms every_measure_dominated_by_count
#print axioms real_counting_measure_not_sfinite
#print axioms decoder_radius_not_sufficient
#print axioms zero_disturbance_common_repair
#print axioms nonshrinking_disturbance_common_repair
#print axioms linear_tolerance_common_repair
#print axioms known_norm_strict_repair
#print axioms zero_sample_fair_test
#print axioms exact_point_observation_not_dominated
#print axioms parameter_indexed_readout_is_vacuous

end FreshProofAudit
