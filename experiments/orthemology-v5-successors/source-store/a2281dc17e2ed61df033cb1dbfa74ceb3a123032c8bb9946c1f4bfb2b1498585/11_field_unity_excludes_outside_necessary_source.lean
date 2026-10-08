import Controls
open AnchoredSourceBridge AnchoredSourceBridge.Controls
-- Intentionally false overclaim: the reproducible build must reject this.
example : S.g = S.h := by decide
