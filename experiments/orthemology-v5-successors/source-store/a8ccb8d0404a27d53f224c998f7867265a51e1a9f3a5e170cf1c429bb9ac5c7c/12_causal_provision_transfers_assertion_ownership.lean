import Controls
open AnchoredSourceBridge AnchoredSourceBridge.Controls
-- Intentionally false overclaim: the reproducible build must reject this.
example : SourceOwns .g .v := by finite_check
