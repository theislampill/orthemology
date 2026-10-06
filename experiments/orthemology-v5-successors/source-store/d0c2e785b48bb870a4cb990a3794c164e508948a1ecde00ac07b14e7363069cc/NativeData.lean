import AliasRuntime

/-! Executable finite data. Mathematical projection and proofs are separated
from these definitions; no native definition invokes Classical.choice. -/
namespace SharedAlias.Native
open ComposedExecution
open OperationalJoin.Typed (BoundedEnvelope interface rootView)

/-- Finite first-match table. Missing entries receive an explicit supplied
value. This operation never manufactures policy authentication. -/
def tableRead {α β : Type} [DecidableEq α] (rows : List (α × β)) (key : α) (fallback : β) : β :=
  match rows with
  | [] => fallback
  | (k, v) :: rest => if key = k then v else tableRead rest key fallback

@[simp] theorem tableRead_nil {α β : Type} [DecidableEq α] (key : α) (fallback : β) :
    tableRead [] key fallback = fallback := rfl

@[simp] theorem tableRead_cons_same {α β : Type} [DecidableEq α]
    (rows : List (α × β)) (key : α) (value fallback : β) :
    tableRead ((key, value) :: rows) key fallback = value := by simp [tableRead]

@[simp] theorem tableRead_cons_other {α β : Type} [DecidableEq α]
    (rows : List (α × β)) (key other : α) (value fallback : β) (ne : other ≠ key) :
    tableRead ((key, value) :: rows) other fallback = tableRead rows other fallback := by
  simp [tableRead, ne]

/-- Hidden fixed data for the service machine. This is not an actor input. -/
structure Routing (m : Nat) where
  aliasMembers : List (Fin m)
  faultyRoots : List (Option (Fin m))
  budget : Nat
  q : Nat
  r : Nat

/-- Accepted canonical one-class routing, represented with finite data. -/
def rootOf {m} (D : Routing m) (i : Fin m) : Option (Fin m) :=
  if i ∈ D.aliasMembers then none else some i

def faulty {m} (D : Routing m) (i : Fin m) : Bool :=
  decide (rootOf D i ∈ D.faultyRoots)

/-- All stored data are finite. Raw malformed historical envelopes remain raw
and are ignored only by the accepted typed projection, never rewritten. -/
structure FiniteState (m : Nat) where
  epoch : Nat
  defaultRoot : Root
  rootRows : List (Option (Fin m) × Root)
  pending : Bool
  acks : List (Fin m)
  certificateRows : List (Nat × List (Fin m))
  cancelRows : List (ComposedExecution.Envelope × List (Fin m))
  plant : Plant

def rootAt {m} (C : FiniteState m) (r : Option (Fin m)) : Root :=
  tableRead C.rootRows r C.defaultRoot

def setRoot {m} (C : FiniteState m) (r : Option (Fin m)) (z : Root) : FiniteState m :=
  { C with rootRows := (r, z) :: C.rootRows }

def receipts {m} (C : FiniteState m) (e : ComposedExecution.Envelope) : List (Fin m) :=
  tableRead C.cancelRows e []

/-- Empty history has explicit finite tables. Authentication of policy is a
separate hypothesis in its model-refinement theorem. -/
def initial {m} (policy : Policy) (p : Plant) : FiniteState m :=
  ⟨0, ⟨policy, [], [], []⟩, [], false, [], [], [], p⟩

/-- Read-only snapshot for the unchanged source gate. It is never the storage
implementation: aliases read one shared row and native writes update that row. -/
def gateWorld {m} (D : Routing m) (C : FiniteState m) (time : Nat)
    (suppliedPolicy : Policy) : World where
  n := m
  budget := D.budget
  q := D.q
  r := D.r
  effectivePolicy := suppliedPolicy
  plant := C.plant
  now := time
  roots := fun i => if h : i < m then rootAt C (rootOf D ⟨i, h⟩) else C.defaultRoot
  tainted := fun i => if h : i < m then faulty D ⟨i, h⟩ else false
  completed := []

/-- The exact accepted state represented by native finite data. No native
operation calls this proof-side projection. -/
noncomputable def view {m} (C : FiniteState m) : SharedAlias.State (interface m) where
  epoch := C.epoch
  roots := fun r => rootView (rootAt C r)
  pending := C.pending
  acks := C.acks.toFinset
  certificates := fun e => (tableRead C.certificateRows e []).toFinset
  cancelAcks := fun k => (receipts C k.val).toFinset
  plant := C.plant

/-- Match finite routing to a fixed accepted hidden environment. Policies are
not included: separate history/authentication premises are mandatory. -/
structure RoutingMatches {m} (D : Routing m) (E : SharedAlias.Environment (interface m)) : Prop where
  aliases : D.aliasMembers.toFinset = E.aliasClass
  faults : D.faultyRoots.toFinset = E.actualFaults
  budget : D.budget = E.labelBudget
  quorum : D.q = E.q
  revokeQuorum : D.r = E.r

theorem rootOf_matches {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (i : Fin m) : rootOf D i = E.rootOf i := by
  simp only [rootOf, SharedAlias.Environment.rootOf, AttributionKernel.rootMap,
    ← matchD.aliases, List.mem_toFinset]

theorem faulty_false_iff {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (i : Fin m) :
    faulty D i = false ↔ OperationalJoin.Good E.labelConfig i := by
  rw [SharedAlias.good_iff]
  simp only [faulty, decide_eq_false_iff_not, rootOf_matches D E matchD,
    ← matchD.faults, List.mem_toFinset]

theorem faulty_true_iff {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (i : Fin m) :
    faulty D i = true ↔ i ∈ E.labelConfig.faulty := by
  classical
  constructor
  · intro yes
    by_contra member
    have no := (faulty_false_iff D E matchD i).mpr member
    rw [yes] at no
    cases no
  · intro member
    cases h : faulty D i with
    | true => rfl
    | false => exact False.elim ((faulty_false_iff D E matchD i).mp h member)

@[simp] theorem rootAt_setRoot_same {m} (C : FiniteState m) (r : Option (Fin m)) (z : Root) :
    rootAt (setRoot C r z) r = z := by simp [rootAt, setRoot]

@[simp] theorem rootAt_setRoot_other {m} (C : FiniteState m) (r s : Option (Fin m))
    (z : Root) (ne : s ≠ r) : rootAt (setRoot C r z) s = rootAt C s := by
  simp [rootAt, setRoot, ne]

theorem gateWorld_represents {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (C : FiniteState m) (time : Nat) (suppliedPolicy : Policy) :
    OperationalJoin.Typed.RuntimeRepresents E.labelConfig
      (gateWorld D C time suppliedPolicy) (SharedAlias.Typed.literalSnapshot E (view C)) := by
  refine ⟨rfl, matchD.quorum, rfl, ?_, ?_⟩
  · intro i
    simpa only [gateWorld, dif_pos i.isLt] using faulty_false_iff D E matchD i
  · intro i
    simp only [gateWorld, SharedAlias.Typed.literalSnapshot, view, dif_pos i.isLt,
      rootOf_matches D E matchD]
    exact OperationalJoin.Typed.rootView_represents _

end SharedAlias.Native
