import Mathlib.Data.Real.Sqrt
import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Tactic

open scoped BigOperators

namespace Orthemology.Tranche2

/-- Finite-experiment affinity. The two probability vectors are explicit. -/
noncomputable def affinity {ι : Type*} [Fintype ι] (p q : ι → ℝ) : ℝ :=
  ∑ i, Real.sqrt (p i) * Real.sqrt (q i)

/-- Probability of error when the true model is p and t is the probability of selecting p. -/
def errorP {ι : Type*} [Fintype ι] (p t : ι → ℝ) : ℝ := ∑ i, p i * (1 - t i)

/-- Probability of error when the true model is q. -/
def errorQ {ι : Type*} [Fintype ι] (q t : ι → ℝ) : ℝ := ∑ i, q i * t i

lemma minimum_le_test_error (p q t : ℝ) (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    min p q ≤ p * (1-t) + q*t := by
  have hp := min_le_left p q
  have hq := min_le_right p q
  nlinarith

lemma sqrt_product_min_max (p q : ℝ) (hp : 0 ≤ p) (hq : 0 ≤ q) :
    Real.sqrt p * Real.sqrt q = Real.sqrt (min p q) * Real.sqrt (max p q) := by
  rcases le_total p q with h | h
  · simp [min_eq_left h, max_eq_right h]
  · simp [min_eq_right h, max_eq_left h, mul_comm]

/-- A finite testing obstruction with a randomized test. -/
theorem affinity_sq_le_twice_error_sum {ι : Type*} [Fintype ι]
    (p q t : ι → ℝ) (hp : ∀ i, 0 ≤ p i) (hq : ∀ i, 0 ≤ q i)
    (hsP : ∑ i, p i = 1) (hsQ : ∑ i, q i = 1)
    (ht0 : ∀ i, 0 ≤ t i) (ht1 : ∀ i, t i ≤ 1) :
    affinity p q ^ 2 ≤ 2 * (errorP p t + errorQ q t) := by
  let a : ι → ℝ := fun i => Real.sqrt (min (p i) (q i))
  let b : ι → ℝ := fun i => Real.sqrt (max (p i) (q i))
  have ha : ∀ i, a i ^ 2 = min (p i) (q i) := by
    intro i
    exact Real.sq_sqrt (le_min (hp i) (hq i))
  have hb : ∀ i, b i ^ 2 = max (p i) (q i) := by
    intro i
    exact Real.sq_sqrt ((hp i).trans (le_max_left _ _))
  have hab : affinity p q = ∑ i, a i * b i := by
    apply Finset.sum_congr rfl
    intro i _
    exact sqrt_product_min_max _ _ (hp i) (hq i)
  have hc := Finset.sum_mul_sq_le_sq_mul_sq Finset.univ a b
  rw [← hab] at hc
  simp_rw [ha, hb] at hc
  have hmin0 : 0 ≤ ∑ i, min (p i) (q i) :=
    Finset.sum_nonneg fun i _ => le_min (hp i) (hq i)
  have hsum : (∑ i, min (p i) (q i)) + (∑ i, max (p i) (q i)) = 2 := by
    rw [← Finset.sum_add_distrib]
    simp_rw [min_add_max]
    rw [Finset.sum_add_distrib, hsP, hsQ]
    norm_num
  have he : (∑ i, min (p i) (q i)) ≤ errorP p t + errorQ q t := by
    rw [errorP, errorQ, ← Finset.sum_add_distrib]
    exact Finset.sum_le_sum fun i _ => minimum_le_test_error _ _ _ (ht0 i) (ht1 i)
  nlinarith [sq_nonneg (∑ i, min (p i) (q i))]

theorem affinity_error_lower_bound {ι : Type*} [Fintype ι]
    (p q t : ι → ℝ) (hp : ∀ i, 0 ≤ p i) (hq : ∀ i, 0 ≤ q i)
    (hsP : ∑ i, p i = 1) (hsQ : ∑ i, q i = 1)
    (ht0 : ∀ i, 0 ≤ t i) (ht1 : ∀ i, t i ≤ 1) :
    affinity p q ^ 2 / 4 ≤ max (errorP p t) (errorQ q t) := by
  have h := affinity_sq_le_twice_error_sum p q t hp hq hsP hsQ ht0 ht1
  have h1 := le_max_left (errorP p t) (errorQ q t)
  have h2 := le_max_right (errorP p t) (errorQ q t)
  linarith

end Orthemology.Tranche2

namespace Orthemology.Tranche2

lemma affinity_nonneg {ι : Type*} [Fintype ι] (p q : ι → ℝ) : 0 ≤ affinity p q := by
  exact Finset.sum_nonneg fun i _ => mul_nonneg (Real.sqrt_nonneg _) (Real.sqrt_nonneg _)

lemma affinity_tensor {ι κ : Type*} [Fintype ι] [Fintype κ]
    (p q : ι → ℝ) (r s : κ → ℝ)
    (hp : ∀ i, 0 ≤ p i) (hq : ∀ i, 0 ≤ q i) :
    affinity (fun x : ι × κ => p x.1 * r x.2)
      (fun x : ι × κ => q x.1 * s x.2) = affinity p q * affinity r s := by
  unfold affinity
  rw [Fintype.sum_prod_type, Finset.sum_mul]
  apply Finset.sum_congr rfl
  intro i _
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro j _
  rw [Real.sqrt_mul (hp i), Real.sqrt_mul (hq i)]
  ring

/-- An explicit finite product space for n Bernoulli observations. -/
def Bits : ℕ → Type
  | 0 => Unit
  | n+1 => Bool × Bits n

instance bitsFintype : (n : ℕ) → Fintype (Bits n)
  | 0 => inferInstanceAs (Fintype Unit)
  | n+1 => @instFintypeProd Bool (Bits n) inferInstance (bitsFintype n)

def coinMass (p : ℝ) (b : Bool) : ℝ := if b then p else 1-p

def bernoulliMass : (n : ℕ) → ℝ → Bits n → ℝ
  | 0, _, _ => 1
  | n+1, p, x => coinMass p x.1 * bernoulliMass n p x.2

lemma coinMass_nonneg (p : ℝ) (hp0 : 0 ≤ p) (hp1 : p ≤ 1) (b : Bool) :
    0 ≤ coinMass p b := by
  cases b <;> simp [coinMass] <;> linarith

lemma bernoulliMass_nonneg (n : ℕ) (p : ℝ) (hp0 : 0 ≤ p) (hp1 : p ≤ 1) :
    ∀ w, 0 ≤ bernoulliMass n p w := by
  induction n with
  | zero => intro w; norm_num [bernoulliMass]
  | succ n ih =>
      intro w
      exact mul_nonneg (coinMass_nonneg p hp0 hp1 w.1) (ih w.2)

lemma bernoulliMass_sum (n : ℕ) (p : ℝ) : ∑ w, bernoulliMass n p w = 1 := by
  induction n with
  | zero => simp [bernoulliMass, Bits]
  | succ n ih =>
      change (∑ w : Bool × Bits n, coinMass p w.1 * bernoulliMass n p w.2) = 1
      rw [Fintype.sum_prod_type]
      simp_rw [← Finset.mul_sum, ih]
      simp [coinMass]

lemma coin_affinity (p q : ℝ) : affinity (coinMass p) (coinMass q) =
    Real.sqrt (1-p) * Real.sqrt (1-q) + Real.sqrt p * Real.sqrt q := by
  simp [affinity, coinMass, add_comm]

lemma bernoulli_affinity (n : ℕ) (p q : ℝ)
    (hp0 : 0 ≤ p) (hp1 : p ≤ 1) (hq0 : 0 ≤ q) (hq1 : q ≤ 1) :
    affinity (bernoulliMass n p) (bernoulliMass n q) =
      (affinity (coinMass p) (coinMass q)) ^ n := by
  induction n with
  | zero => simp [affinity, bernoulliMass, Bits]
  | succ n ih =>
      change affinity (fun w : Bool × Bits n => coinMass p w.1 * bernoulliMass n p w.2)
        (fun w : Bool × Bits n => coinMass q w.1 * bernoulliMass n q w.2) = _
      rw [affinity_tensor _ _ _ _ (coinMass_nonneg p hp0 hp1) (coinMass_nonneg q hq0 hq1), ih]
      rw [pow_succ]
      ring

lemma symmetric_coin_affinity_sq (e : ℝ) (he0 : 0 ≤ e) (he1 : e ≤ 1/2) :
    affinity (coinMass (1/2-e)) (coinMass (1/2+e)) ^ 2 = 1 - 4*e^2 := by
  rw [coin_affinity]
  have h1 : 1 - (1/2-e) = 1/2+e := by ring
  have h2 : 1 - (1/2+e) = 1/2-e := by ring
  rw [h1,h2]
  have hm : 0 ≤ (1/2:ℝ)-e := by linarith
  have hp : 0 ≤ (1/2:ℝ)+e := by linarith
  have sm := Real.sq_sqrt hm
  have sp := Real.sq_sqrt hp
  nlinarith [sq_nonneg (Real.sqrt (1/2-e) * Real.sqrt (1/2+e))]

/-- Exact finite-sample testing lower bound for two symmetric Bernoulli standards.
A t-valued randomized test includes arbitrary parameter-independent randomization
conditional on the observed sample. -/
theorem symmetric_bernoulli_test_lower_bound (n : ℕ) (e : ℝ)
    (he0 : 0 ≤ e) (he1 : e ≤ 1/2) (t : Bits n → ℝ)
    (ht0 : ∀ w, 0 ≤ t w) (ht1 : ∀ w, t w ≤ 1) :
    (1-4*e^2)^n / 4 ≤
      max (errorP (bernoulliMass n (1/2-e)) t)
          (errorQ (bernoulliMass n (1/2+e)) t) := by
  have hm0 : 0 ≤ (1/2:ℝ)-e := by linarith
  have hm1 : (1/2:ℝ)-e ≤ 1 := by linarith
  have hp0 : 0 ≤ (1/2:ℝ)+e := by linarith
  have hp1 : (1/2:ℝ)+e ≤ 1 := by linarith
  have h := affinity_error_lower_bound (bernoulliMass n (1/2-e))
    (bernoulliMass n (1/2+e)) t
    (bernoulliMass_nonneg n _ hm0 hm1) (bernoulliMass_nonneg n _ hp0 hp1)
    (bernoulliMass_sum n _) (bernoulliMass_sum n _) ht0 ht1
  rw [bernoulli_affinity n _ _ hm0 hm1 hp0 hp1] at h
  rw [← pow_mul, Nat.mul_comm n 2, pow_mul, symmetric_coin_affinity_sq e he0 he1] at h
  exact h

end Orthemology.Tranche2

#print axioms Orthemology.Tranche2.affinity_sq_le_twice_error_sum
#print axioms Orthemology.Tranche2.affinity_error_lower_bound
#print axioms Orthemology.Tranche2.affinity_tensor
#print axioms Orthemology.Tranche2.bernoulliMass_sum
#print axioms Orthemology.Tranche2.bernoulli_affinity
#print axioms Orthemology.Tranche2.symmetric_bernoulli_test_lower_bound
#check Orthemology.Tranche2.symmetric_bernoulli_test_lower_bound
