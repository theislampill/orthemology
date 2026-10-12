import SeparatingProjection
open scoped BigOperators
example {K : Type*} [Field K] [Infinite K] {N d : ℕ}
    (x : Fin N → Fin d → K) :
    ∃ v : Fin d → K, Function.Injective (fun i => ∑ j, v j * x i j) := by
  exact FiniteMoment.exists_separating_projection x
