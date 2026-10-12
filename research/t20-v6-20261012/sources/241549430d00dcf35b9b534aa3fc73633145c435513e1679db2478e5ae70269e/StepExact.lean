import StepCode
import AuxiliaryExactViews
namespace AuxiliaryCodeComputability
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity
open AuxiliaryCertificates OrthemologyV2 P01D
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000
attribute [local irreducible] Nat.pair

theorem checkStepCode_exact (c : StepCert) (t u : Term) :
    checkStepCode (encode c) (encode t) (encode u) = checkStep c t u := by
  induction c generalizing t u with
  | i x =>
    rw [checkStepCode,evaluate]
    simp only [encode_step_i,stepShape,stepChildren,pack,List.foldr_cons,List.foldr_nil,
      a1,a2,a3,a4,v1,v2,v3,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,
      unpair_leaf,lhs_pair,rhs_pair,tmApp_exact,encode_injective.eq_iff,checkStep]
    simp
  | k x y =>
    rw [checkStepCode,evaluate]
    simp only [encode_step_k,stepShape,stepChildren,pack,List.foldr_cons,List.foldr_nil,
      a1,a2,a3,a4,v1,v2,v3,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,
      unpair_leaf,lhs_pair,rhs_pair,tmApp_exact,encode_injective.eq_iff,checkStep]
    simp
  | s f g x =>
    rw [checkStepCode,evaluate]
    simp only [encode_step_s,stepShape,stepChildren,pack,List.foldr_cons,List.foldr_nil,
      a1,a2,a3,a4,v1,v2,v3,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,
      unpair_leaf,lhs_pair,rhs_pair,tmApp_exact,encode_injective.eq_iff,checkStep]
    simp
  | left f g x c ih =>
    have hc : encode c < encode (StepCert.left f g x c) := by
      rw [encode_step_left]; exact field_lt_pack _ _ (by simp)
    rw [checkStepCode,evaluate]
    simp only [encode_step_left,stepShape,stepChildren,pack,List.foldr_cons,List.foldr_nil,
      a1,a2,a3,a4,v1,v2,v3,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,
      unpair_leaf,lhs_pair,rhs_pair,tmApp_exact,encode_injective.eq_iff,checkStep]
    simp only [encode_step_left,pack,List.foldr_cons,List.foldr_nil] at hc
    simp [hc,eval_step,ih]
  | right f x y c ih =>
    have hc : encode c < encode (StepCert.right f x y c) := by
      rw [encode_step_right]; exact field_lt_pack _ _ (by simp)
    rw [checkStepCode,evaluate]
    simp only [encode_step_right,stepShape,stepChildren,pack,List.foldr_cons,List.foldr_nil,
      a1,a2,a3,a4,v1,v2,v3,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,
      unpair_leaf,lhs_pair,rhs_pair,tmApp_exact,encode_injective.eq_iff,checkStep]
    simp only [encode_step_right,pack,List.foldr_cons,List.foldr_nil] at hc
    simp [hc,eval_step,ih]

#print axioms primrec_checkStepCode
#print axioms checkStepCode_exact
end AuxiliaryCodeComputability
