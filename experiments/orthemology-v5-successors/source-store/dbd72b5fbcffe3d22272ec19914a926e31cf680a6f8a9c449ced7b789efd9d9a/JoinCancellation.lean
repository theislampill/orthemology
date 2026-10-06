import JoinOperations
namespace OperationalJoin
noncomputable section
open Classical

def cancelMany {n} {I : Interface n} (c : Config I) (k : I.Command) : State I → List (Fin n) → State I
  | s, [] => s
  | s, i :: is => cancelMany c k (cancelAck c s i k) is

@[simp] theorem cancelMany_epoch {n} {I : Interface n} (c : Config I) (k : I.Command)
    (s : State I) (is : List (Fin n)) : (cancelMany c k s is).epoch = s.epoch := by
  induction is generalizing s with
  | nil => rfl
  | cons i is ih => simpa [cancelMany, cancelAck] using ih (cancelAck c s i k)
@[simp] theorem cancelMany_plant {n} {I : Interface n} (c : Config I) (k : I.Command)
    (s : State I) (is : List (Fin n)) : (cancelMany c k s is).plant = s.plant := by
  induction is generalizing s with
  | nil => rfl
  | cons i is ih => simpa [cancelMany, cancelAck] using ih (cancelAck c s i k)
@[simp] theorem cancelMany_pending {n} {I : Interface n} (c : Config I) (k : I.Command)
    (s : State I) (is : List (Fin n)) : (cancelMany c k s is).pending = s.pending := by
  induction is generalizing s with
  | nil => rfl
  | cons i is ih => simpa [cancelMany, cancelAck] using ih (cancelAck c s i k)
@[simp] theorem cancelMany_damaged {n} {I : Interface n} (c : Config I) (k : I.Command)
    (s : State I) (is : List (Fin n)) : (cancelMany c k s is).damaged = s.damaged := by
  induction is generalizing s with
  | nil => rfl
  | cons i is ih => simpa [cancelMany, cancelAck] using ih (cancelAck c s i k)
@[simp] theorem cancelMany_certificates {n} {I : Interface n} (c : Config I) (k : I.Command)
    (s : State I) (is : List (Fin n)) : (cancelMany c k s is).certificates = s.certificates := by
  induction is generalizing s with
  | nil => rfl
  | cons i is ih => simpa [cancelMany, cancelAck] using ih (cancelAck c s i k)

theorem cancelMany_root {n} {I : Interface n} (c : Config I) (k : I.Command)
    (s : State I) (is : List (Fin n)) (j : Fin n) :
    (cancelMany c k s is).roots j =
      if Good c j ∧ j ∈ is then
        { s.roots j with cancelled := insert k (s.roots j).cancelled }
      else s.roots j := by
  induction is generalizing s with
  | nil => simp [cancelMany]
  | cons i is ih =>
      simp only [cancelMany, ih, cancelAck, List.mem_cons]
      by_cases goodJ : Good c j <;> by_cases goodI : Good c i <;>
        by_cases same : j = i <;> by_cases member : j ∈ is <;>
        simp_all [Function.update_apply]

/-- Acknowledgements accumulate by distinct root, including across calls. -/
theorem cancelMany_cancelAcks {n} {I : Interface n} (c : Config I) (k : I.Command)
    (s : State I) (is : List (Fin n)) (other : I.Command) :
    (cancelMany c k s is).cancelAcks other =
      if other = k then is.toFinset ∪ s.cancelAcks other else s.cancelAcks other := by
  induction is generalizing s with
  | nil => simp [cancelMany]
  | cons i is ih =>
      simp only [cancelMany, ih, cancelAck, List.toFinset_cons]
      by_cases same : other = k
      · subst other
        simp only [if_pos rfl, if_true, Function.update_self]
        ext j
        simp only [Finset.mem_union, Finset.mem_insert]
        tauto
      · simp [same, Function.update_of_ne same]

theorem cancelMany_trace {n} {I : Interface n} (c : Config I) (s : State I)
    (is : List (Fin n)) (k : I.Command) (requester : I.Requester)
    (selected : ∀ i ∈ is, i ∈ I.commandPath k)
    (auth : ∀ i ∈ is, i ∈ c.faulty ∨ requester = I.recipient k) :
    Trace c s (is.map (fun i => Event.cancelAck i k requester)) (cancelMany c k s is) := by
  induction is generalizing s with
  | nil => exact .nil _
  | cons i is ih =>
      exact .cons (Step.cancelAck s i k requester (selected i List.mem_cons_self)
        (auth i List.mem_cons_self))
        (ih (cancelAck c s i k) (fun j member => selected j (List.mem_cons_of_mem i member))
          (fun j member => auth j (List.mem_cons_of_mem i member)))

end
end OperationalJoin
