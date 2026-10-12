import ClosedChurchIdentity
import OpenDevelopments

/- Effective source-identity decision on the promised domain of supplied actual
   closed HasE Church derivations. This never decides HasE membership. -/
namespace EffectiveChurchIdentity
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC P01AC.ExtensionalRepair
open P01AC.EffectiveCompleteness (N inputNumeral)
open P01AC.ExtensionalRepair.ExactScalarFusion (i)
open OpenDevelopments (extractIteration)

/-- The original source term is typed-identical to its computably extracted
    numeral; the equality is source Id_N, not raw polynomial conversion. -/
theorem extracted_canonicity {n : Poly} (hn : HasE [] n N) :
    HasE [] i (.identity N n (inputNumeral (extractIteration n hn).val)) :=
  ClosedChurchIdentity.canonicity_at_count hn (extractIteration n hn).property

theorem identity_iff_extracted_counts {p q : Poly}
    (hp : HasE [] p N) (hq : HasE [] q N) :
    HasE [] i (.identity N p q) ↔
      (extractIteration p hp).val = (extractIteration q hq).val :=
  ClosedChurchIdentity.identity_iff_count_eq hp hq
    (extractIteration p hp).property (extractIteration q hq).property

theorem identity_exists_iff_extracted_counts {p q : Poly}
    (hp : HasE [] p N) (hq : HasE [] q N) :
    (∃ r, HasE [] r (.identity N p q)) ↔
      (extractIteration p hp).val = (extractIteration q hq).val :=
  ClosedChurchIdentity.identity_exists_iff_count_eq hp hq
    (extractIteration p hp).property (extractIteration q hq).property

/-- Exact semantic/source identity completeness at this one closed input type.
    The interpretation is the original inherited F, at any type environment. -/
theorem identity_iff_original_semantics {p q : Poly}
    (hp : HasE [] p N) (hq : HasE [] q N) (ρ : OEnv) :
    HasE [] i (.identity N p q) ↔ F N ρ zeroEnv (eval p zeroEnv) (eval q zeroEnv) := by
  constructor
  · intro h
    exact (ExtensionalRepair.unary_fundamental h (ρ := ρ) ⟨rfl,rfl⟩).1
  · intro h
    apply (identity_iff_extracted_counts hp hq).mpr
    exact IdentityComplexity.related_same_index h
      (ClosedChurchIdentity.observation_uniform (ClosedProofCanonicalisation.has_scope hp)
        (extractIteration p hp).property)
      (ClosedChurchIdentity.observation_uniform (ClosedProofCanonicalisation.has_scope hq)
        (extractIteration q hq).property)

/-- Executable decision procedure on already-supplied closed Church typings.
    Both source terms are retained unchanged. -/
def decideTypedIdentity {p q : Poly} (hp : HasE [] p N) (hq : HasE [] q N) :
    Decidable (HasE [] i (.identity N p q)) :=
  if h : (extractIteration p hp).val = (extractIteration q hq).val then
    .isTrue ((identity_iff_extracted_counts hp hq).mpr h)
  else .isFalse (fun hi => h ((identity_iff_extracted_counts hp hq).mp hi))

def decideTypedIdentityExists {p q : Poly} (hp : HasE [] p N) (hq : HasE [] q N) :
    Decidable (∃ r, HasE [] r (.identity N p q)) :=
  if h : (extractIteration p hp).val = (extractIteration q hq).val then
    .isTrue ((identity_exists_iff_extracted_counts hp hq).mpr h)
  else .isFalse (fun hi => h ((identity_exists_iff_extracted_counts hp hq).mp hi))

#print axioms identity_iff_original_semantics
#print axioms extracted_canonicity
#print axioms identity_iff_extracted_counts
#print axioms identity_exists_iff_extracted_counts
#print axioms decideTypedIdentity
#print axioms decideTypedIdentityExists
end EffectiveChurchIdentity
