import SCCPruning
import MarkovSupportAdapter

/-! Replacing the powerset MEC selector throughout parity pruning, with exact
refinement to the unchanged target theorem. Runtime cost is accounted separately. -/
set_option linter.unusedSectionVars false

namespace HiddenParity.SCCPruning
variable {State Pair Model Row : Type*}
variable [Fintype State] [DecidableEq State] [DecidableEq Pair] [DecidableEq Row]

/-- Bounded odd-layer test on a precomputed component family. -/
def BadWithin (Ds : Finset (Finset Pair)) (B : Finset Model)
    (row : Model → Pair → Row) (priority : Model → Pair → Nat)
    (theta : Model) (e : Pair) : Prop :=
  ∃ D ∈ Ds, e ∈ D ∧ ∃ sigma ∈ B,
    Match row theta sigma D ∧ IsMinimum (priority sigma) D (priority sigma e) ∧
      priority sigma e % 2 = 1

instance badWithinDecidable (Ds : Finset (Finset Pair)) (B : Finset Model)
    (row : Model → Pair → Row) (priority : Model → Pair → Nat)
    (theta : Model) (e : Pair) : Decidable (BadWithin Ds B row priority theta e) := by
  unfold BadWithin
  infer_instance

def parityStep (source : Pair → State) (succ : Pair → Finset State)
    (B : Finset Model) (row : Model → Pair → Row) (priority : Model → Pair → Nat)
    (theta : Model) (U : Finset Pair) : Finset Pair :=
  let Ds := mecs source succ U
  (Ds.biUnion id).filter (fun e => ¬ BadWithin Ds B row priority theta e)

theorem parityStep_eq (source : Pair → State) (succ : Pair → Finset State)
    (B : Finset Model) (row : Model → Pair → Row) (priority : Model → Pair → Nat)
    (theta : Model) (U : Finset Pair) :
    parityStep source succ B row priority theta U =
      executableStep source succ B row priority theta U := by
  simp only [parityStep, mecs_eq_executable, executableStep, ExecutableBadPair, BadWithin]

def parityIterate (source : Pair → State) (succ : Pair → Finset State)
    (B : Finset Model) (row : Model → Pair → Row) (priority : Model → Pair → Nat)
    (theta : Model) : Nat → Finset Pair → Finset Pair
  | 0, U => U
  | n+1, U => parityIterate source succ B row priority theta n
      (parityStep source succ B row priority theta U)

theorem parityIterate_eq (source : Pair → State) (succ : Pair → Finset State)
    (B : Finset Model) (row : Model → Pair → Row) (priority : Model → Pair → Nat)
    (theta : Model) (n : Nat) (U : Finset Pair) :
    parityIterate source succ B row priority theta n U =
      executableIterate source succ B row priority theta n U := by
  induction n generalizing U with
  | zero => rfl
  | succ n ih => simp only [parityIterate, executableIterate, parityStep_eq, ih]

def parityOutput (source : Pair → State) (succ : Pair → Finset State)
    (B : Finset Model) (row : Model → Pair → Row) (priority : Model → Pair → Nat)
    (theta : Model) (U : Finset Pair) : Finset (Finset Pair) :=
  mecs source succ (parityIterate source succ B row priority theta U.card U)

theorem parityOutput_eq (source : Pair → State) (succ : Pair → Finset State)
    (B : Finset Model) (row : Model → Pair → Row) (priority : Model → Pair → Nat)
    (theta : Model) (U : Finset Pair) :
    parityOutput source succ B row priority theta U =
      executableOutput source succ B row priority theta U := by
  simp only [parityOutput, executableOutput, mecs_eq_executable, parityIterate_eq]

theorem parityOutput_exact (source : Pair → State) (succ : Pair → Finset State)
    (B : Finset Model) (row : Model → Pair → Row) (priority : Model → Pair → Nat)
    (theta : Model) (U D : Finset Pair) :
    D ∈ parityOutput source succ B row priority theta U ↔
      MaximalValid (endComponentFamily source succ) B row priority theta U D := by
  rw [parityOutput_eq]
  exact executable_output_iff_maximal_valid source succ B row priority theta U D

def targetStates (source : Pair → State) (succ : Pair → Finset State)
    (B : Finset Model) (row : Model → Pair → Row) (priority : Model → Pair → Nat)
    (theta : Model) (U : Finset Pair) : Finset State :=
  (parityOutput source succ B row priority theta U).biUnion (usedStates source)

theorem targetStates_eq (source : Pair → State) (succ : Pair → Finset State)
    (B : Finset Model) (row : Model → Pair → Row) (priority : Model → Pair → Nat)
    (theta : Model) (U : Finset Pair) :
    targetStates source succ B row priority theta U =
      executableTargetStates source succ B row priority theta U := by
  simp only [targetStates, executableTargetStates, parityOutput_eq]

theorem targetStates_exact (source : Pair → State) (succ : Pair → Finset State)
    (B : Finset Model) (row : Model → Pair → Row) (priority : Model → Pair → Nat)
    (theta : Model) (U : Finset Pair) (s : State) :
    s ∈ targetStates source succ B row priority theta U ↔
      IsTargetState source succ B row priority theta U s := by
  rw [targetStates_eq]
  exact executable_targetStates_exact source succ B row priority theta U s

/-- Full normalized-row interface, with exactly the old supplied-licence boundary. -/
def markovTarget (P : RationalKernel Model Pair State) (source : Pair → State)
    (B : Finset Model) (priority : Model → Pair → Nat) (theta : Model)
    (allowed : Finset Pair) : Finset State :=
  targetStates source (internalSuccessors P B) B P.row priority theta
    (zeroExitPairs P B theta allowed)

theorem markovTarget_eq (P : RationalKernel Model Pair State) (source : Pair → State)
    (B : Finset Model) (priority : Model → Pair → Nat) (theta : Model)
    (allowed : Finset Pair) :
    markovTarget P source B priority theta allowed =
      HiddenParity.markovTargetStates P source B priority theta allowed := by
  simp only [markovTarget, HiddenParity.markovTargetStates, targetStates_eq]

theorem markovTarget_exact (P : RationalKernel Model Pair State) (source : Pair → State)
    (B : Finset Model) (priority : Model → Pair → Nat) (theta : Model)
    (allowed : Finset Pair) (s : State) :
    s ∈ markovTarget P source B priority theta allowed ↔
      ∃ E, MarkovQualifying P source B priority theta allowed E ∧ s ∈ usedStates source E := by
  rw [markovTarget_eq]
  exact HiddenParity.markovTargetStates_exact P source B priority theta allowed s

end HiddenParity.SCCPruning
