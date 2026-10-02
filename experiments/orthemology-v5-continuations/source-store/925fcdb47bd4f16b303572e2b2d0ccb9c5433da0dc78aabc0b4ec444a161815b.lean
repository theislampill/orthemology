import RecursiveGeneratedController
import RecordedBudgetTransfer
import StoppedRecordActions
import dependencies.PhysicalFlattening

noncomputable section
open MeasureTheory ProbabilityTheory Filter Finset
open scoped BigOperators ENNReal

namespace Orthemology.Tranche2
variable {Θ A Y : Type*} [Fintype Θ] [Fintype Y] [DecidableEq Θ] [DecidableEq A]
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A) (menu : Finset Θ → Finset A)

abbrev RecursiveRecordState := RecordedState
  (Obs := fun p σ => StopObs Y (phaseActs P good menu p σ).length)

def recursiveRecordedLaw (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu) :=
  markovTrajectory (recordedTransitionKernel (recursiveFullKernel P good menu) (recursiveKeep P good menu)
    (phaseNext P good menu) (recursivePolicy P good menu)
    (recursiveFull_nonneg P good menu hP) (recursiveFull_normalized P good menu hN) θ) (⟨p,[]⟩,none)

def recursiveExecuted (s : RecursiveRecordState P good menu) : List A :=
  executedRecordBlock (phaseActs P good menu) s

/-- Finite recursive certificates imply finitely many bad ACTUALLY EXECUTED
prefix actions, under a generated law that retains all exit observations. -/
theorem recursive_recorded_bad_eventually_zero
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu) (hθ : θ ∈ p.val) :
    ∀ᵐ x ∂recursiveRecordedLaw P good menu hP hN θ p, ∀ᶠ n in atTop,
      plannedBadCount (good θ) (recursiveExecuted P good menu (x n)) = 0 := by
  classical
  obtain ⟨C,hbudget⟩ := recursive_finite_budget P good menu hP hN θ p hθ
  apply (recorded_nat_charge_transfer (recursiveFullKernel P good menu) (recursiveKeep P good menu)
    (phaseNext P good menu) (recursivePolicy P good menu)
    (recursiveFull_nonneg P good menu hP) (recursiveFull_normalized P good menu hN) θ
    (recursiveBadCharge P good menu θ) (fun s => plannedBadCount (good θ) (recursiveExecuted P good menu s))
    ?_ p C hbudget).2
  intro s y
  have hl : recursivePolicy P good menu s.1.1 s.1.2 ∈ s.1.1.val :=
    greedyMax_live_mem _ _ _ (phaseInitial_mem P good menu s.1.1)
  change plannedBadCount (good θ)
      (stoppedActions (phaseActs P good menu s.1.1 (recursivePolicy P good menu s.1.1 s.1.2)) y) ≤ _
  rw [recursiveBadCharge, if_pos hl]
  exact stopped_bad_count_le_planned _ _ _

/-- Null placeholder records cannot stall physical time: all fresh records are
nonempty executed prefixes, so eventually every block has an action. -/
theorem recursive_recorded_eventually_nonempty
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu) :
    ∀ᵐ x ∂recursiveRecordedLaw P good menu hP hN θ p, ∀ᶠ n in atTop,
      recursiveExecuted P good menu (x n) ≠ [] := by
  classical
  let g := fun s : RecursiveRecordState P good menu => if recursiveExecuted P good menu s = [] then 1 else 0
  have hg := (recorded_nat_charge_transfer (recursiveFullKernel P good menu) (recursiveKeep P good menu)
    (phaseNext P good menu) (recursivePolicy P good menu)
    (recursiveFull_nonneg P good menu hP) (recursiveFull_normalized P good menu hN) θ
    (fun _ _ => 0) g (by
      intro s y
      have hn := executedRecordBlock_nonempty_on_update (phaseActs P good menu)
        (fun p σ => (phaseActs_spec P good menu p σ).1) (recursiveKeep P good menu)
        (phaseNext P good menu) (recursivePolicy P good menu) s y
      simp only [g, recursiveExecuted, if_neg hn, le_refl]) p 0 (by
        intro n
        simpa only [Nat.cast_zero] using (resetCost_zero (recursiveFullKernel P good menu)
          (recursiveKeep P good menu) (phaseNext P good menu) (recursivePolicy P good menu) θ n p []).le)).2
  filter_upwards [hg] with x hx
  filter_upwards [hx] with n hn
  simpa only [g, ite_eq_right_iff, one_ne_zero, imp_false] using hn

/-- The physical action stream is the concatenation of actual stopped prefixes.
No unfinished old plan is executed after a support-changing observation. -/
theorem recursive_physical_eventually_good
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu) (hθ : θ ∈ p.val) :
    ∀ᵐ x ∂recursiveRecordedLaw P good menu hP hN θ p,
      ∃ hu : PhysicalFlattening.Unbounded (fun n => recursiveExecuted P good menu (x n)),
        ∀ᶠ t in atTop, PhysicalFlattening.flatten (fun n => recursiveExecuted P good menu (x n)) hu t ∈ good θ := by
  filter_upwards [recursive_recorded_bad_eventually_zero P good menu hP hN θ p hθ,
    recursive_recorded_eventually_nonempty P good menu hP hN θ p] with x hb hn
  let blocks := fun n => recursiveExecuted P good menu (x n)
  let hu := PhysicalFlattening.unbounded_of_eventually_nonempty blocks hn
  refine ⟨hu, PhysicalFlattening.eventually_flatten_good blocks hu (fun a => a ∈ good θ) ?_⟩
  filter_upwards [hb] with n hz
  intro a ha
  have hs : (blocks n).toFinset ⊆ good θ := by
    by_contra hbad
    have hp := (plannedBadCount_pos_iff (good θ) (blocks n)).mpr hbad
    rw [hz] at hp
    exact Nat.lt_irrefl 0 hp
  exact hs (List.mem_toFinset.mpr ha)

end Orthemology.Tranche2
