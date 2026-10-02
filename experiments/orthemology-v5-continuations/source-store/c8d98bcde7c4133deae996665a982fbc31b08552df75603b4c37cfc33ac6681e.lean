import AuditContractBinding
import RandomisedRepairRegret

namespace IndependentStatisticalControls
open Orthemology.Tranche2 Orthemology.Tranche3
open MeasureTheory Set
open scoped BigOperators ENNReal

theorem upper_includes_tie : rationalUpper 1 1 (1/2) = 1/2 := by
  unfold rationalUpper
  change (∑ w : Bool × Unit, if 1 ≤ rationalCount 1 w then rationalMass 1 (1/2) w else 0) = 1/2
  rw [Fintype.sum_prod_type]
  norm_num [rationalCount,rationalMass]
theorem lower_includes_tie : rationalLower 1 0 (1/2) = 1/2 := by
  unfold rationalLower
  change (∑ w : Bool × Unit, if rationalCount 1 w ≤ 0 then rationalMass 1 (1/2) w else 0) = 1/2
  rw [Fintype.sum_prod_type]
  norm_num [rationalCount,rationalMass]
theorem count_zero_upper_is_one : rationalUpper 1 0 (1/2) = 1 := by
  unfold rationalUpper
  change (∑ w : Bool × Unit, if 0 ≤ rationalCount 1 w then rationalMass 1 (1/2) w else 0) = 1
  rw [Fintype.sum_prod_type]
  norm_num [rationalCount,rationalMass]
theorem degenerate_zero_mass : rationalMass 2 0 (true,(false,())) = 0 := by norm_num [Bits,bitsFintype,rationalUpper,rationalLower,rationalCount,rationalMass,Fintype.sum_prod_type,rationalSpending,auditRepair,referenceLower,referenceUpper,lowerBisect,upperBisect,rationalCertificate,RationalValid,rationalValue,rationalReport]
theorem degenerate_one_mass : rationalMass 2 1 (true,(false,())) = 0 := by norm_num [Bits,bitsFintype,rationalUpper,rationalLower,rationalCount,rationalMass,Fintype.sum_prod_type,rationalSpending,auditRepair,referenceLower,referenceUpper,lowerBisect,upperBisect,rationalCertificate,RationalValid,rationalValue,rationalReport]

theorem zero_precision_outward_lower : referenceLower 4 2 (1/100) 0 = 0 := rfl
theorem zero_precision_outward_upper : referenceUpper 4 2 (1/100) 0 = 1 := rfl
theorem empty_count_lower_exception : referenceLower 0 0 0 8 = 0 := rfl
theorem full_count_upper_exception : referenceUpper 4 4 0 8 = 1 := rfl

theorem finite_precision_tail_bracket (n steps : ℕ) :
    TailBracket n (1/100)
      (fun w => (referenceLower n (rationalCount n w) (1/100) steps : ℝ))
      (fun w => (referenceUpper n (rationalCount n w) (1/100) steps : ℝ)) := by
  convert reference_tailBracket n (1/100) steps (by norm_num) (by norm_num) using 1; norm_num

theorem first_spending_term : rationalSpending (1/20) 0 = 1/80 := by norm_num [Bits,bitsFintype,rationalUpper,rationalLower,rationalCount,rationalMass,Fintype.sum_prod_type,rationalSpending,auditRepair,referenceLower,referenceUpper,lowerBisect,upperBisect,rationalCertificate,RationalValid,rationalValue,rationalReport]
theorem second_spending_term : rationalSpending (1/20) 1 = 1/240 := by norm_num [Bits,bitsFintype,rationalUpper,rationalLower,rationalCount,rationalMass,Fintype.sum_prod_type,rationalSpending,auditRepair,referenceLower,referenceUpper,lowerBisect,upperBisect,rationalCertificate,RationalValid,rationalValue,rationalReport]
theorem first_two_double_spending : 2*rationalSpending (1/20) 0 + 2*rationalSpending (1/20) 1 = 1/30 := by norm_num [Bits,bitsFintype,rationalUpper,rationalLower,rationalCount,rationalMass,Fintype.sum_prod_type,rationalSpending,auditRepair,referenceLower,referenceUpper,lowerBisect,upperBisect,rationalCertificate,RationalValid,rationalValue,rationalReport]

theorem precision_zero_abstains :
    auditRepair (1/20) (fun _ => 0) (fun _ _ => 1/4) (fun _ _ => 0) 0 (true,()) = none := by norm_num [Bits,bitsFintype,rationalUpper,rationalLower,rationalCount,rationalMass,Fintype.sum_prod_type,rationalSpending,auditRepair,referenceLower,referenceUpper,lowerBisect,upperBisect,rationalCertificate,RationalValid,rationalValue,rationalReport]
theorem zero_disturbance_emits :
    auditRepair (1/20) (fun _ => 0) (fun _ _ => 0) (fun _ _ => 0) 0 (true,()) = some (1/2) := by norm_num [Bits,bitsFintype,rationalUpper,rationalLower,rationalCount,rationalMass,Fintype.sum_prod_type,rationalSpending,auditRepair,referenceLower,referenceUpper,lowerBisect,upperBisect,rationalCertificate,RationalValid,rationalValue,rationalReport]
theorem invalid_disturbance_abstains :
    auditRepair (1/20) (fun _ => 0) (fun _ _ => 1/2) (fun _ _ => 100) 0 (true,()) = none := by norm_num [Bits,bitsFintype,rationalUpper,rationalLower,rationalCount,rationalMass,Fintype.sum_prod_type,rationalSpending,auditRepair,referenceLower,referenceUpper,lowerBisect,upperBisect,rationalCertificate,RationalValid,rationalValue,rationalReport]

theorem no_future_input (δ : ℚ) (precision : ℕ → ℕ)
    (disturbance tolerance : (n : ℕ) → Bits (n+1) → ℚ) (n : ℕ)
    (ω ν : ℕ → Bool) (h : ∀ k, k<n+1 → ω k=ν k) :
    auditRepair δ precision disturbance tolerance n (observedPrefix (n+1) ω) =
      auditRepair δ precision disturbance tolerance n (observedPrefix (n+1) ν) := by
  apply congrArg (auditRepair δ precision disturbance tolerance n)
  apply (observedPrefix_eq_iff (n+1) ω (observedPrefix (n+1) ν)).mpr
  intro k hk
  exact (h k hk).trans ((observedPrefix_eq_iff (n+1) ν _).mp rfl k hk)

theorem actual_boundary_prefix_zero :
    (auditSourceLaw 0 (by norm_num) (by norm_num)).map (observedPrefix 1) {(true,())} = 0 := by
  rw [auditSource_prefix_mass]
  norm_num [bernoulliMass,coinMass]

theorem actual_boundary_prefix_one :
    (auditSourceLaw 1 (by norm_num) (by norm_num)).map (observedPrefix 1) {(false,())} = 0 := by
  rw [auditSource_prefix_mass]
  norm_num [bernoulliMass,coinMass]

theorem actual_next_joint :
    auditSourceLaw (1/2) (by norm_num) (by norm_num)
      {ω | observedPrefix 1 ω=(true,()) ∧ ω 1=true} = (1/4 : ℝ≥0∞) := by
  rw [auditSource_next_joint]
  norm_num [bernoulliMass,coinMass,ENNReal.ofReal_div_of_pos]
  rw [← ENNReal.mul_inv]
  all_goals norm_num

theorem realised_loss_not_guaranteed :
    auditCharge (5/8) (3/8) false false > auditCharge (3/4) (1/2) false false := by
  norm_num [auditCharge]

theorem emitted_failures_are_measurable (a : ℝ) (δ : ℚ) (precision : ℕ → ℕ)
    (d t : (n : ℕ) → Bits (n+1) → ℚ) :
    MeasurableSet (AuditRepairFailure a δ precision d t) :=
  auditRepairFailure_measurable a δ precision d t

#eval referenceLower 4 2 (1/100) 8
#eval referenceUpper 4 2 (1/100) 8
#eval referenceLower 4 0 (1/100) 8
#eval referenceUpper 4 4 (1/100) 8
#eval auditRepair (1/20) (fun _ => 8) (fun _ _ => 1/4) (fun _ _ => 1/4) 3 (true,(false,(true,(false,()))))
#eval auditRepair (1/20) (fun _ => 8) (fun _ _ => 1/4) (fun _ _ => 0) 3 (true,(false,(true,(false,()))))
end IndependentStatisticalControls
