import FullESigmaBoundary
open P01AC P01D P01AC.ExtensionalRepair SigmaCompletion
example (d e : Poly) : HasE FullE.BoundaryControls.Γ (elim d (.var 0) e)
    (.identity (.sigma .raw .raw) (.var 0) (reconstruct (.var 0))) := by
  exact elim_erases d (.var 0) e
