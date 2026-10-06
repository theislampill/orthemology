import SharedStateTransport

namespace SharedAlias.OrderTransport
open OperationalJoin
open OperationalJoin.Typed (BoundedEnvelope interface path)
noncomputable section
open Classical

theorem step_map {m} (T : Symmetry m) (E : Environment (interface m))
    {C D : SharedAlias.State (interface m)} {e : Event (interface m)}
    (h : SharedAlias.Step E C e D) :
    SharedAlias.Step E (state T C) (event T e) (state T D) := by
  cases h with
  | request idle =>
      simpa only [event, state_request] using (SharedAlias.Step.request (E := E) (state T C) idle)
  | acknowledge i pending =>
      simpa only [event, state_acknowledge] using (SharedAlias.Step.acknowledge (E := E) (state T C) i pending)
  | complete pending quorum =>
      simpa only [event, state_complete] using (SharedAlias.Step.complete (E := E) (state T C) pending quorum)
  | deliver i e cert =>
      simpa only [event, state_deliver] using (SharedAlias.Step.deliver (E := E) (state T C) i e cert)
  | prepare i k who time selected valid grant =>
      have selected' : i ∈ (interface m).commandPath (T.command k) := by
        simpa only [interface, T.support] using selected
      have grant' : i ∈ E.labelConfig.faulty ∨
          Envelope (state T C).plant time ((state T C).roots (E.rootOf i)) (T.command k) who := by
        rcases grant with bad | good
        · exact Or.inl bad
        · exact Or.inr ((envelope_iff T _ _ _ _ _).mpr good)
      simpa only [event, state_prepare] using
        (SharedAlias.Step.prepare (state T C) i (T.command k) who time selected'
          ((valid_iff T E k).mpr valid) grant')
  | cancelAck i k who selected auth =>
      have selected' : i ∈ (interface m).commandPath (T.command k) := by
        simpa only [interface, T.support] using selected
      have auth' : i ∈ E.labelConfig.faulty ∨ who = (interface m).recipient (T.command k) := by
        simpa only [interface, T.action] using auth
      simpa only [event, state_cancelAck] using
        (SharedAlias.Step.cancelAck (state T C) i (T.command k) who selected' auth')
  | close k certificate =>
      have cert : E.labelBudget < ((state T C).cancelAcks (T.command k)).card := by
        simpa only [state_receipts] using certificate
      exact SharedAlias.Step.close (state T C) (T.command k) cert
  | land k who time admitted =>
      simpa only [event, state_land] using
        (SharedAlias.Step.land (state T C) (T.command k) who time ((lands_iff T E C time k who).mpr admitted))
  | hold => exact SharedAlias.Step.hold (state T C)
  | corrupt i z bad =>
      simpa only [event, state_setRoot] using
        (SharedAlias.Step.corrupt (state T C) i (root T z) bad)

theorem step_iff {m} (T : Symmetry m) (E : Environment (interface m))
    (C D : SharedAlias.State (interface m)) (e : Event (interface m)) :
    SharedAlias.Step E C e D ↔ SharedAlias.Step E (state T C) (event T e) (state T D) := by
  constructor
  · exact step_map T E
  · intro h
    simpa only [state_involutive, event_involutive] using step_map T E h

theorem trace_map {m} (T : Symmetry m) (E : Environment (interface m))
    {C D : SharedAlias.State (interface m)} {es : List (Event (interface m))}
    (h : SharedAlias.Trace E C es D) :
    SharedAlias.Trace E (state T C) (es.map (event T)) (state T D) := by
  induction h with
  | nil C => exact .nil _
  | cons h _ ih => exact .cons (step_map T E h) ih

theorem trace_iff {m} (T : Symmetry m) (E : Environment (interface m))
    (C D : SharedAlias.State (interface m)) (es : List (Event (interface m))) :
    SharedAlias.Trace E C es D ↔ SharedAlias.Trace E (state T C) (es.map (event T)) (state T D) := by
  constructor
  · exact trace_map T E
  · intro h
    simpa only [state_involutive, List.map_map, Function.comp_def, event_involutive,
      List.map_id_fun'] using trace_map T E h

theorem reachable_iff {m} (T : Symmetry m) (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) :
    SharedAlias.Reachable E C ↔ SharedAlias.Reachable E (state T C) := by
  have forward : ∀ D, SharedAlias.Reachable E D → SharedAlias.Reachable E (state T D) := by
    intro D ⟨p, es, h⟩
    refine ⟨p, es.map (event T), ?_⟩
    simpa only [state_initial] using trace_map T E h
  exact ⟨forward C, fun h => by simpa only [state_involutive] using forward (state T C) h⟩

@[simp] theorem trace_length {m} (T : Symmetry m) (es : List (Event (interface m))) :
    (es.map (event T)).length = es.length := List.length_map (event T)

end
end SharedAlias.OrderTransport
