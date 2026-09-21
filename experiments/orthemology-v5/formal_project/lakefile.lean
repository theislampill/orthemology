import Lake
open Lake DSL

package orthemologyConvergence

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "c44e0c8ee63ca166450922a373c7409c5d26b00b"

@[default_target]
lean_lib OrthemologyConvergence where
  roots := #[`InternalPolymorphism, `HurkensBoundary, `FiniteBridge, `BoundaryResults, `EffectsAndDependence, `AlmostSureBoundary, `NormalisationAndNumerals, `OperationalKernel, `OperationalBoundary, `RelationalFragment, `GeneratedExamples, `AuditSupport, `CrossCheck, `Verification]
