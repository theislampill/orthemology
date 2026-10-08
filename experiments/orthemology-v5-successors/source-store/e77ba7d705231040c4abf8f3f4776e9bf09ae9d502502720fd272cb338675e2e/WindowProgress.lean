import SharedAuthority

namespace SharedAlias.Progress
open OperationalJoin
open OperationalJoin.Typed (interface BoundedEnvelope)
noncomputable section
open Classical

/-- A reference service clock, not wall-clock latency. Each scheduled trial
uses one common sampled time for its local checks; trial times do not go back.
All requested slots still require their explicit bounded completion contract. -/
structure ServiceClock (observed lo hi count : Nat) (times : Nat → Nat) : Prop where
  monotone : Monotone times
  after_observation : ∀ n < count, observed ≤ times n
  in_window : ∀ n < count, lo ≤ times n ∧ times n ≤ hi

/-- End-to-end conditional progress from a reachable idle shared state. Actor,
action and public paths are fixed before the hidden world. It is unnecessary
to read either the map or faulty-root set, and no successful execution is
assumed. Full-window source admission and tombstone freshness are explicit
applicability premises. The protected interpreter permits only its prescribed
service slots, with arbitrary bad replies at those slots. -/
theorem protected_window_progress {m}
    (actor : ComposedExecution.Actor) (action : ComposedExecution.Action)
    (paths : List (Finset (Fin m)))
    (E : Environment (interface m)) (C : SharedAlias.State (interface m))
    (next : ComposedExecution.Plant) (lo hi : Nat)
    (times : Nat → Nat) (badSync : Fin m → Bool) (bad : Nat → Replies m)
    (reach : SharedAlias.Reachable E C) (idle : C.pending = false)
    (observedPlant : actor.observedPlant = C.plant)
    (sourcePolicy : actor.policy = E.source C.epoch)
    (auth : actor.identity = action.actor)
    (observedTime : lo ≤ actor.observedTime ∧ actor.observedTime ≤ hi)
    (clock : ServiceClock actor.observedTime lo hi paths.length times)
    (availableWork : ∀ t, lo ≤ t → t ≤ hi →
      ComposedExecution.localStep C.plant (E.source C.epoch) t action = some next)
    (uniform : ∀ P ∈ paths, P.card = E.q)
    (fresh : ∀ k ∈ publicCommands actor action next 0 paths, ∀ i, Good E.labelConfig i →
      k ∉ (C.roots (E.rootOf i)).cancelled)
    (hit : ∃ P ∈ paths, ∀ i ∈ P, Good E.labelConfig i) :
    ∃ specs events, compile actor action paths times bad = some specs ∧
      specs.length = paths.length ∧
      SharedAlias.Trace E C events (run E (actorSynchronize E actor badSync C) actor.identity specs) ∧
      events.length = m + paths.length * (2 * E.q + 2) ∧
      (run E (actorSynchronize E actor badSync C) actor.identity specs).plant = next := by
  rw [actorSynchronize_eq E actor badSync C sourcePolicy]
  have proposal : ComposedExecution.localStep actor.observedPlant actor.policy actor.observedTime action = some next := by
    simpa only [observedPlant, sourcePolicy] using
      availableWork actor.observedTime observedTime.1 observedTime.2
  have epoch : action.epoch = C.epoch := by
    have same := ComposedExecution.local_action_epoch C.plant (E.source C.epoch)
      actor.observedTime action next (availableWork actor.observedTime observedTime.1 observedTime.2)
    exact same.trans (E.source_epoch C.epoch)
  have clear : ∀ k ∈ publicCommands actor action next 0 paths,
      Clear E (synchronize E badSync C) k actor.policy := by
    intro k member
    have inSpecs : k ∈ (scheduled actor action next times bad 0 paths).map TrialSpec.command := by
      simpa only [scheduled_publicCommands] using member
    obtain ⟨s, hs, same⟩ := List.mem_map.mp inSpecs
    obtain ⟨n, P, _, _, _, cmd, _⟩ := scheduled_member actor action next times bad 0 paths s hs
    have commandEpoch : (interface m).commandEpoch k = C.epoch := by
      rw [← same, cmd]
      exact epoch
    rw [sourcePolicy]
    exact synchronized_clear E badSync C reach idle k commandEpoch (fresh k member)
  have work : ∀ n < paths.length,
      ComposedExecution.localStep (synchronize E badSync C).plant actor.policy (times n) action = some next := by
    intro n hn
    rw [synchronize_plant, sourcePolicy]
    exact availableWork (times n) (clock.in_window n hn).1 (clock.in_window n hn).2
  obtain ⟨specs, compiled, progress, batch, batchTrace, count⟩ :=
    source_controller_progress actor action next paths E (synchronize E badSync C) times bad
      proposal uniform auth clear work hit
  obtain ⟨prelude, preludeTrace, preludeSize⟩ := synchronize_trace E badSync C
  have same : specs = scheduled actor action next times bad 0 paths := by
    rw [compile_eq actor action next paths times bad proposal] at compiled
    exact (Option.some.inj compiled).symm
  exact ⟨specs, prelude ++ batch, compiled, by simp [same],
    trace_append preludeTrace batchTrace, by simp only [List.length_append, preludeSize, count], progress⟩

/-- Seven public labels, five selected per trial: 21 source proposals and 259
serviced reference transitions including the seven-slot synchronization prelude.
The environment must separately satisfy the accepted one-alias-class budget
conditions; the actual map/fault set remains fixed and hidden throughout. -/
theorem seven_protected_window_progress
    (actor : ComposedExecution.Actor) (action : ComposedExecution.Action)
    (E : Environment (interface 7)) (C : SharedAlias.State (interface 7))
    (next : ComposedExecution.Plant) (lo hi : Nat)
    (times : Nat → Nat) (badSync : Fin 7 → Bool) (bad : Nat → Replies 7)
    (q : E.q = 5) (reach : SharedAlias.Reachable E C) (idle : C.pending = false)
    (observedPlant : actor.observedPlant = C.plant)
    (sourcePolicy : actor.policy = E.source C.epoch)
    (auth : actor.identity = action.actor)
    (observedTime : lo ≤ actor.observedTime ∧ actor.observedTime ≤ hi)
    (clock : ServiceClock actor.observedTime lo hi 21 times)
    (availableWork : ∀ t, lo ≤ t → t ≤ hi →
      ComposedExecution.localStep C.plant (E.source C.epoch) t action = some next)
    (fresh : ∀ k ∈ publicCommands actor action next 0 sevenPaths, ∀ i, Good E.labelConfig i →
      k ∉ (C.roots (E.rootOf i)).cancelled) :
    ∃ specs events, compile actor action sevenPaths times bad = some specs ∧
      specs.length = 21 ∧
      SharedAlias.Trace E C events (run E (actorSynchronize E actor badSync C) actor.identity specs) ∧
      events.length = 259 ∧ (run E (actorSynchronize E actor badSync C) actor.identity specs).plant = next := by
  simpa only [sevenPaths_length, q] using
    protected_window_progress actor action sevenPaths E C next lo hi times badSync bad reach idle
      observedPlant sourcePolicy auth observedTime clock availableWork
      (by simpa only [q] using sevenPaths_uniform) fresh (sevenPaths_hit E q)

end
end SharedAlias.Progress
