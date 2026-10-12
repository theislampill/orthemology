import FamilyComputability

namespace CodedScope
open P01D P01AC Encodable SourceFamilyComputability
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- Arithmetic views of the exact retained source syntax encoding. -/
def first (c : Nat) : Nat := c.unpair.1 - 1
def rest (c : Nat) : Nat := c.unpair.2
def tag (c : Nat) : Nat := (first c).unpair.2
def arg1 (c : Nat) : Nat := first (rest c)
def arg2 (c : Nat) : Nat := first (rest (rest c))
def varIndex (c : Nat) : Nat := (arg1 c).unpair.2

theorem primrec_first : Primrec first := Primrec.pred.comp (Primrec.fst.comp Primrec.unpair)
theorem primrec_rest : Primrec rest := Primrec.snd.comp Primrec.unpair
theorem primrec_tag : Primrec tag := primrec_rest.comp primrec_first
theorem primrec_arg1 : Primrec arg1 := primrec_first.comp primrec_rest
theorem primrec_arg2 : Primrec arg2 := primrec_first.comp (primrec_rest.comp primrec_rest)
theorem primrec_varIndex : Primrec varIndex := primrec_rest.comp primrec_arg1

@[simp] theorem first_node (a b : Nat) : first (node a b) = a := by simp [first, node]
@[simp] theorem rest_node (a b : Nat) : rest (node a b) = b := by simp [rest, node]
@[simp] theorem rest_leaf (n : Nat) : rest (leaf n) = n := by simp [rest, leaf]

theorem encode_var (n : Nat) : encode (Poly.var n) = node (leaf 0) (node (leaf n) (leaf 0)) := rfl
theorem encode_atom (t : OrthemologyV2.Term) :
    encode (Poly.atom t) = node (leaf 1) (node (leaf (encode t)) (leaf 0)) := rfl

@[simp] theorem tag_var (n : Nat) : tag (encode (Poly.var n)) = 0 := by
  simp only [encode_var, tag, first_node]; rfl
@[simp] theorem tag_atom (t : OrthemologyV2.Term) : tag (encode (Poly.atom t)) = 1 := by
  simp only [encode_atom, tag, first_node]; rfl
@[simp] theorem tag_app (p q : Poly) : tag (encode (Poly.app p q)) = 2 := by
  simp only [encode_app, appCode, tag, first_node]; rfl
@[simp] theorem varIndex_var (n : Nat) : varIndex (encode (Poly.var n)) = n := by
  simp [encode_var, varIndex, arg1, first_node, rest_node, leaf]
@[simp] theorem arg1_app (p q : Poly) : arg1 (encode (Poly.app p q)) = encode p := by
  simp [encode_app, appCode, arg1]
@[simp] theorem arg2_app (p q : Poly) : arg2 (encode (Poly.app p q)) = encode q := by
  simp [encode_app, appCode, arg2]

theorem left_lt_node (a b : Nat) : a < node a b := by
  have h := Nat.left_le_pair (a+1) b
  exact Nat.lt_of_lt_of_le (Nat.lt_succ_self a) h

theorem right_le_node (a b : Nat) : b ≤ node a b := Nat.right_le_pair _ _

theorem left_lt_appCode (a b : Nat) : a < appCode a b :=
  lt_of_lt_of_le (left_lt_node _ _) (right_le_node _ _)

theorem right_lt_appCode (a b : Nat) : b < appCode a b :=
  lt_of_lt_of_le (left_lt_node _ _) (le_trans (right_le_node _ _) (right_le_node _ _))

/-- Total arithmetic extension of the actual Scoped test. Invalid natural inputs
    have no source-syntax meaning; recursive calls are explicitly bounded. -/
def checkScope (n c : Nat) : Bool :=
  if tag c = 0 then decide (varIndex c < n)
  else if tag c = 1 then true
  else if tag c = 2 then
    if _h₁ : arg1 c < c then
      if _h₂ : arg2 c < c then checkScope n (arg1 c) && checkScope n (arg2 c)
      else false
    else false
  else false
termination_by c

/-- One primitive-recursive step on the finite table of smaller-code results. -/
def scopeStep (n : Nat) (values : List Bool) : Bool :=
  let c := values.length
  if tag c = 0 then decide (varIndex c < n)
  else if tag c = 1 then true
  else if tag c = 2 then
    if arg1 c < c then
      if arg2 c < c then values[arg1 c]?.getD false && values[arg2 c]?.getD false
      else false
    else false
  else false

theorem primrec_scopeStep : Primrec₂ scopeStep := by
  have hl : Primrec (fun p : Nat × List Bool => p.2.length) := Primrec.list_length.comp .snd
  have ht := primrec_tag.comp hl
  have hi := primrec_varIndex.comp hl
  have ha := primrec_arg1.comp hl
  have hb := primrec_arg2.comp hl
  have hgetA := Primrec.option_getD.comp (Primrec.list_getElem?.comp Primrec.snd ha) (Primrec.const false)
  have hgetB := Primrec.option_getD.comp (Primrec.list_getElem?.comp Primrec.snd hb) (Primrec.const false)
  exact Primrec.ite (Primrec.eq.comp ht (Primrec.const 0)) (Primrec.nat_lt.comp hi Primrec.fst)
    (Primrec.ite (Primrec.eq.comp ht (Primrec.const 1)) (Primrec.const true)
      (Primrec.ite (Primrec.eq.comp ht (Primrec.const 2))
        (Primrec.ite (Primrec.nat_lt.comp ha hl)
          (Primrec.ite (Primrec.nat_lt.comp hb hl) (Primrec.and.comp hgetA hgetB) (Primrec.const false))
          (Primrec.const false))
        (Primrec.const false)))

theorem scopeStep_exact (n c : Nat) :
    scopeStep n ((List.range c).map (checkScope n)) = checkScope n c := by
  rw [checkScope]
  unfold scopeStep
  simp only [List.length_map, List.length_range]
  by_cases ht0 : tag c = 0
  · simp [ht0]
  by_cases ht1 : tag c = 1
  · simp [ht0, ht1]
  by_cases ht2 : tag c = 2
  · by_cases ha : arg1 c < c
    · by_cases hb : arg2 c < c
      · simp [ht0, ht1, ht2, ha, hb, List.getElem?_map,
          List.getElem?_range ha, List.getElem?_range hb]
      · simp [ht0, ht1, ht2, ha, hb]
    · simp [ht0, ht1, ht2, ha]
  · simp [ht0, ht1, ht2]

/-- The actual recursively computed source scoping test has a Mathlib PR
    realizer on the existing natural syntax codes. No decoder assumption. -/
theorem primrec_checkScope : Primrec₂ checkScope :=
  Primrec.nat_strong_rec checkScope
    (Primrec.option_some.comp₂ primrec_scopeStep)
    (fun n c => congrArg some (scopeStep_exact n c))

theorem checkScope_exact (n : Nat) (p : Poly) :
    checkScope n (encode p) = decide (Scoped n p) := by
  induction p with
  | var k => rw [checkScope]; simp only [tag_var, varIndex_var, ↓reduceIte]; rfl
  | atom a => rw [checkScope]; simp only [tag_atom, Nat.one_ne_zero, ↓reduceIte]; rfl
  | app p q hp hq =>
    rw [checkScope]
    have hpa : arg1 (encode (Poly.app p q)) < encode (Poly.app p q) := by
      rw [arg1_app, encode_app]; exact left_lt_appCode _ _
    have hqa : arg2 (encode (Poly.app p q)) < encode (Poly.app p q) := by
      rw [arg2_app, encode_app]; exact right_lt_appCode _ _
    simp only [arg1_app] at hpa
    simp only [arg2_app] at hqa
    simp [tag_app, arg1_app, arg2_app, hpa, hqa, hp, hq, Scoped]

/-- This is a computable Boolean test, not merely an executable Lean definition. -/
theorem computable_checkScope : Computable₂ checkScope := primrec_checkScope.to_comp

#print axioms primrec_checkScope
#print axioms checkScope_exact
end CodedScope
