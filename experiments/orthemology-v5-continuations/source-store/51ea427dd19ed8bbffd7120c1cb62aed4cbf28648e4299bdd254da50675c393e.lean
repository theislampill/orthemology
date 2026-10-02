import GeneratorRigidity

noncomputable section
open scoped Topology BigOperators
open Set Filter SmoothRigidity

namespace BregmanProjection

lemma score_strictConvex (s : SmoothScalar.Score) : StrictConvexOn ℝ (Icc 0 1) s.f := by
  apply strictConvexOn_of_deriv2_pos (convex_Icc 0 1) s.cont
  intro x hx
  have hx' : x ∈ Ioo 0 1 := by simpa only [interior_Icc] using hx
  have heq : deriv s.f =ᶠ[𝓝 x] s.df := by
    filter_upwards [Ioo_mem_nhds hx'.1 hx'.2] with y hy
    exact (s.deriv y hy).deriv
  have hdd := ((s.second x hx').congr_of_eventuallyEq heq).deriv
  change 0 < deriv (deriv s.f) x
  rw [hdd]
  exact s.positive x hx'

lemma boundary_divergence_pos (s : SmoothScalar.Score) (v p : ℝ)
    (hv : v ∈ Icc 0 1) (hp : p ∈ Ioo 0 1) (hne : v ≠ p) :
    0 < SmoothScalar.divergence s v p := by
  have hp' : p ∈ Icc 0 1 := ⟨hp.1.le, hp.2.le⟩
  rcases lt_or_gt_of_ne hne with hvp | hpv
  · have hh := (score_strictConvex s).slope_lt_of_hasDerivAt hv hp' hvp (s.deriv p hp)
    rw [slope_def_field] at hh
    have hm := (div_lt_iff₀ (sub_pos.mpr hvp)).mp hh
    dsimp [SmoothScalar.divergence]
    nlinarith
  · have hh := (score_strictConvex s).lt_slope_of_hasDerivAt hp' hv hpv (s.deriv p hp)
    rw [slope_def_field] at hh
    have hm := (lt_div_iff₀ (sub_pos.mpr hpv)).mp hh
    dsimp [SmoothScalar.divergence]
    nlinarith

lemma boundary_divergence_nonneg (s : SmoothScalar.Score) (v p : ℝ)
    (hv : v ∈ Icc 0 1) (hp : p ∈ Ioo 0 1) : 0 ≤ SmoothScalar.divergence s v p := by
  by_cases h : v = p
  · simp [h]
  · exact (boundary_divergence_pos s v p hv hp h).le

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

lemma potential_hasFDerivAt (s : ι → SmoothScalar.Score) (p : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1) : HasFDerivAt (potential s) (SmoothRigidity.gradient s p) p := by
  have hj : ∀ i, HasFDerivAt (fun x : Vec ι => (s i).f (x i))
      ((s i).df (p i) • (ContinuousLinearMap.proj i : Vec ι →L[ℝ] ℝ)) p := by
    intro i
    exact ((s i).deriv (p i) (hp i)).comp_hasFDerivAt p
      (ContinuousLinearMap.proj i : Vec ι →L[ℝ] ℝ).hasFDerivAt
  simpa only [potential, SmoothRigidity.gradient] using HasFDerivAt.sum (u := Finset.univ) (fun i _ => hj i)

lemma potential_continuousOn (s : ι → SmoothScalar.Score) :
    ContinuousOn (potential s) (stdSimplex ℝ ι) := by
  apply continuousOn_finset_sum
  intro i _
  exact (s i).cont.comp (continuous_apply i).continuousOn
    (fun x hx => mem_Icc_of_mem_stdSimplex hx i)

lemma gradient_continuousAt (s : ι → SmoothScalar.Score) (p : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1) : ContinuousAt (SmoothRigidity.gradient s) p := by
  unfold ContinuousAt SmoothRigidity.gradient
  apply tendsto_finset_sum
  intro i _
  have hcoord : Tendsto (fun x : Vec ι => x i) (𝓝 p) (𝓝 (p i)) := (continuous_apply i).tendsto p
  exact (((s i).second (p i) (hp i)).continuousAt.tendsto.comp hcoord).smul tendsto_const_nhds

lemma totalDiv_continuousOn_first (s : ι → SmoothScalar.Score) (b : Vec ι) :
    ContinuousOn (fun c => totalDiv s c b) (stdSimplex ℝ ι) := by
  have hlin : Continuous (fun c : Vec ι => SmoothRigidity.gradient s b (c - b)) := by fun_prop
  exact ((potential_continuousOn s).sub continuousOn_const).sub hlin.continuousOn

lemma totalDiv_first_positive (s : ι → SmoothScalar.Score) (c p : Vec ι)
    (hc : c ∈ stdSimplex ℝ ι) (hp : ∀ i, p i ∈ Ioo 0 1) (hne : c ≠ p) :
    0 < totalDiv s c p := by
  rw [totalDiv_eq_sum]
  have hex : ∃ i, c i ≠ p i := by
    by_contra! hh
    exact hne (funext hh)
  obtain ⟨j, hj⟩ := hex
  apply Finset.sum_pos'
  · intro i _
    exact boundary_divergence_nonneg (s i) (c i) (p i) (mem_Icc_of_mem_stdSimplex hc i) (hp i)
  · exact ⟨j, Finset.mem_univ j,
      boundary_divergence_pos (s j) (c j) (p j) (mem_Icc_of_mem_stdSimplex hc j) (hp j) hj⟩

lemma exists_projection (s : ι → SmoothScalar.Score) (p b : Vec ι)
    (hp : p ∈ stdSimplex ℝ ι) :
    ∃ q ∈ stdSimplex ℝ ι, IsMinOn (fun c => totalDiv s c b) (stdSimplex ℝ ι) q :=
  (isCompact_stdSimplex ι).exists_isMinOn ⟨p, hp⟩ (totalDiv_continuousOn_first s b)



lemma totalDiv_joint_tendsto (s : ι → SmoothScalar.Score) (p q : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1) (hq : q ∈ stdSimplex ℝ ι)
    (b c : ℕ → Vec ι) (hb : Tendsto b atTop (𝓝 p)) (hc : Tendsto c atTop (𝓝 q))
    (hcmem : ∀ n, c n ∈ stdSimplex ℝ ι) :
    Tendsto (fun n => totalDiv s (c n) (b n)) atTop (𝓝 (totalDiv s q p)) := by
  have hwithin : Tendsto c atTop (𝓝[stdSimplex ℝ ι] q) :=
    tendsto_nhdsWithin_iff.mpr ⟨hc, Filter.Eventually.of_forall hcmem⟩
  have hpotc := ((potential_continuousOn s) q hq).tendsto.comp hwithin
  have hpotb := (potential_hasFDerivAt s p hp).continuousAt.tendsto.comp hb
  have hgrad := (gradient_continuousAt s p hp).tendsto.comp hb
  have heval : Continuous (fun x : (Vec ι →L[ℝ] ℝ) × Vec ι => x.1 x.2) := by fun_prop
  have hpair := hgrad.prodMk_nhds (hc.sub hb)
  have hlinear := (heval.tendsto (SmoothRigidity.gradient s p, q - p)).comp hpair
  simpa only [Function.comp_apply, totalDiv, bregman] using (hpotc.sub hpotb).sub hlinear

/-- Compact minimizers of the actual Bregman objective converge back to an
interior coherent p as the incoming forecast tends to p. -/
lemma projections_tendsto (s : ι → SmoothScalar.Score) (p : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1) (hpsum : ∑ i, p i = 1)
    (b q : ℕ → Vec ι) (hb : Tendsto b atTop (𝓝 p))
    (hq : ∀ n, q n ∈ stdSimplex ℝ ι)
    (hmin : ∀ n, IsMinOn (fun c => totalDiv s c (b n)) (stdSimplex ℝ ι) (q n)) :
    Tendsto q atTop (𝓝 p) := by
  have hpC : p ∈ stdSimplex ℝ ι := ⟨fun i => (hp i).1.le, hpsum⟩
  apply (isCompact_stdSimplex ι).tendsto_nhds_of_unique_mapClusterPt (Filter.Eventually.of_forall hq)
  intro x hx hcluster
  obtain ⟨phi, hphi, hqphi⟩ := TopologicalSpace.FirstCountableTopology.tendsto_subseq hcluster
  have hbphi := hb.comp hphi.tendsto_atTop
  have hleft := totalDiv_joint_tendsto s p x hp hx (b ∘ phi) (q ∘ phi) hbphi hqphi
    (fun n => hq (phi n))
  have hright : Tendsto (fun n => totalDiv s p (b (phi n))) atTop (𝓝 0) := by
    have ht := (score_hasFDerivAt s p p hp).continuousAt.tendsto.comp hbphi
    simpa [totalDiv, bregman, Function.comp_def] using ht
  have hle : totalDiv s x p ≤ 0 := le_of_tendsto_of_tendsto hleft hright
    (Filter.Eventually.of_forall (fun n => hmin (phi n) hpC))
  by_contra hne
  exact (not_le_of_gt (totalDiv_first_positive s x p hx hp hne)) hle

lemma tangent_path_in_simplex (q v : Vec ι)
    (hq : ∀ i, q i ∈ Ioo 0 1) (hqsum : ∑ i, q i = 1)
    (hv : v ∈ stdSimplex ℝ ι) :
    ∀ᶠ e : ℝ in 𝓝 0, q + e • (v - q) ∈ stdSimplex ℝ ι := by
  have hcoords : ∀ i, ∀ᶠ e : ℝ in 𝓝 0, 0 ≤ (q + e • (v - q)) i := by
    intro i
    have ht : Tendsto (fun e : ℝ => (q + e • (v - q)) i) (𝓝 0) (𝓝 (q i)) := by
      have hc : Continuous (fun e : ℝ => (q + e • (v - q)) i) := by fun_prop
      simpa using hc.tendsto 0
    exact (ht.eventually (eventually_gt_nhds (hq i).1)).mono (fun _ h => h.le)
  filter_upwards [Filter.eventually_all.mpr hcoords] with e he
  refine ⟨he, ?_⟩
  simp only [Pi.add_apply, Pi.smul_apply, Pi.sub_apply, smul_eq_mul,
    Finset.sum_add_distrib, ← Finset.mul_sum, Finset.sum_sub_distrib, hqsum, hv.2]
  ring

lemma projection_normal (s : ι → SmoothScalar.Score) (b q v : Vec ι)
    (hq : ∀ i, q i ∈ Ioo 0 1) (hqsum : ∑ i, q i = 1)
    (hv : v ∈ stdSimplex ℝ ι)
    (hmin : IsMinOn (fun c => totalDiv s c b) (stdSimplex ℝ ι) q) :
    (SmoothRigidity.gradient s q - SmoothRigidity.gradient s b) (v - q) = 0 := by
  have hd : HasFDerivAt (fun c => totalDiv s c b)
      (SmoothRigidity.gradient s q - SmoothRigidity.gradient s b) q := by
    have hh := ((potential_hasFDerivAt s q hq).sub_const (potential s b)).sub
      ((SmoothRigidity.gradient s b).hasFDerivAt.sub_const (SmoothRigidity.gradient s b b))
    simpa only [totalDiv, bregman, map_sub] using hh
  exact hmin.hasLineDerivAt_eq_zero (hd.hasLineDerivAt (v - q))
    (tangent_path_in_simplex q v hq hqsum hv)

lemma projection_weakly_repairs (s : ι → SmoothScalar.Score) (b q : Vec ι)
    (hb : ∀ i, b i ∈ Ioo 0 1) (hq : ∀ i, q i ∈ Ioo 0 1) (hqsum : ∑ i, q i = 1)
    (hmin : IsMinOn (fun c => totalDiv s c b) (stdSimplex ℝ ι) q) :
    ∀ i, totalDiv s (vertex i) q ≤ totalDiv s (vertex i) b := by
  intro i
  have hn := projection_normal s b q (vertex i) hq hqsum (single_mem_stdSimplex ℝ i) hmin
  have hg := bregman_gain (potential s) (SmoothRigidity.gradient s) q (vertex i) b q
  have hself : totalDiv s q q = 0 := by simp [totalDiv, bregman]
  change totalDiv s (vertex i) b - totalDiv s (vertex i) q =
    totalDiv s q b - totalDiv s q q + (SmoothRigidity.gradient s q - SmoothRigidity.gradient s b) (vertex i - q) at hg
  rw [hn, hself] at hg
  have hnonneg := totalDiv_nonneg s q b hq hb
  linarith



/-- Classical positive local repair, proved from compact Bregman projections.
The returned input and repair forecasts both stay in the interior cube. -/
theorem single_score_local_repairs (s : ι → SmoothScalar.Score) (p h : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1) (hpsum : ∑ i, p i = 1) :
    ∃ (e : ℕ → ℝ) (c : ℕ → Vec ι),
      (∀ n, 0 < e n) ∧ Tendsto e atTop (𝓝 0) ∧
      (∀ n i, (p + e n • h) i ∈ Ioo 0 1) ∧
      (∀ n i, c n i ∈ Ioo 0 1) ∧ (∀ n, ∑ i, c n i = 1) ∧
      (∀ n i, totalDiv s (vertex i) (c n) ≤ totalDiv s (vertex i) (p + e n • h)) := by
  let r : ℕ → ℝ := fun n => 1 / ((n : ℝ) + 1)
  let base : ℕ → Vec ι := fun n => p + r n • h
  have hr : Tendsto r atTop (𝓝 0) := tendsto_one_div_add_atTop_nhds_zero_nat
  have hbase : Tendsto base atTop (𝓝 p) := by
    simpa [base] using
      (tendsto_const_nhds : Tendsto (fun _ : ℕ => p) atTop (𝓝 p)).add
        (hr.smul (tendsto_const_nhds : Tendsto (fun _ : ℕ => h) atTop (𝓝 h)))
  have hpC : p ∈ stdSimplex ℝ ι := ⟨fun i => (hp i).1.le, hpsum⟩
  choose q hq hmin using fun n => exists_projection s p (base n) hpC
  have hqt := projections_tendsto s p hp hpsum base q hbase hq hmin
  have hbint : ∀ᶠ n in atTop, ∀ i, base n i ∈ Ioo 0 1 := by
    apply Filter.eventually_all.mpr
    intro i
    exact ((tendsto_pi_nhds.mp hbase) i).eventually (Ioo_mem_nhds (hp i).1 (hp i).2)
  have hqint : ∀ᶠ n in atTop, ∀ i, q n i ∈ Ioo 0 1 := by
    apply Filter.eventually_all.mpr
    intro i
    exact ((tendsto_pi_nhds.mp hqt) i).eventually (Ioo_mem_nhds (hp i).1 (hp i).2)
  obtain ⟨N, hN⟩ := Filter.eventually_atTop.mp (hbint.and hqint)
  refine ⟨(fun n => r (n + N)), (fun n => q (n + N)), ?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro n
    dsimp [r]
    positivity
  · exact (tendsto_add_atTop_iff_nat N).mpr hr
  · intro n i
    exact (hN (n + N) (Nat.le_add_left N n)).1 i
  · intro n i
    exact (hN (n + N) (Nat.le_add_left N n)).2 i
  · intro n
    exact (hq (n + N)).2
  · intro n i
    exact projection_weakly_repairs s (base (n + N)) (q (n + N))
      (hN (n + N) (Nat.le_add_left N n)).1 (hN (n + N) (Nat.le_add_left N n)).2
      (hq (n + N)).2 (hmin (n + N)) i

lemma affine_gradient_coordinate (s t : SmoothScalar.Score) (a b d x : ℝ)
    (hx : x ∈ Ioo 0 1)
    (hf : ∀ y ∈ Icc 0 1, s.f y = a * t.f y + b * y + d) :
    s.df x = a * t.df x + b := by
  have hr : HasDerivAt (fun y => a * t.f y + b * y + d) (a * t.df x + b) x := by
    simpa using (((t.deriv x hx).const_mul a).add ((hasDerivAt_id x).const_mul b)).add_const d
  have heq : s.f =ᶠ[𝓝 x] (fun y => a * t.f y + b * y + d) := by
    filter_upwards [Ioo_mem_nhds hx.1 hx.2] with y hy
    exact hf y ⟨hy.1.le, hy.2.le⟩
  exact (s.deriv x hx).unique (hr.congr_of_eventuallyEq heq)

lemma affine_totalDiv (s t : ι → SmoothScalar.Score) (a : ℝ) (b d : ι → ℝ)
    (hf : ∀ i x, x ∈ Icc 0 1 → (s i).f x = a * (t i).f x + b i * x + d i)
    (v c : Vec ι) (hv : ∀ i, v i ∈ Icc 0 1) (hc : ∀ i, c i ∈ Ioo 0 1) :
    totalDiv s v c = a * totalDiv t v c := by
  rw [totalDiv_eq_sum, totalDiv_eq_sum, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i _
  have hdf := affine_gradient_coordinate (s i) (t i) a (b i) (d i) (c i) (hc i) (hf i)
  simp only [SmoothScalar.divergence]
  rw [hf i (v i) (hv i), hf i (c i) ⟨(hc i).1.le, (hc i).2.le⟩, hdf]
  ring

def CommonLocalRepairs (s t : ι → SmoothScalar.Score) (i0 : ι) : Prop :=
  ∀ p : Vec ι, (∀ i, p i ∈ Ioo 0 1) → (∑ i, p i = 1) →
    ∃ (e : ℕ → ℝ) (c : ℕ → Vec ι),
      (∀ n, 0 < e n) ∧ Tendsto e atTop (𝓝 0) ∧
      (∀ n i, c n i ∈ Ioo 0 1) ∧ (∀ n, ∑ i, c n i = 1) ∧
      (∀ n i, totalDiv s (vertex i) (c n) ≤ totalDiv s (vertex i) (p + e n • vertex i0)) ∧
      (∀ n i, totalDiv t (vertex i) (c n) ≤ totalDiv t (vertex i) (p + e n • vertex i0))

def PositiveAffineEquivalent (s t : ι → SmoothScalar.Score) : Prop :=
  ∃ a > 0, ∃ b d : ι → ℝ, ∀ i x, x ∈ Icc 0 1 →
    (s i).f x = a * (t i).f x + b i * x + d i

/-- The full smooth additive-generator characterization S2, including the
positive common-repair construction. No generator-equivalence or localization
assumption is smuggled into the repair premise. -/
theorem universal_common_repair_iff_affine (hcard : 3 ≤ Fintype.card ι)
    (s t : ι → SmoothScalar.Score) (i0 : ι) :
    CommonLocalRepairs s t i0 ↔ PositiveAffineEquivalent s t := by
  constructor
  · exact GeneratorRigidity.universal_common_repairs_force_affine hcard s t i0
  · rintro ⟨a, ha, b, d, hf⟩
    intro p hp hpsum
    obtain ⟨e, c, hepos, helim, hbint, hcint, hcsum, ht⟩ := single_score_local_repairs t p (vertex i0) hp hpsum
    refine ⟨e, c, hepos, helim, hcint, hcsum, ?_, ht⟩
    intro n i
    have hv : ∀ j, (vertex i : Vec ι) j ∈ Icc 0 1 :=
      fun j => mem_Icc_of_mem_stdSimplex (single_mem_stdSimplex ℝ i) j
    rw [affine_totalDiv s t a b d hf (vertex i) (c n) hv (hcint n),
      affine_totalDiv s t a b d hf (vertex i) (p + e n • vertex i0) hv (hbint n)]
    exact mul_le_mul_of_nonneg_left (ht n i) ha.le

#print axioms single_score_local_repairs
#print axioms universal_common_repair_iff_affine
#check universal_common_repair_iff_affine
end BregmanProjection
