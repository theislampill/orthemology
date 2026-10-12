import AuxiliaryCodeCore
namespace AuxiliaryCodeComputability
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity
open AuxiliaryCertificates OrthemologyV2 P01D
set_option maxRecDepth 8192
set_option maxHeartbeats 200000
attribute [local irreducible] Nat.pair

@[simp] theorem encode_poly_refl (p : Poly) : encode (.refl p : PolyCert) = pack 0 [leaf (encode p)] := rfl

@[simp] theorem encode_poly_symm (p q : Poly) (c : PolyCert) : encode (.symm p q c : PolyCert) = pack 1 [leaf (encode p), leaf (encode q), encode c] := rfl

@[simp] theorem encode_poly_trans (p q r : Poly) (c d : PolyCert) : encode (.trans p q r c d : PolyCert) = pack 2 [leaf (encode p), leaf (encode q), leaf (encode r), encode c, encode d] := rfl

@[simp] theorem encode_poly_app (f g p q : Poly) (c d : PolyCert) : encode (.app f g p q c d : PolyCert) = pack 3 [leaf (encode f), leaf (encode g), leaf (encode p), leaf (encode q), encode c, encode d] := rfl

@[simp] theorem encode_poly_i (p : Poly) : encode (.i p : PolyCert) = pack 4 [leaf (encode p)] := rfl

@[simp] theorem encode_poly_k (p q : Poly) : encode (.k p q : PolyCert) = pack 5 [leaf (encode p), leaf (encode q)] := rfl

@[simp] theorem encode_poly_s (p q r : Poly) : encode (.s p q r : PolyCert) = pack 6 [leaf (encode p), leaf (encode q), leaf (encode r)] := rfl

@[simp] theorem encode_poly_bridge (r t : Term) : encode (.bridge r t : PolyCert) = pack 7 [leaf (encode r), leaf (encode t)] := rfl

def polyShape (s : Nat × Nat) : Bool :=
  if tag s.2 = 0 then (decide (lhs s = v1 s.2) && decide (rhs s = v1 s.2))
  else if tag s.2 = 1 then (decide (lhs s = v2 s.2) && decide (rhs s = v1 s.2))
  else if tag s.2 = 2 then (decide (lhs s = v1 s.2) && decide (rhs s = v3 s.2))
  else if tag s.2 = 3 then (decide (lhs s = polyApp (v1 s.2) (v3 s.2)) && decide (rhs s = polyApp (v2 s.2) (v4 s.2)))
  else if tag s.2 = 4 then (decide (lhs s = polyApp (polyAtom (encode Term.i)) (v1 s.2)) && decide (rhs s = v1 s.2))
  else if tag s.2 = 5 then (decide (lhs s = polyApp (polyApp (polyAtom (encode Term.k)) (v1 s.2)) (v2 s.2)) && decide (rhs s = v1 s.2))
  else if tag s.2 = 6 then (decide (lhs s = polyApp (polyApp (polyApp (polyAtom (encode Term.s)) (v1 s.2)) (v2 s.2)) (v3 s.2)) && decide (rhs s = polyApp (polyApp (v1 s.2) (v3 s.2)) (polyApp (v2 s.2) (v3 s.2))))
  else if tag s.2 = 7 then (decide (lhs s = polyAtom (tmApp (v1 s.2) (v2 s.2))) && decide (rhs s = polyApp (polyAtom (v1 s.2)) (polyAtom (v2 s.2))))
  else false

def polyChildren (s : Nat × Nat) : List (Nat × Nat) :=
  if tag s.2 = 1 then [(Nat.pair (v1 s.2) (v2 s.2), a3 s.2)]
  else if tag s.2 = 2 then [(Nat.pair (v1 s.2) (v2 s.2), a4 s.2), (Nat.pair (v2 s.2) (v3 s.2), a5 s.2)]
  else if tag s.2 = 3 then [(Nat.pair (v1 s.2) (v2 s.2), a5 s.2), (Nat.pair (v3 s.2) (v4 s.2), a6 s.2)]
  else []

def checkPolyCode (c a b : Nat) : Bool := evaluate polyShape polyChildren (Nat.pair a b,c)

theorem primrec_polyShape : Primrec polyShape :=
  (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 0)) (Primrec.and.comp (Primrec.eq.comp primrec_lhs (primrec_v1.comp Primrec.snd)) (Primrec.eq.comp primrec_rhs (primrec_v1.comp Primrec.snd))) (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 1)) (Primrec.and.comp (Primrec.eq.comp primrec_lhs (primrec_v2.comp Primrec.snd)) (Primrec.eq.comp primrec_rhs (primrec_v1.comp Primrec.snd))) (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 2)) (Primrec.and.comp (Primrec.eq.comp primrec_lhs (primrec_v1.comp Primrec.snd)) (Primrec.eq.comp primrec_rhs (primrec_v3.comp Primrec.snd))) (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 3)) (Primrec.and.comp (Primrec.eq.comp primrec_lhs (primrec_polyApp.comp (primrec_v1.comp Primrec.snd) (primrec_v3.comp Primrec.snd))) (Primrec.eq.comp primrec_rhs (primrec_polyApp.comp (primrec_v2.comp Primrec.snd) (primrec_v4.comp Primrec.snd)))) (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 4)) (Primrec.and.comp (Primrec.eq.comp primrec_lhs (primrec_polyApp.comp (primrec_polyAtom.comp (Primrec.const _)) (primrec_v1.comp Primrec.snd))) (Primrec.eq.comp primrec_rhs (primrec_v1.comp Primrec.snd))) (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 5)) (Primrec.and.comp (Primrec.eq.comp primrec_lhs (primrec_polyApp.comp (primrec_polyApp.comp (primrec_polyAtom.comp (Primrec.const _)) (primrec_v1.comp Primrec.snd)) (primrec_v2.comp Primrec.snd))) (Primrec.eq.comp primrec_rhs (primrec_v1.comp Primrec.snd))) (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 6)) (Primrec.and.comp (Primrec.eq.comp primrec_lhs (primrec_polyApp.comp (primrec_polyApp.comp (primrec_polyApp.comp (primrec_polyAtom.comp (Primrec.const _)) (primrec_v1.comp Primrec.snd)) (primrec_v2.comp Primrec.snd)) (primrec_v3.comp Primrec.snd))) (Primrec.eq.comp primrec_rhs (primrec_polyApp.comp (primrec_polyApp.comp (primrec_v1.comp Primrec.snd) (primrec_v3.comp Primrec.snd)) (primrec_polyApp.comp (primrec_v2.comp Primrec.snd) (primrec_v3.comp Primrec.snd))))) (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 7)) (Primrec.and.comp (Primrec.eq.comp primrec_lhs (primrec_polyAtom.comp (primrec_tmApp.comp (primrec_v1.comp Primrec.snd) (primrec_v2.comp Primrec.snd)))) (Primrec.eq.comp primrec_rhs (primrec_polyApp.comp (primrec_polyAtom.comp (primrec_v1.comp Primrec.snd)) (primrec_polyAtom.comp (primrec_v2.comp Primrec.snd))))) (Primrec.const false)))))))))

theorem primrec_polyChildren : Primrec polyChildren :=
  (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 1)) (Primrec.list_cons.comp ((Primrec₂.natPair.comp (primrec_v1.comp Primrec.snd) (primrec_v2.comp Primrec.snd)).pair (primrec_a3.comp Primrec.snd)) (Primrec.const [])) (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 2)) (Primrec.list_cons.comp ((Primrec₂.natPair.comp (primrec_v1.comp Primrec.snd) (primrec_v2.comp Primrec.snd)).pair (primrec_a4.comp Primrec.snd)) (Primrec.list_cons.comp ((Primrec₂.natPair.comp (primrec_v2.comp Primrec.snd) (primrec_v3.comp Primrec.snd)).pair (primrec_a5.comp Primrec.snd)) (Primrec.const []))) (Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 3)) (Primrec.list_cons.comp ((Primrec₂.natPair.comp (primrec_v1.comp Primrec.snd) (primrec_v2.comp Primrec.snd)).pair (primrec_a5.comp Primrec.snd)) (Primrec.list_cons.comp ((Primrec₂.natPair.comp (primrec_v3.comp Primrec.snd) (primrec_v4.comp Primrec.snd)).pair (primrec_a6.comp Primrec.snd)) (Primrec.const []))) (Primrec.const []))))

theorem primrec_checkPolyCode : Primrec (fun p : Nat × Nat × Nat => checkPolyCode p.1 p.2.1 p.2.2) :=
  (primrec_evaluate primrec_polyShape primrec_polyChildren).comp
    ((Primrec₂.natPair.comp (Primrec.fst.comp Primrec.snd) (Primrec.snd.comp Primrec.snd)).pair Primrec.fst)

theorem eval_poly (a b c : Nat) : evaluate polyShape polyChildren (Nat.pair a b,c) = checkPolyCode c a b := rfl

end AuxiliaryCodeComputability
