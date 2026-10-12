import SmoothRobustness
import GeometryControls
open Set Filter
open scoped Topology BigOperators
namespace RobustnessAudit
open SmoothRigidity BregmanProjection SmoothRobustness GeometryAudit

theorem approximate_iff_exact {ι : Type*} [Fintype ι] [DecidableEq ι]
    (hcard : 3 ≤ Fintype.card ι) (s t : ι → SmoothScalar.Score) (i0 : ι) :
    ApproximateCommonLocalRepairs s t i0 ↔ CommonLocalRepairs s t i0 :=
  (universal_approximate_common_repair_iff_affine hcard s t i0).trans
    (universal_common_repair_iff_affine hcard s t i0).symm

theorem unequal_scales_still_excluded (i0 : Fin 3) :
    ¬ ApproximateCommonLocalRepairs unequalFamily unitFamily i0 := by
  intro h
  exact coordinate_scales_not_global_affine
    ((universal_approximate_common_repair_iff_affine (by norm_num) unequalFamily unitFamily i0).mp h)

-- Linear tolerance allows the unchanged p to serve both non-equivalent scores.
theorem linear_tolerance_keeps_original_p (p : Fin 3 → ℝ)
    (hp : ∀ i, p i ∈ Ioo 0 1) (e : ℝ) (he : 0 ≤ e) :
    (∀ i, totalDiv unequalFamily (vertex i) p ≤
      totalDiv unequalFamily (vertex i) (p + e • vertex 0) + 2*e) ∧
    (∀ i, totalDiv unitFamily (vertex i) p ≤
      totalDiv unitFamily (vertex i) (p + e • vertex 0) + 2*e) := by
  have h0 := (hp 0).1
  have he0 := mul_nonneg he h0.le
  have he2 := sq_nonneg e
  constructor <;> intro i <;> fin_cases i <;>
    simp [totalDiv_eq_sum, Fin.sum_univ_succ, SmoothScalar.divergence,
      unequalFamily,unitFamily,quadratic,weights,vertex,Pi.single_apply] <;> nlinarith

theorem linear_tolerance_ratio (e : ℝ) (he : 0 < e) : (2*e)/e=2 := by
  field_simp

theorem square_root_bound_does_not_give_linear_bound (x : ℝ) (hx : 0 < x) :
    (1/x^3)^2 = (1/x^6) ∧
    (1/x^6)/(1/x^4) = 1/x^2 ∧
    (1/x^3)/(1/x^4) = x := by
  have hne : x ≠ 0 := ne_of_gt hx
  constructor
  · field_simp; ring
  constructor <;> field_simp <;> ring

-- All-state derivative information is essential: one vertex alone is not coercive.
theorem one_vertex_derivative_can_vanish :
    ∃ x : Fin 3 → ℝ, x ≠ 0 ∧ (∑ i, x i)=0 ∧
      (∑ i, ((1/3:ℝ)-(vertex (0:Fin 3)) i)*x i)=0 := by
  refine ⟨![0,1,-1], ?_, ?_, ?_⟩
  · intro h
    have hh := congrFun h 1
    norm_num at hh
  · norm_num [Fin.sum_univ_succ]
  · norm_num [Fin.sum_univ_succ,vertex,Pi.single_apply]

-- In a noncoherent radial direction all three vertex losses change only quadratically.
-- Combined with the preceding power family this invalidates linear normalization
-- if exact sum-one coherence is replaced by subprobability.
theorem radial_noncoherent_quadratic (d : ℝ) :
    ((1/3-d)-1)^2+2*(1/3-d)^2 - (((1/3:ℝ)-1)^2+2*(1/3:ℝ)^2) = 3*d^2 ∧
    3*(1/3-d)=1-3*d := by constructor <;> ring

theorem boundary_barycenter_not_coercive :
    ¬ ∃ a > (0:ℝ), ∀ x : ℝ, a*|x| ≤ max (0*x) 0 + max ((-1)*x) 0 := by
  rintro ⟨a,ha,h⟩
  have hh := h 1
  norm_num at hh
  linarith

-- The actual theorem has eta/e -> 0 and derives bounded normalization.
example {ι : Type*} [Fintype ι] [DecidableEq ι]
    (s : ι → SmoothScalar.Score) (p h : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1) (hsum : ∑ i, p i = 1)
    (e eta : ℕ → ℝ) (c : ℕ → Vec ι)
    (hepos : ∀ n, 0 < e n) (he : Tendsto e atTop (𝓝 0))
    (heta0 : ∀ n, 0 ≤ eta n)
    (heta : Tendsto (fun n => eta n/e n) atTop (𝓝 0))
    (hc : ∀ n i, c n i ∈ Ioo 0 1) (hcsum : ∀ n, ∑ i, c n i = 1)
    (hgain : ∀ n i, totalDiv s (vertex i) (c n) ≤
      totalDiv s (vertex i) (p + e n • h) + eta n) :
    ∃ R : ℝ, ∀ᶠ n in atTop, ‖(e n)⁻¹ • (c n-p)‖ ≤ R :=
  normalized_approximate_repairs_bounded s p h hp hsum e eta c hepos he heta0 heta hc hcsum hgain
end RobustnessAudit
