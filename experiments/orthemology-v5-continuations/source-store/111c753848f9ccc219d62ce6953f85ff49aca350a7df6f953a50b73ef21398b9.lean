import HeavyCylinders
open Set MeasureTheory
open scoped ENNReal NNReal
namespace AtomicMembership

theorem nnrat_le_cast (a b : ℚ≥0) : (a : ℝ≥0∞) ≤ b ↔ a ≤ b := by
  change ((a : ℝ≥0) : ℝ≥0∞) ≤ ((b : ℝ≥0) : ℝ≥0∞) ↔ _
  norm_cast

theorem nnrat_lt_cast (a b : ℚ≥0) : (a : ℝ≥0∞) < b ↔ a < b := by
  change ((a : ℝ≥0) : ℝ≥0∞) < ((b : ℝ≥0) : ℝ≥0∞) ↔ _
  norm_cast

theorem nnrat_cast_sum {ι : Type} (s : Finset ι) (f : ι → ℚ≥0) :
    ((∑ i ∈ s, f i : ℚ≥0) : ℝ≥0∞) = ∑ i ∈ s, (f i : ℝ≥0∞) := by
  have h : ((∑ i ∈ s, f i : ℚ≥0) : ℝ≥0) = ∑ i ∈ s, (f i : ℝ≥0) :=
    map_sum (NNRat.castHom ℝ≥0) f s
  change (((∑ i ∈ s, f i : ℚ≥0) : ℝ≥0) : ℝ≥0∞) = _
  rw [h, ENNReal.coe_finset_sum]
  rfl

theorem nnrat_threshold_cast (k : ℕ) :
    (↑((1/2 : ℚ≥0)^k) : ℝ≥0∞) = (2⁻¹ : ℝ≥0∞)^k := by
  simp only [← ENNReal.coe_nnratCast]
  push_cast
  norm_num

open P02A2 P02A2.Q8Measure

def rationalHeavyWords (p : (n : ℕ) → (Fin n → Bool) → ℚ≥0) (k n : ℕ) :
    Finset (Fin n → Bool) := Finset.univ.filter (fun w => (1/2 : ℚ≥0)^k ≤ p n w)

def rationalHeavyMass (p : (n : ℕ) → (Fin n → Bool) → ℚ≥0) (k n : ℕ) : ℚ≥0 :=
  ∑ w ∈ rationalHeavyWords p k n, p n w

theorem rational_heavy_words (μ : Measure Cantor)
    (p : (n : ℕ) → (Fin n → Bool) → ℚ≥0)
    (hp : ∀ n w, (p n w : ℝ≥0∞) = μ (cylinder n w)) (k n : ℕ) :
    rationalHeavyWords p k n = heavyWords μ k n := by
  classical
  ext w
  simp only [rationalHeavyWords, heavyWords, Finset.mem_filter, Finset.mem_univ, true_and]
  rw [← hp n w, ← nnrat_threshold_cast]
  exact (nnrat_le_cast _ _).symm

theorem rational_heavy_mass (μ : Measure Cantor)
    (p : (n : ℕ) → (Fin n → Bool) → ℚ≥0)
    (hp : ∀ n w, (p n w : ℝ≥0∞) = μ (cylinder n w)) (k n : ℕ) :
    (rationalHeavyMass p k n : ℝ≥0∞) = μ (heavy μ k n) := by
  rw [rationalHeavyMass, nnrat_cast_sum, rational_heavy_words μ p hp, heavy_finite_sum]
  exact Finset.sum_congr rfl (fun w _ => hp n w)

theorem nnrat_cast_real (r : ℚ≥0) :
    (r : ℝ≥0∞) = (Real.toNNReal (r : ℚ) : ℝ≥0∞) := by
  rw [← ENNReal.coe_nnratCast]
  congr 1
  apply NNReal.eq
  change ((r : ℝ≥0) : ℝ) = max ((r : ℚ) : ℝ) 0
  have h0 : (0 : ℝ) ≤ ((r : ℚ) : ℝ) := by exact_mod_cast r.property
  rw [max_eq_left h0]
  rfl

theorem mass_one_nnrat_normal (μ : Measure Cantor) [IsProbabilityMeasure μ] :
    mass μ = 1 ↔ ∀ q : ℚ≥0, q < 1 → ∃ k, ∀ n, (q : ℝ≥0∞) ≤ μ (heavy μ k n) := by
  constructor
  · intro hm q hq
    have hl : (q : ℝ≥0∞) < ⨆ k, ⨅ n, μ (heavy μ k n) := by
      rw [← atomic_mass_formula, hm]
      simpa only [← ENNReal.coe_nnratCast, NNRat.cast_one, ENNReal.coe_one] using (nnrat_lt_cast q 1).mpr hq
    obtain ⟨k,hk⟩ := lt_iSup_iff.mp hl
    exact ⟨k,fun n => hk.le.trans (iInf_le _ n)⟩
  · intro h
    apply (mass_one_normal_form μ).mpr
    intro q hq hq1
    have hc : (q.toNNRat : ℝ≥0∞) = (Real.toNNReal q : ℝ≥0∞) := by
      simpa only [Rat.coe_toNNRat q hq] using nnrat_cast_real q.toNNRat
    have hsmall : q.toNNRat < 1 := by
      apply (nnrat_lt_cast _ 1).mp
      rw [hc]
      simpa only [← ENNReal.coe_nnratCast, NNRat.cast_one, ENNReal.coe_one] using hq1
    obtain ⟨k,hk⟩ := h q.toNNRat hsmall
    exact ⟨k,fun n => by simpa only [hc] using hk n⟩

theorem defect_zero_rational_normal (μ : Measure Cantor) [IsProbabilityMeasure μ]
    (p : (n : ℕ) → (Fin n → Bool) → ℚ≥0)
    (hp : ∀ n w, (p n w : ℝ≥0∞) = μ (cylinder n w)) :
    defect μ = 0 ↔ ∀ q : ℚ≥0, q < 1 → ∃ k, ∀ n, q ≤ rationalHeavyMass p k n := by
  have hd : defect μ = 0 ↔ mass μ = 1 := by
    change 1 - (mass μ).toReal = 0 ↔ mass μ = 1
    rw [sub_eq_zero, eq_comm, ENNReal.toReal_eq_one_iff]
  rw [hd, mass_one_nnrat_normal]
  apply forall_congr'
  intro q
  apply imp_congr_right
  intro _
  apply exists_congr
  intro k
  apply forall_congr'
  intro n
  rw [← rational_heavy_mass μ p hp, nnrat_le_cast]

end AtomicMembership
