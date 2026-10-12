import IndependentControls
open OrthemologyV2 OrthemologyV3 P01D P01AC TypedStructuredObserver TypedObserverReview
-- Must fail: the state binder shifts B's endpoint var 0 to var 1.
example : Has (Carrier DepB :: DepΓ) (body (.atom .i)) (Carrier DepB) :=
  body_has dep_update
