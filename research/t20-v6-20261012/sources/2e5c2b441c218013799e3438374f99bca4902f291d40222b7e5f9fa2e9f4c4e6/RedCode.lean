import StepExact
namespace AuxiliaryCodeComputability
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity
open AuxiliaryCertificates OrthemologyV2 OrthemologyV3 P01D
set_option maxRecDepth 8192
set_option maxHeartbeats 200000
attribute [local irreducible] Nat.pair checkStepCode

@[simp] theorem encode_red_refl (t : Term) : encode (.refl t : RedCert) = pack 0 [leaf (encode t)] := rfl

@[simp] theorem encode_red_tail (t u v : Term) (s : StepCert) (r : RedCert) : encode (.tail t u v s r : RedCert) = pack 1 [leaf (encode t), leaf (encode u), leaf (encode v), leaf (encode s), encode r] := rfl

def redShape (s : Nat × Nat) : Bool :=
  if tag s.2 = 0 then (decide (lhs s = v1 s.2) && decide (rhs s = v1 s.2))
  else if tag s.2 = 1 then ((decide (lhs s = v1 s.2) && decide (rhs s = v3 s.2)) && checkStepCode (v4 s.2) (v1 s.2) (v2 s.2))
  else false

def redChildren (s : Nat × Nat) : List (Nat × Nat) :=
  if tag s.2 = 1 then [(Nat.pair (v2 s.2) (v3 s.2), a5 s.2)]
  else []

def checkRedCode (c a b : Nat) : Bool := evaluate redShape redChildren (Nat.pair a b,c)

theorem primrec_redShape : Primrec redShape := by
  have h4 : Primrec (fun s : Nat × Nat => v4 s.2) := primrec_v4.comp Primrec.snd
  have h1 : Primrec (fun s : Nat × Nat => v1 s.2) := primrec_v1.comp Primrec.snd
  have h2 : Primrec (fun s : Nat × Nat => v2 s.2) := primrec_v2.comp Primrec.snd
  have hi : Primrec (fun s : Nat × Nat => (v4 s.2,(v1 s.2,v2 s.2))) := h4.pair (h1.pair h2)
  have hs0 := primrec_checkStepCode.comp hi
  have hs : Primrec (fun s : Nat × Nat => checkStepCode (v4 s.2) (v1 s.2) (v2 s.2)) := hs0.of_eq (by intro s; dsimp only)
  have h := (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 0)) (Primrec.and.comp (Primrec.eq.comp primrec_lhs (primrec_v1.comp Primrec.snd)) (Primrec.eq.comp primrec_rhs (primrec_v1.comp Primrec.snd))) (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 1)) (Primrec.and.comp (Primrec.and.comp (Primrec.eq.comp primrec_lhs (primrec_v1.comp Primrec.snd)) (Primrec.eq.comp primrec_rhs (primrec_v3.comp Primrec.snd))) hs) (Primrec.const false)))
  exact h.of_eq (by intro s; dsimp only [redShape])

theorem primrec_redChildren : Primrec redChildren :=
  (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 1)) (Primrec.list_cons.comp ((Primrec₂.natPair.comp (primrec_v2.comp Primrec.snd) (primrec_v3.comp Primrec.snd)).pair (primrec_a5.comp Primrec.snd)) (Primrec.const [])) (Primrec.const []))

theorem primrec_checkRedCode : Primrec (fun p : Nat × Nat × Nat => checkRedCode p.1 p.2.1 p.2.2) :=
  (primrec_evaluate primrec_redShape primrec_redChildren).comp
    ((Primrec₂.natPair.comp (Primrec.fst.comp Primrec.snd) (Primrec.snd.comp Primrec.snd)).pair Primrec.fst)

theorem eval_red (a b c : Nat) : evaluate redShape redChildren (Nat.pair a b,c) = checkRedCode c a b := rfl

end AuxiliaryCodeComputability
