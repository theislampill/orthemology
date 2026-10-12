import CoreGrammar
namespace CodedPolyTransformations
open P01AC P01D Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

def scopeTyShape (s : Nat × Nat) : Bool :=
  if tag s.2 = 6 then
    checkScope s.1 (rest (arg2 s.2)) && checkScope s.1 (rest (arg3 s.2))
  else true

def scopeTyChildren (s : Nat × Nat) : List (Nat × Nat) :=
  if tag s.2 = 2 then [(s.1,arg1 s.2)]
  else if tag s.2 = 4 ∨ tag s.2 = 5 then [(s.1,arg1 s.2),(s.1+1,arg2 s.2)]
  else if tag s.2 = 6 then [(s.1,arg1 s.2)] else []

def checkTyScope (n c : Nat) : Bool := evaluate scopeTyShape scopeTyChildren (n,c)

theorem primrec_arg3 : Primrec arg3 :=
  primrec_first.comp (primrec_rest.comp (primrec_rest.comp primrec_rest))

theorem primrec_scopeTyShape : Primrec scopeTyShape :=
  Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 6))
    (Primrec.and.comp
      (primrec_checkScope.comp Primrec.fst (primrec_rest.comp (primrec_arg2.comp Primrec.snd)))
      (primrec_checkScope.comp Primrec.fst (primrec_rest.comp (primrec_arg3.comp Primrec.snd))))
    (.const true)

theorem primrec_scopeTyChildren : Primrec scopeTyChildren := by
  have ht := primrec_tag.comp (Primrec.snd : Primrec (fun s : Nat × Nat => s.2))
  have ha : Primrec (fun s : Nat × Nat => (s.1,arg1 s.2)) := Primrec.fst.pair (primrec_arg1.comp Primrec.snd)
  have hb : Primrec (fun s : Nat × Nat => (s.1+1,arg2 s.2)) := (Primrec.succ.comp Primrec.fst).pair (primrec_arg2.comp Primrec.snd)
  have hsingle := Primrec.list_cons.comp ha (Primrec.const [])
  have hdouble := Primrec.list_cons.comp ha (Primrec.list_cons.comp hb (Primrec.const []))
  exact Primrec.ite (Primrec.eq.comp ht (.const 2)) hsingle
    (Primrec.ite ((Primrec.eq.comp ht (.const 4)).or (Primrec.eq.comp ht (.const 5))) hdouble
      (Primrec.ite (Primrec.eq.comp ht (.const 6)) hsingle (.const [])))

theorem primrec_checkTyScope : Primrec₂ checkTyScope :=
  primrec_evaluate primrec_scopeTyShape primrec_scopeTyChildren

theorem unary_child_lt (t a : Nat) : a < unary t a :=
  lt_of_lt_of_le (left_lt_node _ _) (right_le_node _ _)
theorem binary_left_lt (t a b : Nat) : a < binary t a b :=
  lt_of_lt_of_le (left_lt_node _ _) (right_le_node _ _)
theorem binary_right_lt (t a b : Nat) : b < binary t a b :=
  lt_of_lt_of_le (left_lt_node _ _) (le_trans (right_le_node _ _) (right_le_node _ _))
theorem ternary_left_lt (t a b d : Nat) : a < ternary t a b d :=
  lt_of_lt_of_le (left_lt_node _ _) (right_le_node _ _)

theorem eval_scope (n c : Nat) : evaluate scopeTyShape scopeTyChildren (n,c) = checkTyScope n c := rfl

/-- Exactness to the actual binder-sensitive TyScoped predicate. -/
theorem checkTyScope_exact (n : Nat) (A : Ty) :
    checkTyScope n (encode A) = decide (TyScoped n A) := by
  induction A generalizing n with
  | param k =>
    rw [checkTyScope,evaluate]
    simp [scopeTyShape,scopeTyChildren,TyScoped]
  | bottom =>
    rw [checkTyScope,evaluate]
    simp [scopeTyShape,scopeTyChildren,TyScoped]
  | raw =>
    rw [checkTyScope,evaluate]
    simp [scopeTyShape,scopeTyChildren,TyScoped]
  | all B ih =>
    rw [checkTyScope,evaluate]
    have h := unary_child_lt 2 (encode B)
    simp [scopeTyShape,scopeTyChildren,h,eval_scope,ih,TyScoped]
  | pi A B iha ihb =>
    rw [checkTyScope,evaluate]
    have ha := binary_left_lt 4 (encode A) (encode B)
    have hb := binary_right_lt 4 (encode A) (encode B)
    simp [scopeTyShape,scopeTyChildren,ha,hb,eval_scope,iha,ihb,TyScoped]
  | sigma A B iha ihb =>
    rw [checkTyScope,evaluate]
    have ha := binary_left_lt 5 (encode A) (encode B)
    have hb := binary_right_lt 5 (encode A) (encode B)
    simp [scopeTyShape,scopeTyChildren,ha,hb,eval_scope,iha,ihb,TyScoped]
  | identity A p q ih =>
    rw [checkTyScope,evaluate]
    have ha := ternary_left_lt 6 (encode A) (leaf (encode p)) (leaf (encode q))
    simp [scopeTyShape,scopeTyChildren,ha,eval_scope,ih,checkScope_exact,TyScoped,
      Bool.and_comm,Bool.and_left_comm,Bool.and_assoc]

#print axioms primrec_checkTyScope
#print axioms checkTyScope_exact
end CodedPolyTransformations
