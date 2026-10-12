import LiteralSourceQ
namespace NegativeCertificateControls
open OpenTermStandardness (T)
open ScalarCertificates

/-- A leaf cannot contain a redex, even if a JSON trace claims otherwise. -/
theorem reject_leaf_address : (stepAt (.var 0) [.left]).isSome = false := by decide
/-- A well-formed address that names a non-redex is rejected. -/
theorem reject_nonredex_root : (stepAt (.app (.var 1) (.var 0)) []).isSome = false := by decide
/-- A genuine step cannot authenticate a forged endpoint. -/
theorem reject_forged_endpoint :
    (replayTo (.app .i (.var 0)) (.var 17) [[]]).isSome = false := by decide
/-- The target is exact generic iteration syntax, so a forged count fails. -/
theorem reject_forged_count :
    (replayTo (.app .i (.var 0)) (OpenTermStandardness.iter (.var 1) (.var 0) 1) [[]]).isSome = false := by decide
#print axioms reject_leaf_address
#print axioms reject_nonredex_root
#print axioms reject_forged_endpoint
#print axioms reject_forged_count
end NegativeCertificateControls
