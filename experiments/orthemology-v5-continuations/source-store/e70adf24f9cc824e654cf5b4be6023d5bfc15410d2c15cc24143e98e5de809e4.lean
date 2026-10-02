import BregmanProjection

/-!
S7 robustness extension, separate from the frozen six-module exact chain.
The additive tolerance is nonnegative and eta_n / epsilon_n tends to zero.
No linear-scale localization is assumed: all-state first-derivative coercivity
and absorption prove it, after scalar Bregman localization. The result covers
fixed smooth additive generators on finite genuine categorical outcomes.
-/

noncomputable section
open scoped Topology BigOperators
open Filter Set Asymptotics

namespace SmoothRobustness
open SmoothRigidity LocalRigidity

variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]

/-- The positive part of all statewise first derivatives is coercive on the
coherent tangent space. Its coercivity uses every truth state. -/
lemma positive_derivative_coercive [FiniteDimensional ℝ E]
    {ι : Type*} [Fintype ι]
    (B : Form E) (hpos : ∀ x : E, x ≠ 0 → 0 < B x x)
    (v : ι → E) (w : ι → ℝ) (p : E)
    (hw : ∀ i, 0 < w i) (hsum : ∑ i, w i = 1)
    (hcenter : ∑ i, w i • v i = p) :
    ∃ a > 0, ∀ x ∈ Submodule.span ℝ (Set.range (fun i => p - v i)),
      a * ‖x‖ ≤ ∑ i, max (B (p - v i) x) 0 := by
  let T := Submodule.span ℝ (Set.range (fun i => p - v i))
  let g : T → ℝ := fun x => ∑ i, max (B (p - v i) x) 0
  have hgcont : Continuous g := by dsimp [g]; fun_prop
  have hgpos : ∀ x ∈ Metric.sphere (0 : T) 1, 0 < g x := by
    intro x hx
    have hxne : (x : E) ≠ 0 := by
      intro hz
      have hnorm : ‖x‖ = 1 := by simpa only [Metric.mem_sphere, dist_zero_right] using hx
      have : x = 0 := Subtype.ext hz
      simp [this] at hnorm
    have hg0 : 0 ≤ g x := Finset.sum_nonneg (fun i _ => le_max_right _ _)
    by_contra! hn
    have hgz : g x = 0 := le_antisymm hn hg0
    have hall : ∀ i, B (p - v i) (x : E) ≤ 0 := by
      have hh := (Finset.sum_eq_zero_iff_of_nonneg (fun i (_ : i ∈ Finset.univ) =>
        (le_max_right (B (p - v i) (x : E)) 0))).mp hgz
      intro i
      have hi := hh i (Finset.mem_univ i)
      exact le_trans (le_max_left _ _) (le_of_eq hi)
    have hzero := barycenter_nonnegative_vanish B v w p (-(x : E)) hw hsum hcenter
      (fun i => by simpa only [map_neg, neg_nonneg] using hall i)
    have hxx := orthogonal_span B v p (-(x : E)) hzero (x : E) x.property
    simp only [map_neg] at hxx
    have hh := hpos (x : E) hxne
    linarith
  obtain ⟨a, ha, hmin⟩ := (isCompact_sphere (0 : T) 1).exists_forall_le'
    hgcont.continuousOn hgpos
  refine ⟨a, ha, ?_⟩
  intro x hx
  by_cases hx0 : x = 0
  · simp [hx0]
  have hnx : 0 < ‖x‖ := norm_pos_iff.mpr hx0
  let y : T := ⟨‖x‖⁻¹ • x, T.smul_mem _ hx⟩
  have hnorm : ‖y‖ = 1 := by
    change ‖‖x‖⁻¹ • x‖ = 1
    rw [norm_smul, Real.norm_eq_abs, abs_inv, abs_of_pos hnx,
      inv_mul_cancel₀ (ne_of_gt hnx)]
  have hy : y ∈ Metric.sphere (0 : T) 1 := by
    simpa only [Metric.mem_sphere, dist_zero_right] using hnorm
  have hh := mul_le_mul_of_nonneg_right (hmin y hy) hnx.le
  have hscale : g y * ‖x‖ = ∑ i, max (B (p - v i) x) 0 := by
    dsimp [g, y]
    rw [Finset.sum_mul]
    apply Finset.sum_congr rfl
    intro i _
    simp only [map_smul, smul_eq_mul]
    rw [max_mul_of_nonneg _ _ hnx.le]
    field_simp
  rwa [hscale] at hh


lemma approximate_first_order_nonnegative (f : E → ℝ) (L : E →L[ℝ] ℝ) (p h z : E)
    (hf : HasFDerivAt f L p) (e eta : ℕ → ℝ) (r : ℕ → E)
    (hepos : ∀ n, 0 < e n) (he : Tendsto e atTop (𝓝 0))
    (heta : Tendsto (fun n => eta n / e n) atTop (𝓝 0))
    (hr : Tendsto r atTop (𝓝 z))
    (hgain : ∀ n, f (p + e n • r n) ≤ f (p + e n • h) + eta n) :
    0 ≤ L (h - z) := by
  have hbase := varying_direction_limit f L p h hf e (fun _ => h) hepos he tendsto_const_nhds
  have hrepair := varying_direction_limit f L p z hf e r hepos he hr
  have hlim := (hbase.sub hrepair).add heta
  have hnonneg : ∀ᶠ n in atTop,
      0 ≤ (f (p + e n • h) - f p) / e n -
        (f (p + e n • r n) - f p) / e n + eta n / e n := by
    apply Filter.Eventually.of_forall
    intro n
    have hn := (div_le_div_iff_of_pos_right (hepos n)).mpr (hgain n)
    rw [add_div] at hn
    simp only [sub_div]
    linarith
  have hh := ge_of_tendsto hlim hnonneg
  simpa only [map_sub, add_zero] using hh

section FiniteScores
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

lemma approximate_vertex_regret_bound (s : ι → SmoothScalar.Score) (p b c : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1) (hsum : ∑ i, p i = 1) (eta : ℝ)
    (hgain : ∀ i, totalDiv s (vertex i) c ≤ totalDiv s (vertex i) b + eta) :
    totalDiv s p c ≤ totalDiv s p b + eta := by
  have hh : -eta ≤ ∑ i, p i * (totalDiv s (vertex i) b - totalDiv s (vertex i) c) := by
    calc
      -eta = ∑ i, p i * (-eta) := by rw [← Finset.sum_mul, hsum, one_mul]
      _ ≤ _ := Finset.sum_le_sum (fun i _ => mul_le_mul_of_nonneg_left
        (by linarith [hgain i]) (hp i).1.le)
  rw [weighted_bregman_gain (potential s) (gradient s) vertex p p b c hsum (vertex_barycenter p)] at hh
  linarith

lemma approximate_repairs_tendsto (s : ι → SmoothScalar.Score) (p : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1) (hsum : ∑ i, p i = 1)
    (b c : ℕ → Vec ι) (eta : ℕ → ℝ)
    (hb : Tendsto b atTop (𝓝 p)) (heta : Tendsto eta atTop (𝓝 0))
    (hc : ∀ n i, c n i ∈ Ioo 0 1)
    (hgain : ∀ n i, totalDiv s (vertex i) (c n) ≤ totalDiv s (vertex i) (b n) + eta n) :
    Tendsto c atTop (𝓝 p) := by
  have hregret := fun n => approximate_vertex_regret_bound s p (b n) (c n) hp hsum (eta n) (hgain n)
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

lemma sublinear_tolerance_tendsto_zero (e eta : ℕ → ℝ)
    (hepos : ∀ n, 0 < e n) (he : Tendsto e atTop (𝓝 0))
    (heta : Tendsto (fun n => eta n / e n) atTop (𝓝 0)) :
    Tendsto eta atTop (𝓝 0) := by
  have hh := heta.mul he
  have hid : (fun n => eta n / e n * e n) = eta := by
    funext n
    exact div_mul_cancel₀ _ (ne_of_gt (hepos n))
  simpa only [hid, mul_zero] using hh

/-- The all-state bound improves the barycentric square-root bound to linear
scale, including tolerances between quadratic and linear size. -/
lemma normalized_approximate_repairs_bounded (s : ι → SmoothScalar.Score) (p h : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1) (hsum : ∑ i, p i = 1)
    (e eta : ℕ → ℝ) (c : ℕ → Vec ι)
    (hepos : ∀ n, 0 < e n) (he : Tendsto e atTop (𝓝 0))
    (heta0 : ∀ n, 0 ≤ eta n)
    (heta : Tendsto (fun n => eta n / e n) atTop (𝓝 0))
    (hc : ∀ n i, c n i ∈ Ioo 0 1) (hcsum : ∀ n, ∑ i, c n i = 1)
    (hgain : ∀ n i, totalDiv s (vertex i) (c n) ≤
      totalDiv s (vertex i) (p + e n • h) + eta n) :
    ∃ R : ℝ, ∀ᶠ n in atTop, ‖(e n)⁻¹ • (c n - p)‖ ≤ R := by
  have hne : Nonempty ι := by
    by_contra hn
    have : IsEmpty ι := not_nonempty_iff.mp hn
    simp at hsum
  letI := hne
  let N : ℝ := Fintype.card ι
  have hN : 0 < N := by
    dsimp [N]
    exact_mod_cast (Fintype.card_pos : 0 < Fintype.card ι)
  let f : ι → Vec ι → ℝ := fun i => totalDiv s (vertex i)
  let L : ι → Vec ι →L[ℝ] ℝ := fun i => hessian s p (p - vertex i)
  have hf : ∀ i, HasFDerivAt (f i) (L i) p := fun i => score_hasFDerivAt s (vertex i) p hp
  obtain ⟨a, ha, hco⟩ := positive_derivative_coercive (hessian s p)
    (fun x hx => hessian_positive s p x hp hx) vertex p p (fun i => (hp i).1) hsum (vertex_barycenter p)
  let base : ℕ → Vec ι := fun n => p + e n • h
  have hbase : Tendsto base atTop (𝓝 p) := by
    simpa [base] using
      (tendsto_const_nhds : Tendsto (fun _ : ℕ => p) atTop (𝓝 p)).add
        (he.smul (tendsto_const_nhds : Tendsto (fun _ : ℕ => h) atTop (𝓝 h)))
  have hct := approximate_repairs_tendsto s p hp hsum base c eta hbase
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
  have hcmem : c n ∈ convexHull ℝ (Set.range (vertex : ι → Vec ι)) :=
    mem_convexHull_of_exists_fintype (c n) vertex (fun i => (hc n i).1.le)
      (hcsum n) (fun i => Set.mem_range_self i) (vertex_barycenter (c n))
  have hlow := hco (c n - p) (convexHull_sub_mem vertex p (c n) hcmem)
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

theorem approximate_common_repair_hessian_necessary {K : Type*}
    (s : K → ι → SmoothScalar.Score) (k0 : K) (p h : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1) (hsum : ∑ i, p i = 1)
    (e eta : ℕ → ℝ) (c : ℕ → Vec ι)
    (hepos : ∀ n, 0 < e n) (he : Tendsto e atTop (𝓝 0))
    (heta0 : ∀ n, 0 ≤ eta n)
    (heta : Tendsto (fun n => eta n / e n) atTop (𝓝 0))
    (hc : ∀ n i, c n i ∈ Ioo 0 1) (hcsum : ∀ n, ∑ i, c n i = 1)
    (hgain : ∀ n k i, totalDiv (s k) (vertex i) (c n) ≤
      totalDiv (s k) (vertex i) (p + e n • h) + eta n) :
    ∃ z ∈ Submodule.span ℝ (Set.range (fun i => p - vertex i)),
      ∀ k u, u ∈ Submodule.span ℝ (Set.range (fun i => p - vertex i)) →
        hessian (s k) p (h - z) u = 0 := by
  let r : ℕ → Vec ι := fun n => (e n)⁻¹ • (c n - p)
  obtain ⟨R, hR⟩ := normalized_approximate_repairs_bounded (s k0) p h hp hsum e eta c hepos he heta0 heta hc hcsum
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
    apply approximate_first_order_nonnegative (totalDiv (s k) (vertex i))
      (hessian (s k) p (p - vertex i)) p h z (score_hasFDerivAt (s k) (vertex i) p hp)
      (e ∘ phi) (eta ∘ phi) (r ∘ phi) (fun n => hepos (phi n))
      (he.comp hphi.tendsto_atTop) (heta.comp hphi.tendsto_atTop) hzlim
    intro n
    simp only [Function.comp_apply]
    rw [hrepr]
    exact hgain (phi n) k i
  have hzall := LocalRigidity.barycenter_nonnegative_vanish (hessian (s k) p) vertex p p (h - z)
    (fun i => (hp i).1) hsum (vertex_barycenter p) hn
  rw [hessian_symmetric]
  exact LocalRigidity.orthogonal_span (hessian (s k) p) vertex p (h - z) hzall u hu


#print axioms normalized_approximate_repairs_bounded
#print axioms approximate_common_repair_hessian_necessary
#check approximate_common_repair_hessian_necessary
open GeneratorRigidity

theorem approximate_repairs_hessians_proportional
    (s t : ι → SmoothScalar.Score) (i0 : ι) (p : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1) (hsum : ∑ i, p i = 1)
    (e eta : ℕ → ℝ) (c : ℕ → Vec ι)
    (hepos : ∀ n, 0 < e n) (he : Tendsto e atTop (𝓝 0))
    (heta0 : ∀ n, 0 ≤ eta n)
    (heta : Tendsto (fun n => eta n / e n) atTop (𝓝 0))
    (hc : ∀ n i, c n i ∈ Ioo 0 1) (hcsum : ∀ n, ∑ i, c n i = 1)
    (hsgain : ∀ n i, totalDiv s (vertex i) (c n) ≤ totalDiv s (vertex i) (p + e n • vertex i0) + eta n)
    (htgain : ∀ n i, totalDiv t (vertex i) (c n) ≤ totalDiv t (vertex i) (p + e n • vertex i0) + eta n) :
    ∃ r > 0, ∀ i, (s i).ddf (p i) = r * (t i).ddf (p i) := by
  let fam : Bool → ι → SmoothScalar.Score := fun k => if k then t else s
  have hboth : ∀ n k i, totalDiv (fam k) (vertex i) (c n) ≤
      totalDiv (fam k) (vertex i) (p + e n • vertex i0) + eta n := by
    intro n k i
    cases k
    · exact hsgain n i
    · exact htgain n i
  obtain ⟨z, hz, hnormal⟩ := approximate_common_repair_hessian_necessary fam false p (vertex i0)
    hp hsum e eta c hepos he heta0 heta hc hcsum hboth
  let u := vertex i0 - z
  have hu : u ≠ 0 := by
    intro hzero
    have heq : vertex i0 = z := sub_eq_zero.mp hzero
    exact vertex_transverse p hsum i0 (heq ▸ hz)
  apply positive_normal_proportional (fun i => (s i).ddf (p i))
    (fun i => (t i).ddf (p i)) u (fun i => (s i).positive (p i) (hp i))
    (fun i => (t i).positive (p i) (hp i)) hu
  · intro i j
    have hn := hnormal false (vertex i - vertex j) (vertex_difference_tangent p i j)
    change hessian s p u (vertex i - vertex j) = 0 at hn
    rw [map_sub, hessian_vertex, hessian_vertex] at hn
    exact sub_eq_zero.mp hn
  · intro i j
    have hn := hnormal true (vertex i - vertex j) (vertex_difference_tangent p i j)
    change hessian t p u (vertex i - vertex j) = 0 at hn
    rw [map_sub, hessian_vertex, hessian_vertex] at hn
    exact sub_eq_zero.mp hn



theorem universal_approximate_repairs_force_affine
    (hcard : 3 ≤ Fintype.card ι) (s t : ι → SmoothScalar.Score) (i0 : ι)
    (hcommon : ∀ p : Vec ι, (∀ i, p i ∈ Ioo 0 1) → (∑ i, p i = 1) →
      ∃ (e eta : ℕ → ℝ) (c : ℕ → Vec ι),
        (∀ n, 0 < e n) ∧ Tendsto e atTop (𝓝 0) ∧
        (∀ n, 0 ≤ eta n) ∧ Tendsto (fun n => eta n / e n) atTop (𝓝 0) ∧
        (∀ n i, c n i ∈ Ioo 0 1) ∧ (∀ n, ∑ i, c n i = 1) ∧
        (∀ n i, totalDiv s (vertex i) (c n) ≤ totalDiv s (vertex i) (p + e n • vertex i0) + eta n) ∧
        (∀ n i, totalDiv t (vertex i) (c n) ≤ totalDiv t (vertex i) (p + e n • vertex i0) + eta n)) :
    ∃ a > 0, ∃ b d : ι → ℝ, ∀ i x, x ∈ Icc 0 1 →
      (s i).f x = a * (t i).f x + b i * x + d i := by
  let r : ι → ℝ → ℝ := fun i x => (s i).ddf x / (t i).ddf x
  have hcompat : ∀ p : Vec ι, (∀ i, p i ∈ Ioo 0 1) → (∑ i, p i = 1) →
      ∀ i j, r i (p i) = r j (p j) := by
    intro p hp hsum i j
    obtain ⟨e, eta, c, hepos, helim, heta0, heta, hc, hcsum, hs, ht⟩ := hcommon p hp hsum
    obtain ⟨a, ha, haa⟩ := approximate_repairs_hessians_proportional s t i0 p hp hsum e eta c
      hepos helim heta0 heta hc hcsum hs ht
    dsimp [r]
    rw [haa i, haa j]
    field_simp [ne_of_gt ((t i).positive (p i) (hp i)), ne_of_gt ((t j).positive (p j) (hp j))]
  obtain ⟨a, ha⟩ := simplex_ratio_connectivity hcard r hcompat
  have hmid : (1 : ℝ) / 2 ∈ Ioo 0 1 := by constructor <;> norm_num
  have hapos : 0 < a := by
    have hm : 0 < r i0 ((1 : ℝ) / 2) :=
      div_pos ((s i0).positive _ hmid) ((t i0).positive _ hmid)
    rw [ha i0 ((1 : ℝ) / 2) hmid] at hm
    exact hm
  have hdd : ∀ i x, x ∈ Ioo 0 1 → (s i).ddf x = a * (t i).ddf x := by
    intro i x hx
    exact (div_eq_iff (ne_of_gt ((t i).positive x hx))).mp (ha i x hx)
  choose b d hbd using fun i => generators_affine_of_hessian_eq (s i) (t i) a (hdd i)
  exact ⟨a, hapos, b, d, hbd⟩


/-- One shared tolerance is measured in the declared score units. Separate
sublinear tolerances can be enlarged to their pointwise maximum. -/
def ApproximateCommonLocalRepairs (s t : ι → SmoothScalar.Score) (i0 : ι) : Prop :=
  ∀ p : Vec ι, (∀ i, p i ∈ Ioo 0 1) → (∑ i, p i = 1) →
    ∃ (e eta : ℕ → ℝ) (c : ℕ → Vec ι),
      (∀ n, 0 < e n) ∧ Tendsto e atTop (𝓝 0) ∧
      (∀ n, 0 ≤ eta n) ∧ Tendsto (fun n => eta n / e n) atTop (𝓝 0) ∧
      (∀ n i, c n i ∈ Ioo 0 1) ∧ (∀ n, ∑ i, c n i = 1) ∧
      (∀ n i, totalDiv s (vertex i) (c n) ≤ totalDiv s (vertex i) (p + e n • vertex i0) + eta n) ∧
      (∀ n i, totalDiv t (vertex i) (c n) ≤ totalDiv t (vertex i) (p + e n • vertex i0) + eta n)

/-- Sublinear additive loss tolerance does not enlarge the globally compatible
smooth additive generator classes in three or more genuine outcomes. -/
theorem universal_approximate_common_repair_iff_affine (hcard : 3 ≤ Fintype.card ι)
    (s t : ι → SmoothScalar.Score) (i0 : ι) :
    ApproximateCommonLocalRepairs s t i0 ↔ BregmanProjection.PositiveAffineEquivalent s t := by
  constructor
  · exact universal_approximate_repairs_force_affine hcard s t i0
  · intro ha
    have he := (BregmanProjection.universal_common_repair_iff_affine hcard s t i0).mpr ha
    intro p hp hpsum
    obtain ⟨e, c, hepos, helim, hc, hcsum, hs, ht⟩ := he p hp hpsum
    refine ⟨e, (fun _ => 0), c, hepos, helim, (fun _ => le_rfl), ?_, hc, hcsum, ?_, ?_⟩
    · simpa only [zero_div] using (tendsto_const_nhds : Tendsto (fun _ : ℕ => (0 : ℝ)) atTop (𝓝 0))
    · simpa only [add_zero] using hs
    · simpa only [add_zero] using ht

#print ApproximateCommonLocalRepairs
#print axioms positive_derivative_coercive
#print axioms universal_approximate_common_repair_iff_affine
#check universal_approximate_common_repair_iff_affine

end FiniteScores
end SmoothRobustness
