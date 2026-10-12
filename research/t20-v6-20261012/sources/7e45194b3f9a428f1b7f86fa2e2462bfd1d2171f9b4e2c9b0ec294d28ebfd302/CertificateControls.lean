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

-- Runtime acceptance exercises every actual certificate constructor, including all 63 Rule rows.
set_option pp.deepTerms true
set_option pp.maxSteps 100000
#eval [
  certValid 6 (encode (StepCert.i (Term.i))),
  certValid 6 (encode (StepCert.k (Term.i) (Term.i))),
  certValid 6 (encode (StepCert.s (Term.i) (Term.i) (Term.i))),
  certValid 6 (encode (StepCert.left (Term.i) (Term.i) (Term.i) (StepCert.i Term.i))),
  certValid 6 (encode (StepCert.right (Term.i) (Term.i) (Term.i) (StepCert.i Term.i))),
  certValid 7 (encode (RedCert.refl (Term.i))),
  certValid 7 (encode (RedCert.tail (Term.i) (Term.i) (Term.i) (StepCert.i Term.i) (RedCert.refl Term.i))),
  certValid 8 (encode (FiniteCert.i (TypeCode.var 0))),
  certValid 8 (encode (FiniteCert.k (TypeCode.var 0) (TypeCode.var 0))),
  certValid 8 (encode (FiniteCert.s (TypeCode.var 0) (TypeCode.var 0) (TypeCode.var 0))),
  certValid 8 (encode (FiniteCert.app (Term.i) (Term.i) (TypeCode.var 0) (TypeCode.var 0) (FiniteCert.i (TypeCode.var 0)) (FiniteCert.i (TypeCode.var 0)))),
  certValid 8 (encode (FiniteCert.allI (Term.i) (TypeCode.var 0) (FiniteCert.i (TypeCode.var 0)))),
  certValid 8 (encode (FiniteCert.allE (Term.i) (TypeCode.var 0) (TypeCode.var 0) (FiniteCert.i (TypeCode.var 0)))),
  certValid 8 (encode (FiniteCert.reduce (Term.i) (Term.i) (TypeCode.var 0) (FiniteCert.i (TypeCode.var 0)) (RedCert.refl Term.i))),
  certValid 9 (encode (PolyCert.refl (Poly.var 0))),
  certValid 9 (encode (PolyCert.symm (Poly.var 0) (Poly.var 0) (PolyCert.refl (Poly.var 0)))),
  certValid 9 (encode (PolyCert.trans (Poly.var 0) (Poly.var 0) (Poly.var 0) (PolyCert.refl (Poly.var 0)) (PolyCert.refl (Poly.var 0)))),
  certValid 9 (encode (PolyCert.app (Poly.var 0) (Poly.var 0) (Poly.var 0) (Poly.var 0) (PolyCert.refl (Poly.var 0)) (PolyCert.refl (Poly.var 0)))),
  certValid 9 (encode (PolyCert.i (Poly.var 0))),
  certValid 9 (encode (PolyCert.k (Poly.var 0) (Poly.var 0))),
  certValid 9 (encode (PolyCert.s (Poly.var 0) (Poly.var 0) (Poly.var 0))),
  certValid 9 (encode (PolyCert.bridge (Term.i) (Term.i))),
  certValid 10 (encode (LookupCert.zero (([] : Tel)) (Ty.param 0))),
  certValid 10 (encode (LookupCert.succ (([] : Tel)) (0) (Ty.param 0) (Ty.param 0) (LookupCert.zero [] (Ty.param 0)))),
  certValid 11 (encode (Claim.ctxJ (([] : Tel)))),
  certValid 11 (encode (Claim.formJ (([] : Tel)) (Ty.param 0))),
  certValid 11 (encode (Claim.hasJ (([] : Tel)) (Poly.var 0) (Ty.param 0))),
  certValid 11 (encode (Claim.ctxE (([] : Tel)))),
  certValid 11 (encode (Claim.formE (([] : Tel)) (Ty.param 0))),
  certValid 11 (encode (Claim.hasE (([] : Tel)) (Poly.var 0) (Ty.param 0))),
  certValid 12 (encode (Rule.CtxJ_ctxBase (([] : Tel)))),
  certValid 12 (encode (Rule.CtxJ_nil)),
  certValid 12 (encode (Rule.CtxJ_ext (([] : Tel)) (Ty.param 0))),
  certValid 12 (encode (Rule.FormJ_formBase (([] : Tel)) (Ty.param 0))),
  certValid 12 (encode (Rule.FormJ_param (([] : Tel)) (0))),
  certValid 12 (encode (Rule.FormJ_bottom (([] : Tel)))),
  certValid 12 (encode (Rule.FormJ_all (([] : Tel)) (Ty.param 0))),
  certValid 12 (encode (Rule.FormJ_raw (([] : Tel)))),
  certValid 12 (encode (Rule.FormJ_pi (([] : Tel)) (Ty.param 0) (Ty.param 0))),
  certValid 12 (encode (Rule.FormJ_sigma (([] : Tel)) (Ty.param 0) (Ty.param 0))),
  certValid 12 (encode (Rule.FormJ_identity (([] : Tel)) (Ty.param 0) (Poly.var 0) (Poly.var 0))),
  certValid 12 (encode (Rule.HasJ_hasBase (([] : Tel)) (Poly.var 0) (Ty.param 0))),
  certValid 12 (encode (Rule.HasJ_var (([] : Tel)) (Ty.param 0) (0) (LookupCert.zero [] (Ty.param 0)))),
  certValid 12 (encode (Rule.HasJ_i (([] : Tel)) (Ty.param 0))),
  certValid 12 (encode (Rule.HasJ_k (([] : Tel)) (Ty.param 0) (Ty.param 0))),
  certValid 12 (encode (Rule.HasJ_s (([] : Tel)) (Ty.param 0) (Ty.param 0) (Ty.param 0))),
  certValid 12 (encode (Rule.HasJ_finite (TypeCode.var 0) (([] : Tel)) (Term.i) (([] : List Ty)) (FiniteCert.i (TypeCode.var 0)))),
  certValid 12 (encode (Rule.HasJ_allIntro (([] : Tel)) (Ty.param 0) (Poly.var 0))),
  certValid 12 (encode (Rule.HasJ_allElim (([] : Tel)) (Ty.param 0) (Ty.param 0) (Poly.var 0))),
  certValid 12 (encode (Rule.HasJ_rawAtom (([] : Tel)) (Term.i))),
  certValid 12 (encode (Rule.HasJ_rawApp (([] : Tel)) (Poly.var 0) (Poly.var 0))),
  certValid 12 (encode (Rule.HasJ_piIntro (([] : Tel)) (Ty.param 0) (Ty.param 0) (Poly.var 0))),
  certValid 12 (encode (Rule.HasJ_piElim (([] : Tel)) (Ty.param 0) (Ty.param 0) (Poly.var 0) (Poly.var 0))),
  certValid 12 (encode (Rule.HasJ_sigmaIntro (([] : Tel)) (Ty.param 0) (Ty.param 0) (Poly.var 0) (Poly.var 0))),
  certValid 12 (encode (Rule.HasJ_sigmaFst (([] : Tel)) (Ty.param 0) (Ty.param 0) (Poly.var 0))),
  certValid 12 (encode (Rule.HasJ_sigmaSnd (([] : Tel)) (Ty.param 0) (Ty.param 0) (Poly.var 0))),
  certValid 12 (encode (Rule.HasJ_identityIntro (([] : Tel)) (Ty.param 0) (Poly.var 0) (Poly.var 0) (PolyCert.refl (Poly.var 0)))),
  certValid 12 (encode (Rule.HasJ_proofErase (([] : Tel)) (Ty.param 0) (Poly.var 0) (Poly.var 0) (Poly.var 0))),
  certValid 12 (encode (Rule.HasJ_j (([] : Tel)) (Ty.param 0) (Poly.var 0) (Ty.param 0) (Poly.var 0) (Poly.var 0) (Poly.var 0))),
  certValid 12 (encode (Rule.HasJ_conv (([] : Tel)) (Ty.param 0) (Poly.var 0) (Poly.var 0) (PolyCert.refl (Poly.var 0)))),
  certValid 12 (encode (Rule.HasJ_piExt (([] : Tel)) (Ty.param 0) (Ty.param 0) (Poly.var 0) (Poly.var 0) (Poly.var 0))),
  certValid 12 (encode (Rule.HasJ_allExt (([] : Tel)) (Ty.param 0) (Poly.var 0) (Poly.var 0) (Poly.var 0))),
  certValid 12 (encode (Rule.HasJ_sigmaElim (([] : Tel)) (Ty.param 0) (Ty.param 0) (Ty.param 0) (Poly.var 0) (Poly.var 0))),
  certValid 12 (encode (Rule.HasJ_natInduction (([] : Tel)) (Ty.param 0) (Poly.var 0) (Poly.var 0))),
  certValid 12 (encode (Rule.CtxE_nil)),
  certValid 12 (encode (Rule.CtxE_ext (([] : Tel)) (Ty.param 0))),
  certValid 12 (encode (Rule.FormE_param (([] : Tel)) (0))),
  certValid 12 (encode (Rule.FormE_bottom (([] : Tel)))),
  certValid 12 (encode (Rule.FormE_all (([] : Tel)) (Ty.param 0))),
  certValid 12 (encode (Rule.FormE_raw (([] : Tel)))),
  certValid 12 (encode (Rule.FormE_pi (([] : Tel)) (Ty.param 0) (Ty.param 0))),
  certValid 12 (encode (Rule.FormE_sigma (([] : Tel)) (Ty.param 0) (Ty.param 0))),
  certValid 12 (encode (Rule.FormE_identity (([] : Tel)) (Ty.param 0) (Poly.var 0) (Poly.var 0))),
  certValid 12 (encode (Rule.HasE_var (([] : Tel)) (Ty.param 0) (0) (LookupCert.zero [] (Ty.param 0)))),
  certValid 12 (encode (Rule.HasE_i (([] : Tel)) (Ty.param 0))),
  certValid 12 (encode (Rule.HasE_k (([] : Tel)) (Ty.param 0) (Ty.param 0))),
  certValid 12 (encode (Rule.HasE_s (([] : Tel)) (Ty.param 0) (Ty.param 0) (Ty.param 0))),
  certValid 12 (encode (Rule.HasE_finite (TypeCode.var 0) (([] : Tel)) (Term.i) (([] : List Ty)) (FiniteCert.i (TypeCode.var 0)))),
  certValid 12 (encode (Rule.HasE_allIntro (([] : Tel)) (Ty.param 0) (Poly.var 0))),
  certValid 12 (encode (Rule.HasE_allElim (([] : Tel)) (Ty.param 0) (Ty.param 0) (Poly.var 0))),
  certValid 12 (encode (Rule.HasE_rawAtom (([] : Tel)) (Term.i))),
  certValid 12 (encode (Rule.HasE_rawApp (([] : Tel)) (Poly.var 0) (Poly.var 0))),
  certValid 12 (encode (Rule.HasE_piIntro (([] : Tel)) (Ty.param 0) (Ty.param 0) (Poly.var 0))),
  certValid 12 (encode (Rule.HasE_piElim (([] : Tel)) (Ty.param 0) (Ty.param 0) (Poly.var 0) (Poly.var 0))),
  certValid 12 (encode (Rule.HasE_sigmaIntro (([] : Tel)) (Ty.param 0) (Ty.param 0) (Poly.var 0) (Poly.var 0))),
  certValid 12 (encode (Rule.HasE_sigmaFst (([] : Tel)) (Ty.param 0) (Ty.param 0) (Poly.var 0))),
  certValid 12 (encode (Rule.HasE_sigmaSnd (([] : Tel)) (Ty.param 0) (Ty.param 0) (Poly.var 0))),
  certValid 12 (encode (Rule.HasE_identityIntro (([] : Tel)) (Ty.param 0) (Poly.var 0) (Poly.var 0) (PolyCert.refl (Poly.var 0)))),
  certValid 12 (encode (Rule.HasE_proofErase (([] : Tel)) (Ty.param 0) (Poly.var 0) (Poly.var 0) (Poly.var 0))),
  certValid 12 (encode (Rule.HasE_j (([] : Tel)) (Ty.param 0) (Poly.var 0) (Ty.param 0) (Poly.var 0) (Poly.var 0) (Poly.var 0))),
  certValid 12 (encode (Rule.HasE_conv (([] : Tel)) (Ty.param 0) (Poly.var 0) (Poly.var 0) (PolyCert.refl (Poly.var 0)))),
  certValid 12 (encode (Rule.HasE_piExt (([] : Tel)) (Ty.param 0) (Ty.param 0) (Poly.var 0) (Poly.var 0) (Poly.var 0))),
  certValid 12 (encode (Rule.HasE_allExt (([] : Tel)) (Ty.param 0) (Poly.var 0) (Poly.var 0) (Poly.var 0))),
  certValid 13 (encode (SerialCert.node (Rule.CtxJ_nil) (SerialCertList.nil))),
  certValid 14 (encode (SerialCertList.nil)),
  certValid 14 (encode (SerialCertList.cons (SerialCert.node Rule.CtxJ_nil SerialCertList.nil) (SerialCertList.nil)))]
#eval [certValid 6 (pack 0 [leaf 0]), certValid 8 (pack 0 [leaf 0]), certValid 9 (pack 0 [leaf 0]), certValid 11 (pack 0 [leaf 1]), certValid 12 (pack 13 [leaf 0,leaf 0]), certValid 13 (pack 0 [leaf 0, encode SerialCertList.nil]), certValid 14 (pack 1 [0,encode SerialCertList.nil]), certValid 14 (pack 1 [encode (SerialCert.node Rule.CtxJ_nil SerialCertList.nil),0])]
end CertificateCodeValidity.Controls
