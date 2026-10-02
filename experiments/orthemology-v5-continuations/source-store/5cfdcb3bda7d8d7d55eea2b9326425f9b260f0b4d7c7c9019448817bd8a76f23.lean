import RationalTailReference
import Mathlib.Data.Nat.Choose.Basic

open scoped BigOperators
open Orthemology.Tranche2

namespace Orthemology.Tranche3

def countMass (n k : ℕ) (p : ℚ) : ℚ :=
  ∑ w, if rationalCount n w=k then rationalMass n p w else 0

lemma countMass_zero_base (k : ℕ) (p : ℚ) : countMass 0 k p = if k=0 then 1 else 0 := by
  simp [countMass,rationalCount,rationalMass,Bits,eq_comm]

lemma countMass_above (n k : ℕ) (p : ℚ) (hk : n<k) : countMass n k p = 0 := by
  apply Finset.sum_eq_zero
  intro w _
  have hc := rationalCount_le n w
  have hne : rationalCount n w ≠ k := by omega
  simp [hne]

lemma countMass_succ_zero (n : ℕ) (p : ℚ) :
    countMass (n+1) 0 p = (1-p)*countMass n 0 p := by
  unfold countMass
  change (∑ w : Bool × Bits n, if rationalCount (n+1) w=0 then rationalMass (n+1) p w else 0) = _
  rw [Fintype.sum_prod_type]
  simp only [Fintype.sum_bool,rationalCount,rationalMass,Bool.false_eq_true,if_false,if_true]
  have hz : (∑ x : Bits n, if 1+rationalCount n x=0 then p*rationalMass n p x else 0)=0 := by
    apply Finset.sum_eq_zero
    intro x _
    have hne : 1+rationalCount n x ≠ 0 := by omega
    simp [hne]
  rw [hz,zero_add]
  simp only [zero_add]
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro w _
  split_ifs <;> ring

lemma countMass_succ_succ (n k : ℕ) (p : ℚ) :
    countMass (n+1) (k+1) p = p*countMass n k p+(1-p)*countMass n (k+1) p := by
  unfold countMass
  change (∑ w : Bool × Bits n, if rationalCount (n+1) w=k+1 then rationalMass (n+1) p w else 0) = _
  rw [Fintype.sum_prod_type]
  simp only [Fintype.sum_bool,rationalCount,rationalMass,Bool.false_eq_true,if_false,if_true,zero_add]
  rw [Finset.mul_sum,Finset.mul_sum]
  congr 1
  · apply Finset.sum_congr rfl
    intro w _
    have he : (1+rationalCount n w=k+1) ↔ rationalCount n w=k := by omega
    simp only [he]
    split_ifs <;> ring
  · apply Finset.sum_congr rfl
    intro w _
    split_ifs <;> ring

/-- Grouping the actual finite-word experiment by number of successes yields
exactly the binomial polynomial, for all rational p, without numerical fitting. -/
theorem countMass_binomial : ∀ n k (p : ℚ),
    countMass n k p = (n.choose k:ℚ)*p^k*(1-p)^(n-k) := by
  intro n
  induction n with
  | zero =>
      intro k p
      cases k <;> simp [countMass_zero_base]
  | succ n ih =>
      intro k p
      cases k with
      | zero =>
          rw [countMass_succ_zero,ih]
          simp only [Nat.choose_zero_right,Nat.sub_zero,pow_zero,mul_one,one_mul,pow_succ]
          ring
      | succ k =>
          by_cases hkn : k<n
          · rw [countMass_succ_succ,ih,ih,Nat.choose_succ_succ]
            have hsub1 : n+1-(k+1)=n-k := by omega
            have hsub2 : n-k=(n-(k+1))+1 := by omega
            rw [hsub1,hsub2,pow_succ,pow_succ]
            push_cast
            ring
          · by_cases he : k=n
            · subst k
              rw [countMass_succ_succ,ih,countMass_above n (n+1) p (by omega)]
              simp [Nat.choose_self,Nat.sub_self,pow_succ,mul_comm]
            · have hab : n+1<k+1 := by omega
              rw [countMass_above _ _ _ hab,Nat.choose_eq_zero_of_lt hab]
              simp

def efficientUpper (n k : ℕ) (p : ℚ) : ℚ :=
  ∑ s ∈ Finset.range (n+1), if k≤s then (n.choose s:ℚ)*p^s*(1-p)^(n-s) else 0

def efficientLower (n k : ℕ) (p : ℚ) : ℚ :=
  ∑ s ∈ Finset.range (n+1), if s≤k then (n.choose s:ℚ)*p^s*(1-p)^(n-s) else 0

lemma sum_grouped_count (n : ℕ) (p : ℚ) (P : ℕ → Prop) [DecidablePred P] :
    (∑ s ∈ Finset.range (n+1), if P s then countMass n s p else 0) =
      ∑ w, if P (rationalCount n w) then rationalMass n p w else 0 := by
  classical
  have he : ∀ s, (if P s then countMass n s p else 0) =
      ∑ w : Bits n, if rationalCount n w=s then (if P (rationalCount n w) then rationalMass n p w else 0) else 0 := by
    intro s
    unfold countMass
    by_cases hs : P s
    · rw [if_pos hs]
      apply Finset.sum_congr rfl
      intro w _
      by_cases hc : rationalCount n w=s
      · simp [hc,hs]
      · simp [hc]
    · rw [if_neg hs]
      symm
      apply Finset.sum_eq_zero
      intro w _
      by_cases hc : rationalCount n w=s
      · simp [hc,hs]
      · simp [hc]
  simp_rw [he]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro w _
  have hc : rationalCount n w ∈ Finset.range (n+1) := Finset.mem_range.mpr (by have := rationalCount_le n w; omega)
  simp [Finset.sum_ite_eq',hc]

/-- Exact equality to the finite-word reference reduces a tail evaluation from
2^n word terms to n+1 binomial terms. Arithmetic bit complexity is still relevant. -/
theorem efficientUpper_eq (n k : ℕ) (p : ℚ) : efficientUpper n k p = rationalUpper n k p := by
  unfold efficientUpper rationalUpper
  simp_rw [← countMass_binomial]
  exact sum_grouped_count n p (fun s => k≤s)

theorem efficientLower_eq (n k : ℕ) (p : ℚ) : efficientLower n k p = rationalLower n k p := by
  unfold efficientLower rationalLower
  simp_rw [← countMass_binomial]
  exact sum_grouped_count n p (fun s => s≤k)

end Orthemology.Tranche3

#print axioms Orthemology.Tranche3.countMass_binomial
#print axioms Orthemology.Tranche3.efficientUpper_eq
#print axioms Orthemology.Tranche3.efficientLower_eq
#eval Orthemology.Tranche3.efficientUpper 32 16 (1/2)
