import FamilyComputability

namespace SourceFamilyComputability
open P01AC P01AC.ExtensionalRepair P01AC.BooleanPrimitive Encodable FullPERTests

/-- Semantic validity as a predicate on the existing source syntax codes.
    Malformed natural codes that encode no source type do not satisfy this predicate. -/
def codedHolds (c : Nat) : Prop := ∃ A : Ty, encode A = c ∧ Holds A

def codedFormedHolds (c : Nat) : Prop :=
  ∃ A : Ty, encode A = c ∧ FormE [] A ∧ Holds A

@[simp] theorem codedHolds_encode (A : Ty) : codedHolds (encode A) ↔ Holds A := by
  constructor
  · rintro ⟨B, hcode, hB⟩
    exact encode_injective hcode ▸ hB
  · exact fun h => ⟨A, rfl, h⟩

@[simp] theorem codedFormedHolds_encode (A : Ty) :
    codedFormedHolds (encode A) ↔ FormE [] A ∧ Holds A := by
  constructor
  · rintro ⟨B, hcode, hB⟩
    exact encode_injective hcode ▸ hB
  · exact fun h => ⟨A, rfl, h⟩

/-- Unconditional semantic non-r.e. theorem on the exact natural source codes.
    This invokes Mathlib's computable-preimage closure using the proved family
    map, rather than stipulating its computability. -/
theorem codedHolds_not_re : ¬ REPred codedHolds := by
  intro h
  obtain ⟨f, _, hnre, _⟩ := exists_non_re_formed_family
  apply hnre
  exact REPred.of_eq (h.comp (computable_encode_programType f)) (fun e => codedHolds_encode _)

/-- Restricting to actual E-formed source types does not restore r.e.-ness. -/
theorem codedFormedHolds_not_re : ¬ REPred codedFormedHolds := by
  intro h
  obtain ⟨f, hf, hnre, _⟩ := exists_non_re_formed_family
  apply hnre
  refine REPred.of_eq (h.comp (computable_encode_programType f)) (fun e => ?_)
  rw [codedFormedHolds_encode]
  exact ⟨And.right, fun hv => ⟨hf e, hv⟩⟩

#print axioms codedHolds_not_re
#print axioms codedFormedHolds_not_re
end SourceFamilyComputability
