import FiniteTypeEnvironments
namespace CodedMixedTransformations
open P01D P01AC OrthemologyV3 Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity CodedPolyTransformations
set_option maxRecDepth 8192
set_option maxHeartbeats 12000000
abbrev MixedState := MixedEnvCode × Nat

def mixedInputs (children : MixedState → List MixedState) (s : MixedState) : List MixedState :=
  (children s).filter (fun t => decide (t.2 < s.2))
def mixedFold (children : MixedState → List MixedState)
    (step : MixedState → List Nat → Nat) (s : MixedState) : Nat :=
  step s ((mixedInputs children s).attach.map (fun t => mixedFold children step t.val))
termination_by s.2
decreasing_by exact of_decide_eq_true (List.mem_filter.mp t.property).2

theorem mixedFold_eq (children : MixedState → List MixedState)
    (step : MixedState → List Nat → Nat) (s : MixedState) :
    mixedFold children step s = step s ((mixedInputs children s).map (mixedFold children step)) := by
  rw [mixedFold]; simp only [List.attach_map_val]

theorem primrec_mixedFold {children : MixedState → List MixedState}
    {step : MixedState → List Nat → Nat} (hc : Primrec children) (hs : Primrec₂ step) :
    Primrec (mixedFold children step) := by
  have hb : Primrec (mixedInputs children) := primrec_list_filter hc
    (Primrec.nat_lt.comp₂ (Primrec.snd.comp₂ Primrec₂.right) (Primrec.snd.comp₂ Primrec₂.left))
  apply Primrec.nat_omega_rec' (mixedFold children step) (m := Prod.snd) (l := mixedInputs children)
    (g := fun s vals => some (step s vals)) Primrec.snd hb (Primrec.option_some.comp₂ hs)
  · intro s t ht
    exact of_decide_eq_true (List.mem_filter.mp ht).2
  · intro s
    exact congrArg some (mixedFold_eq children step s).symm

def mixedChildren (s : MixedState) : List MixedState :=
  if tag s.2 = 2 then [(typeLift s.1,arg1 s.2)]
  else if tag s.2 = 4 ∨ tag s.2 = 5 then [(s.1,arg1 s.2),(termLift s.1,arg2 s.2)]
  else if tag s.2 = 6 then [(s.1,arg1 s.2)] else []

def mixedStep (s : MixedState) (values : List Nat) : Nat :=
  if tag s.2 = 0 then typeImageCode s.1.2 (varIndex s.2)
  else if tag s.2 = 2 then unary 2 (values[0]?.getD 0)
  else if tag s.2 = 4 then binary 4 (values[0]?.getD 0) (values[1]?.getD 0)
  else if tag s.2 = 5 then binary 5 (values[0]?.getD 0) (values[1]?.getD 0)
  else if tag s.2 = 6 then ternary 6 (values[0]?.getD 0)
    (leaf (substituteCode s.1.1 (rest (arg2 s.2)))) (leaf (substituteCode s.1.1 (rest (arg3 s.2))))
  else s.2

def mixedCode (env : MixedEnvCode) (c : Nat) : Nat := mixedFold mixedChildren mixedStep (env,c)

theorem primrec_mixedChildren : Primrec mixedChildren := by
  have ht := primrec_tag.comp (Primrec.snd : Primrec (fun s : MixedState => s.2))
  have ha : Primrec (fun s : MixedState => (s.1,arg1 s.2)) := Primrec.fst.pair (primrec_arg1.comp Primrec.snd)
  have hb : Primrec (fun s : MixedState => (termLift s.1,arg2 s.2)) :=
    (primrec_termLift.comp Primrec.fst).pair (primrec_arg2.comp Primrec.snd)
  have hall : Primrec (fun s : MixedState => (typeLift s.1,arg1 s.2)) :=
    (primrec_typeLift.comp Primrec.fst).pair (primrec_arg1.comp Primrec.snd)
  exact Primrec.ite (Primrec.eq.comp ht (.const 2)) (Primrec.list_cons.comp hall (.const []))
    (Primrec.ite ((Primrec.eq.comp ht (.const 4)).or (Primrec.eq.comp ht (.const 5)))
      (Primrec.list_cons.comp ha (Primrec.list_cons.comp hb (.const [])))
      (Primrec.ite (Primrec.eq.comp ht (.const 6)) (Primrec.list_cons.comp ha (.const [])) (.const [])))

theorem primrec_mixedStep : Primrec₂ mixedStep := by
  have hc : Primrec (fun p : MixedState × List Nat => p.1.2) := Primrec.snd.comp Primrec.fst
  have he : Primrec (fun p : MixedState × List Nat => p.1.1) := Primrec.fst.comp Primrec.fst
  have hpEnv := Primrec.fst.comp he
  have htEnv := Primrec.snd.comp he
  have ht := primrec_tag.comp hc
  have h0 : Primrec (fun p : MixedState × List Nat => p.2[0]?.getD 0) :=
    Primrec.option_getD.comp (Primrec.list_getElem?.comp Primrec.snd (.const 0)) (.const 0)
  have h1 : Primrec (fun p : MixedState × List Nat => p.2[1]?.getD 0) :=
    Primrec.option_getD.comp (Primrec.list_getElem?.comp Primrec.snd (.const 1)) (.const 0)
  have hp := primrec_leaf.comp (primrec_substituteCode.comp hpEnv (primrec_rest.comp (primrec_arg2.comp hc)))
  have hq := primrec_leaf.comp (primrec_substituteCode.comp hpEnv (primrec_rest.comp (primrec_arg3.comp hc)))
  have hi : Primrec (fun p : MixedState × List Nat => ternary 6
      (p.2[0]?.getD 0) (leaf (substituteCode p.1.1.1 (rest (arg2 p.1.2))))
      (leaf (substituteCode p.1.1.1 (rest (arg3 p.1.2))))) :=
    primrec_node.comp (.const _) (primrec_node.comp h0 (primrec_node.comp hp (primrec_node.comp hq (.const _))))
  exact Primrec.ite (Primrec.eq.comp ht (.const 0))
    (primrec_typeImageCode.comp htEnv (primrec_varIndex.comp hc))
    (Primrec.ite (Primrec.eq.comp ht (.const 2)) ((primrec_unary_fixed 2).comp h0)
      (Primrec.ite (Primrec.eq.comp ht (.const 4)) ((primrec_binary_fixed 4).comp h0 h1)
        (Primrec.ite (Primrec.eq.comp ht (.const 5)) ((primrec_binary_fixed 5).comp h0 h1)
          (Primrec.ite (Primrec.eq.comp ht (.const 6)) hi hc))))

theorem primrec_mixedCode : Primrec₂ mixedCode := primrec_mixedFold primrec_mixedChildren primrec_mixedStep

theorem mixedCode_eq (env : MixedEnvCode) (c : Nat) :
    mixedCode env c = mixedStep (env,c)
      ((mixedInputs mixedChildren (env,c)).map (mixedFold mixedChildren mixedStep)) :=
  mixedFold_eq _ _ _
theorem fold_eq_mixedCode (env : MixedEnvCode) (c : Nat) :
    mixedFold mixedChildren mixedStep (env,c) = mixedCode env c := rfl

/-- The actual corrected mixed substitution, for all finite source environments. -/
theorem mixedCode_exact (p : SourcePolyEnv) (t : SourceTypeEnv) (A : Ty) :
    mixedCode (encodeEnv p t) (encode A) =
      encode (mixed (finiteEnv p.1 p.2) (finiteTyEnv t.1 t.2.1 t.2.2) A) := by
  induction A generalizing p t with
  | param n =>
    rcases t with ⟨images,mode,shift⟩
    rw [mixedCode_eq]
    simp [mixedStep,mixed,encodeEnv,varIndex,leaf,typeImageCode_exact]
  | bottom => rw [mixedCode_eq]; simp [mixedStep,mixed]
  | raw => rw [mixedCode_eq]; simp [mixedStep,mixed]
  | all B ih =>
    rw [mixedCode_eq]
    have h := unary_child_lt 2 (encode B)
    have hi := ih p (sourceTTypeLift t)
    simp only [sourceTTypeLift,finiteTyEnv_type] at hi
    simp [mixedStep,mixedChildren,mixedInputs,h,fold_eq_mixedCode,typeLift_exact,sourceTTypeLift,hi,mixed]
  | pi A B iha ihb =>
    rw [mixedCode_eq]
    have ha := binary_left_lt 4 (encode A) (encode B)
    have hb := binary_right_lt 4 (encode A) (encode B)
    have hi := ihb (sourcePLift p) (sourceTTermLift t)
    simp only [sourcePLift,sourceTTermLift,finiteEnv_pup,finiteTyEnv_term] at hi
    simp [mixedStep,mixedChildren,mixedInputs,ha,hb,fold_eq_mixedCode,termLift_exact,sourcePLift,sourceTTermLift,iha,hi,mixed]
  | sigma A B iha ihb =>
    rw [mixedCode_eq]
    have ha := binary_left_lt 5 (encode A) (encode B)
    have hb := binary_right_lt 5 (encode A) (encode B)
    have hi := ihb (sourcePLift p) (sourceTTermLift t)
    simp only [sourcePLift,sourceTTermLift,finiteEnv_pup,finiteTyEnv_term] at hi
    simp [mixedStep,mixedChildren,mixedInputs,ha,hb,fold_eq_mixedCode,termLift_exact,sourcePLift,sourceTTermLift,iha,hi,mixed]
  | identity A a b ih =>
    rw [mixedCode_eq]
    have ha := ternary_left_lt 6 (encode A) (leaf (encode a)) (leaf (encode b))
    have hi := ih p t
    simp only [encodeEnv] at hi
    simp [mixedStep,mixedChildren,mixedInputs,ha,fold_eq_mixedCode,hi,mixed,encodeEnv,
      substituteCode_exact]

#print axioms primrec_mixedCode
#print axioms mixedCode_exact
end CodedMixedTransformations
