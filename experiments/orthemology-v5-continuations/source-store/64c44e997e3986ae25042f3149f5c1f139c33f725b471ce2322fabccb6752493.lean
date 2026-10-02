import LocalRigidity
import SmoothScalar

noncomputable section
open scoped Topology BigOperators
open Filter Set Asymptotics

namespace SmoothRigidity

variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]

/-- First-order expansion along a convergent varying direction, rather than
only a fixed directional ray. -/
lemma varying_direction_limit (f : E → ℝ) (L : E →L[ℝ] ℝ) (p z : E)
    (hf : HasFDerivAt f L p) (e : ℕ → ℝ) (r : ℕ → E)
    (hepos : ∀ n, 0 < e n) (he : Tendsto e atTop (𝓝 0))
    (hr : Tendsto r atTop (𝓝 z)) :
    Tendsto (fun n => (f (p + e n • r n) - f p) / e n) atTop (𝓝 (L z)) := by
  have hpert : Tendsto (fun n => e n • r n) atTop (𝓝 (0 : E)) := by
    simpa using he.smul hr
  have hrem := (hasFDerivAt_iff_isLittleO_nhds_zero.mp hf).comp_tendsto hpert
  have hscale : (fun n => e n • r n) =O[atTop] e := by
    simpa using (isBigO_refl e atTop).smul (hr.isBigO_one ℝ)
  have hsmall := hrem.trans_isBigO hscale
  have hremdiv := hsmall.tendsto_div_nhds_zero
  have hlinear : Tendsto (fun n => L (r n)) atTop (𝓝 (L z)) := L.continuous.tendsto z |>.comp hr
  have hsum := hremdiv.add hlinear
  have hid : ∀ n, (f (p + e n • r n) - f p) / e n =
      (f (p + e n • r n) - f p - L (e n • r n)) / e n + L (r n) := by
    intro n
    rw [map_smul]
    simp only [smul_eq_mul]
    field_simp [ne_of_gt (hepos n)]
    ring
  simpa only [Function.comp_apply, ← hid, zero_add] using hsum

lemma smooth_first_order_nonnegative (f : E → ℝ) (L : E →L[ℝ] ℝ) (p h z : E)
    (hf : HasFDerivAt f L p) (e : ℕ → ℝ) (r : ℕ → E)
    (hepos : ∀ n, 0 < e n) (he : Tendsto e atTop (𝓝 0))
    (hr : Tendsto r atTop (𝓝 z))
    (hgain : ∀ n, f (p + e n • r n) ≤ f (p + e n • h)) :
    0 ≤ L (h - z) := by
  have hbase := varying_direction_limit f L p h hf e (fun _ => h) hepos he tendsto_const_nhds
  have hrepair := varying_direction_limit f L p z hf e r hepos he hr
  have hlim := hbase.sub hrepair
  have hnonneg : ∀ᶠ n in atTop,
      0 ≤ (f (p + e n • h) - f p) / e n -
        (f (p + e n • r n) - f p) / e n := by
    apply Filter.Eventually.of_forall
    intro n
    exact sub_nonneg.mpr ((div_le_div_iff_of_pos_right (hepos n)).mpr (by linarith [hgain n]))
  have h := ge_of_tendsto hlim hnonneg
  simpa only [map_sub] using h



def bregman (F : E → ℝ) (G : E → E →L[ℝ] ℝ) (v b : E) : ℝ :=
  F v - F b - G b (v - b)

lemma bregman_gain (F : E → ℝ) (G : E → E →L[ℝ] ℝ) (p v b c : E) :
    bregman F G v b - bregman F G v c =
      bregman F G p b - bregman F G p c + (G c - G b) (v - p) := by
  simp only [bregman, map_sub, ContinuousLinearMap.sub_apply]
  ring

lemma weighted_bregman_gain {ι : Type*} [Fintype ι]
    (F : E → ℝ) (G : E → E →L[ℝ] ℝ)
    (v : ι → E) (w : ι → ℝ) (p b c : E)
    (hsum : ∑ i, w i = 1) (hcenter : ∑ i, w i • v i = p) :
    (∑ i, w i * (bregman F G (v i) b - bregman F G (v i) c)) =
      bregman F G p b - bregman F G p c := by
  have hvzero := LocalRigidity.barycenter_sub_sum v w p hsum hcenter
  have hlin : (∑ i, w i * (G c - G b) (v i - p)) = 0 := by
    have hzero : ∑ i, w i • (v i - p) = 0 := by
      have heq : (∑ i, w i • (v i - p)) = -(∑ i, w i • (p - v i)) := by
        simp only [← Finset.sum_neg_distrib, ← smul_neg, neg_sub]
      rw [heq, hvzero, neg_zero]
    have happly : (G c - G b) (∑ i, w i • (v i - p)) = 0 := by rw [hzero]; simp
    simpa only [map_sum, map_smul, smul_eq_mul] using happly
  rw [show (∑ i, w i * (bregman F G (v i) b - bregman F G (v i) c)) =
      ∑ i, w i * (bregman F G p b - bregman F G p c + (G c - G b) (v i - p)) by
    apply Finset.sum_congr rfl
    intro i _
    rw [bregman_gain F G p]]
  simp only [mul_add, Finset.sum_add_distrib, ← Finset.sum_mul]
  rw [hlin, hsum]
  ring

lemma bregman_regret_bound {ι : Type*} [Fintype ι]
    (F : E → ℝ) (G : E → E →L[ℝ] ℝ)
    (v : ι → E) (w : ι → ℝ) (p b c : E)
    (hw : ∀ i, 0 ≤ w i) (hsum : ∑ i, w i = 1) (hcenter : ∑ i, w i • v i = p)
    (hgain : ∀ i, bregman F G (v i) c ≤ bregman F G (v i) b) :
    bregman F G p c ≤ bregman F G p b := by
  have hnonneg : 0 ≤ ∑ i, w i * (bregman F G (v i) b - bregman F G (v i) c) := by
    exact Finset.sum_nonneg (fun i _ => mul_nonneg (hw i) (sub_nonneg.mpr (hgain i)))
  rw [weighted_bregman_gain F G v w p b c hsum hcenter] at hnonneg
  linarith

section FiniteScores
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

abbrev Vec (ι : Type*) := ι → ℝ

def potential (s : ι → SmoothScalar.Score) (x : Vec ι) : ℝ := ∑ i, (s i).f (x i)

def gradient (s : ι → SmoothScalar.Score) (x : Vec ι) : Vec ι →L[ℝ] ℝ :=
  ∑ i, (s i).df (x i) • (ContinuousLinearMap.proj i : Vec ι →L[ℝ] ℝ)

def hessian (s : ι → SmoothScalar.Score) (p : Vec ι) : LocalRigidity.Form (Vec ι) :=
  ∑ i, (ContinuousLinearMap.proj i : Vec ι →L[ℝ] ℝ).smulRight
    ((s i).ddf (p i) • (ContinuousLinearMap.proj i : Vec ι →L[ℝ] ℝ))

abbrev totalDiv (s : ι → SmoothScalar.Score) := bregman (potential s) (gradient s)

def vertex (i : ι) : Vec ι := Pi.single i 1

lemma hessian_apply (s : ι → SmoothScalar.Score) (p x y : Vec ι) :
    hessian s p x y = ∑ i, (s i).ddf (p i) * x i * y i := by
  simp only [hessian, ContinuousLinearMap.sum_apply, ContinuousLinearMap.smulRight_apply,
    ContinuousLinearMap.smul_apply, ContinuousLinearMap.proj_apply, smul_eq_mul]
  apply Finset.sum_congr rfl
  intro i _
  ring

lemma totalDiv_eq_sum (s : ι → SmoothScalar.Score) (v b : Vec ι) :
    totalDiv s v b = ∑ i, SmoothScalar.divergence (s i) (v i) (b i) := by
  simp only [totalDiv, bregman, potential, gradient, ContinuousLinearMap.sum_apply,
    ContinuousLinearMap.smul_apply, ContinuousLinearMap.proj_apply, Pi.sub_apply, smul_eq_mul,
    SmoothScalar.divergence, Finset.sum_sub_distrib]

lemma score_hasFDerivAt (s : ι → SmoothScalar.Score) (v p : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1) :
    HasFDerivAt (totalDiv s v) (hessian s p (p - v)) p := by
  have hj : ∀ i, HasFDerivAt (fun x : Vec ι => SmoothScalar.divergence (s i) (v i) (x i))
      (((s i).ddf (p i) * (p i - v i)) • (ContinuousLinearMap.proj i : Vec ι →L[ℝ] ℝ)) p := by
    intro i
    exact (SmoothScalar.divergence_deriv (s i) (v i) (p i) (hp i)).comp_hasFDerivAt p
      (ContinuousLinearMap.proj i : Vec ι →L[ℝ] ℝ).hasFDerivAt
  have hh := HasFDerivAt.sum (u := Finset.univ) (fun i _ => hj i)
  have heq : (∑ i, ((s i).ddf (p i) * (p i - v i)) •
      (ContinuousLinearMap.proj i : Vec ι →L[ℝ] ℝ)) = hessian s p (p - v) := by
    ext x
    simp only [ContinuousLinearMap.sum_apply, ContinuousLinearMap.smul_apply,
      ContinuousLinearMap.proj_apply, smul_eq_mul, hessian_apply, Pi.sub_apply]
  rw [heq] at hh
  simpa only [← totalDiv_eq_sum] using hh

lemma vertex_barycenter (p : Vec ι) : ∑ i, p i • vertex i = p := by
  ext j
  simp [vertex, Pi.single_apply]

lemma totalDiv_nonneg (s : ι → SmoothScalar.Score) (p c : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1) (hc : ∀ i, c i ∈ Ioo 0 1) : 0 ≤ totalDiv s p c := by
  rw [totalDiv_eq_sum]
  exact Finset.sum_nonneg (fun i _ => SmoothScalar.divergence_nonneg (s i) (p i) (c i) (hp i) (hc i))



lemma vertex_regret_bound (s : ι → SmoothScalar.Score) (p b c : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1) (hsum : ∑ i, p i = 1)
    (hgain : ∀ i, totalDiv s (vertex i) c ≤ totalDiv s (vertex i) b) :
    totalDiv s p c ≤ totalDiv s p b :=
  bregman_regret_bound (potential s) (gradient s) vertex p p b c
    (fun i => (hp i).1.le) hsum (vertex_barycenter p) hgain

lemma scalar_divergence_le_total (s : ι → SmoothScalar.Score) (p c : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1) (hc : ∀ i, c i ∈ Ioo 0 1) (i : ι) :
    SmoothScalar.divergence (s i) (p i) (c i) ≤ totalDiv s p c := by
  rw [totalDiv_eq_sum]
  exact Finset.single_le_sum
    (fun j _ => SmoothScalar.divergence_nonneg (s j) (p j) (c j) (hp j) (hc j)) (Finset.mem_univ i)

/-- Successful coherent repairs localize without any assumed bound on endpoint derivatives. -/
lemma repairs_tendsto (s : ι → SmoothScalar.Score) (p : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1) (hsum : ∑ i, p i = 1)
    (b c : ℕ → Vec ι) (hb : Tendsto b atTop (𝓝 p))
    (hc : ∀ n i, c n i ∈ Ioo 0 1)
    (hgain : ∀ n i, totalDiv s (vertex i) (c n) ≤ totalDiv s (vertex i) (b n)) :
    Tendsto c atTop (𝓝 p) := by
  have hregret : ∀ n, totalDiv s p (c n) ≤ totalDiv s p (b n) :=
    fun n => vertex_regret_bound s p (b n) (c n) hp hsum (hgain n)
  have hlim : Tendsto (fun n => totalDiv s p (b n)) atTop (𝓝 0) := by
    have h := (score_hasFDerivAt s p p hp).continuousAt.tendsto.comp hb
    simpa [totalDiv, bregman, Function.comp_def] using h
  apply tendsto_pi_nhds.mpr
  intro i
  apply SmoothScalar.tendsto_of_divergence_tendsto_zero (s i) (p i) (hp i) (fun n => c n i)
    (fun n => hc n i)
  exact squeeze_zero
    (fun n => SmoothScalar.divergence_nonneg (s i) (p i) (c n i) (hp i) (hc n i))
    (fun n => (scalar_divergence_le_total s p (c n) hp (hc n) i).trans (hregret n)) hlim

/-- Local lower and upper Hessian bounds prove bounded normalized repairs.
This estimate is derived from actual Bregman score inequalities. -/
lemma normalized_repairs_bounded (s : ι → SmoothScalar.Score) (p h : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1) (hsum : ∑ i, p i = 1)
    (e : ℕ → ℝ) (c : ℕ → Vec ι)
    (hepos : ∀ n, 0 < e n) (he : Tendsto e atTop (𝓝 0))
    (hc : ∀ n i, c n i ∈ Ioo 0 1)
    (hgain : ∀ n i, totalDiv s (vertex i) (c n) ≤ totalDiv s (vertex i) (p + e n • h)) :
    ∃ R : ℝ, ∀ᶠ n in atTop, ‖(e n)⁻¹ • (c n - p)‖ ≤ R := by
  let base : ℕ → Vec ι := fun n => p + e n • h
  have hbase : Tendsto base atTop (𝓝 p) := by
    simpa [base] using
      (tendsto_const_nhds : Tendsto (fun _ : ℕ => p) atTop (𝓝 p)).add
        (he.smul (tendsto_const_nhds : Tendsto (fun _ : ℕ => h) atTop (𝓝 h)))
  have hct := repairs_tendsto s p hp hsum base c hbase hc hgain
  choose a ha b hb hcurv using fun i => SmoothScalar.local_curvature_sandwich (s i) (p i) (hp i)
  let K : ℝ := ∑ i, b i * (h i) ^ 2
  have hK : 0 ≤ K := Finset.sum_nonneg (fun i _ => mul_nonneg (hb i).le (sq_nonneg (h i)))
  let R : ℝ := ∑ i, (K / a i + 1)
  have hterm : ∀ i, 0 ≤ K / a i + 1 := by
    intro i
    exact add_nonneg (div_nonneg hK (ha i).le) (by norm_num)
  have hR : 0 ≤ R := Finset.sum_nonneg (fun i _ => hterm i)
  have hlow : ∀ᶠ n in atTop, ∀ i,
      a i * (c n i - p i) ^ 2 ≤ SmoothScalar.divergence (s i) (p i) (c n i) := by
    apply Filter.eventually_all.mpr
    intro i
    exact ((tendsto_pi_nhds.mp hct) i).eventually ((hcurv i).mono (fun x hx => hx.1))
  have hupp : ∀ᶠ n in atTop, ∀ i,
      SmoothScalar.divergence (s i) (p i) (base n i) ≤ b i * (base n i - p i) ^ 2 := by
    apply Filter.eventually_all.mpr
    intro i
    exact ((tendsto_pi_nhds.mp hbase) i).eventually ((hcurv i).mono (fun x hx => hx.2))
  refine ⟨R, ?_⟩
  filter_upwards [hlow, hupp] with n hnlow hnupp
  have hregret := vertex_regret_bound s p (base n) (c n) hp hsum (hgain n)
  have htotal : totalDiv s p (base n) ≤ (e n) ^ 2 * K := by
    rw [totalDiv_eq_sum]
    calc
      (∑ i, SmoothScalar.divergence (s i) (p i) (base n i)) ≤
          ∑ i, b i * (base n i - p i) ^ 2 := Finset.sum_le_sum (fun i _ => hnupp i)
      _ = (e n) ^ 2 * K := by
        dsimp [base, K]
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro i _
        ring
  apply (pi_norm_le_iff_of_nonneg hR).mpr
  intro i
  have hcoord : a i * (c n i - p i) ^ 2 ≤ (e n) ^ 2 * K :=
    (hnlow i).trans ((scalar_divergence_le_total s p (c n) hp (hc n) i).trans (hregret.trans htotal))
  let r : ℝ := ((e n)⁻¹ • (c n - p)) i
  have hid : c n i - p i = e n * r := by
    dsimp [r]
    field_simp [ne_of_gt (hepos n)]
  rw [hid] at hcoord
  have hnormalized : a i * r ^ 2 ≤ K := by
    have hmul : (e n) ^ 2 * (a i * r ^ 2) ≤ (e n) ^ 2 * K := by nlinarith
    exact (mul_le_mul_left (sq_pos_of_pos (hepos n))).mp hmul
  have hsq : |r| ^ 2 ≤ K / a i := by
    apply (le_div_iff₀ (ha i)).mpr
    rw [sq_abs]
    nlinarith
  have habs : |r| ≤ K / a i + 1 := by
    nlinarith [sq_nonneg (|r| - (1 : ℝ) / 2)]
  have hsumterm : K / a i + 1 ≤ R := Finset.single_le_sum (fun j _ => hterm j) (Finset.mem_univ i)
  change ‖r‖ ≤ R
  rw [Real.norm_eq_abs]
  exact habs.trans hsumterm



lemma hessian_symmetric (s : ι → SmoothScalar.Score) (p x y : Vec ι) :
    hessian s p x y = hessian s p y x := by
  rw [hessian_apply, hessian_apply]
  apply Finset.sum_congr rfl
  intro i _
  ring

lemma hessian_positive (s : ι → SmoothScalar.Score) (p x : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1) (hx : x ≠ 0) : 0 < hessian s p x x := by
  rw [hessian_apply]
  have hex : ∃ i, x i ≠ 0 := by
    by_contra! hn
    apply hx
    funext i
    exact hn i
  obtain ⟨j, hj⟩ := hex
  apply Finset.sum_pos'
  · intro i _
    simpa only [pow_two, mul_assoc] using
      mul_nonneg ((s i).positive (p i) (hp i)).le (sq_nonneg (x i))
  · refine ⟨j, Finset.mem_univ j, ?_⟩
    simpa only [pow_two, mul_assoc] using
      mul_pos ((s j).positive (p j) (hp j)) (sq_pos_of_ne_zero hj)

/-- Smooth S1: common small-error repairs force one tangent direction normal
under all positive Hessians. Localization, bounded scaling, compactness and
varying-direction differentiation are proved, not assumed. -/
theorem smooth_common_repair_hessian_necessary {K : Type*}
    (s : K → ι → SmoothScalar.Score) (k0 : K) (p h : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1) (hsum : ∑ i, p i = 1)
    (e : ℕ → ℝ) (c : ℕ → Vec ι)
    (hepos : ∀ n, 0 < e n) (he : Tendsto e atTop (𝓝 0))
    (hc : ∀ n i, c n i ∈ Ioo 0 1) (hcsum : ∀ n, ∑ i, c n i = 1)
    (hgain : ∀ n k i, totalDiv (s k) (vertex i) (c n) ≤
      totalDiv (s k) (vertex i) (p + e n • h)) :
    ∃ z ∈ Submodule.span ℝ (Set.range (fun i => p - vertex i)),
      ∀ k u, u ∈ Submodule.span ℝ (Set.range (fun i => p - vertex i)) →
        hessian (s k) p (h - z) u = 0 := by
  let r : ℕ → Vec ι := fun n => (e n)⁻¹ • (c n - p)
  obtain ⟨R, hR⟩ := normalized_repairs_bounded (s k0) p h hp hsum e c hepos he hc
    (fun n i => hgain n k0 i)
  have hrball : ∀ᶠ n in atTop, r n ∈ Metric.closedBall (0 : Vec ι) R := by
    simpa only [Metric.mem_closedBall, dist_zero_right] using hR
  obtain ⟨z, hzball, phi, hphi, hzlim⟩ :=
    (isCompact_closedBall (0 : Vec ι) R).tendsto_subseq' hrball.frequently
  let T : Submodule ℝ (Vec ι) := Submodule.span ℝ (Set.range (fun i => p - vertex i))
  have hcmem : ∀ n, c n ∈ convexHull ℝ (Set.range (vertex : ι → Vec ι)) := by
    intro n
    exact mem_convexHull_of_exists_fintype (c n) vertex (fun i => (hc n i).1.le)
      (hcsum n) (fun i => Set.mem_range_self i) (vertex_barycenter (c n))
  have hrmem : ∀ n, r n ∈ T := by
    intro n
    exact T.smul_mem ((e n)⁻¹) (LocalRigidity.convexHull_sub_mem vertex p (c n) (hcmem n))
  have hzmem : z ∈ T := (Submodule.closed_of_finiteDimensional T).mem_of_tendsto hzlim
    (Filter.Eventually.of_forall (fun n => hrmem (phi n)))
  have hrepr : ∀ n, p + e n • r n = c n := by
    intro n
    dsimp [r]
    rw [smul_smul, mul_inv_cancel₀ (ne_of_gt (hepos n)), one_smul]
    abel
  refine ⟨z, hzmem, ?_⟩
  intro k u hu
  have hn : ∀ i, 0 ≤ hessian (s k) p (p - vertex i) (h - z) := by
    intro i
    apply smooth_first_order_nonnegative (totalDiv (s k) (vertex i))
      (hessian (s k) p (p - vertex i)) p h z (score_hasFDerivAt (s k) (vertex i) p hp)
      (e ∘ phi) (r ∘ phi) (fun n => hepos (phi n))
      (he.comp hphi.tendsto_atTop) hzlim
    intro n
    simp only [Function.comp_apply]
    rw [hrepr]
    exact hgain (phi n) k i
  have hzall := LocalRigidity.barycenter_nonnegative_vanish (hessian (s k) p) vertex p p (h - z)
    (fun i => (hp i).1) hsum (vertex_barycenter p) hn
  rw [hessian_symmetric]
  exact LocalRigidity.orthogonal_span (hessian (s k) p) vertex p (h - z) hzall u hu

end FiniteScores
#print axioms smooth_common_repair_hessian_necessary
#check smooth_common_repair_hessian_necessary
end SmoothRigidity
