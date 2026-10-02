import FiniteHullApproximateIff

/-! Literal intrinsic-interior interface for the frozen positive-barycentric
finite-hull theorems. No finite-dimensional assumption is needed for the
centroid/segment-extension certificate itself. -/
noncomputable section
open scoped Topology BigOperators
open Filter Set

namespace IntrinsicBarycentric
variable {E J : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] [Fintype J]

lemma finite_convex_weights (v : J → E) (y : E)
    (hy : y ∈ convexHull ℝ (Set.range v)) :
    ∃ w : J → ℝ, (∀ j, 0 ≤ w j) ∧ (∑ j, w j = 1) ∧ (∑ j, w j • v j = y) := by
  classical
  rw [convexHull_range_eq_exists_affineCombination] at hy
  obtain ⟨s, a, ha, hsum, hcenter⟩ := hy
  let w : J → ℝ := fun j => if j ∈ s then a j else 0
  have hmass : ∑ j, w j = ∑ j ∈ s, a j := by simp [w]
  have hsumv : ∑ j, w j • v j = ∑ j ∈ s, a j • v j := by simp [w, ite_smul]
  refine ⟨w, ?_, hmass.trans hsum, ?_⟩
  · intro j
    dsimp [w]
    split_ifs with hj
    · exact ha j hj
    · exact le_rfl
  · rw [hsumv]
    rwa [Finset.affineCombination_eq_linear_combination s v a hsum] at hcenter

/-- Any intrinsic-interior point of a nonempty finite hull admits weights
strictly positive at every listed truth vector, including duplicated entries. -/
theorem intrinsicInterior_positive_barycentric (v : J → E) (p : E)
    (hp : p ∈ intrinsicInterior ℝ (convexHull ℝ (Set.range v))) :
    ∃ w : J → ℝ, (∀ j, 0 < w j) ∧ (∑ j, w j = 1) ∧ (∑ j, w j • v j = p) := by
  classical
  have hpC : p ∈ convexHull ℝ (Set.range v) := intrinsicInterior_subset hp
  have hJ : Nonempty J := by
    by_contra hn
    haveI : IsEmpty J := not_nonempty_iff.mp hn
    rw [Set.range_eq_empty v, convexHull_empty] at hpC
    exact hpC
  letI := hJ
  let N : ℝ := Fintype.card J
  have hN : 0 < N := by dsimp [N]; exact_mod_cast (Fintype.card_pos : 0 < Fintype.card J)
  let q : E := ∑ j, (1 / N) • v j
  have hmass : (∑ _ : J, (1 : ℝ) / N) = 1 := by
    simp only [Finset.sum_const, Finset.card_univ, nsmul_eq_mul]
    dsimp [N] at *
    field_simp
  have hqC : q ∈ convexHull ℝ (Set.range v) :=
    mem_convexHull_of_exists_fintype (fun _ : J => (1 : ℝ) / N) v
      (fun _ => (div_pos (by norm_num) hN).le) hmass (fun j => Set.mem_range_self j) rfl
  let A := affineSpan ℝ (convexHull ℝ (Set.range v))
  obtain ⟨pA, hpA, hpcoe⟩ := mem_intrinsicInterior.mp hp
  haveI : Nonempty A := ⟨pA⟩
  let qA : A := ⟨q, subset_affineSpan ℝ _ hqC⟩
  have htend : Tendsto (AffineMap.lineMap qA pA) (𝓝 (1 : ℝ)) (𝓝 pA) := by
    have hcont : Continuous (fun t : ℝ => AffineMap.lineMap qA pA t) := by
      simp only [AffineMap.lineMap_apply]
      fun_prop
    simpa using hcont.tendsto 1
  have hev : ∀ᶠ t in 𝓝 (1 : ℝ),
      AffineMap.lineMap qA pA t ∈ ((↑) ⁻¹' convexHull ℝ (Set.range v) : Set A) :=
    htend.eventually (mem_interior_iff_mem_nhds.mp hpA)
  obtain ⟨t, ht, hty⟩ := hev.exists_gt
  let y : E := ↑(AffineMap.lineMap qA pA t)
  have hy : y ∈ convexHull ℝ (Set.range v) := hty
  have hyexpr : y = (1-t) • q + t • p := by
    change t • ((pA : E) - q) + q = (1-t) • q + t • p
    rw [hpcoe]
    module
  obtain ⟨u, hu, husum, hucenter⟩ := finite_convex_weights v y hy
  let alpha : ℝ := (t-1)/t
  let beta : ℝ := 1/t
  have htp : 0 < t := by linarith
  have hap : 0 < alpha := div_pos (by linarith) htp
  have hbp : 0 < beta := div_pos (by norm_num) htp
  have hab : alpha + beta = 1 := by dsimp [alpha, beta]; field_simp
  have hcancel : alpha + beta * (1-t) = 0 := by dsimp [alpha, beta]; field_simp
  have hbt : beta * t = 1 := by dsimp [beta]; field_simp
  refine ⟨(fun j => alpha / N + beta * u j), ?_, ?_, ?_⟩
  · intro j
    exact add_pos_of_pos_of_nonneg (div_pos hap hN) (mul_nonneg hbp.le (hu j))
  · simp only [Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ, nsmul_eq_mul,
      ← Finset.mul_sum, husum, mul_one]
    have hn : (Fintype.card J : ℝ) * (alpha / N) = alpha := by dsimp [N]; field_simp
    rw [hn, hab]
  · calc
      (∑ j, (alpha / N + beta * u j) • v j) = alpha • q + beta • y := by
        rw [← hucenter]
        dsimp [q]
        simp only [add_smul, Finset.sum_add_distrib, Finset.smul_sum, smul_smul]
        congr 1
        apply Finset.sum_congr rfl
        intro j _
        congr 1
        ring
      _ = p := by
        rw [hyexpr, smul_add, smul_smul, smul_smul, ← add_assoc, ← add_smul, hcancel, hbt]
        simp

open LocalRigidity

theorem quadratic_local_common_repair_iff_intrinsicInterior [FiniteDimensional ℝ E]
    {K : Type*}
    (Bs : K → Form E) (k0 : K)
    (hsym : ∀ k x y, Bs k x y = Bs k y x)
    (hpos : ∀ k u, u ≠ 0 → 0 < Bs k u u)
    (v : J → E) (p h : E)
    (hp : p ∈ intrinsicInterior ℝ (convexHull ℝ (Set.range v)))
    (htrans : h ∉ Submodule.span ℝ (Set.range (fun i => p - v i))) :
    (∃ (e : ℕ → ℝ) (c : ℕ → E),
      (∀ n, 0 < e n) ∧ Tendsto e atTop (𝓝 0) ∧
      (∀ n, c n ∈ convexHull ℝ (Set.range v)) ∧
      (∀ n k i, loss (Bs k) (c n) (v i) ≤ loss (Bs k) (p + e n • h) (v i))) ↔
    (∃ z ∈ Submodule.span ℝ (Set.range (fun i => p - v i)),
      ∀ k u, u ∈ Submodule.span ℝ (Set.range (fun i => p - v i)) →
        Bs k (h - z) u = 0) := by
  obtain ⟨w, hw, hsum, hcenter⟩ := intrinsicInterior_positive_barycentric v p hp
  exact LocalRigidity.local_common_repair_iff Bs k0 hsym hpos v w p h hw hsum hcenter htrans

#print axioms intrinsicInterior_positive_barycentric
#check intrinsicInterior_positive_barycentric

section Smooth
variable {ι : Type*} [Fintype ι] [DecidableEq ι]
open SmoothRigidity FiniteHullSmoothRigidity

theorem smooth_finite_hull_approximate_necessary_intrinsicInterior {K : Type*}
    (s : K → ι → SmoothScalar.Score) (k0 : K) (v : J → Vec ι) (p h : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1)
    (hri : p ∈ intrinsicInterior ℝ (convexHull ℝ (Set.range v)))
    (e eta : ℕ → ℝ) (c : ℕ → Vec ι)
    (hepos : ∀ n, 0 < e n) (he : Tendsto e atTop (𝓝 0))
    (heta0 : ∀ n, 0 ≤ eta n) (heta : Tendsto (fun n => eta n / e n) atTop (𝓝 0))
    (hc : ∀ n i, c n i ∈ Ioo 0 1)
    (hcmem : ∀ n, c n ∈ convexHull ℝ (Set.range v))
    (hgain : ∀ n k j, totalDiv (s k) (v j) (c n) ≤ totalDiv (s k) (v j) (p + e n • h) + eta n) :
    ∃ z ∈ Submodule.span ℝ (Set.range (fun j => p - v j)),
      ∀ k u, u ∈ Submodule.span ℝ (Set.range (fun j => p - v j)) →
        hessian (s k) p (h-z) u = 0 := by
  obtain ⟨w, hw, hsum, hcenter⟩ := intrinsicInterior_positive_barycentric v p hri
  exact finite_hull_approximate_hessian_necessary s k0 v w p h hp hw hsum hcenter
    e eta c hepos he heta0 heta hc hcmem hgain

variable {K : Type*}

theorem smooth_finite_hull_approximate_iff_intrinsicInterior
    [Fintype K] (s : K → ι → SmoothScalar.Score) (k0 : K)
    (v : J → Vec ι) (p h : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1)
    (hri : p ∈ intrinsicInterior ℝ (convexHull ℝ (Set.range v))) :
    (∃ (e eta : ℕ → ℝ) (c : ℕ → Vec ι),
      (∀ n, 0 < e n) ∧ Tendsto e atTop (𝓝 0) ∧
      (∀ n, 0 ≤ eta n) ∧ Tendsto (fun n => eta n / e n) atTop (𝓝 0) ∧
      (∀ n i, c n i ∈ Ioo 0 1) ∧
      (∀ n, c n ∈ convexHull ℝ (Set.range v)) ∧
      (∀ n k j, totalDiv (s k) (v j) (c n) ≤ totalDiv (s k) (v j) (p + e n • h) + eta n)) ↔
    (∃ z ∈ Submodule.span ℝ (Set.range (fun j => p - v j)),
      ∀ k u, u ∈ Submodule.span ℝ (Set.range (fun j => p - v j)) →
        hessian (s k) p (h-z) u = 0) := by
  obtain ⟨w, hw, hsum, hcenter⟩ := intrinsicInterior_positive_barycentric v p hri
  exact FiniteHullApproximateIff.finite_hull_local_approximate_iff s k0 v w p h hp hw hsum hcenter

end Smooth
#print axioms smooth_finite_hull_approximate_iff_intrinsicInterior
#check smooth_finite_hull_approximate_iff_intrinsicInterior
#print axioms quadratic_local_common_repair_iff_intrinsicInterior
#print axioms smooth_finite_hull_approximate_necessary_intrinsicInterior
#check quadratic_local_common_repair_iff_intrinsicInterior
#check smooth_finite_hull_approximate_necessary_intrinsicInterior
end IntrinsicBarycentric

