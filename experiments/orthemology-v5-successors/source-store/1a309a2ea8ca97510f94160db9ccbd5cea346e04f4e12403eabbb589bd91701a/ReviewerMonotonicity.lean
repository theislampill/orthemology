import Composition
open ComposedExecution

theorem local_versions_monotone (p : Plant) (policy : Policy) (now : Nat)
    (a : Action) (next : Plant) (h : localStep p policy now a = some next) :
    p.ruleVersion ≤ next.ruleVersion ∧ p.draftRevision ≤ next.draftRevision := by
  cases a with
  | install c =>
      rw [local_install_full_effect p policy now c next h]
      simp
  | repair c =>
      rw [local_repair_full_effect p policy now c next h]
      simp

theorem install_no_replay_after_monotone_progress (p : Plant) (policy : Policy) (now : Nat)
    (c : CriterionInstallation.InstallCommand) (next : Plant)
    (step : localStep p policy now (.install c) = some next)
    (later : Plant) (laterPolicy : Policy) (laterNow : Nat)
    (monotone : next.ruleVersion ≤ later.ruleVersion) :
    localStep later laterPolicy laterNow (.install c) = none := by
  cases h : localStep later laterPolicy laterNow (.install c) with
  | none => rfl
  | some after =>
      have old := local_install_expected_version p policy now c next step
      have new := local_install_expected_version later laterPolicy laterNow c after h
      have effect := local_install_full_effect p policy now c next step
      rw [effect] at monotone
      simp only at monotone
      omega

theorem repair_no_replay_after_monotone_progress (p : Plant) (policy : Policy) (now : Nat)
    (c : TypedCriterionGuard.Command) (next : Plant)
    (step : localStep p policy now (.repair c) = some next)
    (later : Plant) (laterPolicy : Policy) (laterNow : Nat)
    (monotone : next.draftRevision ≤ later.draftRevision) :
    localStep later laterPolicy laterNow (.repair c) = none := by
  cases h : localStep later laterPolicy laterNow (.repair c) with
  | none => rfl
  | some after =>
      have old := local_repair_expected_revision p policy now c next step
      have new := local_repair_expected_revision later laterPolicy laterNow c after h
      have effect := local_repair_full_effect p policy now c next step
      rw [effect] at monotone
      simp only at monotone
      omega

#print axioms local_versions_monotone
#print axioms install_no_replay_after_monotone_progress
#print axioms repair_no_replay_after_monotone_progress
