import MomentRecovery
import Counterexample

/-! Positive controls for edge cases and the link between the concrete and generic moments. -/

noncomputable section

open scoped BigOperators

namespace FiniteMoment.Checks

example {K : Type*} [Field K] (a w : Fin 0 → K) :
    recover a (record a w) = w := by
  exact recover_record a (Function.injective_of_subsingleton a) w

example {K : Type*} [Field K] (a w : Fin 1 → K) :
    recover a (record a w) = w := by
  exact recover_record a (Function.injective_of_subsingleton a) w

example {K : Type*} [Field K] {N : ℕ} (a : Fin N → K)
    (ha : Function.Injective a) (w : Fin N → K) :
    (recordLinearEquiv a ha).symm ((recordLinearEquiv a ha) w) = w := by
  exact (recordLinearEquiv a ha).symm_apply_apply w

open FiniteMomentRecovery.FourPoint in
example (w : Fin 4 → ℝ) (r : ℕ) :
    FiniteMoment.moment x w r = FiniteMomentRecovery.FourPoint.moment w r := rfl

end FiniteMoment.Checks
