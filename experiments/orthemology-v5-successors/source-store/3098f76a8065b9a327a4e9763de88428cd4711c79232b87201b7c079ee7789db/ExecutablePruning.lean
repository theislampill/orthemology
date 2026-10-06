import EndComponents
import FiniteReachability

/-!
# Executable exhaustive reference, proved equal to the abstract pruning kernel

Finite reachability is proved sound and complete. Maximal components are selected
by checking subsets of the current pair set, so this reference is exponential.
No polynomial-time implementation claim is made.
-/
namespace HiddenParity

variable {State Pair Model Row : Type*}
variable [Fintype State] [DecidableEq State] [DecidableEq Pair]

instance edgeDecidable (source : Pair → State) (succ : Pair → Finset State)
    (E : Finset Pair) : DecidableRel (Edge source succ E) := by
  intro s t
  unfold Edge
  infer_instance

/-- The executable reachability-based check has no unbounded path quantifier. -/
def CheckedEndComponent (source : Pair → State) (succ : Pair → Finset State)
    (E : Finset Pair) : Prop :=
  E.Nonempty ∧ (∀ e ∈ E, (succ e).Nonempty) ∧
    (∀ e ∈ E, succ e ⊆ usedStates source E) ∧
    ∀ s ∈ usedStates source E, ∀ t ∈ usedStates source E,
      t ∈ FiniteReachability.reachable (Edge source succ E) s

instance checkedEndComponentDecidable (source : Pair → State)
    (succ : Pair → Finset State) (E : Finset Pair) :
    Decidable (CheckedEndComponent source succ E) := by
  unfold CheckedEndComponent
  infer_instance

omit [DecidableEq Pair] in
theorem checkedEndComponent_iff (source : Pair → State)
    (succ : Pair → Finset State) (E : Finset Pair) :
    CheckedEndComponent source succ E ↔ IsEndComponent source succ E := by
  constructor
  · rintro ⟨hne, hSucc, hClosed, hConnected⟩
    refine ⟨hne, hSucc, hClosed, ?_⟩
    intro s hs t ht
    exact (FiniteReachability.reachable_iff _ s t).mp (hConnected s hs t ht)
  · intro h
    refine ⟨h.nonempty, h.successors_nonempty, h.closed, ?_⟩
    intro s hs t ht
    exact (FiniteReachability.reachable_iff _ s t).mpr (h.connected s hs t ht)

instance endComponentDecidable (source : Pair → State)
    (succ : Pair → Finset State) (E : Finset Pair) :
    Decidable (IsEndComponent source succ E) :=
  decidable_of_iff (CheckedEndComponent source succ E)
    (checkedEndComponent_iff source succ E)

/-- Bounded maximality test over the current powerset; no classical decision procedure. -/
def executableMECs (source : Pair → State) (succ : Pair → Finset State)
    (U : Finset Pair) : Finset (Finset Pair) :=
  U.powerset.filter (fun D => IsEndComponent source succ D ∧
    ∀ F ∈ U.powerset, IsEndComponent source succ F → D ⊆ F → F = D)

theorem executableMECs_eq (source : Pair → State) (succ : Pair → Finset State)
    (U : Finset Pair) :
    executableMECs source succ U = maximalComponents (endComponentFamily source succ) U := by
  classical
  ext D
  simp only [executableMECs, Finset.mem_filter, Finset.mem_powerset,
    mem_maximalComponents, MaximalComponent]
  constructor
  · rintro ⟨hDU, hD, hmax⟩
    exact ⟨hD, hDU, fun F hF hFU hDF => hmax F hFU hF hDF⟩
  · rintro ⟨hD, hDU, hmax⟩
    exact ⟨hDU, hD, fun F hFU hF hDF => hmax F hF hFU hDF⟩

variable [DecidableEq Row]

instance matchDecidable (row : Model → Pair → Row) (θ σ : Model) (E : Finset Pair) :
    Decidable (Match row θ σ E) := by
  unfold Match
  infer_instance

instance minimumDecidable (priority : Pair → ℕ) (E : Finset Pair) (d : ℕ) :
    Decidable (IsMinimum priority E d) := by
  unfold IsMinimum
  infer_instance

def ExecutableBadPair (source : Pair → State) (succ : Pair → Finset State)
    (B : Finset Model) (row : Model → Pair → Row) (priority : Model → Pair → ℕ)
    (θ : Model) (U : Finset Pair) (e : Pair) : Prop :=
  ∃ D ∈ executableMECs source succ U, e ∈ D ∧ ∃ σ ∈ B,
    Match row θ σ D ∧ IsMinimum (priority σ) D (priority σ e) ∧
      priority σ e % 2 = 1

instance executableBadPairDecidable (source : Pair → State) (succ : Pair → Finset State)
    (B : Finset Model) (row : Model → Pair → Row) (priority : Model → Pair → ℕ)
    (θ : Model) (U : Finset Pair) (e : Pair) :
    Decidable (ExecutableBadPair source succ B row priority θ U e) := by
  unfold ExecutableBadPair
  infer_instance

def executableStep (source : Pair → State) (succ : Pair → Finset State)
    (B : Finset Model) (row : Model → Pair → Row) (priority : Model → Pair → ℕ)
    (θ : Model) (U : Finset Pair) : Finset Pair :=
  ((executableMECs source succ U).biUnion id).filter
    (fun e => ¬ ExecutableBadPair source succ B row priority θ U e)

theorem executableStep_eq (source : Pair → State) (succ : Pair → Finset State)
    (B : Finset Model) (row : Model → Pair → Row) (priority : Model → Pair → ℕ)
    (θ : Model) (U : Finset Pair) :
    executableStep source succ B row priority θ U =
      step (endComponentFamily source succ) B row priority θ U := by
  classical
  ext e
  simp only [executableStep, step, Finset.mem_filter, Finset.mem_biUnion,
    ExecutableBadPair, BadPair, executableMECs_eq]

def executableIterate (source : Pair → State) (succ : Pair → Finset State)
    (B : Finset Model) (row : Model → Pair → Row) (priority : Model → Pair → ℕ)
    (θ : Model) : ℕ → Finset Pair → Finset Pair
  | 0, U => U
  | n + 1, U => executableIterate source succ B row priority θ n
      (executableStep source succ B row priority θ U)

theorem executableIterate_eq (source : Pair → State) (succ : Pair → Finset State)
    (B : Finset Model) (row : Model → Pair → Row) (priority : Model → Pair → ℕ)
    (θ : Model) (n : ℕ) (U : Finset Pair) :
    executableIterate source succ B row priority θ n U =
      iterate (endComponentFamily source succ) B row priority θ n U := by
  induction n generalizing U with
  | zero => rfl
  | succ n ih => simp only [executableIterate, iterate, executableStep_eq, ih]

def executableOutput (source : Pair → State) (succ : Pair → Finset State)
    (B : Finset Model) (row : Model → Pair → Row) (priority : Model → Pair → ℕ)
    (θ : Model) (U : Finset Pair) : Finset (Finset Pair) :=
  executableMECs source succ (executableIterate source succ B row priority θ U.card U)

/-- Complete algorithm equivalence, including recomputation of components and rivals. -/
theorem executable_output_eq (source : Pair → State) (succ : Pair → Finset State)
    (B : Finset Model) (row : Model → Pair → Row) (priority : Model → Pair → ℕ)
    (θ : Model) (U : Finset Pair) :
    executableOutput source succ B row priority θ U =
      output (endComponentFamily source succ) B row priority θ U := by
  simp only [executableOutput, output, executableMECs_eq, executableIterate_eq]

theorem executable_output_iff_maximal_valid
    (source : Pair → State) (succ : Pair → Finset State)
    (B : Finset Model) (row : Model → Pair → Row) (priority : Model → Pair → ℕ)
    (θ : Model) (U D : Finset Pair) :
    D ∈ executableOutput source succ B row priority θ U ↔
      MaximalValid (endComponentFamily source succ) B row priority θ U D := by
  rw [executable_output_eq]
  exact output_iff_maximal_valid

def executableTargetStates (source : Pair → State) (succ : Pair → Finset State)
    (B : Finset Model) (row : Model → Pair → Row) (priority : Model → Pair → ℕ)
    (θ : Model) (U : Finset Pair) : Finset State :=
  (executableOutput source succ B row priority θ U).biUnion (usedStates source)

theorem executable_targetStates_exact
    (source : Pair → State) (succ : Pair → Finset State)
    (B : Finset Model) (row : Model → Pair → Row) (priority : Model → Pair → ℕ)
    (θ : Model) (U : Finset Pair) (s : State) :
    s ∈ executableTargetStates source succ B row priority θ U ↔
      IsTargetState source succ B row priority θ U s := by
  rw [executableTargetStates, executable_output_eq]
  exact targetStates_exact source succ B row priority θ U s

end HiddenParity
