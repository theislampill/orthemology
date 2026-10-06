import NativeHistory

namespace SharedAlias.Native
open ComposedExecution
open OperationalJoin.Typed (BoundedEnvelope interface)

/-- Unlike tableRead, a missing policy is represented as none, never a default. -/
def tableFind {α β : Type} [DecidableEq α] : List (α × β) → α → Option β
  | [], _ => none
  | (key, value) :: rest, query => if query = key then some value else tableFind rest query

/-- Publicly sampled finite policy data. Key/epoch consistency is executable;
authenticity to an external authority is an independent history premise. -/
def policySample (rows : List (Nat × Policy)) (epoch : Nat) : Option Policy := do
  let policy ← tableFind rows epoch
  if policy.epoch = epoch then some policy else none

/-- A finite history request may name an epoch without embedding its policy.
Resolution below must obtain that payload from the explicit finite input. -/
inductive HistoryRequest (m : Nat) where
  | request
  | acknowledge (i : Fin m)
  | complete
  | deliver (i : Fin m) (epoch : Nat)
  | prepare (i : Fin m) (k : BoundedEnvelope m) (who : String) (time : Nat)
  | cancelAck (i : Fin m) (k : BoundedEnvelope m) (who : String)
  | close (k : BoundedEnvelope m)
  | land (k : BoundedEnvelope m) (who : String) (time : Nat)
  | hold
  | corrupt (i : Fin m) (root : Root)

def resolveInput {m} (samples : List (Nat × Policy)) : HistoryRequest m → Option (HistoryInput m)
  | .request => some .request
  | .acknowledge i => some (.acknowledge i)
  | .complete => some .complete
  | .deliver i epoch => (policySample samples epoch).map (HistoryInput.deliver i)
  | .prepare i k who time => some (.prepare i k who time)
  | .cancelAck i k who => some (.cancelAck i k who)
  | .close k => some (.close k)
  | .land k who time => some (.land k who time)
  | .hold => some .hold
  | .corrupt i z => some (.corrupt i z)

def resolveHistory {m} (samples : List (Nat × Policy)) :
    List (HistoryRequest m) → Option (List (HistoryInput m))
  | [] => some []
  | event :: rest => do
      let first ← resolveInput samples event
      let later ← resolveHistory samples rest
      pure (first :: later)

/-- Callable finite-data constructor. There is no Environment/source argument.
It refuses a missing/wrong-epoch initial or delivery policy sample. It replays
already accepted histories only; it does not verify legal authority by itself. -/
def reconstruct {m} (D : Routing m) (p : Plant) (samples : List (Nat × Policy))
    (history : List (HistoryRequest m)) : Option (FiniteState m) := do
  let policy ← policySample samples 0
  let inputs ← resolveHistory samples history
  pure (replayHistory D (initial policy p) inputs)

@[simp] theorem policySample_missing (epoch : Nat) : policySample [] epoch = none := rfl

theorem policySample_wrong_epoch (key : Nat) (policy : Policy) (wrong : policy.epoch ≠ key) :
    policySample [(key, policy)] key = none := by
  simp [policySample, tableFind, wrong]

theorem policySample_exact (epoch : Nat) (policy : Policy) (same : policy.epoch = epoch) :
    policySample [(epoch, policy)] epoch = some policy := by
  simp [policySample, tableFind, same]

theorem missing_delivery_refused {m} (i : Fin m) (epoch : Nat) :
    resolveInput [] (.deliver i epoch) = none := rfl

theorem incomplete_history_refused {m} (samples : List (Nat × Policy)) (i : Fin m) (epoch : Nat)
    (rest : List (HistoryRequest m)) (missing : policySample samples epoch = none) :
    resolveHistory samples (.deliver i epoch :: rest) = none := by
  simp [resolveHistory, resolveInput, missing]

theorem missing_initial_refused {m} (D : Routing m) (p : Plant)
    (history : List (HistoryRequest m)) : reconstruct D p [] history = none := rfl

theorem wrong_initial_refused {m} (D : Routing m) (p : Plant)
    (policy : Policy) (history : List (HistoryRequest m)) (wrong : policy.epoch ≠ 0) :
    reconstruct D p [(0, policy)] history = none := by
  simp [reconstruct, policySample_wrong_epoch 0 policy wrong]

/-- Executable constructor success supplies the actual resolved finite inputs;
it neither invents nor queries missing policy payloads. -/
theorem reconstruct_success_iff {m} (D : Routing m) (p : Plant)
    (samples : List (Nat × Policy)) (history : List (HistoryRequest m)) (C : FiniteState m) :
    reconstruct D p samples history = some C ↔
      ∃ policy inputs, policySample samples 0 = some policy ∧
        resolveHistory samples history = some inputs ∧
        replayHistory D (initial policy p) inputs = C := by
  unfold reconstruct
  cases policy : policySample samples 0 with
  | none => simp [policy]
  | some value =>
      cases inputs : resolveHistory samples history with
      | none => simp [policy, inputs]
      | some values => simp [policy, inputs]

/-- Erase sampled policy payloads to explicit expected epochs. -/
def HistoryInput.skeleton {m} : HistoryInput m → HistoryRequest m
  | .request => .request
  | .acknowledge i => .acknowledge i
  | .complete => .complete
  | .deliver i policy => .deliver i policy.epoch
  | .prepare i k who time => .prepare i k who time
  | .cancelAck i k who => .cancelAck i k who
  | .close k => .close k
  | .land k who time => .land k who time
  | .hold => .hold
  | .corrupt i z => .corrupt i z

/-- A finite collection of the payloads already supplied in a reified history.
No opaque source function is read by this executable collector. -/
def collectPolicies {m} : List (HistoryInput m) → List (Nat × Policy)
  | [] => []
  | .deliver _ policy :: rest => (policy.epoch, policy) :: collectPolicies rest
  | _ :: rest => collectPolicies rest

def sampleHistory {m} (initialPolicy : Policy) (inputs : List (HistoryInput m)) : List (Nat × Policy) :=
  (0, initialPolicy) :: collectPolicies inputs

theorem tableFind_consistent {α β : Type} [DecidableEq α] (rows : List (α × β))
    (key : α) (value : β) (present : (key, value) ∈ rows)
    (consistent : ∀ row ∈ rows, row.1 = key → row.2 = value) :
    tableFind rows key = some value := by
  induction rows with
  | nil => cases present
  | cons row rows ih =>
      by_cases same : key = row.1
      · have val := consistent row (by simp) same.symm
        simp only [tableFind, if_pos same, val]
      · have later : (key, value) ∈ rows := by
          rcases List.mem_cons.mp present with head | tail
          · exact False.elim (same (congrArg Prod.fst head))
          · exact tail
        simpa only [tableFind, if_neg same] using ih later
          (fun x member => consistent x (List.mem_cons_of_mem row member))

theorem collectPolicies_member {m} (inputs : List (HistoryInput m)) (i : Fin m) (policy : Policy)
    (member : HistoryInput.deliver i policy ∈ inputs) :
    (policy.epoch, policy) ∈ collectPolicies inputs := by
  induction inputs with
  | nil => cases member
  | cons input rest ih =>
      rcases List.mem_cons.mp member with rfl | later
      · simp [collectPolicies]
      · cases input <;> simp only [collectPolicies]
        all_goals first | exact ih later | exact List.mem_cons_of_mem _ (ih later)

theorem resolveHistory_of_resolved_inputs {m} (samples : List (Nat × Policy))
    (inputs : List (HistoryInput m))
    (resolved : ∀ input ∈ inputs, resolveInput samples input.skeleton = some input) :
    resolveHistory samples (inputs.map HistoryInput.skeleton) = some inputs := by
  induction inputs with
  | nil => rfl
  | cons input inputs ih =>
      simp only [List.map_cons, resolveHistory, resolved input (by simp), Option.bind_some,
        ih (fun x member => resolved x (List.mem_cons_of_mem input member)), pure]
      rfl

noncomputable section
open Classical

theorem collected_policies_authentic {m} (E : SharedAlias.Environment (interface m))
    (inputs : List (HistoryInput m)) (authentic : ∀ input ∈ inputs, input.Authentic E) :
    ∀ row ∈ collectPolicies inputs, row.2 = E.source row.1 := by
  induction inputs with
  | nil => simp [collectPolicies]
  | cons input inputs ih =>
      have rest := ih (fun x member => authentic x (List.mem_cons_of_mem input member))
      cases input <;> simp only [collectPolicies]
      all_goals try exact rest
      rename_i label policy
      intro row member
      rcases List.mem_cons.mp member with rfl | later
      · exact authentic (.deliver label policy) (List.mem_cons_self)
      · exact rest row later

theorem sampleHistory_authentic {m} (E : SharedAlias.Environment (interface m))
    (inputs : List (HistoryInput m)) (authentic : ∀ input ∈ inputs, input.Authentic E) :
    ∀ row ∈ sampleHistory (E.source 0) inputs, row.2 = E.source row.1 := by
  intro row member
  rcases List.mem_cons.mp member with rfl | later
  · rfl
  · exact collected_policies_authentic E inputs authentic row later

theorem authentic_sample_present {m} (E : SharedAlias.Environment (interface m))
    (rows : List (Nat × Policy))
    (authentic : ∀ row ∈ rows, row.2 = E.source row.1)
    (epoch : Nat) (present : (epoch, E.source epoch) ∈ rows) :
    policySample rows epoch = some (E.source epoch) := by
  have found := tableFind_consistent rows epoch (E.source epoch) present (by
    intro row member same
    simpa only [same] using authentic row member)
  simp [policySample, found, source_epoch_value]

theorem collected_samples_resolve {m} (E : SharedAlias.Environment (interface m))
    (inputs : List (HistoryInput m)) (authentic : ∀ input ∈ inputs, input.Authentic E) :
    policySample (sampleHistory (E.source 0) inputs) 0 = some (E.source 0) ∧
      resolveHistory (sampleHistory (E.source 0) inputs) (inputs.map HistoryInput.skeleton) = some inputs := by
  have samplesAuth := sampleHistory_authentic E inputs authentic
  constructor
  · exact authentic_sample_present E _ samplesAuth 0 (by simp [sampleHistory])
  · apply resolveHistory_of_resolved_inputs
    intro input member
    cases input <;> try rfl
    rename_i i policy
    have auth : policy = E.source policy.epoch := authentic _ member
    have present : (policy.epoch, E.source policy.epoch) ∈ sampleHistory (E.source 0) inputs := by
      apply List.mem_cons_of_mem
      have found := collectPolicies_member inputs i policy member
      simpa only [← auth] using found
    have value := authentic_sample_present E _ samplesAuth policy.epoch present
    simp only [resolveInput, HistoryInput.skeleton, value, Option.map_some, ← auth]
    rfl

/-- A checked finite replay agrees with the independently supplied accepted
history endpoint. That endpoint is not defined to be the replay result. -/
theorem reconstruct_from_accepted {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (p : Plant) (samples : List (Nat × Policy))
    (history : List (HistoryRequest m)) (policy : Policy) (inputs : List (HistoryInput m))
    (initialSample : policySample samples 0 = some policy)
    (initialAuthentic : policy = E.source 0)
    (resolved : resolveHistory samples history = some inputs)
    (authentic : ∀ input ∈ inputs, input.Authentic E)
    (next : SharedAlias.State (interface m))
    (accepted : SharedAlias.Trace E (SharedAlias.initial E p)
      (inputs.map HistoryInput.event) next) :
    ∃ native, reconstruct D p samples history = some native ∧ view native = next := by
  refine ⟨replayHistory D (initial policy p) inputs,
    (reconstruct_success_iff D p samples history _).mpr
      ⟨policy, inputs, initialSample, resolved, rfl⟩, ?_⟩
  apply replay_accepted_history_exact D E matchD _ inputs authentic
  simpa only [initialAuthentic, initial_view] using accepted

/-- Constructive finite-data coverage of every accepted finite history, once
its policy and raw-root samples are reified. Sampling from E happens only in
this existence proof, never inside the executable constructor. -/
theorem accepted_history_has_checked_constructor {m} (D : Routing m)
    (E : SharedAlias.Environment (interface m)) (matchD : RoutingMatches D E)
    (p : Plant) (events : List (OperationalJoin.Event (interface m)))
    (next : SharedAlias.State (interface m))
    (accepted : SharedAlias.Trace E (SharedAlias.initial E p) events next) :
    ∃ samples requests inputs native,
      resolveHistory samples requests = some inputs ∧
      inputs.map HistoryInput.event = events ∧
      reconstruct D p samples requests = some native ∧
      view native = next ∧ (∀ input ∈ inputs, input.Authentic E) ∧
      (∀ row ∈ samples, row.2 = E.source row.1) := by
  have represented : SharedAlias.Trace E (view (initial (E.source 0) p)) events next := by
    simpa only [initial_view] using accepted
  obtain ⟨inputs, eventsEq, authentic, exactView⟩ :=
    accepted_trace_reifiable D E matchD (initial (E.source 0) p) represented
  obtain ⟨init, resolved⟩ := collected_samples_resolve E inputs authentic
  refine ⟨sampleHistory (E.source 0) inputs, inputs.map HistoryInput.skeleton, inputs,
    replayHistory D (initial (E.source 0) p) inputs, resolved, eventsEq, ?_, exactView,
    authentic, sampleHistory_authentic E inputs authentic⟩
  exact (reconstruct_success_iff D p _ _ _).mpr ⟨E.source 0, inputs, init, resolved, rfl⟩

end
end SharedAlias.Native
