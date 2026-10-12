import FiniteHullSmoothRigidity
import GeometryControls
open Set Filter
open scoped Topology BigOperators
noncomputable section
namespace HullAudit
open SmoothRigidity GeometryAudit FiniteHullSmoothRigidity

def truths (j : Bool) (i : Fin 3) : ℝ :=
  if i=2 then 1/2 else if i=0 then (if j then 1 else 0) else (if j then 0 else 1)
def center : Fin 3 → ℝ := fun _ => 1/2

lemma center_interior : ∀ i, center i ∈ Ioo 0 1 := by intro i; norm_num [center]
lemma positive_barycenter : ∑ j : Bool, (1/2:ℝ) • truths j = center := by
  ext i; fin_cases i <;> norm_num [Fintype.sum_bool,truths,center] <;> norm_num [Fin.ext_iff]

lemma center_mem_hull : center ∈ convexHull ℝ (Set.range truths) :=
  mem_convexHull_of_exists_fintype (fun _ : Bool => (1/2:ℝ)) truths
    (fun _ => by norm_num) (by norm_num [Fintype.sum_bool])
    (fun j => Set.mem_range_self j) positive_barycenter

lemma center_not_categorical_simplex : center ∉ stdSimplex ℝ (Fin 3) := by
  intro h
  have hh := h.2
  norm_num [center,Fin.sum_univ_three] at hh

lemma hull_affine_constraints (x : Fin 3 → ℝ) (hx : x ∈ convexHull ℝ (Set.range truths)) :
    x 0+x 1=1 ∧ x 2=1/2 := by
  have hv : Set.range truths ⊆ {x : Fin 3 → ℝ | x 0+x 1=1 ∧ x 2=1/2} := by
    rintro x ⟨j,rfl⟩
    cases j <;> norm_num [truths] <;> norm_num [Fin.ext_iff]
  have hc : Convex ℝ {x : Fin 3 → ℝ | x 0+x 1=1 ∧ x 2=1/2} := by
    intro x hx y hy a b ha hb hab
    constructor <;> dsimp at * <;> nlinarith [hx.1,hx.2,hy.1,hy.2]
  exact convexHull_min hv hc hx

def weights (i : Fin 3) : ℝ := if i=2 then 2 else 1
lemma weights_positive (i : Fin 3) : 0 < weights i := by unfold weights; split_ifs <;> norm_num
noncomputable def weighted (i : Fin 3) := quadratic (weights i) (weights_positive i)

lemma weights_not_global_affine : ¬ BregmanProjection.PositiveAffineEquivalent weighted unitFamily := by
  rintro ⟨a,ha,b,d,h⟩
  have h00 := h 0 0 (by norm_num)
  have h01 := h 0 1 (by norm_num)
  have h0m := h 0 (1/2) (by norm_num)
  have h20 := h 2 0 (by norm_num)
  have h21 := h 2 1 (by norm_num)
  have h2m := h 2 (1/2) (by norm_num)
  norm_num [weighted,unitFamily,quadratic,weights] at h00 h01 h0m h20 h21 h2m
  norm_num [Fin.ext_iff] at h00 h01 h0m h20 h21 h2m
  nlinarith

lemma different_metrics_share_all_tangent_projections (h : Fin 3 → ℝ) :
    ∃ z ∈ Submodule.span ℝ (Set.range (fun j => center-truths j)),
      (∀ u ∈ Submodule.span ℝ (Set.range (fun j => center-truths j)),
        hessian unitFamily center (h-z) u=0) ∧
      (∀ u ∈ Submodule.span ℝ (Set.range (fun j => center-truths j)),
        hessian weighted center (h-z) u=0) := by
  let z := (h 0-h 1) • (center-truths false)
  have hz : z ∈ Submodule.span ℝ (Set.range (fun j => center-truths j)) :=
    Submodule.smul_mem _ _ (Submodule.subset_span (Set.mem_range_self false))
  refine ⟨z,hz,?_,?_⟩
  · intro u hu
    rw [hessian_symmetric]
    apply LocalRigidity.orthogonal_span (hessian unitFamily center) truths center (h-z) ?_ u hu
    intro j; cases j <;>
      norm_num [hessian_apply,Fin.sum_univ_three,z,unitFamily,quadratic,center,truths] <;>
      norm_num [Fin.ext_iff] <;> ring
  · intro u hu
    rw [hessian_symmetric]
    apply LocalRigidity.orthogonal_span (hessian weighted center) truths center (h-z) ?_ u hu
    intro j; cases j <;>
      norm_num [hessian_apply,Fin.sum_univ_three,z,weighted,weights,quadratic,center,truths] <;>
      norm_num [Fin.ext_iff] <;> ring

lemma duplicate_truth_rows_do_not_change_tangent {ι J : Type*} [Nonempty J]
    (v : J → (ι → ℝ)) (p : ι → ℝ) :
    Submodule.span ℝ (Set.range (fun j : J × Bool => p-v j.1)) =
      Submodule.span ℝ (Set.range (fun j => p-v j)) := by
  congr 1
  ext x
  constructor
  · rintro ⟨j,rfl⟩; exact ⟨j.1,rfl⟩
  · rintro ⟨j,rfl⟩; exact ⟨(j,false),rfl⟩

lemma singleton_truth_tangent_trivial {ι : Type*} (p : ι → ℝ) :
    Submodule.span ℝ (Set.range (fun _ : Unit => p-p)) = ⊥ := by simp

-- Literal general-hull statement: truth indices J and coordinates ι are separate.
example {ι J K : Type*} [Fintype ι] [DecidableEq ι] [Fintype J]
    (s : K → ι → SmoothScalar.Score) (k0 : K)
    (v : J → Vec ι) (w : J → ℝ) (p h : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1) (hw : ∀ j, 0 < w j)
    (hsum : ∑ j, w j=1) (hcenter : ∑ j, w j • v j=p)
    (e eta : ℕ → ℝ) (c : ℕ → Vec ι)
    (hepos : ∀ n, 0<e n) (he : Tendsto e atTop (𝓝 0))
    (heta0 : ∀ n, 0≤eta n) (heta : Tendsto (fun n => eta n/e n) atTop (𝓝 0))
    (hc : ∀ n i, c n i ∈ Ioo 0 1)
    (hcmem : ∀ n, c n ∈ convexHull ℝ (Set.range v))
    (hgain : ∀ n k j, totalDiv (s k) (v j) (c n) ≤ totalDiv (s k) (v j) (p+e n • h)+eta n) :
    ∃ z ∈ Submodule.span ℝ (Set.range (fun j => p-v j)),
      ∀ k u, u ∈ Submodule.span ℝ (Set.range (fun j => p-v j)) →
        hessian (s k) p (h-z) u=0 :=
  finite_hull_approximate_hessian_necessary s k0 v w p h hp hw hsum hcenter e eta c hepos he heta0 heta hc hcmem hgain
end HullAudit
