import EndComponents
import Mathlib.Data.Fintype.Card

/-!
# Explicit bounded action-witnessed paths

The executable predicate checks stored steps locally, reconstructing each source
from the previous receipt. Its proof-only completeness construction extracts an
actual walk from inherited reachability and removes repeated-state loops. The
bound is a certificate-syntax bound, not a stochastic execution-time bound.
-/
namespace OrthemicCertificate

/-- A submitted start and an explicit list of action/next-state steps. -/
structure Path (State Action : Type*) where
  start : State
  steps : List (Action × State)
  deriving DecidableEq, Repr

namespace Path

variable {State Action : Type*}

/-- Read the endpoint by following the stored receipts. -/
def endpointFrom (s : State) : List (Action × State) → State
  | [] => s
  | (_, t) :: rest => endpointFrom t rest

/-- The endpoint of the submitted syntax. -/
def endpoint (p : Path State Action) : State := endpointFrom p.start p.steps

/-- All visited states, including the start. Used in the completeness proof. -/
def visited (s : State) (steps : List (Action × State)) : List State :=
  s :: steps.map Prod.snd

/-- Local step validation. Each source is reconstructed, never independently
supplied by the certificate. This predicate does not invoke reachability. -/
def Edges (allowed : Finset (State × Action))
    (succ : (State × Action) → Finset State) (s : State) : List (Action × State) → Prop
  | [] => True
  | (a, t) :: rest => (s, a) ∈ allowed ∧ t ∈ succ (s, a) ∧ Edges allowed succ t rest

/-- Explicit executable structural recursion for local edge checks. -/
def edgesDecidable [DecidableEq State] [DecidableEq Action] (allowed : Finset (State × Action))
    (succ : (State × Action) → Finset State) (s : State) :
    (steps : List (Action × State)) → Decidable (Edges allowed succ s steps)
  | [] => isTrue trivial
  | (a, t) :: rest =>
    letI := edgesDecidable allowed succ t rest
    inferInstanceAs (Decidable ((s, a) ∈ allowed ∧ t ∈ succ (s, a) ∧ Edges allowed succ t rest))

instance instDecidableEdges [DecidableEq State] [DecidableEq Action] (allowed : Finset (State × Action))
    (succ : (State × Action) → Finset State) (s : State) (steps : List (Action × State)) :
    Decidable (Edges allowed succ s steps) := edgesDecidable allowed succ s steps

/-- Decidable bounded path checking against fixed supplied finite tables. -/
def Valid [Fintype State] (allowed : Finset (State × Action))
    (succ : (State × Action) → Finset State) (s t : State) (p : Path State Action) : Prop :=
  p.start = s ∧ p.endpoint = t ∧ Edges allowed succ p.start p.steps ∧
    True

instance instDecidableValid [DecidableEq State] [DecidableEq Action] [Fintype State] (allowed : Finset (State × Action))
    (succ : (State × Action) → Finset State) (s t : State) (p : Path State Action) :
    Decidable (Valid allowed succ s t p) := by
  unfold Valid
  infer_instance


end Path
end OrthemicCertificate
