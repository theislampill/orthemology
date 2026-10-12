import Mathlib.Data.Real.Basic

/-! Exact scalar type obligation at the changed cutoff-tail application.
Expected failure must be an application/type mismatch, never timeout credit. -/
example (ε η : ℝ) (hηpos : 0 < η) (hη : η ≤ ε) : η ≤ ε / 2 := by
  exact hη
