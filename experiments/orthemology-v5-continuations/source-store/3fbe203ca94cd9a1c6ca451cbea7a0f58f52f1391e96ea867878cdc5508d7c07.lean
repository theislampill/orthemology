import ActualIntervalCoverage

noncomputable section
attribute [local instance] Classical.propDecidable
open MeasureTheory
open scoped ENNReal BigOperators Function
open Orthemology.Tranche2.PolicyEmbedding
namespace HiddenParity.Cost
open HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Empirical
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
local notation "H" => runHistory P menu priority B₀ s₀ fallback fallbackAction reject
local notation "tail" => runTail P menu priority B₀ s₀ fallback fallbackAction reject
local notation "π" => pairPolicy s₀ (generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject)

/-- Possible dangerous starts of one chronological index. They are countable
full histories, not bare phase labels or row sample counts. -/
def DangerousStart (σ : Model) (j : ℕ) :=
  {h : History (State × Action) State |
    historyIsStart P menu priority B₀ s₀ fallback reject σ h ∧
    historyProgressCount P menu priority B₀ s₀ fallback reject σ h=j ∧
    historyDanger P menu priority B₀ s₀ fallback reject σ h}

def longStartEvent (σ : Model) (j d : ℕ) : Set (Unit × FlatStack (State × Action) State) :=
  ⋃ h : DangerousStart P menu priority B₀ s₀ fallback reject σ j,
    {z | H z h.val.length=h.val} ∩
      {z | historySlice P menu priority B₀ s₀ fallback reject σ h.val (tail z h.val.length d)}

/-- Each chronological interval index incurs only one copy of the tail bound,
even after arbitrarily long skipped zero-cost operation and arbitrary history. -/
theorem longStartEvent_bound
    (hs₀ : s₀  ∈  winningRegion P menu priority B₀) (σ : Model) (hσ : σ  ∈  B₀)
    (p : ℝ) (hp : 0 ≤ p) (hp1 : p ≤ 1)
    (hmin : ∀ e y,0<realRows P σ e y → p ≤ realRows P σ e y) (j k : ℕ) :
    ((Measure.dirac ()).prod (stackMeasure (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ)))
      (longStartEvent P menu priority B₀ s₀ fallback fallbackAction reject σ j (k*FrozenRotor.dimension State Action))
       ≤ ENNReal.ofReal ((1-p^FrozenRotor.dimension State Action)^k) := by
  have hπ := pairPolicy_measurable s₀ _
    (generatedPhasePolicy_measurable P menu priority B₀ s₀ fallback fallbackAction reject)
  apply disjoint_history_union_bound
  · intro h
    exact (measurableSet_singleton h.val).preimage
      ((measurable_pi_apply h.val.length).comp (stackHistoryTrajectory_measurable π hπ))
  · intro h g hne
    apply Set.disjoint_left.mpr
    intro z hh hg
    have hsh := (historyIsStart_run P menu priority B₀ s₀ fallback fallbackAction reject σ z h.val.length).mp
      (hh.symm ▸ h.property.1)
    have hsg := (historyIsStart_run P menu priority B₀ s₀ fallback fallbackAction reject σ z g.val.length).mp
      (hg.symm ▸ g.property.1)
    have hch := historyProgressCount_run P menu priority B₀ s₀ fallback fallbackAction reject σ z h.val.length
    have hcg := historyProgressCount_run P menu priority B₀ s₀ fallback fallbackAction reject σ z g.val.length
    rw [hh,h.property.2.1] at hch
    rw [hg,g.property.2.1] at hcg
    have he := start_eq_of_progressCount_eq
      (runProgress P menu priority B₀ s₀ fallback fallbackAction reject σ z)
      h.val.length g.val.length hsh hsg (hch.symm.trans hcg)
    apply hne
    apply Subtype.ext
    exact hh.symm.trans (he ▸ hg)
  · intro h
    exact stack_historySlice_inter_bound P menu priority B₀ s₀ fallback fallbackAction reject hs₀ σ hσ h.val
      h.property.2.2 p hp hp1 hmin k

/-- Finite union of chronological dangerous intervals. No conditional MGF,
interval independence, or tail conditional on the raw cutoff event is used. -/
theorem finite_longStart_union_bound
    (hs₀ : s₀  ∈  winningRegion P menu priority B₀) (σ : Model) (hσ : σ  ∈  B₀)
    (p : ℝ) (hp : 0 ≤ p) (hp1 : p ≤ 1)
    (hmin : ∀ e y,0<realRows P σ e y → p ≤ realRows P σ e y) (J k : ℕ) :
    ((Measure.dirac ()).prod (stackMeasure (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ)))
      (⋃ j ∈ Finset.range J,longStartEvent P menu priority B₀ s₀ fallback fallbackAction reject σ j
        (k*FrozenRotor.dimension State Action))
       ≤ (J:ℝ≥0∞)*ENNReal.ofReal ((1-p^FrozenRotor.dimension State Action)^k) := by
  refine (measure_biUnion_finset_le _ _).trans ?_
  calc
    _  ≤  ∑ j ∈ Finset.range J, ENNReal.ofReal ((1-p^FrozenRotor.dimension State Action)^k) :=
      Finset.sum_le_sum (fun j _ => longStartEvent_bound P menu priority B₀ s₀ fallback fallbackAction reject
        hs₀ σ hσ p hp hp1 hmin j k)
    _ = _ := by simp [nsmul_eq_mul]

end HiddenParity.Cost
