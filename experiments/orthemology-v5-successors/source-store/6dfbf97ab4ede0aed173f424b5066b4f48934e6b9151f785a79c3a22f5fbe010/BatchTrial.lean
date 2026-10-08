import BatchSource

namespace OperationalJoin.Offset.Batch
noncomputable section
open Classical
open ComposedExecution

/-- The exact source service sequence after a successful proposal, including
partial preparation and unconditional cleanup. -/
def serviceTrial (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) : ComposedExecution.World × AttemptTrace :=
  let prepared := ComposedExecution.prepare w e requester true
  let landed := if prepared.2 then attempt prepared.1 e requester false else (prepared.1, false)
  let closed := cancelWith landed.1 e requester e.path
  (closed.1, ⟨e.nonce, e.path, prepared.2, landed.2, closed.2,
    closed.1.plant.ruleVersion, closed.1.plant.draftRevision⟩)

theorem batchBody_of_proposal (actor : Actor) (action : Action)
    (acc : ComposedExecution.World × List AttemptTrace) (path : List Nat)
    (e : ComposedExecution.Envelope)
    (proposal : propose { actor with nonce := actor.nonce + acc.2.length } action path = some e) :
    batchBody actor action acc path =
      ((serviceTrial acc.1 e actor.identity).1, acc.2 ++ [(serviceTrial acc.1 e actor.identity).2]) := by
  have pathEq := (proposal_fields _ _ _ e proposal).2.1
  simp only [batchBody, proposal, serviceTrial, pathEq]

theorem prepare_plant (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (badSign : Bool) :
    (ComposedExecution.prepare w e requester badSign).1.plant = w.plant := by
  unfold ComposedExecution.prepare
  split <;> rfl

theorem prepare_static (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (badSign : Bool) :
    (ComposedExecution.prepare w e requester badSign).1.n = w.n ∧
    (ComposedExecution.prepare w e requester badSign).1.q = w.q ∧
    (ComposedExecution.prepare w e requester badSign).1.budget = w.budget ∧
    (ComposedExecution.prepare w e requester badSign).1.now = w.now ∧
    (ComposedExecution.prepare w e requester badSign).1.effectivePolicy = w.effectivePolicy ∧
    (ComposedExecution.prepare w e requester badSign).1.tainted = w.tainted := by
  unfold ComposedExecution.prepare
  split <;> exact ⟨rfl, rfl, rfl, rfl, rfl, rfl⟩

theorem attempt_static (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (badOpen : Bool) :
    (attempt w e requester badOpen).1.n = w.n ∧
    (attempt w e requester badOpen).1.q = w.q ∧
    (attempt w e requester badOpen).1.budget = w.budget ∧
    (attempt w e requester badOpen).1.now = w.now ∧
    (attempt w e requester badOpen).1.effectivePolicy = w.effectivePolicy ∧
    (attempt w e requester badOpen).1.tainted = w.tainted := by
  unfold attempt
  split <;> exact ⟨rfl, rfl, rfl, rfl, rfl, rfl⟩

theorem cancel_plant (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (acks : List Nat) :
    (cancelWith w e requester acks).1.plant = w.plant := by
  unfold cancelWith
  split <;> rfl

theorem cancel_static (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (acks : List Nat) :
    (cancelWith w e requester acks).1.n = w.n ∧
    (cancelWith w e requester acks).1.q = w.q ∧
    (cancelWith w e requester acks).1.budget = w.budget ∧
    (cancelWith w e requester acks).1.now = w.now ∧
    (cancelWith w e requester acks).1.effectivePolicy = w.effectivePolicy ∧
    (cancelWith w e requester acks).1.tainted = w.tainted := by
  unfold cancelWith
  split <;> exact ⟨rfl, rfl, rfl, rfl, rfl, rfl⟩

theorem serviceTrial_static (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) :
    (serviceTrial w e requester).1.n = w.n ∧
    (serviceTrial w e requester).1.q = w.q ∧
    (serviceTrial w e requester).1.budget = w.budget ∧
    (serviceTrial w e requester).1.now = w.now ∧
    (serviceTrial w e requester).1.effectivePolicy = w.effectivePolicy ∧
    (serviceTrial w e requester).1.tainted = w.tainted := by
  cases ready : (ComposedExecution.prepare w e requester true).2 with
  | false =>
      simpa only [serviceTrial, ready, Bool.false_eq_true, if_false] using
        (show (cancelWith (ComposedExecution.prepare w e requester true).1 e requester e.path).1.n = w.n ∧
          (cancelWith (ComposedExecution.prepare w e requester true).1 e requester e.path).1.q = w.q ∧
          (cancelWith (ComposedExecution.prepare w e requester true).1 e requester e.path).1.budget = w.budget ∧
          (cancelWith (ComposedExecution.prepare w e requester true).1 e requester e.path).1.now = w.now ∧
          (cancelWith (ComposedExecution.prepare w e requester true).1 e requester e.path).1.effectivePolicy = w.effectivePolicy ∧
          (cancelWith (ComposedExecution.prepare w e requester true).1 e requester e.path).1.tainted = w.tainted from by
            have hc := cancel_static (ComposedExecution.prepare w e requester true).1 e requester e.path
            have hp := prepare_static w e requester true
            exact ⟨hc.1.trans hp.1, hc.2.1.trans hp.2.1, hc.2.2.1.trans hp.2.2.1,
              hc.2.2.2.1.trans hp.2.2.2.1, hc.2.2.2.2.1.trans hp.2.2.2.2.1,
              hc.2.2.2.2.2.trans hp.2.2.2.2.2⟩)
  | true =>
      simp only [serviceTrial, ready, if_true]
      have hc := cancel_static (attempt (ComposedExecution.prepare w e requester true).1 e requester false).1 e requester e.path
      have ha := attempt_static (ComposedExecution.prepare w e requester true).1 e requester false
      have hp := prepare_static w e requester true
      exact ⟨hc.1.trans (ha.1.trans hp.1), hc.2.1.trans (ha.2.1.trans hp.2.1),
        hc.2.2.1.trans (ha.2.2.1.trans hp.2.2.1), hc.2.2.2.1.trans (ha.2.2.2.1.trans hp.2.2.2.1),
        hc.2.2.2.2.1.trans (ha.2.2.2.2.1.trans hp.2.2.2.2.1),
        hc.2.2.2.2.2.trans (ha.2.2.2.2.2.trans hp.2.2.2.2.2)⟩

/-- Withholding at every faulty gate makes any success on a nonempty path
supply an intact local-step witness. This needs no cardinal fault bound. -/
theorem withholding_attempt_witness (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (nonempty : e.path ≠ [])
    (applied : (attempt w e requester false).2 = true) :
    ∃ i, i ∈ e.path ∧ w.tainted i = false ∧
      localStep w.plant (w.roots i).policy w.now e.action = some e.successor := by
  have gates : e.path.all (gateOpen w e requester false) = true := by
    unfold attempt at applied
    split at applied
    · rename_i guard
      exact (show validPath w e = true ∧ e.path.all (gateOpen w e requester false) = true from
        by simpa only [Bool.and_eq_true] using guard).2
    · cases applied
  obtain ⟨i, member⟩ := List.exists_mem_of_ne_nil e.path nonempty
  have gate := List.all_eq_true.mp gates i member
  have good : w.tainted i = false := by
    cases bad : w.tainted i with
    | false => rfl
    | true => simp [gateOpen, bad] at gate
  refine ⟨i, member, good, ?_⟩
  exact permits_imported_step w.plant w.now (w.roots i) e requester
    (by simpa only [gateOpen, good, Bool.false_eq_true, if_false] using gate)

theorem serviceTrial_landing_witness (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (nonempty : e.path ≠ [])
    (landed : (serviceTrial w e requester).2.landed = true) :
    ∃ policy, localStep w.plant policy w.now e.action = some e.successor := by
  cases ready : (ComposedExecution.prepare w e requester true).2 with
  | false => simp only [serviceTrial, ready, Bool.false_eq_true, if_false] at landed
  | true =>
      have applied : (attempt (ComposedExecution.prepare w e requester true).1 e requester false).2 = true := by
        simpa only [serviceTrial, ready, if_true] using landed
      obtain ⟨i, _, _, step⟩ := withholding_attempt_witness
        (ComposedExecution.prepare w e requester true).1 e requester nonempty applied
      refine ⟨((ComposedExecution.prepare w e requester true).1.roots i).policy, ?_⟩
      simpa only [prepare_plant, (prepare_static w e requester true).2.2.2.1] using step

theorem serviceTrial_plant (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) :
    (serviceTrial w e requester).1.plant =
      if (serviceTrial w e requester).2.landed then e.successor else w.plant := by
  cases ready : (ComposedExecution.prepare w e requester true).2 with
  | false => simp only [serviceTrial, ready, Bool.false_eq_true, if_false, cancel_plant, prepare_plant]
  | true =>
      simp only [serviceTrial, ready, if_true, cancel_plant]
      cases applied : (attempt (ComposedExecution.prepare w e requester true).1 e requester false).2 with
      | false =>
          simp only [Bool.false_eq_true, if_false,
            rejected_attempt_full_identity _ _ _ _ applied, prepare_plant]
      | true =>
          simp only [if_true, applied_attempt_exact_successor _ _ _ _ applied]

theorem serviceTrial_no_relanding (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (nonempty : e.path ≠ [])
    (blocked : ∀ policy time, localStep w.plant policy time e.action = none) :
    (serviceTrial w e requester).2.landed = false ∧
      (serviceTrial w e requester).1.plant = w.plant := by
  have rejected : (serviceTrial w e requester).2.landed = false := by
    cases landed : (serviceTrial w e requester).2.landed with
    | false => rfl
    | true =>
        obtain ⟨policy, step⟩ := serviceTrial_landing_witness w e requester nonempty landed
        rw [blocked] at step
        cases step
  exact ⟨rejected, by rw [serviceTrial_plant, rejected]; rfl⟩

#print axioms withholding_attempt_witness
#print axioms serviceTrial_no_relanding
end
end OperationalJoin.Offset.Batch
