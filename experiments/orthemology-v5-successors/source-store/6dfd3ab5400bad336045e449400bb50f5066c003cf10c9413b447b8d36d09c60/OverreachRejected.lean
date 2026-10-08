import OriginationTypeControl
open T20.OntologyTypeControl
-- Deliberately false strengthening. Success would be an audit failure.
example : Created (.gAct 1) := by
  unfold Created
  decide
-- Potential labels do not supply existence at an empty actual state.
example : E (actual 2) (.effect 2) := by
  unfold E actual
  decide
