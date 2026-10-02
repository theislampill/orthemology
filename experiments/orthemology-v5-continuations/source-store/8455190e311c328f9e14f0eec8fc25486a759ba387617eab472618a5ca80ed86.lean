import Mathlib

noncomputable section
open scoped Topology
open Set Filter

namespace CriticalZero

def psi (t : ℝ) : ℝ := (t-1/2)^2/2+(2/3)*(t-1/2)^3+(t-1/2)^4
def dpsi (t : ℝ) : ℝ := (t-1/2)+2*(t-1/2)^2+4*(t-1/2)^3
def curvature (t : ℝ) : ℝ := 1+4*(t-1/2)+12*(t-1/2)^2
def div (v t : ℝ) : ℝ := psi v-psi t-dpsi t*(v-t)

def loss (q : ℝ) : ℝ := 2*div 1 q
def baselineF (eps : ℝ) : ℝ := div 1 (1/2+eps)+div 1 (1/2)
def baselineG (eps : ℝ) : ℝ := ((1/2+eps)^2+(1/2)^2)/2
def envelope (eps : ℝ) : ℝ := 1/2+eps/2+eps^2/4-eps^3/8

def tailP (eps : ℝ) : ℝ :=
  9*eps^9-72*eps^8+72*eps^7+592*eps^6-816*eps^5-2304*eps^4+
    1696*eps^3+4992*eps^2-17280*eps+2304

lemma psi_deriv (t : ℝ) : HasDerivAt psi (dpsi t) t := by
  have h := (hasDerivAt_id t).sub_const (1/2)
  convert (((h.pow 2).div_const 2).add ((h.pow 3).const_mul (2/3))).add (h.pow 4) using 1 <;>
    simp [psi,dpsi] <;> ring

lemma dpsi_deriv (t : ℝ) : HasDerivAt dpsi (curvature t) t := by
  have h := (hasDerivAt_id t).sub_const (1/2)
  convert (h.add ((h.pow 2).const_mul 2)).add ((h.pow 3).const_mul 4) using 1 <;>
    simp [dpsi,curvature] <;> ring

lemma curvature_pos (t : ℝ) : 0 < curvature t := by
  have heq : curvature t = 12*(t-1/3)^2+2/3 := by dsimp [curvature]; ring
  rw [heq]
  nlinarith [sq_nonneg (t-1/3)]

lemma loss_deriv (q : ℝ) : HasDerivAt loss (2*(q-1)*curvature q) q := by
  have hh := ((((hasDerivAt_const q (psi 1)).sub (psi_deriv q)).sub
    ((dpsi_deriv q).mul ((hasDerivAt_const q 1).sub (hasDerivAt_id q)))).const_mul 2)
  convert hh using 1 <;> dsimp [loss, div] <;> ring

lemma loss_strictAnti : StrictAntiOn loss (Icc 0 1) := by
  apply strictAntiOn_of_deriv_neg (convex_Icc 0 1)
  · intro q hq
    exact (loss_deriv q).continuousAt.continuousWithinAt
  · intro q hq
    have hq' : q ∈ Ioo 0 1 := by simpa only [interior_Icc] using hq
    rw [(loss_deriv q).deriv]
    have hr := curvature_pos q
    exact mul_neg_of_neg_of_pos (mul_neg_of_pos_of_neg (by norm_num) (by linarith [hq'.2])) hr

lemma envelope_excess (eps : ℝ) :
    (envelope eps)^2-baselineG eps = eps^3*(eps^3-4*eps^2-4*eps+8)/64 := by
  dsimp [envelope,baselineG]
  ring

lemma nonlinear_excess (eps : ℝ) :
    loss (envelope eps)-baselineF eps = eps^3*tailP eps/6144 := by
  dsimp [loss,envelope,baselineF,tailP,div,psi,dpsi]
  ring

lemma tailP_pos (eps : ℝ) (he : 0 < eps) (hu : eps ≤ 1/100) : 0 < tailP eps := by
  have h1 : eps ≤ 1 := by linarith
  have h4 : eps^4 ≤ eps := by simpa using pow_le_pow_of_le_one he.le h1 (show 1 ≤ 4 by norm_num)
  have h5 : eps^5 ≤ eps := by simpa using pow_le_pow_of_le_one he.le h1 (show 1 ≤ 5 by norm_num)
  have h8 : eps^8 ≤ eps := by simpa using pow_le_pow_of_le_one he.le h1 (show 1 ≤ 8 by norm_num)
  have hp : 0 ≤ 9*eps^9+72*eps^7+592*eps^6+1696*eps^3+4992*eps^2 := by positivity
  dsimp [tailP]
  nlinarith

lemma envelope_mem (eps : ℝ) (he : 0 < eps) (hu : eps ≤ 1/100) : envelope eps ∈ Ioo 0 1 := by
  have h1 : eps ≤ 1 := by linarith
  have h2 : eps^2 ≤ eps := by simpa using pow_le_pow_of_le_one he.le h1 (show 1 ≤ 2 by norm_num)
  have h3 : eps^3 ≤ eps := by simpa using pow_le_pow_of_le_one he.le h1 (show 1 ≤ 3 by norm_num)
  have hp3 : 0 ≤ eps^3 := pow_nonneg he.le 3
  dsimp [envelope]
  constructor <;> nlinarith [sq_nonneg eps]

/-- Actual exact nonlinear failure on a rational interval despite a feasible
zero-margin second-order programme. -/
theorem no_exact_repair (eps : ℝ) (he : 0 < eps) (hu : eps ≤ 1/100) :
    ¬ ∃ q ∈ Icc (0:ℝ) 1, q^2 ≤ baselineG eps ∧ loss q ≤ baselineF eps := by
  rintro ⟨q,hq,hG,hF⟩
  have henv := envelope_mem eps he hu
  have he2 : eps^2 ≤ (1:ℝ)/10000 := by nlinarith
  have hbr : 0 < eps^3-4*eps^2-4*eps+8 := by nlinarith [pow_pos he 3]
  have hex : 0 < (envelope eps)^2-baselineG eps := by
    rw [envelope_excess]
    exact div_pos (mul_pos (pow_pos he 3) hbr) (by norm_num)
  have hqlt : q < envelope eps := by
    by_contra hn
    have hsq := pow_le_pow_left₀ henv.1.le (le_of_not_gt hn) 2
    linarith
  have hmono := loss_strictAnti hq ⟨henv.1.le,henv.2.le⟩ hqlt
  have hbad : 0 < loss (envelope eps)-baselineF eps := by
    rw [nonlinear_excess]
    exact div_pos (mul_pos (pow_pos he 3) (tailP_pos eps he hu)) (by norm_num)
  linarith

/-- The four second-order coefficients at the specified context and ray. -/
def leading (b : ℝ) : Fin 4 → ℝ := ![1/4-b,1/4+b,3/4-b,b-1/4]

theorem second_order_optimum_zero :
    (∀ i : Fin 4, 0 ≤ leading (1/4) i) ∧
    (∀ b tau : ℝ, (∀ i : Fin 4, tau ≤ leading b i) → tau ≤ 0) := by
  constructor
  · intro i
    fin_cases i <;> norm_num [leading]
  · intro b tau hh
    have h0 := hh 0
    have h3 := hh 3
    norm_num [leading] at h0 h3
    change tau ≤ b-1/4 at h3
    linarith

def fRem (a b eps : ℝ) : ℝ :=
  (5/2-3*a-(3-4*a)*b) + (21/8-(3-4*a)*b^2-(5-6*a)*b)*eps +
    (-(10-12*a)*b^2-3*b)*eps^2 + (-(20/3-8*a)*b^3-9*b^2)*eps^3 -
    12*b^3*eps^4-6*b^4*eps^5

/-- Exact score identity binds the nonlinear pair of LP coefficients. -/
lemma actual_second_order_F (a b eps : ℝ) :
    div a (1/2+eps)+div a (1/2)-2*div a (1/2+eps/2+eps^2*b) =
      eps^2*(1/4+(1/2-a)*(1-2*b)+eps*fRem a b eps) := by
  dsimp [div,psi,dpsi,fRem]
  ring

lemma actual_second_order_G (a b eps : ℝ) :
    ((1/2+eps-a)^2+(1/2-a)^2)/2-(1/2+eps/2+eps^2*b-a)^2 =
      eps^2*(1/4-2*(1/2-a)*b+eps*(-b-eps*b^2)) := by
  ring

#print axioms no_exact_repair
#print axioms second_order_optimum_zero
#print axioms actual_second_order_F
end CriticalZero
