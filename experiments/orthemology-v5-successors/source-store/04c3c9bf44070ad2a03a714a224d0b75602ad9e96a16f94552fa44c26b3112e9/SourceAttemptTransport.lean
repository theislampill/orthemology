import SharedTraceTransport

namespace SharedAlias.OrderTransport
open OperationalJoin
open OperationalJoin.Typed (BoundedEnvelope interface path)
noncomputable section
open Classical

theorem command_path_perm {m} (T : Symmetry m) (k : BoundedEnvelope m) :
    (T.command k).val.path.Perm k.val.path := by
  have h := command_perm_old (T.command k)
  rw [T.support] at h
  exact h.trans (command_perm_old k).symm

theorem raw_rootPermits_eq {m} (T : Symmetry m) (p : ComposedExecution.Plant)
    (time : Nat) (z : RootState (interface m)) (k : BoundedEnvelope m) (who : String) :
    ComposedExecution.rootPermits p time (SharedAlias.Typed.rawRoot (root T z)) (T.command k).val who =
      ComposedExecution.rootPermits p time (SharedAlias.Typed.rawRoot z) k.val who := by
  apply Bool.eq_iff_iff.mpr
  exact (OperationalJoin.Typed.root_gate_iff p time _ _
      (SharedAlias.Typed.rawRoot_represents (root T z)) (T.command k) who).symm.trans
    ((permits_iff T p time z k who).trans
      (OperationalJoin.Typed.root_gate_iff p time _ _ (SharedAlias.Typed.rawRoot_represents z) k who))

theorem gateOpen_eq {m} (T : Symmetry m) (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (k : BoundedEnvelope m)
    (who : String) (time : Nat) (badOpen : Bool) (j : Nat) (bound : j < m) :
    ComposedExecution.gateOpen (SharedAlias.Typed.gateWorld E (state T C) time)
        (T.command k).val who badOpen j =
      ComposedExecution.gateOpen (SharedAlias.Typed.gateWorld E C time) k.val who badOpen j := by
  simp only [ComposedExecution.gateOpen, SharedAlias.Typed.gateWorld, dif_pos bound]
  split
  · rfl
  · exact raw_rootPermits_eq T C.plant time (C.roots (E.rootOf ⟨j,bound⟩)) k who

theorem source_validPath_eq {m} (T : Symmetry m) (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (k : BoundedEnvelope m) (time : Nat) :
    ComposedExecution.validPath (SharedAlias.Typed.gateWorld E (state T C) time) (T.command k).val =
      ComposedExecution.validPath (SharedAlias.Typed.gateWorld E C time) k.val := by
  apply Bool.eq_iff_iff.mpr
  exact (OperationalJoin.Typed.valid_path_iff E.labelConfig _ rfl rfl (T.command k)).symm.trans
    ((valid_iff T E k).trans (OperationalJoin.Typed.valid_path_iff E.labelConfig _ rfl rfl k))

/-- The SAME badOpen is preserved, including the false/withholding branch. -/
theorem applied_eq {m} (T : Symmetry m) (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (k : BoundedEnvelope m)
    (who : String) (time : Nat) (badOpen : Bool) :
    SharedAlias.Progress.applied E (state T C) (T.command k) who time badOpen =
      SharedAlias.Progress.applied E C k who time badOpen := by
  have allEq : (T.command k).val.path.all
      (ComposedExecution.gateOpen (SharedAlias.Typed.gateWorld E (state T C) time) (T.command k).val who badOpen) =
      k.val.path.all (ComposedExecution.gateOpen (SharedAlias.Typed.gateWorld E C time) k.val who badOpen) := by
    apply Bool.eq_iff_iff.mpr
    simp only [List.all_eq_true]
    constructor
    · intro h j hj
      have h' := h j ((command_path_perm T k).mem_iff.mpr hj)
      rwa [gateOpen_eq T E C k who time badOpen j (k.property.2 j hj)] at h'
    · intro h j hj
      have old := (command_path_perm T k).mem_iff.mp hj
      rw [gateOpen_eq T E C k who time badOpen j (k.property.2 j old)]
      exact h j old
  simp only [SharedAlias.Progress.applied, ComposedExecution.attempt,
    source_validPath_eq T E C k time, allEq]
  split <;> rfl

theorem attemptSlot_eq {m} (T : Symmetry m) (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (k : BoundedEnvelope m)
    (who : String) (time : Nat) (badOpen : Bool) :
    state T (SharedAlias.Progress.attemptSlot E C k who time badOpen) =
      SharedAlias.Progress.attemptSlot E (state T C) (T.command k) who time badOpen := by
  simp only [SharedAlias.Progress.attemptSlot, applied_eq]
  split <;> simp only [state_land]

end
end SharedAlias.OrderTransport
