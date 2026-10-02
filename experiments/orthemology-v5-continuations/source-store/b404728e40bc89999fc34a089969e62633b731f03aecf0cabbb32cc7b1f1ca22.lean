import RawPrefixDeviation

noncomputable section
open MeasureTheory ProbabilityTheory Set
open scoped BigOperators ENNReal
open Orthemology.Tranche2.PolicyEmbedding

namespace HiddenParity.Exponential
open HiddenParity.Empirical

lemma exponential_tail_sum (c : ℝ) (hc : 0 < c) (N : ℕ) :
    (∑' k : ℕ, ENNReal.ofReal (2 * Real.exp (-((N+k:ℕ):ℝ)*c))) =
      ENNReal.ofReal (2 * Real.exp (-(N:ℝ)*c) / (1-Real.exp (-c))) := by
  have hq : Real.exp (-c) < 1 := Real.exp_lt_one_iff.mpr (by linarith)
  have hden : 0 < 1-Real.exp (-c) := by linarith
  have he (k : ℕ) : ENNReal.ofReal (2 * Real.exp (-((N+k:ℕ):ℝ)*c)) =
      ENNReal.ofReal (2 * Real.exp (-(N:ℝ)*c)) * ENNReal.ofReal (Real.exp (-c))^k := by
    rw [← ENNReal.ofReal_pow (Real.exp_pos _).le,
      ← ENNReal.ofReal_mul (show 0 ≤ 2 * Real.exp (-(N:ℝ)*c) by positivity),
      ← Real.exp_nat_mul]
    congr 1
    rw [mul_assoc,← Real.exp_add]
    congr 2
    push_cast
    ring
  simp_rw [he]
  rw [ENNReal.tsum_mul_left, ENNReal.tsum_geometric,
    ENNReal.ofReal_div_of_pos hden, ENNReal.ofReal_sub 1 (Real.exp_pos _).le]
  norm_num [div_eq_mul_inv]

universe u v
variable {A Y : Type u} {R : Type v}
variable [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
variable [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
variable [MeasurableSpace Y] [MeasurableSingletonClass Y]

/-- A fully derived exponential all-future deterministic-prefix deviation bound
for the literal raw tapes. The dimension factor counts every row and symbol. -/
theorem seeded_rawTailDeviation_exponential
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (N : ℕ) (hNpos : 0 < N) {η : ℝ} (hη : 0 < η) (hη1 : η ≤ 1) :
    (ρ.prod (stackMeasure P hP hN)) (RawTailDeviation (R := R) P η N) ≤
      ENNReal.ofReal ((Fintype.card A : ℝ) * (Fintype.card Y : ℝ) *
        (2 * Real.exp (-(N:ℝ)*(η^2/2)) / (1-Real.exp (-(η^2/2))))) := by
  let μ := ρ.prod (stackMeasure P hP hN)
  let E : A → Y → ℕ → Set (R × FlatStack A Y) :=
    fun a y k => {z | η ≤ |rawFrequency a y (N+k) z - P a y|}
  have he : RawTailDeviation (R := R) P η N = ⋃ a, ⋃ y, ⋃ k, E a y k := by
    ext z
    simp only [RawTailDeviation,Set.mem_setOf_eq,Set.mem_iUnion,E]
    constructor
    · rintro ⟨a,y,n,hn,hz⟩
      refine ⟨a,y,n-N,?_⟩
      simpa [Nat.add_sub_of_le hn] using hz
    · rintro ⟨a,y,k,hz⟩
      exact ⟨a,y,N+k,by omega,hz⟩
  have hc : 0 < η^2/2 := by positivity
  have hone (a : A) (y : Y) : μ (⋃ k, E a y k) ≤
      ENNReal.ofReal (2 * Real.exp (-(N:ℝ)*(η^2/2)) / (1-Real.exp (-(η^2/2)))) := by
    calc
      _ ≤ ∑' k, μ (E a y k) := measure_iUnion_le _
      _ ≤ ∑' k : ℕ, ENNReal.ofReal (2 * Real.exp (-((N+k:ℕ):ℝ)*(η^2/2))) := by
        apply ENNReal.tsum_le_tsum
        intro k
        have h := seeded_rawFrequency_exponential ρ P hP hN a y (N+k) (by omega) hη.le hη1
        convert h using 1 <;> congr 2 <;> ring
      _ = _ := exponential_tail_sum (η^2/2) hc N
  rw [he]
  change μ (⋃ a, ⋃ y, ⋃ k, E a y k) ≤ _
  calc
    _ ≤ ∑ a, μ (⋃ y, ⋃ k, E a y k) := measure_iUnion_fintype_le μ _
    _ ≤ ∑ a, ∑ y, μ (⋃ k, E a y k) :=
      Finset.sum_le_sum (fun a _ => measure_iUnion_fintype_le μ _)
    _ ≤ ∑ _a : A, ∑ _y : Y,
        ENNReal.ofReal (2 * Real.exp (-(N:ℝ)*(η^2/2)) / (1-Real.exp (-(η^2/2)))) :=
      Finset.sum_le_sum (fun a _ => Finset.sum_le_sum (fun y _ => hone a y))
    _ = _ := by
      simp only [Finset.sum_const,Finset.card_univ,nsmul_eq_mul]
      rw [ENNReal.ofReal_mul (show 0 ≤ (Fintype.card A : ℝ)*(Fintype.card Y : ℝ) by positivity),
        ENNReal.ofReal_mul (Nat.cast_nonneg _)]
      simp only [ENNReal.ofReal_natCast]
      ring

#print axioms seeded_rawTailDeviation_exponential
end HiddenParity.Exponential
