import JoinOperations
namespace OperationalJoin
noncomputable section
open Classical

def acknowledgeMany {n} {I : Interface n} (c : Config I) : State I → List (Fin n) → State I
  | s, [] => s
  | s, i :: is => acknowledgeMany c (acknowledge c s i) is

@[simp] theorem acknowledgeMany_epoch {n} {I : Interface n} (c : Config I)
    (s : State I) (is : List (Fin n)) : (acknowledgeMany c s is).epoch = s.epoch := by
  induction is generalizing s with
  | nil => rfl
  | cons i is ih => simpa [acknowledgeMany, acknowledge] using ih (acknowledge c s i)
@[simp] theorem acknowledgeMany_plant {n} {I : Interface n} (c : Config I)
    (s : State I) (is : List (Fin n)) : (acknowledgeMany c s is).plant = s.plant := by
  induction is generalizing s with
  | nil => rfl
  | cons i is ih => simpa [acknowledgeMany, acknowledge] using ih (acknowledge c s i)
@[simp] theorem acknowledgeMany_pending {n} {I : Interface n} (c : Config I)
    (s : State I) (is : List (Fin n)) : (acknowledgeMany c s is).pending = s.pending := by
  induction is generalizing s with
  | nil => rfl
  | cons i is ih => simpa [acknowledgeMany, acknowledge] using ih (acknowledge c s i)
@[simp] theorem acknowledgeMany_damaged {n} {I : Interface n} (c : Config I)
    (s : State I) (is : List (Fin n)) : (acknowledgeMany c s is).damaged = s.damaged := by
  induction is generalizing s with
  | nil => rfl
  | cons i is ih => simpa [acknowledgeMany, acknowledge] using ih (acknowledge c s i)
@[simp] theorem acknowledgeMany_certificates {n} {I : Interface n} (c : Config I)
    (s : State I) (is : List (Fin n)) : (acknowledgeMany c s is).certificates = s.certificates := by
  induction is generalizing s with
  | nil => rfl
  | cons i is ih => simpa [acknowledgeMany, acknowledge] using ih (acknowledge c s i)
@[simp] theorem acknowledgeMany_cancelAcks {n} {I : Interface n} (c : Config I)
    (s : State I) (is : List (Fin n)) : (acknowledgeMany c s is).cancelAcks = s.cancelAcks := by
  induction is generalizing s with
  | nil => rfl
  | cons i is ih => simpa [acknowledgeMany, acknowledge] using ih (acknowledge c s i)

@[simp] theorem acknowledgeMany_acks {n} {I : Interface n} (c : Config I)
    (s : State I) (is : List (Fin n)) :
    (acknowledgeMany c s is).acks = is.toFinset ∪ s.acks := by
  induction is generalizing s with
  | nil => simp [acknowledgeMany]
  | cons i is ih =>
      simp only [acknowledgeMany, ih, acknowledge, List.toFinset_cons]
      ext j
      simp only [Finset.mem_union, Finset.mem_insert]
      tauto

/-- The root closes before its acknowledgement contributes to completion. -/
theorem acknowledgeMany_root {n} {I : Interface n} (c : Config I)
    (s : State I) (is : List (Fin n)) (j : Fin n) :
    (acknowledgeMany c s is).roots j =
      if Good c j ∧ j ∈ is then
        { s.roots j with revoked := insert s.epoch (s.roots j).revoked }
      else s.roots j := by
  induction is generalizing s with
  | nil => simp [acknowledgeMany]
  | cons i is ih =>
      simp only [acknowledgeMany, ih, acknowledge, List.mem_cons]
      by_cases goodJ : Good c j <;> by_cases goodI : Good c i <;>
        by_cases same : j = i <;> by_cases member : j ∈ is <;>
        simp_all [Function.update_apply]

theorem acknowledgeMany_trace {n} {I : Interface n} (c : Config I)
    (s : State I) (is : List (Fin n)) (pending : s.pending = true) :
    Trace c s (is.map Event.acknowledge) (acknowledgeMany c s is) := by
  induction is generalizing s with
  | nil => exact .nil _
  | cons i is ih =>
      exact .cons (Step.acknowledge s i pending) (ih (acknowledge c s i) pending)

def certifyMany {n} {I : Interface n} (c : Config I) (s : State I) (is : List (Fin n)) : State I :=
  complete (acknowledgeMany c (request s) is)

theorem certifyMany_trace {n} {I : Interface n} (c : Config I)
    (s : State I) (is : List (Fin n)) (idle : s.pending = false)
    (quorum : is.toFinset.card = c.r) :
    Trace c s (.request :: is.map Event.acknowledge ++ [.complete]) (certifyMany c s is) := by
  apply Trace.cons (Step.request s idle)
  apply trace_append (acknowledgeMany_trace c (request s) is rfl)
  apply Trace.cons (Step.complete _ (by simp [request]) ?_)
  · exact Trace.nil _
  · simpa [request] using quorum

@[simp] theorem certifyMany_epoch {n} {I : Interface n} (c : Config I)
    (s : State I) (is : List (Fin n)) : (certifyMany c s is).epoch = s.epoch + 1 := by
  simp [certifyMany, complete, request]
@[simp] theorem certifyMany_plant {n} {I : Interface n} (c : Config I)
    (s : State I) (is : List (Fin n)) : (certifyMany c s is).plant = s.plant := by
  simp [certifyMany, complete, request]
@[simp] theorem certifyMany_pending {n} {I : Interface n} (c : Config I)
    (s : State I) (is : List (Fin n)) : (certifyMany c s is).pending = false := rfl
@[simp] theorem certifyMany_damaged {n} {I : Interface n} (c : Config I)
    (s : State I) (is : List (Fin n)) : (certifyMany c s is).damaged = s.damaged := by
  simp [certifyMany, complete, request]
@[simp] theorem certifyMany_cancelAcks {n} {I : Interface n} (c : Config I)
    (s : State I) (is : List (Fin n)) : (certifyMany c s is).cancelAcks = s.cancelAcks := by
  simp [certifyMany, complete, request]
@[simp] theorem certifyMany_certificates {n} {I : Interface n} (c : Config I)
    (s : State I) (is : List (Fin n)) :
    (certifyMany c s is).certificates = Function.update s.certificates s.epoch is.toFinset := by
  simp [certifyMany, complete, request]
@[simp] theorem certifyMany_root {n} {I : Interface n} (c : Config I)
    (s : State I) (is : List (Fin n)) (j : Fin n) :
    (certifyMany c s is).roots j =
      if Good c j ∧ j ∈ is then
        { s.roots j with revoked := insert s.epoch (s.roots j).revoked }
      else s.roots j := by
  simp only [certifyMany, complete, acknowledgeMany_root, request]


def deliverMany {n} {I : Interface n} (c : Config I) (epoch : Nat) : State I → List (Fin n) → State I
  | s, [] => s
  | s, i :: is => deliverMany c epoch (deliver c s i epoch) is

@[simp] theorem deliverMany_epoch {n} {I : Interface n} (c : Config I) (epoch : Nat)
    (s : State I) (is : List (Fin n)) : (deliverMany c epoch s is).epoch = s.epoch := by
  induction is generalizing s with
  | nil => rfl
  | cons i is ih => simp [deliverMany, ih]
@[simp] theorem deliverMany_plant {n} {I : Interface n} (c : Config I) (epoch : Nat)
    (s : State I) (is : List (Fin n)) : (deliverMany c epoch s is).plant = s.plant := by
  induction is generalizing s with
  | nil => rfl
  | cons i is ih => simp [deliverMany, ih]
@[simp] theorem deliverMany_pending {n} {I : Interface n} (c : Config I) (epoch : Nat)
    (s : State I) (is : List (Fin n)) : (deliverMany c epoch s is).pending = s.pending := by
  induction is generalizing s with
  | nil => rfl
  | cons i is ih =>
      simp only [deliverMany, ih]
      unfold deliver
      split <;> rfl
@[simp] theorem deliverMany_damaged {n} {I : Interface n} (c : Config I) (epoch : Nat)
    (s : State I) (is : List (Fin n)) : (deliverMany c epoch s is).damaged = s.damaged := by
  induction is generalizing s with
  | nil => rfl
  | cons i is ih => simp [deliverMany, ih]
@[simp] theorem deliverMany_certificates {n} {I : Interface n} (c : Config I) (epoch : Nat)
    (s : State I) (is : List (Fin n)) : (deliverMany c epoch s is).certificates = s.certificates := by
  induction is generalizing s with
  | nil => rfl
  | cons i is ih =>
      simp only [deliverMany, ih]
      unfold deliver
      split <;> rfl
@[simp] theorem deliverMany_cancelAcks {n} {I : Interface n} (c : Config I) (epoch : Nat)
    (s : State I) (is : List (Fin n)) : (deliverMany c epoch s is).cancelAcks = s.cancelAcks := by
  induction is generalizing s with
  | nil => rfl
  | cons i is ih =>
      simp only [deliverMany, ih]
      unfold deliver
      split <;> rfl

theorem deliverMany_root {n} {I : Interface n} (c : Config I) (epoch : Nat)
    (s : State I) (is : List (Fin n)) (j : Fin n) :
    (deliverMany c epoch s is).roots j =
      if j ∈ is ∧ I.policyEpoch (s.roots j).descriptor < epoch then
        { s.roots j with descriptor := c.source epoch }
      else s.roots j := by
  induction is generalizing s with
  | nil => simp [deliverMany]
  | cons i is ih =>
      simp only [deliverMany, ih, deliver, List.mem_cons]
      by_cases same : j = i <;> by_cases member : j ∈ is <;>
        by_cases newer : I.policyEpoch (s.roots i).descriptor < epoch <;>
        by_cases newerJ : I.policyEpoch (s.roots j).descriptor < epoch <;>
        simp_all [setRoot, Function.update_apply, c.source_epoch] <;>
        split_ifs <;> simp_all [setRoot, Function.update_apply, c.source_epoch]

theorem deliverMany_trace {n} {I : Interface n} (c : Config I) (epoch : Nat)
    (s : State I) (is : List (Fin n)) (cert : 0 < epoch ∧ epoch ≤ s.epoch) :
    Trace c s (is.map (fun i => Event.deliver i epoch)) (deliverMany c epoch s is) := by
  induction is generalizing s with
  | nil => exact .nil _
  | cons i is ih =>
      exact .cons (Step.deliver s i epoch cert)
        (ih (deliver c s i epoch) (by simpa using cert))

end
end OperationalJoin
