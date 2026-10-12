import FiniteExact
import TermTypeSubstitution
import EncodedCertificatePayloads
namespace AuxiliaryCodeComputability
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity CodedPolyTransformations
open AuxiliaryCertificates OrthemologyV2 OrthemologyV3 P01D P01AC
set_option maxRecDepth 8192
set_option maxHeartbeats 200000
attribute [local irreducible] Nat.pair wkTyCode

@[simp] theorem encode_lookup_zero (Γ : Tel) (A : Ty) :
    encode (LookupCert.zero Γ A) = pack 0 [leaf (encode Γ), leaf (encode A)] := rfl
@[simp] theorem encode_lookup_succ (Γ : Tel) (n : Nat) (A B : Ty) (c : LookupCert) :
    encode (LookupCert.succ Γ n A B c) =
      pack 1 [leaf (encode Γ), leaf n, leaf (encode A), leaf (encode B), encode c] := rfl

def telCons (A Γ : Nat) := (Nat.pair A Γ).succ
def lookupIndex (s : Nat × Nat) := (rhs s).unpair.1
def lookupType (s : Nat × Nat) := (rhs s).unpair.2

theorem primrec_telCons : Primrec₂ telCons := Primrec.succ.comp₂ Primrec₂.natPair
theorem primrec_lookupIndex : Primrec lookupIndex := Primrec.fst.comp (Primrec.unpair.comp primrec_rhs)
theorem primrec_lookupType : Primrec lookupType := Primrec.snd.comp (Primrec.unpair.comp primrec_rhs)

@[simp] theorem telCons_exact (A : Ty) (Γ : Tel) : telCons (encode A) (encode Γ) = encode (A :: Γ) := (encode_list_cons _ _).symm
@[simp] theorem lookupIndex_pair (a n b c : Nat) : lookupIndex (Nat.pair a (Nat.pair n b),c) = n := by simp [lookupIndex]
@[simp] theorem lookupType_pair (a n b c : Nat) : lookupType (Nat.pair a (Nat.pair n b),c) = b := by simp [lookupType]

def lookupShape (s : Nat × Nat) : Bool :=
  if tag s.2 = 0 then
    decide (lhs s = telCons (v2 s.2) (v1 s.2)) && decide (lookupIndex s = 0) &&
      decide (lookupType s = wkTyCode (v2 s.2))
  else if tag s.2 = 1 then
    decide (lhs s = telCons (v4 s.2) (v1 s.2)) && decide (lookupIndex s = (v2 s.2).succ) &&
      decide (lookupType s = wkTyCode (v3 s.2))
  else false

def lookupChildren (s : Nat × Nat) : List (Nat × Nat) :=
  if tag s.2 = 1 then [(Nat.pair (v1 s.2) (Nat.pair (v2 s.2) (v3 s.2)),a5 s.2)] else []

def checkLookupCode (c Γ n A : Nat) := evaluate lookupShape lookupChildren (Nat.pair Γ (Nat.pair n A),c)

theorem primrec_lookupShape : Primrec lookupShape := by
  have h1 := primrec_v1.comp (Primrec.snd : Primrec (fun s : Nat × Nat => s.2))
  have h2 := primrec_v2.comp (Primrec.snd : Primrec (fun s : Nat × Nat => s.2))
  have h3 := primrec_v3.comp (Primrec.snd : Primrec (fun s : Nat × Nat => s.2))
  have h4 := primrec_v4.comp (Primrec.snd : Primrec (fun s : Nat × Nat => s.2))
  have hz := Primrec.and.comp
    (Primrec.and.comp (Primrec.eq.comp primrec_lhs (primrec_telCons.comp h2 h1))
      (Primrec.eq.comp primrec_lookupIndex (Primrec.const 0)))
    (Primrec.eq.comp primrec_lookupType (primrec_wkTyCode.comp h2))
  have hs := Primrec.and.comp
    (Primrec.and.comp (Primrec.eq.comp primrec_lhs (primrec_telCons.comp h4 h1))
      (Primrec.eq.comp primrec_lookupIndex (Primrec.succ.comp h2)))
    (Primrec.eq.comp primrec_lookupType (primrec_wkTyCode.comp h3))
  have ht := primrec_tag.comp (Primrec.snd : Primrec (fun s : Nat × Nat => s.2))
  have h := Primrec.ite (Primrec.eq.comp ht (.const 0)) hz
    (Primrec.ite (Primrec.eq.comp ht (.const 1)) hs (.const false))
  exact h.of_eq (by intro s; dsimp only [lookupShape])

theorem primrec_lookupChildren : Primrec lookupChildren :=
  Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const 1))
    (Primrec.list_cons.comp
      ((Primrec₂.natPair.comp (primrec_v1.comp Primrec.snd)
        (Primrec₂.natPair.comp (primrec_v2.comp Primrec.snd) (primrec_v3.comp Primrec.snd))).pair
        (primrec_a5.comp Primrec.snd)) (.const [])) (.const [])

theorem primrec_checkLookupCode :
    Primrec (fun p : Nat × Nat × Nat × Nat => checkLookupCode p.1 p.2.1 p.2.2.1 p.2.2.2) :=
  (primrec_evaluate primrec_lookupShape primrec_lookupChildren).comp
    ((Primrec₂.natPair.comp (Primrec.fst.comp Primrec.snd)
      (Primrec₂.natPair.comp (Primrec.fst.comp (Primrec.snd.comp Primrec.snd))
        (Primrec.snd.comp (Primrec.snd.comp Primrec.snd)))).pair Primrec.fst)

theorem eval_lookup (Γ n A c : Nat) : evaluate lookupShape lookupChildren (Nat.pair Γ (Nat.pair n A),c) = checkLookupCode c Γ n A := rfl

theorem checkLookupCode_exact (c : LookupCert) (Δ : Tel) (k : Nat) (C : Ty) :
    checkLookupCode (encode c) (encode Δ) k (encode C) = checkLookup c Δ k C := by
  induction c generalizing Δ k C with
  | zero Γ A =>
    rw [checkLookupCode,evaluate]
    simp only [encode_lookup_zero,lookupShape,lookupChildren,pack,List.foldr_cons,List.foldr_nil,
      a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,
      unpair_leaf,lhs_pair,lookupIndex_pair,lookupType_pair,telCons_exact,wkTyCode_exact,
      encode_injective.eq_iff,checkLookup]
    simp [Bool.and_assoc]
  | succ Γ n A B c ih =>
    have hc : encode c < encode (LookupCert.succ Γ n A B c) := by
      rw [encode_lookup_succ]; exact field_lt_pack _ _ (by simp)
    rw [checkLookupCode,evaluate]
    simp only [encode_lookup_succ,lookupShape,lookupChildren,pack,List.foldr_cons,List.foldr_nil,
      a1,a2,a3,a4,a5,a6,v1,v2,v3,v4,v5,v6,tag,arg1,arg2,arg3,first_node,rest_node,rest_leaf,
      unpair_leaf,lhs_pair,lookupIndex_pair,lookupType_pair,telCons_exact,wkTyCode_exact,
      encode_injective.eq_iff,checkLookup]
    simp only [encode_lookup_succ,pack,List.foldr_cons,List.foldr_nil] at hc
    simp [hc,eval_lookup,ih,Bool.and_assoc]

#print axioms primrec_checkLookupCode
#print axioms checkLookupCode_exact
end AuxiliaryCodeComputability
