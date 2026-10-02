import MixedRepair

noncomputable section
open scoped BigOperators
open Set PolynomialAND ANDCorrection MixedHull MixedScore MixedRepair
open ANDScore (mean)

namespace MixedGeometry

lemma truth_boolean (i j : Fin 6) : truth i j=0 ∨ truth i j=1 := by
  fin_cases i <;> fin_cases j <;> norm_num [truth]


lemma highSum_add (a b : Vec) : highSum (a+b)=highSum a+highSum b := by
  dsimp [highSum]
  ring
lemma highSum_smul (r : ℝ) (a : Vec) : highSum (r • a)=r*highSum a := by
  dsimp [highSum]
  ring

def tangent : Submodule ℝ Vec where
  carrier := {h | h 0=h 1 ∧ highSum h=0}
  zero_mem' := by simp [highSum]
  add_mem' := by
    intro a b ha hb
    exact ⟨by simpa [ha.1,hb.1],by rw [highSum_add,ha.2,hb.2]; ring⟩
  smul_mem' := by
    intro r a ha
    exact ⟨by simpa [ha.1],by rw [highSum_smul,ha.2]; ring⟩

def direction (i : Fin 6) : Vec := truth i-truth 5

lemma span_directions_eq : Submodule.span ℝ (Set.range direction)=tangent := by
  apply le_antisymm
  · apply Submodule.span_le.mpr
    rintro u ⟨i,rfl⟩
    fin_cases i <;> simp [tangent,direction,truth,highSum]
  · intro d hd
    have hd01 : d 0=d 1 := hd.1
    have hds : highSum d=0 := hd.2
    have hc := coefficients_center d hd01 hds
    have heq : (∑ i, coefficients d i • direction i)=d := by
      dsimp [direction]
      simp only [smul_sub,Finset.sum_sub_distrib]
      rw [hc,← Finset.sum_smul,coefficients_sum]
      simp
    rw [← heq]
    apply Submodule.sum_mem
    intro i _
    exact Submodule.smul_mem _ _ (Submodule.subset_span (Set.mem_range_self i))

lemma transverse_iff (h : Vec) :
    h ∉ Submodule.span ℝ (Set.range direction) ↔ h 0 ≠ h 1 ∨ highSum h ≠ 0 := by
  rw [span_directions_eq]
  change ¬ (h 0=h 1 ∧ highSum h=0) ↔ _
  tauto

def projection (h : Vec) : Vec :=
  ![mean (h 0) (h 1),mean (h 0) (h 1),h 2-kappa h,h 3-kappa h,h 4-kappa h,h 5-kappa h]

lemma projection_mem (h : Vec) : projection h ∈ tangent := by
  constructor
  · rfl
  · dsimp [highSum,projection,kappa]
    ring

lemma common_hessian_normal (p h u : Vec) (hp01 : p 0=p 1) (hu : u ∈ tangent) :
    (∑ i : Fin 6, (h i-projection h i)*u i)=0 ∧
    (∑ i : Fin 6, coordDDF i (p i)*(h i-projection h i)*u i)=0 := by
  have hu1 : u 1=u 0 := hu.1.symm
  have hu5 : u 5 = -u 2-u 3-u 4 := by
    have hh := hu.2
    dsimp [highSum] at hh
    linarith
  have hp1 := hp01.symm
  constructor <;> simp [projection,coordDDF,Fin.sum_univ_succ,mean,hu1,hu5,hp1] <;> ring

lemma no_free_coordinate (i : Fin 6) : (Pi.single i (1:ℝ) : Vec) ∉ tangent := by
  have h01 : (0:Fin 6) ≠ 1 := by decide
  have h02 : (0:Fin 6) ≠ 2 := by decide
  have h03 : (0:Fin 6) ≠ 3 := by decide
  have h04 : (0:Fin 6) ≠ 4 := by decide
  have h05 : (0:Fin 6) ≠ 5 := by decide
  have h10 : (1:Fin 6) ≠ 0 := by decide
  have h12 : (1:Fin 6) ≠ 2 := by decide
  have h13 : (1:Fin 6) ≠ 3 := by decide
  have h14 : (1:Fin 6) ≠ 4 := by decide
  have h15 : (1:Fin 6) ≠ 5 := by decide
  have h20 : (2:Fin 6) ≠ 0 := by decide
  have h21 : (2:Fin 6) ≠ 1 := by decide
  have h23 : (2:Fin 6) ≠ 3 := by decide
  have h24 : (2:Fin 6) ≠ 4 := by decide
  have h25 : (2:Fin 6) ≠ 5 := by decide
  have h30 : (3:Fin 6) ≠ 0 := by decide
  have h31 : (3:Fin 6) ≠ 1 := by decide
  have h32 : (3:Fin 6) ≠ 2 := by decide
  have h34 : (3:Fin 6) ≠ 4 := by decide
  have h35 : (3:Fin 6) ≠ 5 := by decide
  have h40 : (4:Fin 6) ≠ 0 := by decide
  have h41 : (4:Fin 6) ≠ 1 := by decide
  have h42 : (4:Fin 6) ≠ 2 := by decide
  have h43 : (4:Fin 6) ≠ 3 := by decide
  have h45 : (4:Fin 6) ≠ 5 := by decide
  have h50 : (5:Fin 6) ≠ 0 := by decide
  have h51 : (5:Fin 6) ≠ 1 := by decide
  have h52 : (5:Fin 6) ≠ 2 := by decide
  have h53 : (5:Fin 6) ≠ 3 := by decide
  have h54 : (5:Fin 6) ≠ 4 := by decide
  fin_cases i
  · change (Pi.single (0:Fin 6) (1:ℝ) : Vec) ∉ tangent
    norm_num [tangent,highSum,Pi.single_apply,h01,h02,h03,h04,h05,h10,h12,h13,h14,h15,h20,h21,h23,h24,h25,h30,h31,h32,h34,h35,h40,h41,h42,h43,h45,h50,h51,h52,h53,h54]
  · change (Pi.single (1:Fin 6) (1:ℝ) : Vec) ∉ tangent
    norm_num [tangent,highSum,Pi.single_apply,h01,h02,h03,h04,h05,h10,h12,h13,h14,h15,h20,h21,h23,h24,h25,h30,h31,h32,h34,h35,h40,h41,h42,h43,h45,h50,h51,h52,h53,h54]
  · change (Pi.single (2:Fin 6) (1:ℝ) : Vec) ∉ tangent
    norm_num [tangent,highSum,Pi.single_apply,h01,h02,h03,h04,h05,h10,h12,h13,h14,h15,h20,h21,h23,h24,h25,h30,h31,h32,h34,h35,h40,h41,h42,h43,h45,h50,h51,h52,h53,h54]
  · change (Pi.single (3:Fin 6) (1:ℝ) : Vec) ∉ tangent
    norm_num [tangent,highSum,Pi.single_apply,h01,h02,h03,h04,h05,h10,h12,h13,h14,h15,h20,h21,h23,h24,h25,h30,h31,h32,h34,h35,h40,h41,h42,h43,h45,h50,h51,h52,h53,h54]
  · change (Pi.single (4:Fin 6) (1:ℝ) : Vec) ∉ tangent
    norm_num [tangent,highSum,Pi.single_apply,h01,h02,h03,h04,h05,h10,h12,h13,h14,h15,h20,h21,h23,h24,h25,h30,h31,h32,h34,h35,h40,h41,h42,h43,h45,h50,h51,h52,h53,h54]
  · change (Pi.single (5:Fin 6) (1:ℝ) : Vec) ∉ tangent
    norm_num [tangent,highSum,Pi.single_apply,h01,h02,h03,h04,h05,h10,h12,h13,h14,h15,h20,h21,h23,h24,h25,h30,h31,h32,h34,h35,h40,h41,h42,h43,h45,h50,h51,h52,h53,h54]

#print axioms span_directions_eq
#print axioms common_hessian_normal
#print axioms no_free_coordinate
end MixedGeometry
