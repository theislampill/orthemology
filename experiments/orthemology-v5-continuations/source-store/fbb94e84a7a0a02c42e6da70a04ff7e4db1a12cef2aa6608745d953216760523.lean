import SmoothRobustness

/-!
General finite-truth-hull smooth necessity. Truth indices and coordinate indices
are distinct. The interior certificate is a strictly positive barycentric
presentation, not a literal Mathlib intrinsicInterior input. This module does
not formalize the separate diagonal-stabilizer/matroid component theorem.
-/
noncomputable section
open scoped Topology BigOperators
open Filter Set Asymptotics SmoothRigidity SmoothRobustness LocalRigidity

namespace FiniteHullSmoothRigidity
variable {ι J : Type*} [Fintype ι] [DecidableEq ι] [Fintype J]

omit [DecidableEq ι] in
lemma weighted_approximate_regret_bound
    (s : ι → SmoothScalar.Score) (v : J → Vec ι) (w : J → ℝ) (p b c : Vec ι)
    (hw : ∀ j, 0 ≤ w j) (hsum : ∑ j, w j = 1) (hcenter : ∑ j, w j • v j = p)
    (eta : ℝ) (hgain : ∀ j, totalDiv s (v j) c ≤ totalDiv s (v j) b + eta) :
    totalDiv s p c ≤ totalDiv s p b + eta := by
  have hh : -eta ≤ ∑ j, w j * (totalDiv s (v j) b - totalDiv s (v j) c) := by
    calc
      -eta = ∑ j, w j * (-eta) := by rw [← Finset.sum_mul, hsum, one_mul]
      _ ≤ _ := Finset.sum_le_sum (fun j _ => mul_le_mul_of_nonneg_left
        (by linarith [hgain j]) (hw j))
  rw [weighted_bregman_gain (potential s) (gradient s) v w p b c hsum hcenter] at hh
  linarith

lemma weighted_approximate_repairs_tendsto
    (s : ι → SmoothScalar.Score) (v : J → Vec ι) (w : J → ℝ) (p : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1) (hw : ∀ j, 0 ≤ w j)
    (hsum : ∑ j, w j = 1) (hcenter : ∑ j, w j • v j = p)
    (b c : ℕ → Vec ι) (eta : ℕ → ℝ)
    (hb : Tendsto b atTop (𝓝 p)) (heta : Tendsto eta atTop (𝓝 0))
    (hc : ∀ n i, c n i ∈ Ioo 0 1)
    (hgain : ∀ n j, totalDiv s (v j) (c n) ≤ totalDiv s (v j) (b n) + eta n) :
    Tendsto c atTop (𝓝 p) := by
  have hregret := fun n => weighted_approximate_regret_bound s v w p (b n) (c n)
    hw hsum hcenter (eta n) (hgain n)
  have hlim : Tendsto (fun n => totalDiv s p (b n) + eta n) atTop (𝓝 0) := by
    have hh := (score_hasFDerivAt s p p hp).continuousAt.tendsto.comp hb
    have ht := hh.add heta
    simpa [totalDiv, bregman, Function.comp_def] using ht
  apply tendsto_pi_nhds.mpr
  intro i
  apply SmoothScalar.tendsto_of_divergence_tendsto_zero (s i) (p i) (hp i) (fun n => c n i)
    (fun n => hc n i)
  exact squeeze_zero
    (fun n => SmoothScalar.divergence_nonneg (s i) (p i) (c n i) (hp i) (hc n i))
    (fun n => (scalar_divergence_le_total s p (c n) hp (hc n) i).trans (hregret n)) hlim

lemma finite_hull_normalized_approximate_repairs_bounded (s : ι → SmoothScalar.Score) (v : J → Vec ι) (w : J → ℝ) (p h : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1) (hw : ∀ j, 0 < w j)
    (hsum : ∑ j, w j = 1) (hcenter : ∑ j, w j • v j = p)
    (e eta : ℕ → ℝ) (c : ℕ → Vec ι)
    (hepos : ∀ n, 0 < e n) (he : Tendsto e atTop (𝓝 0))
    (heta0 : ∀ n, 0 ≤ eta n)
    (heta : Tendsto (fun n => eta n / e n) atTop (𝓝 0))
    (hc : ∀ n i, c n i ∈ Ioo 0 1)
    (hcmem : ∀ n, c n ∈ convexHull ℝ (Set.range v))
    (hgain : ∀ n i, totalDiv s (v i) (c n) ≤
      totalDiv s (v i) (p + e n • h) + eta n) :
    ∃ R : ℝ, ∀ᶠ n in atTop, ‖(e n)⁻¹ • (c n - p)‖ ≤ R := by
  have hne : Nonempty J := by
    by_contra hn
    have : IsEmpty J := not_nonempty_iff.mp hn
    simp at hsum
  letI := hne
  let N : ℝ := Fintype.card J
  have hN : 0 < N := by
    dsimp [N]
    exact_mod_cast (Fintype.card_pos : 0 < Fintype.card J)
  let f : J → Vec ι → ℝ := fun i => totalDiv s (v i)
  let L : J → Vec ι →L[ℝ] ℝ := fun i => hessian s p (p - v i)
  have hf : ∀ i, HasFDerivAt (f i) (L i) p := fun i => score_hasFDerivAt s (v i) p hp
  obtain ⟨a, ha, hco⟩ := positive_derivative_coercive (hessian s p)
    (fun x hx => hessian_positive s p x hp hx) v w p hw hsum hcenter
  let base : ℕ → Vec ι := fun n => p + e n • h
  have hbase : Tendsto base atTop (𝓝 p) := by
    simpa [base] using
      (tendsto_const_nhds : Tendsto (fun _ : ℕ => p) atTop (𝓝 p)).add
        (he.smul (tendsto_const_nhds : Tendsto (fun _ : ℕ => h) atTop (𝓝 h)))
  have hct := weighted_approximate_repairs_tendsto s v w p hp (fun j => (hw j).le) hsum hcenter base c eta hbase
    (sublinear_tolerance_tendsto_zero e eta hepos he heta) hc hgain
  have hxi : Tendsto (fun n => c n - p) atTop (𝓝 (0 : Vec ι)) := by
    simpa using hct.sub (tendsto_const_nhds : Tendsto (fun _ : ℕ => p) atTop (𝓝 p))
  have hrem : ∀ᶠ n in atTop, ∀ i,
      |f i (c n) - f i p - L i (c n - p)| ≤ (a / (2 * N)) * ‖c n - p‖ := by
    apply Filter.eventually_all.mpr
    intro i
    have hlo := (hasFDerivAt_iff_isLittleO_nhds_zero.mp (hf i)).comp_tendsto hxi
    have hh := isLittleO_iff.mp hlo (c := a / (2 * N)) (div_pos ha (mul_pos (by norm_num) hN))
    have hid : ∀ n, p + (c n - p) = c n := by intro n; abel
    simpa only [Function.comp_apply, hid, Real.norm_eq_abs] using hh
  let M : ℝ := ∑ i, (|L i h| + 1)
  have hM : 0 ≤ M := Finset.sum_nonneg (fun i _ => by positivity)
  have hbasebound : ∀ᶠ n in atTop, ∀ i, f i (base n) - f i p ≤ e n * M := by
    apply Filter.eventually_all.mpr
    intro i
    have ht := varying_direction_limit (f i) (L i) p h (hf i) e (fun _ => h) hepos he tendsto_const_nhds
    have hh : ∀ᶠ n in atTop, (f i (base n) - f i p) / e n ≤ |L i h| + 1 := by
      have hevent : ∀ᶠ n in atTop, (f i (base n) - f i p) / e n < |L i h| + 1 :=
        ht (Iio_mem_nhds (show L i h < |L i h| + 1 by linarith [le_abs_self (L i h)]))
      exact hevent.mono (fun n hn => hn.le)
    filter_upwards [hh] with n hn
    have hm : |L i h| + 1 ≤ M := by
      dsimp [M]
      exact Finset.single_le_sum (fun j (_ : j ∈ Finset.univ) => add_nonneg (abs_nonneg (L j h)) (by norm_num)) (Finset.mem_univ i)
    have hdiv := (div_le_iff₀ (hepos n)).mp hn
    calc
      f i (base n) - f i p ≤ (|L i h| + 1) * e n := hdiv
      _ ≤ M * e n := mul_le_mul_of_nonneg_right hm (hepos n).le
      _ = e n * M := mul_comm _ _
  have hetabound : ∀ᶠ n in atTop, eta n ≤ e n := by
    have hh := heta (Iio_mem_nhds (show (0 : ℝ) < 1 by norm_num))
    filter_upwards [hh] with n hn
    simpa only [one_mul] using ((div_lt_iff₀ (hepos n)).mp hn).le
  refine ⟨2 * N * (M + 1) / a, ?_⟩
  filter_upwards [hrem, hbasebound, hetabound] with n hnrem hnbase hneta
  have hlow := hco (c n - p) (convexHull_sub_mem v p (c n) (hcmem n))
  have hupper : (∑ i, max (L i (c n - p)) 0) ≤
      N * (e n * M + eta n) + a / 2 * ‖c n - p‖ := by
    have hi : ∀ i, max (L i (c n - p)) 0 ≤
        e n * M + eta n + (a / (2 * N)) * ‖c n - p‖ := by
      intro i
      apply max_le
      · have hh := (abs_le.mp (hnrem i)).1
        have hg := hgain n i
        have hb := hnbase i
        change f i (c n) ≤ f i (base n) + eta n at hg
        linarith
      · exact add_nonneg (add_nonneg (mul_nonneg (hepos n).le hM) (heta0 n))
          (mul_nonneg (div_nonneg ha.le (mul_pos (by norm_num) hN).le) (norm_nonneg _))
    have hh := Finset.sum_le_sum (fun i (_ : i ∈ Finset.univ) => hi i)
    simp only [Finset.sum_const, Finset.card_univ, nsmul_eq_mul] at hh
    convert hh using 1
    dsimp [N]
    field_simp
    ring
  change a * ‖c n - p‖ ≤ ∑ i, max (L i (c n - p)) 0 at hlow
  have hlin : a * ‖c n - p‖ ≤ 2 * N * e n * (M + 1) := by
    nlinarith [norm_nonneg (c n - p)]
  rw [norm_smul, Real.norm_eq_abs, abs_inv, abs_of_pos (hepos n)]
  apply (le_div_iff₀ ha).mpr
  calc
    (e n)⁻¹ * ‖c n - p‖ * a = (a * ‖c n - p‖) / e n := by ring
    _ ≤ 2 * N * (M + 1) := (div_le_iff₀ (hepos n)).mpr (by nlinarith [hlin])


theorem finite_hull_approximate_hessian_necessary {K : Type*}
    (s : K → ι → SmoothScalar.Score) (k0 : K)
    (v : J → Vec ι) (w : J → ℝ) (p h : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1) (hw : ∀ j, 0 < w j)
    (hsum : ∑ j, w j = 1) (hcenter : ∑ j, w j • v j = p)
    (e eta : ℕ → ℝ) (c : ℕ → Vec ι)
    (hepos : ∀ n, 0 < e n) (he : Tendsto e atTop (𝓝 0))
    (heta0 : ∀ n, 0 ≤ eta n)
    (heta : Tendsto (fun n => eta n / e n) atTop (𝓝 0))
    (hc : ∀ n i, c n i ∈ Ioo 0 1)
    (hcmem : ∀ n, c n ∈ convexHull ℝ (Set.range v))
    (hgain : ∀ n k i, totalDiv (s k) (v i) (c n) ≤
      totalDiv (s k) (v i) (p + e n • h) + eta n) :
    ∃ z ∈ Submodule.span ℝ (Set.range (fun i => p - v i)),
      ∀ k u, u ∈ Submodule.span ℝ (Set.range (fun i => p - v i)) →
        hessian (s k) p (h - z) u = 0 := by
  let r : ℕ → Vec ι := fun n => (e n)⁻¹ • (c n - p)
  obtain ⟨R, hR⟩ := finite_hull_normalized_approximate_repairs_bounded (s k0) v w p h hp hw hsum hcenter e eta c hepos he heta0 heta hc hcmem
    (fun n i => hgain n k0 i)
  have hrball : ∀ᶠ n in atTop, r n ∈ Metric.closedBall (0 : Vec ι) R := by
    simpa only [Metric.mem_closedBall, dist_zero_right] using hR
  obtain ⟨z, hzball, phi, hphi, hzlim⟩ :=
    (isCompact_closedBall (0 : Vec ι) R).tendsto_subseq' hrball.frequently
  let T : Submodule ℝ (Vec ι) := Submodule.span ℝ (Set.range (fun i => p - v i))
  have hrmem : ∀ n, r n ∈ T := by
    intro n
    exact T.smul_mem ((e n)⁻¹) (LocalRigidity.convexHull_sub_mem v p (c n) (hcmem n))
  have hzmem : z ∈ T := (Submodule.closed_of_finiteDimensional T).mem_of_tendsto hzlim
    (Filter.Eventually.of_forall (fun n => hrmem (phi n)))
  have hrepr : ∀ n, p + e n • r n = c n := by
    intro n
    dsimp [r]
    rw [smul_smul, mul_inv_cancel₀ (ne_of_gt (hepos n)), one_smul]
    abel
  refine ⟨z, hzmem, ?_⟩
  intro k u hu
  have hn : ∀ i, 0 ≤ hessian (s k) p (p - v i) (h - z) := by
    intro i
    apply approximate_first_order_nonnegative (totalDiv (s k) (v i))
      (hessian (s k) p (p - v i)) p h z (score_hasFDerivAt (s k) (v i) p hp)
      (e ∘ phi) (eta ∘ phi) (r ∘ phi) (fun n => hepos (phi n))
      (he.comp hphi.tendsto_atTop) (heta.comp hphi.tendsto_atTop) hzlim
    intro n
    simp only [Function.comp_apply]
    rw [hrepr]
    exact hgain (phi n) k i
  have hzall := LocalRigidity.barycenter_nonnegative_vanish (hessian (s k) p) v w p (h - z)
    hw hsum hcenter hn
  rw [hessian_symmetric]
  exact LocalRigidity.orthogonal_span (hessian (s k) p) v p (h - z) hzall u hu



/-- Exact common repairs are the zero-tolerance specialization. -/
theorem finite_hull_common_hessian_necessary {K : Type*}
    (s : K → ι → SmoothScalar.Score) (k0 : K)
    (v : J → Vec ι) (w : J → ℝ) (p h : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1) (hw : ∀ j, 0 < w j)
    (hsum : ∑ j, w j = 1) (hcenter : ∑ j, w j • v j = p)
    (e : ℕ → ℝ) (c : ℕ → Vec ι)
    (hepos : ∀ n, 0 < e n) (he : Tendsto e atTop (𝓝 0))
    (hc : ∀ n i, c n i ∈ Ioo 0 1)
    (hcmem : ∀ n, c n ∈ convexHull ℝ (Set.range v))
    (hgain : ∀ n k j, totalDiv (s k) (v j) (c n) ≤ totalDiv (s k) (v j) (p + e n • h)) :
    ∃ z ∈ Submodule.span ℝ (Set.range (fun j => p - v j)),
      ∀ k u, u ∈ Submodule.span ℝ (Set.range (fun j => p - v j)) →
        hessian (s k) p (h - z) u = 0 := by
  apply finite_hull_approximate_hessian_necessary s k0 v w p h hp hw hsum hcenter
    e (fun _ => 0) c hepos he (fun _ => le_rfl) ?_ hc hcmem
  · simpa only [add_zero] using hgain
  · simpa only [zero_div] using (tendsto_const_nhds : Tendsto (fun _ : ℕ => (0 : ℝ)) atTop (𝓝 0))

#print axioms finite_hull_normalized_approximate_repairs_bounded
#print axioms finite_hull_approximate_hessian_necessary
#print axioms finite_hull_common_hessian_necessary
#check finite_hull_approximate_hessian_necessary
#check finite_hull_common_hessian_necessary

end FiniteHullSmoothRigidity
