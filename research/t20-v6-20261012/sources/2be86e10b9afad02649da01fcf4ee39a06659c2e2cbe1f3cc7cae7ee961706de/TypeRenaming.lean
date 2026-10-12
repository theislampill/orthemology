import TermTypeSubstitution
namespace CodedMixedTransformations
open P01D P01AC OrthemologyV3 Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity CodedPolyTransformations
set_option maxRecDepth 8192
set_option maxHeartbeats 12000000

def finiteRen (images : List Nat) (shift n : Nat) : Nat := images[n]?.getD (n-images.length+shift)
def renImage (env : List Nat × Nat) (n : Nat) : Nat := finiteRen env.1 env.2 n

def liftRenCode (env : List Nat × Nat) : List Nat × Nat := (0 :: env.1.map Nat.succ, env.2+1)

theorem primrec_renImage : Primrec₂ renImage := by
  have hl : Primrec (fun p : (List Nat × Nat) × Nat => p.1.1) := Primrec.fst.comp Primrec.fst
  exact Primrec.option_getD.comp (Primrec.list_getElem?.comp hl Primrec.snd)
    (Primrec.nat_add.comp (Primrec.nat_sub.comp Primrec.snd (Primrec.list_length.comp hl))
      (Primrec.snd.comp Primrec.fst))

theorem primrec_liftRenCode : Primrec liftRenCode :=
  (Primrec.list_cons.comp (.const 0)
    (Primrec.list_map Primrec.fst (Primrec.succ.comp Primrec.snd).to₂)).pair (Primrec.succ.comp Primrec.snd)

theorem finiteRen_lift (images : List Nat) (shift : Nat) :
    finiteRen (0 :: images.map Nat.succ) (shift+1) = liftRen (finiteRen images shift) := by
  funext n
  cases n with
  | zero => simp [finiteRen,liftRen]
  | succ n =>
    simp only [finiteRen,liftRen,List.getElem?_cons_succ,List.getElem?_map,List.length_cons,List.length_map]
    cases h : images[n]? <;> simp [h,Nat.add_assoc]

def paramCode (n : Nat) : Nat := unary 0 (leaf n)
theorem primrec_paramCode : Primrec paramCode := (primrec_unary_fixed 0).comp primrec_leaf

def renameTyChildren (s : SubstState) : List SubstState :=
  if tag s.2 = 2 then [(liftRenCode s.1,arg1 s.2)]
  else if tag s.2 = 4 ∨ tag s.2 = 5 then [(s.1,arg1 s.2),(s.1,arg2 s.2)]
  else if tag s.2 = 6 then [(s.1,arg1 s.2)] else []

def renameTyStep (s : SubstState) (values : List Nat) : Nat :=
  if tag s.2 = 0 then paramCode (renImage s.1 (varIndex s.2))
  else if tag s.2 = 2 then unary 2 (values[0]?.getD 0)
  else if tag s.2 = 4 then binary 4 (values[0]?.getD 0) (values[1]?.getD 0)
  else if tag s.2 = 5 then binary 5 (values[0]?.getD 0) (values[1]?.getD 0)
  else if tag s.2 = 6 then ternary 6 (values[0]?.getD 0) (arg2 s.2) (arg3 s.2)
  else s.2

def renameTyCode (env : List Nat × Nat) (c : Nat) : Nat := foldSubst renameTyChildren renameTyStep (env,c)

theorem primrec_renameTyChildren : Primrec renameTyChildren := by
  have ht := primrec_tag.comp (Primrec.snd : Primrec (fun s : SubstState => s.2))
  have ha : Primrec (fun s : SubstState => (s.1,arg1 s.2)) := Primrec.fst.pair (primrec_arg1.comp Primrec.snd)
  have hb : Primrec (fun s : SubstState => (s.1,arg2 s.2)) := Primrec.fst.pair (primrec_arg2.comp Primrec.snd)
  have hall : Primrec (fun s : SubstState => (liftRenCode s.1,arg1 s.2)) :=
    (primrec_liftRenCode.comp Primrec.fst).pair (primrec_arg1.comp Primrec.snd)
  exact Primrec.ite (Primrec.eq.comp ht (.const 2)) (Primrec.list_cons.comp hall (.const []))
    (Primrec.ite ((Primrec.eq.comp ht (.const 4)).or (Primrec.eq.comp ht (.const 5)))
      (Primrec.list_cons.comp ha (Primrec.list_cons.comp hb (.const [])))
      (Primrec.ite (Primrec.eq.comp ht (.const 6)) (Primrec.list_cons.comp ha (.const [])) (.const [])))

theorem primrec_renameTyStep : Primrec₂ renameTyStep := by
  have hc : Primrec (fun p : SubstState × List Nat => p.1.2) := Primrec.snd.comp Primrec.fst
  have he : Primrec (fun p : SubstState × List Nat => p.1.1) := Primrec.fst.comp Primrec.fst
  have ht := primrec_tag.comp hc
  have h0 : Primrec (fun p : SubstState × List Nat => p.2[0]?.getD 0) :=
    Primrec.option_getD.comp (Primrec.list_getElem?.comp Primrec.snd (.const 0)) (.const 0)
  have h1 : Primrec (fun p : SubstState × List Nat => p.2[1]?.getD 0) :=
    Primrec.option_getD.comp (Primrec.list_getElem?.comp Primrec.snd (.const 1)) (.const 0)
  have hi : Primrec (fun p : SubstState × List Nat => ternary 6
      (p.2[0]?.getD 0) (arg2 p.1.2) (arg3 p.1.2)) :=
    primrec_node.comp (.const _) (primrec_node.comp h0
      (primrec_node.comp (primrec_arg2.comp hc) (primrec_node.comp (primrec_arg3.comp hc) (.const _))))
  exact Primrec.ite (Primrec.eq.comp ht (.const 0))
    (primrec_paramCode.comp (primrec_renImage.comp he (primrec_varIndex.comp hc)))
    (Primrec.ite (Primrec.eq.comp ht (.const 2)) ((primrec_unary_fixed 2).comp h0)
      (Primrec.ite (Primrec.eq.comp ht (.const 4)) ((primrec_binary_fixed 4).comp h0 h1)
        (Primrec.ite (Primrec.eq.comp ht (.const 5)) ((primrec_binary_fixed 5).comp h0 h1)
          (Primrec.ite (Primrec.eq.comp ht (.const 6)) hi hc))))

theorem primrec_renameTyCode : Primrec₂ renameTyCode :=
  primrec_foldSubst primrec_renameTyChildren primrec_renameTyStep

theorem renameTyCode_eq (env : List Nat × Nat) (c : Nat) :
    renameTyCode env c = renameTyStep (env,c)
      ((boundedInputs renameTyChildren (env,c)).map (foldSubst renameTyChildren renameTyStep)) :=
  foldSubst_eq _ _ _
theorem fold_eq_renameTyCode (env : List Nat × Nat) (c : Nat) :
    foldSubst renameTyChildren renameTyStep (env,c) = renameTyCode env c := rfl

theorem renameTyCode_exact (images : List Nat) (shift : Nat) (A : Ty) :
    renameTyCode (images,shift) (encode A) = encode (trename (finiteRen images shift) A) := by
  induction A generalizing images shift with
  | param n => rw [renameTyCode_eq]; simp [renameTyStep,trename,paramCode,varIndex,renImage,leaf]
  | bottom => rw [renameTyCode_eq]; simp [renameTyStep,trename]
  | raw => rw [renameTyCode_eq]; simp [renameTyStep,trename]
  | all B ih =>
    rw [renameTyCode_eq]
    have h := unary_child_lt 2 (encode B)
    have hi := ih (0 :: images.map Nat.succ) (shift+1)
    rw [finiteRen_lift] at hi
    simp [renameTyStep,renameTyChildren,boundedInputs,h,fold_eq_renameTyCode,liftRenCode,hi,trename]
  | pi A B iha ihb =>
    rw [renameTyCode_eq]
    have ha := binary_left_lt 4 (encode A) (encode B)
    have hb := binary_right_lt 4 (encode A) (encode B)
    simp [renameTyStep,renameTyChildren,boundedInputs,ha,hb,fold_eq_renameTyCode,iha,ihb,trename]
  | sigma A B iha ihb =>
    rw [renameTyCode_eq]
    have ha := binary_left_lt 5 (encode A) (encode B)
    have hb := binary_right_lt 5 (encode A) (encode B)
    simp [renameTyStep,renameTyChildren,boundedInputs,ha,hb,fold_eq_renameTyCode,iha,ihb,trename]
  | identity A p q ih =>
    rw [renameTyCode_eq]
    have ha := ternary_left_lt 6 (encode A) (leaf (encode p)) (leaf (encode q))
    simp [renameTyStep,renameTyChildren,boundedInputs,ha,fold_eq_renameTyCode,ih,trename]

def twkCode (c : Nat) : Nat := renameTyCode ([],1) c
theorem primrec_twkCode : Primrec twkCode := primrec_renameTyCode.comp (.const ([],1)) Primrec.id

theorem twkCode_exact (A : Ty) : twkCode (encode A) = encode (twk A) := by
  simpa only [twkCode, finiteRen,List.getElem?_nil,Option.getD_none,List.length_nil,Nat.sub_zero,
    twk] using renameTyCode_exact [] 1 A

#print axioms primrec_twkCode
#print axioms twkCode_exact
end CodedMixedTransformations
