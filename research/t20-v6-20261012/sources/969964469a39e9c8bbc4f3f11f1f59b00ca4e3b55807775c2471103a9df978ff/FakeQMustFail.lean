import LiteralSourceQ
set_option maxRecDepth 32768
set_option maxHeartbeats 8000000
def fake_q_n : P01D.Poly := (.app (.atom .k) (.atom .i))
def fake_q_l : List P01Certificate.Address := [[.left],[]]
def fake_q_r : List P01Certificate.Address := [[.left,.left],[.left],[]]
theorem fake_q_iteration : P01AC.Intensional.Plus.PolyConvPlus
    (ClosedScalarInstances.scalarLeft fake_q_n) (P01AC.EffectiveCompleteness.iterationPoly 0) :=
  ScalarCertificates.checkedIteration fake_q_n 0 fake_q_l (by decide)
theorem fake_q_right_iteration : P01AC.Intensional.Plus.PolyConvPlus
    (ClosedScalarInstances.scalarRight fake_q_n) (P01AC.EffectiveCompleteness.iterationPoly 0) :=
  ScalarCertificates.checkedRightIteration fake_q_n 0 fake_q_r (by
    unfold ClosedScalarInstances.scalarRight
    rw [ScalarCertificates.originalQ_expanded]
    decide)
theorem fake_q_conversion : P01AC.Intensional.Plus.PolyConvPlus
    (ClosedScalarInstances.scalarLeft fake_q_n) (ClosedScalarInstances.scalarRight fake_q_n) :=
  fake_q_iteration.trans fake_q_right_iteration.symm
#print axioms fake_q_conversion
#print axioms fake_q_iteration
theorem fake_q_source_instance : P01AC.ExtensionalRepair.HasE []
    (.app P01AC.ExtensionalRepair.ExactScalarFusion.c3 fake_q_n)
    (P01AC.inst (.all (.pi P01AC.ExtensionalRepair.ExactScalarFusion.End
      (.pi P01AC.ExtensionalRepair.ExactScalarFusion.A
        (P01AC.ExtensionalRepair.ExactScalarFusion.Leaf FullPER.Application.originalQ)))) fake_q_n) :=
  ScalarCertificates.exactSourceInstanceFromConversions
    (by simp [P01AC.Scoped, fake_q_n]) 0 fake_q_iteration fake_q_right_iteration
#print axioms fake_q_source_instance
