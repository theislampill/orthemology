import NegativeControls
open InterlockHistory
open InterlockHistory.Controls (trace_append reachable_after)
namespace InterlockHistory.MultiEpoch

def source (e : Nat) : Descriptor :=
  ⟨e, 7, e, 11, 3, if e % 2 = 0 then (false, true) else (true, false), true⟩

def cfg : Config 4 := { Controls.cfg with source := source, source_epoch := by intro e; rfl }
def command (e nonce : Nat) : Command 4 :=
  ⟨e, 7, e, 11, 3, (source e).table, nonce, {0,1,2}⟩
def initial : State 4 := Initial cfg (true,true)
def advance (s : State 4) : State 4 :=
  complete (acknowledge cfg (acknowledge cfg (acknowledge cfg (request s) 1) 2) 3)

theorem advance_trace (s : State 4) (idle : s.pending = false) :
    Trace cfg s [.request, .acknowledge 1, .acknowledge 2, .acknowledge 3, .complete]
      (advance s) := by
  apply Trace.cons (Step.request _ idle)
  apply Trace.cons (Step.acknowledge _ 1 rfl)
  apply Trace.cons (Step.acknowledge _ 2 rfl)
  apply Trace.cons (Step.acknowledge _ 3 rfl)
  apply Trace.cons (Step.complete _ rfl (by
    change (insert 3 (insert 2 (insert 1 (∅ : Finset (Fin 4))))).card = 3
    decide))
  exact Trace.nil _

def epoch1 : State 4 := advance initial
def epoch2 : State 4 := advance epoch1

theorem epoch2_reachable : Reachable cfg epoch2 := by
  have init : Reachable cfg initial := ⟨(true,true), [], .nil _⟩
  exact reachable_after (reachable_after init (advance_trace initial rfl))
    (advance_trace epoch1 rfl)

/-- Root 1 learns epoch 2 directly; root 2 first learns valid old epoch 1. -/
def partialDelivery : State 4 := deliver cfg (deliver cfg epoch2 1 2) 2 1

theorem partial_trace : Trace cfg epoch2 [.deliver 1 2, .deliver 2 1] partialDelivery := by
  apply Trace.cons (Step.deliver _ 1 2 (by decide))
  apply Trace.cons (Step.deliver _ 2 1 (by decide))
  exact Trace.nil _

example : partialDelivery.epoch = 2 ∧
    (partialDelivery.roots 1).descriptor.epoch = 2 ∧
    (partialDelivery.roots 2).descriptor.epoch = 1 := by decide

/-- Repeated stale certificate cannot rewind root 1; root 2 now catches up. -/
def delivered : State 4 := deliver cfg (deliver cfg partialDelivery 1 1) 2 2

theorem finish_delivery : Trace cfg partialDelivery [.deliver 1 1, .deliver 2 2] delivered := by
  apply Trace.cons (Step.deliver _ 1 1 (by decide))
  apply Trace.cons (Step.deliver _ 2 2 (by decide))
  exact Trace.nil _

example : (delivered.roots 1).descriptor.epoch = 2 ∧
    (delivered.roots 2).descriptor.epoch = 2 ∧ (delivered.roots 3).descriptor.epoch = 0 := by
  decide

def prepared : State 4 := prepare (prepare (prepare delivered 0 (command 2 8))
  1 (command 2 8)) 2 (command 2 8)

theorem preparation_trace : Trace cfg delivered
    [.prepare 0 (command 2 8) 11, .prepare 1 (command 2 8) 11,
      .prepare 2 (command 2 8) 11] prepared := by
  apply Trace.cons (Step.prepare _ 0 _ 11 (by decide) (by decide) (Or.inl (by decide)))
  apply Trace.cons (Step.prepare _ 1 _ 11 (by decide) (by decide) (Or.inr (by decide)))
  apply Trace.cons (Step.prepare _ 2 _ 11 (by decide) (by decide) (Or.inr (by decide)))
  exact Trace.nil _

def repaired : State 4 := land cfg prepared (command 2 8) 11

theorem actual_landing : Step cfg prepared (.land (command 2 8) 11) repaired :=
  Step.land _ _ _ (by decide)

theorem repaired_reachable : Reachable cfg repaired := by
  have reached := reachable_after (reachable_after (reachable_after epoch2_reachable
    partial_trace) finish_delivery) preparation_trace
  exact reachable_after reached (.cons actual_landing (.nil _))

theorem restored_after_two_transitions : Restored cfg repaired := by
  unfold Restored
  decide

example : ¬Lands cfg repaired (command 0 1) 11 ∧
    ¬Lands cfg repaired (command 1 2) 11 := by
  constructor
  · exact stale_cannot_land (reachable_consistent repaired_reachable) _ _ (by decide)
  · exact stale_cannot_land (reachable_consistent repaired_reachable) _ _ (by decide)

#print axioms repaired_reachable
#print axioms restored_after_two_transitions
end InterlockHistory.MultiEpoch
