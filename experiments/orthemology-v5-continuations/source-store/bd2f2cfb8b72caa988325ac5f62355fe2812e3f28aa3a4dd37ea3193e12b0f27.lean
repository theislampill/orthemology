import ChainHellingerBudget

noncomputable section
open MeasureTheory ProbabilityTheory Filter Finset
open scoped BigOperators ENNReal
namespace Orthemology.Tranche3
open Orthemology.Tranche2
variable {Θ A Y : Type*} [Fintype Θ] [Fintype Y] [DecidableEq Θ] [DecidableEq A]
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A) (menu : Finset Θ → Finset A)

/-- Any proved uniform reset bound transfers to actual physical action cost.
This reusable transport lemma is internal to the explicit chain endpoint below. -/
theorem recursive_physical_budget_transfer
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu) (d : A) (C : ℝ)
    (hbudget : ∀ n, resetCost (recursiveFullKernel P good menu) (recursiveKeep P good menu)
      (phaseNext P good menu) (recursivePolicy P good menu)
      (fun q σ => (recursiveBadCharge P good menu θ q σ : ℝ)) θ n p [] ≤ C) :
    (∫⁻ x, ∑' t, badActionCost (good θ) (recursivePhysicalAction P good menu d x t)
      ∂recursiveRecordedLaw P good menu hP hN θ p) ≤ ENNReal.ofReal C := by
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
      exact stopped_bad_count_le_planned _ _ _) p C hbudget).1
  have hrecords : (∫⁻ x, ∑' n, (plannedBadCount (good θ) (recursiveExecuted P good menu (x n)) : ℝ≥0∞)
      ∂recursiveRecordedLaw P good menu hP hN θ p) ≤ ENNReal.ofReal C := by
    simpa only [recursiveExecuted,executedRecordBlock,plannedBadCount,List.filter_nil,List.length_nil,
      Nat.cast_zero,add_zero] using hb
  apply le_trans (lintegral_mono_ae ?_) hrecords
  filter_upwards [recursive_recorded_all_post_nonempty P good menu hP hN θ p] with x hx
  rw [recursive_physical_total_bad_eq_post_records P good menu θ d x hx]
  exact ENNReal.tsum_comp_le_tsum_of_injective (fun a b h => Nat.add_right_cancel h)
    (fun n => (plannedBadCount (good θ) (recursiveExecuted P good menu (x n)) : ℝ≥0∞))

section PhysicalLaw
variable [MeasurableSpace A] [Countable A] [MeasurableSingletonClass A]

/-- Main strengthened result: the same zero-support physical controller has
expected total actual bad actions bounded by its potential-exit-chain budget. -/
theorem recursivePhysicalLaw_total_bad_chain_budget
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu) (hθ : θ ∈ p.val) (d : A) :
    (∫⁻ x, ∑' t, badActionCost (good θ) (x t)
      ∂recursivePhysicalLaw P good menu hP hN θ p d) ≤
        ENNReal.ofReal (recursiveChainBudget P good menu hP θ p) := by
  rw [recursivePhysicalLaw,lintegral_map (total_bad_measurable (good θ))
    (recursivePhysicalAction_path_measurable P good menu d)]
  exact recursive_physical_budget_transfer P good menu hP hN θ p d _
    (recursive_resetCost_le_chainBudget P good menu hP hN θ p hθ)

/-- Every deterministic physical-time prefix obeys the chain bound. -/
theorem recursivePhysicalLaw_finite_bad_chain_budget
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu) (hθ : θ ∈ p.val) (d : A) (T : ℕ) :
    (∫⁻ x, ∑ t ∈ Finset.range T, badActionCost (good θ) (x t)
      ∂recursivePhysicalLaw P good menu hP hN θ p d) ≤
        ENNReal.ofReal (recursiveChainBudget P good menu hP θ p) := by
  exact (lintegral_mono (fun _ => ENNReal.sum_le_tsum (Finset.range T))).trans
    (recursivePhysicalLaw_total_bad_chain_budget P good menu hP hN θ p hθ d)

/-- This is a tail estimate on total error count, not on restoration time. -/
theorem recursivePhysicalLaw_chain_bad_count_tail
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu) (hθ : θ ∈ p.val) (d : A)
    (k : ℕ) (hk : 0 < k) :
    recursivePhysicalLaw P good menu hP hN θ p d
      {x | (k : ℝ≥0∞) ≤ ∑' t, badActionCost (good θ) (x t)} ≤
        ENNReal.ofReal (recursiveChainBudget P good menu hP θ p) / k := by
  exact (meas_ge_le_lintegral_div
    (μ := recursivePhysicalLaw P good menu hP hN θ p d)
    (total_bad_measurable (good θ)).aemeasurable
    (show (k : ℝ≥0∞) ≠ 0 by exact_mod_cast Nat.ne_of_gt hk) (by simp : (k : ℝ≥0∞) ≠ ⊤)).trans
    (ENNReal.div_le_div_right
      (recursivePhysicalLaw_total_bad_chain_budget P good menu hP hN θ p hθ d) _)

/-- Finite expected total physical bad count also supplies almost-sure finiteness
of that count directly in the physical sequence law. -/
theorem recursivePhysicalLaw_total_bad_finite_ae
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu) (hθ : θ ∈ p.val) (d : A) :
    ∀ᵐ x ∂recursivePhysicalLaw P good menu hP hN θ p d,
      (∑' t, badActionCost (good θ) (x t)) < ⊤ := by
  exact ae_lt_top (total_bad_measurable (good θ))
    (ne_top_of_le_ne_top ENNReal.ofReal_ne_top
      (recursivePhysicalLaw_total_bad_chain_budget P good menu hP hN θ p hθ d))
end PhysicalLaw
end Orthemology.Tranche3
