import GlobalParitySufficiency

/-! A source-owned restricted specialization of the accepted controller.
Singleton state menus erase its internal classical choices on every supported
run. The resulting executable selector still reacts to the actual observations. -/
noncomputable section
open MeasureTheory
open Orthemology.Tranche2.PolicyEmbedding
namespace Orthemology.RuntimeBridge.Controller
open HiddenParity HiddenParity.Stochastic HiddenParity.Necessity
open HiddenParity.Sufficiency HiddenParity.Adaptive HiddenParity.Stage
universe u w
variable {State Action : Type u} {Model : Type w}
set_option linter.unusedSectionVars false
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

def singletonMenu (select : State → Action) (_ : Finset Model) (s : State) : Finset Action := {select s}

def selectedPolicy (select : State → Action) (s₀ : State)
    (_ : Unit) (h : History Action State) : Action := select (observedState s₀ h)

theorem selectedPolicy_measurable (select : State → Action) (s₀ : State) :
    Measurable (fun z : Unit × History Action State => selectedPolicy select s₀ z.1 z.2) :=
  measurable_of_countable _

theorem pair_selectedPolicy (select : State → Action) (s₀ : State)
    (r : Unit) (h : History (State × Action) State) :
    pairPolicy s₀ (selectedPolicy select s₀) r h =
      (currentState s₀ h, select (currentState s₀ h)) := by
  simp [pairPolicy, selectedPolicy, observedState_erase]

theorem singleton_lawful_action (P : RationalKernel Model (State × Action) State)
    (select : State → Action) (B : Finset Model) (s₀ : State)
    (π : Unit → History Action State → Action)
    (lawful : Lawful P (singletonMenu select) B s₀ π (Measure.dirac ()))
    (h : History (State × Action) State) (hLive : (liveHistory P B h).Nonempty)
    (hComp : ActionCompatible (pairPolicy s₀ π) () h) :
    pairPolicy s₀ π () h = (currentState s₀ h, select (currentState s₀ h)) := by
  have ha := (ae_dirac_iff (Set.toFinite _).measurableSet).mp (lawful h hLive) hComp
  have he : (pairPolicy s₀ π () h).2 = select (currentState s₀ h) :=
    Finset.mem_singleton.mp ha
  exact Prod.ext rfl he

theorem singleton_supported_action (P : RationalKernel Model (State × Action) State)
    (select : State → Action) (B : Finset Model) (s₀ : State)
    (π : Unit → History Action State → Action)
    (lawful : Lawful P (singletonMenu select) B s₀ π (Measure.dirac ()))
    (σ : Model) (hσ : σ ∈ B) (z : Unit × FlatStack (State × Action) State)
    (hSupported : ∀ e k, 0 < realRows P σ e (z.2 (e,k))) (n : ℕ) :
    stackActionTrajectory (pairPolicy s₀ π) z n =
      (currentState s₀ (stackHistoryTrajectory (pairPolicy s₀ π) z n),
       select (currentState s₀ (stackHistoryTrajectory (pairPolicy s₀ π) z n))) := by
  cases hz : z.1
  apply singleton_lawful_action P select B s₀ π lawful
  · exact ⟨σ, stack_true_model_survives P B σ hσ s₀ π z hSupported n⟩
  · simpa only [hz] using stack_history_compatible (pairPolicy s₀ π) z n

/-- Equality of the entire acquired history on each supported raw-tape input.
It is proved through local choices and the actual next-unused stack cell. -/
theorem singleton_supported_histories (P : RationalKernel Model (State × Action) State)
    (select : State → Action) (B : Finset Model) (s₀ : State)
    (π : Unit → History Action State → Action)
    (lawful : Lawful P (singletonMenu select) B s₀ π (Measure.dirac ()))
    (σ : Model) (hσ : σ ∈ B) (z : Unit × FlatStack (State × Action) State)
    (hSupported : ∀ e k, 0 < realRows P σ e (z.2 (e,k))) :
    stackHistoryTrajectory (pairPolicy s₀ π) z =
      stackHistoryTrajectory (pairPolicy s₀ (selectedPolicy select s₀)) z := by
  funext n
  induction n with
  | zero => rfl
  | succ n ih =>
      rw [stack_history_succ, stack_history_succ]
      have ha : stackActionTrajectory (pairPolicy s₀ π) z n =
          stackActionTrajectory (pairPolicy s₀ (selectedPolicy select s₀)) z n := by
        rw [singleton_supported_action P select B s₀ π lawful σ hσ z hSupported n, ih]
        exact (pair_selectedPolicy select s₀ z.1 _).symm
      have hy : stackReceipt (pairPolicy s₀ π) z n =
          stackReceipt (pairPolicy s₀ (selectedPolicy select s₀)) z n := by
        simp only [stackReceipt, countBefore, ha, ih]
      rw [ha, hy, ih]

/-- The accepted generated controller has this finite, observation-only exact
specialization even though its unused phase/component calculations are classical. -/
theorem generated_singleton_histories
    (P : RationalKernel Model (State × Action) State) (select : State → Action)
    (priority : Model → (State × Action) → ℕ) (B : Finset Model) (s₀ : State)
    (hs : s₀ ∈ winningRegion P (singletonMenu select) priority B)
    (fallback : Model) (fallbackAction : Action)
    (reject : Model → ℕ → History (State × Action) State → Bool)
    (σ : Model) (hσ : σ ∈ B) (z : Unit × FlatStack (State × Action) State)
    (hSupported : ∀ e k, 0 < realRows P σ e (z.2 (e,k))) :
    stackHistoryTrajectory
      (pairPolicy s₀ (generatedPhasePolicy P (singletonMenu select) priority B s₀ fallback fallbackAction reject)) z =
      stackHistoryTrajectory (pairPolicy s₀ (selectedPolicy select s₀)) z := by
  exact singleton_supported_histories P select B s₀ _
    (generatedPhasePolicy_lawful P (singletonMenu select) priority B s₀ hs fallback fallbackAction reject)
    σ hσ z hSupported

end Orthemology.RuntimeBridge.Controller

noncomputable section
open MeasureTheory
open Orthemology.Tranche2.PolicyEmbedding
namespace Orthemology.RuntimeBridge.Controller
open HiddenParity HiddenParity.Stochastic HiddenParity.Necessity
open HiddenParity.Sufficiency HiddenParity.Adaptive HiddenParity.Stage
universe u w
variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]
set_option linter.unusedSectionVars false

theorem markov_law_stack (P : RationalKernel Model (State × Action) State)
    (σ : Model) (s₀ : State) (π : Unit → History Action State → Action) :
    markovHistoryLaw P σ s₀ π (Measure.dirac ()) =
      ((Measure.dirac ()).prod (stackMeasure (realRows P σ)
        (realRows_nonnegative P σ) (realRows_normalized P σ))).map
          (stackHistoryTrajectory (pairPolicy s₀ π)) := by
  have hm : Measurable (fun z : Unit × History (State × Action) State => pairPolicy s₀ π z.1 z.2) :=
    measurable_of_countable _
  rw [markovHistoryLaw, ← observedTraceLaw_eq_all_query Finset.univ (pairPolicy s₀ π) hm
    (Measure.dirac ()) (realRows P σ) (realRows P σ)
    (realRows_nonnegative P σ) (realRows_normalized P σ)
    (realRows_nonnegative P σ) (realRows_normalized P σ) (fun _ _ => rfl)]
  exact observedTraceLaw_univ_eq_stack _ hm _ _ _ _

/-- Complete observed-history law equality for any lawful Unit-seed policy
under singleton menus. Null off-policy branches are not assumed lawful. -/
theorem singleton_law_exact (P : RationalKernel Model (State × Action) State)
    (select : State → Action) (B : Finset Model) (s₀ : State)
    (π : Unit → History Action State → Action)
    (lawful : Lawful P (singletonMenu select) B s₀ π (Measure.dirac ()))
    (σ : Model) (hσ : σ ∈ B) :
    markovHistoryLaw P σ s₀ π (Measure.dirac ()) =
      markovHistoryLaw P σ s₀ (selectedPolicy select s₀) (Measure.dirac ()) := by
  rw [markov_law_stack, markov_law_stack]
  apply Measure.map_congr
  filter_upwards [seeded_all_tapes_supported (Measure.dirac ()) (realRows P σ)
    (realRows_nonnegative P σ) (realRows_normalized P σ)] with z hz
  exact singleton_supported_histories P select B s₀ π lawful σ hσ z hz

/-- Exact law specialization of the literal accepted history-policy generator,
including its actual acquired history and the chosen hidden environment row. -/
theorem generated_singleton_law
    (P : RationalKernel Model (State × Action) State) (select : State → Action)
    (priority : Model → (State × Action) → ℕ) (B : Finset Model) (s₀ : State)
    (hs : s₀ ∈ winningRegion P (singletonMenu select) priority B)
    (fallback : Model) (fallbackAction : Action)
    (reject : Model → ℕ → History (State × Action) State → Bool)
    (σ : Model) (hσ : σ ∈ B) :
    markovHistoryLaw P σ s₀
      (generatedPhasePolicy P (singletonMenu select) priority B s₀ fallback fallbackAction reject)
      (Measure.dirac ()) =
    markovHistoryLaw P σ s₀ (selectedPolicy select s₀) (Measure.dirac ()) := by
  exact singleton_law_exact P select B s₀ _
    (generatedPhasePolicy_lawful P (singletonMenu select) priority B s₀ hs fallback fallbackAction reject) σ hσ

end Orthemology.RuntimeBridge.Controller
