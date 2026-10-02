import MembershipHeavyBridge
import MembershipComputable

/-! Formal uniform effectivity of the exact already-sealed natural-number
membership matrix. The rational comparison is replaced only through a proved
identity with the actual finite integer numerator. -/
namespace P02.Codec.UniformComputability
open AtomicMembership

attribute [local irreducible] Computable Primrec evaluateIndex outputList wordCount heavyCount membershipMatrix finiteMassTest rationalOfCode

abbrev MatrixInput := ℕ × ℕ × ℕ × ℕ

def integerMatrix (p : MatrixInput) : Bool :=
  decide (p.2.1.unpair.2 = 0 ∨ p.2.1.unpair.2 ≤ p.2.1.unpair.1 ∨
    p.2.1.unpair.1 * 2^p.2.2.2 ≤ p.2.1.unpair.2 * heavyCount p.1 p.2.2.1 p.2.2.2)

theorem integerMatrix_computable : Computable integerMatrix := by
  have he : Computable (fun p : MatrixInput => p.1) := Computable.fst
  have hi : Computable (fun p : MatrixInput => p.2.1) := Computable.fst.comp Computable.snd
  have hk : Computable (fun p : MatrixInput => p.2.2.1) := Computable.fst.comp (Computable.snd.comp Computable.snd)
  have hn : Computable (fun p : MatrixInput => p.2.2.2) := Computable.snd.comp (Computable.snd.comp Computable.snd)
  have ha := Computable.fst.comp (Computable.unpair.comp hi)
  have hd := Computable.snd.comp (Computable.unpair.comp hi)
  have hH := Computable.comp heavyCount_computable (he.pair (hk.pair hn))
  have hpow := (Primrec₂.unpaired'.mp Nat.Primrec.pow).to_comp.comp (Computable.const 2) hn
  have hz := Primrec.eq.to_comp.comp hd (Computable.const 0)
  have hv := Primrec.nat_le.to_comp.comp hd ha
  have hc := Primrec.nat_le.to_comp.comp (Primrec.nat_mul.to_comp.comp ha hpow)
    (Primrec.nat_mul.to_comp.comp hd hH)
  apply (Primrec.or.to_comp.comp hz (Primrec.or.to_comp.comp hv hc)).of_eq
  intro p
  apply Bool.eq_iff_iff.mpr
  simp [integerMatrix, Bool.or_eq_true]

/-- Exact original predicate, with all four natural parameters variable. -/
theorem membershipMatrix_computable :
    Computable (fun p : MatrixInput => decide (membershipMatrix p.1 p.2.1 p.2.2.1 p.2.2.2)) := by
  apply Computable.of_eq integerMatrix_computable
  intro p
  unfold integerMatrix
  apply Bool.eq_iff_iff.mpr
  simpa only [decide_eq_true_eq] using (membershipMatrix_integer_iff p.1 p.2.1 p.2.2.1 p.2.2.2).symm

/-- Explicit standard Nat coding for the four inputs, independent of all
internal Expr/Stmt/Task representations. -/
def matrixInputOfNat (z : ℕ) : MatrixInput :=
  (z.unpair.1,z.unpair.2.unpair.1,z.unpair.2.unpair.2.unpair.1,z.unpair.2.unpair.2.unpair.2)

theorem matrixInputOfNat_primrec : Primrec matrixInputOfNat :=
  (Primrec.fst.comp Primrec.unpair).pair
    ((Primrec.fst.comp (Primrec.unpair.comp (Primrec.snd.comp Primrec.unpair))).pair
      (Primrec.unpair.comp (Primrec.snd.comp (Primrec.unpair.comp (Primrec.snd.comp Primrec.unpair)))))

theorem membershipMatrix_nat_computable : Computable (fun z : ℕ =>
    decide (membershipMatrix z.unpair.1 z.unpair.2.unpair.1
      z.unpair.2.unpair.2.unpair.1 z.unpair.2.unpair.2.unpair.2)) := by
  have h : Computable (fun z : ℕ => decide (membershipMatrix (matrixInputOfNat z).1
      (matrixInputOfNat z).2.1 (matrixInputOfNat z).2.2.1 (matrixInputOfNat z).2.2.2)) :=
    Computable.comp membershipMatrix_computable matrixInputOfNat_primrec.to_comp
  apply Computable.of_eq h
  intro z
  rfl

/-- A standard Nat-to-Nat characteristic function for the same exact matrix. -/
theorem membershipMatrix_characteristic_computable : Computable (fun z : ℕ =>
    (decide (membershipMatrix z.unpair.1 z.unpair.2.unpair.1
      z.unpair.2.unpair.2.unpair.1 z.unpair.2.unpair.2.unpair.2)).toNat) :=
  Computable.comp (Primrec.dom_bool Bool.toNat).to_comp membershipMatrix_nat_computable

/-- The actual index set has a uniformly computable natural-number matrix in
its proved forall-exists-forall normal form. -/
theorem effective_membership_normal_form :
    Computable (fun p : MatrixInput => decide (membershipMatrix p.1 p.2.1 p.2.2.1 p.2.2.2)) ∧
    ∀ e, e ∈ P02A2.Pi3IndexReduction.zeroDefectIndices ↔
      ∀ i, ∃ k, ∀ n, membershipMatrix e i k n :=
  ⟨membershipMatrix_computable, numeric_zero_defect_nat_normal⟩

end P02.Codec.UniformComputability
