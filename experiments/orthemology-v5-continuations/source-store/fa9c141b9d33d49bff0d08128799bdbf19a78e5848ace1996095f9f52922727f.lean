import ANDIntrinsic
import IsolatedObstruction

noncomputable section
open Set PolynomialAND ANDCorrection ANDScore ANDRepair ANDPotentialBinding
open scoped BigOperators

namespace PolynomialANDAudit

/-- Independent check: the actual hull forces equality of coordinates 0 and 1. -/
theorem hull_diagonal (p : Vec) (hp : p ∈ hull) : p 0 = p 1 := by
  obtain ⟨a, _, _, ha⟩ := FiniteHullWeights.finite_convex_weights truth p hp
  have h0 := congrArg (fun v : Vec => v 0) ha
  have h1 := congrArg (fun v : Vec => v 1) ha
  simp [truth, Fin.sum_univ_succ] at h0 h1
  linarith

/-- Every baseline in the main theorem really is outside the coherent hull. -/
theorem transverse_baseline_outside (s z w h1 h2 hz hw eps : ℝ)
    (hne : h1 ≠ h2) (he : eps ≠ 0) :
    baseline s z w h1 h2 hz hw eps ∉ hull := by
  intro hc
  have hd := hull_diagonal _ hc
  simp [baseline] at hd
  exact hd.elim hne he

/-- Dropping transversality cannot leave a strict repair claim for this candidate. -/
theorem tangent_candidate_eq (s z w h hz hw eps : ℝ) :
    candidate s z w h h hz hw eps = baseline s z w h h hz hw eps := by
  ext i
  fin_cases i <;> simp [candidate, baseline, mean, variance, beta, gamma]

theorem tangent_not_strict (s z w h hz hw eps : ℝ) :
    ¬ scoreG (truth 0) (candidate s z w h h hz hw eps) <
      scoreG (truth 0) (baseline s z w h h hz hw eps) := by
  rw [tangent_candidate_eq]
  exact lt_irrefl _

/-- The affine coordinate reflection gives exactly the original Boolean AND vectors. -/
def naturalTruth : Fin 4 → Vec :=
  ![![0,1,0,0], ![0,1,1,0], ![0,1,0,1], ![1,0,1,1]]
def reflect (v : Vec) : Vec := ![v 0,1-v 1,v 2,v 3]

theorem reflect_involutive (v : Vec) : reflect (reflect v) = v := by
  ext i
  fin_cases i <;> simp [reflect]

theorem natural_truth_binding (i : Fin 4) : reflect (naturalTruth i) = truth i := by
  fin_cases i <;> ext j <;> fin_cases j <;> norm_num [naturalTruth, truth, reflect] <;> rfl

/-- Formal curvature audit: the scalar nonlinear potential is strictly convex on all reals. -/
theorem psi_strictConvex : StrictConvexOn ℝ univ psi := by
  have hfirst : deriv psi = dpsi := funext (fun t => (psi_deriv t).deriv)
  have hsecond : deriv dpsi = curvature := funext (fun t => (dpsi_deriv t).deriv)
  apply strictConvexOn_univ_of_deriv2_pos
  · exact continuous_iff_continuousAt.mpr (fun t => (psi_deriv t).continuousAt)
  · intro t
    simpa [Function.iterate_succ_apply', hfirst, hsecond] using curvature_pos t

/-- A single input family witnesses full-hull strict success and projected-line
weak failure at the very same small positive scales. -/
theorem full_success_with_projected_failure :
    ∃ delta > 0, ∀ eps : ℝ, 0 < eps → eps < delta →
      candidate (1/4) (1/2) (1/2) 1 0 0 0 eps ∈ hull ∧
      (∀ i : Fin 4,
        scoreG (truth i) (candidate (1/4) (1/2) (1/2) 1 0 0 0 eps) <
          scoreG (truth i) (baseline (1/4) (1/2) (1/2) 1 0 0 0 eps) ∧
        scoreF (truth i) (candidate (1/4) (1/2) (1/2) 1 0 0 0 eps) <
          scoreF (truth i) (baseline (1/4) (1/2) (1/2) 1 0 0 0 eps)) ∧
      ¬ ∃ q ∈ Icc (0:ℝ) 1,
        q^2 ≤ IsolatedObstruction.baseA eps ∧
        IsolatedObstruction.endpointLoss q ≤ IsolatedObstruction.nonlinearBaseline eps := by
  obtain ⟨delta, hd, hh⟩ := universal_strict_repair
    (1/4) (1/2) (1/2) 1 0 0 0 (by norm_num) (by norm_num)
      (by norm_num) (by norm_num) (by norm_num)
  refine ⟨min delta (1/100), lt_min hd (by norm_num), ?_⟩
  intro eps he hsmall
  have hp := hh eps he (lt_of_lt_of_le hsmall (min_le_left _ _))
  exact ⟨hp.2.1,hp.2.2,
    IsolatedObstruction.no_isolated_common_repair eps he
      (le_of_lt (lt_of_lt_of_le hsmall (min_le_right _ _)))⟩

#print axioms full_success_with_projected_failure
#print axioms transverse_baseline_outside
#print axioms tangent_not_strict
#print axioms natural_truth_binding
#print axioms psi_strictConvex
end PolynomialANDAudit
