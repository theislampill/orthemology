import CertificateImage
import ValidityControls
import TelescopeValidityControls
namespace CertificateCodeValidity.Controls
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity AuxiliaryCodeComputability
open OrthemologyV2 P01D P01AC AuxiliaryCertificates JointCertificates TelescopeCodeValidity
set_option maxRecDepth 16384
set_option maxHeartbeats 1000000

example (a : AuxiliaryCertificates.StepCert) : certValid 6 (encode a) = true := (valid_StepCert _).mpr ⟨a,rfl⟩
example (a : AuxiliaryCertificates.RedCert) : certValid 7 (encode a) = true := (valid_RedCert _).mpr ⟨a,rfl⟩
example (a : AuxiliaryCertificates.FiniteCert) : certValid 8 (encode a) = true := (valid_FiniteCert _).mpr ⟨a,rfl⟩
example (a : AuxiliaryCertificates.PolyCert) : certValid 9 (encode a) = true := (valid_PolyCert _).mpr ⟨a,rfl⟩
example (a : AuxiliaryCertificates.LookupCert) : certValid 10 (encode a) = true := (valid_LookupCert _).mpr ⟨a,rfl⟩
example (a : JointCertificates.Claim) : certValid 11 (encode a) = true := (valid_Claim _).mpr ⟨a,rfl⟩
example (a : JointCertificates.Rule) : certValid 12 (encode a) = true := (valid_Rule _).mpr ⟨a,rfl⟩
example (a : JointCertificates.SerialCert) : certValid 13 (encode a) = true := (valid_SerialCert _).mpr ⟨a,rfl⟩
example (a : JointCertificates.SerialCertList) : certValid 14 (encode a) = true := (valid_SerialCertList _).mpr ⟨a,rfl⟩

theorem certValid_unfold (s c : Nat) : certValid s c = (certShape (s,c) &&
    (certChildren (s,c)).all (fun d => if d.2 < c then certValid d.1 d.2 else false)) := by
  rw [certValid, evaluate]
  rfl

theorem reject_shape (s c : Nat) (hs : certShape (s,c) = false) : certValid s c = false := by
  rw [certValid_unfold, hs]
  rfl

@[simp] theorem zero_lt_pack (t : Nat) (xs : List Nat) : 0 < pack t xs :=
  lt_of_le_of_lt (Nat.zero_le _) (left_lt_node _ _)
@[simp] theorem wrapped_lt_pack (t n : Nat) (xs : List Nat) (h : leaf n ∈ xs) : n < pack t xs :=
  lt_of_le_of_lt (le_leaf n) (field_lt_pack t xs h)

@[simp] theorem rejectTermZero : certValid 0 0 = false := by
  rw [certValid_unfold]
  simp [certShape, ExactSyntaxValidity.Controls.rejectTermZero]
@[simp] theorem rejectTypeZero : certValid 1 0 = false := by
  rw [certValid_unfold]
  simp [certShape, ExactSyntaxValidity.Controls.rejectTypeZero]
@[simp] theorem rejectPolyZero : certValid 2 0 = false := by
  rw [certValid_unfold]
  simp [certShape, ExactSyntaxValidity.Controls.rejectPolyZero]
@[simp] theorem rejectTyZero : certValid 3 0 = false := by
  rw [certValid_unfold]
  simp [certShape, ExactSyntaxValidity.Controls.rejectTyZero]
@[simp] theorem rejectBadTel : certValid 5 1 = false := by
  rw [certValid_unfold]
  simp [certShape, TelescopeCodeValidity.rejectTelOne]
@[simp] theorem rejectRuleZero : certValid 12 0 = false := reject_shape _ _ (by decide)
@[simp] theorem rejectSerialZero : certValid 13 0 = false := reject_shape _ _ (by decide)
@[simp] theorem rejectSerialListZero : certValid 14 0 = false := reject_shape _ _ (by decide)

-- Canonical syntax images overlap exactly where the original codec does.
example : certValid 14 (encode Term.i) = true := (valid_SerialCertList _).mpr ⟨.nil,rfl⟩
example : certValid 12 (encode Term.k) = true := (valid_Rule _).mpr ⟨.CtxJ_nil,rfl⟩
example : certValid 11 (encode (Poly.var 0)) = true := (valid_Claim _).mpr ⟨.ctxJ [],rfl⟩

-- Exact arity, terminator, wrapper, sort, and constructor-tag checks.
example : certValid 15 1 = false := reject_shape _ _ (by decide)
example : certValid 6 (pack 5 []) = false := reject_shape _ _ (by decide)
example : certValid 12 (pack 63 []) = false := reject_shape _ _ (by simp [certShape, allDescriptions, localShape, ruleDescription])
theorem rejectSerialTerminator : certValid 14 (node (leaf 0) (leaf 1)) = false :=
  reject_shape _ _ (by decide)
theorem rejectSerialWrapper : certValid 13 (pack 0 [encode Rule.CtxJ_nil, encode SerialCertList.nil]) = false :=
  reject_shape _ _ (by
    simp [certShape, allDescriptions, localShape, serialCertDescription, rebuild, rebuildField, fieldCode, List.range_succ]
    simp [pack, node, leaf, Nat.pair_eq_pair])

-- Local shape is correct; rejection genuinely depends on the child sort.
theorem shapeBadStepTerm : localShape stepCertDescription (pack 0 [leaf 0]) = true := by
  simp [stepCertDescription, localShape, localChildren, rebuild, rebuildField, dependencies, fieldCode, List.range_succ]
theorem rejectBadStepTerm : certValid 6 (pack 0 [leaf 0]) = false := by
  rw [certValid_unfold]
  simp [certShape, certChildren, allDescriptions, stepCertDescription, localShape, localChildren, rebuild, rebuildField, dependencies, fieldCode, List.range_succ]

-- Local shape is correct; rejection genuinely depends on the child sort.
theorem shapeBadFiniteType : localShape finiteCertDescription (pack 0 [leaf 0]) = true := by
  simp [finiteCertDescription, localShape, localChildren, rebuild, rebuildField, dependencies, fieldCode, List.range_succ]
theorem rejectBadFiniteType : certValid 8 (pack 0 [leaf 0]) = false := by
  rw [certValid_unfold]
  simp [certShape, certChildren, allDescriptions, finiteCertDescription, localShape, localChildren, rebuild, rebuildField, dependencies, fieldCode, List.range_succ]

-- Local shape is correct; rejection genuinely depends on the child sort.
theorem shapeBadPolyPayload : localShape polyCertDescription (pack 0 [leaf 0]) = true := by
  simp [polyCertDescription, localShape, localChildren, rebuild, rebuildField, dependencies, fieldCode, List.range_succ]
theorem rejectBadPolyPayload : certValid 9 (pack 0 [leaf 0]) = false := by
  rw [certValid_unfold]
  simp [certShape, certChildren, allDescriptions, polyCertDescription, localShape, localChildren, rebuild, rebuildField, dependencies, fieldCode, List.range_succ]

-- Local shape is correct; rejection genuinely depends on the child sort.
theorem shapeBadClaimTel : localShape claimDescription (pack 0 [leaf 1]) = true := by
  simp [claimDescription, localShape, localChildren, rebuild, rebuildField, dependencies, fieldCode, List.range_succ]
theorem rejectBadClaimTel : certValid 11 (pack 0 [leaf 1]) = false := by
  rw [certValid_unfold]
  simp [certShape, certChildren, allDescriptions, claimDescription, localShape, localChildren, rebuild, rebuildField, dependencies, fieldCode, List.range_succ]

-- Local shape is correct; rejection genuinely depends on the child sort.
theorem shapeBadRuleTy : localShape ruleDescription (pack 13 [leaf 0,leaf 0]) = true := by
  simp [ruleDescription, localShape, localChildren, rebuild, rebuildField, dependencies, fieldCode, List.range_succ]
theorem rejectBadRuleTy : certValid 12 (pack 13 [leaf 0,leaf 0]) = false := by
  rw [certValid_unfold]
  simp [certShape, certChildren, allDescriptions, ruleDescription, localShape, localChildren, rebuild, rebuildField, dependencies, fieldCode, List.range_succ]

-- Local shape is correct; rejection genuinely depends on the child sort.
theorem shapeBadSerialRule : localShape serialCertDescription (pack 0 [leaf 0, encode SerialCertList.nil]) = true := by
  simp [serialCertDescription, localShape, localChildren, rebuild, rebuildField, dependencies, fieldCode, List.range_succ]
theorem rejectBadSerialRule : certValid 13 (pack 0 [leaf 0, encode SerialCertList.nil]) = false := by
  rw [certValid_unfold]
  simp [certShape, certChildren, allDescriptions, serialCertDescription, localShape, localChildren, rebuild, rebuildField, dependencies, fieldCode, List.range_succ]

-- Local shape is correct; rejection genuinely depends on the child sort.
theorem shapeBadSerialLeft : localShape serialCertListDescription (pack 1 [0,encode SerialCertList.nil]) = true := by
  simp [serialCertListDescription, localShape, localChildren, rebuild, rebuildField, dependencies, fieldCode, List.range_succ]
theorem rejectBadSerialLeft : certValid 14 (pack 1 [0,encode SerialCertList.nil]) = false := by
  rw [certValid_unfold]
  simp [certShape, certChildren, allDescriptions, serialCertListDescription, localShape, localChildren, rebuild, rebuildField, dependencies, fieldCode, List.range_succ]

-- Local shape is correct; rejection genuinely depends on the child sort.
theorem shapeBadSerialRight : localShape serialCertListDescription (pack 1 [encode (SerialCert.node Rule.CtxJ_nil SerialCertList.nil),0]) = true := by
  simp [serialCertListDescription, localShape, localChildren, rebuild, rebuildField, dependencies, fieldCode, List.range_succ]
theorem rejectBadSerialRight : certValid 14 (pack 1 [encode (SerialCert.node Rule.CtxJ_nil SerialCertList.nil),0]) = false := by
  rw [certValid_unfold]
  simp [certShape, certChildren, allDescriptions, serialCertListDescription, localShape, localChildren, rebuild, rebuildField, dependencies, fieldCode, List.range_succ]

end CertificateCodeValidity.Controls
