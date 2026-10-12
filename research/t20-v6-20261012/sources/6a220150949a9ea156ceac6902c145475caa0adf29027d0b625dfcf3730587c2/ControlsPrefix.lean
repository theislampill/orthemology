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

end CertificateCodeValidity.Controls
