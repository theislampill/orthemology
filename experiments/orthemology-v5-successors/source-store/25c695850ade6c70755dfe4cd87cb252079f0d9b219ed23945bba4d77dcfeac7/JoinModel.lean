import Mathlib.Data.Finset.Card
import Mathlib.Tactic

/-! The common kernel contains no goal or safety assumption. Its only local
interface laws expose the epoch and requester already checked by admission. -/
namespace OperationalJoin

structure Interface (n : Nat) where
  Policy : Type
  Command : Type
  Plant : Type
  Requester : Type
  policyEpoch : Policy → Nat
  commandEpoch : Command → Nat
  commandPath : Command → Finset (Fin n)
  recipient : Command → Requester
  admits : Plant → Nat → Policy → Command → Requester → Prop
  effect : Plant → Command → Plant
  admitted_epoch : ∀ p time d k requester,
    admits p time d k requester → commandEpoch k = policyEpoch d
  admitted_requester : ∀ p time d k requester,
    admits p time d k requester → requester = recipient k

noncomputable section
open Classical

structure RootState {n} (I : Interface n) where
  descriptor : I.Policy
  revoked : Finset Nat := ∅
  commitments : Finset I.Command := ∅
  cancelled : Finset I.Command := ∅

structure Config {n} (I : Interface n) where
  budget : Nat
  q : Nat
  r : Nat
  faulty : Finset (Fin n)
  budget_bound : faulty.card ≤ budget
  overlap : n + budget < q + r
  budget_lt_roots : budget < n
  repair_available : q + budget ≤ n
  revoke_available : r + budget ≤ n
  source : Nat → I.Policy
  source_epoch : ∀ e, I.policyEpoch (source e) = e

/-- Epoch and certificates are proof-side control state, not live gate input. -/
structure State {n} (I : Interface n) where
  epoch : Nat
  roots : Fin n → RootState I
  pending : Bool
  acks : Finset (Fin n)
  certificates : Nat → Finset (Fin n)
  cancelAcks : I.Command → Finset (Fin n)
  plant : I.Plant
  damaged : Bool

abbrev Good {n} {I : Interface n} (c : Config I) (i : Fin n) : Prop := i ∉ c.faulty

def Initial {n} {I : Interface n} (c : Config I) (plant : I.Plant) : State I :=
  ⟨0, fun _ => ⟨c.source 0, ∅, ∅, ∅⟩, false, ∅, fun _ => ∅,
    fun _ => ∅, plant, false⟩

abbrev ValidPath {n} {I : Interface n} (c : Config I) (k : I.Command) : Prop :=
  (I.commandPath k).card = c.q

abbrev Envelope {n} {I : Interface n} (p : I.Plant) (time : Nat)
    (z : RootState I) (k : I.Command) (requester : I.Requester) : Prop :=
  I.admits p time z.descriptor k requester ∧
  I.commandEpoch k ∉ z.revoked ∧ k ∉ z.cancelled

abbrev Permits {n} {I : Interface n} (p : I.Plant) (time : Nat)
    (z : RootState I) (k : I.Command) (requester : I.Requester) : Prop :=
  k ∈ z.commitments ∧ Envelope p time z k requester

abbrev Lands {n} {I : Interface n} (c : Config I) (s : State I)
    (time : Nat) (k : I.Command) (requester : I.Requester) : Prop :=
  ValidPath c k ∧ ∀ i ∈ I.commandPath k, Good c i →
    Permits s.plant time (s.roots i) k requester

def setRoot {n} {I : Interface n} (s : State I) (i : Fin n) (z : RootState I) : State I :=
  { s with roots := Function.update s.roots i z }

def request {n} {I : Interface n} (s : State I) : State I :=
  { s with pending := true, acks := ∅ }

def acknowledge {n} {I : Interface n} (c : Config I) (s : State I) (i : Fin n) : State I :=
  { s with acks := insert i s.acks
           roots := if Good c i then Function.update s.roots i
             { s.roots i with revoked := insert s.epoch (s.roots i).revoked } else s.roots }

def complete {n} {I : Interface n} (s : State I) : State I :=
  { s with epoch := s.epoch + 1, pending := false, acks := ∅,
           certificates := Function.update s.certificates s.epoch s.acks }

def deliver {n} {I : Interface n} (c : Config I) (s : State I) (i : Fin n) (e : Nat) : State I :=
  if I.policyEpoch (s.roots i).descriptor < e then
    setRoot s i { s.roots i with descriptor := c.source e }
  else s

def prepare {n} {I : Interface n} (s : State I) (i : Fin n) (k : I.Command) : State I :=
  setRoot s i { s.roots i with commitments := insert k (s.roots i).commitments }

def cancelAck {n} {I : Interface n} (c : Config I) (s : State I) (i : Fin n)
    (k : I.Command) : State I :=
  { s with cancelAcks := Function.update s.cancelAcks k (insert i (s.cancelAcks k))
           roots := if Good c i then Function.update s.roots i
             { s.roots i with cancelled := insert k (s.roots i).cancelled } else s.roots }

/-- The global predicate classifies an already admitted effect; Lands never
reads it. The absorbing damage branch matches the original history kernel. -/
def land {n} {I : Interface n} (c : Config I) (s : State I) (time : Nat)
    (k : I.Command) (requester : I.Requester) : State I :=
  if s.damaged = true ∨ ¬I.admits s.plant time (c.source s.epoch) k requester
  then { s with damaged := true }
  else { s with plant := I.effect s.plant k }

inductive Event {n} (I : Interface n) where
  | request
  | acknowledge (i : Fin n)
  | complete
  | deliver (i : Fin n) (epoch : Nat)
  | prepare (i : Fin n) (command : I.Command) (requester : I.Requester) (time : Nat)
  | cancelAck (i : Fin n) (command : I.Command) (requester : I.Requester)
  | close (command : I.Command)
  | land (command : I.Command) (requester : I.Requester) (time : Nat)
  | hold
  | corrupt (i : Fin n) (root : RootState I)

inductive Step {n} {I : Interface n} (c : Config I) : State I → Event I → State I → Prop where
  | request (s) (idle : s.pending = false) : Step c s .request (request s)
  | acknowledge (s i) (pending : s.pending = true) :
      Step c s (.acknowledge i) (acknowledge c s i)
  | complete (s) (pending : s.pending = true) (quorum : s.acks.card = c.r) :
      Step c s .complete (complete s)
  | deliver (s i e) (existsCert : 0 < e ∧ e ≤ s.epoch) :
      Step c s (.deliver i e) (deliver c s i e)
  | prepare (s i k requester time) (selected : i ∈ I.commandPath k) (path : ValidPath c k)
      (grant : i ∈ c.faulty ∨ Envelope s.plant time (s.roots i) k requester) :
      Step c s (.prepare i k requester time) (prepare s i k)
  | cancelAck (s i k requester) (selected : i ∈ I.commandPath k)
      (auth : i ∈ c.faulty ∨ requester = I.recipient k) :
      Step c s (.cancelAck i k requester) (cancelAck c s i k)
  | close (s k) (certificate : c.budget < (s.cancelAcks k).card) :
      Step c s (.close k) s
  | land (s k requester time) (admitted : Lands c s time k requester) :
      Step c s (.land k requester time) (land c s time k requester)
  | hold (s) : Step c s .hold s
  | corrupt (s i z) (bad : i ∈ c.faulty) :
      Step c s (.corrupt i z) (setRoot s i z)

inductive Trace {n} {I : Interface n} (c : Config I) : State I → List (Event I) → State I → Prop where
  | nil (s) : Trace c s [] s
  | cons {s t u a as} : Step c s a t → Trace c t as u → Trace c s (a :: as) u

def Reachable {n} {I : Interface n} (c : Config I) (s : State I) : Prop :=
  ∃ plant events, Trace c (Initial c plant) events s

/-- Only structural history facts, with no desired safety or goal as a field. -/
structure Consistent {n} {I : Interface n} (c : Config I) (s : State I) : Prop where
  local_authentic : ∀ i, Good c i →
    (s.roots i).descriptor = c.source (I.policyEpoch (s.roots i).descriptor)
  local_not_future : ∀ i, Good c i → I.policyEpoch (s.roots i).descriptor ≤ s.epoch
  past_certificates : ∀ e, e < s.epoch → (s.certificates e).card = c.r ∧
    ∀ i ∈ s.certificates e, Good c i → e ∈ (s.roots i).revoked
  pending_revoked : ∀ i ∈ s.acks, Good c i → s.epoch ∈ (s.roots i).revoked
  cancel_selected : ∀ k i, i ∈ s.cancelAcks k → i ∈ I.commandPath k
  cancel_durable : ∀ k i, i ∈ s.cancelAcks k → Good c i → k ∈ (s.roots i).cancelled

end
end OperationalJoin
