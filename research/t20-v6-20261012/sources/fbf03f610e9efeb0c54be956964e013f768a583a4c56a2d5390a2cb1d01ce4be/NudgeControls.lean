import CoherentNudgeRigidity
import GeometryControls
open Set Filter
open scoped Topology BigOperators
noncomputable section
namespace NudgeAudit
open SmoothRigidity GeometryAudit NudgeRigidity BregmanProjection

def input : Fin 3 → ℝ := fun i => if i=0 then 1/2 else 7/20
def direction : Fin 3 → ℝ := fun i => if i=0 then -13/10 else -1

lemma input_interior : ∀ i, input i ∈ Ioo 0 1 := by
  intro i; fin_cases i <;> norm_num [input]

lemma pointwise_strict_common_nudge :
    (∀ i, hessian unitFamily input (input-vertex i) direction < 0) ∧
    (∀ i, hessian unequalFamily input (input-vertex i) direction < 0) := by
  constructor <;> intro i <;> fin_cases i <;>
    norm_num [hessian_apply, Fin.sum_univ_three, input,direction,vertex,
      unitFamily,unequalFamily,quadratic,weights,Pi.single_apply] <;> norm_num [Fin.ext_iff]

lemma no_pointwise_common_coherent_endpoint (c : Fin 3 → ℝ)
    (hsum : ∑ i, c i = 1)
    (hunit : ∀ i, totalDiv unitFamily (vertex i) c ≤ totalDiv unitFamily (vertex i) input)
    (hweighted : ∀ i, totalDiv unequalFamily (vertex i) c ≤ totalDiv unequalFamily (vertex i) input) :
    False := by
  have h0 := hunit 0
  have h1 := hweighted 1
  have h2 := hweighted 2
  norm_num [totalDiv_eq_sum, Fin.sum_univ_three, SmoothScalar.divergence,
    input,vertex,unitFamily,unequalFamily,quadratic,weights,Pi.single_apply] at h0 h1 h2
  norm_num [Fin.ext_iff] at h0 h1 h2
  norm_num [Fin.sum_univ_three] at hsum
  have hd := sq_nonneg (c 1-c 2)
  have hb1 : (1-c 0)^2 ≤ (33:ℝ)/100 := by nlinarith
  have hb2 : (c 0)^2 ≤ (17:ℝ)/100 := by nlinarith
  have ht : 5/12 < c 0 := by
    apply lt_of_not_ge
    intro hle
    nlinarith [sq_nonneg (c 0-5/12)]
  nlinarith [sq_nonneg (c 0-5/12)]

def coherentTarget : Fin 3 → ℝ := fun i => if i=0 then 139/330 else 191/660

lemma pointwise_coherent_directed_nudge :
    (∀ i, coherentTarget i ∈ Ioo 0 1) ∧ (∑ i, coherentTarget i)=1 ∧
    (∀ i, hessian unitFamily input (input-vertex i) (coherentTarget-input) < 0) ∧
    (∀ i, hessian unequalFamily input (input-vertex i) (coherentTarget-input) < 0) := by
  have hdir : coherentTarget-input = (2/33:ℝ) • direction := by
    ext i; fin_cases i <;> norm_num [coherentTarget,input,direction]
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro i; fin_cases i <;> norm_num [coherentTarget]
  · norm_num [coherentTarget,Fin.sum_univ_three] <;> norm_num [Fin.ext_iff]
  · intro i
    rw [hdir,map_smul,smul_eq_mul]
    exact mul_neg_of_pos_of_neg (by norm_num) (pointwise_strict_common_nudge.1 i)
  · intro i
    rw [hdir,map_smul,smul_eq_mul]
    exact mul_neg_of_pos_of_neg (by norm_num) (pointwise_strict_common_nudge.2 i)

lemma no_universal_common_nudge (i0 : Fin 3) :
    ¬ CommonLocalNudges unequalFamily unitFamily i0 := by
  intro h
  exact coordinate_scales_not_global_affine
    ((universal_local_nudge_iff_affine (by norm_num) unequalFamily unitFamily i0).mp h)

lemma weak_zero_direction_is_vacuous {ι : Type*} [Fintype ι] [DecidableEq ι]
    (s t : ι → SmoothScalar.Score) (b : Vec ι) :
    (∀ i, hessian s b (b-vertex i) 0 ≤ 0) ∧
    (∀ i, hessian t b (b-vertex i) 0 ≤ 0) := by simp

lemma canonical_nudge_vanishes_on_coherent_input {ι : Type*} [Fintype ι] [DecidableEq ι]
    (s : ι → SmoothScalar.Score) (b : Vec ι) (hsum : ∑ i, b i=1) :
    (fun i => (1-∑ k, b k)/(s i).ddf (b i)) = 0 := by funext i; simp [hsum]

lemma distinct_planes_share_nonzero_vector :
    let u : Fin 3 → ℝ := ![0,0,1]
    u ≠ 0 ∧ u 1=0 ∧ u 0=0 ∧
      ({x : Fin 3 → ℝ | x 1=0} : Set (Fin 3 → ℝ)) ≠ {x | x 0=0} := by
  dsimp
  refine ⟨?_, by norm_num, by norm_num, ?_⟩
  · intro h
    have hh := congrFun h 2
    change (1:ℝ)=0 at hh
    norm_num at hh
  · intro h
    have hm : (![1,0,0] : Fin 3 → ℝ) ∈ {x : Fin 3 → ℝ | x 1=0} := by norm_num
    rw [h] at hm
    norm_num at hm

-- Exact universal theorem, with all-context quantification retained in the definitions.
example {ι : Type*} [Fintype ι] [DecidableEq ι]
    (hcard : 3 ≤ Fintype.card ι) (s t : ι → SmoothScalar.Score) (i0 : ι) :
    CommonLocalNudges s t i0 ↔ CommonLocalRepairs s t i0 :=
  universal_local_nudge_iff_common_repair hcard s t i0

example {ι : Type*} [Fintype ι] [DecidableEq ι]
    (hcard : 3 ≤ Fintype.card ι) (s t : ι → SmoothScalar.Score) (i0 : ι) :
    CoherentNudgeRigidity.CommonCoherentLocalNudges s t i0 ↔ CommonLocalRepairs s t i0 :=
  CoherentNudgeRigidity.universal_coherent_nudge_iff_common_repair hcard s t i0

end NudgeAudit
