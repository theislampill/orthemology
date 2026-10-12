import LiteralShiftWeights
import LiteralShiftMixture

/-! End-to-end probability correctness of the reconstructed original literal
selector/replay AST, using its actual fair-source output and actual atomic
defect. All selector probabilities and the exceptional null branch are derived.
The original Python source-to-AST transcription remains a separate boundary. -/
namespace P02.LiteralShift
open Set MeasureTheory P02A2 P02A2.Q8Measure P02A2.ObserverCore
open scoped ENNReal NNReal

/-- The original literal compiler's exact stopping-prefix mixture, with the
unresolved-null premise discharged by its own selector analysis. -/
theorem compileShift_probability_law (body : Stmt) (output a b : ℕ) (hb : 0 < b) :
    fairCantor.map (compiledOutput body output a b) =
      Measure.sum (fun l : StopLeaf a b => leafWeight l • leafLaw body output l) :=
  literal_shift_mixture_law body output a b (fair_unresolved a b hb)

/-- Exact total coefficient of the actual above stopping cylinders. -/
theorem compileShift_above_weight (a b : ℕ) (hb : 0 < b) (hab : a ≤ b) :
    (∑' l : StopLeaf a b, if l.1.2.2 then (leafWeight l : ℝ≥0∞) else 0) =
      1 - (a : ℝ≥0∞) / b := by
  rw [← above_event_probability_sum, fair_firstCut_above a b hb hab]

/-- The actual stopping cylinders exhaust fair measure, despite a possible
indefinitely unresolved input. -/
theorem compileShift_total_weight (a b : ℕ) (hb : 0 < b) :
    (∑' l : StopLeaf a b, (leafWeight l : ℝ≥0∞)) = 1 := by
  have h := congrArg (fun μ : Measure Cantor => μ univ)
    (fairCantor_sum_leaf_restrict a b (fair_unresolved a b hb))
  simpa [Measure.sum_apply, Measure.restrict_apply, leafEvent_probability] using h.symm

/-- Exact total coefficient of the actual below stopping cylinders. -/
theorem compileShift_below_weight (a b : ℕ) (hb : 0 < b) (hab : a ≤ b) :
    (∑' l : StopLeaf a b, if l.1.2.2 then 0 else (leafWeight l : ℝ≥0∞)) =
      (a : ℝ≥0∞) / b := by
  have hp : (∑' l : StopLeaf a b, if l.1.2.2 then 0 else (leafWeight l : ℝ≥0∞)) +
      (∑' l : StopLeaf a b, if l.1.2.2 then (leafWeight l : ℝ≥0∞) else 0) = 1 := by
    rw [← ENNReal.tsum_add]
    convert compileShift_total_weight a b hb using 1
    apply tsum_congr
    intro l
    split <;> simp
  have hq : (a : ℝ≥0∞)/b ≤ 1 := ENNReal.div_le_of_le_mul (by
    simpa using (show (a : ℝ≥0∞) ≤ b by exact_mod_cast hab))
  rw [compileShift_above_weight a b hb hab] at hp
  have h := ENNReal.eq_sub_of_add_eq' (by norm_num : (1 : ℝ≥0∞) ≠ ∞) hp
  exact h.trans (ENNReal.sub_sub_cancel (by simp) hq)

/-- The source-lowered literal compiler's actual output atomic mass. -/
theorem compileShift_atomic_mass (body : Stmt) (output a b : ℕ)
    (hb : 0 < b) (hab : a ≤ b) :
    mass (fairCantor.map (compiledOutput body output a b)) =
      (1 - (a : ℝ≥0∞)/b) *
        mass (fairCantor.map (P02A2.ObserverCore.output (programValue body output))) := by
  rw [literal_shift_atomic_mass body output a b (fair_unresolved a b hb),
    fair_firstCut_above a b hb hab]

/-- End-to-end affine defect correctness for every literal base AST, output
register and accepted rational parameter, including unreduced denominators. -/
theorem compileShift_defect (body : Stmt) (output a b : ℕ)
    (hb : 0 < b) (hab : a ≤ b) :
    defect (fairCantor.map (compiledOutput body output a b)) =
      (a : ℝ)/b + (1 - (a : ℝ)/b) *
        defect (fairCantor.map (P02A2.ObserverCore.output (programValue body output))) := by
  have hq : (a : ℝ≥0∞)/b ≤ 1 := ENNReal.div_le_of_le_mul (by
    simpa using (show (a : ℝ≥0∞) ≤ b by exact_mod_cast hab))
  rw [literal_shift_defect_by_above_probability body output a b (fair_unresolved a b hb),
    fair_firstCut_above a b hb hab,
    ENNReal.toReal_sub_of_le hq (by simp)]
  simp only [ENNReal.toReal_one, ENNReal.toReal_div, ENNReal.toReal_natCast]
  ring

theorem compileShift_zero_defect (body : Stmt) (output b : ℕ) (hb : 0 < b) :
    defect (fairCantor.map (compiledOutput body output 0 b)) =
      defect (fairCantor.map (P02A2.ObserverCore.output (programValue body output))) := by
  simpa using compileShift_defect body output 0 b hb (Nat.zero_le b)

theorem compileShift_one_defect (body : Stmt) (output b : ℕ) (hb : 0 < b) :
    defect (fairCantor.map (compiledOutput body output b b)) = 1 := by
  have hbR : (b : ℝ) ≠ 0 := by exact_mod_cast (Nat.ne_of_gt hb)
  simpa [hbR] using compileShift_defect body output b b hb le_rfl

end P02.LiteralShift
#print axioms P02.LiteralShift.compileShift_defect
