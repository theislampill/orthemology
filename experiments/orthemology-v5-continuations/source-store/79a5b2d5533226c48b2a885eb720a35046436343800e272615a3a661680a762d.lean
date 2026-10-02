import AnytimeRepairCoverage
import RationalTailReference
import RationalRepairCertificate

open MeasureTheory Set
open scoped ENNReal
open Orthemology.Tranche2

namespace Orthemology.Tranche3

def rationalSpending (delta : ℚ) (n : ℕ) : ℚ :=
  delta/(2*((n:ℚ)+1)*((n:ℚ)+2))

lemma rationalSpending_cast (delta : ℚ) (n : ℕ) :
    (rationalSpending delta n : ℝ) = tailSpending delta n := by
  simp only [rationalSpending,tailSpending]
  push_cast
  rfl

lemma rationalSpending_bounds (delta : ℚ) (hd0 : 0 ≤ delta) (hd1 : delta < 1) (n : ℕ) :
    0 ≤ rationalSpending delta n ∧ rationalSpending delta n < 1/2 := by
  have hn : (0:ℚ) ≤ n := by positivity
  have hD : 0 < 2*((n:ℚ)+1)*((n:ℚ)+2) := by positivity
  have hD4 : 4 ≤ 2*((n:ℚ)+1)*((n:ℚ)+2) := by nlinarith
  constructor
  · unfold rationalSpending; positivity
  · unfold rationalSpending
    apply (div_lt_iff₀ hD).mpr
    nlinarith

/-- All inputs are the observed finite word, public rational budgets, and
public precision. No hidden alpha enters this executable function. -/
def auditRepair (delta : ℚ) (precision : ℕ → ℕ)
    (disturbance tolerance : (n : ℕ) → Bits (n+1) → ℚ)
    (n : ℕ) (w : Bits (n+1)) : Option ℚ :=
  let l := referenceLower (n+1) (rationalCount (n+1) w) (rationalSpending delta n) (precision n)
  let u := referenceUpper (n+1) (rationalCount (n+1) w) (rationalSpending delta n) (precision n)
  rationalCertificate l u (disturbance n w) (tolerance n w)

/-- A failure means an actually emitted report violates a stated bound.
Returning none is abstention, not successful repair. -/
def AuditRepairFailure (a : ℝ) (delta : ℚ) (precision : ℕ → ℕ)
    (disturbance tolerance : (n : ℕ) → Bits (n+1) → ℚ) : Set (ℕ → Bool) :=
  {ω | ∃ n q, auditRepair delta precision disturbance tolerance n (observedPrefix (n+1) ω)=some q ∧
    ¬ (0 ≤ (q:ℝ) ∧ (q:ℝ) ≤ 1 ∧
      excessZero a (disturbance n (observedPrefix (n+1) ω)) q ≤ tolerance n (observedPrefix (n+1) ω) ∧
      excessOne a (disturbance n (observedPrefix (n+1) ω)) q ≤ tolerance n (observedPrefix (n+1) ω))}

/-- End-to-end anytime safety for the actual executable reference procedure
under the constructed iid source law, for every real alpha. The tail-bracket,
finite-law and statistical-coverage obligations are derived here. -/
theorem executable_auditRepair_anytime_sound (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1)
    (delta : ℚ) (hd0 : 0 ≤ delta) (hd1 : delta < 1)
    (precision : ℕ → ℕ) (disturbance tolerance : (n : ℕ) → Bits (n+1) → ℚ) :
    auditSourceLaw a ha0 ha1 (AuditRepairFailure a delta precision disturbance tolerance) ≤
      ENNReal.ofReal delta := by
  classical
  let lower : (n : ℕ) → Bits (n+1) → ℝ := fun n w =>
    referenceLower (n+1) (rationalCount (n+1) w) (rationalSpending delta n) (precision n)
  let upper : (n : ℕ) → Bits (n+1) → ℝ := fun n w =>
    referenceUpper (n+1) (rationalCount (n+1) w) (rationalSpending delta n) (precision n)
  have hc : ∀ n, TailBracket (n+1) (tailSpending delta n) (lower n) (upper n) := by
    intro n
    have hb := rationalSpending_bounds delta hd0 hd1 n
    have h := reference_tailBracket (n+1) (rationalSpending delta n) (precision n) hb.1 hb.2
    rwa [rationalSpending_cast] at h
  have hsub : AuditRepairFailure a delta precision disturbance tolerance ⊆
      {ω | ∃ n, a < lower n (observedPrefix (n+1) ω) ∨ upper n (observedPrefix (n+1) ω) < a} := by
    rintro ω ⟨n,q,hout,hbad⟩
    by_contra hn
    have hcover : lower n (observedPrefix (n+1) ω) ≤ a ∧ a ≤ upper n (observedPrefix (n+1) ω) := by
      have hx : ¬ (a < lower n (observedPrefix (n+1) ω) ∨ upper n (observedPrefix (n+1) ω) < a) :=
        fun h => hn ⟨n,h⟩
      simpa only [not_or,not_lt] using hx
    have hg := rationalCertificate_sound _ _ _ _ q hout
    exact hbad ⟨hg.1,hg.2.1,(hg.2.2 a hcover.1 hcover.2).1,(hg.2.2 a hcover.1 hcover.2).2⟩
  exact (measure_mono hsub).trans (auditSource_anytime_coverage a delta ha0 ha1
    (by exact_mod_cast hd0) lower upper hc)


/-- The actual failure event is measurable, not merely controlled in outer measure. -/
theorem auditRepairFailure_measurable (a : ℝ) (delta : ℚ) (precision : ℕ → ℕ)
    (disturbance tolerance : (n : ℕ) → Bits (n+1) → ℚ) :
    MeasurableSet (AuditRepairFailure a delta precision disturbance tolerance) := by
  classical
  simp only [AuditRepairFailure,setOf_exists]
  apply MeasurableSet.iUnion
  intro n
  apply MeasurableSet.iUnion
  intro q
  let E : Set (Bits (n+1)) := {w | auditRepair delta precision disturbance tolerance n w=some q ∧
    ¬ (0 ≤ (q:ℝ) ∧ (q:ℝ) ≤ 1 ∧ excessZero a (disturbance n w) q ≤ tolerance n w ∧
      excessOne a (disturbance n w) q ≤ tolerance n w)}
  exact (Set.toFinite E).measurableSet.preimage (observedPrefix_measurable (n+1))

end Orthemology.Tranche3

#print axioms Orthemology.Tranche3.executable_auditRepair_anytime_sound
#eval Orthemology.Tranche3.auditRepair (1/20) (fun _ => 8)
  (fun _ _ => 1/4) (fun _ _ => 0) 3 (true,(false,(true,(false,()))))

#print axioms Orthemology.Tranche3.auditRepairFailure_measurable
