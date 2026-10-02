import FiniteSelector
import Mathlib.Computability.Primrec

namespace OrthemologyTagged

theorem readBit_primrec : Primrec₂ (fun p : ℕ × ℕ => readBit p.1 p.2) := by
  have hn : Primrec (fun p : (ℕ × ℕ) × ℕ => p.1.1) := Primrec.fst.comp Primrec.fst
  have hb : Primrec (fun p : (ℕ × ℕ) × ℕ => p.1.2) := Primrec.snd.comp Primrec.fst
  have hj : Primrec (fun p : (ℕ × ℕ) × ℕ => p.2) := Primrec.snd
  have hp := (Primrec₂.unpaired'.mp Nat.Primrec.pow).comp (Primrec.const 2)
    (Primrec.nat_sub.comp hn hj)
  exact (Primrec.eq.comp (Primrec.nat_mod.comp (Primrec.nat_div.comp hb hp)
    (Primrec.const 2)) (Primrec.const 1)).to₂

theorem scannedBits_eq_map (n b : ℕ) :
    scannedBits n b = (List.range (n+1)).map (readBit n b) := by
  have h := List.ofFn_getElem_eq_map (List.range (n+1)) (readBit n b)
  simpa only [List.length_range, List.getElem_range] using h

theorem scannedBits_primrec : Primrec₂ scannedBits := by
  have h := Primrec.list_map
    (Primrec.list_range.comp (Primrec.succ.comp (Primrec.fst : Primrec (fun p : ℕ × ℕ => p.1))))
    readBit_primrec
  exact (h.of_eq (fun p => (scannedBits_eq_map p.1 p.2).symm)).to₂

theorem selector_primrec : Primrec₂ selector := by
  exact (Primrec.list_findIdx scannedBits_primrec
    (Primrec.not.comp Primrec.snd).to₂).to₂

end OrthemologyTagged
#print axioms OrthemologyTagged.selector_primrec
