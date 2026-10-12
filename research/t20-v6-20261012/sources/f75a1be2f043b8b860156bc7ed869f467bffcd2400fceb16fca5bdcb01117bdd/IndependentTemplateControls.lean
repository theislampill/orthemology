import RuleConclusionCode
import RulePremisesCode
import RuleSideCode
namespace IndependentRuleMapReview
open Encodable CodedRuleTemplates P01D P01AC JointCertificates AuxiliaryCertificates OrthemologyV2
open SourceFamilyComputability CodedPolyTransformations CodedMixedTransformations TelescopeCodeValidity
set_option maxRecDepth 32768
set_option maxHeartbeats 4000000
attribute [local irreducible] Nat.pair

-- These raw code equations unfold the implementations, without using any code-exactness theorem.
theorem raw_branch_orientation (d a b : Nat) : branchAtCode d a b = substituteCode ([b,a],0) d := rfl
theorem raw_motive_orientation (B y e : Nat) : motiveAtCode B y e = substTyCode ([e,y],0) B := rfl
theorem raw_branch_offset (P : Nat) : branchTypeCode P = substTyCode ([encode (pairPoly (.var 1) (.var 0))],2) P := rfl
theorem raw_successor_offset (P : Nat) : successorFamilyCode P = substTyCode ([encode (BooleanPrimitive.succPoly.app (.var 0))],1) P := rfl
theorem raw_section_double_shift (p s : Nat) : sectionPolyCode p s = abstractCode (sectionBodyCode (shiftCode 1 p) (shiftCode 1 s) (encode (Poly.var 0))) := rfl
theorem raw_uncurried_step (s : Nat) : uncurriedStepCode s = appCode (appCode (shiftCode 1 s) (encode (fstPoly (.var 0)))) (encode (sndPoly (.var 0))) := rfl
theorem raw_theta_order (Γ : List Nat) (A x : Nat) : thetaListCode Γ A x = identityTyCode (wkTyCode A) (shiftCode 1 x) (encode (Poly.var 0)) :: A :: Γ := rfl

-- Expected source equations are independently evaluated at the unchanged syntax functions.
theorem source_branch_orientation (a b : Poly) : SigmaCompletion.branchAt (.app (.var 0) (.var 1)) a b = .app b a := rfl
theorem source_full_instantiation (a b : Poly) : SigmaCompletion.branchAt (.var 2) a b = .var 0 := rfl
theorem source_branch_offset : SigmaCompletion.branchType (.identity .raw (.var 1) (.var 2)) = .identity .raw (.var 2) (.var 3) := rfl
theorem source_branch_pi_binder : SigmaCompletion.branchType (.pi .raw (.identity .raw (.var 1) (.var 2))) = .pi .raw (.identity .raw (pren Nat.succ (pairPoly (.var 1) (.var 0))) (.var 3)) := rfl
theorem source_motive_all_no_term_lift (y e : Poly) : motiveAt (.all (.identity .raw (.var 0) (.var 1))) y e = .all (.identity .raw e y) := rfl
theorem source_motive_pi_lift (y e : Poly) : motiveAt (.pi .raw (.identity .raw (.var 1) (.var 2))) y e = .pi .raw (.identity .raw (pren Nat.succ e) (pren Nat.succ y)) := rfl
theorem source_theta_order (Γ : Tel) (A : Ty) (x : Poly) : theta Γ A x = .identity (wk A) (pren Nat.succ x) (.var 0) :: A :: Γ := rfl

-- Every image, including unused and duplicate entries, is retained in source order.
theorem finiteJ_all_images (C : TypeCode) (Γ : Tel) (t : Term) (τ : List Ty) (c : FiniteCert) :
    (Rule.HasJ_finite C Γ t τ c).premises = τ.map (Claim.formJ Γ) ++ [Claim.formJ Γ (tsubst (typeImages τ) (fin C))] := by
  simp only [Rule.premises, ofFn_typeImages]
theorem finiteE_all_images (C : TypeCode) (Γ : Tel) (t : Term) (τ : List Ty) (c : FiniteCert) :
    (Rule.HasE_finite C Γ t τ c).premises = τ.map (Claim.formE Γ) ++ [Claim.formE Γ (tsubst (typeImages τ) (fin C))] := by
  simp only [Rule.premises, ofFn_typeImages]
theorem generic_transport_without_Primcodable {α : Type*} [Encodable α] (xs : List α) :
    listNatDecode (encode xs) = xs.map encode := listNatDecode_encode xs

theorem sigma_elim_root_order (Γ : Tel) (A B P : Ty) (d z : Poly) :
    (Rule.HasJ_sigmaElim Γ A B P d z).premises =
      [.ctxJ Γ,.formJ Γ A,.formJ (A::Γ) B,.formJ (A.sigma B::Γ) P,
       .hasJ (B::A::Γ) d (SigmaCompletion.branchType P),.hasJ Γ z (A.sigma B)] := rfl
theorem induction_root_order (Γ : Tel) (P : Ty) (p s : Poly) :
    (Rule.HasJ_natInduction Γ P p s).premises =
      [.ctxJ Γ,.formJ (EffectiveCompleteness.N::Γ) P,.hasJ Γ p (inst P SourceRigidity.zero),.hasJ Γ s (RigidityInitiality.dependentStepType P)] := rfl

-- Auxiliary maps are actual functions of the supplied payloads and endpoints.
theorem raw_lookup_actual (c : Nat) : side_HasJ_var c =
    (AuxiliaryCodeComputability.checkLookupCode (ruleField c 3) (ruleField c 0) (ruleField c 2) (ruleField c 1) && true) := rfl
theorem raw_finite_actual (c : Nat) : side_HasE_finite c =
    (decide (finSupportCode (ruleField c 0) ≤ telLengthCode (ruleField c 3)) &&
      (AuxiliaryCodeComputability.checkFiniteCode (ruleField c 4) (ruleField c 2) (ruleField c 0) && true)) := rfl
theorem raw_poly_actual (c : Nat) : side_HasJ_identityIntro c =
    (AuxiliaryCodeComputability.checkPolyCode (ruleField c 4) (ruleField c 2) (ruleField c 3) && true) := rfl

-- Some malformed codes intentionally satisfy a side condition: no source-domain validator is claimed.
theorem malformed_side_accepted : checkSideCode (AuxiliaryCodeComputability.pack 1 [SourceFamilyComputability.leaf 99]) = true := by
  simp [checkSideCode,sideDispatch0,sideDispatch1,side_CtxJ_nil,CertificateCodeValidity.tag_pack]
theorem source_base_context (Γ : Tel) : (Rule.CtxJ_ctxBase Γ).premises = [.ctxE Γ] := rfl
theorem source_base_formation (Γ : Tel) (A : Ty) : (Rule.FormJ_formBase Γ A).premises = [.formE Γ A] := rfl
theorem source_base_typing (Γ : Tel) (p : Poly) (A : Ty) : (Rule.HasJ_hasBase Γ p A).premises = [.hasE Γ p A] := rfl

theorem raw_sigma_elimination_slots (c : Nat) : conclusion_HasJ_sigmaElim c =
    hasCode 2 (ruleField c 0)
      (branchAtCode (ruleField c 4) (fstPolyCode (ruleField c 5)) (sndPolyCode (ruleField c 5)))
      (instTyCode (ruleField c 5) (ruleField c 3)) := rfl
theorem raw_J_slots (c : Nat) : conclusion_HasE_j c =
    hasCode 5 (ruleField c 0) (jPolyCode (ruleField c 6) (ruleField c 4) (ruleField c 5))
      (motiveAtCode (ruleField c 3) (ruleField c 4) (ruleField c 5)) := rfl
end IndependentRuleMapReview
