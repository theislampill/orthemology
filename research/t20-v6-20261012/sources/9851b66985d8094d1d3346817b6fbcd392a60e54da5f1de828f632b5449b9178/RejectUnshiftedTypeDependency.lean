import IndependentControls
open OrthemologyV2 OrthemologyV3 P01D P01AC TypedStructuredObserver TypedObserverReview
open P01AC.EffectiveCompleteness (inputNumeral)
-- Must fail: fresh parameter 0 shifts the original parameter in B to 1.
example : Has (twkTel DepΓ) (observe (inputNumeral 0) (.atom .i) (.atom .i)) DepB :=
  dependent_fresh
