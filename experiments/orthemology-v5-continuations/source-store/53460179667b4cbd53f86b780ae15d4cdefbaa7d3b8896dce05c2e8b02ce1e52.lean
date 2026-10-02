import BernoulliPrefixLaw
import CertifiedRepairCoverage

open MeasureTheory Set
open scoped BigOperators ENNReal
open Orthemology.Tranche2

namespace Orthemology.Tranche3
noncomputable section

/-- Exact probability of any finite-word event under the actual source. -/
theorem auditSource_word_event (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1)
    (n : ℕ) (E : Bits n → Prop) [DecidablePred E] :
    auditSourceLaw a ha0 ha1 {ω | E (observedPrefix n ω)} =
      ENNReal.ofReal (∑ w, if E w then bernoulliMass n a w else 0) := by
  classical
  let S := Finset.univ.filter E
  have hset : {ω | E (observedPrefix n ω)} = observedPrefix n ⁻¹' (S : Set (Bits n)) := by
    ext ω; simp [S]
  rw [hset,← Measure.map_apply (observedPrefix_measurable n) (by exact S.measurableSet),
    ← sum_measure_singleton]
  simp_rw [auditSource_prefix_mass]
  rw [← ENNReal.ofReal_sum_of_nonneg (fun w _ => bernoulliMass_nonneg n a ha0 ha1 w)]
  congr 1
  simp [S,Finset.sum_filter]

/-- Coverage failure at a single sample count has the certified tail budget. -/
theorem auditSource_interval_failure (a beta : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1)
    (n : ℕ) (hb : 0 ≤ beta) (lower upper : Bits n → ℝ)
    (hc : TailBracket n beta lower upper) :
    auditSourceLaw a ha0 ha1 {ω | a < lower (observedPrefix n ω) ∨ upper (observedPrefix n ω) < a} ≤
      ENNReal.ofReal (2*beta) := by
  classical
  rw [auditSource_word_event a ha0 ha1 n (fun w => a < lower w ∨ upper w < a)]
  exact ENNReal.ofReal_le_ofReal (bernoulli_interval_coverage n a beta ha0 ha1 hb lower upper hc)

/-- The first term refers to one observed draw. -/
def tailSpending (delta : ℝ) (n : ℕ) : ℝ :=
  delta / (2*((n:ℝ)+1)*((n:ℝ)+2))

lemma tailSpending_nonneg (delta : ℝ) (hd : 0 ≤ delta) (n : ℕ) :
    0 ≤ tailSpending delta n := by unfold tailSpending; positivity

lemma double_tailSpending (delta : ℝ) (n : ℕ) :
    2*tailSpending delta n = delta / (((n:ℝ)+1)*((n:ℝ)+2)) := by
  unfold tailSpending
  have h1 : (n:ℝ)+1 ≠ 0 := by positivity
  have h2 : (n:ℝ)+2 ≠ 0 := by positivity
  field_simp
  ring

lemma spending_partial_sum (delta : ℝ) (N : ℕ) :
    (∑ n ∈ Finset.range N, 2*tailSpending delta n) = delta-delta/((N:ℝ)+1) := by
  induction N with
  | zero => simp
  | succ N ih =>
      rw [Finset.sum_range_succ,ih,double_tailSpending]
      push_cast
      have h1 : (N:ℝ)+1 ≠ 0 := by positivity
      have h2 : (N:ℝ)+2 ≠ 0 := by positivity
      field_simp
      ring

lemma spending_total_le (delta : ℝ) (hd : 0 ≤ delta) :
    (∑' n, ENNReal.ofReal (2*tailSpending delta n)) ≤ ENNReal.ofReal delta := by
  apply ENNReal.tsum_le_of_sum_range_le
  intro N
  rw [← ENNReal.ofReal_sum_of_nonneg (fun n _ => mul_nonneg (by norm_num) (tailSpending_nonneg delta hd n)),
    spending_partial_sum]
  apply ENNReal.ofReal_le_ofReal
  have h : 0 ≤ delta/((N:ℝ)+1) := by positivity
  linarith

/-- One actual infinite Bernoulli experiment, with every finite interval checked
by exact tail inequalities, has simultaneous coverage error at most delta.
No independent coverage, finite-prefix law, or optional-stopping premise remains. -/
theorem auditSource_anytime_coverage (a delta : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1)
    (hd : 0 ≤ delta) (lower upper : (n : ℕ) → Bits (n+1) → ℝ)
    (hc : ∀ n, TailBracket (n+1) (tailSpending delta n) (lower n) (upper n)) :
    auditSourceLaw a ha0 ha1
      {ω | ∃ n, a < lower n (observedPrefix (n+1) ω) ∨ upper n (observedPrefix (n+1) ω) < a} ≤
      ENNReal.ofReal delta := by
  classical
  simp only [setOf_exists]
  calc
    auditSourceLaw a ha0 ha1 (⋃ n, {ω | a < lower n (observedPrefix (n+1) ω) ∨ upper n (observedPrefix (n+1) ω) < a}) ≤
      ∑' n, auditSourceLaw a ha0 ha1 {ω | a < lower n (observedPrefix (n+1) ω) ∨ upper n (observedPrefix (n+1) ω) < a} :=
        measure_iUnion_le _
    _ ≤ ∑' n, ENNReal.ofReal (2*tailSpending delta n) := ENNReal.tsum_le_tsum (fun n =>
      auditSource_interval_failure a _ ha0 ha1 (n+1) (tailSpending_nonneg delta hd n) (lower n) (upper n) (hc n))
    _ ≤ ENNReal.ofReal delta := spending_total_le delta hd

/-- The same law and the same observed prefixes drive every certificate. -/
theorem auditSource_all_certificates_sound (a delta : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1)
    (hd : 0 ≤ delta) (lower upper : (n : ℕ) → Bits (n+1) → ℝ)
    (hc : ∀ n, TailBracket (n+1) (tailSpending delta n) (lower n) (upper n))
    (disturbance tolerance : (ℕ → Bool) → ℕ → ℝ)
    (he : ∀ ω n, 0 ≤ disturbance ω n ∧ disturbance ω n ≤ 1/4) :
    auditSourceLaw a ha0 ha1
      (AllCertificatesSound a (fun ω n => lower n (observedPrefix (n+1) ω))
        (fun ω n => upper n (observedPrefix (n+1) ω)) disturbance tolerance)ᶜ ≤ ENNReal.ofReal delta := by
  have hb := certificate_failure_measure_le (auditSourceLaw a ha0 ha1) a
    (fun ω n => lower n (observedPrefix (n+1) ω))
    (fun ω n => upper n (observedPrefix (n+1) ω)) disturbance tolerance
    (by intro ω n; exact ⟨((hc n).1 _).1,((hc n).1 _).2.2,(he ω n).1,(he ω n).2⟩)
  have heq : (IntervalCoverage a (fun ω n => lower n (observedPrefix (n+1) ω))
        (fun ω n => upper n (observedPrefix (n+1) ω)))ᶜ =
      {ω | ∃ n, a < lower n (observedPrefix (n+1) ω) ∨ upper n (observedPrefix (n+1) ω) < a} := by
    ext ω
    simp only [IntervalCoverage,Set.mem_compl_iff,Set.mem_setOf_eq,not_forall,not_and_or,not_le]
  rw [heq] at hb
  exact hb.trans (auditSource_anytime_coverage a delta ha0 ha1 hd lower upper hc)

end
end Orthemology.Tranche3

#print axioms Orthemology.Tranche3.auditSource_anytime_coverage
#print axioms Orthemology.Tranche3.auditSource_all_certificates_sound
