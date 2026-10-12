import AuxiliaryCodeCore
namespace AuxiliaryCodeComputability
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity
open AuxiliaryCertificates OrthemologyV2 P01D
set_option maxRecDepth 8192
set_option maxHeartbeats 200000
attribute [local irreducible] Nat.pair

@[simp] theorem encode_step_i (x : Term) : encode (.i x : StepCert) = pack 0 [leaf (encode x)] := rfl

@[simp] theorem encode_step_k (x y : Term) : encode (.k x y : StepCert) = pack 1 [leaf (encode x), leaf (encode y)] := rfl

@[simp] theorem encode_step_s (f g x : Term) : encode (.s f g x : StepCert) = pack 2 [leaf (encode f), leaf (encode g), leaf (encode x)] := rfl

@[simp] theorem encode_step_left (f g x : Term) (c : StepCert) : encode (.left f g x c : StepCert) = pack 3 [leaf (encode f), leaf (encode g), leaf (encode x), encode c] := rfl

@[simp] theorem encode_step_right (f x y : Term) (c : StepCert) : encode (.right f x y c : StepCert) = pack 4 [leaf (encode f), leaf (encode x), leaf (encode y), encode c] := rfl

def stepShape (s : Nat × Nat) : Bool :=
  if tag s.2 = 0 then (decide (lhs s = tmApp (encode Term.i) (v1 s.2)) && decide (rhs s = v1 s.2))
  else if tag s.2 = 1 then (decide (lhs s = tmApp (tmApp (encode Term.k) (v1 s.2)) (v2 s.2)) && decide (rhs s = v1 s.2))
  else if tag s.2 = 2 then (decide (lhs s = tmApp (tmApp (tmApp (encode Term.s) (v1 s.2)) (v2 s.2)) (v3 s.2)) && decide (rhs s = tmApp (tmApp (v1 s.2) (v3 s.2)) (tmApp (v2 s.2) (v3 s.2))))
  else if tag s.2 = 3 then (decide (lhs s = tmApp (v1 s.2) (v3 s.2)) && decide (rhs s = tmApp (v2 s.2) (v3 s.2)))
  else if tag s.2 = 4 then (decide (lhs s = tmApp (v1 s.2) (v2 s.2)) && decide (rhs s = tmApp (v1 s.2) (v3 s.2)))
  else false

def stepChildren (s : Nat × Nat) : List (Nat × Nat) :=
  if tag s.2 = 3 then [(Nat.pair (v1 s.2) (v2 s.2), a4 s.2)]
  else if tag s.2 = 4 then [(Nat.pair (v2 s.2) (v3 s.2), a4 s.2)]
  else []

def checkStepCode (c a b : Nat) : Bool := evaluate stepShape stepChildren (Nat.pair a b,c)

theorem primrec_stepShape : Primrec stepShape :=
  (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 0)) (Primrec.and.comp (Primrec.eq.comp primrec_lhs (primrec_tmApp.comp (Primrec.const _) (primrec_v1.comp Primrec.snd))) (Primrec.eq.comp primrec_rhs (primrec_v1.comp Primrec.snd))) (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 1)) (Primrec.and.comp (Primrec.eq.comp primrec_lhs (primrec_tmApp.comp (primrec_tmApp.comp (Primrec.const _) (primrec_v1.comp Primrec.snd)) (primrec_v2.comp Primrec.snd))) (Primrec.eq.comp primrec_rhs (primrec_v1.comp Primrec.snd))) (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 2)) (Primrec.and.comp (Primrec.eq.comp primrec_lhs (primrec_tmApp.comp (primrec_tmApp.comp (primrec_tmApp.comp (Primrec.const _) (primrec_v1.comp Primrec.snd)) (primrec_v2.comp Primrec.snd)) (primrec_v3.comp Primrec.snd))) (Primrec.eq.comp primrec_rhs (primrec_tmApp.comp (primrec_tmApp.comp (primrec_v1.comp Primrec.snd) (primrec_v3.comp Primrec.snd)) (primrec_tmApp.comp (primrec_v2.comp Primrec.snd) (primrec_v3.comp Primrec.snd))))) (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 3)) (Primrec.and.comp (Primrec.eq.comp primrec_lhs (primrec_tmApp.comp (primrec_v1.comp Primrec.snd) (primrec_v3.comp Primrec.snd))) (Primrec.eq.comp primrec_rhs (primrec_tmApp.comp (primrec_v2.comp Primrec.snd) (primrec_v3.comp Primrec.snd)))) (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 4)) (Primrec.and.comp (Primrec.eq.comp primrec_lhs (primrec_tmApp.comp (primrec_v1.comp Primrec.snd) (primrec_v2.comp Primrec.snd))) (Primrec.eq.comp primrec_rhs (primrec_tmApp.comp (primrec_v1.comp Primrec.snd) (primrec_v3.comp Primrec.snd)))) (Primrec.const false))))))

theorem primrec_stepChildren : Primrec stepChildren :=
  (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 3)) (Primrec.list_cons.comp ((Primrec₂.natPair.comp (primrec_v1.comp Primrec.snd) (primrec_v2.comp Primrec.snd)).pair (primrec_a4.comp Primrec.snd)) (Primrec.const [])) (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 4)) (Primrec.list_cons.comp ((Primrec₂.natPair.comp (primrec_v2.comp Primrec.snd) (primrec_v3.comp Primrec.snd)).pair (primrec_a4.comp Primrec.snd)) (Primrec.const [])) (Primrec.const [])))

theorem primrec_checkStepCode : Primrec (fun p : Nat × Nat × Nat => checkStepCode p.1 p.2.1 p.2.2) :=
  (primrec_evaluate primrec_stepShape primrec_stepChildren).comp
    ((Primrec₂.natPair.comp (Primrec.fst.comp Primrec.snd) (Primrec.snd.comp Primrec.snd)).pair Primrec.fst)

theorem eval_step (a b c : Nat) : evaluate stepShape stepChildren (Nat.pair a b,c) = checkStepCode c a b := rfl

end AuxiliaryCodeComputability
