import Std

namespace TypedCriterionGuard

abbrev Target := String × String × String

structure Source where
  target : Target
  content : List Nat
  roots : List String
  deriving DecidableEq, BEq

structure Grant where
  actor : String
  destination : String
  target : Target
  authorizationEpoch : Nat
  notBefore : Nat
  expires : Nat
  operation : String
  deriving DecidableEq, BEq

structure State where
  source : Source
  destination : String
  draft : List Nat
  revision : Nat
  authorizationEpoch : Nat
  grant : Option Grant
  revoked : Bool
  now : Nat
  history : List (List Nat)
  deriving DecidableEq, BEq

structure Command where
  actor : String
  destination : String
  target : Target
  criterion : String
  expectedRevision : Nat
  authorizationEpoch : Nat
  payload : List Nat
  operation : String
  observedAt : Nat
  leaseEnd : Nat
  deriving DecidableEq, BEq

structure Outcome where
  applied : Bool
  state : State
  deriving DecidableEq, BEq

def applyCommand (s : State) (c : Command) : State :=
  { s with draft := c.payload, revision := s.revision + 1,
           history := s.history ++ [s.draft] }

/- Model-level conditions. Their real-world interpretation is an independent
warrant burden, especially the source record and current grant store. -/
def GrantValid (s : State) (c : Command) (g : Grant) : Prop :=
  g.actor = c.actor ∧
  g.destination = c.destination ∧
  g.target = c.target ∧
  g.authorizationEpoch = s.authorizationEpoch ∧
  g.operation = c.operation ∧
  g.notBefore ≤ s.now ∧ s.now < g.expires ∧
  c.observedAt ≤ s.now ∧ s.now < c.leaseEnd ∧ c.leaseEnd ≤ g.expires

def ContextValid (s : State) (c : Command) : Prop :=
  c.target = s.source.target ∧
  c.destination = s.destination ∧
  c.criterion = "C1-exact" ∧
  c.expectedRevision = s.revision ∧
  c.authorizationEpoch = s.authorizationEpoch ∧
  c.operation = "replace-derived" ∧
  c.payload = s.source.content ∧
  s.revoked = false ∧
  match s.grant with
  | none => False
  | some g => GrantValid s c g

instance (s : State) (c : Command) (g : Grant) : Decidable (GrantValid s c g) := by
  unfold GrantValid
  infer_instance

instance (s : State) (c : Command) : Decidable (ContextValid s c) := by
  unfold ContextValid
  cases s.grant <;> infer_instance

def guard (s : State) (c : Command) : Bool := decide (ContextValid s c)

theorem guard_true_iff_context_valid (s : State) (c : Command) :
    guard s c = true ↔ ContextValid s c := by
  exact ⟨of_decide_eq_true, decide_eq_true⟩

def execute (s : State) (c : Command) : Outcome :=
  if guard s c then ⟨true, applyCommand s c⟩ else ⟨false, s⟩

theorem applied_iff_context_valid (s : State) (c : Command) :
    (execute s c).applied = true ↔ ContextValid s c := by
  constructor
  · intro h
    unfold execute at h
    split at h
    · rename_i hg
      exact (guard_true_iff_context_valid s c).mp hg
    · cases h
  · intro h
    have hg := (guard_true_iff_context_valid s c).mpr h
    unfold execute
    rw [hg]
    rfl

theorem source_preserved (s : State) (c : Command) :
    (execute s c).state.source = s.source := by
  unfold execute
  split <;> rfl

theorem rejected_unchanged (s : State) (c : Command)
    (rejected : (execute s c).applied = false) : (execute s c).state = s := by
  unfold execute at rejected ⊢
  by_cases h : guard s c = true
  · rw [if_pos h] at rejected
    cases rejected
  · rw [if_neg h]

theorem accepted_payload_is_exact (s : State) (c : Command)
    (accepted : (execute s c).applied = true) : c.payload = s.source.content := by
  have valid := (applied_iff_context_valid s c).mp accepted
  obtain ⟨ht, hd, hc, hv, he, ho, hp, hr, hg⟩ := valid
  exact hp

theorem accepted_current_grant (s : State) (c : Command)
    (accepted : (execute s c).applied = true) :
    s.revoked = false ∧ ∃ g, s.grant = some g ∧ GrantValid s c g := by
  have valid := (applied_iff_context_valid s c).mp accepted
  obtain ⟨ht, hd, hc, hv, he, ho, hp, hr, hg⟩ := valid
  refine ⟨hr, ?_⟩
  cases hs : s.grant with
  | none =>
      rw [hs] at hg
      exact False.elim hg
  | some g =>
      rw [hs] at hg
      exact ⟨g, rfl, hg⟩

theorem accepted_repairs_and_retains_history (s : State) (c : Command)
    (accepted : (execute s c).applied = true) :
    (execute s c).state.draft = s.source.content ∧
    (execute s c).state.revision = s.revision + 1 ∧
    (execute s c).state.history = s.history ++ [s.draft] := by
  have payload := accepted_payload_is_exact s c accepted
  have hg := (guard_true_iff_context_valid s c).mpr
    ((applied_iff_context_valid s c).mp accepted)
  unfold execute
  rw [hg]
  exact ⟨payload, rfl, rfl⟩

theorem existing_repair_preserved (s : State) (c : Command)
    (repaired : s.draft = s.source.content) :
    (execute s c).state.draft = (execute s c).state.source.content := by
  cases h : (execute s c).applied with
  | false =>
      rw [rejected_unchanged s c h]
      exact repaired
  | true =>
      rw [source_preserved]
      exact (accepted_repairs_and_retains_history s c h).1

def run (s : State) : List Command → State
  | [] => s
  | c :: cs => run (execute s c).state cs

theorem mediated_persistence (commands : List Command) (s : State)
    (repaired : s.draft = s.source.content) :
    (run s commands).draft = (run s commands).source.content := by
  induction commands generalizing s with
  | nil => exact repaired
  | cons c cs ih =>
      exact ih (execute s c).state (existing_repair_preserved s c repaired)

end TypedCriterionGuard

#print axioms TypedCriterionGuard.applied_iff_context_valid
#print axioms TypedCriterionGuard.accepted_current_grant
#print axioms TypedCriterionGuard.accepted_repairs_and_retains_history
#print axioms TypedCriterionGuard.mediated_persistence
