import MembershipWitnesses
import MatrixSemanticControls

namespace MatrixIndependentAudit
open P02.Codec P02.Codec.UniformComputability AtomicMembership

theorem exact_four_input_predicate :
    Computable (fun p : ℕ × ℕ × ℕ × ℕ =>
      decide (AtomicMembership.membershipMatrix p.1 p.2.1 p.2.2.1 p.2.2.2)) :=
  membershipMatrix_computable

theorem exact_nat_coded_predicate : Computable (fun z : ℕ =>
    decide (AtomicMembership.membershipMatrix z.unpair.1 z.unpair.2.unpair.1
      z.unpair.2.unpair.2.unpair.1 z.unpair.2.unpair.2.unpair.2)) :=
  membershipMatrix_nat_computable

theorem four_input_pairing_roundtrip (e i k N : ℕ) :
    matrixInputOfNat (Nat.pair e (Nat.pair i (Nat.pair k N))) = (e,i,k,N) := by
  simp [matrixInputOfNat]

theorem exact_integer_boolean (e i k N : ℕ) :
    integerMatrix (e,i,k,N) = decide (AtomicMembership.membershipMatrix e i k N) := by
  simp [integerMatrix, membershipMatrix_integer_iff]

/-- Standard all-natural characteristic output, derived without a predicate oracle. -/
theorem characteristic_nat_to_nat : Computable (fun z : ℕ =>
    if AtomicMembership.membershipMatrix z.unpair.1 z.unpair.2.unpair.1
      z.unpair.2.unpair.2.unpair.1 z.unpair.2.unpair.2.unpair.2 then (1:ℕ) else 0) := by
  have hg : Primrec (fun b : Bool => if b then (1:ℕ) else 0) := by
    apply (Primrec.cond Primrec.id (Primrec.const 1) (Primrec.const 0)).of_eq
    intro b
    cases b <;> rfl
  apply (hg.to_comp.comp membershipMatrix_nat_computable).of_eq
  intro z
  by_cases h : AtomicMembership.membershipMatrix z.unpair.1 z.unpair.2.unpair.1
      z.unpair.2.unpair.2.unpair.1 z.unpair.2.unpair.2.unpair.2 <;> simp [h]

/-- The outer quantifiers remain in a logical equivalence; this theorem does
not claim a computable characteristic function for the infinite index set. -/
theorem exact_quantifier_order (e : ℕ) :
    e ∈ P02A2.Pi3IndexReduction.zeroDefectIndices ↔
      ∀ i, ∃ k, ∀ N, AtomicMembership.membershipMatrix e i k N :=
  effective_membership_normal_form.2 e

theorem exact_heavy_mass_bridge (e k N : ℕ) :
    AtomicMembership.rationalHeavyMass (P02A2.FiniteOutputTable.indexTable e) k N =
      (heavyCount e k N : ℚ≥0)/(2:ℚ≥0)^N := rationalHeavyMass_heavyCount e k N

end MatrixIndependentAudit
