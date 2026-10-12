import TypeRenaming
namespace CodedMixedTransformations
open P01D P01AC OrthemologyV3 Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity CodedPolyTransformations
set_option maxRecDepth 8192
set_option maxHeartbeats 12000000

abbrev TypeEnvCode := List Nat × Bool × Nat
abbrev SourceTypeEnv := List Ty × Bool × Nat
abbrev SourcePolyEnv := List Poly × Nat
abbrev MixedEnvCode := (List Nat × Nat) × TypeEnvCode

def finiteTyEnv (images : List Ty) (variableTail : Bool) (shift n : Nat) : Ty :=
  images[n]?.getD (bif variableTail then .param (n-images.length+shift) else .bottom)

def typeImageCode (env : TypeEnvCode) (n : Nat) : Nat :=
  env.1[n]?.getD (bif env.2.1 then paramCode (n-env.1.length+env.2.2) else encode Ty.bottom)

def encodeEnv (p : SourcePolyEnv) (t : SourceTypeEnv) : MixedEnvCode :=
  ((p.1.map encode,p.2),(t.1.map encode,t.2))

def termLift (env : MixedEnvCode) : MixedEnvCode :=
  (liftEnvCode env.1,(env.2.1.map wkTyCode,env.2.2))
def typeLift (env : MixedEnvCode) : MixedEnvCode :=
  (env.1,(paramCode 0 :: env.2.1.map twkCode,env.2.2.1,env.2.2.2+1))

def sourcePLift (env : SourcePolyEnv) : SourcePolyEnv :=
  (.var 0 :: env.1.map (pren Nat.succ), env.2+1)
def sourceTTermLift (env : SourceTypeEnv) : SourceTypeEnv := (env.1.map wk,env.2)
def sourceTTypeLift (env : SourceTypeEnv) : SourceTypeEnv :=
  (.param 0 :: env.1.map twk,env.2.1,env.2.2+1)

theorem primrec_typeImageCode : Primrec₂ typeImageCode := by
  have hl : Primrec (fun p : TypeEnvCode × Nat => p.1.1) := Primrec.fst.comp Primrec.fst
  have ht : Primrec (fun p : TypeEnvCode × Nat => p.1.2.1) := Primrec.fst.comp (Primrec.snd.comp Primrec.fst)
  have hs : Primrec (fun p : TypeEnvCode × Nat => p.1.2.2) := Primrec.snd.comp (Primrec.snd.comp Primrec.fst)
  exact Primrec.option_getD.comp (Primrec.list_getElem?.comp hl Primrec.snd)
    (Primrec.cond ht (primrec_paramCode.comp
      (Primrec.nat_add.comp (Primrec.nat_sub.comp Primrec.snd (Primrec.list_length.comp hl)) hs)) (.const _))

theorem primrec_termLift : Primrec termLift :=
  (primrec_liftEnvCode.comp Primrec.fst).pair
    ((Primrec.list_map (Primrec.fst.comp Primrec.snd) (primrec_wkTyCode.comp Primrec.snd).to₂).pair
      (Primrec.snd.comp Primrec.snd))

theorem primrec_typeLift : Primrec typeLift :=
  Primrec.fst.pair
    ((Primrec.list_cons.comp (.const _)
      (Primrec.list_map (Primrec.fst.comp Primrec.snd) (primrec_twkCode.comp Primrec.snd).to₂)).pair
      ((Primrec.fst.comp (Primrec.snd.comp Primrec.snd)).pair
        (Primrec.succ.comp (Primrec.snd.comp (Primrec.snd.comp Primrec.snd)))))

theorem typeImageCode_exact (images : List Ty) (mode : Bool) (shift n : Nat) :
    typeImageCode (images.map encode,mode,shift) n = encode (finiteTyEnv images mode shift n) := by
  simp only [typeImageCode,finiteTyEnv,List.getElem?_map,List.length_map]
  cases h : images[n]? <;> cases mode <;> simp [h,paramCode]

theorem finiteTyEnv_term (images : List Ty) (mode : Bool) (shift : Nat) :
    finiteTyEnv (images.map wk) mode shift = fun n => wk (finiteTyEnv images mode shift n) := by
  funext n
  simp only [finiteTyEnv,List.getElem?_map,List.length_map]
  cases h : images[n]? <;> cases mode <;> simp [h,wk,subst]

theorem finiteTyEnv_type (images : List Ty) (mode : Bool) (shift : Nat) :
    finiteTyEnv (.param 0 :: images.map twk) mode (shift+1) = tup (finiteTyEnv images mode shift) := by
  funext n
  cases n with
  | zero => simp [finiteTyEnv,tup,P01F.cons]
  | succ n =>
    simp only [finiteTyEnv,tup,P01F.cons,List.getElem?_cons_succ,List.getElem?_map,List.length_cons,List.length_map]
    cases h : images[n]? <;> cases mode <;> simp [h,twk,trename,Nat.add_assoc]

theorem termLift_exact (p : SourcePolyEnv) (t : SourceTypeEnv) :
    termLift (encodeEnv p t) = encodeEnv (sourcePLift p) (sourceTTermLift t) := by
  simp [termLift,encodeEnv,sourcePLift,sourceTTermLift,liftEnvCode_exact,List.map_map,
    Function.comp_def,wkTyCode_exact]

theorem typeLift_exact (p : SourcePolyEnv) (t : SourceTypeEnv) :
    typeLift (encodeEnv p t) = encodeEnv p (sourceTTypeLift t) := by
  simp [typeLift,encodeEnv,sourceTTypeLift,paramCode,List.map_map,Function.comp_def,twkCode_exact]

#print axioms primrec_termLift
#print axioms finiteTyEnv_type
#print axioms typeLift_exact
end CodedMixedTransformations
