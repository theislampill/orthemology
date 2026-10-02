import Mathlib

/- Reused finite-hull barycentric bridge from tranche 2, with only the
namespace/import dependency reduced. Not a new theorem claim. -/
noncomputable section
open scoped Topology BigOperators
open Filter Set

namespace FiniteHullWeights
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

end FiniteHullWeights
