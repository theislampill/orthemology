import LiteralSourceQ
set_option maxRecDepth 32768
set_option maxHeartbeats 8000000
def open_erased_n : P01D.Poly := (.app (.app (.atom .k) (.app (.atom .k) (.atom .i))) (.var 42))
def open_erased_l : List P01Certificate.Address := [[.left,.left],[.left],[]]
def open_erased_r : List P01Certificate.Address := [[.left,.left,.right],[.left,.left],[.left,.left,.left],[.left,.left,.right],[.left,.left,.left,.left],[.left,.left,.left,.right],[.left,.left,.left,.left,.left],[.left,.left,.left,.left,.right],[.left,.left,.left,.left],[.left,.left,.left],[.left,.left],[.left,.left,.left],[.left,.left,.right],[.left,.left,.left,.left],[.left,.left,.left,.right],[.left,.left,.left],[.left,.left],[.left],[]]
theorem open_erased_iteration : P01AC.Intensional.Plus.PolyConvPlus
    (ClosedScalarInstances.scalarLeft open_erased_n) (P01AC.EffectiveCompleteness.iterationPoly 0) :=
  ScalarCertificates.checkedIteration open_erased_n 0 open_erased_l (by decide)
theorem open_erased_right_iteration : P01AC.Intensional.Plus.PolyConvPlus
    (ClosedScalarInstances.scalarRight open_erased_n) (P01AC.EffectiveCompleteness.iterationPoly 0) :=
  ScalarCertificates.checkedRightIteration open_erased_n 0 open_erased_r (by
    unfold ClosedScalarInstances.scalarRight
    rw [ScalarCertificates.originalQ_expanded]
    decide)
theorem open_erased_conversion : P01AC.Intensional.Plus.PolyConvPlus
    (ClosedScalarInstances.scalarLeft open_erased_n) (ClosedScalarInstances.scalarRight open_erased_n) :=
  open_erased_iteration.trans open_erased_right_iteration.symm
#print axioms open_erased_conversion
#print axioms open_erased_iteration
