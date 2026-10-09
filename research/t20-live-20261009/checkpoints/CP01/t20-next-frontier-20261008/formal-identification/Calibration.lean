import Mathlib.NumberTheory.Padics.PadicVal.Basic
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Lean.Elab.Tactic.Omega

/-! The exact calibrated rational code, with no probability-space or physical assumptions. -/
namespace CalibratedIdentification

local instance : Fact (Nat.Prime 2) := ⟨by decide⟩
local instance : Fact (Nat.Prime 3) := ⟨by decide⟩
local instance : Fact (Nat.Prime 5) := ⟨by decide⟩

/-- Joint-profile absence code for three unguarded route counts. -/
def jointCode (a b c : ℕ) : ℚ :=
  (1 / 2 : ℚ) ^ a * (2 / 3 : ℚ) ^ b * (5 / 6 : ℚ) ^ c

lemma val_nat_not_dvd (p n : ℕ) (h : ¬p ∣ n) :
    padicValRat p (n : ℚ) = 0 := by
  rw [padicValRat.of_nat, padicValNat.eq_zero_of_not_dvd h]
  rfl

lemma val_six (p : ℕ) [Fact p.Prime] :
    padicValRat p (6 : ℚ) = padicValRat p (2 : ℚ) + padicValRat p (3 : ℚ) := by
  rw [show (6 : ℚ) = 2 * 3 by norm_num, padicValRat.mul (by norm_num) (by norm_num)]

lemma val_half (p : ℕ) [Fact p.Prime] :
    padicValRat p (1 / 2 : ℚ) = -padicValRat p (2 : ℚ) := by
  rw [padicValRat.div (by norm_num) (by norm_num), padicValRat.one, zero_sub]

lemma val_two_thirds (p : ℕ) [Fact p.Prime] :
    padicValRat p (2 / 3 : ℚ) = padicValRat p (2 : ℚ) - padicValRat p (3 : ℚ) := by
  rw [padicValRat.div (by norm_num) (by norm_num)]

lemma val_five_sixths (p : ℕ) [Fact p.Prime] :
    padicValRat p (5 / 6 : ℚ) =
      padicValRat p (5 : ℚ) - (padicValRat p (2 : ℚ) + padicValRat p (3 : ℚ)) := by
  rw [padicValRat.div (by norm_num) (by norm_num), val_six]

lemma jointCode_valuation (p a b c : ℕ) [Fact p.Prime] :
    padicValRat p (jointCode a b c) =
      (a : ℤ) * padicValRat p (1 / 2 : ℚ) +
      (b : ℤ) * padicValRat p (2 / 3 : ℚ) +
      (c : ℤ) * padicValRat p (5 / 6 : ℚ) := by
  unfold jointCode
  rw [padicValRat.mul
    (mul_ne_zero (pow_ne_zero _ (by norm_num)) (pow_ne_zero _ (by norm_num)))
    (pow_ne_zero _ (by norm_num))]
  rw [padicValRat.mul (pow_ne_zero _ (by norm_num)) (pow_ne_zero _ (by norm_num))]
  rw [padicValRat.pow (by norm_num), padicValRat.pow (by norm_num),
    padicValRat.pow (by norm_num)]

lemma v2_two : padicValRat 2 (2 : ℚ) = 1 := by
  simpa only [Nat.cast_ofNat] using (padicValRat.self (by decide : 1 < 2))
lemma v2_three : padicValRat 2 (3 : ℚ) = 0 := by
  simpa only [Nat.cast_ofNat] using (val_nat_not_dvd 2 3 (by decide))
lemma v2_five : padicValRat 2 (5 : ℚ) = 0 := by
  simpa only [Nat.cast_ofNat] using (val_nat_not_dvd 2 5 (by decide))
lemma v3_two : padicValRat 3 (2 : ℚ) = 0 := by
  simpa only [Nat.cast_ofNat] using (val_nat_not_dvd 3 2 (by decide))
lemma v3_three : padicValRat 3 (3 : ℚ) = 1 := by
  simpa only [Nat.cast_ofNat] using (padicValRat.self (by decide : 1 < 3))
lemma v3_five : padicValRat 3 (5 : ℚ) = 0 := by
  simpa only [Nat.cast_ofNat] using (val_nat_not_dvd 3 5 (by decide))
lemma v5_two : padicValRat 5 (2 : ℚ) = 0 := by
  simpa only [Nat.cast_ofNat] using (val_nat_not_dvd 5 2 (by decide))
lemma v5_three : padicValRat 5 (3 : ℚ) = 0 := by
  simpa only [Nat.cast_ofNat] using (val_nat_not_dvd 5 3 (by decide))
lemma v5_five : padicValRat 5 (5 : ℚ) = 1 := by
  simpa only [Nat.cast_ofNat] using (padicValRat.self (by decide : 1 < 5))

lemma jointCode_v5 (a b c : ℕ) : padicValRat 5 (jointCode a b c) = (c : ℤ) := by
  rw [jointCode_valuation, val_half, val_two_thirds, val_five_sixths,
    v5_two, v5_three, v5_five]
  ring

lemma jointCode_v3 (a b c : ℕ) :
    padicValRat 3 (jointCode a b c) = -(b : ℤ) - (c : ℤ) := by
  rw [jointCode_valuation, val_half, val_two_thirds, val_five_sixths,
    v3_two, v3_three, v3_five]
  ring

lemma jointCode_v2 (a b c : ℕ) :
    padicValRat 2 (jointCode a b c) = -(a : ℤ) + (b : ℤ) - (c : ℤ) := by
  rw [jointCode_valuation, val_half, val_two_thirds, val_five_sixths,
    v2_two, v2_three, v2_five]
  ring

/-- Concrete prime factor coding is injective for all natural triples. -/
theorem jointCode_injective {a b c a' b' c' : ℕ}
    (h : jointCode a b c = jointCode a' b' c') :
    a = a' ∧ b = b' ∧ c = c' := by
  have h5 := congrArg (padicValRat 5) h
  have h3 := congrArg (padicValRat 3) h
  have h2 := congrArg (padicValRat 2) h
  rw [jointCode_v5, jointCode_v5] at h5
  rw [jointCode_v3, jointCode_v3] at h3
  rw [jointCode_v2, jointCode_v2] at h2
  omega

lemma half_pow_injective {a b : ℕ} (h : (1 / 2 : ℚ) ^ a = (1 / 2 : ℚ) ^ b) :
    a = b := by
  have hv := congrArg (padicValRat 2) h
  rw [padicValRat.pow (by norm_num), padicValRat.pow (by norm_num), val_half,
    v2_two] at hv
  omega

lemma two_thirds_pow_injective {a b : ℕ} (h : (2 / 3 : ℚ) ^ a = (2 / 3 : ℚ) ^ b) :
    a = b := by
  have hv := congrArg (padicValRat 3) h
  rw [padicValRat.pow (by norm_num), padicValRat.pow (by norm_num), val_two_thirds,
    v3_two, v3_three] at hv
  omega

/-- All five hit counts are identified by the actual three rational values. -/
theorem calibrated_five_counts_injective {a b c d e a' b' c' d' e' : ℕ}
    (hAB : jointCode a b c = jointCode a' b' c')
    (hA : (1 / 2 : ℚ) ^ (a + d) = (1 / 2 : ℚ) ^ (a' + d'))
    (hB : (2 / 3 : ℚ) ^ (b + e) = (2 / 3 : ℚ) ^ (b' + e')) :
    a = a' ∧ b = b' ∧ c = c' ∧ d = d' ∧ e = e' := by
  obtain ⟨ha, hb, hc⟩ := jointCode_injective hAB
  have hd := half_pow_injective hA
  have he := two_thirds_pow_injective hB
  omega

end CalibratedIdentification
