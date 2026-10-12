import RuleCodeBasics
namespace CodedRuleTemplates
open P01D P01AC Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity CodedPolyTransformations CodedMixedTransformations
open AuxiliaryCodeComputability CertificateCodeValidity TelescopeCodeValidity JointCertificates
set_option maxRecDepth 32768
set_option maxHeartbeats 12000000
set_option linter.unusedVariables false
attribute [local irreducible] Nat.pair


def conclusion_CtxJ_ctxBase (c : Nat) : Nat := (ctxCode 0 (ruleField c 0))
theorem primrec_conclusion_CtxJ_ctxBase : Primrec conclusion_CtxJ_ctxBase := by
  have h := ((primrec_ctxCode 0).comp (primrec_ruleField.comp Primrec.id (.const 0)))
  exact h.of_eq (by intro c; simp only [conclusion_CtxJ_ctxBase,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_CtxJ_ctxBase_exact (Γ : P01AC.Tel) : conclusion_CtxJ_ctxBase (encode (Rule.CtxJ_ctxBase Γ)) = encode ((Rule.CtxJ_ctxBase Γ).conclusion) := by
  simp only [conclusion_CtxJ_ctxBase,Rule.conclusion,encode_Rule_CtxJ_ctxBase,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_CtxJ_nil (c : Nat) : Nat := (ctxCode 0 (encode ([] : Tel)))
theorem primrec_conclusion_CtxJ_nil : Primrec conclusion_CtxJ_nil := by
  have h : Primrec (fun _ : Nat => ((ctxCode 0 (encode ([] : Tel))) : Nat)) := Primrec.const _
  exact h.of_eq (by intro c; simp only [conclusion_CtxJ_nil,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_CtxJ_nil_exact  : conclusion_CtxJ_nil (encode (Rule.CtxJ_nil )) = encode ((Rule.CtxJ_nil ).conclusion) := by
  simp only [conclusion_CtxJ_nil,Rule.conclusion,encode_Rule_CtxJ_nil,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_CtxJ_ext (c : Nat) : Nat := (ctxCode 0 ((telConsCode (ruleField c 1) (ruleField c 0))))
theorem primrec_conclusion_CtxJ_ext : Primrec conclusion_CtxJ_ext := by
  have h := ((primrec_ctxCode 0).comp (primrec_telConsCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 0))))
  exact h.of_eq (by intro c; simp only [conclusion_CtxJ_ext,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_CtxJ_ext_exact (Γ : P01AC.Tel) (A : P01AC.Ty) : conclusion_CtxJ_ext (encode (Rule.CtxJ_ext Γ A)) = encode ((Rule.CtxJ_ext Γ A).conclusion) := by
  simp only [conclusion_CtxJ_ext,Rule.conclusion,encode_Rule_CtxJ_ext,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_FormJ_formBase (c : Nat) : Nat := (formCode 1 (ruleField c 0) (ruleField c 1))
theorem primrec_conclusion_FormJ_formBase : Primrec conclusion_FormJ_formBase := by
  have h := ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 1)))
  exact h.of_eq (by intro c; simp only [conclusion_FormJ_formBase,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_FormJ_formBase_exact (Γ : P01AC.Tel) (A : P01AC.Ty) : conclusion_FormJ_formBase (encode (Rule.FormJ_formBase Γ A)) = encode ((Rule.FormJ_formBase Γ A).conclusion) := by
  simp only [conclusion_FormJ_formBase,Rule.conclusion,encode_Rule_FormJ_formBase,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_FormJ_param (c : Nat) : Nat := (formCode 1 (ruleField c 0) ((paramCode (ruleField c 1))))
theorem primrec_conclusion_FormJ_param : Primrec conclusion_FormJ_param := by
  have h := ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_paramCode.comp (primrec_ruleField.comp Primrec.id (.const 1))))
  exact h.of_eq (by intro c; simp only [conclusion_FormJ_param,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_FormJ_param_exact (Γ : P01AC.Tel) (n : Nat) : conclusion_FormJ_param (encode (Rule.FormJ_param Γ n)) = encode ((Rule.FormJ_param Γ n).conclusion) := by
  simp only [conclusion_FormJ_param,Rule.conclusion,encode_Rule_FormJ_param,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_FormJ_bottom (c : Nat) : Nat := (formCode 1 (ruleField c 0) (encode (P01AC.Ty.bottom)))
theorem primrec_conclusion_FormJ_bottom : Primrec conclusion_FormJ_bottom := by
  have h := ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (Primrec.const (encode (P01AC.Ty.bottom))))
  exact h.of_eq (by intro c; simp only [conclusion_FormJ_bottom,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_FormJ_bottom_exact (Γ : P01AC.Tel) : conclusion_FormJ_bottom (encode (Rule.FormJ_bottom Γ)) = encode ((Rule.FormJ_bottom Γ).conclusion) := by
  simp only [conclusion_FormJ_bottom,Rule.conclusion,encode_Rule_FormJ_bottom,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_FormJ_all (c : Nat) : Nat := (formCode 1 (ruleField c 0) ((allTyCode (ruleField c 1))))
theorem primrec_conclusion_FormJ_all : Primrec conclusion_FormJ_all := by
  have h := ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_allTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1))))
  exact h.of_eq (by intro c; simp only [conclusion_FormJ_all,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_FormJ_all_exact (Γ : P01AC.Tel) (B : P01AC.Ty) : conclusion_FormJ_all (encode (Rule.FormJ_all Γ B)) = encode ((Rule.FormJ_all Γ B).conclusion) := by
  simp only [conclusion_FormJ_all,Rule.conclusion,encode_Rule_FormJ_all,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_FormJ_raw (c : Nat) : Nat := (formCode 1 (ruleField c 0) (encode (P01AC.Ty.raw)))
theorem primrec_conclusion_FormJ_raw : Primrec conclusion_FormJ_raw := by
  have h := ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (Primrec.const (encode (P01AC.Ty.raw))))
  exact h.of_eq (by intro c; simp only [conclusion_FormJ_raw,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_FormJ_raw_exact (Γ : P01AC.Tel) : conclusion_FormJ_raw (encode (Rule.FormJ_raw Γ)) = encode ((Rule.FormJ_raw Γ).conclusion) := by
  simp only [conclusion_FormJ_raw,Rule.conclusion,encode_Rule_FormJ_raw,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_FormJ_pi (c : Nat) : Nat := (formCode 1 (ruleField c 0) ((piCode (ruleField c 1) (ruleField c 2))))
theorem primrec_conclusion_FormJ_pi : Primrec conclusion_FormJ_pi := by
  have h := ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_piCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2))))
  exact h.of_eq (by intro c; simp only [conclusion_FormJ_pi,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_FormJ_pi_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : conclusion_FormJ_pi (encode (Rule.FormJ_pi Γ A B)) = encode ((Rule.FormJ_pi Γ A B).conclusion) := by
  simp only [conclusion_FormJ_pi,Rule.conclusion,encode_Rule_FormJ_pi,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_FormJ_sigma (c : Nat) : Nat := (formCode 1 (ruleField c 0) ((sigmaTyCode (ruleField c 1) (ruleField c 2))))
theorem primrec_conclusion_FormJ_sigma : Primrec conclusion_FormJ_sigma := by
  have h := ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_sigmaTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2))))
  exact h.of_eq (by intro c; simp only [conclusion_FormJ_sigma,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_FormJ_sigma_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : conclusion_FormJ_sigma (encode (Rule.FormJ_sigma Γ A B)) = encode ((Rule.FormJ_sigma Γ A B).conclusion) := by
  simp only [conclusion_FormJ_sigma,Rule.conclusion,encode_Rule_FormJ_sigma,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_FormJ_identity (c : Nat) : Nat := (formCode 1 (ruleField c 0) ((identityTyCode (ruleField c 1) (ruleField c 2) (ruleField c 3))))
theorem primrec_conclusion_FormJ_identity : Primrec conclusion_FormJ_identity := by
  have h := ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_identityTyCode.comp ((primrec_ruleField.comp Primrec.id (.const 1)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 3))))))
  exact h.of_eq (by intro c; simp only [conclusion_FormJ_identity,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_FormJ_identity_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) : conclusion_FormJ_identity (encode (Rule.FormJ_identity Γ A p q)) = encode ((Rule.FormJ_identity Γ A p q).conclusion) := by
  simp only [conclusion_FormJ_identity,Rule.conclusion,encode_Rule_FormJ_identity,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasJ_hasBase (c : Nat) : Nat := (hasCode 2 (ruleField c 0) (ruleField c 1) (ruleField c 2))
theorem primrec_conclusion_HasJ_hasBase : Primrec conclusion_HasJ_hasBase := by
  have h := ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 1)).pair (primrec_ruleField.comp Primrec.id (.const 2)))))
  exact h.of_eq (by intro c; simp only [conclusion_HasJ_hasBase,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasJ_hasBase_exact (Γ : P01AC.Tel) (p : P01D.Poly) (A : P01AC.Ty) : conclusion_HasJ_hasBase (encode (Rule.HasJ_hasBase Γ p A)) = encode ((Rule.HasJ_hasBase Γ p A).conclusion) := by
  simp only [conclusion_HasJ_hasBase,Rule.conclusion,encode_Rule_HasJ_hasBase,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasJ_var (c : Nat) : Nat := (hasCode 2 (ruleField c 0) ((varCode (ruleField c 2))) (ruleField c 1))
theorem primrec_conclusion_HasJ_var : Primrec conclusion_HasJ_var := by
  have h := ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_varCode.comp (primrec_ruleField.comp Primrec.id (.const 2))).pair (primrec_ruleField.comp Primrec.id (.const 1)))))
  exact h.of_eq (by intro c; simp only [conclusion_HasJ_var,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasJ_var_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (n : Nat) (aux0 : AuxiliaryCertificates.LookupCert) : conclusion_HasJ_var (encode (Rule.HasJ_var Γ A n aux0)) = encode ((Rule.HasJ_var Γ A n aux0).conclusion) := by
  simp only [conclusion_HasJ_var,Rule.conclusion,encode_Rule_HasJ_var,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasJ_i (c : Nat) : Nat := (hasCode 2 (ruleField c 0) ((polyAtom (encode (OrthemologyV2.Term.i)))) ((arrCode (ruleField c 1) (ruleField c 1))))
theorem primrec_conclusion_HasJ_i : Primrec conclusion_HasJ_i := by
  have h := ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_polyAtom.comp (Primrec.const (encode (OrthemologyV2.Term.i)))).pair (primrec_arrCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 1))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasJ_i,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasJ_i_exact (Γ : P01AC.Tel) (A : P01AC.Ty) : conclusion_HasJ_i (encode (Rule.HasJ_i Γ A)) = encode ((Rule.HasJ_i Γ A).conclusion) := by
  simp only [conclusion_HasJ_i,Rule.conclusion,encode_Rule_HasJ_i,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasJ_k (c : Nat) : Nat := (hasCode 2 (ruleField c 0) ((polyAtom (encode (OrthemologyV2.Term.k)))) ((arrCode (ruleField c 1) ((arrCode (ruleField c 2) (ruleField c 1))))))
theorem primrec_conclusion_HasJ_k : Primrec conclusion_HasJ_k := by
  have h := ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_polyAtom.comp (Primrec.const (encode (OrthemologyV2.Term.k)))).pair (primrec_arrCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_arrCode.comp (primrec_ruleField.comp Primrec.id (.const 2)) (primrec_ruleField.comp Primrec.id (.const 1)))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasJ_k,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasJ_k_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : conclusion_HasJ_k (encode (Rule.HasJ_k Γ A B)) = encode ((Rule.HasJ_k Γ A B).conclusion) := by
  simp only [conclusion_HasJ_k,Rule.conclusion,encode_Rule_HasJ_k,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasJ_s (c : Nat) : Nat := (hasCode 2 (ruleField c 0) ((polyAtom (encode (OrthemologyV2.Term.s)))) ((arrCode ((arrCode (ruleField c 1) ((arrCode (ruleField c 2) (ruleField c 3))))) ((arrCode ((arrCode (ruleField c 1) (ruleField c 2))) ((arrCode (ruleField c 1) (ruleField c 3))))))))
theorem primrec_conclusion_HasJ_s : Primrec conclusion_HasJ_s := by
  have h := ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_polyAtom.comp (Primrec.const (encode (OrthemologyV2.Term.s)))).pair (primrec_arrCode.comp (primrec_arrCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_arrCode.comp (primrec_ruleField.comp Primrec.id (.const 2)) (primrec_ruleField.comp Primrec.id (.const 3)))) (primrec_arrCode.comp (primrec_arrCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2))) (primrec_arrCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 3))))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasJ_s,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasJ_s_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (C : P01AC.Ty) : conclusion_HasJ_s (encode (Rule.HasJ_s Γ A B C)) = encode ((Rule.HasJ_s Γ A B C).conclusion) := by
  simp only [conclusion_HasJ_s,Rule.conclusion,encode_Rule_HasJ_s,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasJ_finite (c : Nat) : Nat := (hasCode 2 (ruleField c 1) ((polyAtom (ruleField c 2))) ((tsubstTelCode (ruleField c 3) ((finCode (ruleField c 0))))))
theorem primrec_conclusion_HasJ_finite : Primrec conclusion_HasJ_finite := by
  have h := ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 1)).pair ((primrec_polyAtom.comp (primrec_ruleField.comp Primrec.id (.const 2))).pair (primrec_tsubstTelCode.comp (primrec_ruleField.comp Primrec.id (.const 3)) (primrec_finCode.comp (primrec_ruleField.comp Primrec.id (.const 0)))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasJ_finite,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasJ_finite_exact (C : OrthemologyV2.TypeCode) (Γ : P01AC.Tel) (t : OrthemologyV2.Term) (τ : List P01AC.Ty) (aux0 : AuxiliaryCertificates.FiniteCert) : conclusion_HasJ_finite (encode (Rule.HasJ_finite C Γ t τ aux0)) = encode ((Rule.HasJ_finite C Γ t τ aux0).conclusion) := by
  simp only [conclusion_HasJ_finite,Rule.conclusion,encode_Rule_HasJ_finite,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasJ_allIntro (c : Nat) : Nat := (hasCode 2 (ruleField c 0) (ruleField c 2) ((allTyCode (ruleField c 1))))
theorem primrec_conclusion_HasJ_allIntro : Primrec conclusion_HasJ_allIntro := by
  have h := ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_allTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasJ_allIntro,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasJ_allIntro_exact (Γ : P01AC.Tel) (B : P01AC.Ty) (p : P01D.Poly) : conclusion_HasJ_allIntro (encode (Rule.HasJ_allIntro Γ B p)) = encode ((Rule.HasJ_allIntro Γ B p).conclusion) := by
  simp only [conclusion_HasJ_allIntro,Rule.conclusion,encode_Rule_HasJ_allIntro,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasJ_allElim (c : Nat) : Nat := (hasCode 2 (ruleField c 0) (ruleField c 3) ((tinstCode (ruleField c 2) (ruleField c 1))))
theorem primrec_conclusion_HasJ_allElim : Primrec conclusion_HasJ_allElim := by
  have h := ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 3)).pair (primrec_tinstCode.comp (primrec_ruleField.comp Primrec.id (.const 2)) (primrec_ruleField.comp Primrec.id (.const 1))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasJ_allElim,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasJ_allElim_exact (Γ : P01AC.Tel) (B : P01AC.Ty) (A : P01AC.Ty) (p : P01D.Poly) : conclusion_HasJ_allElim (encode (Rule.HasJ_allElim Γ B A p)) = encode ((Rule.HasJ_allElim Γ B A p).conclusion) := by
  simp only [conclusion_HasJ_allElim,Rule.conclusion,encode_Rule_HasJ_allElim,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasJ_rawAtom (c : Nat) : Nat := (hasCode 2 (ruleField c 0) ((polyAtom (ruleField c 1))) (encode (P01AC.Ty.raw)))
theorem primrec_conclusion_HasJ_rawAtom : Primrec conclusion_HasJ_rawAtom := by
  have h := ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_polyAtom.comp (primrec_ruleField.comp Primrec.id (.const 1))).pair (Primrec.const (encode (P01AC.Ty.raw))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasJ_rawAtom,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasJ_rawAtom_exact (Γ : P01AC.Tel) (t : OrthemologyV2.Term) : conclusion_HasJ_rawAtom (encode (Rule.HasJ_rawAtom Γ t)) = encode ((Rule.HasJ_rawAtom Γ t).conclusion) := by
  simp only [conclusion_HasJ_rawAtom,Rule.conclusion,encode_Rule_HasJ_rawAtom,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasJ_rawApp (c : Nat) : Nat := (hasCode 2 (ruleField c 0) ((appCode (ruleField c 1) (ruleField c 2))) (encode (P01AC.Ty.raw)))
theorem primrec_conclusion_HasJ_rawApp : Primrec conclusion_HasJ_rawApp := by
  have h := ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_appCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2))).pair (Primrec.const (encode (P01AC.Ty.raw))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasJ_rawApp,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasJ_rawApp_exact (Γ : P01AC.Tel) (f : P01D.Poly) (a : P01D.Poly) : conclusion_HasJ_rawApp (encode (Rule.HasJ_rawApp Γ f a)) = encode ((Rule.HasJ_rawApp Γ f a).conclusion) := by
  simp only [conclusion_HasJ_rawApp,Rule.conclusion,encode_Rule_HasJ_rawApp,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasJ_piIntro (c : Nat) : Nat := (hasCode 2 (ruleField c 0) ((abstractCode (ruleField c 3))) ((piCode (ruleField c 1) (ruleField c 2))))
theorem primrec_conclusion_HasJ_piIntro : Primrec conclusion_HasJ_piIntro := by
  have h := ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_abstractCode.comp (primrec_ruleField.comp Primrec.id (.const 3))).pair (primrec_piCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasJ_piIntro,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasJ_piIntro_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (b : P01D.Poly) : conclusion_HasJ_piIntro (encode (Rule.HasJ_piIntro Γ A B b)) = encode ((Rule.HasJ_piIntro Γ A B b).conclusion) := by
  simp only [conclusion_HasJ_piIntro,Rule.conclusion,encode_Rule_HasJ_piIntro,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasJ_piElim (c : Nat) : Nat := (hasCode 2 (ruleField c 0) ((appCode (ruleField c 4) (ruleField c 3))) ((instTyCode (ruleField c 3) (ruleField c 2))))
theorem primrec_conclusion_HasJ_piElim : Primrec conclusion_HasJ_piElim := by
  have h := ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_appCode.comp (primrec_ruleField.comp Primrec.id (.const 4)) (primrec_ruleField.comp Primrec.id (.const 3))).pair (primrec_instTyCode.comp (primrec_ruleField.comp Primrec.id (.const 3)) (primrec_ruleField.comp Primrec.id (.const 2))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasJ_piElim,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasJ_piElim_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (a : P01D.Poly) (f : P01D.Poly) : conclusion_HasJ_piElim (encode (Rule.HasJ_piElim Γ A B a f)) = encode ((Rule.HasJ_piElim Γ A B a f).conclusion) := by
  simp only [conclusion_HasJ_piElim,Rule.conclusion,encode_Rule_HasJ_piElim,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasJ_sigmaIntro (c : Nat) : Nat := (hasCode 2 (ruleField c 0) ((pairPolyCode (ruleField c 3) (ruleField c 4))) ((sigmaTyCode (ruleField c 1) (ruleField c 2))))
theorem primrec_conclusion_HasJ_sigmaIntro : Primrec conclusion_HasJ_sigmaIntro := by
  have h := ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_pairPolyCode.comp (primrec_ruleField.comp Primrec.id (.const 3)) (primrec_ruleField.comp Primrec.id (.const 4))).pair (primrec_sigmaTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasJ_sigmaIntro,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasJ_sigmaIntro_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (a : P01D.Poly) (b : P01D.Poly) : conclusion_HasJ_sigmaIntro (encode (Rule.HasJ_sigmaIntro Γ A B a b)) = encode ((Rule.HasJ_sigmaIntro Γ A B a b).conclusion) := by
  simp only [conclusion_HasJ_sigmaIntro,Rule.conclusion,encode_Rule_HasJ_sigmaIntro,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasJ_sigmaFst (c : Nat) : Nat := (hasCode 2 (ruleField c 0) ((fstPolyCode (ruleField c 3))) (ruleField c 1))
theorem primrec_conclusion_HasJ_sigmaFst : Primrec conclusion_HasJ_sigmaFst := by
  have h := ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_fstPolyCode.comp (primrec_ruleField.comp Primrec.id (.const 3))).pair (primrec_ruleField.comp Primrec.id (.const 1)))))
  exact h.of_eq (by intro c; simp only [conclusion_HasJ_sigmaFst,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasJ_sigmaFst_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (z : P01D.Poly) : conclusion_HasJ_sigmaFst (encode (Rule.HasJ_sigmaFst Γ A B z)) = encode ((Rule.HasJ_sigmaFst Γ A B z).conclusion) := by
  simp only [conclusion_HasJ_sigmaFst,Rule.conclusion,encode_Rule_HasJ_sigmaFst,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasJ_sigmaSnd (c : Nat) : Nat := (hasCode 2 (ruleField c 0) ((sndPolyCode (ruleField c 3))) ((instTyCode ((fstPolyCode (ruleField c 3))) (ruleField c 2))))
theorem primrec_conclusion_HasJ_sigmaSnd : Primrec conclusion_HasJ_sigmaSnd := by
  have h := ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_sndPolyCode.comp (primrec_ruleField.comp Primrec.id (.const 3))).pair (primrec_instTyCode.comp (primrec_fstPolyCode.comp (primrec_ruleField.comp Primrec.id (.const 3))) (primrec_ruleField.comp Primrec.id (.const 2))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasJ_sigmaSnd,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasJ_sigmaSnd_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (z : P01D.Poly) : conclusion_HasJ_sigmaSnd (encode (Rule.HasJ_sigmaSnd Γ A B z)) = encode ((Rule.HasJ_sigmaSnd Γ A B z).conclusion) := by
  simp only [conclusion_HasJ_sigmaSnd,Rule.conclusion,encode_Rule_HasJ_sigmaSnd,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasJ_identityIntro (c : Nat) : Nat := (hasCode 2 (ruleField c 0) ((polyAtom (encode (OrthemologyV2.Term.i)))) ((identityTyCode (ruleField c 1) (ruleField c 2) (ruleField c 3))))
theorem primrec_conclusion_HasJ_identityIntro : Primrec conclusion_HasJ_identityIntro := by
  have h := ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_polyAtom.comp (Primrec.const (encode (OrthemologyV2.Term.i)))).pair (primrec_identityTyCode.comp ((primrec_ruleField.comp Primrec.id (.const 1)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 3))))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasJ_identityIntro,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasJ_identityIntro_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (aux0 : AuxiliaryCertificates.PolyCert) : conclusion_HasJ_identityIntro (encode (Rule.HasJ_identityIntro Γ A p q aux0)) = encode ((Rule.HasJ_identityIntro Γ A p q aux0).conclusion) := by
  simp only [conclusion_HasJ_identityIntro,Rule.conclusion,encode_Rule_HasJ_identityIntro,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasJ_proofErase (c : Nat) : Nat := (hasCode 2 (ruleField c 0) (ruleField c 4) (encode (P01AC.Ty.raw)))
theorem primrec_conclusion_HasJ_proofErase : Primrec conclusion_HasJ_proofErase := by
  have h := ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 4)).pair (Primrec.const (encode (P01AC.Ty.raw))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasJ_proofErase,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasJ_proofErase_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (x : P01D.Poly) (y : P01D.Poly) (p : P01D.Poly) : conclusion_HasJ_proofErase (encode (Rule.HasJ_proofErase Γ A x y p)) = encode ((Rule.HasJ_proofErase Γ A x y p).conclusion) := by
  simp only [conclusion_HasJ_proofErase,Rule.conclusion,encode_Rule_HasJ_proofErase,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasJ_j (c : Nat) : Nat := (hasCode 2 (ruleField c 0) ((jPolyCode (ruleField c 6) (ruleField c 4) (ruleField c 5))) ((motiveAtCode (ruleField c 3) (ruleField c 4) (ruleField c 5))))
theorem primrec_conclusion_HasJ_j : Primrec conclusion_HasJ_j := by
  have h := ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_jPolyCode.comp ((primrec_ruleField.comp Primrec.id (.const 6)).pair ((primrec_ruleField.comp Primrec.id (.const 4)).pair (primrec_ruleField.comp Primrec.id (.const 5))))).pair (primrec_motiveAtCode.comp ((primrec_ruleField.comp Primrec.id (.const 3)).pair ((primrec_ruleField.comp Primrec.id (.const 4)).pair (primrec_ruleField.comp Primrec.id (.const 5))))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasJ_j,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasJ_j_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (x : P01D.Poly) (B : P01AC.Ty) (y : P01D.Poly) (e : P01D.Poly) (d : P01D.Poly) : conclusion_HasJ_j (encode (Rule.HasJ_j Γ A x B y e d)) = encode ((Rule.HasJ_j Γ A x B y e d).conclusion) := by
  simp only [conclusion_HasJ_j,Rule.conclusion,encode_Rule_HasJ_j,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasJ_conv (c : Nat) : Nat := (hasCode 2 (ruleField c 0) (ruleField c 3) (ruleField c 1))
theorem primrec_conclusion_HasJ_conv : Primrec conclusion_HasJ_conv := by
  have h := ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 3)).pair (primrec_ruleField.comp Primrec.id (.const 1)))))
  exact h.of_eq (by intro c; simp only [conclusion_HasJ_conv,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasJ_conv_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (aux0 : AuxiliaryCertificates.PolyCert) : conclusion_HasJ_conv (encode (Rule.HasJ_conv Γ A p q aux0)) = encode ((Rule.HasJ_conv Γ A p q aux0).conclusion) := by
  simp only [conclusion_HasJ_conv,Rule.conclusion,encode_Rule_HasJ_conv,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasJ_piExt (c : Nat) : Nat := (hasCode 2 (ruleField c 0) ((polyAtom (encode (OrthemologyV2.Term.i)))) ((identityTyCode ((piCode (ruleField c 1) (ruleField c 2))) (ruleField c 3) (ruleField c 4))))
theorem primrec_conclusion_HasJ_piExt : Primrec conclusion_HasJ_piExt := by
  have h := ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_polyAtom.comp (Primrec.const (encode (OrthemologyV2.Term.i)))).pair (primrec_identityTyCode.comp ((primrec_piCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2))).pair ((primrec_ruleField.comp Primrec.id (.const 3)).pair (primrec_ruleField.comp Primrec.id (.const 4))))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasJ_piExt,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasJ_piExt_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (h : P01D.Poly) : conclusion_HasJ_piExt (encode (Rule.HasJ_piExt Γ A B p q h)) = encode ((Rule.HasJ_piExt Γ A B p q h).conclusion) := by
  simp only [conclusion_HasJ_piExt,Rule.conclusion,encode_Rule_HasJ_piExt,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasJ_allExt (c : Nat) : Nat := (hasCode 2 (ruleField c 0) ((polyAtom (encode (OrthemologyV2.Term.i)))) ((identityTyCode ((allTyCode (ruleField c 1))) (ruleField c 2) (ruleField c 3))))
theorem primrec_conclusion_HasJ_allExt : Primrec conclusion_HasJ_allExt := by
  have h := ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_polyAtom.comp (Primrec.const (encode (OrthemologyV2.Term.i)))).pair (primrec_identityTyCode.comp ((primrec_allTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1))).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 3))))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasJ_allExt,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasJ_allExt_exact (Γ : P01AC.Tel) (B : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (h : P01D.Poly) : conclusion_HasJ_allExt (encode (Rule.HasJ_allExt Γ B p q h)) = encode ((Rule.HasJ_allExt Γ B p q h).conclusion) := by
  simp only [conclusion_HasJ_allExt,Rule.conclusion,encode_Rule_HasJ_allExt,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasJ_sigmaElim (c : Nat) : Nat := (hasCode 2 (ruleField c 0) ((branchAtCode (ruleField c 4) ((fstPolyCode (ruleField c 5))) ((sndPolyCode (ruleField c 5))))) ((instTyCode (ruleField c 5) (ruleField c 3))))
theorem primrec_conclusion_HasJ_sigmaElim : Primrec conclusion_HasJ_sigmaElim := by
  have h := ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_branchAtCode.comp ((primrec_ruleField.comp Primrec.id (.const 4)).pair ((primrec_fstPolyCode.comp (primrec_ruleField.comp Primrec.id (.const 5))).pair (primrec_sndPolyCode.comp (primrec_ruleField.comp Primrec.id (.const 5)))))).pair (primrec_instTyCode.comp (primrec_ruleField.comp Primrec.id (.const 5)) (primrec_ruleField.comp Primrec.id (.const 3))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasJ_sigmaElim,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasJ_sigmaElim_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (P : P01AC.Ty) (d : P01D.Poly) (z : P01D.Poly) : conclusion_HasJ_sigmaElim (encode (Rule.HasJ_sigmaElim Γ A B P d z)) = encode ((Rule.HasJ_sigmaElim Γ A B P d z).conclusion) := by
  simp only [conclusion_HasJ_sigmaElim,Rule.conclusion,encode_Rule_HasJ_sigmaElim,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasJ_natInduction (c : Nat) : Nat := (hasCode 2 (ruleField c 0) ((sectionPolyCode (ruleField c 2) (ruleField c 3))) ((piCode (encode (P01AC.EffectiveCompleteness.N)) (ruleField c 1))))
theorem primrec_conclusion_HasJ_natInduction : Primrec conclusion_HasJ_natInduction := by
  have h := ((primrec_hasCode 2).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_sectionPolyCode.comp (primrec_ruleField.comp Primrec.id (.const 2)) (primrec_ruleField.comp Primrec.id (.const 3))).pair (primrec_piCode.comp (Primrec.const (encode (P01AC.EffectiveCompleteness.N))) (primrec_ruleField.comp Primrec.id (.const 1))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasJ_natInduction,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasJ_natInduction_exact (Γ : P01AC.Tel) (P : P01AC.Ty) (p : P01D.Poly) (s : P01D.Poly) : conclusion_HasJ_natInduction (encode (Rule.HasJ_natInduction Γ P p s)) = encode ((Rule.HasJ_natInduction Γ P p s).conclusion) := by
  simp only [conclusion_HasJ_natInduction,Rule.conclusion,encode_Rule_HasJ_natInduction,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_CtxE_nil (c : Nat) : Nat := (ctxCode 3 (encode ([] : Tel)))
theorem primrec_conclusion_CtxE_nil : Primrec conclusion_CtxE_nil := by
  have h : Primrec (fun _ : Nat => ((ctxCode 3 (encode ([] : Tel))) : Nat)) := Primrec.const _
  exact h.of_eq (by intro c; simp only [conclusion_CtxE_nil,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_CtxE_nil_exact  : conclusion_CtxE_nil (encode (Rule.CtxE_nil )) = encode ((Rule.CtxE_nil ).conclusion) := by
  simp only [conclusion_CtxE_nil,Rule.conclusion,encode_Rule_CtxE_nil,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_CtxE_ext (c : Nat) : Nat := (ctxCode 3 ((telConsCode (ruleField c 1) (ruleField c 0))))
theorem primrec_conclusion_CtxE_ext : Primrec conclusion_CtxE_ext := by
  have h := ((primrec_ctxCode 3).comp (primrec_telConsCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 0))))
  exact h.of_eq (by intro c; simp only [conclusion_CtxE_ext,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_CtxE_ext_exact (Γ : P01AC.Tel) (A : P01AC.Ty) : conclusion_CtxE_ext (encode (Rule.CtxE_ext Γ A)) = encode ((Rule.CtxE_ext Γ A).conclusion) := by
  simp only [conclusion_CtxE_ext,Rule.conclusion,encode_Rule_CtxE_ext,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_FormE_param (c : Nat) : Nat := (formCode 4 (ruleField c 0) ((paramCode (ruleField c 1))))
theorem primrec_conclusion_FormE_param : Primrec conclusion_FormE_param := by
  have h := ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_paramCode.comp (primrec_ruleField.comp Primrec.id (.const 1))))
  exact h.of_eq (by intro c; simp only [conclusion_FormE_param,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_FormE_param_exact (Γ : P01AC.Tel) (n : Nat) : conclusion_FormE_param (encode (Rule.FormE_param Γ n)) = encode ((Rule.FormE_param Γ n).conclusion) := by
  simp only [conclusion_FormE_param,Rule.conclusion,encode_Rule_FormE_param,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_FormE_bottom (c : Nat) : Nat := (formCode 4 (ruleField c 0) (encode (P01AC.Ty.bottom)))
theorem primrec_conclusion_FormE_bottom : Primrec conclusion_FormE_bottom := by
  have h := ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (Primrec.const (encode (P01AC.Ty.bottom))))
  exact h.of_eq (by intro c; simp only [conclusion_FormE_bottom,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_FormE_bottom_exact (Γ : P01AC.Tel) : conclusion_FormE_bottom (encode (Rule.FormE_bottom Γ)) = encode ((Rule.FormE_bottom Γ).conclusion) := by
  simp only [conclusion_FormE_bottom,Rule.conclusion,encode_Rule_FormE_bottom,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_FormE_all (c : Nat) : Nat := (formCode 4 (ruleField c 0) ((allTyCode (ruleField c 1))))
theorem primrec_conclusion_FormE_all : Primrec conclusion_FormE_all := by
  have h := ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_allTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1))))
  exact h.of_eq (by intro c; simp only [conclusion_FormE_all,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_FormE_all_exact (Γ : P01AC.Tel) (B : P01AC.Ty) : conclusion_FormE_all (encode (Rule.FormE_all Γ B)) = encode ((Rule.FormE_all Γ B).conclusion) := by
  simp only [conclusion_FormE_all,Rule.conclusion,encode_Rule_FormE_all,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_FormE_raw (c : Nat) : Nat := (formCode 4 (ruleField c 0) (encode (P01AC.Ty.raw)))
theorem primrec_conclusion_FormE_raw : Primrec conclusion_FormE_raw := by
  have h := ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (Primrec.const (encode (P01AC.Ty.raw))))
  exact h.of_eq (by intro c; simp only [conclusion_FormE_raw,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_FormE_raw_exact (Γ : P01AC.Tel) : conclusion_FormE_raw (encode (Rule.FormE_raw Γ)) = encode ((Rule.FormE_raw Γ).conclusion) := by
  simp only [conclusion_FormE_raw,Rule.conclusion,encode_Rule_FormE_raw,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_FormE_pi (c : Nat) : Nat := (formCode 4 (ruleField c 0) ((piCode (ruleField c 1) (ruleField c 2))))
theorem primrec_conclusion_FormE_pi : Primrec conclusion_FormE_pi := by
  have h := ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_piCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2))))
  exact h.of_eq (by intro c; simp only [conclusion_FormE_pi,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_FormE_pi_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : conclusion_FormE_pi (encode (Rule.FormE_pi Γ A B)) = encode ((Rule.FormE_pi Γ A B).conclusion) := by
  simp only [conclusion_FormE_pi,Rule.conclusion,encode_Rule_FormE_pi,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_FormE_sigma (c : Nat) : Nat := (formCode 4 (ruleField c 0) ((sigmaTyCode (ruleField c 1) (ruleField c 2))))
theorem primrec_conclusion_FormE_sigma : Primrec conclusion_FormE_sigma := by
  have h := ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_sigmaTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2))))
  exact h.of_eq (by intro c; simp only [conclusion_FormE_sigma,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_FormE_sigma_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : conclusion_FormE_sigma (encode (Rule.FormE_sigma Γ A B)) = encode ((Rule.FormE_sigma Γ A B).conclusion) := by
  simp only [conclusion_FormE_sigma,Rule.conclusion,encode_Rule_FormE_sigma,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_FormE_identity (c : Nat) : Nat := (formCode 4 (ruleField c 0) ((identityTyCode (ruleField c 1) (ruleField c 2) (ruleField c 3))))
theorem primrec_conclusion_FormE_identity : Primrec conclusion_FormE_identity := by
  have h := ((primrec_formCode 4).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_identityTyCode.comp ((primrec_ruleField.comp Primrec.id (.const 1)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 3))))))
  exact h.of_eq (by intro c; simp only [conclusion_FormE_identity,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_FormE_identity_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) : conclusion_FormE_identity (encode (Rule.FormE_identity Γ A p q)) = encode ((Rule.FormE_identity Γ A p q).conclusion) := by
  simp only [conclusion_FormE_identity,Rule.conclusion,encode_Rule_FormE_identity,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasE_var (c : Nat) : Nat := (hasCode 5 (ruleField c 0) ((varCode (ruleField c 2))) (ruleField c 1))
theorem primrec_conclusion_HasE_var : Primrec conclusion_HasE_var := by
  have h := ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_varCode.comp (primrec_ruleField.comp Primrec.id (.const 2))).pair (primrec_ruleField.comp Primrec.id (.const 1)))))
  exact h.of_eq (by intro c; simp only [conclusion_HasE_var,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasE_var_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (n : Nat) (aux0 : AuxiliaryCertificates.LookupCert) : conclusion_HasE_var (encode (Rule.HasE_var Γ A n aux0)) = encode ((Rule.HasE_var Γ A n aux0).conclusion) := by
  simp only [conclusion_HasE_var,Rule.conclusion,encode_Rule_HasE_var,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasE_i (c : Nat) : Nat := (hasCode 5 (ruleField c 0) ((polyAtom (encode (OrthemologyV2.Term.i)))) ((arrCode (ruleField c 1) (ruleField c 1))))
theorem primrec_conclusion_HasE_i : Primrec conclusion_HasE_i := by
  have h := ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_polyAtom.comp (Primrec.const (encode (OrthemologyV2.Term.i)))).pair (primrec_arrCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 1))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasE_i,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasE_i_exact (Γ : P01AC.Tel) (A : P01AC.Ty) : conclusion_HasE_i (encode (Rule.HasE_i Γ A)) = encode ((Rule.HasE_i Γ A).conclusion) := by
  simp only [conclusion_HasE_i,Rule.conclusion,encode_Rule_HasE_i,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasE_k (c : Nat) : Nat := (hasCode 5 (ruleField c 0) ((polyAtom (encode (OrthemologyV2.Term.k)))) ((arrCode (ruleField c 1) ((arrCode (ruleField c 2) (ruleField c 1))))))
theorem primrec_conclusion_HasE_k : Primrec conclusion_HasE_k := by
  have h := ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_polyAtom.comp (Primrec.const (encode (OrthemologyV2.Term.k)))).pair (primrec_arrCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_arrCode.comp (primrec_ruleField.comp Primrec.id (.const 2)) (primrec_ruleField.comp Primrec.id (.const 1)))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasE_k,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasE_k_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : conclusion_HasE_k (encode (Rule.HasE_k Γ A B)) = encode ((Rule.HasE_k Γ A B).conclusion) := by
  simp only [conclusion_HasE_k,Rule.conclusion,encode_Rule_HasE_k,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasE_s (c : Nat) : Nat := (hasCode 5 (ruleField c 0) ((polyAtom (encode (OrthemologyV2.Term.s)))) ((arrCode ((arrCode (ruleField c 1) ((arrCode (ruleField c 2) (ruleField c 3))))) ((arrCode ((arrCode (ruleField c 1) (ruleField c 2))) ((arrCode (ruleField c 1) (ruleField c 3))))))))
theorem primrec_conclusion_HasE_s : Primrec conclusion_HasE_s := by
  have h := ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_polyAtom.comp (Primrec.const (encode (OrthemologyV2.Term.s)))).pair (primrec_arrCode.comp (primrec_arrCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_arrCode.comp (primrec_ruleField.comp Primrec.id (.const 2)) (primrec_ruleField.comp Primrec.id (.const 3)))) (primrec_arrCode.comp (primrec_arrCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2))) (primrec_arrCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 3))))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasE_s,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasE_s_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (C : P01AC.Ty) : conclusion_HasE_s (encode (Rule.HasE_s Γ A B C)) = encode ((Rule.HasE_s Γ A B C).conclusion) := by
  simp only [conclusion_HasE_s,Rule.conclusion,encode_Rule_HasE_s,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasE_finite (c : Nat) : Nat := (hasCode 5 (ruleField c 1) ((polyAtom (ruleField c 2))) ((tsubstTelCode (ruleField c 3) ((finCode (ruleField c 0))))))
theorem primrec_conclusion_HasE_finite : Primrec conclusion_HasE_finite := by
  have h := ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 1)).pair ((primrec_polyAtom.comp (primrec_ruleField.comp Primrec.id (.const 2))).pair (primrec_tsubstTelCode.comp (primrec_ruleField.comp Primrec.id (.const 3)) (primrec_finCode.comp (primrec_ruleField.comp Primrec.id (.const 0)))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasE_finite,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasE_finite_exact (C : OrthemologyV2.TypeCode) (Γ : P01AC.Tel) (t : OrthemologyV2.Term) (τ : List P01AC.Ty) (aux0 : AuxiliaryCertificates.FiniteCert) : conclusion_HasE_finite (encode (Rule.HasE_finite C Γ t τ aux0)) = encode ((Rule.HasE_finite C Γ t τ aux0).conclusion) := by
  simp only [conclusion_HasE_finite,Rule.conclusion,encode_Rule_HasE_finite,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasE_allIntro (c : Nat) : Nat := (hasCode 5 (ruleField c 0) (ruleField c 2) ((allTyCode (ruleField c 1))))
theorem primrec_conclusion_HasE_allIntro : Primrec conclusion_HasE_allIntro := by
  have h := ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_allTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasE_allIntro,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasE_allIntro_exact (Γ : P01AC.Tel) (B : P01AC.Ty) (p : P01D.Poly) : conclusion_HasE_allIntro (encode (Rule.HasE_allIntro Γ B p)) = encode ((Rule.HasE_allIntro Γ B p).conclusion) := by
  simp only [conclusion_HasE_allIntro,Rule.conclusion,encode_Rule_HasE_allIntro,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasE_allElim (c : Nat) : Nat := (hasCode 5 (ruleField c 0) (ruleField c 3) ((tinstCode (ruleField c 2) (ruleField c 1))))
theorem primrec_conclusion_HasE_allElim : Primrec conclusion_HasE_allElim := by
  have h := ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 3)).pair (primrec_tinstCode.comp (primrec_ruleField.comp Primrec.id (.const 2)) (primrec_ruleField.comp Primrec.id (.const 1))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasE_allElim,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasE_allElim_exact (Γ : P01AC.Tel) (B : P01AC.Ty) (A : P01AC.Ty) (p : P01D.Poly) : conclusion_HasE_allElim (encode (Rule.HasE_allElim Γ B A p)) = encode ((Rule.HasE_allElim Γ B A p).conclusion) := by
  simp only [conclusion_HasE_allElim,Rule.conclusion,encode_Rule_HasE_allElim,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasE_rawAtom (c : Nat) : Nat := (hasCode 5 (ruleField c 0) ((polyAtom (ruleField c 1))) (encode (P01AC.Ty.raw)))
theorem primrec_conclusion_HasE_rawAtom : Primrec conclusion_HasE_rawAtom := by
  have h := ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_polyAtom.comp (primrec_ruleField.comp Primrec.id (.const 1))).pair (Primrec.const (encode (P01AC.Ty.raw))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasE_rawAtom,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasE_rawAtom_exact (Γ : P01AC.Tel) (t : OrthemologyV2.Term) : conclusion_HasE_rawAtom (encode (Rule.HasE_rawAtom Γ t)) = encode ((Rule.HasE_rawAtom Γ t).conclusion) := by
  simp only [conclusion_HasE_rawAtom,Rule.conclusion,encode_Rule_HasE_rawAtom,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasE_rawApp (c : Nat) : Nat := (hasCode 5 (ruleField c 0) ((appCode (ruleField c 1) (ruleField c 2))) (encode (P01AC.Ty.raw)))
theorem primrec_conclusion_HasE_rawApp : Primrec conclusion_HasE_rawApp := by
  have h := ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_appCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2))).pair (Primrec.const (encode (P01AC.Ty.raw))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasE_rawApp,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasE_rawApp_exact (Γ : P01AC.Tel) (f : P01D.Poly) (a : P01D.Poly) : conclusion_HasE_rawApp (encode (Rule.HasE_rawApp Γ f a)) = encode ((Rule.HasE_rawApp Γ f a).conclusion) := by
  simp only [conclusion_HasE_rawApp,Rule.conclusion,encode_Rule_HasE_rawApp,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasE_piIntro (c : Nat) : Nat := (hasCode 5 (ruleField c 0) ((abstractCode (ruleField c 3))) ((piCode (ruleField c 1) (ruleField c 2))))
theorem primrec_conclusion_HasE_piIntro : Primrec conclusion_HasE_piIntro := by
  have h := ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_abstractCode.comp (primrec_ruleField.comp Primrec.id (.const 3))).pair (primrec_piCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasE_piIntro,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasE_piIntro_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (b : P01D.Poly) : conclusion_HasE_piIntro (encode (Rule.HasE_piIntro Γ A B b)) = encode ((Rule.HasE_piIntro Γ A B b).conclusion) := by
  simp only [conclusion_HasE_piIntro,Rule.conclusion,encode_Rule_HasE_piIntro,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasE_piElim (c : Nat) : Nat := (hasCode 5 (ruleField c 0) ((appCode (ruleField c 4) (ruleField c 3))) ((instTyCode (ruleField c 3) (ruleField c 2))))
theorem primrec_conclusion_HasE_piElim : Primrec conclusion_HasE_piElim := by
  have h := ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_appCode.comp (primrec_ruleField.comp Primrec.id (.const 4)) (primrec_ruleField.comp Primrec.id (.const 3))).pair (primrec_instTyCode.comp (primrec_ruleField.comp Primrec.id (.const 3)) (primrec_ruleField.comp Primrec.id (.const 2))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasE_piElim,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasE_piElim_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (a : P01D.Poly) (f : P01D.Poly) : conclusion_HasE_piElim (encode (Rule.HasE_piElim Γ A B a f)) = encode ((Rule.HasE_piElim Γ A B a f).conclusion) := by
  simp only [conclusion_HasE_piElim,Rule.conclusion,encode_Rule_HasE_piElim,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasE_sigmaIntro (c : Nat) : Nat := (hasCode 5 (ruleField c 0) ((pairPolyCode (ruleField c 3) (ruleField c 4))) ((sigmaTyCode (ruleField c 1) (ruleField c 2))))
theorem primrec_conclusion_HasE_sigmaIntro : Primrec conclusion_HasE_sigmaIntro := by
  have h := ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_pairPolyCode.comp (primrec_ruleField.comp Primrec.id (.const 3)) (primrec_ruleField.comp Primrec.id (.const 4))).pair (primrec_sigmaTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasE_sigmaIntro,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasE_sigmaIntro_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (a : P01D.Poly) (b : P01D.Poly) : conclusion_HasE_sigmaIntro (encode (Rule.HasE_sigmaIntro Γ A B a b)) = encode ((Rule.HasE_sigmaIntro Γ A B a b).conclusion) := by
  simp only [conclusion_HasE_sigmaIntro,Rule.conclusion,encode_Rule_HasE_sigmaIntro,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasE_sigmaFst (c : Nat) : Nat := (hasCode 5 (ruleField c 0) ((fstPolyCode (ruleField c 3))) (ruleField c 1))
theorem primrec_conclusion_HasE_sigmaFst : Primrec conclusion_HasE_sigmaFst := by
  have h := ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_fstPolyCode.comp (primrec_ruleField.comp Primrec.id (.const 3))).pair (primrec_ruleField.comp Primrec.id (.const 1)))))
  exact h.of_eq (by intro c; simp only [conclusion_HasE_sigmaFst,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasE_sigmaFst_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (z : P01D.Poly) : conclusion_HasE_sigmaFst (encode (Rule.HasE_sigmaFst Γ A B z)) = encode ((Rule.HasE_sigmaFst Γ A B z).conclusion) := by
  simp only [conclusion_HasE_sigmaFst,Rule.conclusion,encode_Rule_HasE_sigmaFst,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasE_sigmaSnd (c : Nat) : Nat := (hasCode 5 (ruleField c 0) ((sndPolyCode (ruleField c 3))) ((instTyCode ((fstPolyCode (ruleField c 3))) (ruleField c 2))))
theorem primrec_conclusion_HasE_sigmaSnd : Primrec conclusion_HasE_sigmaSnd := by
  have h := ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_sndPolyCode.comp (primrec_ruleField.comp Primrec.id (.const 3))).pair (primrec_instTyCode.comp (primrec_fstPolyCode.comp (primrec_ruleField.comp Primrec.id (.const 3))) (primrec_ruleField.comp Primrec.id (.const 2))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasE_sigmaSnd,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasE_sigmaSnd_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (z : P01D.Poly) : conclusion_HasE_sigmaSnd (encode (Rule.HasE_sigmaSnd Γ A B z)) = encode ((Rule.HasE_sigmaSnd Γ A B z).conclusion) := by
  simp only [conclusion_HasE_sigmaSnd,Rule.conclusion,encode_Rule_HasE_sigmaSnd,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasE_identityIntro (c : Nat) : Nat := (hasCode 5 (ruleField c 0) ((polyAtom (encode (OrthemologyV2.Term.i)))) ((identityTyCode (ruleField c 1) (ruleField c 2) (ruleField c 3))))
theorem primrec_conclusion_HasE_identityIntro : Primrec conclusion_HasE_identityIntro := by
  have h := ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_polyAtom.comp (Primrec.const (encode (OrthemologyV2.Term.i)))).pair (primrec_identityTyCode.comp ((primrec_ruleField.comp Primrec.id (.const 1)).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 3))))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasE_identityIntro,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasE_identityIntro_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (aux0 : AuxiliaryCertificates.PolyCert) : conclusion_HasE_identityIntro (encode (Rule.HasE_identityIntro Γ A p q aux0)) = encode ((Rule.HasE_identityIntro Γ A p q aux0).conclusion) := by
  simp only [conclusion_HasE_identityIntro,Rule.conclusion,encode_Rule_HasE_identityIntro,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasE_proofErase (c : Nat) : Nat := (hasCode 5 (ruleField c 0) (ruleField c 4) (encode (P01AC.Ty.raw)))
theorem primrec_conclusion_HasE_proofErase : Primrec conclusion_HasE_proofErase := by
  have h := ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 4)).pair (Primrec.const (encode (P01AC.Ty.raw))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasE_proofErase,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasE_proofErase_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (x : P01D.Poly) (y : P01D.Poly) (p : P01D.Poly) : conclusion_HasE_proofErase (encode (Rule.HasE_proofErase Γ A x y p)) = encode ((Rule.HasE_proofErase Γ A x y p).conclusion) := by
  simp only [conclusion_HasE_proofErase,Rule.conclusion,encode_Rule_HasE_proofErase,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasE_j (c : Nat) : Nat := (hasCode 5 (ruleField c 0) ((jPolyCode (ruleField c 6) (ruleField c 4) (ruleField c 5))) ((motiveAtCode (ruleField c 3) (ruleField c 4) (ruleField c 5))))
theorem primrec_conclusion_HasE_j : Primrec conclusion_HasE_j := by
  have h := ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_jPolyCode.comp ((primrec_ruleField.comp Primrec.id (.const 6)).pair ((primrec_ruleField.comp Primrec.id (.const 4)).pair (primrec_ruleField.comp Primrec.id (.const 5))))).pair (primrec_motiveAtCode.comp ((primrec_ruleField.comp Primrec.id (.const 3)).pair ((primrec_ruleField.comp Primrec.id (.const 4)).pair (primrec_ruleField.comp Primrec.id (.const 5))))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasE_j,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasE_j_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (x : P01D.Poly) (B : P01AC.Ty) (y : P01D.Poly) (e : P01D.Poly) (d : P01D.Poly) : conclusion_HasE_j (encode (Rule.HasE_j Γ A x B y e d)) = encode ((Rule.HasE_j Γ A x B y e d).conclusion) := by
  simp only [conclusion_HasE_j,Rule.conclusion,encode_Rule_HasE_j,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasE_conv (c : Nat) : Nat := (hasCode 5 (ruleField c 0) (ruleField c 3) (ruleField c 1))
theorem primrec_conclusion_HasE_conv : Primrec conclusion_HasE_conv := by
  have h := ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_ruleField.comp Primrec.id (.const 3)).pair (primrec_ruleField.comp Primrec.id (.const 1)))))
  exact h.of_eq (by intro c; simp only [conclusion_HasE_conv,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasE_conv_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (aux0 : AuxiliaryCertificates.PolyCert) : conclusion_HasE_conv (encode (Rule.HasE_conv Γ A p q aux0)) = encode ((Rule.HasE_conv Γ A p q aux0).conclusion) := by
  simp only [conclusion_HasE_conv,Rule.conclusion,encode_Rule_HasE_conv,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasE_piExt (c : Nat) : Nat := (hasCode 5 (ruleField c 0) ((polyAtom (encode (OrthemologyV2.Term.i)))) ((identityTyCode ((piCode (ruleField c 1) (ruleField c 2))) (ruleField c 3) (ruleField c 4))))
theorem primrec_conclusion_HasE_piExt : Primrec conclusion_HasE_piExt := by
  have h := ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_polyAtom.comp (Primrec.const (encode (OrthemologyV2.Term.i)))).pair (primrec_identityTyCode.comp ((primrec_piCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 2))).pair ((primrec_ruleField.comp Primrec.id (.const 3)).pair (primrec_ruleField.comp Primrec.id (.const 4))))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasE_piExt,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasE_piExt_exact (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (h : P01D.Poly) : conclusion_HasE_piExt (encode (Rule.HasE_piExt Γ A B p q h)) = encode ((Rule.HasE_piExt Γ A B p q h).conclusion) := by
  simp only [conclusion_HasE_piExt,Rule.conclusion,encode_Rule_HasE_piExt,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusion_HasE_allExt (c : Nat) : Nat := (hasCode 5 (ruleField c 0) ((polyAtom (encode (OrthemologyV2.Term.i)))) ((identityTyCode ((allTyCode (ruleField c 1))) (ruleField c 2) (ruleField c 3))))
theorem primrec_conclusion_HasE_allExt : Primrec conclusion_HasE_allExt := by
  have h := ((primrec_hasCode 5).comp ((primrec_ruleField.comp Primrec.id (.const 0)).pair ((primrec_polyAtom.comp (Primrec.const (encode (OrthemologyV2.Term.i)))).pair (primrec_identityTyCode.comp ((primrec_allTyCode.comp (primrec_ruleField.comp Primrec.id (.const 1))).pair ((primrec_ruleField.comp Primrec.id (.const 2)).pair (primrec_ruleField.comp Primrec.id (.const 3))))))))
  exact h.of_eq (by intro c; simp only [conclusion_HasE_allExt,id,Nat.succ_eq_add_one,List.append_eq])
@[simp] theorem conclusion_HasE_allExt_exact (Γ : P01AC.Tel) (B : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (h : P01D.Poly) : conclusion_HasE_allExt (encode (Rule.HasE_allExt Γ B p q h)) = encode ((Rule.HasE_allExt Γ B p q h).conclusion) := by
  simp only [conclusion_HasE_allExt,Rule.conclusion,encode_Rule_HasE_allExt,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat,polyAtom_exact,varCode_exact,paramCode_exact,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append,List.append_eq]

def conclusionDispatch62 (c : Nat) : Nat := if tag c = 62 then conclusion_HasE_allExt c else 0
theorem primrec_conclusionDispatch62 : Primrec conclusionDispatch62 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 62)) primrec_conclusion_HasE_allExt (.const 0)

def conclusionDispatch61 (c : Nat) : Nat := if tag c = 61 then conclusion_HasE_piExt c else conclusionDispatch62 c
theorem primrec_conclusionDispatch61 : Primrec conclusionDispatch61 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 61)) primrec_conclusion_HasE_piExt primrec_conclusionDispatch62

def conclusionDispatch60 (c : Nat) : Nat := if tag c = 60 then conclusion_HasE_conv c else conclusionDispatch61 c
theorem primrec_conclusionDispatch60 : Primrec conclusionDispatch60 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 60)) primrec_conclusion_HasE_conv primrec_conclusionDispatch61

def conclusionDispatch59 (c : Nat) : Nat := if tag c = 59 then conclusion_HasE_j c else conclusionDispatch60 c
theorem primrec_conclusionDispatch59 : Primrec conclusionDispatch59 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 59)) primrec_conclusion_HasE_j primrec_conclusionDispatch60

def conclusionDispatch58 (c : Nat) : Nat := if tag c = 58 then conclusion_HasE_proofErase c else conclusionDispatch59 c
theorem primrec_conclusionDispatch58 : Primrec conclusionDispatch58 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 58)) primrec_conclusion_HasE_proofErase primrec_conclusionDispatch59

def conclusionDispatch57 (c : Nat) : Nat := if tag c = 57 then conclusion_HasE_identityIntro c else conclusionDispatch58 c
theorem primrec_conclusionDispatch57 : Primrec conclusionDispatch57 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 57)) primrec_conclusion_HasE_identityIntro primrec_conclusionDispatch58

def conclusionDispatch56 (c : Nat) : Nat := if tag c = 56 then conclusion_HasE_sigmaSnd c else conclusionDispatch57 c
theorem primrec_conclusionDispatch56 : Primrec conclusionDispatch56 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 56)) primrec_conclusion_HasE_sigmaSnd primrec_conclusionDispatch57

def conclusionDispatch55 (c : Nat) : Nat := if tag c = 55 then conclusion_HasE_sigmaFst c else conclusionDispatch56 c
theorem primrec_conclusionDispatch55 : Primrec conclusionDispatch55 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 55)) primrec_conclusion_HasE_sigmaFst primrec_conclusionDispatch56

def conclusionDispatch54 (c : Nat) : Nat := if tag c = 54 then conclusion_HasE_sigmaIntro c else conclusionDispatch55 c
theorem primrec_conclusionDispatch54 : Primrec conclusionDispatch54 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 54)) primrec_conclusion_HasE_sigmaIntro primrec_conclusionDispatch55

def conclusionDispatch53 (c : Nat) : Nat := if tag c = 53 then conclusion_HasE_piElim c else conclusionDispatch54 c
theorem primrec_conclusionDispatch53 : Primrec conclusionDispatch53 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 53)) primrec_conclusion_HasE_piElim primrec_conclusionDispatch54

def conclusionDispatch52 (c : Nat) : Nat := if tag c = 52 then conclusion_HasE_piIntro c else conclusionDispatch53 c
theorem primrec_conclusionDispatch52 : Primrec conclusionDispatch52 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 52)) primrec_conclusion_HasE_piIntro primrec_conclusionDispatch53

def conclusionDispatch51 (c : Nat) : Nat := if tag c = 51 then conclusion_HasE_rawApp c else conclusionDispatch52 c
theorem primrec_conclusionDispatch51 : Primrec conclusionDispatch51 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 51)) primrec_conclusion_HasE_rawApp primrec_conclusionDispatch52

def conclusionDispatch50 (c : Nat) : Nat := if tag c = 50 then conclusion_HasE_rawAtom c else conclusionDispatch51 c
theorem primrec_conclusionDispatch50 : Primrec conclusionDispatch50 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 50)) primrec_conclusion_HasE_rawAtom primrec_conclusionDispatch51

def conclusionDispatch49 (c : Nat) : Nat := if tag c = 49 then conclusion_HasE_allElim c else conclusionDispatch50 c
theorem primrec_conclusionDispatch49 : Primrec conclusionDispatch49 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 49)) primrec_conclusion_HasE_allElim primrec_conclusionDispatch50

def conclusionDispatch48 (c : Nat) : Nat := if tag c = 48 then conclusion_HasE_allIntro c else conclusionDispatch49 c
theorem primrec_conclusionDispatch48 : Primrec conclusionDispatch48 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 48)) primrec_conclusion_HasE_allIntro primrec_conclusionDispatch49

def conclusionDispatch47 (c : Nat) : Nat := if tag c = 47 then conclusion_HasE_finite c else conclusionDispatch48 c
theorem primrec_conclusionDispatch47 : Primrec conclusionDispatch47 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 47)) primrec_conclusion_HasE_finite primrec_conclusionDispatch48

def conclusionDispatch46 (c : Nat) : Nat := if tag c = 46 then conclusion_HasE_s c else conclusionDispatch47 c
theorem primrec_conclusionDispatch46 : Primrec conclusionDispatch46 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 46)) primrec_conclusion_HasE_s primrec_conclusionDispatch47

def conclusionDispatch45 (c : Nat) : Nat := if tag c = 45 then conclusion_HasE_k c else conclusionDispatch46 c
theorem primrec_conclusionDispatch45 : Primrec conclusionDispatch45 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 45)) primrec_conclusion_HasE_k primrec_conclusionDispatch46

def conclusionDispatch44 (c : Nat) : Nat := if tag c = 44 then conclusion_HasE_i c else conclusionDispatch45 c
theorem primrec_conclusionDispatch44 : Primrec conclusionDispatch44 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 44)) primrec_conclusion_HasE_i primrec_conclusionDispatch45

def conclusionDispatch43 (c : Nat) : Nat := if tag c = 43 then conclusion_HasE_var c else conclusionDispatch44 c
theorem primrec_conclusionDispatch43 : Primrec conclusionDispatch43 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 43)) primrec_conclusion_HasE_var primrec_conclusionDispatch44

def conclusionDispatch42 (c : Nat) : Nat := if tag c = 42 then conclusion_FormE_identity c else conclusionDispatch43 c
theorem primrec_conclusionDispatch42 : Primrec conclusionDispatch42 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 42)) primrec_conclusion_FormE_identity primrec_conclusionDispatch43

def conclusionDispatch41 (c : Nat) : Nat := if tag c = 41 then conclusion_FormE_sigma c else conclusionDispatch42 c
theorem primrec_conclusionDispatch41 : Primrec conclusionDispatch41 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 41)) primrec_conclusion_FormE_sigma primrec_conclusionDispatch42

def conclusionDispatch40 (c : Nat) : Nat := if tag c = 40 then conclusion_FormE_pi c else conclusionDispatch41 c
theorem primrec_conclusionDispatch40 : Primrec conclusionDispatch40 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 40)) primrec_conclusion_FormE_pi primrec_conclusionDispatch41

def conclusionDispatch39 (c : Nat) : Nat := if tag c = 39 then conclusion_FormE_raw c else conclusionDispatch40 c
theorem primrec_conclusionDispatch39 : Primrec conclusionDispatch39 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 39)) primrec_conclusion_FormE_raw primrec_conclusionDispatch40

def conclusionDispatch38 (c : Nat) : Nat := if tag c = 38 then conclusion_FormE_all c else conclusionDispatch39 c
theorem primrec_conclusionDispatch38 : Primrec conclusionDispatch38 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 38)) primrec_conclusion_FormE_all primrec_conclusionDispatch39

def conclusionDispatch37 (c : Nat) : Nat := if tag c = 37 then conclusion_FormE_bottom c else conclusionDispatch38 c
theorem primrec_conclusionDispatch37 : Primrec conclusionDispatch37 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 37)) primrec_conclusion_FormE_bottom primrec_conclusionDispatch38

def conclusionDispatch36 (c : Nat) : Nat := if tag c = 36 then conclusion_FormE_param c else conclusionDispatch37 c
theorem primrec_conclusionDispatch36 : Primrec conclusionDispatch36 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 36)) primrec_conclusion_FormE_param primrec_conclusionDispatch37

def conclusionDispatch35 (c : Nat) : Nat := if tag c = 35 then conclusion_CtxE_ext c else conclusionDispatch36 c
theorem primrec_conclusionDispatch35 : Primrec conclusionDispatch35 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 35)) primrec_conclusion_CtxE_ext primrec_conclusionDispatch36

def conclusionDispatch34 (c : Nat) : Nat := if tag c = 34 then conclusion_CtxE_nil c else conclusionDispatch35 c
theorem primrec_conclusionDispatch34 : Primrec conclusionDispatch34 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 34)) primrec_conclusion_CtxE_nil primrec_conclusionDispatch35

def conclusionDispatch33 (c : Nat) : Nat := if tag c = 33 then conclusion_HasJ_natInduction c else conclusionDispatch34 c
theorem primrec_conclusionDispatch33 : Primrec conclusionDispatch33 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 33)) primrec_conclusion_HasJ_natInduction primrec_conclusionDispatch34

def conclusionDispatch32 (c : Nat) : Nat := if tag c = 32 then conclusion_HasJ_sigmaElim c else conclusionDispatch33 c
theorem primrec_conclusionDispatch32 : Primrec conclusionDispatch32 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 32)) primrec_conclusion_HasJ_sigmaElim primrec_conclusionDispatch33

def conclusionDispatch31 (c : Nat) : Nat := if tag c = 31 then conclusion_HasJ_allExt c else conclusionDispatch32 c
theorem primrec_conclusionDispatch31 : Primrec conclusionDispatch31 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 31)) primrec_conclusion_HasJ_allExt primrec_conclusionDispatch32

def conclusionDispatch30 (c : Nat) : Nat := if tag c = 30 then conclusion_HasJ_piExt c else conclusionDispatch31 c
theorem primrec_conclusionDispatch30 : Primrec conclusionDispatch30 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 30)) primrec_conclusion_HasJ_piExt primrec_conclusionDispatch31

def conclusionDispatch29 (c : Nat) : Nat := if tag c = 29 then conclusion_HasJ_conv c else conclusionDispatch30 c
theorem primrec_conclusionDispatch29 : Primrec conclusionDispatch29 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 29)) primrec_conclusion_HasJ_conv primrec_conclusionDispatch30

def conclusionDispatch28 (c : Nat) : Nat := if tag c = 28 then conclusion_HasJ_j c else conclusionDispatch29 c
theorem primrec_conclusionDispatch28 : Primrec conclusionDispatch28 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 28)) primrec_conclusion_HasJ_j primrec_conclusionDispatch29

def conclusionDispatch27 (c : Nat) : Nat := if tag c = 27 then conclusion_HasJ_proofErase c else conclusionDispatch28 c
theorem primrec_conclusionDispatch27 : Primrec conclusionDispatch27 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 27)) primrec_conclusion_HasJ_proofErase primrec_conclusionDispatch28

def conclusionDispatch26 (c : Nat) : Nat := if tag c = 26 then conclusion_HasJ_identityIntro c else conclusionDispatch27 c
theorem primrec_conclusionDispatch26 : Primrec conclusionDispatch26 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 26)) primrec_conclusion_HasJ_identityIntro primrec_conclusionDispatch27

def conclusionDispatch25 (c : Nat) : Nat := if tag c = 25 then conclusion_HasJ_sigmaSnd c else conclusionDispatch26 c
theorem primrec_conclusionDispatch25 : Primrec conclusionDispatch25 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 25)) primrec_conclusion_HasJ_sigmaSnd primrec_conclusionDispatch26

def conclusionDispatch24 (c : Nat) : Nat := if tag c = 24 then conclusion_HasJ_sigmaFst c else conclusionDispatch25 c
theorem primrec_conclusionDispatch24 : Primrec conclusionDispatch24 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 24)) primrec_conclusion_HasJ_sigmaFst primrec_conclusionDispatch25

def conclusionDispatch23 (c : Nat) : Nat := if tag c = 23 then conclusion_HasJ_sigmaIntro c else conclusionDispatch24 c
theorem primrec_conclusionDispatch23 : Primrec conclusionDispatch23 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 23)) primrec_conclusion_HasJ_sigmaIntro primrec_conclusionDispatch24

def conclusionDispatch22 (c : Nat) : Nat := if tag c = 22 then conclusion_HasJ_piElim c else conclusionDispatch23 c
theorem primrec_conclusionDispatch22 : Primrec conclusionDispatch22 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 22)) primrec_conclusion_HasJ_piElim primrec_conclusionDispatch23

def conclusionDispatch21 (c : Nat) : Nat := if tag c = 21 then conclusion_HasJ_piIntro c else conclusionDispatch22 c
theorem primrec_conclusionDispatch21 : Primrec conclusionDispatch21 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 21)) primrec_conclusion_HasJ_piIntro primrec_conclusionDispatch22

def conclusionDispatch20 (c : Nat) : Nat := if tag c = 20 then conclusion_HasJ_rawApp c else conclusionDispatch21 c
theorem primrec_conclusionDispatch20 : Primrec conclusionDispatch20 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 20)) primrec_conclusion_HasJ_rawApp primrec_conclusionDispatch21

def conclusionDispatch19 (c : Nat) : Nat := if tag c = 19 then conclusion_HasJ_rawAtom c else conclusionDispatch20 c
theorem primrec_conclusionDispatch19 : Primrec conclusionDispatch19 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 19)) primrec_conclusion_HasJ_rawAtom primrec_conclusionDispatch20

def conclusionDispatch18 (c : Nat) : Nat := if tag c = 18 then conclusion_HasJ_allElim c else conclusionDispatch19 c
theorem primrec_conclusionDispatch18 : Primrec conclusionDispatch18 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 18)) primrec_conclusion_HasJ_allElim primrec_conclusionDispatch19

def conclusionDispatch17 (c : Nat) : Nat := if tag c = 17 then conclusion_HasJ_allIntro c else conclusionDispatch18 c
theorem primrec_conclusionDispatch17 : Primrec conclusionDispatch17 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 17)) primrec_conclusion_HasJ_allIntro primrec_conclusionDispatch18

def conclusionDispatch16 (c : Nat) : Nat := if tag c = 16 then conclusion_HasJ_finite c else conclusionDispatch17 c
theorem primrec_conclusionDispatch16 : Primrec conclusionDispatch16 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 16)) primrec_conclusion_HasJ_finite primrec_conclusionDispatch17

def conclusionDispatch15 (c : Nat) : Nat := if tag c = 15 then conclusion_HasJ_s c else conclusionDispatch16 c
theorem primrec_conclusionDispatch15 : Primrec conclusionDispatch15 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 15)) primrec_conclusion_HasJ_s primrec_conclusionDispatch16

def conclusionDispatch14 (c : Nat) : Nat := if tag c = 14 then conclusion_HasJ_k c else conclusionDispatch15 c
theorem primrec_conclusionDispatch14 : Primrec conclusionDispatch14 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 14)) primrec_conclusion_HasJ_k primrec_conclusionDispatch15

def conclusionDispatch13 (c : Nat) : Nat := if tag c = 13 then conclusion_HasJ_i c else conclusionDispatch14 c
theorem primrec_conclusionDispatch13 : Primrec conclusionDispatch13 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 13)) primrec_conclusion_HasJ_i primrec_conclusionDispatch14

def conclusionDispatch12 (c : Nat) : Nat := if tag c = 12 then conclusion_HasJ_var c else conclusionDispatch13 c
theorem primrec_conclusionDispatch12 : Primrec conclusionDispatch12 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 12)) primrec_conclusion_HasJ_var primrec_conclusionDispatch13

def conclusionDispatch11 (c : Nat) : Nat := if tag c = 11 then conclusion_HasJ_hasBase c else conclusionDispatch12 c
theorem primrec_conclusionDispatch11 : Primrec conclusionDispatch11 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 11)) primrec_conclusion_HasJ_hasBase primrec_conclusionDispatch12

def conclusionDispatch10 (c : Nat) : Nat := if tag c = 10 then conclusion_FormJ_identity c else conclusionDispatch11 c
theorem primrec_conclusionDispatch10 : Primrec conclusionDispatch10 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 10)) primrec_conclusion_FormJ_identity primrec_conclusionDispatch11

def conclusionDispatch9 (c : Nat) : Nat := if tag c = 9 then conclusion_FormJ_sigma c else conclusionDispatch10 c
theorem primrec_conclusionDispatch9 : Primrec conclusionDispatch9 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 9)) primrec_conclusion_FormJ_sigma primrec_conclusionDispatch10

def conclusionDispatch8 (c : Nat) : Nat := if tag c = 8 then conclusion_FormJ_pi c else conclusionDispatch9 c
theorem primrec_conclusionDispatch8 : Primrec conclusionDispatch8 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 8)) primrec_conclusion_FormJ_pi primrec_conclusionDispatch9

def conclusionDispatch7 (c : Nat) : Nat := if tag c = 7 then conclusion_FormJ_raw c else conclusionDispatch8 c
theorem primrec_conclusionDispatch7 : Primrec conclusionDispatch7 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 7)) primrec_conclusion_FormJ_raw primrec_conclusionDispatch8

def conclusionDispatch6 (c : Nat) : Nat := if tag c = 6 then conclusion_FormJ_all c else conclusionDispatch7 c
theorem primrec_conclusionDispatch6 : Primrec conclusionDispatch6 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 6)) primrec_conclusion_FormJ_all primrec_conclusionDispatch7

def conclusionDispatch5 (c : Nat) : Nat := if tag c = 5 then conclusion_FormJ_bottom c else conclusionDispatch6 c
theorem primrec_conclusionDispatch5 : Primrec conclusionDispatch5 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 5)) primrec_conclusion_FormJ_bottom primrec_conclusionDispatch6

def conclusionDispatch4 (c : Nat) : Nat := if tag c = 4 then conclusion_FormJ_param c else conclusionDispatch5 c
theorem primrec_conclusionDispatch4 : Primrec conclusionDispatch4 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 4)) primrec_conclusion_FormJ_param primrec_conclusionDispatch5

def conclusionDispatch3 (c : Nat) : Nat := if tag c = 3 then conclusion_FormJ_formBase c else conclusionDispatch4 c
theorem primrec_conclusionDispatch3 : Primrec conclusionDispatch3 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 3)) primrec_conclusion_FormJ_formBase primrec_conclusionDispatch4

def conclusionDispatch2 (c : Nat) : Nat := if tag c = 2 then conclusion_CtxJ_ext c else conclusionDispatch3 c
theorem primrec_conclusionDispatch2 : Primrec conclusionDispatch2 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 2)) primrec_conclusion_CtxJ_ext primrec_conclusionDispatch3

def conclusionDispatch1 (c : Nat) : Nat := if tag c = 1 then conclusion_CtxJ_nil c else conclusionDispatch2 c
theorem primrec_conclusionDispatch1 : Primrec conclusionDispatch1 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 1)) primrec_conclusion_CtxJ_nil primrec_conclusionDispatch2

def conclusionDispatch0 (c : Nat) : Nat := if tag c = 0 then conclusion_CtxJ_ctxBase c else conclusionDispatch1 c
theorem primrec_conclusionDispatch0 : Primrec conclusionDispatch0 :=
  Primrec.ite (Primrec.eq.comp primrec_tag (.const 0)) primrec_conclusion_CtxJ_ctxBase primrec_conclusionDispatch1

def conclusionCode := conclusionDispatch0
theorem primrec_conclusionCode : Primrec conclusionCode := primrec_conclusionDispatch0
@[simp] theorem conclusionCode_CtxJ_ctxBase (Γ : P01AC.Tel) : conclusionCode (encode (Rule.CtxJ_ctxBase Γ)) = conclusion_CtxJ_ctxBase (encode (Rule.CtxJ_ctxBase Γ)) := by
  have ht : tag (encode (Rule.CtxJ_ctxBase Γ)) = 0 := by rw [encode_Rule_CtxJ_ctxBase]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_CtxJ_nil  : conclusionCode (encode (Rule.CtxJ_nil )) = conclusion_CtxJ_nil (encode (Rule.CtxJ_nil )) := by
  have ht : tag (encode (Rule.CtxJ_nil )) = 1 := by rw [encode_Rule_CtxJ_nil]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_CtxJ_ext (Γ : P01AC.Tel) (A : P01AC.Ty) : conclusionCode (encode (Rule.CtxJ_ext Γ A)) = conclusion_CtxJ_ext (encode (Rule.CtxJ_ext Γ A)) := by
  have ht : tag (encode (Rule.CtxJ_ext Γ A)) = 2 := by rw [encode_Rule_CtxJ_ext]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_FormJ_formBase (Γ : P01AC.Tel) (A : P01AC.Ty) : conclusionCode (encode (Rule.FormJ_formBase Γ A)) = conclusion_FormJ_formBase (encode (Rule.FormJ_formBase Γ A)) := by
  have ht : tag (encode (Rule.FormJ_formBase Γ A)) = 3 := by rw [encode_Rule_FormJ_formBase]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_FormJ_param (Γ : P01AC.Tel) (n : Nat) : conclusionCode (encode (Rule.FormJ_param Γ n)) = conclusion_FormJ_param (encode (Rule.FormJ_param Γ n)) := by
  have ht : tag (encode (Rule.FormJ_param Γ n)) = 4 := by rw [encode_Rule_FormJ_param]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_FormJ_bottom (Γ : P01AC.Tel) : conclusionCode (encode (Rule.FormJ_bottom Γ)) = conclusion_FormJ_bottom (encode (Rule.FormJ_bottom Γ)) := by
  have ht : tag (encode (Rule.FormJ_bottom Γ)) = 5 := by rw [encode_Rule_FormJ_bottom]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_FormJ_all (Γ : P01AC.Tel) (B : P01AC.Ty) : conclusionCode (encode (Rule.FormJ_all Γ B)) = conclusion_FormJ_all (encode (Rule.FormJ_all Γ B)) := by
  have ht : tag (encode (Rule.FormJ_all Γ B)) = 6 := by rw [encode_Rule_FormJ_all]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_FormJ_raw (Γ : P01AC.Tel) : conclusionCode (encode (Rule.FormJ_raw Γ)) = conclusion_FormJ_raw (encode (Rule.FormJ_raw Γ)) := by
  have ht : tag (encode (Rule.FormJ_raw Γ)) = 7 := by rw [encode_Rule_FormJ_raw]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_FormJ_pi (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : conclusionCode (encode (Rule.FormJ_pi Γ A B)) = conclusion_FormJ_pi (encode (Rule.FormJ_pi Γ A B)) := by
  have ht : tag (encode (Rule.FormJ_pi Γ A B)) = 8 := by rw [encode_Rule_FormJ_pi]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_FormJ_sigma (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : conclusionCode (encode (Rule.FormJ_sigma Γ A B)) = conclusion_FormJ_sigma (encode (Rule.FormJ_sigma Γ A B)) := by
  have ht : tag (encode (Rule.FormJ_sigma Γ A B)) = 9 := by rw [encode_Rule_FormJ_sigma]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_FormJ_identity (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) : conclusionCode (encode (Rule.FormJ_identity Γ A p q)) = conclusion_FormJ_identity (encode (Rule.FormJ_identity Γ A p q)) := by
  have ht : tag (encode (Rule.FormJ_identity Γ A p q)) = 10 := by rw [encode_Rule_FormJ_identity]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasJ_hasBase (Γ : P01AC.Tel) (p : P01D.Poly) (A : P01AC.Ty) : conclusionCode (encode (Rule.HasJ_hasBase Γ p A)) = conclusion_HasJ_hasBase (encode (Rule.HasJ_hasBase Γ p A)) := by
  have ht : tag (encode (Rule.HasJ_hasBase Γ p A)) = 11 := by rw [encode_Rule_HasJ_hasBase]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasJ_var (Γ : P01AC.Tel) (A : P01AC.Ty) (n : Nat) (aux0 : AuxiliaryCertificates.LookupCert) : conclusionCode (encode (Rule.HasJ_var Γ A n aux0)) = conclusion_HasJ_var (encode (Rule.HasJ_var Γ A n aux0)) := by
  have ht : tag (encode (Rule.HasJ_var Γ A n aux0)) = 12 := by rw [encode_Rule_HasJ_var]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasJ_i (Γ : P01AC.Tel) (A : P01AC.Ty) : conclusionCode (encode (Rule.HasJ_i Γ A)) = conclusion_HasJ_i (encode (Rule.HasJ_i Γ A)) := by
  have ht : tag (encode (Rule.HasJ_i Γ A)) = 13 := by rw [encode_Rule_HasJ_i]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasJ_k (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : conclusionCode (encode (Rule.HasJ_k Γ A B)) = conclusion_HasJ_k (encode (Rule.HasJ_k Γ A B)) := by
  have ht : tag (encode (Rule.HasJ_k Γ A B)) = 14 := by rw [encode_Rule_HasJ_k]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasJ_s (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (C : P01AC.Ty) : conclusionCode (encode (Rule.HasJ_s Γ A B C)) = conclusion_HasJ_s (encode (Rule.HasJ_s Γ A B C)) := by
  have ht : tag (encode (Rule.HasJ_s Γ A B C)) = 15 := by rw [encode_Rule_HasJ_s]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasJ_finite (C : OrthemologyV2.TypeCode) (Γ : P01AC.Tel) (t : OrthemologyV2.Term) (τ : List P01AC.Ty) (aux0 : AuxiliaryCertificates.FiniteCert) : conclusionCode (encode (Rule.HasJ_finite C Γ t τ aux0)) = conclusion_HasJ_finite (encode (Rule.HasJ_finite C Γ t τ aux0)) := by
  have ht : tag (encode (Rule.HasJ_finite C Γ t τ aux0)) = 16 := by rw [encode_Rule_HasJ_finite]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasJ_allIntro (Γ : P01AC.Tel) (B : P01AC.Ty) (p : P01D.Poly) : conclusionCode (encode (Rule.HasJ_allIntro Γ B p)) = conclusion_HasJ_allIntro (encode (Rule.HasJ_allIntro Γ B p)) := by
  have ht : tag (encode (Rule.HasJ_allIntro Γ B p)) = 17 := by rw [encode_Rule_HasJ_allIntro]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasJ_allElim (Γ : P01AC.Tel) (B : P01AC.Ty) (A : P01AC.Ty) (p : P01D.Poly) : conclusionCode (encode (Rule.HasJ_allElim Γ B A p)) = conclusion_HasJ_allElim (encode (Rule.HasJ_allElim Γ B A p)) := by
  have ht : tag (encode (Rule.HasJ_allElim Γ B A p)) = 18 := by rw [encode_Rule_HasJ_allElim]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasJ_rawAtom (Γ : P01AC.Tel) (t : OrthemologyV2.Term) : conclusionCode (encode (Rule.HasJ_rawAtom Γ t)) = conclusion_HasJ_rawAtom (encode (Rule.HasJ_rawAtom Γ t)) := by
  have ht : tag (encode (Rule.HasJ_rawAtom Γ t)) = 19 := by rw [encode_Rule_HasJ_rawAtom]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasJ_rawApp (Γ : P01AC.Tel) (f : P01D.Poly) (a : P01D.Poly) : conclusionCode (encode (Rule.HasJ_rawApp Γ f a)) = conclusion_HasJ_rawApp (encode (Rule.HasJ_rawApp Γ f a)) := by
  have ht : tag (encode (Rule.HasJ_rawApp Γ f a)) = 20 := by rw [encode_Rule_HasJ_rawApp]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasJ_piIntro (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (b : P01D.Poly) : conclusionCode (encode (Rule.HasJ_piIntro Γ A B b)) = conclusion_HasJ_piIntro (encode (Rule.HasJ_piIntro Γ A B b)) := by
  have ht : tag (encode (Rule.HasJ_piIntro Γ A B b)) = 21 := by rw [encode_Rule_HasJ_piIntro]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasJ_piElim (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (a : P01D.Poly) (f : P01D.Poly) : conclusionCode (encode (Rule.HasJ_piElim Γ A B a f)) = conclusion_HasJ_piElim (encode (Rule.HasJ_piElim Γ A B a f)) := by
  have ht : tag (encode (Rule.HasJ_piElim Γ A B a f)) = 22 := by rw [encode_Rule_HasJ_piElim]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasJ_sigmaIntro (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (a : P01D.Poly) (b : P01D.Poly) : conclusionCode (encode (Rule.HasJ_sigmaIntro Γ A B a b)) = conclusion_HasJ_sigmaIntro (encode (Rule.HasJ_sigmaIntro Γ A B a b)) := by
  have ht : tag (encode (Rule.HasJ_sigmaIntro Γ A B a b)) = 23 := by rw [encode_Rule_HasJ_sigmaIntro]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasJ_sigmaFst (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (z : P01D.Poly) : conclusionCode (encode (Rule.HasJ_sigmaFst Γ A B z)) = conclusion_HasJ_sigmaFst (encode (Rule.HasJ_sigmaFst Γ A B z)) := by
  have ht : tag (encode (Rule.HasJ_sigmaFst Γ A B z)) = 24 := by rw [encode_Rule_HasJ_sigmaFst]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasJ_sigmaSnd (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (z : P01D.Poly) : conclusionCode (encode (Rule.HasJ_sigmaSnd Γ A B z)) = conclusion_HasJ_sigmaSnd (encode (Rule.HasJ_sigmaSnd Γ A B z)) := by
  have ht : tag (encode (Rule.HasJ_sigmaSnd Γ A B z)) = 25 := by rw [encode_Rule_HasJ_sigmaSnd]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasJ_identityIntro (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (aux0 : AuxiliaryCertificates.PolyCert) : conclusionCode (encode (Rule.HasJ_identityIntro Γ A p q aux0)) = conclusion_HasJ_identityIntro (encode (Rule.HasJ_identityIntro Γ A p q aux0)) := by
  have ht : tag (encode (Rule.HasJ_identityIntro Γ A p q aux0)) = 26 := by rw [encode_Rule_HasJ_identityIntro]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasJ_proofErase (Γ : P01AC.Tel) (A : P01AC.Ty) (x : P01D.Poly) (y : P01D.Poly) (p : P01D.Poly) : conclusionCode (encode (Rule.HasJ_proofErase Γ A x y p)) = conclusion_HasJ_proofErase (encode (Rule.HasJ_proofErase Γ A x y p)) := by
  have ht : tag (encode (Rule.HasJ_proofErase Γ A x y p)) = 27 := by rw [encode_Rule_HasJ_proofErase]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasJ_j (Γ : P01AC.Tel) (A : P01AC.Ty) (x : P01D.Poly) (B : P01AC.Ty) (y : P01D.Poly) (e : P01D.Poly) (d : P01D.Poly) : conclusionCode (encode (Rule.HasJ_j Γ A x B y e d)) = conclusion_HasJ_j (encode (Rule.HasJ_j Γ A x B y e d)) := by
  have ht : tag (encode (Rule.HasJ_j Γ A x B y e d)) = 28 := by rw [encode_Rule_HasJ_j]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasJ_conv (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (aux0 : AuxiliaryCertificates.PolyCert) : conclusionCode (encode (Rule.HasJ_conv Γ A p q aux0)) = conclusion_HasJ_conv (encode (Rule.HasJ_conv Γ A p q aux0)) := by
  have ht : tag (encode (Rule.HasJ_conv Γ A p q aux0)) = 29 := by rw [encode_Rule_HasJ_conv]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasJ_piExt (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (h : P01D.Poly) : conclusionCode (encode (Rule.HasJ_piExt Γ A B p q h)) = conclusion_HasJ_piExt (encode (Rule.HasJ_piExt Γ A B p q h)) := by
  have ht : tag (encode (Rule.HasJ_piExt Γ A B p q h)) = 30 := by rw [encode_Rule_HasJ_piExt]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasJ_allExt (Γ : P01AC.Tel) (B : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (h : P01D.Poly) : conclusionCode (encode (Rule.HasJ_allExt Γ B p q h)) = conclusion_HasJ_allExt (encode (Rule.HasJ_allExt Γ B p q h)) := by
  have ht : tag (encode (Rule.HasJ_allExt Γ B p q h)) = 31 := by rw [encode_Rule_HasJ_allExt]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasJ_sigmaElim (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (P : P01AC.Ty) (d : P01D.Poly) (z : P01D.Poly) : conclusionCode (encode (Rule.HasJ_sigmaElim Γ A B P d z)) = conclusion_HasJ_sigmaElim (encode (Rule.HasJ_sigmaElim Γ A B P d z)) := by
  have ht : tag (encode (Rule.HasJ_sigmaElim Γ A B P d z)) = 32 := by rw [encode_Rule_HasJ_sigmaElim]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasJ_natInduction (Γ : P01AC.Tel) (P : P01AC.Ty) (p : P01D.Poly) (s : P01D.Poly) : conclusionCode (encode (Rule.HasJ_natInduction Γ P p s)) = conclusion_HasJ_natInduction (encode (Rule.HasJ_natInduction Γ P p s)) := by
  have ht : tag (encode (Rule.HasJ_natInduction Γ P p s)) = 33 := by rw [encode_Rule_HasJ_natInduction]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, conclusionDispatch33, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_CtxE_nil  : conclusionCode (encode (Rule.CtxE_nil )) = conclusion_CtxE_nil (encode (Rule.CtxE_nil )) := by
  have ht : tag (encode (Rule.CtxE_nil )) = 34 := by rw [encode_Rule_CtxE_nil]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, conclusionDispatch33, conclusionDispatch34, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_CtxE_ext (Γ : P01AC.Tel) (A : P01AC.Ty) : conclusionCode (encode (Rule.CtxE_ext Γ A)) = conclusion_CtxE_ext (encode (Rule.CtxE_ext Γ A)) := by
  have ht : tag (encode (Rule.CtxE_ext Γ A)) = 35 := by rw [encode_Rule_CtxE_ext]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, conclusionDispatch33, conclusionDispatch34, conclusionDispatch35, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_FormE_param (Γ : P01AC.Tel) (n : Nat) : conclusionCode (encode (Rule.FormE_param Γ n)) = conclusion_FormE_param (encode (Rule.FormE_param Γ n)) := by
  have ht : tag (encode (Rule.FormE_param Γ n)) = 36 := by rw [encode_Rule_FormE_param]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, conclusionDispatch33, conclusionDispatch34, conclusionDispatch35, conclusionDispatch36, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_FormE_bottom (Γ : P01AC.Tel) : conclusionCode (encode (Rule.FormE_bottom Γ)) = conclusion_FormE_bottom (encode (Rule.FormE_bottom Γ)) := by
  have ht : tag (encode (Rule.FormE_bottom Γ)) = 37 := by rw [encode_Rule_FormE_bottom]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, conclusionDispatch33, conclusionDispatch34, conclusionDispatch35, conclusionDispatch36, conclusionDispatch37, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_FormE_all (Γ : P01AC.Tel) (B : P01AC.Ty) : conclusionCode (encode (Rule.FormE_all Γ B)) = conclusion_FormE_all (encode (Rule.FormE_all Γ B)) := by
  have ht : tag (encode (Rule.FormE_all Γ B)) = 38 := by rw [encode_Rule_FormE_all]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, conclusionDispatch33, conclusionDispatch34, conclusionDispatch35, conclusionDispatch36, conclusionDispatch37, conclusionDispatch38, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_FormE_raw (Γ : P01AC.Tel) : conclusionCode (encode (Rule.FormE_raw Γ)) = conclusion_FormE_raw (encode (Rule.FormE_raw Γ)) := by
  have ht : tag (encode (Rule.FormE_raw Γ)) = 39 := by rw [encode_Rule_FormE_raw]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, conclusionDispatch33, conclusionDispatch34, conclusionDispatch35, conclusionDispatch36, conclusionDispatch37, conclusionDispatch38, conclusionDispatch39, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_FormE_pi (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : conclusionCode (encode (Rule.FormE_pi Γ A B)) = conclusion_FormE_pi (encode (Rule.FormE_pi Γ A B)) := by
  have ht : tag (encode (Rule.FormE_pi Γ A B)) = 40 := by rw [encode_Rule_FormE_pi]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, conclusionDispatch33, conclusionDispatch34, conclusionDispatch35, conclusionDispatch36, conclusionDispatch37, conclusionDispatch38, conclusionDispatch39, conclusionDispatch40, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_FormE_sigma (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : conclusionCode (encode (Rule.FormE_sigma Γ A B)) = conclusion_FormE_sigma (encode (Rule.FormE_sigma Γ A B)) := by
  have ht : tag (encode (Rule.FormE_sigma Γ A B)) = 41 := by rw [encode_Rule_FormE_sigma]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, conclusionDispatch33, conclusionDispatch34, conclusionDispatch35, conclusionDispatch36, conclusionDispatch37, conclusionDispatch38, conclusionDispatch39, conclusionDispatch40, conclusionDispatch41, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_FormE_identity (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) : conclusionCode (encode (Rule.FormE_identity Γ A p q)) = conclusion_FormE_identity (encode (Rule.FormE_identity Γ A p q)) := by
  have ht : tag (encode (Rule.FormE_identity Γ A p q)) = 42 := by rw [encode_Rule_FormE_identity]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, conclusionDispatch33, conclusionDispatch34, conclusionDispatch35, conclusionDispatch36, conclusionDispatch37, conclusionDispatch38, conclusionDispatch39, conclusionDispatch40, conclusionDispatch41, conclusionDispatch42, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasE_var (Γ : P01AC.Tel) (A : P01AC.Ty) (n : Nat) (aux0 : AuxiliaryCertificates.LookupCert) : conclusionCode (encode (Rule.HasE_var Γ A n aux0)) = conclusion_HasE_var (encode (Rule.HasE_var Γ A n aux0)) := by
  have ht : tag (encode (Rule.HasE_var Γ A n aux0)) = 43 := by rw [encode_Rule_HasE_var]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, conclusionDispatch33, conclusionDispatch34, conclusionDispatch35, conclusionDispatch36, conclusionDispatch37, conclusionDispatch38, conclusionDispatch39, conclusionDispatch40, conclusionDispatch41, conclusionDispatch42, conclusionDispatch43, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasE_i (Γ : P01AC.Tel) (A : P01AC.Ty) : conclusionCode (encode (Rule.HasE_i Γ A)) = conclusion_HasE_i (encode (Rule.HasE_i Γ A)) := by
  have ht : tag (encode (Rule.HasE_i Γ A)) = 44 := by rw [encode_Rule_HasE_i]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, conclusionDispatch33, conclusionDispatch34, conclusionDispatch35, conclusionDispatch36, conclusionDispatch37, conclusionDispatch38, conclusionDispatch39, conclusionDispatch40, conclusionDispatch41, conclusionDispatch42, conclusionDispatch43, conclusionDispatch44, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasE_k (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) : conclusionCode (encode (Rule.HasE_k Γ A B)) = conclusion_HasE_k (encode (Rule.HasE_k Γ A B)) := by
  have ht : tag (encode (Rule.HasE_k Γ A B)) = 45 := by rw [encode_Rule_HasE_k]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, conclusionDispatch33, conclusionDispatch34, conclusionDispatch35, conclusionDispatch36, conclusionDispatch37, conclusionDispatch38, conclusionDispatch39, conclusionDispatch40, conclusionDispatch41, conclusionDispatch42, conclusionDispatch43, conclusionDispatch44, conclusionDispatch45, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasE_s (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (C : P01AC.Ty) : conclusionCode (encode (Rule.HasE_s Γ A B C)) = conclusion_HasE_s (encode (Rule.HasE_s Γ A B C)) := by
  have ht : tag (encode (Rule.HasE_s Γ A B C)) = 46 := by rw [encode_Rule_HasE_s]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, conclusionDispatch33, conclusionDispatch34, conclusionDispatch35, conclusionDispatch36, conclusionDispatch37, conclusionDispatch38, conclusionDispatch39, conclusionDispatch40, conclusionDispatch41, conclusionDispatch42, conclusionDispatch43, conclusionDispatch44, conclusionDispatch45, conclusionDispatch46, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasE_finite (C : OrthemologyV2.TypeCode) (Γ : P01AC.Tel) (t : OrthemologyV2.Term) (τ : List P01AC.Ty) (aux0 : AuxiliaryCertificates.FiniteCert) : conclusionCode (encode (Rule.HasE_finite C Γ t τ aux0)) = conclusion_HasE_finite (encode (Rule.HasE_finite C Γ t τ aux0)) := by
  have ht : tag (encode (Rule.HasE_finite C Γ t τ aux0)) = 47 := by rw [encode_Rule_HasE_finite]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, conclusionDispatch33, conclusionDispatch34, conclusionDispatch35, conclusionDispatch36, conclusionDispatch37, conclusionDispatch38, conclusionDispatch39, conclusionDispatch40, conclusionDispatch41, conclusionDispatch42, conclusionDispatch43, conclusionDispatch44, conclusionDispatch45, conclusionDispatch46, conclusionDispatch47, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasE_allIntro (Γ : P01AC.Tel) (B : P01AC.Ty) (p : P01D.Poly) : conclusionCode (encode (Rule.HasE_allIntro Γ B p)) = conclusion_HasE_allIntro (encode (Rule.HasE_allIntro Γ B p)) := by
  have ht : tag (encode (Rule.HasE_allIntro Γ B p)) = 48 := by rw [encode_Rule_HasE_allIntro]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, conclusionDispatch33, conclusionDispatch34, conclusionDispatch35, conclusionDispatch36, conclusionDispatch37, conclusionDispatch38, conclusionDispatch39, conclusionDispatch40, conclusionDispatch41, conclusionDispatch42, conclusionDispatch43, conclusionDispatch44, conclusionDispatch45, conclusionDispatch46, conclusionDispatch47, conclusionDispatch48, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasE_allElim (Γ : P01AC.Tel) (B : P01AC.Ty) (A : P01AC.Ty) (p : P01D.Poly) : conclusionCode (encode (Rule.HasE_allElim Γ B A p)) = conclusion_HasE_allElim (encode (Rule.HasE_allElim Γ B A p)) := by
  have ht : tag (encode (Rule.HasE_allElim Γ B A p)) = 49 := by rw [encode_Rule_HasE_allElim]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, conclusionDispatch33, conclusionDispatch34, conclusionDispatch35, conclusionDispatch36, conclusionDispatch37, conclusionDispatch38, conclusionDispatch39, conclusionDispatch40, conclusionDispatch41, conclusionDispatch42, conclusionDispatch43, conclusionDispatch44, conclusionDispatch45, conclusionDispatch46, conclusionDispatch47, conclusionDispatch48, conclusionDispatch49, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasE_rawAtom (Γ : P01AC.Tel) (t : OrthemologyV2.Term) : conclusionCode (encode (Rule.HasE_rawAtom Γ t)) = conclusion_HasE_rawAtom (encode (Rule.HasE_rawAtom Γ t)) := by
  have ht : tag (encode (Rule.HasE_rawAtom Γ t)) = 50 := by rw [encode_Rule_HasE_rawAtom]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, conclusionDispatch33, conclusionDispatch34, conclusionDispatch35, conclusionDispatch36, conclusionDispatch37, conclusionDispatch38, conclusionDispatch39, conclusionDispatch40, conclusionDispatch41, conclusionDispatch42, conclusionDispatch43, conclusionDispatch44, conclusionDispatch45, conclusionDispatch46, conclusionDispatch47, conclusionDispatch48, conclusionDispatch49, conclusionDispatch50, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasE_rawApp (Γ : P01AC.Tel) (f : P01D.Poly) (a : P01D.Poly) : conclusionCode (encode (Rule.HasE_rawApp Γ f a)) = conclusion_HasE_rawApp (encode (Rule.HasE_rawApp Γ f a)) := by
  have ht : tag (encode (Rule.HasE_rawApp Γ f a)) = 51 := by rw [encode_Rule_HasE_rawApp]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, conclusionDispatch33, conclusionDispatch34, conclusionDispatch35, conclusionDispatch36, conclusionDispatch37, conclusionDispatch38, conclusionDispatch39, conclusionDispatch40, conclusionDispatch41, conclusionDispatch42, conclusionDispatch43, conclusionDispatch44, conclusionDispatch45, conclusionDispatch46, conclusionDispatch47, conclusionDispatch48, conclusionDispatch49, conclusionDispatch50, conclusionDispatch51, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasE_piIntro (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (b : P01D.Poly) : conclusionCode (encode (Rule.HasE_piIntro Γ A B b)) = conclusion_HasE_piIntro (encode (Rule.HasE_piIntro Γ A B b)) := by
  have ht : tag (encode (Rule.HasE_piIntro Γ A B b)) = 52 := by rw [encode_Rule_HasE_piIntro]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, conclusionDispatch33, conclusionDispatch34, conclusionDispatch35, conclusionDispatch36, conclusionDispatch37, conclusionDispatch38, conclusionDispatch39, conclusionDispatch40, conclusionDispatch41, conclusionDispatch42, conclusionDispatch43, conclusionDispatch44, conclusionDispatch45, conclusionDispatch46, conclusionDispatch47, conclusionDispatch48, conclusionDispatch49, conclusionDispatch50, conclusionDispatch51, conclusionDispatch52, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasE_piElim (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (a : P01D.Poly) (f : P01D.Poly) : conclusionCode (encode (Rule.HasE_piElim Γ A B a f)) = conclusion_HasE_piElim (encode (Rule.HasE_piElim Γ A B a f)) := by
  have ht : tag (encode (Rule.HasE_piElim Γ A B a f)) = 53 := by rw [encode_Rule_HasE_piElim]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, conclusionDispatch33, conclusionDispatch34, conclusionDispatch35, conclusionDispatch36, conclusionDispatch37, conclusionDispatch38, conclusionDispatch39, conclusionDispatch40, conclusionDispatch41, conclusionDispatch42, conclusionDispatch43, conclusionDispatch44, conclusionDispatch45, conclusionDispatch46, conclusionDispatch47, conclusionDispatch48, conclusionDispatch49, conclusionDispatch50, conclusionDispatch51, conclusionDispatch52, conclusionDispatch53, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasE_sigmaIntro (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (a : P01D.Poly) (b : P01D.Poly) : conclusionCode (encode (Rule.HasE_sigmaIntro Γ A B a b)) = conclusion_HasE_sigmaIntro (encode (Rule.HasE_sigmaIntro Γ A B a b)) := by
  have ht : tag (encode (Rule.HasE_sigmaIntro Γ A B a b)) = 54 := by rw [encode_Rule_HasE_sigmaIntro]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, conclusionDispatch33, conclusionDispatch34, conclusionDispatch35, conclusionDispatch36, conclusionDispatch37, conclusionDispatch38, conclusionDispatch39, conclusionDispatch40, conclusionDispatch41, conclusionDispatch42, conclusionDispatch43, conclusionDispatch44, conclusionDispatch45, conclusionDispatch46, conclusionDispatch47, conclusionDispatch48, conclusionDispatch49, conclusionDispatch50, conclusionDispatch51, conclusionDispatch52, conclusionDispatch53, conclusionDispatch54, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasE_sigmaFst (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (z : P01D.Poly) : conclusionCode (encode (Rule.HasE_sigmaFst Γ A B z)) = conclusion_HasE_sigmaFst (encode (Rule.HasE_sigmaFst Γ A B z)) := by
  have ht : tag (encode (Rule.HasE_sigmaFst Γ A B z)) = 55 := by rw [encode_Rule_HasE_sigmaFst]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, conclusionDispatch33, conclusionDispatch34, conclusionDispatch35, conclusionDispatch36, conclusionDispatch37, conclusionDispatch38, conclusionDispatch39, conclusionDispatch40, conclusionDispatch41, conclusionDispatch42, conclusionDispatch43, conclusionDispatch44, conclusionDispatch45, conclusionDispatch46, conclusionDispatch47, conclusionDispatch48, conclusionDispatch49, conclusionDispatch50, conclusionDispatch51, conclusionDispatch52, conclusionDispatch53, conclusionDispatch54, conclusionDispatch55, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasE_sigmaSnd (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (z : P01D.Poly) : conclusionCode (encode (Rule.HasE_sigmaSnd Γ A B z)) = conclusion_HasE_sigmaSnd (encode (Rule.HasE_sigmaSnd Γ A B z)) := by
  have ht : tag (encode (Rule.HasE_sigmaSnd Γ A B z)) = 56 := by rw [encode_Rule_HasE_sigmaSnd]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, conclusionDispatch33, conclusionDispatch34, conclusionDispatch35, conclusionDispatch36, conclusionDispatch37, conclusionDispatch38, conclusionDispatch39, conclusionDispatch40, conclusionDispatch41, conclusionDispatch42, conclusionDispatch43, conclusionDispatch44, conclusionDispatch45, conclusionDispatch46, conclusionDispatch47, conclusionDispatch48, conclusionDispatch49, conclusionDispatch50, conclusionDispatch51, conclusionDispatch52, conclusionDispatch53, conclusionDispatch54, conclusionDispatch55, conclusionDispatch56, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasE_identityIntro (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (aux0 : AuxiliaryCertificates.PolyCert) : conclusionCode (encode (Rule.HasE_identityIntro Γ A p q aux0)) = conclusion_HasE_identityIntro (encode (Rule.HasE_identityIntro Γ A p q aux0)) := by
  have ht : tag (encode (Rule.HasE_identityIntro Γ A p q aux0)) = 57 := by rw [encode_Rule_HasE_identityIntro]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, conclusionDispatch33, conclusionDispatch34, conclusionDispatch35, conclusionDispatch36, conclusionDispatch37, conclusionDispatch38, conclusionDispatch39, conclusionDispatch40, conclusionDispatch41, conclusionDispatch42, conclusionDispatch43, conclusionDispatch44, conclusionDispatch45, conclusionDispatch46, conclusionDispatch47, conclusionDispatch48, conclusionDispatch49, conclusionDispatch50, conclusionDispatch51, conclusionDispatch52, conclusionDispatch53, conclusionDispatch54, conclusionDispatch55, conclusionDispatch56, conclusionDispatch57, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasE_proofErase (Γ : P01AC.Tel) (A : P01AC.Ty) (x : P01D.Poly) (y : P01D.Poly) (p : P01D.Poly) : conclusionCode (encode (Rule.HasE_proofErase Γ A x y p)) = conclusion_HasE_proofErase (encode (Rule.HasE_proofErase Γ A x y p)) := by
  have ht : tag (encode (Rule.HasE_proofErase Γ A x y p)) = 58 := by rw [encode_Rule_HasE_proofErase]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, conclusionDispatch33, conclusionDispatch34, conclusionDispatch35, conclusionDispatch36, conclusionDispatch37, conclusionDispatch38, conclusionDispatch39, conclusionDispatch40, conclusionDispatch41, conclusionDispatch42, conclusionDispatch43, conclusionDispatch44, conclusionDispatch45, conclusionDispatch46, conclusionDispatch47, conclusionDispatch48, conclusionDispatch49, conclusionDispatch50, conclusionDispatch51, conclusionDispatch52, conclusionDispatch53, conclusionDispatch54, conclusionDispatch55, conclusionDispatch56, conclusionDispatch57, conclusionDispatch58, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasE_j (Γ : P01AC.Tel) (A : P01AC.Ty) (x : P01D.Poly) (B : P01AC.Ty) (y : P01D.Poly) (e : P01D.Poly) (d : P01D.Poly) : conclusionCode (encode (Rule.HasE_j Γ A x B y e d)) = conclusion_HasE_j (encode (Rule.HasE_j Γ A x B y e d)) := by
  have ht : tag (encode (Rule.HasE_j Γ A x B y e d)) = 59 := by rw [encode_Rule_HasE_j]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, conclusionDispatch33, conclusionDispatch34, conclusionDispatch35, conclusionDispatch36, conclusionDispatch37, conclusionDispatch38, conclusionDispatch39, conclusionDispatch40, conclusionDispatch41, conclusionDispatch42, conclusionDispatch43, conclusionDispatch44, conclusionDispatch45, conclusionDispatch46, conclusionDispatch47, conclusionDispatch48, conclusionDispatch49, conclusionDispatch50, conclusionDispatch51, conclusionDispatch52, conclusionDispatch53, conclusionDispatch54, conclusionDispatch55, conclusionDispatch56, conclusionDispatch57, conclusionDispatch58, conclusionDispatch59, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasE_conv (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (aux0 : AuxiliaryCertificates.PolyCert) : conclusionCode (encode (Rule.HasE_conv Γ A p q aux0)) = conclusion_HasE_conv (encode (Rule.HasE_conv Γ A p q aux0)) := by
  have ht : tag (encode (Rule.HasE_conv Γ A p q aux0)) = 60 := by rw [encode_Rule_HasE_conv]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, conclusionDispatch33, conclusionDispatch34, conclusionDispatch35, conclusionDispatch36, conclusionDispatch37, conclusionDispatch38, conclusionDispatch39, conclusionDispatch40, conclusionDispatch41, conclusionDispatch42, conclusionDispatch43, conclusionDispatch44, conclusionDispatch45, conclusionDispatch46, conclusionDispatch47, conclusionDispatch48, conclusionDispatch49, conclusionDispatch50, conclusionDispatch51, conclusionDispatch52, conclusionDispatch53, conclusionDispatch54, conclusionDispatch55, conclusionDispatch56, conclusionDispatch57, conclusionDispatch58, conclusionDispatch59, conclusionDispatch60, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasE_piExt (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (h : P01D.Poly) : conclusionCode (encode (Rule.HasE_piExt Γ A B p q h)) = conclusion_HasE_piExt (encode (Rule.HasE_piExt Γ A B p q h)) := by
  have ht : tag (encode (Rule.HasE_piExt Γ A B p q h)) = 61 := by rw [encode_Rule_HasE_piExt]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, conclusionDispatch33, conclusionDispatch34, conclusionDispatch35, conclusionDispatch36, conclusionDispatch37, conclusionDispatch38, conclusionDispatch39, conclusionDispatch40, conclusionDispatch41, conclusionDispatch42, conclusionDispatch43, conclusionDispatch44, conclusionDispatch45, conclusionDispatch46, conclusionDispatch47, conclusionDispatch48, conclusionDispatch49, conclusionDispatch50, conclusionDispatch51, conclusionDispatch52, conclusionDispatch53, conclusionDispatch54, conclusionDispatch55, conclusionDispatch56, conclusionDispatch57, conclusionDispatch58, conclusionDispatch59, conclusionDispatch60, conclusionDispatch61, ht, Nat.reduceEqDiff, ↓reduceIte]
@[simp] theorem conclusionCode_HasE_allExt (Γ : P01AC.Tel) (B : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (h : P01D.Poly) : conclusionCode (encode (Rule.HasE_allExt Γ B p q h)) = conclusion_HasE_allExt (encode (Rule.HasE_allExt Γ B p q h)) := by
  have ht : tag (encode (Rule.HasE_allExt Γ B p q h)) = 62 := by rw [encode_Rule_HasE_allExt]; exact tag_pack _ _
  simp only [conclusionCode,conclusionDispatch0, conclusionDispatch1, conclusionDispatch2, conclusionDispatch3, conclusionDispatch4, conclusionDispatch5, conclusionDispatch6, conclusionDispatch7, conclusionDispatch8, conclusionDispatch9, conclusionDispatch10, conclusionDispatch11, conclusionDispatch12, conclusionDispatch13, conclusionDispatch14, conclusionDispatch15, conclusionDispatch16, conclusionDispatch17, conclusionDispatch18, conclusionDispatch19, conclusionDispatch20, conclusionDispatch21, conclusionDispatch22, conclusionDispatch23, conclusionDispatch24, conclusionDispatch25, conclusionDispatch26, conclusionDispatch27, conclusionDispatch28, conclusionDispatch29, conclusionDispatch30, conclusionDispatch31, conclusionDispatch32, conclusionDispatch33, conclusionDispatch34, conclusionDispatch35, conclusionDispatch36, conclusionDispatch37, conclusionDispatch38, conclusionDispatch39, conclusionDispatch40, conclusionDispatch41, conclusionDispatch42, conclusionDispatch43, conclusionDispatch44, conclusionDispatch45, conclusionDispatch46, conclusionDispatch47, conclusionDispatch48, conclusionDispatch49, conclusionDispatch50, conclusionDispatch51, conclusionDispatch52, conclusionDispatch53, conclusionDispatch54, conclusionDispatch55, conclusionDispatch56, conclusionDispatch57, conclusionDispatch58, conclusionDispatch59, conclusionDispatch60, conclusionDispatch61, conclusionDispatch62, ht, Nat.reduceEqDiff, ↓reduceIte]

theorem conclusionCode_exact (r : Rule) : conclusionCode (encode r) = encode r.conclusion := by
  cases r <;> simp only [conclusionCode_CtxJ_ctxBase, conclusionCode_CtxJ_nil, conclusionCode_CtxJ_ext, conclusionCode_FormJ_formBase, conclusionCode_FormJ_param, conclusionCode_FormJ_bottom, conclusionCode_FormJ_all, conclusionCode_FormJ_raw, conclusionCode_FormJ_pi, conclusionCode_FormJ_sigma, conclusionCode_FormJ_identity, conclusionCode_HasJ_hasBase, conclusionCode_HasJ_var, conclusionCode_HasJ_i, conclusionCode_HasJ_k, conclusionCode_HasJ_s, conclusionCode_HasJ_finite, conclusionCode_HasJ_allIntro, conclusionCode_HasJ_allElim, conclusionCode_HasJ_rawAtom, conclusionCode_HasJ_rawApp, conclusionCode_HasJ_piIntro, conclusionCode_HasJ_piElim, conclusionCode_HasJ_sigmaIntro, conclusionCode_HasJ_sigmaFst, conclusionCode_HasJ_sigmaSnd, conclusionCode_HasJ_identityIntro, conclusionCode_HasJ_proofErase, conclusionCode_HasJ_j, conclusionCode_HasJ_conv, conclusionCode_HasJ_piExt, conclusionCode_HasJ_allExt, conclusionCode_HasJ_sigmaElim, conclusionCode_HasJ_natInduction, conclusionCode_CtxE_nil, conclusionCode_CtxE_ext, conclusionCode_FormE_param, conclusionCode_FormE_bottom, conclusionCode_FormE_all, conclusionCode_FormE_raw, conclusionCode_FormE_pi, conclusionCode_FormE_sigma, conclusionCode_FormE_identity, conclusionCode_HasE_var, conclusionCode_HasE_i, conclusionCode_HasE_k, conclusionCode_HasE_s, conclusionCode_HasE_finite, conclusionCode_HasE_allIntro, conclusionCode_HasE_allElim, conclusionCode_HasE_rawAtom, conclusionCode_HasE_rawApp, conclusionCode_HasE_piIntro, conclusionCode_HasE_piElim, conclusionCode_HasE_sigmaIntro, conclusionCode_HasE_sigmaFst, conclusionCode_HasE_sigmaSnd, conclusionCode_HasE_identityIntro, conclusionCode_HasE_proofErase, conclusionCode_HasE_j, conclusionCode_HasE_conv, conclusionCode_HasE_piExt, conclusionCode_HasE_allExt, conclusion_CtxJ_ctxBase_exact, conclusion_CtxJ_nil_exact, conclusion_CtxJ_ext_exact, conclusion_FormJ_formBase_exact, conclusion_FormJ_param_exact, conclusion_FormJ_bottom_exact, conclusion_FormJ_all_exact, conclusion_FormJ_raw_exact, conclusion_FormJ_pi_exact, conclusion_FormJ_sigma_exact, conclusion_FormJ_identity_exact, conclusion_HasJ_hasBase_exact, conclusion_HasJ_var_exact, conclusion_HasJ_i_exact, conclusion_HasJ_k_exact, conclusion_HasJ_s_exact, conclusion_HasJ_finite_exact, conclusion_HasJ_allIntro_exact, conclusion_HasJ_allElim_exact, conclusion_HasJ_rawAtom_exact, conclusion_HasJ_rawApp_exact, conclusion_HasJ_piIntro_exact, conclusion_HasJ_piElim_exact, conclusion_HasJ_sigmaIntro_exact, conclusion_HasJ_sigmaFst_exact, conclusion_HasJ_sigmaSnd_exact, conclusion_HasJ_identityIntro_exact, conclusion_HasJ_proofErase_exact, conclusion_HasJ_j_exact, conclusion_HasJ_conv_exact, conclusion_HasJ_piExt_exact, conclusion_HasJ_allExt_exact, conclusion_HasJ_sigmaElim_exact, conclusion_HasJ_natInduction_exact, conclusion_CtxE_nil_exact, conclusion_CtxE_ext_exact, conclusion_FormE_param_exact, conclusion_FormE_bottom_exact, conclusion_FormE_all_exact, conclusion_FormE_raw_exact, conclusion_FormE_pi_exact, conclusion_FormE_sigma_exact, conclusion_FormE_identity_exact, conclusion_HasE_var_exact, conclusion_HasE_i_exact, conclusion_HasE_k_exact, conclusion_HasE_s_exact, conclusion_HasE_finite_exact, conclusion_HasE_allIntro_exact, conclusion_HasE_allElim_exact, conclusion_HasE_rawAtom_exact, conclusion_HasE_rawApp_exact, conclusion_HasE_piIntro_exact, conclusion_HasE_piElim_exact, conclusion_HasE_sigmaIntro_exact, conclusion_HasE_sigmaFst_exact, conclusion_HasE_sigmaSnd_exact, conclusion_HasE_identityIntro_exact, conclusion_HasE_proofErase_exact, conclusion_HasE_j_exact, conclusion_HasE_conv_exact, conclusion_HasE_piExt_exact, conclusion_HasE_allExt_exact]

#print axioms primrec_conclusionCode
#print axioms conclusionCode_exact
end CodedRuleTemplates
