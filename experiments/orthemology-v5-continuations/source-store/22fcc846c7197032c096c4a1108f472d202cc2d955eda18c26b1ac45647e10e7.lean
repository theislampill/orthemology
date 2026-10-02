import FrozenRotorHistory

noncomputable section
open MeasureTheory
open scoped ENNReal
open Orthemology.Tranche2.PolicyEmbedding
namespace HiddenParity.Cost.HistoryPMF
attribute [local instance] Classical.propDecidable
open HiddenParity.ResidualSeed HiddenParity.ResidualSeed.Continuation
universe u
variable {A Y : Type u} [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
variable [MeasurableSpace A] [MeasurableSingletonClass A]
variable [MeasurableSpace Y] [MeasurableSingletonClass Y]

/-- A deterministic Unit seed is unchanged by conditioning on a compatible
history. There is no fresh private seed introduced at this restart. -/
theorem unit_seedPosterior (π : History A Y → A) (h : History A Y)
    (hc : ActionCompatible (fun (_ : Unit) h => π h) () h) :
    commonSeedPosterior (fun (_ : Unit) h => π h) (Measure.dirac ()) h=Measure.dirac () := by
  have hs : CompatibleSeeds (fun (_ : Unit) h => π h) h=Set.univ := by
    ext r
    cases r
    simp [CompatibleSeeds,hc]
  simp [commonSeedPosterior,normalizedRestriction,hs]

/-- Positive actual-prefix conditioning retains the entire original history
inside the restarted policy; it does not restart the generated memory at zero. -/
theorem unit_conditionalContinuationLaw
    (π : History A Y → A) (P : A → Y → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y=1)
    (h : History A Y)
    (hpos : 0 < CanonicalInput (Measure.dirac ()) P hP hN
      (PrefixEvent (fun (_ : Unit) h => π h) h)) :
    conditionalContinuationLaw (fun (_ : Unit) h => π h) (Measure.dirac ()) P hP hN h =
      observedTraceLaw ∅ (fun (_ : Unit) tail => π (tail++h)) (Measure.dirac ()) P P hP hN hP hN := by
  classical
  let πu : Unit → History A Y → A := fun _ h => π h
  have hπ : Measurable (fun z : Unit × History A Y => πu z.1 z.2) := measurable_of_countable _
  have hseeds := positive_prefix_compatible_seeds πu (Measure.dirac ()) P hP hN h hpos
  have hc : ActionCompatible πu () h := by
    by_contra hnot
    have hz : (Measure.dirac ()) (CompatibleSeeds πu h)=0 := by
      rw [Measure.dirac_apply' _ (compatibleSeeds_measurable πu hπ h)]
      simp [CompatibleSeeds,hnot]
    rw [hz] at hseeds
    exact (lt_irrefl 0 hseeds)
  rw [conditionalContinuationLaw_eq_restart πu hπ (Measure.dirac ()) P hP hN h hpos,
    unit_seedPosterior π h hc]
  rfl

end HiddenParity.Cost.HistoryPMF

namespace HiddenParity.Cost.FrozenRotor
attribute [local instance] Classical.propDecidable
open HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Adaptive
open HiddenParity.Necessity HiddenParity.Stage FiniteChainHitting
open HiddenParity.ResidualSeed HiddenParity.ResidualSeed.Continuation
universe u w
variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- Uniform monitored progress under the *actual conditional continuation law*
after any positive full observed history. The restarted policy keeps h, and
the true-row product experiment and posterior are derived by the predecessor.
An arbitrary random sample count or non-stopping last-error index is not used
as a conditioning event. -/
theorem conditional_monitored_kernel_tail
    (F : Finset (State × Action)) (fallback : Action) (s₀ : State)
    (before : State × Action → Prop) (after : State × Action → State → Prop)
    (P : RationalKernel Model (State × Action) State) (σ : Model)
    (π : History (State × Action) State → State × Action)
    (h : History (State × Action) State)
    (hpos : 0 < CanonicalInput (Measure.dirac ()) (realRows P σ)
      (realRows_nonnegative P σ) (realRows_normalized P σ) (PrefixEvent (fun (_ : Unit) h => π h) h))
    (halt : History (State × Action) State → Prop) (q₀ : Aug F)
    (p : ℝ) (hp : 0 ≤ p) (hp1 : p ≤ 1)
    (hmin : ∀ e y, 0 < realRows P σ e y → p ≤ realRows P σ e y)
    (hclasses : ∀ C, ClosedClass (fun q q' => 0 < (kernel F fallback s₀ before after P σ).row q q') C →
      (none : Aug F) ∈ C) (k : ℕ) :
    (conditionalContinuationLaw (fun (_ : Unit) h => π h) (Measure.dirac ()) (realRows P σ)
      (realRows_nonnegative P σ) (realRows_normalized P σ) h)
      {H | HistoryPMF.monitor (pairChoice F fallback s₀) (next F fallback before after) none halt q₀
        (H (k*dimension State Action)) ≠ none} ≤ ENNReal.ofReal ((1-p^dimension State Action)^k) := by
  rw [HistoryPMF.unit_conditionalContinuationLaw π (realRows P σ)
    (realRows_nonnegative P σ) (realRows_normalized P σ) h hpos]
  exact actual_monitored_kernel_tail F fallback s₀ before after P σ (fun tail => π (tail++h))
    halt q₀ p hp hp1 hmin hclasses k

end HiddenParity.Cost.FrozenRotor
