import Mathlib

/-!
Exact score-repair controls for the 2026-09-30 isolated research tranche.
The main polynomial theorem excludes every real coherent repair of a fixed
rational three-outcome forecast. No claim of a kernel proof of the general
analytic rigidity theorem is made by this file.
-/

namespace RepairObstruction

/-- The same arithmetic repair improves both binary log-score products. -/
theorem binary_product_identities (x y : ℝ) :
    let t := (x + 1 - y) / 2
    t ^ 2 - x * (1 - y) = (x + y - 1) ^ 2 / 4 ∧
      (1 - t) ^ 2 - (1 - x) * y = (x + y - 1) ^ 2 / 4 := by
  dsimp
  constructor <;> ring

/-- Exact Euclidean improvement of arithmetic binary coherification. -/
theorem binary_quadratic_identities (x y : ℝ) :
    let t := (x + 1 - y) / 2
    ((x - 1) ^ 2 + y ^ 2) - ((t - 1) ^ 2 + (1 - t) ^ 2) =
        (x + y - 1) ^ 2 / 2 ∧
      (x ^ 2 + (y - 1) ^ 2) - (t ^ 2 + ((1 - t) - 1) ^ 2) =
        (x + y - 1) ^ 2 / 2 := by
  dsimp
  constructor <;> ring

/-- An exact quantitative binary dominance-cell bound with allowed worsening. -/
theorem binary_cell_bound (q D eta delta : ℝ)
    (hqlo : (1 : ℝ) / 2 ≤ q) (hqup : q ≤ (3 : ℝ) / 4)
    (hD : 0 ≤ D) (heta : 0 ≤ eta)
    (hzero : delta ^ 2 + 2 * q * delta ≤ D + eta)
    (hone : delta ^ 2 - 2 * (1 - q) * delta ≤ D + eta) :
    |delta| ≤ 2 * (D + eta) := by
  rcases le_total 0 delta with hpos | hneg
  · rw [abs_of_nonneg hpos]
    have hm := mul_nonneg (sub_nonneg.mpr hqlo) hpos
    nlinarith [sq_nonneg delta]
  · rw [abs_of_nonpos hneg]
    have hm := mul_nonneg (sub_nonneg.mpr hqup) (neg_nonneg.mpr hneg)
    nlinarith [sq_nonneg delta]

/-- Every accepted weighted-quadratic binary repair identifies the norm weight
up to a shrinking interval, before any probabilistic interpretation is added. -/
theorem binary_repair_readout (alpha e t eta : ℝ)
    (ha0 : 0 ≤ alpha) (ha1 : alpha ≤ 1)
    (he0 : 0 ≤ e) (he1 : e ≤ (1 : ℝ) / 4)
    (heta : 0 ≤ eta)
    (hzero : t ^ 2 ≤ alpha * ((1 : ℝ) / 2 + e) ^ 2 +
      (1 - alpha) * ((1 : ℝ) / 2) ^ 2 + eta)
    (hone : (1 - t) ^ 2 ≤ alpha * ((1 : ℝ) / 2 - e) ^ 2 +
      (1 - alpha) * ((1 : ℝ) / 2) ^ 2 + eta) :
    |t - ((1 : ℝ) / 2 + alpha * e)| ≤ e ^ 2 / 2 + 2 * eta := by
  let q : ℝ := 1 / 2 + alpha * e
  let D : ℝ := alpha * (1 - alpha) * e ^ 2
  have hqlo : (1 : ℝ) / 2 ≤ q := by dsimp [q]; nlinarith [mul_nonneg ha0 he0]
  have hqup : q ≤ (3 : ℝ) / 4 := by
    have hmul := mul_le_mul_of_nonneg_right ha1 he0
    dsimp [q]
    nlinarith
  have hD : 0 ≤ D := by
    dsimp [D]
    exact mul_nonneg (mul_nonneg ha0 (sub_nonneg.mpr ha1)) (sq_nonneg e)
  have hzero' : (t - q) ^ 2 + 2 * q * (t - q) ≤ D + eta := by
    dsimp [q, D]
    nlinarith
  have hone' : (t - q) ^ 2 - 2 * (1 - q) * (t - q) ≤ D + eta := by
    dsimp [q, D]
    nlinarith
  have hbound := binary_cell_bound q D eta (t - q) hqlo hqup hD heta hzero' hone'
  have hquarter : D ≤ e ^ 2 / 4 := by
    have hmul := mul_nonneg (sq_nonneg (alpha - (1 : ℝ) / 2)) (sq_nonneg e)
    dsimp [D]
    nlinarith
  dsimp [q] at hbound
  linarith

/-- Quadratic dominance puts every coherent candidate in a tiny rational box. -/
theorem quadratic_box (x y z : ℝ)
    (hsum : x + y + z = 1)
    (h1 : (x - 1) ^ 2 + y ^ 2 + z ^ 2 ≤
      ((501 : ℝ) / 1000 - 1) ^ 2 + ((1 : ℝ) / 3) ^ 2 + ((1 : ℝ) / 6) ^ 2)
    (h2 : x ^ 2 + (y - 1) ^ 2 + z ^ 2 ≤
      ((501 : ℝ) / 1000) ^ 2 + ((1 : ℝ) / 3 - 1) ^ 2 + ((1 : ℝ) / 6) ^ 2)
    (h3 : x ^ 2 + y ^ 2 + (z - 1) ^ 2 ≤
      ((501 : ℝ) / 1000) ^ 2 + ((1 : ℝ) / 3) ^ 2 + ((1 : ℝ) / 6 - 1) ^ 2) :
    (751 : ℝ) / 1500 - 1 / 1000000 ≤ x ∧
      x ≤ (751 : ℝ) / 1500 + 1 / 1000000 ∧
    (333 : ℝ) / 1000 - 1 / 1000000 ≤ y ∧
      y ≤ (333 : ℝ) / 1000 + 1 / 1000000 ∧
    (499 : ℝ) / 3000 - 1 / 1000000 ≤ z ∧
      z ≤ (499 : ℝ) / 3000 + 1 / 1000000 := by
  have hx := sq_nonneg (x - (751 : ℝ) / 1500)
  have hy := sq_nonneg (y - (333 : ℝ) / 1000)
  have hz := sq_nonneg (z - (499 : ℝ) / 3000)
  constructor
  · nlinarith
  constructor
  · nlinarith
  constructor
  · nlinarith
  constructor
  · nlinarith
  constructor <;> nlinarith

/-- No coherent forecast jointly dominates the fixed rational baseline under
Euclidean accuracy and even the third binary-log product constraint. -/
theorem no_common_polynomial_repair (x y z : ℝ)
    (hsum : x + y + z = 1)
    (h1 : (x - 1) ^ 2 + y ^ 2 + z ^ 2 ≤
      ((501 : ℝ) / 1000 - 1) ^ 2 + ((1 : ℝ) / 3) ^ 2 + ((1 : ℝ) / 6) ^ 2)
    (h2 : x ^ 2 + (y - 1) ^ 2 + z ^ 2 ≤
      ((501 : ℝ) / 1000) ^ 2 + ((1 : ℝ) / 3 - 1) ^ 2 + ((1 : ℝ) / 6) ^ 2)
    (h3 : x ^ 2 + y ^ 2 + (z - 1) ^ 2 ≤
      ((501 : ℝ) / 1000) ^ 2 + ((1 : ℝ) / 3) ^ 2 + ((1 : ℝ) / 6 - 1) ^ 2)
    (hlog : ((1 : ℝ) / 6) * (1 - (501 : ℝ) / 1000) * (1 - (1 : ℝ) / 3) ≤
      z * (1 - x) * (1 - y)) : False := by
  obtain ⟨hxl, hxu, hyl, hyu, hzl, hzu⟩ := quadratic_box x y z hsum h1 h2 h3
  have hx1 : x ≤ 1 := by linarith
  have hy1 : y ≤ 1 := by linarith
  have hx : 1 - x ≤ 1 - (751 : ℝ) / 1500 + 1 / 1000000 := by linarith
  have hy : 1 - y ≤ 1 - (333 : ℝ) / 1000 + 1 / 1000000 := by linarith
  have hzx : z * (1 - x) ≤
      ((499 : ℝ) / 3000 + 1 / 1000000) *
        (1 - (751 : ℝ) / 1500 + 1 / 1000000) :=
    mul_le_mul hzu hx (sub_nonneg.mpr hx1) (by norm_num)
  have hprod : z * (1 - x) * (1 - y) ≤
      (((499 : ℝ) / 3000 + 1 / 1000000) *
        (1 - (751 : ℝ) / 1500 + 1 / 1000000)) *
          (1 - (333 : ℝ) / 1000 + 1 / 1000000) :=
    mul_le_mul hzx hy (sub_nonneg.mpr hy1) (by norm_num)
  norm_num at hlog hprod
  linarith


/-- The product certificate is connected to the actual logarithmic loss in
Lean, for interior forecasts where the logarithms express the proper loss. -/
theorem no_common_logarithmic_repair (x y z : ℝ)
    (_hx0 : 0 < x) (hx1 : x < 1)
    (_hy0 : 0 < y) (hy1 : y < 1)
    (hz0 : 0 < z) (_hz1 : z < 1)
    (hsum : x + y + z = 1)
    (h1 : (x - 1) ^ 2 + y ^ 2 + z ^ 2 ≤
      ((501 : ℝ) / 1000 - 1) ^ 2 + ((1 : ℝ) / 3) ^ 2 + ((1 : ℝ) / 6) ^ 2)
    (h2 : x ^ 2 + (y - 1) ^ 2 + z ^ 2 ≤
      ((501 : ℝ) / 1000) ^ 2 + ((1 : ℝ) / 3 - 1) ^ 2 + ((1 : ℝ) / 6) ^ 2)
    (h3 : x ^ 2 + y ^ 2 + (z - 1) ^ 2 ≤
      ((501 : ℝ) / 1000) ^ 2 + ((1 : ℝ) / 3) ^ 2 + ((1 : ℝ) / 6 - 1) ^ 2)
    (hlog : -Real.log z - Real.log (1 - x) - Real.log (1 - y) ≤
      -Real.log ((1 : ℝ) / 6) - Real.log (1 - (501 : ℝ) / 1000) -
        Real.log (1 - (1 : ℝ) / 3)) : False := by
  have hxc : 0 < 1 - x := sub_pos.mpr hx1
  have hyc : 0 < 1 - y := sub_pos.mpr hy1
  have hcpos : 0 < z * (1 - x) * (1 - y) := by positivity
  have hbpos : 0 < ((1 : ℝ) / 6) * (1 - (501 : ℝ) / 1000) *
      (1 - (1 : ℝ) / 3) := by norm_num
  have hcLog : Real.log (z * (1 - x) * (1 - y)) =
      Real.log z + Real.log (1 - x) + Real.log (1 - y) := by
    rw [Real.log_mul (by positivity) (ne_of_gt hyc),
      Real.log_mul (ne_of_gt hz0) (ne_of_gt hxc)]
  have hbLog : Real.log (((1 : ℝ) / 6) * (1 - (501 : ℝ) / 1000) *
      (1 - (1 : ℝ) / 3)) =
      Real.log ((1 : ℝ) / 6) + Real.log (1 - (501 : ℝ) / 1000) +
        Real.log (1 - (1 : ℝ) / 3) := by
    rw [Real.log_mul (by norm_num) (by norm_num),
      Real.log_mul (by norm_num) (by norm_num)]
  have hlogs : Real.log (((1 : ℝ) / 6) * (1 - (501 : ℝ) / 1000) *
      (1 - (1 : ℝ) / 3)) ≤ Real.log (z * (1 - x) * (1 - y)) := by
    rw [hcLog, hbLog]
    linarith
  have hp := (Real.log_le_log_iff hbpos hcpos).mp hlogs
  exact no_common_polynomial_repair x y z hsum h1 h2 h3 hp

/-- The quantitative cell bound expressed as an actual norm-parameter decoder. -/
theorem binary_parameter_decoder (alpha e t eta : ℝ)
    (ha0 : 0 ≤ alpha) (ha1 : alpha ≤ 1)
    (he0 : 0 < e) (he1 : e ≤ (1 : ℝ) / 4)
    (heta : 0 ≤ eta)
    (hzero : t ^ 2 ≤ alpha * ((1 : ℝ) / 2 + e) ^ 2 +
      (1 - alpha) * ((1 : ℝ) / 2) ^ 2 + eta)
    (hone : (1 - t) ^ 2 ≤ alpha * ((1 : ℝ) / 2 - e) ^ 2 +
      (1 - alpha) * ((1 : ℝ) / 2) ^ 2 + eta) :
    |(t - (1 : ℝ) / 2) / e - alpha| ≤ e / 2 + 2 * eta / e := by
  have h := binary_repair_readout alpha e t eta ha0 ha1 he0.le he1 heta hzero hone
  have hdiv : |t - ((1 : ℝ) / 2 + alpha * e)| / e ≤
      (e ^ 2 / 2 + 2 * eta) / e := (div_le_div_iff_of_pos_right he0).mpr h
  have hid : (t - (1 : ℝ) / 2) / e - alpha =
      (t - ((1 : ℝ) / 2 + alpha * e)) / e := by
    field_simp
    <;> ring
  have hrhs : (e ^ 2 / 2 + 2 * eta) / e = e / 2 + 2 * eta / e := by
    field_simp
    <;> ring
  rw [hid, abs_div, abs_of_pos he0, ← hrhs]
  exact hdiv

#print axioms binary_product_identities
#print axioms binary_quadratic_identities
#print axioms binary_cell_bound
#print axioms binary_repair_readout
#print axioms binary_parameter_decoder
#print axioms quadratic_box
#print axioms no_common_polynomial_repair
#print axioms no_common_logarithmic_repair
#check binary_parameter_decoder
#check no_common_logarithmic_repair

end RepairObstruction
