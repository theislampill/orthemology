import EffectiveRenewalBoundary
open EffectiveRenewal EffectiveRenewal.Contract
-- A blanket every-environment claim contradicts the proved advice boundary.
example : ¬ ∃ env : Environment, (∀ n, (env n).1 = true) ∧
    Committed (controllerSnapshot copyInputObserver env) ∧
    (∀ t, diagonalTree (controllerSnapshot copyInputObserver env t)) ∧
    UnboundedOutput (controllerSnapshot copyInputObserver env) := by
  intro _
  exact some_environment_supplies_path_advice
