import StatisticalRepair
import FiniteTailCoverage

open scoped BigOperators
open Orthemology.Tranche2

namespace Orthemology.Tranche3
noncomputable section

/-- Coordinatewise binary order without choosing an order on sample identities. -/
def BitsLE : (n : ℕ) → Bits n → Bits n → Prop
  | 0, _, _ => True
  | n+1, x, y => (x.1 = false ∨ y.1 = true) ∧ BitsLE n x.2 y.2

lemma bitsLE_refl : ∀ n (x : Bits n), BitsLE n x x := by
  intro n
  induction n with
  | zero => intro x; trivial
  | succ n ih =>
      intro x
      refine ⟨?_,ih x.2⟩
      cases x.1 <;> simp

def countOnes : (n : ℕ) → Bits n → ℕ
  | 0, _ => 0
  | n+1, x => (if x.1 then 1 else 0) + countOnes n x.2

lemma countOnes_mono : ∀ n (x y : Bits n), BitsLE n x y → countOnes n x ≤ countOnes n y := by
  intro n
  induction n with
  | zero => intro x y h; rfl
  | succ n ih =>
      intro x y h
      have ht := ih x.2 y.2 h.2
      rcases x with ⟨b,x⟩
      rcases y with ⟨c,y⟩
      cases b <;> cases c <;> simp [BitsLE,countOnes] at h ht ⊢ <;> omega

def coinExpectation (n : ℕ) (p : ℝ) (f : Bits n → ℝ) : ℝ :=
  ∑ w, bernoulliMass n p w*f w

lemma coinExpectation_step (n : ℕ) (p : ℝ) (f : Bits (n+1) → ℝ) :
    coinExpectation (n+1) p f =
      (1-p)*coinExpectation n p (fun w => f (false,w))+
      p*coinExpectation n p (fun w => f (true,w)) := by
  unfold coinExpectation
  change (∑ w : Bool × Bits n, coinMass p w.1*bernoulliMass n p w.2*f w) = _
  rw [Fintype.sum_prod_type]
  simp [coinMass,Finset.mul_sum,mul_assoc,add_comm]

/-- Product Bernoulli laws preserve every increasing finite-sample statistic.
This derives parameter stochastic monotonicity from actual product masses. -/
theorem coinExpectation_mono_parameter : ∀ n (p q : ℝ) (f : Bits n → ℝ),
    0 ≤ p → p ≤ q → q ≤ 1 →
    (∀ x y, BitsLE n x y → f x ≤ f y) →
    coinExpectation n p f ≤ coinExpectation n q f := by
  intro n
  induction n with
  | zero => intro p q f hp hpq hq hf; simp [coinExpectation,bernoulliMass]
  | succ n ih =>
      intro p q f hp hpq hq hf
      have hp1 : p ≤ 1 := hpq.trans hq
      have hq0 : 0 ≤ q := hp.trans hpq
      have hf0 := ih p q (fun w => f (false,w)) hp hpq hq
        (fun x y h => hf (false,x) (false,y) ⟨Or.inl rfl,h⟩)
      have hf1 := ih p q (fun w => f (true,w)) hp hpq hq
        (fun x y h => hf (true,x) (true,y) ⟨Or.inr rfl,h⟩)
      have hcross : coinExpectation n q (fun w => f (false,w)) ≤
          coinExpectation n q (fun w => f (true,w)) := by
        apply Finset.sum_le_sum
        intro w _
        exact mul_le_mul_of_nonneg_left
          (hf (false,w) (true,w) ⟨Or.inl rfl,bitsLE_refl n w⟩)
          (bernoulliMass_nonneg n q hq0 hq w)
      rw [coinExpectation_step,coinExpectation_step]
      nlinarith [mul_nonneg (sub_nonneg.mpr hf0) (sub_nonneg.mpr hp1),
        mul_nonneg (sub_nonneg.mpr hf1) hp,
        mul_nonneg (sub_nonneg.mpr hcross) (sub_nonneg.mpr hpq)]

def bernoulliUpper (n k : ℕ) (p : ℝ) : ℝ :=
  coinExpectation n p (fun w => if k ≤ countOnes n w then 1 else 0)
def bernoulliLower (n k : ℕ) (p : ℝ) : ℝ :=
  coinExpectation n p (fun w => if countOnes n w ≤ k then 1 else 0)

theorem bernoulliUpper_mono (n k : ℕ) (p q : ℝ)
    (hp : 0 ≤ p) (hpq : p ≤ q) (hq : q ≤ 1) :
    bernoulliUpper n k p ≤ bernoulliUpper n k q := by
  apply coinExpectation_mono_parameter n p q _ hp hpq hq
  intro x y h
  have hm := countOnes_mono n x y h
  split_ifs <;> norm_num at *
  all_goals omega

theorem bernoulliLower_antitone (n k : ℕ) (p q : ℝ)
    (hp : 0 ≤ p) (hpq : p ≤ q) (hq : q ≤ 1) :
    bernoulliLower n k q ≤ bernoulliLower n k p := by
  have h := coinExpectation_mono_parameter n p q
    (fun w => if countOnes n w ≤ k then (-1:ℝ) else 0) hp hpq hq (by
      intro x y hxy
      have hm := countOnes_mono n x y hxy
      dsimp only
      split_ifs <;> norm_num at *
      all_goals omega)
  have he : ∀ r : ℝ, coinExpectation n r (fun w => if countOnes n w ≤ k then (-1:ℝ) else 0) =
      -bernoulliLower n k r := by
    intro r
    simp only [bernoulliLower,coinExpectation]
    rw [← Finset.sum_neg_distrib]
    apply Finset.sum_congr rfl
    intro w _
    split_ifs <;> ring
  rw [he,he] at h
  linarith

lemma bernoulliUpper_as_tail (n : ℕ) (p : ℝ) (w : Bits n) :
    bernoulliUpper n (countOnes n w) p = upperTail (bernoulliMass n p) (countOnes n) w := by
  simp only [bernoulliUpper,coinExpectation,upperTail]
  apply Finset.sum_congr rfl
  intro x _
  split_ifs <;> simp

lemma bernoulliLower_as_tail (n : ℕ) (p : ℝ) (w : Bits n) :
    bernoulliLower n (countOnes n w) p = lowerTail (bernoulliMass n p) (countOnes n) w := by
  simp only [bernoulliLower,coinExpectation,lowerTail]
  apply Finset.sum_congr rfl
  intro x _
  split_ifs <;> simp

end
end Orthemology.Tranche3

#print axioms Orthemology.Tranche3.coinExpectation_mono_parameter
#print axioms Orthemology.Tranche3.bernoulliUpper_mono
#print axioms Orthemology.Tranche3.bernoulliLower_antitone
