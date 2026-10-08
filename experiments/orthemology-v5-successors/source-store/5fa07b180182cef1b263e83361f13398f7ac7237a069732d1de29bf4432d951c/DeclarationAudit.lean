import SignedControllerService
import Lean.Util.CollectAxioms
import Lean.Util.FoldConsts
import Lean.Compiler.ImplementedByAttr

open Lean Elab Command Meta
set_option pp.universes true
set_option pp.fullNames true
set_option pp.proofs false
set_option maxHeartbeats 0

elab "audit_all_new_declarations" : command => do
  let env ← getEnv
  let modules : List String := ["OrderedCycle", "StageFamily", "SubmittedFamily", "DirectController", "DirectMemoryTransitions", "DirectSafety", "DirectRun", "DirectDynamics", "DirectCycling", "DirectStability", "DirectParity", "DirectActualLaw", "RationalTest", "DirectEndpoint", "Refutation", "FiniteLists", "IndexedCoverage", "FiniteEnumeration", "PositiveFormula", "SignedService", "SignedControllerService"]
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  let mut unsafeCount := 0
  let mut opaqueCount := 0
  for (name, ci) in env.constants.toList do
    let some idx := env.getModuleIdxFor? name | continue
    let mod := env.header.moduleNames[idx]!
    unless modules.contains mod.toString do continue
    count := count + 1
    if ci.isUnsafe then
      unsafeCount := unsafeCount + 1
      logInfo m!"COMPILER_OR_ELABORATOR_ARTIFACT {mod} | {name}"
      continue
    let axs ← collectAxioms name
    unless axs.toList.all (allowed.contains ·) do
      throwError "NONSTANDARD_AXIOM {name}: {axs}"
    if ci matches .opaqueInfo _ then opaqueCount := opaqueCount + 1
    let ty ← liftTermElabM (Meta.ppExpr ci.type)
    logInfo m!"DECL {mod} | {name}\nTYPE {ty}\nAXIOMS {axs}\nUNSAFE {ci.isUnsafe}"
  logInfo m!"PASS all new-module declarations={count}; excluded compiler/elaborator unsafe artifacts={unsafeCount}; safe declarations={count-unsafeCount}; safe opaque={opaqueCount}; safe-declaration axioms limited to propext/Classical.choice/Quot.sound."

audit_all_new_declarations
