import ReviewSemanticControls
open HiddenChange HiddenParity NecessityReview
example : (1 : Action 2) ∈ commonMenu forbiddenEven 0 := by simp only [excluded_action]
