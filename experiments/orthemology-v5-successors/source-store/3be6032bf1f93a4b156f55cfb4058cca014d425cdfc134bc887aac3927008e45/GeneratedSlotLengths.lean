import ChronologicalDurations
import ActualSliceUnionBound

noncomputable section
attribute [local instance] Classical.propDecidable
open MeasureTheory
open scoped ENNReal BigOperators
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
local notation "H" => runHistory P menu priority B₀ s₀ fallback fallbackAction reject
local notation "m" => runMemory P menu priority B₀ s₀ fallback fallbackAction reject
local notation "progress" => runProgress P menu priority B₀ s₀ fallback fallbackAction reject
local notation "π" => pairPolicy s₀ (generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject)

def runSlotLength (σ : Model) (T j : ℕ) (z : Unit × FlatStack (State × Action) State) : ℕ :=
  slotLength (progress σ z) (fun t => historyDanger P menu priority B₀ s₀ fallback reject σ (H z t)) T j

def historySlotLength (σ : Model) (h : History (State × Action) State) (j : ℕ) : ℕ :=
  ((Finset.range h.length).filter (fun t =>
    historyProgressCount P menu priority B₀ s₀ fallback reject σ (h.drop (h.length-t))=j ∧
    historyDanger P menu priority B₀ s₀ fallback reject σ (h.drop (h.length-t)))).card

theorem runSlotLength_eq_history (σ : Model) (T j : ℕ) (z : Unit × FlatStack (State × Action) State) :
    runSlotLength P menu priority B₀ s₀ fallback fallbackAction ε σ T j z=
      historySlotLength P menu priority B₀ s₀ fallback ε σ (H z T) j := by
  have hl : (H z T).length=T := observedHistory_length _ _ _ _ _ _
  unfold runSlotLength slotLength historySlotLength
  rw [hl]
  congr 1
  apply Finset.filter_congr
  intro t ht
  have hd := observedHistory_drop Finset.univ π (fun _ _ => default) z.1 (fun a k => z.2 (a,k)) T t
    (Finset.mem_range.mp ht).le
  change (H z T).drop (T-t)=H z t at hd
  rw [hd,historyProgressCount_run]

theorem runSlotLength_measurable (σ : Model) (T j : ℕ) :
    Measurable (runSlotLength P menu priority B₀ s₀ fallback fallbackAction ε σ T j) := by
  have he := funext (runSlotLength_eq_history P menu priority B₀ s₀ fallback fallbackAction ε σ T j)
  rw [he]
  exact (measurable_of_countable (fun h => historySlotLength P menu priority B₀ s₀ fallback ε σ h j)).comp
    ((measurable_pi_apply T).comp (stackHistoryTrajectory_measurable π
      (pairPolicy_measurable s₀ _ (generatedPhasePolicy_measurable P menu priority B₀ s₀ fallback fallbackAction reject))))

/-- All preceding slot lengths are fixed by the next full start history. No
independence, bare row count, or future cutoff event appears in this identity. -/
theorem runSlotLength_prior_known (σ : Model) (T j i : ℕ) (hij : i < j)
    (base : History (State × Action) State) (hsT : base.length ≤ T)
    (hj : historyProgressCount P menu priority B₀ s₀ fallback reject σ base=j)
    (z : Unit × FlatStack (State × Action) State) (hbase : H z base.length=base) :
    runSlotLength P menu priority B₀ s₀ fallback fallbackAction ε σ T i z=
      historySlotLength P menu priority B₀ s₀ fallback ε σ base i := by
  have hpc : progressCount (progress σ z) base.length=j := by
    rw [← historyProgressCount_run,hbase,hj]
  have he := preceding_slotLength_eq_prefix (progress σ z)
    (fun t => historyDanger P menu priority B₀ s₀ fallback reject σ (H z t)) T j base.length i hsT hpc hij
  change runSlotLength P menu priority B₀ s₀ fallback fallbackAction ε σ T i z=
    runSlotLength P menu priority B₀ s₀ fallback fallbackAction ε σ base.length i z at he
  rw [he,runSlotLength_eq_history,hbase]

/-- Long actual slot length after a genuine start forces the already-proved
literal generated continuing event, even without any empirical accuracy guard. -/
theorem runSlotLength_long_implies_slice
    (hs₀ : s₀  ∈  winningRegion P menu priority B₀) (σ : Model) (hσ : σ  ∈  B₀)
    (T j n : ℕ) (base : History (State × Action) State)
    (hstart : historyIsStart P menu priority B₀ s₀ fallback reject σ base)
    (hj : historyProgressCount P menu priority B₀ s₀ fallback reject σ base=j)
    (z : Unit × FlatStack (State × Action) State)
    (hSupported : ∀ e k,0 < realRows P σ e (z.2 (e,k)))
    (hbase : H z base.length=base)
    (hl : n < runSlotLength P menu priority B₀ s₀ fallback fallbackAction ε σ T j z) :
    historySlice P menu priority B₀ s₀ fallback reject σ base
      (runTail P menu priority B₀ s₀ fallback fallbackAction reject z base.length n) := by
  have hs := (historyIsStart_run P menu priority B₀ s₀ fallback fallbackAction reject σ z base.length).mp
    (hbase.symm ▸ hstart)
  have hpc : progressCount (progress σ z) base.length=j := by rw [← historyProgressCount_run,hbase,hj]
  have hn := (no_progress_of_long_slot (progress σ z)
    (fun t => historyDanger P menu priority B₀ s₀ fallback reject σ (H z t)) T j base.length n hs hpc hl).2
  suffices historySlice P menu priority B₀ s₀ fallback reject σ (H z base.length)
      (runTail P menu priority B₀ s₀ fallback fallbackAction reject z base.length n) by
    simpa only [hbase] using this
  cases he : (m z base.length).retained with
  | none =>
      change (currentMemory P menu priority B₀ s₀ fallback reject (erasePairSources (H z base.length))).retained=none at he
      simpa only [historySlice,he] using run_navigation_continues P menu priority B₀ s₀ fallback fallbackAction reject
        hs₀ σ hσ z hSupported base.length n he hn
  | some E =>
      change (currentMemory P menu priority B₀ s₀ fallback reject (erasePairSources (H z base.length))).retained=some E at he
      simpa only [historySlice,he] using run_operation_continues P menu priority B₀ s₀ fallback fallbackAction reject
        hs₀ σ hσ z hSupported base.length n E he hn

end HiddenParity.Cost
