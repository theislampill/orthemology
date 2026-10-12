import IndependentControls
open ActualSourceEnumerability Encodable
example (A : P01AC.Ty) (p : P01D.Poly) :
    (inhabitantSearch (encode A)).Dom ↔ JointCompletion.HasJ [] p A := by
  exact inhabitantSearch_exact A
