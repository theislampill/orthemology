import FinitePortfolio

namespace SharedAlias.Progress
open OperationalJoin
noncomputable section
open Classical

/-- Direct shared-history invariant, stronger in the needed direction than
weak simulation's subset relation on veto memories. -/
def RevocationBound {m} {I : Interface m} (E : Environment I) (C : SharedAlias.State I) : Prop :=
  ∀ i, Good E.labelConfig i → ∀ e ∈ (C.roots (E.rootOf i)).revoked,
    e ≤ C.epoch ∧ (e = C.epoch → C.pending = true)

theorem revocationBound_initial {m} {I : Interface m} (E : Environment I) (p : I.Plant) :
    RevocationBound E (SharedAlias.initial E p) := by
  intro i good e member
  simp [SharedAlias.initial] at member

theorem revocationBound_step {m} {I : Interface m} (E : Environment I)
    {C D : SharedAlias.State I} {event : Event I}
    (bound : RevocationBound E C) (step : SharedAlias.Step E C event D) : RevocationBound E D := by
  cases step with
  | request idle =>
      intro i good e member
      exact ⟨(bound i good e member).1, fun _ => rfl⟩
  | acknowledge i pending =>
      intro j goodJ e member
      have lower : e ≤ C.epoch := by
        by_cases goodI : Good E.labelConfig i
        · by_cases same : E.rootOf j = E.rootOf i
          · simp only [SharedAlias.acknowledge, if_pos goodI, same, Function.update_self,
              Finset.mem_insert] at member
            rcases member with rfl | old
            · exact le_rfl
            · exact (bound j goodJ e (by simpa only [same] using old)).1
          · have old : e ∈ (C.roots (E.rootOf j)).revoked := by
              simpa only [SharedAlias.acknowledge, if_pos goodI, Function.update_of_ne same] using member
            exact (bound j goodJ e old).1
        · have old : e ∈ (C.roots (E.rootOf j)).revoked := by
            simpa only [SharedAlias.acknowledge, if_neg goodI] using member
          exact (bound j goodJ e old).1
      exact ⟨lower, fun _ => pending⟩
  | complete pending quorum =>
      intro i good e member
      have old := (bound i good e member).1
      exact ⟨by change e ≤ C.epoch + 1; omega,
        fun same => by change e = C.epoch + 1 at same; omega⟩
  | deliver i epoch certificate =>
      intro j good e member
      have old : e ∈ (C.roots (E.rootOf j)).revoked := by
        unfold SharedAlias.deliver at member
        split at member
        · by_cases same : E.rootOf j = E.rootOf i
          · simpa [SharedAlias.setRoot, same] using member
          · simpa [SharedAlias.setRoot, Function.update_of_ne same] using member
        · exact member
      have past := bound j good e old
      unfold SharedAlias.deliver
      split <;> exact past
  | prepare i k who time selected valid grant =>
      intro j good e member
      have old : e ∈ (C.roots (E.rootOf j)).revoked := by
        by_cases same : E.rootOf j = E.rootOf i
        · simpa [SharedAlias.prepare, SharedAlias.setRoot, same] using member
        · simpa [SharedAlias.prepare, SharedAlias.setRoot, Function.update_of_ne same] using member
      exact bound j good e old
  | cancelAck i k who selected auth =>
      intro j good e member
      have old : e ∈ (C.roots (E.rootOf j)).revoked := by
        by_cases goodI : Good E.labelConfig i
        · by_cases same : E.rootOf j = E.rootOf i
          · simpa only [SharedAlias.cancelAck, if_pos goodI, same, Function.update_self] using member
          · simpa only [SharedAlias.cancelAck, if_pos goodI, Function.update_of_ne same] using member
        · simpa only [SharedAlias.cancelAck, if_neg goodI] using member
      exact bound j good e old
  | close k certificate => exact bound
  | land k who time admitted => exact bound
  | hold => exact bound
  | corrupt i z bad =>
      intro j good e member
      have different : E.rootOf j ≠ E.rootOf i := by
        intro same
        exact ((good_same_root E j i same).mp good) bad
      have old : e ∈ (C.roots (E.rootOf j)).revoked := by
        simpa [SharedAlias.setRoot, Function.update_of_ne different] using member
      exact bound j good e old

theorem revocationBound_trace {m} {I : Interface m} (E : Environment I)
    {C D : SharedAlias.State I} {events : List (Event I)}
    (bound : RevocationBound E C) (trace : SharedAlias.Trace E C events D) : RevocationBound E D := by
  induction trace with
  | nil => exact bound
  | cons step _ ih => exact ih (revocationBound_step E bound step)

theorem reachable_idle_current_unrevoked {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (reach : SharedAlias.Reachable E C) (idle : C.pending = false)
    (i : Fin m) (good : Good E.labelConfig i) :
    C.epoch ∉ (C.roots (E.rootOf i)).revoked := by
  obtain ⟨p, events, trace⟩ := reach
  have bound := revocationBound_trace E (revocationBound_initial E p) trace
  intro member
  have pending := (bound i good C.epoch member).2 rfl
  rw [idle] at pending
  cases pending

/-- Existing safety simulation does give exact good-root descriptor authenticity
and no future descriptor. It is not used to infer missing revocation facts. -/
theorem reachable_descriptor {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (reach : SharedAlias.Reachable E C)
    (i : Fin m) (good : Good E.labelConfig i) :
    (C.roots (E.rootOf i)).descriptor = E.source (I.policyEpoch (C.roots (E.rootOf i)).descriptor) ∧
      I.policyEpoch (C.roots (E.rootOf i)).descriptor ≤ C.epoch := by
  obtain ⟨s, reachable, related⟩ := SharedAlias.reachable_witness reach
  have consistent := OperationalJoin.reachable_consistent reachable
  have authentic := consistent.local_authentic i good
  have earlier := consistent.local_not_future i good
  have policy := (related.roots i good).policy
  simpa only [policy, related.epoch] using And.intro authentic earlier

/-- Policy synchronization requests name every label, not every hidden root.
Epoch zero needs no delivery certificate. Good roots service the request; a
bad label may either accept delivery or withhold in its completed slot. -/
def syncSlot {m} {I : Interface m} (E : Environment I) (epoch : Nat)
    (respond : Fin m → Bool) (C : SharedAlias.State I) (i : Fin m) : SharedAlias.State I :=
  if epoch ≠ 0 ∧ (Good E.labelConfig i ∨ respond i = true)
    then SharedAlias.deliver E C i epoch else C

/-- Proof-side spelling with the certified current epoch. The actor-facing
prelude below supplies actor.policy.epoch and proves this correspondence. -/
def synchronize {m} {I : Interface m} (E : Environment I) (respond : Fin m → Bool)
    (C : SharedAlias.State I) : SharedAlias.State I :=
  serviceList (syncSlot E C.epoch respond) C Finset.univ.toList

@[simp] theorem syncSlot_epoch {m} {I : Interface m} (E : Environment I) (epoch : Nat)
    (respond : Fin m → Bool) (C : SharedAlias.State I) (i : Fin m) :
    (syncSlot E epoch respond C i).epoch = C.epoch := by
  unfold syncSlot SharedAlias.deliver
  split
  · split <;> rfl
  · rfl

@[simp] theorem syncSlot_plant {m} {I : Interface m} (E : Environment I) (epoch : Nat)
    (respond : Fin m → Bool) (C : SharedAlias.State I) (i : Fin m) :
    (syncSlot E epoch respond C i).plant = C.plant := by
  unfold syncSlot SharedAlias.deliver
  split
  · split <;> rfl
  · rfl

theorem syncSlot_step {m} {I : Interface m} (E : Environment I) (epoch : Nat)
    (respond : Fin m → Bool) (C : SharedAlias.State I) (i : Fin m) (current : epoch = C.epoch) :
    ∃ event, SharedAlias.Step E C event (syncSlot E epoch respond C i) := by
  by_cases delivery : epoch ≠ 0 ∧ (Good E.labelConfig i ∨ respond i = true)
  · refine ⟨.deliver i epoch, ?_⟩
    rw [syncSlot, if_pos delivery]
    exact SharedAlias.Step.deliver C i epoch ⟨by omega, by omega⟩
  · exact ⟨.hold, by simpa only [syncSlot, if_neg delivery] using (SharedAlias.Step.hold (E := E) C)⟩

theorem synchronize_epoch {m} {I : Interface m} (E : Environment I) (respond : Fin m → Bool)
    (C : SharedAlias.State I) : (synchronize E respond C).epoch = C.epoch :=
  serviceList_invariant _ (fun D => D.epoch = C.epoch)
    (fun D i old => (syncSlot_epoch E C.epoch respond D i).trans old) _ _ rfl

theorem synchronize_plant {m} {I : Interface m} (E : Environment I) (respond : Fin m → Bool)
    (C : SharedAlias.State I) : (synchronize E respond C).plant = C.plant :=
  serviceList_preserves_plant _ (fun D i => syncSlot_plant E C.epoch respond D i) _ _

theorem syncList_trace {m} {I : Interface m} (E : Environment I) (epoch : Nat)
    (respond : Fin m → Bool) (C : SharedAlias.State I) (labels : List (Fin m))
    (current : epoch = C.epoch) :
    ∃ events, SharedAlias.Trace E C events (serviceList (syncSlot E epoch respond) C labels) ∧
      events.length = labels.length := by
  induction labels generalizing C with
  | nil => exact ⟨[], .nil _, rfl⟩
  | cons i labels ih =>
      obtain ⟨event, first⟩ := syncSlot_step E epoch respond C i current
      obtain ⟨events, rest, count⟩ := ih (syncSlot E epoch respond C i) (by simpa using current)
      exact ⟨event :: events, .cons first rest, by simpa only [List.length_cons] using congrArg Nat.succ count⟩

theorem synchronize_trace {m} {I : Interface m} (E : Environment I) (respond : Fin m → Bool)
    (C : SharedAlias.State I) :
    ∃ events, SharedAlias.Trace E C events (synchronize E respond C) ∧ events.length = m := by
  obtain ⟨events, trace, count⟩ := syncList_trace E C.epoch respond C Finset.univ.toList rfl
  exact ⟨events, trace, by simpa using count⟩

theorem syncSlot_descriptor_self {m} {I : Interface m} (E : Environment I) (epoch : Nat)
    (respond : Fin m → Bool) (C : SharedAlias.State I) (i : Fin m) (current : epoch = C.epoch)
    (reach : SharedAlias.Reachable E C) (good : Good E.labelConfig i) :
    ((syncSlot E epoch respond C i).roots (E.rootOf i)).descriptor = E.source epoch := by
  obtain ⟨authentic, past⟩ := reachable_descriptor E C reach i good
  rw [← current] at past
  by_cases zero : epoch = 0
  · have policyEpoch : I.policyEpoch (C.roots (E.rootOf i)).descriptor = epoch := by omega
    simpa only [syncSlot, zero, ne_eq, not_true_eq_false, false_and, if_false, policyEpoch] using authentic
  · have delivery : epoch ≠ 0 ∧ (Good E.labelConfig i ∨ respond i = true) := ⟨zero, Or.inl good⟩
    simp only [syncSlot, if_pos delivery, SharedAlias.deliver]
    split
    · simp [SharedAlias.setRoot]
    · rename_i notEarlier
      have same : I.policyEpoch (C.roots (E.rootOf i)).descriptor = epoch := by omega
      simpa only [same] using authentic

theorem syncSlot_preserves_descriptor {m} {I : Interface m} (E : Environment I) (epoch : Nat)
    (respond : Fin m → Bool) (C : SharedAlias.State I) (i j : Fin m)
    (already : (C.roots (E.rootOf j)).descriptor = E.source epoch) :
    ((syncSlot E epoch respond C i).roots (E.rootOf j)).descriptor = E.source epoch := by
  unfold syncSlot
  split
  · unfold SharedAlias.deliver
    split
    · by_cases same : E.rootOf j = E.rootOf i
      · simp [SharedAlias.setRoot, same]
      · simpa [SharedAlias.setRoot, Function.update_of_ne same] using already
    · exact already
  · exact already

theorem syncList_descriptor {m} {I : Interface m} (E : Environment I) (epoch : Nat)
    (respond : Fin m → Bool) (C : SharedAlias.State I) (labels : List (Fin m))
    (current : epoch = C.epoch) (reach : SharedAlias.Reachable E C)
    (j : Fin m) (member : j ∈ labels) (good : Good E.labelConfig j) :
    ((serviceList (syncSlot E epoch respond) C labels).roots (E.rootOf j)).descriptor = E.source epoch := by
  induction labels generalizing C with
  | nil => simp at member
  | cons i labels ih =>
      simp only [serviceList]
      rcases List.mem_cons.mp member with same | later
      · subst j
        apply serviceList_invariant _ (fun D => (D.roots (E.rootOf i)).descriptor = E.source epoch)
        · intro D j old; exact syncSlot_preserves_descriptor E epoch respond D j i old
        · exact syncSlot_descriptor_self E epoch respond C i current reach good
      · apply ih (syncSlot E epoch respond C i) (by simpa using current)
        · obtain ⟨event, step⟩ := syncSlot_step E epoch respond C i current
          exact reachable_after reach (.cons step (.nil _))
        · exact later

theorem synchronized_descriptor {m} {I : Interface m} (E : Environment I) (respond : Fin m → Bool)
    (C : SharedAlias.State I) (reach : SharedAlias.Reachable E C)
    (i : Fin m) (good : Good E.labelConfig i) :
    ((synchronize E respond C).roots (E.rootOf i)).descriptor = E.source C.epoch :=
  syncList_descriptor E C.epoch respond C Finset.univ.toList rfl reach i (by simp) good

theorem syncSlot_memories {m} {I : Interface m} (E : Environment I) (epoch : Nat)
    (respond : Fin m → Bool) (C : SharedAlias.State I) (i j : Fin m) :
    ((syncSlot E epoch respond C i).roots (E.rootOf j)).revoked = (C.roots (E.rootOf j)).revoked ∧
      ((syncSlot E epoch respond C i).roots (E.rootOf j)).cancelled = (C.roots (E.rootOf j)).cancelled := by
  unfold syncSlot
  split
  · unfold SharedAlias.deliver
    split
    · by_cases same : E.rootOf j = E.rootOf i
      · simp [SharedAlias.setRoot, same]
      · simp [SharedAlias.setRoot, Function.update_of_ne same]
    · exact ⟨rfl, rfl⟩
  · exact ⟨rfl, rfl⟩

theorem synchronized_memories {m} {I : Interface m} (E : Environment I) (respond : Fin m → Bool)
    (C : SharedAlias.State I) (j : Fin m) :
    ((synchronize E respond C).roots (E.rootOf j)).revoked = (C.roots (E.rootOf j)).revoked ∧
      ((synchronize E respond C).roots (E.rootOf j)).cancelled = (C.roots (E.rootOf j)).cancelled := by
  apply serviceList_invariant _ (fun D =>
    (D.roots (E.rootOf j)).revoked = (C.roots (E.rootOf j)).revoked ∧
      (D.roots (E.rootOf j)).cancelled = (C.roots (E.rootOf j)).cancelled) _ C _ ⟨rfl, rfl⟩
  intro D i old
  have preserved := syncSlot_memories E C.epoch respond D i j
  exact ⟨preserved.1.trans old.1, preserved.2.trans old.2⟩

theorem synchronized_clear {m} {I : Interface m} (E : Environment I) (respond : Fin m → Bool)
    (C : SharedAlias.State I) (reach : SharedAlias.Reachable E C) (idle : C.pending = false)
    (k : I.Command) (current : I.commandEpoch k = C.epoch)
    (fresh : ∀ i, Good E.labelConfig i → k ∉ (C.roots (E.rootOf i)).cancelled) :
    Clear E (synchronize E respond C) k (E.source C.epoch) := by
  intro i good
  have memories := synchronized_memories E respond C i
  refine ⟨synchronized_descriptor E respond C reach i good, ?_, ?_⟩
  · rw [memories.1, current]
    exact reachable_idle_current_unrevoked E C reach idle i good
  · rw [memories.2]; exact fresh i good

open OperationalJoin.Typed (interface)

/-- The prelude's instruction list contains only public labels and the actor's
supplied policy epoch. Fixed-world equality is proved separately below. -/
def publicPrelude (m : Nat) (actor : ComposedExecution.Actor) : List (Fin m × Nat) :=
  Finset.univ.toList.map (fun i => (i, actor.policy.epoch))

def actorSynchronize {m} (E : Environment (interface m)) (actor : ComposedExecution.Actor)
    (respond : Fin m → Bool) (C : SharedAlias.State (interface m)) : SharedAlias.State (interface m) :=
  serviceList (syncSlot E actor.policy.epoch respond) C Finset.univ.toList

theorem actorSynchronize_eq {m} (E : Environment (interface m)) (actor : ComposedExecution.Actor)
    (respond : Fin m → Bool) (C : SharedAlias.State (interface m))
    (authentic : actor.policy = E.source C.epoch) :
    actorSynchronize E actor respond C = synchronize E respond C := by
  have epoch : actor.policy.epoch = C.epoch := by
    rw [authentic]
    exact E.source_epoch C.epoch
  simp only [actorSynchronize, synchronize, epoch]

end
end SharedAlias.Progress
