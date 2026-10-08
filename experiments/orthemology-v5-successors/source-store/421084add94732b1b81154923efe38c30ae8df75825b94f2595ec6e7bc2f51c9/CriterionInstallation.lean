import TypedCriterionGuard

namespace CriterionInstallation

open TypedCriterionGuard (Target Source Grant)

/- A small typed rule language. The constructors denote these definitions;
they are not labels for arbitrary sender-supplied executable code. -/
inductive Rule where
  | normalizedLF
  | exact
  deriving DecidableEq, BEq

def stripTrailingLF (xs : List Nat) : List Nat :=
  (xs.reverse.dropWhile (fun n => n == 10)).reverse

def Accepts (rule : Rule) (candidate source : List Nat) : Prop :=
  match rule with
  | .normalizedLF => stripTrailingLF candidate = stripTrailingLF source
  | .exact => candidate = source

instance (rule : Rule) (candidate source : List Nat) :
    Decidable (Accepts rule candidate source) := by
  cases rule <;> unfold Accepts <;> infer_instance

def accepts (rule : Rule) (candidate source : List Nat) : Bool :=
  decide (Accepts rule candidate source)

theorem exact_rule_adequate (source candidate : List Nat) :
    Accepts .exact candidate source ↔ candidate = source := by
  rfl

theorem normalization_erases_appended_LF (source : List Nat) :
    stripTrailingLF (source ++ [10]) = stripTrailingLF source := by
  simp [stripTrailingLF, List.reverse_append, List.dropWhile]

theorem appended_LF_changes_finite_sequence (source : List Nat) :
    source ++ [10] ≠ source := by
  intro h
  have lengths := congrArg List.length h
  simp at lengths

theorem normalized_rule_false_acceptance (source : List Nat) :
    Accepts .normalizedLF (source ++ [10]) source ∧ source ++ [10] ≠ source := by
  exact ⟨normalization_erases_appended_LF source, appended_LF_changes_finite_sequence source⟩

structure RuleState where
  source : Source
  destination : String
  standard : String
  draft : List Nat
  draftRevision : Nat
  rule : Rule
  ruleVersion : Nat
  authorizationEpoch : Nat
  grant : Option Grant
  revoked : Bool
  now : Nat
  ruleHistory : List Rule
  unrelated : List String
  deriving DecidableEq, BEq

structure InstallCommand where
  actor : String
  destination : String
  target : Target
  expectedRule : Rule
  expectedVersion : Nat
  authorizationEpoch : Nat
  newRule : Rule
  operation : String
  observedAt : Nat
  leaseEnd : Nat
  deriving DecidableEq, BEq

structure InstallOutcome where
  applied : Bool
  state : RuleState
  deriving DecidableEq, BEq

def InstallGrantValid (s : RuleState) (c : InstallCommand) (g : Grant) : Prop :=
  g.actor = c.actor ∧ g.destination = c.destination ∧ g.target = c.target ∧
  g.authorizationEpoch = s.authorizationEpoch ∧ g.operation = "install-criterion" ∧
  g.notBefore ≤ s.now ∧ s.now < g.expires ∧
  c.observedAt ≤ s.now ∧ s.now < c.leaseEnd ∧ c.leaseEnd ≤ g.expires

def InstallValid (s : RuleState) (c : InstallCommand) : Prop :=
  s.standard = "exact-source-recovery" ∧
  c.target = s.source.target ∧ c.destination = s.destination ∧
  c.expectedRule = s.rule ∧ c.expectedVersion = s.ruleVersion ∧
  c.authorizationEpoch = s.authorizationEpoch ∧ c.newRule = .exact ∧
  c.operation = "install-criterion" ∧ s.revoked = false ∧
  match s.grant with
  | none => False
  | some g => InstallGrantValid s c g

instance (s : RuleState) (c : InstallCommand) (g : Grant) :
    Decidable (InstallGrantValid s c g) := by
  unfold InstallGrantValid
  infer_instance

instance (s : RuleState) (c : InstallCommand) : Decidable (InstallValid s c) := by
  unfold InstallValid
  cases s.grant <;> infer_instance

def installGuard (s : RuleState) (c : InstallCommand) : Bool := decide (InstallValid s c)

def applyInstallation (s : RuleState) (c : InstallCommand) : RuleState :=
  { s with rule := c.newRule, ruleVersion := s.ruleVersion + 1,
           ruleHistory := s.ruleHistory ++ [s.rule] }

def install (s : RuleState) (c : InstallCommand) : InstallOutcome :=
  if installGuard s c then ⟨true, applyInstallation s c⟩ else ⟨false, s⟩

theorem guard_true_iff_valid (s : RuleState) (c : InstallCommand) :
    installGuard s c = true ↔ InstallValid s c := by
  exact ⟨of_decide_eq_true, decide_eq_true⟩

theorem applied_iff_valid (s : RuleState) (c : InstallCommand) :
    (install s c).applied = true ↔ InstallValid s c := by
  constructor
  · intro h
    unfold install at h
    split at h
    · rename_i hg
      exact (guard_true_iff_valid s c).mp hg
    · cases h
  · intro h
    unfold install
    rw [(guard_true_iff_valid s c).mpr h]
    rfl

theorem installation_frame (s : RuleState) (c : InstallCommand) :
    (install s c).state.source = s.source ∧
    (install s c).state.draft = s.draft ∧
    (install s c).state.draftRevision = s.draftRevision ∧
    (install s c).state.standard = s.standard ∧
    (install s c).state.destination = s.destination ∧
    (install s c).state.authorizationEpoch = s.authorizationEpoch ∧
    (install s c).state.grant = s.grant ∧
    (install s c).state.revoked = s.revoked ∧
    (install s c).state.now = s.now ∧
    (install s c).state.unrelated = s.unrelated := by
  unfold install
  split <;> exact ⟨rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl⟩

theorem accepted_changes_rule_and_history (s : RuleState) (c : InstallCommand)
    (accepted : (install s c).applied = true) :
    (install s c).state.rule = .exact ∧
    (install s c).state.ruleVersion = s.ruleVersion + 1 ∧
    (install s c).state.ruleHistory = s.ruleHistory ++ [s.rule] := by
  have valid := (applied_iff_valid s c).mp accepted
  obtain ⟨hm, ht, hd, hr, hv, he, hn, ho, hrev, hg⟩ := valid
  have guarded := (guard_true_iff_valid s c).mpr ((applied_iff_valid s c).mp accepted)
  unfold install
  rw [guarded]
  exact ⟨hn, rfl, rfl⟩

theorem accepted_rule_adequate (s : RuleState) (c : InstallCommand)
    (accepted : (install s c).applied = true) :
    ∀ candidate, Accepts (install s c).state.rule candidate s.source.content ↔
      candidate = s.source.content := by
  intro candidate
  rw [(accepted_changes_rule_and_history s c accepted).1]
  rfl

theorem actual_decision_behavior_changes (s : RuleState) (c : InstallCommand)
    (oldRule : s.rule = .normalizedLF)
    (accepted : (install s c).applied = true) :
    Accepts s.rule (s.source.content ++ [10]) s.source.content ∧
    ¬ Accepts (install s c).state.rule (s.source.content ++ [10]) s.source.content ∧
    Accepts (install s c).state.rule s.source.content s.source.content := by
  constructor
  · rw [oldRule]
    exact (normalized_rule_false_acceptance s.source.content).1
  · rw [(accepted_changes_rule_and_history s c accepted).1]
    exact ⟨appended_LF_changes_finite_sequence s.source.content, rfl⟩

theorem rejected_unchanged (s : RuleState) (c : InstallCommand)
    (rejected : (install s c).applied = false) : (install s c).state = s := by
  unfold install at rejected ⊢
  by_cases h : installGuard s c = true
  · rw [if_pos h] at rejected
    cases rejected
  · rw [if_neg h]

theorem accepted_has_install_specific_grant (s : RuleState) (c : InstallCommand)
    (accepted : (install s c).applied = true) :
    s.revoked = false ∧ ∃ g, s.grant = some g ∧ InstallGrantValid s c g := by
  have valid := (applied_iff_valid s c).mp accepted
  obtain ⟨hm, ht, hd, hr, hv, he, hn, ho, hrev, hg⟩ := valid
  refine ⟨hrev, ?_⟩
  cases hs : s.grant with
  | none =>
      rw [hs] at hg
      exact False.elim hg
  | some g =>
      rw [hs] at hg
      exact ⟨g, rfl, hg⟩

theorem data_repair_permission_is_not_install_permission
    (s : RuleState) (c : InstallCommand) (g : Grant)
    (active : s.grant = some g) (dataOnly : g.operation = "replace-derived") :
    ¬ (install s c).applied = true := by
  intro accepted
  obtain ⟨hrev, other, hother, valid⟩ := accepted_has_install_specific_grant s c accepted
  have same : g = other := Option.some.inj (active.symm.trans hother)
  subst other
  obtain ⟨ha, hd, ht, he, ho, rest⟩ := valid
  rw [dataOnly] at ho
  exact (by decide : ("replace-derived" : String) ≠ "install-criterion") ho

end CriterionInstallation

#print axioms CriterionInstallation.normalized_rule_false_acceptance
#print axioms CriterionInstallation.normalization_erases_appended_LF
#print axioms CriterionInstallation.appended_LF_changes_finite_sequence
#print axioms CriterionInstallation.applied_iff_valid
#print axioms CriterionInstallation.installation_frame
#print axioms CriterionInstallation.accepted_rule_adequate
#print axioms CriterionInstallation.actual_decision_behavior_changes
#print axioms CriterionInstallation.data_repair_permission_is_not_install_permission
