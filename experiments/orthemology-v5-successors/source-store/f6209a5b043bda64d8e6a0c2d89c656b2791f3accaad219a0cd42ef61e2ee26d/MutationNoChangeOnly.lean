import NecessityControls
open HiddenChange HiddenChangeNecessityTests
-- noChange_only_wins is kernel-proved in the imported control. The omitted
-- fixed-index obligations are substantive: this claimed body cannot exist.
example : ∃ body : PositiveBody 1 1, positiveCheck (singletonInput 0 1) 0 body = true := by
  apply (positiveCheck_iff_region _ (singleton_admissible 0 1) _).mpr
  decide +kernel
