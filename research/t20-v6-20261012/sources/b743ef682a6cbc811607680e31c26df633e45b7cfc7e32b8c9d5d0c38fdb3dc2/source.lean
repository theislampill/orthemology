import Composition

namespace SharedAlias.Executable
open ComposedExecution

abbrev Command (m : Nat) :=
  { e : ComposedExecution.Envelope // e.path.Nodup ∧ ∀ i ∈ e.path, i < m }

def tableRead {α β : Type} [DecidableEq α] (rows : List (α × β)) (key : α) (fallback : β) : β :=
  match rows with
  | [] => fallback
  | (k, v) :: rest => if key = k then v else tableRead rest key fallback


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


/-- Complete source eligibility, not a nonce-only or unordered-key shortcut. -/
def prepareAllowed {m} (D : Routing m) (C : FiniteState m) (i : Fin m)
    (k : Command m) (who : String) (time : Nat) (badReply : Bool) : Bool :=
  decide (i.val ∈ k.val.path) &&
    ComposedExecution.validPath (gateWorld D C time C.defaultRoot.policy) k.val &&
    if faulty D i then badReply
    else decide (ComposedExecution.Eligible C.plant time (rootAt C (rootOf D i)) k.val who)

def prepareUpdate {m} (D : Routing m) (C : FiniteState m) (i : Fin m)
    (k : Command m) : FiniteState m :=
  let z := rootAt C (rootOf D i)
  setRoot C (rootOf D i) { z with commitments := k.val :: z.commitments }

def prepareSlot {m} (D : Routing m) (C : FiniteState m) (i : Fin m)
    (k : Command m) (who : String) (time : Nat) (badReply : Bool) : FiniteState m :=
  if prepareAllowed D C i k who time badReply then prepareUpdate D C i k else C

/-- One actual addressed receipt. The alias store update never issues a
receipt for a different label. -/
def cancelAllowed {m} (D : Routing m) (i : Fin m)
    (k : Command m) (who : String) (badReply : Bool) : Bool :=
  decide (i.val ∈ k.val.path) && if faulty D i then badReply else decide (who = k.val.action.actor)

def cancelUpdate {m} (D : Routing m) (C : FiniteState m) (i : Fin m)
    (k : Command m) : FiniteState m :=
  let R := { C with cancelRows := (k.val, i :: receipts C k.val) :: C.cancelRows }
  if faulty D i then R
  else
    let z := rootAt C (rootOf D i)
    setRoot R (rootOf D i) { z with cancelled := k.val :: z.cancelled }

def cancelSlot {m} (D : Routing m) (C : FiniteState m) (i : Fin m)
    (k : Command m) (who : String) (badReply : Bool) : FiniteState m :=
  if cancelAllowed D i k who badReply then cancelUpdate D C i k else C

/-- Literally call the unchanged executable source attempt. Its policy field
is unused by that live gate; no authority is inferred from defaultRoot. -/
def applied {m} (D : Routing m) (C : FiniteState m)
    (k : Command m) (who : String) (time : Nat) (badOpen : Bool) : Bool :=
  (ComposedExecution.attempt (gateWorld D C time C.defaultRoot.policy) k.val who badOpen).2

def attemptSlot {m} (D : Routing m) (C : FiniteState m)
    (k : Command m) (who : String) (time : Nat) (badOpen : Bool) : FiniteState m :=
  let result := ComposedExecution.attempt (gateWorld D C time C.defaultRoot.policy) k.val who badOpen
  if result.2 then { C with plant := result.1.plant } else C

/-- Finite distinct-label counting without a proof-library dependency. -/
def distinctCount {α : Type} [DecidableEq α] : List α → Nat
  | [] => 0
  | x :: xs => if x ∈ xs then distinctCount xs else distinctCount xs + 1

def closed {m} (D : Routing m) (C : FiniteState m) (k : Command m) : Bool :=
  decide (D.budget < distinctCount (receipts C k.val))

inductive ServiceEvent (m : Nat) where
  | prepare (i : Fin m) (k : Command m) (who : String) (time : Nat)
  | cancelAck (i : Fin m) (k : Command m) (who : String)
  | land (k : Command m) (who : String) (time : Nat)
  | close (k : Command m)
  | hold

/-- Actual emitted events use precisely the same executable branch as state. -/
def prepareEvent {m} (D : Routing m) (C : FiniteState m) (i : Fin m)
    (k : Command m) (who : String) (time : Nat) (badReply : Bool) :
    ServiceEvent m :=
  if prepareAllowed D C i k who time badReply then .prepare i k who time else .hold

def cancelEvent {m} (D : Routing m) (i : Fin m)
    (k : Command m) (who : String) (badReply : Bool) :
    ServiceEvent m :=
  if cancelAllowed D i k who badReply then .cancelAck i k who else .hold

def attemptEvent {m} (D : Routing m) (C : FiniteState m)
    (k : Command m) (who : String) (time : Nat) (badOpen : Bool) :
    ServiceEvent m :=
  if applied D C k who time badOpen then .land k who time else .hold

def closeEvent {m} (D : Routing m) (C : FiniteState m) (k : Command m) :
    ServiceEvent m :=
  if closed D C k then .close k else .hold


/-- An explicit public ordering, not Finset.toList and not a root-map query. -/
abbrev OrderedPath (m : Nat) := { labels : List (Fin m) // labels.Nodup }

def orderedLabelList {m} (path : OrderedPath m) : List Nat := path.val.map Fin.val

theorem orderedLabelList_nodup {m} (path : OrderedPath m) : (orderedLabelList path).Nodup :=
  path.property.map (fun i j h => Fin.ext h)

theorem orderedLabelList_bounded {m} (path : OrderedPath m) : ∀ i ∈ orderedLabelList path, i < m := by
  intro i member
  obtain ⟨j, _, rfl⟩ := List.mem_map.mp member
  exact j.isLt

def issueOrdered {m} (actor : Actor) (action : Action) (next : Plant)
    (n : Nat) (path : OrderedPath m) : Command m :=
  ⟨⟨action, next, actor.nonce + n + 1, orderedLabelList path⟩,
    orderedLabelList_nodup path, orderedLabelList_bounded path⟩

/-- Actor-only computation. No hidden environment, actual state, clock,
service response or acknowledgement is accepted by this function. -/
def orderedCommands {m} (actor : Actor) (action : Action) (next : Plant) :
    Nat → List (OrderedPath m) → List (Command m)
  | _, [] => []
  | n, path :: rest => issueOrdered actor action next n path :: orderedCommands actor action next (n+1) rest

def orderedProgram {m} (actor : Actor) (action : Action) (paths : List (OrderedPath m)) :
    Option (List (Command m)) :=
  (ComposedExecution.localStep actor.observedPlant actor.policy actor.observedTime action).map
    (fun next => orderedCommands actor action next 0 paths)

/-- Explicit finite service data. The checked annotation constructor below
requires exactly m prepare bits and m cancel bits at every trial. -/
structure Annotation (m : Nat) where
  time : Nat
  prepareBits : List Bool
  openGate : Bool
  cancelBits : List Bool

def annotationValid {m} (a : Annotation m) : Bool :=
  decide (a.prepareBits.length = m ∧ a.cancelBits.length = m)

def prepareReply {m} (a : Annotation m) (i : Fin m) : Bool := a.prepareBits.getD i.val false
def cancelReply {m} (a : Annotation m) (i : Fin m) : Bool := a.cancelBits.getD i.val false

structure Spec (m : Nat) where
  command : Command m
  annotation : Annotation m

/-- Exact-length consumption. BOTH missing and excess annotations reject;
no zip/truncation or fabricated clock sample changes the public program. -/
def annotate {m} : List (Command m) → List (Annotation m) → Option (List (Spec m))
  | [], [] => some []
  | k :: commands, a :: annotations =>
      if annotationValid a then (annotate commands annotations).map (fun rest => ⟨k,a⟩ :: rest)
      else none
  | _, _ => none

def compileOrdered {m} (actor : Actor) (action : Action) (paths : List (OrderedPath m))
    (annotations : List (Annotation m)) : Option (List (Spec m)) := do
  let commands ← orderedProgram actor action paths
  annotate commands annotations


/-- Recover the bounded labels in the exact order stored in this command.
No Finset.toList or hidden routing input is used. -/
def commandLabels {m} (k : Command m) : List (Fin m) :=
  k.val.path.attach.map (fun item => ⟨item.val, k.property.2 item.val item.property⟩)

structure Outcome (m : Nat) where
  state : FiniteState m
  events : List (ServiceEvent m)

/-- One slot emits one genuine accepted primitive event (possibly hold). -/
def serviceLoop {m} (handler : FiniteState m → Fin m →
    FiniteState m × ServiceEvent m) :
    FiniteState m → List (Fin m) → Outcome m
  | C, [] => ⟨C, []⟩
  | C, i :: rest =>
      let first := handler C i
      let later := serviceLoop handler first.1 rest
      ⟨later.state, first.2 :: later.events⟩

def prepareRun {m} (D : Routing m) (C : FiniteState m) (k : Command m)
    (who : String) (a : Annotation m) : Outcome m :=
  serviceLoop (fun C i =>
    (prepareSlot D C i k who a.time (prepareReply a i),
     prepareEvent D C i k who a.time (prepareReply a i))) C (commandLabels k)

def cancelRun {m} (D : Routing m) (C : FiniteState m) (k : Command m)
    (who : String) (a : Annotation m) : Outcome m :=
  serviceLoop (fun C i =>
    (cancelSlot D C i k who (cancelReply a i),
     cancelEvent D i k who (cancelReply a i))) C (commandLabels k)

def trialRun {m} (D : Routing m) (C : FiniteState m) (who : String) (spec : Spec m) : Outcome m :=
  let prep := prepareRun D C spec.command who spec.annotation
  let landed := attemptSlot D prep.state spec.command who spec.annotation.time spec.annotation.openGate
  let event := attemptEvent D prep.state spec.command who spec.annotation.time spec.annotation.openGate
  let cancel := cancelRun D landed spec.command who spec.annotation
  ⟨cancel.state, prep.events ++ event :: (cancel.events ++ [closeEvent D cancel.state spec.command])⟩

/-- The controller deliberately services every fixed public trial. It does
not trust a success receipt or inspect the hidden environment to choose paths. -/
def runNative {m} (D : Routing m) (who : String) : FiniteState m → List (Spec m) → Outcome m
  | C, [] => ⟨C, []⟩
  | C, spec :: rest =>
      let first := trialRun D C who spec
      let later := runNative D who first.state rest
      ⟨later.state, first.events ++ later.events⟩


/-- Specialized epoch-zero entry point. It creates the stated initial finite
reference machine, emits m completed hold/sync slots, then all public trials.
It does not implement nonzero delivery or infer missing source authority. -/
def runInitial {m} (D : Routing m) (actor : Actor) (action : Action)
    (paths : List (OrderedPath m)) (annotations : List (Annotation m)) : Option (Outcome m) :=
  if actor.policy.epoch = 0 then
    (compileOrdered actor action paths annotations).map (fun specs =>
      let result := runNative D actor.identity (initial actor.policy actor.observedPlant) specs
      ⟨result.state, List.replicate m .hold ++ result.events⟩)
  else none


end SharedAlias.Executable
