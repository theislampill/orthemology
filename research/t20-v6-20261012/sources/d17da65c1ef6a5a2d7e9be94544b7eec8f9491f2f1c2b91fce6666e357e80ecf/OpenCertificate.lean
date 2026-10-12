import LiteralSourceQ
set_option maxRecDepth 32768
set_option maxHeartbeats 8000000
def open_erasing_n : P01D.Poly := (.app (.app (.atom .k) (.app (.atom .k) (.atom .i))) (.var 42))
def open_erasing_l : List P01Certificate.Address := [[.left,.left],[.left],[]]
def open_erasing_r : List P01Certificate.Address := [[.left,.left,.right],[.left,.left],[.left,.left,.left],[.left,.left,.right],[.left,.left,.left,.left],[.left,.left,.left,.right],[.left,.left,.left,.left,.left],[.left,.left,.left,.left,.right],[.left,.left,.left,.left],[.left,.left,.left],[.left,.left],[.left,.left,.left],[.left,.left,.right],[.left,.left,.left,.left],[.left,.left,.left,.right],[.left,.left,.left],[.left,.left],[.left],[]]
theorem open_erasing_iteration : P01AC.Intensional.Plus.PolyConvPlus
    (ClosedScalarInstances.scalarLeft open_erasing_n) (P01AC.EffectiveCompleteness.iterationPoly 0) :=
  ScalarCertificates.checkedIteration open_erasing_n 0 open_erasing_l (by decide)
theorem open_erasing_right_iteration : P01AC.Intensional.Plus.PolyConvPlus
    (ClosedScalarInstances.scalarRight open_erasing_n) (P01AC.EffectiveCompleteness.iterationPoly 0) :=
  ScalarCertificates.checkedRightIteration open_erasing_n 0 open_erasing_r (by
    unfold ClosedScalarInstances.scalarRight
    rw [ScalarCertificates.originalQ_expanded]
    decide)
theorem open_erasing_conversion : P01AC.Intensional.Plus.PolyConvPlus
    (ClosedScalarInstances.scalarLeft open_erasing_n) (ClosedScalarInstances.scalarRight open_erasing_n) :=
  open_erasing_iteration.trans open_erasing_right_iteration.symm
#print axioms open_erasing_conversion
#print axioms open_erasing_iteration
