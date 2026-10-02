import PhysicalCostConservation

noncomputable section
open MeasureTheory ProbabilityTheory Filter Finset
open scoped BigOperators ENNReal

namespace Orthemology.Tranche3
open Orthemology.Tranche2
open PhysicalCost
variable {Θ A Y : Type*} [Fintype Θ] [Fintype Y] [DecidableEq Θ] [DecidableEq A]
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A) (menu : Finset Θ → Finset A)

/-- Explicit inherited Hellinger constant for target-bad actual action count.
Only phases retaining the true model and positive target charge contribute. -/
def recursivePhysicalBudget (θ : Θ) (p : WinningPhase P good menu) : ℝ :=
  ((phaseRank P good menu p : ℝ) + 1) *
    ∑ q : WinningPhase P good menu, ∑ σ : Θ,
      if θ ∈ q.val ∧ 0 < recursiveBadCharge P good menu θ q σ then
        (recursiveBadCharge P good menu θ q σ : ℝ) /
          (1 - survivalAffinity (P θ) (P σ) (supportStay P q.val) (phaseActs P good menu q σ))
      else 0

/-- The explicit constant bounds every finite planning horizon. Its denominator
positivity is derived by the existing source/exit certificate theorem. -/
theorem recursive_resetCost_le_physicalBudget
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu) (hθ : θ ∈ p.val) (n : ℕ) :
    resetCost (recursiveFullKernel P good menu) (recursiveKeep P good menu)
      (phaseNext P good menu) (recursivePolicy P good menu)
      (fun q σ => (recursiveBadCharge P good menu θ q σ : ℝ)) θ n p [] ≤
        recursivePhysicalBudget P good menu θ p := by
  classical
  let cost := fun q σ => (recursiveBadCharge P good menu θ q σ : ℝ)
  have hc : ∀ q σ, 0 ≤ cost q σ := fun q σ => Nat.cast_nonneg _
  have hbad : ∀ q σ, 0 < cost q σ → σ ∈ q.val ∧ ¬ (phaseActs P good menu q σ).toFinset ⊆ good θ := by
    intro q σ hp
    dsimp [cost,recursiveBadCharge] at hp
    split_ifs at hp with hs
    · exact ⟨hs,(plannedBadCount_pos_iff _ _).mp (by exact_mod_cast hp)⟩
    · norm_num at hp
  have hb := (guarded_live_stopped_controller_budget P good (fun q => q.val) (phaseActs P good menu)
    (fun q => supportStay P q.val) (phaseInitial P good menu) (phaseNext P good menu) hP hN
    (phaseInitial_mem P good menu) (phaseActs_certificate P good menu) θ cost hc hbad (phaseRank P good menu)
    (fun q σ w hθ hw hp => (phaseNext_actual_support P good menu hP θ q σ w hθ hw hp).2.1)
    (phaseNext_rank_decreases P good menu hP θ) n p hθ).2
  simpa only [cost,recursivePhysicalBudget,Nat.cast_pos] using hb

lemma recursivePhysicalBudget_nonneg
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu) (hθ : θ ∈ p.val) :
    0 ≤ recursivePhysicalBudget P good menu θ p := by
  simpa only [resetCost] using recursive_resetCost_le_physicalBudget P good menu hP hN θ p hθ 0

/-- The recorded experiment's complete expected target-bad prefix count is
bounded by the explicit Hellinger constant, without an extra placeholder charge. -/
theorem recursive_recorded_total_bad_budget
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu) (hθ : θ ∈ p.val) :
    (∫⁻ x, ∑' n, (plannedBadCount (good θ) (recursiveExecuted P good menu (x n)) : ℝ≥0∞)
      ∂recursiveRecordedLaw P good menu hP hN θ p) ≤
        ENNReal.ofReal (recursivePhysicalBudget P good menu θ p) := by
  have hb := (recorded_nat_charge_transfer (recursiveFullKernel P good menu) (recursiveKeep P good menu)
    (phaseNext P good menu) (recursivePolicy P good menu)
    (recursiveFull_nonneg P good menu hP) (recursiveFull_normalized P good menu hN) θ
    (recursiveBadCharge P good menu θ) (fun s => plannedBadCount (good θ) (recursiveExecuted P good menu s))
    (by
      intro s y
      have hl : recursivePolicy P good menu s.1.1 s.1.2 ∈ s.1.1.val :=
        greedyMax_live_mem _ _ _ (phaseInitial_mem P good menu s.1.1)
      change plannedBadCount (good θ)
        (stoppedActions (phaseActs P good menu s.1.1 (recursivePolicy P good menu s.1.1 s.1.2)) y) ≤ _
      rw [recursiveBadCharge, if_pos hl]
      exact stopped_bad_count_le_planned _ _ _)
    p (recursivePhysicalBudget P good menu θ p)
    (recursive_resetCost_le_physicalBudget P good menu hP hN θ p hθ)).1
  simpa only [recursiveExecuted,executedRecordBlock,plannedBadCount,List.filter_nil,List.length_nil,
    Nat.cast_zero,add_zero] using hb

/-- One unit of charge per actually executed target-bad action. -/
def badActionCost (G : Finset A) (a : A) : ℝ≥0∞ := if a ∈ G then 0 else 1

lemma listCost_badActionCost (G : Finset A) (as : List A) :
    listCost (badActionCost G) as = (plannedBadCount G as : ℝ≥0∞) := by
  induction as with
  | nil => simp [listCost,plannedBadCount]
  | cons a as ih =>
    by_cases ha : a ∈ G
    · simpa [listCost,badActionCost,plannedBadCount,ha] using ih
    · simpa [listCost,badActionCost,plannedBadCount,ha,Nat.cast_add,add_comm] using congrArg (fun x : ℝ≥0∞ => 1+x) ih

omit [Fintype Θ] [Fintype Y] in
/-- Exact count conservation on every actual non-stalling recorded run. -/
theorem recursive_physical_total_bad_eq_post_records
    (θ : Θ) (d : A) (x : ℕ → RecursiveRecordState P good menu)
    (hne : ∀ n, recursiveExecuted P good menu (x (n+1)) ≠ []) :
    (∑' t, badActionCost (good θ) (recursivePhysicalAction P good menu d x t)) =
      ∑' n, (plannedBadCount (good θ) (recursiveExecuted P good menu (x (n+1))) : ℝ≥0∞) := by
  have he := decode_total_cost (badActionCost (good θ)) d
    (fun n => recursiveExecuted P good menu (x (n+1))) hne
  simpa only [recursivePhysicalAction,listCost_badActionCost] using he

/-- Hellinger cost control reaches the physical action clock, before a law
pushforward. The all-post-initial-nonempty event is proved by the controller. -/
theorem recursive_physical_total_bad_budget
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu) (hθ : θ ∈ p.val) (d : A) :
    (∫⁻ x, ∑' t, badActionCost (good θ) (recursivePhysicalAction P good menu d x t)
      ∂recursiveRecordedLaw P good menu hP hN θ p) ≤
        ENNReal.ofReal (recursivePhysicalBudget P good menu θ p) := by
  apply le_trans (lintegral_mono_ae ?_) (recursive_recorded_total_bad_budget P good menu hP hN θ p hθ)
  filter_upwards [recursive_recorded_all_post_nonempty P good menu hP hN θ p] with x hx
  rw [recursive_physical_total_bad_eq_post_records P good menu θ d x hx]
  exact ENNReal.tsum_comp_le_tsum_of_injective (fun a b h => Nat.add_right_cancel h)
    (fun n => (plannedBadCount (good θ) (recursiveExecuted P good menu (x n)) : ℝ≥0∞))

section PhysicalLaw
variable [MeasurableSpace A] [Countable A] [MeasurableSingletonClass A]

/-- The actual physical sequence law of the same recursive recorded controller.
This definition does not assert equality with the separate seeded actionLaw. -/
def recursivePhysicalLaw
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu) (d : A) : Measure (ℕ → A) :=
  (recursiveRecordedLaw P good menu hP hN θ p).map (recursivePhysicalAction P good menu d)

lemma recursivePhysicalAction_path_measurable (d : A) :
    Measurable (recursivePhysicalAction P good menu d) :=
  measurable_pi_lambda _ (recursivePhysicalAction_measurable P good menu d)

lemma total_bad_measurable (G : Finset A) :
    Measurable (fun x : ℕ → A => ∑' t, badActionCost G (x t)) :=
  Measurable.ennreal_tsum (fun t => (measurable_of_countable (badActionCost G)).comp (measurable_pi_apply t))

instance recursivePhysicalLaw_probability
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu) (d : A) :
    IsProbabilityMeasure (recursivePhysicalLaw P good menu hP hN θ p d) := by
  haveI : IsProbabilityMeasure (recursiveRecordedLaw P good menu hP hN θ p) :=
    markovTrajectory_probability _ _
  unfold recursivePhysicalLaw
  exact isProbabilityMeasure_map (recursivePhysicalAction_path_measurable P good menu d).aemeasurable

/-- End-to-end quantitative bad-action bound in the measurable physical law.
Zeros, arbitrary support menus, variable block lengths, and early interruption
are retained. No externally supplied transfer or clock hypothesis occurs. -/
theorem recursivePhysicalLaw_total_bad_budget
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu) (hθ : θ ∈ p.val) (d : A) :
    (∫⁻ x, ∑' t, badActionCost (good θ) (x t)
      ∂recursivePhysicalLaw P good menu hP hN θ p d) ≤
        ENNReal.ofReal (recursivePhysicalBudget P good menu θ p) := by
  rw [recursivePhysicalLaw,lintegral_map (total_bad_measurable (good θ))
    (recursivePhysicalAction_path_measurable P good menu d)]
  exact recursive_physical_total_bad_budget P good menu hP hN θ p hθ d

/-- Every deterministic physical horizon inherits the same bound. -/
theorem recursivePhysicalLaw_finite_bad_budget
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu) (hθ : θ ∈ p.val) (d : A) (T : ℕ) :
    (∫⁻ x, ∑ t ∈ Finset.range T, badActionCost (good θ) (x t)
      ∂recursivePhysicalLaw P good menu hP hN θ p d) ≤
        ENNReal.ofReal (recursivePhysicalBudget P good menu θ p) := by
  exact (lintegral_mono (fun _ => ENNReal.sum_le_tsum (Finset.range T))).trans
    (recursivePhysicalLaw_total_bad_budget P good menu hP hN θ p hθ d)

/-- The probability of at least k total bad physical actions is at most C/k.
This concerns the number of errors, not the time of the last error. -/
theorem recursivePhysicalLaw_bad_count_tail
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu) (hθ : θ ∈ p.val) (d : A)
    (k : ℕ) (hk : 0 < k) :
    recursivePhysicalLaw P good menu hP hN θ p d
      {x | (k : ℝ≥0∞) ≤ ∑' t, badActionCost (good θ) (x t)} ≤
        ENNReal.ofReal (recursivePhysicalBudget P good menu θ p) / k := by
  have hmark := meas_ge_le_lintegral_div (μ := recursivePhysicalLaw P good menu hP hN θ p d) (total_bad_measurable (good θ)).aemeasurable
    (show (k : ℝ≥0∞) ≠ 0 by exact_mod_cast Nat.ne_of_gt hk) (by simp : (k : ℝ≥0∞) ≠ ⊤)
  exact hmark.trans (ENNReal.div_le_div_right
    (recursivePhysicalLaw_total_bad_budget P good menu hP hN θ p hθ d) _)

end PhysicalLaw
end Orthemology.Tranche3
