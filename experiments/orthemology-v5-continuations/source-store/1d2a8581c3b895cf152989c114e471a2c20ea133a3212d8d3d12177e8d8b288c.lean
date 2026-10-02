import MembershipMatrixComputable

namespace P02.Codec.UniformComputability
open P02A2.ObserverCore P02A2.PRProgram AtomicMembership

def echoPacked : PackedProgram := ⟨2,1,.skip⟩

theorem echo_value (n word : ℕ) : evaluateIndex (programIndex echoPacked) n word = word%2 := by
  rw [evaluateIndex, decodeIndex_programIndex]
  simp [echoPacked, exec, binaryStore]

theorem invalid_zero_heavy_count : heavyCount 0 0 2 = 4 := by
  decide +kernel

theorem echo_below_threshold : heavyCount (programIndex echoPacked) 1 2 = 0 := by
  unfold heavyCount wordCount outputList
  simp_rw [echo_value]
  decide +kernel

theorem echo_inclusive_threshold : heavyCount (programIndex echoPacked) 2 2 = 4 := by
  unfold heavyCount wordCount outputList
  simp_rw [echo_value]
  decide +kernel

theorem membership_zero_denominator (e a k N : ℕ) : membershipMatrix e (Nat.pair a 0) k N := by
  apply (membershipMatrix_integer_iff _ _ _ _).mpr
  simp

theorem membership_vacuous_one (e k N : ℕ) : membershipMatrix e (Nat.pair 1 1) k N := by
  apply (membershipMatrix_integer_iff _ _ _ _).mpr
  simp


theorem zero_horizon_heavy (e k : ℕ) : heavyCount e k 0 = 1 := by
  have hk : 1 ≤ 2^k := Nat.one_le_iff_ne_zero.mpr (pow_ne_zero _ (by decide))
  simp [heavyCount, allWords, wordCount, outputList, hk]

end P02.Codec.UniformComputability
