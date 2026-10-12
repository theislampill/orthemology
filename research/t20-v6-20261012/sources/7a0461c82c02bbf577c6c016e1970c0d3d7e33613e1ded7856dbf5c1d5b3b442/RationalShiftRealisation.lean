import UnaryShiftLaw
import BinaryWeights
import UnaryPrefixRealisation
import FiniteOutputTable
import Pi3Program

/-! Alternative rational unary-tag shift realised in the original P02-L1
numeric evaluator. This does not identify the Python compile_shift syntax.
Only a fixed jointly PR family is compiled; no universal PR evaluator occurs. -/

namespace OrthemologyRationalShift
open P02A2 P02A2.ObserverCore P02A2.Q8Measure P02A2.PRProgram P02.Codec
open OrthemologyTagged RationalBinaryWeights

theorem rational_unaryShift_defect (a b : ℕ) (hb : 0 < b) (hab : a ≤ b)
    {base : Cantor → Cantor} (hm : Measurable base) :
    defect (fairCantor.map (unaryShift (closedDigit a b) base)) =
      (a : ℝ)/b + (1-(a : ℝ)/b) * defect (fairCantor.map base) := by
  apply unaryShift_defect_of_weight _ hm
  simpa [RationalBinaryWeights.weight] using closed_binary_tsum a b hb hab

/-- A fixed jointly PR family has actual numeric output laws with exactly the
rational affine defect. The numeric parameter transformer is primitive recursive. -/
theorem exists_primrec_rational_shift (F : ℕ → ℕ → ℕ → ℕ)
    (hF : Primrec₂ (fun p : ℕ × ℕ => F p.1 p.2))
    (a b : ℕ) (hb : 0 < b) (hab : a ≤ b) :
    ∃ p : Program 3, Primrec (parameterIndex p) ∧ ∀ e,
      output (evaluateIndex (parameterIndex p e)) =
        unaryShift (closedDigit a b) (output (F e)) ∧
      defect (fairCantor.map (output (evaluateIndex (parameterIndex p e)))) =
        (a : ℝ)/b + (1-(a : ℝ)/b) * defect (fairCantor.map (output (F e))) := by
  obtain ⟨p,hp,he⟩ := UnaryPrefix.exists_primrec_numeric_family F (closedDigit a b)
    hF (closedDigit_primrec a b)
  refine ⟨p,hp,fun e => ?_⟩
  have ho : output (evaluateIndex (parameterIndex p e)) =
      unaryShift (closedDigit a b) (output (F e)) := he e
  refine ⟨ho,?_⟩
  rw [ho]
  exact rational_unaryShift_defect a b hb hab (P02A2.FiniteOutputTable.output_measurable _)

/-- Composition with the existing Pi3 family. This is kernel assurance of an
alternative lower reduction, not a new ordinary threshold classification. -/
theorem exists_primrec_pi3_threshold_reduction
    (R : ℕ → ℕ → ℕ → ℕ → Prop) [∀ e i, DecidableRel (R e i)]
    (hR : PrimrecRel (fun p : (ℕ × ℕ) × ℕ => R p.1.1 p.1.2 p.2))
    (a b : ℕ) (hab : a < b) :
    ∃ f : ℕ → ℕ, Primrec f ∧ ∀ e,
      (defect (fairCantor.map (output (evaluateIndex (f e)))) = (a : ℝ)/b ↔
        ∀ i, ∃ s, ∀ t, R e i s t) ∧
      (defect (fairCantor.map (output (evaluateIndex (f e)))) ≤ (a : ℝ)/b ↔
        ∀ i, ∃ s, ∀ t, R e i s t) ∧
      ((a : ℝ)/b < defect (fairCantor.map (output (evaluateIndex (f e)))) ↔
        ∃ i, ∀ s, ∃ t, ¬ R e i s t) := by
  have hb : 0 < b := by omega
  have hq : (a : ℝ)/b < 1 := (div_lt_one (by exact_mod_cast hb)).mpr (by exact_mod_cast hab)
  obtain ⟨p,hp,hpLaw⟩ := exists_primrec_rational_shift (pi3PrefixValue R)
    (pi3PrefixValue_primrec R hR) a b hb (Nat.le_of_lt hab)
  refine ⟨parameterIndex p,hp,fun e => ?_⟩
  have hlaw := (hpLaw e).2
  rw [pi3PrefixValue_output] at hlaw
  have hnonneg : 0 ≤ defect (fairCantor.map (pi3Observer R e)) := pi3_defect_nonnegative R e
  rw [hlaw, shift_eq_threshold _ _ hq,
    shift_le_threshold _ _ hq hnonneg]
  refine ⟨pi3_zero_defect_iff R e, pi3_zero_defect_iff R e, ?_⟩
  exact (shift_gt_threshold ((a : ℝ)/b) (defect (fairCantor.map (pi3Observer R e))) hq).trans
    (pi3_positive_defect_iff R e)

end OrthemologyRationalShift
#print axioms OrthemologyRationalShift.exists_primrec_rational_shift

#print axioms OrthemologyRationalShift.exists_primrec_pi3_threshold_reduction
