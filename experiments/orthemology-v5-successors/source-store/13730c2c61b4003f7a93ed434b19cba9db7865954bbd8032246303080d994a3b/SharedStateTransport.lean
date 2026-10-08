import SelectedOrderTransport

namespace SharedAlias.OrderTransport
open OperationalJoin
open OperationalJoin.Typed (BoundedEnvelope interface path)
noncomputable section
open Classical

-- Match the abstract accepted interface's classical command-key operations.
local instance {m} : DecidableEq (BoundedEnvelope m) := Classical.decEq _

@[simp] theorem command_command {m} (T : Symmetry m) (k : BoundedEnvelope m) :
    T.command (T.command k) = k := T.involutive k

@[simp] theorem command_eq_command {m} (T : Symmetry m) (a b : BoundedEnvelope m) :
    T.command a = T.command b ↔ a = b := T.involutive.injective.eq_iff

/-- Finite preimage of membership, represented by the involution's image. -/
def memory {m} (T : Symmetry m) (ks : Finset (BoundedEnvelope m)) := ks.image T.command

@[simp] theorem mem_memory_command {m} (T : Symmetry m)
    (ks : Finset (BoundedEnvelope m)) (k : BoundedEnvelope m) :
    T.command k ∈ memory T ks ↔ k ∈ ks := by
  simp [memory, Finset.mem_image]

@[simp] theorem mem_memory {m} (T : Symmetry m)
    (ks : Finset (BoundedEnvelope m)) (k : BoundedEnvelope m) :
    k ∈ memory T ks ↔ T.command k ∈ ks := by
  simpa only [command_command] using mem_memory_command T ks (T.command k)

@[simp] theorem memory_memory {m} (T : Symmetry m) (ks : Finset (BoundedEnvelope m)) :
    memory T (memory T ks) = ks := by ext k; simp only [mem_memory, command_command]

@[simp] theorem memory_insert {m} (T : Symmetry m)
    (ks : Finset (BoundedEnvelope m)) (k : BoundedEnvelope m) :
    memory T (insert k ks) = insert (T.command k) (memory T ks) := Finset.image_insert T.command k ks

@[simp] theorem memory_empty {m} (T : Symmetry m) : memory T ∅ = ∅ := Finset.image_empty T.command

def root {m} (T : Symmetry m) (z : RootState (interface m)) : RootState (interface m) :=
  { z with commitments := memory T z.commitments, cancelled := memory T z.cancelled }

def state {m} (T : Symmetry m) (C : SharedAlias.State (interface m)) : SharedAlias.State (interface m) :=
  { C with roots := fun r => root T (C.roots r), cancelAcks := fun k => C.cancelAcks (T.command k) }

def event {m} (T : Symmetry m) : Event (interface m) → Event (interface m)
  | .prepare i k who time => .prepare i (T.command k) who time
  | .cancelAck i k who => .cancelAck i (T.command k) who
  | .close k => .close (T.command k)
  | .land k who time => .land (T.command k) who time
  | .corrupt i z => .corrupt i (root T z)
  | .request => .request
  | .acknowledge i => .acknowledge i
  | .complete => .complete
  | .deliver i e => .deliver i e
  | .hold => .hold

@[simp] theorem root_involutive {m} (T : Symmetry m) (z : RootState (interface m)) :
    root T (root T z) = z := by cases z; simp [root]

@[simp] theorem state_involutive {m} (T : Symmetry m) (C : SharedAlias.State (interface m)) :
    state T (state T C) = C := by cases C; simp [state]

@[simp] theorem event_involutive {m} (T : Symmetry m) (e : Event (interface m)) :
    event T (event T e) = e := by cases e <;> simp [event]

@[simp] theorem state_initial {m} (T : Symmetry m)
    (E : Environment (interface m)) (p : ComposedExecution.Plant) :
    state T (initial E p) = initial E p := by simp [state, root, initial, memory]

@[simp] theorem state_receipts {m} (T : Symmetry m)
    (C : SharedAlias.State (interface m)) (k : BoundedEnvelope m) :
    (state T C).cancelAcks (T.command k) = C.cancelAcks k := by simp [state]

@[simp] theorem admits_iff {m} (T : Symmetry m) (p : ComposedExecution.Plant)
    (time : Nat) (d : ComposedExecution.Policy) (k : BoundedEnvelope m) (who : String) :
    (interface m).admits p time d (T.command k) who ↔ (interface m).admits p time d k who := by
  simp only [interface, T.action, T.successor]

@[simp] theorem envelope_iff {m} (T : Symmetry m) (p : ComposedExecution.Plant)
    (time : Nat) (z : RootState (interface m)) (k : BoundedEnvelope m) (who : String) :
    Envelope p time (root T z) (T.command k) who ↔ Envelope p time z k who := by
  simp only [Envelope, root, admits_iff, interface, T.action, T.successor, mem_memory_command]

@[simp] theorem permits_iff {m} (T : Symmetry m) (p : ComposedExecution.Plant)
    (time : Nat) (z : RootState (interface m)) (k : BoundedEnvelope m) (who : String) :
    Permits p time (root T z) (T.command k) who ↔ Permits p time z k who := by
  change (T.command k ∈ memory T z.commitments ∧ _) ↔ _
  rw [mem_memory_command, envelope_iff]

@[simp] theorem valid_iff {m} (T : Symmetry m) (E : Environment (interface m))
    (k : BoundedEnvelope m) : ValidPath E.labelConfig (T.command k) ↔ ValidPath E.labelConfig k := by
  simp only [ValidPath, interface, T.support]

@[simp] theorem lands_iff {m} (T : Symmetry m) (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (time : Nat) (k : BoundedEnvelope m) (who : String) :
    SharedAlias.Lands E (state T C) time (T.command k) who ↔ SharedAlias.Lands E C time k who := by
  change (ValidPath E.labelConfig (T.command k) ∧
    ∀ i ∈ path (T.command k), Good E.labelConfig i →
      Permits C.plant time (root T (C.roots (E.rootOf i))) (T.command k) who) ↔ _
  rw [valid_iff, T.support]
  simp only [permits_iff]
  rfl

theorem state_setRoot {m} (T : Symmetry m) (C : SharedAlias.State (interface m))
    (r : Option (Fin m)) (z : RootState (interface m)) :
    state T (SharedAlias.setRoot C r z) = SharedAlias.setRoot (state T C) r (root T z) := by
  unfold state SharedAlias.setRoot
  congr 1
  funext s
  simp only [Function.update_apply]
  split_ifs <;> rfl

@[simp] theorem state_prepare {m} (T : Symmetry m) (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (i : Fin m) (k : BoundedEnvelope m) :
    state T (SharedAlias.prepare E C i k) = SharedAlias.prepare E (state T C) i (T.command k) := by
  unfold SharedAlias.prepare
  rw [state_setRoot]
  congr 1
  simp only [state, root, memory, Finset.image_insert]

theorem state_cancelAck {m} (T : Symmetry m) (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (i : Fin m) (k : BoundedEnvelope m) :
    state T (SharedAlias.cancelAck E C i k) = SharedAlias.cancelAck E (state T C) i (T.command k) := by
  have receipts : (fun x => Function.update C.cancelAcks k (insert i (C.cancelAcks k)) (T.command x)) =
      Function.update (fun x => C.cancelAcks (T.command x)) (T.command k) (insert i (C.cancelAcks k)) := by
    funext x
    have eq : T.command x = k ↔ x = T.command k := by
      constructor
      · intro h; have h' := congrArg T.command h; simpa only [command_command] using h'
      · intro h; rw [h, command_command]
    simp only [Function.update_apply, eq]
  by_cases good : Good E.labelConfig i
  · simp only [SharedAlias.cancelAck, state, if_pos good, command_command]
    congr 1
    · funext r
      simp only [Function.update_apply]
      split_ifs <;> simp only [root, memory, Finset.image_insert]
  · simp only [SharedAlias.cancelAck, state, if_neg good, command_command]
    congr 1

@[simp] theorem state_land {m} (T : Symmetry m) (C : SharedAlias.State (interface m))
    (k : BoundedEnvelope m) : state T (SharedAlias.land C k) = SharedAlias.land (state T C) (T.command k) := by
  simp only [state, SharedAlias.land, interface, T.successor]

@[simp] theorem state_request {m} (T : Symmetry m) (C : SharedAlias.State (interface m)) :
    state T (SharedAlias.request C) = SharedAlias.request (state T C) := rfl

@[simp] theorem state_complete {m} (T : Symmetry m) (C : SharedAlias.State (interface m)) :
    state T (SharedAlias.complete C) = SharedAlias.complete (state T C) := rfl

theorem state_acknowledge {m} (T : Symmetry m) (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (i : Fin m) :
    state T (SharedAlias.acknowledge E C i) = SharedAlias.acknowledge E (state T C) i := by
  by_cases good : Good E.labelConfig i
  · simp only [SharedAlias.acknowledge, state, if_pos good]
    congr 1
    funext r
    simp only [Function.update_apply]
    split_ifs <;> rfl
  · simp only [SharedAlias.acknowledge, state, if_neg good]

theorem state_deliver {m} (T : Symmetry m) (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (i : Fin m) (e : Nat) :
    state T (SharedAlias.deliver E C i e) = SharedAlias.deliver E (state T C) i e := by
  unfold SharedAlias.deliver
  change state T (if _ then _ else _) = if (interface m).policyEpoch (C.roots (E.rootOf i)).descriptor < e then _ else _
  split_ifs
  · rw [state_setRoot]; rfl
  · rfl

end
end SharedAlias.OrderTransport
