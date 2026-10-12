import RedExact
import TypeCodeSubstitution
namespace AuxiliaryCodeComputability
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity
open CodedMixedTransformations
open AuxiliaryCertificates OrthemologyV2 OrthemologyV3 P01D
set_option maxRecDepth 8192
set_option maxHeartbeats 200000
attribute [local irreducible] Nat.pair checkStepCode checkRedCode instantiateTypeCode

@[simp] theorem encode_finite_i (A : TypeCode) : encode (.i A : FiniteCert) = pack 0 [leaf (encode A)] := rfl

@[simp] theorem encode_finite_k (A B : TypeCode) : encode (.k A B : FiniteCert) = pack 1 [leaf (encode A), leaf (encode B)] := rfl

@[simp] theorem encode_finite_s (A B C : TypeCode) : encode (.s A B C : FiniteCert) = pack 2 [leaf (encode A), leaf (encode B), leaf (encode C)] := rfl

@[simp] theorem encode_finite_app (f x : Term) (A B : TypeCode) (p q : FiniteCert) : encode (.app f x A B p q : FiniteCert) = pack 3 [leaf (encode f), leaf (encode x), leaf (encode A), leaf (encode B), encode p, encode q] := rfl

@[simp] theorem encode_finite_allI (t : Term) (B : TypeCode) (p : FiniteCert) : encode (.allI t B p : FiniteCert) = pack 4 [leaf (encode t), leaf (encode B), encode p] := rfl

@[simp] theorem encode_finite_allE (t : Term) (B A : TypeCode) (p : FiniteCert) : encode (.allE t B A p : FiniteCert) = pack 5 [leaf (encode t), leaf (encode B), leaf (encode A), encode p] := rfl

@[simp] theorem encode_finite_reduce (t u : Term) (A : TypeCode) (p : FiniteCert) (r : RedCert) : encode (.reduce t u A p r : FiniteCert) = pack 6 [leaf (encode t), leaf (encode u), leaf (encode A), encode p, leaf (encode r)] := rfl

def finiteShape (s : Nat × Nat) : Bool :=
  if tag s.2 = 0 then (decide (lhs s = encode Term.i) && decide (rhs s = tyArrow (v1 s.2) (v1 s.2)))
  else if tag s.2 = 1 then (decide (lhs s = encode Term.k) && decide (rhs s = tyArrow (v1 s.2) (tyArrow (v2 s.2) (v1 s.2))))
  else if tag s.2 = 2 then (decide (lhs s = encode Term.s) && decide (rhs s = tyArrow (tyArrow (v1 s.2) (tyArrow (v2 s.2) (v3 s.2))) (tyArrow (tyArrow (v1 s.2) (v2 s.2)) (tyArrow (v1 s.2) (v3 s.2)))))
  else if tag s.2 = 3 then (decide (lhs s = tmApp (v1 s.2) (v2 s.2)) && decide (rhs s = v4 s.2))
  else if tag s.2 = 4 then (decide (lhs s = v1 s.2) && decide (rhs s = tyAll (v2 s.2)))
  else if tag s.2 = 5 then (decide (lhs s = v1 s.2) && decide (rhs s = instantiateTypeCode (v3 s.2) (v2 s.2)))
  else if tag s.2 = 6 then ((decide (lhs s = v2 s.2) && decide (rhs s = v3 s.2)) && checkRedCode (v5 s.2) (v1 s.2) (v2 s.2))
  else false

def finiteChildren (s : Nat × Nat) : List (Nat × Nat) :=
  if tag s.2 = 3 then [(Nat.pair (v1 s.2) (tyArrow (v3 s.2) (v4 s.2)), a5 s.2), (Nat.pair (v2 s.2) (v3 s.2), a6 s.2)]
  else if tag s.2 = 4 then [(Nat.pair (v1 s.2) (v2 s.2), a3 s.2)]
  else if tag s.2 = 5 then [(Nat.pair (v1 s.2) (tyAll (v2 s.2)), a4 s.2)]
  else if tag s.2 = 6 then [(Nat.pair (v1 s.2) (v3 s.2), a4 s.2)]
  else []

def checkFiniteCode (c a b : Nat) : Bool := evaluate finiteShape finiteChildren (Nat.pair a b,c)

theorem primrec_finiteShape : Primrec finiteShape := by
  have h := (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 0)) (Primrec.and.comp (Primrec.eq.comp primrec_lhs (Primrec.const (encode Term.i))) (Primrec.eq.comp primrec_rhs (primrec_tyArrow.comp (primrec_v1.comp Primrec.snd) (primrec_v1.comp Primrec.snd)))) (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 1)) (Primrec.and.comp (Primrec.eq.comp primrec_lhs (Primrec.const (encode Term.k))) (Primrec.eq.comp primrec_rhs (primrec_tyArrow.comp (primrec_v1.comp Primrec.snd) (primrec_tyArrow.comp (primrec_v2.comp Primrec.snd) (primrec_v1.comp Primrec.snd))))) (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 2)) (Primrec.and.comp (Primrec.eq.comp primrec_lhs (Primrec.const (encode Term.s))) (Primrec.eq.comp primrec_rhs (primrec_tyArrow.comp (primrec_tyArrow.comp (primrec_v1.comp Primrec.snd) (primrec_tyArrow.comp (primrec_v2.comp Primrec.snd) (primrec_v3.comp Primrec.snd))) (primrec_tyArrow.comp (primrec_tyArrow.comp (primrec_v1.comp Primrec.snd) (primrec_v2.comp Primrec.snd)) (primrec_tyArrow.comp (primrec_v1.comp Primrec.snd) (primrec_v3.comp Primrec.snd)))))) (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 3)) (Primrec.and.comp (Primrec.eq.comp primrec_lhs (primrec_tmApp.comp (primrec_v1.comp Primrec.snd) (primrec_v2.comp Primrec.snd))) (Primrec.eq.comp primrec_rhs (primrec_v4.comp Primrec.snd))) (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 4)) (Primrec.and.comp (Primrec.eq.comp primrec_lhs (primrec_v1.comp Primrec.snd)) (Primrec.eq.comp primrec_rhs (primrec_tyAll.comp (primrec_v2.comp Primrec.snd)))) (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 5)) (Primrec.and.comp (Primrec.eq.comp primrec_lhs (primrec_v1.comp Primrec.snd)) (Primrec.eq.comp primrec_rhs (CodedMixedTransformations.primrec_instantiateTypeCode.comp (primrec_v3.comp Primrec.snd) (primrec_v2.comp Primrec.snd)))) (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 6)) (Primrec.and.comp (Primrec.and.comp (Primrec.eq.comp primrec_lhs (primrec_v2.comp Primrec.snd)) (Primrec.eq.comp primrec_rhs (primrec_v3.comp Primrec.snd))) (primrec_checkRedCode.comp ((primrec_v5.comp Primrec.snd).pair ((primrec_v1.comp Primrec.snd).pair (primrec_v2.comp Primrec.snd))))) (Primrec.const false))))))))
  exact h.of_eq (by intro s; dsimp only [finiteShape])

theorem primrec_finiteChildren : Primrec finiteChildren :=
  (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 3)) (Primrec.list_cons.comp ((Primrec₂.natPair.comp (primrec_v1.comp Primrec.snd) (primrec_tyArrow.comp (primrec_v3.comp Primrec.snd) (primrec_v4.comp Primrec.snd))).pair (primrec_a5.comp Primrec.snd)) (Primrec.list_cons.comp ((Primrec₂.natPair.comp (primrec_v2.comp Primrec.snd) (primrec_v3.comp Primrec.snd)).pair (primrec_a6.comp Primrec.snd)) (Primrec.const []))) (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 4)) (Primrec.list_cons.comp ((Primrec₂.natPair.comp (primrec_v1.comp Primrec.snd) (primrec_v2.comp Primrec.snd)).pair (primrec_a3.comp Primrec.snd)) (Primrec.const [])) (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 5)) (Primrec.list_cons.comp ((Primrec₂.natPair.comp (primrec_v1.comp Primrec.snd) (primrec_tyAll.comp (primrec_v2.comp Primrec.snd))).pair (primrec_a4.comp Primrec.snd)) (Primrec.const [])) (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 6)) (Primrec.list_cons.comp ((Primrec₂.natPair.comp (primrec_v1.comp Primrec.snd) (primrec_v3.comp Primrec.snd)).pair (primrec_a4.comp Primrec.snd)) (Primrec.const [])) (Primrec.const [])))))

theorem primrec_checkFiniteCode : Primrec (fun p : Nat × Nat × Nat => checkFiniteCode p.1 p.2.1 p.2.2) :=
  (primrec_evaluate primrec_finiteShape primrec_finiteChildren).comp
    ((Primrec₂.natPair.comp (Primrec.fst.comp Primrec.snd) (Primrec.snd.comp Primrec.snd)).pair Primrec.fst)

theorem eval_finite (a b c : Nat) : evaluate finiteShape finiteChildren (Nat.pair a b,c) = checkFiniteCode c a b := rfl

end AuxiliaryCodeComputability
