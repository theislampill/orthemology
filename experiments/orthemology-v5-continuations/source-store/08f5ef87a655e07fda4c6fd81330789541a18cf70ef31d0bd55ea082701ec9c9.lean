import CodecNumeric
import Mathlib.Computability.Primrec

/-!
# Primitive-recursive byte/numeric serialization components

The executable encoders remain the exact definitions in `CodecVarint` and
`CodecNumeric`. Here they receive Mathlib `Primrec` proofs, with Mathlib's
standard `Primcodable` representation for finite lists.

`uv_primrec` uses primitive-recursive course-of-values recursion: a finite
list stores all previously computed encodings, and at stage n the encoder
reads entry n/128. This is a termination/definability argument, not an efficient
implementation claim. `encodeNumeric_primrec` follows from a byte-list fold.

These results certify numeric serialization functions only. They do not assert
that a universal evaluator indexed by arbitrary program codes is primitive
recursive, nor do they give a uniform bound on evaluation of such programs.
-/

namespace P02.Codec

/-- The next varint encoding computed from the finite table of earlier values. -/
def uvTableStep (table : List (List Nat)) : Option (List Nat) :=
  let n := table.length
  if n < 128 then some [n]
  else (table[n / 128]?).map (fun tail => (n % 128 + 128) :: tail)

theorem uvTableStep_primrec : Primrec uvTableStep := by
  have hlen : Primrec (fun table : List (List Nat) => table.length) := Primrec.list_length
  have hquot : Primrec (fun table : List (List Nat) => table.length / 128) :=
    Primrec.nat_div.comp hlen (Primrec.const 128)
  have hbyte : Primrec (fun table : List (List Nat) => table.length % 128 + 128) :=
    Primrec.nat_add.comp (Primrec.nat_mod.comp hlen (Primrec.const 128)) (Primrec.const 128)
  have hget : Primrec (fun table : List (List Nat) => table[table.length / 128]?) :=
    Primrec.list_getElem?.comp Primrec.id hquot
  have hcons : Primrec₂ (fun (table : List (List Nat)) (tail : List Nat) =>
      (table.length % 128 + 128) :: tail) :=
    (Primrec.list_cons.comp (hbyte.comp Primrec.fst) Primrec.snd).to₂
  exact Primrec.ite (Primrec.nat_lt.comp hlen (Primrec.const 128))
    (Primrec.option_some.comp (Primrec.list_cons.comp hlen (Primrec.const [])))
    (Primrec.option_map hget hcons)

/-- The course-of-values table step computes the exact bitwise serializer. -/
theorem uvTableStep_table (n : Nat) :
    uvTableStep ((List.range n).map uv) = some (uv n) := by
  simp only [uvTableStep, List.length_map, List.length_range]
  by_cases hn : n < 128
  · rw [if_pos hn, uv, dif_pos hn]
  · have hd : n / 128 < n := Nat.div_lt_self (by omega) (by omega)
    rw [if_neg hn, List.getElem?_map, List.getElem?_range hd]
    rw [uv, dif_neg hn, continuation_byte]
    rfl

/-- The exact canonical unsigned LEB128 encoder is primitive recursive. -/
theorem uv_primrec : Primrec uv := by
  have hs : Primrec₂ (fun (_ : Unit) n => uv n) :=
    Primrec.nat_strong_rec (fun (_ : Unit) n => uv n)
      ((uvTableStep_primrec.comp Primrec.snd).to₂)
      (fun _ n => uvTableStep_table n)
  exact hs.comp (Primrec.const ()) Primrec.id

/-- Big-endian conversion is primitive recursive on arbitrary natural lists. -/
theorem fromBytes_primrec : Primrec fromBytes := by
  have hs : Primrec₂ (fun (_ : List Nat) (p : Nat × Nat) => 256 * p.1 + p.2) :=
    (Primrec.nat_add.comp
      (Primrec.nat_mul.comp (Primrec.const 256) (Primrec.fst.comp Primrec.snd))
      (Primrec.snd.comp Primrec.snd)).to₂
  exact Primrec.list_foldl Primrec.id (Primrec.const 0) hs

/-- The sentinel-prefixed numeric index is primitive recursive on byte lists.
The function itself is total on all natural lists; roundtrip requires `Bytes`. -/
theorem encodeNumeric_primrec : Primrec encodeNumeric :=
  fromBytes_primrec.comp (Primrec.list_cons.comp (Primrec.const 1) Primrec.id)

/-- Composing canonical varints with the numeric envelope is primitive recursive. -/
theorem numeric_uv_primrec : Primrec (fun n => encodeNumeric (uv n)) :=
  encodeNumeric_primrec.comp uv_primrec

/-- Any primitive-recursive family of byte payloads gives a primitive-recursive
numeric index family. This is the reusable fixed-program serialization bridge. -/
theorem encodeNumeric_comp_primrec {α : Type*} [Primcodable α]
    {bytes : α → List Nat} (hbytes : Primrec bytes) :
    Primrec (fun x => encodeNumeric (bytes x)) :=
  encodeNumeric_primrec.comp hbytes

end P02.Codec
