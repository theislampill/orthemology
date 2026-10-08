import OriginationTypeControl
open T20.OntologyTypeControl
namespace IndependentReview

-- R has a successor everywhere: the checked Box claim is not dead-end vacuity.
theorem frame_serial (w : World) : ∃ v, R w v :=
  ⟨active (w.serial + 1), Nat.lt_succ_self _⟩

-- The owner and Power are explicit representation inputs, not an explanation
-- of why R admits fresh acts or a derivation of God from persistent possibility.
theorem fresh_act_has_explicit_owner (w v : World) (fresh : FreshG w v) :
    ∃ a, E v a ∧ DivineAct a .ground ∧ Inheres a .ground ∧
      Power v .ground ∧ ¬ Created a := by
  obtain ⟨n, _, he, _⟩ := fresh
  exact ⟨.gAct n, he, ⟨True.intro, rfl⟩, ⟨True.intro, rfl⟩,
    ⟨True.intro, rfl⟩, fun h => h⟩

-- Concrete, existent, temporally novel counterexample. Emergent itself is a
-- kind predicate and must not be mistaken for a temporal definition.
theorem actual_novelty_not_created_or_received :
    ∃ a, ¬ E (actual 0) a ∧ E (actual 1) a ∧ Emergent a ∧
      ¬ Created a ∧ ¬ ExternalReceipt (actual 1) a := by
  refine ⟨.gAct 1, ?_⟩
  simp [E, actual, Emergent, Created, ExternalReceipt]

theorem inhabited_emergence_not_universally_created :
    ¬ (∀ w a, E w a → Emergent a → Created a) := by
  intro all
  exact (act_product_boundary.2.2.2.2.2.2.2.1)
    (all (actual 1) (.gAct 1) act_product_boundary.2.1 True.intro)

-- An all-quiet stipulated trajectory still has fresh modal alternatives.
-- Thus the modal theorem does not force actual future occurrences.
theorem modal_renewability_does_not_populate_quiet_trajectory :
    (∀ t, EmptyG (quiet t)) ∧ (∀ t, Box (quiet t) PossibleFreshG) := by
  exact ⟨fun t => (empty_all t).2,
    fun t => (empty_and_renewable (quiet t)).2.2⟩

-- The auxiliary kind is not globally uninhabited, although otherOn is false
-- on the author's actual trajectory. Its actual cessation clause is vacuous.
theorem auxiliary_kind_possible_but_absent_on_actual :
    (∃ w, E w (.other 0)) ∧ (∀ t n, ¬ E (actual t) (.other n)) := by
  constructor
  · exact ⟨⟨0, false, true⟩, rfl, rfl⟩
  · intro t n h
    exact Bool.noConfusion h.2

-- Applying a whole-bearer receipt principle to every object label is an extra
-- premise; this control does not refute the separately typed B conditional.
theorem unrestricted_receipt_need_not_satisfied :
    ¬ (∀ x, E (actual 1) x → ¬ Necessary x → ExternalReceipt (actual 1) x) := by
  intro need
  have absent : ¬ Necessary (.gAct 1) := by
    intro h
    exact Bool.noConfusion (h (quiet 1)).2
  exact need (.gAct 1) (by simp [E, actual]) absent

#print axioms frame_serial
#print axioms fresh_act_has_explicit_owner
#print axioms actual_novelty_not_created_or_received
#print axioms inhabited_emergence_not_universally_created
#print axioms modal_renewability_does_not_populate_quiet_trajectory
#print axioms auxiliary_kind_possible_but_absent_on_actual
#print axioms unrestricted_receipt_need_not_satisfied
end IndependentReview
