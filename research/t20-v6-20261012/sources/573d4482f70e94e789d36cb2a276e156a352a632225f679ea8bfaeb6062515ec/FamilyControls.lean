import CodeBoundary

namespace SourceFamilyComputability
open P01D P01AC P01AC.EffectiveCompleteness P01AC.BooleanPrimitive Encodable FullPERTests

/-- The recurrence has the literal zero numeral as its base. -/
example : numeralCode 0 = encode (Poly.app (.atom .k) (.atom .i)) := by
  rw [numeralCode_exact, inputNumeral_zero]

/-- The first two successors exercise the exact bracket-abstraction recurrence. -/
example : inputNumeral 1 = .app numeralStep (.app (.atom .k) (.atom .i)) := by
  rw [show 1 = 0+1 from rfl, inputNumeral_succ, inputNumeral_zero]
example : inputNumeral 2 =
    .app numeralStep (.app numeralStep (.app (.atom .k) (.atom .i))) := by
  rw [show 2 = 1+1 from rfl, inputNumeral_succ,
    show 1 = 0+1 from rfl, inputNumeral_succ, inputNumeral_zero]

theorem numeral_zero_ne_one : inputNumeral 0 ≠ inputNumeral 1 := by
  rw [show 1 = 0+1 from rfl, inputNumeral_succ, inputNumeral_zero]
  decide

/-- An exact encoding cannot collapse distinct source numerals. -/
example : encode (inputNumeral 0) ≠ encode (inputNumeral 1) :=
  fun h => numeral_zero_ne_one (encode_injective h)

/-- The checked family map really retains the machine-index syntax. -/
theorem family_zero_ne_one (f : PR 2) : encode (programType f 0) ≠ encode (programType f 1) := by
  intro h
  have hs := encode_injective h
  simp only [programType, testType, testBody, simFamily, Ty.pi.injEq, Ty.identity.injEq,
    Poly.app.injEq, true_and, and_true] at hs
  exact numeral_zero_ne_one hs

/-- Reject confusing a polynomial-application tag with a type-Pi tag. -/
example (a b : Nat) : appCode a b ≠ piCode a b := by
  simp [appCode, piCode, node, leaf, Nat.pair_eq_pair]

/-- Both theorem signatures are unconditional at the natural-code boundary. -/
example (f : PR 2) : Primrec (fun e => encode (programType f e)) :=
  primrec_encode_programType f
example : ¬ REPred codedFormedHolds := codedFormedHolds_not_re

#print axioms family_zero_ne_one
end SourceFamilyComputability
