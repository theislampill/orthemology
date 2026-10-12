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
  have h : Primrec (fun c : Nat => (ctxCode 0 (ruleField c 0))) := ((primrec_ctxCode 0).comp (primrec_ruleField.comp Primrec.id (.const 0)))
  exact h.of_eq (by intro c; rfl)
@[simp] theorem conclusion_CtxJ_ctxBase_exact (Γ : P01AC.Tel) : conclusion_CtxJ_ctxBase (encode (Rule.CtxJ_ctxBase Γ)) = encode ((Rule.CtxJ_ctxBase Γ).conclusion) := by
  simp only [conclusion_CtxJ_ctxBase,Rule.conclusion]
  simp only [encode_Rule_CtxJ_ctxBase,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat]
  simp only [polyAtom_exact,varCode_exact,paramCode,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append]

def conclusion_CtxJ_nil (c : Nat) : Nat := (ctxCode 0 (encode ([] : Tel)))
theorem primrec_conclusion_CtxJ_nil : Primrec conclusion_CtxJ_nil := by
  have h : Primrec (fun c : Nat => (ctxCode 0 (encode ([] : Tel)))) := ((primrec_ctxCode 0).comp (Primrec.const (encode ([] : Tel))))
  exact h.of_eq (by intro c; rfl)
@[simp] theorem conclusion_CtxJ_nil_exact  : conclusion_CtxJ_nil (encode (Rule.CtxJ_nil )) = encode ((Rule.CtxJ_nil ).conclusion) := by
  simp only [conclusion_CtxJ_nil,Rule.conclusion]
  simp only [encode_Rule_CtxJ_nil,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat]
  simp only [polyAtom_exact,varCode_exact,paramCode,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append]

def conclusion_CtxJ_ext (c : Nat) : Nat := (ctxCode 0 ((telConsCode (ruleField c 1) (ruleField c 0))))
theorem primrec_conclusion_CtxJ_ext : Primrec conclusion_CtxJ_ext := by
  have h : Primrec (fun c : Nat => (ctxCode 0 ((telConsCode (ruleField c 1) (ruleField c 0))))) := ((primrec_ctxCode 0).comp (primrec_telConsCode.comp (primrec_ruleField.comp Primrec.id (.const 1)) (primrec_ruleField.comp Primrec.id (.const 0))))
  exact h.of_eq (by intro c; rfl)
@[simp] theorem conclusion_CtxJ_ext_exact (Γ : P01AC.Tel) (A : P01AC.Ty) : conclusion_CtxJ_ext (encode (Rule.CtxJ_ext Γ A)) = encode ((Rule.CtxJ_ext Γ A).conclusion) := by
  simp only [conclusion_CtxJ_ext,Rule.conclusion]
  simp only [encode_Rule_CtxJ_ext,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat]
  simp only [polyAtom_exact,varCode_exact,paramCode,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append]

def conclusion_FormJ_formBase (c : Nat) : Nat := (formCode 1 (ruleField c 0) (ruleField c 1))
theorem primrec_conclusion_FormJ_formBase : Primrec conclusion_FormJ_formBase := by
  have h : Primrec (fun c : Nat => (formCode 1 (ruleField c 0) (ruleField c 1))) := ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_ruleField.comp Primrec.id (.const 1)))
  exact h.of_eq (by intro c; rfl)
@[simp] theorem conclusion_FormJ_formBase_exact (Γ : P01AC.Tel) (A : P01AC.Ty) : conclusion_FormJ_formBase (encode (Rule.FormJ_formBase Γ A)) = encode ((Rule.FormJ_formBase Γ A).conclusion) := by
  simp only [conclusion_FormJ_formBase,Rule.conclusion]
  simp only [encode_Rule_FormJ_formBase,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat]
  simp only [polyAtom_exact,varCode_exact,paramCode,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append]

def conclusion_FormJ_param (c : Nat) : Nat := (formCode 1 (ruleField c 0) ((paramCode (ruleField c 1))))
theorem primrec_conclusion_FormJ_param : Primrec conclusion_FormJ_param := by
  have h : Primrec (fun c : Nat => (formCode 1 (ruleField c 0) ((paramCode (ruleField c 1))))) := ((primrec_formCode 1).comp (primrec_ruleField.comp Primrec.id (.const 0)) (primrec_paramCode.comp (primrec_ruleField.comp Primrec.id (.const 1))))
  exact h.of_eq (by intro c; rfl)
@[simp] theorem conclusion_FormJ_param_exact (Γ : P01AC.Tel) (n : Nat) : conclusion_FormJ_param (encode (Rule.FormJ_param Γ n)) = encode ((Rule.FormJ_param Γ n).conclusion) := by
  simp only [conclusion_FormJ_param,Rule.conclusion]
  simp only [encode_Rule_FormJ_param,ruleField,slot,iterRest_succ,iterRest_zero,pack,
    List.foldr_cons,List.foldr_nil,first_node,rest_node,rest_leaf,encode_nat]
  simp only [polyAtom_exact,varCode_exact,paramCode,← encode_app,← encode_pi,
    allTyCode_exact,sigmaTyCode_exact,identityTyCode_exact,arrCode_exact,
    twkTelCode_exact,thetaCode_exact,motiveAtCode_exact,abstractCode_exact,pairPolyCode_exact,
    fstPolyCode_exact,sndPolyCode_exact,jPolyCode_exact,branchAtCode_exact,branchTypeCode_exact,
    dependentStepTypeCode_exact,sectionPolyCode_exact,finCode_exact,shiftCode_one_exact,
    tsubstTelCode_exact,instTyCode_exact,tinstCode_exact,telConsCode_exact,
    ctxJCode_exact,ctxECode_exact,formJCode_exact,formECode_exact,hasJCode_exact,hasECode_exact,
    formJImagesCode_exact,formEImagesCode_exact,List.map_cons,List.map_nil,List.map_append]

end CodedRuleTemplates
