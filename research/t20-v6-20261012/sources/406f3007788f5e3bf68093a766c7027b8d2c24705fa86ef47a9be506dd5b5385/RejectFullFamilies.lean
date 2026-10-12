import IndependentControls
open TypedObserverFamilyContract TypedObserverReview
-- Must fail: compositional reintroduction of full families is not the identity.
example : FixedAllContract Bool Bool (Bool → Bool) where
  decode := freeDecode
  reintroAt := freeReintro
  assembly := free_assembly
  erased_cycle := by intro r x; rfl
