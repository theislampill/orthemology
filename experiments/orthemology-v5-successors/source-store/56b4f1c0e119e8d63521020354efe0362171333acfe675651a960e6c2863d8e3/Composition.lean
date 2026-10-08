import CriterionInstallation
import DynamicInterlock

namespace ComposedExecution
open TypedCriterionGuard (Source Target Grant)
open CriterionInstallation (Rule)

structure Plant where
  source : Source
  destination : String
  standard : String
  draft : List Nat
  draftRevision : Nat
  draftHistory : List (List Nat)
  rule : Rule
  ruleVersion : Nat
  ruleHistory : List Rule
  unrelated : List String
  deriving DecidableEq, BEq

structure Policy where
  target : Target
  destination : String
  actor : String
  scope : String
  epoch : Nat
  grant : Option Grant
  allowed : Bool := true
  deriving DecidableEq, BEq

inductive Action where
  | install (command : CriterionInstallation.InstallCommand)
  | repair (command : TypedCriterionGuard.Command)
  deriving DecidableEq, BEq

def Action.actor : Action → String
  | .install c => c.actor
  | .repair c => c.actor

def Action.operation : Action → String
  | .install c => c.operation
  | .repair c => c.operation

def Action.epoch : Action → Nat
  | .install c => c.authorizationEpoch
  | .repair c => c.authorizationEpoch

def policyAllows (p : Plant) (policy : Policy) (a : Action) : Bool :=
  policy.allowed && policy.target == p.source.target &&
  policy.destination == p.destination && policy.actor == a.actor &&
  policy.scope == a.operation

def ruleState (p : Plant) (policy : Policy) (now : Nat) : CriterionInstallation.RuleState :=
  { source := p.source, destination := p.destination, standard := p.standard,
    draft := p.draft, draftRevision := p.draftRevision, rule := p.rule,
    ruleVersion := p.ruleVersion, authorizationEpoch := policy.epoch,
    grant := policy.grant, revoked := !policy.allowed, now,
    ruleHistory := p.ruleHistory, unrelated := p.unrelated }

def dataState (p : Plant) (policy : Policy) (now : Nat) : TypedCriterionGuard.State :=
  { source := p.source, destination := p.destination, draft := p.draft,
    revision := p.draftRevision, authorizationEpoch := policy.epoch,
    grant := policy.grant, revoked := !policy.allowed, now,
    history := p.draftHistory }

def installProjection (p : Plant) (s : CriterionInstallation.RuleState) : Plant :=
  { p with rule := s.rule, ruleVersion := s.ruleVersion, ruleHistory := s.ruleHistory }

def repairProjection (p : Plant) (s : TypedCriterionGuard.State) : Plant :=
  { p with draft := s.draft, draftRevision := s.revision, draftHistory := s.history }

/- These calls are the runtime decisions. No parallel Python evaluator exists.
The additional rule constructor and interpreter checks connect the old protocol
string to the actually installed acceptance rule. -/
def localStep (p : Plant) (policy : Policy) (now : Nat) (a : Action) : Option Plant :=
  if policyAllows p policy a then
    match a with
    | .install c =>
        let result := CriterionInstallation.install (ruleState p policy now) c
        if result.applied then some (installProjection p result.state) else none
    | .repair c =>
        if decide (p.rule = .exact) && CriterionInstallation.accepts p.rule c.payload p.source.content then
          let result := TypedCriterionGuard.execute (dataState p policy now) c
          if result.applied then some (repairProjection p result.state) else none
        else none
  else none

def Goals (p : Plant) : Prop := p.rule = .exact ∧ p.draft = p.source.content

structure Envelope where
  action : Action
  successor : Plant
  nonce : Nat
  path : List Nat
  deriving DecidableEq

structure Root where
  policy : Policy
  revoked : List Nat := []
  commitments : List Envelope := []
  cancelled : List Envelope := []

structure Certificate where
  previousEpoch : Nat
  policy : Policy
  acknowledgers : List Nat
  deriving DecidableEq

structure World where
  n : Nat
  budget : Nat
  q : Nat
  r : Nat
  effectivePolicy : Policy
  plant : Plant
  now : Nat
  roots : Nat → Root
  tainted : Nat → Bool
  completed : List Certificate := []

structure Actor where
  policy : Policy
  observedPlant : Plant
  identity : String
  observedTime : Nat
  nonce : Nat := 0

def initialWorld (p : Plant) (policy : Policy) (bad : List Nat) : World :=
  ⟨4, 1, 3, 3, policy, p, 2, fun _ => ⟨policy, [], [], []⟩, fun i => bad.contains i, []⟩

def propose (actor : Actor) (a : Action) (path : List Nat) : Option Envelope :=
  (localStep actor.observedPlant actor.policy actor.observedTime a).map
    (fun p => ⟨a, p, actor.nonce + 1, path⟩)

def validPath (w : World) (e : Envelope) : Bool :=
  decide (e.path.Nodup ∧ e.path.length = w.q ∧ ∀ i ∈ e.path, i < w.n)

def Eligible (p : Plant) (now : Nat) (root : Root) (e : Envelope) (requester : String) : Prop :=
  requester = e.action.actor ∧ e.action.epoch ∉ root.revoked ∧ e ∉ root.cancelled ∧
  localStep p root.policy now e.action = some e.successor

instance (p : Plant) (now : Nat) (root : Root) (e : Envelope) (requester : String) :
    Decidable (Eligible p now root e requester) := by
  unfold Eligible
  infer_instance

def rootPermits (p : Plant) (now : Nat) (root : Root) (e : Envelope) (requester : String) : Bool :=
  decide (e ∈ root.commitments ∧ Eligible p now root e requester)

def prepare (w : World) (e : Envelope) (requester : String) (badSign : Bool := true) : World × Bool :=
  if validPath w e then
    let signs := fun i => if w.tainted i then badSign
      else decide (Eligible w.plant w.now (w.roots i) e requester)
    let roots := fun i => if e.path.contains i && signs i then
      { w.roots i with commitments := e :: (w.roots i).commitments } else w.roots i
    ({ w with roots }, e.path.all signs)
  else (w, false)

def gateOpen (w : World) (e : Envelope) (requester : String) (badOpen : Bool) (i : Nat) : Bool :=
  if w.tainted i then badOpen else rootPermits w.plant w.now (w.roots i) e requester

/- The only mutation event. This intentionally does not inspect effectivePolicy.
Every selected gate checks the complete envelope against its local policy and
an atomic observation of the same actual Plant. No cached votes are used. -/
def attempt (w : World) (e : Envelope) (requester : String) (badOpen : Bool := true) : World × Bool :=
  if validPath w e && e.path.all (gateOpen w e requester badOpen) then
    (w, true)
  else (w, false)

def cancelWith (w : World) (e : Envelope) (requester : String) (acks : List Nat) : World × Bool :=
  if validPath w e && decide (acks.Nodup ∧ ∀ i ∈ acks, i ∈ e.path) then
    let responders := acks.filter (fun i => w.tainted i || requester == e.action.actor)
    let roots := fun i => if acks.contains i && !w.tainted i && requester == e.action.actor then
      { w.roots i with cancelled := e :: (w.roots i).cancelled } else w.roots i
    let cancel_threshold := w.budget + 1
    ({ w with roots }, decide (cancel_threshold ≤ responders.length))
  else (w, false)

/- The legitimate owner's serial next Policy is an external model input.
This operation simulates certificate completion; it grants no real authority.
Intact acknowledgers close before completion and do not yet install next. -/
def certifyTransition (w : World) (acks : List Nat) (next : Policy) : World × Option Certificate :=
  if decide (acks.Nodup ∧ acks.length = w.r ∧ (∀ i ∈ acks, i < w.n) ∧
      next.epoch = w.effectivePolicy.epoch + 1) then
    let roots := fun i => if acks.contains i && !w.tainted i then
      { w.roots i with revoked := w.effectivePolicy.epoch :: (w.roots i).revoked }
      else w.roots i
    let certificate := ⟨w.effectivePolicy.epoch, next, acks⟩
    ({ w with effectivePolicy := next, roots, completed := certificate :: w.completed }, some certificate)
  else (w, none)

def deliver (w : World) (certificate : Certificate) : World :=
  if decide (certificate ∈ w.completed) then
    { w with roots := fun i =>
        if !w.tainted i && decide ((w.roots i).policy.epoch < certificate.policy.epoch) then
          { w.roots i with policy := certificate.policy } else w.roots i }
  else w

def receiveActor (actor : Actor) (certificate : Certificate) (n r : Nat) : Actor :=
  if decide (certificate.acknowledgers.Nodup ∧ certificate.acknowledgers.length = r ∧
      (∀ i ∈ certificate.acknowledgers, i < n) ∧
      certificate.policy.epoch = certificate.previousEpoch + 1 ∧
      actor.policy.epoch < certificate.policy.epoch) then
    { actor with policy := certificate.policy }
  else actor

def fourPaths : List (List Nat) := [[0,1,2], [0,1,3], [0,2,3], [1,2,3]]

structure AttemptTrace where
  nonce : Nat
  path : List Nat
  prepared : Bool
  landed : Bool
  closed : Bool
  ruleVersion : Nat
  draftRevision : Nat
  deriving Repr

/- The four-path n=4/B=1 portfolio. The actor never stops on a receipt and
never sees the taint set. Faulty execution gates withhold; preparation and
cancellation may mimic honest responses. Each new trial has a fresh nonce.
No real-time clock advance is inferred from these logical service phases. -/
def runBatch (w : World) (actor : Actor) (a : Action) : World × List AttemptTrace :=
  fourPaths.foldl (fun acc path =>
    let current := acc.1
    let traces := acc.2
    let trialActor := { actor with nonce := actor.nonce + traces.length }
    match propose trialActor a path with
    | none => (current, traces ++ [⟨trialActor.nonce + 1, path, false, false, true,
        current.plant.ruleVersion, current.plant.draftRevision⟩])
    | some e =>
        let prepared := prepare current e actor.identity
        let landed := if prepared.2 then attempt prepared.1 e actor.identity false else (prepared.1, false)
        let closed := cancelWith landed.1 e actor.identity e.path
        (closed.1, traces ++ [⟨e.nonce, path, prepared.2, landed.2, closed.2,
          closed.1.plant.ruleVersion, closed.1.plant.draftRevision⟩])
    ) (w, [])

end ComposedExecution

