import Controls
open AnchoredSourceBridge AnchoredSourceBridge.Controls
-- Intentionally false overclaim: the reproducible build must reject this.
example : Admissible aggregate := by finite_check
