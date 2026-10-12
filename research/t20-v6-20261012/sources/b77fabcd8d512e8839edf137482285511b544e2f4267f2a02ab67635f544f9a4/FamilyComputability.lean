import EncodedCertificateSyntax
import FullPERHalting

/- An exact bridge for the existing syntax encoding. No Primcodable instance for
   source syntax, alternate encoding, or checker computability is assumed. -/
namespace SourceFamilyComputability
open P01D P01AC P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open Encodable
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- Number-leaf and pair-node arithmetic of the existing derived codec. -/
def leaf (n : Nat) : Nat := Nat.pair 0 n
def node (a b : Nat) : Nat := Nat.pair (a + 1) b

def appCode (a b : Nat) : Nat := node (leaf 2) (node a (node b (leaf 0)))
def piCode (a b : Nat) : Nat := node (leaf 4) (node a (node b (leaf 0)))
def identityCode (a p q : Nat) : Nat :=
  node (leaf 6) (node a (node (leaf p) (node (leaf q) (leaf 0))))

theorem encode_app (p q : Poly) : encode (Poly.app p q) = appCode (encode p) (encode q) := rfl
theorem encode_pi (A B : Ty) : encode (Ty.pi A B) = piCode (encode A) (encode B) := rfl
theorem encode_identity (A : Ty) (p q : Poly) :
    encode (Ty.identity A p q) = identityCode (encode A) (encode p) (encode q) := rfl

/-- Exact (un-normalised) source syntax inserted at each numeral step. -/
def numeralStep : Poly := .app (.atom .s)
  (.app (.app (.atom .s) (.app (.atom .k) (.atom .s)))
    (.app (.app (.atom .s) (.app (.atom .k) (.atom .k))) (.atom .i)))

theorem freeZero_iteration (n : Nat) : freeZero (iterationPoly n) = true := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [iterationPoly, freeZero, ih, Bool.or_true]

theorem abstract_iteration_succ (n : Nat) :
    abstract (iterationPoly (n+1)) =
      .app (.app (.atom .s) (.app (.atom .k) (.var 0))) (abstract (iterationPoly n)) := by
  rw [iterationPoly, abstract]
  simp only [freeZero, freeZero_iteration, Bool.or_true, ↓reduceIte]
  simp only [abstract, freeZero, beq_iff_eq, reduceCtorEq, Bool.false_eq_true, ↓reduceIte, drop, pren, psub, Nat.pred_succ]

theorem inputNumeral_zero : inputNumeral 0 = .app (.atom .k) (.atom .i) := by
  simp [inputNumeral, iterationPoly, abstract, freeZero, drop, pren, psub]

theorem inputNumeral_succ (n : Nat) :
    inputNumeral (n+1) = .app numeralStep (inputNumeral n) := by
  unfold inputNumeral
  rw [abstract_iteration_succ]
  rw [abstract]
  simp [freeZero, abstract, drop, pren, psub, numeralStep]

theorem primrec_leaf : Primrec leaf :=
  Primrec₂.natPair.comp (Primrec.const 0) Primrec.id

theorem primrec_node : Primrec₂ node :=
  Primrec₂.natPair.comp₂ (Primrec.succ.comp Primrec.fst).to₂ Primrec₂.right

theorem primrec_appCode : Primrec₂ appCode :=
  primrec_node.comp₂ (.const _) (primrec_node.comp₂ .left (primrec_node.comp₂ .right (.const _)))

theorem primrec_piCode : Primrec₂ piCode :=
  primrec_node.comp₂ (.const _) (primrec_node.comp₂ .left (primrec_node.comp₂ .right (.const _)))

def numeralCode : Nat → Nat := Nat.rec (encode (inputNumeral 0))
  (fun _ previous => appCode (encode numeralStep) previous)

theorem numeralCode_exact (n : Nat) : numeralCode n = encode (inputNumeral n) := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [numeralCode, Nat.rec_add_one, inputNumeral_succ, encode_app, ← ih]

theorem primrec_numeralCode : Primrec numeralCode :=
  Primrec.nat_rec₁ _ (primrec_appCode.comp₂ (.const _) .right)

/-- Mathlib primitive-recursive certificate for the actual source numeral code. -/
theorem primrec_encode_inputNumeral : Primrec (fun n => encode (inputNumeral n)) :=
  primrec_numeralCode.of_eq numeralCode_exact

/-- Mathlib primitive-recursive certificate for the actual simulator family code,
    uniformly over the natural machine index; the PR program itself is fixed. -/
theorem primrec_encode_simFamily (f : PR 2) : Primrec (fun e => encode (simFamily f e)) := by
  simpa only [simFamily, encode_app] using
    primrec_appCode.comp (Primrec.const (encode (simulator f))) primrec_encode_inputNumeral

theorem primrec_encode_testBody {p : Nat → Poly} (hp : Primrec (fun n => encode (p n))) :
    Primrec (fun n => encode (FullPERTests.testBody (p n))) := by
  simpa only [FullPERTests.testBody, encode_app] using
    primrec_appCode.comp
      (primrec_appCode.comp
        (primrec_appCode.comp hp (Primrec.const (encode (Poly.var 0))))
        (Primrec.const (encode (Poly.atom .zero))))
      (Primrec.const (encode (Poly.atom .one)))

/-- The source-to-code family map in the semantic non-r.e. boundary is primitive
    recursive under exactly the existing syntax Encodable instance. -/
theorem primrec_encode_programType (f : PR 2) :
    Primrec (fun e => encode (FullPERTests.programType f e)) := by
  have hp := primrec_encode_testBody (primrec_encode_simFamily f)
  have hbody : Primrec (fun e => identityCode (encode Ty.raw)
      (encode (FullPERTests.testBody (simFamily f e))) (encode (Poly.atom .zero))) :=
    primrec_node.comp (Primrec.const _) (primrec_node.comp (Primrec.const _)
      (primrec_node.comp (primrec_leaf.comp hp)
        (Primrec.const (node (leaf (encode (Poly.atom .zero))) (leaf 0)))))
  simpa only [FullPERTests.programType, FullPERTests.testType, encode_pi, encode_identity] using
    primrec_piCode.comp (Primrec.const (encode N)) hbody

theorem computable_encode_programType (f : PR 2) :
    Computable (fun e => encode (FullPERTests.programType f e)) :=
  (primrec_encode_programType f).to_comp

#print axioms primrec_encode_inputNumeral
#print axioms primrec_encode_programType
#print axioms computable_encode_programType
#print axioms inputNumeral_succ
#print axioms encode_app
end SourceFamilyComputability
