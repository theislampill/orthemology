import RationalThresholdComputable

namespace AtomicMembership.RationalThreshold
open P02.Codec.UniformComputability

/-- Comparison of two *original* rational codes, with their total division convention. -/
theorem rationalCodes_lt_iff (i j : ℕ) :
    rationalOfCode i < rationalOfCode j ↔
      j.unpair.2 ≠ 0 ∧ 0 < j.unpair.1 ∧
        (i.unpair.2 = 0 ∨ i.unpair.1 * j.unpair.2 < j.unpair.1 * i.unpair.2) := by
  by_cases hj : j.unpair.2 = 0
  · simp [rationalOfCode, hj]
  · have hdj : (0 : ℚ≥0) < j.unpair.2 := by exact_mod_cast Nat.pos_of_ne_zero hj
    by_cases hi : i.unpair.2 = 0
    · have hp : (0 : ℚ≥0) < NNRat.divNat j.unpair.1 j.unpair.2 ↔ 0 < j.unpair.1 := by
        rw [divNat_eq_div, div_pos_iff_of_pos_right hdj]
        exact_mod_cast Iff.rfl
      simpa [rationalOfCode, hi, hj] using hp
    · have hdi : (0 : ℚ≥0) < i.unpair.2 := by exact_mod_cast Nat.pos_of_ne_zero hi
      have hc : rationalOfCode i < rationalOfCode j ↔
          i.unpair.1 * j.unpair.2 < j.unpair.1 * i.unpair.2 := by
        unfold rationalOfCode
        rw [divNat_eq_div, divNat_eq_div, div_lt_div_iff₀ hdi hdj]
        exact_mod_cast Iff.rfl
      rw [hc]
      constructor
      · intro h
        exact ⟨hj,by nlinarith,Or.inr h⟩
      · rintro ⟨_,_,h|h⟩
        · exact (hi h).elim
        · exact h

theorem rationalCodes_lt_primrec :
    Primrec (fun p : ℕ × ℕ => decide (rationalOfCode p.1 < rationalOfCode p.2)) := by
  have ha : Primrec (fun p : ℕ × ℕ => p.1.unpair.1) := Primrec.fst.comp (Primrec.unpair.comp Primrec.fst)
  have hd : Primrec (fun p : ℕ × ℕ => p.1.unpair.2) := Primrec.snd.comp (Primrec.unpair.comp Primrec.fst)
  have hb : Primrec (fun p : ℕ × ℕ => p.2.unpair.1) := Primrec.fst.comp (Primrec.unpair.comp Primrec.snd)
  have hf : Primrec (fun p : ℕ × ℕ => p.2.unpair.2) := Primrec.snd.comp (Primrec.unpair.comp Primrec.snd)
  have hz := (Primrec.eq.comp hf (Primrec.const 0)).not
  have hp := Primrec.nat_lt.comp (Primrec.const 0) hb
  have hd0 := Primrec.eq.comp hd (Primrec.const 0)
  have hc := Primrec.nat_lt.comp (Primrec.nat_mul.comp ha hf) (Primrec.nat_mul.comp hb hd)
  apply (hz.and (hp.and (hd0.or hc))).of_eq
  intro p
  exact (rationalCodes_lt_iff p.1 p.2).symm

abbrev CodedMatrixInput := ℕ × MatrixInput

theorem lowerCutMatrix_code_computable :
    Computable (fun p : CodedMatrixInput => decide
      (lowerCutMatrix (rationalOfCode p.1) p.2.1 p.2.2.1 p.2.2.2.1 p.2.2.2.2)) := by
  have hj : Computable (fun p : CodedMatrixInput => p.1) := Computable.fst
  have hp : Computable (fun p : CodedMatrixInput => p.2) := Computable.snd
  have hi : Computable (fun p : CodedMatrixInput => p.2.2.1) :=
    Computable.fst.comp (Computable.snd.comp Computable.snd)
  have hlt := rationalCodes_lt_primrec.to_comp.comp (hj.pair hi)
  have h1 := (code_lt_rational_computable 1).comp hi
  have hm := membershipMatrix_computable.comp hp
  apply (Primrec.and.to_comp.comp hlt (Primrec.and.to_comp.comp h1 hm)).of_eq
  intro p
  apply Bool.eq_iff_iff.mpr
  simp [lowerCutMatrix, Bool.and_eq_true]

theorem upperCutMatrix_code_computable :
    Computable (fun p : CodedMatrixInput => decide
      (upperCutMatrix (rationalOfCode p.1) p.2.1 p.2.2.1 p.2.2.2.1 p.2.2.2.2)) := by
  have hj : Computable (fun p : CodedMatrixInput => p.1) := Computable.fst
  have hp : Computable (fun p : CodedMatrixInput => p.2) := Computable.snd
  have hi : Computable (fun p : CodedMatrixInput => p.2.2.1) :=
    Computable.fst.comp (Computable.snd.comp Computable.snd)
  have hlt := rationalCodes_lt_primrec.to_comp.comp (hi.pair hj)
  have hm := membershipMatrix_computable.comp hp
  apply (Primrec.or.to_comp.comp (Primrec.not.to_comp.comp hlt) hm).of_eq
  intro p
  apply Bool.eq_iff_iff.mpr
  simp [upperCutMatrix, Bool.or_eq_true, imp_iff_not_or]

/-- Complement code uses the same rational decoder, including denominator-zero semantics. -/
def complementCode (j : ℕ) : ℕ :=
  if j.unpair.2 = 0 then Nat.pair 1 1
  else Nat.pair (j.unpair.2 - j.unpair.1) j.unpair.2

theorem rationalOfCode_complement (j : ℕ) :
    rationalOfCode (complementCode j) = 1 - rationalOfCode j := by
  by_cases hd : j.unpair.2 = 0
  · norm_num [complementCode, hd, rationalOfCode, divNat_eq_div]
  · simp only [complementCode, hd, ↓reduceIte, rationalOfCode, Nat.unpair_pair]
    rw [divNat_eq_div, divNat_eq_div, Nat.cast_tsub, tsub_div]
    simp [hd]

theorem complementCode_primrec : Primrec complementCode := by
  have ha := Primrec.fst.comp Primrec.unpair
  have hd := Primrec.snd.comp Primrec.unpair
  have hz := Primrec.eq.comp hd (Primrec.const 0)
  have hp := Primrec₂.natPair.comp (Primrec.nat_sub.comp hd ha) hd
  exact (Primrec.ite hz (Primrec.const (Nat.pair 1 1)) hp)

theorem lowerDefectMatrix_code_computable :
    Computable (fun p : CodedMatrixInput => decide
      (lowerCutMatrix (1-rationalOfCode p.1) p.2.1 p.2.2.1 p.2.2.2.1 p.2.2.2.2)) := by
  have hf : Computable (fun p : CodedMatrixInput => (complementCode p.1,p.2)) :=
    (complementCode_primrec.to_comp.comp Computable.fst).pair Computable.snd
  apply (lowerCutMatrix_code_computable.comp hf).of_eq
  intro p
  simp only [rationalOfCode_complement]

theorem upperDefectMatrix_code_computable :
    Computable (fun p : CodedMatrixInput => decide
      (upperCutMatrix (1-rationalOfCode p.1) p.2.1 p.2.2.1 p.2.2.2.1 p.2.2.2.2)) := by
  have hf : Computable (fun p : CodedMatrixInput => (complementCode p.1,p.2)) :=
    (complementCode_primrec.to_comp.comp Computable.fst).pair Computable.snd
  apply (upperCutMatrix_code_computable.comp hf).of_eq
  intro p
  simp only [rationalOfCode_complement]

end AtomicMembership.RationalThreshold
