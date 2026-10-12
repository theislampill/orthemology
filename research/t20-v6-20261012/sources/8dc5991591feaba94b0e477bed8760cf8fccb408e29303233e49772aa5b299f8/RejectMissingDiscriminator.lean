import IndependentControls
open TypedObserverFamilyContract TypeIndexedFamilyObstructions TypedObserverReview
-- Must fail: singleton result carriers cannot supply the a != b premise.
example : (Unit.unit : Unit) ≠ Unit.unit := by decide
