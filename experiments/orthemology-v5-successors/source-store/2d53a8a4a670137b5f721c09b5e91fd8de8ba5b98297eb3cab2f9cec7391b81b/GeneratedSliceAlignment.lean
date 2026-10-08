import RotorHistorySnapshot

noncomputable section
open Orthemology.Tranche2.PolicyEmbedding
namespace HiddenParity.Cost.GeneratedSlice
attribute [local instance] Classical.propDecidable
open HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Adaptive
open HiddenParity.Necessity HiddenParity.Stage
universe u w
variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]
variable (P : RationalKernel Model (State × Action) State)
variable (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
variable (B₀ : Finset Model) (s₀ : State) (fallback : Model) (fallbackAction : Action)
variable (reject : Model → ℕ → History (State × Action) State → Bool)

abbrev policy := generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject

def pair (h : History (State × Action) State) : State × Action :=
  pairPolicy s₀ (policy P menu priority B₀ s₀ fallback fallbackAction reject) () h

def active (h : History (State × Action) State) : Finset (State × Action) :=
  activePairs P menu priority (liveHistory P B₀ (augmentHistory s₀ (erasePairSources h)))
    (currentMemory P menu priority B₀ s₀ fallback reject (erasePairSources h))

theorem pair_formula (h : History (State × Action) State) :
    pair P menu priority B₀ s₀ fallback fallbackAction reject h =
      (currentState s₀ h,cycleAction (retainedActions (active P menu priority B₀ s₀ fallback reject h)
        (currentState s₀ h)) fallbackAction (historyVisits s₀ (currentState s₀ h) (erasePairSources h))) := by
  simp only [pair,policy,pairPolicy,generatedPhasePolicy,active,observedState_erase]

theorem agrees_with_snapshot (F : Finset (State × Action)) (h : History (State × Action) State)
    (hF : active P menu priority B₀ s₀ fallback reject h=F) :
    pair P menu priority B₀ s₀ fallback fallbackAction reject h =
      FrozenRotor.pairChoice F fallbackAction s₀ (FrozenRotor.snapshot F s₀ h) := by
  rw [pair_formula,hF,FrozenRotor.pairChoice_snapshot]

/-- Availability at a compatible live history is derived from the actual
source invariant, including retained-component validity. -/
theorem active_source_used (hs₀ : s₀ ∈ winningRegion P menu priority B₀)
    (h : History (State × Action) State)
    (hc : ActionCompatible (pairPolicy s₀ (policy P menu priority B₀ s₀ fallback fallbackAction reject)) () h)
    (hlive : (liveHistory P B₀ h).Nonempty) :
    currentState s₀ h ∈ usedStates Prod.fst (active P menu priority B₀ s₀ fallback reject h) := by
  let π := policy P menu priority B₀ s₀ fallback fallbackAction reject
  have hAug := augmentHistory_compatible s₀ π () h hc
  have hInv := generated_history_invariant P menu priority B₀ s₀ hs₀ fallback fallbackAction reject
    (erasePairSources h) (by simpa only [hAug] using hlive) (by simpa only [hAug] using hc)
  have hValid := normalizeMemory_valid P menu priority fallback
    (liveHistory P B₀ (augmentHistory s₀ (erasePairSources h)))
    (observedState s₀ (erasePairSources h))
    (phaseMemory P menu priority B₀ s₀ fallback reject (erasePairSources h)) hInv.2
  have hAvail := valid_activePairs P menu priority fallback _ (by simpa only [hAug] using hlive)
    _ hInv.1 _ hValid
  simpa only [active,currentMemory,observedState_erase] using hAvail.2

/-- A completed slice that has not crossed a chosen progress/extra-stop guard.
F is required to stay the literal active pair set, not an assumed fair menu.
The halt predicate can include actual phase/support changes and τ_n detection. -/
def Continues (F : Finset (State × Action))
    (before : State × Action → Prop) (after : State × Action → State → Prop)
    (halt : History (State × Action) State → Prop) (base : History (State × Action) State) :
    History (State × Action) State → Prop
  | [] => True
  | (e,y)::tail => Continues F before after halt base tail ∧
      active P menu priority B₀ s₀ fallback reject (tail++base)=F ∧
      ¬ before e ∧ ¬ after e y ∧ ¬ halt ((e,y)::tail)

/-- The disagreement kill guard is impossible on a genuinely continuing slice
of the *actual generated policy*. The finite memory is reconstructed from the
whole old history, so phase/support entry does not reset source counters. -/
theorem monitor_eq_snapshot
    (hs₀ : s₀ ∈ winningRegion P menu priority B₀)
    (F : Finset (State × Action))
    (before : State × Action → Prop) (after : State × Action → State → Prop)
    (halt : History (State × Action) State → Prop) (base tail : History (State × Action) State)
    (hc : ActionCompatible (pairPolicy s₀ (policy P menu priority B₀ s₀ fallback fallbackAction reject)) () (tail++base))
    (hlive : (liveHistory P B₀ (tail++base)).Nonempty)
    (hcontinue : Continues P menu priority B₀ s₀ fallback reject F before after halt base tail) :
    HistoryPMF.monitor (FrozenRotor.pairChoice F fallbackAction s₀)
      (FrozenRotor.next F fallbackAction before after) none halt (FrozenRotor.snapshot F s₀ base) tail =
      FrozenRotor.snapshot F s₀ (tail++base) := by
  induction tail with
  | nil => rfl
  | cons ey tail ih =>
      rcases ey with ⟨e,y⟩
      have hcOld : ActionCompatible (pairPolicy s₀ (policy P menu priority B₀ s₀ fallback fallbackAction reject)) ()
          (tail++base) := hc.1
      have hliveOld : (liveHistory P B₀ (tail++base)).Nonempty := by
        rw [List.cons_append,liveHistory_cons] at hlive
        exact hlive.mono (Finset.filter_subset _ _)
      obtain ⟨hOld,hF,hBefore,hAfter,hHalt⟩ := hcontinue
      have hi := ih hcOld hliveOld hOld
      have hchosen : pair P menu priority B₀ s₀ fallback fallbackAction reject (tail++base)=e := hc.2
      have hEq : e=FrozenRotor.pairChoice F fallbackAction s₀ (FrozenRotor.snapshot F s₀ (tail++base)) :=
        hchosen.symm.trans (agrees_with_snapshot P menu priority B₀ s₀ fallback fallbackAction reject F (tail++base) hF)
      have hUsed := active_source_used P menu priority B₀ s₀ fallback fallbackAction reject hs₀ (tail++base) hcOld hliveOld
      rw [hF] at hUsed
      have hGuard : ¬ (FrozenRotor.snapshot F s₀ (tail++base)=none ∨
          e≠FrozenRotor.pairChoice F fallbackAction s₀ (FrozenRotor.snapshot F s₀ (tail++base)) ∨
          halt ((e,y)::tail)) :=
        not_or.mpr ⟨FrozenRotor.snapshot_ne_none F s₀ (tail++base),not_or.mpr ⟨not_not.mpr hEq,hHalt⟩⟩
      rw [HistoryPMF.monitor,hi,if_neg hGuard]
      simpa only [List.cons_append] using FrozenRotor.next_snapshot_of_clear F fallbackAction s₀ before after
        (tail++base) e y hEq hUsed hBefore hAfter

end HiddenParity.Cost.GeneratedSlice
