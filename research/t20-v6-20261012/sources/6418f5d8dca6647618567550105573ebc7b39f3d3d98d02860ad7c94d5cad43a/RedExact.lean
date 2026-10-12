import RedCode
import AuxiliaryExactViews
namespace AuxiliaryCodeComputability
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity
open AuxiliaryCertificates OrthemologyV2 OrthemologyV3 P01D
set_option maxRecDepth 8192
set_option maxHeartbeats 200000
attribute [local irreducible] Nat.pair

theorem checkRedCode_exact (c : RedCert) (inputLeft inputRight : Term) :
    checkRedCode (encode c) (encode inputLeft) (encode inputRight) = checkRed c inputLeft inputRight := by
  induction c generalizing inputLeft inputRight with
  | refl t =>
    rw [checkRedCode,evaluate]
    simp only [encode_red_refl,redShape,redChildren,pack,List.foldr_cons,List.foldr_nil,
      a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,
      unpair_leaf,lhs_pair,rhs_pair,tmApp_exact,polyApp_exact,polyAtom_exact,tyArrow_exact,tyAll_exact,encode_injective.eq_iff,checkRed]
    simp [eval_red, Bool.and_assoc, Bool.and_left_comm, Bool.and_comm, checkStepCode_exact]
  | tail t u v s r ihr =>
    have hr : encode r < encode (.tail t u v s r : RedCert) := by
      rw [encode_red_tail]; exact field_lt_pack _ _ (by simp)
    rw [checkRedCode,evaluate]
    simp only [encode_red_tail,redShape,redChildren,pack,List.foldr_cons,List.foldr_nil,
      a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,
      unpair_leaf,lhs_pair,rhs_pair,tmApp_exact,polyApp_exact,polyAtom_exact,tyArrow_exact,tyAll_exact,encode_injective.eq_iff,checkRed]
    simp only [encode_red_tail,pack,List.foldr_cons,List.foldr_nil] at hr
    simp [hr, eval_red, ihr, Bool.and_assoc, Bool.and_left_comm, Bool.and_comm, checkStepCode_exact]

#print axioms primrec_checkRedCode
#print axioms checkRedCode_exact
end AuxiliaryCodeComputability
