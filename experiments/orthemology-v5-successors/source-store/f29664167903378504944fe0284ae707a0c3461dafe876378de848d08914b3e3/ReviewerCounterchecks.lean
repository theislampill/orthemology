import RationalFixtures

namespace ReviewerCounterchecks
open TraceControls
open scoped BigOperators
variable {K : Type*} [Field K] [LinearOrder K] [IsStrictOrderedRing K]

-- Full observation-space check: the declared diagonal support loses no mass.
omit [LinearOrder K] [IsStrictOrderedRing K] in
theorem off_support_zero (m : ℕ) (w : Word) (z : Fin m → Trace)
    (hz : z ∉ copySupport m) : (copyMass m w z : K) = 0 := by
  classical
  unfold copyMass
  apply Finset.sum_eq_zero
  intro t _
  have hne : copies m t ≠ z := by
    intro h
    apply hz
    rw [← h]
    exact Finset.mem_image.mpr ⟨t, Finset.mem_univ _, rfl⟩
  simp [hne]

theorem full_copy_normalization (m : ℕ) (w : Word) :
    (∑ z : Fin m → Trace, (copyMass m w z : K)) = 1 := by
  classical
  unfold copyMass
  rw [Finset.sum_comm]
  simpa using (trace_total (K := K) w)

theorem full_copy_tv (m : ℕ) :
    (1/2 : K) * (∑ z : Fin m → Trace,
      |(copyMass m word00 z : K) - copyMass m word01 z|) = copiedTV m := by
  classical
  unfold copiedTV
  congr 1
  symm
  apply Finset.sum_subset (Finset.subset_univ _)
  intro z _ hz
  simp [off_support_zero m word00 z hz, off_support_zero m word01 z hz]

-- This connects the operational pullback expectation to literal pushforward masses.
omit [LinearOrder K] [IsStrictOrderedRing K] in
theorem pushforward_expectation (m : ℕ) (w : Word) (h : (Fin m → Trace) → K) :
    (∑ z, copyMass m w z * h z) = ∑ t, mass w t * h (copies m t) := by
  classical
  unfold copyMass
  simp_rw [Finset.sum_mul]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro t _
  simp

-- Attainability is independently checked for every ordered field, not only ℚ.
def optimal (t : Trace) : K := if t.val = 2 ∨ t.val = 4 then 1 else 0

theorem optimal_bounded : ∀ t, (0 : K) ≤ optimal t ∧ (optimal t : K) ≤ 1 := by
  intro t
  unfold optimal
  split_ifs <;> norm_num

theorem optimal_attains : success (optimal : Trace → K) = 5/8 := by
  rw [success_formula]
  norm_num [optimal, Fin.coe_ofNat_eq_mod]

theorem copied_optimal_attains (m : ℕ) (hm : 0 < m) :
    duplicateSuccess m (fun z => (optimal (z ⟨0,hm⟩) : K)) = 5/8 := by
  change success (optimal : Trace → K) = 5/8
  exact optimal_attains

theorem zero_is_not_injective : ¬Function.Injective (copies 0) := by
  intro h
  have bad := h (show copies 0 empty = copies 0 zero from Subsingleton.elim _ _)
  norm_num [empty, zero, Fin.ext_iff] at bad

-- The two incompatible masks exhaust the conditional mass, and their premise is nonzero.
theorem mask_conditioning_complete :
    (0 : K) < mass word00 zero ∧
    conditionalMaskMass (false,false) = (0 : K) ∧
    conditionalMaskMass (true,true) = (0 : K) ∧
    (∑ a : Mask, (conditionalMaskMass a : K)) = 1 := by
  norm_num [conditionalMaskMass, mass, emit, word00, zero,
    maskWeight, retention, Fintype.sum_prod_type, Fintype.sum_bool, Fin.coe_ofNat_eq_mod]

-- There is no simultaneous 2/3 guarantee for both words under a bounded binary rule.
theorem not_both_two_thirds (h : Trace → K)
    (hh : ∀ t, 0 ≤ h t ∧ h t ≤ 1) :
    ¬ (((2/3 : K) ≤ ∑ t, mass word00 t * (1-h t)) ∧
      ((2/3 : K) ≤ ∑ t, mass word01 t * h t)) := by
  intro hboth
  have hb := randomized_success_bound h hh
  unfold success at hb
  linarith [hboth.1, hboth.2]

-- Probability constraints are material, rather than decorative assumptions.
theorem missing_upper_bound_counterexample :
    (5/8 : ℚ) < success (fun t => if t.val = 2 then 2 else 0) := by
  rw [success_formula]
  norm_num [Fin.coe_ofNat_eq_mod]

theorem missing_lower_bound_counterexample :
    (5/8 : ℚ) < success (fun t => if t.val = 1 then -2 else 0) := by
  rw [success_formula]
  norm_num [Fin.coe_ofNat_eq_mod]

end ReviewerCounterchecks
