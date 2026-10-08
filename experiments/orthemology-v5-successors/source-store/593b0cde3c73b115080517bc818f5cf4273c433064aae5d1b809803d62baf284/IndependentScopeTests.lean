import BridgeControls

namespace IndependentOriginalBearerReview
open Orthemology.Tranche20.OriginalBearerBridge
open Orthemology.Tranche20.OriginalBearerBridge.Controls
open Orthemology.Tranche3.SourceIdentity

set_option synthInstance.maxSize 16384
set_option maxRecDepth 8192
set_option maxHeartbeats 1600000

/-- The broad philosophical consequence does not require the binary adapter.
This is a scope test, not a new philosophical warrant or ownership claim. -/
theorem broad_abc_without_representation {W B R T : Type*}
    (s : Framework W B R T)
    (occurrence : ∃ t, s.targetReceived t) (completion : Completion s)
    (realisation : Realisation s) (support : SupportTransport s)
    (need : ContingencyNeed s) (constitution : ConstitutiveReception s) :
    ∃ t r g, OriginalWitness s t r g ∧ Necessary s.existsAt g ∧
      EssentialNonreceipt s g := by
  obtain ⟨t, ht⟩ := occurrence
  obtain ⟨r, g, hg⟩ := original_bearer_of_completion s t ht completion realisation support
  have ho : ActualWholeOriginal s g := hg.2.2.2.2
  have hn : Necessary s.existsAt g := by
    classical
    by_contra h
    exact ho.2 (need g ho.1 h)
  exact ⟨t, r, g, hg, hn, essential_nonreceipt_of_actual_original s g ho constitution⟩

/-- A genuinely independent binary relation can disagree with broad receipt.
The edge goes from an existing received effect to the broad original at actuality;
it is acyclic and has existing endpoints, but does not represent whole receipt. -/
def representationMismatch : Framework Bool Bool Bool Unit :=
  { positive with dep := fun w y x => w = false ∧ y = true ∧ x = false }

theorem representation_is_needed_for_binary_uniform_target :
    (∃ t, representationMismatch.targetReceived t) ∧
    Completion representationMismatch ∧ Realisation representationMismatch ∧
    SupportTransport representationMismatch ∧ ContingencyNeed representationMismatch ∧
    ConstitutiveReception representationMismatch ∧ ¬ ReceiptRepresentation representationMismatch ∧
    (∃ g, ActualWholeOriginal representationMismatch g ∧
      Necessary representationMismatch.existsAt g ∧ EssentialNonreceipt representationMismatch g) ∧
    (∀ w x, ¬ representationMismatch.dep w x x) ∧
    (∀ w y x, representationMismatch.dep w y x →
      representationMismatch.existsAt w y ∧ representationMismatch.existsAt w x) ∧
    ¬ ∃ g, UniformRoot representationMismatch.existsAt representationMismatch.dep g := by
  simp only [Completion, Realisation, SupportTransport, ContingencyNeed,
    ConstitutiveReception, ReceiptRepresentation, ActualOriginalResource,
    ActualWholeOriginal, EssentialNonreceipt, Necessary, UniformRoot, Root, Received,
    representationMismatch, positive]
  decide

/-- Two disjoint productive fields: each has an original necessary source and
an actually received contingent effect. Target provision is field-specific. -/
def plural : Framework Bool (Bool × Bool) (Bool × Bool) Bool where
  actual := false
  existsAt := fun w g => g.2 = false ∨ w = false
  wholeReceived := fun w g => w = false ∧ g.2 = true
  dep := fun w y x => w = false ∧ y.1 = x.1 ∧ y.2 = false ∧ x.2 = true
  resourceActual := fun _ => True
  resourceReceived := fun r => r.2 = true
  intrinsic := fun g r => g = r
  targetReceived := fun _ => True
  relevant := fun r t => r.1 = t ∧ r.2 = false

theorem plural_full : FullPremises plural := by
  constructor
  all_goals
    simp only [Completion, Realisation, SupportTransport, ReceiptRepresentation,
      ContingencyNeed, ConstitutiveReception, ActualOriginalResource, plural, Received, Necessary]
    try simp only [Prod.forall, Prod.exists]
    decide

theorem plural_nonvacuous_and_no_common_bearer :
    ((false, false) : Bool × Bool) ≠ (true, false) ∧
    (∀ field, OriginalWitness plural field (field, false) (field, false) ∧
      Necessary plural.existsAt (field, false) ∧ UniformRoot plural.existsAt plural.dep (field, false) ∧
      plural.wholeReceived false (field, true) ∧ ¬ Necessary plural.existsAt (field, true) ∧
      plural.dep false (field, false) (field, true)) ∧
    ¬ ∃ g, ∀ t, ∃ r, OriginalWitness plural t r g := by
  simp only [OriginalWitness, ActualOriginalResource, ActualWholeOriginal,
    Necessary, UniformRoot, Root, Received, plural]
  simp only [Prod.forall, Prod.exists]
  decide

/-- General Realisation/Support/Need/Constitution quantifiers are not required
when the single resource and bearer with their local instances are supplied.
The local backward-transfer assumption here carries no independent warrant. -/
theorem witness_local_sufficiency {W B R T : Type*} (s : Framework W B R T)
    (t : T) (r : R) (g : B)
    (occurrence : s.targetReceived t) (relevant : s.relevant r t)
    (original : ActualOriginalResource s r) (actual : s.existsAt s.actual g)
    (intrinsic : s.intrinsic g r)
    (support : s.wholeReceived s.actual g → s.resourceReceived r)
    (need : ¬ Necessary s.existsAt g → s.wholeReceived s.actual g)
    (transfer : (∃ w, s.wholeReceived w g) → s.wholeReceived s.actual g) :
    OriginalWitness s t r g ∧ Necessary s.existsAt g ∧ EssentialNonreceipt s g := by
  have hnot : ¬ s.wholeReceived s.actual g := fun h => original.2 (support h)
  have hn : Necessary s.existsAt g := by
    classical
    by_contra h
    exact hnot (need h)
  refine ⟨⟨occurrence, relevant, original, intrinsic, actual, hnot⟩, hn, ?_⟩
  intro w _ h
  exact hnot (transfer ⟨w, h⟩)

/-- Without target occurrence the remaining six major assumptions can all hold,
on a nonempty domain with no original bearer. No causal cycle is needed. -/
def noOccurrence : Framework Unit Nat Unit Unit :=
  { withoutCompletion with targetReceived := fun _ => False }

theorem occurrence_is_not_free :
    Completion noOccurrence ∧ Realisation noOccurrence ∧ SupportTransport noOccurrence ∧
    ReceiptRepresentation noOccurrence ∧ ContingencyNeed noOccurrence ∧
    ConstitutiveReception noOccurrence ∧ ¬ (∃ t, noOccurrence.targetReceived t) ∧
    ¬ ∃ g, ActualWholeOriginal noOccurrence g := by
  refine ⟨?_, ?_, ?_, nat_representation True (fun g => g = 0), nat_need True (fun g => g = 0),
    nat_constitution True (fun g => g = 0), ?_, nat_no_original True (fun g => g = 0)⟩
  · intro t h
    exact False.elim h
  · intro r _
    exact ⟨0, trivial, rfl⟩
  · intro g r _ _ _
    trivial
  · rintro ⟨t, h⟩
    exact h

#print axioms broad_abc_without_representation
#print axioms representation_is_needed_for_binary_uniform_target
#print axioms plural_full
#print axioms plural_nonvacuous_and_no_common_bearer
#print axioms witness_local_sufficiency
#print axioms occurrence_is_not_free
end IndependentOriginalBearerReview
