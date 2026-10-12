import CrossReviewControls
open CrossTypedObserver CrossTypingReview
-- Membership evidence does not supply equality of opposite observations.
example : sigmaObservation (fun _ seed => seed) false true =
    churchObservation (fun step seed => step seed) false true := by decide
