import RationalThresholdCuts

namespace AtomicMembership.RationalThreshold
open P02.Codec.UniformComputability

/-- Exact division semantics includes noncanonical and zero-denominator codes. -/
theorem code_lt_rational_iff (q : ℚ≥0) (i : ℕ) :
    rationalOfCode i < q ↔
      0 < q.num ∧ (i.unpair.2 = 0 ∨ i.unpair.1 * q.den < q.num * i.unpair.2) := by
  by_cases hd : i.unpair.2 = 0
  · simp [rationalOfCode, hd, NNRat.num_pos]
  · have hdq : (0 : ℚ≥0) < i.unpair.2 := by exact_mod_cast Nat.pos_of_ne_zero hd
    have hqd : (0 : ℚ≥0) < q.den := by exact_mod_cast q.den_pos
    have hrepr : (q.num : ℚ≥0) / q.den = q := by
      rw [← divNat_eq_div, NNRat.num_divNat_den]
    have hcross : rationalOfCode i < q ↔ i.unpair.1 * q.den < q.num * i.unpair.2 := by
      calc
        rationalOfCode i < q ↔ (i.unpair.1 : ℚ≥0) / i.unpair.2 < (q.num : ℚ≥0) / q.den := by
          rw [hrepr, rationalOfCode, divNat_eq_div]
        _ ↔ _ := by rw [div_lt_div_iff₀ hdq hqd]; exact_mod_cast Iff.rfl
    rw [hcross]
    constructor
    · intro h
      exact ⟨by nlinarith, Or.inr h⟩
    · rintro ⟨_,h|h⟩
      · exact (hd h).elim
      · exact h

theorem rational_lt_code_iff (q : ℚ≥0) (i : ℕ) :
    q < rationalOfCode i ↔
      i.unpair.2 ≠ 0 ∧ q.num * i.unpair.2 < i.unpair.1 * q.den := by
  by_cases hd : i.unpair.2 = 0
  · simp [rationalOfCode, hd]
  · have hdq : (0 : ℚ≥0) < i.unpair.2 := by exact_mod_cast Nat.pos_of_ne_zero hd
    have hqd : (0 : ℚ≥0) < q.den := by exact_mod_cast q.den_pos
    have hrepr : (q.num : ℚ≥0) / q.den = q := by
      rw [← divNat_eq_div, NNRat.num_divNat_den]
    have hcross : q < rationalOfCode i ↔ q.num * i.unpair.2 < i.unpair.1 * q.den := by
      calc
        q < rationalOfCode i ↔ (q.num : ℚ≥0) / q.den < (i.unpair.1 : ℚ≥0) / i.unpair.2 := by
          rw [hrepr, rationalOfCode, divNat_eq_div]
        _ ↔ _ := by rw [div_lt_div_iff₀ hqd hdq]; exact_mod_cast Iff.rfl
    simpa [hd] using hcross

theorem code_lt_rational_computable (q : ℚ≥0) :
    Computable (fun i : ℕ => decide (rationalOfCode i < q)) := by
  have ha := Primrec.fst.comp Primrec.unpair
  have hd := Primrec.snd.comp Primrec.unpair
  have hpos := Primrec.nat_lt.comp (Primrec.const 0) (Primrec.const q.num)
  have hz := Primrec.eq.comp hd (Primrec.const 0)
  have hc := Primrec.nat_lt.comp (Primrec.nat_mul.comp ha (Primrec.const q.den))
    (Primrec.nat_mul.comp (Primrec.const q.num) hd)
  apply ((hpos.and (hz.or hc)).to_comp).of_eq
  intro i
  apply Bool.eq_iff_iff.mpr
  simpa only [decide_eq_true_eq] using (code_lt_rational_iff q i).symm

theorem rational_lt_code_computable (q : ℚ≥0) :
    Computable (fun i : ℕ => decide (q < rationalOfCode i)) := by
  have ha := Primrec.fst.comp Primrec.unpair
  have hd := Primrec.snd.comp Primrec.unpair
  have hz := (Primrec.eq.comp hd (Primrec.const 0)).not
  have hc := Primrec.nat_lt.comp (Primrec.nat_mul.comp (Primrec.const q.num) hd)
    (Primrec.nat_mul.comp ha (Primrec.const q.den))
  apply ((hz.and hc).to_comp).of_eq
  intro i
  apply Bool.eq_iff_iff.mpr
  simpa only [decide_eq_true_eq] using (rational_lt_code_iff q i).symm

theorem lowerCutMatrix_computable (q : ℚ≥0) :
    Computable (fun p : MatrixInput => decide (lowerCutMatrix q p.1 p.2.1 p.2.2.1 p.2.2.2)) := by
  have hi : Computable (fun p : MatrixInput => p.2.1) := Computable.fst.comp Computable.snd
  have hlt := (rational_lt_code_computable q).comp hi
  have h1 := (code_lt_rational_computable 1).comp hi
  apply (Primrec.and.to_comp.comp hlt (Primrec.and.to_comp.comp h1 membershipMatrix_computable)).of_eq
  intro p
  apply Bool.eq_iff_iff.mpr
  simp [lowerCutMatrix, Bool.and_eq_true]

theorem upperCutMatrix_computable (q : ℚ≥0) :
    Computable (fun p : MatrixInput => decide (upperCutMatrix q p.1 p.2.1 p.2.2.1 p.2.2.2)) := by
  have hi : Computable (fun p : MatrixInput => p.2.1) := Computable.fst.comp Computable.snd
  have hlt := (code_lt_rational_computable q).comp hi
  apply (Primrec.or.to_comp.comp (Primrec.not.to_comp.comp hlt) membershipMatrix_computable).of_eq
  intro p
  apply Bool.eq_iff_iff.mpr
  simp [upperCutMatrix, Bool.or_eq_true, imp_iff_not_or]

end AtomicMembership.RationalThreshold
