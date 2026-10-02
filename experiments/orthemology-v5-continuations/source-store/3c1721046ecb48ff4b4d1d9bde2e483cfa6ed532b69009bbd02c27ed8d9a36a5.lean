import Mathlib

noncomputable section
open scoped BigOperators Topology
open Set Filter

namespace PolynomialAND

def bernstein5 (b0 b1 b2 b3 b4 b5 t : ℝ) : ℝ :=
  b0 * (1-t)^5 + 5*b1*t*(1-t)^4 + 10*b2*t^2*(1-t)^3 +
    10*b3*t^3*(1-t)^2 + 5*b4*t^4*(1-t) + b5*t^5

lemma bernstein5_lower (b0 b1 b2 b3 b4 b5 m t : ℝ)
    (ht0 : 0 ≤ t) (ht1 : t ≤ 1)
    (h0 : m ≤ b0) (h1 : m ≤ b1) (h2 : m ≤ b2)
    (h3 : m ≤ b3) (h4 : m ≤ b4) (h5 : m ≤ b5) :
    m ≤ bernstein5 b0 b1 b2 b3 b4 b5 t := by
  have hu : 0 ≤ 1-t := sub_nonneg.mpr ht1
  have hb1 : 0 ≤ b1-m := sub_nonneg.mpr h1
  have hb2 : 0 ≤ b2-m := sub_nonneg.mpr h2
  have hb3 : 0 ≤ b3-m := sub_nonneg.mpr h3
  have hb4 : 0 ≤ b4-m := sub_nonneg.mpr h4
  have H0 : 0 ≤ (b0-m)*(1-t)^5 := mul_nonneg (sub_nonneg.mpr h0) (pow_nonneg hu _)
  have H1 : 0 ≤ 5*(b1-m)*t*(1-t)^4 := by positivity
  have H2 : 0 ≤ 10*(b2-m)*t^2*(1-t)^3 := by positivity
  have H3 : 0 ≤ 10*(b3-m)*t^3*(1-t)^2 := by positivity
  have H4 : 0 ≤ 5*(b4-m)*t^4*(1-t) := by positivity
  have H5 : 0 ≤ (b5-m)*t^5 := mul_nonneg (sub_nonneg.mpr h5) (pow_nonneg ht0 _)
  dsimp [bernstein5]
  nlinarith [H0, H1, H2, H3, H4, H5]

def certificateP (s : ℝ) : ℝ :=
  -2304*s^5-2304*s^4+14304*s^3-4896*s^2+99*s+99

lemma certificateP_cell0 (s : ℝ) (hlo : (0 : ℝ)/8 ≤ s)
    (hhi : s ≤ (1 : ℝ)/8) : (132 : ℝ)/5 ≤ certificateP s := by
  have ht0 : 0 ≤ 8*s-0 := by linarith
  have ht1 : 8*s-0 ≤ 1 := by linarith
  have hb := bernstein5_lower 99 (4059 / 40) (963 / 10) (13803 / 160) (1185 / 16) (7959 / 128) (132/5) (8*s-0) ht0 ht1
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  have heq : certificateP s = bernstein5 99 (4059 / 40) (963 / 10) (13803 / 160) (1185 / 16) (7959 / 128) (8*s-0) := by
    dsimp [certificateP, bernstein5]
    ring
  rw [heq]
  exact hb
lemma certificateP_cell1 (s : ℝ) (hlo : (1 : ℝ)/8 ≤ s)
    (hhi : s ≤ (2 : ℝ)/8) : (132 : ℝ)/5 ≤ certificateP s := by
  have ht0 : 0 ≤ 8*s-1 := by linarith
  have ht1 : 8*s-1 ≤ 1 := by linarith
  have hb := bernstein5_lower (7959 / 128) (3219 / 64) (3099 / 80) 30 (132 / 5) 30 (132/5) (8*s-1) ht0 ht1
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  have heq : certificateP s = bernstein5 (7959 / 128) (3219 / 64) (3099 / 80) 30 (132 / 5) 30 (8*s-1) := by
    dsimp [certificateP, bernstein5]
    ring
  rw [heq]
  exact hb
lemma certificateP_cell2 (s : ℝ) (hlo : (2 : ℝ)/8 ≤ s)
    (hhi : s ≤ (3 : ℝ)/8) : (132 : ℝ)/5 ≤ certificateP s := by
  have ht0 : 0 ≤ 8*s-2 := by linarith
  have ht1 : 8*s-2 ≤ 1 := by linarith
  have hb := bernstein5_lower 30 (168 / 5) (222 / 5) (5157 / 80) (30591 / 320) (17829 / 128) (132/5) (8*s-2) ht0 ht1
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  have heq : certificateP s = bernstein5 30 (168 / 5) (222 / 5) (5157 / 80) (30591 / 320) (17829 / 128) (8*s-2) := by
    dsimp [certificateP, bernstein5]
    ring
  rw [heq]
  exact hb
lemma certificateP_cell3 (s : ℝ) (hlo : (3 : ℝ)/8 ≤ s)
    (hhi : s ≤ (4 : ℝ)/8) : (132 : ℝ)/5 ≤ certificateP s := by
  have ht0 : 0 ≤ 8*s-3 := by linarith
  have ht1 : 8*s-3 ≤ 1 := by linarith
  have hb := bernstein5_lower (17829 / 128) (29277 / 160) (38277 / 160) (12381 / 40) (15801 / 40) (993 / 2) (132/5) (8*s-3) ht0 ht1
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  have heq : certificateP s = bernstein5 (17829 / 128) (29277 / 160) (38277 / 160) (12381 / 40) (15801 / 40) (993 / 2) (8*s-3) := by
    dsimp [certificateP, bernstein5]
    ring
  rw [heq]
  exact hb
lemma certificateP_cell4 (s : ℝ) (hlo : (4 : ℝ)/8 ≤ s)
    (hhi : s ≤ (5 : ℝ)/8) : (132 : ℝ)/5 ≤ certificateP s := by
  have ht0 : 0 ≤ 8*s-4 := by linarith
  have ht1 : 8*s-4 ≤ 1 := by linarith
  have hb := bernstein5_lower (993 / 2) (23919 / 40) (28617 / 40) (135939 / 160) (160149 / 160) (149667 / 128) (132/5) (8*s-4) ht0 ht1
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  have heq : certificateP s = bernstein5 (993 / 2) (23919 / 40) (28617 / 40) (135939 / 160) (160149 / 160) (149667 / 128) (8*s-4) := by
    dsimp [certificateP, bernstein5]
    ring
  rw [heq]
  exact hb
lemma certificateP_cell5 (s : ℝ) (hlo : (5 : ℝ)/8 ≤ s)
    (hhi : s ≤ (6 : ℝ)/8) : (132 : ℝ)/5 ≤ certificateP s := by
  have ht0 : 0 ≤ 8*s-5 := by linarith
  have ht1 : 8*s-5 ≤ 1 := by linarith
  have hb := bernstein5_lower (149667 / 128) (428037 / 320) (121839 / 80) (17253 / 10) 1944 2178 (132/5) (8*s-5) ht0 ht1
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  have heq : certificateP s = bernstein5 (149667 / 128) (428037 / 320) (121839 / 80) (17253 / 10) 1944 2178 (8*s-5) := by
    dsimp [certificateP, bernstein5]
    ring
  rw [heq]
  exact hb
lemma certificateP_cell6 (s : ℝ) (hlo : (6 : ℝ)/8 ≤ s)
    (hhi : s ≤ (7 : ℝ)/8) : (132 : ℝ)/5 ≤ certificateP s := by
  have ht0 : 0 ≤ 8*s-6 := by linarith
  have ht1 : 8*s-6 ≤ 1 := by linarith
  have hb := bernstein5_lower 2178 2412 (26613 / 10) (46797 / 16) (1024293 / 320) (446385 / 128) (132/5) (8*s-6) ht0 ht1
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  have heq : certificateP s = bernstein5 2178 2412 (26613 / 10) (46797 / 16) (1024293 / 320) (446385 / 128) (8*s-6) := by
    dsimp [certificateP, bernstein5]
    ring
  rw [heq]
  exact hb
lemma certificateP_cell7 (s : ℝ) (hlo : (7 : ℝ)/8 ≤ s)
    (hhi : s ≤ (8 : ℝ)/8) : (132 : ℝ)/5 ≤ certificateP s := by
  have ht0 : 0 ≤ 8*s-7 := by linarith
  have ht1 : 8*s-7 ≤ 1 := by linarith
  have hb := bernstein5_lower (446385 / 128) (75477 / 20) (651309 / 160) (87513 / 20) (187437 / 40) 4998 (132/5) (8*s-7) ht0 ht1
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  have heq : certificateP s = bernstein5 (446385 / 128) (75477 / 20) (651309 / 160) (87513 / 20) (187437 / 40) 4998 (8*s-7) := by
    dsimp [certificateP, bernstein5]
    ring
  rw [heq]
  exact hb
theorem certificateP_lower (s : ℝ) (hs0 : 0 ≤ s) (hs1 : s ≤ 1) :
    (132 : ℝ)/5 ≤ certificateP s := by
  by_cases h0 : s ≤ (1 : ℝ)/8
  · exact certificateP_cell0 s (by simpa using hs0) h0
  by_cases h1 : s ≤ (2 : ℝ)/8
  · exact certificateP_cell1 s (by linarith) h1
  by_cases h2 : s ≤ (3 : ℝ)/8
  · exact certificateP_cell2 s (by linarith) h2
  by_cases h3 : s ≤ (4 : ℝ)/8
  · exact certificateP_cell3 s (by linarith) h3
  by_cases h4 : s ≤ (5 : ℝ)/8
  · exact certificateP_cell4 s (by linarith) h4
  by_cases h5 : s ≤ (6 : ℝ)/8
  · exact certificateP_cell5 s (by linarith) h5
  by_cases h6 : s ≤ (7 : ℝ)/8
  · exact certificateP_cell6 s (by linarith) h6
  exact certificateP_cell7 s (by linarith) (by simpa using hs1)

def psi (t : ℝ) : ℝ := t^2/2+4*t^4
def dpsi (t : ℝ) : ℝ := t+16*t^3
def curvature (s : ℝ) : ℝ := 1+48*s^2

def scalarDiv (v t : ℝ) : ℝ := psi v-psi t-dpsi t*(v-t)

lemma psi_deriv (t : ℝ) : HasDerivAt psi (dpsi t) t := by
  convert ((hasDerivAt_id t).pow 2).div_const 2 |>.add
    (((hasDerivAt_id t).pow 4).const_mul 4) using 1 <;> simp [psi, dpsi] <;> ring

lemma dpsi_deriv (t : ℝ) : HasDerivAt dpsi (curvature t) t := by
  convert (hasDerivAt_id t).add (((hasDerivAt_id t).pow 3).const_mul 16) using 1 <;>
    simp [dpsi, curvature] <;> ring

lemma curvature_pos (t : ℝ) : 0 < curvature t := by
  dsimp [curvature]
  nlinarith [sq_nonneg t]

lemma scalarDiv_expansion (v t : ℝ) :
    scalarDiv v t = (v-t)^2/2+4*v^4+12*t^4-16*v*t^3 := by
  dsimp [scalarDiv, psi, dpsi]
  ring

end PolynomialAND
