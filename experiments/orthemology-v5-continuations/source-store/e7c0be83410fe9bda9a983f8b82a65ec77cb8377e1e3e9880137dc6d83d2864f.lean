import Mathlib

noncomputable section
open scoped Topology
open Set Filter

namespace SmoothScalar

/-- Exact one-coordinate assumptions of the smooth-score report. -/
structure Score where
  f : ℝ → ℝ
  df : ℝ → ℝ
  ddf : ℝ → ℝ
  cont : ContinuousOn f (Icc 0 1)
  deriv : ∀ x ∈ Ioo 0 1, HasDerivAt f (df x) x
  second : ∀ x ∈ Ioo 0 1, HasDerivAt df (ddf x) x
  cont_second : ContinuousOn ddf (Ioo 0 1)
  positive : ∀ x ∈ Ioo 0 1, 0 < ddf x

def divergence (s : Score) (p x : ℝ) : ℝ :=
  s.f p - s.f x - s.df x * (p - x)

@[simp] lemma divergence_self (s : Score) (p : ℝ) : divergence s p p = 0 := by
  simp [divergence]

lemma divergence_deriv (s : Score) (p x : ℝ) (hx : x ∈ Ioo 0 1) :
    HasDerivAt (divergence s p) (s.ddf x * (x - p)) x := by
  have h := ((hasDerivAt_const x (s.f p)).sub (s.deriv x hx)).sub
    ((s.second x hx).mul ((hasDerivAt_const x p).sub (hasDerivAt_id x)))
  convert h using 1
  dsimp [divergence]
  ring

lemma divergence_strictMono_right (s : Score) (p : ℝ) (hp : p ∈ Ioo 0 1) :
    StrictMonoOn (divergence s p) (Ico p 1) := by
  apply strictMonoOn_of_deriv_pos (convex_Ico p 1)
  · intro x hx
    exact (divergence_deriv s p x ⟨hp.1.trans_le hx.1, hx.2⟩).continuousAt.continuousWithinAt
  · intro x hx
    have hx' : p < x ∧ x < 1 := by simpa only [interior_Ico] using hx
    rw [(divergence_deriv s p x ⟨hp.1.trans hx'.1, hx'.2⟩).deriv]
    exact mul_pos (s.positive x ⟨hp.1.trans hx'.1, hx'.2⟩) (sub_pos.mpr hx'.1)

lemma divergence_strictAnti_left (s : Score) (p : ℝ) (hp : p ∈ Ioo 0 1) :
    StrictAntiOn (divergence s p) (Ioc 0 p) := by
  apply strictAntiOn_of_deriv_neg (convex_Ioc 0 p)
  · intro x hx
    exact (divergence_deriv s p x ⟨hx.1, hx.2.trans_lt hp.2⟩).continuousAt.continuousWithinAt
  · intro x hx
    have hx' : 0 < x ∧ x < p := by simpa only [interior_Ioc] using hx
    rw [(divergence_deriv s p x ⟨hx'.1, hx'.2.trans hp.2⟩).deriv]
    exact mul_neg_of_pos_of_neg (s.positive x ⟨hx'.1, hx'.2.trans hp.2⟩) (sub_neg.mpr hx'.2)

lemma divergence_pos (s : Score) (p x : ℝ) (hp : p ∈ Ioo 0 1)
    (hx : x ∈ Ioo 0 1) (hne : x ≠ p) : 0 < divergence s p x := by
  rcases lt_or_gt_of_ne hne with hlt | hgt
  · have hh := divergence_strictAnti_left s p hp ⟨hx.1, hlt.le⟩ ⟨hp.1, le_rfl⟩ hlt
    simpa using hh
  · have hh := divergence_strictMono_right s p hp ⟨le_rfl, hp.2⟩ ⟨hgt.le, hx.2⟩ hgt
    simpa using hh

lemma divergence_nonneg (s : Score) (p x : ℝ) (hp : p ∈ Ioo 0 1)
    (hx : x ∈ Ioo 0 1) : 0 ≤ divergence s p x := by
  by_cases h : x = p
  · simp [h]
  · exact (divergence_pos s p x hp hx h).le



/-- Vanishing Bregman regret localizes interior reports even when endpoint
score derivatives are unbounded. No compact extension of the derivative is assumed. -/
theorem tendsto_of_divergence_tendsto_zero (s : Score) (p : ℝ)
    (hp : p ∈ Ioo 0 1) (c : ℕ → ℝ) (hc : ∀ n, c n ∈ Ioo 0 1)
    (hD : Tendsto (fun n => divergence s p (c n)) atTop (𝓝 0)) :
    Tendsto c atTop (𝓝 p) := by
  apply Metric.tendsto_nhds.mpr
  intro eps heps
  let d := min (eps / 2) (min (p / 2) ((1 - p) / 2))
  have hdpos : 0 < d := lt_min (half_pos heps)
    (lt_min (half_pos hp.1) (half_pos (sub_pos.mpr hp.2)))
  have hde : d ≤ eps / 2 := min_le_left _ _
  have hdp : d ≤ p / 2 := (min_le_right _ _).trans (min_le_left _ _)
  have hdq : d ≤ (1 - p) / 2 := (min_le_right _ _).trans (min_le_right _ _)
  have hlmem : p - d ∈ Ioo 0 1 := by constructor <;> linarith [hp.1, hp.2]
  have hrmem : p + d ∈ Ioo 0 1 := by constructor <;> linarith [hp.1, hp.2]
  have hlp : p - d < p := by linarith
  have hpr : p < p + d := by linarith
  have hL := divergence_pos s p (p - d) hp hlmem (ne_of_lt hlp)
  have hR := divergence_pos s p (p + d) hp hrmem (ne_of_gt hpr)
  have hmin : 0 < min (divergence s p (p - d)) (divergence s p (p + d)) := lt_min hL hR
  have hsmall : ∀ᶠ n in atTop, divergence s p (c n) <
      min (divergence s p (p - d)) (divergence s p (p + d)) :=
    hD.eventually (eventually_lt_nhds hmin)
  filter_upwards [hsmall] with n hn
  have hl : p - d < c n := by
    by_contra! hnot
    have hle : c n ≤ p - d := hnot
    have hm := (divergence_strictAnti_left s p hp).antitoneOn
      ⟨(hc n).1, hle.trans hlp.le⟩ ⟨hlmem.1, hlp.le⟩ hle
    have hb := min_le_left (divergence s p (p - d)) (divergence s p (p + d))
    linarith
  have hr : c n < p + d := by
    by_contra! hnot
    have hle : p + d ≤ c n := hnot
    have hm := (divergence_strictMono_right s p hp).monotoneOn
      ⟨hpr.le, hrmem.2⟩ ⟨hpr.le.trans hle, (hc n).2⟩ hle
    have hb := min_le_right (divergence s p (p - d)) (divergence s p (p + d))
    linarith
  rw [Real.dist_eq]
  apply abs_lt.mpr
  constructor <;> linarith



lemma radial_local_min (f k : ℝ → ℝ) (p : ℝ)
    (hp : HasDerivAt f 0 p)
    (hd : ∀ᶠ x in 𝓝 p, HasDerivAt f (k x * (x - p)) x)
    (hk : ∀ᶠ x in 𝓝 p, 0 ≤ k x) : IsLocalMin f p := by
  have hdiff : ∀ᶠ x in 𝓝 p, DifferentiableAt ℝ f x := hd.mono (fun _ h => h.differentiableAt)
  apply isLocalMin_of_deriv' hp.continuousAt
    (hdiff.filter_mono nhdsWithin_le_nhds) (hdiff.filter_mono nhdsWithin_le_nhds)
  · filter_upwards [hd.filter_mono nhdsWithin_le_nhds,
      hk.filter_mono nhdsWithin_le_nhds, self_mem_nhdsWithin] with x hx hkx hxp
    rw [hx.deriv]
    exact mul_nonpos_of_nonneg_of_nonpos hkx (sub_nonpos.mpr (le_of_lt hxp))
  · filter_upwards [hd.filter_mono nhdsWithin_le_nhds,
      hk.filter_mono nhdsWithin_le_nhds, self_mem_nhdsWithin] with x hx hkx hxp
    rw [hx.deriv]
    exact mul_nonneg hkx (sub_nonneg.mpr (le_of_lt hxp))

lemma adjusted_divergence_deriv (s : Score) (p m x : ℝ) (hx : x ∈ Ioo 0 1) :
    HasDerivAt (fun y => divergence s p y - (m / 2) * (y - p) ^ 2)
      ((s.ddf x - m) * (x - p)) x := by
  have h := (divergence_deriv s p x hx).sub
    ((((hasDerivAt_id x).sub_const p).pow 2).const_mul (m / 2))
  convert h using 1
  simp only [id_eq]
  ring

lemma local_curvature_sandwich (s : Score) (p : ℝ) (hp : p ∈ Ioo 0 1) :
    ∃ a > 0, ∃ b > 0, ∀ᶠ x in 𝓝 p,
      a * (x - p) ^ 2 ≤ divergence s p x ∧
      divergence s p x ≤ b * (x - p) ^ 2 := by
  let d := s.ddf p
  have hd : 0 < d := s.positive p hp
  have hcont : ContinuousAt s.ddf p := s.cont_second.continuousAt (Ioo_mem_nhds hp.1 hp.2)
  have hlo : ∀ᶠ x in 𝓝 p, d / 2 < s.ddf x :=
    hcont.eventually (eventually_gt_nhds (by dsimp [d] at *; linarith))
  have hhi : ∀ᶠ x in 𝓝 p, s.ddf x < 2 * d :=
    hcont.eventually (eventually_lt_nhds (by dsimp [d] at *; linarith))
  have hdom : ∀ᶠ x in 𝓝 p, x ∈ Ioo 0 1 := Ioo_mem_nhds hp.1 hp.2
  have hlowmin : IsLocalMin (fun x => divergence s p x - ((d / 2) / 2) * (x - p) ^ 2) p := by
    apply radial_local_min _ (fun x => s.ddf x - d / 2) p
    · simpa using adjusted_divergence_deriv s p (d / 2) p hp
    · exact hdom.mono (fun x hx => adjusted_divergence_deriv s p (d / 2) x hx)
    · filter_upwards [hlo] with x hx
      linarith
  have hhighmin : IsLocalMin (fun x => -(divergence s p x - ((2 * d) / 2) * (x - p) ^ 2)) p := by
    apply radial_local_min _ (fun x => 2 * d - s.ddf x) p
    · simpa using (adjusted_divergence_deriv s p (2 * d) p hp).neg
    · filter_upwards [hdom] with x hx
      convert (adjusted_divergence_deriv s p (2 * d) x hx).neg using 1
      ring
    · filter_upwards [hhi] with x hx
      linarith
  refine ⟨d / 4, by positivity, d, hd, ?_⟩
  filter_upwards [hlowmin, hhighmin] with x hxlow hxhigh
  simp only [divergence_self, sub_self, zero_pow, mul_zero, sub_zero, neg_zero] at hxlow hxhigh
  constructor <;> nlinarith

#print axioms local_curvature_sandwich
end SmoothScalar
