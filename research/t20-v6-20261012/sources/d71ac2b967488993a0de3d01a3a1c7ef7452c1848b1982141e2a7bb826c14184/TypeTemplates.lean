import PolyTemplates
namespace CodedRuleTemplates
open P01D P01AC Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity CodedPolyTransformations CodedMixedTransformations
set_option maxRecDepth 8192
set_option maxHeartbeats 10000000
attribute [local irreducible] Nat.pair

def arrCode (A B : Nat) := binary 4 A (wkTyCode B)
def identityTyCode (A p q : Nat) := ternary 6 A (leaf p) (leaf q)
def motiveAtCode (B y e : Nat) := substTyCode ([e,y],0) B

theorem primrec_arrCode : Primrec₂ arrCode := (primrec_binary_fixed 4).comp Primrec.fst (primrec_wkTyCode.comp Primrec.snd)
theorem primrec_identityTyCode : Primrec (fun s : Nat × Nat × Nat => identityTyCode s.1 s.2.1 s.2.2) :=
  primrec_node.comp (.const _) (primrec_node.comp Primrec.fst
    (primrec_node.comp (primrec_leaf.comp (Primrec.fst.comp Primrec.snd))
      (primrec_node.comp (primrec_leaf.comp (Primrec.snd.comp Primrec.snd)) (.const _))))
theorem primrec_motiveAtCode : Primrec (fun s : Nat × Nat × Nat => motiveAtCode s.1 s.2.1 s.2.2) :=
  primrec_substTyCode.comp ((Primrec.list_cons.comp (Primrec.snd.comp Primrec.snd)
    (Primrec.list_cons.comp (Primrec.fst.comp Primrec.snd) (.const []))).pair (.const 0)) Primrec.fst

@[simp] theorem arrCode_exact (A B : Ty) : arrCode (encode A) (encode B) = encode (arr A B) := by
  simp only [arrCode,wkTyCode_exact,arr,encode_ty_pi]
@[simp] theorem identityTyCode_exact (A : Ty) (p q : Poly) : identityTyCode (encode A) (encode p) (encode q) = encode (A.identity p q) := rfl
@[simp] theorem motiveAtCode_exact (B : Ty) (y e : Poly) : motiveAtCode (encode B) (encode y) (encode e) = encode (motiveAt B y e) := by
  simpa only [motiveAtCode,List.map_cons,List.map_nil,finiteEnv_double,motiveAt] using substTyCode_exact [e,y] 0 B

theorem finiteEnv_pairSub : finiteEnv [pairPoly (.var 1) (.var 0)] 2 = SigmaCompletion.pairSub := by
  funext n; cases n <;> simp [finiteEnv,SigmaCompletion.pairSub,P01F.cons]
theorem finiteEnv_successor : finiteEnv [BooleanPrimitive.succPoly.app (.var 0)] 1 =
    P01F.cons (BooleanPrimitive.succPoly.app (.var 0)) (fun k => Poly.var (k+1)) := by
  funext n; cases n <;> simp [finiteEnv,P01F.cons]

def branchTypeCode (P : Nat) := substTyCode ([encode (pairPoly (.var 1) (.var 0))],2) P
def successorFamilyCode (P : Nat) := substTyCode ([encode (BooleanPrimitive.succPoly.app (.var 0))],1) P
def dependentStepTypeCode (P : Nat) := binary 4 (encode EffectiveCompleteness.N) (arrCode P (successorFamilyCode P))

theorem primrec_branchTypeCode : Primrec branchTypeCode := primrec_substTyCode.comp (.const _) Primrec.id
theorem primrec_successorFamilyCode : Primrec successorFamilyCode := primrec_substTyCode.comp (.const _) Primrec.id
theorem primrec_dependentStepTypeCode : Primrec dependentStepTypeCode :=
  (primrec_binary_fixed 4).comp (.const _) (primrec_arrCode.comp Primrec.id primrec_successorFamilyCode)

@[simp] theorem branchTypeCode_exact (P : Ty) : branchTypeCode (encode P) = encode (SigmaCompletion.branchType P) := by
  simpa only [branchTypeCode,List.map_cons,List.map_nil,finiteEnv_pairSub,SigmaCompletion.branchType] using substTyCode_exact [pairPoly (.var 1) (.var 0)] 2 P
@[simp] theorem successorFamilyCode_exact (P : Ty) : successorFamilyCode (encode P) = encode (RigidityInitiality.successorFamily P) := by
  simpa only [successorFamilyCode,List.map_cons,List.map_nil,finiteEnv_successor,RigidityInitiality.successorFamily] using substTyCode_exact [BooleanPrimitive.succPoly.app (.var 0)] 1 P
@[simp] theorem dependentStepTypeCode_exact (P : Ty) : dependentStepTypeCode (encode P) = encode (RigidityInitiality.dependentStepType P) := by
  simp only [dependentStepTypeCode,successorFamilyCode_exact,arrCode_exact,← encode_ty_pi,RigidityInitiality.dependentStepType]

def thetaListCode (Γ : List Nat) (A x : Nat) := identityTyCode (wkTyCode A) (shiftCode 1 x) (encode (Poly.var 0)) :: A :: Γ

theorem primrec_thetaListCode : Primrec (fun s : List Nat × Nat × Nat => thetaListCode s.1 s.2.1 s.2.2) :=
  Primrec.list_cons.comp
    (primrec_identityTyCode.comp ((primrec_wkTyCode.comp (Primrec.fst.comp Primrec.snd)).pair
      ((primrec_shiftCode.comp (.const 1) (Primrec.snd.comp Primrec.snd)).pair (.const _))))
    (Primrec.list_cons.comp (Primrec.fst.comp Primrec.snd) Primrec.fst)

@[simp] theorem thetaListCode_exact (Γ : Tel) (A : Ty) (x : Poly) : thetaListCode (Γ.map encode) (encode A) (encode x) = (theta Γ A x).map encode := by
  simp only [thetaListCode,wkTyCode_exact,shiftCode_one_exact,identityTyCode_exact,theta,List.map_cons]

end CodedRuleTemplates
