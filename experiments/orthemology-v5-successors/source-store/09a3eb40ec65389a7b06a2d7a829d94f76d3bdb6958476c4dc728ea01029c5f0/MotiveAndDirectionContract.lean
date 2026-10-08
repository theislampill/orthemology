import LiteralScalarFusion
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.ExactScalarFusion
open P01AC.UnaryIdentity.IntensionalBoundary P01AC.EffectiveCompleteness
example : M = .pi N (.all (.pi (arr (.param 0) (.param 0)) (.pi (.param 0)
    (.identity (.param 0)
      (.app (.app (.var 2) (.var 1)) (.var 0))
      (.app (.app (.app (.var 4) (.var 2)) (.var 1)) (.var 0)))))) := rfl
example (e : Poly) : motiveAt M redundantExpr.closed e = W redundantExpr.closed :=
  M_at (has_scoped q_current) e
example : c3 = .app (.atom .k) (.app (.atom .k) (.app (.atom .k) (.atom .i))) := by
  simp [c3, i, abstract, freeZero, drop, pren, psub]
example (r : Poly) (h : HasE [] r (.identity (arr N N) variableExpr.closed redundantExpr.closed)) :
    HasE [] (abstract (abstract (abstract (.atom .i)))) (W redundantExpr.closed) := literal_forward h
example (h : Poly) (hh : HasE [] h (W redundantExpr.closed)) :
    HasE [] (.atom .i) (.identity (arr N N) variableExpr.closed redundantExpr.closed) := literal_reverse hh
example : HasE [W q] i literalB := by rw [literalB_exact]; exact local_closed_identity q_current
example : HasE [N, W q] i (PointN q) := local_N_identity q_current
