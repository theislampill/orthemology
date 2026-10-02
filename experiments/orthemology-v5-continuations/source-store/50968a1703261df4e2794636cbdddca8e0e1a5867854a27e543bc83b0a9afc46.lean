import SmoothRobustness

/-! A precise comparison with the common-infinitesimal-improvement literature.
A nudge is a strict directional decrease of the actual Bregman state losses,
not a coherent endpoint. Fixed additive generators and >=3 categorical truth
states make universal local nudging equivalent to the common-repair class.
-/
noncomputable section
open scoped Topology BigOperators
open Filter Set SmoothRigidity GeneratorRigidity

namespace NudgeRigidity
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

lemma hessian_loss_direction_tendsto (s : ι → SmoothScalar.Score) (p : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1) (b d : ℕ → Vec ι) (z : Vec ι)
    (hb : Tendsto b atTop (𝓝 p)) (hd : Tendsto d atTop (𝓝 z)) (i : ι) :
    Tendsto (fun n => hessian s (b n) (b n - vertex i) (d n)) atTop
      (𝓝 (hessian s p (p - vertex i) z)) := by
  simp only [hessian_apply]
  apply tendsto_finset_sum
  intro j _
  have hdd : Tendsto (fun n => (s j).ddf (b n j)) atTop (𝓝 ((s j).ddf (p j))) := by
    exact ((s j).cont_second.continuousAt (Ioo_mem_nhds (hp j).1 (hp j).2)).tendsto.comp
      ((tendsto_pi_nhds.mp hb) j)
  exact (hdd.mul (((tendsto_pi_nhds.mp hb) j).sub tendsto_const_nhds)).mul
    ((tendsto_pi_nhds.mp hd) j)

/-- Common strict directional descent at forecasts converging to p forces
one nonzero shared Hessian-normal direction. No normalization is assumed. -/
theorem local_nudges_hessians_proportional (s t : ι → SmoothScalar.Score) (i0 : ι)
    (p : Vec ι) (hp : ∀ i, p i ∈ Ioo 0 1) (hsum : ∑ i, p i = 1)
    (b d : ℕ → Vec ι) (hb : Tendsto b atTop (𝓝 p))
    (hs : ∀ n i, hessian s (b n) (b n - vertex i) (d n) < 0)
    (ht : ∀ n i, hessian t (b n) (b n - vertex i) (d n) < 0) :
    ∃ a > 0, ∀ i, (s i).ddf (p i) = a * (t i).ddf (p i) := by
  have hdne : ∀ n, d n ≠ 0 := by
    intro n hn
    have hh := hs n i0
    simp [hn] at hh
  let r : ℕ → Vec ι := fun n => ‖d n‖⁻¹ • d n
  have hrnorm : ∀ n, ‖r n‖ = 1 := by
    intro n
    dsimp [r]
    rw [norm_smul, Real.norm_eq_abs, abs_inv, abs_of_pos (norm_pos_iff.mpr (hdne n)),
      inv_mul_cancel₀ (norm_ne_zero_iff.mpr (hdne n))]
  have hrball : ∀ n, r n ∈ Metric.closedBall (0 : Vec ι) 1 := by
    intro n
    simp only [Metric.mem_closedBall, dist_zero_right, hrnorm, le_refl]
  obtain ⟨z, hzball, phi, hphi, hzlim⟩ := (isCompact_closedBall (0 : Vec ι) 1).tendsto_subseq hrball
  have hznorm : ‖z‖ = 1 := by
    have hh := hzlim.norm
    have hc : Tendsto (fun n => ‖r (phi n)‖) atTop (𝓝 (1 : ℝ)) := by
      simpa only [hrnorm] using (tendsto_const_nhds : Tendsto (fun _ : ℕ => (1 : ℝ)) atTop (𝓝 1))
    exact tendsto_nhds_unique hh hc
  have hzne : z ≠ 0 := by intro hh; simp [hh] at hznorm
  have hnormal : ∀ a : ι → SmoothScalar.Score,
      (∀ n i, hessian a (b n) (b n - vertex i) (d n) < 0) →
      ∀ i, hessian a p (p - vertex i) z = 0 := by
    intro a hagain
    have hn : ∀ i, 0 ≤ hessian a p (p - vertex i) (-z) := by
      intro i
      have hlim := hessian_loss_direction_tendsto a p hp (b ∘ phi) (r ∘ phi) z
        (hb.comp hphi.tendsto_atTop) hzlim i
      have hevent : ∀ᶠ n in atTop, hessian a (b (phi n)) (b (phi n) - vertex i) (r (phi n)) ≤ 0 := by
        apply Filter.Eventually.of_forall
        intro n
        dsimp [r]
        rw [map_smul, smul_eq_mul]
        exact (mul_neg_of_pos_of_neg (inv_pos.mpr (norm_pos_iff.mpr (hdne (phi n)))) (hagain (phi n) i)).le
      have hh := le_of_tendsto hlim hevent
      simpa only [map_neg, neg_nonneg] using hh
    have hz := LocalRigidity.barycenter_nonnegative_vanish (hessian a p) vertex p p (-z)
      (fun i => (hp i).1) hsum (vertex_barycenter p) hn
    intro i
    have hh := hz i
    simpa only [map_neg, neg_eq_zero] using hh
  have hsn := hnormal s hs
  have htn := hnormal t ht
  apply positive_normal_proportional (fun i => (s i).ddf (p i))
    (fun i => (t i).ddf (p i)) z (fun i => (s i).positive (p i) (hp i))
    (fun i => (t i).positive (p i) (hp i)) hzne
  · intro i j
    have hh := LocalRigidity.orthogonal_span (hessian s p) vertex p z hsn
      (vertex i - vertex j) (vertex_difference_tangent p i j)
    rw [hessian_symmetric, map_sub, hessian_vertex, hessian_vertex] at hh
    exact sub_eq_zero.mp hh
  · intro i j
    have hh := LocalRigidity.orthogonal_span (hessian t p) vertex p z htn
      (vertex i - vertex j) (vertex_difference_tangent p i j)
    rw [hessian_symmetric, map_sub, hessian_vertex, hessian_vertex] at hh
    exact sub_eq_zero.mp hh


def CommonLocalNudges (s t : ι → SmoothScalar.Score) (i0 : ι) : Prop :=
  ∀ p : Vec ι, (∀ i, p i ∈ Ioo 0 1) → (∑ i, p i = 1) →
    ∃ (e : ℕ → ℝ) (d : ℕ → Vec ι),
      (∀ n, 0 < e n) ∧ Tendsto e atTop (𝓝 0) ∧
      (∀ n i, (p + e n • vertex i0) i ∈ Ioo 0 1) ∧
      (∀ n i, hessian s (p + e n • vertex i0) (p + e n • vertex i0 - vertex i) (d n) < 0) ∧
      (∀ n i, hessian t (p + e n • vertex i0) (p + e n • vertex i0 - vertex i) (d n) < 0)

/-- These are the actual derivatives of the scored state losses. -/
lemma nudge_derivative_is_actual (s : ι → SmoothScalar.Score) (b : Vec ι)
    (hb : ∀ i, b i ∈ Ioo 0 1) (i : ι) :
    HasFDerivAt (totalDiv s (vertex i)) (hessian s b (b - vertex i)) b :=
  score_hasFDerivAt s (vertex i) b hb

theorem universal_local_nudges_force_affine
    (hcard : 3 ≤ Fintype.card ι) (s t : ι → SmoothScalar.Score) (i0 : ι)
    (hcommon : CommonLocalNudges s t i0) :
    BregmanProjection.PositiveAffineEquivalent s t := by
  let r : ι → ℝ → ℝ := fun i x => (s i).ddf x / (t i).ddf x
  have hcompat : ∀ p : Vec ι, (∀ i, p i ∈ Ioo 0 1) → (∑ i, p i = 1) →
      ∀ i j, r i (p i) = r j (p j) := by
    intro p hp hsum i j
    obtain ⟨e, d, hepos, helim, hbint, hs, ht⟩ := hcommon p hp hsum
    have hb : Tendsto (fun n => p + e n • vertex i0) atTop (𝓝 p) := by
      simpa using
        (tendsto_const_nhds : Tendsto (fun _ : ℕ => p) atTop (𝓝 p)).add
          (helim.smul (tendsto_const_nhds : Tendsto (fun _ : ℕ => vertex i0) atTop (𝓝 (vertex i0))))
    obtain ⟨a, ha, haa⟩ := local_nudges_hessians_proportional s t i0 p hp hsum
      (fun n => p + e n • vertex i0) d hb hs ht
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

lemma affine_second_derivative (s t : SmoothScalar.Score) (a b d x : ℝ)
    (hx : x ∈ Ioo 0 1)
    (hf : ∀ y ∈ Icc 0 1, s.f y = a * t.f y + b * y + d) :
    s.ddf x = a * t.ddf x := by
  have heq : s.df =ᶠ[𝓝 x] (fun y => a * t.df y + b) := by
    filter_upwards [Ioo_mem_nhds hx.1 hx.2] with y hy
    exact BregmanProjection.affine_gradient_coordinate s t a b d y hy hf
  exact (s.second x hx).unique ((((t.second x hx).const_mul a).add_const b).congr_of_eventuallyEq heq)

/-- A closed-form strict descent direction at every incoherent interior input.
It need not itself land on the simplex; it supplies an infinitesimal nudge. -/
lemma canonical_nudge_gain (s : ι → SmoothScalar.Score) (b : Vec ι)
    (hb : ∀ i, b i ∈ Ioo 0 1) (j : ι) :
    hessian s b (b - vertex j) (fun i => (1 - ∑ k, b k) / (s i).ddf (b i)) =
      -(∑ k, b k - 1) ^ 2 := by
  rw [hessian_apply]
  have hh : ∀ i, (s i).ddf (b i) * (b - vertex j) i *
      ((1 - ∑ k, b k) / (s i).ddf (b i)) =
      (1 - ∑ k, b k) * (b - vertex j) i := by
    intro i
    field_simp [ne_of_gt ((s i).positive (b i) (hb i))]
    ring
  simp_rw [hh]
  rw [← Finset.mul_sum]
  simp only [Pi.sub_apply, Finset.sum_sub_distrib, vertex_sum]
  ring

lemma affine_hessian_direction (s t : ι → SmoothScalar.Score) (a : ℝ) (b d : ι → ℝ)
    (hf : ∀ i x, x ∈ Icc 0 1 → (s i).f x = a * (t i).f x + b i * x + d i)
    (x u z : Vec ι) (hx : ∀ i, x i ∈ Ioo 0 1) :
    hessian s x u z = a * hessian t x u z := by
  rw [hessian_apply, hessian_apply, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i _
  rw [affine_second_derivative (s i) (t i) a (b i) (d i) (x i) (hx i) (hf i)]
  ring

theorem universal_local_nudge_iff_affine (hcard : 3 ≤ Fintype.card ι)
    (s t : ι → SmoothScalar.Score) (i0 : ι) :
    CommonLocalNudges s t i0 ↔ BregmanProjection.PositiveAffineEquivalent s t := by
  constructor
  · exact universal_local_nudges_force_affine hcard s t i0
  · rintro ⟨a, ha, f, g, hfg⟩
    intro p hp hpsum
    obtain ⟨e, c, hepos, helim, hbint, hcint, hcsum, ht⟩ :=
      BregmanProjection.single_score_local_repairs t p (vertex i0) hp hpsum
    let base : ℕ → Vec ι := fun n => p + e n • vertex i0
    let d : ℕ → Vec ι := fun n i => (1 - ∑ k, base n k) / (t i).ddf (base n i)
    have hsum : ∀ n, ∑ k, base n k = 1 + e n := by
      intro n
      simp only [base, Pi.add_apply, Pi.smul_apply, smul_eq_mul,
        Finset.sum_add_distrib, ← Finset.mul_sum, hpsum, vertex_sum, mul_one]
    have htneg : ∀ n i, hessian t (base n) (base n - vertex i) (d n) < 0 := by
      intro n i
      rw [show d n = (fun j => (1 - ∑ k, base n k) / (t j).ddf (base n j)) from rfl,
        canonical_nudge_gain t (base n) (hbint n), hsum]
      have hh := sq_pos_of_pos (hepos n)
      nlinarith
    refine ⟨e, d, hepos, helim, hbint, ?_, htneg⟩
    intro n i
    rw [affine_hessian_direction s t a f g hfg _ _ _ (hbint n)]
    exact mul_neg_of_pos_of_neg ha (htneg n i)

/-- The exact relation between coherent endpoint repair and local nudging.
The equivalence is universal across contexts, not pointwise at one forecast. -/
theorem universal_local_nudge_iff_common_repair (hcard : 3 ≤ Fintype.card ι)
    (s t : ι → SmoothScalar.Score) (i0 : ι) :
    CommonLocalNudges s t i0 ↔ BregmanProjection.CommonLocalRepairs s t i0 :=
  (universal_local_nudge_iff_affine hcard s t i0).trans
    (BregmanProjection.universal_common_repair_iff_affine hcard s t i0).symm

#check nudge_derivative_is_actual
#check canonical_nudge_gain
#print axioms local_nudges_hessians_proportional
#print axioms canonical_nudge_gain
#print CommonLocalNudges
#print axioms universal_local_nudge_iff_affine
#print axioms universal_local_nudge_iff_common_repair
#check universal_local_nudge_iff_affine
#check universal_local_nudge_iff_common_repair
end NudgeRigidity

