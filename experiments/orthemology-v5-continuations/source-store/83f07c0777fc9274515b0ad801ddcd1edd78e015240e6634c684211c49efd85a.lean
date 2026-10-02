import PositiveHistorySlices
import ActualBadCount

noncomputable section
attribute [local instance] Classical.propDecidable
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
variable (ε : ℝ)
local notation "reject" => empiricalReject P ε
local notation "b" => runSupport P menu priority B₀ s₀ fallback fallbackAction reject
local notation "m" => runMemory P menu priority B₀ s₀ fallback fallbackAction reject
local notation "H" => runHistory P menu priority B₀ s₀ fallback fallbackAction reject
local notation "x" => runAction P menu priority B₀ s₀ fallback fallbackAction reject
local notation "label" => generatedSegmentLabel P menu priority B₀ s₀ fallback fallbackAction reject
local notation "tail" => runTail P menu priority B₀ s₀ fallback fallbackAction reject
local notation "progress" => runProgress P menu priority B₀ s₀ fallback fallbackAction reject

theorem truncatedProgressEnds_eq_generatedCharges (σ : Model)
    (z : Unit × FlatStack (State × Action) State) (T : ℕ) :
    truncatedProgressEnds (progress σ z) T=generatedChargeTimes P menu priority B₀ s₀ fallback fallbackAction ε σ z T := by
  ext t
  simp only [truncatedProgressEnds,generatedChargeTimes,interiorMismatchTimes,segmentEnds,
    Finset.mem_union,Finset.mem_filter,Finset.mem_range,runProgress_iff,generatedMismatch]
  by_cases ht : t < T <;> by_cases hend : t+1=T <;> by_cases hl : label z (t+1)=label z t <;> simp_all <;> omega

theorem historyDanger_eq_of_label_eq
    (σ : Model) (h g : History (State × Action) State)
    (he : historySegmentLabel P menu priority B₀ s₀ fallback reject h=
      historySegmentLabel P menu priority B₀ s₀ fallback reject g) :
    historyDanger P menu priority B₀ s₀ fallback reject σ h=
      historyDanger P menu priority B₀ s₀ fallback reject σ g := by
  have hb := congrArg Prod.fst he
  have hi := congrArg (fun v => v.2.1) he
  have hr := congrArg (fun v => v.2.2) he
  dsimp only [historySegmentLabel] at hb hi hr
  simp only [historyDanger,phaseCandidate,hb,hi,hr]

/-- A bad coBüchi action cannot lie in fully matching operation. -/
theorem bad_action_implies_danger
    (bad : Model → (State × Action) → Prop) [∀ σ, DecidablePred (bad σ)]
    (hpriority : priority=fun σ => coBuchiPriority (bad σ))
    (hs₀ : s₀  ∈  winningRegion P menu priority B₀) (σ : Model) (hσ : σ  ∈  B₀)
    (z : Unit × FlatStack (State × Action) State)
    (hSupported : ∀ e k,0<realRows P σ e (z.2 (e,k))) (t : ℕ) (hbad : bad σ (x z t)) :
    historyDanger P menu priority B₀ s₀ fallback reject σ (H z t) := by
  have hv := run_invariant P menu priority B₀ s₀ fallback fallbackAction reject hs₀ σ hσ z hSupported t
  have hx := runAction_mem_active P menu priority B₀ s₀ fallback fallbackAction reject hs₀ σ hσ z hSupported t
  change (match (m z t).retained with
    | none => True
    | some E => ¬Match P.row (phaseCandidate (b z t) fallback (m z t)) σ E)
  cases he : (m z t).retained with
  | none => trivial
  | some E =>
      intro hm
      have hQ := (hv.2.2 E he).1
      have hQ' : MarkovQualifying P Prod.fst (b z t) (fun σ => coBuchiPriority (bad σ))
          (phaseCandidate (b z t) fallback (m z t)) (stageActions P menu priority (b z t)) E := by
        rw [← hpriority]
        exact hQ
      have hg := qualifying_matching_all_good P Prod.fst (b z t) bad
        (phaseCandidate (b z t) fallback (m z t)) σ hv.1 (stageActions P menu priority (b z t)) E hQ' hm
      have hxE : x z t  ∈  E := by simpa only [activePairs,he,Option.getD_some] using hx
      exact hg _ hxE hbad

/-- On an accurate observed prefix, excess bad visits force a long dangerous
continuing slice starting at one of the bounded chronological history slots. -/
theorem actual_long_history_slice_of_excess
    (bad : Model → (State × Action) → Prop) [∀ σ, DecidablePred (bad σ)]
    (hpriority : priority=fun σ => coBuchiPriority (bad σ))
    (hs₀ : s₀  ∈  winningRegion P menu priority B₀) (σ : Model) (hσ : σ  ∈  B₀)
    (η : ℝ) (hη : η ≤ ε) (N T d : ℕ)
    (hSep : ∀ θ ∈ B₀, ∀ e,P.row θ e ≠ P.row σ e → ∃ y, ε+η ≤ |realRows P σ e y-realRows P θ e y|)
    (z : Unit × FlatStack (State × Action) State)
    (hSupported : ∀ e k,0<realRows P σ e (z.2 (e,k)))
    (hAcc : ∀ t,t < T → HistoryAccurate P σ η N (H z t))
    (hex : (Fintype.card (State × Action)*(N+B₀.card-1)+2*B₀.card*(N+B₀.card))*d <
      ((Finset.range T).filter (fun t => bad σ (x z t))).card) :
    ∃ base : History (State × Action) State,
      historyIsStart P menu priority B₀ s₀ fallback reject σ base ∧
      historyDanger P menu priority B₀ s₀ fallback reject σ base ∧
      historyProgressCount P menu priority B₀ s₀ fallback reject σ base <
        Fintype.card (State × Action)*(N+B₀.card-1)+2*B₀.card*(N+B₀.card) ∧
      H z base.length=base ∧
      historySlice P menu priority B₀ s₀ fallback reject σ base (tail z base.length d) := by
  let J := Fintype.card (State × Action)*(N+B₀.card-1)+2*B₀.card*(N+B₀.card)
  have hJ : (truncatedProgressEnds (progress σ z) T).card ≤ J := by
    rw [truncatedProgressEnds_eq_generatedCharges]
    exact accurate_generated_charge_budget P menu priority B₀ s₀ fallback fallbackAction ε σ η hη N T
      hs₀ hσ hSep z hSupported hAcc
  obtain ⟨t,ht,hbad,hage,hstart,hNo⟩ := long_interval_of_excess_count (progress σ z)
    (fun t => bad σ (x z t)) T J d hJ hex
  let s := lastIntervalStart (progress σ z) t
  have hst : s ≤ t := lastIntervalStart_le (progress σ z) t
  have hl : label z t=label z s := by
    have he := run_label_eq_of_no_progress P menu priority B₀ s₀ fallback fallbackAction reject σ z s (t-s)
      (by intro i his hit;exact no_progress_since_start (progress σ z) t i his (by omega))
    simpa only [Nat.add_sub_of_le hst] using he
  have hd := bad_action_implies_danger P menu priority B₀ s₀ fallback fallbackAction ε bad hpriority hs₀ σ hσ z hSupported t hbad
  have hdStart : historyDanger P menu priority B₀ s₀ fallback reject σ (H z s) := by
    have he := historyDanger_eq_of_label_eq P menu priority B₀ s₀ fallback ε σ (H z t) (H z s) hl
    exact he ▸ hd
  have hlen : (H z s).length=s := observedHistory_length _ _ _ _ _ _
  refine ⟨H z s,(historyIsStart_run P menu priority B₀ s₀ fallback fallbackAction reject σ z s).mpr hstart,
    hdStart,?_,by rw [hlen],?_⟩
  · rw [historyProgressCount_run]
    exact (progressCount_lt_endpoint_card (progress σ z) s T (by omega)).trans_le hJ
  · rw [hlen]
    cases he : (m z s).retained with
    | none =>
        change (currentMemory P menu priority B₀ s₀ fallback reject (erasePairSources (H z s))).retained=none at he
        simpa only [historySlice,he] using run_navigation_continues P menu priority B₀ s₀ fallback fallbackAction reject
          hs₀ σ hσ z hSupported s d he hNo
    | some E =>
        change (currentMemory P menu priority B₀ s₀ fallback reject (erasePairSources (H z s))).retained=some E at he
        simpa only [historySlice,he] using run_operation_continues P menu priority B₀ s₀ fallback fallbackAction reject
          hs₀ σ hσ z hSupported s d E he hNo

end HiddenParity.Cost
