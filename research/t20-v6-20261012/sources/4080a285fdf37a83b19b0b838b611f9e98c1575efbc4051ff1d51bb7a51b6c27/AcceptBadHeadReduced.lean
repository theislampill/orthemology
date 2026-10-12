import TelescopeValidityControls
open TelescopeCodeValidity
example : validTel 1 = true := by
  rw [rejectTelOne]
  decide
