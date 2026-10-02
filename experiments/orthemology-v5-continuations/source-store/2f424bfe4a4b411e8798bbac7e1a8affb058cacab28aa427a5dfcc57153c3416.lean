import MarkovSupportAdapter
import ControlTests

namespace HiddenParity.Controls

set_option maxRecDepth 100000
set_option maxHeartbeats 8000000

/-- Actual normalized two-outcome rows from the full-row countercontrol. -/
def exitKernel : RationalKernel Two One Two where
  row := exitRow
  nonnegative := by
    intro m e y
    fin_cases m <;> fin_cases e <;> fin_cases y <;>
      norm_num [exitRow, half_eq]
  normalized := by
    intro m e
    fin_cases m <;> fin_cases e <;>
      norm_num [exitRow, half_eq, Fin.sum_univ_two]

theorem candidate_zero_exit :
    NoExit exitKernel (Finset.univ : Finset Two) 0 (0 : One) := by decide

theorem rival_has_exit :
    ¬ NoExit exitKernel (Finset.univ : Finset Two) 1 (0 : One) := by decide

theorem exact_internal_support :
    internalSuccessors exitKernel (Finset.univ : Finset Two) (0 : One) =
      ({0} : Finset Two) := by decide

/-- The complete normalized-kernel wrapper retains precisely observed state 0. -/
theorem normalized_adapter_target :
    markovTargetStates exitKernel singleSource Finset.univ oppositePriority 0 Finset.univ =
      ({0} : Finset Two) := by decide

/-- The full-row-mismatching rival is not silently used as the true candidate. -/
theorem normalized_adapter_rival_empty :
    markovTargetStates exitKernel singleSource Finset.univ oppositePriority 1 Finset.univ =
      (∅ : Finset Two) := by decide

end HiddenParity.Controls
