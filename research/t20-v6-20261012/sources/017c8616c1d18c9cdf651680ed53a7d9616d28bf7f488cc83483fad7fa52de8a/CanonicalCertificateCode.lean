import SerialCertificateCheck
import RuleConclusionCode
import RulePremisesCode
import RuleSideCode
import CertificateGrammar
namespace ActualSourceEnumerability
open Encodable JointCertificates SourceFamilyComputability CodedScope ExactSyntaxValidity
open AuxiliaryCodeComputability TelescopeCodeValidity CertificateCodeValidity CodedRuleTemplates
set_option maxRecDepth 16384
set_option maxHeartbeats 4000000
attribute [local irreducible] Nat.pair

/-- Source-list order is checked by simultaneous head/tail traversal, never zip. -/
def checkerShape (s : Nat × Nat) : Bool :=
  if lhs s = 0 then checkSideCode (v1 s.2) && decide (conclusionCode (v1 s.2) = rhs s)
  else if lhs s = 1 then
    if tag s.2 = 0 then decide (listNatDecode (rhs s) = [])
    else if tag s.2 = 1 then decide (listNatDecode (rhs s) ≠ [])
    else false
  else false

def expectedHead (s : Nat × Nat) : Nat := (listNatDecode (rhs s)).head?.getD 0
def expectedTail (s : Nat × Nat) : Nat := encode (listNatDecode (rhs s)).tail

def checkerChildren (s : Nat × Nat) : List (Nat × Nat) :=
  if lhs s = 0 then [(Nat.pair 1 (encode (premisesCode (v1 s.2))), a2 s.2)]
  else if lhs s = 1 ∧ tag s.2 = 1 then
    [(Nat.pair 0 (expectedHead s), a1 s.2), (Nat.pair 1 (expectedTail s), a2 s.2)]
  else []

def runNode (claimCode certCode : Nat) : Bool :=
  evaluate checkerShape checkerChildren (Nat.pair 0 claimCode, certCode)
def runList (claimListCode certListCode : Nat) : Bool :=
  evaluate checkerShape checkerChildren (Nat.pair 1 claimListCode, certListCode)

/-- Only exact canonical source codes are admitted; the local evaluator is total
    on every natural input, but need not emulate the old decoder off its image. -/
def checkCanonical (claimCode certCode : Nat) : Bool :=
  certValid 11 claimCode && certValid 13 certCode && runNode claimCode certCode

theorem primrec_expectedHead : Primrec expectedHead :=
  Primrec.option_getD.comp (Primrec.list_head?.comp (primrec_listNatDecode.comp primrec_rhs)) (.const 0)
theorem primrec_expectedTail : Primrec expectedTail :=
  Primrec.encode.comp (Primrec.list_tail.comp (primrec_listNatDecode.comp primrec_rhs))

theorem primrec_checkerShape : Primrec checkerShape :=
  Primrec.ite (Primrec.eq.comp primrec_lhs (.const 0))
    (Primrec.and.comp (primrec_checkSideCode.comp (primrec_v1.comp Primrec.snd))
      (Primrec.eq.comp (primrec_conclusionCode.comp (primrec_v1.comp Primrec.snd)) primrec_rhs))
    (Primrec.ite (Primrec.eq.comp primrec_lhs (.const 1))
      (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 0))
        (Primrec.eq.comp (primrec_listNatDecode.comp primrec_rhs) (.const []))
        (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 1))
          (Primrec.eq.comp (primrec_listNatDecode.comp primrec_rhs) (.const [])).not
          (.const false))) (.const false))

theorem primrec_checkerChildren : Primrec checkerChildren :=
  Primrec.ite (Primrec.eq.comp primrec_lhs (.const 0))
    (Primrec.list_cons.comp
      ((Primrec₂.natPair.comp (.const 1) (Primrec.encode.comp
        (primrec_premisesCode.comp (primrec_v1.comp Primrec.snd)))).pair (primrec_a2.comp Primrec.snd))
      (.const []))
    (Primrec.ite (PrimrecPred.and (Primrec.eq.comp primrec_lhs (.const 1))
        (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 1)))
      (Primrec.list_cons.comp
        ((Primrec₂.natPair.comp (.const 0) primrec_expectedHead).pair (primrec_a1.comp Primrec.snd))
        (Primrec.list_cons.comp
          ((Primrec₂.natPair.comp (.const 1) primrec_expectedTail).pair (primrec_a2.comp Primrec.snd))
          (.const []))) (.const []))

theorem primrec_runNode : Primrec₂ runNode :=
  (primrec_evaluate primrec_checkerShape primrec_checkerChildren).comp
    ((Primrec₂.natPair.comp (.const 0) Primrec.fst).pair Primrec.snd)
theorem primrec_runList : Primrec₂ runList :=
  (primrec_evaluate primrec_checkerShape primrec_checkerChildren).comp
    ((Primrec₂.natPair.comp (.const 1) Primrec.fst).pair Primrec.snd)
theorem primrec_checkCanonical : Primrec₂ checkCanonical :=
  Primrec.and.comp (Primrec.and.comp
    (primrec_certValid.comp (.const 11) Primrec.fst)
    (primrec_certValid.comp (.const 13) Primrec.snd)) primrec_runNode

@[simp] theorem serial_list_node_lt (r : Rule) (cs : SerialCertList) :
    encode cs < encode (SerialCert.node r cs) := by
  rw [encode_SerialCert_node]
  apply field_lt_pack; simp
@[simp] theorem serial_cons_head_lt (c : SerialCert) (cs : SerialCertList) :
    encode c < encode (SerialCertList.cons c cs) := by
  rw [encode_SerialCertList_cons]
  apply field_lt_pack; simp
@[simp] theorem serial_cons_tail_lt (c : SerialCert) (cs : SerialCertList) :
    encode cs < encode (SerialCertList.cons c cs) := by
  rw [encode_SerialCertList_cons]
  apply field_lt_pack; simp

@[simp] theorem node_rule_view (r : Rule) (cs : SerialCertList) :
    v1 (encode (SerialCert.node r cs)) = encode r := by
  simp [v1, a1, arg1, encode_SerialCert_node, pack]
@[simp] theorem node_list_view (r : Rule) (cs : SerialCertList) :
    a2 (encode (SerialCert.node r cs)) = encode cs := by
  simp [a2, arg2, encode_SerialCert_node, pack]
@[simp] theorem list_nil_tag : tag (encode SerialCertList.nil) = 0 := by
  simp
@[simp] theorem list_cons_tag (c : SerialCert) (cs : SerialCertList) :
    tag (encode (SerialCertList.cons c cs)) = 1 := by simp
@[simp] theorem list_head_view (c : SerialCert) (cs : SerialCertList) :
    a1 (encode (SerialCertList.cons c cs)) = encode c := by
  simp [a1, arg1, encode_SerialCertList_cons, pack]
@[simp] theorem list_tail_view (c : SerialCert) (cs : SerialCertList) :
    a2 (encode (SerialCertList.cons c cs)) = encode cs := by
  simp [a2, arg2, encode_SerialCertList_cons, pack]

theorem runNode_node (r : Rule) (cs : SerialCertList) (j : Claim) :
    runNode (encode j) (encode (SerialCert.node r cs)) =
      (r.checkSide && decide (r.conclusion = j) && runList (encode r.premises) (encode cs)) := by
  rw [runNode, evaluate]
  simp only [checkerShape, checkerChildren, lhs_pair, rhs_pair, node_rule_view,
    node_list_view, checkSideCode_exact, conclusionCode_exact, premisesCode_exact,
    Encodable.encode_injective.eq_iff, encode_map_encode, if_pos rfl,
    List.all_cons, List.all_nil, serial_list_node_lt, ↓reduceDIte, Bool.and_true,
    ite_true, ite_false, dite_true]
  rfl

theorem runList_nil (js : List Claim) :
    runList (encode js) (encode SerialCertList.nil) = decide (js = []) := by
  rw [runList, evaluate]
  simp only [checkerShape, checkerChildren, lhs_pair, rhs_pair, list_nil_tag,
    Nat.one_ne_zero, ↓reduceIte, and_false, List.all_nil, Bool.and_true,
    listNatDecode_encode, List.map_eq_nil_iff, Nat.zero_ne_one, and_false, ite_false,
    List.all_nil, Bool.and_true]

theorem runList_cons_nil (c : SerialCert) (cs : SerialCertList) :
    runList (encode ([] : List Claim)) (encode (SerialCertList.cons c cs)) = false := by
  rw [runList, evaluate]
  simp only [checkerShape, lhs_pair, rhs_pair, list_cons_tag, Nat.one_ne_zero,
    ↓reduceIte, listNatDecode_encode, List.map_nil, not_true_eq_false,
    decide_false, Bool.false_and, ne_eq, eq_self_iff_true, not_true_eq_false,
    decide_false, Bool.false_and]

theorem runList_cons_cons (c : SerialCert) (cs : SerialCertList) (j : Claim) (js : List Claim) :
    runList (encode (j :: js)) (encode (SerialCertList.cons c cs)) =
      (runNode (encode j) (encode c) && runList (encode js) (encode cs)) := by
  rw [runList, evaluate]
  simp only [checkerShape, checkerChildren, lhs_pair, rhs_pair, list_cons_tag,
    Nat.one_ne_zero, ↓reduceIte, and_self, list_head_view, list_tail_view,
    listNatDecode_encode, List.map_cons, List.cons_ne_nil, not_false_eq_true,
    decide_true, Bool.true_and, List.all_cons, List.all_nil, Bool.and_true,
    serial_cons_head_lt, serial_cons_tail_lt, ↓reduceDIte,
    expectedHead, expectedTail, lhs_pair, rhs_pair, listNatDecode_encode,
    List.map_cons, List.head?_cons, Option.getD_some, List.tail_cons, encode_map_encode]
  rfl

mutual
theorem runNode_exact (c : SerialCert) (j : Claim) :
    runNode (encode j) (encode c) = serialCheck c j := by
  cases c with
  | node r cs => rw [runNode_node, serialCheck, runList_exact]

theorem runList_exact (cs : SerialCertList) (js : List Claim) :
    runList (encode js) (encode cs) = serialCheckList cs js := by
  cases cs with
  | nil => cases js <;> rw [runList_nil] <;> rfl
  | cons c cs =>
    cases js with
    | nil => rw [runList_cons_nil]; rfl
    | cons j js => rw [runList_cons_cons, serialCheckList, runNode_exact, runList_exact]
end

#print axioms primrec_checkCanonical
#print axioms runNode_exact
end ActualSourceEnumerability
