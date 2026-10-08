import Mathlib
set_option autoImplicit false

/-! Finite radix residue classification. This is arithmetic only; no retained
selector, orientation or executable policy is evaluated. -/
namespace Orthemology.Ninth.SelectorExtraction

/-- A radix digit is preserved by truncation above its position. -/
theorem digit_mod_pow (a b n i : ℕ) (hi : i < n) :
    (a % b ^ n) / b ^ i % b = a / b ^ i % b := by
  have hd : b ^ (i + 1) ∣ b ^ n := pow_dvd_pow b (Nat.succ_le_of_lt hi)
  rw [← Nat.mod_mul_right_div_self, ← pow_succ,
    Nat.mod_mod_of_dvd a hd, pow_succ, Nat.mod_mul_right_div_self]

/-- Every used radix digit determines, and is determined by, the used-width residue. -/
theorem residue_eq_iff_digits (a c b n : ℕ) :
    a % b ^ n = c % b ^ n ↔ ∀ i, i < n → a / b ^ i % b = c / b ^ i % b := by
  constructor
  · intro h i hi
    rw [← digit_mod_pow a b n i hi, ← digit_mod_pow c b n i hi, h]
  · intro h
    induction n with
    | zero => simp only [pow_zero, Nat.mod_one]
    | succ n ih =>
      rw [Nat.mod_pow_succ, Nat.mod_pow_succ,
        ih (fun i hi => h i (Nat.lt_succ_of_lt hi)), h n (Nat.lt_succ_self n)]

/-- Bounded values have unique digit encodings. No leading-zero convention is needed. -/
theorem bounded_eq_iff_digits (a c b n : ℕ) (ha : a < b ^ n) (hc : c < b ^ n) :
    a = c ↔ ∀ i, i < n → a / b ^ i % b = c / b ^ i % b := by
  simpa only [Nat.mod_eq_of_lt ha, Nat.mod_eq_of_lt hc] using residue_eq_iff_digits a c b n

end Orthemology.Ninth.SelectorExtraction
