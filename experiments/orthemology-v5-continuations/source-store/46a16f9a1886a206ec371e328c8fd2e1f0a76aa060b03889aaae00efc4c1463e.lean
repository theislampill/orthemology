import PolynomialAND

noncomputable section
open scoped Topology
open Set Filter PolynomialAND

namespace IsolatedObstruction

def envelope (eps : ℝ) : ℝ := 1/4+eps/2+13*eps^2/24
def baseA (eps : ℝ) : ℝ := ((1/4+eps)^2+(1/4)^2)/2
def tailP (eps : ℝ) : ℝ :=
  28561*eps^6+105456*eps^5+128440*eps^4+41184*eps^3-
    246864*eps^2-63360*eps+3456

def endpointLoss (q : ℝ) : ℝ := 2*scalarDiv 1 q

def nonlinearBaseline (eps : ℝ) : ℝ := scalarDiv 1 (1/4+eps)+scalarDiv 1 (1/4)

lemma envelope_excess (eps : ℝ) :
    (envelope eps)^2-baseA eps = eps^2*(169*eps^2+312*eps+12)/576 := by
  dsimp [envelope, baseA]
  ring

lemma nonlinear_excess (eps : ℝ) :
    endpointLoss (envelope eps)-nonlinearBaseline eps = eps^2*tailP eps/13824 := by
  dsimp [endpointLoss, nonlinearBaseline, envelope, tailP, scalarDiv, psi, dpsi]
  ring

lemma tailP_pos (eps : ℝ) (he : 0 < eps) (hu : eps ≤ 1/100) : 0 < tailP eps := by
  have he2 : eps^2 ≤ (1:ℝ)/10000 := by nlinarith
  have hp : 0 ≤ 28561*eps^6+105456*eps^5+128440*eps^4+41184*eps^3 := by positivity
  dsimp [tailP]
  nlinarith

lemma envelope_mem (eps : ℝ) (he : 0 < eps) (hu : eps ≤ 1/100) :
    envelope eps ∈ Ioo 0 1 := by
  have he2 : eps^2 ≤ (1:ℝ)/10000 := by nlinarith
  dsimp [envelope]
  constructor <;> nlinarith [sq_nonneg eps]

lemma endpointLoss_deriv (q : ℝ) :
    HasDerivAt endpointLoss (2*(q-1)*curvature q) q := by
  have hh := ((((hasDerivAt_const q (psi 1)).sub (psi_deriv q)).sub
    ((dpsi_deriv q).mul ((hasDerivAt_const q 1).sub (hasDerivAt_id q)))).const_mul 2)
  convert hh using 1 <;> dsimp [endpointLoss, scalarDiv] <;> ring

lemma endpointLoss_strictAnti : StrictAntiOn endpointLoss (Icc 0 1) := by
  apply strictAntiOn_of_deriv_neg (convex_Icc 0 1)
  · intro q hq
    exact (endpointLoss_deriv q).continuousAt.continuousWithinAt
  · intro q hq
    have hq' : q ∈ Ioo 0 1 := by simpa only [interior_Icc] using hq
    rw [(endpointLoss_deriv q).deriv]
    have hr := curvature_pos q
    have hneg : q-1 < 0 := by linarith [hq'.2]
    exact mul_neg_of_neg_of_pos (mul_neg_of_pos_of_neg (by norm_num) hneg) hr

/-- Full rational epsilon interval, with genuine nonlinear score inequalities. -/
theorem no_isolated_common_repair (eps : ℝ) (he : 0 < eps) (hu : eps ≤ 1/100) :
    ¬ ∃ q ∈ Icc (0:ℝ) 1,
      q^2 ≤ baseA eps ∧ endpointLoss q ≤ nonlinearBaseline eps := by
  rintro ⟨q, hq, hquad, hnonlin⟩
  have henv := envelope_mem eps he hu
  have hexc : 0 < (envelope eps)^2-baseA eps := by
    rw [envelope_excess]
    positivity
  have hqlt : q < envelope eps := by
    by_contra hh
    have hle : envelope eps ≤ q := le_of_not_gt hh
    have hsq := pow_le_pow_left₀ henv.1.le hle 2
    linarith
  have hmono := endpointLoss_strictAnti hq ⟨henv.1.le,henv.2.le⟩ hqlt
  have hnlexc : 0 < endpointLoss (envelope eps)-nonlinearBaseline eps := by
    rw [nonlinear_excess]
    exact div_pos (mul_pos (pow_pos he 2) (tailP_pos eps he hu)) (by norm_num)
  linarith

def isoQuadratic (a t1 t2 : ℝ) : ℝ := ((t1-a)^2+(t2-a)^2)/2

theorem no_isolated_all_state_repair (eps : ℝ) (he : 0 < eps) (hu : eps ≤ 1/100) :
    ¬ ∃ q ∈ Icc (0:ℝ) 1,
      (∀ a : Fin 2, isoQuadratic (a.val:ℝ) q q ≤
        isoQuadratic (a.val:ℝ) (1/4+eps) (1/4)) ∧
      (∀ a : Fin 2, scalarDiv (a.val:ℝ) q+scalarDiv (a.val:ℝ) q ≤
        scalarDiv (a.val:ℝ) (1/4+eps)+scalarDiv (a.val:ℝ) (1/4)) := by
  rintro ⟨q,hq,hG,hF⟩
  apply no_isolated_common_repair eps he hu
  refine ⟨q,hq,?_,?_⟩
  · have hg := hG 0
    norm_num [isoQuadratic] at hg
    dsimp [baseA]
    nlinarith
  · have hf := hF 1
    simpa [endpointLoss, nonlinearBaseline, two_mul] using hf

/-- The same score's isolated log-curvature slope violates the exact criterion. -/
theorem isolated_slope_violation :
    (96*(1/4 : ℝ))/curvature (1/4) > 1/((1/4)*(1-1/4)) := by
  norm_num [curvature]

#print axioms no_isolated_common_repair
end IsolatedObstruction
