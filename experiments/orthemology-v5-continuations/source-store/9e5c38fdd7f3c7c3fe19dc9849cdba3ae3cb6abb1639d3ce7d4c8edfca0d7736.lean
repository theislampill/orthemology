import ActualBadCount

noncomputable section
open MeasureTheory
open scoped ENNReal
open Orthemology.Tranche2.PolicyEmbedding
namespace HiddenParity.Cost
open HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Necessity
universe u w
variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- Equality of the actual generated controller's entire nonnegative cost
moment with the raw-tape experiment. Unlike an a.e. parity bridge, this transports
expectations, including infinity, and preserves the first executed action. -/
theorem generated_badCount_moment_eq_stack
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B₀ : Finset Model) (s₀ : State) (fallback : Model) (fallbackAction : Action)
    (reject : Model → ℕ → History (State × Action) State → Bool) (σ : Model)
    (bad : (State × Action) → Prop) [DecidablePred bad] (d : State × Action) (k : ℕ) :
    (∫⁻ H, badCount bad (historyAction d H) ^ k
      ∂markovHistoryLaw P σ s₀
        (generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject) (Measure.dirac ())) =
    ∫⁻ z, badCount bad (runAction P menu priority B₀ s₀ fallback fallbackAction reject z) ^ k
      ∂(Measure.dirac ()).prod (stackMeasure (realRows P σ)
        (realRows_nonnegative P σ) (realRows_normalized P σ)) := by
  let π := generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject
  have hπ := generatedPhasePolicy_measurable P menu priority B₀ s₀ fallback fallbackAction reject
  have hpair := pairPolicy_measurable s₀ π hπ
  let f : (ℕ → State × Action) → ℝ≥0∞ := fun x => badCount bad x ^ k
  have hf : Measurable f := (badCount_measurable bad).pow_const k
  change (∫⁻ H, f (historyAction d H) ∂markovHistoryLaw P σ s₀ π (Measure.dirac ())) = _
  rw [← lintegral_map hf (historyAction_measurable d)]
  change (∫⁻ x, f x ∂actionLaw (pairPolicy s₀ π) (Measure.dirac ())
    (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ) d) = _
  rw [← stackActionTrajectory_law (pairPolicy s₀ π) hpair (Measure.dirac ())
    (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ) d,
    lintegral_map hf (stackActionTrajectory_measurable (pairPolicy s₀ π) hpair)]
  rfl

/-- Exact conditional interface for the remaining stopped-cost analysis: a raw
stack cost bound transfers to the actual law, without supplying that bound as
a fabricated theorem about the controller. -/
theorem generated_badCount_finite_of_stack_bound
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B₀ : Finset Model) (s₀ : State) (fallback : Model) (fallbackAction : Action)
    (reject : Model → ℕ → History (State × Action) State → Bool) (σ : Model)
    (bad : (State × Action) → Prop) [DecidablePred bad] (d : State × Action)
    (b : ℝ≥0∞) (hb : b < ⊤)
    (hbound : (∫⁻ z, badCount bad (runAction P menu priority B₀ s₀ fallback fallbackAction reject z)
      ∂(Measure.dirac ()).prod (stackMeasure (realRows P σ)
        (realRows_nonnegative P σ) (realRows_normalized P σ))) ≤ b) :
    (∫⁻ H, badCount bad (historyAction d H)
      ∂markovHistoryLaw P σ s₀
        (generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject) (Measure.dirac ())) < ⊤ := by
  have he := generated_badCount_moment_eq_stack P menu priority B₀ s₀ fallback fallbackAction reject σ bad d 1
  simp only [pow_one] at he
  rw [he]
  exact hbound.trans_lt hb

end HiddenParity.Cost
