import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Push
import Aesop

/-!
# Scalar positivity certificates for the truncated moment obstruction

The certificates here are independent of the multivariate-polynomial encoding.
Every identity and inequality is checked by Lean; no extra axioms are introduced.
-/

namespace TruncatedMoment

/-- The dehomogenized Choi–Lam polynomial. -/
def choiLam (x y z : ℝ) : ℝ :=
  1 - 4 * x * y * z + x ^ 2 * y ^ 2 + x ^ 2 * z ^ 2 + y ^ 2 * z ^ 2

/-- The square certificate used when `x * y` is nonnegative. -/
theorem choiLam_pos_product_identity (x y z : ℝ) :
    choiLam x y z =
      (x * y - 1) ^ 2 + z ^ 2 * (x - y) ^ 2 + 2 * (x * y) * (z - 1) ^ 2 := by
  unfold choiLam
  ring

/-- The square certificate used when `x * y` is nonpositive. -/
theorem choiLam_neg_product_identity (x y z : ℝ) :
    choiLam x y z =
      (x * y + 1) ^ 2 + z ^ 2 * (x + y) ^ 2 - 2 * (x * y) * (z + 1) ^ 2 := by
  unfold choiLam
  ring

/-- Global nonnegativity of the Choi–Lam polynomial. -/
theorem choiLam_nonneg (x y z : ℝ) : 0 ≤ choiLam x y z := by
  by_cases hxy : 0 ≤ x * y
  · rw [choiLam_pos_product_identity]
    exact add_nonneg
      (add_nonneg (sq_nonneg _) (mul_nonneg (sq_nonneg _) (sq_nonneg _)))
      (mul_nonneg (mul_nonneg (by norm_num) hxy) (sq_nonneg _))
  · rw [choiLam_neg_product_identity]
    have hxy' : x * y ≤ 0 := le_of_not_ge hxy
    have hp : 2 * (x * y) * (z + 1) ^ 2 ≤ 0 :=
      mul_nonpos_of_nonpos_of_nonneg
        (mul_nonpos_of_nonneg_of_nonpos (by norm_num) hxy') (sq_nonneg _)
    exact sub_nonneg.mpr (le_trans hp
      (add_nonneg (sq_nonneg _) (mul_nonneg (sq_nonneg _) (sq_nonneg _))))

/-- The four-dimensional even-parity block. -/
def evenBlock (c a b d : ℝ) : ℝ :=
  c ^ 2 + 8 * c * (a + b + d) + 50 * (a ^ 2 + b ^ 2 + d ^ 2) +
    2 * (a * b + a * d + b * d)

/-- A rational sum-of-squares certificate for the even block. -/
theorem evenBlock_identity (c a b d : ℝ) :
    evenBlock c a b d =
      (c + 4 * (a + b + d)) ^ 2 + 4 * (a ^ 2 + b ^ 2 + d ^ 2) +
        15 * ((a - b) ^ 2 + (a - d) ^ 2 + (b - d) ^ 2) := by
  unfold evenBlock
  ring

theorem evenBlock_nonneg (c a b d : ℝ) : 0 ≤ evenBlock c a b d := by
  rw [evenBlock_identity]
  nlinarith [sq_nonneg (c + 4 * (a + b + d)), sq_nonneg a, sq_nonneg b,
    sq_nonneg d, sq_nonneg (a - b), sq_nonneg (a - d), sq_nonneg (b - d)]

/-- The even block vanishes exactly at the origin. -/
theorem evenBlock_eq_zero_iff (c a b d : ℝ) :
    evenBlock c a b d = 0 ↔ c = 0 ∧ a = 0 ∧ b = 0 ∧ d = 0 := by
  constructor
  · intro h
    rw [evenBlock_identity] at h
    have hs : 0 ≤ (c + 4 * (a + b + d)) ^ 2 := sq_nonneg _
    have ht : 0 ≤ (a - b) ^ 2 + (a - d) ^ 2 + (b - d) ^ 2 :=
      add_nonneg (add_nonneg (sq_nonneg _) (sq_nonneg _)) (sq_nonneg _)
    have ha : a = 0 := by nlinarith [sq_nonneg a, sq_nonneg b, sq_nonneg d]
    have hb : b = 0 := by nlinarith [sq_nonneg a, sq_nonneg b, sq_nonneg d]
    have hd : d = 0 := by nlinarith [sq_nonneg a, sq_nonneg b, sq_nonneg d]
    subst a
    subst b
    subst d
    have hc : c = 0 := by nlinarith [sq_nonneg c]
    exact ⟨hc, rfl, rfl, rfl⟩
  · rintro ⟨rfl, rfl, rfl, rfl⟩
    norm_num [evenBlock]

/-- A two-dimensional odd-parity block. -/
def oddBlock (u v : ℝ) : ℝ := 4 * u ^ 2 + 3 * u * v + v ^ 2

/-- A rational sum-of-squares certificate for each odd block. -/
theorem oddBlock_identity (u v : ℝ) :
    oddBlock u v = (2 * u + 3 * v / 4) ^ 2 + 7 * v ^ 2 / 16 := by
  unfold oddBlock
  ring

theorem oddBlock_nonneg (u v : ℝ) : 0 ≤ oddBlock u v := by
  rw [oddBlock_identity]
  nlinarith [sq_nonneg (2 * u + 3 * v / 4), sq_nonneg v]

/-- Each odd block vanishes exactly at the origin. -/
theorem oddBlock_eq_zero_iff (u v : ℝ) :
    oddBlock u v = 0 ↔ u = 0 ∧ v = 0 := by
  constructor
  · intro h
    rw [oddBlock_identity] at h
    have hv : v = 0 := by nlinarith [sq_nonneg (2 * u + 3 * v / 4), sq_nonneg v]
    subst v
    have hu : u = 0 := by nlinarith [sq_nonneg u]
    exact ⟨hu, rfl⟩
  · rintro ⟨rfl, rfl⟩
    norm_num [oddBlock]

/-- The full ten-dimensional quadratic moment form, in parity-block order. -/
def momentForm (c a b d u₁ v₁ u₂ v₂ u₃ v₃ : ℝ) : ℝ :=
  evenBlock c a b d + oddBlock u₁ v₁ + oddBlock u₂ v₂ + oddBlock u₃ v₃

theorem momentForm_nonneg (c a b d u₁ v₁ u₂ v₂ u₃ v₃ : ℝ) :
    0 ≤ momentForm c a b d u₁ v₁ u₂ v₂ u₃ v₃ := by
  exact add_nonneg (add_nonneg (add_nonneg (evenBlock_nonneg c a b d)
    (oddBlock_nonneg u₁ v₁)) (oddBlock_nonneg u₂ v₂)) (oddBlock_nonneg u₃ v₃)

/-- Vanishing of the full form forces all ten coefficients to vanish. -/
theorem momentForm_eq_zero_iff (c a b d u₁ v₁ u₂ v₂ u₃ v₃ : ℝ) :
    momentForm c a b d u₁ v₁ u₂ v₂ u₃ v₃ = 0 ↔
      c = 0 ∧ a = 0 ∧ b = 0 ∧ d = 0 ∧
      u₁ = 0 ∧ v₁ = 0 ∧ u₂ = 0 ∧ v₂ = 0 ∧ u₃ = 0 ∧ v₃ = 0 := by
  constructor
  · intro h
    have he := evenBlock_nonneg c a b d
    have h₁ := oddBlock_nonneg u₁ v₁
    have h₂ := oddBlock_nonneg u₂ v₂
    have h₃ := oddBlock_nonneg u₃ v₃
    unfold momentForm at h
    have he0 : evenBlock c a b d = 0 := by linarith
    have h₁0 : oddBlock u₁ v₁ = 0 := by linarith
    have h₂0 : oddBlock u₂ v₂ = 0 := by linarith
    have h₃0 : oddBlock u₃ v₃ = 0 := by linarith
    obtain ⟨hc, ha, hb, hd⟩ := (evenBlock_eq_zero_iff c a b d).mp he0
    obtain ⟨hu₁, hv₁⟩ := (oddBlock_eq_zero_iff u₁ v₁).mp h₁0
    obtain ⟨hu₂, hv₂⟩ := (oddBlock_eq_zero_iff u₂ v₂).mp h₂0
    obtain ⟨hu₃, hv₃⟩ := (oddBlock_eq_zero_iff u₃ v₃).mp h₃0
    exact ⟨hc, ha, hb, hd, hu₁, hv₁, hu₂, hv₂, hu₃, hv₃⟩
  · rintro ⟨rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl⟩
    norm_num [momentForm, evenBlock, oddBlock]

/-- Strict positivity is equivalent to at least one nonzero coefficient. -/
theorem momentForm_pos_iff (c a b d u₁ v₁ u₂ v₂ u₃ v₃ : ℝ) :
    0 < momentForm c a b d u₁ v₁ u₂ v₂ u₃ v₃ ↔
      c ≠ 0 ∨ a ≠ 0 ∨ b ≠ 0 ∨ d ≠ 0 ∨
      u₁ ≠ 0 ∨ v₁ ≠ 0 ∨ u₂ ≠ 0 ∨ v₂ ≠ 0 ∨ u₃ ≠ 0 ∨ v₃ ≠ 0 := by
  have hn := momentForm_nonneg c a b d u₁ v₁ u₂ v₂ u₃ v₃
  have hz := momentForm_eq_zero_iff c a b d u₁ v₁ u₂ v₂ u₃ v₃
  constructor
  · intro hp
    by_contra h
    push_neg at h
    have heq := hz.mpr h
    linarith
  · intro h
    have hne : momentForm c a b d u₁ v₁ u₂ v₂ u₃ v₃ ≠ 0 := by
      intro hzero
      rcases hz.mp hzero with ⟨hc, ha, hb, hd, hu₁, hv₁, hu₂, hv₂, hu₃, hv₃⟩
      aesop
    exact lt_of_le_of_ne hn (Ne.symm hne)

end TruncatedMoment

#print axioms TruncatedMoment.choiLam_nonneg
#print axioms TruncatedMoment.evenBlock_eq_zero_iff
#print axioms TruncatedMoment.oddBlock_eq_zero_iff
#print axioms TruncatedMoment.momentForm_nonneg
#print axioms TruncatedMoment.momentForm_eq_zero_iff
#print axioms TruncatedMoment.momentForm_pos_iff
