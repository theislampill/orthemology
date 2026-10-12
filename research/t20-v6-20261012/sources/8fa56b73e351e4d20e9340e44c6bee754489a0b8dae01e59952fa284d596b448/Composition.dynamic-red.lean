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
  deriving DecidableEq, BEq

structure Root where
  policy : Policy
  revoked : List Nat := []
  commitments : List Envelope := []
  cancelled : List Envelope := []

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

structure Actor where
  policy : Policy
  observedPlant : Plant
  identity : String
  nonce : Nat := 0

def initialWorld (p : Plant) (policy : Policy) (bad : List Nat) : World :=
  ⟨4, 1, 3, 3, policy, p, 2, fun _ => ⟨policy, [], [], []⟩, fun i => bad.contains i⟩

def propose (actor : Actor) (now : Nat) (a : Action) (path : List Nat) : Option Envelope :=
  (localStep actor.observedPlant actor.policy now a).map
    (fun p => ⟨a, p, actor.nonce + 1, path⟩)

-- Deliberate RED dynamic layer: preparation and landing never act.
def prepare (w : World) (_e : Envelope) (_requester : String) (_badSign : Bool := true) : World × Bool := (w, false)
def attempt (w : World) (_e : Envelope) (_requester : String) (_badOpen : Bool := true) : World × Bool := (w, false)

end ComposedExecution

#print axioms ComposedExecution.local_install_refinement
#print axioms ComposedExecution.local_repair_refinement
#print axioms ComposedExecution.local_source_and_custody_frame
#print axioms ComposedExecution.local_install_full_effect
#print axioms ComposedExecution.local_repair_full_effect
#print axioms ComposedExecution.fixed_action_cannot_succeed_twice
#print axioms ComposedExecution.local_goals_persist
