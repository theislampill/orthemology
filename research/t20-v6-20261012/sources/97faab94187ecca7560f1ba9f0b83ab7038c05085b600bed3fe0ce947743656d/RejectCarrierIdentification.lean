import CrossReviewControls
open P01AC CrossTypedObserver CrossTypingReview
-- The observer's shared result type does not identify the two carrier types.
example : Product DepB = ChurchPair DepB := rfl
