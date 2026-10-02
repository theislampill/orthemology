import SequentialBinomialTails
import ExecutableAuditRepair

open MeasureTheory Set
open scoped ENNReal
open Orthemology.Tranche2

namespace Orthemology.Tranche3

def sequentialReferenceLower (n k : ℕ) (beta : ℚ) (steps : ℕ) : ℚ :=
  if k=0 then 0 else (lowerBisect (sequentialUpper n k) beta steps (0,1)).1

def sequentialReferenceUpper (n k : ℕ) (beta : ℚ) (steps : ℕ) : ℚ :=
  if n≤k then 1 else (upperBisect (sequentialLower n k) beta steps (0,1)).2

lemma sequentialReferenceLower_eq (n k : ℕ) (beta : ℚ) (steps : ℕ) :
    sequentialReferenceLower n k beta steps = referenceLower n k beta steps := by
  have h : sequentialUpper n k=rationalUpper n k := funext (sequentialUpper_eq n k)
  simp only [sequentialReferenceLower,referenceLower,h]

lemma sequentialReferenceUpper_eq (n k : ℕ) (beta : ℚ) (steps : ℕ) :
    sequentialReferenceUpper n k beta steps = referenceUpper n k beta steps := by
  have h : sequentialLower n k=rationalLower n k := funext (sequentialLower_eq n k)
  simp only [sequentialReferenceUpper,referenceUpper,h]

/-- Sequential exact arithmetic reuses each preceding binomial term. -/
def sequentialAuditRepair (delta : ℚ) (precision : ℕ → ℕ)
    (disturbance tolerance : (n : ℕ) → Bits (n+1) → ℚ)
    (n : ℕ) (w : Bits (n+1)) : Option ℚ :=
  let l := sequentialReferenceLower (n+1) (rationalCount (n+1) w) (rationalSpending delta n) (precision n)
  let u := sequentialReferenceUpper (n+1) (rationalCount (n+1) w) (rationalSpending delta n) (precision n)
  rationalCertificate l u (disturbance n w) (tolerance n w)

/-- Universal source-level refinement, not a finite collection of test cases. -/
theorem sequentialAuditRepair_eq (delta : ℚ) (precision : ℕ → ℕ)
    (disturbance tolerance : (n : ℕ) → Bits (n+1) → ℚ) (n : ℕ) (w : Bits (n+1)) :
    sequentialAuditRepair delta precision disturbance tolerance n w =
      auditRepair delta precision disturbance tolerance n w := by
  simp only [sequentialAuditRepair,auditRepair,sequentialReferenceLower_eq,sequentialReferenceUpper_eq]

/-- The sequential executable procedure inherits the all-time guarantee under
exactly the same actual source law and finite-history input contract. -/
theorem sequential_auditRepair_anytime_sound (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1)
    (delta : ℚ) (hd0 : 0 ≤ delta) (hd1 : delta < 1)
    (precision : ℕ → ℕ) (disturbance tolerance : (n : ℕ) → Bits (n+1) → ℚ) :
    auditSourceLaw a ha0 ha1
      {ω | ∃ n q, sequentialAuditRepair delta precision disturbance tolerance n (observedPrefix (n+1) ω)=some q ∧
        ¬ (0 ≤ (q:ℝ) ∧ (q:ℝ) ≤ 1 ∧
          excessZero a (disturbance n (observedPrefix (n+1) ω)) q ≤ tolerance n (observedPrefix (n+1) ω) ∧
          excessOne a (disturbance n (observedPrefix (n+1) ω)) q ≤ tolerance n (observedPrefix (n+1) ω))} ≤
      ENNReal.ofReal delta := by
  simpa only [sequentialAuditRepair_eq,AuditRepairFailure] using
    executable_auditRepair_anytime_sound a ha0 ha1 delta hd0 hd1 precision disturbance tolerance

end Orthemology.Tranche3

#print axioms Orthemology.Tranche3.sequentialAuditRepair_eq
#print axioms Orthemology.Tranche3.sequential_auditRepair_anytime_sound
