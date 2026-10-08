import FiniteControls
open ModalUnion ModalUnion.Controls
/- Each false finite claim must be rejected by kernel-producing decide. -/
example : switchedLocal 2 1 = switchedAnchor 1 := by decide
example : ∀ s t : Bool, collapsingTransport true s = collapsingTransport true t → s = t := by decide
example : chainFrame.crossing 1 1 2 := by decide
