import ANDPotentialBinding
import FiniteHullWeights

noncomputable section
open scoped BigOperators Topology
open Set Filter PolynomialAND ANDCorrection ANDScore ANDRepair ANDPotentialBinding

namespace ANDIntrinsic

lemma interior_parameters (p : Vec) (hp : p ∈ intrinsicInterior ℝ hull) :
    p 0 = p 1 ∧ 0 < p 0 ∧ p 0 < p 2 ∧ p 0 < p 3 ∧ p 2+p 3 < 1+p 0 := by
  obtain ⟨a, ha, hsum, hcenter⟩ :=
    FiniteHullWeights.intrinsicInterior_positive_barycentric truth p hp
  have h0 := congrArg (fun v : Vec => v 0) hcenter
  have h1 := congrArg (fun v : Vec => v 1) hcenter
  have h2 := congrArg (fun v : Vec => v 2) hcenter
  have h3 := congrArg (fun v : Vec => v 3) hcenter
  simp [truth, Fin.sum_univ_succ] at h0 h1 h2 h3 hsum
  have ha0 := ha 0
  have ha1 := ha 1
  have ha2 := ha 2
  have ha3 := ha 3
  constructor
  · linarith
  constructor
  · linarith
  constructor
  · linarith
  constructor <;> linarith

/-- No parametric stand-in for relative interior: every point of the literal
intrinsic interior of the finite AND truth hull has the nonlinear repair. -/
theorem intrinsic_universal_Bregman_repair (p h : Vec)
    (hp : p ∈ intrinsicInterior ℝ hull) (htrans : h 0 ≠ h 1) :
    ∃ delta > 0, ∀ eps : ℝ, 0 < eps → eps < delta →
      (∀ j : Fin 4, (p+eps • h) j ∈ Ioo 0 1) ∧
      candidate (p 0) (p 2) (p 3) (h 0) (h 1) (h 2) (h 3) eps ∈ hull ∧
      (∀ i : Fin 4,
        divergence coordG coordDG (truth i)
          (candidate (p 0) (p 2) (p 3) (h 0) (h 1) (h 2) (h 3) eps) <
          divergence coordG coordDG (truth i) (p+eps • h) ∧
        divergence coordF coordDF (truth i)
          (candidate (p 0) (p 2) (p 3) (h 0) (h 1) (h 2) (h 3) eps) <
          divergence coordF coordDF (truth i) (p+eps • h)) := by
  obtain ⟨hp01, hs, hz, hw, hsum⟩ := interior_parameters p hp
  obtain ⟨delta, hd, hh⟩ := universal_Bregman_repair
    (p 0) (p 2) (p 3) (h 0) (h 1) (h 2) (h 3) hs hz hw hsum htrans
  refine ⟨delta, hd, ?_⟩
  intro eps he hsmall
  have hb : baseline (p 0) (p 2) (p 3) (h 0) (h 1) (h 2) (h 3) eps = p+eps • h := by
    ext i
    fin_cases i <;> simp [baseline, hp01]
  simpa only [hb] using hh eps he hsmall

def tangent : Submodule ℝ Vec where
  carrier := {u | u 0 = u 1}
  zero_mem' := by simp
  add_mem' := by intro a b ha hb; simp only [Set.mem_setOf_eq] at *; simp [ha,hb]
  smul_mem' := by intro a b hb; simp only [Set.mem_setOf_eq] at *; simp [hb]

lemma span_truth_eq_tangent : Submodule.span ℝ (Set.range truth) = tangent := by
  apply le_antisymm
  · apply Submodule.span_le.mpr
    rintro u ⟨i,rfl⟩
    fin_cases i <;> simp [tangent, truth]
  · intro h hh
    have h01 : h 0 = h 1 := hh
    have h1 : truth 1 ∈ Submodule.span ℝ (Set.range truth) := Submodule.subset_span (Set.mem_range_self 1)
    have h2 : truth 2 ∈ Submodule.span ℝ (Set.range truth) := Submodule.subset_span (Set.mem_range_self 2)
    have h3 : truth 3 ∈ Submodule.span ℝ (Set.range truth) := Submodule.subset_span (Set.mem_range_self 3)
    have hm := (Submodule.span ℝ (Set.range truth)).add_mem
      ((Submodule.span ℝ (Set.range truth)).add_mem
        ((Submodule.span ℝ (Set.range truth)).smul_mem (h 0) h3)
        ((Submodule.span ℝ (Set.range truth)).smul_mem (h 2-h 0) h1))
      ((Submodule.span ℝ (Set.range truth)).smul_mem (h 3-h 0) h2)
    have heq : (h 0) • truth 3+(h 2-h 0) • truth 1+(h 3-h 0) • truth 2 = h := by
      ext i
      fin_cases i <;> simp [truth, h01]
    rwa [heq] at hm

lemma transverse_iff (h : Vec) :
    h ∉ Submodule.span ℝ (Set.range truth) ↔ h 0 ≠ h 1 := by
  rw [span_truth_eq_tangent]
  rfl

#print axioms intrinsic_universal_Bregman_repair
end ANDIntrinsic
