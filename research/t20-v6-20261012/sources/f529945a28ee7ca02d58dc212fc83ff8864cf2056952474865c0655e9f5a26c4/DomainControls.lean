import OpenDevelopments

namespace OpenDevelopments.DomainControls
open OrthemologyV2 OrthemologyV3 P01D P01AC P01AC.ExtensionalRepair
open P01AC.EffectiveCompleteness (N inputNumeral inputNumeral_has)
open P01AC.Intensional.Plus (PolyConvPlus)
set_option maxRecDepth 16384
set_option maxHeartbeats 4000000

def padded (k : Nat) : Poly :=
  .app (.app (.atom .k) (inputNumeral k)) (.atom omega)

/-- Actual HasE.conv admits a discarded untyped diverging subterm. -/
theorem padded_has (k : Nat) : HasE [] (padded k) N := by
  have h := has_inclusion (inputNumeral_has k)
  exact .conv (ClosedProofCanonicalisation.formed h) h
    (PolyConvPlus.k (inputNumeral k) (.atom omega)).symm
    ⟨⟨trivial, ClosedProofCanonicalisation.has_scope h⟩,trivial⟩

/-- Hence inherited finite_SN must not be applied to arbitrary HasE inhabitants. -/
theorem padded_not_SN (k : Nat) : ¬ StronglyNormalising (eval (padded k) zeroEnv) :=
  three_cycle_not_SN
    (OrthemologyV2.Step.right _ omega_step1)
    (OrthemologyV2.Step.right _ omega_step2)
    (OrthemologyV2.Step.right _ omega_step3)

def packed (k : Nat) : Poly := .atom (eval (inputNumeral k) zeroEnv)

theorem packed_has (k : Nat) : HasE [] (packed k) N := by
  have h := has_inclusion (inputNumeral_has k)
  exact .conv (ClosedProofCanonicalisation.formed h) h
    (P01AC.Intensional.Plus.closed_pack _ (ClosedProofCanonicalisation.has_scope h) zeroEnv)
    trivial

/- These run the computable definition with proof arguments erased. -/
#eval (extractIteration (inputNumeral 0) (has_inclusion (inputNumeral_has 0))).val
#eval (extractIteration (inputNumeral 1) (has_inclusion (inputNumeral_has 1))).val
#eval (extractIteration (inputNumeral 2) (has_inclusion (inputNumeral_has 2))).val
#eval (extractIteration (padded 2) (padded_has 2)).val
#eval (extractIteration (packed 2) (packed_has 2)).val

#print axioms padded_has
#print axioms padded_not_SN
#print axioms packed_has
end OpenDevelopments.DomainControls
