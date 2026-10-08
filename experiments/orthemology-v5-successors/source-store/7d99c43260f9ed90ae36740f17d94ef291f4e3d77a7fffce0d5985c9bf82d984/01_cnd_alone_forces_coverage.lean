import Controls
open AnchoredSourceBridge AnchoredSourceBridge.Controls
-- Intentionally false overclaim: the reproducible build must reject this.
example : GlobalCoverage split .g := by finite_check
