import Mathlib

noncomputable section
open scoped BigOperators

namespace FiniteLPCertificates

variable {I E : Type*} [Fintype I] [AddCommGroup E] [Module ℝ E]

def margin (B : I → ℝ) (L : I → E →ₗ[ℝ] ℝ) (w : E) (i : I) : ℝ := B i-L i w

/-- Exact weak duality for a finite tangent-correction LP. The balance condition
is on all tangent vectors, so no favorable correction can evade the certificate. -/
theorem dual_bound (B : I → ℝ) (L : I → E →ₗ[ℝ] ℝ) (weight : I → ℝ)
    (hweight : ∀ i, 0 ≤ weight i) (hmass : ∑ i, weight i = 1)
    (hbalance : ∀ w : E, ∑ i, weight i*L i w = 0)
    (w : E) (tau : ℝ) (hprimal : ∀ i, tau ≤ margin B L w i) :
    tau ≤ ∑ i, weight i*B i := by
  calc
    tau = ∑ i, weight i*tau := by rw [← Finset.sum_mul,hmass,one_mul]
    _ ≤ ∑ i, weight i*margin B L w i :=
      Finset.sum_le_sum (fun i _ => mul_le_mul_of_nonneg_left (hprimal i) (hweight i))
    _ = ∑ i, weight i*B i := by
      simp only [margin,mul_sub,Finset.sum_sub_distrib,hbalance,sub_zero]

theorem negative_dual_excludes_weak (B : I → ℝ) (L : I → E →ₗ[ℝ] ℝ) (weight : I → ℝ)
    (hweight : ∀ i, 0 ≤ weight i) (hmass : ∑ i, weight i = 1)
    (hbalance : ∀ w : E, ∑ i, weight i*L i w = 0)
    (hnegative : (∑ i, weight i*B i) < 0) :
    ¬ ∃ w : E, ∀ i, 0 ≤ margin B L w i := by
  rintro ⟨w,hw⟩
  have hh := dual_bound B L weight hweight hmass hbalance w 0 hw
  linarith

theorem zero_dual_excludes_strict (B : I → ℝ) (L : I → E →ₗ[ℝ] ℝ) (weight : I → ℝ)
    (hweight : ∀ i, 0 ≤ weight i) (hmass : ∑ i, weight i = 1)
    (hbalance : ∀ w : E, ∑ i, weight i*L i w = 0)
    (hnonpos : (∑ i, weight i*B i) ≤ 0) :
    ¬ ∃ w : E, ∀ i, 0 < margin B L w i := by
  rintro ⟨w,hw⟩
  have hex : ∃ i, 0 < weight i := by
    by_contra! hn
    have hs : (∑ i, weight i) ≤ 0 := by
      simpa using Finset.sum_le_sum (fun i (_ : i ∈ Finset.univ) => hn i)
    linarith
  obtain ⟨j,hj⟩ := hex
  have hpos : 0 < ∑ i, weight i*margin B L w i := by
    apply Finset.sum_pos'
    · intro i _
      exact mul_nonneg (hweight i) (hw i).le
    · exact ⟨j,Finset.mem_univ j,mul_pos hj (hw j)⟩
  have heq : (∑ i, weight i*margin B L w i) = ∑ i, weight i*B i := by
    simp only [margin,mul_sub,Finset.sum_sub_distrib,hbalance,sub_zero]
  rw [heq] at hpos
  linarith

#print axioms dual_bound
#print axioms negative_dual_excludes_weak
#print axioms zero_dual_excludes_strict
end FiniteLPCertificates
