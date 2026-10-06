import Mathlib.Data.Finset.Card
import Mathlib.Tactic

/-! Finite-history refinement of the accepted, fixed dynamic V2 interlock family.
    Authentication, root separation and physical mediation are model premises.
    All root-local guards below use only the actual local state and command. -/
namespace InterlockHistory

abbrev Table := Bool × Bool

structure Descriptor where
  epoch : Nat
  targetId : Nat
  targetVersion : Nat
  recipient : Nat
  scope : Nat
  table : Table
  allowed : Bool
  deriving DecidableEq

structure Command (n : Nat) where
  epoch : Nat
  targetId : Nat
  targetVersion : Nat
  recipient : Nat
  scope : Nat
  table : Table
  nonce : Nat
  path : Finset (Fin n)
  deriving DecidableEq

def Authorized {n} (k : Command n) (d : Descriptor) : Prop :=
  d.allowed = true ∧ k.epoch = d.epoch ∧ k.targetId = d.targetId ∧
  k.targetVersion = d.targetVersion ∧ k.recipient = d.recipient ∧
  k.scope = d.scope ∧ k.table = d.table

instance {n} (k : Command n) (d : Descriptor) : Decidable (Authorized k d) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ _ ∧ _ ∧ _ ∧ _))

structure RootState (n : Nat) where
  descriptor : Descriptor
  revoked : Finset Nat := ∅
  commitments : Finset (Command n) := ∅
  cancelled : Finset (Command n) := ∅
  deriving DecidableEq

/-- Preparation and live landing separately check this same local envelope. -/
abbrev Envelope {n} (z : RootState n) (k : Command n) (requester : Nat) : Prop :=
  requester = k.recipient ∧ Authorized k z.descriptor ∧
  k.epoch ∉ z.revoked ∧ k ∉ z.cancelled

abbrev Permits {n} (z : RootState n) (k : Command n) (requester : Nat) : Prop :=
  k ∈ z.commitments ∧ Envelope z k requester

structure Config (n : Nat) where
  budget : Nat
  q : Nat
  r : Nat
  faulty : Finset (Fin n)
  budget_bound : faulty.card ≤ budget
  overlap : n + budget < q + r
  budget_lt_roots : budget < n
  repair_available : q + budget ≤ n
  revoke_available : r + budget ≤ n
  source : Nat → Descriptor
  source_epoch : ∀ e, (source e).epoch = e

/-- These global fields are proof/classification state, never a gate input. -/
structure State (n : Nat) where
  epoch : Nat
  roots : Fin n → RootState n
  pending : Bool
  acks : Finset (Fin n)
  certificates : Nat → Finset (Fin n)
  cancelAcks : Command n → Finset (Fin n)
  table : Table
  damaged : Bool

abbrev Good {n} (c : Config n) (i : Fin n) : Prop := i ∉ c.faulty

def Initial {n} (c : Config n) (table : Table) : State n :=
  ⟨0, fun _ => ⟨c.source 0, ∅, ∅, ∅⟩, false, ∅, fun _ => ∅,
    fun _ => ∅, table, false⟩

abbrev ValidPath {n} (c : Config n) (k : Command n) : Prop := k.path.card = c.q

/-- Bad roots can open their own gates; they cannot override any good veto.
    F appears only in this semantic behavior relation, not inside Permits. -/
abbrev Lands {n} (c : Config n) (s : State n) (k : Command n) (requester : Nat) : Prop :=
  ValidPath c k ∧ ∀ i ∈ k.path, Good c i → Permits (s.roots i) k requester

def setRoot {n} (s : State n) (i : Fin n) (z : RootState n) : State n :=
  { s with roots := Function.update s.roots i z }

def request {n} (s : State n) : State n :=
  { s with pending := true, acks := ∅ }

def acknowledge {n} (c : Config n) (s : State n) (i : Fin n) : State n :=
  { s with
    acks := insert i s.acks
    roots := if Good c i then Function.update s.roots i
      { s.roots i with revoked := insert s.epoch (s.roots i).revoked } else s.roots }

def complete {n} (s : State n) : State n :=
  { s with
    epoch := s.epoch + 1
    pending := false
    acks := ∅
    certificates := Function.update s.certificates s.epoch s.acks }

def deliver {n} (c : Config n) (s : State n) (i : Fin n) (e : Nat) : State n :=
  if (s.roots i).descriptor.epoch < e then
    setRoot s i { s.roots i with descriptor := c.source e }
  else s

def prepare {n} (s : State n) (i : Fin n) (k : Command n) : State n :=
  setRoot s i { s.roots i with commitments := insert k (s.roots i).commitments }

def cancelAck {n} (c : Config n) (s : State n) (i : Fin n) (k : Command n) : State n :=
  { s with
    cancelAcks := Function.update s.cancelAcks k (insert i (s.cancelAcks k))
    roots := if Good c i then Function.update s.roots i
      { s.roots i with cancelled := insert k (s.roots i).cancelled } else s.roots }

/-- Global authorization only classifies the already-admitted effect. It does
    not occur in Lands and cannot stop a landing. X is absorbing. -/
def land {n} (c : Config n) (s : State n) (k : Command n) (requester : Nat) : State n :=
  if s.damaged = true ∨ requester ≠ k.recipient ∨ ¬Authorized k (c.source s.epoch)
  then { s with damaged := true }
  else { s with table := k.table }

inductive Event (n : Nat) where
  | request
  | acknowledge (i : Fin n)
  | complete
  | deliver (i : Fin n) (epoch : Nat)
  | prepare (i : Fin n) (command : Command n) (requester : Nat)
  | cancelAck (i : Fin n) (command : Command n) (requester : Nat)
  | close (command : Command n)
  | land (command : Command n) (requester : Nat)
  | hold
  | corrupt (i : Fin n) (root : RootState n)

/-- Individual acknowledgements precede completion. Only completed authentic
    certificates can advance a root; deliveries can be delayed/repeated/reordered.
    No guard asks whether the actor has learned the effective global epoch. -/
inductive Step {n} (c : Config n) : State n → Event n → State n → Prop where
  | request (s) (idle : s.pending = false) : Step c s .request (request s)
  | acknowledge (s i) (pending : s.pending = true) :
      Step c s (.acknowledge i) (acknowledge c s i)
  | complete (s) (pending : s.pending = true) (quorum : s.acks.card = c.r) :
      Step c s .complete (complete s)
  | deliver (s i e) (existsCert : 0 < e ∧ e ≤ s.epoch) :
      Step c s (.deliver i e) (deliver c s i e)
  | prepare (s i k requester) (selected : i ∈ k.path) (path : ValidPath c k)
      (grant : i ∈ c.faulty ∨ Envelope (s.roots i) k requester) :
      Step c s (.prepare i k requester) (prepare s i k)
  | cancelAck (s i k requester) (selected : i ∈ k.path)
      (auth : i ∈ c.faulty ∨ requester = k.recipient) :
      Step c s (.cancelAck i k requester) (cancelAck c s i k)
  | close (s k) (certificate : c.budget < (s.cancelAcks k).card) :
      Step c s (.close k) s
  | land (s k requester) (admitted : Lands c s k requester) :
      Step c s (.land k requester) (land c s k requester)
  | hold (s) : Step c s .hold s
  | corrupt (s i z) (bad : i ∈ c.faulty) :
      Step c s (.corrupt i z) (setRoot s i z)

inductive Trace {n} (c : Config n) : State n → List (Event n) → State n → Prop where
  | nil (s) : Trace c s [] s
  | cons {s t u a as} : Step c s a t → Trace c t as u → Trace c s (a :: as) u

def Reachable {n} (c : Config n) (s : State n) : Prop :=
  ∃ table events, Trace c (Initial c table) events s

/-- Structural history facts only, with no desired landing safety as a field. -/
structure Consistent {n} (c : Config n) (s : State n) : Prop where
  local_authentic : ∀ i, Good c i → (s.roots i).descriptor = c.source (s.roots i).descriptor.epoch
  local_not_future : ∀ i, Good c i → (s.roots i).descriptor.epoch ≤ s.epoch
  past_certificates : ∀ e, e < s.epoch → (s.certificates e).card = c.r ∧
    ∀ i ∈ s.certificates e, Good c i → e ∈ (s.roots i).revoked
  pending_revoked : ∀ i ∈ s.acks, Good c i → s.epoch ∈ (s.roots i).revoked
  cancel_selected : ∀ k i, i ∈ s.cancelAcks k → i ∈ k.path
  cancel_durable : ∀ k i, i ∈ s.cancelAcks k → Good c i → k ∈ (s.roots i).cancelled

end InterlockHistory
