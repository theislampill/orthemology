import FiniteCode
import AuxiliaryExactViews
namespace AuxiliaryCodeComputability
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity
open AuxiliaryCertificates OrthemologyV2 OrthemologyV3 P01D
set_option maxRecDepth 8192
set_option maxHeartbeats 200000
attribute [local irreducible] Nat.pair

theorem checkFiniteCode_exact (c : FiniteCert) (inputLeft : Term) (inputRight : TypeCode) :
    checkFiniteCode (encode c) (encode inputLeft) (encode inputRight) = checkFinite c inputLeft inputRight := by
  induction c generalizing inputLeft inputRight with
  | i A =>
    rw [checkFiniteCode,evaluate]
    simp only [encode_finite_i,finiteShape,finiteChildren,pack,List.foldr_cons,List.foldr_nil,
      a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,
      unpair_leaf,lhs_pair,rhs_pair,tmApp_exact,polyApp_exact,polyAtom_exact,tyArrow_exact,tyAll_exact,encode_injective.eq_iff,checkFinite]
    simp [-encode_type_arrow, -encode_type_all, eval_finite, Bool.and_assoc, Bool.and_left_comm, Bool.and_comm, checkStepCode_exact, checkRedCode_exact, CodedMixedTransformations.instantiateTypeCode_exact]
  | k A B =>
    rw [checkFiniteCode,evaluate]
    simp only [encode_finite_k,finiteShape,finiteChildren,pack,List.foldr_cons,List.foldr_nil,
      a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,
      unpair_leaf,lhs_pair,rhs_pair,tmApp_exact,polyApp_exact,polyAtom_exact,tyArrow_exact,tyAll_exact,encode_injective.eq_iff,checkFinite]
    simp [-encode_type_arrow, -encode_type_all, eval_finite, Bool.and_assoc, Bool.and_left_comm, Bool.and_comm, checkStepCode_exact, checkRedCode_exact, CodedMixedTransformations.instantiateTypeCode_exact]
  | s A B C =>
    rw [checkFiniteCode,evaluate]
    simp only [encode_finite_s,finiteShape,finiteChildren,pack,List.foldr_cons,List.foldr_nil,
      a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,
      unpair_leaf,lhs_pair,rhs_pair,tmApp_exact,polyApp_exact,polyAtom_exact,tyArrow_exact,tyAll_exact,encode_injective.eq_iff,checkFinite]
    simp [-encode_type_arrow, -encode_type_all, eval_finite, Bool.and_assoc, Bool.and_left_comm, Bool.and_comm, checkStepCode_exact, checkRedCode_exact, CodedMixedTransformations.instantiateTypeCode_exact]
  | app f x A B p q ihp ihq =>
    have hp : encode p < encode (.app f x A B p q : FiniteCert) := by
      rw [encode_finite_app]; exact field_lt_pack _ _ (by simp)
    have hq : encode q < encode (.app f x A B p q : FiniteCert) := by
      rw [encode_finite_app]; exact field_lt_pack _ _ (by simp)
    rw [checkFiniteCode,evaluate]
    simp only [encode_finite_app,finiteShape,finiteChildren,pack,List.foldr_cons,List.foldr_nil,
      a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,
      unpair_leaf,lhs_pair,rhs_pair,tmApp_exact,polyApp_exact,polyAtom_exact,tyArrow_exact,tyAll_exact,encode_injective.eq_iff,checkFinite]
    simp only [encode_finite_app,pack,List.foldr_cons,List.foldr_nil] at hp
    simp only [encode_finite_app,pack,List.foldr_cons,List.foldr_nil] at hq
    simp [-encode_type_arrow, -encode_type_all, hp, hq, eval_finite, ihp, ihq, Bool.and_assoc, Bool.and_left_comm, Bool.and_comm, checkStepCode_exact, checkRedCode_exact, CodedMixedTransformations.instantiateTypeCode_exact]
  | allI t B p ihp =>
    have hp : encode p < encode (.allI t B p : FiniteCert) := by
      rw [encode_finite_allI]; exact field_lt_pack _ _ (by simp)
    rw [checkFiniteCode,evaluate]
    simp only [encode_finite_allI,finiteShape,finiteChildren,pack,List.foldr_cons,List.foldr_nil,
      a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,
      unpair_leaf,lhs_pair,rhs_pair,tmApp_exact,polyApp_exact,polyAtom_exact,tyArrow_exact,tyAll_exact,encode_injective.eq_iff,checkFinite]
    simp only [encode_finite_allI,pack,List.foldr_cons,List.foldr_nil] at hp
    simp [-encode_type_arrow, -encode_type_all, hp, eval_finite, ihp, Bool.and_assoc, Bool.and_left_comm, Bool.and_comm, checkStepCode_exact, checkRedCode_exact, CodedMixedTransformations.instantiateTypeCode_exact]
  | allE t B A p ihp =>
    have hp : encode p < encode (.allE t B A p : FiniteCert) := by
      rw [encode_finite_allE]; exact field_lt_pack _ _ (by simp)
    rw [checkFiniteCode,evaluate]
    simp only [encode_finite_allE,finiteShape,finiteChildren,pack,List.foldr_cons,List.foldr_nil,
      a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,
      unpair_leaf,lhs_pair,rhs_pair,tmApp_exact,polyApp_exact,polyAtom_exact,tyArrow_exact,tyAll_exact,encode_injective.eq_iff,checkFinite]
    simp only [encode_finite_allE,pack,List.foldr_cons,List.foldr_nil] at hp
    simp [-encode_type_arrow, -encode_type_all, hp, eval_finite, ihp, Bool.and_assoc, Bool.and_left_comm, Bool.and_comm, checkStepCode_exact, checkRedCode_exact, CodedMixedTransformations.instantiateTypeCode_exact]
  | reduce t u A p r ihp =>
    have hp : encode p < encode (.reduce t u A p r : FiniteCert) := by
      rw [encode_finite_reduce]; exact field_lt_pack _ _ (by simp)
    rw [checkFiniteCode,evaluate]
    simp only [encode_finite_reduce,finiteShape,finiteChildren,pack,List.foldr_cons,List.foldr_nil,
      a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,
      unpair_leaf,lhs_pair,rhs_pair,tmApp_exact,polyApp_exact,polyAtom_exact,tyArrow_exact,tyAll_exact,encode_injective.eq_iff,checkFinite]
    simp only [encode_finite_reduce,pack,List.foldr_cons,List.foldr_nil] at hp
    simp [-encode_type_arrow, -encode_type_all, hp, eval_finite, ihp, Bool.and_assoc, Bool.and_left_comm, Bool.and_comm, checkStepCode_exact, checkRedCode_exact, CodedMixedTransformations.instantiateTypeCode_exact]

#print axioms primrec_checkFiniteCode
#print axioms checkFiniteCode_exact
end AuxiliaryCodeComputability
