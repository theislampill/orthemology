import IndependentBoundaries
import Lean
open Lean Elab Command
partial def reviewValueDeps (env : Environment) (n : Name) : StateM NameSet Unit := do
  if (← get).contains n then return
  modify (·.insert n)
  if let some ci := env.find? n then
    if let some v := ci.value? true then
      for dep in v.getUsedConstants do
        reviewValueDeps env dep
run_cmd do
  let env ← getEnv
  let targets := [``SeededSource.body_has, ``SeededSource.sampler_has,
    ``SeededSource.sampler_hasE, ``SeededSource.sampler_hasJ,
    ``SeededSource.sampler_observes, ``SeededSource.finite_sampler_observes,
    ``SeededSource.runSource_typed, ``SeededSource.runSource_observes]
  for target in targets do
    let (_, ax) := ((Lean.CollectAxioms.collect target).run env).run {}
    for a in ax.axioms do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains a do
        throwError "Unexpected axiom in {target}: {a}"
    let visited := (reviewValueDeps env target).run {} |>.snd
    for forbidden in [``FullPER.fundamental, ``JointCompletion.fundamental,
        ``P01AC.ExtensionalRepair.fundamental, ``P01AC.fundamental,
        ``HenkinSoundness.fundamental, ``JointCompletion.HasJ.natInduction,
        ``JointCompletion.HasJ.sigmaElim] do
      if visited.contains forbidden then
        throwError "Forbidden dependency in {target}: {forbidden}"
    logInfo m!"PASS {target} standard axioms and original-source dependency scope"
  let compiled := (reviewValueDeps env ``SeededSource.sampler_has).run {} |>.snd
  unless compiled.contains ``P01AC.BooleanPrimitive.PR.compile_has do
    throwError "Missing original PR compiler typing theorem"
  for n in env.header.moduleNames do
    let p ← findOLean n
    logInfo m!"IMPORT_OBJECT {n} {p}"
