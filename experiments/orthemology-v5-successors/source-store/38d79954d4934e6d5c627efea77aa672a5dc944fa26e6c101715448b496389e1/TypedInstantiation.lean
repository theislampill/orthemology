import JoinTrace
import Composition

namespace OperationalJoin.Typed
noncomputable section
open Classical
open ComposedExecution

/-- The ordered path remains inside the complete command identity. Its separate
well-formedness proof prevents a Finset abstraction dropping malformed entries. -/
abbrev BoundedEnvelope (n : Nat) :=
  {e : ComposedExecution.Envelope // e.path.Nodup ∧ ∀ i ∈ e.path, i < n}

def path {n} (e : BoundedEnvelope n) : Finset (Fin n) :=
  Finset.univ.filter (fun i => i.val ∈ e.val.path)

@[simp] theorem mem_path {n} (e : BoundedEnvelope n) (i : Fin n) :
    i ∈ path e ↔ i.val ∈ e.val.path := by simp [path]

theorem path_card {n} (e : BoundedEnvelope n) : (path e).card = e.val.path.length := by
  have image : (path e).image Fin.val = e.val.path.toFinset := by
    ext i
    simp only [Finset.mem_image, mem_path, List.mem_toFinset]
    constructor
    · rintro ⟨j, hj, eq⟩
      simpa [← eq] using hj
    · intro hi
      exact ⟨⟨i, e.property.2 i hi⟩, hi, rfl⟩
  calc
    (path e).card = ((path e).image Fin.val).card := by
      symm
      exact Finset.card_image_of_injective _ Fin.val_injective
    _ = e.val.path.toFinset.card := congrArg Finset.card image
    _ = e.val.path.length := List.toFinset_card_of_nodup e.property.1

def interface (n : Nat) : Interface n where
  Policy := ComposedExecution.Policy
  Command := BoundedEnvelope n
  Plant := ComposedExecution.Plant
  Requester := String
  policyEpoch := ComposedExecution.Policy.epoch
  commandEpoch := fun e => e.val.action.epoch
  commandPath := path
  recipient := fun e => e.val.action.actor
  admits := fun p time policy e requester =>
    requester = e.val.action.actor ∧ localStep p policy time e.val.action = some e.val.successor
  effect := fun _ e => e.val.successor
  admitted_epoch := by
    intro p time policy e requester h
    exact local_action_epoch p policy time e.val.action e.val.successor h.2
  admitted_requester := by intro p time policy e requester h; exact h.1

/-- Representation ignores repetition/order of root memory lists, which the
compiled gates observe only by membership; it does not quotient envelopes. -/
def RootRepresents {n} (r : ComposedExecution.Root) (z : RootState (interface n)) : Prop :=
  z.descriptor = r.policy ∧
  (∀ epoch, epoch ∈ z.revoked ↔ epoch ∈ r.revoked) ∧
  (∀ e : BoundedEnvelope n, e ∈ z.commitments ↔ e.val ∈ r.commitments) ∧
  (∀ e : BoundedEnvelope n, e ∈ z.cancelled ↔ e.val ∈ r.cancelled)

def memory {n} (es : List ComposedExecution.Envelope) : Finset (BoundedEnvelope n) :=
  let valid : Finset ComposedExecution.Envelope :=
    es.toFinset.filter (fun e => e.path.Nodup ∧ ∀ i ∈ e.path, i < n)
  valid.attach.image (fun e : {x // x ∈ valid} =>
    (⟨e.val, (Finset.mem_filter.mp e.property).2⟩ : BoundedEnvelope n))

@[simp] theorem mem_memory {n} (es : List ComposedExecution.Envelope) (e : BoundedEnvelope n) :
    e ∈ memory es ↔ e.val ∈ es := by
  unfold memory
  constructor
  · intro h
    obtain ⟨raw, _, eq⟩ := Finset.mem_image.mp h
    have valEq := congrArg Subtype.val eq
    have member := (Finset.mem_filter.mp raw.property).1
    rw [valEq] at member
    exact List.mem_toFinset.mp member
  · intro h
    let raw : {x // x ∈ es.toFinset.filter
        (fun x => x.path.Nodup ∧ ∀ i ∈ x.path, i < n)} :=
      ⟨e.val, Finset.mem_filter.mpr ⟨List.mem_toFinset.mpr h, e.property⟩⟩
    apply Finset.mem_image.mpr
    refine ⟨raw, by simp, ?_⟩
    apply Subtype.ext
    rfl

def rootView {n} (r : ComposedExecution.Root) : RootState (interface n) :=
  ⟨r.policy, r.revoked.toFinset, memory r.commitments, memory r.cancelled⟩

theorem rootView_represents {n} (r : ComposedExecution.Root) :
    RootRepresents r (rootView (n := n) r) := by
  refine ⟨rfl, ?_, ?_, ?_⟩
  · intro epoch; exact List.mem_toFinset
  · intro e; exact mem_memory r.commitments e
  · intro e; exact mem_memory r.cancelled e

theorem root_gate_iff {n} (p : ComposedExecution.Plant) (time : Nat)
    (r : ComposedExecution.Root) (z : RootState (interface n))
    (representation : RootRepresents r z) (e : BoundedEnvelope n) (requester : String) :
    Permits p time z e requester ↔ rootPermits p time r e.val requester = true := by
  obtain ⟨policy, revoked, committed, cancelled⟩ := representation
  simp only [Permits, Envelope, interface]
  rw [committed, policy, revoked, cancelled]
  simp [rootPermits, Eligible, and_assoc, and_left_comm, and_comm]

theorem valid_path_iff {n} (c : Config (interface n)) (w : ComposedExecution.World)
    (roots : w.n = n) (quorum : w.q = c.q) (e : BoundedEnvelope n) :
    ValidPath c e ↔ validPath w e.val = true := by
  simp only [ValidPath, interface, path_card, validPath, decide_eq_true_eq]
  rw [roots, quorum]
  exact ⟨fun h => ⟨e.property.1, h, e.property.2⟩, fun h => h.2.1⟩

/-- A compiled successful attempt supplies the exact well-formedness witness. -/
theorem attempted_path_well_formed (w : ComposedExecution.World)
    (e : ComposedExecution.Envelope) (requester : String) (badOpen : Bool)
    (applied : (attempt w e requester badOpen).2 = true) :
    e.path.Nodup ∧ e.path.length = w.q ∧ ∀ i ∈ e.path, i < w.n := by
  unfold attempt at applied
  split at applied
  · rename_i guard
    have parts : validPath w e = true ∧ e.path.all (gateOpen w e requester badOpen) = true :=
      by simpa only [Bool.and_eq_true] using guard
    exact of_decide_eq_true parts.1
  · cases applied

/-- A snapshot relation, not a claim that every compiled macro operation
has already been simulated by common primitive events. -/
structure RuntimeRepresents {n} (c : Config (interface n))
    (w : ComposedExecution.World) (s : State (interface n)) : Prop where
  root_count : w.n = n
  quorum : w.q = c.q
  actual_plant : w.plant = s.plant
  taint : ∀ i : Fin n, w.tainted i.val = false ↔ Good c i
  roots : ∀ i : Fin n, RootRepresents (w.roots i.val) (s.roots i)

/-- The compiled Bool branch, path check and each exact local gate are consumed.
False/withheld bad gates may add rejection; no independent per-root bad choices
are silently substituted for the runtime's single badOpen Boolean. -/
theorem successful_attempt_lands {n} {c : Config (interface n)}
    (w : ComposedExecution.World) (s : State (interface n))
    (representation : RuntimeRepresents c w s) (e : BoundedEnvelope n)
    (requester : String) (badOpen : Bool)
    (applied : (attempt w e.val requester badOpen).2 = true) :
    Lands c s w.now e requester := by
  have wf := attempted_path_well_formed w e.val requester badOpen applied
  refine ⟨?_, ?_⟩
  · change (path e).card = c.q
    rw [path_card, wf.2.1, representation.quorum]
  · intro i selected good
    have onPath : decide (i.val ∈ e.val.path) = true := decide_eq_true (mem_path e i |>.mp selected)
    have actualLands := attempt_applied_implies_lands w e.val requester badOpen applied
    have opened := actualLands i.val (by rw [representation.root_count]; exact i.isLt) onPath
    have honest := (representation.taint i).mpr good
    simp only [gateOpen, honest, Bool.false_eq_true, if_false] at opened
    apply (root_gate_iff s.plant w.now (w.roots i.val) (s.roots i)
      (representation.roots i) e requester).mpr
    simpa only [representation.actual_plant] using opened

/-- When the same shared badOpen value opens faulty gates, the live compiled
attempt and common Lands are extensionally equivalent at represented snapshots. -/
theorem open_attempt_iff_lands {n} {c : Config (interface n)}
    (w : ComposedExecution.World) (s : State (interface n))
    (representation : RuntimeRepresents c w s) (e : BoundedEnvelope n) (requester : String) :
    (attempt w e.val requester true).2 = true ↔ Lands c s w.now e requester := by
  constructor
  · exact successful_attempt_lands w s representation e requester true
  · intro lands
    have pathValid := (valid_path_iff c w representation.root_count representation.quorum e).mp lands.1
    have allOpen : e.val.path.all (gateOpen w e.val requester true) = true := by
      apply List.all_eq_true.mpr
      intro j selected
      have bounded : j < n := e.property.2 j selected
      let i : Fin n := ⟨j, bounded⟩
      cases faulty : w.tainted j with
      | true => simp [gateOpen, faulty]
      | false =>
          have good : Good c i := (representation.taint i).mp faulty
          have permitted := lands.2 i ((mem_path e i).mpr selected) good
          have opened := (root_gate_iff s.plant w.now (w.roots j) (s.roots i)
            (representation.roots i) e requester).mp permitted
          simpa [gateOpen, faulty, representation.actual_plant] using opened
    simp [attempt, pathValid, allOpen]

/-- Exact full successor correspondence at a genuinely reached common state.
The common damage classifier is proved inactive, rather than used as a gate. -/
theorem successful_attempt_exact_effect {n} {c : Config (interface n)}
    (w : ComposedExecution.World) (s : State (interface n))
    (representation : RuntimeRepresents c w s) (reachable : Reachable c s)
    (safe : s.damaged = false) (e : BoundedEnvelope n) (requester : String) (badOpen : Bool)
    (applied : (attempt w e.val requester badOpen).2 = true) :
    (attempt w e.val requester badOpen).1.plant =
      (land c s w.now e requester).plant ∧
    (land c s w.now e requester).plant = e.val.successor := by
  have lands := successful_attempt_lands w s representation e requester badOpen applied
  have admitted := (admitted_current_authorized (reachable_consistent reachable)
    w.now e requester lands).2.2
  have effect : (land c s w.now e requester).plant = e.val.successor := by
    have noDamage : ¬(s.damaged = true ∨
        ¬(interface n).admits s.plant w.now (c.source s.epoch) e requester) := by
      simp only [safe, Bool.false_eq_true, false_or, not_not]
      exact admitted
    rw [land, if_neg noDamage]
    rfl
  exact ⟨(applied_attempt_exact_successor w e.val requester badOpen applied).trans effect.symm, effect⟩

/-- Arbitrary finite typed histories derive current full-policy admission from
local policy storage and durable certificate history, with no current oracle. -/
theorem finite_history_compiled_admission {n} (c : Config (interface n))
    (initialPlant : ComposedExecution.Plant) {s : State (interface n)}
    {events : List (Event (interface n))}
    (history : Trace c (Initial c initialPlant) events s)
    (time : Nat) (e : BoundedEnvelope n) (requester : String)
    (admitted : Lands c s time e requester) :
    requester = e.val.action.actor ∧ e.val.action.epoch = s.epoch ∧
      localStep s.plant (c.source s.epoch) time e.val.action = some e.val.successor := by
  obtain ⟨req, epoch, _, step⟩ := finite_history_admission c initialPlant history time e requester admitted
  exact ⟨req, epoch, step⟩

theorem finite_history_install_effect {n} (c : Config (interface n))
    (initialPlant : ComposedExecution.Plant) {s : State (interface n)}
    {events : List (Event (interface n))}
    (history : Trace c (Initial c initialPlant) events s)
    (time : Nat) (e : BoundedEnvelope n) (requester : String)
    (admitted : Lands c s time e requester)
    (command : CriterionInstallation.InstallCommand) (kind : e.val.action = .install command) :
    e.val.successor = { s.plant with
      rule := .exact
      ruleVersion := s.plant.ruleVersion + 1
      ruleHistory := s.plant.ruleHistory ++ [s.plant.rule] } := by
  have step := (finite_history_compiled_admission c initialPlant history time e requester admitted).2.2
  rw [kind] at step
  exact local_install_full_effect _ _ _ _ _ step

theorem finite_history_repair_effect {n} (c : Config (interface n))
    (initialPlant : ComposedExecution.Plant) {s : State (interface n)}
    {events : List (Event (interface n))}
    (history : Trace c (Initial c initialPlant) events s)
    (time : Nat) (e : BoundedEnvelope n) (requester : String)
    (admitted : Lands c s time e requester)
    (command : TypedCriterionGuard.Command) (kind : e.val.action = .repair command) :
    e.val.successor = { s.plant with
      draft := s.plant.source.content
      draftRevision := s.plant.draftRevision + 1
      draftHistory := s.plant.draftHistory ++ [s.plant.draft] } := by
  have step := (finite_history_compiled_admission c initialPlant history time e requester admitted).2.2
  rw [kind] at step
  exact local_repair_full_effect _ _ _ _ _ step

theorem finite_history_goals_persist {n} {c : Config (interface n)} {s t : State (interface n)}
    {events : List (Event (interface n))} (reachable : Reachable c s)
    (safe : s.damaged = false) (goals : Goals s.plant) (history : Trace c s events t) :
    Goals t.plant := by
  apply trace_preserves Goals ?_ (reachable_consistent reachable) safe goals history
  intro p time policy e requester admitted old
  exact local_goals_persist p policy time e.val.action e.val.successor admitted.2 old

/-- No literal full-state idempotence is claimed. The exact imported effect
still increments one version/history coordinate on every fresh valid action. -/
theorem admitted_action_cannot_repeat {n} (p : ComposedExecution.Plant)
    (time : Nat) (policy : ComposedExecution.Policy) (e : BoundedEnvelope n)
    (requester : String) (admitted : (interface n).admits p time policy e requester)
    (laterPolicy : ComposedExecution.Policy) (laterTime : Nat) :
    localStep e.val.successor laterPolicy laterTime e.val.action = none :=
  fixed_action_cannot_succeed_twice p policy time e.val.action e.val.successor
    admitted.2 laterPolicy laterTime

#print axioms path_card
#print axioms root_gate_iff
#print axioms finite_history_compiled_admission
#print axioms finite_history_install_effect
#print axioms finite_history_repair_effect
#print axioms finite_history_goals_persist
end
end OperationalJoin.Typed
