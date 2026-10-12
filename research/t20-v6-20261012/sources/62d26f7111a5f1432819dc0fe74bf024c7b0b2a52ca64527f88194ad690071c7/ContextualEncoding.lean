import Mathlib.Data.Nat.Basic

namespace T20Resumed.Language

inductive Person
  | speaker | addressee | named : Nat → Person
  deriving DecidableEq
inductive Instant
  | now | at : Nat → Instant
  deriving DecidableEq
structure Context where
  speaker : Nat
  addressee : Nat
  time : Nat
  deriving DecidableEq

def person (c : Context) : Person → Nat
  | .speaker => c.speaker
  | .addressee => c.addressee
  | .named n => n
def instant (c : Context) : Instant → Nat
  | .now => c.time
  | .at n => n

inductive Formula
  | at : Person → Nat → Instant → Formula
  | duty : Person → Nat → Instant → Nat → Formula
  | neg : Formula → Formula
  | conj : Formula → Formula → Formula
  deriving DecidableEq
inductive Proposition
  | at : Nat → Nat → Nat → Proposition
  | duty : Nat → Nat → Nat → Nat → Proposition
  | neg : Proposition → Proposition
  | conj : Proposition → Proposition → Proposition
  deriving DecidableEq

def resolve (c : Context) : Formula → Proposition
  | .at who place when_ => .at (person c who) place (instant c when_)
  | .duty who act start duration =>
      .duty (person c who) act (instant c start) (instant c start + duration)
  | .neg p => .neg (resolve c p)
  | .conj p q => .conj (resolve c p) (resolve c q)

/-- A distinct constructor/argument encoding, not a natural-language translator. -/
inductive EncodingB
  | located : Instant → Nat → Person → EncodingB
  | obligation : Nat → Instant → Nat → Person → EncodingB
  | negated : EncodingB → EncodingB
  | both : EncodingB → EncodingB → EncodingB
  deriving DecidableEq
def translate : Formula → EncodingB
  | .at who place when_ => .located when_ place who
  | .duty who act start duration => .obligation duration start act who
  | .neg p => .negated (translate p)
  | .conj p q => .both (translate p) (translate q)
def interpretB (c : Context) : EncodingB → Proposition
  | .located when_ place who => .at (person c who) place (instant c when_)
  | .obligation duration start act who =>
      .duty (person c who) act (instant c start) (instant c start + duration)
  | .negated p => .neg (interpretB c p)
  | .both p q => .conj (interpretB c p) (interpretB c q)

theorem compositional_contextual_translation (c : Context) (f : Formula) :
    interpretB c (translate f) = resolve c f := by
  induction f with
  | «at» => rfl
  | duty => rfl
  | neg f ih => simp only [translate, interpretB, resolve, ih]
  | conj f g ihf ihg => simp only [translate, interpretB, resolve, ihf, ihg]

inductive Force
  | assert | quote | directive
  deriving DecidableEq
structure OccurrenceA where
  event : Nat
  original : Context
  force : Force
  formula : Formula
structure ReceivedB where
  carrierEvent : Nat
  carrierContext : Context
  carrierForce : Force
  sourceEvent : Nat
  sourceContext : Context
  sourceForce : Force
  payload : EncodingB

def relay (o : OccurrenceA) (event : Nat) (ctx : Context) : ReceivedB :=
  ⟨event, ctx, .quote, o.event, o.original, o.force, translate o.formula⟩

theorem relay_preserves_source_act (o : OccurrenceA) (event : Nat) (ctx : Context) :
    let r := relay o event ctx
    r.sourceEvent = o.event ∧ r.sourceForce = o.force ∧
      interpretB r.sourceContext r.payload = resolve o.original o.formula ∧
      r.carrierForce = .quote := by
  exact ⟨rfl, rfl, compositional_contextual_translation o.original o.formula, rfl⟩

def c0 : Context := ⟨0, 1, 0⟩
def c1 : Context := ⟨2, 3, 1⟩
def indexedClaim : Formula := .at .speaker 5 .now
theorem same_formula_rebound_different_proposition :
    resolve c0 indexedClaim ≠ resolve c1 indexedClaim := by decide

/-- Explicit separating valuation, stronger than unequal metadata. -/
def valuation (p : Proposition) : Prop := p = .at 0 5 0
theorem changed_binding_changes_truth_in_a_valuation :
    valuation (resolve c0 indexedClaim) ∧ ¬ valuation (resolve c1 indexedClaim) := by
  unfold valuation
  decide

theorem quote_is_not_assertion : Force.quote ≠ Force.assert := by decide
theorem directive_is_not_assertion : Force.directive ≠ Force.assert := by decide

end T20Resumed.Language
