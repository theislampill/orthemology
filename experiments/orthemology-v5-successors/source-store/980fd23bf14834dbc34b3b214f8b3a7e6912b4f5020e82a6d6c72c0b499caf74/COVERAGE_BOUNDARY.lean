import Mathlib

/-!
# Productive coverage is stronger than local orthability

The finite control computes actual outputs from two cooperative partial powers.
The middle/joint token is genuinely produced; it is not a hole with no source.
No token has two individually complete sources. The control is against deriving
whole-field coverage from weaker premises, not against two sources after the
complete-unconditioned-universal role has been granted.

The general envelope theorem gives exact minimality relative to the declared
unary prerequisite propagation mechanism, not an absolutely weakest metaphysical
premise. No claim of general mathematical novelty or metaphysical possibility.
-/

namespace Orthemology.Tranche3.CoverageBoundary

inductive Source where
  | a | b
  deriving DecidableEq, Fintype, Repr

inductive Token where
  | evaluation | auxiliary | joint
  deriving DecidableEq, Fintype, Repr

open Source Token

abbrev World := Source → Bool

/-- Worlds vary exercises, not the existence of these two partial enablers. -/
abbrev SourceExists (_w : World) (_s : Source) : Prop := True

def actual : World := fun _ => true

def available (U : Finset Source) : World := fun s => decide (s ∈ U)

abbrev Payload : Token → Type
  | evaluation => ℕ
  | auxiliary => Bool
  | joint => ℕ × Bool

def evaluationOutput (w : World) : Option ℕ :=
  if w a then some (2 + 2) else none

def auxiliaryOutput (w : World) : Option Bool :=
  if w b then some true else none

/-- The joint output is assembled from both actual inputs. This is conjunctive
cooperation, not two separate complete productions of the same whole token. -/
def output (w : World) : (t : Token) → Option (Payload t)
  | evaluation => evaluationOutput w
  | auxiliary => auxiliaryOutput w
  | joint => do
      let x ← evaluationOutput w
      let y ← auxiliaryOutput w
      pure (x, y)

abbrev ExistsToken (w : World) (t : Token) : Prop := (output w t).isSome = true

abbrev Provides (U : Finset Source) (t : Token) : Prop := ExistsToken (available U) t

abbrev Complete (s : Source) (t : Token) : Prop := Provides {s} t

def requirements : Token → Finset Source
  | evaluation => {a}
  | auxiliary => {b}
  | joint => {a, b}

abbrev Needs (x y : Token) : Prop :=
  x = joint ∧ (y = evaluation ∨ y = auxiliary)

instance : DecidableRel Needs := fun _ _ => inferInstance

theorem provides_iff_requirements (U : Finset Source) (t : Token) :
    Provides U t ↔ requirements t ⊆ U := by
  cases t <;> by_cases ha : a ∈ U <;> by_cases hb : b ∈ U <;>
    simp [Provides, ExistsToken, output, available, evaluationOutput,
      auxiliaryOutput, requirements, ha, hb, Finset.insert_subset_iff]

theorem actual_outputs :
    output actual evaluation = some 4 ∧
    output actual auxiliary = some true ∧
    output actual joint = some (4, true) := by
  decide

/-- Truth is the standard arithmetic equality, not whatever the output says. -/
theorem actual_evaluation_correct :
    output actual evaluation = some 4 ∧ (2 + 2 : ℕ) = 4 ∧ (2 + 2 : ℕ) ≠ 5 := by
  decide

theorem enablers_exist_necessarily : ∀ s w, SourceExists w s := by
  intro s w
  trivial

theorem every_actual_token_produced :
    ∀ t, ExistsToken actual t ∧ Provides {a, b} t := by
  decide

theorem local_but_not_universal :
    Complete a evaluation ∧ ¬ Complete a auxiliary ∧ ¬ Complete a joint := by
  decide

theorem no_individual_complete_for_joint : ∀ s, ¬ Complete s joint := by
  decide

theorem no_universal_individual : ¬ ∃ s, ∀ t, Complete s t := by
  decide

theorem local_exclusive :
    ∀ s r t, Complete s t → Complete r t → s = r := by
  decide

theorem prerequisite_closed :
    ∀ s x y, Complete s x → Needs x y → Complete s y := by
  decide

/-- Every field token is either the common hub or adjacent to it. Thus the
undirected prerequisite graph is connected despite the missing single-source
coverage of the actually produced joint token. -/
theorem connected_hub : ∀ t, t = joint ∨ Needs joint t := by
  decide

/-- Both source exercises are indispensable to the actual joint production. -/
theorem genuine_cooperation :
    output (available {a}) joint = none ∧
    output (available {b}) joint = none ∧
    output (available {a, b}) joint = some (4, true) := by
  decide

/-- Existing enablers can withhold activity; derivative tokens are contingent.
No impossible absence of a necessarily existing bearer is used. -/
theorem effects_contingent :
    ∀ t, ExistsToken actual t ∧ ¬ ExistsToken (fun _ => false) t := by
  decide

abbrev Node := Source ⊕ Token

abbrev NodeExists (w : World) : Node → Prop
  | Sum.inl s => SourceExists w s
  | Sum.inr t => ExistsToken w t

abbrev Origin (w : World) : Node → Node → Prop
  | Sum.inl s, Sum.inr t => w s = true ∧ s ∈ requirements t ∧ ExistsToken w t
  | Sum.inr x, Sum.inr y => Needs y x ∧ ExistsToken w x ∧ ExistsToken w y
  | _, _ => False

instance nodeExistsDecidable (w : World) (x : Node) : Decidable (NodeExists w x) := by
  cases x <;> simp only [NodeExists, SourceExists] <;> infer_instance

instance originDecidable (w : World) (x y : Node) : Decidable (Origin w x y) := by
  cases x <;> cases y <;> simp only [Origin] <;> infer_instance

def rank : Node → ℕ
  | Sum.inl _ => 0
  | Sum.inr evaluation => 1
  | Sum.inr auxiliary => 1
  | Sum.inr joint => 2

theorem source_roots_necessary :
    ∀ s, (∀ w, NodeExists w (Sum.inl s)) ∧
      (∀ w x, ¬ Origin w x (Sum.inl s)) := by
  decide

theorem origin_factive :
    ∀ w x y, Origin w x y → NodeExists w x ∧ NodeExists w y := by
  decide

theorem origin_strict_rank :
    ∀ w x y, Origin w x y → rank x < rank y := by
  decide

/-- Even the actual contingent-source principle can be retained. It does not
convert either necessary partial root into a universal complete source. -/
theorem actual_contingent_source_principle :
    ∀ x, NodeExists actual x → ¬ (∀ w, NodeExists w x) →
      ∃ y, Origin actual y x := by
  decide

theorem generic_reception_retained :
    ∀ x, (∃ w y, Origin w y x) → ∀ v, NodeExists v x → ∃ y, Origin v y x := by
  decide

section Envelope

variable {V : Type*}

inductive InEnvelope (seed : Set V) (requires : V → V → Prop) : V → Prop
  | initial {x} : seed x → InEnvelope seed requires x
  | prerequisite {x y} : InEnvelope seed requires x → requires x y →
      InEnvelope seed requires y

def ClosedUnder (requires : V → V → Prop) (C : Set V) : Prop :=
  ∀ x y, C x → requires x y → C y

theorem envelope_closed (seed : Set V) (requires : V → V → Prop) :
    ClosedUnder requires (InEnvelope seed requires) := by
  intro x y hx hxy
  exact InEnvelope.prerequisite hx hxy

theorem envelope_least (seed C : Set V) (requires : V → V → Prop)
    (initial : seed ⊆ C) (closed : ClosedUnder requires C) :
    ∀ x, InEnvelope seed requires x → C x := by
  intro x hx
  induction hx with
  | initial h => exact initial h
  | prerequisite h hxy ih => exact closed _ _ ih hxy

/-- Exactly the extra scope fact needed by this propagation mechanism.
It says which actualities lie in the prerequisite envelope; it contains no
source, completeness, or necessity predicate. -/
theorem universal_propagation_iff_envelope
    (seed : Set V) (requires : V → V → Prop) :
    (∀ C : Set V, seed ⊆ C → ClosedUnder requires C → ∀ x, C x) ↔
      ∀ x, InEnvelope seed requires x := by
  constructor
  · intro h
    exact h (InEnvelope seed requires) (fun _ hx => InEnvelope.initial hx)
      (envelope_closed seed requires)
  · intro all_in C initial closed x
    exact envelope_least seed C requires initial closed x (all_in x)

theorem complete_on_field_of_envelope {S : Type*}
    (complete : S → V → Prop) (s : S) (seed : Set V)
    (requires : V → V → Prop)
    (initial : ∀ x, seed x → complete s x)
    (closed : ∀ x y, complete s x → requires x y → complete s y)
    (scope : ∀ x, InEnvelope seed requires x) :
    ∀ x, complete s x := by
  exact envelope_least seed (complete s) requires initial closed |> fun h x => h x (scope x)

end Envelope

theorem seed_evaluation_envelope_only :
    ∀ t, InEnvelope ({evaluation} : Set Token) Needs t → t = evaluation := by
  apply envelope_least ({evaluation} : Set Token) {evaluation} Needs
  · exact Set.Subset.refl _
  · intro x y hx hxy
    have he : x = evaluation := hx
    have hj : x = joint := hxy.1
    cases he.symm.trans hj

theorem connected_does_not_give_prerequisite_scope :
    (∀ t, t = joint ∨ Needs joint t) ∧
      ¬ (∀ t, InEnvelope ({evaluation} : Set Token) Needs t) := by
  refine ⟨connected_hub, ?_⟩
  intro h
  have hh := seed_evaluation_envelope_only auxiliary (h auxiliary)
  cases hh

#print axioms provides_iff_requirements
#print axioms actual_evaluation_correct
#print axioms every_actual_token_produced
#print axioms local_but_not_universal
#print axioms no_universal_individual
#print axioms local_exclusive
#print axioms prerequisite_closed
#print axioms genuine_cooperation
#print axioms effects_contingent
#print axioms source_roots_necessary
#print axioms origin_strict_rank
#print axioms actual_contingent_source_principle
#print axioms generic_reception_retained
#print axioms universal_propagation_iff_envelope
#print axioms complete_on_field_of_envelope
#print axioms connected_does_not_give_prerequisite_scope

end Orthemology.Tranche3.CoverageBoundary
