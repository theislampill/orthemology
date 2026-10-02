import RecursiveHistorySafety

noncomputable section
set_option linter.unusedSectionVars false
open MeasureTheory ProbabilityTheory Filter Finset
open scoped BigOperators ENNReal
namespace Orthemology.Tranche3
open Orthemology.Tranche2
open Orthemology.Tranche2.PolicyEmbedding
universe u v
variable {Θ A Y : Type u} {R : Type v}
    [Fintype Θ] [Fintype A] [Fintype Y] [DecidableEq Θ] [DecidableEq A] [Inhabited Y]
    [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y]

/-- One shared canonical causal policy simultaneously supplies exact dynamic
licensing on every feasible consistent history, expected total bad-action control,
and almost-sure restoration in every initially live model. The existential
policy precedes the true-model quantifier. This is sufficiency, not necessity. -/
theorem recursive_certificate_canonical_policy_exists
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A) (menu : Finset Θ → Finset A)
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (B₀ : Finset Θ) (hwin : RecursiveWinning P good menu B₀)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (d : A) :
    ∃ π : R → History A Y → A,
      Measurable (fun z : R × History A Y => π z.1 z.2) ∧
      (∀ r h, ActionCompatible π r h → (historySupport P B₀ h).Nonempty →
        π r h ∈ menu (historySupport P B₀ h)) ∧
      ∀ θ ∈ B₀,
        ((∫⁻ x, ∑' t, badActionCost (good θ) (x t) ∂actionLaw π ρ (P θ) (hP θ) (hN θ) d) ≤
          ENNReal.ofReal (recursiveChainBudget P good menu hP θ ⟨B₀,hwin⟩)) ∧
        (∀ᵐ x ∂actionLaw π ρ (P θ) (hP θ) (hN θ) d, ∀ᶠ t in atTop, x t ∈ good θ) := by
  refine ⟨recursiveHistoryPolicy P good menu ⟨B₀,hwin⟩,
    recursiveHistoryPolicy_measurable P good menu ⟨B₀,hwin⟩, ?_, ?_⟩
  · exact recursiveHistoryPolicy_licensed P good menu hP ⟨B₀,hwin⟩
  · intro θ hθ
    exact ⟨recursiveHistoryPolicy_actionLaw_total_bad_budget P good menu hP hN θ ⟨B₀,hwin⟩ hθ ρ d,
      recursiveHistoryPolicy_actionLaw_eventually_good P good menu hP hN θ ⟨B₀,hwin⟩ hθ ρ d⟩

/-- The pointwise public-history licence contract remains separate from target
quality, so early target errors are still licensed. -/
theorem recursiveHistoryPolicy_canonical_bad_count_tail
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A) (menu : Finset Θ → Finset A)
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu) (hθ : θ ∈ p.val)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (d : A) (k : ℕ) (hk : 0 < k) :
    actionLaw (recursiveHistoryPolicy P good menu p) ρ (P θ) (hP θ) (hN θ) d
      {x | (k : ℝ≥0∞) ≤ ∑' t, badActionCost (good θ) (x t)} ≤
        ENNReal.ofReal (recursiveChainBudget P good menu hP θ p) / k := by
  exact (meas_ge_le_lintegral_div (μ := actionLaw (recursiveHistoryPolicy P good menu p) ρ (P θ) (hP θ) (hN θ) d)
    (total_bad_measurable (good θ)).aemeasurable
    (show (k : ℝ≥0∞) ≠ 0 by exact_mod_cast Nat.ne_of_gt hk) (by simp : (k : ℝ≥0∞) ≠ ⊤)).trans
    (ENNReal.div_le_div_right
      (recursiveHistoryPolicy_actionLaw_total_bad_budget P good menu hP hN θ p hθ ρ d) _)
end Orthemology.Tranche3
