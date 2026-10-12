import PolyCode
import AuxiliaryExactViews
namespace AuxiliaryCodeComputability
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity
open AuxiliaryCertificates OrthemologyV2 P01D
set_option maxRecDepth 8192
set_option maxHeartbeats 200000
attribute [local irreducible] Nat.pair

theorem checkPolyCode_exact (c : PolyCert) (t u : Poly) :
    checkPolyCode (encode c) (encode t) (encode u) = checkPoly c t u := by
  induction c generalizing t u with
  | refl p =>
    rw [checkPolyCode,evaluate]
    simp only [encode_poly_refl,polyShape,polyChildren,pack,List.foldr_cons,List.foldr_nil,
      a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,
      unpair_leaf,lhs_pair,rhs_pair,tmApp_exact,polyApp_exact,polyAtom_exact,encode_injective.eq_iff,checkPoly]
    simp [eval_poly, Bool.and_assoc]
  | symm p q c ihc =>
    have hc : encode c < encode (.symm p q c : PolyCert) := by
      rw [encode_poly_symm]; exact field_lt_pack _ _ (by simp)
    rw [checkPolyCode,evaluate]
    simp only [encode_poly_symm,polyShape,polyChildren,pack,List.foldr_cons,List.foldr_nil,
      a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,
      unpair_leaf,lhs_pair,rhs_pair,tmApp_exact,polyApp_exact,polyAtom_exact,encode_injective.eq_iff,checkPoly]
    simp only [encode_poly_symm,pack,List.foldr_cons,List.foldr_nil] at hc
    simp [hc, eval_poly, ihc, Bool.and_assoc]
  | trans p q r c d ihc ihd =>
    have hc : encode c < encode (.trans p q r c d : PolyCert) := by
      rw [encode_poly_trans]; exact field_lt_pack _ _ (by simp)
    have hd : encode d < encode (.trans p q r c d : PolyCert) := by
      rw [encode_poly_trans]; exact field_lt_pack _ _ (by simp)
    rw [checkPolyCode,evaluate]
    simp only [encode_poly_trans,polyShape,polyChildren,pack,List.foldr_cons,List.foldr_nil,
      a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,
      unpair_leaf,lhs_pair,rhs_pair,tmApp_exact,polyApp_exact,polyAtom_exact,encode_injective.eq_iff,checkPoly]
    simp only [encode_poly_trans,pack,List.foldr_cons,List.foldr_nil] at hc
    simp only [encode_poly_trans,pack,List.foldr_cons,List.foldr_nil] at hd
    simp [hc, hd, eval_poly, ihc, ihd, Bool.and_assoc]
  | app f g p q c d ihc ihd =>
    have hc : encode c < encode (.app f g p q c d : PolyCert) := by
      rw [encode_poly_app]; exact field_lt_pack _ _ (by simp)
    have hd : encode d < encode (.app f g p q c d : PolyCert) := by
      rw [encode_poly_app]; exact field_lt_pack _ _ (by simp)
    rw [checkPolyCode,evaluate]
    simp only [encode_poly_app,polyShape,polyChildren,pack,List.foldr_cons,List.foldr_nil,
      a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,
      unpair_leaf,lhs_pair,rhs_pair,tmApp_exact,polyApp_exact,polyAtom_exact,encode_injective.eq_iff,checkPoly]
    simp only [encode_poly_app,pack,List.foldr_cons,List.foldr_nil] at hc
    simp only [encode_poly_app,pack,List.foldr_cons,List.foldr_nil] at hd
    simp [hc, hd, eval_poly, ihc, ihd, Bool.and_assoc]
  | i p =>
    rw [checkPolyCode,evaluate]
    simp only [encode_poly_i,polyShape,polyChildren,pack,List.foldr_cons,List.foldr_nil,
      a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,
      unpair_leaf,lhs_pair,rhs_pair,tmApp_exact,polyApp_exact,polyAtom_exact,encode_injective.eq_iff,checkPoly]
    simp [eval_poly, Bool.and_assoc]
  | k p q =>
    rw [checkPolyCode,evaluate]
    simp only [encode_poly_k,polyShape,polyChildren,pack,List.foldr_cons,List.foldr_nil,
      a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,
      unpair_leaf,lhs_pair,rhs_pair,tmApp_exact,polyApp_exact,polyAtom_exact,encode_injective.eq_iff,checkPoly]
    simp [eval_poly, Bool.and_assoc]
  | s p q r =>
    rw [checkPolyCode,evaluate]
    simp only [encode_poly_s,polyShape,polyChildren,pack,List.foldr_cons,List.foldr_nil,
      a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,
      unpair_leaf,lhs_pair,rhs_pair,tmApp_exact,polyApp_exact,polyAtom_exact,encode_injective.eq_iff,checkPoly]
    simp [eval_poly, Bool.and_assoc]
  | bridge r t =>
    rw [checkPolyCode,evaluate]
    simp only [encode_poly_bridge,polyShape,polyChildren,pack,List.foldr_cons,List.foldr_nil,
      a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,
      unpair_leaf,lhs_pair,rhs_pair,tmApp_exact,polyApp_exact,polyAtom_exact,encode_injective.eq_iff,checkPoly]
    simp [eval_poly, Bool.and_assoc]

#print axioms primrec_checkPolyCode
#print axioms checkPolyCode_exact
end AuxiliaryCodeComputability
