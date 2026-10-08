import TypedFixtureHelpers
import HistoryModel

namespace OperationalJoin.Typed.Controls
noncomputable section
open Classical
open ComposedExecution
open Examples

/-- No injective full-plant encoding into the predecessor's four physical
binary-table values exists. This does not rule out a weaker goal abstraction. -/
theorem no_full_plant_table_injection (encode : ComposedExecution.Plant → InterlockHistory.Table) :
    ¬Function.Injective encode := by
  intro injective
  let plantOf : Nat → ComposedExecution.Plant := fun version => { before with ruleVersion := version }
  have plantInjective : Function.Injective plantOf := by
    intro x y eq
    exact congrArg ComposedExecution.Plant.ruleVersion eq
  haveI : Finite Nat := Finite.of_injective (encode ∘ plantOf) (injective.comp plantInjective)
  exact not_finite Nat

def freshInstall : CriterionInstallation.InstallCommand :=
  { installCommand with expectedRule := .exact, expectedVersion := 4 }
def installedAgain : ComposedExecution.Plant :=
  { installed with ruleVersion := 5, ruleHistory := [.normalizedLF, .exact] }

theorem fresh_install_not_idempotent :
    localStep installed (source 0) 2 (.install freshInstall) = some installedAgain ∧
    installedAgain ≠ installed ∧ installedAgain.rule = installed.rule ∧
    installedAgain.draft = installed.draft := by
  exact ⟨by decide, by decide, rfl, rfl⟩

theorem original_action_rejected_after_install :
    localStep installed (source 0) 2 (.install installCommand) = none := by decide

def tamperedEnvelope : BoundedEnvelope 4 :=
  ⟨{ installEnvelope.val with successor := { installed with ruleVersion := 999 } }, installEnvelope.property⟩

theorem same_nonce_does_not_identify_command :
    tamperedEnvelope.val.nonce = installEnvelope.val.nonce ∧
    path tamperedEnvelope = path installEnvelope ∧
    tamperedEnvelope ≠ installEnvelope := by
  refine ⟨rfl, rfl, ?_⟩
  intro eq
  have versions := congrArg (fun e : BoundedEnvelope 4 => e.val.successor.ruleVersion) eq
  change 999 = 4 at versions
  omega

theorem full_successor_tampering_rejected :
    ¬(interface 4).admits before 2 (source 0) tamperedEnvelope "A" := by
  intro h
  have eq := install_local.symm.trans h.2
  have states := Option.some.inj eq
  have versions := congrArg ComposedExecution.Plant.ruleVersion states
  change 4 = 999 at versions
  omega

def reorderedEnvelope : BoundedEnvelope 4 :=
  ⟨{ installEnvelope.val with path := [3,2,1] }, by decide⟩

theorem ordered_path_identity_preserved :
    path reorderedEnvelope = path installEnvelope ∧ reorderedEnvelope ≠ installEnvelope := by
  constructor
  · ext i
    simp [path, reorderedEnvelope, installEnvelope, or_comm, or_left_comm, or_assoc]
  · intro eq
    have listEq := congrArg (fun e : BoundedEnvelope 4 => e.val.path) eq
    change [3,2,1] = [1,2,3] at listEq
    cases listEq

/-- A stale whole-plant observation permits a locally valid proposal, but the
actual live plant would require retaining the intervening rule audit update. -/
def freshlyRepaired : ComposedExecution.Plant :=
  { installedAgain with draft := [65,66,67], draftRevision := 9
                        draftHistory := [[88], [65,66,67,10]] }

theorem cached_observation_would_overwrite_intervening_audit :
    localStep installed (source 1) 3 (.repair repairCommand) = some repaired ∧
    localStep installedAgain (source 1) 3 (.repair repairCommand) = some freshlyRepaired ∧
    freshlyRepaired ≠ repaired ∧
    freshlyRepaired.ruleVersion = 5 ∧ repaired.ruleVersion = 4 := by
  exact ⟨repair_local, by decide, by decide, rfl, rfl⟩

theorem actual_successor_binding_blocks_cached_overwrite :
    ¬(interface 4).admits installedAgain 3 (source 1) repairEnvelope "A" := by
  intro h
  have live := cached_observation_would_overwrite_intervening_audit.2.1
  have equal := Option.some.inj (live.symm.trans h.2)
  exact cached_observation_would_overwrite_intervening_audit.2.2.1 equal

/-- Time authenticity is not inferred from a successful test at another time. -/
theorem actual_expiry_changes_admission :
    localStep before (source 0) 2 (.install installCommand) = some installed ∧
    localStep before (source 0) 100 (.install installCommand) = none := by
  exact ⟨install_local, by decide⟩

theorem grant_scope_is_separate :
    localStep installed (source 0) 3 (.repair repairCommand) = none ∧
    localStep before (source 1) 2 (.install installCommand) = none := by
  constructor <;> decide

/-- Internal admission does not create actual external permission. -/
theorem external_reservation_not_automatic :
    ¬Reservation cfg (fun _ _ _ _ => False) := by
  intro reservation
  have reachable : Reachable cfg preparedInstall :=
    ⟨before, _, installation_preparation_trace⟩
  exact admitted_externally_authorized reservation reachable 2 installEnvelope "A" installation_lands

def lateInstallEnvelope : BoundedEnvelope 4 :=
  ⟨⟨.install freshInstall, installedAgain, 19, [1,2,3]⟩, by decide⟩

def preparedLateInstall : State (interface 4) := prepare123 afterInstall lateInstallEnvelope

theorem late_install_ready (i : Fin 4) (selected : i = 1 ∨ i = 2 ∨ i = 3) :
    Envelope afterInstall.plant 2 (afterInstall.roots i) lateInstallEnvelope "A" := by
  rw [installation_state]
  rcases selected with rfl | rfl | rfl <;>
    simp [Envelope, interface, preparedInstall, prepare, setRoot, initial, Initial,
      cfg, lateInstallEnvelope, Function.update_apply, fresh_install_not_idempotent.1] <;> rfl

theorem late_install_preparation : Trace cfg afterInstall
    [.prepare 1 lateInstallEnvelope "A" 2, .prepare 2 lateInstallEnvelope "A" 2,
      .prepare 3 lateInstallEnvelope "A" 2] preparedLateInstall :=
  prepare123_trace cfg afterInstall lateInstallEnvelope "A" 2 rfl rfl late_install_ready

def revokedLateInstall : State (interface 4) := complete
  (acknowledge cfg (acknowledge cfg (acknowledge cfg (request preparedLateInstall) 1) 2) 3)

theorem late_install_revocation : Trace cfg preparedLateInstall
    [.request, .acknowledge 1, .acknowledge 2, .acknowledge 3, .complete] revokedLateInstall := by
  apply Trace.cons (Step.request (c := cfg) _ ?_)
  · apply Trace.cons (Step.acknowledge _ 1 rfl)
    apply Trace.cons (Step.acknowledge _ 2 rfl)
    apply Trace.cons (Step.acknowledge _ 3 rfl)
    apply Trace.cons (Step.complete _ rfl ?_)
    · exact Trace.nil _
    · change ({3,2,1} : Finset (Fin 4)).card = 3
      decide
  · simp [preparedLateInstall, prepare123, prepare, setRoot, afterInstall,
      preparedInstall, initial, Initial]

def NoRevocation (s : State (interface 4)) (time : Nat)
    (e : BoundedEnvelope 4) (requester : String) : Prop :=
  ValidPath cfg e ∧ ∀ i ∈ path e, Good cfg i →
    e ∈ (s.roots i).commitments ∧
    (interface 4).admits s.plant time (s.roots i).descriptor e requester ∧
    e ∉ (s.roots i).cancelled

theorem dropped_revocation_admits_a_reachable_stale_write :
    Reachable cfg revokedLateInstall ∧
    ¬Lands cfg revokedLateInstall 2 lateInstallEnvelope "A" ∧
    NoRevocation revokedLateInstall 2 lateInstallEnvelope "A" := by
  have afterReach : Reachable cfg afterInstall :=
    ⟨before, _, trace_append installation_preparation_trace
      (Trace.cons (Step.land (c := cfg) _ _ _ _ installation_lands) (Trace.nil _))⟩
  have reach := reachable_after (reachable_after afterReach late_install_preparation) late_install_revocation
  refine ⟨reach, ?_, ?_⟩
  · apply stale_cannot_land (reachable_consistent reach)
    simp [interface, lateInstallEnvelope, Action.epoch, freshInstall, installCommand,
      revokedLateInstall, complete, acknowledge, request, preparedLateInstall, prepare123,
      prepare, setRoot, afterInstall, preparedInstall, initial, Initial]
  · constructor
    · change (path lateInstallEnvelope).card = 3
      rw [path_card]
      rfl
    · intro i selected _good
      have cases : i = 1 ∨ i = 2 ∨ i = 3 := by
        simpa [path, lateInstallEnvelope, Fin.ext_iff] using selected
      rcases cases with rfl | rfl | rfl <;>
        simp [NoRevocation, revokedLateInstall, complete, acknowledge, request,
          preparedLateInstall, prepare123, prepare, setRoot, installation_state,
          preparedInstall, initial, Initial, cfg, Good, interface, lateInstallEnvelope,
          Function.update_apply, fresh_install_not_idempotent.1] <;> rfl

#print axioms no_full_plant_table_injection
#print axioms fresh_install_not_idempotent
#print axioms same_nonce_does_not_identify_command
#print axioms ordered_path_identity_preserved
#print axioms actual_successor_binding_blocks_cached_overwrite
#print axioms actual_expiry_changes_admission
end
end OperationalJoin.Typed.Controls
