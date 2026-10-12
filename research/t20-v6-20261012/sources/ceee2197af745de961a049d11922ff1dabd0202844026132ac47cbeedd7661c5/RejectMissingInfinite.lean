import SeparatingProjection
open scoped BigOperators
example {K : Type*} [Field K] {N d : ℕ}
    (x : Fin N → Fin d → K) (hx : Function.Injective x) :
    ∃ v : Fin d → K, Function.Injective (fun i => ∑ j, v j * x i j) := by
  exact FiniteMoment.exists_separating_projection x hx
