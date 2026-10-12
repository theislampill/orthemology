import IntrinsicBarycentric
open Set Filter
open scoped Topology BigOperators
noncomputable section
namespace HullInterfaceAudit
open IntrinsicBarycentric SmoothRigidity

def endpointTruth (b : Bool) : ℝ := if b then 1 else 0

lemma boundary_has_no_strictly_positive_certificate :
    ¬ ∃ w : Bool → ℝ, (∀ b, 0<w b) ∧ (∑ b, w b=1) ∧
      (∑ b, w b • endpointTruth b=(0:ℝ)) := by
  rintro ⟨w,hw,hs,hc⟩
  have ht := hw true
  norm_num [Fintype.sum_bool,endpointTruth,smul_eq_mul] at hc
  linarith

lemma boundary_not_intrinsic_interior :
    (0:ℝ) ∉ intrinsicInterior ℝ (convexHull ℝ (Set.range endpointTruth)) := by
  intro h
  exact boundary_has_no_strictly_positive_certificate
    (intrinsicInterior_positive_barycentric endpointTruth 0 h)

lemma singleton_intrinsic_does_not_imply_cube_interior :
    (0:ℝ) ∈ intrinsicInterior ℝ ({0} : Set ℝ) ∧ (0:ℝ) ∉ Ioo 0 1 := by
  simp [intrinsicInterior_singleton]

lemma empty_hull_has_no_intrinsic_point :
    intrinsicInterior ℝ (convexHull ℝ (∅ : Set ℝ)) = ∅ := by simp

lemma all_duplicate_truths_admit_positive_weights
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] (p : E) :
    ∃ w : Bool → ℝ, (∀ b, 0<w b) ∧ (∑ b, w b=1) ∧ (∑ b, w b • p=p) := by
  apply intrinsicInterior_positive_barycentric (fun _ : Bool => p) p
  simp [intrinsicInterior_singleton]

lemma duplicated_midpoint_certificate :
    ∃ w : Fin 3 → ℝ, (∀ i, 0<w i) ∧ (∑ i, w i=1) ∧
      (∑ i, w i * (if i=2 then (1:ℝ) else 0)=1/2) := by
  refine ⟨(fun i => if i=2 then 1/2 else 1/4),?_,?_,?_⟩
  · intro i; dsimp; split_ifs <;> norm_num
  · norm_num [Fin.sum_univ_three] <;> norm_num [Fin.ext_iff]
  · norm_num [Fin.sum_univ_three] <;> norm_num [Fin.ext_iff]

-- Pointwise vanishing over an infinite family cannot be replaced by uniform vanishing.
def spikeRatio (k n : ℕ) : ℝ := if n=k then 1 else 0
lemma every_fixed_ratio_eventually_zero (k : ℕ) :
    ∀ᶠ n : ℕ in atTop, spikeRatio k n=0 := by
  apply eventually_atTop.mpr
  refine ⟨k+1,?_⟩
  intro n hn
  have hne : n≠k := by omega
  simp [spikeRatio,hne]

lemma diagonal_ratio_always_one (n : ℕ) : spikeRatio n n=1 := by simp [spikeRatio]

lemma no_uniform_eventual_small_ratio :
    ¬ (∀ᶠ n : ℕ in atTop, ∀ k, |spikeRatio k n|<1/2) := by
  intro h
  obtain ⟨n,hn⟩ := h.exists
  have hh := hn n
  norm_num [spikeRatio] at hh

-- A common normal direction supplies a constructed sublinear tolerance.
-- This checks the literal finite-family iff, including both independent interior premises.
example {ι J K : Type*} [Fintype ι] [DecidableEq ι] [Fintype J] [Fintype K]
    (s : K → ι → SmoothScalar.Score) (k0 : K) (v : J → Vec ι) (p h : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1)
    (hri : p ∈ intrinsicInterior ℝ (convexHull ℝ (Set.range v))) :
    (∃ (e eta : ℕ → ℝ) (c : ℕ → Vec ι),
      (∀ n, 0<e n) ∧ Tendsto e atTop (𝓝 0) ∧
      (∀ n, 0≤eta n) ∧ Tendsto (fun n => eta n/e n) atTop (𝓝 0) ∧
      (∀ n i, c n i ∈ Ioo 0 1) ∧
      (∀ n, c n ∈ convexHull ℝ (Set.range v)) ∧
      (∀ n k j, totalDiv (s k) (v j) (c n) ≤ totalDiv (s k) (v j) (p+e n • h)+eta n)) ↔
    (∃ z ∈ Submodule.span ℝ (Set.range (fun j => p-v j)),
      ∀ k u, u ∈ Submodule.span ℝ (Set.range (fun j => p-v j)) →
        hessian (s k) p (h-z) u=0) :=
  smooth_finite_hull_approximate_iff_intrinsicInterior s k0 v p h hp hri
end HullInterfaceAudit
