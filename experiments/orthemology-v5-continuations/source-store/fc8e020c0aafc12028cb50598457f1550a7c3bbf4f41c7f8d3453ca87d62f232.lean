import EfficientAuditRepair
import Mathlib.MeasureTheory.OuterMeasure.BorelCantelli
import Mathlib.MeasureTheory.Integral.Lebesgue.Add

open MeasureTheory Set Filter
open scoped ENNReal
open Orthemology.Tranche2

namespace Orthemology.Tranche3
noncomputable section

/-- An incorrect report was actually emitted at this opportunity. Abstention
is excluded from this event, not identified with a successful correction. -/
def AuditStepFailure (a : ℝ) (delta : ℚ) (precision : ℕ → ℕ)
    (disturbance tolerance : (n : ℕ) → Bits (n+1) → ℚ) (n : ℕ) : Set (ℕ → Bool) :=
  {ω | ∃ q, efficientAuditRepair delta precision disturbance tolerance n (observedPrefix (n+1) ω)=some q ∧
    ¬ (0 ≤ (q:ℝ) ∧ (q:ℝ) ≤ 1 ∧
      excessZero a (disturbance n (observedPrefix (n+1) ω)) q ≤ tolerance n (observedPrefix (n+1) ω) ∧
      excessOne a (disturbance n (observedPrefix (n+1) ω)) q ≤ tolerance n (observedPrefix (n+1) ω))}

lemma auditStepFailure_measurable (a : ℝ) (delta : ℚ) (precision : ℕ → ℕ)
    (disturbance tolerance : (n : ℕ) → Bits (n+1) → ℚ) (n : ℕ) :
    MeasurableSet (AuditStepFailure a delta precision disturbance tolerance n) := by
  classical
  simp only [AuditStepFailure,setOf_exists]
  apply MeasurableSet.iUnion
  intro q
  let E : Set (Bits (n+1)) := {w | efficientAuditRepair delta precision disturbance tolerance n w=some q ∧
    ¬ (0 ≤ (q:ℝ) ∧ (q:ℝ) ≤ 1 ∧ excessZero a (disturbance n w) q ≤ tolerance n w ∧
      excessOne a (disturbance n w) q ≤ tolerance n w)}
  exact (Set.toFinite E).measurableSet.preimage (observedPrefix_measurable (n+1))

lemma auditStepFailure_bound (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1)
    (delta : ℚ) (hd0 : 0 ≤ delta) (hd1 : delta < 1)
    (precision : ℕ → ℕ) (disturbance tolerance : (n : ℕ) → Bits (n+1) → ℚ) (n : ℕ) :
    auditSourceLaw a ha0 ha1 (AuditStepFailure a delta precision disturbance tolerance n) ≤
      ENNReal.ofReal (2*tailSpending delta n) := by
  classical
  let l : Bits (n+1) → ℝ := fun w => referenceLower (n+1) (rationalCount (n+1) w) (rationalSpending delta n) (precision n)
  let u : Bits (n+1) → ℝ := fun w => referenceUpper (n+1) (rationalCount (n+1) w) (rationalSpending delta n) (precision n)
  have hb := rationalSpending_bounds delta hd0 hd1 n
  have hc : TailBracket (n+1) (tailSpending delta n) l u := by
    have h := reference_tailBracket (n+1) (rationalSpending delta n) (precision n) hb.1 hb.2
    rwa [rationalSpending_cast] at h
  have hs : AuditStepFailure a delta precision disturbance tolerance n ⊆
      {ω | a < l (observedPrefix (n+1) ω) ∨ u (observedPrefix (n+1) ω) < a} := by
    rintro ω ⟨q,hout,hbad⟩
    by_contra h
    have hv : l (observedPrefix (n+1) ω) ≤ a ∧ a ≤ u (observedPrefix (n+1) ω) := by
      simpa only [Set.mem_setOf_eq,not_or,not_lt] using h
    rw [efficientAuditRepair_eq] at hout
    have hg := rationalCertificate_sound _ _ _ _ q hout
    exact hbad ⟨hg.1,hg.2.1,(hg.2.2 a hv.1 hv.2).1,(hg.2.2 a hv.1 hv.2).2⟩
  exact (measure_mono hs).trans (auditSource_interval_failure a _ ha0 ha1 (n+1)
    (tailSpending_nonneg delta (by exact_mod_cast hd0) n) l u hc)

/-- Expected total number of incorrect emitted reports is at most delta.
This does not count abstentions, latency, or the time of the last mistake. -/
theorem expected_incorrect_reports_le (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1)
    (delta : ℚ) (hd0 : 0 ≤ delta) (hd1 : delta < 1)
    (precision : ℕ → ℕ) (disturbance tolerance : (n : ℕ) → Bits (n+1) → ℚ) :
    (∫⁻ ω, ∑' n, (AuditStepFailure a delta precision disturbance tolerance n).indicator 1 ω
      ∂auditSourceLaw a ha0 ha1) ≤ ENNReal.ofReal delta := by
  rw [lintegral_tsum (f := fun n => (AuditStepFailure a delta precision disturbance tolerance n).indicator
      (1 : (ℕ → Bool) → ℝ≥0∞)) (fun n =>
    ((show Measurable (1 : (ℕ → Bool) → ℝ≥0∞) from measurable_const).indicator
      (auditStepFailure_measurable a delta precision disturbance tolerance n)).aemeasurable)]
  simp_rw [lintegral_indicator_one (auditStepFailure_measurable a delta precision disturbance tolerance _)]
  exact (ENNReal.tsum_le_tsum (fun n => auditStepFailure_bound a ha0 ha1 delta hd0 hd1 precision disturbance tolerance n)).trans
    (spending_total_le delta (by exact_mod_cast hd0))

/-- Almost surely only finitely many emitted reports are incorrect.
There is deliberately no assertion that a report is eventually emitted. -/
theorem eventually_no_incorrect_emissions (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1)
    (delta : ℚ) (hd0 : 0 ≤ delta) (hd1 : delta < 1)
    (precision : ℕ → ℕ) (disturbance tolerance : (n : ℕ) → Bits (n+1) → ℚ) :
    ∀ᵐ ω ∂auditSourceLaw a ha0 ha1, ∀ᶠ n in atTop,
      ω ∉ AuditStepFailure a delta precision disturbance tolerance n := by
  apply ae_eventually_not_mem
  have hs := (ENNReal.tsum_le_tsum (fun n => auditStepFailure_bound a ha0 ha1 delta hd0 hd1 precision disturbance tolerance n)).trans
    (spending_total_le delta (by exact_mod_cast hd0))
  exact ne_top_of_le_ne_top ENNReal.ofReal_ne_top hs

end
end Orthemology.Tranche3

#print axioms Orthemology.Tranche3.expected_incorrect_reports_le
#print axioms Orthemology.Tranche3.eventually_no_incorrect_emissions
