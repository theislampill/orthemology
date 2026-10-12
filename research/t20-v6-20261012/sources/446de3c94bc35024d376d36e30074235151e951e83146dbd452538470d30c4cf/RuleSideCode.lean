import RuleCodeBasics
import LookupCode
import PolyExact
namespace CodedRuleTemplates
open P01D P01AC Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity CodedPolyTransformations CodedMixedTransformations
open AuxiliaryCodeComputability CertificateCodeValidity TelescopeCodeValidity JointCertificates
set_option maxRecDepth 32768
set_option maxHeartbeats 12000000
set_option linter.unusedVariables false
attribute [local irreducible] Nat.pair


def side_CtxJ_ctxBase (c : Nat) : Bool := true
theorem primrec_side_CtxJ_ctxBase : Primrec side_CtxJ_ctxBase := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_CtxJ_ctxBase,id,Nat.succ_eq_add_one])
@[simp] theorem side_CtxJ_ctxBase_exact (Γ : P01AC.Tel) : side_CtxJ_ctxBase (encode (Rule.CtxJ_ctxBase Γ)) = (Rule.CtxJ_ctxBase Γ).checkSide := by
  simp only [side_CtxJ_ctxBase,Rule.checkSide,encode_Rule_CtxJ_ctxBase,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_CtxJ_nil (c : Nat) : Bool := true
theorem primrec_side_CtxJ_nil : Primrec side_CtxJ_nil := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_CtxJ_nil,id,Nat.succ_eq_add_one])
@[simp] theorem side_CtxJ_nil_exact  : side_CtxJ_nil (encode (Rule.CtxJ_nil )) = (Rule.CtxJ_nil ).checkSide := by
  simp only [side_CtxJ_nil,Rule.checkSide,encode_Rule_CtxJ_nil,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_CtxJ_ext (c : Nat) : Bool := true
theorem primrec_side_CtxJ_ext : Primrec side_CtxJ_ext := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_CtxJ_ext,id,Nat.succ_eq_add_one])
@[simp] theorem side_CtxJ_ext_exact (Γ : P01AC.Tel) (A : P01AC.Ty) : side_CtxJ_ext (encode (Rule.CtxJ_ext Γ A)) = (Rule.CtxJ_ext Γ A).checkSide := by
  simp only [side_CtxJ_ext,Rule.checkSide,encode_Rule_CtxJ_ext,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_FormJ_formBase (c : Nat) : Bool := true
theorem primrec_side_FormJ_formBase : Primrec side_FormJ_formBase := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_FormJ_formBase,id,Nat.succ_eq_add_one])
@[simp] theorem side_FormJ_formBase_exact (Γ : P01AC.Tel) (A : P01AC.Ty) : side_FormJ_formBase (encode (Rule.FormJ_formBase Γ A)) = (Rule.FormJ_formBase Γ A).checkSide := by
  simp only [side_FormJ_formBase,Rule.checkSide,encode_Rule_FormJ_formBase,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_FormJ_param (c : Nat) : Bool := true
theorem primrec_side_FormJ_param : Primrec side_FormJ_param := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_FormJ_param,id,Nat.succ_eq_add_one])
@[simp] theorem side_FormJ_param_exact (Γ : P01AC.Tel) (n : Nat) : side_FormJ_param (encode (Rule.FormJ_param Γ n)) = (Rule.FormJ_param Γ n).checkSide := by
  simp only [side_FormJ_param,Rule.checkSide,encode_Rule_FormJ_param,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_FormJ_bottom (c : Nat) : Bool := true
theorem primrec_side_FormJ_bottom : Primrec side_FormJ_bottom := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_FormJ_bottom,id,Nat.succ_eq_add_one])
@[simp] theorem side_FormJ_bottom_exact (Γ : P01AC.Tel) : side_FormJ_bottom (encode (Rule.FormJ_bottom Γ)) = (Rule.FormJ_bottom Γ).checkSide := by
  simp only [side_FormJ_bottom,Rule.checkSide,encode_Rule_FormJ_bottom,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_FormJ_all (c : Nat) : Bool := true
theorem primrec_side_FormJ_all : Primrec side_FormJ_all := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_FormJ_all,id,Nat.succ_eq_add_one])
@[simp] theorem side_FormJ_all_exact (Γ : P01AC.Tel) (B : P01AC.Ty) : side_FormJ_all (encode (Rule.FormJ_all Γ B)) = (Rule.FormJ_all Γ B).checkSide := by
  simp only [side_FormJ_all,Rule.checkSide,encode_Rule_FormJ_all,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_FormJ_raw (c : Nat) : Bool := true
theorem primrec_side_FormJ_raw : Primrec side_FormJ_raw := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_FormJ_raw,id,Nat.succ_eq_add_one])
@[simp] theorem side_FormJ_raw_exact (Γ : P01AC.Tel) : side_FormJ_raw (encode (Rule.FormJ_raw Γ)) = (Rule.FormJ_raw Γ).checkSide := by
  simp only [side_FormJ_raw,Rule.checkSide,encode_Rule_FormJ_raw,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_FormJ_pi (c : Nat) : Bool := true
theorem primrec_side_FormJ_pi : Primrec side_FormJ_pi := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_FormJ_pi,id,Nat.succ_eq_add_one])
@[simp] theorem side_FormJ_pi_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : side_FormJ_pi (encode (Rule.FormJ_pi Γ A B)) = (Rule.FormJ_pi Γ A B).checkSide := by
  simp only [side_FormJ_pi,Rule.checkSide,encode_Rule_FormJ_pi,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_FormJ_sigma (c : Nat) : Bool := true
theorem primrec_side_FormJ_sigma : Primrec side_FormJ_sigma := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_FormJ_sigma,id,Nat.succ_eq_add_one])
@[simp] theorem side_FormJ_sigma_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : side_FormJ_sigma (encode (Rule.FormJ_sigma Γ A B)) = (Rule.FormJ_sigma Γ A B).checkSide := by
  simp only [side_FormJ_sigma,Rule.checkSide,encode_Rule_FormJ_sigma,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_FormJ_identity (c : Nat) : Bool := true
theorem primrec_side_FormJ_identity : Primrec side_FormJ_identity := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_FormJ_identity,id,Nat.succ_eq_add_one])
@[simp] theorem side_FormJ_identity_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) : side_FormJ_identity (encode (Rule.FormJ_identity Γ A p q)) = (Rule.FormJ_identity Γ A p q).checkSide := by
  simp only [side_FormJ_identity,Rule.checkSide,encode_Rule_FormJ_identity,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasJ_hasBase (c : Nat) : Bool := true
theorem primrec_side_HasJ_hasBase : Primrec side_HasJ_hasBase := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_HasJ_hasBase,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasJ_hasBase_exact (Γ : P01AC.Tel) (p : P01D.Poly) (A : P01AC.Ty) : side_HasJ_hasBase (encode (Rule.HasJ_hasBase Γ p A)) = (Rule.HasJ_hasBase Γ p A).checkSide := by
  simp only [side_HasJ_hasBase,Rule.checkSide,encode_Rule_HasJ_hasBase,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasJ_var (c : Nat) : Bool := ((checkLookupCode (ruleField c 3) (ruleField c 0) (ruleField c 2) (ruleField c 1)) && true)
theorem primrec_side_HasJ_var : Primrec side_HasJ_var := by
  have h := (Primrec.and.comp (primrec_checkLookupCode.comp ((primrec_ruleField.comp Primrec.id (.const 3)).pair ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 1)))))) (Primrec.const true))
  exact h.of_eq (by intro c; simp only [side_HasJ_var,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasJ_var_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (n : Nat) (aux0 : AuxiliaryCertificates.LookupCert) : side_HasJ_var (encode (Rule.HasJ_var Γ A n aux0)) = (Rule.HasJ_var Γ A n aux0).checkSide := by
  simp only [side_HasJ_var,Rule.checkSide,encode_Rule_HasJ_var,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasJ_i (c : Nat) : Bool := true
theorem primrec_side_HasJ_i : Primrec side_HasJ_i := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_HasJ_i,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasJ_i_exact (Γ : P01AC.Tel) (A : P01AC.Ty) : side_HasJ_i (encode (Rule.HasJ_i Γ A)) = (Rule.HasJ_i Γ A).checkSide := by
  simp only [side_HasJ_i,Rule.checkSide,encode_Rule_HasJ_i,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasJ_k (c : Nat) : Bool := true
theorem primrec_side_HasJ_k : Primrec side_HasJ_k := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_HasJ_k,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasJ_k_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : side_HasJ_k (encode (Rule.HasJ_k Γ A B)) = (Rule.HasJ_k Γ A B).checkSide := by
  simp only [side_HasJ_k,Rule.checkSide,encode_Rule_HasJ_k,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasJ_s (c : Nat) : Bool := true
theorem primrec_side_HasJ_s : Primrec side_HasJ_s := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_HasJ_s,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasJ_s_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (C : P01AC.Ty) : side_HasJ_s (encode (Rule.HasJ_s Γ A B C)) = (Rule.HasJ_s Γ A B C).checkSide := by
  simp only [side_HasJ_s,Rule.checkSide,encode_Rule_HasJ_s,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasJ_finite (c : Nat) : Bool := (decide ((finSupportCode (ruleField c 0)) ≤ (telLengthCode (ruleField c 3))) && ((checkFiniteCode (ruleField c 4) (ruleField c 2) (ruleField c 0)) && true))
theorem primrec_side_HasJ_finite : Primrec side_HasJ_finite := by
  have h := (Primrec.and.comp (Primrec.nat_le.comp (primrec_finSupportCode.comp (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_telLengthCode.comp (primrec_ruleField.comp Primrec.id (.const 3)))) (Primrec.and.comp (primrec_checkFiniteCode.comp ((primrec_ruleField.comp Primrec.id (.const 4)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 0))))) (Primrec.const true)))
  exact h.of_eq (by intro c; simp only [side_HasJ_finite,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasJ_finite_exact (C : OrthemologyV2.TypeCode) (Γ : P01AC.Tel) (t : OrthemologyV2.Term) (τ : List P01AC.Ty) (aux0 : AuxiliaryCertificates.FiniteCert) : side_HasJ_finite (encode (Rule.HasJ_finite C Γ t τ aux0)) = (Rule.HasJ_finite C Γ t τ aux0).checkSide := by
  simp only [side_HasJ_finite,Rule.checkSide,encode_Rule_HasJ_finite,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasJ_allIntro (c : Nat) : Bool := true
theorem primrec_side_HasJ_allIntro : Primrec side_HasJ_allIntro := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_HasJ_allIntro,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasJ_allIntro_exact (Γ : P01AC.Tel) (B : P01AC.Ty) (p : P01D.Poly) : side_HasJ_allIntro (encode (Rule.HasJ_allIntro Γ B p)) = (Rule.HasJ_allIntro Γ B p).checkSide := by
  simp only [side_HasJ_allIntro,Rule.checkSide,encode_Rule_HasJ_allIntro,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasJ_allElim (c : Nat) : Bool := true
theorem primrec_side_HasJ_allElim : Primrec side_HasJ_allElim := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_HasJ_allElim,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasJ_allElim_exact (Γ : P01AC.Tel) (B : P01AC.Ty) (A : P01AC.Ty) (p : P01D.Poly) : side_HasJ_allElim (encode (Rule.HasJ_allElim Γ B A p)) = (Rule.HasJ_allElim Γ B A p).checkSide := by
  simp only [side_HasJ_allElim,Rule.checkSide,encode_Rule_HasJ_allElim,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasJ_rawAtom (c : Nat) : Bool := true
theorem primrec_side_HasJ_rawAtom : Primrec side_HasJ_rawAtom := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_HasJ_rawAtom,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasJ_rawAtom_exact (Γ : P01AC.Tel) (t : OrthemologyV2.Term) : side_HasJ_rawAtom (encode (Rule.HasJ_rawAtom Γ t)) = (Rule.HasJ_rawAtom Γ t).checkSide := by
  simp only [side_HasJ_rawAtom,Rule.checkSide,encode_Rule_HasJ_rawAtom,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasJ_rawApp (c : Nat) : Bool := true
theorem primrec_side_HasJ_rawApp : Primrec side_HasJ_rawApp := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_HasJ_rawApp,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasJ_rawApp_exact (Γ : P01AC.Tel) (f : P01D.Poly) (a : P01D.Poly) : side_HasJ_rawApp (encode (Rule.HasJ_rawApp Γ f a)) = (Rule.HasJ_rawApp Γ f a).checkSide := by
  simp only [side_HasJ_rawApp,Rule.checkSide,encode_Rule_HasJ_rawApp,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasJ_piIntro (c : Nat) : Bool := ((checkScope ((telLengthCode (ruleField c 0))) ((abstractCode (ruleField c 3)))) && true)
theorem primrec_side_HasJ_piIntro : Primrec side_HasJ_piIntro := by
  have h := (Primrec.and.comp (primrec_checkScope.comp (primrec_telLengthCode.comp (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_abstractCode.comp (primrec_ruleField.comp Primrec.id (.const 3)))) (Primrec.const true))
  exact h.of_eq (by intro c; simp only [side_HasJ_piIntro,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasJ_piIntro_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (b : P01D.Poly) : side_HasJ_piIntro (encode (Rule.HasJ_piIntro Γ A B b)) = (Rule.HasJ_piIntro Γ A B b).checkSide := by
  simp only [side_HasJ_piIntro,Rule.checkSide,encode_Rule_HasJ_piIntro,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasJ_piElim (c : Nat) : Bool := true
theorem primrec_side_HasJ_piElim : Primrec side_HasJ_piElim := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_HasJ_piElim,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasJ_piElim_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (a : P01D.Poly) (f : P01D.Poly) : side_HasJ_piElim (encode (Rule.HasJ_piElim Γ A B a f)) = (Rule.HasJ_piElim Γ A B a f).checkSide := by
  simp only [side_HasJ_piElim,Rule.checkSide,encode_Rule_HasJ_piElim,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasJ_sigmaIntro (c : Nat) : Bool := true
theorem primrec_side_HasJ_sigmaIntro : Primrec side_HasJ_sigmaIntro := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_HasJ_sigmaIntro,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasJ_sigmaIntro_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (a : P01D.Poly) (b : P01D.Poly) : side_HasJ_sigmaIntro (encode (Rule.HasJ_sigmaIntro Γ A B a b)) = (Rule.HasJ_sigmaIntro Γ A B a b).checkSide := by
  simp only [side_HasJ_sigmaIntro,Rule.checkSide,encode_Rule_HasJ_sigmaIntro,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasJ_sigmaFst (c : Nat) : Bool := true
theorem primrec_side_HasJ_sigmaFst : Primrec side_HasJ_sigmaFst := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_HasJ_sigmaFst,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasJ_sigmaFst_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (z : P01D.Poly) : side_HasJ_sigmaFst (encode (Rule.HasJ_sigmaFst Γ A B z)) = (Rule.HasJ_sigmaFst Γ A B z).checkSide := by
  simp only [side_HasJ_sigmaFst,Rule.checkSide,encode_Rule_HasJ_sigmaFst,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasJ_sigmaSnd (c : Nat) : Bool := true
theorem primrec_side_HasJ_sigmaSnd : Primrec side_HasJ_sigmaSnd := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_HasJ_sigmaSnd,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasJ_sigmaSnd_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (z : P01D.Poly) : side_HasJ_sigmaSnd (encode (Rule.HasJ_sigmaSnd Γ A B z)) = (Rule.HasJ_sigmaSnd Γ A B z).checkSide := by
  simp only [side_HasJ_sigmaSnd,Rule.checkSide,encode_Rule_HasJ_sigmaSnd,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasJ_identityIntro (c : Nat) : Bool := ((checkPolyCode (ruleField c 4) (ruleField c 2) (ruleField c 3)) && true)
theorem primrec_side_HasJ_identityIntro : Primrec side_HasJ_identityIntro := by
  have h := (Primrec.and.comp (primrec_checkPolyCode.comp ((primrec_ruleField.comp Primrec.id (.const 4)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 3))))) (Primrec.const true))
  exact h.of_eq (by intro c; simp only [side_HasJ_identityIntro,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasJ_identityIntro_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (aux0 : AuxiliaryCertificates.PolyCert) : side_HasJ_identityIntro (encode (Rule.HasJ_identityIntro Γ A p q aux0)) = (Rule.HasJ_identityIntro Γ A p q aux0).checkSide := by
  simp only [side_HasJ_identityIntro,Rule.checkSide,encode_Rule_HasJ_identityIntro,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasJ_proofErase (c : Nat) : Bool := true
theorem primrec_side_HasJ_proofErase : Primrec side_HasJ_proofErase := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_HasJ_proofErase,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasJ_proofErase_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (x : P01D.Poly) (y : P01D.Poly) (p : P01D.Poly) : side_HasJ_proofErase (encode (Rule.HasJ_proofErase Γ A x y p)) = (Rule.HasJ_proofErase Γ A x y p).checkSide := by
  simp only [side_HasJ_proofErase,Rule.checkSide,encode_Rule_HasJ_proofErase,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasJ_j (c : Nat) : Bool := true
theorem primrec_side_HasJ_j : Primrec side_HasJ_j := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_HasJ_j,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasJ_j_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (x : P01D.Poly) (B : P01AC.Ty) (y : P01D.Poly) (e : P01D.Poly) (d : P01D.Poly) : side_HasJ_j (encode (Rule.HasJ_j Γ A x B y e d)) = (Rule.HasJ_j Γ A x B y e d).checkSide := by
  simp only [side_HasJ_j,Rule.checkSide,encode_Rule_HasJ_j,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasJ_conv (c : Nat) : Bool := ((checkPolyCode (ruleField c 4) (ruleField c 2) (ruleField c 3)) && ((checkScope ((telLengthCode (ruleField c 0))) (ruleField c 3)) && true))
theorem primrec_side_HasJ_conv : Primrec side_HasJ_conv := by
  have h := (Primrec.and.comp (primrec_checkPolyCode.comp ((primrec_ruleField.comp Primrec.id (.const 4)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 3))))) (Primrec.and.comp (primrec_checkScope.comp (primrec_telLengthCode.comp (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 3))) (Primrec.const true)))
  exact h.of_eq (by intro c; simp only [side_HasJ_conv,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasJ_conv_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (aux0 : AuxiliaryCertificates.PolyCert) : side_HasJ_conv (encode (Rule.HasJ_conv Γ A p q aux0)) = (Rule.HasJ_conv Γ A p q aux0).checkSide := by
  simp only [side_HasJ_conv,Rule.checkSide,encode_Rule_HasJ_conv,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasJ_piExt (c : Nat) : Bool := ((checkScope ((telLengthCode (ruleField c 0))) (ruleField c 3)) && ((checkScope ((telLengthCode (ruleField c 0))) (ruleField c 4)) && ((checkScope ((telLengthCode (ruleField c 0))) (ruleField c 5)) && ((checkTyScope ((telLengthCode (ruleField c 0))) (ruleField c 1)) && ((checkTyScope (((fun c => telLengthCode c + 1) (ruleField c 0))) (ruleField c 2)) && true)))))
theorem primrec_side_HasJ_piExt : Primrec side_HasJ_piExt := by
  have h := (Primrec.and.comp (primrec_checkScope.comp (primrec_telLengthCode.comp (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 3))) (Primrec.and.comp (primrec_checkScope.comp (primrec_telLengthCode.comp (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 4))) (Primrec.and.comp (primrec_checkScope.comp (primrec_telLengthCode.comp (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 5))) (Primrec.and.comp (primrec_checkTyScope.comp (primrec_telLengthCode.comp (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.and.comp (primrec_checkTyScope.comp ((Primrec.succ.comp primrec_telLengthCode).comp (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 2))) (Primrec.const true))))))
  exact h.of_eq (by intro c; simp only [side_HasJ_piExt,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasJ_piExt_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (h : P01D.Poly) : side_HasJ_piExt (encode (Rule.HasJ_piExt Γ A B p q h)) = (Rule.HasJ_piExt Γ A B p q h).checkSide := by
  simp only [side_HasJ_piExt,Rule.checkSide,encode_Rule_HasJ_piExt,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasJ_allExt (c : Nat) : Bool := ((checkScope ((telLengthCode (ruleField c 0))) (ruleField c 2)) && ((checkScope ((telLengthCode (ruleField c 0))) (ruleField c 3)) && ((checkScope ((telLengthCode (ruleField c 0))) (ruleField c 4)) && ((checkTyScope ((telLengthCode (ruleField c 0))) (ruleField c 1)) && true))))
theorem primrec_side_HasJ_allExt : Primrec side_HasJ_allExt := by
  have h := (Primrec.and.comp (primrec_checkScope.comp (primrec_telLengthCode.comp (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 2))) (Primrec.and.comp (primrec_checkScope.comp (primrec_telLengthCode.comp (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 3))) (Primrec.and.comp (primrec_checkScope.comp (primrec_telLengthCode.comp (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 4))) (Primrec.and.comp (primrec_checkTyScope.comp (primrec_telLengthCode.comp (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.const true)))))
  exact h.of_eq (by intro c; simp only [side_HasJ_allExt,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasJ_allExt_exact (Γ : P01AC.Tel) (B : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (h : P01D.Poly) : side_HasJ_allExt (encode (Rule.HasJ_allExt Γ B p q h)) = (Rule.HasJ_allExt Γ B p q h).checkSide := by
  simp only [side_HasJ_allExt,Rule.checkSide,encode_Rule_HasJ_allExt,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasJ_sigmaElim (c : Nat) : Bool := true
theorem primrec_side_HasJ_sigmaElim : Primrec side_HasJ_sigmaElim := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_HasJ_sigmaElim,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasJ_sigmaElim_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (P : P01AC.Ty) (d : P01D.Poly) (z : P01D.Poly) : side_HasJ_sigmaElim (encode (Rule.HasJ_sigmaElim Γ A B P d z)) = (Rule.HasJ_sigmaElim Γ A B P d z).checkSide := by
  simp only [side_HasJ_sigmaElim,Rule.checkSide,encode_Rule_HasJ_sigmaElim,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasJ_natInduction (c : Nat) : Bool := true
theorem primrec_side_HasJ_natInduction : Primrec side_HasJ_natInduction := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_HasJ_natInduction,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasJ_natInduction_exact (Γ : P01AC.Tel) (P : P01AC.Ty) (p : P01D.Poly) (s : P01D.Poly) : side_HasJ_natInduction (encode (Rule.HasJ_natInduction Γ P p s)) = (Rule.HasJ_natInduction Γ P p s).checkSide := by
  simp only [side_HasJ_natInduction,Rule.checkSide,encode_Rule_HasJ_natInduction,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_CtxE_nil (c : Nat) : Bool := true
theorem primrec_side_CtxE_nil : Primrec side_CtxE_nil := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_CtxE_nil,id,Nat.succ_eq_add_one])
@[simp] theorem side_CtxE_nil_exact  : side_CtxE_nil (encode (Rule.CtxE_nil )) = (Rule.CtxE_nil ).checkSide := by
  simp only [side_CtxE_nil,Rule.checkSide,encode_Rule_CtxE_nil,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_CtxE_ext (c : Nat) : Bool := true
theorem primrec_side_CtxE_ext : Primrec side_CtxE_ext := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_CtxE_ext,id,Nat.succ_eq_add_one])
@[simp] theorem side_CtxE_ext_exact (Γ : P01AC.Tel) (A : P01AC.Ty) : side_CtxE_ext (encode (Rule.CtxE_ext Γ A)) = (Rule.CtxE_ext Γ A).checkSide := by
  simp only [side_CtxE_ext,Rule.checkSide,encode_Rule_CtxE_ext,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_FormE_param (c : Nat) : Bool := true
theorem primrec_side_FormE_param : Primrec side_FormE_param := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_FormE_param,id,Nat.succ_eq_add_one])
@[simp] theorem side_FormE_param_exact (Γ : P01AC.Tel) (n : Nat) : side_FormE_param (encode (Rule.FormE_param Γ n)) = (Rule.FormE_param Γ n).checkSide := by
  simp only [side_FormE_param,Rule.checkSide,encode_Rule_FormE_param,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_FormE_bottom (c : Nat) : Bool := true
theorem primrec_side_FormE_bottom : Primrec side_FormE_bottom := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_FormE_bottom,id,Nat.succ_eq_add_one])
@[simp] theorem side_FormE_bottom_exact (Γ : P01AC.Tel) : side_FormE_bottom (encode (Rule.FormE_bottom Γ)) = (Rule.FormE_bottom Γ).checkSide := by
  simp only [side_FormE_bottom,Rule.checkSide,encode_Rule_FormE_bottom,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_FormE_all (c : Nat) : Bool := true
theorem primrec_side_FormE_all : Primrec side_FormE_all := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_FormE_all,id,Nat.succ_eq_add_one])
@[simp] theorem side_FormE_all_exact (Γ : P01AC.Tel) (B : P01AC.Ty) : side_FormE_all (encode (Rule.FormE_all Γ B)) = (Rule.FormE_all Γ B).checkSide := by
  simp only [side_FormE_all,Rule.checkSide,encode_Rule_FormE_all,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_FormE_raw (c : Nat) : Bool := true
theorem primrec_side_FormE_raw : Primrec side_FormE_raw := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_FormE_raw,id,Nat.succ_eq_add_one])
@[simp] theorem side_FormE_raw_exact (Γ : P01AC.Tel) : side_FormE_raw (encode (Rule.FormE_raw Γ)) = (Rule.FormE_raw Γ).checkSide := by
  simp only [side_FormE_raw,Rule.checkSide,encode_Rule_FormE_raw,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_FormE_pi (c : Nat) : Bool := true
theorem primrec_side_FormE_pi : Primrec side_FormE_pi := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_FormE_pi,id,Nat.succ_eq_add_one])
@[simp] theorem side_FormE_pi_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : side_FormE_pi (encode (Rule.FormE_pi Γ A B)) = (Rule.FormE_pi Γ A B).checkSide := by
  simp only [side_FormE_pi,Rule.checkSide,encode_Rule_FormE_pi,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_FormE_sigma (c : Nat) : Bool := true
theorem primrec_side_FormE_sigma : Primrec side_FormE_sigma := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_FormE_sigma,id,Nat.succ_eq_add_one])
@[simp] theorem side_FormE_sigma_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : side_FormE_sigma (encode (Rule.FormE_sigma Γ A B)) = (Rule.FormE_sigma Γ A B).checkSide := by
  simp only [side_FormE_sigma,Rule.checkSide,encode_Rule_FormE_sigma,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_FormE_identity (c : Nat) : Bool := true
theorem primrec_side_FormE_identity : Primrec side_FormE_identity := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_FormE_identity,id,Nat.succ_eq_add_one])
@[simp] theorem side_FormE_identity_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) : side_FormE_identity (encode (Rule.FormE_identity Γ A p q)) = (Rule.FormE_identity Γ A p q).checkSide := by
  simp only [side_FormE_identity,Rule.checkSide,encode_Rule_FormE_identity,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasE_var (c : Nat) : Bool := ((checkLookupCode (ruleField c 3) (ruleField c 0) (ruleField c 2) (ruleField c 1)) && true)
theorem primrec_side_HasE_var : Primrec side_HasE_var := by
  have h := (Primrec.and.comp (primrec_checkLookupCode.comp ((primrec_ruleField.comp Primrec.id (.const 3)).pair ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 1)))))) (Primrec.const true))
  exact h.of_eq (by intro c; simp only [side_HasE_var,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasE_var_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (n : Nat) (aux0 : AuxiliaryCertificates.LookupCert) : side_HasE_var (encode (Rule.HasE_var Γ A n aux0)) = (Rule.HasE_var Γ A n aux0).checkSide := by
  simp only [side_HasE_var,Rule.checkSide,encode_Rule_HasE_var,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasE_i (c : Nat) : Bool := true
theorem primrec_side_HasE_i : Primrec side_HasE_i := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_HasE_i,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasE_i_exact (Γ : P01AC.Tel) (A : P01AC.Ty) : side_HasE_i (encode (Rule.HasE_i Γ A)) = (Rule.HasE_i Γ A).checkSide := by
  simp only [side_HasE_i,Rule.checkSide,encode_Rule_HasE_i,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasE_k (c : Nat) : Bool := true
theorem primrec_side_HasE_k : Primrec side_HasE_k := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_HasE_k,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasE_k_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : side_HasE_k (encode (Rule.HasE_k Γ A B)) = (Rule.HasE_k Γ A B).checkSide := by
  simp only [side_HasE_k,Rule.checkSide,encode_Rule_HasE_k,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasE_s (c : Nat) : Bool := true
theorem primrec_side_HasE_s : Primrec side_HasE_s := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_HasE_s,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasE_s_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (C : P01AC.Ty) : side_HasE_s (encode (Rule.HasE_s Γ A B C)) = (Rule.HasE_s Γ A B C).checkSide := by
  simp only [side_HasE_s,Rule.checkSide,encode_Rule_HasE_s,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasE_finite (c : Nat) : Bool := (decide ((finSupportCode (ruleField c 0)) ≤ (telLengthCode (ruleField c 3))) && ((checkFiniteCode (ruleField c 4) (ruleField c 2) (ruleField c 0)) && true))
theorem primrec_side_HasE_finite : Primrec side_HasE_finite := by
  have h := (Primrec.and.comp (Primrec.nat_le.comp (primrec_finSupportCode.comp (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_telLengthCode.comp (primrec_ruleField.comp Primrec.id (.const 3)))) (Primrec.and.comp (primrec_checkFiniteCode.comp ((primrec_ruleField.comp Primrec.id (.const 4)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 0))))) (Primrec.const true)))
  exact h.of_eq (by intro c; simp only [side_HasE_finite,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasE_finite_exact (C : OrthemologyV2.TypeCode) (Γ : P01AC.Tel) (t : OrthemologyV2.Term) (τ : List P01AC.Ty) (aux0 : AuxiliaryCertificates.FiniteCert) : side_HasE_finite (encode (Rule.HasE_finite C Γ t τ aux0)) = (Rule.HasE_finite C Γ t τ aux0).checkSide := by
  simp only [side_HasE_finite,Rule.checkSide,encode_Rule_HasE_finite,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasE_allIntro (c : Nat) : Bool := true
theorem primrec_side_HasE_allIntro : Primrec side_HasE_allIntro := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_HasE_allIntro,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasE_allIntro_exact (Γ : P01AC.Tel) (B : P01AC.Ty) (p : P01D.Poly) : side_HasE_allIntro (encode (Rule.HasE_allIntro Γ B p)) = (Rule.HasE_allIntro Γ B p).checkSide := by
  simp only [side_HasE_allIntro,Rule.checkSide,encode_Rule_HasE_allIntro,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasE_allElim (c : Nat) : Bool := true
theorem primrec_side_HasE_allElim : Primrec side_HasE_allElim := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_HasE_allElim,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasE_allElim_exact (Γ : P01AC.Tel) (B : P01AC.Ty) (A : P01AC.Ty) (p : P01D.Poly) : side_HasE_allElim (encode (Rule.HasE_allElim Γ B A p)) = (Rule.HasE_allElim Γ B A p).checkSide := by
  simp only [side_HasE_allElim,Rule.checkSide,encode_Rule_HasE_allElim,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasE_rawAtom (c : Nat) : Bool := true
theorem primrec_side_HasE_rawAtom : Primrec side_HasE_rawAtom := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_HasE_rawAtom,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasE_rawAtom_exact (Γ : P01AC.Tel) (t : OrthemologyV2.Term) : side_HasE_rawAtom (encode (Rule.HasE_rawAtom Γ t)) = (Rule.HasE_rawAtom Γ t).checkSide := by
  simp only [side_HasE_rawAtom,Rule.checkSide,encode_Rule_HasE_rawAtom,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasE_rawApp (c : Nat) : Bool := true
theorem primrec_side_HasE_rawApp : Primrec side_HasE_rawApp := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_HasE_rawApp,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasE_rawApp_exact (Γ : P01AC.Tel) (f : P01D.Poly) (a : P01D.Poly) : side_HasE_rawApp (encode (Rule.HasE_rawApp Γ f a)) = (Rule.HasE_rawApp Γ f a).checkSide := by
  simp only [side_HasE_rawApp,Rule.checkSide,encode_Rule_HasE_rawApp,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasE_piIntro (c : Nat) : Bool := ((checkScope ((telLengthCode (ruleField c 0))) ((abstractCode (ruleField c 3)))) && true)
theorem primrec_side_HasE_piIntro : Primrec side_HasE_piIntro := by
  have h := (Primrec.and.comp (primrec_checkScope.comp (primrec_telLengthCode.comp (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_abstractCode.comp (primrec_ruleField.comp Primrec.id (.const 3)))) (Primrec.const true))
  exact h.of_eq (by intro c; simp only [side_HasE_piIntro,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasE_piIntro_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (b : P01D.Poly) : side_HasE_piIntro (encode (Rule.HasE_piIntro Γ A B b)) = (Rule.HasE_piIntro Γ A B b).checkSide := by
  simp only [side_HasE_piIntro,Rule.checkSide,encode_Rule_HasE_piIntro,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasE_piElim (c : Nat) : Bool := true
theorem primrec_side_HasE_piElim : Primrec side_HasE_piElim := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_HasE_piElim,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasE_piElim_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (a : P01D.Poly) (f : P01D.Poly) : side_HasE_piElim (encode (Rule.HasE_piElim Γ A B a f)) = (Rule.HasE_piElim Γ A B a f).checkSide := by
  simp only [side_HasE_piElim,Rule.checkSide,encode_Rule_HasE_piElim,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasE_sigmaIntro (c : Nat) : Bool := true
theorem primrec_side_HasE_sigmaIntro : Primrec side_HasE_sigmaIntro := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_HasE_sigmaIntro,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasE_sigmaIntro_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (a : P01D.Poly) (b : P01D.Poly) : side_HasE_sigmaIntro (encode (Rule.HasE_sigmaIntro Γ A B a b)) = (Rule.HasE_sigmaIntro Γ A B a b).checkSide := by
  simp only [side_HasE_sigmaIntro,Rule.checkSide,encode_Rule_HasE_sigmaIntro,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasE_sigmaFst (c : Nat) : Bool := true
theorem primrec_side_HasE_sigmaFst : Primrec side_HasE_sigmaFst := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_HasE_sigmaFst,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasE_sigmaFst_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (z : P01D.Poly) : side_HasE_sigmaFst (encode (Rule.HasE_sigmaFst Γ A B z)) = (Rule.HasE_sigmaFst Γ A B z).checkSide := by
  simp only [side_HasE_sigmaFst,Rule.checkSide,encode_Rule_HasE_sigmaFst,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasE_sigmaSnd (c : Nat) : Bool := true
theorem primrec_side_HasE_sigmaSnd : Primrec side_HasE_sigmaSnd := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_HasE_sigmaSnd,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasE_sigmaSnd_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (z : P01D.Poly) : side_HasE_sigmaSnd (encode (Rule.HasE_sigmaSnd Γ A B z)) = (Rule.HasE_sigmaSnd Γ A B z).checkSide := by
  simp only [side_HasE_sigmaSnd,Rule.checkSide,encode_Rule_HasE_sigmaSnd,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasE_identityIntro (c : Nat) : Bool := ((checkPolyCode (ruleField c 4) (ruleField c 2) (ruleField c 3)) && true)
theorem primrec_side_HasE_identityIntro : Primrec side_HasE_identityIntro := by
  have h := (Primrec.and.comp (primrec_checkPolyCode.comp ((primrec_ruleField.comp Primrec.id (.const 4)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 3))))) (Primrec.const true))
  exact h.of_eq (by intro c; simp only [side_HasE_identityIntro,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasE_identityIntro_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (aux0 : AuxiliaryCertificates.PolyCert) : side_HasE_identityIntro (encode (Rule.HasE_identityIntro Γ A p q aux0)) = (Rule.HasE_identityIntro Γ A p q aux0).checkSide := by
  simp only [side_HasE_identityIntro,Rule.checkSide,encode_Rule_HasE_identityIntro,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasE_proofErase (c : Nat) : Bool := true
theorem primrec_side_HasE_proofErase : Primrec side_HasE_proofErase := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_HasE_proofErase,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasE_proofErase_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (x : P01D.Poly) (y : P01D.Poly) (p : P01D.Poly) : side_HasE_proofErase (encode (Rule.HasE_proofErase Γ A x y p)) = (Rule.HasE_proofErase Γ A x y p).checkSide := by
  simp only [side_HasE_proofErase,Rule.checkSide,encode_Rule_HasE_proofErase,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasE_j (c : Nat) : Bool := true
theorem primrec_side_HasE_j : Primrec side_HasE_j := by
  have h : Primrec (fun _ : Nat => true) := Primrec.const true
  exact h.of_eq (by intro c; simp only [side_HasE_j,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasE_j_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (x : P01D.Poly) (B : P01AC.Ty) (y : P01D.Poly) (e : P01D.Poly) (d : P01D.Poly) : side_HasE_j (encode (Rule.HasE_j Γ A x B y e d)) = (Rule.HasE_j Γ A x B y e d).checkSide := by
  simp only [side_HasE_j,Rule.checkSide,encode_Rule_HasE_j,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasE_conv (c : Nat) : Bool := ((checkPolyCode (ruleField c 4) (ruleField c 2) (ruleField c 3)) && ((checkScope ((telLengthCode (ruleField c 0))) (ruleField c 3)) && true))
theorem primrec_side_HasE_conv : Primrec side_HasE_conv := by
  have h := (Primrec.and.comp (primrec_checkPolyCode.comp ((primrec_ruleField.comp Primrec.id (.const 4)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 3))))) (Primrec.and.comp (primrec_checkScope.comp (primrec_telLengthCode.comp (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 3))) (Primrec.const true)))
  exact h.of_eq (by intro c; simp only [side_HasE_conv,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasE_conv_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (aux0 : AuxiliaryCertificates.PolyCert) : side_HasE_conv (encode (Rule.HasE_conv Γ A p q aux0)) = (Rule.HasE_conv Γ A p q aux0).checkSide := by
  simp only [side_HasE_conv,Rule.checkSide,encode_Rule_HasE_conv,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasE_piExt (c : Nat) : Bool := ((checkScope ((telLengthCode (ruleField c 0))) (ruleField c 3)) && ((checkScope ((telLengthCode (ruleField c 0))) (ruleField c 4)) && ((checkScope ((telLengthCode (ruleField c 0))) (ruleField c 5)) && ((checkTyScope ((telLengthCode (ruleField c 0))) (ruleField c 1)) && ((checkTyScope (((fun c => telLengthCode c + 1) (ruleField c 0))) (ruleField c 2)) && true)))))
theorem primrec_side_HasE_piExt : Primrec side_HasE_piExt := by
  have h := (Primrec.and.comp (primrec_checkScope.comp (primrec_telLengthCode.comp (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 3))) (Primrec.and.comp (primrec_checkScope.comp (primrec_telLengthCode.comp (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 4))) (Primrec.and.comp (primrec_checkScope.comp (primrec_telLengthCode.comp (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 5))) (Primrec.and.comp (primrec_checkTyScope.comp (primrec_telLengthCode.comp (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.and.comp (primrec_checkTyScope.comp ((Primrec.succ.comp primrec_telLengthCode).comp (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 2))) (Primrec.const true))))))
  exact h.of_eq (by intro c; simp only [side_HasE_piExt,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasE_piExt_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (h : P01D.Poly) : side_HasE_piExt (encode (Rule.HasE_piExt Γ A B p q h)) = (Rule.HasE_piExt Γ A B p q h).checkSide := by
  simp only [side_HasE_piExt,Rule.checkSide,encode_Rule_HasE_piExt,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def side_HasE_allExt (c : Nat) : Bool := ((checkScope ((telLengthCode (ruleField c 0))) (ruleField c 2)) && ((checkScope ((telLengthCode (ruleField c 0))) (ruleField c 3)) && ((checkScope ((telLengthCode (ruleField c 0))) (ruleField c 4)) && ((checkTyScope ((telLengthCode (ruleField c 0))) (ruleField c 1)) && true))))
theorem primrec_side_HasE_allExt : Primrec side_HasE_allExt := by
  have h := (Primrec.and.comp (primrec_checkScope.comp (primrec_telLengthCode.comp (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 2))) (Primrec.and.comp (primrec_checkScope.comp (primrec_telLengthCode.comp (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 3))) (Primrec.and.comp (primrec_checkScope.comp (primrec_telLengthCode.comp (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 4))) (Primrec.and.comp (primrec_checkTyScope.comp (primrec_telLengthCode.comp (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.const true)))))
  exact h.of_eq (by intro c; simp only [side_HasE_allExt,id,Nat.succ_eq_add_one])
@[simp] theorem side_HasE_allExt_exact (Γ : P01AC.Tel) (B : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (h : P01D.Poly) : side_HasE_allExt (encode (Rule.HasE_allExt Γ B p q h)) = (Rule.HasE_allExt Γ B p q h).checkSide := by
  simp only [side_HasE_allExt,Rule.checkSide,encode_Rule_HasE_allExt,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,
    checkLookupCode_exact,checkFiniteCode_exact,checkPolyCode_exact,finSupportCode_exact,
    telLengthCode_exact,abstractCode_exact,checkScope_exact,checkTyScope_exact,
    Bool.decide_and,Bool.decide_coe,decide_true]

def sideDispatch62 (c : Nat) : Bool := if tag c = 62 then side_HasE_allExt c else false
theorem primrec_sideDispatch62 : Primrec sideDispatch62 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 62)) primrec_side_HasE_allExt (.const false)

def sideDispatch61 (c : Nat) : Bool := if tag c = 61 then side_HasE_piExt c else sideDispatch62 c
theorem primrec_sideDispatch61 : Primrec sideDispatch61 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 61)) primrec_side_HasE_piExt primrec_sideDispatch62

def sideDispatch60 (c : Nat) : Bool := if tag c = 60 then side_HasE_conv c else sideDispatch61 c
theorem primrec_sideDispatch60 : Primrec sideDispatch60 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 60)) primrec_side_HasE_conv primrec_sideDispatch61

def sideDispatch59 (c : Nat) : Bool := if tag c = 59 then side_HasE_j c else sideDispatch60 c
theorem primrec_sideDispatch59 : Primrec sideDispatch59 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 59)) primrec_side_HasE_j primrec_sideDispatch60

def sideDispatch58 (c : Nat) : Bool := if tag c = 58 then side_HasE_proofErase c else sideDispatch59 c
theorem primrec_sideDispatch58 : Primrec sideDispatch58 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 58)) primrec_side_HasE_proofErase primrec_sideDispatch59

def sideDispatch57 (c : Nat) : Bool := if tag c = 57 then side_HasE_identityIntro c else sideDispatch58 c
theorem primrec_sideDispatch57 : Primrec sideDispatch57 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 57)) primrec_side_HasE_identityIntro primrec_sideDispatch58

def sideDispatch56 (c : Nat) : Bool := if tag c = 56 then side_HasE_sigmaSnd c else sideDispatch57 c
theorem primrec_sideDispatch56 : Primrec sideDispatch56 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 56)) primrec_side_HasE_sigmaSnd primrec_sideDispatch57

def sideDispatch55 (c : Nat) : Bool := if tag c = 55 then side_HasE_sigmaFst c else sideDispatch56 c
theorem primrec_sideDispatch55 : Primrec sideDispatch55 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 55)) primrec_side_HasE_sigmaFst primrec_sideDispatch56

def sideDispatch54 (c : Nat) : Bool := if tag c = 54 then side_HasE_sigmaIntro c else sideDispatch55 c
theorem primrec_sideDispatch54 : Primrec sideDispatch54 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 54)) primrec_side_HasE_sigmaIntro primrec_sideDispatch55

def sideDispatch53 (c : Nat) : Bool := if tag c = 53 then side_HasE_piElim c else sideDispatch54 c
theorem primrec_sideDispatch53 : Primrec sideDispatch53 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 53)) primrec_side_HasE_piElim primrec_sideDispatch54

def sideDispatch52 (c : Nat) : Bool := if tag c = 52 then side_HasE_piIntro c else sideDispatch53 c
theorem primrec_sideDispatch52 : Primrec sideDispatch52 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 52)) primrec_side_HasE_piIntro primrec_sideDispatch53

def sideDispatch51 (c : Nat) : Bool := if tag c = 51 then side_HasE_rawApp c else sideDispatch52 c
theorem primrec_sideDispatch51 : Primrec sideDispatch51 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 51)) primrec_side_HasE_rawApp primrec_sideDispatch52

def sideDispatch50 (c : Nat) : Bool := if tag c = 50 then side_HasE_rawAtom c else sideDispatch51 c
theorem primrec_sideDispatch50 : Primrec sideDispatch50 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 50)) primrec_side_HasE_rawAtom primrec_sideDispatch51

def sideDispatch49 (c : Nat) : Bool := if tag c = 49 then side_HasE_allElim c else sideDispatch50 c
theorem primrec_sideDispatch49 : Primrec sideDispatch49 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 49)) primrec_side_HasE_allElim primrec_sideDispatch50

def sideDispatch48 (c : Nat) : Bool := if tag c = 48 then side_HasE_allIntro c else sideDispatch49 c
theorem primrec_sideDispatch48 : Primrec sideDispatch48 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 48)) primrec_side_HasE_allIntro primrec_sideDispatch49

def sideDispatch47 (c : Nat) : Bool := if tag c = 47 then side_HasE_finite c else sideDispatch48 c
theorem primrec_sideDispatch47 : Primrec sideDispatch47 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 47)) primrec_side_HasE_finite primrec_sideDispatch48

def sideDispatch46 (c : Nat) : Bool := if tag c = 46 then side_HasE_s c else sideDispatch47 c
theorem primrec_sideDispatch46 : Primrec sideDispatch46 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 46)) primrec_side_HasE_s primrec_sideDispatch47

def sideDispatch45 (c : Nat) : Bool := if tag c = 45 then side_HasE_k c else sideDispatch46 c
theorem primrec_sideDispatch45 : Primrec sideDispatch45 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 45)) primrec_side_HasE_k primrec_sideDispatch46

def sideDispatch44 (c : Nat) : Bool := if tag c = 44 then side_HasE_i c else sideDispatch45 c
theorem primrec_sideDispatch44 : Primrec sideDispatch44 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 44)) primrec_side_HasE_i primrec_sideDispatch45

def sideDispatch43 (c : Nat) : Bool := if tag c = 43 then side_HasE_var c else sideDispatch44 c
theorem primrec_sideDispatch43 : Primrec sideDispatch43 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 43)) primrec_side_HasE_var primrec_sideDispatch44

def sideDispatch42 (c : Nat) : Bool := if tag c = 42 then side_FormE_identity c else sideDispatch43 c
theorem primrec_sideDispatch42 : Primrec sideDispatch42 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 42)) primrec_side_FormE_identity primrec_sideDispatch43

def sideDispatch41 (c : Nat) : Bool := if tag c = 41 then side_FormE_sigma c else sideDispatch42 c
theorem primrec_sideDispatch41 : Primrec sideDispatch41 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 41)) primrec_side_FormE_sigma primrec_sideDispatch42

def sideDispatch40 (c : Nat) : Bool := if tag c = 40 then side_FormE_pi c else sideDispatch41 c
theorem primrec_sideDispatch40 : Primrec sideDispatch40 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 40)) primrec_side_FormE_pi primrec_sideDispatch41

def sideDispatch39 (c : Nat) : Bool := if tag c = 39 then side_FormE_raw c else sideDispatch40 c
theorem primrec_sideDispatch39 : Primrec sideDispatch39 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 39)) primrec_side_FormE_raw primrec_sideDispatch40

def sideDispatch38 (c : Nat) : Bool := if tag c = 38 then side_FormE_all c else sideDispatch39 c
theorem primrec_sideDispatch38 : Primrec sideDispatch38 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 38)) primrec_side_FormE_all primrec_sideDispatch39

def sideDispatch37 (c : Nat) : Bool := if tag c = 37 then side_FormE_bottom c else sideDispatch38 c
theorem primrec_sideDispatch37 : Primrec sideDispatch37 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 37)) primrec_side_FormE_bottom primrec_sideDispatch38

def sideDispatch36 (c : Nat) : Bool := if tag c = 36 then side_FormE_param c else sideDispatch37 c
theorem primrec_sideDispatch36 : Primrec sideDispatch36 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 36)) primrec_side_FormE_param primrec_sideDispatch37

def sideDispatch35 (c : Nat) : Bool := if tag c = 35 then side_CtxE_ext c else sideDispatch36 c
theorem primrec_sideDispatch35 : Primrec sideDispatch35 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 35)) primrec_side_CtxE_ext primrec_sideDispatch36

def sideDispatch34 (c : Nat) : Bool := if tag c = 34 then side_CtxE_nil c else sideDispatch35 c
theorem primrec_sideDispatch34 : Primrec sideDispatch34 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 34)) primrec_side_CtxE_nil primrec_sideDispatch35

def sideDispatch33 (c : Nat) : Bool := if tag c = 33 then side_HasJ_natInduction c else sideDispatch34 c
theorem primrec_sideDispatch33 : Primrec sideDispatch33 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 33)) primrec_side_HasJ_natInduction primrec_sideDispatch34

def sideDispatch32 (c : Nat) : Bool := if tag c = 32 then side_HasJ_sigmaElim c else sideDispatch33 c
theorem primrec_sideDispatch32 : Primrec sideDispatch32 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 32)) primrec_side_HasJ_sigmaElim primrec_sideDispatch33

def sideDispatch31 (c : Nat) : Bool := if tag c = 31 then side_HasJ_allExt c else sideDispatch32 c
theorem primrec_sideDispatch31 : Primrec sideDispatch31 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 31)) primrec_side_HasJ_allExt primrec_sideDispatch32

def sideDispatch30 (c : Nat) : Bool := if tag c = 30 then side_HasJ_piExt c else sideDispatch31 c
theorem primrec_sideDispatch30 : Primrec sideDispatch30 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 30)) primrec_side_HasJ_piExt primrec_sideDispatch31

def sideDispatch29 (c : Nat) : Bool := if tag c = 29 then side_HasJ_conv c else sideDispatch30 c
theorem primrec_sideDispatch29 : Primrec sideDispatch29 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 29)) primrec_side_HasJ_conv primrec_sideDispatch30

def sideDispatch28 (c : Nat) : Bool := if tag c = 28 then side_HasJ_j c else sideDispatch29 c
theorem primrec_sideDispatch28 : Primrec sideDispatch28 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 28)) primrec_side_HasJ_j primrec_sideDispatch29

def sideDispatch27 (c : Nat) : Bool := if tag c = 27 then side_HasJ_proofErase c else sideDispatch28 c
theorem primrec_sideDispatch27 : Primrec sideDispatch27 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 27)) primrec_side_HasJ_proofErase primrec_sideDispatch28

def sideDispatch26 (c : Nat) : Bool := if tag c = 26 then side_HasJ_identityIntro c else sideDispatch27 c
theorem primrec_sideDispatch26 : Primrec sideDispatch26 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 26)) primrec_side_HasJ_identityIntro primrec_sideDispatch27

def sideDispatch25 (c : Nat) : Bool := if tag c = 25 then side_HasJ_sigmaSnd c else sideDispatch26 c
theorem primrec_sideDispatch25 : Primrec sideDispatch25 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 25)) primrec_side_HasJ_sigmaSnd primrec_sideDispatch26

def sideDispatch24 (c : Nat) : Bool := if tag c = 24 then side_HasJ_sigmaFst c else sideDispatch25 c
theorem primrec_sideDispatch24 : Primrec sideDispatch24 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 24)) primrec_side_HasJ_sigmaFst primrec_sideDispatch25

def sideDispatch23 (c : Nat) : Bool := if tag c = 23 then side_HasJ_sigmaIntro c else sideDispatch24 c
theorem primrec_sideDispatch23 : Primrec sideDispatch23 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 23)) primrec_side_HasJ_sigmaIntro primrec_sideDispatch24

def sideDispatch22 (c : Nat) : Bool := if tag c = 22 then side_HasJ_piElim c else sideDispatch23 c
theorem primrec_sideDispatch22 : Primrec sideDispatch22 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 22)) primrec_side_HasJ_piElim primrec_sideDispatch23

def sideDispatch21 (c : Nat) : Bool := if tag c = 21 then side_HasJ_piIntro c else sideDispatch22 c
theorem primrec_sideDispatch21 : Primrec sideDispatch21 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 21)) primrec_side_HasJ_piIntro primrec_sideDispatch22

def sideDispatch20 (c : Nat) : Bool := if tag c = 20 then side_HasJ_rawApp c else sideDispatch21 c
theorem primrec_sideDispatch20 : Primrec sideDispatch20 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 20)) primrec_side_HasJ_rawApp primrec_sideDispatch21

def sideDispatch19 (c : Nat) : Bool := if tag c = 19 then side_HasJ_rawAtom c else sideDispatch20 c
theorem primrec_sideDispatch19 : Primrec sideDispatch19 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 19)) primrec_side_HasJ_rawAtom primrec_sideDispatch20

def sideDispatch18 (c : Nat) : Bool := if tag c = 18 then side_HasJ_allElim c else sideDispatch19 c
theorem primrec_sideDispatch18 : Primrec sideDispatch18 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 18)) primrec_side_HasJ_allElim primrec_sideDispatch19

def sideDispatch17 (c : Nat) : Bool := if tag c = 17 then side_HasJ_allIntro c else sideDispatch18 c
theorem primrec_sideDispatch17 : Primrec sideDispatch17 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 17)) primrec_side_HasJ_allIntro primrec_sideDispatch18

def sideDispatch16 (c : Nat) : Bool := if tag c = 16 then side_HasJ_finite c else sideDispatch17 c
theorem primrec_sideDispatch16 : Primrec sideDispatch16 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 16)) primrec_side_HasJ_finite primrec_sideDispatch17

def sideDispatch15 (c : Nat) : Bool := if tag c = 15 then side_HasJ_s c else sideDispatch16 c
theorem primrec_sideDispatch15 : Primrec sideDispatch15 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 15)) primrec_side_HasJ_s primrec_sideDispatch16

def sideDispatch14 (c : Nat) : Bool := if tag c = 14 then side_HasJ_k c else sideDispatch15 c
theorem primrec_sideDispatch14 : Primrec sideDispatch14 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 14)) primrec_side_HasJ_k primrec_sideDispatch15

def sideDispatch13 (c : Nat) : Bool := if tag c = 13 then side_HasJ_i c else sideDispatch14 c
theorem primrec_sideDispatch13 : Primrec sideDispatch13 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 13)) primrec_side_HasJ_i primrec_sideDispatch14

def sideDispatch12 (c : Nat) : Bool := if tag c = 12 then side_HasJ_var c else sideDispatch13 c
theorem primrec_sideDispatch12 : Primrec sideDispatch12 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 12)) primrec_side_HasJ_var primrec_sideDispatch13

def sideDispatch11 (c : Nat) : Bool := if tag c = 11 then side_HasJ_hasBase c else sideDispatch12 c
theorem primrec_sideDispatch11 : Primrec sideDispatch11 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 11)) primrec_side_HasJ_hasBase primrec_sideDispatch12

def sideDispatch10 (c : Nat) : Bool := if tag c = 10 then side_FormJ_identity c else sideDispatch11 c
theorem primrec_sideDispatch10 : Primrec sideDispatch10 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 10)) primrec_side_FormJ_identity primrec_sideDispatch11

def sideDispatch9 (c : Nat) : Bool := if tag c = 9 then side_FormJ_sigma c else sideDispatch10 c
theorem primrec_sideDispatch9 : Primrec sideDispatch9 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 9)) primrec_side_FormJ_sigma primrec_sideDispatch10

def sideDispatch8 (c : Nat) : Bool := if tag c = 8 then side_FormJ_pi c else sideDispatch9 c
theorem primrec_sideDispatch8 : Primrec sideDispatch8 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 8)) primrec_side_FormJ_pi primrec_sideDispatch9

def sideDispatch7 (c : Nat) : Bool := if tag c = 7 then side_FormJ_raw c else sideDispatch8 c
theorem primrec_sideDispatch7 : Primrec sideDispatch7 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 7)) primrec_side_FormJ_raw primrec_sideDispatch8

def sideDispatch6 (c : Nat) : Bool := if tag c = 6 then side_FormJ_all c else sideDispatch7 c
theorem primrec_sideDispatch6 : Primrec sideDispatch6 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 6)) primrec_side_FormJ_all primrec_sideDispatch7

def sideDispatch5 (c : Nat) : Bool := if tag c = 5 then side_FormJ_bottom c else sideDispatch6 c
theorem primrec_sideDispatch5 : Primrec sideDispatch5 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 5)) primrec_side_FormJ_bottom primrec_sideDispatch6

def sideDispatch4 (c : Nat) : Bool := if tag c = 4 then side_FormJ_param c else sideDispatch5 c
theorem primrec_sideDispatch4 : Primrec sideDispatch4 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 4)) primrec_side_FormJ_param primrec_sideDispatch5

def sideDispatch3 (c : Nat) : Bool := if tag c = 3 then side_FormJ_formBase c else sideDispatch4 c
theorem primrec_sideDispatch3 : Primrec sideDispatch3 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 3)) primrec_side_FormJ_formBase primrec_sideDispatch4

def sideDispatch2 (c : Nat) : Bool := if tag c = 2 then side_CtxJ_ext c else sideDispatch3 c
theorem primrec_sideDispatch2 : Primrec sideDispatch2 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 2)) primrec_side_CtxJ_ext primrec_sideDispatch3

def sideDispatch1 (c : Nat) : Bool := if tag c = 1 then side_CtxJ_nil c else sideDispatch2 c
theorem primrec_sideDispatch1 : Primrec sideDispatch1 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 1)) primrec_side_CtxJ_nil primrec_sideDispatch2

def sideDispatch0 (c : Nat) : Bool := if tag c = 0 then side_CtxJ_ctxBase c else sideDispatch1 c
theorem primrec_sideDispatch0 : Primrec sideDispatch0 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 0)) primrec_side_CtxJ_ctxBase primrec_sideDispatch1

def checkSideCode := sideDispatch0
theorem primrec_checkSideCode : Primrec checkSideCode := primrec_sideDispatch0
@[simp] theorem checkSideCode_CtxJ_ctxBase (Γ : P01AC.Tel) : checkSideCode (encode (Rule.CtxJ_ctxBase Γ)) = side_CtxJ_ctxBase (encode (Rule.CtxJ_ctxBase Γ)) := by
  have ht : tag (encode (Rule.CtxJ_ctxBase Γ)) = 0 := by rw [encode_Rule_CtxJ_ctxBase]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_CtxJ_nil  : checkSideCode (encode (Rule.CtxJ_nil )) = side_CtxJ_nil (encode (Rule.CtxJ_nil )) := by
  have ht : tag (encode (Rule.CtxJ_nil )) = 1 := by rw [encode_Rule_CtxJ_nil]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_CtxJ_ext (Γ : P01AC.Tel) (A : P01AC.Ty) : checkSideCode (encode (Rule.CtxJ_ext Γ A)) = side_CtxJ_ext (encode (Rule.CtxJ_ext Γ A)) := by
  have ht : tag (encode (Rule.CtxJ_ext Γ A)) = 2 := by rw [encode_Rule_CtxJ_ext]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_FormJ_formBase (Γ : P01AC.Tel) (A : P01AC.Ty) : checkSideCode (encode (Rule.FormJ_formBase Γ A)) = side_FormJ_formBase (encode (Rule.FormJ_formBase Γ A)) := by
  have ht : tag (encode (Rule.FormJ_formBase Γ A)) = 3 := by rw [encode_Rule_FormJ_formBase]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_FormJ_param (Γ : P01AC.Tel) (n : Nat) : checkSideCode (encode (Rule.FormJ_param Γ n)) = side_FormJ_param (encode (Rule.FormJ_param Γ n)) := by
  have ht : tag (encode (Rule.FormJ_param Γ n)) = 4 := by rw [encode_Rule_FormJ_param]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_FormJ_bottom (Γ : P01AC.Tel) : checkSideCode (encode (Rule.FormJ_bottom Γ)) = side_FormJ_bottom (encode (Rule.FormJ_bottom Γ)) := by
  have ht : tag (encode (Rule.FormJ_bottom Γ)) = 5 := by rw [encode_Rule_FormJ_bottom]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_FormJ_all (Γ : P01AC.Tel) (B : P01AC.Ty) : checkSideCode (encode (Rule.FormJ_all Γ B)) = side_FormJ_all (encode (Rule.FormJ_all Γ B)) := by
  have ht : tag (encode (Rule.FormJ_all Γ B)) = 6 := by rw [encode_Rule_FormJ_all]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_FormJ_raw (Γ : P01AC.Tel) : checkSideCode (encode (Rule.FormJ_raw Γ)) = side_FormJ_raw (encode (Rule.FormJ_raw Γ)) := by
  have ht : tag (encode (Rule.FormJ_raw Γ)) = 7 := by rw [encode_Rule_FormJ_raw]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_FormJ_pi (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : checkSideCode (encode (Rule.FormJ_pi Γ A B)) = side_FormJ_pi (encode (Rule.FormJ_pi Γ A B)) := by
  have ht : tag (encode (Rule.FormJ_pi Γ A B)) = 8 := by rw [encode_Rule_FormJ_pi]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_FormJ_sigma (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : checkSideCode (encode (Rule.FormJ_sigma Γ A B)) = side_FormJ_sigma (encode (Rule.FormJ_sigma Γ A B)) := by
  have ht : tag (encode (Rule.FormJ_sigma Γ A B)) = 9 := by rw [encode_Rule_FormJ_sigma]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_FormJ_identity (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) : checkSideCode (encode (Rule.FormJ_identity Γ A p q)) = side_FormJ_identity (encode (Rule.FormJ_identity Γ A p q)) := by
  have ht : tag (encode (Rule.FormJ_identity Γ A p q)) = 10 := by rw [encode_Rule_FormJ_identity]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasJ_hasBase (Γ : P01AC.Tel) (p : P01D.Poly) (A : P01AC.Ty) : checkSideCode (encode (Rule.HasJ_hasBase Γ p A)) = side_HasJ_hasBase (encode (Rule.HasJ_hasBase Γ p A)) := by
  have ht : tag (encode (Rule.HasJ_hasBase Γ p A)) = 11 := by rw [encode_Rule_HasJ_hasBase]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasJ_var (Γ : P01AC.Tel) (A : P01AC.Ty) (n : Nat) (aux0 : AuxiliaryCertificates.LookupCert) : checkSideCode (encode (Rule.HasJ_var Γ A n aux0)) = side_HasJ_var (encode (Rule.HasJ_var Γ A n aux0)) := by
  have ht : tag (encode (Rule.HasJ_var Γ A n aux0)) = 12 := by rw [encode_Rule_HasJ_var]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasJ_i (Γ : P01AC.Tel) (A : P01AC.Ty) : checkSideCode (encode (Rule.HasJ_i Γ A)) = side_HasJ_i (encode (Rule.HasJ_i Γ A)) := by
  have ht : tag (encode (Rule.HasJ_i Γ A)) = 13 := by rw [encode_Rule_HasJ_i]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasJ_k (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : checkSideCode (encode (Rule.HasJ_k Γ A B)) = side_HasJ_k (encode (Rule.HasJ_k Γ A B)) := by
  have ht : tag (encode (Rule.HasJ_k Γ A B)) = 14 := by rw [encode_Rule_HasJ_k]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasJ_s (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (C : P01AC.Ty) : checkSideCode (encode (Rule.HasJ_s Γ A B C)) = side_HasJ_s (encode (Rule.HasJ_s Γ A B C)) := by
  have ht : tag (encode (Rule.HasJ_s Γ A B C)) = 15 := by rw [encode_Rule_HasJ_s]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasJ_finite (C : OrthemologyV2.TypeCode) (Γ : P01AC.Tel) (t : OrthemologyV2.Term) (τ : List P01AC.Ty) (aux0 : AuxiliaryCertificates.FiniteCert) : checkSideCode (encode (Rule.HasJ_finite C Γ t τ aux0)) = side_HasJ_finite (encode (Rule.HasJ_finite C Γ t τ aux0)) := by
  have ht : tag (encode (Rule.HasJ_finite C Γ t τ aux0)) = 16 := by rw [encode_Rule_HasJ_finite]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasJ_allIntro (Γ : P01AC.Tel) (B : P01AC.Ty) (p : P01D.Poly) : checkSideCode (encode (Rule.HasJ_allIntro Γ B p)) = side_HasJ_allIntro (encode (Rule.HasJ_allIntro Γ B p)) := by
  have ht : tag (encode (Rule.HasJ_allIntro Γ B p)) = 17 := by rw [encode_Rule_HasJ_allIntro]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasJ_allElim (Γ : P01AC.Tel) (B : P01AC.Ty) (A : P01AC.Ty) (p : P01D.Poly) : checkSideCode (encode (Rule.HasJ_allElim Γ B A p)) = side_HasJ_allElim (encode (Rule.HasJ_allElim Γ B A p)) := by
  have ht : tag (encode (Rule.HasJ_allElim Γ B A p)) = 18 := by rw [encode_Rule_HasJ_allElim]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasJ_rawAtom (Γ : P01AC.Tel) (t : OrthemologyV2.Term) : checkSideCode (encode (Rule.HasJ_rawAtom Γ t)) = side_HasJ_rawAtom (encode (Rule.HasJ_rawAtom Γ t)) := by
  have ht : tag (encode (Rule.HasJ_rawAtom Γ t)) = 19 := by rw [encode_Rule_HasJ_rawAtom]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasJ_rawApp (Γ : P01AC.Tel) (f : P01D.Poly) (a : P01D.Poly) : checkSideCode (encode (Rule.HasJ_rawApp Γ f a)) = side_HasJ_rawApp (encode (Rule.HasJ_rawApp Γ f a)) := by
  have ht : tag (encode (Rule.HasJ_rawApp Γ f a)) = 20 := by rw [encode_Rule_HasJ_rawApp]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasJ_piIntro (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (b : P01D.Poly) : checkSideCode (encode (Rule.HasJ_piIntro Γ A B b)) = side_HasJ_piIntro (encode (Rule.HasJ_piIntro Γ A B b)) := by
  have ht : tag (encode (Rule.HasJ_piIntro Γ A B b)) = 21 := by rw [encode_Rule_HasJ_piIntro]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasJ_piElim (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (a : P01D.Poly) (f : P01D.Poly) : checkSideCode (encode (Rule.HasJ_piElim Γ A B a f)) = side_HasJ_piElim (encode (Rule.HasJ_piElim Γ A B a f)) := by
  have ht : tag (encode (Rule.HasJ_piElim Γ A B a f)) = 22 := by rw [encode_Rule_HasJ_piElim]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasJ_sigmaIntro (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (a : P01D.Poly) (b : P01D.Poly) : checkSideCode (encode (Rule.HasJ_sigmaIntro Γ A B a b)) = side_HasJ_sigmaIntro (encode (Rule.HasJ_sigmaIntro Γ A B a b)) := by
  have ht : tag (encode (Rule.HasJ_sigmaIntro Γ A B a b)) = 23 := by rw [encode_Rule_HasJ_sigmaIntro]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasJ_sigmaFst (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (z : P01D.Poly) : checkSideCode (encode (Rule.HasJ_sigmaFst Γ A B z)) = side_HasJ_sigmaFst (encode (Rule.HasJ_sigmaFst Γ A B z)) := by
  have ht : tag (encode (Rule.HasJ_sigmaFst Γ A B z)) = 24 := by rw [encode_Rule_HasJ_sigmaFst]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasJ_sigmaSnd (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (z : P01D.Poly) : checkSideCode (encode (Rule.HasJ_sigmaSnd Γ A B z)) = side_HasJ_sigmaSnd (encode (Rule.HasJ_sigmaSnd Γ A B z)) := by
  have ht : tag (encode (Rule.HasJ_sigmaSnd Γ A B z)) = 25 := by rw [encode_Rule_HasJ_sigmaSnd]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasJ_identityIntro (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (aux0 : AuxiliaryCertificates.PolyCert) : checkSideCode (encode (Rule.HasJ_identityIntro Γ A p q aux0)) = side_HasJ_identityIntro (encode (Rule.HasJ_identityIntro Γ A p q aux0)) := by
  have ht : tag (encode (Rule.HasJ_identityIntro Γ A p q aux0)) = 26 := by rw [encode_Rule_HasJ_identityIntro]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasJ_proofErase (Γ : P01AC.Tel) (A : P01AC.Ty) (x : P01D.Poly) (y : P01D.Poly) (p : P01D.Poly) : checkSideCode (encode (Rule.HasJ_proofErase Γ A x y p)) = side_HasJ_proofErase (encode (Rule.HasJ_proofErase Γ A x y p)) := by
  have ht : tag (encode (Rule.HasJ_proofErase Γ A x y p)) = 27 := by rw [encode_Rule_HasJ_proofErase]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasJ_j (Γ : P01AC.Tel) (A : P01AC.Ty) (x : P01D.Poly) (B : P01AC.Ty) (y : P01D.Poly) (e : P01D.Poly) (d : P01D.Poly) : checkSideCode (encode (Rule.HasJ_j Γ A x B y e d)) = side_HasJ_j (encode (Rule.HasJ_j Γ A x B y e d)) := by
  have ht : tag (encode (Rule.HasJ_j Γ A x B y e d)) = 28 := by rw [encode_Rule_HasJ_j]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasJ_conv (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (aux0 : AuxiliaryCertificates.PolyCert) : checkSideCode (encode (Rule.HasJ_conv Γ A p q aux0)) = side_HasJ_conv (encode (Rule.HasJ_conv Γ A p q aux0)) := by
  have ht : tag (encode (Rule.HasJ_conv Γ A p q aux0)) = 29 := by rw [encode_Rule_HasJ_conv]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasJ_piExt (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (h : P01D.Poly) : checkSideCode (encode (Rule.HasJ_piExt Γ A B p q h)) = side_HasJ_piExt (encode (Rule.HasJ_piExt Γ A B p q h)) := by
  have ht : tag (encode (Rule.HasJ_piExt Γ A B p q h)) = 30 := by rw [encode_Rule_HasJ_piExt]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasJ_allExt (Γ : P01AC.Tel) (B : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (h : P01D.Poly) : checkSideCode (encode (Rule.HasJ_allExt Γ B p q h)) = side_HasJ_allExt (encode (Rule.HasJ_allExt Γ B p q h)) := by
  have ht : tag (encode (Rule.HasJ_allExt Γ B p q h)) = 31 := by rw [encode_Rule_HasJ_allExt]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasJ_sigmaElim (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (P : P01AC.Ty) (d : P01D.Poly) (z : P01D.Poly) : checkSideCode (encode (Rule.HasJ_sigmaElim Γ A B P d z)) = side_HasJ_sigmaElim (encode (Rule.HasJ_sigmaElim Γ A B P d z)) := by
  have ht : tag (encode (Rule.HasJ_sigmaElim Γ A B P d z)) = 32 := by rw [encode_Rule_HasJ_sigmaElim]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasJ_natInduction (Γ : P01AC.Tel) (P : P01AC.Ty) (p : P01D.Poly) (s : P01D.Poly) : checkSideCode (encode (Rule.HasJ_natInduction Γ P p s)) = side_HasJ_natInduction (encode (Rule.HasJ_natInduction Γ P p s)) := by
  have ht : tag (encode (Rule.HasJ_natInduction Γ P p s)) = 33 := by rw [encode_Rule_HasJ_natInduction]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, sideDispatch33, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_CtxE_nil  : checkSideCode (encode (Rule.CtxE_nil )) = side_CtxE_nil (encode (Rule.CtxE_nil )) := by
  have ht : tag (encode (Rule.CtxE_nil )) = 34 := by rw [encode_Rule_CtxE_nil]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, sideDispatch33, sideDispatch34, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_CtxE_ext (Γ : P01AC.Tel) (A : P01AC.Ty) : checkSideCode (encode (Rule.CtxE_ext Γ A)) = side_CtxE_ext (encode (Rule.CtxE_ext Γ A)) := by
  have ht : tag (encode (Rule.CtxE_ext Γ A)) = 35 := by rw [encode_Rule_CtxE_ext]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, sideDispatch33, sideDispatch34, sideDispatch35, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_FormE_param (Γ : P01AC.Tel) (n : Nat) : checkSideCode (encode (Rule.FormE_param Γ n)) = side_FormE_param (encode (Rule.FormE_param Γ n)) := by
  have ht : tag (encode (Rule.FormE_param Γ n)) = 36 := by rw [encode_Rule_FormE_param]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, sideDispatch33, sideDispatch34, sideDispatch35, sideDispatch36, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_FormE_bottom (Γ : P01AC.Tel) : checkSideCode (encode (Rule.FormE_bottom Γ)) = side_FormE_bottom (encode (Rule.FormE_bottom Γ)) := by
  have ht : tag (encode (Rule.FormE_bottom Γ)) = 37 := by rw [encode_Rule_FormE_bottom]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, sideDispatch33, sideDispatch34, sideDispatch35, sideDispatch36, sideDispatch37, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_FormE_all (Γ : P01AC.Tel) (B : P01AC.Ty) : checkSideCode (encode (Rule.FormE_all Γ B)) = side_FormE_all (encode (Rule.FormE_all Γ B)) := by
  have ht : tag (encode (Rule.FormE_all Γ B)) = 38 := by rw [encode_Rule_FormE_all]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, sideDispatch33, sideDispatch34, sideDispatch35, sideDispatch36, sideDispatch37, sideDispatch38, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_FormE_raw (Γ : P01AC.Tel) : checkSideCode (encode (Rule.FormE_raw Γ)) = side_FormE_raw (encode (Rule.FormE_raw Γ)) := by
  have ht : tag (encode (Rule.FormE_raw Γ)) = 39 := by rw [encode_Rule_FormE_raw]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, sideDispatch33, sideDispatch34, sideDispatch35, sideDispatch36, sideDispatch37, sideDispatch38, sideDispatch39, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_FormE_pi (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : checkSideCode (encode (Rule.FormE_pi Γ A B)) = side_FormE_pi (encode (Rule.FormE_pi Γ A B)) := by
  have ht : tag (encode (Rule.FormE_pi Γ A B)) = 40 := by rw [encode_Rule_FormE_pi]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, sideDispatch33, sideDispatch34, sideDispatch35, sideDispatch36, sideDispatch37, sideDispatch38, sideDispatch39, sideDispatch40, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_FormE_sigma (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : checkSideCode (encode (Rule.FormE_sigma Γ A B)) = side_FormE_sigma (encode (Rule.FormE_sigma Γ A B)) := by
  have ht : tag (encode (Rule.FormE_sigma Γ A B)) = 41 := by rw [encode_Rule_FormE_sigma]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, sideDispatch33, sideDispatch34, sideDispatch35, sideDispatch36, sideDispatch37, sideDispatch38, sideDispatch39, sideDispatch40, sideDispatch41, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_FormE_identity (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) : checkSideCode (encode (Rule.FormE_identity Γ A p q)) = side_FormE_identity (encode (Rule.FormE_identity Γ A p q)) := by
  have ht : tag (encode (Rule.FormE_identity Γ A p q)) = 42 := by rw [encode_Rule_FormE_identity]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, sideDispatch33, sideDispatch34, sideDispatch35, sideDispatch36, sideDispatch37, sideDispatch38, sideDispatch39, sideDispatch40, sideDispatch41, sideDispatch42, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasE_var (Γ : P01AC.Tel) (A : P01AC.Ty) (n : Nat) (aux0 : AuxiliaryCertificates.LookupCert) : checkSideCode (encode (Rule.HasE_var Γ A n aux0)) = side_HasE_var (encode (Rule.HasE_var Γ A n aux0)) := by
  have ht : tag (encode (Rule.HasE_var Γ A n aux0)) = 43 := by rw [encode_Rule_HasE_var]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, sideDispatch33, sideDispatch34, sideDispatch35, sideDispatch36, sideDispatch37, sideDispatch38, sideDispatch39, sideDispatch40, sideDispatch41, sideDispatch42, sideDispatch43, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasE_i (Γ : P01AC.Tel) (A : P01AC.Ty) : checkSideCode (encode (Rule.HasE_i Γ A)) = side_HasE_i (encode (Rule.HasE_i Γ A)) := by
  have ht : tag (encode (Rule.HasE_i Γ A)) = 44 := by rw [encode_Rule_HasE_i]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, sideDispatch33, sideDispatch34, sideDispatch35, sideDispatch36, sideDispatch37, sideDispatch38, sideDispatch39, sideDispatch40, sideDispatch41, sideDispatch42, sideDispatch43, sideDispatch44, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasE_k (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : checkSideCode (encode (Rule.HasE_k Γ A B)) = side_HasE_k (encode (Rule.HasE_k Γ A B)) := by
  have ht : tag (encode (Rule.HasE_k Γ A B)) = 45 := by rw [encode_Rule_HasE_k]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, sideDispatch33, sideDispatch34, sideDispatch35, sideDispatch36, sideDispatch37, sideDispatch38, sideDispatch39, sideDispatch40, sideDispatch41, sideDispatch42, sideDispatch43, sideDispatch44, sideDispatch45, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasE_s (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (C : P01AC.Ty) : checkSideCode (encode (Rule.HasE_s Γ A B C)) = side_HasE_s (encode (Rule.HasE_s Γ A B C)) := by
  have ht : tag (encode (Rule.HasE_s Γ A B C)) = 46 := by rw [encode_Rule_HasE_s]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, sideDispatch33, sideDispatch34, sideDispatch35, sideDispatch36, sideDispatch37, sideDispatch38, sideDispatch39, sideDispatch40, sideDispatch41, sideDispatch42, sideDispatch43, sideDispatch44, sideDispatch45, sideDispatch46, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasE_finite (C : OrthemologyV2.TypeCode) (Γ : P01AC.Tel) (t : OrthemologyV2.Term) (τ : List P01AC.Ty) (aux0 : AuxiliaryCertificates.FiniteCert) : checkSideCode (encode (Rule.HasE_finite C Γ t τ aux0)) = side_HasE_finite (encode (Rule.HasE_finite C Γ t τ aux0)) := by
  have ht : tag (encode (Rule.HasE_finite C Γ t τ aux0)) = 47 := by rw [encode_Rule_HasE_finite]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, sideDispatch33, sideDispatch34, sideDispatch35, sideDispatch36, sideDispatch37, sideDispatch38, sideDispatch39, sideDispatch40, sideDispatch41, sideDispatch42, sideDispatch43, sideDispatch44, sideDispatch45, sideDispatch46, sideDispatch47, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasE_allIntro (Γ : P01AC.Tel) (B : P01AC.Ty) (p : P01D.Poly) : checkSideCode (encode (Rule.HasE_allIntro Γ B p)) = side_HasE_allIntro (encode (Rule.HasE_allIntro Γ B p)) := by
  have ht : tag (encode (Rule.HasE_allIntro Γ B p)) = 48 := by rw [encode_Rule_HasE_allIntro]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, sideDispatch33, sideDispatch34, sideDispatch35, sideDispatch36, sideDispatch37, sideDispatch38, sideDispatch39, sideDispatch40, sideDispatch41, sideDispatch42, sideDispatch43, sideDispatch44, sideDispatch45, sideDispatch46, sideDispatch47, sideDispatch48, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasE_allElim (Γ : P01AC.Tel) (B : P01AC.Ty) (A : P01AC.Ty) (p : P01D.Poly) : checkSideCode (encode (Rule.HasE_allElim Γ B A p)) = side_HasE_allElim (encode (Rule.HasE_allElim Γ B A p)) := by
  have ht : tag (encode (Rule.HasE_allElim Γ B A p)) = 49 := by rw [encode_Rule_HasE_allElim]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, sideDispatch33, sideDispatch34, sideDispatch35, sideDispatch36, sideDispatch37, sideDispatch38, sideDispatch39, sideDispatch40, sideDispatch41, sideDispatch42, sideDispatch43, sideDispatch44, sideDispatch45, sideDispatch46, sideDispatch47, sideDispatch48, sideDispatch49, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasE_rawAtom (Γ : P01AC.Tel) (t : OrthemologyV2.Term) : checkSideCode (encode (Rule.HasE_rawAtom Γ t)) = side_HasE_rawAtom (encode (Rule.HasE_rawAtom Γ t)) := by
  have ht : tag (encode (Rule.HasE_rawAtom Γ t)) = 50 := by rw [encode_Rule_HasE_rawAtom]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, sideDispatch33, sideDispatch34, sideDispatch35, sideDispatch36, sideDispatch37, sideDispatch38, sideDispatch39, sideDispatch40, sideDispatch41, sideDispatch42, sideDispatch43, sideDispatch44, sideDispatch45, sideDispatch46, sideDispatch47, sideDispatch48, sideDispatch49, sideDispatch50, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasE_rawApp (Γ : P01AC.Tel) (f : P01D.Poly) (a : P01D.Poly) : checkSideCode (encode (Rule.HasE_rawApp Γ f a)) = side_HasE_rawApp (encode (Rule.HasE_rawApp Γ f a)) := by
  have ht : tag (encode (Rule.HasE_rawApp Γ f a)) = 51 := by rw [encode_Rule_HasE_rawApp]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, sideDispatch33, sideDispatch34, sideDispatch35, sideDispatch36, sideDispatch37, sideDispatch38, sideDispatch39, sideDispatch40, sideDispatch41, sideDispatch42, sideDispatch43, sideDispatch44, sideDispatch45, sideDispatch46, sideDispatch47, sideDispatch48, sideDispatch49, sideDispatch50, sideDispatch51, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasE_piIntro (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (b : P01D.Poly) : checkSideCode (encode (Rule.HasE_piIntro Γ A B b)) = side_HasE_piIntro (encode (Rule.HasE_piIntro Γ A B b)) := by
  have ht : tag (encode (Rule.HasE_piIntro Γ A B b)) = 52 := by rw [encode_Rule_HasE_piIntro]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, sideDispatch33, sideDispatch34, sideDispatch35, sideDispatch36, sideDispatch37, sideDispatch38, sideDispatch39, sideDispatch40, sideDispatch41, sideDispatch42, sideDispatch43, sideDispatch44, sideDispatch45, sideDispatch46, sideDispatch47, sideDispatch48, sideDispatch49, sideDispatch50, sideDispatch51, sideDispatch52, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasE_piElim (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (a : P01D.Poly) (f : P01D.Poly) : checkSideCode (encode (Rule.HasE_piElim Γ A B a f)) = side_HasE_piElim (encode (Rule.HasE_piElim Γ A B a f)) := by
  have ht : tag (encode (Rule.HasE_piElim Γ A B a f)) = 53 := by rw [encode_Rule_HasE_piElim]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, sideDispatch33, sideDispatch34, sideDispatch35, sideDispatch36, sideDispatch37, sideDispatch38, sideDispatch39, sideDispatch40, sideDispatch41, sideDispatch42, sideDispatch43, sideDispatch44, sideDispatch45, sideDispatch46, sideDispatch47, sideDispatch48, sideDispatch49, sideDispatch50, sideDispatch51, sideDispatch52, sideDispatch53, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasE_sigmaIntro (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (a : P01D.Poly) (b : P01D.Poly) : checkSideCode (encode (Rule.HasE_sigmaIntro Γ A B a b)) = side_HasE_sigmaIntro (encode (Rule.HasE_sigmaIntro Γ A B a b)) := by
  have ht : tag (encode (Rule.HasE_sigmaIntro Γ A B a b)) = 54 := by rw [encode_Rule_HasE_sigmaIntro]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, sideDispatch33, sideDispatch34, sideDispatch35, sideDispatch36, sideDispatch37, sideDispatch38, sideDispatch39, sideDispatch40, sideDispatch41, sideDispatch42, sideDispatch43, sideDispatch44, sideDispatch45, sideDispatch46, sideDispatch47, sideDispatch48, sideDispatch49, sideDispatch50, sideDispatch51, sideDispatch52, sideDispatch53, sideDispatch54, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasE_sigmaFst (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (z : P01D.Poly) : checkSideCode (encode (Rule.HasE_sigmaFst Γ A B z)) = side_HasE_sigmaFst (encode (Rule.HasE_sigmaFst Γ A B z)) := by
  have ht : tag (encode (Rule.HasE_sigmaFst Γ A B z)) = 55 := by rw [encode_Rule_HasE_sigmaFst]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, sideDispatch33, sideDispatch34, sideDispatch35, sideDispatch36, sideDispatch37, sideDispatch38, sideDispatch39, sideDispatch40, sideDispatch41, sideDispatch42, sideDispatch43, sideDispatch44, sideDispatch45, sideDispatch46, sideDispatch47, sideDispatch48, sideDispatch49, sideDispatch50, sideDispatch51, sideDispatch52, sideDispatch53, sideDispatch54, sideDispatch55, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasE_sigmaSnd (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (z : P01D.Poly) : checkSideCode (encode (Rule.HasE_sigmaSnd Γ A B z)) = side_HasE_sigmaSnd (encode (Rule.HasE_sigmaSnd Γ A B z)) := by
  have ht : tag (encode (Rule.HasE_sigmaSnd Γ A B z)) = 56 := by rw [encode_Rule_HasE_sigmaSnd]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, sideDispatch33, sideDispatch34, sideDispatch35, sideDispatch36, sideDispatch37, sideDispatch38, sideDispatch39, sideDispatch40, sideDispatch41, sideDispatch42, sideDispatch43, sideDispatch44, sideDispatch45, sideDispatch46, sideDispatch47, sideDispatch48, sideDispatch49, sideDispatch50, sideDispatch51, sideDispatch52, sideDispatch53, sideDispatch54, sideDispatch55, sideDispatch56, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasE_identityIntro (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (aux0 : AuxiliaryCertificates.PolyCert) : checkSideCode (encode (Rule.HasE_identityIntro Γ A p q aux0)) = side_HasE_identityIntro (encode (Rule.HasE_identityIntro Γ A p q aux0)) := by
  have ht : tag (encode (Rule.HasE_identityIntro Γ A p q aux0)) = 57 := by rw [encode_Rule_HasE_identityIntro]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, sideDispatch33, sideDispatch34, sideDispatch35, sideDispatch36, sideDispatch37, sideDispatch38, sideDispatch39, sideDispatch40, sideDispatch41, sideDispatch42, sideDispatch43, sideDispatch44, sideDispatch45, sideDispatch46, sideDispatch47, sideDispatch48, sideDispatch49, sideDispatch50, sideDispatch51, sideDispatch52, sideDispatch53, sideDispatch54, sideDispatch55, sideDispatch56, sideDispatch57, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasE_proofErase (Γ : P01AC.Tel) (A : P01AC.Ty) (x : P01D.Poly) (y : P01D.Poly) (p : P01D.Poly) : checkSideCode (encode (Rule.HasE_proofErase Γ A x y p)) = side_HasE_proofErase (encode (Rule.HasE_proofErase Γ A x y p)) := by
  have ht : tag (encode (Rule.HasE_proofErase Γ A x y p)) = 58 := by rw [encode_Rule_HasE_proofErase]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, sideDispatch33, sideDispatch34, sideDispatch35, sideDispatch36, sideDispatch37, sideDispatch38, sideDispatch39, sideDispatch40, sideDispatch41, sideDispatch42, sideDispatch43, sideDispatch44, sideDispatch45, sideDispatch46, sideDispatch47, sideDispatch48, sideDispatch49, sideDispatch50, sideDispatch51, sideDispatch52, sideDispatch53, sideDispatch54, sideDispatch55, sideDispatch56, sideDispatch57, sideDispatch58, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasE_j (Γ : P01AC.Tel) (A : P01AC.Ty) (x : P01D.Poly) (B : P01AC.Ty) (y : P01D.Poly) (e : P01D.Poly) (d : P01D.Poly) : checkSideCode (encode (Rule.HasE_j Γ A x B y e d)) = side_HasE_j (encode (Rule.HasE_j Γ A x B y e d)) := by
  have ht : tag (encode (Rule.HasE_j Γ A x B y e d)) = 59 := by rw [encode_Rule_HasE_j]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, sideDispatch33, sideDispatch34, sideDispatch35, sideDispatch36, sideDispatch37, sideDispatch38, sideDispatch39, sideDispatch40, sideDispatch41, sideDispatch42, sideDispatch43, sideDispatch44, sideDispatch45, sideDispatch46, sideDispatch47, sideDispatch48, sideDispatch49, sideDispatch50, sideDispatch51, sideDispatch52, sideDispatch53, sideDispatch54, sideDispatch55, sideDispatch56, sideDispatch57, sideDispatch58, sideDispatch59, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasE_conv (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (aux0 : AuxiliaryCertificates.PolyCert) : checkSideCode (encode (Rule.HasE_conv Γ A p q aux0)) = side_HasE_conv (encode (Rule.HasE_conv Γ A p q aux0)) := by
  have ht : tag (encode (Rule.HasE_conv Γ A p q aux0)) = 60 := by rw [encode_Rule_HasE_conv]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, sideDispatch33, sideDispatch34, sideDispatch35, sideDispatch36, sideDispatch37, sideDispatch38, sideDispatch39, sideDispatch40, sideDispatch41, sideDispatch42, sideDispatch43, sideDispatch44, sideDispatch45, sideDispatch46, sideDispatch47, sideDispatch48, sideDispatch49, sideDispatch50, sideDispatch51, sideDispatch52, sideDispatch53, sideDispatch54, sideDispatch55, sideDispatch56, sideDispatch57, sideDispatch58, sideDispatch59, sideDispatch60, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasE_piExt (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (h : P01D.Poly) : checkSideCode (encode (Rule.HasE_piExt Γ A B p q h)) = side_HasE_piExt (encode (Rule.HasE_piExt Γ A B p q h)) := by
  have ht : tag (encode (Rule.HasE_piExt Γ A B p q h)) = 61 := by rw [encode_Rule_HasE_piExt]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, sideDispatch33, sideDispatch34, sideDispatch35, sideDispatch36, sideDispatch37, sideDispatch38, sideDispatch39, sideDispatch40, sideDispatch41, sideDispatch42, sideDispatch43, sideDispatch44, sideDispatch45, sideDispatch46, sideDispatch47, sideDispatch48, sideDispatch49, sideDispatch50, sideDispatch51, sideDispatch52, sideDispatch53, sideDispatch54, sideDispatch55, sideDispatch56, sideDispatch57, sideDispatch58, sideDispatch59, sideDispatch60, sideDispatch61, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem checkSideCode_HasE_allExt (Γ : P01AC.Tel) (B : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (h : P01D.Poly) : checkSideCode (encode (Rule.HasE_allExt Γ B p q h)) = side_HasE_allExt (encode (Rule.HasE_allExt Γ B p q h)) := by
  have ht : tag (encode (Rule.HasE_allExt Γ B p q h)) = 62 := by rw [encode_Rule_HasE_allExt]; exact tag_pack _ _
  simp only [checkSideCode,sideDispatch0, sideDispatch1, sideDispatch2, sideDispatch3, sideDispatch4, sideDispatch5, sideDispatch6, sideDispatch7, sideDispatch8, sideDispatch9, sideDispatch10, sideDispatch11, sideDispatch12, sideDispatch13, sideDispatch14, sideDispatch15, sideDispatch16, sideDispatch17, sideDispatch18, sideDispatch19, sideDispatch20, sideDispatch21, sideDispatch22, sideDispatch23, sideDispatch24, sideDispatch25, sideDispatch26, sideDispatch27, sideDispatch28, sideDispatch29, sideDispatch30, sideDispatch31, sideDispatch32, sideDispatch33, sideDispatch34, sideDispatch35, sideDispatch36, sideDispatch37, sideDispatch38, sideDispatch39, sideDispatch40, sideDispatch41, sideDispatch42, sideDispatch43, sideDispatch44, sideDispatch45, sideDispatch46, sideDispatch47, sideDispatch48, sideDispatch49, sideDispatch50, sideDispatch51, sideDispatch52, sideDispatch53, sideDispatch54, sideDispatch55, sideDispatch56, sideDispatch57, sideDispatch58, sideDispatch59, sideDispatch60, sideDispatch61, sideDispatch62, ht, Nat.reduceEqDiff, ↓reduceIte]

theorem checkSideCode_exact (r : Rule) : checkSideCode (encode r) = r.checkSide := by
  cases r <;> simp only [checkSideCode_CtxJ_ctxBase, checkSideCode_CtxJ_nil, checkSideCode_CtxJ_ext, checkSideCode_FormJ_formBase, checkSideCode_FormJ_param, checkSideCode_FormJ_bottom, checkSideCode_FormJ_all, checkSideCode_FormJ_raw, checkSideCode_FormJ_pi, checkSideCode_FormJ_sigma, checkSideCode_FormJ_identity, checkSideCode_HasJ_hasBase, checkSideCode_HasJ_var, checkSideCode_HasJ_i, checkSideCode_HasJ_k, checkSideCode_HasJ_s, checkSideCode_HasJ_finite, checkSideCode_HasJ_allIntro, checkSideCode_HasJ_allElim, checkSideCode_HasJ_rawAtom, checkSideCode_HasJ_rawApp, checkSideCode_HasJ_piIntro, checkSideCode_HasJ_piElim, checkSideCode_HasJ_sigmaIntro, checkSideCode_HasJ_sigmaFst, checkSideCode_HasJ_sigmaSnd, checkSideCode_HasJ_identityIntro, checkSideCode_HasJ_proofErase, checkSideCode_HasJ_j, checkSideCode_HasJ_conv, checkSideCode_HasJ_piExt, checkSideCode_HasJ_allExt, checkSideCode_HasJ_sigmaElim, checkSideCode_HasJ_natInduction, checkSideCode_CtxE_nil, checkSideCode_CtxE_ext, checkSideCode_FormE_param, checkSideCode_FormE_bottom, checkSideCode_FormE_all, checkSideCode_FormE_raw, checkSideCode_FormE_pi, checkSideCode_FormE_sigma, checkSideCode_FormE_identity, checkSideCode_HasE_var, checkSideCode_HasE_i, checkSideCode_HasE_k, checkSideCode_HasE_s, checkSideCode_HasE_finite, checkSideCode_HasE_allIntro, checkSideCode_HasE_allElim, checkSideCode_HasE_rawAtom, checkSideCode_HasE_rawApp, checkSideCode_HasE_piIntro, checkSideCode_HasE_piElim, checkSideCode_HasE_sigmaIntro, checkSideCode_HasE_sigmaFst, checkSideCode_HasE_sigmaSnd, checkSideCode_HasE_identityIntro, checkSideCode_HasE_proofErase, checkSideCode_HasE_j, checkSideCode_HasE_conv, checkSideCode_HasE_piExt, checkSideCode_HasE_allExt, side_CtxJ_ctxBase_exact, side_CtxJ_nil_exact, side_CtxJ_ext_exact, side_FormJ_formBase_exact, side_FormJ_param_exact, side_FormJ_bottom_exact, side_FormJ_all_exact, side_FormJ_raw_exact, side_FormJ_pi_exact, side_FormJ_sigma_exact, side_FormJ_identity_exact, side_HasJ_hasBase_exact, side_HasJ_var_exact, side_HasJ_i_exact, side_HasJ_k_exact, side_HasJ_s_exact, side_HasJ_finite_exact, side_HasJ_allIntro_exact, side_HasJ_allElim_exact, side_HasJ_rawAtom_exact, side_HasJ_rawApp_exact, side_HasJ_piIntro_exact, side_HasJ_piElim_exact, side_HasJ_sigmaIntro_exact, side_HasJ_sigmaFst_exact, side_HasJ_sigmaSnd_exact, side_HasJ_identityIntro_exact, side_HasJ_proofErase_exact, side_HasJ_j_exact, side_HasJ_conv_exact, side_HasJ_piExt_exact, side_HasJ_allExt_exact, side_HasJ_sigmaElim_exact, side_HasJ_natInduction_exact, side_CtxE_nil_exact, side_CtxE_ext_exact, side_FormE_param_exact, side_FormE_bottom_exact, side_FormE_all_exact, side_FormE_raw_exact, side_FormE_pi_exact, side_FormE_sigma_exact, side_FormE_identity_exact, side_HasE_var_exact, side_HasE_i_exact, side_HasE_k_exact, side_HasE_s_exact, side_HasE_finite_exact, side_HasE_allIntro_exact, side_HasE_allElim_exact, side_HasE_rawAtom_exact, side_HasE_rawApp_exact, side_HasE_piIntro_exact, side_HasE_piElim_exact, side_HasE_sigmaIntro_exact, side_HasE_sigmaFst_exact, side_HasE_sigmaSnd_exact, side_HasE_identityIntro_exact, side_HasE_proofErase_exact, side_HasE_j_exact, side_HasE_conv_exact, side_HasE_piExt_exact, side_HasE_allExt_exact]

#print axioms primrec_checkSideCode
#print axioms checkSideCode_exact
end CodedRuleTemplates
