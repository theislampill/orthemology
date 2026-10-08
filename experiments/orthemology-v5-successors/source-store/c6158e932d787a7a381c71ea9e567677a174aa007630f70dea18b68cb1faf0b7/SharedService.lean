import AliasRuntime

/-! New finite reference service handlers over the accepted shared store.
These are not the unchanged source preparation or runBatch storage macros.
A scheduled good-root request is serviced in its slot; a bad-root reply may
withhold. No handler returns the hidden map or a denial reason to the actor. -/
namespace SharedAlias.Progress
open OperationalJoin
noncomputable section
open Classical

abbrev Service {m} (I : Interface m) := SharedAlias.State I → Fin m → SharedAlias.State I

def prepareAllowed {m} {I : Interface m} (E : Environment I) (C : SharedAlias.State I)
    (i : Fin m) (k : I.Command) (who : I.Requester) (time : Nat) (badReply : Bool) : Prop :=
  i ∈ I.commandPath k ∧ ValidPath E.labelConfig k ∧
    if Good E.labelConfig i then Envelope C.plant time (C.roots (E.rootOf i)) k who
    else badReply = true

def prepareSlot {m} {I : Interface m} (E : Environment I) (C : SharedAlias.State I)
    (i : Fin m) (k : I.Command) (who : I.Requester) (time : Nat) (badReply : Bool) :
    SharedAlias.State I :=
  if prepareAllowed E C i k who time badReply then SharedAlias.prepare E C i k else C

def cancelAllowed {m} {I : Interface m} (E : Environment I) (i : Fin m)
    (k : I.Command) (who : I.Requester) (badReply : Bool) : Prop :=
  i ∈ I.commandPath k ∧ if Good E.labelConfig i then who = I.recipient k else badReply = true

def cancelSlot {m} {I : Interface m} (E : Environment I) (C : SharedAlias.State I)
    (i : Fin m) (k : I.Command) (who : I.Requester) (badReply : Bool) :
    SharedAlias.State I :=
  if cancelAllowed E i k who badReply then SharedAlias.cancelAck E C i k else C

def serviceList {m} {I : Interface m} (service : Service I)
    (C : SharedAlias.State I) : List (Fin m) → SharedAlias.State I
  | [] => C
  | i :: is => serviceList service (service C i) is

def preparePath {m} {I : Interface m} (E : Environment I) (C : SharedAlias.State I)
    (k : I.Command) (who : I.Requester) (time : Nat) (badReply : Fin m → Bool) :
    SharedAlias.State I :=
  serviceList (fun D i => prepareSlot E D i k who time (badReply i)) C
    (I.commandPath k).toList

def cancelPath {m} {I : Interface m} (E : Environment I) (C : SharedAlias.State I)
    (k : I.Command) (who : I.Requester) (badReply : Fin m → Bool) : SharedAlias.State I :=
  serviceList (fun D i => cancelSlot E D i k who (badReply i)) C
    (I.commandPath k).toList

theorem trace_append {m} {I : Interface m} {E : Environment I}
    {C D F : SharedAlias.State I} {xs ys : List (Event I)}
    (first : SharedAlias.Trace E C xs D) (second : SharedAlias.Trace E D ys F) :
    SharedAlias.Trace E C (xs ++ ys) F := by
  induction first with
  | nil => exact second
  | cons step _ ih => exact .cons step (ih second)

theorem reachable_after {m} {I : Interface m} {E : Environment I}
    {C D : SharedAlias.State I} {events : List (Event I)}
    (reach : SharedAlias.Reachable E C) (trace : SharedAlias.Trace E C events D) :
    SharedAlias.Reachable E D := by
  obtain ⟨p, before, h⟩ := reach
  exact ⟨p, before ++ events, trace_append h trace⟩

theorem prepareSlot_step {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (i : Fin m) (k : I.Command) (who : I.Requester)
    (time : Nat) (badReply : Bool) :
    ∃ event, SharedAlias.Step E C event (prepareSlot E C i k who time badReply) := by
  by_cases allowed : prepareAllowed E C i k who time badReply
  · refine ⟨.prepare i k who time, ?_⟩
    rw [prepareSlot, if_pos allowed]
    apply SharedAlias.Step.prepare C i k who time allowed.1 allowed.2.1
    by_cases good : Good E.labelConfig i
    · exact Or.inr (by simpa only [if_pos good] using allowed.2.2)
    · exact Or.inl (not_not.mp good)
  · exact ⟨.hold, by simpa only [prepareSlot, if_neg allowed] using SharedAlias.Step.hold (E := E) C⟩

theorem cancelSlot_step {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (i : Fin m) (k : I.Command) (who : I.Requester)
    (badReply : Bool) :
    ∃ event, SharedAlias.Step E C event (cancelSlot E C i k who badReply) := by
  by_cases allowed : cancelAllowed E i k who badReply
  · refine ⟨.cancelAck i k who, ?_⟩
    rw [cancelSlot, if_pos allowed]
    apply SharedAlias.Step.cancelAck C i k who allowed.1
    by_cases good : Good E.labelConfig i
    · exact Or.inr (by simpa only [if_pos good] using allowed.2)
    · exact Or.inl (not_not.mp good)
  · exact ⟨.hold, by simpa only [cancelSlot, if_neg allowed] using SharedAlias.Step.hold (E := E) C⟩

theorem serviceList_trace {m} {I : Interface m} (E : Environment I)
    (service : Service I)
    (legal : ∀ C i, ∃ event, SharedAlias.Step E C event (service C i))
    (C : SharedAlias.State I) (labels : List (Fin m)) :
    ∃ events, SharedAlias.Trace E C events (serviceList service C labels) ∧
      events.length = labels.length := by
  induction labels generalizing C with
  | nil => exact ⟨[], .nil C, rfl⟩
  | cons i labels ih =>
      obtain ⟨event, first⟩ := legal C i
      obtain ⟨events, rest, size⟩ := ih (service C i)
      exact ⟨event :: events, .cons first rest, by simpa using size⟩

theorem serviceList_invariant {m} {I : Interface m} (service : Service I)
    (P : SharedAlias.State I → Prop)
    (preserve : ∀ C i, P C → P (service C i))
    (C : SharedAlias.State I) (labels : List (Fin m)) (initial : P C) :
    P (serviceList service C labels) := by
  induction labels generalizing C with
  | nil => exact initial
  | cons i labels ih => exact ih (service C i) (preserve C i initial)

theorem prepare_envelope {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (i j : Fin m) (k checked : I.Command)
    (who : I.Requester) (time : Nat) :
    Envelope (SharedAlias.prepare E C i k).plant time
      ((SharedAlias.prepare E C i k).roots (E.rootOf j)) checked who ↔
      Envelope C.plant time (C.roots (E.rootOf j)) checked who := by
  by_cases same : E.rootOf j = E.rootOf i <;>
    simp [Envelope, SharedAlias.prepare, SharedAlias.setRoot, Function.update_apply, same]

theorem prepareSlot_envelope {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (i j : Fin m) (k checked : I.Command)
    (who requester : I.Requester) (time checkedTime : Nat) (badReply : Bool) :
    Envelope (prepareSlot E C i k who time badReply).plant checkedTime
      ((prepareSlot E C i k who time badReply).roots (E.rootOf j)) checked requester ↔
      Envelope C.plant checkedTime (C.roots (E.rootOf j)) checked requester := by
  unfold prepareSlot
  split
  · exact prepare_envelope E C i j k checked requester checkedTime
  · rfl

@[simp] theorem prepareSlot_plant {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (i : Fin m) (k : I.Command) (who : I.Requester)
    (time : Nat) (badReply : Bool) :
    (prepareSlot E C i k who time badReply).plant = C.plant := by
  unfold prepareSlot; split <;> rfl

@[simp] theorem cancelSlot_plant {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (i : Fin m) (k : I.Command) (who : I.Requester)
    (badReply : Bool) : (cancelSlot E C i k who badReply).plant = C.plant := by
  unfold cancelSlot; split <;> rfl

/-- Good-root service writes the shared store; no class member is queried. -/
theorem prepareSlot_commits {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (i : Fin m) (k : I.Command) (who : I.Requester)
    (time : Nat) (badReply : Bool) (selected : i ∈ I.commandPath k)
    (valid : ValidPath E.labelConfig k) (good : Good E.labelConfig i)
    (ready : Envelope C.plant time (C.roots (E.rootOf i)) k who) :
    k ∈ ((prepareSlot E C i k who time badReply).roots (E.rootOf i)).commitments := by
  have allowed : prepareAllowed E C i k who time badReply :=
    ⟨selected, valid, by simpa only [if_pos good] using ready⟩
  simp [prepareSlot, allowed, SharedAlias.prepare, SharedAlias.setRoot]

theorem prepareSlot_preserves_commitment {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (i j : Fin m) (k checked : I.Command)
    (who : I.Requester) (time : Nat) (badReply : Bool)
    (old : checked ∈ (C.roots (E.rootOf j)).commitments) :
    checked ∈ ((prepareSlot E C i k who time badReply).roots (E.rootOf j)).commitments := by
  unfold prepareSlot
  split
  · by_cases same : E.rootOf j = E.rootOf i
    · simp only [SharedAlias.prepare, SharedAlias.setRoot, same, Function.update_self, Finset.mem_insert]
      exact Or.inr (by simpa only [same] using old)
    · simpa [SharedAlias.prepare, SharedAlias.setRoot, Function.update_of_ne same] using old
  · exact old

/-- The exact config assumptions imply enough honest replies on every q-path. -/
theorem quorum_more_than_twice_budget {m} {I : Interface m} (E : Environment I) :
    2 * E.labelBudget < E.q := by
  have overlap := E.overlap
  have available := E.revoke_available
  change m + E.labelBudget < E.q + E.r at overlap
  change E.r + E.labelBudget ≤ m at available
  omega


theorem serviceList_preserves_plant {m} {I : Interface m} (service : Service I)
    (preserve : ∀ C i, (service C i).plant = C.plant)
    (C : SharedAlias.State I) (labels : List (Fin m)) :
    (serviceList service C labels).plant = C.plant :=
  serviceList_invariant service (fun D => D.plant = C.plant)
    (fun D i h => (preserve D i).trans h) C labels rfl

@[simp] theorem preparePath_plant {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (k : I.Command) (who : I.Requester)
    (time : Nat) (badReply : Fin m → Bool) :
    (preparePath E C k who time badReply).plant = C.plant :=
  serviceList_preserves_plant _ (fun D i => prepareSlot_plant E D i k who time (badReply i)) _ _

@[simp] theorem cancelPath_plant {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (k : I.Command) (who : I.Requester)
    (badReply : Fin m → Bool) : (cancelPath E C k who badReply).plant = C.plant :=
  serviceList_preserves_plant _ (fun D i => cancelSlot_plant E D i k who (badReply i)) _ _

theorem prepareList_envelope {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (labels : List (Fin m)) (j : Fin m)
    (k checked : I.Command) (who requester : I.Requester)
    (time checkedTime : Nat) (badReply : Fin m → Bool)
    (ready : Envelope C.plant checkedTime (C.roots (E.rootOf j)) checked requester) :
    Envelope (serviceList (fun D i => prepareSlot E D i k who time (badReply i)) C labels).plant
      checkedTime
      ((serviceList (fun D i => prepareSlot E D i k who time (badReply i)) C labels).roots
        (E.rootOf j)) checked requester := by
  apply serviceList_invariant _
    (fun D => Envelope D.plant checkedTime (D.roots (E.rootOf j)) checked requester) _ C labels ready
  intro D i old
  exact (prepareSlot_envelope E D i j k checked who requester time checkedTime (badReply i)).mpr old

theorem prepareList_commits {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (labels : List (Fin m)) (k : I.Command)
    (who : I.Requester) (time : Nat) (badReply : Fin m → Bool)
    (valid : ValidPath E.labelConfig k)
    (selected : ∀ i ∈ labels, i ∈ I.commandPath k)
    (ready : ∀ i, Good E.labelConfig i →
      Envelope C.plant time (C.roots (E.rootOf i)) k who)
    (j : Fin m) (member : j ∈ labels) (good : Good E.labelConfig j) :
    k ∈ ((serviceList (fun D i => prepareSlot E D i k who time (badReply i)) C labels).roots
      (E.rootOf j)).commitments := by
  induction labels generalizing C with
  | nil => simp at member
  | cons i labels ih =>
      simp only [serviceList]
      rcases List.mem_cons.mp member with same | later
      · subst j
        apply serviceList_invariant _ (fun D => k ∈ (D.roots (E.rootOf i)).commitments)
        · intro D j old
          exact prepareSlot_preserves_commitment E D j i k k who time (badReply j) old
        · exact prepareSlot_commits E C i k who time (badReply i)
            (selected i (by simp)) valid good (ready i good)
      · apply ih (prepareSlot E C i k who time (badReply i))
        · intro j hj; exact selected j (List.mem_cons_of_mem i hj)
        · intro j goodJ
          exact (prepareSlot_envelope E C i j k k who who time time (badReply i)).mpr (ready j goodJ)
        · exact later

theorem preparePath_permits {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (k : I.Command) (who : I.Requester) (time : Nat)
    (badReply : Fin m → Bool) (valid : ValidPath E.labelConfig k)
    (ready : ∀ i, Good E.labelConfig i →
      Envelope C.plant time (C.roots (E.rootOf i)) k who) :
    SharedAlias.Lands E (preparePath E C k who time badReply) time k who := by
  refine ⟨valid, ?_⟩
  intro i selected good
  exact ⟨prepareList_commits E C _ k who time badReply valid
      (by intro j hj; exact Finset.mem_toList.mp hj) ready i
      (Finset.mem_toList.mpr selected) good,
    prepareList_envelope E C _ i k k who who time time badReply (ready i good)⟩

theorem preparePath_trace {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (k : I.Command) (who : I.Requester) (time : Nat)
    (badReply : Fin m → Bool) (valid : ValidPath E.labelConfig k) :
    ∃ events, SharedAlias.Trace E C events (preparePath E C k who time badReply) ∧
      events.length = E.q := by
  obtain ⟨events, trace, size⟩ := serviceList_trace E
    (fun D i => prepareSlot E D i k who time (badReply i))
    (fun D i => prepareSlot_step E D i k who time (badReply i)) C (I.commandPath k).toList
  exact ⟨events, trace, by simpa only [Finset.length_toList, valid] using size⟩

/-- Receipt growth is per selected label, even if several labels share one store. -/
theorem cancelSlot_receipts_mono {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (i : Fin m) (k : I.Command) (who : I.Requester)
    (badReply : Bool) : C.cancelAcks k ⊆ (cancelSlot E C i k who badReply).cancelAcks k := by
  unfold cancelSlot
  split
  · rw [cancelAck_receipts]; exact Finset.subset_insert _ _
  · exact Finset.Subset.refl _

theorem cancelSlot_good_receipt {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (i : Fin m) (k : I.Command) (who : I.Requester)
    (badReply : Bool) (selected : i ∈ I.commandPath k) (good : Good E.labelConfig i)
    (auth : who = I.recipient k) :
    i ∈ (cancelSlot E C i k who badReply).cancelAcks k := by
  have allowed : cancelAllowed E i k who badReply :=
    ⟨selected, by simpa only [if_pos good] using auth⟩
  simp [cancelSlot, allowed, cancelAck_receipts]

theorem cancelList_good_receipts {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (labels : List (Fin m)) (k : I.Command)
    (who : I.Requester) (badReply : Fin m → Bool)
    (auth : who = I.recipient k) (selected : ∀ i ∈ labels, i ∈ I.commandPath k)
    (j : Fin m) (member : j ∈ labels) (good : Good E.labelConfig j) :
    j ∈ (serviceList (fun D i => cancelSlot E D i k who (badReply i)) C labels).cancelAcks k := by
  induction labels generalizing C with
  | nil => simp at member
  | cons i labels ih =>
      simp only [serviceList]
      rcases List.mem_cons.mp member with same | later
      · subst j
        apply serviceList_invariant _ (fun D => i ∈ D.cancelAcks k)
        · intro D j old; exact cancelSlot_receipts_mono E D j k who (badReply j) old
        · exact cancelSlot_good_receipt E C i k who (badReply i) (selected i (by simp)) good auth
      · apply ih (cancelSlot E C i k who (badReply i))
        · intro j hj; exact selected j (List.mem_cons_of_mem i hj)
        · exact later

theorem cancelPath_closes {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (k : I.Command) (who : I.Requester)
    (badReply : Fin m → Bool) (valid : ValidPath E.labelConfig k)
    (auth : who = I.recipient k) :
    E.labelBudget < ((cancelPath E C k who badReply).cancelAcks k).card := by
  have subset : I.commandPath k \ E.labelConfig.faulty ⊆
      (cancelPath E C k who badReply).cancelAcks k := by
    intro i member
    obtain ⟨selected, good⟩ := Finset.mem_sdiff.mp member
    exact cancelList_good_receipts E C _ k who badReply auth
      (by intro j hj; exact Finset.mem_toList.mp hj) i (Finset.mem_toList.mpr selected) good
  have lower := Finset.card_le_card subset
  have split := Finset.card_sdiff_add_card_inter (I.commandPath k) E.labelConfig.faulty
  have bounded := Finset.card_le_card (Finset.inter_subset_right :
    I.commandPath k ∩ E.labelConfig.faulty ⊆ E.labelConfig.faulty)
  have budget := E.labelConfig.budget_bound
  have quorum := quorum_more_than_twice_budget E
  change (I.commandPath k).card = E.q at valid
  change E.labelConfig.faulty.card ≤ E.labelBudget at budget
  omega

theorem cancelPath_trace {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (k : I.Command) (who : I.Requester)
    (badReply : Fin m → Bool) (valid : ValidPath E.labelConfig k) :
    ∃ events, SharedAlias.Trace E C events (cancelPath E C k who badReply) ∧
      events.length = E.q := by
  obtain ⟨events, trace, size⟩ := serviceList_trace E
    (fun D i => cancelSlot E D i k who (badReply i))
    (fun D i => cancelSlot_step E D i k who (badReply i)) C (I.commandPath k).toList
  exact ⟨events, trace, by simpa only [Finset.length_toList, valid] using size⟩

end
end SharedAlias.Progress
