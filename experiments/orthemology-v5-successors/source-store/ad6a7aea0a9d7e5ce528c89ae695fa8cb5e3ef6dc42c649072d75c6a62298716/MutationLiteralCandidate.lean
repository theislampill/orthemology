import HiddenChangeCertificate
import HiddenChangeTaggedLaw
import RationalTest
import OrderedCycle
import ObservedPhaseController

/-! A new literal two-layer controller over physical histories. It does not
use liveSupport, does not delete candidate 1, and does not receive mode tags.
The data-only Lean body remains distinct from the Python body representation. -/
namespace HiddenChange
open HiddenParity HiddenParity.Sufficiency
open Orthemology.Tranche2.PolicyEmbedding
variable {n k : ℕ}

structure ControllerMemory (n k : ℕ) where
  known1 : Bool
  phase : ℕ
  retained : Option (PairSet n k)
  deriving DecidableEq

def candidate (r : ℕ) : Mode := 0

def knownComponents (c : PositiveBody n k) : List (PairSet n k) :=
  c.known.map KnownObligation.component

def uncertainComponents (θ : Mode) : List (UncertainObligation n k) → List (PairSet n k)
  | [] => []
  | o :: os => match o.witness with
    | .component _ E => if o.candidate = θ then E :: uncertainComponents θ os
        else uncertainComponents θ os
    | .reveal _ _ _ => uncertainComponents θ os

def firstContaining (s : State n) : List (PairSet n k) → Option (PairSet n k)
  | [] => none
  | E :: es => if s ∈ usedStates Prod.fst E then some E else firstContaining s es

def availableComponents (c : PositiveBody n k) (m : ControllerMemory n k) : List (PairSet n k) :=
  if m.known1 then knownComponents c else uncertainComponents (candidate m.phase) c.uncertain

/-- Selection follows the submitted obligation order and happens before action. -/
def prepare (c : PositiveBody n k) (s : State n) (m : ControllerMemory n k) : ControllerMemory n k :=
  match m.retained with
  | some _ => m
  | none => { m with retained := firstContaining s (availableComponents c m) }

def leaves (m : ControllerMemory n k) (y : State n) : Bool :=
  match m.retained with
  | none => false
  | some E => decide (y ∉ usedStates Prod.fst E)

/-- Revelation has priority over rejection and component exit. In known1 the
statistical test is ignored; an impossible off-policy exit only clears E. -/
def advance (I : Input n k) (e : Pair n k) (y : State n)
    (m : ControllerMemory n k) (reject : Bool) : ControllerMemory n k :=
  if m.known1 then
    { m with retained := if leaves m y then none else m.retained }
  else if I.row 0 e y = 0 then
    { m with known1 := true, retained := none }
  else if reject || leaves m y then
    { m with phase := m.phase + 1, retained := none }
  else m

/-- The exact strict count gate sees the full newly extended history. -/
def rejectHistory (I : Input n k) (r : ℕ) (h : PairHistory n k) : Bool :=
  OrthemicCertificate.Direct.rationalReject I
    (OrthemicCertificate.Direct.tolerance I Finset.univ) (candidate r) r h

def memory (I : Input n k) (c : PositiveBody n k) (s₀ : State n) :
    PublicHistory n k → ControllerMemory n k
  | [] => ⟨false, 0, none⟩
  | (a,y) :: h =>
      let m := prepare c (observedState s₀ h) (memory I c s₀ h)
      advance I (observedState s₀ h,a) y m
        (rejectHistory I m.phase (augmentHistory s₀ ((a,y)::h)))

def currentMemory (I : Input n k) (c : PositiveBody n k) (s₀ : State n)
    (h : PublicHistory n k) : ControllerMemory n k :=
  prepare c (observedState s₀ h) (memory I c s₀ h)

def activePairs (c : PositiveBody n k) (m : ControllerMemory n k) : PairSet n k :=
  m.retained.getD (if m.known1 then c.D1 else c.D)

def firstMenuAction (I : Input n k) (hI : Admissible I) (s : State n) : Action k :=
  (commonMenu I s).min' (hI.2 s)

/-- Intersecting with the common menu keeps every malformed/off-policy history
lawful. The intersection is redundant on the proved certificate invariant. -/
def actionMenu (I : Input n k) (c : PositiveBody n k) (s : State n)
    (m : ControllerMemory n k) : Finset (Action k) :=
  retainedActions (activePairs c m) s ∩ commonMenu I s

def compile (I : Input n k) (hI : Admissible I) (s₀ : State n)
    (c : PositiveBody n k) : Policy Unit n k :=
  fun _ h =>
    let s := observedState s₀ h
    let m := currentMemory I c s₀ h
    OrthemicCertificate.Direct.cycleAction (actionMenu I c s m)
      (firstMenuAction I hI s) (historyVisits s₀ s h)


example : candidate 1 = 1 := by decide +kernel

end HiddenChange
