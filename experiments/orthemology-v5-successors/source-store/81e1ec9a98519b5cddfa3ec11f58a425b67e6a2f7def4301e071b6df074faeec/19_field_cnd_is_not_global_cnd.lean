import Controls
open AnchoredSourceBridge AnchoredSourceBridge.Controls
-- Duplication outside the admitted field does not invalidate FieldCND.
example : CND outsideDuplicate := by finite_check
