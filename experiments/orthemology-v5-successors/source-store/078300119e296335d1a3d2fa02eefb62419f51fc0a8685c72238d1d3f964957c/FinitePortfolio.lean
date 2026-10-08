import SourceController

namespace SharedAlias.Progress
open OperationalJoin
open OperationalJoin.Typed (interface BoundedEnvelope path)
noncomputable section
open Classical

/-- Public finite q-path portfolio; no actual-world input is used. -/
def allPaths (m q : Nat) : List (Finset (Fin m)) :=
  (Finset.univ.powersetCard q).toList

theorem allPaths_uniform (m q : Nat) : ∀ P ∈ allPaths m q, P.card = q := by
  intro P member
  exact (Finset.mem_powersetCard.mp (Finset.mem_toList.mp member)).2

@[simp] theorem allPaths_length (m q : Nat) : (allPaths m q).length = m.choose q := by
  simp [allPaths]

/-- This is a fixed-world combinatorial existence fact, not an actor map query. -/
theorem allPaths_hit {m} {I : Interface m} (E : Environment I) :
    ∃ P ∈ allPaths m E.q, ∀ i ∈ P, Good E.labelConfig i := by
  have budget := E.labelConfig.budget_bound
  have available := E.repair_available
  have complement : E.q ≤ (E.labelConfig.faultyᶜ).card := by
    rw [Finset.card_compl]
    simp only [Fintype.card_fin]
    change E.labelConfig.faulty.card ≤ E.labelBudget at budget
    change E.q + E.labelBudget ≤ m at available
    omega
  obtain ⟨P, subset, cardinality⟩ := Finset.exists_subset_card_eq complement
  refine ⟨P, ?_, ?_⟩
  · exact Finset.mem_toList.mpr (Finset.mem_powersetCard.mpr ⟨Finset.subset_univ P, cardinality⟩)
  · intro i member; exact Finset.mem_compl.mp (subset member)

/-- The generic shared reference controller performs at most choose(m,q)
trials; all are deliberately serviced without trusting success receipts. -/
theorem finite_controller_progress {m} (actor : ComposedExecution.Actor)
    (action : ComposedExecution.Action) (next : ComposedExecution.Plant)
    (E : Environment (interface m)) (C : SharedAlias.State (interface m))
    (times : Nat → Nat) (bad : Nat → Replies m)
    (proposal : ComposedExecution.localStep actor.observedPlant actor.policy actor.observedTime action = some next)
    (auth : actor.identity = action.actor)
    (clear : ∀ k ∈ publicCommands actor action next 0 (allPaths m E.q),
      Clear E C k actor.policy)
    (work : ∀ n < m.choose E.q,
      ComposedExecution.localStep C.plant actor.policy (times n) action = some next) :
    ∃ specs, compile actor action (allPaths m E.q) times bad = some specs ∧
      specs.length = m.choose E.q ∧ (run E C actor.identity specs).plant = next ∧
      ∃ events, SharedAlias.Trace E C events (run E C actor.identity specs) ∧
        events.length = m.choose E.q * (2 * E.q + 2) := by
  obtain ⟨specs, compiled, progress, events, trace, count⟩ :=
    source_controller_progress actor action next (allPaths m E.q) E C times bad
      proposal (allPaths_uniform m E.q) auth clear (by simpa using work)
      (allPaths_hit E)
  have same : specs = scheduled actor action next times bad 0 (allPaths m E.q) := by
    rw [compile_eq actor action next (allPaths m E.q) times bad proposal] at compiled
    exact (Option.some.inj compiled).symm
  refine ⟨specs, compiled, ?_, progress, events, trace, ?_⟩
  · simp [same]
  · simpa using count

/-- A concrete public list avoids any reliance on a hidden-world-selected
portfolio. It is the full 7-label/5-label combination schedule. -/
def sevenPaths : List (Finset (Fin 7)) :=
  [{0,1,2,3,4}, {0,1,2,3,5}, {0,1,2,3,6},
   {0,1,2,4,5}, {0,1,2,4,6}, {0,1,2,5,6},
   {0,1,3,4,5}, {0,1,3,4,6}, {0,1,3,5,6}, {0,1,4,5,6},
   {0,2,3,4,5}, {0,2,3,4,6}, {0,2,3,5,6}, {0,2,4,5,6}, {0,3,4,5,6},
   {1,2,3,4,5}, {1,2,3,4,6}, {1,2,3,5,6}, {1,2,4,5,6}, {1,3,4,5,6},
   {2,3,4,5,6}]

theorem sevenPaths_length : sevenPaths.length = 21 := rfl

theorem sevenPaths_exact : sevenPaths.toFinset = Finset.univ.powersetCard 5 := by decide

theorem sevenPaths_uniform : ∀ P ∈ sevenPaths, P.card = 5 := by
  intro P member
  have member' : P ∈ Finset.univ.powersetCard 5 := by
    rw [← sevenPaths_exact]; exact List.mem_toFinset.mpr member
  exact (Finset.mem_powersetCard.mp member').2

theorem sevenPaths_hit (E : Environment (interface 7)) (q : E.q = 5) :
    ∃ P ∈ sevenPaths, ∀ i ∈ P, Good E.labelConfig i := by
  obtain ⟨P, member, good⟩ := allPaths_hit E
  refine ⟨P, ?_, good⟩
  apply List.mem_toFinset.mp
  rw [sevenPaths_exact]
  simpa only [allPaths, q, Finset.mem_toList] using member

/-- The 21/252 constants concern this new shared-store reference program only.
They do not change the accepted source's four-path runBatch implementation. -/
theorem seven_controller_progress (actor : ComposedExecution.Actor)
    (action : ComposedExecution.Action) (next : ComposedExecution.Plant)
    (E : Environment (interface 7)) (C : SharedAlias.State (interface 7))
    (times : Nat → Nat) (bad : Nat → Replies 7) (q : E.q = 5)
    (proposal : ComposedExecution.localStep actor.observedPlant actor.policy actor.observedTime action = some next)
    (auth : actor.identity = action.actor)
    (clear : ∀ k ∈ publicCommands actor action next 0 sevenPaths, Clear E C k actor.policy)
    (work : ∀ n < 21, ComposedExecution.localStep C.plant actor.policy (times n) action = some next) :
    ∃ specs, compile actor action sevenPaths times bad = some specs ∧
      specs.length = 21 ∧ (run E C actor.identity specs).plant = next ∧
      ∃ events, SharedAlias.Trace E C events (run E C actor.identity specs) ∧ events.length = 252 := by
  obtain ⟨specs, compiled, progress, events, trace, count⟩ :=
    source_controller_progress actor action next sevenPaths E C times bad proposal
      (by simpa only [q] using sevenPaths_uniform) auth clear work (sevenPaths_hit E q)
  have same : specs = scheduled actor action next times bad 0 sevenPaths := by
    rw [compile_eq actor action next sevenPaths times bad proposal] at compiled
    exact (Option.some.inj compiled).symm
  exact ⟨specs, compiled, by simp [same, sevenPaths_length], progress, events, trace,
    by simpa only [sevenPaths_length, q] using count⟩

end
end SharedAlias.Progress
