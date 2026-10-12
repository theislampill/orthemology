/-
Finite-tree/natural codec adapted from Mathlib.Tactic.DeriveEncodable.
Copyright (c) 2024 Kyle Miller. Released under Apache 2.0; see vendor/LICENSE.
Explicit PolyCert encoder, decoder, and kernel-checked standalone roundtrip.
-/
import EncodedCertificateSyntax
namespace JointCertificates.PolyEncoding
open P01D OrthemologyV2 AuxiliaryCertificates
set_option maxRecDepth 32768
set_option maxHeartbeats 32000000

inductive Tree : Type where
  | nat (n : ℕ)
  | cons (a b : Tree)

private def Tree.encode : Tree → ℕ
  | nat n => Nat.pair 0 n
  | cons a b => Nat.pair (Tree.encode a + 1) (Tree.encode b)

private lemma nat_unpair_lt_2 {n : ℕ} (h : (Nat.unpair n).1 ≠ 0) : (Nat.unpair n).2 < n := by
  obtain ⟨⟨a, b⟩, rfl⟩ := Nat.pairEquiv.surjective n
  simp only [Nat.pairEquiv_apply, Function.uncurry_apply_pair, Nat.unpair_pair] at *
  unfold Nat.pair
  have := Nat.le_mul_self a
  have := Nat.le_mul_self b
  split <;> omega

private def Tree.decode (n : ℕ) : Tree :=
  let p := Nat.unpair n
  if h : p.1 = 0 then
    Tree.nat p.2
  else
    have : p.1 ≤ n := Nat.unpair_left_le n
    have := Nat.unpair_lt (by omega : 1 ≤ n)
    have := nat_unpair_lt_2 h
    Tree.cons (Tree.decode (p.1 - 1)) (Tree.decode p.2)

private def treeEquiv : Tree ≃ ℕ where
  toFun := Tree.encode
  invFun := Tree.decode
  left_inv s := by
    induction s with
    | nat n =>
      unfold Tree.encode Tree.decode
      simp
    | cons a b iha ihb =>
      unfold Tree.encode Tree.decode
      simp [iha, ihb]
  right_inv n := by -- The fact it's a right inverse isn't needed for the deriving handler.
    induction n using Nat.strongRecOn with | _ n ih =>
    unfold Tree.decode
    dsimp only
    split
    next h =>
      unfold Tree.encode
      rw [← h, Nat.pair_unpair]
    next h =>
      unfold Tree.encode
      rw [ih, ih, Nat.sub_add_cancel, Nat.pair_unpair]
      · rwa [Nat.one_le_iff_ne_zero]
      · exact nat_unpair_lt_2 h
      · obtain _ | n' := n
        · exact False.elim (h rfl)
        · have := Nat.unpair_lt (by omega : 1 ≤ n' + 1)
          omega

instance : Encodable Tree := Encodable.ofEquiv ℕ treeEquiv


def toTree : PolyCert → Tree
  | .refl p => .cons (.nat 0) (.cons (.nat (Encodable.encode p)) (.nat 0))
  | .symm p q c => .cons (.nat 1) (.cons (.nat (Encodable.encode p)) (.cons (.nat (Encodable.encode q)) (.cons (toTree c) (.nat 0))))
  | .trans p q r c d => .cons (.nat 2) (.cons (.nat (Encodable.encode p)) (.cons (.nat (Encodable.encode q)) (.cons (.nat (Encodable.encode r)) (.cons (toTree c) (.cons (toTree d) (.nat 0))))))
  | .app f g p q c d => .cons (.nat 3) (.cons (.nat (Encodable.encode f)) (.cons (.nat (Encodable.encode g)) (.cons (.nat (Encodable.encode p)) (.cons (.nat (Encodable.encode q)) (.cons (toTree c) (.cons (toTree d) (.nat 0)))))))
  | .i p => .cons (.nat 4) (.cons (.nat (Encodable.encode p)) (.nat 0))
  | .k p q => .cons (.nat 5) (.cons (.nat (Encodable.encode p)) (.cons (.nat (Encodable.encode q)) (.nat 0)))
  | .s p q r => .cons (.nat 6) (.cons (.nat (Encodable.encode p)) (.cons (.nat (Encodable.encode q)) (.cons (.nat (Encodable.encode r)) (.nat 0))))
  | .bridge r t => .cons (.nat 7) (.cons (.nat (Encodable.encode r)) (.cons (.nat (Encodable.encode t)) (.nat 0)))

def fromTree (tree : Tree) : Option PolyCert :=
  match tree with
  | .cons (.nat tag) payload =>
    match tag with
    | 0 => match payload with
      | (.cons (.nat p) (.nat 0)) => do
          let p ← Encodable.decode (α := Poly) p
          pure (.refl p)
      | _ => none
    | 1 => match payload with
      | (.cons (.nat p) (.cons (.nat q) (.cons c (.nat 0)))) => do
          let p ← Encodable.decode (α := Poly) p
          let q ← Encodable.decode (α := Poly) q
          let c ← fromTree c
          pure (.symm p q c)
      | _ => none
    | 2 => match payload with
      | (.cons (.nat p) (.cons (.nat q) (.cons (.nat r) (.cons c (.cons d (.nat 0)))))) => do
          let p ← Encodable.decode (α := Poly) p
          let q ← Encodable.decode (α := Poly) q
          let r ← Encodable.decode (α := Poly) r
          let c ← fromTree c
          let d ← fromTree d
          pure (.trans p q r c d)
      | _ => none
    | 3 => match payload with
      | (.cons (.nat f) (.cons (.nat g) (.cons (.nat p) (.cons (.nat q) (.cons c (.cons d (.nat 0))))))) => do
          let f ← Encodable.decode (α := Poly) f
          let g ← Encodable.decode (α := Poly) g
          let p ← Encodable.decode (α := Poly) p
          let q ← Encodable.decode (α := Poly) q
          let c ← fromTree c
          let d ← fromTree d
          pure (.app f g p q c d)
      | _ => none
    | 4 => match payload with
      | (.cons (.nat p) (.nat 0)) => do
          let p ← Encodable.decode (α := Poly) p
          pure (.i p)
      | _ => none
    | 5 => match payload with
      | (.cons (.nat p) (.cons (.nat q) (.nat 0))) => do
          let p ← Encodable.decode (α := Poly) p
          let q ← Encodable.decode (α := Poly) q
          pure (.k p q)
      | _ => none
    | 6 => match payload with
      | (.cons (.nat p) (.cons (.nat q) (.cons (.nat r) (.nat 0)))) => do
          let p ← Encodable.decode (α := Poly) p
          let q ← Encodable.decode (α := Poly) q
          let r ← Encodable.decode (α := Poly) r
          pure (.s p q r)
      | _ => none
    | 7 => match payload with
      | (.cons (.nat r) (.cons (.nat t) (.nat 0))) => do
          let r ← Encodable.decode (α := Term) r
          let t ← Encodable.decode (α := Term) t
          pure (.bridge r t)
      | _ => none
    | _ => none
  | _ => none
termination_by sizeOf tree
decreasing_by all_goals (simp_wf; omega)

theorem fromTree_toTree (c : PolyCert) : fromTree (toTree c) = some c := by
  induction c <;> simp_all only [toTree, fromTree, Encodable.encodek, Option.bind_some, pure]
  all_goals rfl

instance : Encodable PolyCert := Encodable.ofLeftInjection toTree fromTree fromTree_toTree

#print axioms fromTree_toTree
end JointCertificates.PolyEncoding
