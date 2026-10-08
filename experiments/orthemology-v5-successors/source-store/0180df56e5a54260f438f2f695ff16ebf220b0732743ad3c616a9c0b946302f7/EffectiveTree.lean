import Mathlib.Computability.PartrecCode

/-!
An actual primitive-recursive binary tree with uniform finite plans and no
computable infinite path. Bounded evaluation uses Mathlib's fuel/value bound;
it is not asserted to count literal Turing-machine steps.
-/

namespace EffectiveRenewal

open Nat.Partrec (Code)
open Encodable Denumerable

abbrev Word := List Bool

def bitNat (b : Bool) : Nat := if b then 1 else 0

def prefixWord (f : Nat → Bool) (n : Nat) : Word := (List.range n).map f

def diagonal (bound index : Nat) : Option Nat :=
  Code.evaln bound (ofNat Code index) index

def coordinateOK (s : Word) (e : Nat) : Bool :=
  (diagonal s.length e != some 0 || s.getD e false) &&
  (diagonal s.length e != some 1 || !(s.getD e false))

def treeCheck (s : Word) : Bool :=
  ((List.range s.length).map (coordinateOK s)).foldr Bool.and true

def diagonalTree (s : Word) : Prop := treeCheck s = true

def finitePlan (n : Nat) : Word :=
  (List.range n).map fun e => decide (diagonal n e = some 0)

@[simp] theorem length_prefixWord (f : Nat → Bool) (n : Nat) :
    (prefixWord f n).length = n := by simp [prefixWord]

@[simp] theorem getD_prefixWord (f : Nat → Bool) {n e : Nat} (he : e < n) :
    (prefixWord f n).getD e false = f e := by
  simp [prefixWord, List.getD_eq_getElem?_getD, List.getElem?_range he]

@[simp] theorem length_finitePlan (n : Nat) : (finitePlan n).length = n := by
  simp [finitePlan]

@[simp] theorem getD_finitePlan {n e : Nat} (he : e < n) :
    (finitePlan n).getD e false = decide (diagonal n e = some 0) := by
  simp [finitePlan, List.getD_eq_getElem?_getD, List.getElem?_range he]

private theorem foldr_and_true (bs : List Bool) :
    bs.foldr Bool.and true = true ↔ ∀ b ∈ bs, b = true := by
  induction bs with
  | nil => simp
  | cons b bs ih => simp [ih]

theorem diagonalTree_iff (s : Word) : diagonalTree s ↔
    ∀ e < s.length,
      (diagonal s.length e = some 0 → s.getD e false = true) ∧
      (diagonal s.length e = some 1 → s.getD e false = false) := by
  simp [diagonalTree, treeCheck, foldr_and_true, coordinateOK, ← imp_iff_not_or]

instance : DecidablePred diagonalTree := fun s => inferInstanceAs (Decidable (treeCheck s = true))

@[simp] theorem diagonalTree_empty : diagonalTree [] := by
  simp [diagonalTree_iff]

theorem diagonal_mono {n m e v : Nat} (h : n ≤ m)
    (hv : diagonal n e = some v) : diagonal m e = some v :=
  Code.evaln_mono h hv

theorem diagonalTree_prefix_closed {s t : Word} (hpre : s <+: t)
    (ht : diagonalTree t) : diagonalTree s := by
  rw [diagonalTree_iff] at ht ⊢
  intro e he
  have het : e < t.length := lt_of_lt_of_le he hpre.length_le
  have hget : s.getD e false = t.getD e false := by
    simp only [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem he,
      List.getElem?_eq_getElem het, Option.getD_some]
    exact hpre.getElem he
  constructor
  · intro h
    rw [hget]
    exact (ht e het).1 (diagonal_mono hpre.length_le h)
  · intro h
    rw [hget]
    exact (ht e het).2 (diagonal_mono hpre.length_le h)

theorem finitePlan_admitted (n : Nat) : diagonalTree (finitePlan n) := by
  rw [diagonalTree_iff]
  simp only [length_finitePlan]
  intro e he
  rw [getD_finitePlan he]
  constructor
  · intro h; simp [h]
  · intro h; simp [h]

theorem finitePlan_prefix_admitted (n m : Nat) : diagonalTree ((finitePlan n).take m) :=
  diagonalTree_prefix_closed (List.take_prefix _ _) (finitePlan_admitted n)

theorem diagonal_primrec : Primrec₂ diagonal := by
  exact Code.evaln_prim.comp ((Primrec.fst.pair ((Primrec.ofNat Code).comp Primrec.snd)).pair Primrec.snd)

theorem finitePlan_primrec : Primrec finitePlan := by
  exact Primrec.list_map Primrec.list_range
    ((Primrec.eq.comp diagonal_primrec (Primrec.const (some 0))).to₂)

theorem coordinateOK_primrec : Primrec₂ coordinateOK := by
  have hd : Primrec fun p : Word × Nat => diagonal p.1.length p.2 :=
    diagonal_primrec.comp (Primrec.list_length.comp Primrec.fst) Primrec.snd
  have hb : Primrec fun p : Word × Nat => p.1.getD p.2 false :=
    Primrec.list_getD false
  exact (Primrec.and.comp
    (Primrec.or.comp (Primrec.not.comp (Primrec.beq.comp hd (Primrec.const (some 0)))) hb)
    (Primrec.or.comp (Primrec.not.comp (Primrec.beq.comp hd (Primrec.const (some 1))))
      (Primrec.not.comp hb))).of_eq fun p => by
      apply Bool.eq_iff_iff.mpr
      simp [coordinateOK, bne]

theorem treeCheck_primrec : Primrec treeCheck := by
  exact Primrec.list_foldr
    (Primrec.list_map (Primrec.list_range.comp Primrec.list_length) coordinateOK_primrec)
    (Primrec.const true)
    (Primrec.and.comp (Primrec.fst.comp Primrec.snd) (Primrec.snd.comp Primrec.snd)).to₂

theorem bitNat_primrec : Primrec bitNat :=
  (Primrec.cond Primrec.id (Primrec.const 1) (Primrec.const 0)).of_eq
    fun b => by cases b <;> rfl

theorem exists_mathematical_path :
    ∃ f : Nat → Bool, ∀ n, diagonalTree (prefixWord f n) := by
  classical
  let f : Nat → Bool := fun e => decide (0 ∈ Code.eval (ofNat Code e) e)
  refine ⟨f, ?_⟩
  intro n
  rw [diagonalTree_iff]
  simp only [length_prefixWord]
  intro e he
  rw [getD_prefixWord f he]
  constructor
  · intro h
    have hz : 0 ∈ Code.eval (ofNat Code e) e := Code.evaln_sound h
    simp [f, hz]
  · intro h
    have ho : 1 ∈ Code.eval (ofNat Code e) e := Code.evaln_sound h
    have hz : ¬ 0 ∈ Code.eval (ofNat Code e) e := by
      intro hz
      have : (0 : Nat) = 1 := Part.mem_unique hz ho
      omega
    simp [f, hz]

theorem no_computable_path (f : Nat → Bool) (hf : Computable f) :
    ¬ ∀ n, diagonalTree (prefixWord f n) := by
  intro hpath
  have hb : Computable fun e => bitNat (f e) := bitNat_primrec.to_comp.comp hf
  obtain ⟨c, hc⟩ := Code.exists_code.mp (Partrec.nat_iff.mp hb.partrec)
  let e : Nat := encode c
  have hev : bitNat (f e) ∈ Code.eval (ofNat Code e) e := by
    simp only [e, ofNat_encode]
    rw [hc]
    exact Part.mem_some _
  obtain ⟨k, hk⟩ := Code.evaln_complete.mp hev
  let n := max (e + 1) k
  have he : e < n := lt_of_lt_of_le (Nat.lt_succ_self e) (Nat.le_max_left _ _)
  have hk' : diagonal n e = some (bitNat (f e)) :=
    Code.evaln_mono (Nat.le_max_right _ _) hk
  have hp := (diagonalTree_iff _).mp (hpath n) e (by simpa using he)
  simp only [length_prefixWord, getD_prefixWord f he] at hp
  cases hbit : f e with
  | false =>
    have := hp.1 (by simpa [hbit, bitNat] using hk')
    simp [hbit] at this
  | true =>
    have := hp.2 (by simpa [hbit, bitNat] using hk')
    simp [hbit] at this

end EffectiveRenewal
