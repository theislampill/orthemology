import TypeCodeRenaming
namespace CodedMixedTransformations
open OrthemologyV2 OrthemologyV3 Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity CodedPolyTransformations
set_option maxRecDepth 8192
set_option maxHeartbeats 12000000

def finiteTCEnv (images : List TypeCode) (shift n : Nat) : TypeCode :=
  images[n]?.getD (.var (n-images.length+shift))
def liftTCEnv (env : List Nat × Nat) : List Nat × Nat :=
  (paramCode 0 :: env.1.map shiftTypeCode,env.2+1)

theorem primrec_liftTCEnv : Primrec liftTCEnv :=
  (Primrec.list_cons.comp (.const _)
    (Primrec.list_map Primrec.fst (primrec_shiftTypeCode.comp Primrec.snd).to₂)).pair
    (Primrec.succ.comp Primrec.snd)

theorem tcImage_exact (images : List TypeCode) (shift n : Nat) :
    imageCode (images.map encode,shift) n = encode (finiteTCEnv images shift n) := by
  simp only [imageCode,finiteTCEnv,List.getElem?_map,List.length_map]
  cases h : images[n]? <;> simp [h,varCode,unary]

theorem finiteTCEnv_lift (images : List TypeCode) (shift : Nat) :
    finiteTCEnv (.var 0 :: images.map (rename Nat.succ)) (shift+1) = upSub (finiteTCEnv images shift) := by
  funext n
  cases n with
  | zero => simp [finiteTCEnv,upSub]
  | succ n =>
    simp only [finiteTCEnv,upSub,List.getElem?_cons_succ,List.getElem?_map,List.length_cons,List.length_map]
    cases h : images[n]? <;> simp [h,rename,Nat.add_assoc]

theorem liftTCEnv_exact (images : List TypeCode) (shift : Nat) :
    liftTCEnv (images.map encode,shift) =
      ((.var 0 :: images.map (rename Nat.succ)).map encode,shift+1) := by
  simp [liftTCEnv,paramCode,List.map_map,Function.comp_def,shiftTypeCode_exact]

def tcSubChildren (s : SubstState) : List SubstState :=
  if tag s.2 = 2 then [(liftTCEnv s.1,arg1 s.2)]
  else if tag s.2 = 1 then [(s.1,arg1 s.2),(s.1,arg2 s.2)] else []
def tcSubStep (s : SubstState) (values : List Nat) : Nat :=
  if tag s.2 = 0 then imageCode s.1 (varIndex s.2)
  else if tag s.2 = 2 then unary 2 (values[0]?.getD 0)
  else if tag s.2 = 1 then binary 1 (values[0]?.getD 0) (values[1]?.getD 0)
  else s.2

def substituteTypeCode (env : List Nat × Nat) (c : Nat) : Nat := foldSubst tcSubChildren tcSubStep (env,c)

theorem primrec_tcSubChildren : Primrec tcSubChildren := by
  have ht := primrec_tag.comp (Primrec.snd : Primrec (fun s : SubstState => s.2))
  have ha : Primrec (fun s : SubstState => (s.1,arg1 s.2)) := Primrec.fst.pair (primrec_arg1.comp Primrec.snd)
  have hb : Primrec (fun s : SubstState => (s.1,arg2 s.2)) := Primrec.fst.pair (primrec_arg2.comp Primrec.snd)
  have hall : Primrec (fun s : SubstState => (liftTCEnv s.1,arg1 s.2)) :=
    (primrec_liftTCEnv.comp Primrec.fst).pair (primrec_arg1.comp Primrec.snd)
  exact Primrec.ite (Primrec.eq.comp ht (.const 2)) (Primrec.list_cons.comp hall (.const []))
    (Primrec.ite (Primrec.eq.comp ht (.const 1))
      (Primrec.list_cons.comp ha (Primrec.list_cons.comp hb (.const []))) (.const []))

theorem primrec_tcSubStep : Primrec₂ tcSubStep := by
  have hc : Primrec (fun p : SubstState × List Nat => p.1.2) := Primrec.snd.comp Primrec.fst
  have he : Primrec (fun p : SubstState × List Nat => p.1.1) := Primrec.fst.comp Primrec.fst
  have ht := primrec_tag.comp hc
  have h0 : Primrec (fun p : SubstState × List Nat => p.2[0]?.getD 0) :=
    Primrec.option_getD.comp (Primrec.list_getElem?.comp Primrec.snd (.const 0)) (.const 0)
  have h1 : Primrec (fun p : SubstState × List Nat => p.2[1]?.getD 0) :=
    Primrec.option_getD.comp (Primrec.list_getElem?.comp Primrec.snd (.const 1)) (.const 0)
  exact Primrec.ite (Primrec.eq.comp ht (.const 0)) (primrec_imageCode.comp he (primrec_varIndex.comp hc))
    (Primrec.ite (Primrec.eq.comp ht (.const 2)) ((primrec_unary_fixed 2).comp h0)
      (Primrec.ite (Primrec.eq.comp ht (.const 1)) ((primrec_binary_fixed 1).comp h0 h1) hc))

theorem primrec_substituteTypeCode : Primrec₂ substituteTypeCode := primrec_foldSubst primrec_tcSubChildren primrec_tcSubStep

theorem substituteTypeCode_eq (env : List Nat × Nat) (c : Nat) :
    substituteTypeCode env c = tcSubStep (env,c)
      ((boundedInputs tcSubChildren (env,c)).map (foldSubst tcSubChildren tcSubStep)) := foldSubst_eq _ _ _
theorem fold_eq_substituteTypeCode (env : List Nat × Nat) (c : Nat) :
    foldSubst tcSubChildren tcSubStep (env,c) = substituteTypeCode env c := rfl

theorem substituteTypeCode_exact (images : List TypeCode) (shift : Nat) (A : TypeCode) :
    substituteTypeCode (images.map encode,shift) (encode A) = encode (substitute (finiteTCEnv images shift) A) := by
  induction A generalizing images shift with
  | var n => rw [substituteTypeCode_eq]; simp [tcSubStep,substitute,varIndex,leaf,tcImage_exact]
  | bottom => rw [substituteTypeCode_eq]; simp [tcSubStep,substitute]
  | all B ih =>
    rw [substituteTypeCode_eq]
    have h := unary_child_lt 2 (encode B)
    have hi := ih (.var 0 :: images.map (rename Nat.succ)) (shift+1)
    simp only [finiteTCEnv_lift,List.map_cons,List.map_map,encode_type_var] at hi
    simp [tcSubStep,tcSubChildren,boundedInputs,h,fold_eq_substituteTypeCode,liftTCEnv_exact,hi,substitute]
  | arrow A B iha ihb =>
    rw [substituteTypeCode_eq]
    have ha := binary_left_lt 1 (encode A) (encode B)
    have hb := binary_right_lt 1 (encode A) (encode B)
    simp [tcSubStep,tcSubChildren,boundedInputs,ha,hb,fold_eq_substituteTypeCode,iha,ihb,substitute]

def instantiateTypeCode (replacement body : Nat) : Nat := substituteTypeCode ([replacement],0) body

theorem primrec_instantiateTypeCode : Primrec₂ instantiateTypeCode :=
  primrec_substituteTypeCode.comp
    ((Primrec.list_cons.comp Primrec.fst (.const [])).pair (.const 0)) Primrec.snd

theorem finiteTCEnv_single (A : TypeCode) : finiteTCEnv [A] 0 = singleSub A := by
  funext n
  cases n <;> simp [finiteTCEnv,singleSub]

theorem instantiateTypeCode_exact (A B : TypeCode) :
    instantiateTypeCode (encode A) (encode B) = encode (instantiateType B A) := by
  simpa only [instantiateTypeCode,List.map_cons,List.map_nil,finiteTCEnv_single,instantiateType]
    using substituteTypeCode_exact [A] 0 B

#print axioms primrec_instantiateTypeCode
#print axioms instantiateTypeCode_exact
end CodedMixedTransformations
