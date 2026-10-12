import TypeRenaming
namespace CodedMixedTransformations
open OrthemologyV2 OrthemologyV3 Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity CodedPolyTransformations
set_option maxRecDepth 8192
set_option maxHeartbeats 12000000

def tcRenChildren (s : SubstState) : List SubstState :=
  if tag s.2 = 2 then [(liftRenCode s.1,arg1 s.2)]
  else if tag s.2 = 1 then [(s.1,arg1 s.2),(s.1,arg2 s.2)] else []
def tcRenStep (s : SubstState) (values : List Nat) : Nat :=
  if tag s.2 = 0 then paramCode (renImage s.1 (varIndex s.2))
  else if tag s.2 = 2 then unary 2 (values[0]?.getD 0)
  else if tag s.2 = 1 then binary 1 (values[0]?.getD 0) (values[1]?.getD 0)
  else s.2

def renameTypeCode (env : List Nat × Nat) (c : Nat) : Nat := foldSubst tcRenChildren tcRenStep (env,c)

theorem primrec_tcRenChildren : Primrec tcRenChildren := by
  have ht := primrec_tag.comp (Primrec.snd : Primrec (fun s : SubstState => s.2))
  have ha : Primrec (fun s : SubstState => (s.1,arg1 s.2)) := Primrec.fst.pair (primrec_arg1.comp Primrec.snd)
  have hb : Primrec (fun s : SubstState => (s.1,arg2 s.2)) := Primrec.fst.pair (primrec_arg2.comp Primrec.snd)
  have hall : Primrec (fun s : SubstState => (liftRenCode s.1,arg1 s.2)) :=
    (primrec_liftRenCode.comp Primrec.fst).pair (primrec_arg1.comp Primrec.snd)
  exact Primrec.ite (Primrec.eq.comp ht (.const 2)) (Primrec.list_cons.comp hall (.const []))
    (Primrec.ite (Primrec.eq.comp ht (.const 1))
      (Primrec.list_cons.comp ha (Primrec.list_cons.comp hb (.const []))) (.const []))

theorem primrec_tcRenStep : Primrec₂ tcRenStep := by
  have hc : Primrec (fun p : SubstState × List Nat => p.1.2) := Primrec.snd.comp Primrec.fst
  have he : Primrec (fun p : SubstState × List Nat => p.1.1) := Primrec.fst.comp Primrec.fst
  have ht := primrec_tag.comp hc
  have h0 : Primrec (fun p : SubstState × List Nat => p.2[0]?.getD 0) :=
    Primrec.option_getD.comp (Primrec.list_getElem?.comp Primrec.snd (.const 0)) (.const 0)
  have h1 : Primrec (fun p : SubstState × List Nat => p.2[1]?.getD 0) :=
    Primrec.option_getD.comp (Primrec.list_getElem?.comp Primrec.snd (.const 1)) (.const 0)
  exact Primrec.ite (Primrec.eq.comp ht (.const 0))
    (primrec_paramCode.comp (primrec_renImage.comp he (primrec_varIndex.comp hc)))
    (Primrec.ite (Primrec.eq.comp ht (.const 2)) ((primrec_unary_fixed 2).comp h0)
      (Primrec.ite (Primrec.eq.comp ht (.const 1)) ((primrec_binary_fixed 1).comp h0 h1) hc))

theorem primrec_renameTypeCode : Primrec₂ renameTypeCode := primrec_foldSubst primrec_tcRenChildren primrec_tcRenStep

theorem renameTypeCode_eq (env : List Nat × Nat) (c : Nat) :
    renameTypeCode env c = tcRenStep (env,c)
      ((boundedInputs tcRenChildren (env,c)).map (foldSubst tcRenChildren tcRenStep)) := foldSubst_eq _ _ _
theorem fold_eq_renameTypeCode (env : List Nat × Nat) (c : Nat) :
    foldSubst tcRenChildren tcRenStep (env,c) = renameTypeCode env c := rfl

theorem renameTypeCode_exact (images : List Nat) (shift : Nat) (A : TypeCode) :
    renameTypeCode (images,shift) (encode A) = encode (rename (finiteRen images shift) A) := by
  induction A generalizing images shift with
  | var n => rw [renameTypeCode_eq]; simp [tcRenStep,rename,paramCode,varIndex,renImage,leaf]
  | bottom => rw [renameTypeCode_eq]; simp [tcRenStep,rename]
  | all B ih =>
    rw [renameTypeCode_eq]
    have h := unary_child_lt 2 (encode B)
    have hi := ih (0 :: images.map Nat.succ) (shift+1)
    rw [finiteRen_lift] at hi
    simp [tcRenStep,tcRenChildren,boundedInputs,h,fold_eq_renameTypeCode,liftRenCode,hi,rename]
  | arrow A B iha ihb =>
    rw [renameTypeCode_eq]
    have ha := binary_left_lt 1 (encode A) (encode B)
    have hb := binary_right_lt 1 (encode A) (encode B)
    simp [tcRenStep,tcRenChildren,boundedInputs,ha,hb,fold_eq_renameTypeCode,iha,ihb,rename]

def shiftTypeCode (c : Nat) : Nat := renameTypeCode ([],1) c
theorem primrec_shiftTypeCode : Primrec shiftTypeCode := primrec_renameTypeCode.comp (.const ([],1)) Primrec.id

theorem shiftTypeCode_exact (A : TypeCode) : shiftTypeCode (encode A) = encode (rename Nat.succ A) := by
  simpa only [shiftTypeCode,finiteRen,List.getElem?_nil,Option.getD_none,List.length_nil,Nat.sub_zero]
    using renameTypeCode_exact [] 1 A

end CodedMixedTransformations
