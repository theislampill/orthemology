import MonitoredHistoryDomination
import FrozenRotorProgress

noncomputable section
open MeasureTheory
open scoped ENNReal
open Orthemology.Tranche2.PolicyEmbedding
namespace HiddenParity.Cost.FrozenRotor
attribute [local instance] Classical.propDecidable
open HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Adaptive
open HiddenParity.Necessity HiddenParity.Stage FiniteChainHitting
universe u w
variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- Exact frozen pair choice, including the irrelevant default after killing. -/
def pairChoice (F : Finset (State × Action)) (fallback : Action) (s₀ : State) (q : Aug F) : State × Action :=
  (source F s₀ q,action F fallback q)

theorem transition_eq_kernel (F : Finset (State × Action)) (fallback : Action) (s₀ : State)
    (before : State × Action → Prop) (after : State × Action → State → Prop)
    (P : RationalKernel Model (State × Action) State) (σ : Model) :
    HistoryPMF.transition (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ)
      (pairChoice F fallback s₀) (next F fallback before after) = rowPMF (kernel F fallback s₀ before after P σ) := by
  classical
  funext q
  exact HistoryPMF.transition_eq_push_rowPMF (realRows P σ) (realRows_nonnegative P σ)
    (realRows_normalized P σ) (pairChoice F fallback s₀) (next F fallback before after) q

theorem kernel_absorbs_kill (F : Finset (State × Action)) (fallback : Action) (s₀ : State)
    (before : State × Action → Prop) (after : State × Action → State → Prop)
    (P : RationalKernel Model (State × Action) State) (σ : Model) :
    rowPMF (kernel F fallback s₀ before after P σ) none=PMF.pure none := by
  classical
  rw [← transition_eq_kernel]
  change (HistoryPMF.symbolPMF (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ)
    (pairChoice F fallback s₀ none)).map (fun _ => (none : Aug F)) = _
  exact PMF.map_const _ _

/-- Actual canonical-history probability of the monitored frozen readout.
Arbitrary adapted extra killing is allowed; action disagreement is killed too.
The latter guard must be ruled out by a source interval-alignment theorem when
this estimate is used for an actual charged interval. -/
theorem actual_monitored_kernel_tail
    (F : Finset (State × Action)) (fallback : Action) (s₀ : State)
    (before : State × Action → Prop) (after : State × Action → State → Prop)
    (P : RationalKernel Model (State × Action) State) (σ : Model)
    (π : History (State × Action) State → State × Action)
    (halt : History (State × Action) State → Prop) (q₀ : Aug F)
    (p : ℝ) (hp : 0 ≤ p) (hp1 : p ≤ 1)
    (hmin : ∀ e y, 0 < realRows P σ e y → p ≤ realRows P σ e y)
    (hclasses : ∀ C, ClosedClass (fun q q' => 0 < (kernel F fallback s₀ before after P σ).row q q') C →
      (none : Aug F) ∈ C) (k : ℕ) :
    (observedTraceLaw ∅ (fun (_ : Unit) h => π h) (Measure.dirac ())
      (realRows P σ) (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ)
      (realRows_nonnegative P σ) (realRows_normalized P σ))
      {H | HistoryPMF.monitor (pairChoice F fallback s₀) (next F fallback before after) none halt q₀
        (H (k*dimension State Action)) ≠ none} ≤
      ENNReal.ofReal ((1-p^dimension State Action)^k) := by
  classical
  have hdom := HistoryPMF.actual_monitored_survival_le (realRows P σ) (realRows_nonnegative P σ)
    (realRows_normalized P σ) π (pairChoice F fallback s₀) (next F fallback before after)
    none halt q₀ (fun _ => rfl) (k*dimension State Action)
  rw [transition_eq_kernel] at hdom
  rw [HistoryPMF.iteratePMF_eq_absorbed _ (fun q : Aug F => q=none) (by
    intro q hq
    subst q
    exact kernel_absorbs_kill F fallback s₀ before after P σ)] at hdom
  exact hdom.trans (kernel_geometric_tail F fallback s₀ before after P σ p hp hp1 hmin hclasses k q₀)

/-- The actual-law monitored navigation estimate supplies its own source graph
certificate through the computed region and target selectors. -/
theorem actual_monitored_navigation_tail
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (θ σ : Model) (hθ : θ ∈ B) (fallback : Action) (s₀ : State)
    (π : History (State × Action) State → State × Action)
    (halt : History (State × Action) State → Prop) (q₀ : Aug (stageActions P menu priority B))
    (p : ℝ) (hp : 0 ≤ p) (hp1 : p ≤ 1)
    (hmin : ∀ e y, 0 < realRows P σ e y → p ≤ realRows P σ e y) (k : ℕ) :
    (observedTraceLaw ∅ (fun (_ : Unit) h => π h) (Measure.dirac ())
      (realRows P σ) (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ)
      (realRows_nonnegative P σ) (realRows_normalized P σ))
      {H | HistoryPMF.monitor (pairChoice (stageActions P menu priority B) fallback s₀)
        (next (stageActions P menu priority B) fallback (navigationBefore P menu priority B θ σ)
          (navigationAfter P menu priority B θ)) none halt q₀ (H (k*dimension State Action)) ≠ none} ≤
      ENNReal.ofReal ((1-p^dimension State Action)^k) := by
  exact actual_monitored_kernel_tail (stageActions P menu priority B) fallback s₀
    (navigationBefore P menu priority B θ σ) (navigationAfter P menu priority B θ) P σ π halt q₀ p hp hp1 hmin
    (navigation_classes_hit_kill P menu priority B θ σ hθ fallback s₀) k

/-- The same actual-law estimate for a selected qualifying mismatching
operation; all finite rows, rotor states and probability laws are retained. -/
theorem actual_monitored_operation_tail
    (P : RationalKernel Model (State × Action) State) (B : Finset Model)
    (priority : Model → (State × Action) → ℕ) (θ σ : Model) (hσ : σ ∈ B)
    (allowed E : Finset (State × Action)) (hQ : MarkovQualifying P Prod.fst B priority θ allowed E)
    (hNe : ¬ Match P.row θ σ E) (fallback : Action) (s₀ : State)
    (π : History (State × Action) State → State × Action)
    (halt : History (State × Action) State → Prop) (q₀ : Aug E)
    (p : ℝ) (hp : 0 ≤ p) (hp1 : p ≤ 1)
    (hmin : ∀ e y, 0 < realRows P σ e y → p ≤ realRows P σ e y) (k : ℕ) :
    (observedTraceLaw ∅ (fun (_ : Unit) h => π h) (Measure.dirac ())
      (realRows P σ) (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ)
      (realRows_nonnegative P σ) (realRows_normalized P σ))
      {H | HistoryPMF.monitor (pairChoice E fallback s₀)
        (next E fallback (mismatching P θ σ) (operatingAfter P B E)) none halt q₀
        (H (k*dimension State Action)) ≠ none} ≤ ENNReal.ofReal ((1-p^dimension State Action)^k) := by
  exact actual_monitored_kernel_tail E fallback s₀ (mismatching P θ σ) (operatingAfter P B E) P σ π halt q₀
    p hp hp1 hmin (operation_classes_hit_kill P B priority θ σ hσ allowed E hQ hNe fallback s₀) k

end HiddenParity.Cost.FrozenRotor
