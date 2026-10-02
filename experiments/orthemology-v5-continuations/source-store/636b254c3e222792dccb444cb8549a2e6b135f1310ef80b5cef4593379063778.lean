import ChronologicalIntervals
import StoppingHistoryUnion

noncomputable section
attribute [local instance] Classical.propDecidable
open MeasureTheory
open scoped ENNReal Function
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
local notation "b" => runSupport P menu priority B₀ s₀ fallback fallbackAction reject
local notation "m" => runMemory P menu priority B₀ s₀ fallback fallbackAction reject
local notation "H" => runHistory P menu priority B₀ s₀ fallback fallbackAction reject
local notation "x" => runAction P menu priority B₀ s₀ fallback fallbackAction reject
local notation "label" => generatedSegmentLabel P menu priority B₀ s₀ fallback fallbackAction reject
local notation "π" => pairPolicy s₀ (generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject)

/-- Same literal source label, computed solely from the completed history. -/
def historySegmentLabel (h : History (State × Action) State) :=
  let mem := currentMemory P menu priority B₀ s₀ fallback reject (erasePairSources h)
  (liveHistory P B₀ h,mem.index,mem.retained)

theorem historySegmentLabel_run (z : Unit × FlatStack (State × Action) State) (t : ℕ) :
    historySegmentLabel P menu priority B₀ s₀ fallback reject (H z t)=label z t := rfl

/-- Actual progress is a literal segment boundary or full-row mismatch. It is
history-observable for fixed true σ, but σ is only an analysis parameter. -/
def historyProgress (σ : Model) : History (State × Action) State → Prop
  | [] => False
  | (e,y)::h =>
      historySegmentLabel P menu priority B₀ s₀ fallback reject ((e,y)::h) ≠ 
        historySegmentLabel P menu priority B₀ s₀ fallback reject h ∨
      P.row (phaseCandidate (liveHistory P B₀ h) fallback
        (currentMemory P menu priority B₀ s₀ fallback reject (erasePairSources h))) e ≠ P.row σ e

/-- State-free formulation of dangerous mode. It is constant within a literal
segment, and fully matching operation contributes no coBüchi bad pair. -/
def historyDanger (σ : Model) (h : History (State × Action) State) : Prop :=
  let mem := currentMemory P menu priority B₀ s₀ fallback reject (erasePairSources h)
  match mem.retained with
  | none => True
  | some E => ¬Match P.row (phaseCandidate (liveHistory P B₀ h) fallback mem) σ E

def runProgress (σ : Model) (z : Unit × FlatStack (State × Action) State) (t : ℕ) : Prop :=
  historyProgress P menu priority B₀ s₀ fallback reject σ (H z (t+1))

theorem runProgress_iff (σ : Model) (z : Unit × FlatStack (State × Action) State) (t : ℕ) :
    runProgress P menu priority B₀ s₀ fallback fallbackAction reject σ z t ↔
      label z (t+1) ≠ label z t ∨
      P.row (phaseCandidate (b z t) fallback (m z t)) (x z t) ≠ P.row σ (x z t) := by
  change historyProgress _ _ _ _ _ _ _ _ (stackHistoryTrajectory π z (t+1))↔_
  change historyProgress _ _ _ _ _ _ _ _ (stackHistoryTrajectory π z (t+1)) ↔
    historySegmentLabel P menu priority B₀ s₀ fallback reject (stackHistoryTrajectory π z (t+1)) ≠
      historySegmentLabel P menu priority B₀ s₀ fallback reject (stackHistoryTrajectory π z t) ∨ _
  rw [stack_history_succ]
  rfl

/-- Exact continuing segment equality across every prefix with no progress. -/
theorem run_label_eq_of_no_progress (σ : Model) (z : Unit × FlatStack (State × Action) State)
    (s n : ℕ)
    (hp : ∀ i,s ≤ i → i < s+n → ¬runProgress P menu priority B₀ s₀ fallback fallbackAction reject σ z i) :
    label z (s+n)=label z s := by
  induction n with
  | zero => simp
  | succ n ih =>
      have hi := ih (by intro i his hin;exact hp i his (by omega))
      have h := hp (s+n) (by omega) (by omega)
      rw [runProgress_iff] at h
      have he := not_or.mp h |>.1
      have he' : label z (s+n+1)=label z (s+n) := not_not.mp he
      simpa only [Nat.add_assoc] using he'.trans hi

/-- The source normalizes target entry before it next acts: a navigation action
cannot be at a stage target. -/
theorem run_navigation_avoids_target (z : Unit × FlatStack (State × Action) State) (t : ℕ)
    (hn : (m z t).retained=none) :
    (x z t).1 ∉ stageTargets P menu priority (b z t) (phaseCandidate (b z t) fallback (m z t)) := by
  let raw := phaseMemory P menu priority B₀ s₀ fallback reject (erasePairSources (H z t))
  have hm : m z t=normalizeMemory P menu priority fallback (b z t) (x z t).1 raw := by
    simp only [runMemory,currentMemory,runHistory_augment,observedState_erase,runAction_source]
    rfl
  have ha := normalizeMemory_none_avoids P menu priority fallback (b z t) (x z t).1 raw (hm ▸ hn)
  simpa only [hm,phaseCandidate,normalizeMemory_index] using ha

/-- The actual suffix history used by the conditional law. -/
def runTail (z : Unit × FlatStack (State × Action) State) (s n : ℕ) : History (State × Action) State :=
  (H z (s+n)).take n

theorem runTail_append (z : Unit × FlatStack (State × Action) State) (s n : ℕ) :
    runTail P menu priority B₀ s₀ fallback fallbackAction reject z s n++H z s=H z (s+n) := by
  have hd := observedHistory_drop Finset.univ π (fun _ _ => default) z.1 (fun a k => z.2 (a,k))
    (s+n) s (by omega)
  change (H z (s+n)).drop ((s+n)-s)=H z s at hd
  rw [show s+n-s=n by omega] at hd
  rw [← hd]
  exact List.take_append_drop n _

theorem runTail_succ (z : Unit × FlatStack (State × Action) State) (s n : ℕ) :
    runTail P menu priority B₀ s₀ fallback fallbackAction reject z s (n+1)=
      (x z (s+n),(x z (s+n+1)).1)::runTail P menu priority B₀ s₀ fallback fallbackAction reject z s n := by
  unfold runTail
  rw [show s+(n+1)=s+n+1 by omega]
  change (stackHistoryTrajectory π z (s+n+1)).take (n+1)=_
  rw [stack_history_succ,List.take_succ_cons]
  have hr := stack_pair_source_next s₀ (generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject) z (s+n)
  change (x z (s+n+1)).1=stackReceipt π z (s+n) at hr
  rw [hr]
  rfl

/-- Chronological progress index, reconstructed entirely from the finite
observed prefix; no future or cutoff-event information appears here. -/
def historyProgressCount (σ : Model) : History (State × Action) State → ℕ
  | [] => 0
  | ey::h => historyProgressCount σ h + if historyProgress P menu priority B₀ s₀ fallback reject σ (ey::h) then 1 else 0

theorem historyProgressCount_run (σ : Model) (z : Unit × FlatStack (State × Action) State) (t : ℕ) :
    historyProgressCount P menu priority B₀ s₀ fallback reject σ (H z t)=
      progressCount (runProgress P menu priority B₀ s₀ fallback fallbackAction reject σ z) t := by
  classical
  induction t with
  | zero => rfl
  | succ t ih =>
      rw [progressCount_succ]
      change historyProgressCount _ _ _ _ _ _ _ _ (stackHistoryTrajectory π z (t+1))=_
      rw [stack_history_succ,historyProgressCount]
      change historyProgressCount _ _ _ _ _ _ _ _ (H z t)+_=_
      rw [ih]
      simp only [runProgress,runHistory,stack_history_succ]

/-- A possible interval start, after the immediately preceding completed
progress transition (or at the initial empty history). -/
def historyIsStart (σ : Model) (h : History (State × Action) State) : Prop :=
  h=[] ∨ historyProgress P menu priority B₀ s₀ fallback reject σ h

theorem historyIsStart_run (σ : Model) (z : Unit × FlatStack (State × Action) State) (t : ℕ) :
    historyIsStart P menu priority B₀ s₀ fallback reject σ (H z t) ↔
      t=0 ∨ runProgress P menu priority B₀ s₀ fallback fallbackAction reject σ z (t-1) := by
  cases t with
  | zero => simp [historyIsStart,runHistory,stackHistoryTrajectory,observedHistory]
  | succ t =>
      have hn : H z (t+1) ≠ [] := by
        change stackHistoryTrajectory π z (t+1) ≠ []
        rw [stack_history_succ]
        exact List.cons_ne_nil _ _
      simp only [historyIsStart,hn,false_or,Nat.add_eq_zero,one_ne_zero,and_false,Nat.add_sub_cancel,runProgress]

/-- For a fixed chronological index, full-history start cylinders are pairwise
disjoint, even when their physical start times are unbounded. -/
theorem same_index_start_prefixes_disjoint (σ : Model) (j : ℕ) :
    Pairwise (Disjoint on (fun h : {h : History (State × Action) State |
      historyIsStart P menu priority B₀ s₀ fallback reject σ h ∧
      historyProgressCount P menu priority B₀ s₀ fallback reject σ h=j} =>
      {z : Unit × FlatStack (State × Action) State | H z h.val.length=h.val})) := by
  classical
  intro h g hne
  apply Set.disjoint_left.mpr
  intro z hh hg
  have hsh := (historyIsStart_run P menu priority B₀ s₀ fallback fallbackAction reject σ z h.val.length).mp
    (hh.symm ▸ h.property.1)
  have hsg := (historyIsStart_run P menu priority B₀ s₀ fallback fallbackAction reject σ z g.val.length).mp
    (hg.symm ▸ g.property.1)
  have hch := historyProgressCount_run P menu priority B₀ s₀ fallback fallbackAction reject σ z h.val.length
  have hcg := historyProgressCount_run P menu priority B₀ s₀ fallback fallbackAction reject σ z g.val.length
  rw [hh,h.property.2] at hch
  rw [hg,g.property.2] at hcg
  have he := start_eq_of_progressCount_eq
    (runProgress P menu priority B₀ s₀ fallback fallbackAction reject σ z)
    h.val.length g.val.length hsh hsg (hch.symm.trans hcg)
  apply hne
  apply Subtype.ext
  exact hh.symm.trans (he ▸ hg)

end HiddenParity.Cost
