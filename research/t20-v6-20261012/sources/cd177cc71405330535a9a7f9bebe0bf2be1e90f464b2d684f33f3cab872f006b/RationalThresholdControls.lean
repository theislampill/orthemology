import RationalThresholdDefect
import MembershipWitnesses

open Set MeasureTheory
open scoped ENNReal NNReal
namespace AtomicMembership.RationalThreshold
open P02A2 P02A2.ObserverCore P02A2.PRProgram P02A2.FiniteOutputTable
open P02.Codec P02.Codec.UniformComputability

/-- At q=1 the new closed cut is exactly the earlier zero-defect matrix. -/
theorem upper_at_one (e i k n : ℕ) :
    upperCutMatrix 1 e i k n ↔ membershipMatrix e i k n := by
  simp [upperCutMatrix, membershipMatrix]

theorem upper_at_zero (e i k n : ℕ) : upperCutMatrix 0 e i k n := by
  simp [upperCutMatrix]

theorem lower_at_one (e i k n : ℕ) : ¬ lowerCutMatrix 1 e i k n := by
  rintro ⟨hlo,hhi,_⟩
  exact (lt_asymm hlo hhi)

theorem zero_denominator_cannot_witness_strict (q : ℚ≥0) (e a k n : ℕ) :
    ¬ lowerCutMatrix q e (Nat.pair a 0) k n := by
  simp [lowerCutMatrix, rationalOfCode]

theorem exact_threshold_not_a_strict_witness (e k n : ℕ) :
    ¬ lowerCutMatrix (1/2) e (Nat.pair 1 2) k n := by
  simp [lowerCutMatrix, rationalOfCode, divNat_eq_div]

theorem redundant_threshold_code (e k n : ℕ) :
    lowerCutMatrix (1/3) e (Nat.pair 1 2) k n ↔
      lowerCutMatrix (1/3) e (Nat.pair 2 4) k n := by
  norm_num [lowerCutMatrix, membershipMatrix, finiteMassTest, rationalOfCode, divNat_eq_div]

/-- Actual old L1 syntax: hide x_0, output 0 at time 0; thereafter x_0*x_n. -/
def hiddenMixturePacked : PackedProgram := ⟨2,2,
  .branch (.reg 0)
    (.set 2 (.mul (.mod (.div (.reg 1) (.pow2 (.reg 0))) (.constant 2))
      (.mod (.reg 1) (.constant 2))))
    (.set 2 (.constant 0))⟩

theorem hiddenMixture_value (n word : ℕ) :
    evaluateIndex (programIndex hiddenMixturePacked) n word =
      if n=0 then 0 else (((word / 2^n)%2) * (word%2))%2 := by
  rw [evaluateIndex, decodeIndex_programIndex]
  simp [hiddenMixturePacked, exec, evalExpr, binaryStore]

theorem hiddenMixture_count_1 : heavyCount (programIndex hiddenMixturePacked) 1 1 = 2 := by
  unfold heavyCount wordCount outputList
  simp_rw [hiddenMixture_value]
  decide +kernel

theorem hiddenMixture_count_2 : heavyCount (programIndex hiddenMixturePacked) 1 2 = 3 := by
  unfold heavyCount wordCount outputList
  simp_rw [hiddenMixture_value]
  decide +kernel

theorem hiddenMixture_count_3 : heavyCount (programIndex hiddenMixturePacked) 1 3 = 5 := by
  unfold heavyCount wordCount outputList
  simp_rw [hiddenMixture_value]
  decide +kernel

theorem hiddenMixture_count_4 : heavyCount (programIndex hiddenMixturePacked) 1 4 = 9 := by
  unfold heavyCount wordCount outputList
  simp_rw [hiddenMixture_value]
  decide +kernel

theorem hiddenMixture_exact_rational_4 :
    rationalHeavyMass (indexTable (programIndex hiddenMixturePacked)) 1 4 = 9/16 := by
  rw [rationalHeavyMass_heavyCount, hiddenMixture_count_4]
  norm_num

end AtomicMembership.RationalThreshold
