import IndependentControls
import SourceSearchControls
open ActualSourceEnumerability
example : (proofSearch 0).Dom := by
  exact False.elim (Controls.invalidClaimSearchUndefined (by assumption))
