import LiteralSourceQ
set_option maxRecDepth 32768
set_option maxHeartbeats 8000000
def changed_input_n : P01D.Poly := (.app (.app (.atom .s) (.app (.app (.atom .s) (.app (.atom .k) (.atom .s))) (.app (.app (.atom .s) (.app (.atom .k) (.atom .k))) (.atom .i)))) (.app (.atom .k) (.atom .i)))
def changed_input_l : List P01Certificate.Address := [[.left],[]]
def changed_input_r : List P01Certificate.Address := [[.left,.left],[.left,.left,.left],[.left,.left,.right],[.left,.left,.left,.left],[.left,.left,.left,.right],[.left,.left,.left,.left,.left],[.left,.left,.left,.left,.right],[.left,.left,.left,.left],[.left,.left,.left],[.left,.left],[.left,.left,.left],[.left,.left,.right],[.left,.left,.left,.left],[.left,.left,.left,.right],[.left,.left,.left],[.left,.left],[.left],[]]
theorem changed_input_iteration : P01AC.Intensional.Plus.PolyConvPlus
    (ClosedScalarInstances.scalarLeft changed_input_n) (P01AC.EffectiveCompleteness.iterationPoly 0) :=
  ScalarCertificates.checkedIteration changed_input_n 0 changed_input_l (by decide)
theorem changed_input_right_iteration : P01AC.Intensional.Plus.PolyConvPlus
    (ClosedScalarInstances.scalarRight changed_input_n) (P01AC.EffectiveCompleteness.iterationPoly 0) :=
  ScalarCertificates.checkedRightIteration changed_input_n 0 changed_input_r (by
    unfold ClosedScalarInstances.scalarRight
    rw [ScalarCertificates.originalQ_expanded]
    decide)
theorem changed_input_conversion : P01AC.Intensional.Plus.PolyConvPlus
    (ClosedScalarInstances.scalarLeft changed_input_n) (ClosedScalarInstances.scalarRight changed_input_n) :=
  changed_input_iteration.trans changed_input_right_iteration.symm
#print axioms changed_input_conversion
#print axioms changed_input_iteration
theorem changed_input_source_instance : P01AC.ExtensionalRepair.HasE []
    (.app P01AC.ExtensionalRepair.ExactScalarFusion.c3 changed_input_n)
    (P01AC.inst (.all (.pi P01AC.ExtensionalRepair.ExactScalarFusion.End
      (.pi P01AC.ExtensionalRepair.ExactScalarFusion.A
        (P01AC.ExtensionalRepair.ExactScalarFusion.Leaf FullPER.Application.originalQ)))) changed_input_n) :=
  ScalarCertificates.exactSourceInstanceFromConversions
    (by simp [P01AC.Scoped, changed_input_n]) 0 changed_input_iteration changed_input_right_iteration
#print axioms changed_input_source_instance
