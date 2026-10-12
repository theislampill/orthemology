import AuxiliaryControls
open Encodable AuxiliaryCertificates OrthemologyV2 OrthemologyV3 P01D P01AC AuxiliaryCodeComputability
set_option maxRecDepth 8192
set_option maxHeartbeats 200000
example : checkPolyCode (pack 0 [SourceFamilyComputability.leaf 0]) 0 0 = false := by
  rw [checkPolyCode,ExactSyntaxValidity.evaluate]
  simp [polyShape,polyChildren,pack,CodedScope.tag,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,
    CodedScope.arg1,CodedScope.arg2,ExactSyntaxValidity.arg3,unpair_leaf]
