import CodedScope
namespace CodedPolyTransformations
open P01D Encodable SourceFamilyComputability CodedScope
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

abbrev Result := Bool × Nat × Nat

def varCode (n : Nat) : Nat := node (leaf 0) (node (leaf n) (leaf 0))
theorem varCode_exact (n : Nat) : varCode n = encode (Poly.var n) := (encode_var n).symm
theorem primrec_varCode : Primrec varCode :=
  primrec_node.comp (.const _) (primrec_node.comp primrec_leaf (.const _))

def varResult (n : Nat) : Result :=
  (decide (n = 0), varCode (n-1),
    if n = 0 then encode (Poly.atom .i) else appCode (encode (Poly.atom .k)) (varCode (n-1)))
def atomResult (c : Nat) : Result := (false,c,appCode (encode (Poly.atom .k)) c)
def appResult (a b : Result) : Result :=
  let free := a.1 || b.1
  let dropped := appCode a.2.1 b.2.1
  (free, dropped,
    bif free then appCode (appCode (encode (Poly.atom .s)) a.2.2) b.2.2
    else appCode (encode (Poly.atom .k)) dropped)

theorem primrec_varResult : Primrec varResult := by
  have hv := primrec_varCode.comp Primrec.pred
  exact (Primrec.eq.comp Primrec.id (.const 0)).pair
    (hv.pair (Primrec.ite (Primrec.eq.comp Primrec.id (.const 0)) (.const _)
      (primrec_appCode.comp (.const _) hv)))

theorem primrec_atomResult : Primrec atomResult :=
  (Primrec.const false).pair (Primrec.id.pair (primrec_appCode.comp (.const _) Primrec.id))

theorem primrec_appResult : Primrec₂ appResult := by
  have hfree : Primrec (fun p : Result × Result => p.1.1 || p.2.1) :=
    Primrec.or.comp (Primrec.fst.comp Primrec.fst) (Primrec.fst.comp Primrec.snd)
  have hdrop : Primrec (fun p : Result × Result => appCode p.1.2.1 p.2.2.1) :=
    primrec_appCode.comp (Primrec.fst.comp (Primrec.snd.comp Primrec.fst))
      (Primrec.fst.comp (Primrec.snd.comp Primrec.snd))
  have habs : Primrec (fun p : Result × Result =>
      appCode (appCode (encode (Poly.atom .s)) p.1.2.2) p.2.2.2) :=
    primrec_appCode.comp
      (primrec_appCode.comp (.const _) (Primrec.snd.comp (Primrec.snd.comp Primrec.fst)))
      (Primrec.snd.comp (Primrec.snd.comp Primrec.snd))
  exact hfree.pair (hdrop.pair (Primrec.cond hfree habs (primrec_appCode.comp (.const _) hdrop)))

/-- Simultaneously compute free-variable-zero, dropped syntax, and exact compiled
    bracket abstraction. Invalid input is totalized, not asserted valid. -/
def analyze (c : Nat) : Result :=
  if tag c = 0 then varResult (varIndex c)
  else if tag c = 1 then atomResult c
  else if tag c = 2 then
    if _ha : arg1 c < c then
      if _hb : arg2 c < c then appResult (analyze (arg1 c)) (analyze (arg2 c))
      else (false,0,0)
    else (false,0,0)
  else (false,0,0)
termination_by c

def analysisStep (values : List Result) : Result :=
  let c := values.length
  if tag c = 0 then varResult (varIndex c)
  else if tag c = 1 then atomResult c
  else if tag c = 2 then
    if arg1 c < c then
      if arg2 c < c then
        appResult (values[arg1 c]?.getD (false,0,0)) (values[arg2 c]?.getD (false,0,0))
      else (false,0,0)
    else (false,0,0)
  else (false,0,0)

theorem primrec_analysisStep : Primrec analysisStep := by
  have hl : Primrec (fun p : List Result => p.length) := Primrec.list_length
  have ht := primrec_tag.comp hl
  have ha := primrec_arg1.comp hl
  have hb := primrec_arg2.comp hl
  have hgetA := Primrec.option_getD.comp (Primrec.list_getElem?.comp Primrec.id ha) (.const (false,0,0))
  have hgetB := Primrec.option_getD.comp (Primrec.list_getElem?.comp Primrec.id hb) (.const (false,0,0))
  exact Primrec.ite (Primrec.eq.comp ht (.const 0)) (primrec_varResult.comp (primrec_varIndex.comp hl))
    (Primrec.ite (Primrec.eq.comp ht (.const 1)) (primrec_atomResult.comp hl)
      (Primrec.ite (Primrec.eq.comp ht (.const 2))
        (Primrec.ite (Primrec.nat_lt.comp ha hl)
          (Primrec.ite (Primrec.nat_lt.comp hb hl) (primrec_appResult.comp hgetA hgetB) (.const _))
          (.const _)) (.const _)))

theorem analysisStep_exact (c : Nat) :
    analysisStep ((List.range c).map analyze) = analyze c := by
  rw [analyze]
  unfold analysisStep
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

theorem primrec_analyze : Primrec analyze := by
  have h : Primrec₂ (fun (_ : Unit) c => analyze c) :=
    Primrec.nat_strong_rec (fun (_ : Unit) c => analyze c)
      ((Primrec.option_some.comp primrec_analysisStep).comp Primrec.snd).to₂
      (fun _ c => congrArg some (analysisStep_exact c))
  exact h.comp (.const ()) Primrec.id

theorem abstract_app_form (p q : Poly) :
    abstract (.app p q) =
      if freeZero p || freeZero q then
        .app (.app (.atom .s) (abstract p)) (abstract q)
      else .app (.atom .k) (.app (drop p) (drop q)) := by
  rw [abstract]
  rfl

/-- Exact source-level agreement, including the binder-removing drop operation. -/
theorem analyze_exact (p : Poly) :
    analyze (encode p) = (freeZero p, encode (drop p), encode (abstract p)) := by
  induction p with
  | var n =>
    rw [analyze]
    simp only [tag_var, varIndex_var, ↓reduceIte]
    cases n <;> simp [varResult, freeZero, drop, pren, psub, abstract, varCode_exact, encode_app]
  | atom t =>
    rw [analyze]
    simp [tag_atom, atomResult, freeZero, drop, pren, psub, abstract, encode_app]
  | app p q hp hq =>
    rw [analyze]
    have ha : encode p < encode (Poly.app p q) := by rw [encode_app]; exact left_lt_appCode _ _
    have hb : encode q < encode (Poly.app p q) := by rw [encode_app]; exact right_lt_appCode _ _
    simp only [tag_app, arg1_app, arg2_app, ha, hb, Nat.reduceEqDiff, ↓reduceIte, hp, hq]
    cases hfp : freeZero p <;> cases hfq : freeZero q <;>
      simp [appResult, abstract_app_form, freeZero, hfp, hfq, drop, pren, psub, encode_app]

def freeZeroCode (c : Nat) : Bool := (analyze c).1
def dropCode (c : Nat) : Nat := (analyze c).2.1
def abstractCode (c : Nat) : Nat := (analyze c).2.2

theorem primrec_freeZeroCode : Primrec freeZeroCode := Primrec.fst.comp primrec_analyze
theorem primrec_dropCode : Primrec dropCode := Primrec.fst.comp (Primrec.snd.comp primrec_analyze)
theorem primrec_abstractCode : Primrec abstractCode := Primrec.snd.comp (Primrec.snd.comp primrec_analyze)
theorem freeZeroCode_exact (p : Poly) : freeZeroCode (encode p) = freeZero p := by
  simp only [freeZeroCode, analyze_exact]
theorem dropCode_exact (p : Poly) : dropCode (encode p) = encode (drop p) := by
  simp only [dropCode, analyze_exact]
theorem abstractCode_exact (p : Poly) : abstractCode (encode p) = encode (abstract p) := by
  simp only [abstractCode, analyze_exact]

#print axioms primrec_abstractCode
#print axioms abstractCode_exact
end CodedPolyTransformations
