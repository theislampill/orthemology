import TypedExamples

namespace OperationalJoin.Typed
noncomputable section
open Classical

/-- Fixture helper only: explicitly list each selected root event. -/
def prepare123 (s : State (interface 4)) (e : BoundedEnvelope 4) : State (interface 4) :=
  prepare (prepare (prepare s 1 e) 2 e) 3 e

theorem prepare123_trace (c : Config (interface 4)) (s : State (interface 4))
    (e : BoundedEnvelope 4) (requester : String) (time : Nat)
    (pathEq : e.val.path = [1,2,3]) (quorum : c.q = 3)
    (ready : ∀ i : Fin 4, i = 1 ∨ i = 2 ∨ i = 3 →
      Envelope s.plant time (s.roots i) e requester) :
    Trace c s [.prepare 1 e requester time, .prepare 2 e requester time,
      .prepare 3 e requester time] (prepare123 s e) := by
  have selected (i : Fin 4) (h : i = 1 ∨ i = 2 ∨ i = 3) : i ∈ (interface 4).commandPath e := by
    change i ∈ path e
    rw [mem_path, pathEq]
    rcases h with rfl | rfl | rfl <;> decide
  have valid : ValidPath c e := by
    change (path e).card = c.q
    rw [path_card, pathEq, quorum]
    rfl
  apply Trace.cons (Step.prepare (c := c) _ 1 e requester time
    (selected 1 (Or.inl rfl)) valid (Or.inr (ready 1 (Or.inl rfl))))
  apply Trace.cons (Step.prepare (c := c) _ 2 e requester time
    (selected 2 (Or.inr (Or.inl rfl))) valid ?_)
  · apply Trace.cons (Step.prepare (c := c) _ 3 e requester time
      (selected 3 (Or.inr (Or.inr rfl))) valid ?_)
    · exact Trace.nil _
    · right
      simpa only [prepare_envelope] using ready 3 (Or.inr (Or.inr rfl))
  · right
    simpa only [prepare_envelope] using ready 2 (Or.inr (Or.inl rfl))

theorem prepare123_lands (c : Config (interface 4)) (s : State (interface 4))
    (e : BoundedEnvelope 4) (requester : String) (time : Nat)
    (pathEq : e.val.path = [1,2,3]) (quorum : c.q = 3)
    (ready : ∀ i : Fin 4, i = 1 ∨ i = 2 ∨ i = 3 →
      Envelope s.plant time (s.roots i) e requester) :
    Lands c (prepare123 s e) time e requester := by
  constructor
  · change (path e).card = c.q
    rw [path_card, pathEq, quorum]
    rfl
  · intro i selected _good
    have cases : i = 1 ∨ i = 2 ∨ i = 3 := by
      simpa [interface, path, pathEq, Fin.ext_iff] using selected
    constructor
    · rcases cases with rfl | rfl | rfl <;>
        simp [prepare123, prepare, setRoot, Function.update_apply]
    · simpa only [prepare123, prepare_envelope] using ready i cases

end
end OperationalJoin.Typed
