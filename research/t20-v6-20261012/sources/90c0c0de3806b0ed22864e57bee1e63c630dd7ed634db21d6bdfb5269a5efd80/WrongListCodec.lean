import TelescopeValidityControls
open TelescopeCodeValidity Encodable OrthemologyV2 P01AC
example : encode ([Ty.raw] : Tel) = CodedScope.node (encode Ty.raw) 0 := by rfl
