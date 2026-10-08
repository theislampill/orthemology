import SourceIdentity
import ProductiveCompleteness

/-!
# Exact retained relation schemas with independently interpreted cognition

This is a relative interpretation, not a metaphysical possibility proof.
`Knows`, `Owns`, and `Truth` below are conceded semantic inputs represented by
finite tables. No computation or behavioral correctness establishes cognition.
All retained source predicates and theorems are imported without alteration.
-/

namespace Orthemology.Tranche5.KnowledgeScope

open Orthemology.Tranche3

inductive World | a | b | c deriving DecidableEq, Fintype
inductive Entity | u | r | ka | kb | z deriving DecidableEq, Fintype
inductive Content | p | q deriving DecidableEq, Fintype
inductive Mode | ar | aka | br | bkb | cz | dka | dkb deriving DecidableEq, Fintype

open World Entity Content

def Ex (w : World) (x : Entity) : Prop :=
  x = u ∨ (x = r ∧ (w = a ∨ w = b)) ∨ (x = ka ∧ w = a) ∨
    (x = kb ∧ w = b) ∨ (x = z ∧ w = c)

def Dep (w : World) (s x : Entity) : Prop := s = u ∧ Ex w x ∧ x ≠ u

def Complete (w : World) (s x : Entity) : Prop := Dep w s x

def modeWorld : Mode → World
  | .ar | .aka | .dka => a
  | .br | .bkb | .dkb => b
  | .cz => c

def modeTarget : Mode → Entity
  | .ar | .br => r
  | .aka | .dka => ka
  | .bkb | .dkb => kb
  | .cz => z

def Original (m : Mode) : Prop := m ≠ .dka ∧ m ≠ .dkb

def ModeOf (w : World) (x : Entity) (m : Mode) : Prop :=
  modeWorld m = w ∧ modeTarget m = x

def Proper (w : World) (s : Entity) (m : Mode) : Prop :=
  modeWorld m = w ∧ s = u ∧ Original m

def Accounts (w : World) (s : Entity) (m : Mode) : Prop :=
  modeWorld m = w ∧ s = u

/-- Mental ownership is independent of unborrowed productive efficacy. -/
def Owns (w : World) (s k : Entity) : Prop :=
  s = r ∧ ((w = a ∧ k = ka) ∨ (w = b ∧ k = kb))

/-- Conceded actual Knowledge, not inferred from finite behavior. -/
def Knows (w : World) (s : Entity) (p' : Content) : Prop :=
  (w = a ∨ w = b) ∧ s = r ∧ p' = p

def Truth (p' : Content) : Prop := p' = p

def ThoughtContent (k : Entity) (p' : Content) : Prop :=
  (k = ka ∨ k = kb) ∧ p' = p

def LocalActivity (w : World) (s : Entity) (m : Mode) : Prop :=
  s = r ∧ ((w = a ∧ m = .dka) ∨ (w = b ∧ m = .dkb))

/-- The predicate calls in this bundle are the unchanged imported definitions. -/
def ExactSourceSchemas : Prop :=
  SourceIdentity.Necessary Ex u ∧ SourceIdentity.UniformRoot Ex Dep u ∧ SourceIdentity.GenericReception Ex Dep ∧
  (∀ w x, Ex w x → ¬ SourceIdentity.Necessary Ex x → SourceIdentity.Received Dep w x) ∧
  (∀ w x, SourceIdentity.Root Ex Dep w x ↔ x = u) ∧
  (∀ w, ∃ x, Complete w u x) ∧
  (∀ w, ProductiveCompleteness.HistoryComplete (Complete w) (ModeOf w) (Accounts w)) ∧
  (∀ w, ProductiveCompleteness.UnborrowedActs (Proper w) (Accounts w)) ∧
  (∀ w, ProductiveCompleteness.ProductiveWitness (Complete w) (ModeOf w) (Proper w))

/-- Truth linkage and local ownership are inputs preserved by this extension. -/
def CognitiveInterpretation : Prop :=
  Knows a r p ∧ Knows b r p ∧ Owns a r ka ∧ Owns b r kb ∧
  (∀ w s p', Knows w s p' → Ex w s ∧ Truth p' ∧
    ∃ k, Owns w s k ∧ ThoughtContent k p') ∧
  (∀ w s k, Owns w s k → Ex w s ∧ Ex w k) ∧
  (∀ w p', ¬ Knows w u p') ∧ (∀ w k, ¬ Owns w u k) ∧
  Truth p ∧ ¬ Truth q

set_option synthInstance.maxSize 4096
set_option maxRecDepth 10000
set_option maxHeartbeats 2000000

theorem exact_source_schemas : ExactSourceSchemas := by
  simp only [ExactSourceSchemas, SourceIdentity.Necessary,
    SourceIdentity.UniformRoot, SourceIdentity.Root, SourceIdentity.Received,
    SourceIdentity.GenericReception, ProductiveCompleteness.HistoryComplete,
    ProductiveCompleteness.UnborrowedActs, ProductiveCompleteness.ProductiveWitness,
    Complete, Dep, Ex, ModeOf, Proper, Accounts, Original]
  decide

theorem cognitive_interpretation : CognitiveInterpretation := by
  simp only [CognitiveInterpretation, Knows, Owns, Ex, Truth, ThoughtContent]
  decide


/-- Additional checks keep the exact finite interpretation nonvacuous and factive. -/
def RelationalSanity : Prop :=
  (∀ x, x ≠ u → ¬ SourceIdentity.Necessary Ex x) ∧
  (Ex a r ∧ Ex b r ∧ SourceIdentity.Received Dep a r ∧
    SourceIdentity.Received Dep b r) ∧
  (∀ w s x, Dep w s x → Ex w s ∧ Ex w x) ∧
  (∀ w x m, ModeOf w x m → Ex w x) ∧
  (∀ w s m, Proper w s m ∨ Accounts w s m → Ex w s ∧
    ∃ x, ModeOf w x m) ∧
  (∀ w s m, LocalActivity w s m → Accounts w u m ∧ ¬ Proper w s m) ∧
  (LocalActivity a r .dka ∧ LocalActivity b r .dkb)

theorem relational_sanity : RelationalSanity := by
  simp only [RelationalSanity, SourceIdentity.Necessary, SourceIdentity.Received,
    Ex, Dep, ModeOf, Proper, Accounts, Original, LocalActivity]
  decide

/-- Well-foundedness of the modal union, stronger than checking each world. -/
theorem possible_dependence_wellFounded :
    WellFounded (fun y x => ∃ w, Dep w y x) := by
  refine ⟨fun x => Acc.intro x ?_⟩
  intro y hy
  obtain ⟨w, hy⟩ := hy
  have hey : y = u := hy.1
  subst y
  refine Acc.intro u ?_
  intro predecessor hz
  obtain ⟨v, hz⟩ := hz
  exact False.elim (hz.2.2 rfl)

theorem each_world_dependence_wellFounded (w : World) : WellFounded (Dep w) := by
  apply possible_dependence_wellFounded.mono
  intro y x h
  exact ⟨w, h⟩

/-- Apply the retained necessity/reception theorem, not a substitute theorem. -/
theorem uniform_source_via_retained_theorem : SourceIdentity.UniformRoot Ex Dep u := by
  obtain ⟨_, hroot, hgeneric, hreceives, _⟩ := exact_source_schemas
  exact SourceIdentity.uniform_of_contingent_reception Ex Dep a u
    (hroot a) (hreceives a) hgeneric

/-- Actual overlapping complete ultimate sources coincide in this instance. -/
theorem complete_sources_coincide (w : World) (s t x : Entity)
    (hs : Complete w s x) (ht : Complete w t x) : s = t := by
  obtain ⟨_, _, _, _, _, _, hc, hu, hw⟩ := exact_source_schemas
  exact ProductiveCompleteness.uniqueness_of_history_complete
    (Complete w) (ModeOf w) (Proper w) (Accounts w) (hc w) (hu w) (hw w) hs ht

/-- A single joint result: exact imported schemas and granted local cognition,
with no source Knowledge or source ownership, plus worldwise/modal foundation. -/
theorem joint_relative_interpretation :
    ExactSourceSchemas ∧ CognitiveInterpretation ∧ RelationalSanity ∧
    WellFounded (fun y x => ∃ w, Dep w y x) ∧
    (∀ w, WellFounded (Dep w)) :=
  ⟨exact_source_schemas, cognitive_interpretation, relational_sanity,
    possible_dependence_wellFounded, each_world_dependence_wellFounded⟩

/-- Direct readback exposes the positive local facts and source noncognition. -/
theorem exact_schemas_with_recipient_knowledge_without_source_knowledge :
    ExactSourceSchemas ∧ Knows a r p ∧ Owns a r ka ∧
    (∀ w p', ¬ Knows w u p') ∧ (∀ w k, ¬ Owns w u k) := by
  refine ⟨exact_source_schemas, ?_⟩
  simp only [Knows, Owns]
  decide

/-- No original/derivative distinction is erased by mental ownership. -/
def PromotedProper (w : World) (s : Entity) (m : Mode) : Prop :=
  Proper w s m ∨ LocalActivity w s m

theorem promoting_local_activity_breaks_unborrowed :
    ¬ ProductiveCompleteness.UnborrowedActs (PromotedProper a) (Accounts a) := by
  intro h
  have hp : PromotedProper a r .dka := by
    simp only [PromotedProper, Proper, LocalActivity, modeWorld, Original]
    decide
  have ha : Accounts a u .dka := by
    simp only [Accounts, modeWorld]
    decide
  have he : u = r := h u r .dka hp ha
  cases he

section PositiveRoute

variable {S M X P : Type*}

/-- Exact positive criterion. If a genuinely cognitive subject t has an
unborrowed proper exercise among a target's productive modes, its complete
ultimate source s is t. Mere local cognitive ownership is not this premise. -/
theorem identity_and_knowledge_of_unborrowed_exercise
    (complete : S → X → Prop) (modeOf : X → M → Prop)
    (proper accounts : S → M → Prop) (knows : S → P → Prop)
    (closure : ProductiveCompleteness.HistoryComplete complete modeOf accounts)
    (unborrowed : ProductiveCompleteness.UnborrowedActs proper accounts)
    {s t : S} {x : X} {m : M} {p' : P}
    (hs : complete s x) (hm : modeOf x m) (ht : proper t m)
    (hk : knows t p') : s = t ∧ knows s p' := by
  have identity : s = t := unborrowed s t m ht (closure s x m hs hm)
  exact ⟨identity, identity.symm ▸ hk⟩

/-- If both are complete sources of the same target, use the actual imported
uniqueness theorem to transport the cognitive predicate along bearer identity. -/
theorem knowledge_via_retained_uniqueness
    (complete : S → X → Prop) (modeOf : X → M → Prop)
    (proper accounts : S → M → Prop) (knows : S → P → Prop)
    (closure : ProductiveCompleteness.HistoryComplete complete modeOf accounts)
    (unborrowed : ProductiveCompleteness.UnborrowedActs proper accounts)
    (witness : ProductiveCompleteness.ProductiveWitness complete modeOf proper)
    {s t : S} {x : X} {p' : P}
    (hs : complete s x) (ht : complete t x) (hk : knows t p') :
    s = t ∧ knows s p' := by
  have identity := ProductiveCompleteness.uniqueness_of_history_complete
    complete modeOf proper accounts closure unborrowed witness hs ht
  exact ⟨identity, identity.symm ▸ hk⟩

end PositiveRoute

#print axioms exact_source_schemas
#print axioms cognitive_interpretation
#print axioms relational_sanity
#print axioms possible_dependence_wellFounded
#print axioms each_world_dependence_wellFounded
#print axioms uniform_source_via_retained_theorem
#print axioms complete_sources_coincide
#print axioms joint_relative_interpretation
#print axioms exact_schemas_with_recipient_knowledge_without_source_knowledge
#print axioms promoting_local_activity_breaks_unborrowed
#print axioms identity_and_knowledge_of_unborrowed_exercise
#print axioms knowledge_via_retained_uniqueness

end Orthemology.Tranche5.KnowledgeScope
