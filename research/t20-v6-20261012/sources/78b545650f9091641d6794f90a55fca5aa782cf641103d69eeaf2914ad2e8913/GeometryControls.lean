import BregmanProjection
open Set Filter
open scoped Topology BigOperators
namespace GeometryAudit
open SmoothRigidity BregmanProjection

noncomputable def quadratic (w : ℝ) (hw : 0 < w) : SmoothScalar.Score where
  f := fun x => w*x^2
  df := fun x => 2*w*x
  ddf := fun _ => 2*w
  cont := (continuous_const.mul (continuous_id.pow 2)).continuousOn
  deriv := by
    intro x hx
    convert ((hasDerivAt_id x).pow 2).const_mul w using 1 <;> simp only [id_eq] <;> ring
  second := by
    intro x hx
    simpa using (hasDerivAt_id x).const_mul (2*w)
  cont_second := continuous_const.continuousOn
  positive := by intro x hx; positivity

lemma quadratic_divergence (w : ℝ) (hw : 0 < w) (v b : ℝ) :
    SmoothScalar.divergence (quadratic w hw) v b = w*(v-b)^2 := by
  dsimp [SmoothScalar.divergence,quadratic]
  ring

lemma positive_affine_reflexive {ι : Type*} (s : ι → SmoothScalar.Score) :
    PositiveAffineEquivalent s s := by
  refine ⟨1, by norm_num, fun _ => 0, fun _ => 0, ?_⟩
  intros; simp

def weights (i : Fin 3) : ℝ := if i=0 then 1 else 2
lemma weights_positive (i : Fin 3) : 0 < weights i := by
  unfold weights; split_ifs <;> norm_num
noncomputable def unequalFamily (i : Fin 3) := quadratic (weights i) (weights_positive i)
noncomputable def unitFamily (_ : Fin 3) := quadratic 1 (by norm_num)

theorem coordinate_scales_not_global_affine :
    ¬ PositiveAffineEquivalent unequalFamily unitFamily := by
  rintro ⟨a,ha,b,d,h⟩
  have h00 := h 0 0 (by norm_num)
  have h01 := h 0 1 (by norm_num)
  have h0m := h 0 (1/2) (by norm_num)
  have h10 := h 1 0 (by norm_num)
  have h11 := h 1 1 (by norm_num)
  have h1m := h 1 (1/2) (by norm_num)
  norm_num [unequalFamily,unitFamily,quadratic,weights] at h00 h01 h0m h10 h11 h1m
  nlinarith

theorem nonaffine_pair_has_no_universal_common_repairs (i0 : Fin 3) :
    ¬ CommonLocalRepairs unequalFamily unitFamily i0 := by
  intro h
  exact coordinate_scales_not_global_affine
    ((universal_common_repair_iff_affine (by norm_num) unequalFamily unitFamily i0).mp h)

-- Every score can separately repair the same direction; sharing the witness is substantive.
theorem separate_repairs_exist (p : Fin 3 → ℝ)
    (hp : ∀ i, p i ∈ Ioo 0 1) (hsum : ∑ i, p i = 1) (i0 : Fin 3) :
    (∃ (e : ℕ → ℝ) (c : ℕ → Vec (Fin 3)), (∀ n, 0 < e n) ∧ Tendsto e atTop (𝓝 0) ∧
      (∀ n i, c n i ∈ Ioo 0 1) ∧ (∀ n, ∑ i, c n i = 1) ∧
      (∀ n i, totalDiv unequalFamily (vertex i) (c n) ≤
        totalDiv unequalFamily (vertex i) (p + e n • vertex i0))) ∧
    (∃ (e : ℕ → ℝ) (c : ℕ → Vec (Fin 3)), (∀ n, 0 < e n) ∧ Tendsto e atTop (𝓝 0) ∧
      (∀ n i, c n i ∈ Ioo 0 1) ∧ (∀ n, ∑ i, c n i = 1) ∧
      (∀ n i, totalDiv unitFamily (vertex i) (c n) ≤
        totalDiv unitFamily (vertex i) (p + e n • vertex i0))) := by
  obtain ⟨e,c,he,ht,hb,hc,hs,hg⟩ := single_score_local_repairs unequalFamily p (vertex i0) hp hsum
  obtain ⟨f,d,hf,hu,hb',hd,hd',hj⟩ := single_score_local_repairs unitFamily p (vertex i0) hp hsum
  exact ⟨⟨e,c,he,ht,hc,hs,hg⟩,⟨f,d,hf,hu,hd,hd',hj⟩⟩

theorem zero_direction_vacuous {ι : Type*} [Fintype ι] [DecidableEq ι]
    (s t : ι → SmoothScalar.Score) (p : Vec ι) (e : ℝ) :
    (∀ i, totalDiv s (vertex i) p ≤ totalDiv s (vertex i) (p + e • (0 : Vec ι))) ∧
    (∀ i, totalDiv t (vertex i) p ≤ totalDiv t (vertex i) (p + e • (0 : Vec ι))) := by simp

-- Two outcomes allow nonconstant Hessian-ratio functions compatible everywhere.
def binaryRatio (b : Bool) (x : ℝ) : ℝ := if b then 2-x else 1+x
lemma binary_ratio_compatible (p : Bool → ℝ) (hp : p false + p true = 1) :
    binaryRatio false (p false) = binaryRatio true (p true) := by
  simp [binaryRatio]; linarith
lemma binary_ratio_not_constant :
    ¬ ∃ a : ℝ, ∀ b x, x ∈ Ioo 0 1 → binaryRatio b x = a := by
  rintro ⟨a,h⟩
  have h1 := h false (1/4) (by constructor <;> norm_num)
  have h2 := h false (1/2) (by constructor <;> norm_num)
  norm_num [binaryRatio] at h1 h2
  linarith

lemma affine_generator_zero_divergence (v b : ℝ) : v-b-1*(v-b)=0 := by ring

lemma forecast_orientation_matters :
    (1:ℝ)^3-(1/2)^3-3*(1/2)^2*(1-1/2) = 1/2 ∧
    (1/2:ℝ)^3-1^3-3*1^2*(1/2-1) = 5/8 := by norm_num

-- Explicit full main signature; every-p, same sequence and one positive global scale.
example {ι : Type*} [Fintype ι] [DecidableEq ι]
    (hcard : 3 ≤ Fintype.card ι) (s t : ι → SmoothScalar.Score) (i0 : ι) :
    (∀ p : Vec ι, (∀ i, p i ∈ Ioo 0 1) → (∑ i, p i = 1) →
      ∃ (e : ℕ → ℝ) (c : ℕ → Vec ι),
        (∀ n, 0 < e n) ∧ Tendsto e atTop (𝓝 0) ∧
        (∀ n i, c n i ∈ Ioo 0 1) ∧ (∀ n, ∑ i, c n i = 1) ∧
        (∀ n i, totalDiv s (vertex i) (c n) ≤ totalDiv s (vertex i) (p + e n • vertex i0)) ∧
        (∀ n i, totalDiv t (vertex i) (c n) ≤ totalDiv t (vertex i) (p + e n • vertex i0))) ↔
    (∃ a > 0, ∃ b d : ι → ℝ, ∀ i x, x ∈ Icc 0 1 →
      (s i).f x = a * (t i).f x + b i*x + d i) :=
  universal_common_repair_iff_affine hcard s t i0

end GeometryAudit
