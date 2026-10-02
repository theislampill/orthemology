import AtomicApproximation
import TargetMassFixtures

namespace Orthemology.Frontier.MealyMeasure.Fixtures
open scoped ENNReal

example : 0 ≤ residualMassQ zeroMachine () (approximationCutoff zeroMachine () 2) ∧
    residualMassQ zeroMachine () (approximationCutoff zeroMachine () 2) < (1/4 : ℚ) := by
  simpa using approximationCutoff_spec zeroMachine () 2

example : law zeroMachine () (P02A2.positive (law zeroMachine ()) \
    partialAtomSet zeroMachine () (approximationCutoff zeroMachine () 2)) < (1/4 : ℝ≥0∞) := by
  have hpow : (1/2 : ℝ≥0∞)^2 = 1/4 := by
    rw [one_div, ← ENNReal.inv_pow]
    norm_num
  simpa only [hpow] using approximationCutoff_measure_error zeroMachine () 2

/- Supplementary runtime checks: a finite singleton support and an empty support both terminate. -/
#eval approximationCutoff zeroMachine () 2
#eval approximationCutoff copyMachine () 2

end Orthemology.Frontier.MealyMeasure.Fixtures
