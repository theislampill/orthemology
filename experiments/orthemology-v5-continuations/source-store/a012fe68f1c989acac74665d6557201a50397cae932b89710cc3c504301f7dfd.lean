import MembershipWords
import NumericMembership
import MatrixArithmetic

namespace P02.Codec.UniformComputability
open P02A2.FiniteOutputTable AtomicMembership
open scoped BigOperators

theorem dyadic_threshold_count_iff (c k N : ℕ) :
    (1/2 : ℚ≥0)^k ≤ (c : ℚ≥0)/(2:ℚ≥0)^N ↔ 2^N ≤ c*2^k := by
  have hk : (0 : ℚ≥0) < 2^k := by positivity
  have hN : (0 : ℚ≥0) < 2^N := by positivity
  rw [div_pow, one_pow, div_le_div_iff₀ hk hN, one_mul]
  exact_mod_cast (Iff.rfl : (2^N ≤ c*2^k) ↔ (2^N ≤ c*2^k))

def finiteHeavyCount (e k N : ℕ) : ℕ :=
  ∑ w : Fin N → Bool, if 2^N ≤ (preimageWords (evaluateIndex e) N w).card * 2^k
    then (preimageWords (evaluateIndex e) N w).card else 0

theorem rationalHeavyMass_finiteCount (e k N : ℕ) :
    rationalHeavyMass (indexTable e) k N = (finiteHeavyCount e k N : ℚ≥0)/(2:ℚ≥0)^N := by
  unfold rationalHeavyMass rationalHeavyWords indexTable tableProbability
  rw [Finset.sum_filter]
  simp_rw [dyadic_threshold_count_iff]
  simp [finiteHeavyCount, Nat.cast_sum, Finset.sum_div, apply_ite, ite_div]


theorem heavyCount_eq_finite (e k N : ℕ) : heavyCount e k N = finiteHeavyCount e k N := by
  rw [heavyCount, sum_allWords]
  simp only [wordCount_exact, finiteHeavyCount]

/-- The integer numerator computes the exact existing rational heavy mass. -/
theorem rationalHeavyMass_heavyCount (e k N : ℕ) :
    rationalHeavyMass (indexTable e) k N = (heavyCount e k N : ℚ≥0)/(2:ℚ≥0)^N := by
  rw [rationalHeavyMass_finiteCount, heavyCount_eq_finite]

/-- Exact integer form of the original natural-input membership matrix,
including zero denominators, vacuous upper rationals and inclusive ties. -/
theorem membershipMatrix_integer_iff (e i k N : ℕ) :
    membershipMatrix e i k N ↔
      i.unpair.2 = 0 ∨ i.unpair.2 ≤ i.unpair.1 ∨
        i.unpair.1 * 2^N ≤ i.unpair.2 * heavyCount e k N := by
  unfold membershipMatrix finiteMassTest rationalOfCode
  rw [rationalHeavyMass_heavyCount]
  exact rational_imp_dyadic_cross _ _ _ _

end P02.Codec.UniformComputability
