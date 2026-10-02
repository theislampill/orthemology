import BernoulliIntervalCoverage
import Mathlib.Probability.ProductMeasure
import Mathlib.Probability.ProbabilityMassFunction.Constructions

open MeasureTheory ProbabilityTheory Set
open scoped BigOperators ENNReal
open Orthemology.Tranche2

namespace Orthemology.Tranche3
noncomputable section

instance bitsMeasurableSpace : (n : ℕ) → MeasurableSpace (Bits n)
  | 0 => inferInstanceAs (MeasurableSpace Unit)
  | n+1 => @Prod.instMeasurableSpace Bool (Bits n) inferInstance (bitsMeasurableSpace n)

instance bitsMeasurableSingletonClass : (n : ℕ) → MeasurableSingletonClass (Bits n)
  | 0 => inferInstanceAs (MeasurableSingletonClass Unit)
  | n+1 => @Prod.instMeasurableSingletonClass Bool (Bits n) inferInstance
      (bitsMeasurableSpace n) inferInstance (bitsMeasurableSingletonClass n)

def observedPrefix : (n : ℕ) → (ℕ → Bool) → Bits n
  | 0, _ => ()
  | n+1, ω => (ω n, observedPrefix n ω)

lemma observedPrefix_measurable : ∀ n, Measurable (observedPrefix n) := by
  intro n
  induction n with
  | zero => exact measurable_const
  | succ n ih => exact (measurable_pi_apply n).prodMk ih

def prefixDecoder : (n : ℕ) → Bits n → ℕ → Bool
  | 0, _, _ => false
  | n+1, w, k => if k=n then w.1 else prefixDecoder n w.2 k

lemma observedPrefix_eq_iff : ∀ n (ω : ℕ → Bool) (w : Bits n),
    observedPrefix n ω = w ↔ ∀ k, k<n → ω k = prefixDecoder n w k := by
  intro n
  induction n with
  | zero => intro ω w; cases w; simp [observedPrefix]
  | succ n ih =>
      intro ω w
      rcases w with ⟨b,w⟩
      constructor
      · intro h k hk
        have hparts : ω n=b ∧ observedPrefix n ω=w := Prod.mk.inj h
        by_cases he : k=n
        · subst k; simpa [prefixDecoder] using hparts.1
        · have hkn : k<n := by omega
          simpa [prefixDecoder,he] using (ih ω w).mp hparts.2 k hkn
      · intro h
        have hb : ω n=b := by simpa [prefixDecoder] using h n (by omega)
        have ht : observedPrefix n ω=w := (ih ω w).mpr (by
          intro k hk
          have hne : k ≠ n := by omega
          simpa [prefixDecoder,hne] using h k (by omega))
        exact Prod.ext hb ht

lemma observedPrefix_singleton_preimage (n : ℕ) (w : Bits n) :
    observedPrefix n ⁻¹' {w} = Set.pi (Finset.range n : Set ℕ)
      (fun k => {prefixDecoder n w k}) := by
  ext ω
  simp only [Set.mem_preimage,Set.mem_singleton_iff,Set.mem_pi,Finset.mem_coe,Finset.mem_range]
  exact observedPrefix_eq_iff n ω w

def sourceCoin (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1) : PMF Bool :=
  PMF.ofFintype (fun b => ENNReal.ofReal (coinMass a b)) (by
    rw [Fintype.sum_bool,← ENNReal.ofReal_add
      (coinMass_nonneg a ha0 ha1 true) (coinMass_nonneg a ha0 ha1 false)]
    simp [coinMass])

def sourceCoinMeasure (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1) : Measure Bool :=
  (sourceCoin a ha0 ha1).toMeasure
instance sourceCoin_probability (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1) :
    IsProbabilityMeasure (sourceCoinMeasure a ha0 ha1) := by
  unfold sourceCoinMeasure
  infer_instance

def auditSourceLaw (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1) : Measure (ℕ → Bool) :=
  Measure.infinitePi (fun _ : ℕ => sourceCoinMeasure a ha0 ha1)
instance auditSource_probability (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1) :
    IsProbabilityMeasure (auditSourceLaw a ha0 ha1) := by
  unfold auditSourceLaw
  infer_instance

lemma sourceCoin_singleton (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1) (b : Bool) :
    sourceCoinMeasure a ha0 ha1 {b} = ENNReal.ofReal (coinMass a b) := by
  unfold sourceCoinMeasure
  rw [PMF.toMeasure_apply_singleton _ b (measurableSet_singleton b)]
  rfl

lemma decoder_product (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1) : ∀ n (w : Bits n),
    (∏ k ∈ Finset.range n, ENNReal.ofReal (coinMass a (prefixDecoder n w k))) =
      ENNReal.ofReal (bernoulliMass n a w) := by
  intro n
  induction n with
  | zero => intro w; simp [bernoulliMass]
  | succ n ih =>
      intro w
      rw [Finset.prod_range_succ]
      have hp : (∏ k ∈ Finset.range n, ENNReal.ofReal (coinMass a (prefixDecoder (n+1) w k))) =
          ∏ k ∈ Finset.range n, ENNReal.ofReal (coinMass a (prefixDecoder n w.2 k)) := by
        apply Finset.prod_congr rfl
        intro k hk
        have hne : k ≠ n := by have := Finset.mem_range.mp hk; omega
        simp [prefixDecoder,hne]
      rw [hp,ih]
      simp only [prefixDecoder,if_pos rfl,bernoulliMass]
      rw [ENNReal.ofReal_mul (coinMass_nonneg a ha0 ha1 w.1)]
      exact mul_comm _ _

/-- The finite-word probabilities are derived from the actual infinite iid
source law. The unused oracle tail is not part of the certificate input. -/
theorem auditSource_prefix_mass (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1)
    (n : ℕ) (w : Bits n) :
    (auditSourceLaw a ha0 ha1).map (observedPrefix n) {w} =
      ENNReal.ofReal (bernoulliMass n a w) := by
  rw [Measure.map_apply (observedPrefix_measurable n) (measurableSet_singleton w),
    observedPrefix_singleton_preimage,auditSourceLaw,
    Measure.infinitePi_pi _ (fun k _ => measurableSet_singleton _)]
  simp_rw [sourceCoin_singleton]
  exact decoder_product a ha0 ha1 n w

end
end Orthemology.Tranche3

#print axioms Orthemology.Tranche3.auditSource_prefix_mass
