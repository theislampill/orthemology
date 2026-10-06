import SharedService

namespace SharedAlias.Progress
open OperationalJoin
open OperationalJoin.Typed (interface BoundedEnvelope path mem_path)
noncomputable section
open Classical

/-- The source live gate is used verbatim; only its state update is lifted back
into the single shared-root state after proved successful admission. -/
def applied {m} (E : Environment (interface m)) (C : SharedAlias.State (interface m))
    (k : BoundedEnvelope m) (who : String) (time : Nat) (badOpen : Bool) : Bool :=
  (ComposedExecution.attempt (SharedAlias.Typed.gateWorld E C time) k.val who badOpen).2

def attemptSlot {m} (E : Environment (interface m)) (C : SharedAlias.State (interface m))
    (k : BoundedEnvelope m) (who : String) (time : Nat) (badOpen : Bool) :
    SharedAlias.State (interface m) :=
  if applied E C k who time badOpen then SharedAlias.land C k else C

/-- Bad choices are environmental service outcomes; the controller never reads
this record. Honest service is fixed by the scheduled handlers. -/
structure Replies (m : Nat) where
  prepare : Fin m → Bool
  openGate : Bool
  cancel : Fin m → Bool

def trial {m} (E : Environment (interface m)) (C : SharedAlias.State (interface m))
    (k : BoundedEnvelope m) (who : String) (time : Nat) (bad : Replies m) :
    SharedAlias.State (interface m) :=
  let ready := preparePath E C k who time bad.prepare
  let landed := attemptSlot E ready k who time bad.openGate
  cancelPath E landed k who bad.cancel

theorem attemptSlot_step {m} (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (k : BoundedEnvelope m) (who : String)
    (time : Nat) (badOpen : Bool) :
    ∃ event, SharedAlias.Step E C event (attemptSlot E C k who time badOpen) := by
  cases h : applied E C k who time badOpen with
  | false =>
      refine ⟨.hold, ?_⟩
      simpa only [attemptSlot, h, Bool.false_eq_true, if_false] using (SharedAlias.Step.hold (E := E) C)
  | true =>
      refine ⟨.land k who time, ?_⟩
      simp only [attemptSlot, h, if_true]
      exact SharedAlias.Step.land C k who time
        (SharedAlias.Typed.compiled_success_lands E C time k who badOpen h)

/-- On an all-good path, the source's arbitrary faulty-gate Boolean is irrelevant. -/
theorem all_good_attempt_succeeds {m} (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (k : BoundedEnvelope m) (who : String)
    (time : Nat) (badOpen : Bool)
    (allGood : ∀ i ∈ path k, Good E.labelConfig i)
    (lands : SharedAlias.Lands E C time k who) : applied E C k who time badOpen = true := by
  have openSuccess := (SharedAlias.Typed.compiled_attempt_iff E C time k who).mpr lands
  have gateEq : ∀ j ∈ k.val.path,
      ComposedExecution.gateOpen (SharedAlias.Typed.gateWorld E C time) k.val who badOpen j =
      ComposedExecution.gateOpen (SharedAlias.Typed.gateWorld E C time) k.val who true j := by
    intro j member
    have bound : j < m := k.property.2 j member
    let i : Fin m := ⟨j, bound⟩
    have good : Good E.labelConfig i := allGood i ((mem_path k i).mpr member)
    have clean : E.rootOf i ∉ E.actualFaults := (good_iff E i).mp good
    simp [ComposedExecution.gateOpen, SharedAlias.Typed.gateWorld, bound, clean, i] at *
  have allEq :
      k.val.path.all (ComposedExecution.gateOpen (SharedAlias.Typed.gateWorld E C time) k.val who badOpen) =
      k.val.path.all (ComposedExecution.gateOpen (SharedAlias.Typed.gateWorld E C time) k.val who true) := by
    apply Bool.eq_iff_iff.mpr
    simp only [List.all_eq_true]
    constructor
    · intro h j hj
      rw [← gateEq j hj]
      exact h j hj
    · intro h j hj
      rw [gateEq j hj]
      exact h j hj
  simpa only [applied, ComposedExecution.attempt, allEq] using openSuccess

theorem trial_trace {m} (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (k : BoundedEnvelope m) (who : String)
    (time : Nat) (bad : Replies m) (valid : ValidPath E.labelConfig k)
    (auth : who = k.val.action.actor) :
    ∃ events, SharedAlias.Trace E C events (trial E C k who time bad) ∧
      events.length = 2 * E.q + 2 := by
  obtain ⟨ps, prepTrace, prepSize⟩ := preparePath_trace E C k who time bad.prepare valid
  obtain ⟨event, attemptTrace⟩ := attemptSlot_step E (preparePath E C k who time bad.prepare)
    k who time bad.openGate
  obtain ⟨cs, cancelTrace, cancelSize⟩ := cancelPath_trace E
    (attemptSlot E (preparePath E C k who time bad.prepare) k who time bad.openGate)
    k who bad.cancel valid
  have closed := cancelPath_closes E
    (attemptSlot E (preparePath E C k who time bad.prepare) k who time bad.openGate)
    k who bad.cancel valid auth
  refine ⟨ps ++ event :: (cs ++ [.close k]), ?_, ?_⟩
  · have last : SharedAlias.Trace E (trial E C k who time bad) [.close k] (trial E C k who time bad) :=
      .cons (SharedAlias.Step.close (E := E) (trial E C k who time bad) k closed) (.nil _)
    exact trace_append prepTrace (.cons attemptTrace (trace_append cancelTrace last))
  · simp only [List.length_append, List.length_cons, List.length_nil, prepSize, cancelSize]
    omega

/-- Even an arbitrary misleading/withheld bad reply cannot prevent an all-good
scheduled path from applying under the stated local source window. -/
theorem trial_all_good {m} (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (k : BoundedEnvelope m) (who : String)
    (time : Nat) (bad : Replies m) (valid : ValidPath E.labelConfig k)
    (allGood : ∀ i ∈ path k, Good E.labelConfig i)
    (ready : ∀ i, Good E.labelConfig i →
      Envelope C.plant time (C.roots (E.rootOf i)) k who) :
    (trial E C k who time bad).plant = k.val.successor := by
  have permits := preparePath_permits E C k who time bad.prepare valid ready
  have applies := all_good_attempt_succeeds E _ k who time bad.openGate allGood permits
  simp only [trial, cancelPath_plant, attemptSlot, applies, if_true]
  rfl

theorem trial_plant_cases {m} (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (k : BoundedEnvelope m) (who : String)
    (time : Nat) (bad : Replies m) :
    (trial E C k who time bad).plant = C.plant ∨
      (trial E C k who time bad).plant = k.val.successor := by
  simp only [trial, cancelPath_plant]
  unfold attemptSlot
  split
  · exact Or.inr rfl
  · exact Or.inl (preparePath_plant E C k who time bad.prepare)

end
end SharedAlias.Progress
