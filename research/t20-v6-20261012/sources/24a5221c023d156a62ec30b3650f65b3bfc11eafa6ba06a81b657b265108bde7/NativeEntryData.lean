import NativeInitialWitness
import NativePolicyInputs

namespace SharedAlias.Native.Entry
open ComposedExecution
open OperationalJoin.Typed (interface)

/-- Stored completion-acknowledger row. Presence and distinct-label shape
are executable checks; genuine completion requires accepted reachable history. -/
def completionRow {m} (D : Routing m) (C : FiniteState m) : Nat → Option (List (Fin m))
  | 0 => none
  | e + 1 => do
      let labels ← tableFind C.certificateRows e
      if labels.toFinset.card = D.r then some labels else none

/-- All finite samples remain explicit. This checker does not authenticate
policy content or validate a history. In particular a forged coherent input
can pass shape checks without satisfying the theorem's external premises. -/
def checkedPolicy {m} (D : Routing m) (C : FiniteState m) (actor : Actor)
    (samples : List (Nat × Policy)) (syncBits : List Bool) : Option Policy := do
  if C.pending then none else do
    if actor.policy.epoch = C.epoch ∧ actor.observedPlant = C.plant ∧ syncBits.length = m then
      let policy ← policySample samples actor.policy.epoch
      if policy = actor.policy then
        if C.epoch = 0 then some policy else do
          let _ ← completionRow D C C.epoch
          some policy
      else none
    else none

def syncReply {m} (bits : List Bool) (i : Fin m) : Bool := bits.getD i.val false

/-- One numerical legality test plus the prescribed service response. Good
slots complete; a bad label can withhold. No source function is queried. -/
def syncAllowed {m} (D : Routing m) (C : FiniteState m) (policy : Policy)
    (i : Fin m) (reply : Bool) : Bool :=
  decide (0 < policy.epoch ∧ policy.epoch ≤ C.epoch) && (!faulty D i || reply)

def syncSlot {m} (D : Routing m) (C : FiniteState m) (policy : Policy)
    (i : Fin m) (reply : Bool) : FiniteState m :=
  if syncAllowed D C policy i reply then deliverUpdate D C i policy else C

def syncEvent {m} (D : Routing m) (C : FiniteState m) (policy : Policy)
    (i : Fin m) (reply : Bool) : OperationalJoin.Event (interface m) :=
  if syncAllowed D C policy i reply then .deliver i policy.epoch else .hold

/-- An explicit public order, independent of aliases and faults. -/
def publicLabels (m : Nat) : List (Fin m) := List.finRange m

def publicPrelude (m : Nat) (actor : Actor) : List (Fin m × Nat) :=
  (publicLabels m).map (fun i => (i, actor.policy.epoch))

def syncRun {m} (D : Routing m) (C : FiniteState m) (policy : Policy)
    (bits : List Bool) : Outcome m :=
  serviceLoop (fun C i => (syncSlot D C policy i (syncReply bits i),
    syncEvent D C policy i (syncReply bits i))) C (publicLabels m)

/-- Entry into an existing finite state: never reset the plant or memories.
The public programme is compiled unchanged before environmental service. -/
def runRepresented {m} (D : Routing m) (C : FiniteState m) (actor : Actor)
    (action : Action) (paths : List (OrderedPath m)) (samples : List (Nat × Policy))
    (syncBits : List Bool) (annotations : List (Annotation m)) : Option (Outcome m) := do
  let specs ← compileOrdered actor action paths annotations
  let policy ← checkedPolicy D C actor samples syncBits
  let sync := syncRun D C policy syncBits
  let result := runNative D actor.identity sync.state specs
  pure ⟨result.state, sync.events ++ result.events⟩

end SharedAlias.Native.Entry
