import Mathlib.Data.Finset.Powerset
import Mathlib.Data.List.FinRange
import Mathlib.Data.Rat.Defs
import Mathlib.Tactic

open scoped BigOperators
namespace Orthemology.Tranche4.RationalWinning

/-- Fin-indexed tables make every range explicit and canonically enumerable.
Public menus may depend on the entire finite live support. -/
structure Tables (models actions observations : ℕ) where
  kernel : Fin models → Fin actions → Fin observations → ℚ
  good : Fin models → Finset (Fin actions)
  menu : Finset (Fin models) → Finset (Fin actions)

variable {m k l : ℕ}

/-- Primitive rational addition avoids a noncomputable algebraic-instance dependency. -/
def listTotal (f : Fin l → ℚ) : List (Fin l) → ℚ
  | [] => 0
  | y::ys => f y + listTotal f ys

def rowTotal (T : Tables m k l) (θ : Fin m) (a : Fin k) : ℚ :=
  listTotal (T.kernel θ a) (List.finRange l)

def validTable (T : Tables m k l) : Bool :=
  decide (∀ θ a, (∀ y, 0 ≤ T.kernel θ a y) ∧ rowTotal T θ a = 1)

def update (T : Tables m k l) (B : Finset (Fin m)) (a : Fin k) (y : Fin l) : Finset (Fin m) :=
  B.filter (fun θ => 0 < T.kernel θ a y)

/-- Deterministic finite support enumeration, avoiding Finset.toList and choice. -/
def enumerateSupports {A : Type*} [DecidableEq A] : List A → List (Finset A)
  | [] => [∅]
  | a::as => let tail := enumerateSupports as
             tail ++ tail.map (fun U => insert a U)

def supportOptions (actions : ℕ) : List (Finset (Fin actions)) :=
  enumerateSupports (List.finRange actions)

/-- All nonempty proper observation successors must pass. Same-support and
empty successors do not recurse. This predicate is common to every candidate. -/
def admissible (T : Tables m k l) (next : Finset (Fin m) → Bool)
    (B : Finset (Fin m)) (a : Fin k) : Bool :=
  decide (a ∈ T.menu B ∧ ∀ y, (update T B a y).Nonempty →
    ¬ B ⊆ update T B a y → next (update T B a y) = true)

def verifies (T : Tables m k l) (B : Finset (Fin m)) (θ : Fin m) (U : Finset (Fin k)) : Prop :=
  U ⊆ T.good θ ∧ ∀ η ∈ B, (∀ a ∈ U, ∀ y, T.kernel θ a y = T.kernel η a y) → U ⊆ T.good η

instance verifiesDecidable (T : Tables m k l) (B : Finset (Fin m)) (θ : Fin m) (U : Finset (Fin k)) :
    Decidable (verifies T B θ U) := by unfold verifies; infer_instance

/-- Explicit finite search avoids the generic existential decider's choice dependency. -/
def progresses (T : Tables m k l) (B : Finset (Fin m)) (θ : Fin m) (U : Finset (Fin k)) : Bool :=
  (List.finRange k).any (fun a => decide (a ∈ U) &&
    (List.finRange l).any (fun y => decide (¬ B ⊆ update T B a y ∧ 0 < T.kernel θ a y)))

def planCheck (T : Tables m k l) (next : Finset (Fin m) → Bool)
    (B : Finset (Fin m)) (θ : Fin m) (U : Finset (Fin k)) : Bool :=
  decide (U.Nonempty ∧ (∀ a ∈ U, admissible T next B a = true) ∧
    (progresses T B θ U = true ∨ verifies T B θ U))

/-- Bounded recursion depth; callers use fuel=the live-support cardinality. -/
def wins (T : Tables m k l) : ℕ → Finset (Fin m) → Bool
  | 0, _ => false
  | fuel+1, B => decide B.Nonempty &&
      decide (∀ θ ∈ B, (supportOptions k).any (planCheck T (wins T fuel) B θ) = true)

/-- First successful support in a fixed finite enumeration. -/
def selectedSupport (T : Tables m k l) (fuel : ℕ) (B : Finset (Fin m)) (θ : Fin m) :
    Option (Finset (Fin k)) :=
  if θ ∈ B then (supportOptions k).find? (planCheck T (wins T fuel) B θ) else none

/-- Deterministic action order for a selected support; no classical list conversion. -/
def orderedActions (U : Finset (Fin k)) : List (Fin k) :=
  (List.finRange k).filter (fun a => decide (a ∈ U))

def selectedActions (T : Tables m k l) (fuel : ℕ) (B : Finset (Fin m)) (θ : Fin m) :
    Option (List (Fin k)) := (selectedSupport T fuel B θ).map orderedActions

inductive Decision where
  | invalid
  | emptySupport
  | losing
  | winning
  deriving DecidableEq, Repr

/-- Invalid probability tables are distinguished from a valid losing instance. -/
def decideWinning (T : Tables m k l) (B : Finset (Fin m)) : Decision :=
  if validTable T then
    (if B.Nonempty then (if wins T B.card B then .winning else .losing) else .emptySupport)
  else .invalid

/-- Public witness extraction is gated by a validated nonempty winning input. -/
def winningPlan (T : Tables m k l) (B : Finset (Fin m)) (θ : Fin m) : Option (List (Fin k)) :=
  if decideWinning T B = .winning then selectedActions T (B.card-1) B θ else none

end Orthemology.Tranche4.RationalWinning
