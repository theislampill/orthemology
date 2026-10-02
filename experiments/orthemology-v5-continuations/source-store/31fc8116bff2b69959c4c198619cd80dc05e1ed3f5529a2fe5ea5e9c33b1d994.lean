import Mathlib

/-! Exact natural cross-multiplication for the already fixed rational membership
matrix. This arithmetic module does not assume an oracle for the heavy count;
its caller must separately prove that the supplied numerator is the actual
finite-word count. -/
namespace AtomicMembership

theorem divNat_eq_div (a d : ℕ) : NNRat.divNat a d = (a : ℚ≥0) / d := by
  rw [NNRat.div_def]
  simp

theorem rational_imp_cross (a d H T : ℕ) (hT : 0 < T) :
    (NNRat.divNat a d < 1 → NNRat.divNat a d ≤ (H : ℚ≥0) / T) ↔
      d = 0 ∨ d ≤ a ∨ a*T ≤ d*H := by
  by_cases hd : d = 0
  · subst d
    simp
  · have hdq : (0 : ℚ≥0) < d := by exact_mod_cast Nat.pos_of_ne_zero hd
    have hTq : (0 : ℚ≥0) < T := by exact_mod_cast hT
    have hs : NNRat.divNat a d < 1 ↔ a < d := by
      rw [divNat_eq_div, div_lt_one hdq]
      exact_mod_cast Iff.rfl
    have hc : NNRat.divNat a d ≤ (H : ℚ≥0) / T ↔ a*T ≤ d*H := by
      rw [divNat_eq_div, div_le_div_iff₀ hdq hTq]
      norm_cast
      simp only [Nat.mul_comm]
    rw [hs,hc]
    simp [hd, imp_iff_not_or, Nat.not_lt]

theorem rational_imp_dyadic_cross (a d H N : ℕ) :
    (NNRat.divNat a d < 1 → NNRat.divNat a d ≤ (H : ℚ≥0) / (2:ℚ≥0)^N) ↔
      d = 0 ∨ d ≤ a ∨ a*2^N ≤ d*H := by
  have h := rational_imp_cross a d H (2^N) (by positivity)
  simpa only [Nat.cast_pow, Nat.cast_ofNat] using h

theorem zero_denominator_control (a H N : ℕ) :
    NNRat.divNat a 0 < 1 → NNRat.divNat a 0 ≤ (H : ℚ≥0) / (2:ℚ≥0)^N := by
  simp

theorem upper_rational_vacuity (a d H N : ℕ) (hda : d ≤ a) :
    NNRat.divNat a d < 1 → NNRat.divNat a d ≤ (H : ℚ≥0) / (2:ℚ≥0)^N := by
  exact (rational_imp_dyadic_cross a d H N).mpr (Or.inr (Or.inl hda))

theorem inclusive_rational_tie (a d H N : ℕ) (h : a*2^N = d*H) :
    NNRat.divNat a d < 1 → NNRat.divNat a d ≤ (H : ℚ≥0) / (2:ℚ≥0)^N := by
  exact (rational_imp_dyadic_cross a d H N).mpr (Or.inr (Or.inr h.le))

end AtomicMembership
