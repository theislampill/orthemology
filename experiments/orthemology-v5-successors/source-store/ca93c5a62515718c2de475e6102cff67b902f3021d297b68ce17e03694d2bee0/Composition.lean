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

theorem local_install_refinement (p : Plant) (policy : Policy) (now : Nat)
    (c : CriterionInstallation.InstallCommand) (next : Plant)
    (h : localStep p policy now (.install c) = some next) :
    policyAllows p policy (.install c) = true ∧
    (CriterionInstallation.install (ruleState p policy now) c).applied = true ∧
    next = installProjection p (CriterionInstallation.install (ruleState p policy now) c).state := by
  simp only [localStep] at h
  split at h
  · rename_i hp
    split at h
    · rename_i ha
      exact ⟨hp, ha, (Option.some.inj h).symm⟩
    · cases h
  · cases h

theorem local_repair_refinement (p : Plant) (policy : Policy) (now : Nat)
    (c : TypedCriterionGuard.Command) (next : Plant)
    (h : localStep p policy now (.repair c) = some next) :
    policyAllows p policy (.repair c) = true ∧ p.rule = .exact ∧
    CriterionInstallation.accepts p.rule c.payload p.source.content = true ∧
    (TypedCriterionGuard.execute (dataState p policy now) c).applied = true ∧
    next = repairProjection p (TypedCriterionGuard.execute (dataState p policy now) c).state := by
  simp only [localStep] at h
  split at h
  · rename_i hp
    split at h
    · rename_i hr
      have hr' : (decide (p.rule = .exact)) = true ∧ CriterionInstallation.accepts p.rule c.payload p.source.content = true := by simpa only [Bool.and_eq_true] using hr
      have ruleEq : p.rule = .exact := of_decide_eq_true hr'.1
      split at h
      · rename_i ha
        exact ⟨hp, ruleEq, hr'.2, ha, (Option.some.inj h).symm⟩
      · cases h
    · cases h
  · cases h

theorem local_source_and_custody_frame (p : Plant) (policy : Policy) (now : Nat)
    (a : Action) (next : Plant) (h : localStep p policy now a = some next) :
    next.source = p.source ∧ next.destination = p.destination ∧
    next.standard = p.standard ∧ next.unrelated = p.unrelated := by
  cases a with
  | install c =>
      obtain ⟨_, _, rfl⟩ := local_install_refinement p policy now c next h
      exact ⟨rfl, rfl, rfl, rfl⟩
  | repair c =>
      obtain ⟨_, _, _, _, rfl⟩ := local_repair_refinement p policy now c next h
      exact ⟨rfl, rfl, rfl, rfl⟩

theorem local_install_full_effect (p : Plant) (policy : Policy) (now : Nat)
    (c : CriterionInstallation.InstallCommand) (next : Plant)
    (h : localStep p policy now (.install c) = some next) :
    next = { p with rule := .exact, ruleVersion := p.ruleVersion + 1,
                     ruleHistory := p.ruleHistory ++ [p.rule] } := by
  obtain ⟨_, ha, rfl⟩ := local_install_refinement p policy now c next h
  obtain ⟨hr, hv, hh⟩ := CriterionInstallation.accepted_changes_rule_and_history
    (ruleState p policy now) c ha
  unfold installProjection
  rw [hr, hv, hh]
  rfl

theorem local_repair_full_effect (p : Plant) (policy : Policy) (now : Nat)
    (c : TypedCriterionGuard.Command) (next : Plant)
    (h : localStep p policy now (.repair c) = some next) :
    next = { p with draft := p.source.content, draftRevision := p.draftRevision + 1,
                     draftHistory := p.draftHistory ++ [p.draft] } := by
  obtain ⟨_, _, _, ha, rfl⟩ := local_repair_refinement p policy now c next h
  obtain ⟨hd, hv, hh⟩ := TypedCriterionGuard.accepted_repairs_and_retains_history
    (dataState p policy now) c ha
  unfold repairProjection
  rw [hd, hv, hh]
  rfl

theorem local_install_expected_version (p : Plant) (policy : Policy) (now : Nat)
    (c : CriterionInstallation.InstallCommand) (next : Plant)
    (h : localStep p policy now (.install c) = some next) :
    c.expectedVersion = p.ruleVersion := by
  have ha := (local_install_refinement p policy now c next h).2.1
  have hv := (CriterionInstallation.applied_iff_valid (ruleState p policy now) c).mp ha
  exact hv.2.2.2.2.1

theorem local_repair_expected_revision (p : Plant) (policy : Policy) (now : Nat)
    (c : TypedCriterionGuard.Command) (next : Plant)
    (h : localStep p policy now (.repair c) = some next) :
    c.expectedRevision = p.draftRevision := by
  have ha := (local_repair_refinement p policy now c next h).2.2.2.1
  have hv := (TypedCriterionGuard.applied_iff_context_valid (dataState p policy now) c).mp ha
  exact hv.2.2.2.1

theorem fixed_action_cannot_succeed_twice (p : Plant) (policy : Policy) (now : Nat)
    (a : Action) (next : Plant) (h : localStep p policy now a = some next)
    (laterPolicy : Policy) (laterNow : Nat) : localStep next laterPolicy laterNow a = none := by
  cases hx : localStep next laterPolicy laterNow a with
  | none => rfl
  | some later =>
      exfalso
      cases a with
      | install c =>
          have old := local_install_expected_version p policy now c next h
          have new := local_install_expected_version next laterPolicy laterNow c later hx
          have effect := local_install_full_effect p policy now c next h
          rw [effect] at new
          simp only at new
          omega
      | repair c =>
          have old := local_repair_expected_revision p policy now c next h
          have new := local_repair_expected_revision next laterPolicy laterNow c later hx
          have effect := local_repair_full_effect p policy now c next h
          rw [effect] at new
          simp only at new
          omega

def Goals (p : Plant) : Prop := p.rule = .exact ∧ p.draft = p.source.content

theorem local_goals_persist (p : Plant) (policy : Policy) (now : Nat)
    (a : Action) (next : Plant) (h : localStep p policy now a = some next)
    (goals : Goals p) : Goals next := by
  cases a with
  | install c =>
      rw [local_install_full_effect p policy now c next h]
      exact ⟨rfl, goals.2⟩
  | repair c =>
      rw [local_repair_full_effect p policy now c next h]
      exact ⟨goals.1, rfl⟩


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
    ({ w with plant := e.successor }, true)
  else (w, false)

theorem permits_imported_step (p : Plant) (now : Nat) (root : Root)
    (e : Envelope) (requester : String)
    (h : rootPermits p now root e requester = true) :
    localStep p root.policy now e.action = some e.successor := by
  have hv : e ∈ root.commitments ∧ Eligible p now root e requester := of_decide_eq_true h
  exact hv.2.2.2.2

theorem live_landing_refines_imported_step (w : World) (e : Envelope)
    (requester : String) (badOpen : Bool)
    (budget : ChargedInterlock.card w.n w.tainted ≤ w.budget)
    (large : w.budget < ChargedInterlock.card w.n (fun i => decide (i ∈ e.path)))
    (lands : ChargedInterlock.Lands w.n (fun i => decide (i ∈ e.path))
      (fun i => gateOpen w e requester badOpen i = true)) :
    ∃ i, i < w.n ∧ w.tainted i = false ∧
      localStep w.plant (w.roots i).policy w.now e.action = some e.successor := by
  obtain ⟨i, hi, hl, hc⟩ := ChargedInterlock.honest_on_large_path
    w.n w.budget (fun i => decide (i ∈ e.path)) w.tainted budget large
  have opened := lands i hi hl
  simp only [gateOpen, hc, Bool.false_eq_true, if_false] at opened
  exact ⟨i, hi, hc, permits_imported_step w.plant w.now (w.roots i) e requester opened⟩

theorem live_landing_preserves_source (w : World) (e : Envelope)
    (requester : String) (badOpen : Bool)
    (budget : ChargedInterlock.card w.n w.tainted ≤ w.budget)
    (large : w.budget < ChargedInterlock.card w.n (fun i => decide (i ∈ e.path)))
    (lands : ChargedInterlock.Lands w.n (fun i => decide (i ∈ e.path))
      (fun i => gateOpen w e requester badOpen i = true)) :
    e.successor.source = w.plant.source := by
  obtain ⟨i, _, _, step⟩ := live_landing_refines_imported_step w e requester badOpen budget large lands
  exact (local_source_and_custody_frame w.plant (w.roots i).policy w.now e.action e.successor step).1


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

theorem attempt_applied_implies_lands (w : World) (e : Envelope)
    (requester : String) (badOpen : Bool) (h : (attempt w e requester badOpen).2 = true) :
    ChargedInterlock.Lands w.n (fun i => decide (i ∈ e.path))
      (fun i => gateOpen w e requester badOpen i = true) := by
  unfold attempt at h
  split at h
  · rename_i hc
    have parts : validPath w e = true ∧ e.path.all (gateOpen w e requester badOpen) = true := by
      simpa only [Bool.and_eq_true] using hc
    intro i _hi hp
    exact List.all_eq_true.mp parts.2 i (of_decide_eq_true hp)
  · cases h

theorem cancelled_root_veto (p : Plant) (now : Nat) (root : Root)
    (e : Envelope) (requester : String) (cancelled : e ∈ root.cancelled) :
    rootPermits p now root e requester ≠ true := by
  intro h
  have hv : e ∈ root.commitments ∧ Eligible p now root e requester := of_decide_eq_true h
  exact hv.2.2.2.1 cancelled

theorem revoked_root_veto (p : Plant) (now : Nat) (root : Root)
    (e : Envelope) (requester : String) (revoked : e.action.epoch ∈ root.revoked) :
    rootPermits p now root e requester ≠ true := by
  intro h
  have hv : e ∈ root.commitments ∧ Eligible p now root e requester := of_decide_eq_true h
  exact hv.2.2.1 revoked

theorem cancellation_excludes_landing (w : World) (e : Envelope)
    (requester : String) (badOpen : Bool) (cancelSet : Nat → Bool)
    (budget : ChargedInterlock.card w.n w.tainted ≤ w.budget)
    (cancel_threshold : w.budget < ChargedInterlock.card w.n cancelSet)
    (selected : ∀ i, i < w.n → cancelSet i = true → decide (i ∈ e.path) = true)
    (tombstones : ∀ i, i < w.n → cancelSet i = true → w.tainted i = false → e ∈ (w.roots i).cancelled) :
    (attempt w e requester badOpen).2 ≠ true := by
  intro ha
  apply ChargedInterlock.charged_cancellation_blocks w.n w.budget
    (fun i => decide (i ∈ e.path)) cancelSet w.tainted
    (fun i => gateOpen w e requester badOpen i = true) budget cancel_threshold selected
    ?_ (attempt_applied_implies_lands w e requester badOpen ha)
  intro i hi hs hc
  simp only [gateOpen, hc, Bool.false_eq_true, if_false]
  exact cancelled_root_veto w.plant w.now (w.roots i) e requester (tombstones i hi hs hc)

theorem effective_revocation_excludes_landing (w : World) (e : Envelope)
    (requester : String) (badOpen : Bool) (ackSet : Nat → Bool)
    (budget : ChargedInterlock.card w.n w.tainted ≤ w.budget)
    (overlap : w.n + w.budget <
      ChargedInterlock.card w.n (fun i => decide (i ∈ e.path)) + ChargedInterlock.card w.n ackSet)
    (revocations : ∀ i, i < w.n → ackSet i = true → w.tainted i = false →
      e.action.epoch ∈ (w.roots i).revoked) :
    (attempt w e requester badOpen).2 ≠ true := by
  intro ha
  apply ChargedInterlock.effective_revocation_blocks w.n w.budget
    (fun i => decide (i ∈ e.path)) ackSet w.tainted
    (fun i => gateOpen w e requester badOpen i = true) budget overlap
    ?_ (attempt_applied_implies_lands w e requester badOpen ha)
  intro i hi hs hc
  simp only [gateOpen, hc, Bool.false_eq_true, if_false]
  exact revoked_root_veto w.plant w.now (w.roots i) e requester (revocations i hi hs hc)


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

theorem rejected_attempt_full_identity (w : World) (e : Envelope)
    (requester : String) (badOpen : Bool) (h : (attempt w e requester badOpen).2 = false) :
    (attempt w e requester badOpen).1 = w := by
  unfold attempt at h ⊢
  split
  · split at h <;> simp_all
  · rfl

theorem applied_attempt_exact_successor (w : World) (e : Envelope)
    (requester : String) (badOpen : Bool) (h : (attempt w e requester badOpen).2 = true) :
    (attempt w e requester badOpen).1.plant = e.successor := by
  unfold attempt at h ⊢
  split
  · rfl
  · split at h <;> simp_all

/- This theorem handles full version/history state, not just visible rule
labels. After a successful source transition, no root with a later authentic
policy can admit the same action from that successor, even before cancellation. -/
theorem successor_cannot_reland_fixed_action (p : Plant) (policy : Policy) (now : Nat)
    (e : Envelope) (step : localStep p policy now e.action = some e.successor)
    (later : World) (samePlant : later.plant = e.successor)
    (requester : String) (badOpen : Bool)
    (budget : ChargedInterlock.card later.n later.tainted ≤ later.budget)
    (large : later.budget < ChargedInterlock.card later.n (fun i => decide (i ∈ e.path))) :
    (attempt later e requester badOpen).2 ≠ true := by
  intro ha
  obtain ⟨i, _, _, hs⟩ := live_landing_refines_imported_step later e requester badOpen budget large
    (attempt_applied_implies_lands later e requester badOpen ha)
  rw [samePlant] at hs
  rw [fixed_action_cannot_succeed_twice p policy now e.action e.successor step
    (later.roots i).policy later.now] at hs
  cases hs

theorem attempted_goals_persist (w : World) (e : Envelope)
    (requester : String) (badOpen : Bool) (goals : Goals w.plant)
    (budget : ChargedInterlock.card w.n w.tainted ≤ w.budget)
    (large : w.budget < ChargedInterlock.card w.n (fun i => decide (i ∈ e.path))) :
    Goals (attempt w e requester badOpen).1.plant := by
  cases ha : (attempt w e requester badOpen).2 with
  | false =>
      rw [rejected_attempt_full_identity w e requester badOpen ha]
      exact goals
  | true =>
      rw [applied_attempt_exact_successor w e requester badOpen ha]
      obtain ⟨i, _, _, hs⟩ := live_landing_refines_imported_step w e requester badOpen budget large
        (attempt_applied_implies_lands w e requester badOpen ha)
      exact local_goals_persist w.plant (w.roots i).policy w.now e.action e.successor hs goals


/- Distinguish local proof validity from genuinely current policy. Serial,
authentic descriptor custody gives uniqueness at an epoch; certified-effective
reservation supplies the complete old-epoch veto witness. Neither premise is
inferred from a string or a hash. -/
theorem local_action_epoch (p : Plant) (policy : Policy) (now : Nat)
    (a : Action) (next : Plant) (h : localStep p policy now a = some next) :
    a.epoch = policy.epoch := by
  cases a with
  | install c =>
      have ha := (local_install_refinement p policy now c next h).2.1
      have hv := (CriterionInstallation.applied_iff_valid (ruleState p policy now) c).mp ha
      exact hv.2.2.2.2.2.1
  | repair c =>
      have ha := (local_repair_refinement p policy now c next h).2.2.2.1
      have hv := (TypedCriterionGuard.applied_iff_context_valid (dataState p policy now) c).mp ha
      exact hv.2.2.2.2.1

theorem landed_refines_effective_policy (w : World) (e : Envelope)
    (requester : String) (badOpen : Bool)
    (budget : ChargedInterlock.card w.n w.tainted ≤ w.budget)
    (large : w.budget < ChargedInterlock.card w.n (fun i => decide (i ∈ e.path)))
    (noFuturePolicy : ∀ i, i < w.n → w.tainted i = false →
      (w.roots i).policy.epoch ≤ w.effectivePolicy.epoch)
    (sameEpochPolicy : ∀ i, i < w.n → w.tainted i = false →
      (w.roots i).policy.epoch = w.effectivePolicy.epoch → (w.roots i).policy = w.effectivePolicy)
    (staleCertificate : e.action.epoch < w.effectivePolicy.epoch → ∃ ackSet : Nat → Bool,
      w.n + w.budget < ChargedInterlock.card w.n (fun i => decide (i ∈ e.path)) +
        ChargedInterlock.card w.n ackSet ∧
      (∀ i, i < w.n → ackSet i = true → w.tainted i = false → e.action.epoch ∈ (w.roots i).revoked))
    (ha : (attempt w e requester badOpen).2 = true) :
    localStep w.plant w.effectivePolicy w.now e.action = some e.successor := by
  obtain ⟨i, hi, hc, step⟩ := live_landing_refines_imported_step w e requester badOpen budget large
    (attempt_applied_implies_lands w e requester badOpen ha)
  have rootEpoch := local_action_epoch w.plant (w.roots i).policy w.now e.action e.successor step
  have noFuture := noFuturePolicy i hi hc
  have current : e.action.epoch = w.effectivePolicy.epoch := by
    apply Classical.byContradiction
    intro unequal
    have stale : e.action.epoch < w.effectivePolicy.epoch := by omega
    obtain ⟨ackSet, overlap, revoked⟩ := staleCertificate stale
    exact effective_revocation_excludes_landing w e requester badOpen ackSet budget overlap revoked ha
  have equalPolicy := sameEpochPolicy i hi hc (rootEpoch.symm.trans current)
  simpa only [equalPolicy] using step


theorem installed_successor_adequate (p : Plant) (policy : Policy) (now : Nat)
    (command : CriterionInstallation.InstallCommand) (next : Plant)
    (step : localStep p policy now (.install command) = some next) :
    ∀ candidate, CriterionInstallation.Accepts next.rule candidate next.source.content ↔
      candidate = p.source.content := by
  intro candidate
  rw [local_install_full_effect p policy now command next step]
  rfl

theorem installed_successor_changes_actual_behavior (p : Plant) (policy : Policy) (now : Nat)
    (command : CriterionInstallation.InstallCommand) (next : Plant)
    (oldRule : p.rule = .normalizedLF)
    (step : localStep p policy now (.install command) = some next) :
    CriterionInstallation.Accepts p.rule (p.source.content ++ [10]) p.source.content ∧
    ¬ CriterionInstallation.Accepts next.rule (p.source.content ++ [10]) next.source.content := by
  rw [local_install_full_effect p policy now command next step]
  constructor
  · rw [oldRule]
    exact (CriterionInstallation.normalized_rule_false_acceptance p.source.content).1
  · exact CriterionInstallation.appended_LF_changes_finite_sequence p.source.content


/- Definitional input boundary: the actor proposal receives its stored clock
observation, not World.now or a root's newer clock. Authenticity of this stored
observation is an external premise; stale observations remain possible. -/
theorem proposal_uses_actor_observation (actor : Actor) (a : Action) (path : List Nat) :
    propose actor a path =
      (localStep actor.observedPlant actor.policy actor.observedTime a).map
        (fun p => ⟨a, p, actor.nonce + 1, path⟩) := by
  rfl

end ComposedExecution

#print axioms ComposedExecution.local_install_refinement
#print axioms ComposedExecution.local_repair_refinement
#print axioms ComposedExecution.local_source_and_custody_frame
#print axioms ComposedExecution.local_install_full_effect
#print axioms ComposedExecution.local_repair_full_effect
#print axioms ComposedExecution.fixed_action_cannot_succeed_twice
#print axioms ComposedExecution.local_goals_persist

#print axioms ComposedExecution.live_landing_refines_imported_step
#print axioms ComposedExecution.live_landing_preserves_source

#print axioms ComposedExecution.attempt_applied_implies_lands
#print axioms ComposedExecution.cancellation_excludes_landing
#print axioms ComposedExecution.effective_revocation_excludes_landing

#print axioms ComposedExecution.rejected_attempt_full_identity
#print axioms ComposedExecution.applied_attempt_exact_successor
#print axioms ComposedExecution.successor_cannot_reland_fixed_action
#print axioms ComposedExecution.attempted_goals_persist

#print axioms ComposedExecution.local_action_epoch
#print axioms ComposedExecution.landed_refines_effective_policy

#print axioms ComposedExecution.installed_successor_adequate
#print axioms ComposedExecution.installed_successor_changes_actual_behavior

#print axioms ComposedExecution.proposal_uses_actor_observation
