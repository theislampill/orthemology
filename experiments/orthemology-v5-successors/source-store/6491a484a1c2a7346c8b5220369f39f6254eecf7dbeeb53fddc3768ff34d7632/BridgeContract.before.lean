import Mathlib.Data.Bool.Basic

/- API regression contract: before implementation these exact declarations must
be absent; after importing OriginalBearerBridge they must typecheck. -/
#check Orthemology.Tranche20.OriginalBearerBridge.original_bearer_of_resource
#check Orthemology.Tranche20.OriginalBearerBridge.original_bearer_of_completion
#check Orthemology.Tranche20.OriginalBearerBridge.abc_same_witness
#check Orthemology.Tranche20.OriginalBearerBridge.essential_nonreceipt_of_actual_original
