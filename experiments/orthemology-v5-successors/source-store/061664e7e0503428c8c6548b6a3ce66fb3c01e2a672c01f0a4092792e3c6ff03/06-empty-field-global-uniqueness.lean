import BoundaryChecks
open AnchoredSourceBridge AnchoredSourceBridge.Controls
open AnchoredSourceBridge.Controls.ModalAbility IndependentAnchoredReview
example : ∀ s, GlobalCoverage noField s → s = S.g := by independent_finite
