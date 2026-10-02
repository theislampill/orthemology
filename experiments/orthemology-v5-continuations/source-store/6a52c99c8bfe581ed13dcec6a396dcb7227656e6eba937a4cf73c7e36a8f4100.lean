import ObservedPhaseController

noncomputable section
open MeasureTheory
open Orthemology.Tranche2.PolicyEmbedding

namespace HiddenParity.Sufficiency
open HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Necessity HiddenParity.Stage
universe u w
variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

theorem generated_action_safe
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B₀ : Finset Model) (s₀ : State) (fallback : Model) (fallbackAction : Action)
    (reject : Model → ℕ → History (State × Action) State → Bool) (h : History Action State)
    (hLive : (liveHistory P B₀ (augmentHistory s₀ h)).Nonempty)
    (hRegion : observedState s₀ h ∈ winningRegion P menu priority (liveHistory P B₀ (augmentHistory s₀ h)))
    (hMemory : MemoryValid P menu priority fallback (liveHistory P B₀ (augmentHistory s₀ h))
      (observedState s₀ h) (phaseMemory P menu priority B₀ s₀ fallback reject h)) :
    (observedState s₀ h,generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject () h) ∈
      stageActions P menu priority (liveHistory P B₀ (augmentHistory s₀ h)) := by
  let B := liveHistory P B₀ (augmentHistory s₀ h)
  let m := currentMemory P menu priority B₀ s₀ fallback reject h
  have hm : MemoryValid P menu priority fallback B (observedState s₀ h) m :=
    normalizeMemory_valid P menu priority fallback B _ _ hMemory
  have hActive := valid_activePairs P menu priority fallback B hLive _ hRegion m hm
  apply hActive.1
  apply (mem_retainedActions _ _ _).mp
  exact cycleAction_mem _ fallbackAction (retainedActions_nonempty _ _ hActive.2) _

/-- Complete feasible-history invariant for the actual generated policy. Both
all-branch region membership and stored target validity are derived recursively. -/
theorem generated_history_invariant
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B₀ : Finset Model) (s₀ : State) (hs₀ : s₀ ∈ winningRegion P menu priority B₀)
    (fallback : Model) (fallbackAction : Action)
    (reject : Model → ℕ → History (State × Action) State → Bool) (h : History Action State)
    (hLive : (liveHistory P B₀ (augmentHistory s₀ h)).Nonempty)
    (hComp : ActionCompatible
      (pairPolicy s₀ (generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject)) ()
      (augmentHistory s₀ h)) :
    observedState s₀ h ∈ winningRegion P menu priority (liveHistory P B₀ (augmentHistory s₀ h)) ∧
    MemoryValid P menu priority fallback (liveHistory P B₀ (augmentHistory s₀ h))
      (observedState s₀ h) (phaseMemory P menu priority B₀ s₀ fallback reject h) := by
  induction h with
  | nil =>
      refine ⟨?_,?_⟩
      · simpa only [augmentHistory,liveHistory_nil,observedState] using hs₀
      · intro E he; cases he
  | cons ey h ih =>
      obtain ⟨a,y⟩ := ey
      let B := liveHistory P B₀ (augmentHistory s₀ h)
      let C := liveHistory P B₀ (augmentHistory s₀ ((a,y)::h))
      have hCB : C ⊆ B := by
        change liveHistory P B₀ (((observedState s₀ h,a),y)::augmentHistory s₀ h) ⊆ _
        rw [liveHistory_cons]
        exact Finset.filter_subset _ _
      have hB : B.Nonempty := hLive.mono hCB
      have hTail := ih hB hComp.1
      have hAction : generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject () h = a := by
        have ha := congrArg Prod.snd hComp.2
        simpa only [pairPolicy,augmentHistory_erase] using ha
      have he : (observedState s₀ h,a) ∈ stageActions P menu priority B := by
        rw [← hAction]
        exact generated_action_safe P menu priority B₀ s₀ fallback fallbackAction reject h hB hTail.1 hTail.2
      have hCeq : C = liveUpdate P B (observedState s₀ h,a) y := by
        exact liveHistory_cons P B₀ (augmentHistory s₀ h) (observedState s₀ h,a) y
      have hy : y ∈ winningRegion P menu priority C := by
        rw [hCeq]
        exact stageActions_successor P menu priority B _ he y (hCeq ▸ hLive)
      refine ⟨hy,?_⟩
      exact advanceMemory_valid P menu priority fallback B C (observedState s₀ h) y _ _
        (normalizeMemory_valid P menu priority fallback B _ _ hTail.2)

/-- The controller is lawful for every rejection test, including arbitrary
false positives. Safe all-branch menus prevent testing decisions from bypassing
hard legality or the computed child-region requirement. -/
theorem generatedPhasePolicy_lawful
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B₀ : Finset Model) (s₀ : State) (hs₀ : s₀ ∈ winningRegion P menu priority B₀)
    (fallback : Model) (fallbackAction : Action)
    (reject : Model → ℕ → History (State × Action) State → Bool) :
    Lawful P menu B₀ s₀ (generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject)
      (Measure.dirac ()) := by
  intro h hLive
  apply ae_of_all
  intro r hComp
  cases r
  have hAug := augmentHistory_compatible s₀
    (generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject) () h hComp
  have hInv := generated_history_invariant P menu priority B₀ s₀ hs₀ fallback fallbackAction reject
    (erasePairSources h) (by simpa only [hAug] using hLive) (by simpa only [hAug] using hComp)
  have hSafe := generated_action_safe P menu priority B₀ s₀ fallback fallbackAction reject
    (erasePairSources h) (by simpa only [hAug] using hLive) hInv.1 hInv.2
  have hMem := (mem_regionAllowed P menu (liveHistory P B₀ (augmentHistory s₀ (erasePairSources h)))
    _ _ _).mp hSafe
  simpa only [hAug,observedState_erase,pairPolicy] using hMem.2.1

end HiddenParity.Sufficiency
