import AliasExpansion

namespace SharedAlias
open OperationalJoin
noncomputable section
open Classical

def aliases {m} {I : Interface m} (E : Environment I) (i : Fin m) : Finset (Fin m) :=
  Finset.univ.filter (fun j => E.rootOf j = E.rootOf i)

@[simp] theorem mem_aliases {m} {I : Interface m} (E : Environment I) (i j : Fin m) :
    j ∈ aliases E i ↔ E.rootOf j = E.rootOf i := by simp [aliases]

theorem request_refines {m} {I : Interface m} {E : Environment I}
    {C : State I} {s : OperationalJoin.State I} (h : Refines E C s) :
    Refines E (request C) (OperationalJoin.request s) := by
  exact ⟨h.epoch, rfl, rfl, h.certificates, h.cancelAcks, h.plant, h.safe, h.roots⟩

theorem complete_refines {m} {I : Interface m} {E : Environment I}
    {C : State I} {s : OperationalJoin.State I} (h : Refines E C s) :
    Refines E (complete C) (OperationalJoin.complete s) := by
  refine ⟨?_, rfl, rfl, ?_, h.cancelAcks, h.plant, h.safe, h.roots⟩
  · simp only [complete, OperationalJoin.complete, h.epoch]
  · simp only [complete, OperationalJoin.complete, h.epoch, h.certificates, h.acks]

theorem acknowledge_refines {m} {I : Interface m} {E : Environment I}
    {C : State I} {s : OperationalJoin.State I} (h : Refines E C s) (i : Fin m) :
    Refines E (acknowledge E C i) (OperationalJoin.acknowledge E.labelConfig s i) := by
  refine ⟨h.epoch, h.pending, ?_, h.certificates, h.cancelAcks, h.plant, h.safe, ?_⟩
  · simp only [acknowledge, OperationalJoin.acknowledge, h.acks]
  · intro j goodJ
    have old := h.roots j goodJ
    by_cases goodI : Good E.labelConfig i
    · by_cases same : j = i
      · subst j
        simp only [acknowledge, OperationalJoin.acknowledge, if_pos goodI, Function.update_self]
        refine ⟨old.policy, old.commitments, ?_, old.cancelled⟩
        rw [h.epoch]
        exact Finset.insert_subset_insert _ old.revoked
      · by_cases sameRoot : E.rootOf j = E.rootOf i
        · simp only [acknowledge, OperationalJoin.acknowledge, if_pos goodI,
            Function.update_of_ne same, sameRoot, Function.update_self]
          rw [sameRoot] at old
          exact ⟨old.policy, old.commitments, old.revoked.trans (Finset.subset_insert _ _), old.cancelled⟩
        · simpa only [acknowledge, OperationalJoin.acknowledge, if_pos goodI,
            Function.update_of_ne same, Function.update_of_ne sameRoot] using old
    · simpa only [acknowledge, OperationalJoin.acknowledge, if_neg goodI] using old

theorem cancelAck_refines {m} {I : Interface m} {E : Environment I}
    {C : State I} {s : OperationalJoin.State I} (h : Refines E C s)
    (i : Fin m) (k : I.Command) :
    Refines E (cancelAck E C i k) (OperationalJoin.cancelAck E.labelConfig s i k) := by
  refine ⟨h.epoch, h.pending, h.acks, h.certificates, ?_, h.plant, h.safe, ?_⟩
  · simp only [cancelAck, OperationalJoin.cancelAck, h.cancelAcks]
  · intro j goodJ
    have old := h.roots j goodJ
    by_cases goodI : Good E.labelConfig i
    · by_cases same : j = i
      · subst j
        simp only [cancelAck, OperationalJoin.cancelAck, if_pos goodI, Function.update_self]
        exact ⟨old.policy, old.commitments, old.revoked, Finset.insert_subset_insert _ old.cancelled⟩
      · by_cases sameRoot : E.rootOf j = E.rootOf i
        · simp only [cancelAck, OperationalJoin.cancelAck, if_pos goodI,
            Function.update_of_ne same, sameRoot, Function.update_self]
          rw [sameRoot] at old
          exact ⟨old.policy, old.commitments, old.revoked, old.cancelled.trans (Finset.subset_insert _ _)⟩
        · simpa only [cancelAck, OperationalJoin.cancelAck, if_pos goodI,
            Function.update_of_ne same, Function.update_of_ne sameRoot] using old
    · simpa only [cancelAck, OperationalJoin.cancelAck, if_neg goodI] using old

theorem corrupt_refines {m} {I : Interface m} {E : Environment I}
    {C : State I} {s : OperationalJoin.State I} (h : Refines E C s)
    (i : Fin m) (z : RootState I) (bad : i ∈ E.labelConfig.faulty) :
    Refines E (setRoot C (E.rootOf i) z) s := by
  refine ⟨h.epoch, h.pending, h.acks, h.certificates, h.cancelAcks, h.plant, h.safe, ?_⟩
  intro j goodJ
  have different : E.rootOf j ≠ E.rootOf i := by
    intro eq
    have goodI := (good_same_root E j i eq).mp goodJ
    exact goodI bad
  simpa only [setRoot, Function.update_of_ne different] using h.roots j goodJ

theorem prepare_refines {m} {I : Interface m} {E : Environment I}
    {C : State I} {s : OperationalJoin.State I} (h : Refines E C s)
    (i : Fin m) (k : I.Command) :
    Refines E (prepare E C i k)
      (prepareLabels s (I.commandPath k ∩ aliases E i) k) := by
  refine ⟨h.epoch, h.pending, h.acks, h.certificates, h.cancelAcks, h.plant, h.safe, ?_⟩
  intro j goodJ
  have old := h.roots j goodJ
  by_cases sameRoot : E.rootOf j = E.rootOf i
  · by_cases selected : j ∈ I.commandPath k
    · simp only [prepareLabels, prepare, setRoot, Finset.mem_inter, mem_aliases,
        selected, sameRoot, and_self, if_true, Function.update_self]
      rw [sameRoot] at old
      refine ⟨old.policy, ?_, old.revoked, old.cancelled⟩
      intro command
      simp only [Finset.mem_insert, old.commitments]
      by_cases same : command = k
      · subst command; simp [selected]
      · simp [same]
    · simp only [prepareLabels, prepare, setRoot, Finset.mem_inter, mem_aliases,
        selected, false_and, if_false, sameRoot, Function.update_self]
      rw [sameRoot] at old
      refine ⟨old.policy, ?_, old.revoked, old.cancelled⟩
      intro command
      rw [old.commitments]
      simp only [Finset.mem_insert]
      by_cases same : command = k
      · subst command; simp [selected]
      · simp [same]
  · simpa only [prepareLabels, prepare, setRoot, Finset.mem_inter, mem_aliases,
      sameRoot, and_false, if_false, Function.update_of_ne sameRoot] using old

theorem deliver_refines {m} {I : Interface m} {E : Environment I}
    {C : State I} {s : OperationalJoin.State I} (h : Refines E C s)
    (i : Fin m) (e : Nat) :
    Refines E (deliver E C i e) (deliverLabels E.labelConfig s (aliases E i) e) := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · unfold deliver; split <;> exact h.epoch
  · unfold deliver; split <;> exact h.pending
  · unfold deliver; split <;> exact h.acks
  · unfold deliver; split <;> exact h.certificates
  · unfold deliver; split <;> exact h.cancelAcks
  · unfold deliver; split <;> exact h.plant
  · exact h.safe
  · intro j goodJ
    have old := h.roots j goodJ
    by_cases sameRoot : E.rootOf j = E.rootOf i
    · have policy : (s.roots j).descriptor = (C.roots (E.rootOf i)).descriptor := by
        simpa only [sameRoot] using old.policy
      by_cases newer : I.policyEpoch (C.roots (E.rootOf i)).descriptor < e
      · simp only [deliver, if_pos newer, setRoot, deliverLabels, mem_aliases, sameRoot,
          policy, newer, and_self, if_true, Function.update_self]
        rw [sameRoot] at old
        exact ⟨rfl, old.commitments, old.revoked, old.cancelled⟩
      · simpa only [deliver, if_neg newer, deliverLabels, mem_aliases, sameRoot,
          policy, newer, and_false, if_false] using old
    · simp only [deliverLabels, mem_aliases, sameRoot, false_and, if_false]
      unfold deliver
      split
      · simpa only [setRoot, Function.update_of_ne sameRoot] using old
      · exact old

end
end SharedAlias
