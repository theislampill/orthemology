import NativeOrderedProgram
import NativeServiceOrder

namespace SharedAlias.Native
open ComposedExecution
open OperationalJoin.Typed (BoundedEnvelope interface)

/-- Recover the bounded labels in the exact order stored in this command.
No Finset.toList or hidden routing input is used. -/
def commandLabels {m} (k : BoundedEnvelope m) : List (Fin m) :=
  k.val.path.attach.map (fun item => ⟨item.val, k.property.2 item.val item.property⟩)

structure Outcome (m : Nat) where
  state : FiniteState m
  events : List (OperationalJoin.Event (interface m))

/-- One slot emits one genuine accepted primitive event (possibly hold). -/
def serviceLoop {m} (handler : FiniteState m → Fin m →
    FiniteState m × OperationalJoin.Event (interface m)) :
    FiniteState m → List (Fin m) → Outcome m
  | C, [] => ⟨C, []⟩
  | C, i :: rest =>
      let first := handler C i
      let later := serviceLoop handler first.1 rest
      ⟨later.state, first.2 :: later.events⟩

def prepareRun {m} (D : Routing m) (C : FiniteState m) (k : BoundedEnvelope m)
    (who : String) (a : Annotation m) : Outcome m :=
  serviceLoop (fun C i =>
    (prepareSlot D C i k who a.time (prepareReply a i),
     prepareEvent D C i k who a.time (prepareReply a i))) C (commandLabels k)

def cancelRun {m} (D : Routing m) (C : FiniteState m) (k : BoundedEnvelope m)
    (who : String) (a : Annotation m) : Outcome m :=
  serviceLoop (fun C i =>
    (cancelSlot D C i k who (cancelReply a i),
     cancelEvent D i k who (cancelReply a i))) C (commandLabels k)

def trialRun {m} (D : Routing m) (C : FiniteState m) (who : String) (spec : NativeSpec m) : Outcome m :=
  let prep := prepareRun D C spec.command who spec.annotation
  let landed := attemptSlot D prep.state spec.command who spec.annotation.time spec.annotation.openGate
  let event := attemptEvent D prep.state spec.command who spec.annotation.time spec.annotation.openGate
  let cancel := cancelRun D landed spec.command who spec.annotation
  ⟨cancel.state, prep.events ++ event :: (cancel.events ++ [closeEvent D cancel.state spec.command])⟩

/-- The controller deliberately services every fixed public trial. It does
not trust a success receipt or inspect the hidden environment to choose paths. -/
def runNative {m} (D : Routing m) (who : String) : FiniteState m → List (NativeSpec m) → Outcome m
  | C, [] => ⟨C, []⟩
  | C, spec :: rest =>
      let first := trialRun D C who spec
      let later := runNative D who first.state rest
      ⟨later.state, first.events ++ later.events⟩

noncomputable section
open Classical

theorem commandLabels_values {m} (k : BoundedEnvelope m) :
    (commandLabels k).map Fin.val = k.val.path := by
  simp [commandLabels, List.map_map, Function.comp_def]

theorem commandLabels_nodup {m} (k : BoundedEnvelope m) : (commandLabels k).Nodup := by
  have mapped : ((commandLabels k).map Fin.val).Nodup := by
    rw [commandLabels_values]
    exact k.property.1
  exact List.Nodup.of_map Fin.val mapped

theorem mem_commandLabels {m} (k : BoundedEnvelope m) (i : Fin m) :
    i ∈ commandLabels k ↔ i.val ∈ k.val.path := by
  unfold commandLabels
  constructor
  · intro member
    obtain ⟨item, _, same⟩ := List.mem_map.mp member
    have values := congrArg Fin.val same
    simpa only [← values] using item.property
  · intro member
    apply List.mem_map.mpr
    refine ⟨⟨i.val, member⟩, by simp, ?_⟩
    exact Fin.ext rfl

theorem commandLabels_finset {m} (k : BoundedEnvelope m) :
    (commandLabels k).toFinset = OperationalJoin.Typed.path k := by
  ext i
  simp only [List.mem_toFinset, mem_commandLabels, OperationalJoin.Typed.mem_path]

theorem commandLabels_permutation {m} (k : BoundedEnvelope m) :
    (commandLabels k).Perm (OperationalJoin.Typed.path k).toList := by
  apply List.perm_of_nodup_nodup_toFinset_eq (commandLabels_nodup k) (Finset.nodup_toList _)
  simp only [commandLabels_finset, Finset.toList_toFinset]

theorem serviceLoop_trace {m} (E : SharedAlias.Environment (interface m))
    (handler : FiniteState m → Fin m → FiniteState m × OperationalJoin.Event (interface m))
    (legal : ∀ C i, SharedAlias.Step E (view C) (handler C i).2 (view (handler C i).1))
    (C : FiniteState m) (labels : List (Fin m)) :
    SharedAlias.Trace E (view C) (serviceLoop handler C labels).events
      (view (serviceLoop handler C labels).state) := by
  induction labels generalizing C with
  | nil => exact .nil _
  | cons i labels ih => exact .cons (legal C i) (ih (handler C i).1)

theorem serviceLoop_length {m}
    (handler : FiniteState m → Fin m → FiniteState m × OperationalJoin.Event (interface m))
    (C : FiniteState m) (labels : List (Fin m)) :
    (serviceLoop handler C labels).events.length = labels.length := by
  induction labels generalizing C with
  | nil => rfl
  | cons i labels ih => simpa only [serviceLoop, List.length_cons] using congrArg Nat.succ (ih (handler C i).1)

theorem serviceLoop_refines {m}
    (handler : FiniteState m → Fin m → FiniteState m × OperationalJoin.Event (interface m))
    (reference : SharedAlias.Progress.Service (interface m))
    (exactState : ∀ C i, view (handler C i).1 = reference (view C) i)
    (C : FiniteState m) (labels : List (Fin m)) :
    view (serviceLoop handler C labels).state = SharedAlias.Progress.serviceList reference (view C) labels := by
  induction labels generalizing C with
  | nil => rfl
  | cons i labels ih =>
      simpa only [serviceLoop, SharedAlias.Progress.serviceList, exactState] using ih (handler C i).1

theorem prepareRun_exact {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (C : FiniteState m) (k : BoundedEnvelope m)
    (who : String) (a : Annotation m) :
    view (prepareRun D C k who a).state =
      SharedAlias.Progress.preparePath E (view C) k who a.time (prepareReply a) := by
  unfold prepareRun
  rw [serviceLoop_refines _ (fun S i => SharedAlias.Progress.prepareSlot E S i k who a.time (prepareReply a i))
    (fun C i => prepare_refines D E matchD C i k who a.time (prepareReply a i))]
  exact prepare_service_permutation E (view C) k who a.time (prepareReply a) _ _ (commandLabels_permutation k)

theorem cancelRun_exact {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (C : FiniteState m) (k : BoundedEnvelope m)
    (who : String) (a : Annotation m) :
    view (cancelRun D C k who a).state =
      SharedAlias.Progress.cancelPath E (view C) k who (cancelReply a) := by
  unfold cancelRun
  rw [serviceLoop_refines _ (fun S i => SharedAlias.Progress.cancelSlot E S i k who (cancelReply a i))
    (fun C i => cancel_refines D E matchD C i k who (cancelReply a i))]
  exact cancel_service_permutation E (view C) k who (cancelReply a) _ _ (commandLabels_permutation k)

def modelReplies {m} (a : Annotation m) : SharedAlias.Progress.Replies m :=
  ⟨prepareReply a, a.openGate, cancelReply a⟩
def modelSpec {m} (s : NativeSpec m) : SharedAlias.Progress.TrialSpec m :=
  ⟨s.command, s.annotation.time, modelReplies s.annotation⟩

theorem trialRun_exact {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (C : FiniteState m) (who : String) (s : NativeSpec m) :
    view (trialRun D C who s).state =
      SharedAlias.Progress.trial E (view C) s.command who s.annotation.time (modelReplies s.annotation) := by
  simp only [trialRun, cancelRun_exact D E matchD, attempt_exact_reference D E matchD,
    prepareRun_exact D E matchD, SharedAlias.Progress.trial, modelReplies]

theorem runNative_exact {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (C : FiniteState m) (who : String) (specs : List (NativeSpec m)) :
    view (runNative D who C specs).state = SharedAlias.Progress.run E (view C) who (specs.map modelSpec) := by
  induction specs generalizing C with
  | nil => rfl
  | cons s specs ih =>
      simp only [runNative, List.map_cons, SharedAlias.Progress.run, modelSpec]
      rw [ih, trialRun_exact D E matchD]

theorem trialRun_trace {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (C : FiniteState m) (who : String) (s : NativeSpec m) :
    SharedAlias.Trace E (view C) (trialRun D C who s).events (view (trialRun D C who s).state) := by
  have prep := serviceLoop_trace E
    (fun C i => (prepareSlot D C i s.command who s.annotation.time (prepareReply s.annotation i),
      prepareEvent D C i s.command who s.annotation.time (prepareReply s.annotation i)))
    (fun C i => prepare_emitted_step D E matchD C i s.command who s.annotation.time (prepareReply s.annotation i))
    C (commandLabels s.command)
  have attempt := attempt_emitted_step D E matchD (prepareRun D C s.command who s.annotation).state
    s.command who s.annotation.time s.annotation.openGate
  have cancel := serviceLoop_trace E
    (fun C i => (cancelSlot D C i s.command who (cancelReply s.annotation i),
      cancelEvent D i s.command who (cancelReply s.annotation i)))
    (fun C i => cancel_emitted_step D E matchD C i s.command who (cancelReply s.annotation i))
    (attemptSlot D (prepareRun D C s.command who s.annotation).state s.command who
      s.annotation.time s.annotation.openGate) (commandLabels s.command)
  have closing := close_emitted_step D E matchD (trialRun D C who s).state s.command
  exact SharedAlias.Progress.trace_append prep (.cons attempt
    (SharedAlias.Progress.trace_append cancel (.cons closing (.nil _))))

theorem runNative_trace {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (C : FiniteState m) (who : String) (specs : List (NativeSpec m)) :
    SharedAlias.Trace E (view C) (runNative D who C specs).events (view (runNative D who C specs).state) := by
  induction specs generalizing C with
  | nil => exact .nil _
  | cons s specs ih =>
      exact SharedAlias.Progress.trace_append (trialRun_trace D E matchD C who s)
        (ih (trialRun D C who s).state)


theorem commandLabels_length {m} (k : BoundedEnvelope m) :
    (commandLabels k).length = k.val.path.length := by
  simpa only [List.length_map] using congrArg List.length (commandLabels_values k)

theorem trialRun_length {m} (D : Routing m) (C : FiniteState m) (who : String) (s : NativeSpec m) :
    (trialRun D C who s).events.length = 2 * s.command.val.path.length + 2 := by
  simp only [trialRun, prepareRun, cancelRun, List.length_append, List.length_cons,
    List.length_nil, serviceLoop_length, commandLabels_length]
  omega

theorem runNative_length {m} (D : Routing m) (C : FiniteState m) (who : String)
    (specs : List (NativeSpec m)) (q : Nat)
    (uniform : ∀ s ∈ specs, s.command.val.path.length = q) :
    (runNative D who C specs).events.length = specs.length * (2*q+2) := by
  induction specs generalizing C with
  | nil => simp [runNative]
  | cons s specs ih =>
      simp only [runNative, List.length_append, trialRun_length, uniform s (by simp),
        ih (trialRun D C who s).state (fun x member => uniform x (List.mem_cons_of_mem s member)),
        List.length_cons, Nat.add_mul, Nat.one_mul]
      omega

theorem trialRun_really_closed {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (C : FiniteState m) (who : String) (s : NativeSpec m)
    (valid : OperationalJoin.ValidPath E.labelConfig s.command)
    (auth : who = s.command.val.action.actor) :
    closed D (trialRun D C who s).state s.command = true := by
  apply (closed_iff D E matchD _ s.command).mpr
  rw [trialRun_exact D E matchD]
  exact SharedAlias.Progress.cancelPath_closes E _ s.command who (cancelReply s.annotation) valid auth

/-- Reuse accepted progress only with these SAME complete new commands.
No selected-set argument changes any command already stored in memory. -/
theorem runNative_progress {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (C : FiniteState m) (who : String) (specs : List (NativeSpec m))
    (policy : Policy) (next : Plant)
    (valid : ∀ s ∈ specs, OperationalJoin.ValidPath E.labelConfig s.command)
    (auth : ∀ s ∈ specs, who = s.command.val.action.actor)
    (successors : ∀ s ∈ specs, s.command.val.successor = next)
    (fresh : specs.Pairwise (fun a b => a.command ≠ b.command))
    (clear : ∀ s ∈ specs, SharedAlias.Progress.Clear E (view C) s.command policy)
    (work : ∀ s ∈ specs, ComposedExecution.localStep C.plant policy s.annotation.time s.command.val.action =
      some s.command.val.successor)
    (hit : ∃ s ∈ specs, ∀ i ∈ OperationalJoin.Typed.path s.command, OperationalJoin.Good E.labelConfig i) :
    (runNative D who C specs).state.plant = next := by
  have target := SharedAlias.Progress.run_progress E (view C) who (specs.map modelSpec) policy next
  have valid' : ∀ s ∈ specs.map modelSpec, OperationalJoin.ValidPath E.labelConfig s.command := by
    intro s member; obtain ⟨x, hx, rfl⟩ := List.mem_map.mp member; exact valid x hx
  have auth' : ∀ s ∈ specs.map modelSpec, who = s.command.val.action.actor := by
    intro s member; obtain ⟨x, hx, rfl⟩ := List.mem_map.mp member; exact auth x hx
  have successors' : ∀ s ∈ specs.map modelSpec, s.command.val.successor = next := by
    intro s member; obtain ⟨x, hx, rfl⟩ := List.mem_map.mp member; exact successors x hx
  have fresh' : (specs.map modelSpec).Pairwise (fun a b => a.command ≠ b.command) := by
    exact List.pairwise_map.mpr fresh
  have clear' : ∀ s ∈ specs.map modelSpec, SharedAlias.Progress.Clear E (view C) s.command policy := by
    intro s member; obtain ⟨x, hx, rfl⟩ := List.mem_map.mp member; exact clear x hx
  have work' : ∀ s ∈ specs.map modelSpec,
      ComposedExecution.localStep (view C).plant policy s.time s.command.val.action = some s.command.val.successor := by
    intro s member; obtain ⟨x, hx, rfl⟩ := List.mem_map.mp member; exact work x hx
  have hit' : ∃ s ∈ specs.map modelSpec,
      ∀ i ∈ OperationalJoin.Typed.path s.command, OperationalJoin.Good E.labelConfig i := by
    obtain ⟨s, member, good⟩ := hit
    exact ⟨modelSpec s, List.mem_map.mpr ⟨s, member, rfl⟩, good⟩
  have done := target valid' auth' successors' fresh' clear' work' hit'
  have exactState := congrArg SharedAlias.State.plant (runNative_exact D E matchD C who specs)
  exact exactState.trans done

end
end SharedAlias.Native
