import KnowledgeScope

/-!
# Actual original-giver priority and the modal recipient gap

This imports the exact retained source relations and the fifth finite types.
Only the cognitive interpretation is extended. The old Knows table is used
solely for its recipient entries, not as a full interpretation of the new
source's cognition. No metaphysical possibility is certified.

The three-world source is active in every world. It knows in a and b; its
dependent knowing recipient present there. In c it produces z, which does not
know, and the source has no cognition. Worldwise actual-giver priority holds.
Actual Knowledge, necessary source existence, possible cognitive production
from every world, and no external source of the source do not force standing
Knowledge. Intrinsic determination is a strictly stronger premise.
-/

namespace Orthemology.Tranche6.ModalKnowledge

open Orthemology.Tranche5
open KnowledgeScope KnowledgeScope.World KnowledgeScope.Entity KnowledgeScope.Content
open Orthemology.Tranche3

/-- A contingent intrinsic state, not a second external supplier. -/
def Active (w : World) : Prop := w = a ∨ w = b

/-- Conceded source cognition at a and b, together with the retained recipient
entries. The finite table does not infer consciousness from a computation. -/
def Knows (w : World) (s : Entity) (content : Content) : Prop :=
  KnowledgeScope.Knows w s content ∨ (s = u ∧ Active w ∧ KnowledgeScope.Truth content)

def HasKnowledge (w : World) (s : Entity) : Prop := ∃ content, Knows w s content

/-- This is existential cognitive-perfection priority, not omniscient transfer
of every content known by a recipient. -/
def ActualGiverPriority : Prop :=
  ∀ w x, KnowledgeScope.Complete w u x → HasKnowledge w x → HasKnowledge w u

def StandingKnowledge : Prop := ∀ w, HasKnowledge w u

/-- All represented alternatives are accessible. Possible giving is weaker
than present exercise or standing actual cognition. -/
def Accessible (_ _ : World) : Prop := True

def PossibleCognitiveGiving (w : World) : Prop :=
  ∃ v x, Accessible w v ∧ KnowledgeScope.Complete v u x ∧ HasKnowledge v x

/-- Same response law across worlds; its intrinsic activation input varies. -/
def StableResponseLaw : Prop :=
  ∀ w, HasKnowledge w u ↔ Active w

set_option synthInstance.maxSize 4096
set_option maxRecDepth 10000
set_option maxHeartbeats 2000000

theorem actual_giver_priority : ActualGiverPriority := by
  simp only [ActualGiverPriority, HasKnowledge, Knows, KnowledgeScope.Knows,
    KnowledgeScope.Complete, KnowledgeScope.Dep, KnowledgeScope.Ex, KnowledgeScope.Truth, Active]
  decide

theorem cognitive_factivity :
    ∀ w s content, Knows w s content → KnowledgeScope.Ex w s ∧ KnowledgeScope.Truth content := by
  simp only [Knows, KnowledgeScope.Knows, KnowledgeScope.Ex, KnowledgeScope.Truth, Active]
  decide

theorem recipient_and_source_actually_know :
    Knows a r p ∧ Knows a u p := by
  simp only [Knows, KnowledgeScope.Knows, KnowledgeScope.Truth, Active]
  decide

theorem source_not_standing : ¬ StandingKnowledge := by
  simp only [StandingKnowledge, HasKnowledge, Knows, KnowledgeScope.Knows,
    KnowledgeScope.Truth, Active]
  decide

theorem possible_giving_at_every_world : ∀ w, PossibleCognitiveGiving w := by
  simp only [PossibleCognitiveGiving, Accessible, KnowledgeScope.Complete, KnowledgeScope.Dep, KnowledgeScope.Ex,
    HasKnowledge, Knows, KnowledgeScope.Knows, KnowledgeScope.Truth, Active]
  decide

theorem stable_response_law : StableResponseLaw := by
  simp only [StableResponseLaw, HasKnowledge, Knows, KnowledgeScope.Knows, KnowledgeScope.Truth, Active]
  decide

/-- c is not an empty or inactive-source world. -/
theorem source_still_productive_at_c :
    KnowledgeScope.Complete c u z ∧ KnowledgeScope.ModeOf c z .cz ∧ KnowledgeScope.Proper c u .cz := by
  simp only [KnowledgeScope.Complete, KnowledgeScope.Dep, KnowledgeScope.Ex, KnowledgeScope.ModeOf, KnowledgeScope.modeWorld, KnowledgeScope.modeTarget,
    KnowledgeScope.Proper, KnowledgeScope.Original]
  decide

theorem knowledge_not_recipient_thought_ownership :
    Knows a u p ∧ KnowledgeScope.Owns a r ka ∧ ¬ KnowledgeScope.Owns a u ka := by
  simp only [Knows, KnowledgeScope.Knows, KnowledgeScope.Truth, Active, KnowledgeScope.Owns]
  decide

/-- Nonvacuous strengthening of the fifth interpretation: actual source K
and worldwise giver priority are added, but standing K still does not follow. -/
theorem exact_sources_with_giver_priority_without_standing :
    KnowledgeScope.ExactSourceSchemas ∧ KnowledgeScope.RelationalSanity ∧
    (∀ w s content, Knows w s content → KnowledgeScope.Ex w s ∧ KnowledgeScope.Truth content) ∧
    Knows a r p ∧ Knows a u p ∧ ActualGiverPriority ∧
    (∀ w, PossibleCognitiveGiving w) ∧ StableResponseLaw ∧
    KnowledgeScope.Complete c u z ∧ ¬ StandingKnowledge := by
  exact ⟨KnowledgeScope.exact_source_schemas, KnowledgeScope.relational_sanity, cognitive_factivity,
    recipient_and_source_actually_know.1, recipient_and_source_actually_know.2,
    actual_giver_priority, possible_giving_at_every_world, stable_response_law,
    source_still_productive_at_c.1, source_not_standing⟩

section PositiveConditionals
variable {W S X : Type*}

/-- An actual effect activates the explicitly cognitive priority rule. -/
theorem actual_knowledge_of_giver_priority
    (complete : W → S → X → Prop) (cognitiveEffect : W → X → Prop)
    (knows : W → S → Prop)
    (priority : ∀ w s x, complete w s x → cognitiveEffect w x → knows w s)
    {w : W} {s : S} {x : X}
    (hc : complete w s x) (hk : cognitiveEffect w x) : knows w s :=
  priority w s x hc hk

/-- With worldwise recipients, priority does give worldwise Knowledge.
This records the missing antecedent, not a claim that all worlds contain them. -/
theorem standing_of_everywhere_cognitive_giving
    (complete : W → S → X → Prop) (cognitiveEffect : W → X → Prop)
    (knows : W → S → Prop) (s : S)
    (priority : ∀ w x, complete w s x → cognitiveEffect w x → knows w s)
    (giving : ∀ w, ∃ x, complete w s x ∧ cognitiveEffect w x) :
    ∀ w, knows w s := by
  intro w
  obtain ⟨x, hc, hk⟩ := giving w
  exact priority w x hc hk

/-- A complete standing-nature determinant is a distinct sufficient route. -/
theorem standing_of_intrinsic_determination
    (present nature knows : W → S → Prop) (s : S)
    (necessary : ∀ w, present w s)
    (naturePresent : ∀ w, present w s → nature w s)
    (intrinsicDetermination : ∀ w, nature w s → knows w s) :
    ∀ w, knows w s := by
  intro w
  exact intrinsicDetermination w (naturePresent w (necessary w))

end PositiveConditionals

#print axioms actual_giver_priority
#print axioms cognitive_factivity
#print axioms recipient_and_source_actually_know
#print axioms source_not_standing
#print axioms possible_giving_at_every_world
#print axioms stable_response_law
#print axioms source_still_productive_at_c
#print axioms knowledge_not_recipient_thought_ownership
#print axioms exact_sources_with_giver_priority_without_standing
#print axioms actual_knowledge_of_giver_priority
#print axioms standing_of_everywhere_cognitive_giving
#print axioms standing_of_intrinsic_determination

end Orthemology.Tranche6.ModalKnowledge
