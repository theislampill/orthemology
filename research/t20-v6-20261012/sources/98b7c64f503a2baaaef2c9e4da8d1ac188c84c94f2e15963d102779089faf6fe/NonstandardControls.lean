import NonstandardRejection
import DomainControls
namespace NonstandardReview
open OpenTermStandardness OpenDevelopments NonstandardRejection

-- Literal raw zero differs from the Church numeral zero K I.
example : literalZero ≠ P01AC.EffectiveCompleteness.inputNumeral 0 := by
  simp [literalZero, P01AC.EffectiveCompleteness.inputNumeral,
    P01AC.EffectiveCompleteness.iterationPoly, P01D.abstract, P01D.freeZero,
    P01D.drop, P01D.pren, P01D.psub]
example : normalB (.app (.app .zero (.var 1)) (.var 0)) = true := rfl
example : normalB (.app .i (.var 0)) = false := rfl
example : normalB (.app (.var 42) (.app .i (.var 0))) = false := rfl
example : normalB (.app (.app .i (.var 42)) (.var 0)) = false := rfl
example : normalB (.app (.app (.app .s (.var 1)) (.var 2)) (.var 3)) = false := rfl
example : normalB (.app (.app .s (.var 1)) (.var 2)) = true := rfl

-- Executable successful negative premises conclude only this input-domain negation.
theorem exact_negative (n : P01D.Poly) (z : T) (p : List P01Certificate.Address)
    (hr : (ScalarCertificates.replayTo (ImportedOpenTermTransport.interp
      (ClosedScalarInstances.scalarLeft n) T.var) z p).isSome = true)
    (hn : normalB z = true) (hi : readIteration z = none) :
    ¬ P01AC.ExtensionalRepair.HasE [] n P01AC.EffectiveCompleteness.N :=
  checked_non_iteration_refutes n z p hr hn hi

-- The positive theorem includes a reducible/divergent source input; false
-- normality or exhausted search is not a typing rejection premise.
example : P01AC.ExtensionalRepair.HasE []
    (OpenDevelopments.DomainControls.padded 0) P01AC.EffectiveCompleteness.N :=
  OpenDevelopments.DomainControls.padded_has 0

#print axioms exact_negative
end NonstandardReview
