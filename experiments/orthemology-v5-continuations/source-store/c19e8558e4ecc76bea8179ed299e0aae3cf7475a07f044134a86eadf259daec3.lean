import GroupedBinomialTails
import ExecutableAuditRepair

open MeasureTheory Set
open scoped ENNReal
open Orthemology.Tranche2

namespace Orthemology.Tranche3

def efficientReferenceLower (n k : ℕ) (beta : ℚ) (steps : ℕ) : ℚ :=
  if k=0 then 0 else (lowerBisect (efficientUpper n k) beta steps (0,1)).1

def efficientReferenceUpper (n k : ℕ) (beta : ℚ) (steps : ℕ) : ℚ :=
  if n≤k then 1 else (upperBisect (efficientLower n k) beta steps (0,1)).2

lemma efficientReferenceLower_eq (n k : ℕ) (beta : ℚ) (steps : ℕ) :
    efficientReferenceLower n k beta steps = referenceLower n k beta steps := by
  have h : efficientUpper n k=rationalUpper n k := funext (efficientUpper_eq n k)
  simp only [efficientReferenceLower,referenceLower,h]

lemma efficientReferenceUpper_eq (n k : ℕ) (beta : ℚ) (steps : ℕ) :
    efficientReferenceUpper n k beta steps = referenceUpper n k beta steps := by
  have h : efficientLower n k=rationalLower n k := funext (efficientLower_eq n k)
  simp only [efficientReferenceUpper,referenceUpper,h]

/-- Grouped exact arithmetic replaces enumeration of bit words. -/
def efficientAuditRepair (delta : ℚ) (precision : ℕ → ℕ)
    (disturbance tolerance : (n : ℕ) → Bits (n+1) → ℚ)
    (n : ℕ) (w : Bits (n+1)) : Option ℚ :=
  let l := efficientReferenceLower (n+1) (rationalCount (n+1) w) (rationalSpending delta n) (precision n)
  let u := efficientReferenceUpper (n+1) (rationalCount (n+1) w) (rationalSpending delta n) (precision n)
  rationalCertificate l u (disturbance n w) (tolerance n w)

/-- Universal source-level refinement, not a finite collection of test cases. -/
theorem efficientAuditRepair_eq (delta : ℚ) (precision : ℕ → ℕ)
    (disturbance tolerance : (n : ℕ) → Bits (n+1) → ℚ) (n : ℕ) (w : Bits (n+1)) :
    efficientAuditRepair delta precision disturbance tolerance n w =
      auditRepair delta precision disturbance tolerance n w := by
  simp only [efficientAuditRepair,auditRepair,efficientReferenceLower_eq,efficientReferenceUpper_eq]

/-- The grouped executable procedure inherits the all-time guarantee under
exactly the same actual source law and finite-history input contract. -/
theorem efficient_auditRepair_anytime_sound (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1)
    (delta : ℚ) (hd0 : 0 ≤ delta) (hd1 : delta < 1)
    (precision : ℕ → ℕ) (disturbance tolerance : (n : ℕ) → Bits (n+1) → ℚ) :
    auditSourceLaw a ha0 ha1
      {ω | ∃ n q, efficientAuditRepair delta precision disturbance tolerance n (observedPrefix (n+1) ω)=some q ∧
        ¬ (0 ≤ (q:ℝ) ∧ (q:ℝ) ≤ 1 ∧
          excessZero a (disturbance n (observedPrefix (n+1) ω)) q ≤ tolerance n (observedPrefix (n+1) ω) ∧
          excessOne a (disturbance n (observedPrefix (n+1) ω)) q ≤ tolerance n (observedPrefix (n+1) ω))} ≤
      ENNReal.ofReal delta := by
  simpa only [efficientAuditRepair_eq,AuditRepairFailure] using
    executable_auditRepair_anytime_sound a ha0 ha1 delta hd0 hd1 precision disturbance tolerance

end Orthemology.Tranche3

#print axioms Orthemology.Tranche3.efficientAuditRepair_eq
#print axioms Orthemology.Tranche3.efficient_auditRepair_anytime_sound
#eval Orthemology.Tranche3.efficientReferenceLower 128 64 (1/10000) 16
#eval Orthemology.Tranche3.efficientReferenceUpper 128 64 (1/10000) 16
