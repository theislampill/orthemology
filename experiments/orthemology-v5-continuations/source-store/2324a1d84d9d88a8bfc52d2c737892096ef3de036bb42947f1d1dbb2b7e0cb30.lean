import GeneratedIntervalSlices

noncomputable section
attribute [local instance] Classical.propDecidable
open MeasureTheory
open scoped ENNReal
open Orthemology.Tranche2.PolicyEmbedding
namespace HiddenParity.Cost
open HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Empirical
open HiddenParity.Necessity HiddenParity.Stage HiddenParity.ResidualSeed HiddenParity.ResidualSeed.Continuation
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
local notation "π" => pairPolicy s₀ (generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject)
local notation "mem" => currentMemory P menu priority B₀ s₀ fallback reject

/-- A single source-bound slice predicate selects navigation or the exact
current retained component from the full old history. -/
def historySlice (σ : Model) (base tail : History (State × Action) State) : Prop :=
  let B := liveHistory P B₀ base
  let mm := mem (erasePairSources base)
  let θ := phaseCandidate B fallback mm
  match mm.retained with
  | none => GeneratedSlice.Continues P menu priority B₀ s₀ fallback reject (stageActions P menu priority B)
      (FrozenRotor.navigationBefore P menu priority B θ σ) (FrozenRotor.navigationAfter P menu priority B θ)
      (fun _ => False) base tail
  | some E => GeneratedSlice.Continues P menu priority B₀ s₀ fallback reject E
      (FrozenRotor.mismatching P θ σ) (FrozenRotor.operatingAfter P B E) (fun _ => False) base tail

/-- Positive complete histories retain true support and the normalized generated
source invariant. No hypothetical live/compatible event is added to the tail. -/
theorem positive_history_source_invariant
    (hs₀ : s₀  ∈  winningRegion P menu priority B₀) (σ : Model) (hσ : σ  ∈  B₀)
    (base : History (State × Action) State)
    (hpos : 0<CanonicalInput (Measure.dirac ()) (realRows P σ) (realRows_nonnegative P σ)
      (realRows_normalized P σ) (PrefixEvent π base)) :
    σ  ∈  liveHistory P B₀ base ∧
      MemoryValid P menu priority fallback (liveHistory P B₀ base) (currentState s₀ base)
        (mem (erasePairSources base)) := by
  have hc := HistoryPMF.unit_prefix_compatible (fun h => π () h) (realRows P σ)
    (realRows_nonnegative P σ) (realRows_normalized P σ) base hpos
  have hLike : RowLikelihood (realRows P σ) base  ≠  0 := by
    intro hz
    have hh := hpos
    rw [prefix_probability,hz,mul_zero] at hh
    exact lt_irrefl 0 hh
  have hRows := HistoryPMF.rowLikelihood_nonzero_rows (realRows P σ) base hLike
  have hLive : σ  ∈  liveHistory P B₀ base := by
    apply (mem_liveHistory P B₀ base σ).mpr
    refine ⟨hσ,?_⟩
    intro ey hey
    have hr := hRows ey hey
    change (0:ℝ)<(P.row σ ey.1 ey.2:ℝ) at hr
    exact_mod_cast hr
  have hAug := augmentHistory_compatible s₀ (generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject)
    () base hc
  have hInv := generated_history_invariant P menu priority B₀ s₀ hs₀ fallback fallbackAction reject
    (erasePairSources base) (by simpa only [hAug] using (show (liveHistory P B₀ base).Nonempty from ⟨σ,hLive⟩))
    (by simpa only [hAug] using hc)
  refine ⟨hLive,?_⟩
  have hValid := normalizeMemory_valid P menu priority fallback
    (liveHistory P B₀ (augmentHistory s₀ (erasePairSources base)))
    (observedState s₀ (erasePairSources base))
    (phaseMemory P menu priority B₀ s₀ fallback reject (erasePairSources base)) hInv.2
  simpa only [currentMemory,hAug,observedState_erase] using hValid

/-- One uniform conditional tail selected from the literal current source mode.
Only dangerous operation is included, so a matching zero-cost residence is
never falsely assigned a physical-time tail. -/
theorem conditional_historySlice_tail
    (hs₀ : s₀  ∈  winningRegion P menu priority B₀) (σ : Model) (hσ : σ  ∈  B₀)
    (base : History (State × Action) State)
    (hpos : 0<CanonicalInput (Measure.dirac ()) (realRows P σ) (realRows_nonnegative P σ)
      (realRows_normalized P σ) (PrefixEvent π base))
    (hd : historyDanger P menu priority B₀ s₀ fallback reject σ base)
    (p : ℝ) (hp : 0 ≤ p) (hp1 : p ≤ 1)
    (hmin : ∀ e y,0<realRows P σ e y → p ≤ realRows P σ e y) (k : ℕ) :
    (conditionalContinuationLaw π (Measure.dirac ()) (realRows P σ) (realRows_nonnegative P σ)
      (realRows_normalized P σ) base)
      {H | historySlice P menu priority B₀ s₀ fallback reject σ base (H (k*FrozenRotor.dimension State Action))}
       ≤  ENNReal.ofReal ((1-p^FrozenRotor.dimension State Action)^k) := by
  have hv := positive_history_source_invariant P menu priority B₀ s₀ fallback fallbackAction reject hs₀ σ hσ base hpos
  let B := liveHistory P B₀ base
  let mm := mem (erasePairSources base)
  cases he : mm.retained with
  | none =>
      change (mem (erasePairSources base)).retained=none at he
      have hθ : phaseCandidate B fallback mm  ∈  B := cycleAction_mem B fallback ⟨σ,hv.1⟩ mm.index
      simpa only [historySlice,B,mm,he,GeneratedSlice.pair,GeneratedSlice.policy] using
        GeneratedSlice.conditional_generated_navigation_tail P menu priority B₀ s₀ fallback fallbackAction reject
          hs₀ σ hσ base hpos B (phaseCandidate B fallback mm) hθ (fun _ => False) p hp hp1 hmin k
  | some E =>
      change (mem (erasePairSources base)).retained=some E at he
      have hm : ¬Match P.row (phaseCandidate B fallback mm) σ E := by
        simpa only [historyDanger,B,mm,he] using hd
      have hQ := (hv.2 E he).1
      simpa only [historySlice,B,mm,he,GeneratedSlice.pair,GeneratedSlice.policy] using
        GeneratedSlice.conditional_generated_operation_tail P menu priority B₀ s₀ fallback fallbackAction reject
          hs₀ σ hσ base hpos B (phaseCandidate B fallback mm) hv.1 (stageActions P menu priority B) E hQ hm
          (fun _ => False) p hp hp1 hmin k

/-- Unconditional mass of a positive-or-null actual starting prefix followed
by a long dangerous slice. Prefix probability is paid exactly once. -/
theorem stack_historySlice_inter_bound
    (hs₀ : s₀  ∈  winningRegion P menu priority B₀) (σ : Model) (hσ : σ  ∈  B₀)
    (base : History (State × Action) State)
    (hd : historyDanger P menu priority B₀ s₀ fallback reject σ base)
    (p : ℝ) (hp : 0 ≤ p) (hp1 : p ≤ 1)
    (hmin : ∀ e y,0<realRows P σ e y → p ≤ realRows P σ e y) (k : ℕ) :
    let μ := (Measure.dirac ()).prod (stackMeasure (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ))
    let E := {z | stackHistoryTrajectory π z base.length=base}
    μ (E ∩ {z | historySlice P menu priority B₀ s₀ fallback reject σ base
      (runTail P menu priority B₀ s₀ fallback fallbackAction reject z base.length (k*FrozenRotor.dimension State Action))})
       ≤  μ E*ENNReal.ofReal ((1-p^FrozenRotor.dimension State Action)^k) := by
  dsimp only
  have hπ := pairPolicy_measurable s₀ _
    (generatedPhasePolicy_measurable P menu priority B₀ s₀ fallback fallbackAction reject)
  have hE : MeasurableSet {z | stackHistoryTrajectory π z base.length=base} :=
    (measurableSet_singleton base).preimage
      ((measurable_pi_apply base.length).comp (stackHistoryTrajectory_measurable π hπ))
  apply measure_inter_le_of_normalizedRestriction (ι := ℕ) _ _ _ hE
  intro hpos
  have hpos' := hpos
  rw [stack_prefix_probability_eq π hπ (Measure.dirac ()) (realRows P σ)
    (realRows_nonnegative P σ) (realRows_normalized P σ) base] at hpos'
  have hb := conditional_historySlice_tail P menu priority B₀ s₀ fallback fallbackAction reject hs₀ σ hσ base hpos'
    hd p hp hp1 hmin k
  have hs : MeasurableSet {H : ℕ → History (State × Action) State |
      historySlice P menu priority B₀ s₀ fallback reject σ base (H (k*FrozenRotor.dimension State Action))} :=
    (Set.to_countable {tail : History (State × Action) State | historySlice P menu priority B₀ s₀ fallback reject σ base tail}).measurableSet.preimage (measurable_pi_apply (k*FrozenRotor.dimension State Action))
  rw [← stack_conditional_continuation_eq π hπ (Measure.dirac ()) (realRows P σ)
    (realRows_nonnegative P σ) (realRows_normalized P σ) base,
    Measure.map_apply (show Measurable (fun z => continuationReadout base (stackHistoryTrajectory π z)) from
      (continuationReadout_measurable base).comp (stackHistoryTrajectory_measurable π hπ)) hs] at hb
  exact hb

end HiddenParity.Cost
