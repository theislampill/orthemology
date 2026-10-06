import BatchExactProgress
import BatchMemory

namespace OperationalJoin.Offset.Batch
noncomputable section
open Classical
open ComposedExecution

/-- The stable live-admission obligations, without any cancellation-freshness
assumption. They make no claim that an actor can observe the root policies. -/
def AdmissionReady (w : ComposedExecution.World) (action : Action) (successor : Plant)
    (requester : String) : Prop :=
  requester = action.actor ∧
  localStep w.plant w.effectivePolicy w.now action = some successor ∧
  (∀ i, i < w.n → w.tainted i = false →
    (w.roots i).policy = w.effectivePolicy ∧ action.epoch ∉ (w.roots i).revoked)

/-- Proof-side facts only about the selected roots of this complete envelope.
An unselected root's memory is deliberately irrelevant to this predicate. -/
def IntactUncancelled (w : ComposedExecution.World) (e : ComposedExecution.Envelope) : Prop :=
  ∀ i ∈ e.path, w.tainted i = false ∧ e ∉ (w.roots i).cancelled

def HasSurvivingTrial (w : ComposedExecution.World) (action : Action) (successor : Plant)
    (nonce : Nat) (paths : List (List Nat)) : Prop :=
  ∃ e ∈ trialEnvelopes action successor nonce paths, IntactUncancelled w e

theorem prepare_cancelled (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (i : Nat) :
    ((ComposedExecution.prepare w e requester true).1.roots i).cancelled = (w.roots i).cancelled := by
  unfold ComposedExecution.prepare
  split
  · dsimp
    split <;> split <;> rfl
  · rfl

theorem cancel_memory_mono (w : ComposedExecution.World) (e other : ComposedExecution.Envelope)
    (requester : String) (i : Nat) (old : other ∈ (w.roots i).cancelled) :
    other ∈ ((cancelWith w e requester e.path).1.roots i).cancelled := by
  unfold cancelWith
  split
  · dsimp
    split
    · exact List.mem_cons.mpr (Or.inr old)
    · exact old
  · exact old

theorem cancel_other_memory_iff (w : ComposedExecution.World) (e other : ComposedExecution.Envelope)
    (requester : String) (i : Nat) (different : other ≠ e) :
    other ∈ ((cancelWith w e requester e.path).1.roots i).cancelled ↔ other ∈ (w.roots i).cancelled := by
  unfold cancelWith
  split
  · dsimp
    split
    · change other ∈ e :: (w.roots i).cancelled ↔ _
      simp only [List.mem_cons, different, false_or]
    · rfl
  · rfl

theorem serviceTrial_memory_mono (w : ComposedExecution.World) (e other : ComposedExecution.Envelope)
    (requester : String) (i : Nat) (old : other ∈ (w.roots i).cancelled) :
    other ∈ ((serviceTrial w e requester).1.roots i).cancelled := by
  cases prepared : (ComposedExecution.prepare w e requester true).2 with
  | false =>
      simp only [serviceTrial, prepared, Bool.false_eq_true, if_false]
      exact cancel_memory_mono _ e other requester i (by simpa only [prepare_cancelled] using old)
  | true =>
      simp only [serviceTrial, prepared, if_true]
      exact cancel_memory_mono _ e other requester i (by simpa only [attempt_roots, prepare_cancelled] using old)

theorem serviceTrial_other_memory_iff (w : ComposedExecution.World) (e other : ComposedExecution.Envelope)
    (requester : String) (i : Nat) (different : other ≠ e) :
    other ∈ ((serviceTrial w e requester).1.roots i).cancelled ↔ other ∈ (w.roots i).cancelled := by
  cases prepared : (ComposedExecution.prepare w e requester true).2 with
  | false =>
      simp only [serviceTrial, prepared, Bool.false_eq_true, if_false]
      rw [cancel_other_memory_iff _ e other requester i different, prepare_cancelled]
  | true =>
      simp only [serviceTrial, prepared, if_true]
      rw [cancel_other_memory_iff _ e other requester i different, attempt_roots, prepare_cancelled]

theorem intact_uncancelled_before_trial (w : ComposedExecution.World) (e other : ComposedExecution.Envelope)
    (requester : String) (after : IntactUncancelled (serviceTrial w e requester).1 other) :
    IntactUncancelled w other := by
  intro i selected
  obtain ⟨good, fresh⟩ := after i selected
  refine ⟨by simpa only [(serviceTrial_static w e requester).2.2.2.2.2] using good, ?_⟩
  intro old
  exact fresh (serviceTrial_memory_mono w e other requester i old)

theorem intact_uncancelled_after_other_trial (w : ComposedExecution.World)
    (e other : ComposedExecution.Envelope) (requester : String) (different : other ≠ e)
    (before : IntactUncancelled w other) : IntactUncancelled (serviceTrial w e requester).1 other := by
  intro i selected
  obtain ⟨good, fresh⟩ := before i selected
  refine ⟨by simpa only [(serviceTrial_static w e requester).2.2.2.2.2] using good, ?_⟩
  intro cancelled
  exact fresh ((serviceTrial_other_memory_iff w e other requester i different).mp cancelled)

/-- A live successful withholding attempt proves integrity and absence of a
prior exact tombstone at EVERY selected root, without a fault-cardinality premise. -/
theorem landed_trial_was_intact_uncancelled (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (landed : (serviceTrial w e requester).2.landed = true) :
    IntactUncancelled w e := by
  cases prepared : (ComposedExecution.prepare w e requester true).2 with
  | false => simp only [serviceTrial, prepared, Bool.false_eq_true, if_false] at landed
  | true =>
      have applied : (attempt (ComposedExecution.prepare w e requester true).1 e requester false).2 = true := by
        simpa only [serviceTrial, prepared, if_true] using landed
      have gates : e.path.all (gateOpen (ComposedExecution.prepare w e requester true).1 e requester false) = true := by
        unfold attempt at applied
        split at applied
        · rename_i guard
          exact (show validPath (ComposedExecution.prepare w e requester true).1 e = true ∧
            e.path.all (gateOpen (ComposedExecution.prepare w e requester true).1 e requester false) = true from
            by simpa only [Bool.and_eq_true] using guard).2
        · cases applied
      intro i selected
      have gate := List.all_eq_true.mp gates i selected
      have good : (ComposedExecution.prepare w e requester true).1.tainted i = false := by
        cases bad : (ComposedExecution.prepare w e requester true).1.tainted i with
        | false => rfl
        | true => simp [gateOpen, bad] at gate
      have permits : rootPermits (ComposedExecution.prepare w e requester true).1.plant
          (ComposedExecution.prepare w e requester true).1.now
          ((ComposedExecution.prepare w e requester true).1.roots i) e requester = true := by
        simpa only [gateOpen, good, Bool.false_eq_true, if_false] using gate
      have eligible := (show e ∈ ((ComposedExecution.prepare w e requester true).1.roots i).commitments ∧
          Eligible (ComposedExecution.prepare w e requester true).1.plant
            (ComposedExecution.prepare w e requester true).1.now
            ((ComposedExecution.prepare w e requester true).1.roots i) e requester from of_decide_eq_true permits).2
      exact ⟨by simpa only [(prepare_static w e requester true).2.2.2.2.2] using good,
        by simpa only [prepare_cancelled] using eligible.2.2.1⟩

theorem intact_uncancelled_trial_lands (w : ComposedExecution.World) (action : Action) (successor : Plant)
    (requester : String) (ready : AdmissionReady w action successor requester)
    (e : ComposedExecution.Envelope) (sameAction : e.action = action)
    (sameSuccessor : e.successor = successor) (valid : validPath w e = true)
    (survives : IntactUncancelled w e) : (serviceTrial w e requester).2.landed = true := by
  have bounds : ∀ i ∈ e.path, i < w.n := (of_decide_eq_true valid).2.2
  have eligible : ∀ i ∈ e.path, Eligible w.plant w.now (w.roots i) e requester := by
    intro i selected
    obtain ⟨good, fresh⟩ := survives i selected
    obtain ⟨policy, unrevoked⟩ := ready.2.2 i (bounds i selected) good
    refine ⟨by simpa only [sameAction] using ready.1,
      by simpa only [sameAction] using unrevoked, fresh, ?_⟩
    simpa only [sameAction, sameSuccessor, policy] using ready.2.1
  have prepares := prepare_succeeds w e requester valid (by intro i selected _; exact eligible i selected)
  have lands := intact_prepared_attempt w e requester valid (by intro i selected; exact (survives i selected).1) eligible
  simpa only [serviceTrial, prepares, if_true] using lands

theorem rejected_trial_admission_ready (w : ComposedExecution.World) (action : Action) (successor : Plant)
    (requester : String) (ready : AdmissionReady w action successor requester)
    (e : ComposedExecution.Envelope) (rejected : (serviceTrial w e requester).2.landed = false) :
    AdmissionReady (serviceTrial w e requester).1 action successor requester := by
  have frame := serviceTrial_static w e requester
  have plant : (serviceTrial w e requester).1.plant = w.plant := by
    rw [serviceTrial_plant, rejected]
    rfl
  refine ⟨ready.1, ?_, ?_⟩
  · simpa only [plant, frame.2.2.2.1, frame.2.2.2.2.1] using ready.2.1
  · intro i bound good
    have boundBefore : i < w.n := by simpa only [frame.1] using bound
    have goodBefore : w.tainted i = false := by simpa only [frame.2.2.2.2.2] using good
    have root := serviceTrial_root_frame w e requester i
    simpa only [root.1, root.2, frame.2.2.2.2.1] using ready.2.2 i boundBefore goodBefore

theorem cancel_admission_ready (w : ComposedExecution.World) (action : Action) (successor : Plant)
    (requester : String) (ready : AdmissionReady w action successor requester)
    (e : ComposedExecution.Envelope) :
    AdmissionReady (cancelWith w e requester e.path).1 action successor requester := by
  unfold cancelWith
  split
  · refine ⟨ready.1, ready.2.1, ?_⟩
    intro i bound good
    dsimp at bound good ⊢
    split <;> exact ready.2.2 i bound good
  · exact ready

/-- A proof-side coordinate test, not a new service operation: a tombstone at
an unselected root cannot change availability of this exact trial. No claim
that such an arbitrary initial store is lifecycle-reachable is made here. -/
theorem unselected_tombstone_irrelevant (w : ComposedExecution.World)
    (e : ComposedExecution.Envelope) (j : Nat) (unselected : j ∉ e.path) :
    IntactUncancelled { w with roots := fun i => if i = j then
      { w.roots i with cancelled := e :: (w.roots i).cancelled } else w.roots i } e ↔
      IntactUncancelled w e := by
  constructor <;> intro available i selected
  · have different : i ≠ j := by intro same; exact unselected (by simpa only [same] using selected)
    simpa only [if_neg different] using available i selected
  · have different : i ≠ j := by intro same; exact unselected (by simpa only [same] using selected)
    simpa only [if_neg different] using available i selected

#print axioms landed_trial_was_intact_uncancelled
#print axioms intact_uncancelled_trial_lands
#print axioms serviceTrial_other_memory_iff
end
end OperationalJoin.Offset.Batch
