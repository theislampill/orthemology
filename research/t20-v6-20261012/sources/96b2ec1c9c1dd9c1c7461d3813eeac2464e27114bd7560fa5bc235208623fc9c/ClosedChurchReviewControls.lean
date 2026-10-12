import IdentityControls
import DomainControls
import IndependentControls

namespace ClosedChurchReview
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC P01AC.ExtensionalRepair
open P01AC.EffectiveCompleteness (N NBody inputNumeral iterationPoly)
open P01AC.ExtensionalRepair.ExactScalarFusion (End i)
open P01AC.Intensional.Plus (PolyConvPlus)
open ClosedChurchIdentity ClosedChurchIdentity.Controls
open OpenDevelopments OpenDevelopments.DomainControls

-- These aliases retain the full supplied source polynomials, including discarded Omega.
def left := padded 2
def right := packed 2

theorem padded_observation (k : Nat) :
    PolyConvPlus (ClosedScalarInstances.scalarLeft (padded k)) (iterationPoly k) :=
  (PolyConvPlus.app (PolyConvPlus.app
    (PolyConvPlus.k (inputNumeral k) (.atom omega)) (.refl (.var 1)))
    (.refl (.var 0))).trans (numeral_observation k)

theorem packed_observation (k : Nat) :
    PolyConvPlus (ClosedScalarInstances.scalarLeft (packed k)) (iterationPoly k) := by
  have c := Intensional.Plus.closed_pack (inputNumeral k)
    (ClosedProofCanonicalisation.has_scope (numeralTyping k)) zeroEnv
  exact (PolyConvPlus.app (PolyConvPlus.app c.symm (.refl (.var 1)))
    (.refl (.var 0))).trans (numeral_observation k)

-- Genuinely nonliteral endpoints, one not strongly normalizing, agree at count 2.
theorem nonliteral_source_identity : HasE [] i (.identity N left right) :=
  (identity_iff_count_eq (padded_has 2) (packed_has 2)
    (padded_observation 2) (packed_observation 2)).mpr rfl

theorem nonliteral_not_SN : ¬ StronglyNormalising (eval left zeroEnv) := padded_not_SN 2

theorem nonliteral_not_open_SN :
    ¬ Acc (fun u t => OpenDevelopments.Step t u)
      (ImportedOpenTermTransport.interp left OpenTermStandardness.T.var) :=
  CompleteDevelopmentReview.padded_not_open_SN 2

-- Replacing only the endpoint count rejects every witness, rather than just I.
theorem distinct_nonliteral_no_witness :
    ¬ ∃ r, HasE [] r (.identity N (padded 2) (packed 3)) := by
  intro h
  have bad := (identity_exists_iff_count_eq (padded_has 2) (packed_has 3)
    (padded_observation 2) (packed_observation 3)).mp h
  contradiction

-- A noncanonical proof polynomial really inhabits the same identity judgment.
def witness : Poly := .app (.app (.atom .k) i) (.atom omega)
theorem witness_ne_i : witness ≠ i := by intro h; cases h

theorem noncanonical_witness : HasE [] witness (.identity N left right) :=
  .conv (ClosedProofCanonicalisation.formed nonliteral_source_identity)
    nonliteral_source_identity (PolyConvPlus.k i (.atom omega)).symm
    ⟨⟨trivial,trivial⟩,trivial⟩

theorem any_witness_agrees_with_canonical {p q : Poly}
    (hp : HasE [] p N) (hq : HasE [] q N) :
    (∃ r, HasE [] r (.identity N p q)) ↔ HasE [] i (.identity N p q) :=
  (EffectiveChurchIdentity.identity_exists_iff_extracted_counts hp hq).trans
    (EffectiveChurchIdentity.identity_iff_extracted_counts hp hq).symm

-- Rich HasE telescope formation itself consumes a proof with piExt/allExt.
def extIdentity : Ty := .identity N (.atom .i) (.atom P01R.skk)
def proofIdentity : Ty := .identity extIdentity i i

theorem ext_has : HasE [] i extIdentity := source_equal_raw_distinct.1

theorem proofIdentity_form : FormE [] proofIdentity :=
  .identity (ClosedProofCanonicalisation.formed ext_has) ext_has ext_has

def richCtx : CtxE [proofIdentity] := .ext .nil proofIdentity_form

-- Identity-empty renaming preserves arbitrary original source polynomials and types.
theorem lift_extensional_proof : HasE [proofIdentity] i extIdentity :=
  Structural.has_closed ext_has richCtx

theorem lift_noncanonical_proof : HasE [proofIdentity] witness (.identity N left right) :=
  Structural.has_closed noncanonical_witness richCtx

theorem lift_source_nonSN : HasE [proofIdentity] left N :=
  Structural.has_closed (padded_has 2) richCtx

-- Type-parameter renaming and dependent term weakening also work on extensional proofs.
theorem rename_extensional_type :
    HasE (trenameTel (fun n => n + 7) ([] : Tel)) i
      (trename (fun n => n + 7) extIdentity) :=
  Structural.has_trename ext_has (fun n => n + 7)

theorem weaken_extensional_proof : HasE [proofIdentity]
    (pren Nat.succ i) (wk extIdentity) :=
  Structural.has_wk ext_has .nil proofIdentity_form

-- The semantic characterization is at the unchanged inherited F and any rho.
theorem semantic_iff_any_witness {p q : Poly}
    (hp : HasE [] p N) (hq : HasE [] q N) (rho : OEnv) :
    (∃ r, HasE [] r (.identity N p q)) ↔
      F N rho zeroEnv (eval p zeroEnv) (eval q zeroEnv) :=
  (any_witness_agrees_with_canonical hp hq).trans
    (EffectiveChurchIdentity.identity_iff_original_semantics hp hq rho)

-- Reuse the existing genuinely discriminating raw-nonconversion proof.
theorem typed_identity_does_not_imply_raw_conversion :
    (∃ r, HasE [] r (.identity N (.atom .i) (.atom P01R.skk))) ∧
      ¬ PolyConvPlus (.atom .i) (.atom P01R.skk) :=
  ⟨⟨i, source_equal_raw_distinct.1⟩, source_equal_raw_distinct.2⟩

#guard @decide _ (EffectiveChurchIdentity.decideTypedIdentity (padded_has 2) (packed_has 2))
#guard @decide _ (EffectiveChurchIdentity.decideTypedIdentityExists (padded_has 2) (packed_has 2))
#guard !(@decide _ (EffectiveChurchIdentity.decideTypedIdentity (padded_has 2) (packed_has 3)))
#guard !(@decide _ (EffectiveChurchIdentity.decideTypedIdentityExists (padded_has 2) (packed_has 3)))
#eval (extractIteration (padded 2) (padded_has 2)).val
#eval (extractIteration (packed 2) (packed_has 2)).val
#eval (extractIteration (packed 3) (packed_has 3)).val
#print axioms nonliteral_source_identity
#print axioms distinct_nonliteral_no_witness
#print axioms noncanonical_witness
#print axioms lift_extensional_proof
#print axioms semantic_iff_any_witness
end ClosedChurchReview
