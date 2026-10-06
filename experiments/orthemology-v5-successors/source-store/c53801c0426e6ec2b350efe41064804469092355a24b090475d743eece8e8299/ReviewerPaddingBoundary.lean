import FullControllerSource
set_option autoImplicit false

namespace Orthemology.Ninth.SelectorExtraction.ReviewerPadding
open P02A2.ObserverCore P02A2.PRProgram
open Orthemology.RuntimeBridge.PhaseUpdate
open Orthemology.RuntimeBridge.PhaseUpdate.HistoryFold

/-- At the empty-history sentinel the whole fold body is skip, for every step. -/
theorem exhausted_sentinel_is_skip (step : Stmt) (σ : Store) (h : σ 1 = 1) :
    exec (foldBody step) σ = σ := by
  simp [foldBody,exec,evalExpr,h]

/-- The same fact holds throughout the entire below-four padding guard range. -/
theorem exhausted_guard_range_is_skip (step : Stmt) (σ : Store) (h : σ 1 < 4) :
    exec (foldBody step) σ = σ := by
  have hn : ¬ 4 ≤ σ 1 := Nat.not_le.mpr h
  simp [foldBody,exec,evalExpr,hn]

/-- Low source registers survive any duplicate-free collect prefix. -/
theorem component_prefix_preserves_sources
    (ps : Fin 18 → Program 20) (order : List (Fin 18))
    (hn : order.Nodup) (σ : Store) (r : ℕ) (hr : r < 21) :
    exec (collect ps (stepArgs 18) order) σ r = σ r :=
  (collect_correct ps (stepArgs 18) (step_args_fresh 18) order hn σ).1 r hr

#print axioms exhausted_sentinel_is_skip
#print axioms exhausted_guard_range_is_skip
#print axioms component_prefix_preserves_sources
end Orthemology.Ninth.SelectorExtraction.ReviewerPadding
