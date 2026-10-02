import ANDScore

noncomputable section
open scoped BigOperators
open Set PolynomialAND ANDCorrection ANDScore

namespace PolynomialBounds

def value {n : ℕ} (c : Fin n → ℝ) (eps : ℝ) : ℝ := ∑ i, c i*eps^(i.val)
def budget {n : ℕ} (c : Fin n → ℝ) : ℝ := ∑ i, |c i|

lemma budget_nonneg {n : ℕ} (c : Fin n → ℝ) : 0  ≤  budget c :=
  Finset.sum_nonneg (fun i _ => abs_nonneg (c i))

lemma value_bound {n : ℕ} (c : Fin n → ℝ) (eps : ℝ) (he0 : 0  ≤  eps) (he1 : eps  ≤  1) :
    |value c eps|  ≤  budget c := by
  calc
    |value c eps|  ≤  ∑ i, |c i*eps^(i.val)| := Finset.abs_sum_le_sum_abs _ _
    _  ≤  budget c := by
      apply Finset.sum_le_sum
      intro i _
      rw [abs_mul,abs_of_nonneg (pow_nonneg he0 _)]
      exact mul_le_of_le_one_right (abs_nonneg _) (pow_le_one₀ he0 he1)

lemma coordinate_bound {n : ℕ} (c : Fin n → ℝ) (i : Fin n) : |c i|  ≤  budget c :=
  Finset.single_le_sum (fun j _ => abs_nonneg (c j)) (Finset.mem_univ i)

def gCoefficients (h1 h2 hz hw b g : ℝ) : Fin 2 → ℝ :=
  ![-b*(h1+h2)-g*(hz+hw),-(b^2+g^2)]

def fCoefficients (s a h1 h2 hz hw b g : ℝ) : Fin 6 → ℝ :=
  let m := mean h1 h2
  let d2 := 1+144*s^2-96*a*s
  let d3 := 48*s-16*a
  ![d3*(h1^3+h2^3-2*m^3)-2*d2*m*b-100*g*(hz+hw),
    12*(h1^4+h2^4-2*m^4)-d2*b^2-6*d3*m^2*b-100*g^2,
    -6*d3*m*b^2-96*m^3*b,
    -2*d3*b^3-144*m^2*b^2,
    -96*m*b^3,-24*b^4]

lemma gRem_eq_value (h1 h2 hz hw b g eps : ℝ) :
    gRem h1 h2 hz hw b g eps=value (gCoefficients h1 h2 hz hw b g) eps := by
  simp [value,gCoefficients,gRem,Fin.sum_univ_succ]
  ring

lemma fRem_eq_value (s a h1 h2 hz hw b g eps : ℝ) :
    fRem s a h1 h2 hz hw b g eps=value (fCoefficients s a h1 h2 hz hw b g) eps := by
  simp [value,fCoefficients,fRem,Fin.sum_univ_succ]
  ring

lemma gRem_bound (h1 h2 hz hw b g eps : ℝ) (he0 : 0  ≤  eps) (he1 : eps  ≤  1) :
    |gRem h1 h2 hz hw b g eps| ≤ budget (gCoefficients h1 h2 hz hw b g) := by
  rw [gRem_eq_value]
  exact value_bound _ eps he0 he1

lemma fRem_bound (s a h1 h2 hz hw b g eps : ℝ) (he0 : 0  ≤  eps) (he1 : eps  ≤  1) :
    |fRem s a h1 h2 hz hw b g eps| ≤ budget (fCoefficients s a h1 h2 hz hw b g) := by
  rw [fRem_eq_value]
  exact value_bound _ eps he0 he1

/-- A fully explicit scale converts an exact polynomial leading margin into
an actual strict gain. No continuity choice or hidden remainder modulus. -/
lemma strict_gain_of_budget (lead m remainder M eps : ℝ)
    (hm : 0 < m) (hM : 0 ≤ M) (hlead : m ≤ lead) (hR : |remainder| ≤ M)
    (he : 0 < eps) (hscale : eps < m/(2*(M+1))) :
    0 < eps^2*(lead+eps*remainder) := by
  have hd : 0 < 2*(M+1) := by positivity
  have hs := (lt_div_iff₀ hd).mp hscale
  have hlo : -M ≤ remainder := neg_le_of_abs_le hR
  have hmul := mul_le_mul_of_nonneg_left hlo he.le
  have hp : 0 < lead+eps*remainder := by nlinarith
  exact mul_pos (pow_pos he 2) hp

#print axioms strict_gain_of_budget
end PolynomialBounds
