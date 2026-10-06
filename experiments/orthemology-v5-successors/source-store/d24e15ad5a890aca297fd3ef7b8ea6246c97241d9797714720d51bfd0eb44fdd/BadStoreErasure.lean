import ProgressWitness

/-! Additive finite bad-store stuttering, separate from accepted progress-core-v1.
The relation below is proof-side state equality where bad stores are erased;
it is not an actor observation interface or an opacity claim. -/
namespace SharedAlias.Progress.BadStore
open OperationalJoin
open OperationalJoin.Typed (interface BoundedEnvelope)
noncomputable section
open Classical

structure SameGoodState {m} {I : Interface m} (E : Environment I)
    (C D : SharedAlias.State I) : Prop where
  epoch : C.epoch = D.epoch
  pending : C.pending = D.pending
  acks : C.acks = D.acks
  certificates : C.certificates = D.certificates
  cancelAcks : C.cancelAcks = D.cancelAcks
  plant : C.plant = D.plant
  roots : ∀ i, Good E.labelConfig i → C.roots (E.rootOf i) = D.roots (E.rootOf i)

theorem SameGoodState.refl {m} {I : Interface m} (E : Environment I) (C : SharedAlias.State I) :
    SameGoodState E C C := ⟨rfl, rfl, rfl, rfl, rfl, rfl, fun _ _ => rfl⟩

theorem SameGoodState.symm {m} {I : Interface m} {E : Environment I}
    {C D : SharedAlias.State I} (h : SameGoodState E C D) : SameGoodState E D C :=
  ⟨h.epoch.symm, h.pending.symm, h.acks.symm, h.certificates.symm, h.cancelAcks.symm,
    h.plant.symm, fun i good => (h.roots i good).symm⟩

theorem SameGoodState.trans {m} {I : Interface m} {E : Environment I}
    {C D F : SharedAlias.State I} (h : SameGoodState E C D) (g : SameGoodState E D F) : SameGoodState E C F :=
  ⟨h.epoch.trans g.epoch, h.pending.trans g.pending, h.acks.trans g.acks,
    h.certificates.trans g.certificates, h.cancelAcks.trans g.cancelAcks,
    h.plant.trans g.plant, fun i good => (h.roots i good).trans (g.roots i good)⟩

theorem corrupt_preserves {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (i : Fin m) (z : RootState I) (bad : i ∈ E.labelConfig.faulty) :
    SameGoodState E C (SharedAlias.setRoot C (E.rootOf i) z) := by
  refine ⟨rfl, rfl, rfl, rfl, rfl, rfl, ?_⟩
  intro j good
  have different : E.rootOf j ≠ E.rootOf i := by
    intro same; exact ((good_same_root E j i same).mp good) bad
  simp only [SharedAlias.setRoot, Function.update_of_ne different]

theorem prepare_congr {m} {I : Interface m} {E : Environment I}
    {C D : SharedAlias.State I} (h : SameGoodState E C D) (i : Fin m) (k : I.Command) :
    SameGoodState E (SharedAlias.prepare E C i k) (SharedAlias.prepare E D i k) := by
  refine ⟨h.epoch, h.pending, h.acks, h.certificates, h.cancelAcks, h.plant, ?_⟩
  intro j good
  by_cases same : E.rootOf j = E.rootOf i
  · have old := h.roots j good
    rw [same] at old
    simp only [SharedAlias.prepare, SharedAlias.setRoot, same, Function.update_self, old]
  · simpa only [SharedAlias.prepare, SharedAlias.setRoot, Function.update_of_ne same] using h.roots j good

theorem cancel_congr {m} {I : Interface m} {E : Environment I}
    {C D : SharedAlias.State I} (h : SameGoodState E C D) (i : Fin m) (k : I.Command) :
    SameGoodState E (SharedAlias.cancelAck E C i k) (SharedAlias.cancelAck E D i k) := by
  refine ⟨h.epoch, h.pending, h.acks, h.certificates, ?_, h.plant, ?_⟩
  · simp only [SharedAlias.cancelAck, h.cancelAcks]
  · intro j good
    by_cases goodI : Good E.labelConfig i
    · by_cases same : E.rootOf j = E.rootOf i
      · have old := h.roots j good
        rw [same] at old
        simp only [SharedAlias.cancelAck, if_pos goodI, same, Function.update_self, old]
      · simpa only [SharedAlias.cancelAck, if_pos goodI, Function.update_of_ne same] using h.roots j good
    · simpa only [SharedAlias.cancelAck, if_neg goodI] using h.roots j good

theorem acknowledge_congr {m} {I : Interface m} {E : Environment I}
    {C D : SharedAlias.State I} (h : SameGoodState E C D) (i : Fin m) :
    SameGoodState E (SharedAlias.acknowledge E C i) (SharedAlias.acknowledge E D i) := by
  refine ⟨h.epoch, h.pending, ?_, h.certificates, h.cancelAcks, h.plant, ?_⟩
  · simp only [SharedAlias.acknowledge, h.acks]
  · intro j good
    by_cases goodI : Good E.labelConfig i
    · by_cases same : E.rootOf j = E.rootOf i
      · have old := h.roots j good
        rw [same] at old
        simp only [SharedAlias.acknowledge, if_pos goodI, same, Function.update_self, old, h.epoch]
      · simpa only [SharedAlias.acknowledge, if_pos goodI, Function.update_of_ne same] using h.roots j good
    · simpa only [SharedAlias.acknowledge, if_neg goodI] using h.roots j good

theorem request_congr {m} {I : Interface m} {E : Environment I}
    {C D : SharedAlias.State I} (h : SameGoodState E C D) :
    SameGoodState E (SharedAlias.request C) (SharedAlias.request D) :=
  ⟨h.epoch, rfl, rfl, h.certificates, h.cancelAcks, h.plant, h.roots⟩

theorem complete_congr {m} {I : Interface m} {E : Environment I}
    {C D : SharedAlias.State I} (h : SameGoodState E C D) :
    SameGoodState E (SharedAlias.complete C) (SharedAlias.complete D) := by
  refine ⟨congrArg (· + 1) h.epoch, rfl, rfl, ?_, h.cancelAcks, h.plant, h.roots⟩
  simp only [SharedAlias.complete, h.certificates, h.epoch, h.acks]

theorem deliver_congr {m} {I : Interface m} {E : Environment I}
    {C D : SharedAlias.State I} (h : SameGoodState E C D) (i : Fin m) (epoch : Nat) :
    SameGoodState E (SharedAlias.deliver E C i epoch) (SharedAlias.deliver E D i epoch) := by
  have fieldC : ∀ (X : SharedAlias.State I),
      (SharedAlias.deliver E X i epoch).epoch = X.epoch ∧
      (SharedAlias.deliver E X i epoch).pending = X.pending ∧
      (SharedAlias.deliver E X i epoch).acks = X.acks ∧
      (SharedAlias.deliver E X i epoch).certificates = X.certificates ∧
      (SharedAlias.deliver E X i epoch).cancelAcks = X.cancelAcks ∧
      (SharedAlias.deliver E X i epoch).plant = X.plant := by
    intro X; unfold SharedAlias.deliver; split <;> exact ⟨rfl,rfl,rfl,rfl,rfl,rfl⟩
  obtain ⟨ce, cp, ca, cc, ck, cpl⟩ := fieldC C
  obtain ⟨de, dp, da, dc, dk, dpl⟩ := fieldC D
  refine ⟨ce.trans (h.epoch.trans de.symm), cp.trans (h.pending.trans dp.symm),
    ca.trans (h.acks.trans da.symm), cc.trans (h.certificates.trans dc.symm),
    ck.trans (h.cancelAcks.trans dk.symm), cpl.trans (h.plant.trans dpl.symm), ?_⟩
  intro j good
  by_cases same : E.rootOf j = E.rootOf i
  · have old := h.roots j good
    rw [same] at old
    simp only [SharedAlias.deliver, old]
    split
    · simp only [SharedAlias.setRoot, same, Function.update_self, old]
    · exact h.roots j good
  · unfold SharedAlias.deliver
    split <;> split <;>
      simpa only [SharedAlias.setRoot, Function.update_of_ne same] using h.roots j good

theorem lands_congr {m} {I : Interface m} {E : Environment I}
    {C D : SharedAlias.State I} (h : SameGoodState E C D)
    (time : Nat) (k : I.Command) (who : I.Requester) :
    SharedAlias.Lands E C time k who ↔ SharedAlias.Lands E D time k who := by
  constructor
  · intro allowed
    refine ⟨allowed.1, ?_⟩
    intro i selected good
    simpa only [h.plant, h.roots i good] using allowed.2 i selected good
  · intro allowed
    refine ⟨allowed.1, ?_⟩
    intro i selected good
    simpa only [h.plant, h.roots i good] using allowed.2 i selected good

theorem land_congr {m} {I : Interface m} {E : Environment I}
    {C D : SharedAlias.State I} (h : SameGoodState E C D) (k : I.Command) :
    SameGoodState E (SharedAlias.land C k) (SharedAlias.land D k) :=
  ⟨h.epoch, h.pending, h.acks, h.certificates, h.cancelAcks,
    congrArg (fun p => I.effect p k) h.plant, h.roots⟩

/-- Same genuine event can be serviced after finite bad-store changes; there is
no new event, synthetic acknowledgement or weakened local grant condition. -/
theorem step_transport {m} {I : Interface m} {E : Environment I}
    {C D X : SharedAlias.State I} {event : Event I} (h : SameGoodState E C X)
    (step : SharedAlias.Step E C event D) :
    ∃ Y, SharedAlias.Step E X event Y ∧ SameGoodState E D Y := by
  cases step with
  | request idle => exact ⟨_, .request X (h.pending.symm.trans idle), request_congr h⟩
  | acknowledge i pending => exact ⟨_, .acknowledge X i (h.pending.symm.trans pending), acknowledge_congr h i⟩
  | complete pending quorum =>
      exact ⟨_, .complete X (h.pending.symm.trans pending) (by simpa only [h.acks] using quorum), complete_congr h⟩
  | deliver i epoch certificate =>
      exact ⟨_, .deliver X i epoch (by simpa only [h.epoch] using certificate), deliver_congr h i epoch⟩
  | prepare i k who time selected valid grant =>
      refine ⟨_, .prepare X i k who time selected valid ?_, prepare_congr h i k⟩
      by_cases good : Good E.labelConfig i
      · right
        rcases grant with bad | allowed
        · exact False.elim (good bad)
        · simpa only [h.plant, h.roots i good] using allowed
      · exact Or.inl (not_not.mp good)
  | cancelAck i k who selected auth => exact ⟨_, .cancelAck X i k who selected auth, cancel_congr h i k⟩
  | close k certificate => exact ⟨_, .close X k (by simpa only [h.cancelAcks] using certificate), h⟩
  | land k who time admitted => exact ⟨_, .land X k who time ((lands_congr h time k who).mp admitted), land_congr h k⟩
  | hold => exact ⟨_, .hold X, h⟩
  | corrupt i z bad =>
      refine ⟨_, .corrupt X i z bad, ?_⟩
      exact (corrupt_preserves E C i z bad).symm.trans (h.trans (corrupt_preserves E X i z bad))

/-- Source gate Boolean is insensitive to bad store contents, including on
paths which mix good and bad labels. Its one badOpen Boolean is unchanged. -/
theorem applied_congr {m} {E : Environment (interface m)}
    {C D : SharedAlias.State (interface m)} (h : SameGoodState E C D)
    (k : BoundedEnvelope m) (who : String) (time : Nat) (badOpen : Bool) :
    applied E C k who time badOpen = applied E D k who time badOpen := by
  have gates : ∀ j ∈ k.val.path,
      ComposedExecution.gateOpen (SharedAlias.Typed.gateWorld E C time) k.val who badOpen j =
      ComposedExecution.gateOpen (SharedAlias.Typed.gateWorld E D time) k.val who badOpen j := by
    intro j member
    have bound := k.property.2 j member
    let i : Fin m := ⟨j,bound⟩
    by_cases good : Good E.labelConfig i
    · have clean := (good_iff E i).mp good
      have roots := h.roots i good
      simp only [ComposedExecution.gateOpen, SharedAlias.Typed.gateWorld, dif_pos bound]
      simp only [show E.rootOf ⟨j,bound⟩ ∉ E.actualFaults from clean, decide_false, Bool.false_eq_true, if_false]
      rw [show C.roots (E.rootOf ⟨j,bound⟩) = D.roots (E.rootOf ⟨j,bound⟩) from roots, h.plant]
    · have bad : E.rootOf i ∈ E.actualFaults := by
        by_contra clean; exact good ((good_iff E i).mpr clean)
      simp [ComposedExecution.gateOpen, SharedAlias.Typed.gateWorld, bound, bad, i]
  have allEq :
      k.val.path.all (ComposedExecution.gateOpen (SharedAlias.Typed.gateWorld E C time) k.val who badOpen) =
      k.val.path.all (ComposedExecution.gateOpen (SharedAlias.Typed.gateWorld E D time) k.val who badOpen) := by
    apply Bool.eq_iff_iff.mpr
    simp only [List.all_eq_true]
    constructor
    · intro all j hj; rw [← gates j hj]; exact all j hj
    · intro all j hj; rw [gates j hj]; exact all j hj
  have validEq : ComposedExecution.validPath (SharedAlias.Typed.gateWorld E C time) k.val =
      ComposedExecution.validPath (SharedAlias.Typed.gateWorld E D time) k.val := rfl
  simp only [applied, ComposedExecution.attempt, allEq, validEq]
  split <;> rfl


/-- One authorized environmental rewrite of a fixed lifetime-bad root. -/
structure Corruption {m} {I : Interface m} (E : Environment I) where
  label : Fin m
  value : RootState I
  bad : label ∈ E.labelConfig.faulty

def corruptList {m} {I : Interface m} (E : Environment I) :
    SharedAlias.State I → List (Corruption E) → SharedAlias.State I
  | C, [] => C
  | C, c :: rest => corruptList E (SharedAlias.setRoot C (E.rootOf c.label) c.value) rest

def corruptEvents {m} {I : Interface m} {E : Environment I} (cs : List (Corruption E)) :
    List (Event I) := cs.map (fun c => .corrupt c.label c.value)

theorem corruptList_trace {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (cs : List (Corruption E)) :
    SharedAlias.Trace E C (corruptEvents cs) (corruptList E C cs) := by
  induction cs generalizing C with
  | nil => exact .nil _
  | cons c cs ih => exact .cons (.corrupt C c.label c.value c.bad) (ih _)

theorem corruptList_preserves {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (cs : List (Corruption E)) :
    SameGoodState E C (corruptList E C cs) := by
  induction cs generalizing C with
  | nil => exact SameGoodState.refl E C
  | cons c cs ih => exact (corrupt_preserves E C c.label c.value c.bad).trans (ih _)

/-- Without a bound on inserted rewrites, raw event delay remains arbitrarily
large even when every event is a legal bad-root action rather than hold. -/
theorem arbitrary_corruption_delay {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (c : Corruption E) (n : Nat) :
    ∃ events D, SharedAlias.Trace E C events D ∧ events.length = n ∧ D.plant = C.plant := by
  refine ⟨corruptEvents (List.replicate n c), corruptList E C (List.replicate n c),
    corruptList_trace E C _, ?_, ?_⟩
  · simp [corruptEvents]
  · exact (corruptList_preserves E C _).plant.symm

/-- A finite insertion schedule has one possibly-empty corruption block before
each prescribed service event and a final block. Nothing bounds block lengths. -/
inductive Weave {m} {I : Interface m} (E : Environment I) :
    List (Event I) → List (Event I) → Nat → Prop where
  | finish (cs : List (Corruption E)) : Weave E [] (corruptEvents cs) cs.length
  | next (cs : List (Corruption E)) (event : Event I) {service actual : List (Event I)} {count : Nat}
      (tail : Weave E service actual count) :
      Weave E (event :: service) (corruptEvents cs ++ event :: actual) (cs.length + count)

def eraseCorrupt {m} {I : Interface m} : List (Event I) → List (Event I)
  | [] => []
  | .corrupt _ _ :: rest => eraseCorrupt rest
  | event :: rest => event :: eraseCorrupt rest

theorem eraseCorrupt_append {m} {I : Interface m} (xs ys : List (Event I)) :
    eraseCorrupt (xs ++ ys) = eraseCorrupt xs ++ eraseCorrupt ys := by
  induction xs with
  | nil => rfl
  | cons event xs ih => cases event <;> simp [eraseCorrupt, ih]

theorem eraseCorrupt_block {m} {I : Interface m} {E : Environment I} (cs : List (Corruption E)) :
    eraseCorrupt (corruptEvents cs) = [] := by
  induction cs with
  | nil => rfl
  | cons c cs ih => simpa only [corruptEvents, List.map_cons, eraseCorrupt] using ih

theorem weave_erases {m} {I : Interface m} {E : Environment I}
    {service actual : List (Event I)} {count : Nat} (w : Weave E service actual count) :
    eraseCorrupt actual = eraseCorrupt service := by
  induction w with
  | finish cs => exact eraseCorrupt_block cs
  | next cs event tail ih =>
      rw [eraseCorrupt_append, eraseCorrupt_block, List.nil_append]
      cases event <;> simp only [eraseCorrupt, ih]

theorem weave_length {m} {I : Interface m} {E : Environment I}
    {service actual : List (Event I)} {count : Nat} (w : Weave E service actual count) :
    actual.length = service.length + count := by
  induction w with
  | finish cs => simp [corruptEvents]
  | next cs event tail ih => simp [corruptEvents, ih]; omega

/-- Actual prescribed event trace survives every finite bad-store insertion
schedule. The resulting endpoint preserves all common state and every good
store, including plant. This is not a proof about infinite service starvation. -/
theorem finite_weave_transport {m} {I : Interface m} {E : Environment I}
    {C D X : SharedAlias.State I} {service actual : List (Event I)} {count : Nat}
    (trace : SharedAlias.Trace E C service D) (related : SameGoodState E C X)
    (weave : Weave E service actual count) :
    ∃ Y, SharedAlias.Trace E X actual Y ∧ SameGoodState E D Y := by
  induction weave generalizing C D X with
  | finish cs =>
      cases trace
      exact ⟨_, corruptList_trace E X cs, related.trans (corruptList_preserves E X cs)⟩
  | next cs event tail ih =>
      cases trace with
      | cons first rest =>
          have before := related.trans (corruptList_preserves E X cs)
          obtain ⟨middle, transported, same⟩ := step_transport before first
          obtain ⟨Y, last, final⟩ := ih rest same
          exact ⟨Y, trace_append (corruptList_trace E X cs) (.cons transported last), final⟩

theorem step_deterministic {m} {I : Interface m} {E : Environment I}
    {C D F : SharedAlias.State I} {event : Event I}
    (left : SharedAlias.Step E C event D) (right : SharedAlias.Step E C event F) : D = F := by
  cases left <;> cases right <;> rfl

theorem trace_deterministic {m} {I : Interface m} {E : Environment I}
    {C D F : SharedAlias.State I} {events : List (Event I)}
    (left : SharedAlias.Trace E C events D) (right : SharedAlias.Trace E C events F) : D = F := by
  induction left generalizing F with
  | nil => cases right; rfl
  | cons first rest ih =>
      cases right with
      | cons other tail =>
          have middle := step_deterministic first other
          cases middle
          exact ih tail

/-- Universal erasure: every actual trace realizing a finite insertion schedule
has the same good-state endpoint, not merely some chosen successful execution. -/
theorem finite_weave_erasure {m} {I : Interface m} {E : Environment I}
    {C D X Y : SharedAlias.State I} {service actual : List (Event I)} {count : Nat}
    (reference : SharedAlias.Trace E C service D) (related : SameGoodState E C X)
    (weave : Weave E service actual count) (realized : SharedAlias.Trace E X actual Y) :
    SameGoodState E D Y := by
  obtain ⟨Z, transported, endpoint⟩ := finite_weave_transport reference related weave
  have same := trace_deterministic transported realized
  simpa only [same] using endpoint

/-- Corruptions count separately. The 259 bound remains the serviced core
length; finitely inserted adversarial rewrites add their exact count. -/
theorem progress_with_finite_bad_rewrites {m} {I : Interface m} (E : Environment I)
    (C D : SharedAlias.State I) (service : List (Event I)) (next : I.Plant)
    (trace : SharedAlias.Trace E C service D) (done : D.plant = next)
    (actual : List (Event I)) (count : Nat) (weave : Weave E service actual count) :
    ∃ final, SharedAlias.Trace E C actual final ∧ final.plant = next ∧
      actual.length = service.length + count := by
  obtain ⟨final, actualTrace, related⟩ := finite_weave_transport trace (SameGoodState.refl E C) weave
  exact ⟨final, actualTrace, related.plant.symm.trans done, weave_length weave⟩

/-- Guarded preparation decisions really are unchanged; transport does not
silently choose a different service branch after a bad-store corruption. -/
theorem prepareAllowed_congr {m} {I : Interface m} {E : Environment I}
    {C D : SharedAlias.State I} (h : SameGoodState E C D)
    (i : Fin m) (k : I.Command) (who : I.Requester) (time : Nat) (badReply : Bool) :
    prepareAllowed E C i k who time badReply ↔ prepareAllowed E D i k who time badReply := by
  by_cases good : Good E.labelConfig i
  · simp only [prepareAllowed, if_pos good, h.plant, h.roots i good]
  · simp only [prepareAllowed, if_neg good]

theorem prepareSlot_congr {m} {I : Interface m} {E : Environment I}
    {C D : SharedAlias.State I} (h : SameGoodState E C D)
    (i : Fin m) (k : I.Command) (who : I.Requester) (time : Nat) (badReply : Bool) :
    SameGoodState E (prepareSlot E C i k who time badReply) (prepareSlot E D i k who time badReply) := by
  have allowed := prepareAllowed_congr h i k who time badReply
  unfold prepareSlot
  by_cases left : prepareAllowed E C i k who time badReply
  · rw [if_pos left, if_pos (allowed.mp left)]
    exact prepare_congr h i k
  · rw [if_neg left, if_neg (fun right => left (allowed.mpr right))]
    exact h

theorem cancelSlot_congr {m} {I : Interface m} {E : Environment I}
    {C D : SharedAlias.State I} (h : SameGoodState E C D)
    (i : Fin m) (k : I.Command) (who : I.Requester) (badReply : Bool) :
    SameGoodState E (cancelSlot E C i k who badReply) (cancelSlot E D i k who badReply) := by
  unfold cancelSlot
  split
  · exact cancel_congr h i k
  · exact h

theorem attemptSlot_congr {m} {E : Environment (interface m)}
    {C D : SharedAlias.State (interface m)} (h : SameGoodState E C D)
    (k : BoundedEnvelope m) (who : String) (time : Nat) (badOpen : Bool) :
    SameGoodState E (attemptSlot E C k who time badOpen) (attemptSlot E D k who time badOpen) := by
  unfold attemptSlot
  rw [applied_congr h k who time badOpen]
  split
  · exact land_congr h k
  · exact h

theorem syncSlot_congr {m} {I : Interface m} {E : Environment I}
    {C D : SharedAlias.State I} (h : SameGoodState E C D) (epoch : Nat)
    (respond : Fin m → Bool) (i : Fin m) :
    SameGoodState E (syncSlot E epoch respond C i) (syncSlot E epoch respond D i) := by
  unfold syncSlot
  split
  · exact deliver_congr h i epoch
  · exact h


/-- Concrete uniform source fixture combined with the erasure theorem, so no
successful trace is supplied by the caller. Actor/world/replies stay fixed;
only finite bad-store rewrite blocks are added between completed service slots. -/
theorem uniform_installation_with_finite_bad_rewrites
    (E : Environment (interface 7)) (q : E.q = 5)
    (source0 : E.source 0 = Witness.Fixture.source 0)
    (badSync : Fin 7 → Bool) (bad : Nat → Replies 7) :
    ∃ specs service,
      compile Witness.actor Witness.action sevenPaths Witness.times bad = some specs ∧
      specs.length = 21 ∧ service.length = 259 ∧
      SharedAlias.Trace E (SharedAlias.initial E Witness.Fixture.before) service
        (run E (actorSynchronize E Witness.actor badSync (SharedAlias.initial E Witness.Fixture.before))
          Witness.actor.identity specs) ∧
      ∀ actual added, Weave E service actual added →
        ∃ final, SharedAlias.Trace E (SharedAlias.initial E Witness.Fixture.before) actual final ∧
          final.plant = Witness.Fixture.installed ∧ actual.length = 259 + added := by
  obtain ⟨specs, service, compiled, count, trace, length, done⟩ :=
    Witness.uniform_unknown_world_installation E q source0 badSync bad
  refine ⟨specs, service, compiled, count, length, trace, ?_⟩
  intro actual added weave
  obtain ⟨final, actualTrace, endpoint, size⟩ := progress_with_finite_bad_rewrites E _ _ service _ trace done actual added weave
  exact ⟨final, actualTrace, endpoint, by simpa only [length] using size⟩

/-- The no-desired-success-premise fixture also has a universal conclusion over
all realized finite weaves, with unchanged source authority/service contract. -/
theorem every_woven_installation_has_exact_effect
    (E : Environment (interface 7)) (q : E.q = 5)
    (source0 : E.source 0 = Witness.Fixture.source 0)
    (badSync : Fin 7 → Bool) (bad : Nat → Replies 7) :
    ∃ specs service,
      compile Witness.actor Witness.action sevenPaths Witness.times bad = some specs ∧
      specs.length = 21 ∧ service.length = 259 ∧
      SharedAlias.Trace E (SharedAlias.initial E Witness.Fixture.before) service
        (run E (actorSynchronize E Witness.actor badSync (SharedAlias.initial E Witness.Fixture.before))
          Witness.actor.identity specs) ∧
      ∀ actual added final, Weave E service actual added →
        SharedAlias.Trace E (SharedAlias.initial E Witness.Fixture.before) actual final →
          final.plant = Witness.Fixture.installed ∧ actual.length = 259 + added := by
  obtain ⟨specs, service, compiled, count, trace, length, done⟩ :=
    Witness.uniform_unknown_world_installation E q source0 badSync bad
  refine ⟨specs, service, compiled, count, length, trace, ?_⟩
  intro actual added final weave realized
  have related := finite_weave_erasure trace (SameGoodState.refl E _) weave realized
  exact ⟨related.plant.symm.trans done, by simpa only [length] using weave_length weave⟩

end
end SharedAlias.Progress.BadStore
