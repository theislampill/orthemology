import JoinOperations
namespace OperationalJoin
noncomputable section
open Classical

def prepareMany {n} {I : Interface n} (k : I.Command) : State I → List (Fin n) → State I
  | s, [] => s
  | s, i :: is => prepareMany k (prepare s i k) is

@[simp] theorem prepareMany_epoch {n} {I : Interface n} (k : I.Command)
    (s : State I) (is : List (Fin n)) : (prepareMany k s is).epoch = s.epoch := by
  induction is generalizing s with
  | nil => rfl
  | cons i is ih => simp [prepareMany, ih]
@[simp] theorem prepareMany_plant {n} {I : Interface n} (k : I.Command)
    (s : State I) (is : List (Fin n)) : (prepareMany k s is).plant = s.plant := by
  induction is generalizing s with
  | nil => rfl
  | cons i is ih => simp [prepareMany, ih]
@[simp] theorem prepareMany_pending {n} {I : Interface n} (k : I.Command)
    (s : State I) (is : List (Fin n)) : (prepareMany k s is).pending = s.pending := by
  induction is generalizing s with
  | nil => rfl
  | cons i is ih => simpa [prepareMany, prepare, setRoot] using ih (prepare s i k)
@[simp] theorem prepareMany_damaged {n} {I : Interface n} (k : I.Command)
    (s : State I) (is : List (Fin n)) : (prepareMany k s is).damaged = s.damaged := by
  induction is generalizing s with
  | nil => rfl
  | cons i is ih => simp [prepareMany, ih]
@[simp] theorem prepareMany_certificates {n} {I : Interface n} (k : I.Command)
    (s : State I) (is : List (Fin n)) : (prepareMany k s is).certificates = s.certificates := by
  induction is generalizing s with
  | nil => rfl
  | cons i is ih => simpa [prepareMany, prepare, setRoot] using ih (prepare s i k)
@[simp] theorem prepareMany_cancelAcks {n} {I : Interface n} (k : I.Command)
    (s : State I) (is : List (Fin n)) : (prepareMany k s is).cancelAcks = s.cancelAcks := by
  induction is generalizing s with
  | nil => rfl
  | cons i is ih => simpa [prepareMany, prepare, setRoot] using ih (prepare s i k)

theorem prepareMany_root {n} {I : Interface n} (k : I.Command)
    (s : State I) (is : List (Fin n)) (j : Fin n) :
    (prepareMany k s is).roots j =
      if j ∈ is then { s.roots j with commitments := insert k (s.roots j).commitments }
      else s.roots j := by
  induction is generalizing s with
  | nil => simp [prepareMany]
  | cons i is ih =>
      simp only [prepareMany, ih, prepare, setRoot, List.mem_cons]
      by_cases same : j = i <;> by_cases member : j ∈ is <;>
        simp_all [Function.update_apply]

theorem prepareMany_trace {n} {I : Interface n} (c : Config I) (s : State I)
    (is : List (Fin n)) (k : I.Command) (requester : I.Requester) (time : Nat)
    (path : ValidPath c k)
    (selected : ∀ i ∈ is, i ∈ I.commandPath k)
    (grants : ∀ i ∈ is, i ∈ c.faulty ∨ Envelope s.plant time (s.roots i) k requester) :
    Trace c s (is.map (fun i => Event.prepare i k requester time)) (prepareMany k s is) := by
  induction is generalizing s with
  | nil => exact .nil _
  | cons i is ih =>
      apply Trace.cons (Step.prepare s i k requester time
        (selected i (List.mem_cons_self)) path (grants i (List.mem_cons_self)))
      apply ih (prepare s i k)
      · intro j member
        exact selected j (List.mem_cons_of_mem i member)
      · intro j member
        rcases grants j (List.mem_cons_of_mem i member) with bad | ready
        · exact Or.inl bad
        · exact Or.inr ((prepare_envelope s i j k k requester time).mpr ready)

end
end OperationalJoin
