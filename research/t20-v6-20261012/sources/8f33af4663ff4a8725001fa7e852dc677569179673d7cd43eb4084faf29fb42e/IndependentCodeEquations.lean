import FiniteTypeCodeCompilation
namespace IndependentMixedCodeReview
open P01D P01AC OrthemologyV2 OrthemologyV3 Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity CodedPolyTransformations CodedMixedTransformations
set_option maxRecDepth 8192
set_option maxHeartbeats 2000000
-- Direct unfolding/codec arithmetic only: no transformation exactness theorem.
theorem term_lift_shape (p t ps ts : Nat) (b : Bool) :
  termLift (([p],ps),([t],b,ts)) =
  (([varCode 0,shiftCode 1 p],ps+1),([wkTyCode t],b,ts)) := rfl

theorem type_lift_shape (p t ps ts : Nat) (b : Bool) :
  typeLift (([p],ps),([t],b,ts)) =
  (([p],ps),([paramCode 0,twkCode t],b,ts+1)) := rfl

theorem bottom_tail_ignores_shift (s n : Nat) :
  typeImageCode ([],false,s) n = encode Ty.bottom := rfl

theorem shifted_tail_tracks_shift (s n : Nat) :
  typeImageCode ([],true,s) n = paramCode (n+s) := rfl

theorem all_child (e : MixedEnvCode) (B : Ty) :
  mixedChildren (e,encode (Ty.all B)) = [(typeLift e,encode B)] := by simp [mixedChildren]
theorem pi_children (e : MixedEnvCode) (A B : Ty) :
  mixedChildren (e,encode (Ty.pi A B)) = [(e,encode A),(termLift e,encode B)] := by simp [mixedChildren]
theorem sigma_children (e : MixedEnvCode) (A B : Ty) :
  mixedChildren (e,encode (Ty.sigma A B)) = [(e,encode A),(termLift e,encode B)] := by simp [mixedChildren]

theorem rename_pi_no_lift (e : List Nat × Nat) (A B : Ty) :
  renameTyChildren (e,encode (Ty.pi A B)) = [(e,encode A),(e,encode B)] := by simp [renameTyChildren]
theorem rename_all_lifts (e : List Nat × Nat) (B : Ty) :
  renameTyChildren (e,encode (Ty.all B)) = [(liftRenCode e,encode B)] := by simp [renameTyChildren]

theorem fin_arrow_step (A B : TypeCode) (a b : Nat) :
  finStep (([],0),encode (TypeCode.arrow A B)) [a,b] = binary 4 a (wkTyCode b) := by simp [finStep]
theorem support_all_step (B : TypeCode) (n : Nat) :
  supportStep (([],0),encode (TypeCode.all B)) [n] = n-1 := by simp [supportStep]
theorem support_arrow_step (A B : TypeCode) (a b : Nat) :
  supportStep (([],0),encode (TypeCode.arrow A B)) [a,b] = max a b := by simp [supportStep]

theorem tc_sub_all_lifts (e : List Nat × Nat) (B : TypeCode) :
  tcSubChildren (e,encode (TypeCode.all B)) = [(liftTCEnv e,encode B)] := by simp [tcSubChildren]
theorem tinst_boundary (a b : Nat) :
  tinstCode a b = mixedCode (([],0),([a],true,0)) b := rfl
theorem images_boundary (xs : List Nat) (b : Nat) :
  tsubstImagesCode xs b = mixedCode (([],0),(xs,false,0)) b := rfl

-- A direct full realizer reduction on a genuine parameter input.
theorem mixed_missing_param (n : Nat) :
  mixedCode (([],0),([],false,0)) (encode (Ty.param n)) = encode Ty.bottom := by
  rw [mixedCode_eq]
  simp [mixedStep,typeImageCode]
end IndependentMixedCodeReview
