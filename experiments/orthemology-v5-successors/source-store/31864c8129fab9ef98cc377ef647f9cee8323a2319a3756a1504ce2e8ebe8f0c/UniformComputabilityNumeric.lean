import CodecPrimrec
import Mathlib.Computability.Partrec

/-! The actual sentinel decoder is primitive recursive on numeric indices.
This qualifies the numeric envelope; it does not assert uniform evaluation. -/
namespace P02.Codec.UniformComputability
open P02.Codec

def bytesTableStep (table : List (List ℕ)) : Option (List ℕ) :=
  let n := table.length
  if n = 0 then some []
  else (table[n / 256]?).map (fun pre => pre ++ [n % 256])

theorem bytesTableStep_primrec : Primrec bytesTableStep := by
  have hlen : Primrec (fun table : List (List ℕ) => table.length) := Primrec.list_length
  have hquot := Primrec.nat_div.comp hlen (Primrec.const 256)
  have hbyte := Primrec.nat_mod.comp hlen (Primrec.const 256)
  have hget := Primrec.list_getElem?.comp (Primrec.id : Primrec (@id (List (List ℕ)))) hquot
  have hsnoc : Primrec₂ (fun (table : List (List ℕ)) (pre : List ℕ) =>
      pre ++ [table.length % 256]) :=
    (Primrec.list_append.comp Primrec.snd
      (Primrec.list_cons.comp (hbyte.comp Primrec.fst) (Primrec.const []))).to₂
  exact Primrec.ite (Primrec.eq.comp hlen (Primrec.const 0))
    (Primrec.const (some [])) (Primrec.option_map hget hsnoc)

theorem bytesTableStep_table (n : ℕ) :
    bytesTableStep ((List.range n).map toBytes) = some (toBytes n) := by
  simp only [bytesTableStep, List.length_map, List.length_range]
  by_cases hn : n = 0
  · subst n; simp
  · have hd : n / 256 < n := Nat.div_lt_self (by omega) (by omega)
    rw [if_neg hn, List.getElem?_map, List.getElem?_range hd, toBytes, if_neg hn]
    rfl

theorem toBytes_primrec : Primrec toBytes := by
  have hs : Primrec₂ (fun (_ : Unit) n => toBytes n) :=
    Primrec.nat_strong_rec _ ((bytesTableStep_primrec.comp Primrec.snd).to₂)
      (fun _ n => bytesTableStep_table n)
  exact hs.comp (Primrec.const ()) Primrec.id

end P02.Codec.UniformComputability

namespace P02.Codec.UniformComputability
open P02.Codec

/-- The complete sentinel-envelope decoder, including rejection, is primitive recursive. -/
theorem decodeNumeric_primrec : Primrec decodeNumeric := by
  have ht : Primrec (fun n => toBytes n) := toBytes_primrec
  have hh : Primrec (fun n => (toBytes n).head?) := Primrec.list_head?.comp ht
  have htail : Primrec (fun n => (toBytes n).tail) := Primrec.list_tail.comp ht
  have hc : Primrec (fun n =>
      if n = 0 then (none : Option (List ℕ))
      else if (toBytes n).head? = some 1 then some (toBytes n).tail else none) :=
    Primrec.ite (Primrec.eq.comp Primrec.id (Primrec.const 0)) (Primrec.const none)
      (Primrec.ite (Primrec.eq.comp hh (Primrec.const (some 1)))
        (Primrec.option_some.comp htail) (Primrec.const none))
  apply hc.of_eq
  intro n
  unfold decodeNumeric
  by_cases hn : n = 0
  · simp [hn]
  · simp only [hn, ↓reduceIte]
    cases hbs : toBytes n with
    | nil => simp
    | cons b bs =>
      by_cases hb : b = 1
      · subst b; simp
      · simp [hb]

theorem decodeNumeric_computable : Computable decodeNumeric := decodeNumeric_primrec.to_comp

end P02.Codec.UniformComputability
