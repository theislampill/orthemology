import FiniteCostCharacterization

noncomputable section
namespace HiddenParity.Cost.Controls
open HiddenParity.Cost

/-- The detecting/final transition has one endpoint even when there was no
ordinary progress. Removing it would make the zero-slot budget false. -/
theorem final_transition_is_counted :
    truncatedProgressEnds (fun _ => False) 1={0} ∧
    progressCount (fun _ => False) 1=0 := by
  norm_num [truncatedProgressEnds,progressCount,Finset.filter_insert,Finset.filter_singleton]

/-- Chronological rank preserves physical gaps; long zero-cost residence is
never collapsed into a bounded physical-time assertion. -/
theorem long_gap_keeps_offset :
    lastIntervalStart (fun _ => False) 3=0 ∧
    progressCount (fun _ => False) 3=0 := by
  norm_num [lastIntervalStart,progressCount]

/-- A completed progress transition starts a fresh interval at the next action,
without resetting the global chronological index. -/
theorem progress_advances_interval :
    lastIntervalStart (fun n => n=1) 3=2 ∧
    progressCount (fun n => n=1) 3=1 := by
  norm_num [lastIntervalStart,progressCount,Finset.range_succ,Finset.filter_insert,Finset.filter_singleton]

/-- Exact two-slot cover with a skipped initial good action. -/
theorem finite_interval_cover_control :
    ((Finset.range 4).filter (fun t => t≠0)).card ≤
      (truncatedProgressEnds (fun n => n=1) 4).card*2 := by
  norm_num [truncatedProgressEnds,Finset.range_succ,Finset.filter_insert,Finset.filter_singleton]

end HiddenParity.Cost.Controls
