import SequentialAuditRepair
import EventualAuditSafety

namespace IndependentEfficientControls
open Orthemology.Tranche3 Orthemology.Tranche2
open MeasureTheory Set
open scoped ENNReal

theorem zero_sample_upper_at_zero : sequentialUpper 0 0 0 = 1 := by
  norm_num [sequentialUpper,sequentialTail,tailSweep]
theorem zero_sample_upper_beyond : sequentialUpper 0 1 0 = 0 := by
  norm_num [sequentialUpper,sequentialTail,tailSweep]
theorem point_one_upper : sequentialUpper 3 3 1 = 1 := by
  norm_num [sequentialUpper,sequentialTail]
theorem point_one_lower_below : sequentialLower 3 2 1 = 0 := by
  norm_num [sequentialLower,sequentialTail]
theorem point_zero_positive_count : sequentialUpper 1 1 0 = 0 := by
  norm_num [sequentialUpper,sequentialTail,tailSweep,nextBinomialTerm]

theorem division_by_one_boundary_is_real :
    nextBinomialTerm 1 0 1 (binomialTerm 1 0 1) = 0 ∧ binomialTerm 1 1 1 = 1 := by
  norm_num [nextBinomialTerm,binomialTerm]

theorem exhausted_sweep_preserves_accumulator (n i : ℕ) (p term acc : ℚ) (keep : ℕ → Bool) :
    tailSweep n p keep 0 i term acc = acc := rfl

theorem sequential_grouped_upper_agree (n k : ℕ) (p : ℚ) :
    sequentialUpper n k p = efficientUpper n k p := by
  rw [sequentialUpper_eq,efficientUpper_eq]
theorem sequential_grouped_lower_agree (n k : ℕ) (p : ℚ) :
    sequentialLower n k p = efficientLower n k p := by
  rw [sequentialLower_eq,efficientLower_eq]

theorem every_finite_precision_agrees (n k steps : ℕ) (beta : ℚ) :
    sequentialReferenceLower n k beta steps = efficientReferenceLower n k beta steps ∧
    sequentialReferenceUpper n k beta steps = efficientReferenceUpper n k beta steps := by
  simp only [sequentialReferenceLower_eq,sequentialReferenceUpper_eq,
    efficientReferenceLower_eq,efficientReferenceUpper_eq,and_self]

theorem invalid_report_input_always_abstains (δ : ℚ) (precision : ℕ → ℕ)
    (n : ℕ) (w : Bits (n+1)) :
    efficientAuditRepair δ precision (fun _ _ => 1/2) (fun _ _ => 100) n w = none := by
  unfold efficientAuditRepair rationalCertificate
  norm_num [RationalValid]

theorem abstention_has_empty_failure (a : ℝ) (δ : ℚ) (precision : ℕ → ℕ) (n : ℕ) :
    AuditStepFailure a δ precision (fun _ _ => 1/2) (fun _ _ => 100) n = ∅ := by
  simp only [AuditStepFailure,invalid_report_input_always_abstains,reduceCtorEq,false_and,exists_false,Set.setOf_false]

def sequentialStepFailure (a : ℝ) (δ : ℚ) (precision : ℕ → ℕ)
    (d t : (n : ℕ) → Bits (n+1) → ℚ) (n : ℕ) : Set (ℕ → Bool) :=
  {ω | ∃ q, sequentialAuditRepair δ precision d t n (observedPrefix (n+1) ω)=some q ∧
    ¬ (0 ≤ (q:ℝ) ∧ (q:ℝ) ≤ 1 ∧
      excessZero a (d n (observedPrefix (n+1) ω)) q ≤ t n (observedPrefix (n+1) ω) ∧
      excessOne a (d n (observedPrefix (n+1) ω)) q ≤ t n (observedPrefix (n+1) ω))}

theorem literal_sequential_failure_eq (a : ℝ) (δ : ℚ) (precision : ℕ → ℕ)
    (d t : (n : ℕ) → Bits (n+1) → ℚ) (n : ℕ) :
    sequentialStepFailure a δ precision d t n = AuditStepFailure a δ precision d t n := by
  simp only [sequentialStepFailure,AuditStepFailure,sequentialAuditRepair_eq,efficientAuditRepair_eq]

theorem literal_sequential_expected_budget (a : ℝ) (ha0 : 0≤a) (ha1 : a≤1)
    (δ : ℚ) (hδ0 : 0≤δ) (hδ1 : δ<1) (precision : ℕ → ℕ)
    (d t : (n : ℕ) → Bits (n+1) → ℚ) :
    (∫⁻ ω, ∑' n, (sequentialStepFailure a δ precision d t n).indicator 1 ω
      ∂auditSourceLaw a ha0 ha1) ≤ ENNReal.ofReal δ := by
  simp_rw [literal_sequential_failure_eq]
  exact expected_incorrect_reports_le a ha0 ha1 δ hδ0 hδ1 precision d t

#eval sequentialUpper 0 0 0
#eval sequentialLower 0 0 1
#eval sequentialUpper 5 3 0
#eval sequentialUpper 5 3 1
#eval sequentialLower 5 3 1
#eval sequentialUpper 4 2 (1/2)
#eval efficientUpper 4 2 (1/2)
#eval rationalUpper 4 2 (1/2)
#eval sequentialReferenceLower 4 2 (1/100) 8
#eval sequentialReferenceUpper 4 2 (1/100) 8
end IndependentEfficientControls
