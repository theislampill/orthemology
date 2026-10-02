import Mathlib.Data.Finset.Card
import Mathlib.Data.Fintype.Card
import Mathlib.Tactic

/-!
Finite-message safe root selection. These are combinatorial interpretation
lemmas, not proofs of source truthfulness, authentication or world applicability.
Random decoding is represented only by its nonempty support, without a claim
that the shared-randomness measure argument is formalised here.
-/
namespace Orthemology.ActionDisclosure

variable {R M : Type*} [DecidableEq R] [Fintype M]

def safeDecoder (decode : M → R) (budget : ℕ) : Prop :=
  ∀ corrupt : Finset R, corrupt.card ≤ budget →
    ∃ message, decode message ∉ corrupt

theorem safeDecoder_iff_range_card (decode : M → R) (budget : ℕ) :
    safeDecoder decode budget ↔
      budget < (Finset.univ.image decode).card := by
  classical
  constructor
  · intro h
    by_contra hn
    have hc : (Finset.univ.image decode).card ≤ budget := Nat.le_of_not_gt hn
    obtain ⟨m, hm⟩ := h (Finset.univ.image decode) hc
    exact hm (Finset.mem_image.mpr ⟨m, Finset.mem_univ m, rfl⟩)
  · intro h corrupt hc
    by_contra hn
    push_neg at hn
    have hsub : Finset.univ.image decode ⊆ corrupt := by
      intro r hr
      obtain ⟨m, _, rfl⟩ := Finset.mem_image.mp hr
      exact hn m
    have hh := Finset.card_le_card hsub
    omega

theorem safeDecoder_message_lower_bound (decode : M → R) (budget : ℕ)
    (h : safeDecoder decode budget) : budget < Fintype.card M := by
  have hc := (safeDecoder_iff_range_card decode budget).mp h
  have hi : (Finset.univ.image decode).card ≤ Fintype.card M := by
    simpa using Finset.card_image_le (s := Finset.univ) (f := decode)
  omega

theorem injective_menu_suffices (decode : M → R) (budget : ℕ)
    (hinj : Function.Injective decode) (hsize : budget < Fintype.card M) :
    safeDecoder decode budget := by
  rw [safeDecoder_iff_range_card, Finset.card_image_of_injective _ hinj]
  simpa using hsize

/-- A message's possible output roots. Every message has some output because
    permanent abstention is outside the eventually-acting contract. -/
def safeSupportCode (support : M → Set R) (budget : ℕ) : Prop :=
  ∀ corrupt : Finset R, corrupt.card ≤ budget →
    ∃ message, ∀ r ∈ support message, r ∉ corrupt

theorem support_code_lower_bound (support : M → Set R) (budget : ℕ)
    (hnonempty : ∀ m, (support m).Nonempty)
    (hsafe : safeSupportCode support budget) : budget < Fintype.card M := by
  classical
  let pick : M → R := fun m => Classical.choose (hnonempty m)
  have hpick : ∀ m, pick m ∈ support m := fun m => Classical.choose_spec (hnonempty m)
  have hdecode : safeDecoder pick budget := by
    intro corrupt hc
    obtain ⟨m, hm⟩ := hsafe corrupt hc
    exact ⟨m, hm (pick m) (hpick m)⟩
  exact safeDecoder_message_lower_bound pick budget hdecode

/-- Conditional view reduction: D are already corrupt, U are the remaining
    roots, and an additional corruption subset B of U has residual budget b.
    This theorem only records the cardinal accounting; epistemic entitlement
    to D and a static shared report/actuator budget are application premises. -/
theorem residual_budget_card (knownBad restBad : Finset R)
    (hdisjoint : Disjoint knownBad restBad) :
    (knownBad ∪ restBad).card = knownBad.card + restBad.card :=
  Finset.card_union_of_disjoint hdisjoint

#print axioms safeDecoder_iff_range_card
#print axioms safeDecoder_message_lower_bound
#print axioms injective_menu_suffices
#print axioms support_code_lower_bound
#print axioms residual_budget_card
end Orthemology.ActionDisclosure
