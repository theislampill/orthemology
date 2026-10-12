import LookupCode
import PolyExact
namespace IndependentAuxiliaryCodeReview
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity CodedPolyTransformations CodedMixedTransformations AuxiliaryCodeComputability AuxiliaryCertificates OrthemologyV2 OrthemologyV3 P01D P01AC
set_option maxRecDepth 8192
set_option maxHeartbeats 1000000
attribute [local irreducible] Nat.pair wkTyCode instantiateTypeCode checkStepCode checkRedCode
-- Raw finite code equations: direct definitions, never checker exactness.
theorem step_i_shape (a b x : Nat) :
    AuxiliaryCodeComputability.stepShape (Nat.pair a b,pack 0 [leaf x]) = (decide (a = tmApp (encode Term.i) x) && decide (b = x)) := by
  simp only [AuxiliaryCodeComputability.stepShape,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem step_i_children (a b x : Nat) :
    AuxiliaryCodeComputability.stepChildren (Nat.pair a b,pack 0 [leaf x]) = ([]) := by
  simp only [AuxiliaryCodeComputability.stepChildren,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem step_k_shape (a b x y : Nat) :
    AuxiliaryCodeComputability.stepShape (Nat.pair a b,pack 1 [leaf x, leaf y]) = (decide (a = tmApp (tmApp (encode Term.k) x) y) && decide (b = x)) := by
  simp only [AuxiliaryCodeComputability.stepShape,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem step_k_children (a b x y : Nat) :
    AuxiliaryCodeComputability.stepChildren (Nat.pair a b,pack 1 [leaf x, leaf y]) = ([]) := by
  simp only [AuxiliaryCodeComputability.stepChildren,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem step_s_shape (a b x y z : Nat) :
    AuxiliaryCodeComputability.stepShape (Nat.pair a b,pack 2 [leaf x, leaf y, leaf z]) = (decide (a = tmApp (tmApp (tmApp (encode Term.s) x) y) z) && decide (b = tmApp (tmApp x z) (tmApp y z))) := by
  simp only [AuxiliaryCodeComputability.stepShape,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem step_s_children (a b x y z : Nat) :
    AuxiliaryCodeComputability.stepChildren (Nat.pair a b,pack 2 [leaf x, leaf y, leaf z]) = ([]) := by
  simp only [AuxiliaryCodeComputability.stepChildren,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem step_left_shape (a b x y z c : Nat) :
    AuxiliaryCodeComputability.stepShape (Nat.pair a b,pack 3 [leaf x, leaf y, leaf z, c]) = (decide (a = tmApp x z) && decide (b = tmApp y z)) := by
  simp only [AuxiliaryCodeComputability.stepShape,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem step_left_children (a b x y z c : Nat) :
    AuxiliaryCodeComputability.stepChildren (Nat.pair a b,pack 3 [leaf x, leaf y, leaf z, c]) = ([(Nat.pair x y,c)]) := by
  simp only [AuxiliaryCodeComputability.stepChildren,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem step_right_shape (a b x y z c : Nat) :
    AuxiliaryCodeComputability.stepShape (Nat.pair a b,pack 4 [leaf x, leaf y, leaf z, c]) = (decide (a = tmApp x y) && decide (b = tmApp x z)) := by
  simp only [AuxiliaryCodeComputability.stepShape,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem step_right_children (a b x y z c : Nat) :
    AuxiliaryCodeComputability.stepChildren (Nat.pair a b,pack 4 [leaf x, leaf y, leaf z, c]) = ([(Nat.pair y z,c)]) := by
  simp only [AuxiliaryCodeComputability.stepChildren,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem red_refl_shape (a b x : Nat) :
    AuxiliaryCodeComputability.redShape (Nat.pair a b,pack 0 [leaf x]) = (decide (a = x) && decide (b = x)) := by
  simp only [AuxiliaryCodeComputability.redShape,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem red_refl_children (a b x : Nat) :
    AuxiliaryCodeComputability.redChildren (Nat.pair a b,pack 0 [leaf x]) = ([]) := by
  simp only [AuxiliaryCodeComputability.redChildren,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem red_tail_shape (a b x y z c d : Nat) :
    AuxiliaryCodeComputability.redShape (Nat.pair a b,pack 1 [leaf x, leaf y, leaf z, leaf c, d]) = ((decide (a = x) && decide (b = z)) && checkStepCode c x y) := by
  simp only [AuxiliaryCodeComputability.redShape,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem red_tail_children (a b x y z c d : Nat) :
    AuxiliaryCodeComputability.redChildren (Nat.pair a b,pack 1 [leaf x, leaf y, leaf z, leaf c, d]) = ([(Nat.pair y z,d)]) := by
  simp only [AuxiliaryCodeComputability.redChildren,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem finite_i_shape (a b x : Nat) :
    AuxiliaryCodeComputability.finiteShape (Nat.pair a b,pack 0 [leaf x]) = (decide (a = encode Term.i) && decide (b = tyArrow x x)) := by
  simp only [AuxiliaryCodeComputability.finiteShape,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem finite_i_children (a b x : Nat) :
    AuxiliaryCodeComputability.finiteChildren (Nat.pair a b,pack 0 [leaf x]) = ([]) := by
  simp only [AuxiliaryCodeComputability.finiteChildren,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem finite_k_shape (a b x y : Nat) :
    AuxiliaryCodeComputability.finiteShape (Nat.pair a b,pack 1 [leaf x, leaf y]) = (decide (a = encode Term.k) && decide (b = tyArrow x (tyArrow y x))) := by
  simp only [AuxiliaryCodeComputability.finiteShape,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem finite_k_children (a b x y : Nat) :
    AuxiliaryCodeComputability.finiteChildren (Nat.pair a b,pack 1 [leaf x, leaf y]) = ([]) := by
  simp only [AuxiliaryCodeComputability.finiteChildren,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem finite_s_shape (a b x y z : Nat) :
    AuxiliaryCodeComputability.finiteShape (Nat.pair a b,pack 2 [leaf x, leaf y, leaf z]) = (decide (a = encode Term.s) && decide (b = tyArrow (tyArrow x (tyArrow y z)) (tyArrow (tyArrow x y) (tyArrow x z)))) := by
  simp only [AuxiliaryCodeComputability.finiteShape,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem finite_s_children (a b x y z : Nat) :
    AuxiliaryCodeComputability.finiteChildren (Nat.pair a b,pack 2 [leaf x, leaf y, leaf z]) = ([]) := by
  simp only [AuxiliaryCodeComputability.finiteChildren,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem finite_app_shape (a b x y z w c d : Nat) :
    AuxiliaryCodeComputability.finiteShape (Nat.pair a b,pack 3 [leaf x, leaf y, leaf z, leaf w, c, d]) = (decide (a = tmApp x y) && decide (b = w)) := by
  simp only [AuxiliaryCodeComputability.finiteShape,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem finite_app_children (a b x y z w c d : Nat) :
    AuxiliaryCodeComputability.finiteChildren (Nat.pair a b,pack 3 [leaf x, leaf y, leaf z, leaf w, c, d]) = ([(Nat.pair x (tyArrow z w),c),(Nat.pair y z,d)]) := by
  simp only [AuxiliaryCodeComputability.finiteChildren,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem finite_allI_shape (a b x y c : Nat) :
    AuxiliaryCodeComputability.finiteShape (Nat.pair a b,pack 4 [leaf x, leaf y, c]) = (decide (a = x) && decide (b = tyAll y)) := by
  simp only [AuxiliaryCodeComputability.finiteShape,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem finite_allI_children (a b x y c : Nat) :
    AuxiliaryCodeComputability.finiteChildren (Nat.pair a b,pack 4 [leaf x, leaf y, c]) = ([(Nat.pair x y,c)]) := by
  simp only [AuxiliaryCodeComputability.finiteChildren,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem finite_allE_shape (a b x y z c : Nat) :
    AuxiliaryCodeComputability.finiteShape (Nat.pair a b,pack 5 [leaf x, leaf y, leaf z, c]) = (decide (a = x) && decide (b = instantiateTypeCode z y)) := by
  simp only [AuxiliaryCodeComputability.finiteShape,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem finite_allE_children (a b x y z c : Nat) :
    AuxiliaryCodeComputability.finiteChildren (Nat.pair a b,pack 5 [leaf x, leaf y, leaf z, c]) = ([(Nat.pair x (tyAll y),c)]) := by
  simp only [AuxiliaryCodeComputability.finiteChildren,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem finite_reduce_shape (a b x y z c d : Nat) :
    AuxiliaryCodeComputability.finiteShape (Nat.pair a b,pack 6 [leaf x, leaf y, leaf z, c, leaf d]) = ((decide (a = y) && decide (b = z)) && checkRedCode d x y) := by
  simp only [AuxiliaryCodeComputability.finiteShape,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem finite_reduce_children (a b x y z c d : Nat) :
    AuxiliaryCodeComputability.finiteChildren (Nat.pair a b,pack 6 [leaf x, leaf y, leaf z, c, leaf d]) = ([(Nat.pair x z,c)]) := by
  simp only [AuxiliaryCodeComputability.finiteChildren,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem poly_refl_shape (a b x : Nat) :
    AuxiliaryCodeComputability.polyShape (Nat.pair a b,pack 0 [leaf x]) = (decide (a = x) && decide (b = x)) := by
  simp only [AuxiliaryCodeComputability.polyShape,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem poly_refl_children (a b x : Nat) :
    AuxiliaryCodeComputability.polyChildren (Nat.pair a b,pack 0 [leaf x]) = ([]) := by
  simp only [AuxiliaryCodeComputability.polyChildren,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem poly_symm_shape (a b x y c : Nat) :
    AuxiliaryCodeComputability.polyShape (Nat.pair a b,pack 1 [leaf x, leaf y, c]) = (decide (a = y) && decide (b = x)) := by
  simp only [AuxiliaryCodeComputability.polyShape,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem poly_symm_children (a b x y c : Nat) :
    AuxiliaryCodeComputability.polyChildren (Nat.pair a b,pack 1 [leaf x, leaf y, c]) = ([(Nat.pair x y,c)]) := by
  simp only [AuxiliaryCodeComputability.polyChildren,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem poly_trans_shape (a b x y z c d : Nat) :
    AuxiliaryCodeComputability.polyShape (Nat.pair a b,pack 2 [leaf x, leaf y, leaf z, c, d]) = (decide (a = x) && decide (b = z)) := by
  simp only [AuxiliaryCodeComputability.polyShape,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem poly_trans_children (a b x y z c d : Nat) :
    AuxiliaryCodeComputability.polyChildren (Nat.pair a b,pack 2 [leaf x, leaf y, leaf z, c, d]) = ([(Nat.pair x y,c),(Nat.pair y z,d)]) := by
  simp only [AuxiliaryCodeComputability.polyChildren,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem poly_app_shape (a b x y z w c d : Nat) :
    AuxiliaryCodeComputability.polyShape (Nat.pair a b,pack 3 [leaf x, leaf y, leaf z, leaf w, c, d]) = (decide (a = polyApp x z) && decide (b = polyApp y w)) := by
  simp only [AuxiliaryCodeComputability.polyShape,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem poly_app_children (a b x y z w c d : Nat) :
    AuxiliaryCodeComputability.polyChildren (Nat.pair a b,pack 3 [leaf x, leaf y, leaf z, leaf w, c, d]) = ([(Nat.pair x y,c),(Nat.pair z w,d)]) := by
  simp only [AuxiliaryCodeComputability.polyChildren,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem poly_i_shape (a b x : Nat) :
    AuxiliaryCodeComputability.polyShape (Nat.pair a b,pack 4 [leaf x]) = (decide (a = polyApp (polyAtom (encode Term.i)) x) && decide (b = x)) := by
  simp only [AuxiliaryCodeComputability.polyShape,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem poly_i_children (a b x : Nat) :
    AuxiliaryCodeComputability.polyChildren (Nat.pair a b,pack 4 [leaf x]) = ([]) := by
  simp only [AuxiliaryCodeComputability.polyChildren,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem poly_k_shape (a b x y : Nat) :
    AuxiliaryCodeComputability.polyShape (Nat.pair a b,pack 5 [leaf x, leaf y]) = (decide (a = polyApp (polyApp (polyAtom (encode Term.k)) x) y) && decide (b = x)) := by
  simp only [AuxiliaryCodeComputability.polyShape,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem poly_k_children (a b x y : Nat) :
    AuxiliaryCodeComputability.polyChildren (Nat.pair a b,pack 5 [leaf x, leaf y]) = ([]) := by
  simp only [AuxiliaryCodeComputability.polyChildren,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem poly_s_shape (a b x y z : Nat) :
    AuxiliaryCodeComputability.polyShape (Nat.pair a b,pack 6 [leaf x, leaf y, leaf z]) = (decide (a = polyApp (polyApp (polyApp (polyAtom (encode Term.s)) x) y) z) && decide (b = polyApp (polyApp x z) (polyApp y z))) := by
  simp only [AuxiliaryCodeComputability.polyShape,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem poly_s_children (a b x y z : Nat) :
    AuxiliaryCodeComputability.polyChildren (Nat.pair a b,pack 6 [leaf x, leaf y, leaf z]) = ([]) := by
  simp only [AuxiliaryCodeComputability.polyChildren,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem poly_bridge_shape (a b x y : Nat) :
    AuxiliaryCodeComputability.polyShape (Nat.pair a b,pack 7 [leaf x, leaf y]) = (decide (a = polyAtom (tmApp x y)) && decide (b = polyApp (polyAtom x) (polyAtom y))) := by
  simp only [AuxiliaryCodeComputability.polyShape,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem poly_bridge_children (a b x y : Nat) :
    AuxiliaryCodeComputability.polyChildren (Nat.pair a b,pack 7 [leaf x, leaf y]) = ([]) := by
  simp only [AuxiliaryCodeComputability.polyChildren,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem lookup_zero_shape (a b n x y : Nat) :
    AuxiliaryCodeComputability.lookupShape (Nat.pair a (Nat.pair n b),pack 0 [leaf x, leaf y]) = ((decide (a = telCons y x) && decide (n = 0)) && decide (b = wkTyCode y)) := by
  simp only [AuxiliaryCodeComputability.lookupShape,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem lookup_zero_children (a b n x y : Nat) :
    AuxiliaryCodeComputability.lookupChildren (Nat.pair a (Nat.pair n b),pack 0 [leaf x, leaf y]) = ([]) := by
  simp only [AuxiliaryCodeComputability.lookupChildren,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem lookup_succ_shape (a b n x y z w c : Nat) :
    AuxiliaryCodeComputability.lookupShape (Nat.pair a (Nat.pair n b),pack 1 [leaf x, leaf y, leaf z, leaf w, c]) = ((decide (a = telCons w x) && decide (n = y+1)) && decide (b = wkTyCode z)) := by
  simp only [AuxiliaryCodeComputability.lookupShape,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

theorem lookup_succ_children (a b n x y z w c : Nat) :
    AuxiliaryCodeComputability.lookupChildren (Nat.pair a (Nat.pair n b),pack 1 [leaf x, leaf y, leaf z, leaf w, c]) = ([(Nat.pair x (Nat.pair y z),c)]) := by
  simp only [AuxiliaryCodeComputability.lookupChildren,pack,List.foldr_cons,List.foldr_nil,a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,unpair_leaf,lhs_pair,rhs_pair,lookupIndex_pair,lookupType_pair]
  simp

-- Complete evaluator reductions, rather than only local shape checks.
theorem step_i_full (x : Nat) : checkStepCode (pack 0 [leaf x]) (tmApp (encode Term.i) x) x = true := by
  rw [checkStepCode,evaluate]
  simp [step_i_shape,step_i_children]
theorem red_refl_full (x : Nat) : checkRedCode (pack 0 [leaf x]) x x = true := by
  rw [checkRedCode,evaluate]
  simp [red_refl_shape,red_refl_children]
theorem finite_i_full (x : Nat) : checkFiniteCode (pack 0 [leaf x]) (encode Term.i) (tyArrow x x) = true := by
  rw [checkFiniteCode,evaluate]
  simp [finite_i_shape,finite_i_children]
theorem poly_bridge_full (x y : Nat) : checkPolyCode (pack 7 [leaf x,leaf y]) (polyAtom (tmApp x y)) (polyApp (polyAtom x) (polyAtom y)) = true := by
  rw [checkPolyCode,evaluate]
  simp [poly_bridge_shape,poly_bridge_children]
theorem lookup_zero_full (g a : Nat) : checkLookupCode (pack 0 [leaf g,leaf a]) (telCons a g) 0 (wkTyCode a) = true := by
  rw [checkLookupCode,evaluate]
  simp [lookup_zero_shape,lookup_zero_children]

theorem lookup_successor_recurrence (g n a b c : Nat) :
    checkLookupCode (pack 1 [leaf g,leaf n,leaf a,leaf b,c]) (telCons b g) (n+1) (wkTyCode a) =
    checkLookupCode c g n a := by
  have hc : c < pack 1 [leaf g,leaf n,leaf a,leaf b,c] := field_lt_pack _ _ (by simp)
  rw [checkLookupCode,evaluate]
  simp [lookup_succ_shape,lookup_succ_children,hc,eval_lookup]

-- Two successors enforce three actual weakenings from the initial stored type.
theorem lookup_three_weakenings (a b d : Nat) :
  let c0 := pack 0 [leaf 0,leaf a]
  let g1 := telCons a 0
  let c1 := pack 1 [leaf g1,leaf 0,leaf (wkTyCode a),leaf b,c0]
  let g2 := telCons b g1
  let c2 := pack 1 [leaf g2,leaf 1,leaf (wkTyCode (wkTyCode a)),leaf d,c1]
  checkLookupCode c2 (telCons d g2) 2 (wkTyCode (wkTyCode (wkTyCode a))) = true := by
  dsimp only
  rw [lookup_successor_recurrence,lookup_successor_recurrence,lookup_zero_full]
end IndependentAuxiliaryCodeReview
