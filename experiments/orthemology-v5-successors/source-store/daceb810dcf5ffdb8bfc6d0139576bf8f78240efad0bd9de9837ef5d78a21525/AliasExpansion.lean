import AliasRelation

namespace SharedAlias
open OperationalJoin
noncomputable section
open Classical

/-- A proof-side record of landing identities. It is not an observer transcript. -/
def landings {m} {I : Interface m} : List (Event I) → List (I.Command × I.Requester × Nat)
  | [] => []
  | .land k who time :: rest => (k, who, time) :: landings rest
  | _ :: rest => landings rest

@[simp] theorem landings_append {m} {I : Interface m} (xs ys : List (Event I)) :
    landings (xs ++ ys) = landings xs ++ landings ys := by
  induction xs with
  | nil => rfl
  | cons x xs ih => cases x <;> simp [landings, ih]

/-- Internal storage updates. These produce no owner or label acknowledgement. -/
def prepareLabels {m} {I : Interface m} (s : OperationalJoin.State I)
    (labels : Finset (Fin m)) (k : I.Command) : OperationalJoin.State I :=
  { s with roots := fun i => if i ∈ labels then
      { s.roots i with commitments := insert k (s.roots i).commitments } else s.roots i }

theorem prepareLabels_empty {m} {I : Interface m} (s : OperationalJoin.State I) (k : I.Command) :
    prepareLabels s ∅ k = s := by simp [prepareLabels]

theorem prepareLabels_insert {m} {I : Interface m} (s : OperationalJoin.State I)
    (labels : Finset (Fin m)) (i : Fin m) (k : I.Command) :
    prepareLabels s (insert i labels) k =
      prepareLabels (OperationalJoin.prepare s i k) labels k := by
  cases s
  simp only [prepareLabels, OperationalJoin.prepare, OperationalJoin.setRoot]
  congr 1
  funext j
  by_cases same : j = i <;> by_cases mem : j ∈ labels <;>
    simp [same, mem, Function.update_apply]

theorem prepareLabels_trace {m} {I : Interface m} (c : Config I)
    (s : OperationalJoin.State I) (labels : Finset (Fin m))
    (k : I.Command) (who : I.Requester) (time : Nat)
    (path : ValidPath c k)
    (grants : ∀ i ∈ labels, i ∈ I.commandPath k ∧
      (i ∈ c.faulty ∨ Envelope s.plant time (s.roots i) k who)) :
    ∃ events, OperationalJoin.Trace c s events (prepareLabels s labels k) ∧ landings events = [] := by
  induction labels using Finset.induction_on generalizing s with
  | empty =>
      exact ⟨[], by simpa [prepareLabels_empty] using OperationalJoin.Trace.nil s, rfl⟩
  | @insert i labels absent ih =>
      have gi := grants i (Finset.mem_insert_self _ _)
      have first := OperationalJoin.Step.prepare s i k who time gi.1 path gi.2
      have rest : ∀ j ∈ labels, j ∈ I.commandPath k ∧
          (j ∈ c.faulty ∨ Envelope (OperationalJoin.prepare s i k).plant time
            ((OperationalJoin.prepare s i k).roots j) k who) := by
        intro j hj
        have g := grants j (Finset.mem_insert_of_mem hj)
        simpa only [prepare_envelope] using g
      obtain ⟨events, trace, none⟩ := ih (OperationalJoin.prepare s i k) rest
      refine ⟨.prepare i k who time :: events, ?_, ?_⟩
      · rw [prepareLabels_insert]
        exact .cons first trace
      · simpa [landings] using none

def deliverLabels {m} {I : Interface m} (c : Config I)
    (s : OperationalJoin.State I) (labels : Finset (Fin m)) (e : Nat) : OperationalJoin.State I :=
  { s with roots := fun i =>
      if i ∈ labels ∧ I.policyEpoch (s.roots i).descriptor < e then
        { s.roots i with descriptor := c.source e } else s.roots i }

theorem deliverLabels_empty {m} {I : Interface m} (c : Config I)
    (s : OperationalJoin.State I) (e : Nat) : deliverLabels c s ∅ e = s := by
  simp [deliverLabels]

theorem deliverLabels_insert {m} {I : Interface m} (c : Config I)
    (s : OperationalJoin.State I) (labels : Finset (Fin m)) (i : Fin m) (e : Nat) :
    deliverLabels c s (insert i labels) e =
      deliverLabels c (OperationalJoin.deliver c s i e) labels e := by
  unfold OperationalJoin.deliver
  split
  · rename_i newer
    cases s
    rename_i epoch roots pending acks certificates cancelAcks plant damaged
    simp only [deliverLabels, OperationalJoin.setRoot]
    congr 1
    funext j
    by_cases same : j = i <;> by_cases mem : j ∈ labels <;>
      by_cases fresh : I.policyEpoch (roots j).descriptor < e <;>
      simp_all [Function.update_apply, c.source_epoch]
  · rename_i older
    cases s
    simp only [deliverLabels]
    congr 1
    funext j
    by_cases same : j = i <;> by_cases mem : j ∈ labels <;>
      simp_all [Function.update_apply]

theorem deliverLabels_trace {m} {I : Interface m} (c : Config I)
    (s : OperationalJoin.State I) (labels : Finset (Fin m)) (e : Nat)
    (cert : 0 < e ∧ e ≤ s.epoch) :
    ∃ events, OperationalJoin.Trace c s events (deliverLabels c s labels e) ∧ landings events = [] := by
  induction labels using Finset.induction_on generalizing s with
  | empty =>
      exact ⟨[], by simpa [deliverLabels_empty] using OperationalJoin.Trace.nil s, rfl⟩
  | @insert i labels absent ih =>
      have first := OperationalJoin.Step.deliver (c := c) s i e cert
      obtain ⟨events, trace, none⟩ := ih (OperationalJoin.deliver c s i e) (by simpa using cert)
      refine ⟨.deliver i e :: events, ?_, ?_⟩
      · rw [deliverLabels_insert]
        exact .cons first trace
      · simpa [landings] using none

end
end SharedAlias
