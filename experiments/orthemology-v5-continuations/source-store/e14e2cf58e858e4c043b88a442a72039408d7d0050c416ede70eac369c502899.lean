import SupportedConditionalHistories

noncomputable section
open MeasureTheory
open scoped ENNReal
open Orthemology.Tranche2.PolicyEmbedding
namespace HiddenParity.Cost.GeneratedSlice
attribute [local instance] Classical.propDecidable
open HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Adaptive
open HiddenParity.Necessity HiddenParity.Stage HiddenParity.ResidualSeed HiddenParity.ResidualSeed.Continuation
open FiniteChainHitting
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

/-- Uniform geometric bound for a continuing slice of the actual generated
controller after any positive complete observed history. Compatibility/live
support and rotor agreement are derived, not assumed in the event. The full
old history is retained in both the continued policy and rotor snapshot. -/
theorem conditional_generated_slice_tail
    (hs₀ : s₀ ∈ winningRegion P menu priority B₀) (σ : Model) (hσ : σ ∈ B₀)
    (base : History (State × Action) State)
    (hpos : 0 < CanonicalInput (Measure.dirac ()) (realRows P σ)
      (realRows_nonnegative P σ) (realRows_normalized P σ)
      (PrefixEvent (fun (_ : Unit) h => pair P menu priority B₀ s₀ fallback fallbackAction reject h) base))
    (F : Finset (State × Action)) (before : State × Action → Prop) (after : State × Action → State → Prop)
    (halt : History (State × Action) State → Prop)
    (p : ℝ) (hp : 0 ≤ p) (hp1 : p ≤ 1)
    (hmin : ∀ e y, 0 < realRows P σ e y → p ≤ realRows P σ e y)
    (hclasses : ∀ C, ClosedClass (fun q q' => 0 < (FrozenRotor.kernel F fallbackAction s₀ before after P σ).row q q') C →
      (none : FrozenRotor.Aug F) ∈ C) (k : ℕ) :
    (conditionalContinuationLaw
      (fun (_ : Unit) h => pair P menu priority B₀ s₀ fallback fallbackAction reject h) (Measure.dirac ())
      (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ) base)
      {H | Continues P menu priority B₀ s₀ fallback reject F before after halt base
        (H (k*FrozenRotor.dimension State Action))} ≤
      ENNReal.ofReal ((1-p^FrozenRotor.dimension State Action)^k) := by
  let π := pair P menu priority B₀ s₀ fallback fallbackAction reject
  let μ := conditionalContinuationLaw (fun (_ : Unit) h => π h) (Measure.dirac ()) (realRows P σ)
    (realRows_nonnegative P σ) (realRows_normalized P σ) base
  let n := k*FrozenRotor.dimension State Action
  have hAE := HistoryPMF.conditional_history_compatible_live P B₀ σ hσ π base hpos n
  have hInclude : ∀ᵐ H ∂μ,
      H ∈ {H | Continues P menu priority B₀ s₀ fallback reject F before after halt base (H n)} →
      H ∈ {H | HistoryPMF.monitor (FrozenRotor.pairChoice F fallbackAction s₀)
        (FrozenRotor.next F fallbackAction before after) none halt (FrozenRotor.snapshot F s₀ base) (H n)≠none} := by
    filter_upwards [hAE] with H hH
    intro hContinue
    have he := monitor_eq_snapshot P menu priority B₀ s₀ fallback fallbackAction reject hs₀ F before after halt
      base (H n) hH.1 ⟨σ,hH.2⟩ hContinue
    change HistoryPMF.monitor _ _ _ _ _ _≠none
    rw [he]
    exact FrozenRotor.snapshot_ne_none F s₀ (H n++base)
  have hle := measure_mono_ae hInclude
  exact hle.trans (FrozenRotor.conditional_monitored_kernel_tail F fallbackAction s₀ before after P σ π base hpos
    halt (FrozenRotor.snapshot F s₀ base) p hp hp1 hmin hclasses k)

/-- Actual conditional navigation slice probability, using the computed stage
menu and target selector with no supplied closed-class/positive-path premise. -/
theorem conditional_generated_navigation_tail
    (hs₀ : s₀ ∈ winningRegion P menu priority B₀) (σ : Model) (hσ : σ ∈ B₀)
    (base : History (State × Action) State)
    (hpos : 0 < CanonicalInput (Measure.dirac ()) (realRows P σ)
      (realRows_nonnegative P σ) (realRows_normalized P σ)
      (PrefixEvent (fun (_ : Unit) h => pair P menu priority B₀ s₀ fallback fallbackAction reject h) base))
    (B : Finset Model) (θ : Model) (hθ : θ ∈ B) (halt : History (State × Action) State → Prop)
    (p : ℝ) (hp : 0 ≤ p) (hp1 : p ≤ 1)
    (hmin : ∀ e y, 0 < realRows P σ e y → p ≤ realRows P σ e y) (k : ℕ) :
    (conditionalContinuationLaw
      (fun (_ : Unit) h => pair P menu priority B₀ s₀ fallback fallbackAction reject h) (Measure.dirac ())
      (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ) base)
      {H | Continues P menu priority B₀ s₀ fallback reject (stageActions P menu priority B)
        (FrozenRotor.navigationBefore P menu priority B θ σ) (FrozenRotor.navigationAfter P menu priority B θ)
        halt base (H (k*FrozenRotor.dimension State Action))} ≤
      ENNReal.ofReal ((1-p^FrozenRotor.dimension State Action)^k) := by
  exact conditional_generated_slice_tail P menu priority B₀ s₀ fallback fallbackAction reject hs₀ σ hσ base hpos
    (stageActions P menu priority B) (FrozenRotor.navigationBefore P menu priority B θ σ)
    (FrozenRotor.navigationAfter P menu priority B θ) halt p hp hp1 hmin
    (FrozenRotor.navigation_classes_hit_kill P menu priority B θ σ hθ fallbackAction s₀) k

/-- Actual conditional operation slice probability in a genuinely mismatching
qualifying target, with the original global generator unchanged. -/
theorem conditional_generated_operation_tail
    (hs₀ : s₀ ∈ winningRegion P menu priority B₀) (σ : Model) (hσ : σ ∈ B₀)
    (base : History (State × Action) State)
    (hpos : 0 < CanonicalInput (Measure.dirac ()) (realRows P σ)
      (realRows_nonnegative P σ) (realRows_normalized P σ)
      (PrefixEvent (fun (_ : Unit) h => pair P menu priority B₀ s₀ fallback fallbackAction reject h) base))
    (B : Finset Model) (θ : Model) (hσB : σ ∈ B) (allowed E : Finset (State × Action))
    (hQ : MarkovQualifying P Prod.fst B priority θ allowed E) (hNe : ¬ Match P.row θ σ E)
    (halt : History (State × Action) State → Prop)
    (p : ℝ) (hp : 0 ≤ p) (hp1 : p ≤ 1)
    (hmin : ∀ e y, 0 < realRows P σ e y → p ≤ realRows P σ e y) (k : ℕ) :
    (conditionalContinuationLaw
      (fun (_ : Unit) h => pair P menu priority B₀ s₀ fallback fallbackAction reject h) (Measure.dirac ())
      (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ) base)
      {H | Continues P menu priority B₀ s₀ fallback reject E (FrozenRotor.mismatching P θ σ)
        (FrozenRotor.operatingAfter P B E) halt base (H (k*FrozenRotor.dimension State Action))} ≤
      ENNReal.ofReal ((1-p^FrozenRotor.dimension State Action)^k) := by
  exact conditional_generated_slice_tail P menu priority B₀ s₀ fallback fallbackAction reject hs₀ σ hσ base hpos E
    (FrozenRotor.mismatching P θ σ) (FrozenRotor.operatingAfter P B E) halt p hp hp1 hmin
    (FrozenRotor.operation_classes_hit_kill P B priority θ σ hσB allowed E hQ hNe fallbackAction s₀) k

end HiddenParity.Cost.GeneratedSlice
