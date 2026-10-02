import HellingerTree
import Mathlib.Algebra.BigOperators.Ring.Finset

/-!
# Exact lifted observation law of a finite support block

Unused action coordinates contain a fixed public filler, not fresh revealed data.
Normalization and Hellinger product factorization are derived from the action laws.
-/

noncomputable section
open scoped BigOperators
open Finset

namespace Orthemology.Tranche2
variable {A Y : Type*} [Fintype A] [Fintype Y] [DecidableEq A]

omit [Fintype A] in
lemma sqrt_finset_prod (s : Finset A) (f : A → ℝ) (hf : ∀ a ∈ s, 0 ≤ f a) :
    Real.sqrt (∏ a ∈ s, f a) = ∏ a ∈ s, Real.sqrt (f a) := by
  classical
  induction s using Finset.induction_on with
  | empty => simp
  | @insert a s ha ih =>
    rw [Finset.prod_insert ha, Real.sqrt_mul (hf a (Finset.mem_insert_self _ _)),
      Finset.prod_insert ha, ih (fun b hb => hf b (Finset.mem_insert_of_mem hb))]

lemma affinity_product_coordinates (p q : A → Y → ℝ)
    (hp : ∀ a y, 0 ≤ p a y) (hq : ∀ a y, 0 ≤ q a y) :
    affinity (fun w : A → Y => ∏ a, p a (w a))
      (fun w : A → Y => ∏ a, q a (w a)) = ∏ a, affinity (p a) (q a) := by
  classical
  unfold affinity
  calc
    (∑ w : A → Y, Real.sqrt (∏ a, p a (w a)) * Real.sqrt (∏ a, q a (w a))) =
        ∑ w : A → Y, ∏ a, (Real.sqrt (p a (w a)) * Real.sqrt (q a (w a))) := by
      apply Finset.sum_congr rfl
      intro w _
      rw [sqrt_finset_prod _ _ (fun a _ => hp a (w a)),
        sqrt_finset_prod _ _ (fun a _ => hq a (w a)), Finset.prod_mul_distrib]
    _ = ∏ a, ∑ y, Real.sqrt (p a y) * Real.sqrt (q a y) := (Fintype.prod_sum (fun a y => Real.sqrt (p a y) * Real.sqrt (q a y))).symm

def blockCoordinate (p : A → Y → ℝ) (U : Finset A) (filler : Y) (a : A) (y : Y) : ℝ := by
  classical
  exact if a ∈ U then p a y else if y = filler then 1 else 0

def blockMass (p : A → Y → ℝ) (U : Finset A) (filler : Y) (w : A → Y) : ℝ :=
  ∏ a, blockCoordinate p U filler a (w a)

omit [Fintype A] [Fintype Y] in
lemma blockCoordinate_nonneg (p : A → Y → ℝ) (U : Finset A) (filler : Y)
    (hp : ∀ a y, 0 ≤ p a y) (a : A) (y : Y) : 0 ≤ blockCoordinate p U filler a y := by
  classical
  unfold blockCoordinate
  split_ifs <;> first | exact hp a y | norm_num

omit [Fintype A] in
lemma blockCoordinate_sum (p : A → Y → ℝ) (U : Finset A) (filler : Y)
    (hs : ∀ a, ∑ y, p a y = 1) (a : A) : ∑ y, blockCoordinate p U filler a y = 1 := by
  classical
  by_cases ha : a ∈ U <;> simp [blockCoordinate, ha, hs]

omit [Fintype Y] in
lemma blockMass_nonneg (p : A → Y → ℝ) (U : Finset A) (filler : Y)
    (hp : ∀ a y, 0 ≤ p a y) (w : A → Y) : 0 ≤ blockMass p U filler w := by
  exact Finset.prod_nonneg (fun a _ => blockCoordinate_nonneg p U filler hp a (w a))

theorem blockMass_normalized (p : A → Y → ℝ) (U : Finset A) (filler : Y)
    (hs : ∀ a, ∑ y, p a y = 1) : ∑ w : A → Y, blockMass p U filler w = 1 := by
  classical
  unfold blockMass
  rw [← Fintype.prod_sum]
  simp_rw [blockCoordinate_sum p U filler hs]
  simp

omit [Fintype A] in
lemma blockCoordinate_affinity (p q : A → Y → ℝ) (U : Finset A) (filler : Y) (a : A) :
    affinity (blockCoordinate p U filler a) (blockCoordinate q U filler a) =
      if a ∈ U then affinity (p a) (q a) else 1 := by
  classical
  by_cases ha : a ∈ U
  · simp [blockCoordinate, ha, affinity]
  · simp only [blockCoordinate, ha, if_false, affinity]
    calc
      (∑ x, Real.sqrt (if x = filler then 1 else 0) *
          Real.sqrt (if x = filler then 1 else 0)) =
          ∑ x, (if x = filler then (1 : ℝ) else 0) := by
        apply Finset.sum_congr rfl
        intro x _
        by_cases hx : x = filler <;> simp [hx]
      _ = 1 := by simp

theorem blockMass_affinity (p q : A → Y → ℝ) (U : Finset A) (filler : Y)
    (hp : ∀ a y, 0 ≤ p a y) (hq : ∀ a y, 0 ≤ q a y) :
    affinity (blockMass p U filler) (blockMass q U filler) = ∏ a ∈ U, affinity (p a) (q a) := by
  classical
  unfold blockMass
  rw [affinity_product_coordinates _ _
    (blockCoordinate_nonneg p U filler hp) (blockCoordinate_nonneg q U filler hq)]
  simp_rw [blockCoordinate_affinity]
  rw [← Finset.prod_filter]
  simp

omit [Fintype Y] in
/-- A block reveals no value at an action outside its selected support. -/
theorem blockMass_zero_of_unselected (p : A → Y → ℝ) (U : Finset A) (filler : Y)
    (w : A → Y) (a : A) (ha : a ∉ U) (hy : w a ≠ filler) : blockMass p U filler w = 0 := by
  classical
  apply Finset.prod_eq_zero (Finset.mem_univ a)
  simp [blockCoordinate, ha, hy]

theorem blockMass_affinity_lt_one (p q : A → Y → ℝ) (U : Finset A) (filler : Y)
    (hp : ∀ a y, 0 ≤ p a y) (hq : ∀ a y, 0 ≤ q a y)
    (hsp : ∀ a, ∑ y, p a y = 1) (hsq : ∀ a, ∑ y, q a y = 1)
    (hinfo : ∃ a ∈ U, p a ≠ q a) :
    affinity (blockMass p U filler) (blockMass q U filler) < 1 := by
  classical
  obtain ⟨a, ha, hne⟩ := hinfo
  rw [blockMass_affinity p q U filler hp hq]
  have hrest : (∏ b ∈ U.erase a, affinity (p b) (q b)) ≤ 1 := by
    exact Finset.prod_le_one (fun b _ => affinity_nonneg _ _)
      (fun b _ => affinity_le_one _ _ (hp b) (hq b) (hsp b) (hsq b))
  have hprod : (∏ b ∈ U, affinity (p b) (q b)) ≤ affinity (p a) (q a) := by
    calc
      (∏ b ∈ U, affinity (p b) (q b)) = affinity (p a) (q a) *
          ∏ b ∈ U.erase a, affinity (p b) (q b) :=
        (Finset.mul_prod_erase U (fun b => affinity (p b) (q b)) ha).symm
      _ ≤ affinity (p a) (q a) * 1 := mul_le_mul_of_nonneg_left hrest (affinity_nonneg _ _)
      _ = affinity (p a) (q a) := mul_one _
  exact hprod.trans_lt (affinity_lt_one _ _ (hp a) (hq a) (hsp a) (hsq a) hne)

end Orthemology.Tranche2
