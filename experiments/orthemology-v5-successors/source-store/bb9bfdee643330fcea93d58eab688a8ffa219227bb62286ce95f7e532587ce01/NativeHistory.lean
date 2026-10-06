import NativeRefinement

/-! Finite history representation. This replay layer records already justified
history; it is not a guard or an independent source of authority. Policy and
corruption samples are explicit finite input values. -/
namespace SharedAlias.Native
open ComposedExecution
open OperationalJoin.Typed (BoundedEnvelope interface rootView)

/-- Event data sufficient to replay a finite accepted history. Delivery names
its full policy sample, corruption names its raw finite root sample. -/
inductive HistoryInput (m : Nat) where
  | request
  | acknowledge (i : Fin m)
  | complete
  | deliver (i : Fin m) (policy : Policy)
  | prepare (i : Fin m) (k : BoundedEnvelope m) (who : String) (time : Nat)
  | cancelAck (i : Fin m) (k : BoundedEnvelope m) (who : String)
  | close (k : BoundedEnvelope m)
  | land (k : BoundedEnvelope m) (who : String) (time : Nat)
  | hold
  | corrupt (i : Fin m) (root : Root)

def acknowledgeUpdate {m} (D : Routing m) (C : FiniteState m) (i : Fin m) : FiniteState m :=
  let R := { C with acks := i :: C.acks }
  if faulty D i then R
  else
    let z := rootAt C (rootOf D i)
    setRoot R (rootOf D i) { z with revoked := C.epoch :: z.revoked }

def completeUpdate {m} (C : FiniteState m) : FiniteState m :=
  { C with
    epoch := C.epoch + 1
    pending := false
    acks := []
    certificateRows := (C.epoch, C.acks) :: C.certificateRows }

/-- No policy is obtained from a default or missing table entry. The policy
sample is an explicit argument, whose authenticity belongs to history validity. -/
def deliverUpdate {m} (D : Routing m) (C : FiniteState m) (i : Fin m)
    (policy : Policy) : FiniteState m :=
  let z := rootAt C (rootOf D i)
  if z.policy.epoch < policy.epoch then setRoot C (rootOf D i) { z with policy } else C

/-- Guard-free reconstruction of an already accepted event. Do not use it as
an authorization API: the refinement theorem requires an accepted Step. -/
def replayUpdate {m} (D : Routing m) (C : FiniteState m) : HistoryInput m → FiniteState m
  | .request => { C with pending := true, acks := [] }
  | .acknowledge i => acknowledgeUpdate D C i
  | .complete => completeUpdate C
  | .deliver i policy => deliverUpdate D C i policy
  | .prepare i k _ _ => prepareUpdate D C i k
  | .cancelAck i k _ => cancelUpdate D C i k
  | .close _ => C
  | .land k _ _ => { C with plant := k.val.successor }
  | .hold => C
  | .corrupt i z => setRoot C (rootOf D i) z

def replayHistory {m} (D : Routing m) : FiniteState m → List (HistoryInput m) → FiniteState m
  | C, [] => C
  | C, event :: rest => replayHistory D (replayUpdate D C event) rest

noncomputable section
open Classical

/-- Only this proof-side projection mentions accepted Event/rootView. -/
def HistoryInput.event {m} : HistoryInput m → OperationalJoin.Event (interface m)
  | .request => .request
  | .acknowledge i => .acknowledge i
  | .complete => .complete
  | .deliver i policy => .deliver i policy.epoch
  | .prepare i k who time => .prepare i k who time
  | .cancelAck i k who => .cancelAck i k who
  | .close k => .close k
  | .land k who time => .land k who time
  | .hold => .hold
  | .corrupt i z => .corrupt i (rootView z)

/-- Explicit sampled-policy validity, separate from successful lookup or the
native live gate. Only delivery inputs make an authentication claim. -/
def HistoryInput.Authentic {m} (E : SharedAlias.Environment (interface m)) : HistoryInput m → Prop
  | .deliver _ policy => policy = E.source policy.epoch
  | _ => True

theorem rootView_revoked {m} (z : Root) (epoch : Nat) :
    rootView (n := m) { z with revoked := epoch :: z.revoked } =
      { rootView (n := m) z with revoked := insert epoch (rootView (n := m) z).revoked } := by
  simp only [rootView, List.toFinset_cons]

theorem rootView_policy {m} (z : Root) (policy : Policy) :
    rootView (n := m) { z with policy } = { rootView z with descriptor := policy } := rfl

/-- Proof-side reification of a finite root. This theorem does not provide a
callable serializer of opaque SharedAlias.State functions. -/
theorem rootView_rawRoot {m} (z : OperationalJoin.RootState (interface m)) :
    rootView (SharedAlias.Typed.rawRoot z) = z := by
  rcases z with ⟨policy, revoked, commitments, cancelled⟩
  unfold rootView SharedAlias.Typed.rawRoot
  simp only [Finset.toList_toFinset]
  congr 1
  · ext k
    simp only [OperationalJoin.Typed.mem_memory]
    exact SharedAlias.Typed.mem_raw_commands _ k
  · ext k
    simp only [OperationalJoin.Typed.mem_memory]
    exact SharedAlias.Typed.mem_raw_commands _ k

theorem initial_view {m} (E : SharedAlias.Environment (interface m)) (p : Plant) :
    view (initial (E.source 0) p) = SharedAlias.initial E p := rfl

theorem acknowledgeUpdate_refines {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (C : FiniteState m) (i : Fin m) :
    view (acknowledgeUpdate D C i) = SharedAlias.acknowledge E (view C) i := by
  by_cases good : OperationalJoin.Good E.labelConfig i
  · have hbad := (faulty_false_iff D E matchD i).mpr good
    simp only [acknowledgeUpdate, hbad, Bool.false_eq_true, if_false]
    rw [view_setRoot, rootView_revoked, rootOf_matches D E matchD]
    simp only [SharedAlias.acknowledge, SharedAlias.setRoot, if_pos good, view, rootAt, receipts,
      List.toFinset_cons]
  · have hbad : faulty D i = true := by
      cases h : faulty D i with
      | true => rfl
      | false => exact False.elim (good ((faulty_false_iff D E matchD i).mp h))
    simp only [acknowledgeUpdate, hbad, if_true, SharedAlias.acknowledge, if_neg good, view, rootAt, receipts,
      List.toFinset_cons]

theorem completeUpdate_refines {m} (C : FiniteState m) :
    view (completeUpdate C) = SharedAlias.complete (view C) := by
  unfold completeUpdate view SharedAlias.complete
  congr 1
  funext e
  by_cases same : e = C.epoch
  · subst e; simp [tableRead]
  · simp [tableRead, same, Function.update_of_ne same]

theorem source_epoch_value {m} (E : SharedAlias.Environment (interface m)) (epoch : Nat) :
    (E.source epoch).epoch = epoch := E.source_epoch epoch

theorem deliverUpdate_refines {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (C : FiniteState m) (i : Fin m) (epoch : Nat) :
    view (deliverUpdate D C i (E.source epoch)) = SharedAlias.deliver E (view C) i epoch := by
  simp only [deliverUpdate, source_epoch_value, rootOf_matches D E matchD]
  unfold SharedAlias.deliver
  change view (if (rootAt C (E.rootOf i)).policy.epoch < epoch then
    setRoot C (E.rootOf i) { rootAt C (E.rootOf i) with policy := E.source epoch } else C) =
    if (rootAt C (E.rootOf i)).policy.epoch < epoch then
      SharedAlias.setRoot (view C) (E.rootOf i)
        { (view C).roots (E.rootOf i) with descriptor := E.source epoch } else view C
  split
  · rw [view_setRoot, rootView_policy]
    rfl
  · rfl

/-- For the SAME explicit replay input, accepted event validity and explicit
policy authenticity determine the exact reconstructed successor. -/
theorem replay_step_exact {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (C : FiniteState m) (input : HistoryInput m)
    (authentic : input.Authentic E) {next : SharedAlias.State (interface m)}
    (step : SharedAlias.Step E (view C) input.event next) :
    view (replayUpdate D C input) = next := by
  cases input with
  | request => cases step; rfl
  | acknowledge i => cases step; exact acknowledgeUpdate_refines D E matchD C i
  | complete => cases step; exact completeUpdate_refines C
  | deliver i policy =>
      cases step
      change policy = E.source policy.epoch at authentic
      exact (congrArg (fun supplied => view (deliverUpdate D C i supplied)) authentic).trans
        (deliverUpdate_refines D E matchD C i policy.epoch)
  | prepare i k who time => cases step; exact prepareUpdate_refines D E matchD C i k
  | cancelAck i k who => cases step; exact cancelUpdate_refines D E matchD C i k
  | close k => cases step; rfl
  | land k who time => cases step; rfl
  | hold => cases step; rfl
  | corrupt i z =>
      cases step
      simp only [replayUpdate, view_setRoot, rootOf_matches D E matchD]

theorem replay_accepted_history_exact {m} (D : Routing m)
    (E : SharedAlias.Environment (interface m)) (matchD : RoutingMatches D E)
    (C : FiniteState m) (inputs : List (HistoryInput m))
    (authentic : ∀ input ∈ inputs, input.Authentic E)
    {next : SharedAlias.State (interface m)}
    (trace : SharedAlias.Trace E (view C) (inputs.map HistoryInput.event) next) :
    view (replayHistory D C inputs) = next := by
  induction inputs generalizing C with
  | nil => cases trace; rfl
  | cons input inputs ih =>
      cases trace with
      | cons first rest =>
          have projected := replay_step_exact D E matchD C input (authentic input (by simp)) first
          rw [← projected] at rest
          exact ih (replayUpdate D C input)
            (fun x member => authentic x (List.mem_cons_of_mem input member)) rest

/-- Every accepted primitive continuation of a represented state has an
explicit finite replay input and exactly represented full post-state. -/
theorem accepted_step_reifiable {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (C : FiniteState m) {event : OperationalJoin.Event (interface m)}
    {next : SharedAlias.State (interface m)} (step : SharedAlias.Step E (view C) event next) :
    ∃ input : HistoryInput m, input.event = event ∧ input.Authentic E ∧
      view (replayUpdate D C input) = next := by
  cases step with
  | request idle => exact ⟨.request, rfl, trivial, rfl⟩
  | acknowledge i pending =>
      exact ⟨.acknowledge i, rfl, trivial, acknowledgeUpdate_refines D E matchD C i⟩
  | complete pending quorum =>
      exact ⟨.complete, rfl, trivial, completeUpdate_refines C⟩
  | deliver i epoch certificate =>
      refine ⟨.deliver i (E.source epoch), ?_, ?_, deliverUpdate_refines D E matchD C i epoch⟩
      · simp only [HistoryInput.event, source_epoch_value]
      · change E.source epoch = E.source (E.source epoch).epoch
        rw [source_epoch_value]
  | prepare i k who time selected valid grant =>
      exact ⟨.prepare i k who time, rfl, trivial, prepareUpdate_refines D E matchD C i k⟩
  | cancelAck i k who selected auth =>
      exact ⟨.cancelAck i k who, rfl, trivial, cancelUpdate_refines D E matchD C i k⟩
  | close k certificate => exact ⟨.close k, rfl, trivial, rfl⟩
  | land k who time admitted => exact ⟨.land k who time, rfl, trivial, rfl⟩
  | hold => exact ⟨.hold, rfl, trivial, rfl⟩
  | corrupt i z bad =>
      refine ⟨.corrupt i (SharedAlias.Typed.rawRoot z), ?_, trivial, ?_⟩
      · simp only [HistoryInput.event, rootView_rawRoot]
      · simp only [replayUpdate, view_setRoot, rootView_rawRoot, rootOf_matches D E matchD]

/-- Finite accepted histories can be represented by finite sampled inputs
and replayed with a total executable update function. Existential choice of
raw memory lists is proof-side; the supplied replay inputs themselves are data. -/
theorem accepted_trace_reifiable {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (C : FiniteState m) {events : List (OperationalJoin.Event (interface m))}
    {next : SharedAlias.State (interface m)} (trace : SharedAlias.Trace E (view C) events next) :
    ∃ inputs : List (HistoryInput m), inputs.map HistoryInput.event = events ∧
      (∀ input ∈ inputs, input.Authentic E) ∧ view (replayHistory D C inputs) = next := by
  induction events generalizing C with
  | nil =>
      cases trace
      exact ⟨[], rfl, by simp, rfl⟩
  | cons event events ih =>
      cases trace with
      | cons step rest =>
          obtain ⟨input, same, authentic, projected⟩ := accepted_step_reifiable D E matchD C step
          rw [← projected] at rest
          obtain ⟨inputs, sameRest, authRest, final⟩ := ih (replayUpdate D C input) rest
          refine ⟨input :: inputs, ?_, ?_, final⟩
          · simp only [List.map_cons, same, sameRest]
          · intro x member
            rcases List.mem_cons.mp member with rfl | later
            · exact authentic
            · exact authRest x later

/-- The finite-support claim is restricted to reachable states. No arbitrary
function-valued state is claimed to admit finite empty-default tables. -/
theorem reachable_has_finite_representation {m} (D : Routing m)
    (E : SharedAlias.Environment (interface m)) (matchD : RoutingMatches D E)
    (C : SharedAlias.State (interface m)) (reachable : SharedAlias.Reachable E C) :
    ∃ native : FiniteState m, view native = C := by
  obtain ⟨p, events, trace⟩ := reachable
  rw [← initial_view E p] at trace
  obtain ⟨inputs, _, _, same⟩ := accepted_trace_reifiable D E matchD (initial (E.source 0) p) trace
  exact ⟨replayHistory D (initial (E.source 0) p) inputs, same⟩

end
end SharedAlias.Native
