import Std
/-! Conditional mathematical interfaces only. No metaphysical original-source axioms. -/
namespace ReasonKnowledge

def Optimal {P O : Type} (F : P → O) (le : O → O → Prop) (p : P) : Prop :=
  ∀ q, le (F q) (F p)

theorem same_output_same_optimality {P O : Type} (F : P → O)
    (le : O → O → Prop) (p q : P) (same : F p = F q) :
    Optimal F le p ↔ Optimal F le q := by
  constructor <;> intro h r
  · rw [← same]; exact h r
  · rw [same]; exact h r

theorem two_implementations_defeat_unique_plan {P O : Type}
    (F : P → O) (le : O → O → Prop) (p q : P)
    (opt : Optimal F le p) (same : F p = F q) (distinct : p ≠ q) :
    ¬ (∀ r, Optimal F le r → r = p) := by
  intro unique
  have qopt := (same_output_same_optimality F le p q same).mp opt
  exact distinct (unique q qopt).symm

def Knows {W : Type} (R : W → W → Prop) (w : W) (P : W → Prop) : Prop :=
  ∀ v, R w v → P v

theorem knowledge_factive {W : Type} (R : W → W → Prop)
    (reflexive : ∀ w, R w w) (w : W) (P : W → Prop)
    (h : Knows R w P) : P w := h w (reflexive w)

theorem complete_identity_knowledge {W : Type} (w : W) (P : W → Prop) :
    Knows (fun a b => a = b) w P ↔ P w := by
  constructor
  · intro h; exact h w rfl
  · intro h v e; subst v; exact h

-- Total information at every world does not collapse the independent world sort.
theorem omniscience_at_distinct_worlds :
    (∀ (w : Bool) (P : Bool → Prop), Knows (fun a b => a = b) w P ↔ P w) ∧
    (false : Bool) ≠ true := by
  exact ⟨complete_identity_knowledge, by decide⟩

-- Factivity alone gives the same full-state outcome entailment to a passive knower.
theorem factive_record_fixes_value {W V : Type} (output record : W → V)
    (factive : ∀ w, record w = output w) (w v : W)
    (sameRecord : record w = record v) : output w = output v := by
  rw [← factive w, ← factive v]; exact sameRecord

-- A fixed actual accurate content cannot remain accurate at a changed object.
theorem frozen_content_fails_changed_object {V : Type} (content old new : V)
    (accurate : content = old) (changed : old ≠ new) : content ≠ new := by
  rw [accurate]; exact changed

-- Anonymous selection of a fixed reason structure entails a symmetric allocation;
-- anonymity is an explicit additional rule, not supplied by equal capacities.
theorem equivariant_selection_fixed_input {I P : Type} (swapI : I → I)
    (swapP : P → P) (select : I → P)
    (equivariant : ∀ i, select (swapI i) = swapP (select i))
    (i : I) (fixed : swapI i = i) : swapP (select i) = select i := by
  rw [← equivariant i, fixed]

theorem odd_target_no_equal_integer_allocation (a n : Nat) :
    a + a ≠ 2*n + 1 := by omega

-- Means planning is not merely attaching a whole-end label to a half-command.
theorem known_peer_means_selects_complement (a b q : Nat)
    (bound : b ≤ q) (plan : a = q - b) : a + b = q := by omega

theorem replan_after_peer_change_changes_command (a b b' q : Nat)
    (old : a + b = q) (new : a + b' = q) : b = b' := by omega

-- The created end and the broader relational end are distinct predicates.
def RelationalEnd (q a b : Nat) : Prop := a + b = q ∧ 0 < a ∧ 0 < b

theorem relational_end_preserves_created_target (q a b : Nat)
    (h : RelationalEnd q a b) : a + b = q := h.1

theorem solo_created_target_not_relational_end (q : Nat) :
    q + 0 = q ∧ ¬ RelationalEnd q q 0 := by
  constructor
  · omega
  · intro h; have := h.2.2; omega

theorem relational_two_selects_split (a b : Nat) :
    RelationalEnd 2 a b ↔ a = 1 ∧ b = 1 := by
  unfold RelationalEnd; omega

end ReasonKnowledge
#print axioms ReasonKnowledge.same_output_same_optimality
#print axioms ReasonKnowledge.two_implementations_defeat_unique_plan
#print axioms ReasonKnowledge.knowledge_factive
#print axioms ReasonKnowledge.complete_identity_knowledge
#print axioms ReasonKnowledge.omniscience_at_distinct_worlds
#print axioms ReasonKnowledge.factive_record_fixes_value
#print axioms ReasonKnowledge.frozen_content_fails_changed_object
#print axioms ReasonKnowledge.equivariant_selection_fixed_input
#print axioms ReasonKnowledge.odd_target_no_equal_integer_allocation
#print axioms ReasonKnowledge.known_peer_means_selects_complement
#print axioms ReasonKnowledge.replan_after_peer_change_changes_command

#print axioms ReasonKnowledge.relational_end_preserves_created_target
#print axioms ReasonKnowledge.solo_created_target_not_relational_end
#print axioms ReasonKnowledge.relational_two_selects_split
