import AliasPreservation

namespace SharedAlias
open OperationalJoin
noncomputable section
open Classical

/-- Weak forward safety simulation. Auxiliary event lists are proof witnesses,
not observed transcripts. Every genuine landing is retained exactly once. -/
theorem step_simulation {m} {I : Interface m} {E : Environment I}
    {C D : State I} {s : OperationalJoin.State I} {a : Event I}
    (h : Refines E C s) (consistent : Consistent E.labelConfig s)
    (step : Step E C a D) :
    ∃ t events, OperationalJoin.Trace E.labelConfig s events t ∧
      Refines E D t ∧ landings events = landings [a] := by
  cases step with
  | request idle =>
      refine ⟨OperationalJoin.request s, [.request], ?_, request_refines h, rfl⟩
      exact .cons (.request s (h.pending.trans idle)) (.nil _)
  | acknowledge i pending =>
      refine ⟨OperationalJoin.acknowledge E.labelConfig s i, [.acknowledge i], ?_,
        acknowledge_refines h i, rfl⟩
      exact .cons (.acknowledge s i (h.pending.trans pending)) (.nil _)
  | complete pending quorum =>
      refine ⟨OperationalJoin.complete s, [.complete], ?_, complete_refines h, rfl⟩
      apply OperationalJoin.Trace.cons (OperationalJoin.Step.complete s (h.pending.trans pending) ?_)
      · exact .nil _
      · simpa only [h.acks] using quorum
  | deliver i e cert =>
      obtain ⟨events, trace, none⟩ := deliverLabels_trace E.labelConfig s (aliases E i) e
        (by simpa only [h.epoch] using cert)
      exact ⟨_, events, trace, deliver_refines h i e, none⟩
  | prepare i k who time selected path grant =>
      have grants : ∀ j ∈ I.commandPath k ∩ aliases E i, j ∈ I.commandPath k ∧
          (j ∈ E.labelConfig.faulty ∨ Envelope s.plant time (s.roots j) k who) := by
        intro j hj
        obtain ⟨onPath, aliased⟩ := Finset.mem_inter.mp hj
        have sameRoot := (mem_aliases E i j).mp aliased
        refine ⟨onPath, ?_⟩
        by_cases goodJ : Good E.labelConfig j
        · right
          have concrete : Envelope C.plant time (C.roots (E.rootOf j)) k who := by
            rcases grant with bad | allowed
            · exact False.elim (((good_same_root E j i sameRoot).mp goodJ) bad)
            · simpa only [sameRoot] using allowed
          exact concrete_envelope_abstract h j goodJ time k who concrete
        · left
          exact Classical.not_not.mp goodJ
      obtain ⟨events, trace, none⟩ :=
        prepareLabels_trace E.labelConfig s (I.commandPath k ∩ aliases E i) k who time path grants
      exact ⟨_, events, trace, prepare_refines h i k, none⟩
  | cancelAck i k who selected auth =>
      refine ⟨OperationalJoin.cancelAck E.labelConfig s i k, [.cancelAck i k who], ?_,
        cancelAck_refines h i k, rfl⟩
      exact .cons (.cancelAck s i k who selected auth) (.nil _)
  | close k certificate =>
      refine ⟨s, [.close k], ?_, h, rfl⟩
      apply OperationalJoin.Trace.cons (OperationalJoin.Step.close s k ?_)
      · exact .nil _
      · simpa only [h.cancelAcks] using certificate
  | land k who time admitted =>
      have allowed := concrete_lands_abstract h time k who admitted
      have auth := (admitted_current_authorized consistent time k who allowed).2.2
      have actual : OperationalJoin.land E.labelConfig s time k who =
          { s with plant := I.effect s.plant k } := by
        simp [OperationalJoin.land, h.safe, auth]
      refine ⟨OperationalJoin.land E.labelConfig s time k who, [.land k who time],
        .cons (.land s k who time allowed) (.nil _), ?_, rfl⟩
      rw [actual]
      exact ⟨h.epoch, h.pending, h.acks, h.certificates, h.cancelAcks,
        congrArg (fun p => I.effect p k) h.plant, h.safe, h.roots⟩
  | hold => exact ⟨s, [], .nil _, h, rfl⟩
  | corrupt i z bad => exact ⟨s, [], .nil _, corrupt_refines h i z bad, rfl⟩

theorem trace_simulation {m} {I : Interface m} {E : Environment I}
    {C D : State I} {s : OperationalJoin.State I} {events : List (Event I)}
    (h : Refines E C s) (consistent : Consistent E.labelConfig s)
    (trace : Trace E C events D) :
    ∃ t expanded, OperationalJoin.Trace E.labelConfig s expanded t ∧
      Refines E D t ∧ landings expanded = landings events := by
  induction trace generalizing s with
  | nil => exact ⟨s, [], .nil _, h, rfl⟩
  | @cons C D F a events step tail ih =>
      obtain ⟨middle, firstEvents, first, related, firstLandings⟩ := step_simulation h consistent step
      obtain ⟨last, laterEvents, rest, lastRelated, restLandings⟩ :=
        ih related (consistent_trace consistent first)
      refine ⟨last, firstEvents ++ laterEvents, trace_append first rest, lastRelated, ?_⟩
      rw [landings_append, firstLandings, restLandings]
      cases a <;> rfl

theorem initial_trace_simulation {m} {I : Interface m} (E : Environment I)
    (p : I.Plant) {D : State I} {events : List (Event I)}
    (trace : Trace E (initial E p) events D) :
    ∃ t expanded, OperationalJoin.Trace E.labelConfig (Initial E.labelConfig p) expanded t ∧
      Refines E D t ∧ landings expanded = landings events :=
  trace_simulation (initial_refines E p) (consistent_initial E.labelConfig p) trace

theorem reachable_witness {m} {I : Interface m} {E : Environment I} {C : State I}
    (reach : Reachable E C) :
    ∃ s, OperationalJoin.Reachable E.labelConfig s ∧ Refines E C s := by
  obtain ⟨p, events, trace⟩ := reach
  obtain ⟨s, expanded, common, related, _⟩ := initial_trace_simulation E p trace
  exact ⟨s, ⟨p, expanded, common⟩, related⟩

theorem admitted_current {m} {I : Interface m} {E : Environment I} {C : State I}
    (reach : Reachable E C) (time : Nat) (k : I.Command) (who : I.Requester)
    (admitted : Lands E C time k who) :
    who = I.recipient k ∧ I.commandEpoch k = C.epoch ∧
      I.admits C.plant time (E.source C.epoch) k who := by
  obtain ⟨s, commonReach, related⟩ := reachable_witness reach
  have allowed := concrete_lands_abstract related time k who admitted
  have current := admitted_current_authorized (reachable_consistent commonReach) time k who allowed
  simpa only [related.epoch, related.plant] using current

theorem cancellation_persists {m} {I : Interface m} {E : Environment I}
    {C D : State I} {events : List (Event I)} (reach : Reachable E C)
    (trace : Trace E C events D) (k : I.Command)
    (certificate : E.labelBudget < (C.cancelAcks k).card)
    (time : Nat) (who : I.Requester) : ¬Lands E D time k who := by
  obtain ⟨s, commonReach, related⟩ := reachable_witness reach
  obtain ⟨t, expanded, common, laterRelated, _⟩ :=
    trace_simulation related (reachable_consistent commonReach) trace
  have closed : Cancelled E.labelConfig s k := by
    simpa only [Cancelled, related.cancelAcks] using certificate
  intro landed
  exact no_landing_after_cancellation commonReach common time k who closed
    (concrete_lands_abstract laterRelated time k who landed)

end
end SharedAlias
