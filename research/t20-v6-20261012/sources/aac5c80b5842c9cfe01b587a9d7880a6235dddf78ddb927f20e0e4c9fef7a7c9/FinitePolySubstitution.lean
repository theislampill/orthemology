import PolyAnalysis
namespace CodedPolyTransformations
open P01D Encodable SourceFamilyComputability CodedScope
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- Finite images followed by an explicitly shifted variable tail. -/
def finiteEnv (images : List Poly) (tailShift n : Nat) : Poly :=
  images[n]?.getD (.var (n - images.length + tailShift))

def imageCode (env : List Nat × Nat) (n : Nat) : Nat :=
  env.1[n]?.getD (varCode (n - env.1.length + env.2))

theorem primrec_imageCode : Primrec₂ imageCode := by
  have hlist : Primrec (fun p : (List Nat × Nat) × Nat => p.1.1) := Primrec.fst.comp Primrec.fst
  have hshift : Primrec (fun p : (List Nat × Nat) × Nat => p.1.2) := Primrec.snd.comp Primrec.fst
  exact Primrec.option_getD.comp (Primrec.list_getElem?.comp hlist Primrec.snd)
    (primrec_varCode.comp (Primrec.nat_add.comp
      (Primrec.nat_sub.comp Primrec.snd (Primrec.list_length.comp hlist)) hshift))

theorem imageCode_exact (images : List Poly) (shift n : Nat) :
    imageCode (images.map encode, shift) n = encode (finiteEnv images shift n) := by
  simp only [imageCode, finiteEnv, List.length_map, List.getElem?_map]
  cases h : images[n]? <;> simp [h,varCode_exact]

/-- Total extension of actual finite-environment polynomial substitution. -/
def substituteCode (env : List Nat × Nat) (c : Nat) : Nat :=
  if tag c = 0 then imageCode env (varIndex c)
  else if tag c = 1 then c
  else if tag c = 2 then
    if _ha : arg1 c < c then
      if _hb : arg2 c < c then appCode (substituteCode env (arg1 c)) (substituteCode env (arg2 c))
      else 0
    else 0
  else 0
termination_by c

def substitutionStep (env : List Nat × Nat) (values : List Nat) : Nat :=
  let c := values.length
  if tag c = 0 then imageCode env (varIndex c)
  else if tag c = 1 then c
  else if tag c = 2 then
    if arg1 c < c then
      if arg2 c < c then appCode (values[arg1 c]?.getD 0) (values[arg2 c]?.getD 0)
      else 0
    else 0
  else 0

theorem primrec_substitutionStep : Primrec₂ substitutionStep := by
  have hl : Primrec (fun p : (List Nat × Nat) × List Nat => p.2.length) := Primrec.list_length.comp Primrec.snd
  have ht := primrec_tag.comp hl
  have ha := primrec_arg1.comp hl
  have hb := primrec_arg2.comp hl
  have hga := Primrec.option_getD.comp (Primrec.list_getElem?.comp Primrec.snd ha) (.const 0)
  have hgb := Primrec.option_getD.comp (Primrec.list_getElem?.comp Primrec.snd hb) (.const 0)
  exact Primrec.ite (Primrec.eq.comp ht (.const 0))
    (primrec_imageCode.comp Primrec.fst (primrec_varIndex.comp hl))
    (Primrec.ite (Primrec.eq.comp ht (.const 1)) hl
      (Primrec.ite (Primrec.eq.comp ht (.const 2))
        (Primrec.ite (Primrec.nat_lt.comp ha hl)
          (Primrec.ite (Primrec.nat_lt.comp hb hl) (primrec_appCode.comp hga hgb) (.const 0))
          (.const 0)) (.const 0)))

theorem substitutionStep_exact (env : List Nat × Nat) (c : Nat) :
    substitutionStep env ((List.range c).map (substituteCode env)) = substituteCode env c := by
  rw [substituteCode]
  unfold substitutionStep
  simp only [List.length_map, List.length_range]
  by_cases h0 : tag c = 0
  · simp [h0]
  by_cases h1 : tag c = 1
  · simp [h0,h1]
  by_cases h2 : tag c = 2
  · by_cases ha : arg1 c < c
    · by_cases hb : arg2 c < c
      · simp [h0,h1,h2,ha,hb,List.getElem?_map,List.getElem?_range ha,List.getElem?_range hb]
      · simp [h0,h1,h2,ha,hb]
    · simp [h0,h1,h2,ha]
  · simp [h0,h1,h2]

theorem primrec_substituteCode : Primrec₂ substituteCode :=
  Primrec.nat_strong_rec substituteCode
    (Primrec.option_some.comp₂ primrec_substitutionStep)
    (fun e c => congrArg some (substitutionStep_exact e c))

theorem substituteCode_exact (images : List Poly) (shift : Nat) (p : Poly) :
    substituteCode (images.map encode,shift) (encode p) =
      encode (psub (finiteEnv images shift) p) := by
  induction p with
  | var n => rw [substituteCode]; simp [tag_var,varIndex_var,imageCode_exact,psub]
  | atom t => rw [substituteCode]; simp [tag_atom,psub]
  | app p q hp hq =>
    rw [substituteCode]
    have ha : encode p < encode (Poly.app p q) := by rw [encode_app]; exact left_lt_appCode _ _
    have hb : encode q < encode (Poly.app p q) := by rw [encode_app]; exact right_lt_appCode _ _
    simp only [tag_app,arg1_app,arg2_app,ha,hb,Nat.reduceEqDiff,↓reduceDIte,↓reduceIte]
    rw [hp,hq]
    simp only [psub,encode_app]

/-- All finite variable shifts, including the actual `pren Nat.succ` use. -/
def shiftCode (amount c : Nat) : Nat := substituteCode ([],amount) c

theorem primrec_shiftCode : Primrec₂ shiftCode :=
  primrec_substituteCode.comp (Primrec.pair (.const []) Primrec.fst) Primrec.snd

theorem shiftCode_exact (amount : Nat) (p : Poly) :
    shiftCode amount (encode p) = encode (pren (fun n => n+amount) p) := by
  simpa only [shiftCode, List.map_nil, finiteEnv, List.getElem?_nil, Option.getD_none,
    List.length_nil, Nat.sub_zero, pren] using substituteCode_exact [] amount p

theorem shiftCode_one_exact (p : Poly) :
    shiftCode 1 (encode p) = encode (pren Nat.succ p) := shiftCode_exact 1 p

/-- Single substitution, exactly the polynomial environment used by `Ty.inst`. -/
def instPolyCode (a c : Nat) : Nat := substituteCode ([a],0) c

theorem primrec_instPolyCode : Primrec₂ instPolyCode :=
  primrec_substituteCode.comp
    ((Primrec.list_cons.comp Primrec.fst (.const [])).pair (.const 0)) Primrec.snd

theorem finiteEnv_single (a : Poly) : finiteEnv [a] 0 = P01F.cons a Poly.var := by
  funext n
  cases n <;> simp [finiteEnv, P01F.cons]

theorem instPolyCode_exact (a p : Poly) :
    instPolyCode (encode a) (encode p) = encode (psub (P01F.cons a Poly.var) p) := by
  simpa only [instPolyCode,List.map_cons,List.map_nil,finiteEnv_single] using
    substituteCode_exact [a] 0 p

/-- Finite environments are closed under the actual capture-avoiding binder lift. -/
theorem finiteEnv_pup (images : List Poly) (shift : Nat) :
    finiteEnv (.var 0 :: images.map (pren Nat.succ)) (shift+1) = pup (finiteEnv images shift) := by
  funext n
  cases n with
  | zero => simp [finiteEnv,pup]
  | succ n =>
    simp only [finiteEnv,pup,List.getElem?_cons_succ,List.getElem?_map,List.length_cons,List.length_map]
    cases h : images[n]? <;> simp [h,pren,psub,Nat.add_assoc]

/-- Primitive-recursive finite coded environment update for one term binder. -/
def liftEnvCode (env : List Nat × Nat) : List Nat × Nat :=
  (varCode 0 :: env.1.map (shiftCode 1), env.2+1)

theorem primrec_liftEnvCode : Primrec liftEnvCode :=
  (Primrec.list_cons.comp (.const _)
    (Primrec.list_map Primrec.fst ((primrec_shiftCode.comp (.const 1) Primrec.snd).to₂))).pair
    (Primrec.succ.comp Primrec.snd)

theorem liftEnvCode_exact (images : List Poly) (shift : Nat) :
    liftEnvCode (images.map encode,shift) =
      ((.var 0 :: images.map (pren Nat.succ)).map encode, shift+1) := by
  simp only [liftEnvCode,varCode_exact,List.map_cons,List.map_map]
  congr 2
  apply List.map_congr_left
  intro p _
  exact shiftCode_one_exact p

/-- The real capture-avoiding substitution after entering a term binder. -/
theorem lifted_substituteCode_exact (images : List Poly) (shift : Nat) (p : Poly) :
    substituteCode (liftEnvCode (images.map encode,shift)) (encode p) =
      encode (psub (pup (finiteEnv images shift)) p) := by
  rw [liftEnvCode_exact,substituteCode_exact,finiteEnv_pup]

#print axioms primrec_substituteCode
#print axioms substituteCode_exact
#print axioms finiteEnv_pup
#print axioms liftEnvCode_exact
end CodedPolyTransformations
