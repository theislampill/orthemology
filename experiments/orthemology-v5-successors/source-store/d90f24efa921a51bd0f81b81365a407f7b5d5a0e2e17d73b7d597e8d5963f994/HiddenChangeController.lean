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

def candidate (r : ℕ) : Mode := ⟨r % 2, Nat.mod_lt _ (by decide)⟩

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

@[simp] theorem candidate_val (r : ℕ) : (candidate r).val = r % 2 := rfl
@[simp] theorem prepare_phase (c : PositiveBody n k) (s : State n) (m : ControllerMemory n k) :
    (prepare c s m).phase = m.phase := by cases h : m.retained <;> simp [prepare, h]
@[simp] theorem prepare_known1 (c : PositiveBody n k) (s : State n) (m : ControllerMemory n k) :
    (prepare c s m).known1 = m.known1 := by cases h : m.retained <;> simp [prepare, h]

theorem compiled_all_history_lawful (I : Input n k) (hI : Admissible I)
    (s₀ : State n) (c : PositiveBody n k) : AllHistoryLawful I s₀ (compile I hI s₀ c) := by
  intro r h
  have hs : currentObserved s₀ h = observedState s₀ h := by cases h <;> rfl
  rw [hs]
  unfold compile
  change OrthemicCertificate.Direct.cycleAction _ _ _ ∈ commonMenu I (observedState s₀ h)
  by_cases hm : (actionMenu I c (observedState s₀ h) (currentMemory I c s₀ h)).Nonempty
  · exact (Finset.mem_inter.mp (OrthemicCertificate.Direct.cycleAction_mem _ _ hm _)).2
  · simp only [OrthemicCertificate.Direct.cycleAction, dif_neg hm]
    exact Finset.min'_mem _ _

theorem compiled_measurable (I : Input n k) (hI : Admissible I)
    (s₀ : State n) (c : PositiveBody n k) :
    Measurable (fun z : Unit × PublicHistory n k => compile I hI s₀ c z.1 z.2) :=
  measurable_of_countable _

theorem advance_known1_persists (I : Input n k) (e : Pair n k) (y : State n)
    (m : ControllerMemory n k) (b : Bool) (h : m.known1 = true) :
    (advance I e y m b).known1 = true := by simp [advance, h]

theorem advance_reveal_first (I : Input n k) (e : Pair n k) (y : State n)
    (m : ControllerMemory n k) (b : Bool) (h : m.known1 = false) (hz : I.row 0 e y = 0) :
    advance I e y m b = { m with known1 := true, retained := none } := by simp [advance, h, hz]

theorem advance_uncertain_increment (I : Input n k) (e : Pair n k) (y : State n)
    (m : ControllerMemory n k) (b : Bool) :
    (advance I e y m b).phase = m.phase ∨
      (advance I e y m b).phase = m.phase + 1 := by
  unfold advance
  split <;> (try { left; rfl })
  split <;> (try { left; rfl })
  split <;> simp

theorem advance_known1_iff (I : Input n k) (e : Pair n k) (y : State n)
    (m : ControllerMemory n k) (b : Bool) :
    (advance I e y m b).known1 = true ↔ m.known1 = true ∨ I.row 0 e y = 0 := by
  unfold advance
  cases h : m.known1 <;> simp [h]
  split_ifs <;> simp_all

/-- Candidate 1 is never excluded by a mode1-zero receipt. Only P0-zero sets the flag. -/
theorem memory_known1_iff (I : Input n k) (c : PositiveBody n k) (s₀ : State n)
    (h : PublicHistory n k) :
    (memory I c s₀ h).known1 = true ↔
      ∃ z ∈ augmentHistory s₀ h, I.row 0 z.1 z.2 = 0 := by
  induction h with
  | nil => simp [memory, augmentHistory]
  | cons z h ih =>
      rcases z with ⟨a,y⟩
      simp only [memory, advance_known1_iff, prepare_known1, ih, augmentHistory,
        List.mem_cons, exists_eq_or_imp]
      constructor
      · rintro (h | h)
        · exact Or.inr h
        · exact Or.inl h
      · rintro (h | h)
        · exact Or.inr h
        · exact Or.inl h

end HiddenChange
