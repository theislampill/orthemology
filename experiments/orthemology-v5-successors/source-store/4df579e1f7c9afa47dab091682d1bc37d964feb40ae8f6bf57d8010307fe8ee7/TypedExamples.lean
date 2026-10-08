import TypedHistoryProperties
import JoinOperations

namespace OperationalJoin.Typed.Examples
noncomputable section
open Classical
open ComposedExecution

/-- A compact fixture, not a new source-authenticity claim. Its three byte values
stand in for an arbitrary recovered finite source sequence. -/
def target : TypedCriterionGuard.Target := ("fixture-repository", "pinned-commit", "source.md")
def before : ComposedExecution.Plant :=
  { source := ⟨target, [65,66,67], ["fixture-source"]⟩
    destination := "fixture-A"
    standard := "exact-source-recovery"
    draft := [65,66,67,10]
    draftRevision := 8
    draftHistory := [[88]]
    rule := .normalizedLF
    ruleVersion := 3
    ruleHistory := []
    unrelated := ["retain-custody"] }

def policy (scope : String) (epoch : Nat) : ComposedExecution.Policy :=
  { target, destination := "fixture-A", actor := "A", scope, epoch
    grant := some ⟨"A", "fixture-A", target, epoch, 0, 100, scope⟩ }

def source (epoch : Nat) : ComposedExecution.Policy :=
  policy (if epoch = 0 then "install-criterion" else "replace-derived") epoch

def installCommand : CriterionInstallation.InstallCommand :=
  { actor := "A", destination := "fixture-A", target
    expectedRule := .normalizedLF, expectedVersion := 3, authorizationEpoch := 0
    newRule := .exact, operation := "install-criterion", observedAt := 1, leaseEnd := 90 }

def repairCommand : TypedCriterionGuard.Command :=
  { actor := "A", destination := "fixture-A", target, criterion := "C1-exact"
    expectedRevision := 8, authorizationEpoch := 1, payload := [65,66,67]
    operation := "replace-derived", observedAt := 1, leaseEnd := 90 }

def installed : ComposedExecution.Plant :=
  { before with rule := .exact, ruleVersion := 4, ruleHistory := [.normalizedLF] }
def repaired : ComposedExecution.Plant :=
  { installed with draft := [65,66,67], draftRevision := 9
                   draftHistory := [[88], [65,66,67,10]] }

def installEnvelope : BoundedEnvelope 4 :=
  ⟨⟨.install installCommand, installed, 11, [1,2,3]⟩, by decide⟩
def repairEnvelope : BoundedEnvelope 4 :=
  ⟨⟨.repair repairCommand, repaired, 12, [1,2,3]⟩, by decide⟩

def cfg : Config (interface 4) where
  budget := 1
  q := 3
  r := 3
  faulty := {0}
  budget_bound := by decide
  overlap := by decide
  budget_lt_roots := by decide
  repair_available := by decide
  revoke_available := by decide
  source := source
  source_epoch := by intro epoch; rfl

theorem install_local : localStep before (source 0) 2 (.install installCommand) = some installed := by decide
theorem repair_local : localStep installed (source 1) 3 (.repair repairCommand) = some repaired := by decide

def initial : State (interface 4) := Initial cfg before
def preparedInstall : State (interface 4) :=
  prepare (prepare (prepare initial 1 installEnvelope) 2 installEnvelope) 3 installEnvelope

theorem installation_preparation_trace : Trace cfg initial
    [.prepare 1 installEnvelope "A" 2, .prepare 2 installEnvelope "A" 2,
      .prepare 3 installEnvelope "A" 2] preparedInstall := by
  apply Trace.cons (Step.prepare (c := cfg) _ 1 installEnvelope "A" 2 ?_ ?_ ?_)
  · apply Trace.cons (Step.prepare (c := cfg) _ 2 installEnvelope "A" 2 ?_ ?_ ?_)
    · apply Trace.cons (Step.prepare (c := cfg) _ 3 installEnvelope "A" 2 ?_ ?_ ?_)
      · exact Trace.nil _
      · exact (mem_path installEnvelope (3 : Fin 4)).mpr (by decide)
      · simp only [ValidPath, interface]; rw [path_card]; decide
      · right
        simp [Envelope, interface, prepare, setRoot, initial, Initial, cfg,
          installEnvelope, Function.update_apply, install_local]; rfl
    · exact (mem_path installEnvelope (2 : Fin 4)).mpr (by decide)
    · simp only [ValidPath, interface]; rw [path_card]; decide
    · right
      simp [Envelope, interface, prepare, setRoot, initial, Initial, cfg,
        installEnvelope, Function.update_apply, install_local]; rfl
  · exact (mem_path installEnvelope (1 : Fin 4)).mpr (by decide)
  · simp only [ValidPath, interface]; rw [path_card]; decide
  · right
    simp [Envelope, interface, initial, Initial, cfg, installEnvelope, install_local]; rfl

theorem installation_lands : Lands cfg preparedInstall 2 installEnvelope "A" := by
  constructor
  · simp only [ValidPath, interface]; rw [path_card]; decide
  · intro i selected _good
    have cases : i = 1 ∨ i = 2 ∨ i = 3 := by
      simpa [interface, path, installEnvelope, Fin.ext_iff] using selected
    rcases cases with rfl | rfl | rfl <;>
      simp [Permits, Envelope, interface, preparedInstall, prepare, setRoot,
        initial, Initial, cfg, installEnvelope, Function.update_apply, install_local] <;> rfl

def afterInstall : State (interface 4) := land cfg preparedInstall 2 installEnvelope "A"

theorem installation_state : afterInstall = { preparedInstall with plant := installed } := by
  have auth : (interface 4).admits preparedInstall.plant 2 (cfg.source preparedInstall.epoch)
      installEnvelope "A" := by
    exact ⟨rfl, install_local⟩
  have safe : preparedInstall.damaged = false := rfl
  unfold afterInstall land
  rw [if_neg (by simp only [safe, Bool.false_eq_true, false_or, not_not]; exact auth)]
  rfl

def acknowledged : State (interface 4) :=
  acknowledge cfg (acknowledge cfg (acknowledge cfg (request afterInstall) 1) 2) 3
def completed : State (interface 4) := complete acknowledged

theorem transition_trace : Trace cfg afterInstall
    [.request, .acknowledge 1, .acknowledge 2, .acknowledge 3, .complete] completed := by
  apply Trace.cons (Step.request (c := cfg) _ (by simp [afterInstall, preparedInstall, initial, prepare, setRoot, Initial]))
  apply Trace.cons (Step.acknowledge _ 1 rfl)
  apply Trace.cons (Step.acknowledge _ 2 rfl)
  apply Trace.cons (Step.acknowledge _ 3 rfl)
  apply Trace.cons (Step.complete _ rfl ?_)
  · exact Trace.nil _
  · change ({3,2,1} : Finset (Fin 4)).card = 3
    decide

def delivered : State (interface 4) :=
  deliver cfg (deliver cfg (deliver cfg completed 1 1) 2 1) 3 1

theorem delivery_trace : Trace cfg completed [.deliver 1 1, .deliver 2 1, .deliver 3 1] delivered := by
  apply Trace.cons (Step.deliver (c := cfg) _ 1 1 (by simp [completed, complete, acknowledged, acknowledge, request, afterInstall, preparedInstall, initial, Initial]))
  apply Trace.cons (Step.deliver _ 2 1 ?_)
  · apply Trace.cons (Step.deliver _ 3 1 ?_)
    · exact Trace.nil _
    · simp [completed, complete, acknowledged, acknowledge, request, afterInstall, preparedInstall, initial, Initial]
  · simp [completed, complete, acknowledged, acknowledge, request, afterInstall, preparedInstall, initial, Initial]

/-- The distinct current repair grant reaches all selected good roots through
completed-certificate deliveries; no actor/global-current oracle is supplied. -/
theorem delivered_fields :
    delivered.plant = installed ∧ delivered.epoch = 1 ∧ delivered.damaged = false ∧
      (∀ i : Fin 4, i = 1 ∨ i = 2 ∨ i = 3 →
        (delivered.roots i).descriptor = source 1 ∧
        (delivered.roots i).revoked = {0} ∧ (delivered.roots i).cancelled = ∅) := by
  unfold delivered completed acknowledged
  simp only [installation_state]
  simp [deliver, setRoot, complete, acknowledge, request, preparedInstall, prepare,
    initial, Initial, cfg, Good, interface, source, policy, Function.update_apply]


def preparedRepair : State (interface 4) :=
  prepare (prepare (prepare delivered 1 repairEnvelope) 2 repairEnvelope) 3 repairEnvelope


theorem repair_ready (i : Fin 4) (selected : i = 1 ∨ i = 2 ∨ i = 3) :
    Envelope delivered.plant 3 (delivered.roots i) repairEnvelope "A" := by
  obtain ⟨plant, _, _, fields⟩ := delivered_fields
  obtain ⟨descriptor, revoked, cancelled⟩ := fields i selected
  simp only [Envelope, interface, plant, descriptor, revoked, cancelled]
  exact ⟨⟨rfl, repair_local⟩, by simp [repairEnvelope, Action.epoch, repairCommand], by simp⟩

theorem repair_preparation_trace : Trace cfg delivered
    [.prepare 1 repairEnvelope "A" 3, .prepare 2 repairEnvelope "A" 3,
      .prepare 3 repairEnvelope "A" 3] preparedRepair := by
  apply Trace.cons (Step.prepare (c := cfg) _ 1 repairEnvelope "A" 3 ?_ ?_ ?_)
  · apply Trace.cons (Step.prepare (c := cfg) _ 2 repairEnvelope "A" 3 ?_ ?_ ?_)
    · apply Trace.cons (Step.prepare (c := cfg) _ 3 repairEnvelope "A" 3 ?_ ?_ ?_)
      · exact Trace.nil _
      · exact (mem_path repairEnvelope (3 : Fin 4)).mpr (by decide)
      · simp only [ValidPath, interface]; rw [path_card]; decide
      · right
        simpa only [prepare_envelope] using repair_ready 3 (Or.inr (Or.inr rfl))
    · exact (mem_path repairEnvelope (2 : Fin 4)).mpr (by decide)
    · simp only [ValidPath, interface]; rw [path_card]; decide
    · right
      simpa only [prepare_envelope] using repair_ready 2 (Or.inr (Or.inl rfl))
  · exact (mem_path repairEnvelope (1 : Fin 4)).mpr (by decide)
  · simp only [ValidPath, interface]; rw [path_card]; decide
  · exact Or.inr (repair_ready 1 (Or.inl rfl))

theorem repair_lands : Lands cfg preparedRepair 3 repairEnvelope "A" := by
  constructor
  · simp only [ValidPath, interface]; rw [path_card]; decide
  · intro i selected _good
    have cases : i = 1 ∨ i = 2 ∨ i = 3 := by
      simpa [interface, path, repairEnvelope, Fin.ext_iff] using selected
    constructor
    · rcases cases with rfl | rfl | rfl <;>
        simp [preparedRepair, prepare, setRoot, Function.update_apply]
    · simpa only [preparedRepair, prepare_envelope] using repair_ready i cases

def afterRepair : State (interface 4) := land cfg preparedRepair 3 repairEnvelope "A"

def twoStageEvents : List (Event (interface 4)) :=
  [.prepare 1 installEnvelope "A" 2, .prepare 2 installEnvelope "A" 2,
   .prepare 3 installEnvelope "A" 2, .land installEnvelope "A" 2,
   .request, .acknowledge 1, .acknowledge 2, .acknowledge 3, .complete,
   .deliver 1 1, .deliver 2 1, .deliver 3 1,
   .prepare 1 repairEnvelope "A" 3, .prepare 2 repairEnvelope "A" 3,
   .prepare 3 repairEnvelope "A" 3, .land repairEnvelope "A" 3]

theorem two_stage_history : Trace cfg initial twoStageEvents afterRepair := by
  have install := Trace.cons (Step.land (c := cfg) preparedInstall installEnvelope "A" 2 installation_lands)
    (Trace.nil afterInstall)
  have repair := Trace.cons (Step.land (c := cfg) preparedRepair repairEnvelope "A" 3 repair_lands)
    (Trace.nil afterRepair)
  exact trace_append installation_preparation_trace (trace_append install
    (trace_append transition_trace (trace_append delivery_trace
      (trace_append repair_preparation_trace repair))))

theorem repair_state : afterRepair.plant = repaired := by
  have beforeHistory : Trace cfg initial
      [.prepare 1 installEnvelope "A" 2, .prepare 2 installEnvelope "A" 2,
       .prepare 3 installEnvelope "A" 2, .land installEnvelope "A" 2,
       .request, .acknowledge 1, .acknowledge 2, .acknowledge 3, .complete,
       .deliver 1 1, .deliver 2 1, .deliver 3 1,
       .prepare 1 repairEnvelope "A" 3, .prepare 2 repairEnvelope "A" 3,
       .prepare 3 repairEnvelope "A" 3] preparedRepair := by
    exact trace_append installation_preparation_trace
      (Trace.cons (Step.land (c := cfg) _ _ _ _ installation_lands)
        (trace_append transition_trace (trace_append delivery_trace repair_preparation_trace)))
  have ⟨consistent, safe, _⟩ := finite_history_safety cfg before beforeHistory
  exact (step_plant consistent safe (Step.land (c := cfg) _ _ _ _ repair_lands)).2

/-- A non-vacuous finite history changes the actual installed criterion, then
repairs the draft under a distinct later grant, preserving all custody fields. -/
theorem exact_two_stage_result :
    afterRepair.plant = repaired ∧ afterRepair.damaged = false ∧
    Goals afterRepair.plant ∧ Custody before afterRepair.plant ∧
    afterRepair.plant.ruleVersion = 4 ∧ afterRepair.plant.draftRevision = 9 ∧
    afterRepair.plant.ruleHistory = [.normalizedLF] ∧
    afterRepair.plant.draftHistory = [[88], [65,66,67,10]] ∧
    installCount twoStageEvents = 1 ∧ repairCount twoStageEvents = 1 := by
  refine ⟨repair_state, (finite_history_safety cfg before two_stage_history).2.1, ?_⟩
  rw [repair_state]
  exact ⟨⟨rfl, rfl⟩, ⟨rfl, rfl, rfl, rfl⟩, rfl, rfl, rfl, rfl, rfl, rfl⟩

def closedRepair : State (interface 4) :=
  cancelAck cfg (cancelAck cfg afterRepair 1 repairEnvelope) 2 repairEnvelope

theorem repair_cancellation_trace : Trace cfg afterRepair
    [.cancelAck 1 repairEnvelope "A", .cancelAck 2 repairEnvelope "A", .close repairEnvelope] closedRepair := by
  apply Trace.cons (Step.cancelAck (c := cfg) _ 1 repairEnvelope "A" ?_ (Or.inr rfl))
  · apply Trace.cons (Step.cancelAck (c := cfg) _ 2 repairEnvelope "A" ?_ (Or.inr rfl))
    · apply Trace.cons (Step.close (c := cfg) _ repairEnvelope ?_)
      · exact Trace.nil _
      · simp only [cancelAck, Function.update_self]
        change 1 < (insert 2 (insert 1 (afterRepair.cancelAcks repairEnvelope))).card
        have sub : ({1,2} : Finset (Fin 4)) ⊆
            insert 2 (insert 1 (afterRepair.cancelAcks repairEnvelope)) := by
          intro i hi
          simp only [Finset.mem_insert, Finset.mem_singleton] at hi ⊢
          tauto
        have bound := Finset.card_le_card sub
        have size : ({1,2} : Finset (Fin 4)).card = 2 := by decide
        omega
    · exact (mem_path repairEnvelope (2 : Fin 4)).mpr (by decide)
  · exact (mem_path repairEnvelope (1 : Fin 4)).mpr (by decide)

theorem closedRepair_certificate : Cancelled cfg closedRepair repairEnvelope := by
  simp only [Cancelled, closedRepair, cancelAck, Function.update_self]
  change 1 < (insert 2 (insert 1 (afterRepair.cancelAcks repairEnvelope))).card
  have sub : ({1,2} : Finset (Fin 4)) ⊆
      insert 2 (insert 1 (afterRepair.cancelAcks repairEnvelope)) := by
    intro i hi
    simp only [Finset.mem_insert, Finset.mem_singleton] at hi ⊢
    tauto
  have bound := Finset.card_le_card sub
  have size : ({1,2} : Finset (Fin 4)).card = 2 := by decide
  omega

theorem closed_repair_blocks_all_continuations {t : State (interface 4)}
    {events : List (Event (interface 4))} (continuation : Trace cfg closedRepair events t)
    (time : Nat) (requester : String) : ¬Lands cfg t time repairEnvelope requester := by
  have start : Reachable cfg afterRepair := ⟨before, twoStageEvents, two_stage_history⟩
  have closed := reachable_after start repair_cancellation_trace
  exact no_landing_after_cancellation closed continuation time repairEnvelope requester closedRepair_certificate

#print axioms install_local
#print axioms repair_local
#print axioms two_stage_history
#print axioms exact_two_stage_result
#print axioms closed_repair_blocks_all_continuations
end
end OperationalJoin.Typed.Examples
