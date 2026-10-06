import SegmentEnumeration

noncomputable section
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
local notation "π" => pairPolicy s₀ (generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject)

/-- A mismatch means inequality of the full original model rows at the actual
executed pair and actual candidate, rather than an external marked set. -/
def generatedMismatch (σ : Model) (z : Unit × FlatStack (State × Action) State) (t : ℕ) : Prop :=
  P.row (phaseCandidate (b z t) fallback (m z t)) (x z t)≠P.row σ (x z t)

/-- Nonterminal mismatch endpoints. The detecting/final transition is excluded
from this set and charged once through segmentEnds. -/
def interiorMismatchTimes (σ : Model) (z : Unit × FlatStack (State × Action) State) (T : ℕ) : Finset ℕ := by
  classical
  exact (Finset.range T).filter (fun t => t+1<T ∧ label z (t+1)=label z t ∧
    generatedMismatch P menu priority B₀ s₀ fallback fallbackAction ε σ z t)

/-- Actual global progress endpoint census, including every segment terminal
transition and each nonterminal mismatching execution exactly once. -/
def generatedChargeTimes (σ : Model) (z : Unit × FlatStack (State × Action) State) (T : ℕ) : Finset ℕ := by
  classical
  exact interiorMismatchTimes P menu priority B₀ s₀ fallback fallbackAction ε σ z T ∪ segmentEnds (label z) T

theorem interior_mismatch_postcount_lt
    (σ : Model) (η : ℝ) (N L T : ℕ) (hNL : N≤L)
    (hSep : ∀ θ∈B₀, ∀ e, P.row θ e≠P.row σ e →
      ∃ y, ε+η≤|realRows P σ e y-realRows P θ e y|)
    (z : Unit × FlatStack (State × Action) State)
    (hlo : ∀ t, t<T → (m z t).index<L)
    (hlive : ∀ t, t<T → (b z t).Nonempty)
    (hAcc : ∀ t, t<T → HistoryAccurate P σ η N (H z t))
    (t : ℕ) (ht : t∈interiorMismatchTimes P menu priority B₀ s₀ fallback fallbackAction ε σ z T) :
    countBefore π z (x z t) (t+1)<L := by
  classical
  obtain ⟨htT,htNext,hlabel,hMis⟩ := Finset.mem_filter.mp ht
  have htlt := Finset.mem_range.mp htT
  have hb : b z (t+1)=b z t := congrArg Prod.fst hlabel
  have hi : (m z (t+1)).index=(m z t).index := congrArg (fun v => v.2.1) hlabel
  have hNo := run_constant_phase_test_false P menu priority B₀ s₀ fallback fallbackAction reject z t hb hi
  have hθ : phaseCandidate (b z t) fallback (m z t)∈B₀ :=
    (liveHistory_subset P B₀ _) (cycleAction_mem (b z t) fallback (hlive t htlt) (m z t).index)
  obtain ⟨y,hy⟩ := hSep _ hθ (x z t) hMis
  exact nonrejecting_mismatch_count_lt P σ _ ε η N (m z t).index L hNL (hlo t htlt)
    (H z (t+1)) (hAcc (t+1) htNext) hNo (x z t) y hy

/-- All phase/support epochs share the same pair tape counters. The exact
nonterminal generated mismatches consume at most q(L-1) cells in total. -/
theorem generated_interior_mismatch_budget
    (σ : Model) (η : ℝ) (N L T : ℕ) (hNL : N≤L)
    (hSep : ∀ θ∈B₀, ∀ e, P.row θ e≠P.row σ e →
      ∃ y, ε+η≤|realRows P σ e y-realRows P θ e y|)
    (z : Unit × FlatStack (State × Action) State)
    (hlo : ∀ t, t<T → (m z t).index<L)
    (hlive : ∀ t, t<T → (b z t).Nonempty)
    (hAcc : ∀ t, t<T → HistoryAccurate P σ η N (H z t)) :
    (interiorMismatchTimes P menu priority B₀ s₀ fallback fallbackAction ε σ z T).card
      ≤ Fintype.card (State × Action)*(L-1) := by
  apply global_postcount_budget π z
  intro t ht
  exact interior_mismatch_postcount_lt P menu priority B₀ s₀ fallback fallbackAction ε σ η N L T hNL
    hSep z hlo hlive hAcc t ht

/-- Literal generated progress endpoint budget; no assumed segment-count or
per-phase count bound is supplied. The final transition is included, even if
its completed history first violates the accuracy guard. -/
theorem generated_global_charge_budget
    (σ : Model) (η : ℝ) (N L T : ℕ) (hNL : N≤L)
    (hSep : ∀ θ∈B₀, ∀ e, P.row θ e≠P.row σ e →
      ∃ y, ε+η≤|realRows P σ e y-realRows P θ e y|)
    (z : Unit × FlatStack (State × Action) State)
    (hlo : ∀ t, t<T → (m z t).index<L)
    (hlive : ∀ t, t<T → (b z t).Nonempty)
    (hAcc : ∀ t, t<T → HistoryAccurate P σ η N (H z t)) :
    (generatedChargeTimes P menu priority B₀ s₀ fallback fallbackAction ε σ z T).card
      ≤ Fintype.card (State × Action)*(L-1)+2*B₀.card*L := by
  classical
  unfold generatedChargeTimes
  exact Finset.card_union_le _ _ |>.trans (Nat.add_le_add
    (generated_interior_mismatch_budget P menu priority B₀ s₀ fallback fallbackAction ε σ η N L T hNL
      hSep z hlo hlive hAcc)
    (generated_segment_end_budget P menu priority B₀ s₀ fallback fallbackAction reject L T z hlo hlive))

/-- Fully source-bound accurate-prefix charge bound with the actual barrier
L=N+|B₀|, including arbitrary support resets and the final detecting action. -/
theorem accurate_generated_charge_budget
    (σ : Model) (η : ℝ) (hη : η≤ε) (N T : ℕ)
    (hs₀ : s₀∈winningRegion P menu priority B₀) (hσ : σ∈B₀)
    (hSep : ∀ θ∈B₀, ∀ e, P.row θ e≠P.row σ e →
      ∃ y, ε+η≤|realRows P σ e y-realRows P θ e y|)
    (z : Unit × FlatStack (State × Action) State)
    (hSupported : ∀ e k, 0<realRows P σ e (z.2 (e,k)))
    (hAcc : ∀ t, t<T → HistoryAccurate P σ η N (H z t)) :
    (generatedChargeTimes P menu priority B₀ s₀ fallback fallbackAction ε σ z T).card
      ≤ Fintype.card (State × Action)*(N+B₀.card-1)+2*B₀.card*(N+B₀.card) := by
  apply generated_global_charge_budget P menu priority B₀ s₀ fallback fallbackAction ε σ η N (N+B₀.card) T
    (by omega) hSep z
  · intro t ht
    exact generated_index_bounded_of_accurate P menu priority B₀ s₀ fallback fallbackAction ε η hη N t
      hs₀ σ hσ z hSupported (by intro i hi;exact hAcc i (by omega))
  · intro t ht
    exact ⟨σ,(run_invariant P menu priority B₀ s₀ fallback fallbackAction reject
      hs₀ σ hσ z hSupported t).1⟩
  · exact hAcc

end HiddenParity.Cost
