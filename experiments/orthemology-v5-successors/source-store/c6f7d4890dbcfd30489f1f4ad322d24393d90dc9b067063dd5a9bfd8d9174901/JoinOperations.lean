import JoinTrace
namespace OperationalJoin
noncomputable section
open Classical

@[simp] theorem prepare_plant {n} {I : Interface n} (s : State I) (i : Fin n) (k : I.Command) :
    (prepare s i k).plant = s.plant := rfl
@[simp] theorem prepare_epoch {n} {I : Interface n} (s : State I) (i : Fin n) (k : I.Command) :
    (prepare s i k).epoch = s.epoch := rfl
@[simp] theorem prepare_damaged {n} {I : Interface n} (s : State I) (i : Fin n) (k : I.Command) :
    (prepare s i k).damaged = s.damaged := rfl
@[simp] theorem prepare_envelope {n} {I : Interface n} (s : State I) (i j : Fin n)
    (k k' : I.Command) (requester : I.Requester) (time : Nat) :
    Envelope (prepare s i k).plant time ((prepare s i k).roots j) k' requester ↔
      Envelope s.plant time (s.roots j) k' requester := by
  by_cases eq : j = i <;> simp [Envelope, prepare, setRoot, Function.update_apply, eq]

@[simp] theorem deliver_plant {n} {I : Interface n} (c : Config I) (s : State I) (i : Fin n) (e : Nat) :
    (deliver c s i e).plant = s.plant := by unfold deliver; split <;> rfl
@[simp] theorem deliver_epoch {n} {I : Interface n} (c : Config I) (s : State I) (i : Fin n) (e : Nat) :
    (deliver c s i e).epoch = s.epoch := by unfold deliver; split <;> rfl
@[simp] theorem deliver_damaged {n} {I : Interface n} (c : Config I) (s : State I) (i : Fin n) (e : Nat) :
    (deliver c s i e).damaged = s.damaged := by unfold deliver; split <;> rfl
@[simp] theorem land_epoch {n} {I : Interface n} (c : Config I) (s : State I) (time : Nat)
    (k : I.Command) (requester : I.Requester) :
    (land c s time k requester).epoch = s.epoch := by unfold land; split <;> rfl
@[simp] theorem land_pending {n} {I : Interface n} (c : Config I) (s : State I) (time : Nat)
    (k : I.Command) (requester : I.Requester) :
    (land c s time k requester).pending = s.pending := by unfold land; split <;> rfl

end
end OperationalJoin
