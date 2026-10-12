import Mathlib.Analysis.SpecificLimits.Basic
import Mathlib.Computability.Primrec
import Mathlib.Tactic

open Finset Filter Topology
open scoped ENNReal

namespace RationalBinaryWeights

def quotient (a b n : ℕ) : ℕ := a * 2^n / b

def digit (a b n : ℕ) : Bool := decide (quotient a b (n+1) % 2 = 1)

noncomputable def weight (n : ℕ) : ℝ := (1/2 : ℝ)^(n+1)


theorem quotient_step (a b n : ℕ) :
    quotient a b (n+1) / 2 = quotient a b n := by
  unfold quotient
  rw [Nat.div_div_eq_div_mul, pow_succ]
  rw [← Nat.mul_assoc, Nat.mul_div_mul_right _ _ (by decide)]

theorem digit_step (a b n : ℕ) :
    quotient a b (n+1) = 2 * quotient a b n + (if digit a b n then 1 else 0) := by
  have hm := Nat.mod_lt (quotient a b (n+1)) (by decide : 0 < 2)
  have he := Nat.mod_add_div (quotient a b (n+1)) 2
  rw [quotient_step] at he
  unfold digit
  split_ifs with h
  · simp_all
    omega
  · simp_all

theorem digit_primrec (a b : ℕ) : Primrec (digit a b) := by
  have hp := (Primrec₂.unpaired'.mp Nat.Primrec.pow).comp (Primrec.const 2)
    (Primrec.succ : Primrec Nat.succ)
  exact Primrec.eq.comp
    (Primrec.nat_mod.comp
      (Primrec.nat_div.comp (Primrec.nat_mul.comp (Primrec.const a) hp) (Primrec.const b))
      (Primrec.const 2)) (Primrec.const 1)


theorem prefix_sum (a b : ℕ) (hab : a < b) (n : ℕ) :
    ∑ i ∈ range n, (if digit a b i then weight i else 0) =
      (quotient a b n : ℝ) * (1/2 : ℝ)^n := by
  induction n with
  | zero => simp [quotient, Nat.div_eq_of_lt hab]
  | succ n ih =>
    rw [sum_range_succ, ih]
    have hs := digit_step a b n
    have hc : (quotient a b (n+1) : ℝ) =
        2 * (quotient a b n : ℝ) + (if digit a b n then 1 else 0) := by
      exact_mod_cast hs
    rw [hc]
    simp only [weight, pow_succ]
    split_ifs <;> ring

theorem prefix_bounds (a b n : ℕ) (hb : 0 < b) :
    (quotient a b n : ℝ) * (1/2 : ℝ)^n ≤ (a : ℝ) / b ∧
    (a : ℝ) / b ≤ (quotient a b n : ℝ) * (1/2 : ℝ)^n + (1/2 : ℝ)^n := by
  have hbR : (0 : ℝ) < b := by exact_mod_cast hb
  have hp : (0 : ℝ) < 2^n := by positivity
  have hq : b * quotient a b n ≤ a * 2^n := Nat.mul_div_le _ _
  have hu : a * 2^n < b * (quotient a b n + 1) := Nat.lt_mul_div_succ _ hb
  have hqR : (b : ℝ) * (quotient a b n : ℝ) ≤ (a : ℝ) * 2^n := by exact_mod_cast hq
  have huR : (a : ℝ) * 2^n < (b : ℝ) * ((quotient a b n : ℝ) + 1) := by exact_mod_cast hu
  rw [div_pow, one_pow]
  constructor
  · apply (le_div_iff₀ hbR).mpr
    apply (mul_le_mul_right hp).mp
    field_simp
    nlinarith
  · apply (div_le_iff₀ hbR).mpr
    apply (mul_le_mul_right hp).mp
    field_simp
    nlinarith

theorem binary_hasSum (a b : ℕ) (hab : a < b) :
    HasSum (fun i => if digit a b i then weight i else 0) ((a : ℝ) / b) := by
  apply (hasSum_iff_tendsto_nat_of_nonneg (fun i => by
    split_ifs <;> simp [weight]) _).mpr
  simp_rw [prefix_sum a b hab]
  have hz : Tendsto (fun n : ℕ => (1/2 : ℝ)^n) atTop (𝓝 0) :=
    tendsto_pow_atTop_nhds_zero_of_lt_one (by norm_num) (by norm_num)
  have hl : Tendsto (fun n : ℕ => (a : ℝ)/b - (1/2 : ℝ)^n) atTop (𝓝 ((a : ℝ)/b)) := by
    simpa using tendsto_const_nhds.sub hz
  apply tendsto_of_tendsto_of_tendsto_of_le_of_le hl tendsto_const_nhds
  · intro n
    have := (prefix_bounds a b n (by omega)).2
    linarith
  · intro n
    exact (prefix_bounds a b n (by omega)).1

theorem binary_tsum (a b : ℕ) (hab : a < b) :
    (∑' i, if digit a b i then weight i else 0) = (a : ℝ) / b :=
  (binary_hasSum a b hab).tsum_eq

@[simp] theorem digit_zero (b i : ℕ) : digit 0 b i = false := by
  simp [digit, quotient]

theorem weight_hasSum : HasSum weight 1 := by
  have h := (hasSum_geometric_of_lt_one (by norm_num : (0 : ℝ) ≤ 1/2)
    (by norm_num : (1/2 : ℝ) < 1)).mul_left (1/2 : ℝ)
  norm_num at h
  change HasSum (fun i : ℕ => (1/2 : ℝ)^(i+1)) 1
  simpa [pow_succ, mul_comm] using h

/-- Includes the endpoint one by using all digits. -/
def closedDigit (a b i : ℕ) : Bool := if a = b then false else digit a b i

theorem closedDigit_primrec (a b : ℕ) : Primrec (closedDigit a b) := by
  unfold closedDigit
  split_ifs
  · exact Primrec.const true
  · exact digit_primrec a b

theorem closed_binary_hasSum (a b : ℕ) (hb : 0 < b) (hab : a ≤ b) :
    HasSum (fun i => if closedDigit a b i then weight i else 0) ((a : ℝ) / b) := by
  by_cases h : a = b
  · subst a
    simpa [closedDigit, ne_of_gt (show (0 : ℝ) < b by exact_mod_cast hb)] using weight_hasSum
  · simpa [closedDigit, h] using binary_hasSum a b (by omega)

theorem closed_binary_tsum (a b : ℕ) (hb : 0 < b) (hab : a ≤ b) :
    (∑' i, if closedDigit a b i then weight i else 0) = (a : ℝ) / b :=
  (closed_binary_hasSum a b hb hab).tsum_eq

theorem digit_uniform_primrec :
    Primrec (fun p : (ℕ × ℕ) × ℕ => digit p.1.1 p.1.2 p.2) := by
  have ha : Primrec (fun p : (ℕ × ℕ) × ℕ => p.1.1) := Primrec.fst.comp Primrec.fst
  have hb : Primrec (fun p : (ℕ × ℕ) × ℕ => p.1.2) := Primrec.snd.comp Primrec.fst
  have hp := (Primrec₂.unpaired'.mp Nat.Primrec.pow).comp (Primrec.const 2)
    (Primrec.succ.comp (Primrec.snd : Primrec (fun p : (ℕ × ℕ) × ℕ => p.2)))
  exact Primrec.eq.comp
    (Primrec.nat_mod.comp (Primrec.nat_div.comp (Primrec.nat_mul.comp ha hp) hb)
      (Primrec.const 2)) (Primrec.const 1)

theorem closedDigit_uniform_primrec :
    Primrec (fun p : (ℕ × ℕ) × ℕ => closedDigit p.1.1 p.1.2 p.2) := by
  have ha : Primrec (fun p : (ℕ × ℕ) × ℕ => p.1.1) := Primrec.fst.comp Primrec.fst
  have hb : Primrec (fun p : (ℕ × ℕ) × ℕ => p.1.2) := Primrec.snd.comp Primrec.fst
  exact Primrec.ite (Primrec.eq.comp ha hb) (Primrec.const true) digit_uniform_primrec

/-- A concrete primitive-recursive selector for any nonnegative rational at most one. -/
def rationalDigit (q : ℚ≥0) : ℕ → Bool := closedDigit q.num q.den

theorem rationalDigit_primrec (q : ℚ≥0) : Primrec (rationalDigit q) :=
  closedDigit_primrec q.num q.den

theorem rational_binary_tsum (q : ℚ≥0) (hq : q ≤ 1) :
    (∑' i, if rationalDigit q i then weight i else 0) = (q : ℝ) := by
  have hnd : q.num ≤ q.den := by simpa using (NNRat.le_def.mp hq)
  simpa [rationalDigit, NNRat.cast_def] using closed_binary_tsum q.num q.den q.den_pos hnd

theorem closed_binary_tsum_ennreal (a b : ℕ) (hb : 0 < b) (hab : a ≤ b) :
    (∑' i, if closedDigit a b i then (1/2 : ℝ≥0∞)^(i+1) else 0) =
      (a : ℝ≥0∞) / b := by
  have h := ENNReal.ofReal_tsum_of_nonneg (f := fun i => if closedDigit a b i then weight i else 0)
    (fun i => by dsimp; split_ifs <;> simp [weight]) (closed_binary_hasSum a b hb hab).summable
  rw [closed_binary_tsum a b hb hab] at h
  rw [ENNReal.ofReal_div_of_pos (by exact_mod_cast hb), ENNReal.ofReal_natCast,
    ENNReal.ofReal_natCast] at h
  rw [h]
  apply tsum_congr
  intro i
  by_cases hi : closedDigit a b i = true <;>
    simp [hi, weight, ENNReal.ofReal_pow, ENNReal.ofReal_div_of_pos, ENNReal.ofReal_inv_of_pos, ENNReal.inv_pow]

end RationalBinaryWeights

#print axioms RationalBinaryWeights.digit_primrec
#print axioms RationalBinaryWeights.binary_hasSum
#print axioms RationalBinaryWeights.closed_binary_tsum
#print axioms RationalBinaryWeights.closedDigit_uniform_primrec
#print axioms RationalBinaryWeights.rational_binary_tsum
#print axioms RationalBinaryWeights.closed_binary_tsum_ennreal

#print axioms RationalBinaryWeights.rationalDigit_primrec
