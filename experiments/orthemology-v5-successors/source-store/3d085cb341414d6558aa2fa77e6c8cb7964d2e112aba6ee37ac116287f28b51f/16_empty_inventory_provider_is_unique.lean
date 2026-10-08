import Controls
open AnchoredSourceBridge AnchoredSourceBridge.Controls
-- Intentionally false overclaim: the reproducible build must reject this.
example : ∀ s, Complete emptyInventory s .e → s = S.g := by finite_check
