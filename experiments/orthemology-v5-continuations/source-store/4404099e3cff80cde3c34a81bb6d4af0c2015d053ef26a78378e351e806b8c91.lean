import FiniteHullSmoothRigidity

/-! Local approximate repair iff for a finite smooth score family.
This does not assert exact nonlinear common repair from Hessian compatibility.
The finite family permits one common sublinear tolerance by summing remainders.
-/
noncomputable section
open scoped Topology BigOperators
open Filter Set SmoothRigidity LocalRigidity FiniteHullSmoothRigidity

namespace FiniteHullApproximateIff
variable {ι J K : Type*} [Fintype ι] [DecidableEq ι] [Fintype J] [Fintype K]

omit [DecidableEq ι] in
lemma interior_tangent_sequence (v : J → Vec ι) (w : J → ℝ) (p h z : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1) (hw : ∀ j, 0 < w j)
    (hsum : ∑ j, w j = 1) (hcenter : ∑ j, w j • v j = p)
    (hz : z ∈ Submodule.span ℝ (Set.range (fun j => p - v j))) :
    ∃ e : ℕ → ℝ, (∀ n, 0 < e n) ∧ Tendsto e atTop (𝓝 0) ∧
      (∀ n i, (p + e n • h) i ∈ Ioo 0 1) ∧
      (∀ n i, (p + e n • z) i ∈ Ioo 0 1) ∧
      (∀ n, p + e n • z ∈ convexHull ℝ (Set.range v)) := by
  obtain ⟨delta, hdelta, hray⟩ := tangent_ray_in_convexHull v w p z hw hsum hcenter hz
  let r : ℕ → ℝ := fun n => 1 / ((n : ℝ) + 1)
  have hrpos : ∀ n, 0 < r n := by intro n; dsimp [r]; positivity
  have hrt : Tendsto r atTop (𝓝 0) := tendsto_one_div_add_atTop_nhds_zero_nat
  have ht : ∀ x : Vec ι, Tendsto (fun n => p + r n • x) atTop (𝓝 p) := by
    intro x
    simpa using
      (tendsto_const_nhds : Tendsto (fun _ : ℕ => p) atTop (𝓝 p)).add
        (hrt.smul (tendsto_const_nhds : Tendsto (fun _ : ℕ => x) atTop (𝓝 x)))
  have hinside : ∀ x : Vec ι, ∀ᶠ n in atTop, ∀ i, (p + r n • x) i ∈ Ioo 0 1 := by
    intro x
    apply Filter.eventually_all.mpr
    intro i
    exact ((tendsto_pi_nhds.mp (ht x)) i).eventually (Ioo_mem_nhds (hp i).1 (hp i).2)
  have hmem : ∀ᶠ n in atTop, p + r n • z ∈ convexHull ℝ (Set.range v) := by
    have hh : ∀ᶠ n in atTop, r n < delta := hrt (Iio_mem_nhds hdelta)
    exact hh.mono (fun n hn => hray (r n) (hrpos n) hn)
  obtain ⟨N, hN⟩ := Filter.eventually_atTop.mp (((hinside h).and (hinside z)).and hmem)
  exact ⟨(fun n => r (n+N)), (fun n => hrpos (n+N)),
    (tendsto_add_atTop_iff_nat N).mpr hrt,
    (fun n => (hN (n+N) (Nat.le_add_left N n)).1.1),
    (fun n => (hN (n+N) (Nat.le_add_left N n)).1.2),
    (fun n => (hN (n+N) (Nat.le_add_left N n)).2)⟩

lemma common_normal_sublinear_gains (s : K → ι → SmoothScalar.Score)
    (v : J → Vec ι) (p h z : Vec ι) (hp : ∀ i, p i ∈ Ioo 0 1)
    (hnormal : ∀ k u, u ∈ Submodule.span ℝ (Set.range (fun j => p - v j)) →
      hessian (s k) p (h-z) u = 0)
    (e : ℕ → ℝ) (hepos : ∀ n, 0 < e n) (he : Tendsto e atTop (𝓝 0)) :
    ∃ eta : ℕ → ℝ, (∀ n, 0 ≤ eta n) ∧
      Tendsto (fun n => eta n / e n) atTop (𝓝 0) ∧
      (∀ n k j, totalDiv (s k) (v j) (p + e n • z) ≤
        totalDiv (s k) (v j) (p + e n • h) + eta n) := by
  let D : ℕ → K → J → ℝ := fun n k j =>
    totalDiv (s k) (v j) (p + e n • z) - totalDiv (s k) (v j) (p + e n • h)
  have hlim : ∀ k j, Tendsto (fun n => D n k j / e n) atTop (𝓝 0) := by
    intro k j
    let L := hessian (s k) p (p - v j)
    have hb := varying_direction_limit (totalDiv (s k) (v j)) L p h
      (score_hasFDerivAt (s k) (v j) p hp) e (fun _ => h) hepos he tendsto_const_nhds
    have hc := varying_direction_limit (totalDiv (s k) (v j)) L p z
      (score_hasFDerivAt (s k) (v j) p hp) e (fun _ => z) hepos he tendsto_const_nhds
    have hn := hnormal k (p - v j) (Submodule.subset_span (Set.mem_range_self j))
    rw [hessian_symmetric] at hn
    have hz : L z - L h = 0 := by
      rw [← map_sub, show z-h = -(h-z) by abel, map_neg]
      dsimp [L]
      rw [hn, neg_zero]
    have hh := hc.sub hb
    rw [hz] at hh
    convert hh using 1
    funext n
    dsimp [D]
    ring
  let eta : ℕ → ℝ := fun n => ∑ k, ∑ j, |D n k j|
  have heta0 : ∀ n, 0 ≤ eta n := fun n =>
    Finset.sum_nonneg (fun k _ => Finset.sum_nonneg (fun j _ => abs_nonneg _))
  have hquot : ∀ n, eta n / e n = ∑ k, ∑ j, |D n k j / e n| := by
    intro n
    simp only [eta, Finset.sum_div, abs_div, abs_of_pos (hepos n)]
  refine ⟨eta, heta0, ?_, ?_⟩
  · have hh : Tendsto (fun n => ∑ k, ∑ j, |D n k j / e n|) atTop
        (𝓝 (∑ _k : K, ∑ _j : J, (0 : ℝ))) := by
      apply tendsto_finset_sum
      intro k _
      apply tendsto_finset_sum
      intro j _
      simpa using (hlim k j).abs
    simpa only [← hquot, Finset.sum_const_zero] using hh
  · intro n k j
    have hinner : |D n k j| ≤ ∑ l, |D n k l| :=
      Finset.single_le_sum (fun l (_ : l ∈ Finset.univ) => abs_nonneg (D n k l)) (Finset.mem_univ j)
    have houter : (∑ l, |D n k l|) ≤ eta n :=
      Finset.single_le_sum (fun a (_ : a ∈ Finset.univ) => Finset.sum_nonneg (fun l _ => abs_nonneg (D n a l))) (Finset.mem_univ k)
    have hd := (le_abs_self (D n k j)).trans (hinner.trans houter)
    dsimp [D] at hd
    linarith

/-- Finite-family local iff for sublinear additive tolerance. The shared normal
direction is sufficient for approximate repair, not for exact nonlinear repair. -/
theorem finite_hull_local_approximate_iff
    (s : K → ι → SmoothScalar.Score) (k0 : K)
    (v : J → Vec ι) (w : J → ℝ) (p h : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1) (hw : ∀ j, 0 < w j)
    (hsum : ∑ j, w j = 1) (hcenter : ∑ j, w j • v j = p) :
    (∃ (e eta : ℕ → ℝ) (c : ℕ → Vec ι),
      (∀ n, 0 < e n) ∧ Tendsto e atTop (𝓝 0) ∧
      (∀ n, 0 ≤ eta n) ∧ Tendsto (fun n => eta n / e n) atTop (𝓝 0) ∧
      (∀ n i, c n i ∈ Ioo 0 1) ∧
      (∀ n, c n ∈ convexHull ℝ (Set.range v)) ∧
      (∀ n k j, totalDiv (s k) (v j) (c n) ≤ totalDiv (s k) (v j) (p + e n • h) + eta n)) ↔
    (∃ z ∈ Submodule.span ℝ (Set.range (fun j => p - v j)),
      ∀ k u, u ∈ Submodule.span ℝ (Set.range (fun j => p - v j)) →
        hessian (s k) p (h-z) u = 0) := by
  constructor
  · rintro ⟨e, eta, c, hep, hel, hetap, hetal, hc, hcmem, hgain⟩
    exact finite_hull_approximate_hessian_necessary s k0 v w p h hp hw hsum hcenter
      e eta c hep hel hetap hetal hc hcmem hgain
  · rintro ⟨z, hz, hnormal⟩
    obtain ⟨e, hep, hel, hbi, hci, hcmem⟩ := interior_tangent_sequence v w p h z hp hw hsum hcenter hz
    obtain ⟨eta, hetap, hetal, hgain⟩ := common_normal_sublinear_gains s v p h z hp hnormal e hep hel
    exact ⟨e, eta, (fun n => p + e n • z), hep, hel, hetap, hetal, hci, hcmem, hgain⟩

#print axioms common_normal_sublinear_gains
#print axioms finite_hull_local_approximate_iff
#check finite_hull_local_approximate_iff
end FiniteHullApproximateIff
