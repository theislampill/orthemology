import HeavyCylinders
import CodecProgram

/-! Exact finite output-cylinder tables for any productive prefix evaluator.
The source table enumerates all N-bit source words and executes the actual
prefix function. Counts are rational dyadics; the measure identity is for the
actual fair-Cantor pushforward, not an assumed finite approximation. -/
namespace P02A2.FiniteOutputTable
open Set MeasureTheory P02A2.ObserverCore P02A2.Q8Measure AtomicMembership
open scoped ENNReal BigOperators

def extendWord (N : ℕ) (v : Fin N → Bool) : Cantor :=
  fun n => if h : n < N then v ⟨n,h⟩ else false

def finiteOutput (P : ℕ → ℕ → ℕ) (N : ℕ) (v : Fin N → Bool) : Fin N → Bool :=
  bitsPrefix N (output P (extendWord N v))

theorem finiteOutput_actual (P : ℕ → ℕ → ℕ) (N : ℕ) (x : Cantor) :
    finiteOutput P N (bitsPrefix N x) = bitsPrefix N (output P x) := by
  funext i
  apply prefix_causal P _ _ i.val
  intro j hj
  have hjN : j < N := lt_of_le_of_lt hj i.isLt
  simp [extendWord, bitsPrefix, hjN]

theorem output_measurable (P : ℕ → ℕ → ℕ) : Measurable (output P) := by
  apply measurable_pi_lambda
  intro n
  exact (measurable_of_countable (fun v : Fin (n+1) → Bool =>
    decide (P n (sentinel (List.ofFn v)) % 2 = 1))).comp (prefix_measurable (n+1))

theorem fair_cylinder (N : ℕ) (v : Fin N → Bool) :
    fairCantor (cylinder N v) = (1/2 : ℝ≥0∞)^N := by
  have he : cylinder N v = Set.pi (↑(Finset.range N) : Set ℕ)
      (fun k => {extendWord N v k}) := by
    ext x
    change (bitsPrefix N x = v) ↔ _
    constructor
    · intro h k hk
      have hkN : k < N := Finset.mem_range.mp hk
      simpa [bitsPrefix, extendWord, hkN] using congrFun h ⟨k,hkN⟩
    · intro h
      funext i
      have hi := h i.val (Finset.mem_range.mpr i.isLt)
      simpa [bitsPrefix, extendWord, i.isLt] using hi
  rw [he, fairCantor_cylinder, Finset.card_range]

def preimageWords (P : ℕ → ℕ → ℕ) (N : ℕ) (w : Fin N → Bool) : Finset (Fin N → Bool) :=
  Finset.univ.filter (fun v => finiteOutput P N v = w)

theorem output_cylinder_preimage (P : ℕ → ℕ → ℕ) (N : ℕ) (w : Fin N → Bool) :
    output P ⁻¹' cylinder N w = ⋃ v ∈ preimageWords P N w, cylinder N v := by
  ext x
  simp only [mem_iUnion]
  constructor
  · intro hx
    refine ⟨bitsPrefix N x, ?_, rfl⟩
    simp only [preimageWords, Finset.mem_filter, Finset.mem_univ, true_and]
    exact (finiteOutput_actual P N x).trans hx
  · rintro ⟨v,hv,hx⟩
    have hv' : finiteOutput P N v = w := (Finset.mem_filter.mp hv).2
    change bitsPrefix N (output P x) = w
    rw [← finiteOutput_actual P N x]
    change bitsPrefix N x = v at hx
    rw [hx, hv']

noncomputable def outputLaw (P : ℕ → ℕ → ℕ) : Measure Cantor := fairCantor.map (output P)

instance outputLaw_probability (P : ℕ → ℕ → ℕ) : IsProbabilityMeasure (outputLaw P) := by
  constructor
  rw [outputLaw, Measure.map_apply (output_measurable P) MeasurableSet.univ]
  simp

theorem cylinder_probability_count (P : ℕ → ℕ → ℕ) (N : ℕ) (w : Fin N → Bool) :
    outputLaw P (cylinder N w) = (preimageWords P N w).card * (1/2 : ℝ≥0∞)^N := by
  rw [outputLaw, Measure.map_apply (output_measurable P) (cylinder_measurable N w), output_cylinder_preimage]
  rw [measure_biUnion_finset ((cylinders_disjoint N).set_pairwise _) (fun v _ => cylinder_measurable N v)]
  simp [fair_cylinder, nsmul_eq_mul]

def tableProbability (P : ℕ → ℕ → ℕ) (N : ℕ) (w : Fin N → Bool) : ℚ≥0 :=
  (preimageWords P N w).card / (2 : ℚ≥0)^N

theorem tableProbability_exact (P : ℕ → ℕ → ℕ) (N : ℕ) (w : Fin N → Bool) :
    (tableProbability P N w : ℝ≥0∞) = outputLaw P (cylinder N w) := by
  rw [cylinder_probability_count]
  rw [← ENNReal.coe_nnratCast]
  simp only [tableProbability, NNRat.cast_div, NNRat.cast_natCast, NNRat.cast_pow, NNRat.cast_ofNat]
  rw [ENNReal.coe_div (by positivity)]
  simp [div_eq_mul_inv, ENNReal.inv_pow]

/-- This table uses the actual decoded numeric observer evaluator. -/
def indexTable (e N : ℕ) (w : Fin N → Bool) : ℚ≥0 := tableProbability (P02.Codec.evaluateIndex e) N w

theorem indexTable_exact (e N : ℕ) (w : Fin N → Bool) :
    (indexTable e N w : ℝ≥0∞) =
      (fairCantor.map (output (P02.Codec.evaluateIndex e))) (cylinder N w) :=
  tableProbability_exact _ _ _

end P02A2.FiniteOutputTable
