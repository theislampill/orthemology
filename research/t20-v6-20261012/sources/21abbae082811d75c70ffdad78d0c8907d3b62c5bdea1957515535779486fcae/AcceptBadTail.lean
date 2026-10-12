import TelescopeValidityControls
open TelescopeCodeValidity Encodable OrthemologyV2 P01AC
example : validTel (Nat.pair (encode Ty.raw) 1 + 1) = true := by decide
