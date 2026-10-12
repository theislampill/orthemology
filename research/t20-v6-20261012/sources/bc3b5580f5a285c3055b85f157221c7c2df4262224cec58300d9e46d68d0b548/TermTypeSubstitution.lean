import FinitePolySubstitution
import TypeScope
namespace CodedPolyTransformations
open P01D P01AC Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity
set_option maxRecDepth 8192
set_option maxHeartbeats 12000000

abbrev SubstState := (List Nat × Nat) × Nat

def boundedInputs (children : SubstState → List SubstState) (s : SubstState) : List SubstState :=
  (children s).filter (fun t => decide (t.2 < s.2))

def foldSubst (children : SubstState → List SubstState)
    (step : SubstState → List Nat → Nat) (s : SubstState) : Nat :=
  step s ((boundedInputs children s).attach.map (fun t => foldSubst children step t.val))
termination_by s.2
decreasing_by exact of_decide_eq_true (List.mem_filter.mp t.property).2

theorem foldSubst_eq (children : SubstState → List SubstState)
    (step : SubstState → List Nat → Nat) (s : SubstState) :
    foldSubst children step s = step s ((boundedInputs children s).map (foldSubst children step)) := by
  rw [foldSubst]
  simp only [List.attach_map_val]

theorem primrec_foldSubst {children : SubstState → List SubstState}
    {step : SubstState → List Nat → Nat} (hc : Primrec children) (hs : Primrec₂ step) :
    Primrec (foldSubst children step) := by
  have hb : Primrec (boundedInputs children) := primrec_list_filter hc
    (Primrec.nat_lt.comp₂ (Primrec.snd.comp₂ Primrec₂.right) (Primrec.snd.comp₂ Primrec₂.left))
  apply Primrec.nat_omega_rec' (foldSubst children step) (m := Prod.snd) (l := boundedInputs children)
    (g := fun s vals => some (step s vals)) Primrec.snd hb (Primrec.option_some.comp₂ hs)
  · intro s t ht
    exact of_decide_eq_true (List.mem_filter.mp ht).2
  · intro s
    exact congrArg some (foldSubst_eq children step s).symm

def termTyChildren (s : SubstState) : List SubstState :=
  if tag s.2 = 2 then [(s.1,arg1 s.2)]
  else if tag s.2 = 4 ∨ tag s.2 = 5 then [(s.1,arg1 s.2),(liftEnvCode s.1,arg2 s.2)]
  else if tag s.2 = 6 then [(s.1,arg1 s.2)] else []

def termTyStep (s : SubstState) (values : List Nat) : Nat :=
  if tag s.2 = 2 then unary 2 (values[0]?.getD 0)
  else if tag s.2 = 4 then binary 4 (values[0]?.getD 0) (values[1]?.getD 0)
  else if tag s.2 = 5 then binary 5 (values[0]?.getD 0) (values[1]?.getD 0)
  else if tag s.2 = 6 then ternary 6 (values[0]?.getD 0)
    (leaf (substituteCode s.1 (rest (arg2 s.2)))) (leaf (substituteCode s.1 (rest (arg3 s.2))))
  else s.2

def substTyCode (env : List Nat × Nat) (c : Nat) : Nat := foldSubst termTyChildren termTyStep (env,c)

theorem primrec_termTyChildren : Primrec termTyChildren := by
  have ht := primrec_tag.comp (Primrec.snd : Primrec (fun s : SubstState => s.2))
  have ha : Primrec (fun s : SubstState => (s.1,arg1 s.2)) := Primrec.fst.pair (primrec_arg1.comp Primrec.snd)
  have hb : Primrec (fun s : SubstState => (liftEnvCode s.1,arg2 s.2)) :=
    (primrec_liftEnvCode.comp Primrec.fst).pair (primrec_arg2.comp Primrec.snd)
  have hsingle := Primrec.list_cons.comp ha (Primrec.const [])
  have hdouble := Primrec.list_cons.comp ha (Primrec.list_cons.comp hb (Primrec.const []))
  exact Primrec.ite (Primrec.eq.comp ht (.const 2)) hsingle
    (Primrec.ite ((Primrec.eq.comp ht (.const 4)).or (Primrec.eq.comp ht (.const 5))) hdouble
      (Primrec.ite (Primrec.eq.comp ht (.const 6)) hsingle (.const [])))

theorem primrec_unary_fixed (tag : Nat) : Primrec (unary tag) :=
  primrec_node.comp (.const _) (primrec_node.comp Primrec.id (.const _))
theorem primrec_binary_fixed (tag : Nat) : Primrec₂ (binary tag) :=
  primrec_node.comp₂ (.const _) (primrec_node.comp₂ .left (primrec_node.comp₂ .right (.const _)))

theorem primrec_termTyStep : Primrec₂ termTyStep := by
  have hs : Primrec (fun p : SubstState × List Nat => p.1) := Primrec.fst
  have hc := Primrec.snd.comp hs
  have he := Primrec.fst.comp hs
  have ht := primrec_tag.comp hc
  have h0 : Primrec (fun p : SubstState × List Nat => p.2[0]?.getD 0) := Primrec.option_getD.comp (Primrec.list_getElem?.comp Primrec.snd (.const 0)) (.const 0)
  have h1 : Primrec (fun p : SubstState × List Nat => p.2[1]?.getD 0) := Primrec.option_getD.comp (Primrec.list_getElem?.comp Primrec.snd (.const 1)) (.const 0)
  have hp := primrec_leaf.comp (primrec_substituteCode.comp he (primrec_rest.comp (primrec_arg2.comp hc)))
  have hq := primrec_leaf.comp (primrec_substituteCode.comp he (primrec_rest.comp (primrec_arg3.comp hc)))
  have hi : Primrec (fun p : SubstState × List Nat => ternary 6
      (p.2[0]?.getD 0) (leaf (substituteCode p.1.1 (rest (arg2 p.1.2))))
      (leaf (substituteCode p.1.1 (rest (arg3 p.1.2))))) :=
    primrec_node.comp (.const _) (primrec_node.comp h0 (primrec_node.comp hp (primrec_node.comp hq (.const _))))
  exact Primrec.ite (Primrec.eq.comp ht (.const 2)) ((primrec_unary_fixed 2).comp h0)
    (Primrec.ite (Primrec.eq.comp ht (.const 4)) ((primrec_binary_fixed 4).comp h0 h1)
      (Primrec.ite (Primrec.eq.comp ht (.const 5)) ((primrec_binary_fixed 5).comp h0 h1)
        (Primrec.ite (Primrec.eq.comp ht (.const 6)) hi hc)))

theorem primrec_substTyCode : Primrec₂ substTyCode :=
  primrec_foldSubst primrec_termTyChildren primrec_termTyStep

theorem substTyCode_eq (env : List Nat × Nat) (c : Nat) :
    substTyCode env c = termTyStep (env,c)
      ((boundedInputs termTyChildren (env,c)).map (foldSubst termTyChildren termTyStep)) :=
  foldSubst_eq _ _ _

theorem fold_eq_substTyCode (env : List Nat × Nat) (c : Nat) :
    foldSubst termTyChildren termTyStep (env,c) = substTyCode env c := rfl

/-- Exact capture-avoiding type substitution for every finite polynomial environment. -/
theorem substTyCode_exact (images : List Poly) (shift : Nat) (A : Ty) :
    substTyCode (images.map encode,shift) (encode A) = encode (subst (finiteEnv images shift) A) := by
  induction A generalizing images shift with
  | param n => rw [substTyCode_eq]; simp [termTyStep,subst]
  | bottom => rw [substTyCode_eq]; simp [termTyStep,subst]
  | raw => rw [substTyCode_eq]; simp [termTyStep,subst]
  | all B ih =>
    rw [substTyCode_eq]
    have h := unary_child_lt 2 (encode B)
    simp [termTyStep,termTyChildren,boundedInputs,h,fold_eq_substTyCode,ih,subst]
  | pi A B iha ihb =>
    rw [substTyCode_eq]
    have ha := binary_left_lt 4 (encode A) (encode B)
    have hb := binary_right_lt 4 (encode A) (encode B)
    have hB := ihb (.var 0 :: images.map (pren Nat.succ)) (shift+1)
    simp only [finiteEnv_pup,List.map_cons,List.map_map,encode_poly_var] at hB
    simp [termTyStep,termTyChildren,boundedInputs,ha,hb,fold_eq_substTyCode,
      liftEnvCode_exact,iha,hB,finiteEnv_pup,subst]
  | sigma A B iha ihb =>
    rw [substTyCode_eq]
    have ha := binary_left_lt 5 (encode A) (encode B)
    have hb := binary_right_lt 5 (encode A) (encode B)
    have hB := ihb (.var 0 :: images.map (pren Nat.succ)) (shift+1)
    simp only [finiteEnv_pup,List.map_cons,List.map_map,encode_poly_var] at hB
    simp [termTyStep,termTyChildren,boundedInputs,ha,hb,fold_eq_substTyCode,
      liftEnvCode_exact,iha,hB,finiteEnv_pup,subst]
  | identity A p q ih =>
    rw [substTyCode_eq]
    have ha := ternary_left_lt 6 (encode A) (leaf (encode p)) (leaf (encode q))
    simp [termTyStep,termTyChildren,boundedInputs,ha,fold_eq_substTyCode,ih,
      substituteCode_exact,subst]

def wkTyCode (c : Nat) : Nat := substTyCode ([],1) c
def instTyCode (replacement body : Nat) : Nat := substTyCode ([replacement],0) body

theorem primrec_wkTyCode : Primrec wkTyCode := primrec_substTyCode.comp (.const ([],1)) Primrec.id
theorem primrec_instTyCode : Primrec₂ instTyCode := primrec_substTyCode.comp
  ((Primrec.list_cons.comp Primrec.fst (.const [])).pair (.const 0)) Primrec.snd

theorem wkTyCode_exact (A : Ty) : wkTyCode (encode A) = encode (wk A) := by
  simpa only [wkTyCode, List.map_nil, finiteEnv, List.getElem?_nil, Option.getD_none,
    List.length_nil, Nat.sub_zero, wk] using substTyCode_exact [] 1 A

theorem instTyCode_exact (a : Poly) (A : Ty) :
    instTyCode (encode a) (encode A) = encode (inst A a) := by
  simpa only [instTyCode,List.map_cons,List.map_nil,finiteEnv_single,inst] using
    substTyCode_exact [a] 0 A

#print axioms primrec_substTyCode
#print axioms substTyCode_exact
end CodedPolyTransformations
