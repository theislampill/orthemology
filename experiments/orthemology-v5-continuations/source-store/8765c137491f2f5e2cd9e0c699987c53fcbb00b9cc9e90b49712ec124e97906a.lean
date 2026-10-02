import Mathlib

/-!
# History-inclusive productive completeness

This separates entire-actuality completeness from endpoint sufficiency.
`proper s m` means a particular unborrowed exercise of s's agency. It is
not assumed of every joint or creaturely action. `accounts` is ultimate
productive accounting, not thought ownership or mere propositional entailment.
-/

namespace Orthemology.Tranche3.ProductiveCompleteness

variable {S M X : Type*}

/-- Every actual productive mode of the target belongs to the source's
ultimate productive account. Whether this follows from a proposed use of
'complete' is precisely the substantive target-closure bridge. -/
def HistoryComplete (complete : S → X → Prop) (modeOf : X → M → Prop)
    (accounts : S → M → Prop) : Prop :=
  ∀ s x m, complete s x → modeOf x m → accounts s m

/-- An unborrowed proper exercise cannot ultimately be furnished by another
independent source. This is restricted to the agent's proper exercise, not
asserted of every event or every effect. -/
def UnborrowedActs (proper accounts : S → M → Prop) : Prop :=
  ∀ s t m, proper t m → accounts s m → s = t

/-- Actual sourcehood has an actual productive witness, not merely a
counterfactual sufficient-condition truth. -/
def ProductiveWitness (complete : S → X → Prop) (modeOf : X → M → Prop)
    (proper : S → M → Prop) : Prop :=
  ∀ s x, complete s x → ∃ m, modeOf x m ∧ proper s m

theorem uniqueness_of_history_complete
    (complete : S → X → Prop) (modeOf : X → M → Prop)
    (proper accounts : S → M → Prop)
    (closure : HistoryComplete complete modeOf accounts)
    (unborrowed : UnborrowedActs proper accounts)
    (witness : ProductiveWitness complete modeOf proper)
    {s t : S} {x : X} (hs : complete s x) (ht : complete t x) : s = t := by
  obtain ⟨m, hm, hproper⟩ := witness t x ht
  exact unborrowed s t m hproper (closure s x m hs hm)

/-- If complete scope already includes all actual productive modes,
connectedness of the produced domains is not required for this implication.
The universal scope is an independent assumption, not inferred from a finite
connected domain. -/
theorem uniqueness_of_universal_activity_scope
    (source : S → Prop) (proper accounts : S → M → Prop)
    (universal : ∀ s, source s → ∀ m, accounts s m)
    (unborrowed : UnborrowedActs proper accounts)
    (witness : ∀ s, source s → ∃ m, proper s m)
    {s t : S} (hs : source s) (ht : source t) : s = t := by
  obtain ⟨m, hm⟩ := witness t ht
  exact unborrowed s t m hm (universal s hs m)

namespace Controls

/-- A bare two-endpoint-arrow diagram can satisfy unique unborrowed act
ownership and actual witnesses while failing history-inclusive completeness.
It is not a model of the stronger complete ultimate-source role. -/
def endpointOnly (_ : Bool) (_ : Unit) : Prop := True

def everyMode (_ : Unit) (_ : Bool) : Prop := True

def ownMode (s m : Bool) : Prop := s = m

theorem endpoint_sufficiency_does_not_give_history_closure :
    UnborrowedActs ownMode ownMode ∧
    ProductiveWitness endpointOnly everyMode ownMode ∧
    endpointOnly false () ∧ endpointOnly true () ∧
    ¬ HistoryComplete endpointOnly everyMode ownMode := by
  simp only [UnborrowedActs, ProductiveWitness, HistoryComplete,
    endpointOnly, everyMode, ownMode]
  decide

end Controls

#print axioms uniqueness_of_history_complete
#print axioms uniqueness_of_universal_activity_scope
#print axioms Controls.endpoint_sufficiency_does_not_give_history_closure

end Orthemology.Tranche3.ProductiveCompleteness
