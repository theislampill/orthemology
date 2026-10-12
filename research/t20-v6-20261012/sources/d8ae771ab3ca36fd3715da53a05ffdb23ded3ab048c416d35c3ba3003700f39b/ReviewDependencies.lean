import Lean
import IndependentControls
open Lean Elab Command

run_cmd do
  let env ← getEnv
  for target in [
      ``TypedStructuredObserver.body_has,
      ``TypedStructuredObserver.observe_has,
      ``TypedStructuredObserver.observe_fresh_has,
      ``TypedStructuredObserver.observe_all_has,
      ``TypedStructuredObserver.observe_specialized_has,
      ``TypedStructuredObserver.fixed_reabstract,
      ``TypedStructuredObserver.zero_source_identity,
      ``TypedStructuredObserver.one_source_identity,
      ``TypedStructuredObserver.constUpdate_has,
      ``TypedStructuredObserver.one_constant_source_identity,
      ``TypedObserverFamilyContract.fixed_result_constant,
      ``TypedObserverFamilyContract.no_zero_one_assembly,
      ``TypedObserverFamilyContract.collapsed_raw_does_not_remove_this_test,
      ``TypedObserverReview.dependent_body,
      ``TypedObserverReview.dependent_fresh,
      ``TypedObserverReview.dependent_specialize_any,
      ``TypedObserverReview.dependent_constant_one_identity,
      ``TypedObserverReview.free_cycle_fails,
      ``TypedObserverReview.bad_assembly_fails,
      ``TypedObserverReview.singleton_discriminator_survives] do
    let (_, state) := ((Lean.CollectAxioms.collect target).run env).run {}
    for ax in state.axioms do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
        throwError "Unexpected dependency {ax} in {target}"
    logInfo m!"PASS full dependency closure: {target}; axioms {state.axioms}"

  -- Inspect direct proof bodies of the entire new author namespace. Inherited
  -- structural induction lemmas necessarily mention all old grammar cases;
  -- their transitive syntactic dependency set is not a derivation-rule trace.
  let mut count := 0
  for (name, info) in env.constants.toList do
    if name.getRoot == `TypedStructuredObserver then
      if let some body := info.value? true then
        for blocked in [``P01AC.Has.rawApp, ``P01AC.Has.rawAtom,
            ``P01AC.Has.proofErase,
            ``P01AC.ExtensionalRepair.HasE.rawApp,
            ``P01AC.ExtensionalRepair.HasE.rawAtom,
            ``P01AC.ExtensionalRepair.HasE.proofErase] do
          if body.getUsedConstants.contains blocked then
            throwError "Direct Raw escape {blocked} in {name}"
        count := count + 1
  logInfo m!"PASS direct author declaration bodies: {count}; no Raw typing or erasure rules"

#check @TypedStructuredObserver.body_has
#check @TypedStructuredObserver.observe_fresh_has
#check @TypedStructuredObserver.observe_specialized_has
#check @TypedStructuredObserver.zero_source_identity
#check @TypedStructuredObserver.one_constant_source_identity
#check @TypedObserverFamilyContract.no_zero_one_assembly
