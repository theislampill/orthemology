import CausalActionTree
import CanonicalHistoryBudget

noncomputable section
set_option linter.unusedSectionVars false
open MeasureTheory ProbabilityTheory Finset
open scoped BigOperators ENNReal
namespace Orthemology.Tranche3.CausalTree
open Orthemology.Tranche2.PolicyEmbedding CanonicalMicro
universe u v w
variable {A Y : Type u} {R : Type v} {L S : Type w}
    [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
    [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y]

/-- The action policy obtained by replaying a finite causal tree from acquired
history; node labels may carry public controller state, erased before acting. -/
def erasedHistoryPolicy (action : L → A) (spawn : S → NodeState L Y S)
    (s₀ : NodeState L Y S) (_ : R) (h : History A Y) : A :=
  action (replayObserved spawn s₀ h).1

/-- A proved stopped-block potential gives a quantitative bound directly in
the original seeded canonical actionLaw through a constructed causal policy. -/
theorem actionTreePolicy_total_cost
    (action : L → A) (spawn : S → NodeState L Y S)
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (c : A → ℝ) (hc : ∀ a, 0 ≤ c a) (F : S → ℝ) (hF : ∀ s, 0 ≤ F s)
    (I : S → Prop)
    (hvalid : ∀ q, I q → Valid (fun l => P (action l)) I (.node (spawn q).1 (spawn q).2))
    (hspawn : ∀ q, I q → nodeValue (fun l => P (action l)) (fun l => c (action l)) F (spawn q) ≤ F q)
    (q₀ : S) (hq : I q₀) (ρ : Measure R) [IsProbabilityMeasure ρ] (d : A) :
    (∫⁻ x, ∑' t, ENNReal.ofReal (c (x t))
      ∂actionLaw (erasedHistoryPolicy action spawn (spawn q₀)) ρ P hP hN d) ≤ ENNReal.ofReal (F q₀) := by
  let π : History A Y → A := fun h => action (replayObserved spawn (spawn q₀) h).1
  let val : NodeState L Y S → ℝ := nodeValue (fun l => P (action l)) (fun l => c (action l)) F
  let V : History A Y → ℝ≥0∞ := fun h => ENNReal.ofReal (val (replayObserved spawn (spawn q₀) h))
  let J : History A Y → Prop := fun h =>
    Valid (fun l => P (action l)) I (.node (replayObserved spawn (spawn q₀) h).1
      (replayObserved spawn (spawn q₀) h).2)
  have hv : ∀ s, 0 ≤ val s := fun s =>
    treeValue_nonneg _ _ _ (fun l y => hP (action l) y) (fun l => hc (action l)) hF _
  have hj : J [] := hvalid q₀ hq
  have hn : ∀ h y, J h → 0 < P (π h) y → J ((π h,y)::h) := by
    intro h y hh hy
    exact advance_valid (fun l => P (action l)) I spawn hvalid _ hh y hy
  have hs : ∀ h, J h → ENNReal.ofReal (c (π h)) +
      ∑ y, ENNReal.ofReal (P (π h) y) * V ((π h,y)::h) ≤ V h := by
    intro h hh
    let s := replayObserved spawn (spawn q₀) h
    have hb := node_step_bound (fun l => P (action l)) (fun l => c (action l)) F I spawn
      (fun l y => hP (action l) y) hspawn s hh
    have ht := ENNReal.ofReal_le_ofReal hb
    rw [ENNReal.ofReal_add (hc _) (Finset.sum_nonneg (fun y _ => mul_nonneg (hP _ _) (hv _))),
      ENNReal.ofReal_sum_of_nonneg (fun y _ => mul_nonneg (hP _ _) (hv _))] at ht
    simp_rw [ENNReal.ofReal_mul (hP _ _)] at ht
    exact ht
  have hb := canonical_total_cost_of_drift π ρ P hP hN (fun a => ENNReal.ofReal (c a)) V J hj hn hs d
  exact hb.trans (ENNReal.ofReal_le_ofReal (hspawn q₀ hq))
end Orthemology.Tranche3.CausalTree
