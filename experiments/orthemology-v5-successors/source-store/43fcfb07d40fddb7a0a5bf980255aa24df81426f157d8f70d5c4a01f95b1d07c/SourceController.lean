import SharedController

namespace SharedAlias.Progress
open OperationalJoin
open OperationalJoin.Typed (interface BoundedEnvelope path mem_path)
noncomputable section
open Classical

/-- Fixed public label ordering; the complete ordered path remains in identity. -/
def labelList {m} (P : Finset (Fin m)) : List Nat := P.toList.map Fin.val

theorem labelList_nodup {m} (P : Finset (Fin m)) : (labelList P).Nodup := by
  exact P.nodup_toList.map Fin.val_injective

theorem labelList_bounded {m} (P : Finset (Fin m)) : ∀ i ∈ labelList P, i < m := by
  intro i member
  obtain ⟨j, _, rfl⟩ := List.mem_map.mp member
  exact j.isLt

def issue {m} (actor : ComposedExecution.Actor) (action : ComposedExecution.Action)
    (next : ComposedExecution.Plant) (n : Nat) (P : Finset (Fin m)) : BoundedEnvelope m :=
  ⟨⟨action, next, actor.nonce + n + 1, labelList P⟩,
    labelList_nodup P, labelList_bounded P⟩

theorem issue_source_proposal {m} (actor : ComposedExecution.Actor)
    (action : ComposedExecution.Action) (next : ComposedExecution.Plant)
    (n : Nat) (P : Finset (Fin m))
    (proposal : ComposedExecution.localStep actor.observedPlant actor.policy actor.observedTime action = some next) :
    ComposedExecution.propose { actor with nonce := actor.nonce + n } action (labelList P) =
      some (issue actor action next n P).val := by
  simp [ComposedExecution.propose, proposal, issue]

@[simp] theorem issue_path {m} (actor : ComposedExecution.Actor)
    (action : ComposedExecution.Action) (next : ComposedExecution.Plant)
    (n : Nat) (P : Finset (Fin m)) : path (issue actor action next n P) = P := by
  ext i
  simp only [mem_path, issue, labelList, List.mem_map, Finset.mem_toList]
  constructor
  · rintro ⟨j, hj, same⟩
    have eq : j = i := Fin.ext same
    simpa only [eq] using hj
  · intro member; exact ⟨i, member, rfl⟩

/-- A finite instruction schedule generated only from public actor inputs.
Time/reply decorations belong to the interpreter and never affect issue order. -/
def scheduled {m} (actor : ComposedExecution.Actor) (action : ComposedExecution.Action)
    (next : ComposedExecution.Plant) (times : Nat → Nat) (bad : Nat → Replies m) :
    Nat → List (Finset (Fin m)) → List (TrialSpec m)
  | _, [] => []
  | n, P :: rest => ⟨issue actor action next n P, times n, bad n⟩ ::
      scheduled actor action next times bad (n + 1) rest

@[simp] theorem scheduled_length {m} (actor : ComposedExecution.Actor)
    (action : ComposedExecution.Action) (next : ComposedExecution.Plant)
    (times : Nat → Nat) (bad : Nat → Replies m) (n : Nat) (paths : List (Finset (Fin m))) :
    (scheduled actor action next times bad n paths).length = paths.length := by
  induction paths generalizing n with
  | nil => rfl
  | cons P paths ih => simp only [scheduled, List.length_cons, ih]

/-- Actual actor-facing program: source proposals and public paths only.
No clock service result, acknowledgement, actual plant, map or fault set is an
argument. The interpreter decorates these instructions after they are fixed. -/
def publicCommands {m} (actor : ComposedExecution.Actor) (action : ComposedExecution.Action)
    (next : ComposedExecution.Plant) : Nat → List (Finset (Fin m)) → List (BoundedEnvelope m)
  | _, [] => []
  | n, P :: rest => issue actor action next n P :: publicCommands actor action next (n + 1) rest

def program {m} (actor : ComposedExecution.Actor) (action : ComposedExecution.Action)
    (paths : List (Finset (Fin m))) : Option (List (BoundedEnvelope m)) :=
  (ComposedExecution.localStep actor.observedPlant actor.policy actor.observedTime action).map
    (fun next => publicCommands actor action next 0 paths)

theorem scheduled_publicCommands {m} (actor : ComposedExecution.Actor)
    (action : ComposedExecution.Action) (next : ComposedExecution.Plant)
    (times : Nat → Nat) (bad : Nat → Replies m) (n : Nat) (paths : List (Finset (Fin m))) :
    (scheduled actor action next times bad n paths).map TrialSpec.command =
      publicCommands actor action next n paths := by
  induction paths generalizing n with
  | nil => rfl
  | cons P paths ih => simp only [scheduled, List.map_cons, publicCommands, ih]

/-- Proof-side service annotation of the fixed public program. Environmental
replies/times decorate instructions but cannot alter command order or content. -/
def compile {m} (actor : ComposedExecution.Actor) (action : ComposedExecution.Action)
    (paths : List (Finset (Fin m))) (times : Nat → Nat) (bad : Nat → Replies m) :
    Option (List (TrialSpec m)) :=
  (ComposedExecution.localStep actor.observedPlant actor.policy actor.observedTime action).map
    (fun next => scheduled actor action next times bad 0 paths)

theorem compile_public_program {m} (actor : ComposedExecution.Actor)
    (action : ComposedExecution.Action) (paths : List (Finset (Fin m)))
    (times : Nat → Nat) (bad : Nat → Replies m) :
    (compile actor action paths times bad).map (List.map TrialSpec.command) =
      program actor action paths := by
  simp only [compile, program, Option.map_map]
  congr 1
  funext next
  exact scheduled_publicCommands actor action next times bad 0 paths

theorem compile_eq {m} (actor : ComposedExecution.Actor) (action : ComposedExecution.Action)
    (next : ComposedExecution.Plant) (paths : List (Finset (Fin m)))
    (times : Nat → Nat) (bad : Nat → Replies m)
    (proposal : ComposedExecution.localStep actor.observedPlant actor.policy actor.observedTime action = some next) :
    compile actor action paths times bad = some (scheduled actor action next times bad 0 paths) := by
  simp [compile, proposal]

theorem scheduled_member {m} (actor : ComposedExecution.Actor)
    (action : ComposedExecution.Action) (next : ComposedExecution.Plant)
    (times : Nat → Nat) (bad : Nat → Replies m) (n : Nat) (paths : List (Finset (Fin m)))
    (s : TrialSpec m) (member : s ∈ scheduled actor action next times bad n paths) :
    ∃ j P, n ≤ j ∧ j < n + paths.length ∧ P ∈ paths ∧
      s.command = issue actor action next j P ∧ s.time = times j := by
  induction paths generalizing n with
  | nil => simp [scheduled] at member
  | cons P paths ih =>
      simp only [scheduled, List.mem_cons] at member
      rcases member with rfl | later
      · exact ⟨n, P, le_rfl, by simp, by simp, rfl, rfl⟩
      · obtain ⟨j, Q, lower, upper, inPaths, cmd, time⟩ := ih (n + 1) later
        exact ⟨j, Q, by omega, by simp only [List.length_cons]; omega,
          List.mem_cons_of_mem P inPaths, cmd, time⟩

theorem scheduled_has_path {m} (actor : ComposedExecution.Actor)
    (action : ComposedExecution.Action) (next : ComposedExecution.Plant)
    (times : Nat → Nat) (bad : Nat → Replies m) (n : Nat) (paths : List (Finset (Fin m)))
    (P : Finset (Fin m)) (member : P ∈ paths) :
    ∃ s ∈ scheduled actor action next times bad n paths, path s.command = P := by
  induction paths generalizing n with
  | nil => simp at member
  | cons Q paths ih =>
      rcases List.mem_cons.mp member with rfl | later
      · exact ⟨_, List.mem_cons_self, issue_path actor action next n P⟩
      · obtain ⟨s, hs, same⟩ := ih (n + 1) later
        exact ⟨s, List.mem_cons_of_mem _ hs, same⟩

theorem scheduled_fresh {m} (actor : ComposedExecution.Actor)
    (action : ComposedExecution.Action) (next : ComposedExecution.Plant)
    (times : Nat → Nat) (bad : Nat → Replies m) (n : Nat) (paths : List (Finset (Fin m))) :
    (scheduled actor action next times bad n paths).Pairwise (fun a b => a.command ≠ b.command) := by
  induction paths generalizing n with
  | nil => exact List.Pairwise.nil
  | cons P paths ih =>
      apply List.pairwise_cons.mpr
      constructor
      · intro s member same
        obtain ⟨j, Q, lower, _, _, cmd, _⟩ := scheduled_member actor action next times bad (n + 1) paths s member
        have nonces := congrArg (fun k : BoundedEnvelope m => k.val.nonce) same
        simp only [cmd, issue] at nonces
        omega
      · exact ih (n + 1)

/-- Full source-proposal progress with externally fixed actor/nonce inputs.
Freshness is an applicability condition; this controller never computes a
maximum by inspecting hidden tombstones. The environmental world E is fixed. -/
theorem source_controller_progress {m} (actor : ComposedExecution.Actor)
    (action : ComposedExecution.Action) (next : ComposedExecution.Plant)
    (paths : List (Finset (Fin m)))
    (E : Environment (interface m)) (C : SharedAlias.State (interface m))
    (times : Nat → Nat) (bad : Nat → Replies m)
    (proposal : ComposedExecution.localStep actor.observedPlant actor.policy actor.observedTime action = some next)
    (uniform : ∀ P ∈ paths, P.card = E.q)
    (auth : actor.identity = action.actor)
    (clear : ∀ k ∈ publicCommands actor action next 0 paths, Clear E C k actor.policy)
    (work : ∀ n < paths.length, ComposedExecution.localStep C.plant actor.policy (times n) action = some next)
    (hit : ∃ P ∈ paths, ∀ i ∈ P, Good E.labelConfig i) :
    ∃ specs, compile actor action paths times bad = some specs ∧
      (run E C actor.identity specs).plant = next ∧
      ∃ events, SharedAlias.Trace E C events (run E C actor.identity specs) ∧
        events.length = paths.length * (2 * E.q + 2) := by
  let specs := scheduled actor action next times bad 0 paths
  have valid : ∀ s ∈ specs, ValidPath E.labelConfig s.command := by
    intro s member
    obtain ⟨n, P, _, _, hP, cmd, _⟩ := scheduled_member actor action next times bad 0 paths s member
    change (path s.command).card = E.q
    rw [cmd, issue_path]
    exact uniform P hP
  have identity : ∀ s ∈ specs, actor.identity = s.command.val.action.actor := by
    intro s member
    obtain ⟨n, P, _, _, _, cmd, _⟩ := scheduled_member actor action next times bad 0 paths s member
    simpa only [cmd, issue] using auth
  refine ⟨specs, compile_eq actor action next paths times bad proposal, ?_, ?_⟩
  · apply run_progress E C actor.identity specs actor.policy next valid identity
    · intro s member
      obtain ⟨n, P, _, _, _, cmd, _⟩ := scheduled_member actor action next times bad 0 paths s member
      simp only [cmd, issue]
    · exact scheduled_fresh actor action next times bad 0 paths
    · intro s member
      apply clear s.command
      rw [← scheduled_publicCommands actor action next times bad 0 paths]
      exact List.mem_map.mpr ⟨s, member, rfl⟩
    · intro s member
      obtain ⟨n, P, _, hn, _, cmd, time⟩ := scheduled_member actor action next times bad 0 paths s member
      simpa only [cmd, issue, time] using work n (by simpa using hn)
    · obtain ⟨P, hP, clean⟩ := hit
      obtain ⟨s, member, support⟩ := scheduled_has_path actor action next times bad 0 paths P hP
      exact ⟨s, member, by simpa only [support] using clean⟩
  · obtain ⟨events, trace, count⟩ := run_trace E C actor.identity specs valid identity
    exact ⟨events, trace, by simpa only [specs, scheduled_length] using count⟩

end
end SharedAlias.Progress
