import RuleCodeBasics
import LookupCode
import PolyExact
namespace CodedRuleTemplates
open P01D P01AC Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity CodedPolyTransformations CodedMixedTransformations
open AuxiliaryCodeComputability CertificateCodeValidity TelescopeCodeValidity JointCertificates
set_option maxRecDepth 32768
set_option maxHeartbeats 200000
set_option linter.unusedVariables false
attribute [local irreducible] Nat.pair


def side_CtxJ_ctxBase (c : Nat) : Bool := true
theorem primrec_side_CtxJ_ctxBase : Primrec side_CtxJ_ctxBase := by
  have h : Primrec (fun c : Nat => true) := (Primrec.const true)
  exact h.of_eq (by intro c; dsimp only [side_CtxJ_ctxBase])
@[simp] theorem side_CtxJ_ctxBase_exact (Γ : P01AC.Tel) : side_CtxJ_ctxBase (encode (Rule.CtxJ_ctxBase Γ)) = (Rule.CtxJ_ctxBase Γ).checkSide := by
  simp only [side_CtxJ_ctxBase,Rule.checkSide,encode_Rule_CtxJ_ctxBase,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_CtxJ_nil (c : Nat) : Bool := true
theorem primrec_side_CtxJ_nil : Primrec side_CtxJ_nil := by
  have h : Primrec (fun c : Nat => true) := (Primrec.const true)
  exact h.of_eq (by intro c; dsimp only [side_CtxJ_nil])
@[simp] theorem side_CtxJ_nil_exact  : side_CtxJ_nil (encode (Rule.CtxJ_nil )) = (Rule.CtxJ_nil ).checkSide := by
  simp only [side_CtxJ_nil,Rule.checkSide,encode_Rule_CtxJ_nil,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_CtxJ_ext (c : Nat) : Bool := true
theorem primrec_side_CtxJ_ext : Primrec side_CtxJ_ext := by
  have h : Primrec (fun c : Nat => true) := (Primrec.const true)
  exact h.of_eq (by intro c; dsimp only [side_CtxJ_ext])
@[simp] theorem side_CtxJ_ext_exact (Γ : P01AC.Tel) (A : P01AC.Ty) : side_CtxJ_ext (encode (Rule.CtxJ_ext Γ A)) = (Rule.CtxJ_ext Γ A).checkSide := by
  simp only [side_CtxJ_ext,Rule.checkSide,encode_Rule_CtxJ_ext,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_FormJ_formBase (c : Nat) : Bool := true
theorem primrec_side_FormJ_formBase : Primrec side_FormJ_formBase := by
  have h : Primrec (fun c : Nat => true) := (Primrec.const true)
  exact h.of_eq (by intro c; dsimp only [side_FormJ_formBase])
@[simp] theorem side_FormJ_formBase_exact (Γ : P01AC.Tel) (A : P01AC.Ty) : side_FormJ_formBase (encode (Rule.FormJ_formBase Γ A)) = (Rule.FormJ_formBase Γ A).checkSide := by
  simp only [side_FormJ_formBase,Rule.checkSide,encode_Rule_FormJ_formBase,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_FormJ_param (c : Nat) : Bool := true
theorem primrec_side_FormJ_param : Primrec side_FormJ_param := by
  have h : Primrec (fun c : Nat => true) := (Primrec.const true)
  exact h.of_eq (by intro c; dsimp only [side_FormJ_param])
@[simp] theorem side_FormJ_param_exact (Γ : P01AC.Tel) (n : Nat) : side_FormJ_param (encode (Rule.FormJ_param Γ n)) = (Rule.FormJ_param Γ n).checkSide := by
  simp only [side_FormJ_param,Rule.checkSide,encode_Rule_FormJ_param,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_FormJ_bottom (c : Nat) : Bool := true
theorem primrec_side_FormJ_bottom : Primrec side_FormJ_bottom := by
  have h : Primrec (fun c : Nat => true) := (Primrec.const true)
  exact h.of_eq (by intro c; dsimp only [side_FormJ_bottom])
@[simp] theorem side_FormJ_bottom_exact (Γ : P01AC.Tel) : side_FormJ_bottom (encode (Rule.FormJ_bottom Γ)) = (Rule.FormJ_bottom Γ).checkSide := by
  simp only [side_FormJ_bottom,Rule.checkSide,encode_Rule_FormJ_bottom,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_FormJ_all (c : Nat) : Bool := true
theorem primrec_side_FormJ_all : Primrec side_FormJ_all := by
  have h : Primrec (fun c : Nat => true) := (Primrec.const true)
  exact h.of_eq (by intro c; dsimp only [side_FormJ_all])
@[simp] theorem side_FormJ_all_exact (Γ : P01AC.Tel) (B : P01AC.Ty) : side_FormJ_all (encode (Rule.FormJ_all Γ B)) = (Rule.FormJ_all Γ B).checkSide := by
  simp only [side_FormJ_all,Rule.checkSide,encode_Rule_FormJ_all,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_FormJ_raw (c : Nat) : Bool := true
theorem primrec_side_FormJ_raw : Primrec side_FormJ_raw := by
  have h : Primrec (fun c : Nat => true) := (Primrec.const true)
  exact h.of_eq (by intro c; dsimp only [side_FormJ_raw])
@[simp] theorem side_FormJ_raw_exact (Γ : P01AC.Tel) : side_FormJ_raw (encode (Rule.FormJ_raw Γ)) = (Rule.FormJ_raw Γ).checkSide := by
  simp only [side_FormJ_raw,Rule.checkSide,encode_Rule_FormJ_raw,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_FormJ_pi (c : Nat) : Bool := true
theorem primrec_side_FormJ_pi : Primrec side_FormJ_pi := by
  have h : Primrec (fun c : Nat => true) := (Primrec.const true)
  exact h.of_eq (by intro c; dsimp only [side_FormJ_pi])
@[simp] theorem side_FormJ_pi_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : side_FormJ_pi (encode (Rule.FormJ_pi Γ A B)) = (Rule.FormJ_pi Γ A B).checkSide := by
  simp only [side_FormJ_pi,Rule.checkSide,encode_Rule_FormJ_pi,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_FormJ_sigma (c : Nat) : Bool := true
theorem primrec_side_FormJ_sigma : Primrec side_FormJ_sigma := by
  have h : Primrec (fun c : Nat => true) := (Primrec.const true)
  exact h.of_eq (by intro c; dsimp only [side_FormJ_sigma])
@[simp] theorem side_FormJ_sigma_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : side_FormJ_sigma (encode (Rule.FormJ_sigma Γ A B)) = (Rule.FormJ_sigma Γ A B).checkSide := by
  simp only [side_FormJ_sigma,Rule.checkSide,encode_Rule_FormJ_sigma,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_FormJ_identity (c : Nat) : Bool := true
theorem primrec_side_FormJ_identity : Primrec side_FormJ_identity := by
  have h : Primrec (fun c : Nat => true) := (Primrec.const true)
  exact h.of_eq (by intro c; dsimp only [side_FormJ_identity])
@[simp] theorem side_FormJ_identity_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) : side_FormJ_identity (encode (Rule.FormJ_identity Γ A p q)) = (Rule.FormJ_identity Γ A p q).checkSide := by
  simp only [side_FormJ_identity,Rule.checkSide,encode_Rule_FormJ_identity,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasJ_hasBase (c : Nat) : Bool := true
theorem primrec_side_HasJ_hasBase : Primrec side_HasJ_hasBase := by
  have h : Primrec (fun c : Nat => true) := (Primrec.const true)
  exact h.of_eq (by intro c; dsimp only [side_HasJ_hasBase])
@[simp] theorem side_HasJ_hasBase_exact (Γ : P01AC.Tel) (p : P01D.Poly) (A : P01AC.Ty) : side_HasJ_hasBase (encode (Rule.HasJ_hasBase Γ p A)) = (Rule.HasJ_hasBase Γ p A).checkSide := by
  simp only [side_HasJ_hasBase,Rule.checkSide,encode_Rule_HasJ_hasBase,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasJ_var (c : Nat) : Bool := ((checkLookupCode (ruleField c 3) (ruleField c 0) (ruleField c 2) (ruleField c 1)) && true)
theorem primrec_side_HasJ_var : Primrec side_HasJ_var := by
  have h : Primrec (fun c : Nat => ((checkLookupCode (ruleField c 3) (ruleField c 0) (ruleField c 2) (ruleField c 1)) && true)) := (Primrec.and.comp (primrec_checkLookupCode.comp ((primrec_ruleField.comp Primrec.id (.const 3)).pair ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 1)))))) (Primrec.const true))
  exact h.of_eq (by intro c; dsimp only [side_HasJ_var])
@[simp] theorem side_HasJ_var_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (n : Nat) (aux0 : AuxiliaryCertificates.LookupCert) : side_HasJ_var (encode (Rule.HasJ_var Γ A n aux0)) = (Rule.HasJ_var Γ A n aux0).checkSide := by
  simp only [side_HasJ_var,Rule.checkSide,encode_Rule_HasJ_var,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasJ_i (c : Nat) : Bool := true
theorem primrec_side_HasJ_i : Primrec side_HasJ_i := by
  have h : Primrec (fun c : Nat => true) := (Primrec.const true)
  exact h.of_eq (by intro c; dsimp only [side_HasJ_i])
@[simp] theorem side_HasJ_i_exact (Γ : P01AC.Tel) (A : P01AC.Ty) : side_HasJ_i (encode (Rule.HasJ_i Γ A)) = (Rule.HasJ_i Γ A).checkSide := by
  simp only [side_HasJ_i,Rule.checkSide,encode_Rule_HasJ_i,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasJ_k (c : Nat) : Bool := true
theorem primrec_side_HasJ_k : Primrec side_HasJ_k := by
  have h : Primrec (fun c : Nat => true) := (Primrec.const true)
  exact h.of_eq (by intro c; dsimp only [side_HasJ_k])
@[simp] theorem side_HasJ_k_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : side_HasJ_k (encode (Rule.HasJ_k Γ A B)) = (Rule.HasJ_k Γ A B).checkSide := by
  simp only [side_HasJ_k,Rule.checkSide,encode_Rule_HasJ_k,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasJ_s (c : Nat) : Bool := true
theorem primrec_side_HasJ_s : Primrec side_HasJ_s := by
  have h : Primrec (fun c : Nat => true) := (Primrec.const true)
  exact h.of_eq (by intro c; dsimp only [side_HasJ_s])
@[simp] theorem side_HasJ_s_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (C : P01AC.Ty) : side_HasJ_s (encode (Rule.HasJ_s Γ A B C)) = (Rule.HasJ_s Γ A B C).checkSide := by
  simp only [side_HasJ_s,Rule.checkSide,encode_Rule_HasJ_s,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

end CodedRuleTemplates
