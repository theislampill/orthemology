import Lake
open Lake DSL
package orthemologyFrontier
require mathlib from "mathlib4"
@[default_target]
lean_lib OrthemologyFrontier where
  roots := #[`RankTransport, `LowerEnvelopeBudget, `PERRefinement, `PERPotentialFormula, `MealyRefinement, `MealySharpness, `GuardedRefinement, `BlockMismatch, `Verification]
