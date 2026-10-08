import NativePrimitives
import SharedService

namespace SharedAlias.Native
open ComposedExecution
open OperationalJoin.Typed (BoundedEnvelope interface rootView)

noncomputable section
open Classical

theorem view_setRoot {m} (C : FiniteState m) (r : Option (Fin m)) (z : Root) :
    view (setRoot C r z) = SharedAlias.setRoot (view C) r (rootView z) := by
  unfold view setRoot SharedAlias.setRoot rootAt
  congr 1
  funext s
  by_cases same : s = r
  · subst s; simp [tableRead]
  · simp [tableRead, same, Function.update_of_ne]

theorem rootView_commit {m} (z : Root) (k : BoundedEnvelope m) :
    rootView { z with commitments := k.val :: z.commitments } =
      { rootView (n := m) z with commitments := insert k (rootView z).commitments } := by
  unfold rootView
  congr 1
  ext e
  simp only [OperationalJoin.Typed.mem_memory, List.mem_cons, Finset.mem_insert]
  exact or_congr (Subtype.val_injective.eq_iff) Iff.rfl

theorem rootView_cancel {m} (z : Root) (k : BoundedEnvelope m) :
    rootView { z with cancelled := k.val :: z.cancelled } =
      { rootView (n := m) z with cancelled := insert k (rootView z).cancelled } := by
  unfold rootView
  congr 1
  ext e
  simp only [OperationalJoin.Typed.mem_memory, List.mem_cons, Finset.mem_insert]
  exact or_congr (Subtype.val_injective.eq_iff) Iff.rfl

theorem eligible_iff {m} (p : Plant) (time : Nat) (z : Root)
    (k : BoundedEnvelope m) (who : String) :
    ComposedExecution.Eligible p time z k.val who ↔
      OperationalJoin.Envelope p time (rootView z) k who := by
  simp only [ComposedExecution.Eligible, OperationalJoin.Envelope, interface, rootView,
    List.mem_toFinset, OperationalJoin.Typed.mem_memory]
  tauto

theorem prepareUpdate_refines {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (C : FiniteState m) (i : Fin m) (k : BoundedEnvelope m) :
    view (prepareUpdate D C i k) = SharedAlias.prepare E (view C) i k := by
  unfold prepareUpdate
  rw [view_setRoot, rootView_commit, rootOf_matches D E matchD]
  rfl

theorem prepareAllowed_iff {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (C : FiniteState m) (i : Fin m)
    (k : BoundedEnvelope m) (who : String) (time : Nat) (badReply : Bool) :
    prepareAllowed D C i k who time badReply = true ↔
      SharedAlias.Progress.prepareAllowed E (view C) i k who time badReply := by
  have valid := OperationalJoin.Typed.valid_path_iff E.labelConfig
    (gateWorld D C time C.defaultRoot.policy) rfl matchD.quorum k
  by_cases good : OperationalJoin.Good E.labelConfig i
  · have hbad := (faulty_false_iff D E matchD i).mpr good
    simp only [prepareAllowed, hbad, Bool.false_eq_true, if_false, Bool.and_eq_true,
      decide_eq_true_eq, ← valid, SharedAlias.Progress.prepareAllowed, if_pos good,
      interface, OperationalJoin.Typed.mem_path, eligible_iff, rootOf_matches D E matchD, view, and_assoc]
  · have hbad : faulty D i = true := by
      cases h : faulty D i with
      | true => rfl
      | false => exact False.elim (good ((faulty_false_iff D E matchD i).mp h))
    simp only [prepareAllowed, hbad, if_true, Bool.and_eq_true,
      decide_eq_true_eq, ← valid, SharedAlias.Progress.prepareAllowed, if_neg good,
      interface, OperationalJoin.Typed.mem_path, and_assoc]

theorem prepare_refines {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (C : FiniteState m) (i : Fin m)
    (k : BoundedEnvelope m) (who : String) (time : Nat) (badReply : Bool) :
    view (prepareSlot D C i k who time badReply) =
      SharedAlias.Progress.prepareSlot E (view C) i k who time badReply := by
  by_cases h : prepareAllowed D C i k who time badReply = true
  · have href := (prepareAllowed_iff D E matchD C i k who time badReply).mp h
    simpa only [prepareSlot, SharedAlias.Progress.prepareSlot, if_pos h, if_pos href] using
      prepareUpdate_refines D E matchD C i k
  · have href : ¬SharedAlias.Progress.prepareAllowed E (view C) i k who time badReply :=
      fun yes => h ((prepareAllowed_iff D E matchD C i k who time badReply).mpr yes)
    simp only [prepareSlot, SharedAlias.Progress.prepareSlot, if_neg h, if_neg href]

/-- Native good/bad receipt branches match the accepted single-label update. -/
theorem cancelUpdate_refines {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (C : FiniteState m) (i : Fin m) (k : BoundedEnvelope m) :
    view (cancelUpdate D C i k) = SharedAlias.cancelAck E (view C) i k := by
  by_cases good : OperationalJoin.Good E.labelConfig i
  · have hbad := (faulty_false_iff D E matchD i).mpr good
    simp only [cancelUpdate, hbad, Bool.false_eq_true, if_false]
    rw [view_setRoot, rootView_cancel, rootOf_matches D E matchD]
    unfold SharedAlias.cancelAck SharedAlias.setRoot view receipts rootAt
    simp only [if_pos good]
    congr 1
    funext e
    by_cases same : e = k
    · subst e; simp [tableRead]
    · have rawNe : e.val ≠ k.val := fun eq => same (Subtype.ext eq)
      simp [tableRead, rawNe, Function.update_of_ne same]
  · have hbad : faulty D i = true := by
      cases h : faulty D i with
      | true => rfl
      | false => exact False.elim (good ((faulty_false_iff D E matchD i).mp h))
    simp only [cancelUpdate, hbad, if_true, SharedAlias.cancelAck, if_neg good]
    unfold view receipts
    congr 1
    funext e
    by_cases same : e = k
    · subst e; simp [tableRead]
    · have rawNe : e.val ≠ k.val := fun eq => same (Subtype.ext eq)
      simp [tableRead, rawNe, Function.update_of_ne same]

theorem cancelAllowed_iff {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (i : Fin m) (k : BoundedEnvelope m) (who : String) (badReply : Bool) :
    cancelAllowed D i k who badReply = true ↔
      SharedAlias.Progress.cancelAllowed E i k who badReply := by
  by_cases good : OperationalJoin.Good E.labelConfig i
  · have hbad := (faulty_false_iff D E matchD i).mpr good
    simp only [cancelAllowed, hbad, Bool.false_eq_true, if_false, Bool.and_eq_true,
      decide_eq_true_eq, SharedAlias.Progress.cancelAllowed, if_pos good,
      interface, OperationalJoin.Typed.mem_path]
  · have hbad : faulty D i = true := by
      cases h : faulty D i with
      | true => rfl
      | false => exact False.elim (good ((faulty_false_iff D E matchD i).mp h))
    simp only [cancelAllowed, hbad, if_true, Bool.and_eq_true,
      decide_eq_true_eq, SharedAlias.Progress.cancelAllowed, if_neg good,
      interface, OperationalJoin.Typed.mem_path]

theorem cancel_refines {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (C : FiniteState m) (i : Fin m)
    (k : BoundedEnvelope m) (who : String) (badReply : Bool) :
    view (cancelSlot D C i k who badReply) =
      SharedAlias.Progress.cancelSlot E (view C) i k who badReply := by
  by_cases h : cancelAllowed D i k who badReply = true
  · have href := (cancelAllowed_iff D E matchD i k who badReply).mp h
    simpa only [cancelSlot, SharedAlias.Progress.cancelSlot, if_pos h, if_pos href] using
      cancelUpdate_refines D E matchD C i k
  · have href : ¬SharedAlias.Progress.cancelAllowed E i k who badReply :=
      fun yes => h ((cancelAllowed_iff D E matchD i k who badReply).mpr yes)
    simp only [cancelSlot, SharedAlias.Progress.cancelSlot, if_neg h, if_neg href]

theorem successful_native_attempt_lands {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (C : FiniteState m) (k : BoundedEnvelope m)
    (who : String) (time : Nat) (badOpen : Bool) (success : applied D C k who time badOpen = true) :
    SharedAlias.Lands E (view C) time k who := by
  exact OperationalJoin.Typed.successful_attempt_lands
    (gateWorld D C time C.defaultRoot.policy) (SharedAlias.Typed.literalSnapshot E (view C))
    (gateWorld_represents D E matchD C time C.defaultRoot.policy) k who badOpen success

theorem attempt_success_refines {m} (D : Routing m) (C : FiniteState m)
    (k : BoundedEnvelope m) (who : String) (time : Nat) (badOpen : Bool)
    (success : applied D C k who time badOpen = true) :
    view (attemptSlot D C k who time badOpen) = SharedAlias.land (view C) k := by
  have effect := ComposedExecution.applied_attempt_exact_successor
    (gateWorld D C time C.defaultRoot.policy) k.val who badOpen success
  dsimp only [attemptSlot]
  rw [show (ComposedExecution.attempt (gateWorld D C time C.defaultRoot.policy) k.val who badOpen).2 = true from success]
  simp only [if_true]
  rw [effect]
  rfl

/-- The exact successful source effect or exact complete-state identity. -/
theorem attempt_refines {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (C : FiniteState m) (k : BoundedEnvelope m)
    (who : String) (time : Nat) (badOpen : Bool) :
    ∃ event, SharedAlias.Step E (view C) event (view (attemptSlot D C k who time badOpen)) := by
  cases h : applied D C k who time badOpen with
  | true =>
      refine ⟨.land k who time, ?_⟩
      rw [attempt_success_refines D C k who time badOpen h]
      exact .land (view C) k who time (successful_native_attempt_lands D E matchD C k who time badOpen h)
  | false =>
      refine ⟨.hold, ?_⟩
      have identity : attemptSlot D C k who time badOpen = C := by
        dsimp only [attemptSlot]
        rw [show (ComposedExecution.attempt (gateWorld D C time C.defaultRoot.policy) k.val who badOpen).2 = false from h]
        rfl
      rw [identity]
      exact .hold _

theorem closed_iff {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (C : FiniteState m) (k : BoundedEnvelope m) :
    closed D C k = true ↔ E.labelBudget < ((view C).cancelAcks k).card := by
  simp only [closed, decide_eq_true_eq, view, matchD.budget]


/-- A single emitted prepare/hold is an accepted actual shared-store step. -/
theorem prepare_emitted_step {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (C : FiniteState m) (i : Fin m)
    (k : BoundedEnvelope m) (who : String) (time : Nat) (badReply : Bool) :
    SharedAlias.Step E (view C) (prepareEvent D C i k who time badReply)
      (view (prepareSlot D C i k who time badReply)) := by
  by_cases h : prepareAllowed D C i k who time badReply = true
  · have allowed := (prepareAllowed_iff D E matchD C i k who time badReply).mp h
    simp only [prepareEvent, prepareSlot, if_pos h]
    rw [prepareUpdate_refines D E matchD]
    apply SharedAlias.Step.prepare (E := E) (view C) i k who time allowed.1 allowed.2.1
    by_cases good : OperationalJoin.Good E.labelConfig i
    · exact Or.inr (by simpa only [if_pos good] using allowed.2.2)
    · exact Or.inl (not_not.mp good)
  · simp only [prepareEvent, prepareSlot, if_neg h]
    exact .hold _

theorem cancel_emitted_step {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (C : FiniteState m) (i : Fin m)
    (k : BoundedEnvelope m) (who : String) (badReply : Bool) :
    SharedAlias.Step E (view C) (cancelEvent D i k who badReply)
      (view (cancelSlot D C i k who badReply)) := by
  by_cases h : cancelAllowed D i k who badReply = true
  · have allowed := (cancelAllowed_iff D E matchD i k who badReply).mp h
    simp only [cancelEvent, cancelSlot, if_pos h]
    rw [cancelUpdate_refines D E matchD]
    apply SharedAlias.Step.cancelAck (E := E) (view C) i k who allowed.1
    by_cases good : OperationalJoin.Good E.labelConfig i
    · exact Or.inr (by simpa only [if_pos good] using allowed.2)
    · exact Or.inl (not_not.mp good)
  · simp only [cancelEvent, cancelSlot, if_neg h]
    exact .hold _

theorem attempt_emitted_step {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (C : FiniteState m) (k : BoundedEnvelope m)
    (who : String) (time : Nat) (badOpen : Bool) :
    SharedAlias.Step E (view C) (attemptEvent D C k who time badOpen)
      (view (attemptSlot D C k who time badOpen)) := by
  cases h : applied D C k who time badOpen with
  | true =>
      simp only [attemptEvent, h, if_true]
      rw [attempt_success_refines D C k who time badOpen h]
      exact SharedAlias.Step.land (E := E) (view C) k who time (successful_native_attempt_lands D E matchD C k who time badOpen h)
  | false =>
      simp only [attemptEvent, h, Bool.false_eq_true, if_false, rejected_identity D C k who time badOpen h]
      exact .hold _

theorem close_emitted_step {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (C : FiniteState m) (k : BoundedEnvelope m) :
    SharedAlias.Step E (view C) (closeEvent D C k) (view C) := by
  by_cases h : closed D C k = true
  · simp only [closeEvent, if_pos h]
    exact SharedAlias.Step.close (E := E) (view C) k ((closed_iff D E matchD C k).mp h)
  · simp only [closeEvent, if_neg h]
    exact .hold _

/-- Authentication is derived from an accepted reached history, not from
native gateWorld.effectivePolicy or an arbitrary supplied policy. -/
theorem native_success_full_effect {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (C : FiniteState m) (k : BoundedEnvelope m)
    (reach : SharedAlias.Reachable E (view C)) (who : String) (time : Nat) (badOpen : Bool)
    (success : applied D C k who time badOpen = true) :
    ComposedExecution.localStep C.plant (E.source C.epoch) time k.val.action = some k.val.successor ∧
      (attemptSlot D C k who time badOpen).plant = k.val.successor := by
  have lands := successful_native_attempt_lands D E matchD C k who time badOpen success
  have auth := SharedAlias.Typed.finite_history_admission reach time k who lands
  have effect := congrArg SharedAlias.State.plant (attempt_success_refines D C k who time badOpen success)
  exact ⟨auth.2.2, effect⟩

end
end SharedAlias.Native
