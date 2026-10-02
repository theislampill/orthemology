import Mathlib

/-!
General finite-dimensional quadratic common-repair rigidity.
This module is separate from the frozen early exact-certificate module.
Development scope is explicit in each theorem; no axioms or placeholders.
-/

noncomputable section
open scoped BigOperators Topology
open Filter Finset

namespace LocalRigidity

variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]

abbrev Form (E : Type*) [NormedAddCommGroup E] [NormedSpace ℝ E] :=
  E →L[ℝ] E →L[ℝ] ℝ

def loss (B : Form E) (b v : E) : ℝ := B (b - v) (b - v)

lemma gain_expansion (B : Form E) (hsym : ∀ x y, B x y = B y x)
    (p h z v : E) (e : ℝ) :
    loss B (p + e • h) v - loss B (p + e • z) v =
      e * (2 * B (p - v) (h - z) + e * (B h h - B z z)) := by
  unfold loss
  rw [show p + e • h - v = (p - v) + e • h by abel,
      show p + e • z - v = (p - v) + e • z by abel]
  simp only [map_add, map_sub, map_smul, ContinuousLinearMap.add_apply,
    ContinuousLinearMap.smul_apply, ContinuousLinearMap.sub_apply, smul_eq_mul]
  rw [hsym h p, hsym h v, hsym z p, hsym z v]
  ring

lemma continuous_diag (B : Form E) : Continuous (fun x : E => B x x) := by
  exact B.continuous.clm_apply continuous_id

lemma first_order_nonnegative (B : Form E) (hsym : ∀ x y, B x y = B y x)
    (p h v z : E) (e : ℕ → ℝ) (r : ℕ → E)
    (hepos : ∀ n, 0 < e n) (he : Tendsto e atTop (𝓝 0))
    (hr : Tendsto r atTop (𝓝 z))
    (hgain : ∀ n, loss B (p + e n • r n) v ≤ loss B (p + e n • h) v) :
    0 ≤ B (p - v) (h - z) := by
  have hineq : ∀ n, 0 ≤ 2 * B (p - v) (h - r n) +
      e n * (B h h - B (r n) (r n)) := by
    intro n
    have hn := hgain n
    have hx := gain_expansion B hsym p h (r n) v (e n)
    have hm : 0 ≤ e n * (2 * B (p - v) (h - r n) +
        e n * (B h h - B (r n) (r n))) := by linarith
    exact (mul_nonneg_iff_of_pos_left (hepos n)).mp hm
  have hlinear : Tendsto (fun n => B (p - v) (h - r n)) atTop
      (𝓝 (B (p - v) (h - z))) :=
    (B (p - v)).continuous.tendsto (h - z) |>.comp (tendsto_const_nhds.sub hr)
  have hquad : Tendsto (fun n => B (r n) (r n)) atTop (𝓝 (B z z)) :=
    (continuous_diag B).tendsto z |>.comp hr
  have hlim : Tendsto (fun n => 2 * B (p - v) (h - r n) +
      e n * (B h h - B (r n) (r n))) atTop (𝓝 (2 * B (p - v) (h - z))) := by
    simpa using (tendsto_const_nhds.mul hlinear).add
      (he.mul (tendsto_const_nhds.sub hquad))
  have hnonneg := ge_of_tendsto hlim (Filter.Eventually.of_forall hineq)
  linarith



lemma barycenter_sub_sum {ι : Type*} [Fintype ι]
    (v : ι → E) (w : ι → ℝ) (p : E)
    (hwsum : ∑ i, w i = 1) (hcenter : ∑ i, w i • v i = p) :
    ∑ i, w i • (p - v i) = 0 := by
  simp_rw [smul_sub]
  rw [Finset.sum_sub_distrib, ← Finset.sum_smul, hwsum, hcenter, one_smul, sub_self]

lemma barycenter_form_sum {ι : Type*} [Fintype ι]
    (B : Form E) (v : ι → E) (w : ι → ℝ) (p d : E)
    (hwsum : ∑ i, w i = 1) (hcenter : ∑ i, w i • v i = p) :
    ∑ i, w i * B (p - v i) d = 0 := by
  have hzero := barycenter_sub_sum v w p hwsum hcenter
  have hx : B (∑ i, w i • (p - v i)) d = 0 := by rw [hzero]; simp
  simpa only [map_sum, map_smul, ContinuousLinearMap.sum_apply,
    ContinuousLinearMap.smul_apply, smul_eq_mul] using hx

lemma barycenter_nonnegative_vanish {ι : Type*} [Fintype ι]
    (B : Form E) (v : ι → E) (w : ι → ℝ) (p d : E)
    (hwpos : ∀ i, 0 < w i) (hwsum : ∑ i, w i = 1)
    (hcenter : ∑ i, w i • v i = p)
    (hnonneg : ∀ i, 0 ≤ B (p - v i) d) :
    ∀ i, B (p - v i) d = 0 := by
  have hsum := barycenter_form_sum B v w p d hwsum hcenter
  have hterms : ∀ i ∈ (Finset.univ : Finset ι), 0 ≤ w i * B (p - v i) d := by
    intro i _
    exact mul_nonneg (hwpos i).le (hnonneg i)
  have hall := (Finset.sum_eq_zero_iff_of_nonneg hterms).mp hsum
  intro i
  exact (mul_eq_zero.mp (hall i (Finset.mem_univ i))).resolve_left (ne_of_gt (hwpos i))

lemma orthogonal_span {ι : Type*}
    (B : Form E) (v : ι → E) (p d : E)
    (hzero : ∀ i, B (p - v i) d = 0) :
    ∀ u ∈ Submodule.span ℝ (Set.range (fun i => p - v i)), B u d = 0 := by
  intro u hu
  induction hu using Submodule.span_induction with
  | mem x hx =>
      obtain ⟨i, rfl⟩ := hx
      exact hzero i
  | zero => simp
  | add x y hx hy hxe hye => simp [map_add, hxe, hye]
  | smul a x hx hxe => simp [map_smul, hxe]

lemma common_limit_orthogonal {ι K : Type*} [Fintype ι]
    (Bs : K → Form E) (hsym : ∀ k x y, Bs k x y = Bs k y x)
    (v : ι → E) (w : ι → ℝ) (p h z : E)
    (hwpos : ∀ i, 0 < w i) (hwsum : ∑ i, w i = 1)
    (hcenter : ∑ i, w i • v i = p)
    (e : ℕ → ℝ) (r : ℕ → E)
    (hepos : ∀ n, 0 < e n) (he : Tendsto e atTop (𝓝 0))
    (hr : Tendsto r atTop (𝓝 z))
    (hgain : ∀ n k i, loss (Bs k) (p + e n • r n) (v i) ≤
      loss (Bs k) (p + e n • h) (v i)) :
    ∀ k u, u ∈ Submodule.span ℝ (Set.range (fun i => p - v i)) →
      Bs k (h - z) u = 0 := by
  intro k u hu
  have hn : ∀ i, 0 ≤ Bs k (p - v i) (h - z) := by
    intro i
    exact first_order_nonnegative (Bs k) (hsym k) p h (v i) z e r hepos he hr
      (fun n => hgain n k i)
  have hz := barycenter_nonnegative_vanish (Bs k) v w p (h - z) hwpos hwsum hcenter hn
  rw [hsym k (h - z) u]
  exact orthogonal_span (Bs k) v p (h - z) hz u hu



lemma weighted_first_order_sum {ι : Type*} [Fintype ι]
    (B : Form E) (v : ι → E) (w : ι → ℝ) (p d : E) (e D : ℝ)
    (hwsum : ∑ i, w i = 1) (hcenter : ∑ i, w i • v i = p) :
    (∑ i, w i * (2 * B (p - v i) d + e * D)) = e * D := by
  have hf := barycenter_form_sum B v w p d hwsum hcenter
  calc
    (∑ i, w i * (2 * B (p - v i) d + e * D)) =
        2 * (∑ i, w i * B (p - v i) d) + (∑ i, w i) * (e * D) := by
      simp only [Finset.mul_sum, Finset.sum_mul, ← Finset.sum_add_distrib]
      apply Finset.sum_congr rfl
      intro i _
      ring
    _ = e * D := by rw [hf, hwsum]; ring

lemma repair_energy_bound {ι : Type*} [Fintype ι]
    (B : Form E) (hsym : ∀ x y, B x y = B y x)
    (v : ι → E) (w : ι → ℝ) (p h r : E) (e : ℝ)
    (hwpos : ∀ i, 0 < w i) (hwsum : ∑ i, w i = 1)
    (hcenter : ∑ i, w i • v i = p) (he : 0 < e)
    (hgain : ∀ i, loss B (p + e • r) (v i) ≤ loss B (p + e • h) (v i)) :
    B r r ≤ B h h := by
  have hi : ∀ i, 0 ≤ 2 * B (p - v i) (h - r) + e * (B h h - B r r) := by
    intro i
    have hx := gain_expansion B hsym p h r (v i) e
    have hg := hgain i
    have hm : 0 ≤ e * (2 * B (p - v i) (h - r) + e * (B h h - B r r)) := by linarith
    exact (mul_nonneg_iff_of_pos_left he).mp hm
  have hsum : 0 ≤ ∑ i, w i *
      (2 * B (p - v i) (h - r) + e * (B h h - B r r)) := by
    apply Finset.sum_nonneg
    intro i _
    exact mul_nonneg (hwpos i).le (hi i)
  rw [weighted_first_order_sum B v w p (h - r) e (B h h - B r r) hwsum hcenter] at hsum
  have hd := (mul_nonneg_iff_of_pos_left he).mp hsum
  linarith

/-- The full compactness/first-order necessity spine, with coercivity explicit.
All affine-coherent repairs are covered, hence in particular convex-hull repairs.
No convergence of the normalized repairs is assumed: it is extracted here. -/
theorem common_repair_necessary [FiniteDimensional ℝ E]
    {ι K : Type*} [Fintype ι]
    (Bs : K → Form E) (k0 : K)
    (hsym : ∀ k x y, Bs k x y = Bs k y x)
    (hcoercive : IsCoercive (Bs k0))
    (v : ι → E) (w : ι → ℝ) (p h : E)
    (hwpos : ∀ i, 0 < w i) (hwsum : ∑ i, w i = 1)
    (hcenter : ∑ i, w i • v i = p)
    (e : ℕ → ℝ) (r : ℕ → E)
    (hepos : ∀ n, 0 < e n) (he : Tendsto e atTop (𝓝 0))
    (hrmem : ∀ n, r n ∈ Submodule.span ℝ (Set.range (fun i => p - v i)))
    (hgain : ∀ n k i, loss (Bs k) (p + e n • r n) (v i) ≤
      loss (Bs k) (p + e n • h) (v i)) :
    ∃ z ∈ Submodule.span ℝ (Set.range (fun i => p - v i)),
      ∀ k u, u ∈ Submodule.span ℝ (Set.range (fun i => p - v i)) →
        Bs k (h - z) u = 0 := by
  obtain ⟨m, hm, hco⟩ := hcoercive
  let R : ℝ := Bs k0 h h / m + 1
  have hrbound : ∀ n, ‖r n‖ ≤ R := by
    intro n
    have hegy := repair_energy_bound (Bs k0) (hsym k0) v w p h (r n) (e n)
      hwpos hwsum hcenter (hepos n) (fun i => hgain n k0 i)
    have hc := hco (r n)
    have hsq : ‖r n‖ ^ 2 ≤ Bs k0 h h / m := by
      apply (le_div_iff₀ hm).mpr
      nlinarith
    dsimp [R]
    nlinarith [sq_nonneg (‖r n‖ - (1 : ℝ) / 2)]
  have hrball : ∀ n, r n ∈ Metric.closedBall (0 : E) R := by
    intro n
    simpa only [Metric.mem_closedBall, dist_zero_right] using hrbound n
  obtain ⟨z, hzball, phi, hphi, hzlim⟩ := (isCompact_closedBall (0 : E) R).tendsto_subseq hrball
  let T : Submodule ℝ E := Submodule.span ℝ (Set.range (fun i => p - v i))
  have hzmem : z ∈ T := by
    exact (Submodule.closed_of_finiteDimensional T).mem_of_tendsto hzlim
      (Filter.Eventually.of_forall (fun n => hrmem (phi n)))
  refine ⟨z, hzmem, ?_⟩
  apply common_limit_orthogonal Bs hsym v w p h z hwpos hwsum hcenter
    (e ∘ phi) (r ∘ phi) (fun n => hepos (phi n))
    (he.comp hphi.tendsto_atTop) hzlim
  intro n k i
  exact hgain (phi n) k i



lemma positive_definite_coercive [FiniteDimensional ℝ E]
    (B : Form E) (hpos : ∀ u : E, u ≠ 0 → 0 < B u u) : IsCoercive B := by
  have hspos : ∀ u ∈ Metric.sphere (0 : E) 1, 0 < B u u := by
    intro u hu
    have hn : ‖u‖ = 1 := by simpa only [Metric.mem_sphere, dist_zero_right] using hu
    apply hpos u
    intro hzero
    simp [hzero] at hn
  obtain ⟨m, hm, hmin⟩ := (isCompact_sphere (0 : E) 1).exists_forall_le'
    (continuous_diag B).continuousOn hspos
  refine ⟨m, hm, ?_⟩
  intro u
  by_cases hu : u = 0
  · simp [hu]
  have hnu : 0 < ‖u‖ := norm_pos_iff.mpr hu
  have hunorm : ‖‖u‖⁻¹ • u‖ = 1 := by
    rw [norm_smul, Real.norm_eq_abs, abs_inv, abs_of_pos hnu, inv_mul_cancel₀ (ne_of_gt hnu)]
  have huunit : ‖u‖⁻¹ • u ∈ Metric.sphere (0 : E) 1 := by
    simpa only [Metric.mem_sphere, dist_zero_right] using hunorm
  have hbound := hmin (‖u‖⁻¹ • u) huunit
  calc
    m * ‖u‖ * ‖u‖ = m * (‖u‖ * ‖u‖) := by ring
    _ ≤ B (‖u‖⁻¹ • u) (‖u‖⁻¹ • u) * (‖u‖ * ‖u‖) :=
      mul_le_mul_of_nonneg_right hbound (mul_nonneg (norm_nonneg u) (norm_nonneg u))
    _ = B u u := by
      simp only [map_smul, ContinuousLinearMap.smul_apply, smul_eq_mul]
      field_simp

/-- Positive barycentric truth weights provide every small tangent repair ray
inside the original convex hull, with no separate radial-accessibility axiom. -/
lemma tangent_ray_in_convexHull {ι : Type*} [Fintype ι]
    (v : ι → E) (w : ι → ℝ) (p z : E)
    (hwpos : ∀ i, 0 < w i) (hwsum : ∑ i, w i = 1)
    (hcenter : ∑ i, w i • v i = p)
    (hz : z ∈ Submodule.span ℝ (Set.range (fun i => p - v i))) :
    ∃ delta > 0, ∀ e : ℝ, 0 < e → e < delta →
      p + e • z ∈ convexHull ℝ (Set.range v) := by
  obtain ⟨a, ha⟩ := (Submodule.mem_span_range_iff_exists_fun ℝ).mp hz
  let A : ℝ := ∑ i, a i
  let mu : ℝ → ι → ℝ := fun e i => (1 + e * A) * w i - e * a i
  have hapos : ∀ i, ∀ᶠ e in 𝓝 (0 : ℝ), 0 < mu e i := by
    intro i
    have hc : Continuous (fun e : ℝ => mu e i) := by dsimp [mu]; fun_prop
    have ht : Tendsto (fun e : ℝ => mu e i) (𝓝 0) (𝓝 (w i)) := by
      simpa [mu] using hc.tendsto 0
    exact ht (Ioi_mem_nhds (hwpos i))
  have hall : ∀ᶠ e in 𝓝 (0 : ℝ), ∀ i, 0 < mu e i := by
    exact Filter.eventually_all.mpr hapos
  obtain ⟨delta, hdelta, hball⟩ := Metric.mem_nhds_iff.mp hall
  refine ⟨delta, hdelta, ?_⟩
  intro e he hed
  have hweights : ∀ i, 0 ≤ mu e i := by
    have hmem : e ∈ Metric.ball (0 : ℝ) delta := by
      simpa only [Metric.mem_ball, Real.dist_eq, sub_zero, abs_of_pos he] using hed
    exact fun i => (hball hmem i).le
  have hm_sum : ∑ i, mu e i = 1 := by
    dsimp [mu]
    rw [Finset.sum_sub_distrib, ← Finset.mul_sum, ← Finset.mul_sum, hwsum]
    dsimp [A]
    ring
  have hav : ∑ i, a i • v i = A • p - z := by
    have ha' : A • p - ∑ i, a i • v i = z := by
      simpa only [smul_sub, Finset.sum_sub_distrib, ← Finset.sum_smul] using ha
    rw [← ha']
    abel
  have hm_center : ∑ i, mu e i • v i = p + e • z := by
    dsimp [mu]
    simp_rw [sub_smul, mul_smul]
    rw [Finset.sum_sub_distrib, ← Finset.smul_sum, ← Finset.smul_sum, hcenter, hav]
    module
  exact mem_convexHull_of_exists_fintype (mu e) v hweights hm_sum
    (fun i => Set.mem_range_self i) hm_center



lemma convexHull_sub_mem {ι : Type*} (v : ι → E) (p x : E)
    (hx : x ∈ convexHull ℝ (Set.range v)) :
    x - p ∈ Submodule.span ℝ (Set.range (fun i => p - v i)) := by
  let T : Submodule ℝ E := Submodule.span ℝ (Set.range (fun i => p - v i))
  have hsub : Set.range v ⊆ {x : E | x - p ∈ T} := by
    intro x hx
    obtain ⟨i, rfl⟩ := hx
    have hi : p - v i ∈ T := Submodule.subset_span (Set.mem_range_self i)
    have hn := T.neg_mem hi
    simpa only [neg_sub] using hn
  have hconv : Convex ℝ {x : E | x - p ∈ T} := by
    intro x hx y hy a b _ _ hab
    have hm := T.add_mem (T.smul_mem a hx) (T.smul_mem b hy)
    change a • x + b • y - p ∈ T
    have heq : a • x + b • y - p = a • (x - p) + b • (y - p) := by
      have hb : b = 1 - a := by linarith
      rw [hb]
      module
    rw [heq]
    exact hm
  exact convexHull_min hsub hconv hx

lemma normal_gain_identity (B : Form E) (hsym : ∀ x y, B x y = B y x)
    (h z : E) (horth : B (h - z) z = 0) :
    B h h - B z z = B (h - z) (h - z) := by
  simp only [map_sub, ContinuousLinearMap.sub_apply] at horth ⊢
  rw [hsym z h]
  linarith

/-- A simultaneous metric-normal tangent direction gives one strict repair ray. -/
theorem common_repair_sufficient {ι K : Type*} [Fintype ι]
    (Bs : K → Form E) (hsym : ∀ k x y, Bs k x y = Bs k y x)
    (hpos : ∀ k u, u ≠ 0 → 0 < Bs k u u)
    (v : ι → E) (w : ι → ℝ) (p h z : E)
    (hwpos : ∀ i, 0 < w i) (hwsum : ∑ i, w i = 1)
    (hcenter : ∑ i, w i • v i = p)
    (htrans : h ∉ Submodule.span ℝ (Set.range (fun i => p - v i)))
    (hz : z ∈ Submodule.span ℝ (Set.range (fun i => p - v i)))
    (horth : ∀ k u, u ∈ Submodule.span ℝ (Set.range (fun i => p - v i)) →
      Bs k (h - z) u = 0) :
    ∃ delta > 0, ∀ e : ℝ, 0 < e → e < delta →
      p + e • z ∈ convexHull ℝ (Set.range v) ∧
      ∀ k i, loss (Bs k) (p + e • z) (v i) < loss (Bs k) (p + e • h) (v i) := by
  obtain ⟨delta, hdelta, hmem⟩ := tangent_ray_in_convexHull v w p z hwpos hwsum hcenter hz
  refine ⟨delta, hdelta, ?_⟩
  intro e he hed
  refine ⟨hmem e he hed, ?_⟩
  intro k i
  have hres : h - z ≠ 0 := by
    intro hzero
    have hh : h = z := sub_eq_zero.mp hzero
    exact htrans (hh ▸ hz)
  have hpositive := hpos k (h - z) hres
  have hv := horth k (p - v i) (Submodule.subset_span (Set.mem_range_self i))
  have hv' : Bs k (p - v i) (h - z) = 0 := by rw [hsym k]; exact hv
  have hz' := horth k z hz
  have hidentity := normal_gain_identity (Bs k) (hsym k) h z hz'
  have hg := gain_expansion (Bs k) (hsym k) p h z (v i) e
  rw [hv', hidentity] at hg
  have hp : 0 < e * (e * Bs k (h - z) (h - z)) := mul_pos he (mul_pos he hpositive)
  nlinarith

/-- Convex-hull and positive-definite wrapper for the compactness necessity theorem. -/
theorem convex_common_repair_necessary [FiniteDimensional ℝ E]
    {ι K : Type*} [Fintype ι]
    (Bs : K → Form E) (k0 : K)
    (hsym : ∀ k x y, Bs k x y = Bs k y x)
    (hpos : ∀ k u, u ≠ 0 → 0 < Bs k u u)
    (v : ι → E) (w : ι → ℝ) (p h : E)
    (hwpos : ∀ i, 0 < w i) (hwsum : ∑ i, w i = 1)
    (hcenter : ∑ i, w i • v i = p)
    (e : ℕ → ℝ) (c : ℕ → E)
    (hepos : ∀ n, 0 < e n) (he : Tendsto e atTop (𝓝 0))
    (hcmem : ∀ n, c n ∈ convexHull ℝ (Set.range v))
    (hgain : ∀ n k i, loss (Bs k) (c n) (v i) ≤ loss (Bs k) (p + e n • h) (v i)) :
    ∃ z ∈ Submodule.span ℝ (Set.range (fun i => p - v i)),
      ∀ k u, u ∈ Submodule.span ℝ (Set.range (fun i => p - v i)) →
        Bs k (h - z) u = 0 := by
  let r : ℕ → E := fun n => (e n)⁻¹ • (c n - p)
  have hre : ∀ n, p + e n • r n = c n := by
    intro n
    dsimp [r]
    rw [smul_smul, mul_inv_cancel₀ (ne_of_gt (hepos n)), one_smul]
    abel
  have hrmem : ∀ n, r n ∈ Submodule.span ℝ (Set.range (fun i => p - v i)) := by
    intro n
    exact Submodule.smul_mem _ ((e n)⁻¹) (convexHull_sub_mem v p (c n) (hcmem n))
  apply common_repair_necessary Bs k0 hsym (positive_definite_coercive (Bs k0) (hpos k0))
    v w p h hwpos hwsum hcenter e r hepos he hrmem
  intro n k i
  rw [hre]
  exact hgain n k i



/-- General quadratic local common-repair equivalence in positive-barycentric
form. The right side is the basis-free simultaneous orthogonal-projection
condition; all ordinary positive-definite matrix families are instances. -/
theorem local_common_repair_iff [FiniteDimensional ℝ E]
    {ι K : Type*} [Fintype ι]
    (Bs : K → Form E) (k0 : K)
    (hsym : ∀ k x y, Bs k x y = Bs k y x)
    (hpos : ∀ k u, u ≠ 0 → 0 < Bs k u u)
    (v : ι → E) (w : ι → ℝ) (p h : E)
    (hwpos : ∀ i, 0 < w i) (hwsum : ∑ i, w i = 1)
    (hcenter : ∑ i, w i • v i = p)
    (htrans : h ∉ Submodule.span ℝ (Set.range (fun i => p - v i))) :
    (∃ (e : ℕ → ℝ) (c : ℕ → E),
      (∀ n, 0 < e n) ∧ Tendsto e atTop (𝓝 0) ∧
      (∀ n, c n ∈ convexHull ℝ (Set.range v)) ∧
      (∀ n k i, loss (Bs k) (c n) (v i) ≤ loss (Bs k) (p + e n • h) (v i))) ↔
    (∃ z ∈ Submodule.span ℝ (Set.range (fun i => p - v i)),
      ∀ k u, u ∈ Submodule.span ℝ (Set.range (fun i => p - v i)) →
        Bs k (h - z) u = 0) := by
  constructor
  · rintro ⟨e, c, hepos, helim, hcmem, hgain⟩
    exact convex_common_repair_necessary Bs k0 hsym hpos v w p h hwpos hwsum
      hcenter e c hepos helim hcmem hgain
  · rintro ⟨z, hz, horth⟩
    obtain ⟨delta, hdelta, hrepair⟩ := common_repair_sufficient Bs hsym hpos v w p h z
      hwpos hwsum hcenter htrans hz horth
    let e : ℕ → ℝ := fun n => (delta / 2) * (1 / ((n : ℝ) + 1))
    let c : ℕ → E := fun n => p + e n • z
    have hepos : ∀ n, 0 < e n := by
      intro n
      dsimp [e]
      positivity
    have helim : Tendsto e atTop (𝓝 0) := by
      simpa [e] using tendsto_const_nhds.mul tendsto_one_div_add_atTop_nhds_zero_nat
    have hesmall : ∀ n, e n < delta := by
      intro n
      have hn : 0 ≤ (n : ℝ) := Nat.cast_nonneg n
      have hfrac : 1 / ((n : ℝ) + 1) ≤ 1 := by
        apply (div_le_iff₀ (by positivity : 0 < (n : ℝ) + 1)).mpr
        linarith
      have hm := mul_le_mul_of_nonneg_left hfrac (by positivity : 0 ≤ delta / 2)
      dsimp [e]
      nlinarith
    refine ⟨e, c, hepos, helim, ?_, ?_⟩
    · intro n
      exact (hrepair (e n) (hepos n) (hesmall n)).1
    · intro n k i
      exact ((hrepair (e n) (hepos n) (hesmall n)).2 k i).le

lemma simultaneous_normal_unique {ι : Type*}
    (B : Form E) (hpos : ∀ u, u ≠ 0 → 0 < B u u)
    (v : ι → E) (p h z z' : E)
    (hz : z ∈ Submodule.span ℝ (Set.range (fun i => p - v i)))
    (hz' : z' ∈ Submodule.span ℝ (Set.range (fun i => p - v i)))
    (hn : ∀ u ∈ Submodule.span ℝ (Set.range (fun i => p - v i)), B (h - z) u = 0)
    (hn' : ∀ u ∈ Submodule.span ℝ (Set.range (fun i => p - v i)), B (h - z') u = 0) :
    z = z' := by
  by_contra hne
  have hd : z - z' ≠ 0 := sub_ne_zero.mpr hne
  have hdmem := Submodule.sub_mem _ hz hz'
  have hfirst := hn (z - z') hdmem
  have hsecond := hn' (z - z') hdmem
  have hpositive := hpos (z - z') hd
  simp only [map_sub, ContinuousLinearMap.sub_apply] at hfirst hsecond hpositive
  linarith

#print axioms local_common_repair_iff
#print axioms simultaneous_normal_unique
#check local_common_repair_iff
end LocalRigidity
