import RuleImageRule
namespace CertificateCodeValidity
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity AuxiliaryCodeComputability
open OrthemologyV2 P01D P01AC AuxiliaryCertificates JointCertificates TelescopeCodeValidity
set_option maxRecDepth 16384
set_option maxHeartbeats 200000
attribute [local irreducible] Nat.pair

theorem rule_bounds_0 (a0 : P01AC.Tel) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.CtxJ_ctxBase a0)), d.2 < encode (Rule.CtxJ_ctxBase a0) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_1  :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.CtxJ_nil)), d.2 < encode (Rule.CtxJ_nil) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]

theorem rule_bounds_2 (a0 : P01AC.Tel) (a1 : P01AC.Ty) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.CtxJ_ext a0 a1)), d.2 < encode (Rule.CtxJ_ext a0 a1) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_3 (a0 : P01AC.Tel) (a1 : P01AC.Ty) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.FormJ_formBase a0 a1)), d.2 < encode (Rule.FormJ_formBase a0 a1) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_4 (a0 : P01AC.Tel) (a1 : Nat) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.FormJ_param a0 a1)), d.2 < encode (Rule.FormJ_param a0 a1) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_5 (a0 : P01AC.Tel) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.FormJ_bottom a0)), d.2 < encode (Rule.FormJ_bottom a0) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_6 (a0 : P01AC.Tel) (a1 : P01AC.Ty) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.FormJ_all a0 a1)), d.2 < encode (Rule.FormJ_all a0 a1) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_7 (a0 : P01AC.Tel) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.FormJ_raw a0)), d.2 < encode (Rule.FormJ_raw a0) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_8 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.FormJ_pi a0 a1 a2)), d.2 < encode (Rule.FormJ_pi a0 a1 a2) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_9 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.FormJ_sigma a0 a1 a2)), d.2 < encode (Rule.FormJ_sigma a0 a1 a2) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_10 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.FormJ_identity a0 a1 a2 a3)), d.2 < encode (Rule.FormJ_identity a0 a1 a2 a3) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_11 (a0 : P01AC.Tel) (a1 : P01D.Poly) (a2 : P01AC.Ty) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_hasBase a0 a1 a2)), d.2 < encode (Rule.HasJ_hasBase a0 a1 a2) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_12 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : Nat) (a3 : AuxiliaryCertificates.LookupCert) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_var a0 a1 a2 a3)), d.2 < encode (Rule.HasJ_var a0 a1 a2 a3) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_13 (a0 : P01AC.Tel) (a1 : P01AC.Ty) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_i a0 a1)), d.2 < encode (Rule.HasJ_i a0 a1) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_14 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_k a0 a1 a2)), d.2 < encode (Rule.HasJ_k a0 a1 a2) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_15 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01AC.Ty) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_s a0 a1 a2 a3)), d.2 < encode (Rule.HasJ_s a0 a1 a2 a3) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_16 (a0 : OrthemologyV2.TypeCode) (a1 : P01AC.Tel) (a2 : OrthemologyV2.Term) (a3 : List P01AC.Ty) (a4 : AuxiliaryCertificates.FiniteCert) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_finite a0 a1 a2 a3 a4)), d.2 < encode (Rule.HasJ_finite a0 a1 a2 a3 a4) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_17 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_allIntro a0 a1 a2)), d.2 < encode (Rule.HasJ_allIntro a0 a1 a2) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_18 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_allElim a0 a1 a2 a3)), d.2 < encode (Rule.HasJ_allElim a0 a1 a2 a3) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_19 (a0 : P01AC.Tel) (a1 : OrthemologyV2.Term) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_rawAtom a0 a1)), d.2 < encode (Rule.HasJ_rawAtom a0 a1) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_20 (a0 : P01AC.Tel) (a1 : P01D.Poly) (a2 : P01D.Poly) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_rawApp a0 a1 a2)), d.2 < encode (Rule.HasJ_rawApp a0 a1 a2) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_21 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_piIntro a0 a1 a2 a3)), d.2 < encode (Rule.HasJ_piIntro a0 a1 a2 a3) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_22 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) (a4 : P01D.Poly) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_piElim a0 a1 a2 a3 a4)), d.2 < encode (Rule.HasJ_piElim a0 a1 a2 a3 a4) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_23 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) (a4 : P01D.Poly) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_sigmaIntro a0 a1 a2 a3 a4)), d.2 < encode (Rule.HasJ_sigmaIntro a0 a1 a2 a3 a4) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_24 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_sigmaFst a0 a1 a2 a3)), d.2 < encode (Rule.HasJ_sigmaFst a0 a1 a2 a3) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_25 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_sigmaSnd a0 a1 a2 a3)), d.2 < encode (Rule.HasJ_sigmaSnd a0 a1 a2 a3) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_26 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) (a4 : AuxiliaryCertificates.PolyCert) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_identityIntro a0 a1 a2 a3 a4)), d.2 < encode (Rule.HasJ_identityIntro a0 a1 a2 a3 a4) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_27 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) (a4 : P01D.Poly) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_proofErase a0 a1 a2 a3 a4)), d.2 < encode (Rule.HasJ_proofErase a0 a1 a2 a3 a4) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_28 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01AC.Ty) (a4 : P01D.Poly) (a5 : P01D.Poly) (a6 : P01D.Poly) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_j a0 a1 a2 a3 a4 a5 a6)), d.2 < encode (Rule.HasJ_j a0 a1 a2 a3 a4 a5 a6) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_29 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) (a4 : AuxiliaryCertificates.PolyCert) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_conv a0 a1 a2 a3 a4)), d.2 < encode (Rule.HasJ_conv a0 a1 a2 a3 a4) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_30 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) (a4 : P01D.Poly) (a5 : P01D.Poly) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_piExt a0 a1 a2 a3 a4 a5)), d.2 < encode (Rule.HasJ_piExt a0 a1 a2 a3 a4 a5) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_31 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) (a4 : P01D.Poly) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_allExt a0 a1 a2 a3 a4)), d.2 < encode (Rule.HasJ_allExt a0 a1 a2 a3 a4) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_32 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01AC.Ty) (a4 : P01D.Poly) (a5 : P01D.Poly) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_sigmaElim a0 a1 a2 a3 a4 a5)), d.2 < encode (Rule.HasJ_sigmaElim a0 a1 a2 a3 a4 a5) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_33 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_natInduction a0 a1 a2 a3)), d.2 < encode (Rule.HasJ_natInduction a0 a1 a2 a3) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_34  :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.CtxE_nil)), d.2 < encode (Rule.CtxE_nil) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]

theorem rule_bounds_35 (a0 : P01AC.Tel) (a1 : P01AC.Ty) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.CtxE_ext a0 a1)), d.2 < encode (Rule.CtxE_ext a0 a1) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_36 (a0 : P01AC.Tel) (a1 : Nat) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.FormE_param a0 a1)), d.2 < encode (Rule.FormE_param a0 a1) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_37 (a0 : P01AC.Tel) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.FormE_bottom a0)), d.2 < encode (Rule.FormE_bottom a0) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_38 (a0 : P01AC.Tel) (a1 : P01AC.Ty) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.FormE_all a0 a1)), d.2 < encode (Rule.FormE_all a0 a1) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_39 (a0 : P01AC.Tel) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.FormE_raw a0)), d.2 < encode (Rule.FormE_raw a0) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_40 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.FormE_pi a0 a1 a2)), d.2 < encode (Rule.FormE_pi a0 a1 a2) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_41 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.FormE_sigma a0 a1 a2)), d.2 < encode (Rule.FormE_sigma a0 a1 a2) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_42 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.FormE_identity a0 a1 a2 a3)), d.2 < encode (Rule.FormE_identity a0 a1 a2 a3) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_43 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : Nat) (a3 : AuxiliaryCertificates.LookupCert) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_var a0 a1 a2 a3)), d.2 < encode (Rule.HasE_var a0 a1 a2 a3) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_44 (a0 : P01AC.Tel) (a1 : P01AC.Ty) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_i a0 a1)), d.2 < encode (Rule.HasE_i a0 a1) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_45 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_k a0 a1 a2)), d.2 < encode (Rule.HasE_k a0 a1 a2) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_46 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01AC.Ty) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_s a0 a1 a2 a3)), d.2 < encode (Rule.HasE_s a0 a1 a2 a3) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_47 (a0 : OrthemologyV2.TypeCode) (a1 : P01AC.Tel) (a2 : OrthemologyV2.Term) (a3 : List P01AC.Ty) (a4 : AuxiliaryCertificates.FiniteCert) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_finite a0 a1 a2 a3 a4)), d.2 < encode (Rule.HasE_finite a0 a1 a2 a3 a4) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_48 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_allIntro a0 a1 a2)), d.2 < encode (Rule.HasE_allIntro a0 a1 a2) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_49 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_allElim a0 a1 a2 a3)), d.2 < encode (Rule.HasE_allElim a0 a1 a2 a3) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_50 (a0 : P01AC.Tel) (a1 : OrthemologyV2.Term) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_rawAtom a0 a1)), d.2 < encode (Rule.HasE_rawAtom a0 a1) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_51 (a0 : P01AC.Tel) (a1 : P01D.Poly) (a2 : P01D.Poly) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_rawApp a0 a1 a2)), d.2 < encode (Rule.HasE_rawApp a0 a1 a2) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_52 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_piIntro a0 a1 a2 a3)), d.2 < encode (Rule.HasE_piIntro a0 a1 a2 a3) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_53 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) (a4 : P01D.Poly) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_piElim a0 a1 a2 a3 a4)), d.2 < encode (Rule.HasE_piElim a0 a1 a2 a3 a4) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_54 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) (a4 : P01D.Poly) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_sigmaIntro a0 a1 a2 a3 a4)), d.2 < encode (Rule.HasE_sigmaIntro a0 a1 a2 a3 a4) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_55 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_sigmaFst a0 a1 a2 a3)), d.2 < encode (Rule.HasE_sigmaFst a0 a1 a2 a3) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_56 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_sigmaSnd a0 a1 a2 a3)), d.2 < encode (Rule.HasE_sigmaSnd a0 a1 a2 a3) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_57 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) (a4 : AuxiliaryCertificates.PolyCert) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_identityIntro a0 a1 a2 a3 a4)), d.2 < encode (Rule.HasE_identityIntro a0 a1 a2 a3 a4) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_58 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) (a4 : P01D.Poly) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_proofErase a0 a1 a2 a3 a4)), d.2 < encode (Rule.HasE_proofErase a0 a1 a2 a3 a4) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_59 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01AC.Ty) (a4 : P01D.Poly) (a5 : P01D.Poly) (a6 : P01D.Poly) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_j a0 a1 a2 a3 a4 a5 a6)), d.2 < encode (Rule.HasE_j a0 a1 a2 a3 a4 a5 a6) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_60 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) (a4 : AuxiliaryCertificates.PolyCert) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_conv a0 a1 a2 a3 a4)), d.2 < encode (Rule.HasE_conv a0 a1 a2 a3 a4) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_61 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) (a4 : P01D.Poly) (a5 : P01D.Poly) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_piExt a0 a1 a2 a3 a4 a5)), d.2 < encode (Rule.HasE_piExt a0 a1 a2 a3 a4 a5) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem rule_bounds_62 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) (a4 : P01D.Poly) :
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_allExt a0 a1 a2 a3 a4)), d.2 < encode (Rule.HasE_allExt a0 a1 a2 a3 a4) := by
  simp [localChildren, ruleDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

theorem Rule_bounds (c : Nat) (h : ∃ a : Rule, encode a = c) :
    ∀ d ∈ localChildren ruleDescription c, d.2 < c := by
  obtain ⟨a,rfl⟩ := h
  cases a with
  | CtxJ_ctxBase a0 => exact rule_bounds_0 a0
  | CtxJ_nil  => exact rule_bounds_1 
  | CtxJ_ext a0 a1 => exact rule_bounds_2 a0 a1
  | FormJ_formBase a0 a1 => exact rule_bounds_3 a0 a1
  | FormJ_param a0 a1 => exact rule_bounds_4 a0 a1
  | FormJ_bottom a0 => exact rule_bounds_5 a0
  | FormJ_all a0 a1 => exact rule_bounds_6 a0 a1
  | FormJ_raw a0 => exact rule_bounds_7 a0
  | FormJ_pi a0 a1 a2 => exact rule_bounds_8 a0 a1 a2
  | FormJ_sigma a0 a1 a2 => exact rule_bounds_9 a0 a1 a2
  | FormJ_identity a0 a1 a2 a3 => exact rule_bounds_10 a0 a1 a2 a3
  | HasJ_hasBase a0 a1 a2 => exact rule_bounds_11 a0 a1 a2
  | HasJ_var a0 a1 a2 a3 => exact rule_bounds_12 a0 a1 a2 a3
  | HasJ_i a0 a1 => exact rule_bounds_13 a0 a1
  | HasJ_k a0 a1 a2 => exact rule_bounds_14 a0 a1 a2
  | HasJ_s a0 a1 a2 a3 => exact rule_bounds_15 a0 a1 a2 a3
  | HasJ_finite a0 a1 a2 a3 a4 => exact rule_bounds_16 a0 a1 a2 a3 a4
  | HasJ_allIntro a0 a1 a2 => exact rule_bounds_17 a0 a1 a2
  | HasJ_allElim a0 a1 a2 a3 => exact rule_bounds_18 a0 a1 a2 a3
  | HasJ_rawAtom a0 a1 => exact rule_bounds_19 a0 a1
  | HasJ_rawApp a0 a1 a2 => exact rule_bounds_20 a0 a1 a2
  | HasJ_piIntro a0 a1 a2 a3 => exact rule_bounds_21 a0 a1 a2 a3
  | HasJ_piElim a0 a1 a2 a3 a4 => exact rule_bounds_22 a0 a1 a2 a3 a4
  | HasJ_sigmaIntro a0 a1 a2 a3 a4 => exact rule_bounds_23 a0 a1 a2 a3 a4
  | HasJ_sigmaFst a0 a1 a2 a3 => exact rule_bounds_24 a0 a1 a2 a3
  | HasJ_sigmaSnd a0 a1 a2 a3 => exact rule_bounds_25 a0 a1 a2 a3
  | HasJ_identityIntro a0 a1 a2 a3 a4 => exact rule_bounds_26 a0 a1 a2 a3 a4
  | HasJ_proofErase a0 a1 a2 a3 a4 => exact rule_bounds_27 a0 a1 a2 a3 a4
  | HasJ_j a0 a1 a2 a3 a4 a5 a6 => exact rule_bounds_28 a0 a1 a2 a3 a4 a5 a6
  | HasJ_conv a0 a1 a2 a3 a4 => exact rule_bounds_29 a0 a1 a2 a3 a4
  | HasJ_piExt a0 a1 a2 a3 a4 a5 => exact rule_bounds_30 a0 a1 a2 a3 a4 a5
  | HasJ_allExt a0 a1 a2 a3 a4 => exact rule_bounds_31 a0 a1 a2 a3 a4
  | HasJ_sigmaElim a0 a1 a2 a3 a4 a5 => exact rule_bounds_32 a0 a1 a2 a3 a4 a5
  | HasJ_natInduction a0 a1 a2 a3 => exact rule_bounds_33 a0 a1 a2 a3
  | CtxE_nil  => exact rule_bounds_34 
  | CtxE_ext a0 a1 => exact rule_bounds_35 a0 a1
  | FormE_param a0 a1 => exact rule_bounds_36 a0 a1
  | FormE_bottom a0 => exact rule_bounds_37 a0
  | FormE_all a0 a1 => exact rule_bounds_38 a0 a1
  | FormE_raw a0 => exact rule_bounds_39 a0
  | FormE_pi a0 a1 a2 => exact rule_bounds_40 a0 a1 a2
  | FormE_sigma a0 a1 a2 => exact rule_bounds_41 a0 a1 a2
  | FormE_identity a0 a1 a2 a3 => exact rule_bounds_42 a0 a1 a2 a3
  | HasE_var a0 a1 a2 a3 => exact rule_bounds_43 a0 a1 a2 a3
  | HasE_i a0 a1 => exact rule_bounds_44 a0 a1
  | HasE_k a0 a1 a2 => exact rule_bounds_45 a0 a1 a2
  | HasE_s a0 a1 a2 a3 => exact rule_bounds_46 a0 a1 a2 a3
  | HasE_finite a0 a1 a2 a3 a4 => exact rule_bounds_47 a0 a1 a2 a3 a4
  | HasE_allIntro a0 a1 a2 => exact rule_bounds_48 a0 a1 a2
  | HasE_allElim a0 a1 a2 a3 => exact rule_bounds_49 a0 a1 a2 a3
  | HasE_rawAtom a0 a1 => exact rule_bounds_50 a0 a1
  | HasE_rawApp a0 a1 a2 => exact rule_bounds_51 a0 a1 a2
  | HasE_piIntro a0 a1 a2 a3 => exact rule_bounds_52 a0 a1 a2 a3
  | HasE_piElim a0 a1 a2 a3 a4 => exact rule_bounds_53 a0 a1 a2 a3 a4
  | HasE_sigmaIntro a0 a1 a2 a3 a4 => exact rule_bounds_54 a0 a1 a2 a3 a4
  | HasE_sigmaFst a0 a1 a2 a3 => exact rule_bounds_55 a0 a1 a2 a3
  | HasE_sigmaSnd a0 a1 a2 a3 => exact rule_bounds_56 a0 a1 a2 a3
  | HasE_identityIntro a0 a1 a2 a3 a4 => exact rule_bounds_57 a0 a1 a2 a3 a4
  | HasE_proofErase a0 a1 a2 a3 a4 => exact rule_bounds_58 a0 a1 a2 a3 a4
  | HasE_j a0 a1 a2 a3 a4 a5 a6 => exact rule_bounds_59 a0 a1 a2 a3 a4 a5 a6
  | HasE_conv a0 a1 a2 a3 a4 => exact rule_bounds_60 a0 a1 a2 a3 a4
  | HasE_piExt a0 a1 a2 a3 a4 a5 => exact rule_bounds_61 a0 a1 a2 a3 a4 a5
  | HasE_allExt a0 a1 a2 a3 a4 => exact rule_bounds_62 a0 a1 a2 a3 a4

end CertificateCodeValidity
