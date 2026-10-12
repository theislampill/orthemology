import RuleCodeBasics
namespace CodedRuleTemplates
open P01D P01AC Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity CodedPolyTransformations CodedMixedTransformations
open AuxiliaryCodeComputability CertificateCodeValidity TelescopeCodeValidity JointCertificates
set_option maxRecDepth 32768
set_option maxHeartbeats 12000000
set_option linter.unusedVariables false
attribute [local irreducible] Nat.pair


def premises_CtxJ_ctxBase (c : Nat) : List Nat := [(ctxCode 3 (ruleField c 0))]
theorem primrec_premises_CtxJ_ctxBase : Primrec premises_CtxJ_ctxBase := by
  have h := (Primrec.list_cons.comp ((primrec_ctxCode 3).comp (primrec_ruleField.comp Primrec.id (.const 0))) (Primrec.const ([] : List Nat)))
  exact h.of_eq (by intro c; simp only [premises_CtxJ_ctxBase,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_CtxJ_ctxBase_exact (Γ : P01AC.Tel) : premises_CtxJ_ctxBase (encode (Rule.CtxJ_ctxBase Γ)) = ((Rule.CtxJ_ctxBase Γ).premises).map encode := by
  simp only [premises_CtxJ_ctxBase,Rule.premises,encode_Rule_CtxJ_ctxBase,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_CtxJ_nil (c : Nat) : List Nat := []
theorem primrec_premises_CtxJ_nil : Primrec premises_CtxJ_nil := by
  have h : Primrec (fun _ : Nat => ([] : List Nat)) := Primrec.const _
  exact h.of_eq (by intro c; simp only [premises_CtxJ_nil,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_CtxJ_nil_exact  : premises_CtxJ_nil (encode (Rule.CtxJ_nil )) = ((Rule.CtxJ_nil ).premises).map encode := by
  simp only [premises_CtxJ_nil,Rule.premises,encode_Rule_CtxJ_nil,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_CtxJ_ext (c : Nat) : List Nat := [(ctxCode 0 (ruleField c 0)), (formCode 1 (ruleField c 0) (ruleField c 1))]
theorem primrec_premises_CtxJ_ext : Primrec premises_CtxJ_ext := by
  have h := (Primrec.list_cons.comp ((primrec_ctxCode 0).comp (primrec_ruleField.comp Primrec.id (.const 0))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.const ([] : List Nat))))
  exact h.of_eq (by intro c; simp only [premises_CtxJ_ext,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_CtxJ_ext_exact (Γ : P01AC.Tel) (A : P01AC.Ty) : premises_CtxJ_ext (encode (Rule.CtxJ_ext Γ A)) = ((Rule.CtxJ_ext Γ A).premises).map encode := by
  simp only [premises_CtxJ_ext,Rule.premises,encode_Rule_CtxJ_ext,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_FormJ_formBase (c : Nat) : List Nat := [(formCode 4 (ruleField c 0) (ruleField c 1))]
theorem primrec_premises_FormJ_formBase : Primrec premises_FormJ_formBase := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.const ([] : List Nat)))
  exact h.of_eq (by intro c; simp only [premises_FormJ_formBase,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_FormJ_formBase_exact (Γ : P01AC.Tel) (A : P01AC.Ty) : premises_FormJ_formBase (encode (Rule.FormJ_formBase Γ A)) = ((Rule.FormJ_formBase Γ A).premises).map encode := by
  simp only [premises_FormJ_formBase,Rule.premises,encode_Rule_FormJ_formBase,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_FormJ_param (c : Nat) : List Nat := [(ctxCode 0 (ruleField c 0))]
theorem primrec_premises_FormJ_param : Primrec premises_FormJ_param := by
  have h := (Primrec.list_cons.comp ((primrec_ctxCode 0).comp (primrec_ruleField.comp Primrec.id (.const 0))) (Primrec.const ([] : List Nat)))
  exact h.of_eq (by intro c; simp only [premises_FormJ_param,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_FormJ_param_exact (Γ : P01AC.Tel) (n : Nat) : premises_FormJ_param (encode (Rule.FormJ_param Γ n)) = ((Rule.FormJ_param Γ n).premises).map encode := by
  simp only [premises_FormJ_param,Rule.premises,encode_Rule_FormJ_param,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_FormJ_bottom (c : Nat) : List Nat := [(ctxCode 0 (ruleField c 0))]
theorem primrec_premises_FormJ_bottom : Primrec premises_FormJ_bottom := by
  have h := (Primrec.list_cons.comp ((primrec_ctxCode 0).comp (primrec_ruleField.comp Primrec.id (.const 0))) (Primrec.const ([] : List Nat)))
  exact h.of_eq (by intro c; simp only [premises_FormJ_bottom,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_FormJ_bottom_exact (Γ : P01AC.Tel) : premises_FormJ_bottom (encode (Rule.FormJ_bottom Γ)) = ((Rule.FormJ_bottom Γ).premises).map encode := by
  simp only [premises_FormJ_bottom,Rule.premises,encode_Rule_FormJ_bottom,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_FormJ_all (c : Nat) : List Nat := [(ctxCode 0 (ruleField c 0)), (formCode 1 ((twkTelCode (ruleField c 0))) (ruleField c 1))]
theorem primrec_premises_FormJ_all : Primrec premises_FormJ_all := by
  have h := (Primrec.list_cons.comp ((primrec_ctxCode 0).comp (primrec_ruleField.comp Primrec.id (.const 0))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_twkTelCode.comp (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.const ([] : List Nat))))
  exact h.of_eq (by intro c; simp only [premises_FormJ_all,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_FormJ_all_exact (Γ : P01AC.Tel) (B : P01AC.Ty) : premises_FormJ_all (encode (Rule.FormJ_all Γ B)) = ((Rule.FormJ_all Γ B).premises).map encode := by
  simp only [premises_FormJ_all,Rule.premises,encode_Rule_FormJ_all,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_FormJ_raw (c : Nat) : List Nat := [(ctxCode 0 (ruleField c 0))]
theorem primrec_premises_FormJ_raw : Primrec premises_FormJ_raw := by
  have h := (Primrec.list_cons.comp ((primrec_ctxCode 0).comp (primrec_ruleField.comp Primrec.id (.const 0))) (Primrec.const ([] : List Nat)))
  exact h.of_eq (by intro c; simp only [premises_FormJ_raw,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_FormJ_raw_exact (Γ : P01AC.Tel) : premises_FormJ_raw (encode (Rule.FormJ_raw Γ)) = ((Rule.FormJ_raw Γ).premises).map encode := by
  simp only [premises_FormJ_raw,Rule.premises,encode_Rule_FormJ_raw,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_FormJ_pi (c : Nat) : List Nat := [(formCode 1 (ruleField c 0) (ruleField c 1)), (formCode 1 ((telConsCode (ruleField c 1) (ruleField c 0))) (ruleField c 2))]
theorem primrec_premises_FormJ_pi : Primrec premises_FormJ_pi := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_telConsCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 2))) (Primrec.const ([] : List Nat))))
  exact h.of_eq (by intro c; simp only [premises_FormJ_pi,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_FormJ_pi_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : premises_FormJ_pi (encode (Rule.FormJ_pi Γ A B)) = ((Rule.FormJ_pi Γ A B).premises).map encode := by
  simp only [premises_FormJ_pi,Rule.premises,encode_Rule_FormJ_pi,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_FormJ_sigma (c : Nat) : List Nat := [(formCode 1 (ruleField c 0) (ruleField c 1)), (formCode 1 ((telConsCode (ruleField c 1) (ruleField c 0))) (ruleField c 2))]
theorem primrec_premises_FormJ_sigma : Primrec premises_FormJ_sigma := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_telConsCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 2))) (Primrec.const ([] : List Nat))))
  exact h.of_eq (by intro c; simp only [premises_FormJ_sigma,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_FormJ_sigma_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : premises_FormJ_sigma (encode (Rule.FormJ_sigma Γ A B)) = ((Rule.FormJ_sigma Γ A B).premises).map encode := by
  simp only [premises_FormJ_sigma,Rule.premises,encode_Rule_FormJ_sigma,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_FormJ_identity (c : Nat) : List Nat := [(formCode 1 (ruleField c 0) (ruleField c 1)), (hasCode 2 (ruleField c 0) (ruleField c 2) (ruleField c 1)), (hasCode 2 (ruleField c 0) (ruleField c 3) (ruleField c 1))]
theorem primrec_premises_FormJ_identity : Primrec premises_FormJ_identity := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 1))))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 3)).pair (primrec_ruleField.comp Primrec.id (.const 1))))) (Primrec.const ([] : List Nat)))))
  exact h.of_eq (by intro c; simp only [premises_FormJ_identity,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_FormJ_identity_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) : premises_FormJ_identity (encode (Rule.FormJ_identity Γ A p q)) = ((Rule.FormJ_identity Γ A p q).premises).map encode := by
  simp only [premises_FormJ_identity,Rule.premises,encode_Rule_FormJ_identity,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasJ_hasBase (c : Nat) : List Nat := [(hasCode 5 (ruleField c 0) (ruleField c 1) (ruleField c 2))]
theorem primrec_premises_HasJ_hasBase : Primrec premises_HasJ_hasBase := by
  have h := (Primrec.list_cons.comp ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 1)).pair (primrec_ruleField.comp Primrec.id (.const 2))))) (Primrec.const ([] : List Nat)))
  exact h.of_eq (by intro c; simp only [premises_HasJ_hasBase,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasJ_hasBase_exact (Γ : P01AC.Tel) (p : P01D.Poly) (A : P01AC.Ty) : premises_HasJ_hasBase (encode (Rule.HasJ_hasBase Γ p A)) = ((Rule.HasJ_hasBase Γ p A).premises).map encode := by
  simp only [premises_HasJ_hasBase,Rule.premises,encode_Rule_HasJ_hasBase,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasJ_var (c : Nat) : List Nat := [(formCode 1 (ruleField c 0) (ruleField c 1))]
theorem primrec_premises_HasJ_var : Primrec premises_HasJ_var := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.const ([] : List Nat)))
  exact h.of_eq (by intro c; simp only [premises_HasJ_var,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasJ_var_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (n : Nat) (aux0 : AuxiliaryCertificates.LookupCert) : premises_HasJ_var (encode (Rule.HasJ_var Γ A n aux0)) = ((Rule.HasJ_var Γ A n aux0).premises).map encode := by
  simp only [premises_HasJ_var,Rule.premises,encode_Rule_HasJ_var,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasJ_i (c : Nat) : List Nat := [(formCode 1 (ruleField c 0) (ruleField c 1)), (formCode 1 (ruleField c 0) ((arrCode (ruleField c 1) (ruleField c 1))))]
theorem primrec_premises_HasJ_i : Primrec premises_HasJ_i := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_arrCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 1)))) (Primrec.const ([] : List Nat))))
  exact h.of_eq (by intro c; simp only [premises_HasJ_i,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasJ_i_exact (Γ : P01AC.Tel) (A : P01AC.Ty) : premises_HasJ_i (encode (Rule.HasJ_i Γ A)) = ((Rule.HasJ_i Γ A).premises).map encode := by
  simp only [premises_HasJ_i,Rule.premises,encode_Rule_HasJ_i,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasJ_k (c : Nat) : List Nat := [(formCode 1 (ruleField c 0) (ruleField c 1)), (formCode 1 (ruleField c 0) (ruleField c 2)), (formCode 1 (ruleField c 0) ((arrCode (ruleField c 1) ((arrCode (ruleField c 2) (ruleField c 1))))))]
theorem primrec_premises_HasJ_k : Primrec premises_HasJ_k := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 2))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_arrCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_arrCode.comp (primrec_ruleField.comp Primrec.id (.const 2)) (primrec_ruleField.comp Primrec.id (.const 1))))) (Primrec.const ([] : List Nat)))))
  exact h.of_eq (by intro c; simp only [premises_HasJ_k,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasJ_k_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : premises_HasJ_k (encode (Rule.HasJ_k Γ A B)) = ((Rule.HasJ_k Γ A B).premises).map encode := by
  simp only [premises_HasJ_k,Rule.premises,encode_Rule_HasJ_k,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasJ_s (c : Nat) : List Nat := [(formCode 1 (ruleField c 0) (ruleField c 1)), (formCode 1 (ruleField c 0) (ruleField c 2)), (formCode 1 (ruleField c 0) (ruleField c 3)), (formCode 1 (ruleField c 0) ((arrCode ((arrCode (ruleField c 1) ((arrCode (ruleField c 2) (ruleField c 3))))) ((arrCode ((arrCode (ruleField c 1) (ruleField c 2))) ((arrCode (ruleField c 1) (ruleField c 3))))))))]
theorem primrec_premises_HasJ_s : Primrec premises_HasJ_s := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 2))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 3))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_arrCode.comp (primrec_arrCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_arrCode.comp (primrec_ruleField.comp Primrec.id (.const 2)) (primrec_ruleField.comp Primrec.id (.const 3)))) (primrec_arrCode.comp (primrec_arrCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2))) (primrec_arrCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 3)))))) (Primrec.const ([] : List Nat))))))
  exact h.of_eq (by intro c; simp only [premises_HasJ_s,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasJ_s_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (C : P01AC.Ty) : premises_HasJ_s (encode (Rule.HasJ_s Γ A B C)) = ((Rule.HasJ_s Γ A B C).premises).map encode := by
  simp only [premises_HasJ_s,Rule.premises,encode_Rule_HasJ_s,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasJ_finite (c : Nat) : List Nat := (List.append ((formImagesCode 1 (ruleField c 1) (ruleField c 3))) ([(formCode 1 (ruleField c 1) ((tsubstTelCode (ruleField c 3) ((finCode (ruleField c 0))))))]))
theorem primrec_premises_HasJ_finite : Primrec premises_HasJ_finite := by
  have h := (Primrec.list_append.comp ((primrec_formImagesCode 1).comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 3))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_tsubstTelCode.comp (primrec_ruleField.comp Primrec.id (.const 3)) (primrec_finCode.comp (primrec_ruleField.comp Primrec.id (.const 0))))) (Primrec.const ([] : List Nat))))
  exact h.of_eq (by intro c; simp only [premises_HasJ_finite,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasJ_finite_exact (C : OrthemologyV2.TypeCode) (Γ : P01AC.Tel) (t : OrthemologyV2.Term) (τ : List P01AC.Ty) (aux0 : AuxiliaryCertificates.FiniteCert) : premises_HasJ_finite (encode (Rule.HasJ_finite C Γ t τ aux0)) = ((Rule.HasJ_finite C Γ t τ aux0).premises).map encode := by
  simp only [premises_HasJ_finite,Rule.premises,encode_Rule_HasJ_finite,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasJ_allIntro (c : Nat) : List Nat := [(formCode 1 (ruleField c 0) ((allTyCode (ruleField c 1)))), (hasCode 2 ((twkTelCode (ruleField c 0))) (ruleField c 2) (ruleField c 1))]
theorem primrec_premises_HasJ_allIntro : Primrec premises_HasJ_allIntro := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_allTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1)))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_twkTelCode.comp (primrec_ruleField.comp Primrec.id (.const 0))).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 1))))) (Primrec.const ([] : List Nat))))
  exact h.of_eq (by intro c; simp only [premises_HasJ_allIntro,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasJ_allIntro_exact (Γ : P01AC.Tel) (B : P01AC.Ty) (p : P01D.Poly) : premises_HasJ_allIntro (encode (Rule.HasJ_allIntro Γ B p)) = ((Rule.HasJ_allIntro Γ B p).premises).map encode := by
  simp only [premises_HasJ_allIntro,Rule.premises,encode_Rule_HasJ_allIntro,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasJ_allElim (c : Nat) : List Nat := [(formCode 1 (ruleField c 0) ((allTyCode (ruleField c 1)))), (formCode 1 (ruleField c 0) (ruleField c 2)), (formCode 1 (ruleField c 0) ((tinstCode (ruleField c 2) (ruleField c 1)))), (hasCode 2 (ruleField c 0) (ruleField c 3) ((allTyCode (ruleField c 1))))]
theorem primrec_premises_HasJ_allElim : Primrec premises_HasJ_allElim := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_allTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1)))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 2))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_tinstCode.comp (primrec_ruleField.comp Primrec.id (.const 2)) (primrec_ruleField.comp Primrec.id (.const 1)))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 3)).pair (primrec_allTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1)))))) (Primrec.const ([] : List Nat))))))
  exact h.of_eq (by intro c; simp only [premises_HasJ_allElim,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasJ_allElim_exact (Γ : P01AC.Tel) (B : P01AC.Ty) (A : P01AC.Ty) (p : P01D.Poly) : premises_HasJ_allElim (encode (Rule.HasJ_allElim Γ B A p)) = ((Rule.HasJ_allElim Γ B A p).premises).map encode := by
  simp only [premises_HasJ_allElim,Rule.premises,encode_Rule_HasJ_allElim,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasJ_rawAtom (c : Nat) : List Nat := [(formCode 1 (ruleField c 0) (encode (P01AC.Ty.raw)))]
theorem primrec_premises_HasJ_rawAtom : Primrec premises_HasJ_rawAtom := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (Primrec.const (encode (P01AC.Ty.raw)))) (Primrec.const ([] : List Nat)))
  exact h.of_eq (by intro c; simp only [premises_HasJ_rawAtom,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasJ_rawAtom_exact (Γ : P01AC.Tel) (t : OrthemologyV2.Term) : premises_HasJ_rawAtom (encode (Rule.HasJ_rawAtom Γ t)) = ((Rule.HasJ_rawAtom Γ t).premises).map encode := by
  simp only [premises_HasJ_rawAtom,Rule.premises,encode_Rule_HasJ_rawAtom,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasJ_rawApp (c : Nat) : List Nat := [(formCode 1 (ruleField c 0) (encode (P01AC.Ty.raw))), (hasCode 2 (ruleField c 0) (ruleField c 1) (encode (P01AC.Ty.raw))), (hasCode 2 (ruleField c 0) (ruleField c 2) (encode (P01AC.Ty.raw)))]
theorem primrec_premises_HasJ_rawApp : Primrec premises_HasJ_rawApp := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (Primrec.const (encode (P01AC.Ty.raw)))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 1)).pair (Primrec.const (encode (P01AC.Ty.raw)))))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (Primrec.const (encode (P01AC.Ty.raw)))))) (Primrec.const ([] : List Nat)))))
  exact h.of_eq (by intro c; simp only [premises_HasJ_rawApp,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasJ_rawApp_exact (Γ : P01AC.Tel) (f : P01D.Poly) (a : P01D.Poly) : premises_HasJ_rawApp (encode (Rule.HasJ_rawApp Γ f a)) = ((Rule.HasJ_rawApp Γ f a).premises).map encode := by
  simp only [premises_HasJ_rawApp,Rule.premises,encode_Rule_HasJ_rawApp,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasJ_piIntro (c : Nat) : List Nat := [(formCode 1 (ruleField c 0) ((piCode (ruleField c 1) (ruleField c 2)))), (hasCode 2 ((telConsCode (ruleField c 1) (ruleField c 0))) (ruleField c 3) (ruleField c 2))]
theorem primrec_premises_HasJ_piIntro : Primrec premises_HasJ_piIntro := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_piCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2)))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_telConsCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 0))).pair ((primrec_ruleField.comp Primrec.id (.const 3)).pair (primrec_ruleField.comp Primrec.id (.const 2))))) (Primrec.const ([] : List Nat))))
  exact h.of_eq (by intro c; simp only [premises_HasJ_piIntro,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasJ_piIntro_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (b : P01D.Poly) : premises_HasJ_piIntro (encode (Rule.HasJ_piIntro Γ A B b)) = ((Rule.HasJ_piIntro Γ A B b).premises).map encode := by
  simp only [premises_HasJ_piIntro,Rule.premises,encode_Rule_HasJ_piIntro,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasJ_piElim (c : Nat) : List Nat := [(formCode 1 (ruleField c 0) ((piCode (ruleField c 1) (ruleField c 2)))), (formCode 1 (ruleField c 0) ((instTyCode (ruleField c 3) (ruleField c 2)))), (hasCode 2 (ruleField c 0) (ruleField c 4) ((piCode (ruleField c 1) (ruleField c 2)))), (hasCode 2 (ruleField c 0) (ruleField c 3) (ruleField c 1))]
theorem primrec_premises_HasJ_piElim : Primrec premises_HasJ_piElim := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_piCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2)))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_instTyCode.comp (primrec_ruleField.comp Primrec.id (.const 3)) (primrec_ruleField.comp Primrec.id (.const 2)))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 4)).pair (primrec_piCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2)))))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 3)).pair (primrec_ruleField.comp Primrec.id (.const 1))))) (Primrec.const ([] : List Nat))))))
  exact h.of_eq (by intro c; simp only [premises_HasJ_piElim,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasJ_piElim_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (a : P01D.Poly) (f : P01D.Poly) : premises_HasJ_piElim (encode (Rule.HasJ_piElim Γ A B a f)) = ((Rule.HasJ_piElim Γ A B a f).premises).map encode := by
  simp only [premises_HasJ_piElim,Rule.premises,encode_Rule_HasJ_piElim,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasJ_sigmaIntro (c : Nat) : List Nat := [(formCode 1 (ruleField c 0) ((sigmaTyCode (ruleField c 1) (ruleField c 2)))), (formCode 1 (ruleField c 0) ((instTyCode (ruleField c 3) (ruleField c 2)))), (hasCode 2 (ruleField c 0) (ruleField c 3) (ruleField c 1)), (hasCode 2 (ruleField c 0) (ruleField c 4) ((instTyCode (ruleField c 3) (ruleField c 2))))]
theorem primrec_premises_HasJ_sigmaIntro : Primrec premises_HasJ_sigmaIntro := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_sigmaTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2)))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_instTyCode.comp (primrec_ruleField.comp Primrec.id (.const 3)) (primrec_ruleField.comp Primrec.id (.const 2)))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 3)).pair (primrec_ruleField.comp Primrec.id (.const 1))))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 4)).pair (primrec_instTyCode.comp (primrec_ruleField.comp Primrec.id (.const 3)) (primrec_ruleField.comp Primrec.id (.const 2)))))) (Primrec.const ([] : List Nat))))))
  exact h.of_eq (by intro c; simp only [premises_HasJ_sigmaIntro,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasJ_sigmaIntro_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (a : P01D.Poly) (b : P01D.Poly) : premises_HasJ_sigmaIntro (encode (Rule.HasJ_sigmaIntro Γ A B a b)) = ((Rule.HasJ_sigmaIntro Γ A B a b).premises).map encode := by
  simp only [premises_HasJ_sigmaIntro,Rule.premises,encode_Rule_HasJ_sigmaIntro,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasJ_sigmaFst (c : Nat) : List Nat := [(formCode 1 (ruleField c 0) (ruleField c 1)), (formCode 1 (ruleField c 0) ((sigmaTyCode (ruleField c 1) (ruleField c 2)))), (hasCode 2 (ruleField c 0) (ruleField c 3) ((sigmaTyCode (ruleField c 1) (ruleField c 2))))]
theorem primrec_premises_HasJ_sigmaFst : Primrec premises_HasJ_sigmaFst := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_sigmaTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2)))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 3)).pair (primrec_sigmaTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2)))))) (Primrec.const ([] : List Nat)))))
  exact h.of_eq (by intro c; simp only [premises_HasJ_sigmaFst,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasJ_sigmaFst_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (z : P01D.Poly) : premises_HasJ_sigmaFst (encode (Rule.HasJ_sigmaFst Γ A B z)) = ((Rule.HasJ_sigmaFst Γ A B z).premises).map encode := by
  simp only [premises_HasJ_sigmaFst,Rule.premises,encode_Rule_HasJ_sigmaFst,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasJ_sigmaSnd (c : Nat) : List Nat := [(formCode 1 (ruleField c 0) ((sigmaTyCode (ruleField c 1) (ruleField c 2)))), (formCode 1 (ruleField c 0) ((instTyCode ((fstPolyCode (ruleField c 3))) (ruleField c 2)))), (hasCode 2 (ruleField c 0) (ruleField c 3) ((sigmaTyCode (ruleField c 1) (ruleField c 2))))]
theorem primrec_premises_HasJ_sigmaSnd : Primrec premises_HasJ_sigmaSnd := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_sigmaTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2)))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_instTyCode.comp (primrec_fstPolyCode.comp (primrec_ruleField.comp Primrec.id (.const 3))) (primrec_ruleField.comp Primrec.id (.const 2)))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 3)).pair (primrec_sigmaTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2)))))) (Primrec.const ([] : List Nat)))))
  exact h.of_eq (by intro c; simp only [premises_HasJ_sigmaSnd,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasJ_sigmaSnd_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (z : P01D.Poly) : premises_HasJ_sigmaSnd (encode (Rule.HasJ_sigmaSnd Γ A B z)) = ((Rule.HasJ_sigmaSnd Γ A B z).premises).map encode := by
  simp only [premises_HasJ_sigmaSnd,Rule.premises,encode_Rule_HasJ_sigmaSnd,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasJ_identityIntro (c : Nat) : List Nat := [(formCode 1 (ruleField c 0) ((identityTyCode (ruleField c 1) (ruleField c 2) (ruleField c 3)))), (hasCode 2 (ruleField c 0) (ruleField c 2) (ruleField c 1)), (hasCode 2 (ruleField c 0) (ruleField c 3) (ruleField c 1))]
theorem primrec_premises_HasJ_identityIntro : Primrec premises_HasJ_identityIntro := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_identityTyCode.comp ((primrec_ruleField.comp Primrec.id (.const 1)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 3)))))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 1))))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 3)).pair (primrec_ruleField.comp Primrec.id (.const 1))))) (Primrec.const ([] : List Nat)))))
  exact h.of_eq (by intro c; simp only [premises_HasJ_identityIntro,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasJ_identityIntro_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (aux0 : AuxiliaryCertificates.PolyCert) : premises_HasJ_identityIntro (encode (Rule.HasJ_identityIntro Γ A p q aux0)) = ((Rule.HasJ_identityIntro Γ A p q aux0).premises).map encode := by
  simp only [premises_HasJ_identityIntro,Rule.premises,encode_Rule_HasJ_identityIntro,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasJ_proofErase (c : Nat) : List Nat := [(formCode 1 (ruleField c 0) (encode (P01AC.Ty.raw))), (formCode 1 (ruleField c 0) ((identityTyCode (ruleField c 1) (ruleField c 2) (ruleField c 3)))), (hasCode 2 (ruleField c 0) (ruleField c 4) ((identityTyCode (ruleField c 1) (ruleField c 2) (ruleField c 3))))]
theorem primrec_premises_HasJ_proofErase : Primrec premises_HasJ_proofErase := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (Primrec.const (encode (P01AC.Ty.raw)))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_identityTyCode.comp ((primrec_ruleField.comp Primrec.id (.const 1)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 3)))))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 4)).pair (primrec_identityTyCode.comp ((primrec_ruleField.comp Primrec.id (.const 1)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 3)))))))) (Primrec.const ([] : List Nat)))))
  exact h.of_eq (by intro c; simp only [premises_HasJ_proofErase,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasJ_proofErase_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (x : P01D.Poly) (y : P01D.Poly) (p : P01D.Poly) : premises_HasJ_proofErase (encode (Rule.HasJ_proofErase Γ A x y p)) = ((Rule.HasJ_proofErase Γ A x y p).premises).map encode := by
  simp only [premises_HasJ_proofErase,Rule.premises,encode_Rule_HasJ_proofErase,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasJ_j (c : Nat) : List Nat := [(formCode 1 (ruleField c 0) (ruleField c 1)), (formCode 1 ((thetaCode (ruleField c 0) (ruleField c 1) (ruleField c 2))) (ruleField c 3)), (formCode 1 (ruleField c 0) ((identityTyCode (ruleField c 1) (ruleField c 2) (ruleField c 4)))), (formCode 1 (ruleField c 0) ((motiveAtCode (ruleField c 3) (ruleField c 2) ((polyAtom (encode (OrthemologyV2.Term.i))))))), (formCode 1 (ruleField c 0) ((motiveAtCode (ruleField c 3) (ruleField c 4) (ruleField c 5)))), (hasCode 2 (ruleField c 0) (ruleField c 2) (ruleField c 1)), (hasCode 2 (ruleField c 0) (ruleField c 4) (ruleField c 1)), (hasCode 2 (ruleField c 0) (ruleField c 5) ((identityTyCode (ruleField c 1) (ruleField c 2) (ruleField c 4)))), (hasCode 2 (ruleField c 0) (ruleField c 6) ((motiveAtCode (ruleField c 3) (ruleField c 2) ((polyAtom (encode (OrthemologyV2.Term.i)))))))]
theorem primrec_premises_HasJ_j : Primrec premises_HasJ_j := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_thetaCode.comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 1)).pair (primrec_ruleField.comp Primrec.id (.const 2))))) (primrec_ruleField.comp Primrec.id (.const 3))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_identityTyCode.comp ((primrec_ruleField.comp Primrec.id (.const 1)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 4)))))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_motiveAtCode.comp ((primrec_ruleField.comp Primrec.id (.const 3)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_polyAtom.comp (Primrec.const (encode (OrthemologyV2.Term.i)))))))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_motiveAtCode.comp ((primrec_ruleField.comp Primrec.id (.const 3)).pair ((primrec_ruleField.comp Primrec.id (.const 4)).pair (primrec_ruleField.comp Primrec.id (.const 5)))))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 1))))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 4)).pair (primrec_ruleField.comp Primrec.id (.const 1))))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 5)).pair (primrec_identityTyCode.comp ((primrec_ruleField.comp Primrec.id (.const 1)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 4)))))))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 6)).pair (primrec_motiveAtCode.comp ((primrec_ruleField.comp Primrec.id (.const 3)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_polyAtom.comp (Primrec.const (encode (OrthemologyV2.Term.i)))))))))) (Primrec.const ([] : List Nat)))))))))))
  exact h.of_eq (by intro c; simp only [premises_HasJ_j,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasJ_j_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (x : P01D.Poly) (B : P01AC.Ty) (y : P01D.Poly) (e : P01D.Poly) (d : P01D.Poly) : premises_HasJ_j (encode (Rule.HasJ_j Γ A x B y e d)) = ((Rule.HasJ_j Γ A x B y e d).premises).map encode := by
  simp only [premises_HasJ_j,Rule.premises,encode_Rule_HasJ_j,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasJ_conv (c : Nat) : List Nat := [(formCode 1 (ruleField c 0) (ruleField c 1)), (hasCode 2 (ruleField c 0) (ruleField c 2) (ruleField c 1))]
theorem primrec_premises_HasJ_conv : Primrec premises_HasJ_conv := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 1))))) (Primrec.const ([] : List Nat))))
  exact h.of_eq (by intro c; simp only [premises_HasJ_conv,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasJ_conv_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (aux0 : AuxiliaryCertificates.PolyCert) : premises_HasJ_conv (encode (Rule.HasJ_conv Γ A p q aux0)) = ((Rule.HasJ_conv Γ A p q aux0).premises).map encode := by
  simp only [premises_HasJ_conv,Rule.premises,encode_Rule_HasJ_conv,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasJ_piExt (c : Nat) : List Nat := [(formCode 1 (ruleField c 0) (ruleField c 1)), (formCode 1 ((telConsCode (ruleField c 1) (ruleField c 0))) (ruleField c 2)), (formCode 1 (ruleField c 0) ((piCode (ruleField c 1) (ruleField c 2)))), (hasCode 2 (ruleField c 0) (ruleField c 3) ((piCode (ruleField c 1) (ruleField c 2)))), (hasCode 2 (ruleField c 0) (ruleField c 4) ((piCode (ruleField c 1) (ruleField c 2)))), (formCode 1 ((telConsCode (ruleField c 1) (ruleField c 0))) ((identityTyCode (ruleField c 2) ((appCode ((shiftCode 1 (ruleField c 3))) ((varCode (0))))) ((appCode ((shiftCode 1 (ruleField c 4))) ((varCode (0)))))))), (formCode 1 (ruleField c 0) ((piCode (ruleField c 1) ((identityTyCode (ruleField c 2) ((appCode ((shiftCode 1 (ruleField c 3))) ((varCode (0))))) ((appCode ((shiftCode 1 (ruleField c 4))) ((varCode (0)))))))))), (hasCode 2 (ruleField c 0) (ruleField c 5) ((piCode (ruleField c 1) ((identityTyCode (ruleField c 2) ((appCode ((shiftCode 1 (ruleField c 3))) ((varCode (0))))) ((appCode ((shiftCode 1 (ruleField c 4))) ((varCode (0)))))))))), (formCode 1 (ruleField c 0) ((identityTyCode ((piCode (ruleField c 1) (ruleField c 2))) (ruleField c 3) (ruleField c 4))))]
theorem primrec_premises_HasJ_piExt : Primrec premises_HasJ_piExt := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_telConsCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 2))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_piCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2)))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 3)).pair (primrec_piCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2)))))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 4)).pair (primrec_piCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2)))))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_telConsCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_identityTyCode.comp ((primrec_ruleField.comp Primrec.id (.const 2)).pair ((primrec_appCode.comp ((primrec_shiftCode.comp (.const 1) Primrec.id).comp (primrec_ruleField.comp Primrec.id (.const 3))) (primrec_varCode.comp (Primrec.const 0))).pair (primrec_appCode.comp ((primrec_shiftCode.comp (.const 1) Primrec.id).comp (primrec_ruleField.comp Primrec.id (.const 4))) (primrec_varCode.comp (Primrec.const 0))))))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_piCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_identityTyCode.comp ((primrec_ruleField.comp Primrec.id (.const 2)).pair ((primrec_appCode.comp ((primrec_shiftCode.comp (.const 1) Primrec.id).comp (primrec_ruleField.comp Primrec.id (.const 3))) (primrec_varCode.comp (Primrec.const 0))).pair (primrec_appCode.comp ((primrec_shiftCode.comp (.const 1) Primrec.id).comp (primrec_ruleField.comp Primrec.id (.const 4))) (primrec_varCode.comp (Primrec.const 0)))))))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 5)).pair (primrec_piCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_identityTyCode.comp ((primrec_ruleField.comp Primrec.id (.const 2)).pair ((primrec_appCode.comp ((primrec_shiftCode.comp (.const 1) Primrec.id).comp (primrec_ruleField.comp Primrec.id (.const 3))) (primrec_varCode.comp (Primrec.const 0))).pair (primrec_appCode.comp ((primrec_shiftCode.comp (.const 1) Primrec.id).comp (primrec_ruleField.comp Primrec.id (.const 4))) (primrec_varCode.comp (Primrec.const 0)))))))))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_identityTyCode.comp ((primrec_piCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2))).pair ((primrec_ruleField.comp Primrec.id (.const 3)).pair (primrec_ruleField.comp Primrec.id (.const 4)))))) (Primrec.const ([] : List Nat)))))))))))
  exact h.of_eq (by intro c; simp only [premises_HasJ_piExt,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasJ_piExt_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (h : P01D.Poly) : premises_HasJ_piExt (encode (Rule.HasJ_piExt Γ A B p q h)) = ((Rule.HasJ_piExt Γ A B p q h).premises).map encode := by
  simp only [premises_HasJ_piExt,Rule.premises,encode_Rule_HasJ_piExt,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasJ_allExt (c : Nat) : List Nat := [(formCode 1 ((twkTelCode (ruleField c 0))) (ruleField c 1)), (formCode 1 (ruleField c 0) ((allTyCode (ruleField c 1)))), (hasCode 2 (ruleField c 0) (ruleField c 2) ((allTyCode (ruleField c 1)))), (hasCode 2 (ruleField c 0) (ruleField c 3) ((allTyCode (ruleField c 1)))), (formCode 1 ((twkTelCode (ruleField c 0))) ((identityTyCode (ruleField c 1) (ruleField c 2) (ruleField c 3)))), (hasCode 2 ((twkTelCode (ruleField c 0))) (ruleField c 4) ((identityTyCode (ruleField c 1) (ruleField c 2) (ruleField c 3)))), (formCode 1 (ruleField c 0) ((identityTyCode ((allTyCode (ruleField c 1))) (ruleField c 2) (ruleField c 3))))]
theorem primrec_premises_HasJ_allExt : Primrec premises_HasJ_allExt := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_twkTelCode.comp (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_allTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1)))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_allTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1)))))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 3)).pair (primrec_allTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1)))))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_twkTelCode.comp (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_identityTyCode.comp ((primrec_ruleField.comp Primrec.id (.const 1)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 3)))))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_twkTelCode.comp (primrec_ruleField.comp Primrec.id (.const 0))).pair ((primrec_ruleField.comp Primrec.id (.const 4)).pair (primrec_identityTyCode.comp ((primrec_ruleField.comp Primrec.id (.const 1)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 3)))))))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_identityTyCode.comp ((primrec_allTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1))).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 3)))))) (Primrec.const ([] : List Nat)))))))))
  exact h.of_eq (by intro c; simp only [premises_HasJ_allExt,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasJ_allExt_exact (Γ : P01AC.Tel) (B : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (h : P01D.Poly) : premises_HasJ_allExt (encode (Rule.HasJ_allExt Γ B p q h)) = ((Rule.HasJ_allExt Γ B p q h).premises).map encode := by
  simp only [premises_HasJ_allExt,Rule.premises,encode_Rule_HasJ_allExt,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasJ_sigmaElim (c : Nat) : List Nat := [(ctxCode 0 (ruleField c 0)), (formCode 1 (ruleField c 0) (ruleField c 1)), (formCode 1 ((telConsCode (ruleField c 1) (ruleField c 0))) (ruleField c 2)), (formCode 1 ((telConsCode ((sigmaTyCode (ruleField c 1) (ruleField c 2))) (ruleField c 0))) (ruleField c 3)), (hasCode 2 ((telConsCode (ruleField c 2) ((telConsCode (ruleField c 1) (ruleField c 0))))) (ruleField c 4) ((branchTypeCode (ruleField c 3)))), (hasCode 2 (ruleField c 0) (ruleField c 5) ((sigmaTyCode (ruleField c 1) (ruleField c 2))))]
theorem primrec_premises_HasJ_sigmaElim : Primrec premises_HasJ_sigmaElim := by
  have h := (Primrec.list_cons.comp ((primrec_ctxCode 0).comp (primrec_ruleField.comp Primrec.id (.const 0))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_telConsCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 2))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_telConsCode.comp (primrec_sigmaTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2))) (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 3))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_telConsCode.comp (primrec_ruleField.comp Primrec.id (.const 2)) (primrec_telConsCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 0)))).pair ((primrec_ruleField.comp Primrec.id (.const 4)).pair (primrec_branchTypeCode.comp (primrec_ruleField.comp Primrec.id (.const 3)))))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 5)).pair (primrec_sigmaTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2)))))) (Primrec.const ([] : List Nat))))))))
  exact h.of_eq (by intro c; simp only [premises_HasJ_sigmaElim,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasJ_sigmaElim_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (P : P01AC.Ty) (d : P01D.Poly) (z : P01D.Poly) : premises_HasJ_sigmaElim (encode (Rule.HasJ_sigmaElim Γ A B P d z)) = ((Rule.HasJ_sigmaElim Γ A B P d z).premises).map encode := by
  simp only [premises_HasJ_sigmaElim,Rule.premises,encode_Rule_HasJ_sigmaElim,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasJ_natInduction (c : Nat) : List Nat := [(ctxCode 0 (ruleField c 0)), (formCode 1 ((telConsCode (encode (P01AC.EffectiveCompleteness.N)) (ruleField c 0))) (ruleField c 1)), (hasCode 2 (ruleField c 0) (ruleField c 2) ((instTyCode (encode (SourceRigidity.zero)) (ruleField c 1)))), (hasCode 2 (ruleField c 0) (ruleField c 3) ((dependentStepTypeCode (ruleField c 1))))]
theorem primrec_premises_HasJ_natInduction : Primrec premises_HasJ_natInduction := by
  have h := (Primrec.list_cons.comp ((primrec_ctxCode 0).comp (primrec_ruleField.comp Primrec.id (.const 0))) (Primrec.list_cons.comp ((primrec_formCode 1).comp (primrec_telConsCode.comp (Primrec.const (encode (P01AC.EffectiveCompleteness.N))) (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_instTyCode.comp (Primrec.const (encode (SourceRigidity.zero))) (primrec_ruleField.comp Primrec.id (.const 1)))))) (Primrec.list_cons.comp ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 3)).pair (primrec_dependentStepTypeCode.comp (primrec_ruleField.comp Primrec.id (.const 1)))))) (Primrec.const ([] : List Nat))))))
  exact h.of_eq (by intro c; simp only [premises_HasJ_natInduction,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasJ_natInduction_exact (Γ : P01AC.Tel) (P : P01AC.Ty) (p : P01D.Poly) (s : P01D.Poly) : premises_HasJ_natInduction (encode (Rule.HasJ_natInduction Γ P p s)) = ((Rule.HasJ_natInduction Γ P p s).premises).map encode := by
  simp only [premises_HasJ_natInduction,Rule.premises,encode_Rule_HasJ_natInduction,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_CtxE_nil (c : Nat) : List Nat := []
theorem primrec_premises_CtxE_nil : Primrec premises_CtxE_nil := by
  have h : Primrec (fun _ : Nat => ([] : List Nat)) := Primrec.const _
  exact h.of_eq (by intro c; simp only [premises_CtxE_nil,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_CtxE_nil_exact  : premises_CtxE_nil (encode (Rule.CtxE_nil )) = ((Rule.CtxE_nil ).premises).map encode := by
  simp only [premises_CtxE_nil,Rule.premises,encode_Rule_CtxE_nil,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_CtxE_ext (c : Nat) : List Nat := [(ctxCode 3 (ruleField c 0)), (formCode 4 (ruleField c 0) (ruleField c 1))]
theorem primrec_premises_CtxE_ext : Primrec premises_CtxE_ext := by
  have h := (Primrec.list_cons.comp ((primrec_ctxCode 3).comp (primrec_ruleField.comp Primrec.id (.const 0))) (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.const ([] : List Nat))))
  exact h.of_eq (by intro c; simp only [premises_CtxE_ext,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_CtxE_ext_exact (Γ : P01AC.Tel) (A : P01AC.Ty) : premises_CtxE_ext (encode (Rule.CtxE_ext Γ A)) = ((Rule.CtxE_ext Γ A).premises).map encode := by
  simp only [premises_CtxE_ext,Rule.premises,encode_Rule_CtxE_ext,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_FormE_param (c : Nat) : List Nat := [(ctxCode 3 (ruleField c 0))]
theorem primrec_premises_FormE_param : Primrec premises_FormE_param := by
  have h := (Primrec.list_cons.comp ((primrec_ctxCode 3).comp (primrec_ruleField.comp Primrec.id (.const 0))) (Primrec.const ([] : List Nat)))
  exact h.of_eq (by intro c; simp only [premises_FormE_param,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_FormE_param_exact (Γ : P01AC.Tel) (n : Nat) : premises_FormE_param (encode (Rule.FormE_param Γ n)) = ((Rule.FormE_param Γ n).premises).map encode := by
  simp only [premises_FormE_param,Rule.premises,encode_Rule_FormE_param,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_FormE_bottom (c : Nat) : List Nat := [(ctxCode 3 (ruleField c 0))]
theorem primrec_premises_FormE_bottom : Primrec premises_FormE_bottom := by
  have h := (Primrec.list_cons.comp ((primrec_ctxCode 3).comp (primrec_ruleField.comp Primrec.id (.const 0))) (Primrec.const ([] : List Nat)))
  exact h.of_eq (by intro c; simp only [premises_FormE_bottom,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_FormE_bottom_exact (Γ : P01AC.Tel) : premises_FormE_bottom (encode (Rule.FormE_bottom Γ)) = ((Rule.FormE_bottom Γ).premises).map encode := by
  simp only [premises_FormE_bottom,Rule.premises,encode_Rule_FormE_bottom,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_FormE_all (c : Nat) : List Nat := [(ctxCode 3 (ruleField c 0)), (formCode 4 ((twkTelCode (ruleField c 0))) (ruleField c 1))]
theorem primrec_premises_FormE_all : Primrec premises_FormE_all := by
  have h := (Primrec.list_cons.comp ((primrec_ctxCode 3).comp (primrec_ruleField.comp Primrec.id (.const 0))) (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_twkTelCode.comp (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.const ([] : List Nat))))
  exact h.of_eq (by intro c; simp only [premises_FormE_all,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_FormE_all_exact (Γ : P01AC.Tel) (B : P01AC.Ty) : premises_FormE_all (encode (Rule.FormE_all Γ B)) = ((Rule.FormE_all Γ B).premises).map encode := by
  simp only [premises_FormE_all,Rule.premises,encode_Rule_FormE_all,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_FormE_raw (c : Nat) : List Nat := [(ctxCode 3 (ruleField c 0))]
theorem primrec_premises_FormE_raw : Primrec premises_FormE_raw := by
  have h := (Primrec.list_cons.comp ((primrec_ctxCode 3).comp (primrec_ruleField.comp Primrec.id (.const 0))) (Primrec.const ([] : List Nat)))
  exact h.of_eq (by intro c; simp only [premises_FormE_raw,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_FormE_raw_exact (Γ : P01AC.Tel) : premises_FormE_raw (encode (Rule.FormE_raw Γ)) = ((Rule.FormE_raw Γ).premises).map encode := by
  simp only [premises_FormE_raw,Rule.premises,encode_Rule_FormE_raw,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_FormE_pi (c : Nat) : List Nat := [(formCode 4 (ruleField c 0) (ruleField c 1)), (formCode 4 ((telConsCode (ruleField c 1) (ruleField c 0))) (ruleField c 2))]
theorem primrec_premises_FormE_pi : Primrec premises_FormE_pi := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_telConsCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 2))) (Primrec.const ([] : List Nat))))
  exact h.of_eq (by intro c; simp only [premises_FormE_pi,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_FormE_pi_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : premises_FormE_pi (encode (Rule.FormE_pi Γ A B)) = ((Rule.FormE_pi Γ A B).premises).map encode := by
  simp only [premises_FormE_pi,Rule.premises,encode_Rule_FormE_pi,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_FormE_sigma (c : Nat) : List Nat := [(formCode 4 (ruleField c 0) (ruleField c 1)), (formCode 4 ((telConsCode (ruleField c 1) (ruleField c 0))) (ruleField c 2))]
theorem primrec_premises_FormE_sigma : Primrec premises_FormE_sigma := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_telConsCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 2))) (Primrec.const ([] : List Nat))))
  exact h.of_eq (by intro c; simp only [premises_FormE_sigma,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_FormE_sigma_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : premises_FormE_sigma (encode (Rule.FormE_sigma Γ A B)) = ((Rule.FormE_sigma Γ A B).premises).map encode := by
  simp only [premises_FormE_sigma,Rule.premises,encode_Rule_FormE_sigma,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_FormE_identity (c : Nat) : List Nat := [(formCode 4 (ruleField c 0) (ruleField c 1)), (hasCode 5 (ruleField c 0) (ruleField c 2) (ruleField c 1)), (hasCode 5 (ruleField c 0) (ruleField c 3) (ruleField c 1))]
theorem primrec_premises_FormE_identity : Primrec premises_FormE_identity := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.list_cons.comp ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 1))))) (Primrec.list_cons.comp ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 3)).pair (primrec_ruleField.comp Primrec.id (.const 1))))) (Primrec.const ([] : List Nat)))))
  exact h.of_eq (by intro c; simp only [premises_FormE_identity,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_FormE_identity_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) : premises_FormE_identity (encode (Rule.FormE_identity Γ A p q)) = ((Rule.FormE_identity Γ A p q).premises).map encode := by
  simp only [premises_FormE_identity,Rule.premises,encode_Rule_FormE_identity,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasE_var (c : Nat) : List Nat := [(formCode 4 (ruleField c 0) (ruleField c 1))]
theorem primrec_premises_HasE_var : Primrec premises_HasE_var := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.const ([] : List Nat)))
  exact h.of_eq (by intro c; simp only [premises_HasE_var,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasE_var_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (n : Nat) (aux0 : AuxiliaryCertificates.LookupCert) : premises_HasE_var (encode (Rule.HasE_var Γ A n aux0)) = ((Rule.HasE_var Γ A n aux0).premises).map encode := by
  simp only [premises_HasE_var,Rule.premises,encode_Rule_HasE_var,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasE_i (c : Nat) : List Nat := [(formCode 4 (ruleField c 0) (ruleField c 1)), (formCode 4 (ruleField c 0) ((arrCode (ruleField c 1) (ruleField c 1))))]
theorem primrec_premises_HasE_i : Primrec premises_HasE_i := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_arrCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 1)))) (Primrec.const ([] : List Nat))))
  exact h.of_eq (by intro c; simp only [premises_HasE_i,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasE_i_exact (Γ : P01AC.Tel) (A : P01AC.Ty) : premises_HasE_i (encode (Rule.HasE_i Γ A)) = ((Rule.HasE_i Γ A).premises).map encode := by
  simp only [premises_HasE_i,Rule.premises,encode_Rule_HasE_i,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasE_k (c : Nat) : List Nat := [(formCode 4 (ruleField c 0) (ruleField c 1)), (formCode 4 (ruleField c 0) (ruleField c 2)), (formCode 4 (ruleField c 0) ((arrCode (ruleField c 1) ((arrCode (ruleField c 2) (ruleField c 1))))))]
theorem primrec_premises_HasE_k : Primrec premises_HasE_k := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 2))) (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_arrCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_arrCode.comp (primrec_ruleField.comp Primrec.id (.const 2)) (primrec_ruleField.comp Primrec.id (.const 1))))) (Primrec.const ([] : List Nat)))))
  exact h.of_eq (by intro c; simp only [premises_HasE_k,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasE_k_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : premises_HasE_k (encode (Rule.HasE_k Γ A B)) = ((Rule.HasE_k Γ A B).premises).map encode := by
  simp only [premises_HasE_k,Rule.premises,encode_Rule_HasE_k,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasE_s (c : Nat) : List Nat := [(formCode 4 (ruleField c 0) (ruleField c 1)), (formCode 4 (ruleField c 0) (ruleField c 2)), (formCode 4 (ruleField c 0) (ruleField c 3)), (formCode 4 (ruleField c 0) ((arrCode ((arrCode (ruleField c 1) ((arrCode (ruleField c 2) (ruleField c 3))))) ((arrCode ((arrCode (ruleField c 1) (ruleField c 2))) ((arrCode (ruleField c 1) (ruleField c 3))))))))]
theorem primrec_premises_HasE_s : Primrec premises_HasE_s := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 2))) (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 3))) (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_arrCode.comp (primrec_arrCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_arrCode.comp (primrec_ruleField.comp Primrec.id (.const 2)) (primrec_ruleField.comp Primrec.id (.const 3)))) (primrec_arrCode.comp (primrec_arrCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2))) (primrec_arrCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 3)))))) (Primrec.const ([] : List Nat))))))
  exact h.of_eq (by intro c; simp only [premises_HasE_s,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasE_s_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (C : P01AC.Ty) : premises_HasE_s (encode (Rule.HasE_s Γ A B C)) = ((Rule.HasE_s Γ A B C).premises).map encode := by
  simp only [premises_HasE_s,Rule.premises,encode_Rule_HasE_s,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasE_finite (c : Nat) : List Nat := (List.append ((formImagesCode 4 (ruleField c 1) (ruleField c 3))) ([(formCode 4 (ruleField c 1) ((tsubstTelCode (ruleField c 3) ((finCode (ruleField c 0))))))]))
theorem primrec_premises_HasE_finite : Primrec premises_HasE_finite := by
  have h := (Primrec.list_append.comp ((primrec_formImagesCode 4).comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 3))) (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_tsubstTelCode.comp (primrec_ruleField.comp Primrec.id (.const 3)) (primrec_finCode.comp (primrec_ruleField.comp Primrec.id (.const 0))))) (Primrec.const ([] : List Nat))))
  exact h.of_eq (by intro c; simp only [premises_HasE_finite,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasE_finite_exact (C : OrthemologyV2.TypeCode) (Γ : P01AC.Tel) (t : OrthemologyV2.Term) (τ : List P01AC.Ty) (aux0 : AuxiliaryCertificates.FiniteCert) : premises_HasE_finite (encode (Rule.HasE_finite C Γ t τ aux0)) = ((Rule.HasE_finite C Γ t τ aux0).premises).map encode := by
  simp only [premises_HasE_finite,Rule.premises,encode_Rule_HasE_finite,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasE_allIntro (c : Nat) : List Nat := [(formCode 4 (ruleField c 0) ((allTyCode (ruleField c 1)))), (hasCode 5 ((twkTelCode (ruleField c 0))) (ruleField c 2) (ruleField c 1))]
theorem primrec_premises_HasE_allIntro : Primrec premises_HasE_allIntro := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_allTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1)))) (Primrec.list_cons.comp ((primrec_hasCode 5).comp ((primrec_twkTelCode.comp (primrec_ruleField.comp Primrec.id (.const 0))).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 1))))) (Primrec.const ([] : List Nat))))
  exact h.of_eq (by intro c; simp only [premises_HasE_allIntro,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasE_allIntro_exact (Γ : P01AC.Tel) (B : P01AC.Ty) (p : P01D.Poly) : premises_HasE_allIntro (encode (Rule.HasE_allIntro Γ B p)) = ((Rule.HasE_allIntro Γ B p).premises).map encode := by
  simp only [premises_HasE_allIntro,Rule.premises,encode_Rule_HasE_allIntro,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasE_allElim (c : Nat) : List Nat := [(formCode 4 (ruleField c 0) ((allTyCode (ruleField c 1)))), (formCode 4 (ruleField c 0) (ruleField c 2)), (formCode 4 (ruleField c 0) ((tinstCode (ruleField c 2) (ruleField c 1)))), (hasCode 5 (ruleField c 0) (ruleField c 3) ((allTyCode (ruleField c 1))))]
theorem primrec_premises_HasE_allElim : Primrec premises_HasE_allElim := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_allTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1)))) (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 2))) (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_tinstCode.comp (primrec_ruleField.comp Primrec.id (.const 2)) (primrec_ruleField.comp Primrec.id (.const 1)))) (Primrec.list_cons.comp ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 3)).pair (primrec_allTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1)))))) (Primrec.const ([] : List Nat))))))
  exact h.of_eq (by intro c; simp only [premises_HasE_allElim,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasE_allElim_exact (Γ : P01AC.Tel) (B : P01AC.Ty) (A : P01AC.Ty) (p : P01D.Poly) : premises_HasE_allElim (encode (Rule.HasE_allElim Γ B A p)) = ((Rule.HasE_allElim Γ B A p).premises).map encode := by
  simp only [premises_HasE_allElim,Rule.premises,encode_Rule_HasE_allElim,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasE_rawAtom (c : Nat) : List Nat := [(formCode 4 (ruleField c 0) (encode (P01AC.Ty.raw)))]
theorem primrec_premises_HasE_rawAtom : Primrec premises_HasE_rawAtom := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (Primrec.const (encode (P01AC.Ty.raw)))) (Primrec.const ([] : List Nat)))
  exact h.of_eq (by intro c; simp only [premises_HasE_rawAtom,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasE_rawAtom_exact (Γ : P01AC.Tel) (t : OrthemologyV2.Term) : premises_HasE_rawAtom (encode (Rule.HasE_rawAtom Γ t)) = ((Rule.HasE_rawAtom Γ t).premises).map encode := by
  simp only [premises_HasE_rawAtom,Rule.premises,encode_Rule_HasE_rawAtom,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasE_rawApp (c : Nat) : List Nat := [(formCode 4 (ruleField c 0) (encode (P01AC.Ty.raw))), (hasCode 5 (ruleField c 0) (ruleField c 1) (encode (P01AC.Ty.raw))), (hasCode 5 (ruleField c 0) (ruleField c 2) (encode (P01AC.Ty.raw)))]
theorem primrec_premises_HasE_rawApp : Primrec premises_HasE_rawApp := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (Primrec.const (encode (P01AC.Ty.raw)))) (Primrec.list_cons.comp ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 1)).pair (Primrec.const (encode (P01AC.Ty.raw)))))) (Primrec.list_cons.comp ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (Primrec.const (encode (P01AC.Ty.raw)))))) (Primrec.const ([] : List Nat)))))
  exact h.of_eq (by intro c; simp only [premises_HasE_rawApp,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasE_rawApp_exact (Γ : P01AC.Tel) (f : P01D.Poly) (a : P01D.Poly) : premises_HasE_rawApp (encode (Rule.HasE_rawApp Γ f a)) = ((Rule.HasE_rawApp Γ f a).premises).map encode := by
  simp only [premises_HasE_rawApp,Rule.premises,encode_Rule_HasE_rawApp,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasE_piIntro (c : Nat) : List Nat := [(formCode 4 (ruleField c 0) ((piCode (ruleField c 1) (ruleField c 2)))), (hasCode 5 ((telConsCode (ruleField c 1) (ruleField c 0))) (ruleField c 3) (ruleField c 2))]
theorem primrec_premises_HasE_piIntro : Primrec premises_HasE_piIntro := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_piCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2)))) (Primrec.list_cons.comp ((primrec_hasCode 5).comp ((primrec_telConsCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 0))).pair ((primrec_ruleField.comp Primrec.id (.const 3)).pair (primrec_ruleField.comp Primrec.id (.const 2))))) (Primrec.const ([] : List Nat))))
  exact h.of_eq (by intro c; simp only [premises_HasE_piIntro,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasE_piIntro_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (b : P01D.Poly) : premises_HasE_piIntro (encode (Rule.HasE_piIntro Γ A B b)) = ((Rule.HasE_piIntro Γ A B b).premises).map encode := by
  simp only [premises_HasE_piIntro,Rule.premises,encode_Rule_HasE_piIntro,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasE_piElim (c : Nat) : List Nat := [(formCode 4 (ruleField c 0) ((piCode (ruleField c 1) (ruleField c 2)))), (formCode 4 (ruleField c 0) ((instTyCode (ruleField c 3) (ruleField c 2)))), (hasCode 5 (ruleField c 0) (ruleField c 4) ((piCode (ruleField c 1) (ruleField c 2)))), (hasCode 5 (ruleField c 0) (ruleField c 3) (ruleField c 1))]
theorem primrec_premises_HasE_piElim : Primrec premises_HasE_piElim := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_piCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2)))) (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_instTyCode.comp (primrec_ruleField.comp Primrec.id (.const 3)) (primrec_ruleField.comp Primrec.id (.const 2)))) (Primrec.list_cons.comp ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 4)).pair (primrec_piCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2)))))) (Primrec.list_cons.comp ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 3)).pair (primrec_ruleField.comp Primrec.id (.const 1))))) (Primrec.const ([] : List Nat))))))
  exact h.of_eq (by intro c; simp only [premises_HasE_piElim,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasE_piElim_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (a : P01D.Poly) (f : P01D.Poly) : premises_HasE_piElim (encode (Rule.HasE_piElim Γ A B a f)) = ((Rule.HasE_piElim Γ A B a f).premises).map encode := by
  simp only [premises_HasE_piElim,Rule.premises,encode_Rule_HasE_piElim,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasE_sigmaIntro (c : Nat) : List Nat := [(formCode 4 (ruleField c 0) ((sigmaTyCode (ruleField c 1) (ruleField c 2)))), (formCode 4 (ruleField c 0) ((instTyCode (ruleField c 3) (ruleField c 2)))), (hasCode 5 (ruleField c 0) (ruleField c 3) (ruleField c 1)), (hasCode 5 (ruleField c 0) (ruleField c 4) ((instTyCode (ruleField c 3) (ruleField c 2))))]
theorem primrec_premises_HasE_sigmaIntro : Primrec premises_HasE_sigmaIntro := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_sigmaTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2)))) (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_instTyCode.comp (primrec_ruleField.comp Primrec.id (.const 3)) (primrec_ruleField.comp Primrec.id (.const 2)))) (Primrec.list_cons.comp ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 3)).pair (primrec_ruleField.comp Primrec.id (.const 1))))) (Primrec.list_cons.comp ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 4)).pair (primrec_instTyCode.comp (primrec_ruleField.comp Primrec.id (.const 3)) (primrec_ruleField.comp Primrec.id (.const 2)))))) (Primrec.const ([] : List Nat))))))
  exact h.of_eq (by intro c; simp only [premises_HasE_sigmaIntro,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasE_sigmaIntro_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (a : P01D.Poly) (b : P01D.Poly) : premises_HasE_sigmaIntro (encode (Rule.HasE_sigmaIntro Γ A B a b)) = ((Rule.HasE_sigmaIntro Γ A B a b).premises).map encode := by
  simp only [premises_HasE_sigmaIntro,Rule.premises,encode_Rule_HasE_sigmaIntro,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasE_sigmaFst (c : Nat) : List Nat := [(formCode 4 (ruleField c 0) (ruleField c 1)), (formCode 4 (ruleField c 0) ((sigmaTyCode (ruleField c 1) (ruleField c 2)))), (hasCode 5 (ruleField c 0) (ruleField c 3) ((sigmaTyCode (ruleField c 1) (ruleField c 2))))]
theorem primrec_premises_HasE_sigmaFst : Primrec premises_HasE_sigmaFst := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_sigmaTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2)))) (Primrec.list_cons.comp ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 3)).pair (primrec_sigmaTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2)))))) (Primrec.const ([] : List Nat)))))
  exact h.of_eq (by intro c; simp only [premises_HasE_sigmaFst,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasE_sigmaFst_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (z : P01D.Poly) : premises_HasE_sigmaFst (encode (Rule.HasE_sigmaFst Γ A B z)) = ((Rule.HasE_sigmaFst Γ A B z).premises).map encode := by
  simp only [premises_HasE_sigmaFst,Rule.premises,encode_Rule_HasE_sigmaFst,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasE_sigmaSnd (c : Nat) : List Nat := [(formCode 4 (ruleField c 0) ((sigmaTyCode (ruleField c 1) (ruleField c 2)))), (formCode 4 (ruleField c 0) ((instTyCode ((fstPolyCode (ruleField c 3))) (ruleField c 2)))), (hasCode 5 (ruleField c 0) (ruleField c 3) ((sigmaTyCode (ruleField c 1) (ruleField c 2))))]
theorem primrec_premises_HasE_sigmaSnd : Primrec premises_HasE_sigmaSnd := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_sigmaTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2)))) (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_instTyCode.comp (primrec_fstPolyCode.comp (primrec_ruleField.comp Primrec.id (.const 3))) (primrec_ruleField.comp Primrec.id (.const 2)))) (Primrec.list_cons.comp ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 3)).pair (primrec_sigmaTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2)))))) (Primrec.const ([] : List Nat)))))
  exact h.of_eq (by intro c; simp only [premises_HasE_sigmaSnd,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasE_sigmaSnd_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (z : P01D.Poly) : premises_HasE_sigmaSnd (encode (Rule.HasE_sigmaSnd Γ A B z)) = ((Rule.HasE_sigmaSnd Γ A B z).premises).map encode := by
  simp only [premises_HasE_sigmaSnd,Rule.premises,encode_Rule_HasE_sigmaSnd,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasE_identityIntro (c : Nat) : List Nat := [(formCode 4 (ruleField c 0) ((identityTyCode (ruleField c 1) (ruleField c 2) (ruleField c 3)))), (hasCode 5 (ruleField c 0) (ruleField c 2) (ruleField c 1)), (hasCode 5 (ruleField c 0) (ruleField c 3) (ruleField c 1))]
theorem primrec_premises_HasE_identityIntro : Primrec premises_HasE_identityIntro := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_identityTyCode.comp ((primrec_ruleField.comp Primrec.id (.const 1)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 3)))))) (Primrec.list_cons.comp ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 1))))) (Primrec.list_cons.comp ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 3)).pair (primrec_ruleField.comp Primrec.id (.const 1))))) (Primrec.const ([] : List Nat)))))
  exact h.of_eq (by intro c; simp only [premises_HasE_identityIntro,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasE_identityIntro_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (aux0 : AuxiliaryCertificates.PolyCert) : premises_HasE_identityIntro (encode (Rule.HasE_identityIntro Γ A p q aux0)) = ((Rule.HasE_identityIntro Γ A p q aux0).premises).map encode := by
  simp only [premises_HasE_identityIntro,Rule.premises,encode_Rule_HasE_identityIntro,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasE_proofErase (c : Nat) : List Nat := [(formCode 4 (ruleField c 0) (encode (P01AC.Ty.raw))), (formCode 4 (ruleField c 0) ((identityTyCode (ruleField c 1) (ruleField c 2) (ruleField c 3)))), (hasCode 5 (ruleField c 0) (ruleField c 4) ((identityTyCode (ruleField c 1) (ruleField c 2) (ruleField c 3))))]
theorem primrec_premises_HasE_proofErase : Primrec premises_HasE_proofErase := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (Primrec.const (encode (P01AC.Ty.raw)))) (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_identityTyCode.comp ((primrec_ruleField.comp Primrec.id (.const 1)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 3)))))) (Primrec.list_cons.comp ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 4)).pair (primrec_identityTyCode.comp ((primrec_ruleField.comp Primrec.id (.const 1)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 3)))))))) (Primrec.const ([] : List Nat)))))
  exact h.of_eq (by intro c; simp only [premises_HasE_proofErase,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasE_proofErase_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (x : P01D.Poly) (y : P01D.Poly) (p : P01D.Poly) : premises_HasE_proofErase (encode (Rule.HasE_proofErase Γ A x y p)) = ((Rule.HasE_proofErase Γ A x y p).premises).map encode := by
  simp only [premises_HasE_proofErase,Rule.premises,encode_Rule_HasE_proofErase,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasE_j (c : Nat) : List Nat := [(formCode 4 (ruleField c 0) (ruleField c 1)), (formCode 4 ((thetaCode (ruleField c 0) (ruleField c 1) (ruleField c 2))) (ruleField c 3)), (formCode 4 (ruleField c 0) ((identityTyCode (ruleField c 1) (ruleField c 2) (ruleField c 4)))), (formCode 4 (ruleField c 0) ((motiveAtCode (ruleField c 3) (ruleField c 2) ((polyAtom (encode (OrthemologyV2.Term.i))))))), (formCode 4 (ruleField c 0) ((motiveAtCode (ruleField c 3) (ruleField c 4) (ruleField c 5)))), (hasCode 5 (ruleField c 0) (ruleField c 2) (ruleField c 1)), (hasCode 5 (ruleField c 0) (ruleField c 4) (ruleField c 1)), (hasCode 5 (ruleField c 0) (ruleField c 5) ((identityTyCode (ruleField c 1) (ruleField c 2) (ruleField c 4)))), (hasCode 5 (ruleField c 0) (ruleField c 6) ((motiveAtCode (ruleField c 3) (ruleField c 2) ((polyAtom (encode (OrthemologyV2.Term.i)))))))]
theorem primrec_premises_HasE_j : Primrec premises_HasE_j := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_thetaCode.comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 1)).pair (primrec_ruleField.comp Primrec.id (.const 2))))) (primrec_ruleField.comp Primrec.id (.const 3))) (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_identityTyCode.comp ((primrec_ruleField.comp Primrec.id (.const 1)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 4)))))) (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_motiveAtCode.comp ((primrec_ruleField.comp Primrec.id (.const 3)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_polyAtom.comp (Primrec.const (encode (OrthemologyV2.Term.i)))))))) (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_motiveAtCode.comp ((primrec_ruleField.comp Primrec.id (.const 3)).pair ((primrec_ruleField.comp Primrec.id (.const 4)).pair (primrec_ruleField.comp Primrec.id (.const 5)))))) (Primrec.list_cons.comp ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 1))))) (Primrec.list_cons.comp ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 4)).pair (primrec_ruleField.comp Primrec.id (.const 1))))) (Primrec.list_cons.comp ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 5)).pair (primrec_identityTyCode.comp ((primrec_ruleField.comp Primrec.id (.const 1)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 4)))))))) (Primrec.list_cons.comp ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 6)).pair (primrec_motiveAtCode.comp ((primrec_ruleField.comp Primrec.id (.const 3)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_polyAtom.comp (Primrec.const (encode (OrthemologyV2.Term.i)))))))))) (Primrec.const ([] : List Nat)))))))))))
  exact h.of_eq (by intro c; simp only [premises_HasE_j,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasE_j_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (x : P01D.Poly) (B : P01AC.Ty) (y : P01D.Poly) (e : P01D.Poly) (d : P01D.Poly) : premises_HasE_j (encode (Rule.HasE_j Γ A x B y e d)) = ((Rule.HasE_j Γ A x B y e d).premises).map encode := by
  simp only [premises_HasE_j,Rule.premises,encode_Rule_HasE_j,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasE_conv (c : Nat) : List Nat := [(formCode 4 (ruleField c 0) (ruleField c 1)), (hasCode 5 (ruleField c 0) (ruleField c 2) (ruleField c 1))]
theorem primrec_premises_HasE_conv : Primrec premises_HasE_conv := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.list_cons.comp ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 1))))) (Primrec.const ([] : List Nat))))
  exact h.of_eq (by intro c; simp only [premises_HasE_conv,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasE_conv_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (aux0 : AuxiliaryCertificates.PolyCert) : premises_HasE_conv (encode (Rule.HasE_conv Γ A p q aux0)) = ((Rule.HasE_conv Γ A p q aux0).premises).map encode := by
  simp only [premises_HasE_conv,Rule.premises,encode_Rule_HasE_conv,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasE_piExt (c : Nat) : List Nat := [(formCode 4 (ruleField c 0) (ruleField c 1)), (formCode 4 ((telConsCode (ruleField c 1) (ruleField c 0))) (ruleField c 2)), (formCode 4 (ruleField c 0) ((piCode (ruleField c 1) (ruleField c 2)))), (hasCode 5 (ruleField c 0) (ruleField c 3) ((piCode (ruleField c 1) (ruleField c 2)))), (hasCode 5 (ruleField c 0) (ruleField c 4) ((piCode (ruleField c 1) (ruleField c 2)))), (formCode 4 ((telConsCode (ruleField c 1) (ruleField c 0))) ((identityTyCode (ruleField c 2) ((appCode ((shiftCode 1 (ruleField c 3))) ((varCode (0))))) ((appCode ((shiftCode 1 (ruleField c 4))) ((varCode (0)))))))), (formCode 4 (ruleField c 0) ((piCode (ruleField c 1) ((identityTyCode (ruleField c 2) ((appCode ((shiftCode 1 (ruleField c 3))) ((varCode (0))))) ((appCode ((shiftCode 1 (ruleField c 4))) ((varCode (0)))))))))), (hasCode 5 (ruleField c 0) (ruleField c 5) ((piCode (ruleField c 1) ((identityTyCode (ruleField c 2) ((appCode ((shiftCode 1 (ruleField c 3))) ((varCode (0))))) ((appCode ((shiftCode 1 (ruleField c 4))) ((varCode (0)))))))))), (formCode 4 (ruleField c 0) ((identityTyCode ((piCode (ruleField c 1) (ruleField c 2))) (ruleField c 3) (ruleField c 4))))]
theorem primrec_premises_HasE_piExt : Primrec premises_HasE_piExt := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_telConsCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 2))) (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_piCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2)))) (Primrec.list_cons.comp ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 3)).pair (primrec_piCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2)))))) (Primrec.list_cons.comp ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 4)).pair (primrec_piCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2)))))) (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_telConsCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_identityTyCode.comp ((primrec_ruleField.comp Primrec.id (.const 2)).pair ((primrec_appCode.comp ((primrec_shiftCode.comp (.const 1) Primrec.id).comp (primrec_ruleField.comp Primrec.id (.const 3))) (primrec_varCode.comp (Primrec.const 0))).pair (primrec_appCode.comp ((primrec_shiftCode.comp (.const 1) Primrec.id).comp (primrec_ruleField.comp Primrec.id (.const 4))) (primrec_varCode.comp (Primrec.const 0))))))) (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_piCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_identityTyCode.comp ((primrec_ruleField.comp Primrec.id (.const 2)).pair ((primrec_appCode.comp ((primrec_shiftCode.comp (.const 1) Primrec.id).comp (primrec_ruleField.comp Primrec.id (.const 3))) (primrec_varCode.comp (Primrec.const 0))).pair (primrec_appCode.comp ((primrec_shiftCode.comp (.const 1) Primrec.id).comp (primrec_ruleField.comp Primrec.id (.const 4))) (primrec_varCode.comp (Primrec.const 0)))))))) (Primrec.list_cons.comp ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 5)).pair (primrec_piCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_identityTyCode.comp ((primrec_ruleField.comp Primrec.id (.const 2)).pair ((primrec_appCode.comp ((primrec_shiftCode.comp (.const 1) Primrec.id).comp (primrec_ruleField.comp Primrec.id (.const 3))) (primrec_varCode.comp (Primrec.const 0))).pair (primrec_appCode.comp ((primrec_shiftCode.comp (.const 1) Primrec.id).comp (primrec_ruleField.comp Primrec.id (.const 4))) (primrec_varCode.comp (Primrec.const 0)))))))))) (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_identityTyCode.comp ((primrec_piCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2))).pair ((primrec_ruleField.comp Primrec.id (.const 3)).pair (primrec_ruleField.comp Primrec.id (.const 4)))))) (Primrec.const ([] : List Nat)))))))))))
  exact h.of_eq (by intro c; simp only [premises_HasE_piExt,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasE_piExt_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (h : P01D.Poly) : premises_HasE_piExt (encode (Rule.HasE_piExt Γ A B p q h)) = ((Rule.HasE_piExt Γ A B p q h).premises).map encode := by
  simp only [premises_HasE_piExt,Rule.premises,encode_Rule_HasE_piExt,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premises_HasE_allExt (c : Nat) : List Nat := [(formCode 4 ((twkTelCode (ruleField c 0))) (ruleField c 1)), (formCode 4 (ruleField c 0) ((allTyCode (ruleField c 1)))), (hasCode 5 (ruleField c 0) (ruleField c 2) ((allTyCode (ruleField c 1)))), (hasCode 5 (ruleField c 0) (ruleField c 3) ((allTyCode (ruleField c 1)))), (formCode 4 ((twkTelCode (ruleField c 0))) ((identityTyCode (ruleField c 1) (ruleField c 2) (ruleField c 3)))), (hasCode 5 ((twkTelCode (ruleField c 0))) (ruleField c 4) ((identityTyCode (ruleField c 1) (ruleField c 2) (ruleField c 3)))), (formCode 4 (ruleField c 0) ((identityTyCode ((allTyCode (ruleField c 1))) (ruleField c 2) (ruleField c 3))))]
theorem primrec_premises_HasE_allExt : Primrec premises_HasE_allExt := by
  have h := (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_twkTelCode.comp (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_ruleField.comp Primrec.id (.const 1))) (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_allTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1)))) (Primrec.list_cons.comp ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_allTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1)))))) (Primrec.list_cons.comp ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 3)).pair (primrec_allTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1)))))) (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_twkTelCode.comp (primrec_ruleField.comp Primrec.id (.const 0))) (primrec_identityTyCode.comp ((primrec_ruleField.comp Primrec.id (.const 1)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 3)))))) (Primrec.list_cons.comp ((primrec_hasCode 5).comp ((primrec_twkTelCode.comp (primrec_ruleField.comp Primrec.id (.const 0))).pair ((primrec_ruleField.comp Primrec.id (.const 4)).pair (primrec_identityTyCode.comp ((primrec_ruleField.comp Primrec.id (.const 1)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 3)))))))) (Primrec.list_cons.comp ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_identityTyCode.comp ((primrec_allTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1))).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 3)))))) (Primrec.const ([] : List Nat)))))))))
  exact h.of_eq (by intro c; simp only [premises_HasE_allExt,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem premises_HasE_allExt_exact (Γ : P01AC.Tel) (B : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (h : P01D.Poly) : premises_HasE_allExt (encode (Rule.HasE_allExt Γ B p q h)) = ((Rule.HasE_allExt Γ B p q h).premises).map encode := by
  simp only [premises_HasE_allExt,Rule.premises,encode_Rule_HasE_allExt,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def premisesDispatch62 (c : Nat) : List Nat := if tag c = 62 then premises_HasE_allExt c else []
theorem primrec_premisesDispatch62 : Primrec premisesDispatch62 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 62)) primrec_premises_HasE_allExt (.const [])

def premisesDispatch61 (c : Nat) : List Nat := if tag c = 61 then premises_HasE_piExt c else premisesDispatch62 c
theorem primrec_premisesDispatch61 : Primrec premisesDispatch61 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 61)) primrec_premises_HasE_piExt primrec_premisesDispatch62

def premisesDispatch60 (c : Nat) : List Nat := if tag c = 60 then premises_HasE_conv c else premisesDispatch61 c
theorem primrec_premisesDispatch60 : Primrec premisesDispatch60 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 60)) primrec_premises_HasE_conv primrec_premisesDispatch61

def premisesDispatch59 (c : Nat) : List Nat := if tag c = 59 then premises_HasE_j c else premisesDispatch60 c
theorem primrec_premisesDispatch59 : Primrec premisesDispatch59 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 59)) primrec_premises_HasE_j primrec_premisesDispatch60

def premisesDispatch58 (c : Nat) : List Nat := if tag c = 58 then premises_HasE_proofErase c else premisesDispatch59 c
theorem primrec_premisesDispatch58 : Primrec premisesDispatch58 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 58)) primrec_premises_HasE_proofErase primrec_premisesDispatch59

def premisesDispatch57 (c : Nat) : List Nat := if tag c = 57 then premises_HasE_identityIntro c else premisesDispatch58 c
theorem primrec_premisesDispatch57 : Primrec premisesDispatch57 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 57)) primrec_premises_HasE_identityIntro primrec_premisesDispatch58

def premisesDispatch56 (c : Nat) : List Nat := if tag c = 56 then premises_HasE_sigmaSnd c else premisesDispatch57 c
theorem primrec_premisesDispatch56 : Primrec premisesDispatch56 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 56)) primrec_premises_HasE_sigmaSnd primrec_premisesDispatch57

def premisesDispatch55 (c : Nat) : List Nat := if tag c = 55 then premises_HasE_sigmaFst c else premisesDispatch56 c
theorem primrec_premisesDispatch55 : Primrec premisesDispatch55 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 55)) primrec_premises_HasE_sigmaFst primrec_premisesDispatch56

def premisesDispatch54 (c : Nat) : List Nat := if tag c = 54 then premises_HasE_sigmaIntro c else premisesDispatch55 c
theorem primrec_premisesDispatch54 : Primrec premisesDispatch54 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 54)) primrec_premises_HasE_sigmaIntro primrec_premisesDispatch55

def premisesDispatch53 (c : Nat) : List Nat := if tag c = 53 then premises_HasE_piElim c else premisesDispatch54 c
theorem primrec_premisesDispatch53 : Primrec premisesDispatch53 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 53)) primrec_premises_HasE_piElim primrec_premisesDispatch54

def premisesDispatch52 (c : Nat) : List Nat := if tag c = 52 then premises_HasE_piIntro c else premisesDispatch53 c
theorem primrec_premisesDispatch52 : Primrec premisesDispatch52 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 52)) primrec_premises_HasE_piIntro primrec_premisesDispatch53

def premisesDispatch51 (c : Nat) : List Nat := if tag c = 51 then premises_HasE_rawApp c else premisesDispatch52 c
theorem primrec_premisesDispatch51 : Primrec premisesDispatch51 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 51)) primrec_premises_HasE_rawApp primrec_premisesDispatch52

def premisesDispatch50 (c : Nat) : List Nat := if tag c = 50 then premises_HasE_rawAtom c else premisesDispatch51 c
theorem primrec_premisesDispatch50 : Primrec premisesDispatch50 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 50)) primrec_premises_HasE_rawAtom primrec_premisesDispatch51

def premisesDispatch49 (c : Nat) : List Nat := if tag c = 49 then premises_HasE_allElim c else premisesDispatch50 c
theorem primrec_premisesDispatch49 : Primrec premisesDispatch49 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 49)) primrec_premises_HasE_allElim primrec_premisesDispatch50

def premisesDispatch48 (c : Nat) : List Nat := if tag c = 48 then premises_HasE_allIntro c else premisesDispatch49 c
theorem primrec_premisesDispatch48 : Primrec premisesDispatch48 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 48)) primrec_premises_HasE_allIntro primrec_premisesDispatch49

def premisesDispatch47 (c : Nat) : List Nat := if tag c = 47 then premises_HasE_finite c else premisesDispatch48 c
theorem primrec_premisesDispatch47 : Primrec premisesDispatch47 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 47)) primrec_premises_HasE_finite primrec_premisesDispatch48

def premisesDispatch46 (c : Nat) : List Nat := if tag c = 46 then premises_HasE_s c else premisesDispatch47 c
theorem primrec_premisesDispatch46 : Primrec premisesDispatch46 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 46)) primrec_premises_HasE_s primrec_premisesDispatch47

def premisesDispatch45 (c : Nat) : List Nat := if tag c = 45 then premises_HasE_k c else premisesDispatch46 c
theorem primrec_premisesDispatch45 : Primrec premisesDispatch45 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 45)) primrec_premises_HasE_k primrec_premisesDispatch46

def premisesDispatch44 (c : Nat) : List Nat := if tag c = 44 then premises_HasE_i c else premisesDispatch45 c
theorem primrec_premisesDispatch44 : Primrec premisesDispatch44 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 44)) primrec_premises_HasE_i primrec_premisesDispatch45

def premisesDispatch43 (c : Nat) : List Nat := if tag c = 43 then premises_HasE_var c else premisesDispatch44 c
theorem primrec_premisesDispatch43 : Primrec premisesDispatch43 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 43)) primrec_premises_HasE_var primrec_premisesDispatch44

def premisesDispatch42 (c : Nat) : List Nat := if tag c = 42 then premises_FormE_identity c else premisesDispatch43 c
theorem primrec_premisesDispatch42 : Primrec premisesDispatch42 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 42)) primrec_premises_FormE_identity primrec_premisesDispatch43

def premisesDispatch41 (c : Nat) : List Nat := if tag c = 41 then premises_FormE_sigma c else premisesDispatch42 c
theorem primrec_premisesDispatch41 : Primrec premisesDispatch41 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 41)) primrec_premises_FormE_sigma primrec_premisesDispatch42

def premisesDispatch40 (c : Nat) : List Nat := if tag c = 40 then premises_FormE_pi c else premisesDispatch41 c
theorem primrec_premisesDispatch40 : Primrec premisesDispatch40 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 40)) primrec_premises_FormE_pi primrec_premisesDispatch41

def premisesDispatch39 (c : Nat) : List Nat := if tag c = 39 then premises_FormE_raw c else premisesDispatch40 c
theorem primrec_premisesDispatch39 : Primrec premisesDispatch39 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 39)) primrec_premises_FormE_raw primrec_premisesDispatch40

def premisesDispatch38 (c : Nat) : List Nat := if tag c = 38 then premises_FormE_all c else premisesDispatch39 c
theorem primrec_premisesDispatch38 : Primrec premisesDispatch38 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 38)) primrec_premises_FormE_all primrec_premisesDispatch39

def premisesDispatch37 (c : Nat) : List Nat := if tag c = 37 then premises_FormE_bottom c else premisesDispatch38 c
theorem primrec_premisesDispatch37 : Primrec premisesDispatch37 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 37)) primrec_premises_FormE_bottom primrec_premisesDispatch38

def premisesDispatch36 (c : Nat) : List Nat := if tag c = 36 then premises_FormE_param c else premisesDispatch37 c
theorem primrec_premisesDispatch36 : Primrec premisesDispatch36 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 36)) primrec_premises_FormE_param primrec_premisesDispatch37

def premisesDispatch35 (c : Nat) : List Nat := if tag c = 35 then premises_CtxE_ext c else premisesDispatch36 c
theorem primrec_premisesDispatch35 : Primrec premisesDispatch35 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 35)) primrec_premises_CtxE_ext primrec_premisesDispatch36

def premisesDispatch34 (c : Nat) : List Nat := if tag c = 34 then premises_CtxE_nil c else premisesDispatch35 c
theorem primrec_premisesDispatch34 : Primrec premisesDispatch34 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 34)) primrec_premises_CtxE_nil primrec_premisesDispatch35

def premisesDispatch33 (c : Nat) : List Nat := if tag c = 33 then premises_HasJ_natInduction c else premisesDispatch34 c
theorem primrec_premisesDispatch33 : Primrec premisesDispatch33 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 33)) primrec_premises_HasJ_natInduction primrec_premisesDispatch34

def premisesDispatch32 (c : Nat) : List Nat := if tag c = 32 then premises_HasJ_sigmaElim c else premisesDispatch33 c
theorem primrec_premisesDispatch32 : Primrec premisesDispatch32 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 32)) primrec_premises_HasJ_sigmaElim primrec_premisesDispatch33

def premisesDispatch31 (c : Nat) : List Nat := if tag c = 31 then premises_HasJ_allExt c else premisesDispatch32 c
theorem primrec_premisesDispatch31 : Primrec premisesDispatch31 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 31)) primrec_premises_HasJ_allExt primrec_premisesDispatch32

def premisesDispatch30 (c : Nat) : List Nat := if tag c = 30 then premises_HasJ_piExt c else premisesDispatch31 c
theorem primrec_premisesDispatch30 : Primrec premisesDispatch30 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 30)) primrec_premises_HasJ_piExt primrec_premisesDispatch31

def premisesDispatch29 (c : Nat) : List Nat := if tag c = 29 then premises_HasJ_conv c else premisesDispatch30 c
theorem primrec_premisesDispatch29 : Primrec premisesDispatch29 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 29)) primrec_premises_HasJ_conv primrec_premisesDispatch30

def premisesDispatch28 (c : Nat) : List Nat := if tag c = 28 then premises_HasJ_j c else premisesDispatch29 c
theorem primrec_premisesDispatch28 : Primrec premisesDispatch28 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 28)) primrec_premises_HasJ_j primrec_premisesDispatch29

def premisesDispatch27 (c : Nat) : List Nat := if tag c = 27 then premises_HasJ_proofErase c else premisesDispatch28 c
theorem primrec_premisesDispatch27 : Primrec premisesDispatch27 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 27)) primrec_premises_HasJ_proofErase primrec_premisesDispatch28

def premisesDispatch26 (c : Nat) : List Nat := if tag c = 26 then premises_HasJ_identityIntro c else premisesDispatch27 c
theorem primrec_premisesDispatch26 : Primrec premisesDispatch26 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 26)) primrec_premises_HasJ_identityIntro primrec_premisesDispatch27

def premisesDispatch25 (c : Nat) : List Nat := if tag c = 25 then premises_HasJ_sigmaSnd c else premisesDispatch26 c
theorem primrec_premisesDispatch25 : Primrec premisesDispatch25 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 25)) primrec_premises_HasJ_sigmaSnd primrec_premisesDispatch26

def premisesDispatch24 (c : Nat) : List Nat := if tag c = 24 then premises_HasJ_sigmaFst c else premisesDispatch25 c
theorem primrec_premisesDispatch24 : Primrec premisesDispatch24 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 24)) primrec_premises_HasJ_sigmaFst primrec_premisesDispatch25

def premisesDispatch23 (c : Nat) : List Nat := if tag c = 23 then premises_HasJ_sigmaIntro c else premisesDispatch24 c
theorem primrec_premisesDispatch23 : Primrec premisesDispatch23 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 23)) primrec_premises_HasJ_sigmaIntro primrec_premisesDispatch24

def premisesDispatch22 (c : Nat) : List Nat := if tag c = 22 then premises_HasJ_piElim c else premisesDispatch23 c
theorem primrec_premisesDispatch22 : Primrec premisesDispatch22 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 22)) primrec_premises_HasJ_piElim primrec_premisesDispatch23

def premisesDispatch21 (c : Nat) : List Nat := if tag c = 21 then premises_HasJ_piIntro c else premisesDispatch22 c
theorem primrec_premisesDispatch21 : Primrec premisesDispatch21 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 21)) primrec_premises_HasJ_piIntro primrec_premisesDispatch22

def premisesDispatch20 (c : Nat) : List Nat := if tag c = 20 then premises_HasJ_rawApp c else premisesDispatch21 c
theorem primrec_premisesDispatch20 : Primrec premisesDispatch20 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 20)) primrec_premises_HasJ_rawApp primrec_premisesDispatch21

def premisesDispatch19 (c : Nat) : List Nat := if tag c = 19 then premises_HasJ_rawAtom c else premisesDispatch20 c
theorem primrec_premisesDispatch19 : Primrec premisesDispatch19 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 19)) primrec_premises_HasJ_rawAtom primrec_premisesDispatch20

def premisesDispatch18 (c : Nat) : List Nat := if tag c = 18 then premises_HasJ_allElim c else premisesDispatch19 c
theorem primrec_premisesDispatch18 : Primrec premisesDispatch18 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 18)) primrec_premises_HasJ_allElim primrec_premisesDispatch19

def premisesDispatch17 (c : Nat) : List Nat := if tag c = 17 then premises_HasJ_allIntro c else premisesDispatch18 c
theorem primrec_premisesDispatch17 : Primrec premisesDispatch17 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 17)) primrec_premises_HasJ_allIntro primrec_premisesDispatch18

def premisesDispatch16 (c : Nat) : List Nat := if tag c = 16 then premises_HasJ_finite c else premisesDispatch17 c
theorem primrec_premisesDispatch16 : Primrec premisesDispatch16 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 16)) primrec_premises_HasJ_finite primrec_premisesDispatch17

def premisesDispatch15 (c : Nat) : List Nat := if tag c = 15 then premises_HasJ_s c else premisesDispatch16 c
theorem primrec_premisesDispatch15 : Primrec premisesDispatch15 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 15)) primrec_premises_HasJ_s primrec_premisesDispatch16

def premisesDispatch14 (c : Nat) : List Nat := if tag c = 14 then premises_HasJ_k c else premisesDispatch15 c
theorem primrec_premisesDispatch14 : Primrec premisesDispatch14 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 14)) primrec_premises_HasJ_k primrec_premisesDispatch15

def premisesDispatch13 (c : Nat) : List Nat := if tag c = 13 then premises_HasJ_i c else premisesDispatch14 c
theorem primrec_premisesDispatch13 : Primrec premisesDispatch13 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 13)) primrec_premises_HasJ_i primrec_premisesDispatch14

def premisesDispatch12 (c : Nat) : List Nat := if tag c = 12 then premises_HasJ_var c else premisesDispatch13 c
theorem primrec_premisesDispatch12 : Primrec premisesDispatch12 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 12)) primrec_premises_HasJ_var primrec_premisesDispatch13

def premisesDispatch11 (c : Nat) : List Nat := if tag c = 11 then premises_HasJ_hasBase c else premisesDispatch12 c
theorem primrec_premisesDispatch11 : Primrec premisesDispatch11 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 11)) primrec_premises_HasJ_hasBase primrec_premisesDispatch12

def premisesDispatch10 (c : Nat) : List Nat := if tag c = 10 then premises_FormJ_identity c else premisesDispatch11 c
theorem primrec_premisesDispatch10 : Primrec premisesDispatch10 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 10)) primrec_premises_FormJ_identity primrec_premisesDispatch11

def premisesDispatch9 (c : Nat) : List Nat := if tag c = 9 then premises_FormJ_sigma c else premisesDispatch10 c
theorem primrec_premisesDispatch9 : Primrec premisesDispatch9 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 9)) primrec_premises_FormJ_sigma primrec_premisesDispatch10

def premisesDispatch8 (c : Nat) : List Nat := if tag c = 8 then premises_FormJ_pi c else premisesDispatch9 c
theorem primrec_premisesDispatch8 : Primrec premisesDispatch8 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 8)) primrec_premises_FormJ_pi primrec_premisesDispatch9

def premisesDispatch7 (c : Nat) : List Nat := if tag c = 7 then premises_FormJ_raw c else premisesDispatch8 c
theorem primrec_premisesDispatch7 : Primrec premisesDispatch7 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 7)) primrec_premises_FormJ_raw primrec_premisesDispatch8

def premisesDispatch6 (c : Nat) : List Nat := if tag c = 6 then premises_FormJ_all c else premisesDispatch7 c
theorem primrec_premisesDispatch6 : Primrec premisesDispatch6 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 6)) primrec_premises_FormJ_all primrec_premisesDispatch7

def premisesDispatch5 (c : Nat) : List Nat := if tag c = 5 then premises_FormJ_bottom c else premisesDispatch6 c
theorem primrec_premisesDispatch5 : Primrec premisesDispatch5 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 5)) primrec_premises_FormJ_bottom primrec_premisesDispatch6

def premisesDispatch4 (c : Nat) : List Nat := if tag c = 4 then premises_FormJ_param c else premisesDispatch5 c
theorem primrec_premisesDispatch4 : Primrec premisesDispatch4 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 4)) primrec_premises_FormJ_param primrec_premisesDispatch5

def premisesDispatch3 (c : Nat) : List Nat := if tag c = 3 then premises_FormJ_formBase c else premisesDispatch4 c
theorem primrec_premisesDispatch3 : Primrec premisesDispatch3 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 3)) primrec_premises_FormJ_formBase primrec_premisesDispatch4

def premisesDispatch2 (c : Nat) : List Nat := if tag c = 2 then premises_CtxJ_ext c else premisesDispatch3 c
theorem primrec_premisesDispatch2 : Primrec premisesDispatch2 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 2)) primrec_premises_CtxJ_ext primrec_premisesDispatch3

def premisesDispatch1 (c : Nat) : List Nat := if tag c = 1 then premises_CtxJ_nil c else premisesDispatch2 c
theorem primrec_premisesDispatch1 : Primrec premisesDispatch1 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 1)) primrec_premises_CtxJ_nil primrec_premisesDispatch2

def premisesDispatch0 (c : Nat) : List Nat := if tag c = 0 then premises_CtxJ_ctxBase c else premisesDispatch1 c
theorem primrec_premisesDispatch0 : Primrec premisesDispatch0 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 0)) primrec_premises_CtxJ_ctxBase primrec_premisesDispatch1

def premisesCode := premisesDispatch0
theorem primrec_premisesCode : Primrec premisesCode := primrec_premisesDispatch0
@[simp] theorem premisesCode_CtxJ_ctxBase (Γ : P01AC.Tel) : premisesCode (encode (Rule.CtxJ_ctxBase Γ)) = premises_CtxJ_ctxBase (encode (Rule.CtxJ_ctxBase Γ)) := by
  have ht : tag (encode (Rule.CtxJ_ctxBase Γ)) = 0 := by rw [encode_Rule_CtxJ_ctxBase]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_CtxJ_nil  : premisesCode (encode (Rule.CtxJ_nil )) = premises_CtxJ_nil (encode (Rule.CtxJ_nil )) := by
  have ht : tag (encode (Rule.CtxJ_nil )) = 1 := by rw [encode_Rule_CtxJ_nil]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_CtxJ_ext (Γ : P01AC.Tel) (A : P01AC.Ty) : premisesCode (encode (Rule.CtxJ_ext Γ A)) = premises_CtxJ_ext (encode (Rule.CtxJ_ext Γ A)) := by
  have ht : tag (encode (Rule.CtxJ_ext Γ A)) = 2 := by rw [encode_Rule_CtxJ_ext]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_FormJ_formBase (Γ : P01AC.Tel) (A : P01AC.Ty) : premisesCode (encode (Rule.FormJ_formBase Γ A)) = premises_FormJ_formBase (encode (Rule.FormJ_formBase Γ A)) := by
  have ht : tag (encode (Rule.FormJ_formBase Γ A)) = 3 := by rw [encode_Rule_FormJ_formBase]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_FormJ_param (Γ : P01AC.Tel) (n : Nat) : premisesCode (encode (Rule.FormJ_param Γ n)) = premises_FormJ_param (encode (Rule.FormJ_param Γ n)) := by
  have ht : tag (encode (Rule.FormJ_param Γ n)) = 4 := by rw [encode_Rule_FormJ_param]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_FormJ_bottom (Γ : P01AC.Tel) : premisesCode (encode (Rule.FormJ_bottom Γ)) = premises_FormJ_bottom (encode (Rule.FormJ_bottom Γ)) := by
  have ht : tag (encode (Rule.FormJ_bottom Γ)) = 5 := by rw [encode_Rule_FormJ_bottom]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_FormJ_all (Γ : P01AC.Tel) (B : P01AC.Ty) : premisesCode (encode (Rule.FormJ_all Γ B)) = premises_FormJ_all (encode (Rule.FormJ_all Γ B)) := by
  have ht : tag (encode (Rule.FormJ_all Γ B)) = 6 := by rw [encode_Rule_FormJ_all]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_FormJ_raw (Γ : P01AC.Tel) : premisesCode (encode (Rule.FormJ_raw Γ)) = premises_FormJ_raw (encode (Rule.FormJ_raw Γ)) := by
  have ht : tag (encode (Rule.FormJ_raw Γ)) = 7 := by rw [encode_Rule_FormJ_raw]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_FormJ_pi (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : premisesCode (encode (Rule.FormJ_pi Γ A B)) = premises_FormJ_pi (encode (Rule.FormJ_pi Γ A B)) := by
  have ht : tag (encode (Rule.FormJ_pi Γ A B)) = 8 := by rw [encode_Rule_FormJ_pi]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_FormJ_sigma (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : premisesCode (encode (Rule.FormJ_sigma Γ A B)) = premises_FormJ_sigma (encode (Rule.FormJ_sigma Γ A B)) := by
  have ht : tag (encode (Rule.FormJ_sigma Γ A B)) = 9 := by rw [encode_Rule_FormJ_sigma]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_FormJ_identity (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) : premisesCode (encode (Rule.FormJ_identity Γ A p q)) = premises_FormJ_identity (encode (Rule.FormJ_identity Γ A p q)) := by
  have ht : tag (encode (Rule.FormJ_identity Γ A p q)) = 10 := by rw [encode_Rule_FormJ_identity]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasJ_hasBase (Γ : P01AC.Tel) (p : P01D.Poly) (A : P01AC.Ty) : premisesCode (encode (Rule.HasJ_hasBase Γ p A)) = premises_HasJ_hasBase (encode (Rule.HasJ_hasBase Γ p A)) := by
  have ht : tag (encode (Rule.HasJ_hasBase Γ p A)) = 11 := by rw [encode_Rule_HasJ_hasBase]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasJ_var (Γ : P01AC.Tel) (A : P01AC.Ty) (n : Nat) (aux0 : AuxiliaryCertificates.LookupCert) : premisesCode (encode (Rule.HasJ_var Γ A n aux0)) = premises_HasJ_var (encode (Rule.HasJ_var Γ A n aux0)) := by
  have ht : tag (encode (Rule.HasJ_var Γ A n aux0)) = 12 := by rw [encode_Rule_HasJ_var]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasJ_i (Γ : P01AC.Tel) (A : P01AC.Ty) : premisesCode (encode (Rule.HasJ_i Γ A)) = premises_HasJ_i (encode (Rule.HasJ_i Γ A)) := by
  have ht : tag (encode (Rule.HasJ_i Γ A)) = 13 := by rw [encode_Rule_HasJ_i]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasJ_k (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : premisesCode (encode (Rule.HasJ_k Γ A B)) = premises_HasJ_k (encode (Rule.HasJ_k Γ A B)) := by
  have ht : tag (encode (Rule.HasJ_k Γ A B)) = 14 := by rw [encode_Rule_HasJ_k]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasJ_s (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (C : P01AC.Ty) : premisesCode (encode (Rule.HasJ_s Γ A B C)) = premises_HasJ_s (encode (Rule.HasJ_s Γ A B C)) := by
  have ht : tag (encode (Rule.HasJ_s Γ A B C)) = 15 := by rw [encode_Rule_HasJ_s]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasJ_finite (C : OrthemologyV2.TypeCode) (Γ : P01AC.Tel) (t : OrthemologyV2.Term) (τ : List P01AC.Ty) (aux0 : AuxiliaryCertificates.FiniteCert) : premisesCode (encode (Rule.HasJ_finite C Γ t τ aux0)) = premises_HasJ_finite (encode (Rule.HasJ_finite C Γ t τ aux0)) := by
  have ht : tag (encode (Rule.HasJ_finite C Γ t τ aux0)) = 16 := by rw [encode_Rule_HasJ_finite]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasJ_allIntro (Γ : P01AC.Tel) (B : P01AC.Ty) (p : P01D.Poly) : premisesCode (encode (Rule.HasJ_allIntro Γ B p)) = premises_HasJ_allIntro (encode (Rule.HasJ_allIntro Γ B p)) := by
  have ht : tag (encode (Rule.HasJ_allIntro Γ B p)) = 17 := by rw [encode_Rule_HasJ_allIntro]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasJ_allElim (Γ : P01AC.Tel) (B : P01AC.Ty) (A : P01AC.Ty) (p : P01D.Poly) : premisesCode (encode (Rule.HasJ_allElim Γ B A p)) = premises_HasJ_allElim (encode (Rule.HasJ_allElim Γ B A p)) := by
  have ht : tag (encode (Rule.HasJ_allElim Γ B A p)) = 18 := by rw [encode_Rule_HasJ_allElim]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasJ_rawAtom (Γ : P01AC.Tel) (t : OrthemologyV2.Term) : premisesCode (encode (Rule.HasJ_rawAtom Γ t)) = premises_HasJ_rawAtom (encode (Rule.HasJ_rawAtom Γ t)) := by
  have ht : tag (encode (Rule.HasJ_rawAtom Γ t)) = 19 := by rw [encode_Rule_HasJ_rawAtom]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasJ_rawApp (Γ : P01AC.Tel) (f : P01D.Poly) (a : P01D.Poly) : premisesCode (encode (Rule.HasJ_rawApp Γ f a)) = premises_HasJ_rawApp (encode (Rule.HasJ_rawApp Γ f a)) := by
  have ht : tag (encode (Rule.HasJ_rawApp Γ f a)) = 20 := by rw [encode_Rule_HasJ_rawApp]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasJ_piIntro (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (b : P01D.Poly) : premisesCode (encode (Rule.HasJ_piIntro Γ A B b)) = premises_HasJ_piIntro (encode (Rule.HasJ_piIntro Γ A B b)) := by
  have ht : tag (encode (Rule.HasJ_piIntro Γ A B b)) = 21 := by rw [encode_Rule_HasJ_piIntro]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasJ_piElim (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (a : P01D.Poly) (f : P01D.Poly) : premisesCode (encode (Rule.HasJ_piElim Γ A B a f)) = premises_HasJ_piElim (encode (Rule.HasJ_piElim Γ A B a f)) := by
  have ht : tag (encode (Rule.HasJ_piElim Γ A B a f)) = 22 := by rw [encode_Rule_HasJ_piElim]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasJ_sigmaIntro (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (a : P01D.Poly) (b : P01D.Poly) : premisesCode (encode (Rule.HasJ_sigmaIntro Γ A B a b)) = premises_HasJ_sigmaIntro (encode (Rule.HasJ_sigmaIntro Γ A B a b)) := by
  have ht : tag (encode (Rule.HasJ_sigmaIntro Γ A B a b)) = 23 := by rw [encode_Rule_HasJ_sigmaIntro]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasJ_sigmaFst (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (z : P01D.Poly) : premisesCode (encode (Rule.HasJ_sigmaFst Γ A B z)) = premises_HasJ_sigmaFst (encode (Rule.HasJ_sigmaFst Γ A B z)) := by
  have ht : tag (encode (Rule.HasJ_sigmaFst Γ A B z)) = 24 := by rw [encode_Rule_HasJ_sigmaFst]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasJ_sigmaSnd (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (z : P01D.Poly) : premisesCode (encode (Rule.HasJ_sigmaSnd Γ A B z)) = premises_HasJ_sigmaSnd (encode (Rule.HasJ_sigmaSnd Γ A B z)) := by
  have ht : tag (encode (Rule.HasJ_sigmaSnd Γ A B z)) = 25 := by rw [encode_Rule_HasJ_sigmaSnd]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasJ_identityIntro (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (aux0 : AuxiliaryCertificates.PolyCert) : premisesCode (encode (Rule.HasJ_identityIntro Γ A p q aux0)) = premises_HasJ_identityIntro (encode (Rule.HasJ_identityIntro Γ A p q aux0)) := by
  have ht : tag (encode (Rule.HasJ_identityIntro Γ A p q aux0)) = 26 := by rw [encode_Rule_HasJ_identityIntro]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasJ_proofErase (Γ : P01AC.Tel) (A : P01AC.Ty) (x : P01D.Poly) (y : P01D.Poly) (p : P01D.Poly) : premisesCode (encode (Rule.HasJ_proofErase Γ A x y p)) = premises_HasJ_proofErase (encode (Rule.HasJ_proofErase Γ A x y p)) := by
  have ht : tag (encode (Rule.HasJ_proofErase Γ A x y p)) = 27 := by rw [encode_Rule_HasJ_proofErase]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasJ_j (Γ : P01AC.Tel) (A : P01AC.Ty) (x : P01D.Poly) (B : P01AC.Ty) (y : P01D.Poly) (e : P01D.Poly) (d : P01D.Poly) : premisesCode (encode (Rule.HasJ_j Γ A x B y e d)) = premises_HasJ_j (encode (Rule.HasJ_j Γ A x B y e d)) := by
  have ht : tag (encode (Rule.HasJ_j Γ A x B y e d)) = 28 := by rw [encode_Rule_HasJ_j]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasJ_conv (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (aux0 : AuxiliaryCertificates.PolyCert) : premisesCode (encode (Rule.HasJ_conv Γ A p q aux0)) = premises_HasJ_conv (encode (Rule.HasJ_conv Γ A p q aux0)) := by
  have ht : tag (encode (Rule.HasJ_conv Γ A p q aux0)) = 29 := by rw [encode_Rule_HasJ_conv]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasJ_piExt (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (h : P01D.Poly) : premisesCode (encode (Rule.HasJ_piExt Γ A B p q h)) = premises_HasJ_piExt (encode (Rule.HasJ_piExt Γ A B p q h)) := by
  have ht : tag (encode (Rule.HasJ_piExt Γ A B p q h)) = 30 := by rw [encode_Rule_HasJ_piExt]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasJ_allExt (Γ : P01AC.Tel) (B : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (h : P01D.Poly) : premisesCode (encode (Rule.HasJ_allExt Γ B p q h)) = premises_HasJ_allExt (encode (Rule.HasJ_allExt Γ B p q h)) := by
  have ht : tag (encode (Rule.HasJ_allExt Γ B p q h)) = 31 := by rw [encode_Rule_HasJ_allExt]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasJ_sigmaElim (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (P : P01AC.Ty) (d : P01D.Poly) (z : P01D.Poly) : premisesCode (encode (Rule.HasJ_sigmaElim Γ A B P d z)) = premises_HasJ_sigmaElim (encode (Rule.HasJ_sigmaElim Γ A B P d z)) := by
  have ht : tag (encode (Rule.HasJ_sigmaElim Γ A B P d z)) = 32 := by rw [encode_Rule_HasJ_sigmaElim]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasJ_natInduction (Γ : P01AC.Tel) (P : P01AC.Ty) (p : P01D.Poly) (s : P01D.Poly) : premisesCode (encode (Rule.HasJ_natInduction Γ P p s)) = premises_HasJ_natInduction (encode (Rule.HasJ_natInduction Γ P p s)) := by
  have ht : tag (encode (Rule.HasJ_natInduction Γ P p s)) = 33 := by rw [encode_Rule_HasJ_natInduction]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, premisesDispatch33, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_CtxE_nil  : premisesCode (encode (Rule.CtxE_nil )) = premises_CtxE_nil (encode (Rule.CtxE_nil )) := by
  have ht : tag (encode (Rule.CtxE_nil )) = 34 := by rw [encode_Rule_CtxE_nil]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, premisesDispatch33, premisesDispatch34, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_CtxE_ext (Γ : P01AC.Tel) (A : P01AC.Ty) : premisesCode (encode (Rule.CtxE_ext Γ A)) = premises_CtxE_ext (encode (Rule.CtxE_ext Γ A)) := by
  have ht : tag (encode (Rule.CtxE_ext Γ A)) = 35 := by rw [encode_Rule_CtxE_ext]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, premisesDispatch33, premisesDispatch34, premisesDispatch35, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_FormE_param (Γ : P01AC.Tel) (n : Nat) : premisesCode (encode (Rule.FormE_param Γ n)) = premises_FormE_param (encode (Rule.FormE_param Γ n)) := by
  have ht : tag (encode (Rule.FormE_param Γ n)) = 36 := by rw [encode_Rule_FormE_param]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, premisesDispatch33, premisesDispatch34, premisesDispatch35, premisesDispatch36, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_FormE_bottom (Γ : P01AC.Tel) : premisesCode (encode (Rule.FormE_bottom Γ)) = premises_FormE_bottom (encode (Rule.FormE_bottom Γ)) := by
  have ht : tag (encode (Rule.FormE_bottom Γ)) = 37 := by rw [encode_Rule_FormE_bottom]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, premisesDispatch33, premisesDispatch34, premisesDispatch35, premisesDispatch36, premisesDispatch37, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_FormE_all (Γ : P01AC.Tel) (B : P01AC.Ty) : premisesCode (encode (Rule.FormE_all Γ B)) = premises_FormE_all (encode (Rule.FormE_all Γ B)) := by
  have ht : tag (encode (Rule.FormE_all Γ B)) = 38 := by rw [encode_Rule_FormE_all]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, premisesDispatch33, premisesDispatch34, premisesDispatch35, premisesDispatch36, premisesDispatch37, premisesDispatch38, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_FormE_raw (Γ : P01AC.Tel) : premisesCode (encode (Rule.FormE_raw Γ)) = premises_FormE_raw (encode (Rule.FormE_raw Γ)) := by
  have ht : tag (encode (Rule.FormE_raw Γ)) = 39 := by rw [encode_Rule_FormE_raw]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, premisesDispatch33, premisesDispatch34, premisesDispatch35, premisesDispatch36, premisesDispatch37, premisesDispatch38, premisesDispatch39, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_FormE_pi (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : premisesCode (encode (Rule.FormE_pi Γ A B)) = premises_FormE_pi (encode (Rule.FormE_pi Γ A B)) := by
  have ht : tag (encode (Rule.FormE_pi Γ A B)) = 40 := by rw [encode_Rule_FormE_pi]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, premisesDispatch33, premisesDispatch34, premisesDispatch35, premisesDispatch36, premisesDispatch37, premisesDispatch38, premisesDispatch39, premisesDispatch40, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_FormE_sigma (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : premisesCode (encode (Rule.FormE_sigma Γ A B)) = premises_FormE_sigma (encode (Rule.FormE_sigma Γ A B)) := by
  have ht : tag (encode (Rule.FormE_sigma Γ A B)) = 41 := by rw [encode_Rule_FormE_sigma]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, premisesDispatch33, premisesDispatch34, premisesDispatch35, premisesDispatch36, premisesDispatch37, premisesDispatch38, premisesDispatch39, premisesDispatch40, premisesDispatch41, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_FormE_identity (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) : premisesCode (encode (Rule.FormE_identity Γ A p q)) = premises_FormE_identity (encode (Rule.FormE_identity Γ A p q)) := by
  have ht : tag (encode (Rule.FormE_identity Γ A p q)) = 42 := by rw [encode_Rule_FormE_identity]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, premisesDispatch33, premisesDispatch34, premisesDispatch35, premisesDispatch36, premisesDispatch37, premisesDispatch38, premisesDispatch39, premisesDispatch40, premisesDispatch41, premisesDispatch42, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasE_var (Γ : P01AC.Tel) (A : P01AC.Ty) (n : Nat) (aux0 : AuxiliaryCertificates.LookupCert) : premisesCode (encode (Rule.HasE_var Γ A n aux0)) = premises_HasE_var (encode (Rule.HasE_var Γ A n aux0)) := by
  have ht : tag (encode (Rule.HasE_var Γ A n aux0)) = 43 := by rw [encode_Rule_HasE_var]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, premisesDispatch33, premisesDispatch34, premisesDispatch35, premisesDispatch36, premisesDispatch37, premisesDispatch38, premisesDispatch39, premisesDispatch40, premisesDispatch41, premisesDispatch42, premisesDispatch43, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasE_i (Γ : P01AC.Tel) (A : P01AC.Ty) : premisesCode (encode (Rule.HasE_i Γ A)) = premises_HasE_i (encode (Rule.HasE_i Γ A)) := by
  have ht : tag (encode (Rule.HasE_i Γ A)) = 44 := by rw [encode_Rule_HasE_i]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, premisesDispatch33, premisesDispatch34, premisesDispatch35, premisesDispatch36, premisesDispatch37, premisesDispatch38, premisesDispatch39, premisesDispatch40, premisesDispatch41, premisesDispatch42, premisesDispatch43, premisesDispatch44, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasE_k (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : premisesCode (encode (Rule.HasE_k Γ A B)) = premises_HasE_k (encode (Rule.HasE_k Γ A B)) := by
  have ht : tag (encode (Rule.HasE_k Γ A B)) = 45 := by rw [encode_Rule_HasE_k]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, premisesDispatch33, premisesDispatch34, premisesDispatch35, premisesDispatch36, premisesDispatch37, premisesDispatch38, premisesDispatch39, premisesDispatch40, premisesDispatch41, premisesDispatch42, premisesDispatch43, premisesDispatch44, premisesDispatch45, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasE_s (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (C : P01AC.Ty) : premisesCode (encode (Rule.HasE_s Γ A B C)) = premises_HasE_s (encode (Rule.HasE_s Γ A B C)) := by
  have ht : tag (encode (Rule.HasE_s Γ A B C)) = 46 := by rw [encode_Rule_HasE_s]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, premisesDispatch33, premisesDispatch34, premisesDispatch35, premisesDispatch36, premisesDispatch37, premisesDispatch38, premisesDispatch39, premisesDispatch40, premisesDispatch41, premisesDispatch42, premisesDispatch43, premisesDispatch44, premisesDispatch45, premisesDispatch46, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasE_finite (C : OrthemologyV2.TypeCode) (Γ : P01AC.Tel) (t : OrthemologyV2.Term) (τ : List P01AC.Ty) (aux0 : AuxiliaryCertificates.FiniteCert) : premisesCode (encode (Rule.HasE_finite C Γ t τ aux0)) = premises_HasE_finite (encode (Rule.HasE_finite C Γ t τ aux0)) := by
  have ht : tag (encode (Rule.HasE_finite C Γ t τ aux0)) = 47 := by rw [encode_Rule_HasE_finite]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, premisesDispatch33, premisesDispatch34, premisesDispatch35, premisesDispatch36, premisesDispatch37, premisesDispatch38, premisesDispatch39, premisesDispatch40, premisesDispatch41, premisesDispatch42, premisesDispatch43, premisesDispatch44, premisesDispatch45, premisesDispatch46, premisesDispatch47, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasE_allIntro (Γ : P01AC.Tel) (B : P01AC.Ty) (p : P01D.Poly) : premisesCode (encode (Rule.HasE_allIntro Γ B p)) = premises_HasE_allIntro (encode (Rule.HasE_allIntro Γ B p)) := by
  have ht : tag (encode (Rule.HasE_allIntro Γ B p)) = 48 := by rw [encode_Rule_HasE_allIntro]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, premisesDispatch33, premisesDispatch34, premisesDispatch35, premisesDispatch36, premisesDispatch37, premisesDispatch38, premisesDispatch39, premisesDispatch40, premisesDispatch41, premisesDispatch42, premisesDispatch43, premisesDispatch44, premisesDispatch45, premisesDispatch46, premisesDispatch47, premisesDispatch48, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasE_allElim (Γ : P01AC.Tel) (B : P01AC.Ty) (A : P01AC.Ty) (p : P01D.Poly) : premisesCode (encode (Rule.HasE_allElim Γ B A p)) = premises_HasE_allElim (encode (Rule.HasE_allElim Γ B A p)) := by
  have ht : tag (encode (Rule.HasE_allElim Γ B A p)) = 49 := by rw [encode_Rule_HasE_allElim]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, premisesDispatch33, premisesDispatch34, premisesDispatch35, premisesDispatch36, premisesDispatch37, premisesDispatch38, premisesDispatch39, premisesDispatch40, premisesDispatch41, premisesDispatch42, premisesDispatch43, premisesDispatch44, premisesDispatch45, premisesDispatch46, premisesDispatch47, premisesDispatch48, premisesDispatch49, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasE_rawAtom (Γ : P01AC.Tel) (t : OrthemologyV2.Term) : premisesCode (encode (Rule.HasE_rawAtom Γ t)) = premises_HasE_rawAtom (encode (Rule.HasE_rawAtom Γ t)) := by
  have ht : tag (encode (Rule.HasE_rawAtom Γ t)) = 50 := by rw [encode_Rule_HasE_rawAtom]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, premisesDispatch33, premisesDispatch34, premisesDispatch35, premisesDispatch36, premisesDispatch37, premisesDispatch38, premisesDispatch39, premisesDispatch40, premisesDispatch41, premisesDispatch42, premisesDispatch43, premisesDispatch44, premisesDispatch45, premisesDispatch46, premisesDispatch47, premisesDispatch48, premisesDispatch49, premisesDispatch50, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasE_rawApp (Γ : P01AC.Tel) (f : P01D.Poly) (a : P01D.Poly) : premisesCode (encode (Rule.HasE_rawApp Γ f a)) = premises_HasE_rawApp (encode (Rule.HasE_rawApp Γ f a)) := by
  have ht : tag (encode (Rule.HasE_rawApp Γ f a)) = 51 := by rw [encode_Rule_HasE_rawApp]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, premisesDispatch33, premisesDispatch34, premisesDispatch35, premisesDispatch36, premisesDispatch37, premisesDispatch38, premisesDispatch39, premisesDispatch40, premisesDispatch41, premisesDispatch42, premisesDispatch43, premisesDispatch44, premisesDispatch45, premisesDispatch46, premisesDispatch47, premisesDispatch48, premisesDispatch49, premisesDispatch50, premisesDispatch51, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasE_piIntro (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (b : P01D.Poly) : premisesCode (encode (Rule.HasE_piIntro Γ A B b)) = premises_HasE_piIntro (encode (Rule.HasE_piIntro Γ A B b)) := by
  have ht : tag (encode (Rule.HasE_piIntro Γ A B b)) = 52 := by rw [encode_Rule_HasE_piIntro]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, premisesDispatch33, premisesDispatch34, premisesDispatch35, premisesDispatch36, premisesDispatch37, premisesDispatch38, premisesDispatch39, premisesDispatch40, premisesDispatch41, premisesDispatch42, premisesDispatch43, premisesDispatch44, premisesDispatch45, premisesDispatch46, premisesDispatch47, premisesDispatch48, premisesDispatch49, premisesDispatch50, premisesDispatch51, premisesDispatch52, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasE_piElim (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (a : P01D.Poly) (f : P01D.Poly) : premisesCode (encode (Rule.HasE_piElim Γ A B a f)) = premises_HasE_piElim (encode (Rule.HasE_piElim Γ A B a f)) := by
  have ht : tag (encode (Rule.HasE_piElim Γ A B a f)) = 53 := by rw [encode_Rule_HasE_piElim]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, premisesDispatch33, premisesDispatch34, premisesDispatch35, premisesDispatch36, premisesDispatch37, premisesDispatch38, premisesDispatch39, premisesDispatch40, premisesDispatch41, premisesDispatch42, premisesDispatch43, premisesDispatch44, premisesDispatch45, premisesDispatch46, premisesDispatch47, premisesDispatch48, premisesDispatch49, premisesDispatch50, premisesDispatch51, premisesDispatch52, premisesDispatch53, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasE_sigmaIntro (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (a : P01D.Poly) (b : P01D.Poly) : premisesCode (encode (Rule.HasE_sigmaIntro Γ A B a b)) = premises_HasE_sigmaIntro (encode (Rule.HasE_sigmaIntro Γ A B a b)) := by
  have ht : tag (encode (Rule.HasE_sigmaIntro Γ A B a b)) = 54 := by rw [encode_Rule_HasE_sigmaIntro]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, premisesDispatch33, premisesDispatch34, premisesDispatch35, premisesDispatch36, premisesDispatch37, premisesDispatch38, premisesDispatch39, premisesDispatch40, premisesDispatch41, premisesDispatch42, premisesDispatch43, premisesDispatch44, premisesDispatch45, premisesDispatch46, premisesDispatch47, premisesDispatch48, premisesDispatch49, premisesDispatch50, premisesDispatch51, premisesDispatch52, premisesDispatch53, premisesDispatch54, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasE_sigmaFst (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (z : P01D.Poly) : premisesCode (encode (Rule.HasE_sigmaFst Γ A B z)) = premises_HasE_sigmaFst (encode (Rule.HasE_sigmaFst Γ A B z)) := by
  have ht : tag (encode (Rule.HasE_sigmaFst Γ A B z)) = 55 := by rw [encode_Rule_HasE_sigmaFst]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, premisesDispatch33, premisesDispatch34, premisesDispatch35, premisesDispatch36, premisesDispatch37, premisesDispatch38, premisesDispatch39, premisesDispatch40, premisesDispatch41, premisesDispatch42, premisesDispatch43, premisesDispatch44, premisesDispatch45, premisesDispatch46, premisesDispatch47, premisesDispatch48, premisesDispatch49, premisesDispatch50, premisesDispatch51, premisesDispatch52, premisesDispatch53, premisesDispatch54, premisesDispatch55, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasE_sigmaSnd (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (z : P01D.Poly) : premisesCode (encode (Rule.HasE_sigmaSnd Γ A B z)) = premises_HasE_sigmaSnd (encode (Rule.HasE_sigmaSnd Γ A B z)) := by
  have ht : tag (encode (Rule.HasE_sigmaSnd Γ A B z)) = 56 := by rw [encode_Rule_HasE_sigmaSnd]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, premisesDispatch33, premisesDispatch34, premisesDispatch35, premisesDispatch36, premisesDispatch37, premisesDispatch38, premisesDispatch39, premisesDispatch40, premisesDispatch41, premisesDispatch42, premisesDispatch43, premisesDispatch44, premisesDispatch45, premisesDispatch46, premisesDispatch47, premisesDispatch48, premisesDispatch49, premisesDispatch50, premisesDispatch51, premisesDispatch52, premisesDispatch53, premisesDispatch54, premisesDispatch55, premisesDispatch56, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasE_identityIntro (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (aux0 : AuxiliaryCertificates.PolyCert) : premisesCode (encode (Rule.HasE_identityIntro Γ A p q aux0)) = premises_HasE_identityIntro (encode (Rule.HasE_identityIntro Γ A p q aux0)) := by
  have ht : tag (encode (Rule.HasE_identityIntro Γ A p q aux0)) = 57 := by rw [encode_Rule_HasE_identityIntro]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, premisesDispatch33, premisesDispatch34, premisesDispatch35, premisesDispatch36, premisesDispatch37, premisesDispatch38, premisesDispatch39, premisesDispatch40, premisesDispatch41, premisesDispatch42, premisesDispatch43, premisesDispatch44, premisesDispatch45, premisesDispatch46, premisesDispatch47, premisesDispatch48, premisesDispatch49, premisesDispatch50, premisesDispatch51, premisesDispatch52, premisesDispatch53, premisesDispatch54, premisesDispatch55, premisesDispatch56, premisesDispatch57, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasE_proofErase (Γ : P01AC.Tel) (A : P01AC.Ty) (x : P01D.Poly) (y : P01D.Poly) (p : P01D.Poly) : premisesCode (encode (Rule.HasE_proofErase Γ A x y p)) = premises_HasE_proofErase (encode (Rule.HasE_proofErase Γ A x y p)) := by
  have ht : tag (encode (Rule.HasE_proofErase Γ A x y p)) = 58 := by rw [encode_Rule_HasE_proofErase]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, premisesDispatch33, premisesDispatch34, premisesDispatch35, premisesDispatch36, premisesDispatch37, premisesDispatch38, premisesDispatch39, premisesDispatch40, premisesDispatch41, premisesDispatch42, premisesDispatch43, premisesDispatch44, premisesDispatch45, premisesDispatch46, premisesDispatch47, premisesDispatch48, premisesDispatch49, premisesDispatch50, premisesDispatch51, premisesDispatch52, premisesDispatch53, premisesDispatch54, premisesDispatch55, premisesDispatch56, premisesDispatch57, premisesDispatch58, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasE_j (Γ : P01AC.Tel) (A : P01AC.Ty) (x : P01D.Poly) (B : P01AC.Ty) (y : P01D.Poly) (e : P01D.Poly) (d : P01D.Poly) : premisesCode (encode (Rule.HasE_j Γ A x B y e d)) = premises_HasE_j (encode (Rule.HasE_j Γ A x B y e d)) := by
  have ht : tag (encode (Rule.HasE_j Γ A x B y e d)) = 59 := by rw [encode_Rule_HasE_j]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, premisesDispatch33, premisesDispatch34, premisesDispatch35, premisesDispatch36, premisesDispatch37, premisesDispatch38, premisesDispatch39, premisesDispatch40, premisesDispatch41, premisesDispatch42, premisesDispatch43, premisesDispatch44, premisesDispatch45, premisesDispatch46, premisesDispatch47, premisesDispatch48, premisesDispatch49, premisesDispatch50, premisesDispatch51, premisesDispatch52, premisesDispatch53, premisesDispatch54, premisesDispatch55, premisesDispatch56, premisesDispatch57, premisesDispatch58, premisesDispatch59, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasE_conv (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (aux0 : AuxiliaryCertificates.PolyCert) : premisesCode (encode (Rule.HasE_conv Γ A p q aux0)) = premises_HasE_conv (encode (Rule.HasE_conv Γ A p q aux0)) := by
  have ht : tag (encode (Rule.HasE_conv Γ A p q aux0)) = 60 := by rw [encode_Rule_HasE_conv]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, premisesDispatch33, premisesDispatch34, premisesDispatch35, premisesDispatch36, premisesDispatch37, premisesDispatch38, premisesDispatch39, premisesDispatch40, premisesDispatch41, premisesDispatch42, premisesDispatch43, premisesDispatch44, premisesDispatch45, premisesDispatch46, premisesDispatch47, premisesDispatch48, premisesDispatch49, premisesDispatch50, premisesDispatch51, premisesDispatch52, premisesDispatch53, premisesDispatch54, premisesDispatch55, premisesDispatch56, premisesDispatch57, premisesDispatch58, premisesDispatch59, premisesDispatch60, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasE_piExt (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (h : P01D.Poly) : premisesCode (encode (Rule.HasE_piExt Γ A B p q h)) = premises_HasE_piExt (encode (Rule.HasE_piExt Γ A B p q h)) := by
  have ht : tag (encode (Rule.HasE_piExt Γ A B p q h)) = 61 := by rw [encode_Rule_HasE_piExt]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, premisesDispatch33, premisesDispatch34, premisesDispatch35, premisesDispatch36, premisesDispatch37, premisesDispatch38, premisesDispatch39, premisesDispatch40, premisesDispatch41, premisesDispatch42, premisesDispatch43, premisesDispatch44, premisesDispatch45, premisesDispatch46, premisesDispatch47, premisesDispatch48, premisesDispatch49, premisesDispatch50, premisesDispatch51, premisesDispatch52, premisesDispatch53, premisesDispatch54, premisesDispatch55, premisesDispatch56, premisesDispatch57, premisesDispatch58, premisesDispatch59, premisesDispatch60, premisesDispatch61, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem premisesCode_HasE_allExt (Γ : P01AC.Tel) (B : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (h : P01D.Poly) : premisesCode (encode (Rule.HasE_allExt Γ B p q h)) = premises_HasE_allExt (encode (Rule.HasE_allExt Γ B p q h)) := by
  have ht : tag (encode (Rule.HasE_allExt Γ B p q h)) = 62 := by rw [encode_Rule_HasE_allExt]; exact tag_pack _ _
  simp only [premisesCode,premisesDispatch0, premisesDispatch1, premisesDispatch2, premisesDispatch3, premisesDispatch4, premisesDispatch5, premisesDispatch6, premisesDispatch7, premisesDispatch8, premisesDispatch9, premisesDispatch10, premisesDispatch11, premisesDispatch12, premisesDispatch13, premisesDispatch14, premisesDispatch15, premisesDispatch16, premisesDispatch17, premisesDispatch18, premisesDispatch19, premisesDispatch20, premisesDispatch21, premisesDispatch22, premisesDispatch23, premisesDispatch24, premisesDispatch25, premisesDispatch26, premisesDispatch27, premisesDispatch28, premisesDispatch29, premisesDispatch30, premisesDispatch31, premisesDispatch32, premisesDispatch33, premisesDispatch34, premisesDispatch35, premisesDispatch36, premisesDispatch37, premisesDispatch38, premisesDispatch39, premisesDispatch40, premisesDispatch41, premisesDispatch42, premisesDispatch43, premisesDispatch44, premisesDispatch45, premisesDispatch46, premisesDispatch47, premisesDispatch48, premisesDispatch49, premisesDispatch50, premisesDispatch51, premisesDispatch52, premisesDispatch53, premisesDispatch54, premisesDispatch55, premisesDispatch56, premisesDispatch57, premisesDispatch58, premisesDispatch59, premisesDispatch60, premisesDispatch61, premisesDispatch62, ht, Nat.reduceEqDiff, ↓reduceIte]

theorem premisesCode_exact (r : Rule) : premisesCode (encode r) = r.premises.map encode := by
  cases r <;> simp only [premisesCode_CtxJ_ctxBase, premisesCode_CtxJ_nil, premisesCode_CtxJ_ext, premisesCode_FormJ_formBase, premisesCode_FormJ_param, premisesCode_FormJ_bottom, premisesCode_FormJ_all, premisesCode_FormJ_raw, premisesCode_FormJ_pi, premisesCode_FormJ_sigma, premisesCode_FormJ_identity, premisesCode_HasJ_hasBase, premisesCode_HasJ_var, premisesCode_HasJ_i, premisesCode_HasJ_k, premisesCode_HasJ_s, premisesCode_HasJ_finite, premisesCode_HasJ_allIntro, premisesCode_HasJ_allElim, premisesCode_HasJ_rawAtom, premisesCode_HasJ_rawApp, premisesCode_HasJ_piIntro, premisesCode_HasJ_piElim, premisesCode_HasJ_sigmaIntro, premisesCode_HasJ_sigmaFst, premisesCode_HasJ_sigmaSnd, premisesCode_HasJ_identityIntro, premisesCode_HasJ_proofErase, premisesCode_HasJ_j, premisesCode_HasJ_conv, premisesCode_HasJ_piExt, premisesCode_HasJ_allExt, premisesCode_HasJ_sigmaElim, premisesCode_HasJ_natInduction, premisesCode_CtxE_nil, premisesCode_CtxE_ext, premisesCode_FormE_param, premisesCode_FormE_bottom, premisesCode_FormE_all, premisesCode_FormE_raw, premisesCode_FormE_pi, premisesCode_FormE_sigma, premisesCode_FormE_identity, premisesCode_HasE_var, premisesCode_HasE_i, premisesCode_HasE_k, premisesCode_HasE_s, premisesCode_HasE_finite, premisesCode_HasE_allIntro, premisesCode_HasE_allElim, premisesCode_HasE_rawAtom, premisesCode_HasE_rawApp, premisesCode_HasE_piIntro, premisesCode_HasE_piElim, premisesCode_HasE_sigmaIntro, premisesCode_HasE_sigmaFst, premisesCode_HasE_sigmaSnd, premisesCode_HasE_identityIntro, premisesCode_HasE_proofErase, premisesCode_HasE_j, premisesCode_HasE_conv, premisesCode_HasE_piExt, premisesCode_HasE_allExt, premises_CtxJ_ctxBase_exact, premises_CtxJ_nil_exact, premises_CtxJ_ext_exact, premises_FormJ_formBase_exact, premises_FormJ_param_exact, premises_FormJ_bottom_exact, premises_FormJ_all_exact, premises_FormJ_raw_exact, premises_FormJ_pi_exact, premises_FormJ_sigma_exact, premises_FormJ_identity_exact, premises_HasJ_hasBase_exact, premises_HasJ_var_exact, premises_HasJ_i_exact, premises_HasJ_k_exact, premises_HasJ_s_exact, premises_HasJ_finite_exact, premises_HasJ_allIntro_exact, premises_HasJ_allElim_exact, premises_HasJ_rawAtom_exact, premises_HasJ_rawApp_exact, premises_HasJ_piIntro_exact, premises_HasJ_piElim_exact, premises_HasJ_sigmaIntro_exact, premises_HasJ_sigmaFst_exact, premises_HasJ_sigmaSnd_exact, premises_HasJ_identityIntro_exact, premises_HasJ_proofErase_exact, premises_HasJ_j_exact, premises_HasJ_conv_exact, premises_HasJ_piExt_exact, premises_HasJ_allExt_exact, premises_HasJ_sigmaElim_exact, premises_HasJ_natInduction_exact, premises_CtxE_nil_exact, premises_CtxE_ext_exact, premises_FormE_param_exact, premises_FormE_bottom_exact, premises_FormE_all_exact, premises_FormE_raw_exact, premises_FormE_pi_exact, premises_FormE_sigma_exact, premises_FormE_identity_exact, premises_HasE_var_exact, premises_HasE_i_exact, premises_HasE_k_exact, premises_HasE_s_exact, premises_HasE_finite_exact, premises_HasE_allIntro_exact, premises_HasE_allElim_exact, premises_HasE_rawAtom_exact, premises_HasE_rawApp_exact, premises_HasE_piIntro_exact, premises_HasE_piElim_exact, premises_HasE_sigmaIntro_exact, premises_HasE_sigmaFst_exact, premises_HasE_sigmaSnd_exact, premises_HasE_identityIntro_exact, premises_HasE_proofErase_exact, premises_HasE_j_exact, premises_HasE_conv_exact, premises_HasE_piExt_exact, premises_HasE_allExt_exact]

#print axioms primrec_premisesCode
#print axioms premisesCode_exact
end CodedRuleTemplates
