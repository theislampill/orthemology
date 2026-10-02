import StatisticUpdateSource

namespace Orthemology.RuntimeBridge.PhaseUpdate
open P02A2.ObserverCore P02A2.PRProgram

def natDistance (a b : ℕ) : ℕ := (a-b)+(b-a)

theorem distance_cast (a b : ℕ) : (natDistance a b : ℚ) = |(a : ℚ)-(b : ℚ)| := by
  by_cases h : a ≤ b
  · have hq : (a : ℚ) ≤ b := by exact_mod_cast h
    simp [natDistance,Nat.sub_eq_zero_of_le h,Nat.cast_sub h,abs_of_nonpos (sub_nonpos.mpr hq)]
  · have hn : b ≤ a := by omega
    have hq : (b : ℚ) ≤ a := by exact_mod_cast hn
    simp [natDistance,Nat.sub_eq_zero_of_le hn,Nat.cast_sub hn,abs_of_nonneg (sub_nonneg.mpr hq)]

/-- Fixed rational row u/v and rational tolerance t/d. Runtime inputs are the
unbounded phase gate k, pair count n, and matching receipt count m. -/
def deviationExpr (t d u v : ℕ) : Expr :=
  let mv := Expr.mul (.reg 2) (.constant v)
  let un := Expr.mul (.constant u) (.reg 1)
  let diff := Expr.add (.sub mv un) (.sub un mv)
  .le (.mul (.constant t) (.mul (.reg 1) (.constant v))) (.mul (.constant d) diff)

def gateExpr (t d u v : ℕ) : Expr :=
  .mul (.sub (.constant 1) (.le (.reg 1) (.reg 0))) (deviationExpr t d u v)

def gateProgram (t d u v : ℕ) : Program 3 := ⟨.set 3 (gateExpr t d u v),3⟩

theorem rational_cross_gate (t d u v n m : ℕ) (hd : 0 < d) (hv : 0 < v) (hn : 0 < n) :
    (t : ℚ)/d ≤ |(m : ℚ)/n - (u : ℚ)/v| ↔
      t*n*v ≤ d*natDistance (m*v) (u*n) := by
  have hdq : (0 : ℚ) < d := by exact_mod_cast hd
  have hvq : (0 : ℚ) < v := by exact_mod_cast hv
  have hnq : (0 : ℚ) < n := by exact_mod_cast hn
  have hx : (m : ℚ)/n-(u : ℚ)/v = ((m : ℚ)*v-u*n)/(n*v) := by
    field_simp
    ring
  rw [hx,abs_div,abs_of_pos (mul_pos hnq hvq),div_le_div_iff₀ hdq (mul_pos hnq hvq)]
  have hc := distance_cast (m*v) (u*n)
  push_cast at hc
  rw [← hc]
  norm_cast
  simp [Nat.mul_assoc,Nat.mul_comm,Nat.mul_left_comm]

/-- A literal P02 arithmetic guard equals the retained empirical coordinate
condition. Zero counts are rejected by the strict phase gate before comparison. -/
theorem gate_source_exact (t d u v : ℕ) (hd : 0 < d) (hv : 0 < v) (k n m : ℕ) :
    denote (gateProgram t d u v) ![k,n,m] =
      bitNat (decide (k < n ∧ (t : ℚ)/d ≤ |(m : ℚ)/n-(u : ℚ)/v|)) := by
  by_cases h : k < n
  · have hn : 0 < n := by omega
    have hc := rational_cross_gate t d u v n m hd hv hn
    have hnle : ¬ n ≤ k := by omega
    simp [denote,gateProgram,gateExpr,deviationExpr,exec,evalExpr,P02A2.LoopPrimrec.extend,
      hnle,h,bitNat,natDistance,hc,Nat.mul_assoc]
  · have hnle : n ≤ k := by omega
    simp [denote,gateProgram,gateExpr,deviationExpr,exec,evalExpr,P02A2.LoopPrimrec.extend,hnle,h,bitNat]

end Orthemology.RuntimeBridge.PhaseUpdate
