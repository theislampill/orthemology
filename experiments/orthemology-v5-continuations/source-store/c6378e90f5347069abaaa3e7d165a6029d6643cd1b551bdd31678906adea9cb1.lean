import KnowledgeScope

/-!
# Complete self-determination and knowledge of an effect

Generic epistemic closure is explicit. The finite information model checks
determination by a complete act versus generic standing nature. It neither
infers cognition from information nor establishes an essence theory.
-/

namespace Orthemology.Tranche6.CreativeKnowledge

section Generic
variable {P : Type*}

/-- Positive epistemic consequence, with the needed closure visible. -/
theorem effect_knowledge_of_known_complete_act
    (K : P → Prop) (imp : P → P → P)
    (closed : ∀ A X, K (imp A X) → K A → K X)
    (A X : P) (knownAct : K A) (knownEfficacy : K (imp A X)) : K X :=
  closed A X knownEfficacy knownAct

variable {W S E : Type*}

/-- An epistemic range; semantic cognition is not inferred from this relation. -/
def DeterminedBy (self : W → S) (w : W) (p : W → Prop) : Prop :=
  ∀ v, self v = self w → p v

/-- A fixed complete productive determination fixes its output across the
epistemic range. This is not a claim that the determination is necessary. -/
theorem effect_determined_by_complete_state
    (self : W → S) (produce : S → E) (w : W) :
    DeterminedBy self w (fun v => produce (self v) = produce (self w)) := by
  intro v h
  rw [h]

end Generic

open Orthemology.Tranche5.KnowledgeScope
open World

inductive Effect | recipient | other deriving DecidableEq, Fintype
inductive Act | createRecipient | createOther deriving DecidableEq, Fintype

def StandingNature (_ : World) : Unit := ()

def actualAct : World → Act
  | a | b => .createRecipient
  | c => .createOther

def produce : Act → Effect
  | .createRecipient => .recipient
  | .createOther => .other

def actualEffect (w : World) : Effect := produce (actualAct w)

set_option synthInstance.maxSize 4096
set_option maxRecDepth 10000
set_option maxHeartbeats 2000000

theorem complete_act_determines_effect :
    ∀ w, DeterminedBy actualAct w (fun v => actualEffect v = actualEffect w) :=
  effect_determined_by_complete_state actualAct produce

theorem generic_nature_does_not_determine_actual_effect :
    ¬ DeterminedBy StandingNature a (fun v => actualEffect v = .recipient) := by
  simp only [DeterminedBy, StandingNature, actualEffect, actualAct, produce]
  decide

theorem same_nature_different_acts_and_effects :
    StandingNature a = StandingNature c ∧ actualAct a ≠ actualAct c ∧
    actualEffect a ≠ actualEffect c := by
  simp only [StandingNature, actualAct, actualEffect, produce]
  decide

/-- Factivity of the information constraint; this alone is not Knowledge. -/
theorem determined_factive {W S : Type*} (self : W → S) (w : W) (p : W → Prop)
    (h : DeterminedBy self w p) : p w := h w rfl

/-- Closure under a known implication in the idealized epistemic range. -/
theorem determined_closed {W S : Type*} (self : W → S) (w : W)
    (p q : W → Prop)
    (hpq : DeterminedBy self w (fun v => p v → q v))
    (hp : DeterminedBy self w p) : DeterminedBy self w q := by
  intro v h
  exact hpq v h (hp v h)

#print axioms effect_knowledge_of_known_complete_act
#print axioms effect_determined_by_complete_state
#print axioms complete_act_determines_effect
#print axioms generic_nature_does_not_determine_actual_effect
#print axioms same_nature_different_acts_and_effects
#print axioms determined_factive
#print axioms determined_closed

end Orthemology.Tranche6.CreativeKnowledge
