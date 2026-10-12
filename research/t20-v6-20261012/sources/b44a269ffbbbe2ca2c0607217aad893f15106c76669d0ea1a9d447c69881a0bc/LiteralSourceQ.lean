import ScalarCertificates
set_option maxRecDepth 32768
set_option maxHeartbeats 8000000
namespace ScalarCertificates
def literalSourceQ : P01D.Poly := (.app (.app (.atom .s) (.app (.app (.atom .s) (.app (.app (.atom .s) (.atom .i)) (.app (.atom .k) (.app (.app (.atom .s) (.app (.app (.atom .s) (.app (.atom .k) (.atom .s))) (.app (.app (.atom .s) (.app (.atom .k) (.app (.atom .s) (.atom .i)))) (.app (.app (.atom .s) (.app (.atom .k) (.atom .k))) (.app (.app (.atom .s) (.app (.atom .k) (.app (.app (.atom .s) (.app (.atom .k) (.app (.atom .s) (.app (.app (.atom .s) (.app (.atom .k) (.atom .s))) (.app (.app (.atom .s) (.app (.atom .k) (.atom .k))) (.atom .i)))))) (.app (.app (.atom .s) (.app (.app (.atom .s) (.app (.atom .k) (.atom .s))) (.app (.app (.atom .s) (.app (.atom .k) (.app (.atom .s) (.app (.atom .k) (.atom .s))))) (.app (.app (.atom .s) (.app (.atom .k) (.app (.atom .s) (.app (.atom .k) (.atom .k))))) (.app (.app (.atom .s) (.app (.app (.atom .s) (.app (.atom .k) (.atom .s))) (.app (.app (.atom .s) (.app (.atom .k) (.atom .k))) (.atom .i)))) (.app (.atom .k) (.atom .i))))))) (.app (.atom .k) (.app (.atom .k) (.atom .i))))))) (.app (.app (.atom .s) (.atom .i)) (.app (.atom .k) (.atom .k)))))))) (.app (.app (.atom .s) (.app (.atom .k) (.atom .k))) (.app (.app (.atom .s) (.app (.atom .k) (.app (.app (.atom .s) (.app (.atom .k) (.app (.atom .s) (.app (.app (.atom .s) (.app (.atom .k) (.atom .s))) (.app (.app (.atom .s) (.app (.atom .k) (.atom .k))) (.atom .i)))))) (.app (.app (.atom .s) (.app (.app (.atom .s) (.app (.atom .k) (.atom .s))) (.app (.app (.atom .s) (.app (.atom .k) (.app (.atom .s) (.app (.atom .k) (.atom .s))))) (.app (.app (.atom .s) (.app (.atom .k) (.app (.atom .s) (.app (.atom .k) (.atom .k))))) (.app (.app (.atom .s) (.app (.app (.atom .s) (.app (.atom .k) (.atom .s))) (.app (.app (.atom .s) (.app (.atom .k) (.atom .k))) (.atom .i)))) (.app (.atom .k) (.atom .i))))))) (.app (.atom .k) (.app (.atom .k) (.atom .i))))))) (.app (.app (.atom .s) (.atom .i)) (.app (.atom .k) (.app (.atom .k) (.atom .i)))))))))) (.app (.atom .k) (.app (.app (.atom .s) (.app (.app (.atom .s) (.atom .i)) (.app (.atom .k) (.app (.atom .k) (.atom .i))))) (.app (.atom .k) (.app (.atom .k) (.atom .i))))))) (.app (.atom .k) (.app (.atom .k) (.atom .i))))
theorem originalQ_expanded : FullPER.Application.originalQ = literalSourceQ := by
  unfold FullPER.Application.originalQ
  rw [P01AC.ExtensionalRepair.CompilerBodyControl.redundant_closed_exact]
  simp [literalSourceQ,
    P01AC.ExtensionalRepair.CompilerBodyControl.literalPairStateBody,
    P01AC.ExtensionalRepair.CompilerBodyControl.diagonalStep,
    P01AC.ExtensionalRepair.CompilerBodyControl.diagonalStepBody,
    P01AC.ExtensionalRepair.CompilerBodyControl.diagonalZero,
    P01AC.BooleanPrimitive.succPoly, P01AC.BooleanPrimitive.succBody,
    P01AC.EffectiveCompleteness.inputNumeral, P01AC.EffectiveCompleteness.iterationPoly,
    P01D.pairPoly, P01D.fstPoly, P01D.sndPoly,
    P01D.abstract, P01D.freeZero, P01D.drop, P01D.pren, P01D.psub]
#print axioms originalQ_expanded
end ScalarCertificates
